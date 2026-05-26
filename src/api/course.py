"""课程列表 API。"""

from __future__ import annotations

from api import client
from models.course import Course
from models.olclass import OLClass

# ── 获取公开课列表 ──────────────────────────────────────────────────────────────


def get_openclass_courses(
    search_type: str = "1",  # "1" 全部, "2" 学习中, "3" 已完成
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[Course], int, int]:
    """
    获取我的公开课课程列表（单页）。
    返回 (课程列表, 总数, 总页数)。
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
        raise RuntimeError(f"获取公开课课程列表失败: {resp.get('message', resp)}")

    page_data = resp["data"]
    records = page_data.get("records", [])
    total_courses = int(page_data.get("total", 0))
    total_pages = int(page_data.get("pages", 1))

    courses = [
        Course(
            course_guid=str(record.get("courseGuid", "")),
            course_no=str(record.get("courseNo", "")),
            course_name=str(record.get("courseName", "")),
            class_no=str(record.get("olClassNo", "")),
            class_name=str(record.get("olClassName", "")),
            class_type=str(record.get("olClassType", "")),
            center_code=str(record.get("centerCode", None)),
            tenant_code=str(record.get("tenantCode", None)),
            learn_status=str(record.get("learnStatus", None)),
            course_hours=float(record.get("courseHours", 0.0)),
            begin_time=str(record.get("courseBeginTime", None)),
            end_time=str(record.get("courseEndTime", None)),
        )
        for record in records
    ]
    return courses, total_courses, total_pages


# ── 获取专区列表 ──────────────────────────────────────────────────────────────


def get_my_classes(
    page: int = 1,
    page_size: int = 10,
) -> list[OLClass]:
    """
    获取专区列表（专区标签页使用）。
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
        raise RuntimeError(f"获取专区列表失败: {resp.get('message', resp)}")

    records = resp["data"].get("records", [])
    return [
        OLClass(
            class_guid=str(record.get("guid", "")),
            class_no=str(record.get("olClassNo", "")),
            class_name=str(record.get("olClassName", "")),
            class_type=str(record.get("olClassType", "")),
            begin_time=str(record.get("beginTime", None)),
            end_time=str(record.get("endTime", None)),
            center_code=str(record.get("centerCode", "")),
            tenant_code=str(record.get("tenantCode", "")),
            course_num=int(record.get("courseNum", 0)),
        )
        for record in records
    ]


# ── 获取专区课程列表 ──────────────────────────────────────────────────────────────


def get_onlineclass_courses(
    class_no: str,
    class_type: str = "ZE0",
    page: int = 1,
    page_size: int = 5,
) -> tuple[list[Course], int, int]:
    """
    获取专区课程列表（单页）。
    返回 (课程列表, 总数, 总页数)。
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
        raise RuntimeError(f"获取专区课程列表失败: {resp.get('message', resp)}")

    page_data = resp["data"]
    records = page_data.get("records", [])
    total_courses = int(page_data.get("total", 0))
    total_pages = int(page_data.get("pages", 1))

    courses = [
        Course(
            course_guid=str(record.get("guid", "")),
            course_no=str(record.get("courseNo", "")),
            course_name=str(record.get("courseName", "")),
            class_no=str(record.get("olClassNo", "")),
            class_name=str(record.get("olClassName", "")),
            class_type=str(record.get("olClassType", "")),
            center_code=str(record.get("centerCode", None)),
            tenant_code="BSTA",
            learn_status=str(record.get("learnStatus", None)),
            begin_time=str(record.get("beginTime", None)),
            end_time=str(record.get("endTime", None)),
        )
        for record in records
    ]
    return courses, total_courses, total_pages


# ── 获取课程详情 ──────────────────────────────────────────────────────────────


def get_course_detail(course: Course) -> Course:
    """获取课程详情，包含学时等信息。"""
    url = "/service/tms/ols/onlineClassCourse/detailOnlineClassCourse"
    payload = {
        "centerCode": course.center_code,
        "guid": course.course_guid,
        "stuClient": True,
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"获取课程详情失败: {resp.get('message', resp)}")

    data = resp["data"]
    course._course_detail = data
    course.course_guid = str(data.get("guid", ""))
    course.course_no = str(data.get("courseNo", ""))
    course.course_name = str(data.get("courseName", ""))
    course.class_no = str(data.get("olClassNo", ""))
    course.class_name = str(data.get("olClassName", ""))
    course.class_type = str(data.get("olClassType", ""))
    course.center_code = str(data.get("centerCode", None))
    course.tenant_code = str(data.get("tenantCode", None))
    course.course_hours = float(data.get("courseHours", 0.0))
    course.begin_time = str(data.get("beginTime", None))
    course.end_time = str(data.get("endTime", None))
    return course


# ── 课程完成情况 ──────────────────────────────────────────────────────────────


def save_compute_task_course_detail(course: Course) -> None:
    """
    触发服务端重新计算课程完成情况。
    """
    url = "/service/tms/ols/computeTask/saveComputeTask4StuCourseDetail"
    payload = {
        "classNo": course.class_no,
        "courseNo": course.course_no,
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"触发计算课程完成情况失败: {resp.get('message', resp)}")


def get_course_finish_info(course: Course) -> Course:
    """查询课程完成情况。"""
    url = "/service/tms/ols/onlineClassCourse/finishInfo"
    payload = {
        "centerCode": course.center_code,
        "courseNo": course.course_no,
        "olClassNo": course.class_no,
        "tenantCode": course.tenant_code,
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"查询课程完成情况失败: {resp.get('message', resp)}")

    data = resp["data"]
    course._finish_info = data
    if data.get("learnStatus") is not None:
        course.learn_status = str(data["learnStatus"])
    course.course_score = float(data.get("learnScore") or 0.0)

    for detail in data.get("details") or []:
        if detail.get("attributeCode") == "CE002":  # 学习时长
            course.course_duration = float(detail.get("predValue") or 0.0)
            course.course_finished = float(detail.get("finishValue") or 0.0)

    return course
