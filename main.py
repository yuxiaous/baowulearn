"""
宝武学习系统挂课工具 — 入口

运行方式：
    python main.py

打包方式：
    pyinstaller --onefile --windowed main.py
"""

import sys

from PySide6.QtWidgets import QApplication

import config
from api import client
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)

    _state: dict = {"main_win": None}

    def open_main_window() -> None:
        win = MainWindow()

        def _on_logout() -> None:
            client.clear_token()
            _state["main_win"] = None
            open_login_window()

        win.logout_requested.connect(_on_logout)
        win.show()
        _state["main_win"] = win

    def open_login_window() -> None:
        dlg = LoginWindow()
        dlg.login_success.connect(open_main_window)
        dlg.show()

        def _on_finished(_result: int) -> None:
            if not client.get_token():
                app.quit()

        dlg.finished.connect(_on_finished)

    # 如果 config.py 中配置了 TOKEN，直接跳过登录
    if getattr(config, "TOKEN", "").strip():
        client.set_token(config.TOKEN.strip())
        open_main_window()
    else:
        open_login_window()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
