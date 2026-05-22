"""课程列表 API。"""

from __future__ import annotations

from api import client
from models.course import Course


def get_courses(
    learn_status: str = "",
    page: int = 1,
    page_size: int = 100,
) -> list[Course]:
    """
    获取当前学员的公开课列表。

    learn_status: "" 全部, "1" 学习中, "2" 已完成
    返回 Course 列表（单次拉取，默认 page_size=100 覆盖全部）。
    """
    payload = {
        "current": page,
        "size": page_size,
        "data": {
            "learnStatus": learn_status,
            "searchInfo": "",
            "searchType": "1",
            "sortClass": "1",
            "sortType": "desc",
        },
    }
    resp = client.post(
        "/service/tms/ols/student/queryPageOpenClass", json=payload
    )
    if not resp.get("isSuccess"):
        raise RuntimeError(f"获取课程列表失败: {resp.get('message', resp)}")

    records = resp["data"].get("records", [])
    return [Course.from_api(r) for r in records]
