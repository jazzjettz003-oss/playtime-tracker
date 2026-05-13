from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class GameApp:
    """Represents a tracked application or game entry."""

    name: str
    display: str
    total_time: int = 0
    is_tracking: bool = True
    category: str = "General"
    color_tag: str = "#7b2cbf"

    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> "GameApp":
        """Load a GameApp from a saved dictionary, supporting legacy keys."""
        display_value = data.get("display") or data.get("name") or name
        time_value = int(data.get("time", data.get("cumulative_seconds", 0)) or 0)
        is_tracking = bool(data.get("is_tracking", True))
        category = str(data.get("category", "General"))
        color_tag = str(data.get("color_tag", "#7b2cbf"))
        return cls(
            name=name,
            display=display_value,
            total_time=time_value,
            is_tracking=is_tracking,
            category=category,
            color_tag=color_tag,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the GameApp to a JSON-compatible payload."""
        return {
            "name": self.name,
            "display": self.display,
            "time": self.total_time,
            "is_tracking": self.is_tracking,
            "category": self.category,
            "color_tag": self.color_tag,
        }
