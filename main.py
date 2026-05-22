"""
宝武学习系统挂课工具 — 入口

运行方式：
    python main.py

打包方式：
    pyinstaller --onefile --windowed main.py
"""

import sys
import tkinter as tk

from api import client
from ui.login_window import LoginWindow


def main() -> None:
    root = tk.Tk()
    root.withdraw()  # 先隐藏主窗口，等登录成功后再展示

    def on_login_success(token: str) -> None:
        # TODO: 打开主窗口（课程列表 + 挂机队列）
        # 目前阶段：登录成功后仅显示提示，后续版本替换为主窗口
        info = tk.Toplevel(root)
        info.title("登录成功")
        tk.Label(info, text="登录成功！Token 已保存。\n\n（主界面功能正在开发中）", pady=20, padx=20).pack()
        tk.Button(info, text="退出", command=root.quit).pack(pady=10)
        root.deiconify()
        root.withdraw()  # 主窗口自身继续隐藏，只显示 info 窗口

    def on_login_window_closed() -> None:
        # 如果关闭登录窗口且未登录，则退出程序
        if not client.get_token():
            root.quit()

    login_win = LoginWindow(root, on_login_success=on_login_success)
    login_win.protocol("WM_DELETE_WINDOW", lambda: (login_win.destroy(), on_login_window_closed()))

    root.mainloop()


if __name__ == "__main__":
    main()
