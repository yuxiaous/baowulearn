"""
本地持久化存储（tinydb）。

数据文件位置：与脚本/可执行文件同级的 storage.json。
当前存储的表：
  auth — 登录凭据（login_name, password）
"""

from __future__ import annotations

import sys
from pathlib import Path

from tinydb import TinyDB

# 打包为 exe 时用 executable 所在目录，开发时用项目根目录
if getattr(sys, "frozen", False):
    _BASE_DIR = Path(sys.executable).parent
else:
    _BASE_DIR = Path(__file__).parent.parent

_DB_PATH = _BASE_DIR / "storage.json"


def _get_db() -> TinyDB:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return TinyDB(_DB_PATH)


# ── 登录凭据 ──────────────────────────────────────────────────────────────────


def save_credentials(username: str, password: str) -> None:
    """保存登录凭据（覆盖旧记录）。"""
    db = _get_db()
    table = db.table("auth")
    table.truncate()
    table.insert({"username": username, "password": password})
    db.close()


def load_credentials() -> tuple[str, str]:
    """读取上次保存的登录凭据，返回 (username, password)；无记录时返回 ("", "")。"""
    db = _get_db()
    table = db.table("auth")
    records = table.all()
    db.close()
    if records:
        rec = records[0]
        return rec.get("username", ""), rec.get("password", "")
    return "", ""
