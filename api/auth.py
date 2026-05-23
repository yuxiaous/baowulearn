"""
认证 API：获取验证码图片、登录。
"""

from __future__ import annotations

import base64

from api import client
from core.crypto import sm2_encrypt

# ── 验证码 ────────────────────────────────────────────────────────────────────


def get_captcha() -> tuple[bytes, str]:
    """
    获取图片验证码。

    返回 (jpeg_bytes, captcha_id)。
    """
    data = client.post("/service/ss/auth/user/captchaImage")
    if not data.get("isSuccess"):
        raise RuntimeError(f"获取验证码失败: {data}")

    captcha_data = data["data"]
    image_b64: str = captcha_data["captchaImage"]
    captcha_id: str = captcha_data["captchaId"]

    # base64 图片可能带有 data:image/... 前缀
    if "," in image_b64:
        image_b64 = image_b64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_b64)
    return image_bytes, captcha_id


# ── 登录 ──────────────────────────────────────────────────────────────────────


def login(
    login_name: str,
    password: str,
    captcha_code: str,
    captcha_id: str,
) -> str:
    """
    使用工号密码登录。

    工号和密码在发送前用 SM2 公钥加密。
    返回 accessToken 字符串；失败则抛出 RuntimeError。
    """
    payload = {
        "mobile": "",
        "loginName": sm2_encrypt(login_name),
        "password": sm2_encrypt(password),
        "captchaCode": captcha_code,
        "captchaNum": "",
        "captchaId": captcha_id,
        "type": "byPassword",
        "clientType": "PC",
    }

    data = client.post("/service/ss/auth/user/login", json=payload)

    if not data.get("isSuccess"):
        msg = data.get("message") or data.get("msg") or str(data)
        raise RuntimeError(f"登录失败: {msg}")

    token: str = data["data"]["accessToken"]
    print("登录成功，Token:", token)

    client.set_token(token)
    return token
