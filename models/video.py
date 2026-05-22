"""视频数据模型。"""

from __future__ import annotations

from dataclasses import dataclass, field


def _parse_mark_points(marks_str: str) -> list[int]:
    """将 "HH:MM:SS,HH:MM:SS,..." 转换为秒数列表，去重并排序。"""
    result = []
    for part in marks_str.split(","):
        part = part.strip()
        if not part:
            continue
        segments = part.split(":")
        if len(segments) == 3:
            try:
                h, m, s = int(segments[0]), int(segments[1]), int(segments[2])
                result.append(h * 3600 + m * 60 + s)
            except ValueError:
                pass
    return sorted(set(result))


@dataclass
class Video:
    """课程内单个视频的信息。"""

    cata_no: str       # cataNo — 所有视频 API 的标识符
    ware_id: str       # wareCode/wareId
    ware_type: str     # wareType（始终为 "1"）
    name: str          # 显示名称
    duration: int      # 视频总时长（秒）
    mark_points: list[int] = field(default_factory=list)  # 进度打卡点（秒）
    index: int = 0     # 在课程中的序号（0起）

    @classmethod
    def from_outline_item(cls, item: dict, index: int = 0) -> "Video":
        """从 queryCourseOutlineContentTreeListSimple 的 content 条目构建 Video。"""
        marks_str = item.get("markeTimePoint") or ""
        return cls(
            cata_no=str(item["cataNo"]),
            ware_id=str(item["wareCode"]),
            ware_type=str(item.get("wareType", "1")),
            name=str(item.get("newContentName") or item.get("contentName", "")),
            duration=int(item.get("duration") or 0),
            mark_points=_parse_mark_points(marks_str),
            index=index,
        )
