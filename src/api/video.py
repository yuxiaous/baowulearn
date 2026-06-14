"""
视频观看相关 API。
"""

from __future__ import annotations

from api import client
from models.course import Course
from models.video import Video

# ── 辅助函数 ──────────────────────────────────────────────────────────────────


def secs_to_hhmmss(secs: int) -> str:
    """秒数转 HH:MM:SS 字符串。"""
    h = secs // 3600
    m = (secs % 3600) // 60
    s = secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def hhmmss_to_secs(time_str: str) -> int:
    """HH:MM:SS 字符串转秒数。"""
    parts = time_str.split(":")
    if len(parts) == 3:
        try:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        except ValueError:
            pass
    return 0


# ── 视频列表 ──────────────────────────────────────────────────────────────────


def parse_mark_points(marks_str: str) -> list[int]:
    """将 "HH:MM:SS,HH:MM:SS,..." 转换为秒数列表，去重并排序。"""
    result = []
    for part in marks_str.split(","):
        part = part.strip()
        if part:
            result.append(hhmmss_to_secs(part))
    return sorted(set(result))


def get_course_videos(course: Course) -> list[Video]:
    """
    获取课程的视频列表（通过大纲接口）。

    只返回 contentType=="1"（视频）且 status=="1"（有效）的条目。
    """
    url = "/tms/rls/courseOutline/queryCourseOutlineContentTreeListSimple"
    payload = {
        "centerCode": course.center_code,
        "courseNo": course.course_no,
        "isAppendPre": "1",
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"获取课程视频列表失败: {resp.get('message', resp)}")

    videos: list[Video] = []
    idx = 0
    for chapter in resp.get("data", []):
        for item in chapter.get("content", []):
            if str(item.get("contentType")) == "1" and str(item.get("status")) == "1":
                videos.append(
                    Video(
                        video_guid=str(item.get("guid", "")),
                        video_name=str(item.get("newContentName", "")),
                        cata_no=str(item.get("cataNo", "")),
                        cata_type=str(item.get("cataType", "")),
                        ware_id=str(item.get("wareCode", "")),
                        ware_type=str(item.get("wareType", "1")),
                        course_no=str(item.get("courseNo", "")),
                        tenant_code=str(item.get("tenantCode", "")),
                        center_code=str(item.get("centerCode", "")),
                        duration=int(item.get("duration", 0)),
                        mark_points=parse_mark_points(item.get("markeTimePoint", "")),
                        learned_status=str(item.get("learnedStatus", None)),
                        index=idx,
                        course=course,
                    )
                )
                idx += 1
    return videos


# ── 学习记录初始化 ─────────────────────────────────────────────────────────────


def init_learn_record(course: Course, page_id: str) -> tuple[str, str]:
    """
    初始化学习记录，每次开始观看课程时调用一次。
    可以获取到上次的学习进度（续播用）。
    """
    url = "/tms/ols/learnRecord/initLearnRecord"
    payload = {
        "courseNo": course.course_no,
        "olClassNo": course.class_no,
        "pageId": page_id,
    }
    print(f"初始化学习记录: {course.course_name}")
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"初始化学习记录失败: {resp.get('message', resp)}")

    data = resp["data"]
    cata_no = data.get("cataNo", "")
    ware_id = data.get("wareCode", "")

    return cata_no, ware_id


# ── 已播放进度查询 ───────────────────────────────────────────────────────────────


def get_playback_progress(course: Course, video: Video) -> int:
    """
    查询视频已播放的最大时间，返回秒数。
    """
    url = "/tms/ols/learnWareProgress/getMaxTimeAndLastTime"
    payload = {
        "cataNo": video.cata_no,
        "courseNo": course.course_no,
        "olClassNo": course.class_no,
        "wareId": video.ware_id,
        "wareType": video.ware_type,
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        return 0

    data = resp["data"]
    max_time = hhmmss_to_secs(data.get("maxPlayTime", "00:00:00"))
    video.play_progress = max_time
    return max_time


# ── 视频播放控制 ──────────────────────────────────────────────────────────────


def start_video_event(course: Course, video: Video, begin_secs: int = 0) -> None:
    """发送开始播放信号（operateType=1, videoStatus=1）。

    begin_secs - 续播起始位置（秒），默认从头播放。
    """
    url = "/tms/ols/learnVideoRecord/listenVideoOptRecord"
    payload = {
        "cataNo": video.cata_no,
        "classCourseCenterCode": course.center_code,
        "courseNo": course.course_no,
        "olClassNo": course.class_no,
        "operateType": "1",
        "videoBeginTime": secs_to_hhmmss(begin_secs),
        "videoSpeed": 1,
        "videoStatus": "1",
        "wareId": video.ware_id,
        "wareType": video.ware_type,
    }
    print(f"开始播放视频事件: {video.video_name} @ {secs_to_hhmmss(begin_secs)}")
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"开始播放视频事件失败: {resp.get('message', resp)}")


