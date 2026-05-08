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

NO_APPS_MESSAGE = "No tracked apps yet. Scan a running process to start tracking."