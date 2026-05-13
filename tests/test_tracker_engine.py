from typing import Dict

import psutil

from playtime_tracker.model import GameApp
from playtime_tracker.tracker import TrackerEngine


class DummyProcess:
    def __init__(self, name: str):
        self.info = {"name": name}


def test_tracker_engine_increments_active_apps(monkeypatch):
    apps: Dict[str, GameApp] = {
        "example.exe": GameApp(name="example.exe", display="Example", total_time=0),
        "other.exe": GameApp(name="other.exe", display="Other", total_time=0),
    }

    def fake_process_iter(attrs):
        yield DummyProcess("example.exe")

    monkeypatch.setattr(psutil, "process_iter", fake_process_iter)

    engine = TrackerEngine(apps, interval=1)
    engine._tick()

    assert apps["example.exe"].total_time == 1
    assert apps["other.exe"].total_time == 0
    assert engine.get_active_state()["example.exe"] is True
    assert engine.get_active_state()["other.exe"] is False
