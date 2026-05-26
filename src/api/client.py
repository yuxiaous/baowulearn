"""
HTTP 会话封装。

持有一个全局 requests.Session，统一设置请求头；
登录成功后调用 set_token() 写入 token 头；
后续 API 调用均通过此模块的 post() / get() 发起。
"""

from __future__ import annotations

import requests

from config import BASE_URL, DEFAULT_HEADERS

_session = requests.Session()
_session.headers.update(DEFAULT_HEADERS)

# 登录成功后存储的 access token
_access_token: str | None = None


def set_token(token: str) -> None:
    """登录成功后调用，将 token 写入后续请求头。"""
    global _access_token
    _access_token = token
    _session.headers.update({"Token": token})


def get_token() -> str | None:
    return _access_token


def clear_token() -> None:
    global _access_token
    _access_token = None
    _session.headers.pop("Token", None)


def post(path: str, json: dict | None = None, **kwargs) -> dict:
    """发起 POST 请求，自动拼接 BASE_URL，返回响应 JSON。"""
    url = BASE_URL + path
    resp = _session.post(url, json=json or {}, **kwargs)
    resp.raise_for_status()
    return resp.json()


def get(path: str, **kwargs) -> dict:
    """发起 GET 请求，自动拼接 BASE_URL，返回响应 JSON。"""
    url = BASE_URL + path
    resp = _session.get(url, **kwargs)
    resp.raise_for_status()
    return resp.json()
