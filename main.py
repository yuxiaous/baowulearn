"""
宝武学习系统挂课工具 — 入口

运行方式：
    python main.py

打包方式：
    pyinstaller --onefile --windowed main.py
"""

import tkinter as tk

from api import client
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main() -> None:
    root = tk.Tk()
    root.withdraw()  # 先隐藏根窗口，由子窗口负责显示

    def open_main_window(token: str) -> None:
        root.title("宝武学习系统 — 挂课工具")
        root.geometry("780x500")
        root.minsize(620, 380)

        def on_logout() -> None:
            client.clear_token()
            # 销毁主窗口内容，重新打开登录窗口
            for widget in root.winfo_children():
                widget.destroy()
            root.withdraw()
            open_login()

        MainWindow(root, on_logout=on_logout)
        root.deiconify()

    def open_login() -> None:
        def on_close() -> None:
            if not client.get_token():
                root.quit()

        login_win = LoginWindow(root, on_login_success=open_main_window)
        login_win.protocol("WM_DELETE_WINDOW", lambda: (login_win.destroy(), on_close()))

    open_login()
    root.mainloop()


if __name__ == "__main__":
    main()
