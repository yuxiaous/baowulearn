"""课程列表 API。"""

from __future__ import annotations

from api import client
from models.course import Course
from models.olclass import OLClass


def get_openclass_courses(
    search_type: str = "1",  # "1" 全部, "2" 学习中, "3" 已完成
    page: int = 1,
    page_size: int = 100,
) -> list[Course]:
    """
    获取我的公开课课程列表（公开课标签页使用）。
    """
    url = "/service/tms/ols/student/queryPageOpenClass"
    payload = {
        "current": page,
        "size": page_size,
        "data": {
            "learnStatus": "",
            "searchInfo": "",
            "searchType": search_type,
            "sortClass": "1",
            "sortType": "desc",
        },
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"获取课程列表失败: {resp.get('message', resp)}")

    records = resp["data"].get("records", [])
    return [
        Course(
            course_no=str(r.get("courseNo", "")),
            course_name=str(r.get("courseName", "")),
            class_no=str(r.get("olClassNo", "")),
            class_name=str(r.get("olClassName", "")),
            class_type=str(r.get("olClassType", "")),
            center_code=str(r.get("centerCode", None)),
            tenant_code=str(r.get("tenantCode", None)),
            learn_status=str(r.get("learnStatus", None)),
            course_hours=float(r.get("courseHours", 0.0)),
            begin_time=str(r.get("courseBeginTime", None)),
            end_time=str(r.get("courseEndTime", None)),
        )
        for r in records
    ]


def get_my_classes(
    page: int = 1,
    page_size: int = 10,
) -> list[OLClass]:
    """
    获取我的专区课程班列表（专区标签页使用）。
    """
    url = "/service/tms/ols/student/myClassPage"
    payload = {
        "current": page,
        "size": page_size,
        "data": {
            "classType": "ZE0",  # 只查询学习专区
            "isLearnNum": "1",
            "keyWord": "",
            "lastLearnTime": "1",
            "learnStatus": "",
            "sortClass": "1",
            "sortType": "desc",
            "status": "1",  # 只查询进行中的专区
        },
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        return []

    records = resp["data"].get("records", [])
    return [
        OLClass(
            class_guid=str(r.get("guid", "")),
            class_no=str(r.get("olClassNo", "")),
            class_name=str(r.get("olClassName", "")),
            class_type=str(r.get("olClassType", "")),
            begin_time=str(r.get("beginTime", None)),
            end_time=str(r.get("endTime", None)),
            center_code=str(r.get("centerCode", "")),
            tenant_code=str(r.get("tenantCode", "")),
            course_num=int(r.get("courseNum", 0)),
        )
        for r in records
    ]


def get_onlineclass_courses(
    class_no: str,
    class_type: str = "ZE0",
    page: int = 1,
    page_size: int = 4,
) -> list[Course]:
    """
    获取专区课程列表
    """
    url = "/service/tms/ols/onlineClassCourse/getOnlineClassCourseSortPage"
    payload = {
        "current": page,
        "size": page_size,
        "data": {
            "centerCode": "C001",
            "courseName": "",  # 搜索关键词，模糊匹配课程名称
            "courseTypeCode": "",
            "isMine": "1",
            "isRecursiveCourse": "1",
            "olClassNo": class_no,  # 专区编号
            "olClassType": class_type,
        },
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        return []

    records = resp["data"].get("records", [])
    return [
        Course(
            course_no=str(r.get("courseNo", "")),
            course_name=str(r.get("courseName", "")),
            class_no=str(r.get("olClassNo", "")),
            class_name=str(r.get("olClassName", "")),
            class_type=str(r.get("olClassType", "")),
            center_code=str(r.get("centerCode", None)),
            # tenant_code=str(r.get("tenantCode", None)),
            learn_status=str(r.get("learnStatus", None)),
            # course_hours=float(r.get("courseHours", 0.0)),
            begin_time=str(r.get("beginTime", None)),
            end_time=str(r.get("endTime", None)),
        )
        for r in records
    ]
