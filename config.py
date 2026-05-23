"""
宝武学习系统挂课工具 — 全局配置
"""

BASE_URL = "https://learn.baowugroup.com/learn-gateway"

# SM2 非对称加密公钥 (base64编码)，从前端 JS 中提取
# JS 来源: const zi = {sm2PublicKey: "...", algorithm: "SM2"}
SM2_PUBLIC_KEY_B64 = (
    "BJeYoHWNsf60Vr2wPJWEWRvjH6m5r/JvK7Pww8SdohnwAkHKVy0tikYYOYmuKhR83BUS"
    "+duMyjAbVtyXZTfc+jY="
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

# 可选：预设登录 Token，避免每次运行都要扫码登录一次（不要将真实 Token 提交到版本控制）
# TOKEN = ""
