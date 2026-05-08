# Playtime Tracker

A small desktop app for tracking how long Windows apps have been running.

It uses `psutil` to scan processes, stores runtime data in JSON, and renders a compact `customtkinter` dashboard.

## What it does

- Tracks selected apps by process name.
- Shows accumulated runtime per app.
- Updates the active/idle status live.
- Lets you add apps from a running process scan or by executable path.
- Includes a reset button on each card to zero the timer and persist the change.

## Project structure

- `main.py` — app entry point.
- `src/ui.py` — the Tkinter-based interface.
- `src/tracker.py` — background process tracker.
- `src/data_manager.py` — JSON persistence and app state.
- `src/model.py` — `GameApp` model.
- `data/` — persisted runtime state.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Notes

- The tracker keeps data in `data/data.json`.
- If the file is missing or malformed, it rebuilds a default state.
- Status updates are driven by a background tracker thread.

## TODO / Known issues

- Windows-only right now.
- Timer may drift if the system sleeps or the app is suspended.
- No export/import feature yet.
- No automatic app aliasing or metadata beyond process name.
- The UI is intentionally simple and not theme-configurable yet.
