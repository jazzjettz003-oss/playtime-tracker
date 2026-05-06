from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "data.json"

WINDOW_GEOMETRY = "760x520"
TRACKER_INTERVAL_SECONDS = 1
FONT_FAMILY = "Segoe UI Variable Display"

NO_APPS_MESSAGE = "No tracked apps yet. Scan a running process to start tracking."
