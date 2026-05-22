"""
心跳工作线程。

负责观看一门课程的全部视频：
  1. initLearnRecord（课程级，调用一次）
  2. 对每个视频：
       start_video
       → 每 60 秒 send_heartbeat
       → 在 mark_points 时刻 mark_progress
       → 视频结束：final send_heartbeat + complete_video + end_video
  3. 所有视频完成后触发 on_course_complete

支持随时调用 stop() 停止（发完当前心跳后退出）。
"""

from __future__ import annotations

import threading
import time
import uuid
from typing import Callable

from api import video as video_api
from models.course import Course
from models.video import Video


class HeartbeatWorker:
    """后台线程，顺序完成一门课程的所有视频。"""

    def __init__(
        self,
        course: Course,
        on_video_start: Callable[[Course, Video], None],
        on_progress: Callable[[Course, Video, int, int], None],
        on_video_complete: Callable[[Course, Video], None],
        on_course_complete: Callable[[Course], None],
        on_error: Callable[[Course, str], None],
    ):
        self._course = course
        self._on_video_start = on_video_start
        self._on_progress = on_progress
        self._on_video_complete = on_video_complete
        self._on_course_complete = on_course_complete
        self._on_error = on_error

        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True, name=f"HBW-{course.course_no}")

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        """请求停止；当前心跳周期结束后退出。"""
        self._stop_event.set()

    def is_alive(self) -> bool:
        return self._thread.is_alive()

    # ── 主循环 ────────────────────────────────────────────────────────────────

    def _run(self) -> None:
        course = self._course
        try:
            videos = video_api.get_course_videos(course.course_no, course.center_code)
            if not videos:
                self._on_error(course, "课程没有可用视频")
                return

            page_id = str(uuid.uuid4())
            video_api.init_learn_record(course.course_no, course.class_guid, page_id)

            for video in videos:
                if self._stop_event.is_set():
                    break
                self._watch_video(video, page_id)

        except Exception as exc:  # noqa: BLE001
            self._on_error(course, str(exc))
            return

        if not self._stop_event.is_set():
            self._on_course_complete(course)

    # ── 单视频观看流程 ─────────────────────────────────────────────────────────

    def _watch_video(self, video: Video, page_id: str) -> None:
        course = self._course

        # ── 查询已播放进度，决定续播起点 ──────────────────────────────────────
        start_secs = video_api.get_play_progress(course, video)

        # 已到达或超过视频末尾 → 该视频已完成，跳过
        if start_secs >= video.duration:
            self._on_video_complete(course, video)
            return

        self._on_video_start(course, video)

        # 开始播放信号（videoBeginTime = 续播位置）
        self._try_call(video_api.start_video, course, video, start_secs)

        elapsed = start_secs
        last_heartbeat = start_secs
        # 跳过已经经过的 mark_points
        marks = video.mark_points  # 已按秒排好序
        next_mark_idx = next(
            (i for i, t in enumerate(marks) if t > start_secs),
            len(marks),
        )

        while elapsed < video.duration:
            if self._stop_event.is_set():
                # 停止前补发一次心跳，记录已观看时长
                delta = elapsed - last_heartbeat
                if delta > 0:
                    self._try_call(video_api.send_heartbeat, course, video, page_id, elapsed, delta)
                return

            time.sleep(1)
            elapsed += 1

            # 进度打卡：命中 mark_points 时发送
            while next_mark_idx < len(marks) and marks[next_mark_idx] <= elapsed:
                self._try_call(video_api.mark_progress, course, video, page_id, marks[next_mark_idx])
                next_mark_idx += 1

            # 每 60 秒发一次心跳
            if elapsed - last_heartbeat >= 60:
                self._try_call(
                    video_api.send_heartbeat,
                    course, video, page_id, elapsed, elapsed - last_heartbeat,
                )
                last_heartbeat = elapsed
                self._refresh_finish_info()

            # 通知 UI 更新进度（每秒）
            self._on_progress(course, video, elapsed, video.duration)

        # ── 视频结束收尾 ───────────────────────────────────────────────────────

        # 最后一次心跳（剩余秒数）
        remaining = video.duration - last_heartbeat
        if remaining > 0:
            self._try_call(
                video_api.send_heartbeat,
                course, video, page_id, video.duration, remaining,
            )

        # 完成信号
        self._try_call(video_api.complete_video, course.class_guid, course.course_no)

        # 结束播放信号
        self._try_call(video_api.end_video, course, video, video.duration)

        # 视频完成后刷新一次完成情况
        self._refresh_finish_info()

        self._on_video_complete(course, video)

    # ── 容错调用 ──────────────────────────────────────────────────────────────

    def _refresh_finish_info(self) -> None:
        """调用 finishInfo 接口，将结果存入 course.finish_info（后台线程调用）。"""
        try:
            info = video_api.get_finish_info(self._course)
            if info is not None:
                self._course.finish_info = info
        except Exception:  # noqa: BLE001
            pass

    def _try_call(self, fn: Callable, *args, retries: int = 3) -> None:
        """调用 API，失败时重试，最终失败则记录日志继续运行（不中断挂机）。"""
        last_exc: Exception | None = None
        for attempt in range(retries):
            try:
                fn(*args)
                return
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt < retries - 1:
                    time.sleep(3)
        # 全部重试失败：打印到 stderr，不中断流程
        import sys
        print(f"[HeartbeatWorker] API 调用失败（已重试 {retries} 次）: {last_exc}", file=sys.stderr)
