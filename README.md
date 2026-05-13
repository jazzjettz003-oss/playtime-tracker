# Playtime Tracker

A privacy-first Windows desktop app to track game and app playtime locally.

> Suggested GitHub About: Privacy-first Windows desktop playtime tracker with local JSON persistence.
>
> **Social preview:** upload a 1280×640 image showing the app screenshot, title, and tagline.

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

## Overview

Playtime Tracker is a Windows desktop tool that records how long your apps and games run by process name or executable path.
It is built for local use, does not depend on a cloud service, and stores data under `~/.playtime_tracker/data.json`.

This project exists to make playtime tracking simple and privacy-friendly for non-Steam apps, work tools, creative apps, and general software.

## Features

- Track multiple apps by process name or executable path.
- Live active/idle detection for tracked apps.
- Reset any app timer instantly.
- Categories: General / Game / Work / Creative / Other.
- Accent color selection for a personalized dashboard.
- Local JSON persistence under `~/.playtime_tracker/data.json`.

## Screenshots

![Dashboard](assets/dashboard.png)

![Scan Running Processes](assets/scan.png)

> TODO: If the screenshot files are not present yet, add `assets/dashboard.png` and `assets/scan.png` with app screen captures.

## Quickstart

```bash
git clone https://github.com/yourname/playtime-tracker.git
cd playtime-tracker
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playtime_tracker
```

Once packaged, the app can also be installed and run with:

```bash
pip install .
playtime-tracker
```

> Note: This project is Windows-only and requires Python 3.10 or newer.

## Usage

- Scan running processes and add an app directly from the process list.
- Add any executable by path to track apps not currently running.
- Reset timers on individual app cards.
- Change accent color in Settings and see the selection persist across launches.
- Tracked apps continue saving data automatically to the local hidden folder.

## Project Structure

- `main.py` — thin app launcher.
- `playtime_tracker/` — package modules.
  - `__init__.py`
  - `__main__.py`
  - `config.py`
  - `data_manager.py`
  - `model.py`
  - `tracker.py`
  - `ui.py`
- `requirements.txt` — dependencies for development and execution.
- `pyproject.toml` — packaging metadata.
- `tests/` — automated unit tests.
- `assets/` — screenshot and preview images.
- `.github/` — issue, PR and CI templates.

## Contributing

- Open issues for bugs and feature requests.
- Submit pull requests with a clear summary and test coverage.
- Follow PEP 8, use type hints, and add docstrings for public classes and methods.
- Add tests for new behavior before merging.

## Roadmap / TODO

- Windows-only desktop app.
- Timer drift may occur while the system sleeps.
- No export/import support yet.
- Future ideas: activity reports, CSV export, per-app scheduling, multi-platform support.
