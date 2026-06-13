"""打包脚本：将 baowulearn 打包为单文件 exe。

用法（在项目根目录执行）：
    python build.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def _clean_output_dirs() -> None:
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


def _copy_openssl_dlls() -> None:
    """强制覆盖 PyInstaller 可能打包错误的 OpenSSL DLL。"""
    python_dlls = Path(sys.base_prefix) / "DLLs"
    for dll_name in ["libcrypto-3-x64.dll", "libssl-3-x64.dll"]:
        src_dll = python_dlls / dll_name
        if not src_dll.exists():
            print(f"错误：未找到 {src_dll}，请确保 Python 安装完整。")
            sys.exit(1)
        dst_dll = ROOT / "dist" / "baowulearn" / "_internal" / dll_name
        shutil.copy(src_dll, dst_dll)


def main() -> None:
    _clean_output_dirs()

    sep = ";" if sys.platform == "win32" else ":"

    args = [sys.executable, "-m", "PyInstaller"]
    args += ["--noconfirm", "--onedir", "--windowed"]
    args += ["--name", "baowulearn"]
    args += ["--icon", str(ROOT / "assets" / "favicon.ico")]
    args += ["--add-data", f"pyproject.toml{sep}."]
    args += ["--add-data", f"assets{sep}assets"]
    args += ["--add-data", f"LICENSE{sep}."]
    args += ["--add-data", f"third_party_licenses{sep}third_party_licenses"]
    args += ["src/main.py"]
    subprocess.run(args, cwd=ROOT, check=True)

    # fix: 强制覆盖 PyInstaller 可能打包错误的 OpenSSL DLL
    _copy_openssl_dlls()

    exe = "baowulearn.exe" if sys.platform == "win32" else "baowulearn"
    print(f"\n打包完成，输出目录：dist/baowulearn/，入口：dist/baowulearn/{exe}")


if __name__ == "__main__":
    main()
