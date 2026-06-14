"""
心跳工作线程。

负责观看一门课程的全部视频：
  1. initLearnRecord（课程级，调用一次）
  2. 对每个视频： _watch_video
       start_video_event
       → 每 60 秒 send_heartbeat
       → 在 mark_points 时刻 send_mark_progress
       → 视频结束：final send_heartbeat + compute_video_finish + end_video_event
  3. 所有视频完成后触发 on_course_complete

支持随时调用 stop() 停止（发完当前心跳后退出）。
"""

from __future__ import annotations

import sys
import math
import threading
import time
import uuid
from typing import Callable, Protocol

from api import video as video_api
from api import course as course_api
from models.course import Course
from models.video import Video


class HeartbeatListener(Protocol):
    """HeartbeatWorker 的事件监听接口。实现此协议的对象可作为 listener 传入。"""

    def on_course_start(self, course: Course) -> None: ...
    def on_videos_loaded(self, course: Course, videos: list[Video]) -> None: ...
    def on_video_start(self, course: Course, video: Video) -> None: ...
    def on_video_progress(self, course: Course, video: Video, elapsed: int, total: int) -> None: ...
    def on_video_complete(self, course: Course, video: Video) -> None: ...
    def on_course_complete(self, course: Course) -> None: ...
    def on_error(self, course: Course, msg: str) -> None: ...


class HeartbeatWorker:
    """后台线程，顺序完成一门课程的所有视频。"""

    def __init__(self, course: Course, listener: HeartbeatListener) -> None:
        self._course = course
        self._listener = listener

        self._page_id = str(uuid.uuid4())
        self._heartbeat_interval = 60  # 秒，默认心跳间隔（实际以服务端返回为准）
        self._refresh_interval = 60 * 4  # 秒，_refresh_finish_info 调用间隔

        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
            name=f"HBW-{course.course_no}",
        )

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

        self._listener.on_course_start(course)

        try:
            videos = video_api.get_course_videos(course)
            if not videos:
                self._listener.on_error(course, "课程没有可用视频")
                return

            self._listener.on_videos_loaded(course, videos)

            self._heartbeat_interval = video_api.get_heartbeat_interval()

            video_api.init_learn_record(course, self._page_id)

            for video in videos:
                if self._stop_event.is_set():
                    break

                # 轮到该视频时才查询播放进度，并立即更新界面显示
                start_secs = video_api.get_playback_progress(video)
                self._listener.on_video_progress(course, video, start_secs, video.duration)

                # 已到达或超过视频末尾 → 该视频已完成，跳过
                if start_secs >= video.duration:
                    continue

                # 当前视频已完成，跳过
                if video.learned_status == "1":
                    continue

                self._watch_video(video, start_secs)

                # 每个视频结束后间隔几秒再继续下一个，避免请求过快
                time.sleep(3)

        except Exception as exc:  # noqa: BLE001
            self._listener.on_error(course, str(exc))
            return

        if not self._stop_event.is_set():
            if course.zone:
                course_api.compute_zone_finish(course.zone)
            self._listener.on_course_complete(course)

    # ── 单视频观看流程 ─────────────────────────────────────────────────────────

    def _watch_video(self, video: Video, start_secs: int) -> None:
        course = self._course

        self._listener.on_video_start(course, video)

        # 开始播放信号
        self._try_call(video_api.start_video_event, course, video, start_secs)

        elapsed = start_secs
        last_heartbeat = start_secs
        last_refresh = start_secs

        # 跳过已经经过的 mark_points
        marks = video.mark_points  # 已按秒排好序
        next_mark_idx = len(marks)
        for i, t in enumerate(marks):
            if t > start_secs:
                next_mark_idx = i
                break

        while elapsed < video.duration:
            if self._stop_event.is_set():
                # 停止前补发一次心跳，记录已观看时长
                delta = elapsed - last_heartbeat
                if delta > 0:
                    self._try_call(video_api.send_heartbeat, course, video, self._page_id, elapsed, delta)
                return

            time.sleep(1)
            elapsed += 1

            # 进度打卡：命中 mark_points 时发送
            while next_mark_idx < len(marks) and marks[next_mark_idx] <= elapsed:
                self._try_call(video_api.send_mark_progress, course, video, self._page_id, marks[next_mark_idx])
                next_mark_idx += 1

            # 每 60 秒发一次心跳，然后触发服务端重算完成情况``
            delta = elapsed - last_heartbeat
            if delta >= self._heartbeat_interval:
                self._try_call(video_api.send_heartbeat, course, video, self._page_id, elapsed, delta)
                last_heartbeat = elapsed

            # 每 3 分钟刷新一次完成情况
            if elapsed - last_refresh >= self._refresh_interval:
                self._try_call(self._refresh_finish_info)
                last_refresh = elapsed

            # 通知 UI 更新进度（每秒）
            self._listener.on_video_progress(course, video, elapsed, video.duration)

        # ── 视频结束收尾 ───────────────────────────────────────────────────────

        # 最后一次心跳：等待到心跳间隔的整数倍后再发送
        remaining = video.duration - last_heartbeat
        if remaining > 0:
            learn_time = math.ceil(remaining / self._heartbeat_interval) * self._heartbeat_interval
            wait_secs = learn_time - remaining
            for _ in range(wait_secs):
                if self._stop_event.is_set():
                    break
                time.sleep(1)
            self._try_call(video_api.send_heartbeat, course, video, self._page_id, video.duration, learn_time)
            # video_api.send_heartbeat(course, video, self._page_id, video.duration, remaining)

        # 完成信号
        self._try_call(video_api.compute_video_finish, course, video)

        # 结束播放信号
        self._try_call(video_api.end_video_event, course, video, video.duration)

        # 视频完成后刷新一次完成情况
        self._try_call(self._refresh_finish_info)

        self._listener.on_video_complete(course, video)

    def _refresh_finish_info(self) -> None:
        """触发服务端重算。"""
        course_api.compute_course_finish(self._course)
        course_api.get_course_finish_info(self._course)

    def _try_call(self, fn: Callable, *args, retries: int = 3) -> None:
        """调用 API 失败时重试，最多重试 retries 次。"""
        last_exc: Exception | None = None
        for attempt in range(retries):
            try:
                fn(*args)
                return
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                print(f"[Error] API 调用失败（第 {attempt + 1} 次）: {last_exc}", file=sys.stderr)
                if attempt < retries - 1:
                    time.sleep(3)
        raise last_exc
