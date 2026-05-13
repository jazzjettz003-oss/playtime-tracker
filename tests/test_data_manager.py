import json
from pathlib import Path

import pytest

from playtime_tracker.data_manager import DataManager


def test_data_manager_creates_default_data_file(tmp_path: Path):
    data_file = tmp_path / "data.json"
    manager = DataManager(data_file=data_file)

    assert data_file.exists()
    assert manager.apps == {}
    with data_file.open("r", encoding="utf-8") as source:
        payload = json.load(source)
    assert payload == {"apps": {}}


def test_data_manager_recovers_from_malformed_json(tmp_path: Path):
    data_file = tmp_path / "data.json"
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text("{ invalid json", encoding="utf-8")

    manager = DataManager(data_file=data_file)

    assert manager.apps == {}
    assert json.loads(data_file.read_text(encoding="utf-8")) == {"apps": {}}

    manager.add_or_track_app("example.exe", "Example")
    assert "example.exe" in manager.apps
