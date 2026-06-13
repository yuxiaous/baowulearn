"""课程列表 API。"""

from __future__ import annotations

from api import client
from models.course import Course, LearnStatus
from models.zone import Zone

# ── 获取专区列表 ──────────────────────────────────────────────────────────────


def get_zone_list(
    center_code: str,
    page: int = 1,
    page_size: int = 96,
) -> list[Zone]:
    """
    获取专区列表。
    """
    url = "/tms/ols/onlineClass/queryMainOnlineClassPage"
    payload = {
        "current": page,
        "size": page_size,
        "data": {
            "centerCode": center_code,  # 中心编号 C001 集团站点, C002 人才开发院
            "olClassCode": "",
            "olClassType": "ZE0",
            "searchInfo": "",
            "userSource": "1",
            "isMine": "1",
            "sortFlag": 5,
        },
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"获取专区{center_code}列表失败: {resp.get('message', resp)}")

    records = resp["data"].get("records", [])
    zones = [
        Zone(
            class_guid=record.get("guid"),
            class_no=record.get("olClassNo"),
            class_name=record.get("olClassName"),
            class_type=record.get("olClassType"),  # 专区类型 ZE0 学习专区
            begin_time=record.get("beginTime"),  # 专区开始时间
            end_time=record.get("endTime"),  # 专区结束时间
            center_code=record.get("centerCode") or "",  # 中心编号
            tenant_code=record.get("tenantCode") or "",  # 租户编号
        )
        for record in records
    ]
    return zones


# ── 获取公开课列表 ──────────────────────────────────────────────────────────────


def get_open_courses(
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[Course], int, int]:
    """
    获取我的公开课课程列表（单页）。
    返回 (课程列表, 总数, 总页数)。
    """
    url = "/tms/ols/student/queryPageOpenClass"
    payload = {
        "current": page,
        "size": page_size,
        "data": {
            "learnStatus": "",
            "searchInfo": "",  # 搜索过滤字段
            "searchType": "1",  # "1" 全部, "2" 学习中, "3" 已完成
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
            course_guid=record.get("courseGuid"),
            course_no=record.get("courseNo"),
            course_name=record.get("courseName"),
            class_no=record.get("olClassNo") or "",
            class_name=record.get("olClassName") or "",
            class_type=record.get("olClassType") or "",  # 专区类型 "OCE" 公开课
            center_code=record.get("centerCode"),  # 中心编号
            tenant_code=record.get("tenantCode"),  # 租户编号
            learn_status=LearnStatus(record.get("learnStatus") or "0"),  # 服务端状态：None 未学习, "1"学习中, "2"已完成
            course_hours=float(record.get("courseHours") or 0.0),  # 课程学时
            begin_time=record.get("courseBeginTime"),  # 学习开始时间
            end_time=record.get("courseEndTime"),  # 学习结束时间
        )
        for record in records
    ]
    return courses, total_courses, total_pages


# ── 获取专区课程列表 ──────────────────────────────────────────────────────────────


def get_zone_courses(
    zone: Zone,
    page: int = 1,
    page_size: int = 4,
) -> tuple[list[Course], int, int]:
    """
    获取专区课程列表（单页）。
    返回 (课程列表, 总数, 总页数)。
    """
    url = "/tms/ols/onlineClassCourse/getOnlineClassCourseSortPage"
    payload = {
        "current": page,
        "size": page_size,
        "data": {
            "centerCode": zone.center_code,  # 中心编号
            "courseName": "",  # 搜索关键词，模糊匹配课程名称
            "courseTypeCode": "",
            "isMine": "1",
            "isRecursiveCourse": "1",
            "olClassNo": zone.class_no,  # 专区号
            "olClassType": zone.class_type,  # 专区类型
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
            course_guid=record.get("guid"),
            course_no=record.get("courseNo"),
            course_name=record.get("courseName"),
            class_no=zone.class_no,
            class_name=zone.class_name,
            class_type=zone.class_type,
            center_code=zone.center_code,  # 中心编号
            tenant_code=zone.tenant_code,  # 租户编号
            learn_status=LearnStatus(record.get("learnStatus") or "0"),  # 服务端状态：None 未知, "1"学习中, "2"已完成
            begin_time=record.get("beginTime"),  # 学习开始时间
            end_time=record.get("endTime"),  # 学习结束时间
            zone=zone,  # 所属专区
        )
        for record in records
    ]
    return courses, total_courses, total_pages


# ── 获取课程详情 ──────────────────────────────────────────────────────────────


def get_course_detail(course: Course) -> Course:
    """获取课程详情，包含学时等信息。"""
    url = "/tms/ols/onlineClassCourse/detailOnlineClassCourse"
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

    course.course_guid = data.get("guid")
    course.course_no = data.get("courseNo")
    course.course_name = data.get("courseName")
    course.class_no = data.get("olClassNo")
    course.class_name = data.get("olClassName")
    course.class_type = data.get("olClassType")
    course.center_code = data.get("centerCode")  # 中心编号
    course.tenant_code = data.get("tenantCode")  # 租户编号
    course.course_hours = float(data.get("courseHours") or 0.0)  # 课程学时
    course.begin_time = data.get("beginTime")  # 学习开始时间
    course.end_time = data.get("endTime")  # 学习结束时间

    return course


# ── 课程完成情况 ──────────────────────────────────────────────────────────────


def compute_course_finish(course: Course) -> None:
    """
    触发服务端重新计算课程完成情况。
    """
    url = "/tms/ols/computeTask/saveComputeTask4StuCourseDetail"
    payload = {
        "classNo": course.class_no,
        "courseNo": course.course_no,
    }
    print(f"计算课程完成情况: {course.course_name} ({course.course_no})")
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"触发计算课程完成情况失败: {resp.get('message', resp)}")


def get_course_finish_info(course: Course) -> Course:
    """查询课程完成情况。"""
    url = "/tms/ols/onlineClassCourse/finishInfo"
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

    # 学习状态
    if data.get("learnStatus") is not None:
        course.learn_status = LearnStatus(data.get("learnStatus"))
    # 课程成绩
    if data.get("learnScore") is not None:
        course.course_score = float(data.get("learnScore") or 0.0)
    # 其他数据
    for detail in data.get("details") or []:
        # attributeCode: CE001 考试成绩, CE002 学习时长, CE009 课程调查
        if detail.get("attributeCode") == "CE002":  # 学习时长
            # 课程总时长（分钟）
            course.course_duration = float(detail.get("predValue") or 0.0)
            # 课程完成时间（分钟）
            course.course_finished = float(detail.get("finishValue") or 0.0)

    return course


# ── 专区完成情况 ──────────────────────────────────────────────────────────────


def compute_zone_finish(zone: Zone) -> None:
    """
    触发服务端重新计算专区完成情况。
    """
    url = "/tms/ols/computeTask/saveComputeTask4StuClassDetail"
    payload = {
        "classNo": zone.class_no,
    }
    print(f"计算专区完成情况: {zone.class_name} ({zone.class_no})")
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"触发计算专区完成情况失败: {resp.get('message', resp)}")
