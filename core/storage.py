"""
本地持久化存储（tinydb）。

数据文件位置：与脚本/可执行文件同级的 data/settings.json。
当前存储的表：
  credentials — 登录凭据（login_name, password）
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

_DB_PATH = _BASE_DIR / "data" / "credentials.json"


def _get_db() -> TinyDB:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return TinyDB(_DB_PATH)


# ── 登录凭据 ──────────────────────────────────────────────────────────────────

def save_credentials(login_name: str, password: str) -> None:
    """保存登录凭据（覆盖旧记录）。"""
    db = _get_db()
    table = db.table("credentials")
    table.truncate()
    table.insert({"login_name": login_name, "password": password})
    db.close()


def load_credentials() -> tuple[str, str]:
    """读取上次保存的登录凭据，返回 (login_name, password)；无记录时返回 ("", "")。"""
    db = _get_db()
    table = db.table("credentials")
    records = table.all()
    db.close()
    if records:
        rec = records[0]
        return rec.get("login_name", ""), rec.get("password", "")
    return "", ""
