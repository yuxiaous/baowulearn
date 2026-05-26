"""打包脚本：将 baowulearn 打包为单文件 exe。

用法（在项目根目录执行）：
    python build.py
"""

import shutil
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

    # 清理旧的输出目录，若被占用则提示关闭 exe
    for clean_dir in [
        ROOT / "dist" / "baowulearn",
        ROOT / "build" / "baowulearn",
    ]:
        if clean_dir.exists():
            try:
                shutil.rmtree(clean_dir)
            except PermissionError:
                print(f"错误：{clean_dir} 目录被占用，请先关闭正在运行的 baowulearn.exe，再重试。")
                sys.exit(1)

    sep = ";" if sys.platform == "win32" else ":"

    args = [sys.executable, "-m", "PyInstaller"]
    args += ["--noconfirm", "--onedir", "--windowed"]
    args += ["--name", "baowulearn"]
    args += ["--icon", str(ROOT / "assets" / "favicon.ico")]
    args += ["--add-data", f"pyproject.toml{sep}."]
    args += ["--add-data", f"assets{sep}assets"]
    args += ["src/main.py"]
    subprocess.run(args, cwd=ROOT, check=True)

    exe = "baowulearn.exe" if sys.platform == "win32" else "baowulearn"
    print(f"\n打包完成，输出目录：dist/baowulearn/，入口：dist/baowulearn/{exe}")


if __name__ == "__main__":
    main()
