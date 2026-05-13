from pathlib import Path
from typing import Dict, List

# Persistent user data directory and file path.
APP_DIR = Path.home() / ".playtime_tracker"
DATA_FILE = APP_DIR / "data.json"
SETTINGS_FILE = APP_DIR / "settings.json"

# Window layout and theme constants.
WINDOW_GEOMETRY = "760x520"
WINDOW_MIN_SIZE = (600, 400)
SCAN_WINDOW_GEOMETRY = "560x520"
SETTINGS_WINDOW_GEOMETRY = "400x200"
TRACKER_INTERVAL_SECONDS = 1
FONT_FAMILY = "Segoe UI Variable Display"

APP_TITLE = "Playtime Tracker"
BUTTON_SCAN_TEXT = "Scan Running Processes"
BUTTON_ADD_TEXT = "Add App Path"
BUTTON_SETTINGS_TEXT = "⚙ Settings"
SCAN_POPUP_TITLE = "Scan Running Processes"
SETTINGS_POPUP_TITLE = "Settings"
RESET_BUTTON_TEXT = "Reset"
REMOVE_BUTTON_TEXT = "X"
NO_APPS_MESSAGE = "No tracked apps yet. Scan a running process to start tracking."
ACTIVE_STATUS_TEXT = "● Active"
IDLE_STATUS_TEXT = "Idle"

PRIMARY_ACCENT = "#7b2cbf"
ACCENT_NAMES: Dict[str, str] = {
    "Purple": "#7b2cbf",
    "Blue": "#0ea5e9",
    "Amber": "#f59e0b",
    "Red": "#ef4444",
    "Green": "#10b981",
}
ACCENT_HOVER_MAP: Dict[str, str] = {
    "#7b2cbf": "#5a189a",
    "#0ea5e9": "#0284c7",
    "#f59e0b": "#d97706",
    "#ef4444": "#dc2626",
    "#10b981": "#059669",
}

CARD_BG = "#0a0a0a"
ROOT_BG = "#000000"
ACTIVE_COLOR = "#00c896"
IDLE_COLOR = "#9d4edd"
CATEGORY_OPTIONS: List[str] = ["General", "Game", "Work", "Creative", "Other"]
DEFAULT_CATEGORY = "General"
DEFAULT_COLOR_TAG = PRIMARY_ACCENT

# Documented accent palette and category options live here.
# Persistence is rooted at ~/.playtime_tracker/data.json.
