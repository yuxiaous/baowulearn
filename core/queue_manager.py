"""
挂机队列状态机。

一次只运行一门课程（HeartbeatWorker），当前课程完成后自动拉取下一门。
UI 通过 enqueue/dequeue/stop_all 操作队列；
状态变化通过 _schedule(fn) 回调到主线程后由 MainWindow 刷新 UI。
"""

from __future__ import annotations

from collections import deque
from typing import Callable

from core.heartbeat_worker import HeartbeatWorker
from models.course import Course, HangStatus
from models.video import Video


class QueueManager:
    """
    单实例队列管理器（由 MainWindow 持有）。

    schedule_ui(fn)   - 将 fn 投递到 tkinter 主线程执行，
                        通常为 lambda fn: root.after(0, fn)
    on_state_change() - 队列/状态变化后通知 UI 刷新列表
    on_progress(course, video, elapsed, total) - 每秒通知 UI 更新进度标签
    """

    def __init__(
        self,
        schedule_ui: Callable[[Callable], None],
        on_state_change: Callable[[], None],
        on_progress: Callable[[Course, Video, int, int], None],
        on_error: Callable[[str], None],
    ):
        self._queue: deque[Course] = deque()
        self._worker: HeartbeatWorker | None = None
        self._current_course: Course | None = None

        self._schedule = schedule_ui
        self._on_state_change = on_state_change
        self._on_progress = on_progress
        self._on_error = on_error

    # ── 公共接口 ───────────────────────────────────────────────────────────────

    @property
    def is_running(self) -> bool:
        return self._worker is not None and self._worker.is_alive()

    def enqueue(self, course: Course) -> None:
        """将课程加入队列（如当前空闲则立即启动）。"""
        if course.hang_status != HangStatus.IDLE:
            return  # 已在队列中
        course.hang_status = HangStatus.WAITING
        self._queue.append(course)
        if not self.is_running:
            self._start_next()
        self._schedule(self._on_state_change)

    def dequeue(self, course: Course) -> None:
        """从队列移除（若正在挂机则先停止）。"""
        if course is self._current_course and self._worker:
            self._worker.stop()
            self._worker = None
            self._current_course = None
            course.hang_status = HangStatus.IDLE
            # 停止后启动队列中下一个
            self._start_next()
        elif course in self._queue:
            self._queue.remove(course)
            course.hang_status = HangStatus.IDLE
        self._schedule(self._on_state_change)

    def stop_all(self) -> None:
        """停止所有挂机，清空队列。"""
        if self._worker:
            self._worker.stop()
            self._worker = None
        if self._current_course:
            self._current_course.hang_status = HangStatus.IDLE
            self._current_course = None
        for c in self._queue:
            c.hang_status = HangStatus.IDLE
        self._queue.clear()
        self._schedule(self._on_state_change)

    # ── 内部调度 ───────────────────────────────────────────────────────────────

    def _start_next(self) -> None:
        if not self._queue:
            return
        course = self._queue.popleft()
        course.hang_status = HangStatus.HANGING
        self._current_course = course

        worker = HeartbeatWorker(
            course=course,
            on_video_start=lambda c, v: self._schedule(lambda: self._on_video_start(c, v)),
            on_progress=lambda c, v, e, t: self._schedule(lambda: self._on_progress(c, v, e, t)),
            on_video_complete=lambda c, v: self._schedule(lambda: self._on_video_complete(c, v)),
            on_course_complete=lambda c: self._schedule(lambda: self._on_course_complete(c)),
            on_error=lambda c, msg: self._schedule(lambda: self._on_error_cb(c, msg)),
        )
        self._worker = worker
        worker.start()
        self._schedule(self._on_state_change)

    # ── 事件处理（均在主线程执行）───────────────────────────────────────────────

    def _on_video_start(self, course: Course, video: Video) -> None:
        self._on_state_change()

    def _on_video_complete(self, course: Course, video: Video) -> None:
        self._on_state_change()

    def _on_course_complete(self, course: Course) -> None:
        course.hang_status = HangStatus.IDLE
        self._worker = None
        self._current_course = None
        self._on_state_change()
        self._start_next()

    def _on_error_cb(self, course: Course, msg: str) -> None:
        course.hang_status = HangStatus.IDLE
        self._worker = None
        self._current_course = None
        self._on_error(f"挂机出错（{course.course_name}）: {msg}")
        self._on_state_change()
        self._start_next()
