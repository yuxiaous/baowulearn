"""
挂机队列状态机。

一次只运行一门课程（HeartbeatWorker），当前课程完成后自动拉取下一门。
UI 通过 enqueue/dequeue/stop_all 操作队列；
状态变化通过 Qt 信号通知主线程刷新 UI。
"""

from __future__ import annotations

from collections import deque

from PySide6.QtCore import QObject, Qt, Signal

from core.heartbeat_worker import HeartbeatWorker
from models.course import Course, HangStatus
from models.video import Video


class QueueManager(QObject):
    """
    单实例队列管理器（由 MainWindow 持有）。

    通过 Qt 信号向 UI 通知状态变化：
      state_changed          - 队列/挂机状态变化，UI 应刷新列表
      error_occurred(msg)    - 挂机出错
      videos_loaded(c, vs)   - 加载了视频列表
      video_started(c, v)    - 视频开始播放
      video_progress(c, v, e, t)   - 每秒进度更新
      video_completed(c, v)  - 视频完成

    同时实现 HeartbeatListener 协议，可直接作为监听器传入 HeartbeatWorker。
    """

    state_changed = Signal()
    error_occurred = Signal(str)
    videos_loaded = Signal(object, list)  # course, list[Video]
    video_started = Signal(object, object)  # course, video
    video_progress = Signal(object, object, int, int)  # course, video, elapsed, total
    video_completed = Signal(object, object)  # course, video

    # 内部信号：将后台线程的状态变更操作调度到主线程执行
    _dispatch = Signal(object)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._dispatch.connect(self._run_dispatch, Qt.ConnectionType.QueuedConnection)
        self._queue: deque[Course] = deque()
        self._worker: HeartbeatWorker | None = None
        self._current_course: Course | None = None

    def _run_dispatch(self, fn: object) -> None:
        fn()  # type: ignore[operator]

    def _schedule(self, fn) -> None:
        """从后台线程安全地将函数调度到主线程执行。"""
        self._dispatch.emit(fn)

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
        self.state_changed.emit()

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
        self.state_changed.emit()

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
        self.state_changed.emit()

    # ── 内部调度 ───────────────────────────────────────────────────────────────

    def _start_next(self) -> None:
        if not self._queue:
            return
        course = self._queue.popleft()
        course.hang_status = HangStatus.HANGING
        self._current_course = course
        self._worker = HeartbeatWorker(course=course, listener=self)
        self._worker.start()
        self.state_changed.emit()

    # ── HeartbeatListener 实现（均可安全地从后台线程调用）──────────────────────

    def on_course_start(self, course: Course) -> None:
        pass

    def on_videos_loaded(self, course: Course, videos: list[Video]) -> None:
        self.videos_loaded.emit(course, videos)

    def on_video_start(self, course: Course, video: Video) -> None:
        self.video_started.emit(course, video)
        self.state_changed.emit()

    def on_video_progress(self, course: Course, video: Video, elapsed: int, total: int) -> None:
        self.video_progress.emit(course, video, elapsed, total)

    def on_video_complete(self, course: Course, video: Video) -> None:
        self.video_completed.emit(course, video)
        self.state_changed.emit()

    def on_course_complete(self, course: Course) -> None:
        self._schedule(lambda: self._handle_course_complete(course))

    def on_error(self, course: Course, msg: str) -> None:
        self._schedule(lambda: self._handle_error(course, msg))

    # ── 事件处理（均在主线程执行）───────────────────────────────────────────────

    def _handle_course_complete(self, course: Course) -> None:
        course.hang_status = HangStatus.IDLE
        self._worker = None
        self._current_course = None
        self.state_changed.emit()
        self._start_next()

    def _handle_error(self, course: Course, msg: str) -> None:
        # 清空队列中所有课程
        for c in self._queue:
            c.hang_status = HangStatus.IDLE
        self._queue.clear()
        # 停止当前课程
        course.hang_status = HangStatus.IDLE
        self._worker = None
        self._current_course = None
        self.error_occurred.emit(f"挂机出错（{course.course_name}）: {msg}")
        self.state_changed.emit()
