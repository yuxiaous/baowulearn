"""视频数据模型。"""

from __future__ import annotations

from dataclasses import dataclass, field

from models.course import Course


@dataclass
class Video:
    """课程内单个视频的信息。"""

    video_guid: str
    video_name: str
    cata_no: str
    cata_type: str
    ware_id: str  # wareCode/wareId
    ware_type: str  # wareType（"1"视频，"2"文档pdf）
    course_no: str  # courseNo — 课程编号
    tenant_code: str  # tenantCode — 租户编码
    center_code: str  # centerCode — 中心编码
    duration: int  # 视频时长（秒）
    mark_points: list[int] = field(default_factory=list)  # 进度打卡点（秒）
    learned_status: str = None  # 服务端状态：None 未学习, "0"学习中, "1"已完成
    play_progress: int = 0  # 已播放进度（秒），由 get_playback_progress 填充
    course: Course = None  # 所属课程
