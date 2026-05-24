"""
视频观看相关 API。

涵盖从获取视频列表到完成播放的完整流程：
  get_course_videos → init_learn_record → start_video
  → send_heartbeat / mark_progress (循环)
  → complete_video → end_video

辅助查询：
  get_play_progress  — 获取已播放最大时间（续播用）
  get_finish_info    — 获取课程完成情况（学习时长进度、得分等）
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


# ── 视频列表 ──────────────────────────────────────────────────────────────────


def get_course_videos(
    course_no: str,
    center_code: str,
) -> list[Video]:
    """
    获取课程的视频列表（通过大纲接口）。

    只返回 contentType=="1"（视频）且 status=="1"（有效）的条目。
    """
    url = "/service/tms/rls/courseOutline/queryCourseOutlineContentTreeListSimple"
    payload = {
        "centerCode": center_code,
        "courseNo": course_no,
        "isAppendPre": "1",
    }
    resp = client.post(url, json=payload)
    if not resp.get("isSuccess"):
        raise RuntimeError(f"获取视频列表失败: {resp.get('message', resp)}")

    videos: list[Video] = []
    idx = 0
    for chapter in resp.get("data", []):
        for item in chapter.get("content", []):
            if (
                str(item.get("contentType")) == "1"
                and str(item.get("status", "1")) == "1"
            ):
                videos.append(Video.from_outline_item(item, index=idx))
                idx += 1
    return videos


# ── 已播放进度查询 ───────────────────────────────────────────────────────────────


def get_play_progress(course: Course, video: Video) -> int:
    """
    查询视频已播放的最大时间，返回秒数。

    对应 maxPlayTime 字段（HH:MM:SS）。若接口返回 null 或出错则返回 0。
    """
    try:
        resp = client.post(
            "/service/tms/ols/learnWareProgress/getMaxTimeAndLastTime",
            json={
                "cataNo": video.cata_no,
                "courseNo": course.course_no,
                "olClassNo": course.class_no,
                "wareId": video.ware_id,
                "wareType": video.ware_type,
            },
        )
        if not resp.get("isSuccess"):
            return 0
        max_time: str = (resp.get("data") or {}).get("maxPlayTime") or ""
        if not max_time:
            return 0
        parts = max_time.split(":")
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except Exception:  # noqa: BLE001
        pass
    return 0


# ── 课程完成情况 ──────────────────────────────────────────────────────────────


def save_compute_task_course_detail(course: Course) -> None:
    """
    触发服务端重新计算课程完成情况。

    必须在每次心跳后调用，服务端才会更新 finishInfo.finishValue。
    请求体：{"classNo": olClassNo, "courseNo": courseNo}
    """
    try:
        client.post(
            "/service/tms/ols/computeTask/saveComputeTask4StuCourseDetail",
            json={"classNo": course.class_no, "courseNo": course.course_no},
        )
    except Exception:  # noqa: BLE001
        pass


# ── 学习记录初始化 ─────────────────────────────────────────────────────────────


def init_learn_record(course_no: str, ol_class_no: str, page_id: str) -> None:
    """初始化学习记录，每次开始观看课程时调用一次。"""
    client.post(
        "/service/tms/ols/learnRecord/initLearnRecord",
        json={"courseNo": course_no, "olClassNo": ol_class_no, "pageId": page_id},
    )


# ── 视频播放控制 ──────────────────────────────────────────────────────────────


def start_video(course: Course, video: Video, begin_secs: int = 0) -> None:
    """发送开始播放信号（operateType=1, videoStatus=1）。

    begin_secs - 续播起始位置（秒），默认从头播放。
    """
    client.post(
        "/service/tms/ols/learnVideoRecord/listenVideoOptRecord",
        json={
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
        },
    )


def end_video(course: Course, video: Video, end_secs: int) -> None:
    """发送停止播放信号（operateType=2, videoStatus=2）。"""
    client.post(
        "/service/tms/ols/learnVideoRecord/listenVideoOptRecord",
        json={
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
        },
    )


# ── 心跳 ──────────────────────────────────────────────────────────────────────


def send_heartbeat(
    course: Course,
    video: Video,
    page_id: str,
    cur_secs: int,
    learn_real_time: int,
) -> None:
    """
    发送心跳（每 60 秒一次）。

    cur_secs       - 当前播放位置（秒）
    learn_real_time - 距上次心跳的秒数
    """
    client.post(
        "/service/tms/ols/learnHertRecord/saveLearnHertRecord",
        json={
            "cataNo": video.cata_no,
            "classCourseCenterCode": course.center_code,
            "courseNo": course.course_no,
            "curPlayTime": secs_to_hhmmss(cur_secs),
            "isBlur": "0",
            "learnRealTime": learn_real_time,
            "learnTime": learn_real_time,
            "olClassNo": course.class_no,
            "pageId": page_id,
            "status": "1",
            "videoSpeed": 1,
            "wareId": video.ware_id,
            "wareType": video.ware_type,
        },
    )


# ── 进度打卡 ──────────────────────────────────────────────────────────────────


def mark_progress(
    course: Course,
    video: Video,
    page_id: str,
    cur_secs: int,
) -> None:
    """在指定时间点发送进度标记（markeTimePoint）。"""
    ts = secs_to_hhmmss(cur_secs)
    client.post(
        "/service/tms/ols/learnWareProgress/listenVideoMarkProgress",
        json={
            "cataNo": video.cata_no,
            "courseNo": course.course_no,
            "curPlayTime": ts,
            "markeTimePoint": ts,
            "olClassNo": course.class_no,
            "pageId": page_id,
            "wareId": video.ware_id,
            "wareType": video.ware_type,
        },
    )


# ── 完成视频 ──────────────────────────────────────────────────────────────────


def complete_video(ol_class_no: str, course_no: str) -> None:
    """发送视频完成信号（saveComputeTask4AfterVideoPlayed）。"""
    client.post(
        "/service/tms/ols/computeTask/saveComputeTask4AfterVideoPlayed",
        json={"classNo": ol_class_no, "courseNo": course_no},
    )
