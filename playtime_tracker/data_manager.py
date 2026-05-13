import json
from pathlib import Path
from typing import Dict

from .config import DATA_FILE, DEFAULT_CATEGORY, DEFAULT_COLOR_TAG, SETTINGS_FILE
from .model import GameApp

DEFAULT_STATE: Dict[str, Dict[str, object]] = {"apps": {}}


class DataManager:
    """Manage persistent app state and local JSON storage."""

    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = Path(data_file)
        self._ensure_data_file_exists()
        self._data = self._load_data_file()
        self.apps: Dict[str, GameApp] = self._load_apps()

    def _ensure_data_file_exists(self) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._write_default_state()

    def _load_data_file(self) -> Dict[str, object]:
        try:
            with self.data_file.open("r", encoding="utf-8") as source:
                return json.load(source)
        except (json.JSONDecodeError, OSError):
            self._write_default_state()
            return DEFAULT_STATE.copy()

    def _load_apps(self) -> Dict[str, GameApp]:
        apps: Dict[str, GameApp] = {}
        for key, raw_app in self._data.get("apps", {}).items():
            try:
                app = GameApp.from_dict(key.lower(), raw_app)
                apps[app.name] = app
            except Exception as exc:
                print(f"[data_manager] skipping malformed entry '{key}': {exc}")
        return apps

    def _write_default_state(self) -> None:
        with self.data_file.open("w", encoding="utf-8") as target:
            json.dump(DEFAULT_STATE, target, indent=2)

    def save(self) -> None:
        payload = {"apps": {name: app.to_dict() for name, app in self.apps.items()}}
        with self.data_file.open("w", encoding="utf-8") as target:
            json.dump(payload, target, indent=2)

    def get_tracked_apps(self) -> Dict[str, GameApp]:
        return {name: app for name, app in self.apps.items() if app.is_tracking}

    def add_or_track_app(
        self,
        process_name: str,
        display_name: str | None = None,
        category: str = DEFAULT_CATEGORY,
        color_tag: str = DEFAULT_COLOR_TAG,
    ) -> GameApp:
        key = process_name.lower()
        if key in self.apps:
            app = self.apps[key]
            app.is_tracking = True
            if display_name:
                app.display = display_name
            app.category = category
            app.color_tag = color_tag
        else:
            candidate_display = display_name or Path(key).stem
            app = GameApp(
                name=key,
                display=candidate_display,
                total_time=0,
                is_tracking=True,
                category=category,
                color_tag=color_tag,
            )
            self.apps[key] = app
        self.save()
        return app

    def remove_app(self, process_name: str) -> None:
        key = process_name.lower()
        app = self.apps.get(key)
        if not app:
            return
        app.is_tracking = False
        self.save()

    def save_settings(self, settings: Dict[str, str]) -> None:
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with SETTINGS_FILE.open("w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

    def load_settings(self) -> Dict[str, str]:
        if not SETTINGS_FILE.exists():
            return {}
        try:
            with SETTINGS_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
