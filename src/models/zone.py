"""专区数据模型。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Zone:
    """一个专区的完整信息。"""

    class_guid: str  # 专区唯一标识
    class_no: str  # 专区编号
    class_name: str  # 专区名称
    class_type: str  # 专区类型（OCE 公开课, ZE0 学习专区）
    begin_time: str = None  # 专区开始时间（格式 "2024-01-01"）
    end_time: str = None  # 专区结束时间（格式 "2024-01-01"）
    center_code: str = ""  # 专区编号
    tenant_code: str = ""  # 租户编码
