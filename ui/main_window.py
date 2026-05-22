"""主窗口：课程列表 + 挂机队列控制。"""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from api import course as course_api
from core.queue_manager import QueueManager
from models.course import Course, HangStatus
from models.video import Video


class MainWindow(tk.Frame):
    def __init__(self, master: tk.Misc, on_logout: Callable[[], None] | None = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self._on_logout = on_logout
        self._courses: list[Course] = []

        self._queue_mgr = QueueManager(
            schedule_ui=lambda fn: self.after(0, fn),
            on_state_change=self._refresh_tree_tags,
            on_progress=self._on_hang_progress,
            on_error=self._on_hang_error,
        )

        self._build_ui()
        self._load_courses()

    # ── 构建界面 ────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # ── 顶部工具栏 ────────────────────────────────────────────────────────
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=10, pady=(8, 0))

        ttk.Button(toolbar, text="刷新列表", command=self._load_courses).pack(side="left", padx=2)
        ttk.Button(
            toolbar, text="加入队列", command=self._add_to_queue
        ).pack(side="left", padx=2)
        ttk.Button(
            toolbar, text="从队列移除", command=self._remove_from_queue
        ).pack(side="left", padx=2)
        ttk.Button(
            toolbar, text="全部停止", command=self._stop_all
        ).pack(side="left", padx=2)

        if self._on_logout:
            ttk.Button(toolbar, text="退出", command=self._on_logout).pack(
                side="right", padx=2
            )

        self._status_var = tk.StringVar(value="就绪")
        ttk.Label(toolbar, textvariable=self._status_var, foreground="gray").pack(
            side="right", padx=8
        )

        # ── 课程 Treeview ─────────────────────────────────────────────────────
        columns = ("class_name", "course_name", "status", "total", "watched")
        self._tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            selectmode="extended",
        )

        col_cfg = [
            ("class_name",   "班级",      180, "w"),
            ("course_name",  "课程名称",   280, "w"),
            ("status",       "状态",        70, "center"),
            ("total",        "总时长",       70, "center"),
            ("watched",      "已学时长",     80, "center"),
        ]
        for col_id, heading, width, anchor in col_cfg:
            self._tree.heading(col_id, text=heading)
            self._tree.column(col_id, width=width, anchor=anchor, stretch=(col_id == "course_name"))

        # 颜色标记
        self._tree.tag_configure("hanging",  foreground="#0a7a0a", font=("", 0, "bold"))
        self._tree.tag_configure("waiting",  foreground="#0055cc")
        self._tree.tag_configure("completed",foreground="gray")

        # 滚动条
        vsb = ttk.Scrollbar(self, orient="vertical",   command=self._tree.yview)
        hsb = ttk.Scrollbar(self, orient="horizontal",  command=self._tree.xview)
        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self._tree.pack(side="left",  fill="both", expand=True, padx=(10, 0), pady=6)
        vsb.pack(side="left",  fill="y", pady=6)
        hsb.pack(side="bottom", fill="x", padx=10)

    # ── 数据加载 ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _finish_info_str(course: Course) -> str:
        """将 course.finish_info 格式化为显示字符串。

        有数据时返回如 "2.5/151分钟 (100%)";
        无数据时回落到 near_learn_hours 的秒数展示。
        """
        info = course.finish_info
        if info:
            for detail in info.get("details") or []:
                unit = detail.get("attributeUnit", "")
                pct = detail.get("percentage", "")
                finish = detail.get("finishValue") or ""
                pred = detail.get("predValue") or ""
                try:
                    finish_f = float(finish)
                    return f"{finish_f:.2f}/{pred}{unit} ({pct}%)"
                except ValueError:
                    pass
        # 回落：用 near_learn_hours
        sec = course.near_learn_hours
        if sec >= 3600:
            return f"{sec / 3600:.1f}h"
        if sec >= 60:
            return f"{sec // 60}m"
        return f"{sec}s" if sec else "-"

    def _load_courses(self) -> None:
        self._status_var.set("加载中…")
        threading.Thread(target=self._fetch_courses, daemon=True).start()

    def _fetch_courses(self) -> None:
        try:
            courses = course_api.get_courses()
            self.after(0, self._populate_tree, courses)
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
        self._tree.delete(*self._tree.get_children())
        for c in courses:
            total_str = f"{c.course_hours:.1f}h"

            tag = ""
            if c.hang_status == HangStatus.HANGING:
                tag = "hanging"
            elif c.hang_status == HangStatus.WAITING:
                tag = "waiting"
            elif c.is_completed:
                tag = "completed"

            self._tree.insert(
                "",
                "end",
                iid=c.course_guid,
                values=(c.class_name, c.course_name, c.display_status, total_str, self._finish_info_str(c)),
                tags=(tag,) if tag else (),
            )

        self._status_var.set(f"共 {len(courses)} 门课程")

    # ── 按钮操作 ─────────────────────────────────────────────────────────────────

    def _selected_courses(self) -> list[Course]:
        selected_ids = self._tree.selection()
        return [c for c in self._courses if c.course_guid in selected_ids]

    def _add_to_queue(self) -> None:
        courses = self._selected_courses()
        if not courses:
            messagebox.showinfo("提示", "请先选择课程", parent=self)
            return
        for c in courses:
            if c.is_completed:
                messagebox.showwarning("提示", f"《{c.course_name}》已完成，无需挂机", parent=self)
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

    # ── 挂机回调（在主线程执行）──────────────────────────────────────────────────

    def _on_hang_progress(self, course: Course, video: Video, elapsed: int, total: int) -> None:
        """每秒刷新状态栏进度；如果 finish_info 已更新则同步刷新行内容。"""
        pct = elapsed * 100 // total if total else 0
        self._status_var.set(
            f"挂机中：{course.course_name}  [{video.index + 1}] {video.name}"
            f"  {elapsed // 60}:{elapsed % 60:02d}/{total // 60}:{total % 60:02d}"
            f"  ({pct}%)"
        )
        # 每次回调都更新行中的 已学时长 列（finish_info 变化时自动刷新）
        if self._tree.exists(course.course_guid):
            values = self._tree.item(course.course_guid, "values")
            if values:
                self._tree.set(course.course_guid, "watched", self._finish_info_str(course))

    def _on_hang_error(self, msg: str) -> None:
        messagebox.showerror("挂机错误", msg, parent=self)
        self._status_var.set("就绪")

    def _refresh_tree_tags(self) -> None:
        """刷新行标签和 已学时长 列，避免重新请求接口。队列为空时重置状态栏。"""
        for c in self._courses:
            if not self._tree.exists(c.course_guid):
                continue
            tag = ""
            if c.hang_status == HangStatus.HANGING:
                tag = "hanging"
            elif c.hang_status == HangStatus.WAITING:
                tag = "waiting"
            elif c.is_completed:
                tag = "completed"
            self._tree.item(
                c.course_guid,
                tags=(tag,) if tag else (),
            )
            self._tree.set(c.course_guid, "watched", self._finish_info_str(c))
        if not self._queue_mgr.is_running:
            self._status_var.set("就绪")
