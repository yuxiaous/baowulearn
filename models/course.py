"""课程数据模型。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class HangStatus(Enum):
    """本地挂机状态（覆盖在服务端 learnStatus 之上）。"""
    IDLE = "idle"       # 未加入队列
    WAITING = "waiting" # 在队列中等待
    HANGING = "hanging" # 正在挂机


@dataclass
class Course:
    """一门课程的完整信息。"""

    course_guid: str          # courseGuid — 挂机操作用
    course_no: str            # courseNo
    course_name: str          # courseName
    class_name: str           # olClassName

    learn_status: str         # 服务端状态："0"未学, "1"学习中, "2"已完成
    course_hours: float       # 课程总时长（小时）
    near_learn_hours: int     # 已学时长（秒）

    class_guid: str = ""      # olClassNo / guid
    center_code: str = ""     # centerCode

    # 本地挂机状态（不来自服务端）
    hang_status: HangStatus = field(default=HangStatus.IDLE, compare=False)

    # ── 派生属性 ────────────────────────────────────────────────────────────────

    @property
    def total_seconds(self) -> int:
        """课程总时长（秒）。"""
        return int(self.course_hours * 3600)

    @property
    def display_status(self) -> str:
        """UI 显示用状态文字。"""
        if self.hang_status == HangStatus.HANGING:
            return "挂机中"
        if self.hang_status == HangStatus.WAITING:
            return "等待中"
        mapping = {"0": "未学习", "1": "学习中", "2": "已完成"}
        return mapping.get(self.learn_status, self.learn_status)

    @property
    def is_completed(self) -> bool:
        return self.learn_status == "2"

    @classmethod
    def from_api(cls, record: dict) -> "Course":
        """从 queryPageOpenClass 的单条 record 构建 Course。"""
        return cls(
            course_guid=str(record.get("courseGuid", "")),
            course_no=str(record.get("courseNo", "")),
            course_name=str(record.get("courseName", "")),
            class_name=str(record.get("olClassName", "")),
            learn_status=str(record.get("learnStatus", "0")),
            course_hours=float(record.get("courseHours") or 0),
            near_learn_hours=int(record.get("nearLearnHours") or 0),
            class_guid=str(record.get("guid", "")),
            center_code=str(record.get("centerCode", "")),
        )
