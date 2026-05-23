"""课程列表 API。"""

from __future__ import annotations

from api import client
from models.course import Course


def get_openclass_courses(
    page: int = 1,
    page_size: int = 100,
    search_type: str = "1",
) -> list[Course]:
    """
    获取公开课课程列表（公开课标签页使用）。

    search_type: "1" 全部, "2" 学习中, "3" 已完成
    """
    resp = client.post(
        "/service/tms/ols/student/queryPageOpenClass",
        json={
            "current": page,
            "size": page_size,
            "data": {
                "learnStatus": "",
                "searchInfo": "",
                "searchType": search_type,
                "sortClass": "1",
                "sortType": "desc",
            },
        },
    )
    if not resp.get("isSuccess"):
        raise RuntimeError(f"获取课程列表失败: {resp.get('message', resp)}")

    records = resp["data"].get("records", [])
    return [Course.from_api(r) for r in records]


def get_my_classes() -> list[dict]:
    """
    获取我的专区课程班列表（myClassPage），只返回 ZE0 类型的专区记录。
    """
    try:
        resp = client.post(
            "/service/tms/ols/student/myClassPage",
            json={
                "current": 1,
                "size": 10,
                "data": {
                    "classType": "ZE0",
                    "isLearnNum": "1",
                    "keyWord": "",
                    "lastLearnTime": "1",
                    "learnStatus": "",
                    "sortClass": "1",
                    "sortType": "desc",
                    "status": "",
                },
            },
        )
        if not resp.get("isSuccess"):
            return []
        return resp["data"].get("records", [])
    except Exception:  # noqa: BLE001
        return []
