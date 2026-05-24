"""课程数据模型。"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class HangStatus(Enum):
    """本地挂机状态（覆盖在服务端 learnStatus 之上）。"""

    IDLE = "idle"  # 未加入队列
    WAITING = "waiting"  # 在队列中等待
    HANGING = "hanging"  # 正在挂机


@dataclass
class Course:
    """一门课程的完整信息。"""

    course_guid: str  # 课程唯一标识（目前未使用）
    course_no: str  # 课程编号
    course_name: str  # 课程名称
    class_no: str = ""  # 专区编号
    class_name: str = ""  # 专区名称
    class_type: str = ""  # 专区类型（OCE 公开课, ZE0 学习专区）
    center_code: str = None  # 中心编码 (C001)
    tenant_code: str = None  # 租户编码 (BSTA)
    begin_time: str = None  # 学习开始时间（格式 "2024-01-01"）
    end_time: str = None  # 学习结束时间（格式 "2024-01-01"）
    learn_status: str = None  # 服务端状态：None 未知, "1"学习中, "2"已完成
    course_hours: float = 0.0  # 课程学时
    course_score: float = 0.0  # 课程成绩
    course_duration: float = 0  # 课程总时长（分钟）
    course_finished: float = 0  # 课程完成时间 (分钟)

    # 课程详情（原始接口返回的全部字段）
    _course_detail: dict | None = field(default=None, compare=False)

    # 完成情况（原始接口返回的全部字段）
    _finish_info: dict | None = field(default=None, compare=False)

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
