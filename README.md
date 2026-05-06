# Playtime Tracker

This repository contains a small Python application for tracking active Windows applications and recording their runtime.

## Architecture

The code is organized as a Python package under `src/` using a Model-View-Controller pattern:

- `src/model.py` defines the `GameApp` dataclass for app state and persistence conversion.
- `src/data_manager.py` encapsulates JSON storage, file verification, and app state updates.
- `src/tracker.py` contains the `TrackerEngine` background thread, which monitors running processes and updates app runtime.
- `src/ui.py` builds the `customtkinter` interface and forwards user actions to the data and tracker layers.

This separation keeps UI concerns out of the tracking engine and keeps persistence logic out of the view.

## Performance

This release is built as a zero-bloat, single-screen tracking dashboard. The UI is implemented purely in `customtkinter` with a hardcoded, high-contrast theme for consistent rendering and minimal runtime overhead. Runtime tracking is handled by a background thread, keeping the interface responsive while recording active app usage.

## Layout

- `main.py` is the application entry point.
- `src/` contains the package modules.
- `data/` stores runtime data in `data.json`.

## Installation

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

Run the application from the project root:

```bash
python main.py
```

## Notes

- `data/data.json` is excluded from version control because it stores local tracked app state.
- The app starts by loading persisted tracked apps and immediately builds the dashboard cards for any app with `is_tracking == True`.
