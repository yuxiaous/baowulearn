"""主窗口：课程列表 + 挂机队列控制。"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from api import course as course_api
from api import video as video_api
from core.queue_manager import QueueManager
from models.course import Course, HangStatus
from models.olclass import OLClass
from models.video import Video


class _AutoScrollbar(ttk.Scrollbar):
    """Scrollbar that hides itself when all content fits on screen."""

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        super().set(lo, hi)


class MainWindow(tk.Frame):
    def __init__(self, master: tk.Misc, on_logout: Callable[[], None] | None = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self._on_logout = on_logout
        self._courses: list[Course] = []
        self._fetch_gen: int = 0  # 每次刷新递增，用于取消旧的 finishInfo 批量拉取
        self._tab_data: list[dict] = []  # [{"label": str, "class_no": str|None}, ...]
        self._current_tab: int = 0
        self._current_video: Video | None = None  # 当前正在播放的视频

        self._queue_mgr = QueueManager(
            schedule_ui=lambda fn: self.after(0, fn),
            on_state_change=self._refresh_tree_tags,
            on_progress=self._on_hang_progress,
            on_error=self._on_hang_error,
            on_video_start=self._on_video_start,
            on_video_complete=self._on_video_complete,
            on_videos_loaded=self._on_videos_loaded,
        )

        self._build_ui()
        self._load_tabs()

    # ── 构建界面 ────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # ── 顶部工具栏 ────────────────────────────────────────────────────────
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=10, pady=(8, 0))

        ttk.Button(toolbar, text="刷新列表", command=self._load_courses).pack(
            side="left", padx=2
        )
        ttk.Button(toolbar, text="加入队列", command=self._add_to_queue).pack(
            side="left", padx=2
        )
        ttk.Button(toolbar, text="从队列移除", command=self._remove_from_queue).pack(
            side="left", padx=2
        )
        ttk.Button(toolbar, text="全部停止", command=self._stop_all).pack(
            side="left", padx=2
        )

        if self._on_logout:
            ttk.Button(toolbar, text="退出", command=self._logout).pack(
                side="right", padx=2
            )

        # ── 底部状态栏（必须在 Treeview 之前 pack，才能占据底部整行）────────────
        self._status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(
            self,
            textvariable=self._status_var,
            foreground="gray",
            anchor="w",
            relief="sunken",
            padding=(6, 2),
        )
        status_bar.pack(side="bottom", fill="x")

        # ── 主内容区域（三列可拖拽分隔）────────────────────────────────────────
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True, padx=10, pady=(4, 0))

        # ── 左侧专区 ────────────────────────────────────────────────────────
        olclass_outer = ttk.Frame(paned, width=150)

        self._olclass_listbox = tk.Listbox(
            olclass_outer,
            selectmode="single",
            activestyle="none",
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
            font=("", 9),
            cursor="hand2",
        )
        self._olclass_listbox.pack(fill="both", expand=True, pady=(6, 4))
        self._olclass_listbox.bind("<<ListboxSelect>>", self._on_tab_select)

        paned.add(olclass_outer, weight=0)

        # ── 中间课程 ─────────────────────────────────────────────────
        course_frame = ttk.Frame(paned)

        course_columns = ("name", "status", "total", "watched", "score")
        self._course_tree = ttk.Treeview(
            course_frame,
            columns=course_columns,
            show="headings",
            selectmode="extended",
        )

        col_cfg = [
            ("name", "课程名称", 280, "w"),
            ("status", "状态", 70, "center"),
            ("total", "学时", 60, "center"),
            ("watched", "已学时长", 140, "center"),
            ("score", "课程成绩", 80, "center"),
        ]
        for col_id, heading, width, anchor in col_cfg:
            self._course_tree.heading(col_id, text=heading)
            self._course_tree.column(
                col_id, width=width, anchor=anchor, stretch=(col_id == "name")
            )

        # 颜色标记
        self._course_tree.tag_configure("hanging", foreground="#0a7a0a")
        self._course_tree.tag_configure("waiting", foreground="#0055cc")
        self._course_tree.tag_configure("completed", foreground="gray")

        # 滚动条（auto-hide，使用 grid 布局）
        vsb = _AutoScrollbar(course_frame, orient="vertical", command=self._course_tree.yview)
        hsb = _AutoScrollbar(course_frame, orient="horizontal", command=self._course_tree.xview)
        self._course_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        course_frame.columnconfigure(0, weight=1)
        course_frame.rowconfigure(0, weight=1)
        self._course_tree.grid(row=0, column=0, sticky="nsew", pady=6)
        vsb.grid(row=0, column=1, sticky="ns", pady=6)
        hsb.grid(row=1, column=0, sticky="ew")

        paned.add(course_frame, weight=1)

        # ── 右侧视频 ──────────────────────────────────────────────────────
        video_outer = ttk.Frame(paned, width=280)

        # ttk.Label(video_outer, text="视频列表", foreground="gray", font=("", 8)).pack(
        #     anchor="w", pady=(4, 2), padx=4
        # )

        video_frame = ttk.Frame(video_outer)
        video_frame.pack(fill="both", expand=True)

        video_columns = ("vname", "vprogress")
        self._video_tree = ttk.Treeview(
            video_frame,
            columns=video_columns,
            show="headings",
            selectmode="none",
        )
        self._video_tree.heading("vname", text="视频名称")
        self._video_tree.heading("vprogress", text="进度")
        self._video_tree.column("vname", width=170, anchor="w", stretch=True)
        self._video_tree.column("vprogress", width=90, anchor="center", stretch=False)

        self._video_tree.tag_configure("playing", foreground="#0a7a0a")

        vvsb = _AutoScrollbar(video_frame, orient="vertical", command=self._video_tree.yview)
        self._video_tree.configure(yscrollcommand=vvsb.set)

        video_frame.columnconfigure(0, weight=1)
        video_frame.rowconfigure(0, weight=1)
        self._video_tree.grid(row=0, column=0, sticky="nsew", pady=6)
        vvsb.grid(row=0, column=1, sticky="ns", pady=6)

        paned.add(video_outer, weight=0)

    # ── 数据加载 ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _is_duration_completed(course: Course) -> bool:
        """基于已学时长判断是否完成。有 finishInfo 时用它，否则回退到服务端 learnStatus。"""
        info = course.finish_info
        if info:
            for detail in info.get("details") or []:
                try:
                    pred_f = float(detail.get("predValue") or "0")
                    if pred_f <= 0:
                        continue
                    return float(detail.get("finishValue") or "0") >= pred_f
                except ValueError:
                    continue
        return course.is_completed

    @staticmethod
    def _status_str(course: Course) -> str:
        """状态列显示文字：以学时完成情况为准。"""
        if course.hang_status == HangStatus.HANGING:
            return "挂机中"
        if course.hang_status == HangStatus.WAITING:
            return "等待中"
        return "已完成" if MainWindow._is_duration_completed(course) else "未完成"

    @staticmethod
    def _score_str(course: Course) -> str:
        """从 finish_info 取课程成绩（learnScore）。"""
        info = course.finish_info
        if info:
            score = info.get("learnScore") or ""
            try:
                return f"{float(score):.2f}"
            except ValueError:
                pass
        return "-"

    @staticmethod
    def _finish_info_str(course: Course) -> str:
        """将 course.finish_info 格式化为显示字符串。

        直接反映服务端返回的数据，如 "2.5/151分钟 (100%)";
        """
        info = course.finish_info
        if info:
            for detail in info.get("details") or []:
                unit = detail.get("attributeUnit", "")
                finish = detail.get("finishValue") or ""
                pred = detail.get("predValue") or ""
                try:
                    finish_f = float(finish)
                    return f"{finish_f:.2f}/{pred}{unit}"
                except ValueError:
                    pass

    def _load_tabs(self) -> None:
        """初始化标签页：先放公开课，再异步追加有效期内的专区。"""
        self._tab_data = [{"label": "公开课", "class_no": None}]
        self._olclass_listbox.delete(0, "end")
        self._olclass_listbox.insert("end", "公开课")
        self._olclass_listbox.selection_set(0)
        self._current_tab = 0
        self._load_courses()
        threading.Thread(target=self._fetch_tabs, daemon=True).start()

    def _fetch_tabs(self) -> None:
        """后台拉取专区列表，追加到标签栏。"""
        try:
            classes = course_api.get_my_classes()
            self.after(0, self._add_class_tabs, classes)
        except Exception:  # noqa: BLE001
            pass

    def _add_class_tabs(self, classes: list[OLClass]) -> None:
        """将有效专区追加到标签页列表。"""
        for c in classes:
            self._tab_data.append({"label": c.class_name, "class_no": c.class_no})
            self._olclass_listbox.insert("end", c.class_name)

    def _on_tab_select(self, _event=None) -> None:
        """切换标签页时重新加载对应课程列表。"""
        sel = self._olclass_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx == self._current_tab:
            return
        self._current_tab = idx
        self._load_courses()

    def _load_courses(self) -> None:
        self._fetch_gen += 1
        self._status_var.set("加载中…")
        threading.Thread(target=self._fetch_courses, daemon=True).start()

    def _fetch_courses(self) -> None:
        gen = self._fetch_gen
        tab = (
            self._tab_data[self._current_tab] if self._tab_data else {"class_no": None}
        )
        class_no = tab.get("class_no")

        try:
            if class_no is None:
                courses = course_api.get_openclass_courses()
            else:
                courses = course_api.get_onlineclass_courses(class_no)

            self.after(0, self._populate_tree, courses)

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
                        c = future.result()
                        self.after(0, self._update_finish_info_cell, c)
                    except Exception:  # noqa: BLE001
                        pass
        except Exception as exc:  # noqa: BLE001
            self.after(0, lambda: self._status_var.set(f"加载失败: {exc}"))

    def _populate_tree(self, courses: list[Course]) -> None:
        # 保留现有的挂机状态
        hang_map: dict[str, HangStatus] = {
            c.course_guid: c.hang_status for c in self._courses
        }
        for c in courses:
            c.hang_status = hang_map.get(c.course_guid, HangStatus.IDLE)

        self._courses = courses

        # 清空并重填 Treeview
        self._course_tree.delete(*self._course_tree.get_children())
        for c in courses:
            total_str = f"{c.course_hours:.1f}"

            tag = ""
            if c.hang_status == HangStatus.HANGING:
                tag = "hanging"
            elif c.hang_status == HangStatus.WAITING:
                tag = "waiting"
            elif self._is_duration_completed(c):
                tag = "completed"

            self._course_tree.insert(
                "",
                "end",
                iid=c.course_guid,
                values=(
                    c.course_name,
                    self._status_str(c),
                    total_str,
                    self._finish_info_str(c),
                    self._score_str(c),
                ),
                tags=(tag,) if tag else (),
            )

        self._status_var.set(f"共 {len(courses)} 门课程")

    # ── 按钮操作 ─────────────────────────────────────────────────────────────────

    def _selected_courses(self) -> list[Course]:
        selected_ids = self._course_tree.selection()
        return [c for c in self._courses if c.course_guid in selected_ids]

    def _add_to_queue(self) -> None:
        courses = self._selected_courses()
        if not courses:
            messagebox.showinfo("提示", "请先选择课程", parent=self)
            return
        for c in courses:
            if self._is_duration_completed(c):
                messagebox.showwarning(
                    "提示", f"《{c.course_name}》已完成，无需挂机", parent=self
                )
                continue
            self._queue_mgr.enqueue(c)

    def _remove_from_queue(self) -> None:
        courses = self._selected_courses()
        if not courses:
            messagebox.showinfo("提示", "请先选择课程", parent=self)
            return
        for c in courses:
            self._queue_mgr.dequeue(c)

    def _stop_all(self) -> None:
        self._queue_mgr.stop_all()

    def _logout(self) -> None:
        """先停止全部挂机任务，再执行退出回调，避免后台线程访问已销毁的窗口。"""
        self._queue_mgr.stop_all()
        if self._on_logout:
            self._on_logout()

    # ── 挂机回调（在主线程执行）──────────────────────────────────────────────────

    def _on_hang_progress(
        self, course: Course, video: Video, elapsed: int, total: int
    ) -> None:
        """每秒刷新状态栏进度；如果 finish_info 已更新则同步刷新行内容。"""
        pct = elapsed * 100 // total if total else 0
        self._status_var.set(
            f"挂机中：{course.course_name}  [{video.index + 1}] {video.name}"
            f"  {elapsed // 60}:{elapsed % 60:02d}/{total // 60}:{total % 60:02d}"
            f"  ({pct}%)"
        )
        self._update_finish_info_cell(course)
        # 更新视频树中正在播放视频的进度
        self._update_video_progress(video, elapsed, total)

    def _on_hang_error(self, msg: str) -> None:
        messagebox.showerror("挂机错误", msg, parent=self)
        self._status_var.set("就绪")

    def _update_finish_info_cell(self, course: Course) -> None:
        """更新指定行的状态、已学时长和课程成绩列（主线程调用）。"""
        try:
            if self._course_tree.exists(course.course_guid):
                self._course_tree.set(course.course_guid, "status", self._status_str(course))
                self._course_tree.set(
                    course.course_guid, "watched", self._finish_info_str(course)
                )
                self._course_tree.set(course.course_guid, "score", self._score_str(course))
                # 同步更新行颜色标签
                if course.hang_status == HangStatus.HANGING:
                    tag = "hanging"
                elif course.hang_status == HangStatus.WAITING:
                    tag = "waiting"
                elif self._is_duration_completed(course):
                    tag = "completed"
                else:
                    tag = ""
                self._course_tree.item(course.course_guid, tags=(tag,) if tag else ())
        except Exception:  # noqa: BLE001
            pass  # 窗口已销毁，忽略

    def _refresh_tree_tags(self) -> None:
        """刷新行标签和 已学时长 列，避免重新请求接口。队列为空时重置状态栏。"""
        for c in self._courses:
            if not self._course_tree.exists(c.course_guid):
                continue
            tag = ""
            if c.hang_status == HangStatus.HANGING:
                tag = "hanging"
            elif c.hang_status == HangStatus.WAITING:
                tag = "waiting"
            elif self._is_duration_completed(c):
                tag = "completed"
            self._course_tree.item(
                c.course_guid,
                tags=(tag,) if tag else (),
            )
            self._course_tree.set(c.course_guid, "status", self._status_str(c))
            self._update_finish_info_cell(c)
        if not self._queue_mgr.is_running:
            self._status_var.set("就绪")

    # ── 视频列表回调（在主线程执行）──────────────────────────────────────────────

    @staticmethod
    def _fmt_duration(secs: int) -> str:
        return f"{secs // 60}:{secs % 60:02d}"

    def _on_videos_loaded(self, course: Course, videos: list[Video]) -> None:
        """挂机开始时收到视频列表，填充右侧视频树。"""
        self._video_tree.delete(*self._video_tree.get_children())
        self._current_video = None
        for v in videos:
            elapsed_str = self._fmt_duration(v.play_progress)
            total_str = self._fmt_duration(v.duration)
            self._video_tree.insert(
                "",
                "end",
                iid=v.video_guid,
                values=(v.video_name, f"{elapsed_str} / {total_str}"),
            )

    def _on_video_start(self, course: Course, video: Video) -> None:
        """视频开始播放时标记为绿色，取消上一个视频的标记。"""
        if self._current_video and self._video_tree.exists(self._current_video.video_guid):
            self._video_tree.item(self._current_video.video_guid, tags=())
        self._current_video = video
        if self._video_tree.exists(video.video_guid):
            self._video_tree.item(video.video_guid, tags=("playing",))
            self._video_tree.see(video.video_guid)

    def _on_video_complete(self, course: Course, video: Video) -> None:
        """视频完成后取消绿色标记，更新进度为满。"""
        if self._video_tree.exists(video.video_guid):
            total_str = self._fmt_duration(video.duration)
            self._video_tree.item(video.video_guid, tags=())
            self._video_tree.set(
                video.video_guid, "vprogress", f"{total_str} / {total_str}"
            )
        if self._current_video is video:
            self._current_video = None

    def _update_video_progress(self, video: Video, elapsed: int, total: int) -> None:
        """每秒更新视频树中当前视频的进度列。"""
        try:
            if self._video_tree.exists(video.video_guid):
                elapsed_str = self._fmt_duration(elapsed)
                total_str = self._fmt_duration(total)
                self._video_tree.set(
                    video.video_guid, "vprogress", f"{elapsed_str} / {total_str}"
                )
        except Exception:  # noqa: BLE001
            pass
