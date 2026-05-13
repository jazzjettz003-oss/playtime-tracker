import threading
from typing import Dict, Set

import psutil

from .config import TRACKER_INTERVAL_SECONDS
from .model import GameApp


class TrackerEngine(threading.Thread):
    """Background tracker that increments runtime counters for active processes.

    The tracker runs in a separate daemon thread and updates GameApp.total_time
    while the Tkinter mainloop reads the active state through get_active_state().
    """

    def __init__(self, apps: Dict[str, GameApp], interval: int = TRACKER_INTERVAL_SECONDS):
        super().__init__(daemon=True)
        self.apps = apps
        self.interval = interval
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.active: Dict[str, bool] = {name: False for name in apps}

    def run(self) -> None:
        while not self._stop_event.wait(self.interval):
            self._tick()

    def _tick(self) -> None:
        active_names = self._get_running_names()
        active_state: Dict[str, bool] = {name: False for name in self.apps}

        with self._lock:
            for proc_name in active_names:
                if proc_name in self.apps:
                    self.apps[proc_name].total_time += self.interval
                    active_state[proc_name] = True
            self.active = active_state

    def _get_running_names(self) -> Set[str]:
        """Return the currently running process names in lowercase."""
        found: Set[str] = set()
        for proc in psutil.process_iter(["name"]):
            try:
                name = proc.info.get("name")
                if name:
                    found.add(name.lower())
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return found

    def get_active_state(self) -> Dict[str, bool]:
        """Return a copy of the active state map safely under the tracker lock."""
        with self._lock:
            return dict(self.active)

    def stop(self) -> None:
        self._stop_event.set()
        self.join(timeout=self.interval + 1)

    def update_apps(self, apps: Dict[str, GameApp]) -> None:
        with self._lock:
            self.apps = apps
            self.active = {name: self.active.get(name, False) for name in apps}
