from pathlib import Path

# Create a permanent, hidden folder in the user's Home directory (e.g., C:\Users\Ryzn\.playtime_tracker)
APP_DIR = Path.home() / ".playtime_tracker"
DATA_FILE = APP_DIR / "data.json"

# --- Keep the rest of your variables the same below this line ---
WINDOW_GEOMETRY = "760x520"
TRACKER_INTERVAL_SECONDS = 1
FONT_FAMILY = "Segoe UI Variable Display"

PRIMARY_ACCENT = "#7b2cbf"
HOVER_ACCENT = "#5a189a"
CARD_BG = "#0a0a0a"
ROOT_BG = "#000000"

ACTIVE_COLOR = "#00c896"
IDLE_COLOR = "#9d4edd"
ACCENT_NAMES = {
    "Purple": "#7b2cbf",
    "Blue": "#0ea5e9",
    "Amber": "#f59e0b",
    "Red": "#ef4444",
    "Green": "#10b981",
}
CATEGORY_OPTIONS = ["General", "Game", "Work", "Creative", "Other"]
WINDOW_MIN_SIZE = (600, 400)

NO_APPS_MESSAGE = "No tracked apps yet. Scan a running process to start tracking."