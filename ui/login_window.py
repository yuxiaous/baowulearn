"""登录窗口（PySide6）。"""

from __future__ import annotations

import threading
from typing import Callable

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from api import auth
from core import storage


class _Scheduler(QObject):
    """将任意可调用对象调度到主线程执行（线程安全）。"""

    _call: Signal = Signal(object)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._call.connect(self._execute, Qt.QueuedConnection)

    def schedule(self, fn: Callable) -> None:
        self._call.emit(fn)

    def _execute(self, fn: Callable) -> None:
        fn()


class LoginWindow(QDialog):
    def __init__(
        self,
        on_login_success: Callable[[], None],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("宝武学习系统 — 登录")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self._on_success = on_login_success
        self._captcha_id: str = ""
        self._scheduler = _Scheduler(self)

        self._build_ui()
        self._restore_credentials()
        self._load_captcha()

        self.adjustSize()
        self.setFixedSize(self.size())

    # ── 构建界面 ────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(0)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        # 工号
        self._user_edit = QLineEdit()
        self._user_edit.setMinimumWidth(180)
        form.addRow("工号：", self._user_edit)

        # 密码
        self._pwd_edit = QLineEdit()
        self._pwd_edit.setEchoMode(QLineEdit.Password)
        form.addRow("密码：", self._pwd_edit)

        # 验证码图片行
        captcha_row = QHBoxLayout()
        self._captcha_label = QLabel("加载中…")
        self._captcha_label.setFixedWidth(120)
        self._captcha_label.setCursor(Qt.PointingHandCursor)
        self._captcha_label.mousePressEvent = lambda _: self._load_captcha()
        captcha_row.addWidget(self._captcha_label)
        refresh_btn = QPushButton("刷新")
        refresh_btn.setFixedWidth(50)
        refresh_btn.clicked.connect(self._load_captcha)
        captcha_row.addWidget(refresh_btn)
        captcha_row.addStretch()
        form.addRow("验证码：", captcha_row)

        # 验证码输入
        self._captcha_edit = QLineEdit()
        form.addRow("", self._captcha_edit)

        outer.addLayout(form)
        outer.addSpacing(14)

        # 登录按钮
        self._btn_login = QPushButton("登 录")
        self._btn_login.setDefault(True)
        self._btn_login.clicked.connect(self._on_login_click)
        outer.addWidget(self._btn_login, alignment=Qt.AlignHCenter)

        # 回车触发登录
        self._captcha_edit.returnPressed.connect(self._on_login_click)

    # ── 加载验证码 ──────────────────────────────────────────────────────────────

    def _restore_credentials(self) -> None:
        """从本地存储恢复上次登录的工号和密码。"""
        login_name, password = storage.load_credentials()
        if login_name:
            self._user_edit.setText(login_name)
        if password:
            self._pwd_edit.setText(password)

    def _load_captcha(self) -> None:
        self._captcha_label.setPixmap(QPixmap())
        self._captcha_label.setText("加载中…")
        threading.Thread(target=self._fetch_captcha, daemon=True).start()

    def _fetch_captcha(self) -> None:
        try:
            img_bytes, captcha_id = auth.get_captcha()
            self._captcha_id = captcha_id
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes)
            scaled = pixmap.scaledToWidth(120, Qt.SmoothTransformation)
            self._scheduler.schedule(lambda p=scaled: self._set_captcha_image(p))
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            self._scheduler.schedule(
                lambda m=msg: self._captcha_label.setText(f"加载失败\n{m}")
            )

    def _set_captcha_image(self, pixmap: QPixmap) -> None:
        self._captcha_label.setPixmap(pixmap)
        self._captcha_label.setText("")
        self._captcha_edit.clear()
        self._captcha_edit.setFocus()

    # ── 登录逻辑 ────────────────────────────────────────────────────────────────

    def _on_login_click(self) -> None:
        user = self._user_edit.text().strip()
        pwd = self._pwd_edit.text()
        captcha = self._captcha_edit.text().strip()

        if not user:
            QMessageBox.warning(self, "提示", "请输入工号")
            return
        if not pwd:
            QMessageBox.warning(self, "提示", "请输入密码")
            return
        if not captcha:
            QMessageBox.warning(self, "提示", "请输入验证码")
            return
        if not self._captcha_id:
            QMessageBox.warning(self, "提示", "验证码尚未加载，请稍候")
            return

        self._btn_login.setEnabled(False)
        self._btn_login.setText("登录中…")
        threading.Thread(
            target=self._do_login,
            args=(user, pwd, captcha, self._captcha_id),
            daemon=True,
        ).start()

    def _do_login(self, user: str, pwd: str, captcha: str, captcha_id: str) -> None:
        try:
            auth.login(user, pwd, captcha, captcha_id)
            self._scheduler.schedule(self._handle_login_success)
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            self._scheduler.schedule(lambda m=msg: self._handle_login_fail(m))

    def _handle_login_success(self) -> None:
        storage.save_credentials(self._user_edit.text().strip(), self._pwd_edit.text())
        self.accept()
        self._on_success()

    def _handle_login_fail(self, msg: str) -> None:
        QMessageBox.critical(self, "登录失败", msg)
        self._btn_login.setEnabled(True)
        self._btn_login.setText("登 录")
        self._load_captcha()
