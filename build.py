"""打包脚本：将 baowulearn 打包为单文件 exe。

用法（在项目根目录执行）：
    python build.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def main() -> None:
    # 确保 PyInstaller 已安装
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", "pyinstaller"],
        check=True,
    )

    sep = ";" if sys.platform == "win32" else ":"

    subprocess.run(
        [
            sys.executable, "-m", "PyInstaller",
            "--onedir",
            "--windowed",
            "--name", "baowulearn",
            "--add-data", f"pyproject.toml{sep}.",
            "main.py",
        ],
        cwd=ROOT,
        check=True,
    )

    exe = "baowulearn.exe" if sys.platform == "win32" else "baowulearn"
    print(f"\n打包完成，输出目录：dist/baowulearn/，入口：dist/baowulearn/{exe}")


if __name__ == "__main__":
    main()
