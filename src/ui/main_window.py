"""主窗口：课程列表 + 挂机队列控制。"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStatusBar,
    QTreeWidget,
    QTreeWidgetItem,
    QListWidget,
    QVBoxLayout,
    QWidget,
)

from api import course as course_api
from core.queue_manager import QueueManager
from models.course import Course, HangStatus
from models.zone import Zone
from models.video import Video
import config

_COLOR_HANGING = QColor("#0a7a0a")
_COLOR_WAITING = QColor("#0055cc")
_COLOR_COMPLETED = QColor("gray")


class MainWindow(QMainWindow):
    """退出登录时发出 logout_requested 信号。"""

    logout_requested = Signal()

    # 后台线程向主线程传递数据的内部信号
    _tabs_fetched = Signal(list)  # list[Zone]
    _courses_page = Signal(int, list, int, bool)  # gen, courses, total, is_last
    _finish_info_cell = Signal(int, object)  # gen, course
    _fetch_error = Signal(int, str)  # gen, message

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"宝武学习系统 V{config.VERSION}")
        self.setWindowIcon(QIcon(str(config.ASSETS_DIR / "favicon.ico")))
        self.resize(1136, 640)
        self.setMinimumSize(620, 380)

        self._courses: list[Course] = []
        self._fetch_gen: int = 0  # 每次刷新递增，用于取消旧的 finishInfo 批量拉取
        self._tab_data: list[dict] = []  # [{"label": str, "zone": Zone|None}, ...]
        self._current_tab: int = 0
        self._current_video: Video | None = None  # 当前正在播放的视频
        self._course_items: dict[tuple[str, str], QTreeWidgetItem] = {}
        self._video_items: dict[str, QTreeWidgetItem] = {}

        self._queue_mgr = QueueManager(self)
        self._queue_mgr.state_changed.connect(self._refresh_tree_tags)
        self._queue_mgr.video_progress.connect(self._on_hang_progress)
        self._queue_mgr.error_occurred.connect(self._on_hang_error)
        self._queue_mgr.video_started.connect(self._on_video_start)
        self._queue_mgr.video_completed.connect(self._on_video_complete)
        self._queue_mgr.videos_loaded.connect(self._on_videos_loaded)

        # 连接内部信号
        self._tabs_fetched.connect(self._add_zone_tabs)
        self._courses_page.connect(self._on_courses_page)
        self._finish_info_cell.connect(self._on_finish_info_cell)
        self._fetch_error.connect(self._on_fetch_error)

        self._build_ui()
        self._load_tabs()

    # ── 构建界面 ────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 8, 10, 0)
        layout.setSpacing(4)

        # ── 顶部工具栏 ────────────────────────────────────────────────────────
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(4)

        btn_refresh = QPushButton("刷新列表")
        btn_refresh.clicked.connect(self._load_courses)
        toolbar_layout.addWidget(btn_refresh)

        btn_add = QPushButton("加入队列")
        btn_add.clicked.connect(self._add_to_queue)
        toolbar_layout.addWidget(btn_add)

        btn_remove = QPushButton("移出队列")
        btn_remove.clicked.connect(self._remove_from_queue)
        toolbar_layout.addWidget(btn_remove)

        btn_stop = QPushButton("全部停止")
        btn_stop.clicked.connect(self._stop_all)
        toolbar_layout.addWidget(btn_stop)

        toolbar_layout.addStretch()

        btn_logout = QPushButton("退出")
        btn_logout.clicked.connect(self._logout)
        toolbar_layout.addWidget(btn_logout)

        layout.addLayout(toolbar_layout)

        # ── 状态栏 ────────────────────────────────────────────────────────────
        self._status_bar = QStatusBar()
        self._status_bar.setSizeGripEnabled(False)
        self.setStatusBar(self._status_bar)
        self._status_bar.showMessage("就绪")

        # ── 主内容区域（三列可拖拽分隔）────────────────────────────────────────
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter, stretch=1)

        # ── 左侧专区列表 ────────────────────────────────────────────────────────
        self._zone_listbox = QListWidget()
        self._zone_listbox.setMaximumWidth(280)
        self._zone_listbox.setMinimumWidth(60)
        self._zone_listbox.currentRowChanged.connect(self._on_tab_select)
        splitter.addWidget(self._zone_listbox)

        # ── 中间课程树 ─────────────────────────────────────────────────
        self._course_tree = QTreeWidget()
        self._course_tree.setColumnCount(6)
        self._course_tree.setHeaderLabels(["序号", "课程名称", "学时", "课程成绩", "已学时长", "状态"])
        self._course_tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._course_tree.setRootIsDecorated(False)

        ch = self._course_tree.header()
        ch.setStretchLastSection(False)
        ch.setSectionResizeMode(0, ch.ResizeMode.Fixed)
        ch.setSectionResizeMode(1, ch.ResizeMode.Stretch)
        ch.setSectionResizeMode(2, ch.ResizeMode.Fixed)
        ch.setSectionResizeMode(3, ch.ResizeMode.Fixed)
        ch.setSectionResizeMode(4, ch.ResizeMode.Fixed)
        ch.setSectionResizeMode(5, ch.ResizeMode.Fixed)
        self._course_tree.setColumnWidth(0, 40)
        self._course_tree.setColumnWidth(2, 60)
        self._course_tree.setColumnWidth(3, 80)
        self._course_tree.setColumnWidth(4, 140)
        self._course_tree.setColumnWidth(5, 70)

        splitter.addWidget(self._course_tree)

        # ── 右侧视频树 ──────────────────────────────────────────────────────
        self._video_tree = QTreeWidget()
        self._video_tree.setColumnCount(2)
        self._video_tree.setHeaderLabels(["视频名称", "进度"])
        self._video_tree.setSelectionMode(QAbstractItemView.NoSelection)
        self._video_tree.setRootIsDecorated(False)
        self._video_tree.setMaximumWidth(300)
        self._video_tree.setMinimumWidth(80)

        vh = self._video_tree.header()
        vh.setStretchLastSection(False)
        vh.setSectionResizeMode(0, vh.ResizeMode.Stretch)
        vh.setSectionResizeMode(1, vh.ResizeMode.Fixed)
        self._video_tree.setColumnWidth(1, 90)

        splitter.addWidget(self._video_tree)
        splitter.setSizes([280, 700, 300])

    # ── 数据加载 ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _course_status_str(course: Course) -> str:
        """状态列显示文字。"""
        return course.display_status

    @staticmethod
    def _course_score_str(course: Course) -> str:
        """从 course_score 取课程成绩。"""
        if course.course_score:
            return f"{course.course_score:.2f}"
        return "-"

    @staticmethod
    def _course_finish_str(course: Course) -> str:
        """将课程已学时长格式化为显示字符串。"""
        if course.course_duration > 0:
            return f"{course.course_finished:.2f}/{course.course_duration:.2f}分钟"
        return "-"

    @staticmethod
    def _course_hours_str(course: Course) -> str:
        """将课程学时格式化为显示字符串。"""
        if course.course_hours > 0:
            return f"{course.course_hours:.1f}"
        return "-"

    @staticmethod
    def _item_color(course: Course) -> QColor | None:
        if course.hang_status == HangStatus.HANGING:
            return _COLOR_HANGING
        if course.hang_status == HangStatus.WAITING:
            return _COLOR_WAITING
        if course.is_completed:
            return _COLOR_COMPLETED
        return None

    @staticmethod
    def _set_item_color(item: QTreeWidgetItem, color: QColor | None, col_count: int) -> None:
        for i in range(col_count):
            if color is not None:
                item.setForeground(i, QBrush(color))
            else:
                item.setData(i, Qt.ForegroundRole, None)

    def _load_tabs(self) -> None:
        """初始化标签页：先放公开课，再异步追加有效期内的专区。"""
        self._tab_data = [{"label": "公开课", "zone": None}]
        self._zone_listbox.blockSignals(True)
        self._zone_listbox.clear()
        self._zone_listbox.addItem("公开课")
        self._zone_listbox.setCurrentRow(0)
        self._zone_listbox.blockSignals(False)
        self._current_tab = 0
        self._load_courses()
        threading.Thread(target=self._fetch_tabs, daemon=True).start()

    def _fetch_tabs(self) -> None:
        """后台拉取专区列表，追加到标签栏。"""
        try:
            zones = course_api.get_zone_list()
            self._tabs_fetched.emit(zones)
        except Exception:  # noqa: BLE001
            pass

    def _add_zone_tabs(self, zones: list[Zone]) -> None:
        """将有效专区追加到标签页列表。"""
        for z in zones:
            self._tab_data.append({"label": z.class_name, "zone": z})
            self._zone_listbox.addItem(z.class_name)

    def _on_tab_select(self, idx: int) -> None:
        """切换标签页时重新加载对应课程列表。"""
        if idx < 0 or idx >= len(self._tab_data) or idx == self._current_tab:
            return
        self._current_tab = idx
        self._load_courses()

    def _load_courses(self) -> None:
        self._fetch_gen += 1
        self._status_bar.showMessage("加载中…")
        threading.Thread(target=self._fetch_courses, daemon=True).start()

    def _fetch_courses(self) -> None:
        gen = self._fetch_gen
        zone = self._tab_data[self._current_tab]["zone"] if self._tab_data else None

        try:
            if zone is None:

                def _fetch_page(p: int) -> tuple[list[Course], int, int]:
                    return course_api.get_open_courses(page=p)

            else:

                def _fetch_page(p: int) -> tuple[list[Course], int, int]:
                    return course_api.get_zone_courses(zone, page=p)

            all_courses: list[Course] = []
            page = 1
            total_pages = 1
            while page <= total_pages:
                if self._fetch_gen != gen:
                    return
                courses, total_courses, total_pages = _fetch_page(page)
                all_courses.extend(courses)
                courses = all_courses
                is_last = page >= total_pages
                self._courses_page.emit(gen, list(all_courses), total_courses, is_last)
                page += 1

            # 并发拉取每门课的完成情况（最多 8 个并发请求）
            def _fetch_one(c: Course) -> Course:
                if self._fetch_gen != gen:
                    return c
                course_api.get_course_finish_info(c)
                return c

            with ThreadPoolExecutor(max_workers=8) as pool:
                futures = {pool.submit(_fetch_one, c): c for c in courses}
                for future in as_completed(futures):
                    if self._fetch_gen != gen:
                        break
                    try:
                        course = future.result()
                        self._finish_info_cell.emit(gen, course)
                    except Exception as exc:  # noqa: BLE001
                        print("[Error] Fetching course finish info:", exc)
        except Exception as exc:  # noqa: BLE001
            print("[Error] Fetching courses:", exc)
            self._fetch_error.emit(gen, str(exc))

    def _populate_tree(self, courses: list[Course]) -> None:
        # 保留现有的挂机状态
        hang_map: dict[tuple[str, str], HangStatus] = {(c.course_no, c.class_no): c.hang_status for c in self._courses}
        for c in courses:
            c.hang_status = hang_map.get((c.course_no, c.class_no), HangStatus.IDLE)

        self._courses = courses
        self._course_tree.clear()
        self._course_items.clear()

        for idx, c in enumerate(courses, 1):
            item = QTreeWidgetItem(
                [
                    str(idx),
                    c.course_name,
                    self._course_hours_str(c),
                    self._course_score_str(c),
                    self._course_finish_str(c),
                    self._course_status_str(c),
                ]
            )
            for col in range(6):
                item.setTextAlignment(col, Qt.AlignCenter)
            item.setTextAlignment(1, Qt.AlignLeft | Qt.AlignVCenter)
            self._set_item_color(item, self._item_color(c), 6)
            self._course_tree.addTopLevelItem(item)
            self._course_items[(c.course_no, c.class_no)] = item

        self._status_bar.showMessage(f"共 {len(courses)} 门课程")

    def _on_courses_page(self, gen: int, courses: list[Course], total_count: int, is_last: bool) -> None:
        """接收分页课程数据（主线程槽）。"""
        if gen != self._fetch_gen:
            return
        self._populate_tree(courses)
        if not is_last:
            self._status_bar.showMessage(f"加载中… {len(courses)}/{total_count} 门课程")

    def _on_finish_info_cell(self, gen: int, course: Course) -> None:
        """接收单门课程的完成情况更新（主线程槽）。"""
        if gen != self._fetch_gen:
            return
        self._update_finish_info_cell(course)

    def _on_fetch_error(self, gen: int, msg: str) -> None:
        """接收课程加载错误（主线程槽）。"""
        if gen != self._fetch_gen:
            return
        self._status_bar.showMessage(f"加载失败: {msg}")

    # ── 按钮操作 ─────────────────────────────────────────────────────────────────

    def _selected_courses(self) -> list[Course]:
        selected_items = set(self._course_tree.selectedItems())
        return [c for c in self._courses if self._course_items.get((c.course_no, c.class_no)) in selected_items]

    def _add_to_queue(self) -> None:
        courses = self._selected_courses()
        if not courses:
            QMessageBox.information(self, "提示", "请先选择课程")
            return
        for c in courses:
            already_done = c.course_finished >= c.course_duration if c.course_duration > 0 else c.is_completed
            if already_done:
                QMessageBox.warning(self, "提示", f"《{c.course_name}》已完成，无需挂机")
                continue
            self._queue_mgr.enqueue(c)

    def _remove_from_queue(self) -> None:
        courses = self._selected_courses()
        if not courses:
            QMessageBox.information(self, "提示", "请先选择课程")
            return
        for c in courses:
            self._queue_mgr.dequeue(c)

    def _stop_all(self) -> None:
        self._queue_mgr.stop_all()

    def _logout(self) -> None:
        """先停止全部挂机任务，再发出退出信号。"""
        self._queue_mgr.stop_all()
        self.logout_requested.emit()

    # ── 挂机回调（在主线程执行）──────────────────────────────────────────────────

    def _on_hang_progress(self, course: Course, video: Video, elapsed: int, total: int) -> None:
        """每秒刷新状态栏进度；同步刷新行内容。"""
        pct = elapsed * 100 // total if total else 0
        self._status_bar.showMessage(
            f"挂机中：{course.course_name}  [{video.index + 1}] {video.video_name}"
            f"  {elapsed // 60}:{elapsed % 60:02d}/{total // 60}:{total % 60:02d}"
            f"  ({pct}%)"
        )
        self._update_finish_info_cell(course)
        # 更新视频树中正在播放视频的进度
        self._update_video_progress(video, elapsed, total)

    def _on_hang_error(self, msg: str) -> None:
        QMessageBox.critical(self, "错误", msg)
        self._status_bar.showMessage("就绪")

    def _update_finish_info_cell(self, course: Course) -> None:
        """更新指定行的课程成绩、已学时长和状态列（主线程调用）。"""
        item = self._course_items.get((course.course_no, course.class_no))
        if item is None:
            return
        try:
            item.setText(3, self._course_score_str(course))
            item.setText(4, self._course_finish_str(course))
            item.setText(5, self._course_status_str(course))
            self._set_item_color(item, self._item_color(course), 6)
        except Exception:  # noqa: BLE001
            pass  # 窗口已销毁，忽略

    def _refresh_tree_tags(self) -> None:
        """刷新行颜色和 已学时长 列，避免重新请求接口。队列为空时重置状态栏。"""
        for c in self._courses:
            item = self._course_items.get((c.course_no, c.class_no))
            if item is None:
                continue
            self._set_item_color(item, self._item_color(c), 6)
            item.setText(5, self._course_status_str(c))
            self._update_finish_info_cell(c)
        if not self._queue_mgr.is_running:
            self._status_bar.showMessage("就绪")

    # ── 视频列表回调（在主线程执行）──────────────────────────────────────────────

    @staticmethod
    def _fmt_duration(secs: int) -> str:
        return f"{secs // 60}:{secs % 60:02d}"

    def _on_videos_loaded(self, course: Course, videos: list[Video]) -> None:
        """挂机开始时收到视频列表，填充右侧视频树。"""
        self._video_tree.clear()
        self._video_items.clear()
        self._current_video = None
        for v in videos:
            elapsed_str = self._fmt_duration(v.play_progress)
            total_str = self._fmt_duration(v.duration)
            item = QTreeWidgetItem([v.video_name, f"{elapsed_str} / {total_str}"])
            item.setTextAlignment(1, Qt.AlignCenter)
            self._video_tree.addTopLevelItem(item)
            self._video_items[v.video_guid] = item

    def _on_video_start(self, course: Course, video: Video) -> None:
        """视频开始播放时标记为绿色，取消上一个视频的标记。"""
        if self._current_video:
            prev = self._video_items.get(self._current_video.video_guid)
            if prev:
                self._set_item_color(prev, None, 2)
        self._current_video = video
        item = self._video_items.get(video.video_guid)
        if item:
            self._set_item_color(item, _COLOR_HANGING, 2)
            self._video_tree.scrollToItem(item)

    def _on_video_complete(self, course: Course, video: Video) -> None:
        """视频完成后取消绿色标记，更新进度为满。"""
        item = self._video_items.get(video.video_guid)
        if item:
            total_str = self._fmt_duration(video.duration)
            item.setText(1, f"{total_str} / {total_str}")
            self._set_item_color(item, None, 2)
        if self._current_video is video:
            self._current_video = None

    def _update_video_progress(self, video: Video, elapsed: int, total: int) -> None:
        """每秒更新视频树中当前视频的进度列。"""
        try:
            item = self._video_items.get(video.video_guid)
            if item:
                elapsed_str = self._fmt_duration(elapsed)
                total_str = self._fmt_duration(total)
                item.setText(1, f"{elapsed_str} / {total_str}")
        except Exception:  # noqa: BLE001
            pass