def end_video_event(course: Course, video: Video, end_secs: int) -> None:
    """发送停止播放信号（operateType=2, videoStatus=2）。"""
    url = "/tms/ols/learnVideoRecord/listenVideoOptRecord"
    payload = {
        "cataNo": video.cata_no,
        "classCourseCenterCode": course.center_code,
        "courseNo": course.course_no,
        "olClassNo": course.class_no,
        "operateType": "2",
        "videoBeginTime": secs_to_hhmmss(end_secs),
        "videoSpeed": 1,
        "videoStatus": "2",
        "wareId": video.ware_id,
        "wareType": video.ware_type,
    }
    print(f"停止播放视频事件: {video.video_name} @ {secs_to_hhmmss(end_secs)}")
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"停止播放视频事件失败: {resp.get('message', resp)}")


# ── 心跳 ──────────────────────────────────────────────────────────────────────


def send_heartbeat(
    course: Course,
    video: Video,
    page_id: str,
    cur_secs: int,  # 当前播放位置（秒）
    learn_time: int,  # 距上次心跳的秒数
) -> None:
    """
    发送心跳（正常播放时每 60 秒一次，停止播放前补发一次）。
    cur_secs   - 当前播放位置（秒）
    learn_time - 距上次心跳的秒数
    """
    url = "/tms/ols/learnHertRecord/saveLearnHertRecord"
    payload = {
        "cataNo": video.cata_no,
        "classCourseCenterCode": course.center_code,
        "courseNo": course.course_no,
        "curPlayTime": secs_to_hhmmss(cur_secs),
        "isBlur": "0",
        "learnRealTime": learn_time,
        "learnTime": learn_time,
        "olClassNo": course.class_no,
        "pageId": page_id,
        "status": "1",
        "videoSpeed": 1,
        "wareId": video.ware_id,
        "wareType": video.ware_type,
    }
    print(f"发送心跳: {video.video_name} @ {secs_to_hhmmss(cur_secs)} (+{learn_time}s)")
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"发送心跳失败: {resp.get('message', resp)}")


# ── 进度打卡 ──────────────────────────────────────────────────────────────────


def send_mark_progress(
    course: Course,
    video: Video,
    page_id: str,
    mark_secs: int,
) -> None:
    """在指定时间点发送进度标记（markeTimePoint）。"""
    url = "/tms/ols/learnWareProgress/listenVideoMarkProgress"
    payload = {
        "cataNo": video.cata_no,
        "courseNo": course.course_no,
        "curPlayTime": secs_to_hhmmss(mark_secs),
        "markeTimePoint": secs_to_hhmmss(mark_secs),
        "olClassNo": course.class_no,
        "pageId": page_id,
        "wareId": video.ware_id,
        "wareType": video.ware_type,
    }
    print(f"打卡进度: {video.video_name} @ {secs_to_hhmmss(mark_secs)}")
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"进度打卡失败: {resp.get('message', resp)}")


# ── 完成视频 ──────────────────────────────────────────────────────────────────


def compute_video_finish(course: Course, video: Video) -> None:
    """
    触发服务端重新计算视频完成情况。
    """
    url = "/tms/ols/computeTask/saveComputeTask4AfterVideoPlayed"
    payload = {
        "classNo": course.class_no,
        "courseNo": course.course_no,
    }
    print(f"更新视频完成情况: {video.video_name}")
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"更新视频完成情况失败: {resp.get('message', resp)}")


# ── 心跳频率 ──────────────────────────────────────────────────────────────────


def get_heartbeat_interval() -> int:
    """获取心跳发送的时间间隔（秒）。"""
    url = "/ss/properties/queryPropValue"
    payload = {
        "propertiesKey": "heartFrequency",
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        return 60  # 默认 60 秒

    data = resp["data"]
    interval = int(data.get("propertiesValue", "60"))
    return interval
