"""SM2 加密工具，用于登录时加密工号和密码。"""

import base64

from gmssl import sm2 as _sm2

from config import SM2_PUBLIC_KEY_B64


def _load_public_key_hex() -> str:
    """将 base64 公钥解码为十六进制字符串（去掉 04 前缀）。"""
    pk_bytes = base64.b64decode(SM2_PUBLIC_KEY_B64)
    pk_hex = pk_bytes.hex()
    return pk_hex


_SM2_PUBLIC_KEY_HEX = _load_public_key_hex()
# mode=1 → C1+C3+C2 format（与前端 doEncrypt(..., 1) 一致）
_sm2_crypt = _sm2.CryptSM2(public_key=_SM2_PUBLIC_KEY_HEX, private_key="", mode=1)


def sm2_encrypt(plaintext: str) -> str:
    """
    用 SM2 公钥加密明文字符串，返回小写十六进制密文。

    输出格式：C1(128 hex, 无04前缀) + C3/SM3哈希(64 hex) + C2(密文)。
    与前端 doEncrypt(plaintext, publicKey, 1) 格式一致（mode=1 → C1+C3+C2）。

    gmssl.CryptSM2(mode=1) 的 encrypt() 接受 bytes，返回 bytes。
    C1 由内部 _kg() 产生，已是 x+y 的 hex 拼接（128字符），无 04 前缀。
    """
    plaintext_bytes = plaintext.encode("utf-8")
    result_bytes: bytes = _sm2_crypt.encrypt(plaintext_bytes)
    result = result_bytes.hex().lower()

    # 防御性去掉 04 前缀（理论上 gmssl 不会加，但以防万一）
    expected_len = 128 + 64 + len(plaintext_bytes) * 2
    if len(result) == expected_len + 2 and result.startswith("04"):
        result = result[2:]

    return result

