from dataclasses import asdict, dataclass


@dataclass
class GameApp:
    name: str
    display: str
    total_time: int = 0
    is_tracking: bool = True

    @classmethod
    def from_dict(cls, name: str, data: dict) -> "GameApp":
        display_value = data.get("display") or data.get("name") or name
        time_value = data.get("time", data.get("cumulative_seconds", 0))
        is_tracking = data.get("is_tracking", True)
        return cls(name=name, display=display_value, total_time=time_value, is_tracking=is_tracking)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "display": self.display,
            "time": self.total_time,
            "is_tracking": self.is_tracking,
        }
