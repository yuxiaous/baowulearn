"""
登录窗口（tkinter）。

布局：
  工号 + 密码 + 验证码图片 + 验证码输入 + 登录按钮
  
登录成功后关闭自身并调用 on_login_success(token) 回调。
"""

from __future__ import annotations

import io
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from PIL import Image, ImageTk

from api import auth
from core import storage


class LoginWindow(tk.Toplevel):
    def __init__(self, master: tk.Misc, on_login_success: Callable[[], None]):
        super().__init__(master)
        self.title("宝武学习系统 — 登录")
        self.resizable(False, False)
        self._on_success = on_login_success
        self._captcha_id: str = ""
        self._captcha_photo: ImageTk.PhotoImage | None = None

        self._build_ui()
        self._restore_credentials()
        self._load_captcha()

        # 居中显示
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    # ── 构建界面 ────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        pad = {"padx": 10, "pady": 6}

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        # 工号
        ttk.Label(frame, text="工号：").grid(row=0, column=0, sticky="e", **pad)
        self._var_user = tk.StringVar()
        ttk.Entry(frame, textvariable=self._var_user, width=22).grid(
            row=0, column=1, sticky="w", **pad
        )

        # 密码
        ttk.Label(frame, text="密码：").grid(row=1, column=0, sticky="e", **pad)
        self._var_pwd = tk.StringVar()
        ttk.Entry(frame, textvariable=self._var_pwd, show="*", width=22).grid(
            row=1, column=1, sticky="w", **pad
        )

        # 验证码图片
        ttk.Label(frame, text="验证码：").grid(row=2, column=0, sticky="e", **pad)
        captcha_frame = ttk.Frame(frame)
        captcha_frame.grid(row=2, column=1, sticky="w", **pad)

        self._captcha_label = ttk.Label(captcha_frame, text="加载中…", cursor="hand2")
        self._captcha_label.pack(side="left", padx=(0, 6))
        self._captcha_label.bind("<Button-1>", lambda _: self._load_captcha())

        ttk.Button(captcha_frame, text="刷新", command=self._load_captcha, width=5).pack(
            side="left"
        )

        # 验证码输入
        ttk.Label(frame, text="").grid(row=3, column=0)  # spacer
        self._var_captcha = tk.StringVar()
        self._captcha_entry = ttk.Entry(
            frame, textvariable=self._var_captcha, width=22
        )
        self._captcha_entry.grid(row=3, column=1, sticky="w", **pad)

        # 登录按钮
        self._btn_login = ttk.Button(frame, text="登 录", command=self._on_login_click)
        self._btn_login.grid(row=4, column=0, columnspan=2, pady=14)

        # 回车触发登录
        self.bind("<Return>", lambda _: self._on_login_click())

    # ── 加载验证码 ──────────────────────────────────────────────────────────────

    def _restore_credentials(self) -> None:
        """从本地存储恢复上次登录的工号和密码。"""
        login_name, password = storage.load_credentials()
        if login_name:
            self._var_user.set(login_name)
        if password:
            self._var_pwd.set(password)

    def _load_captcha(self) -> None:
        self._captcha_label.config(text="加载中…", image="")
        threading.Thread(target=self._fetch_captcha, daemon=True).start()

    def _fetch_captcha(self) -> None:
        try:
            img_bytes, captcha_id = auth.get_captcha()
            self._captcha_id = captcha_id
            img = Image.open(io.BytesIO(img_bytes))
            # 固定宽度，保持比例
            target_w = 120
            ratio = target_w / img.width
            img = img.resize((target_w, max(1, int(img.height * ratio))), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            # 必须在主线程更新 UI
            self.after(0, self._set_captcha_image, photo)
        except Exception as exc:  # noqa: BLE001
            self.after(0, lambda: self._captcha_label.config(text=f"加载失败\n{exc}", image=""))

    def _set_captcha_image(self, photo: ImageTk.PhotoImage) -> None:
        self._captcha_photo = photo  # 防止被 GC
        self._captcha_label.config(image=photo, text="")
        self._var_captcha.set("")
        self._captcha_entry.focus_set()

    # ── 登录逻辑 ────────────────────────────────────────────────────────────────

    def _on_login_click(self) -> None:
        user = self._var_user.get().strip()
        pwd = self._var_pwd.get()
        captcha = self._var_captcha.get().strip()

        if not user:
            messagebox.showwarning("提示", "请输入工号", parent=self)
            return
        if not pwd:
            messagebox.showwarning("提示", "请输入密码", parent=self)
            return
        if not captcha:
            messagebox.showwarning("提示", "请输入验证码", parent=self)
            return
        if not self._captcha_id:
            messagebox.showwarning("提示", "验证码尚未加载，请稍候", parent=self)
            return

        self._btn_login.config(state="disabled", text="登录中…")
        threading.Thread(
            target=self._do_login, args=(user, pwd, captcha, self._captcha_id), daemon=True
        ).start()

    def _do_login(self, user: str, pwd: str, captcha: str, captcha_id: str) -> None:
        try:
            auth.login(user, pwd, captcha, captcha_id)
            self.after(0, self._handle_login_success)
        except Exception as exc:  # noqa: BLE001
            self.after(0, self._handle_login_fail, str(exc))

    def _handle_login_success(self) -> None:
        storage.save_credentials(self._var_user.get().strip(), self._var_pwd.get())
        self.destroy()
        self._on_success()

    def _handle_login_fail(self, msg: str) -> None:
        messagebox.showerror("登录失败", msg, parent=self)
        self._btn_login.config(state="normal", text="登 录")
        # 验证码错误时自动刷新
        self._load_captcha()
