"""
宝武学习系统挂课工具 — 全局配置
"""

import os
import pathlib
import re
import sys


def base_dir() -> pathlib.Path:
    """打包时返回 _MEIPASS（资源目录），开发时返回项目根目录。"""
    if getattr(sys, "frozen", False):
        return pathlib.Path(sys._MEIPASS)
    return pathlib.Path(__file__).parent.parent


def exe_dir() -> pathlib.Path:
    """打包时返回 exe 所在目录（用户可写），开发时返回项目根目录。"""
    if getattr(sys, "frozen", False):
        return pathlib.Path(sys.executable).parent
    return pathlib.Path(__file__).parent.parent


def _read_version() -> str:
    project_file = base_dir() / "pyproject.toml"
    try:
        text = project_file.read_text(encoding="utf-8")
        m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
        return m.group(1) if m else "unknown"
    except OSError:
        return "unknown"


def _load_dotenv() -> None:
    """从 .env 文件加载环境变量，不覆盖已存在的系统变量。"""
    env_file = exe_dir() / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

VERSION: str = _read_version()


ASSETS_DIR: pathlib.Path = base_dir() / "assets"

# 从环境变量读取 Token（可在 .env 中配置 TOKEN=xxx）
TOKEN: str | None = os.environ.get("TOKEN") or None

BASE_URL = "https://learn.baowugroup.com/learn-gateway"

# SM2 非对称加密公钥 (base64编码)，从前端 JS 中提取
# JS 来源: const zi = {sm2PublicKey: "...", algorithm: "SM2"}
SM2_PUBLIC_KEY_B64 = (
    "BJeYoHWNsf60Vr2wPJWEWRvjH6m5r/JvK7Pww8SdohnwAkHKVy0tikYYOYmuKhR83BUS+duMyjAbVtyXZTfc+jY="
)

# 请求头
DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://learn.baowugroup.com",
    "Referer": "https://learn.baowugroup.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "sec-ch-ua": '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0"
    ),
}
