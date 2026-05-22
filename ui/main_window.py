"""
主窗口：课程列表 + 挂机队列控制。

当前阶段：仅展示课程列表（只读）。
挂机/心跳功能留待后续阶段实现，预留了按钮位置。
"""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from api import course as course_api
from models.course import Course, HangStatus


class MainWindow(tk.Frame):
    def __init__(self, master: tk.Misc, on_logout: Callable[[], None] | None = None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self._on_logout = on_logout
        self._courses: list[Course] = []

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

    # ── 数据加载 ────────────────────────────────────────────────────────────────

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
            watched_sec = c.near_learn_hours
            if watched_sec >= 3600:
                watched_str = f"{watched_sec/3600:.1f}h"
            elif watched_sec >= 60:
                watched_str = f"{watched_sec//60}m"
            else:
                watched_str = f"{watched_sec}s" if watched_sec else "-"

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
                values=(c.class_name, c.course_name, c.display_status, total_str, watched_str),
                tags=(tag,) if tag else (),
            )

        self._status_var.set(f"共 {len(courses)} 门课程")

    # ── 按钮操作（占位，挂机逻辑待 Phase 3 实现）────────────────────────────────

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
            if c.hang_status == HangStatus.IDLE:
                c.hang_status = HangStatus.WAITING
        self._refresh_tree_tags()
        # TODO Phase 3: 通知 queue_manager

    def _remove_from_queue(self) -> None:
        courses = self._selected_courses()
        if not courses:
            messagebox.showinfo("提示", "请先选择课程", parent=self)
            return
        for c in courses:
            if c.hang_status in (HangStatus.WAITING, HangStatus.HANGING):
                c.hang_status = HangStatus.IDLE
        self._refresh_tree_tags()
        # TODO Phase 3: 通知 queue_manager

    def _stop_all(self) -> None:
        for c in self._courses:
            c.hang_status = HangStatus.IDLE
        self._refresh_tree_tags()
        # TODO Phase 3: 停止心跳线程

    def _refresh_tree_tags(self) -> None:
        """仅刷新行标签和状态列，避免重新请求接口。"""
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
            # 刷新状态列
            values = self._tree.item(c.course_guid, "values")
            self._tree.item(
                c.course_guid,
                values=(values[0], values[1], c.display_status, values[3], values[4]),
            )
