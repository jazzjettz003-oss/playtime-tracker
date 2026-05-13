import io
import os
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Dict, Optional

import customtkinter as ctk
import psutil

try:
    from icoextract import IconExtractor
    from PIL import Image
    ICON_SUPPORT = True
except ImportError:
    ICON_SUPPORT = False

from .config import (
    ACTIVE_COLOR,
    ACTIVE_STATUS_TEXT,
    ACCENT_HOVER_MAP,
    ACCENT_NAMES,
    APP_TITLE,
    BUTTON_ADD_TEXT,
    BUTTON_SCAN_TEXT,
    BUTTON_SETTINGS_TEXT,
    CARD_BG,
    CATEGORY_OPTIONS,
    FONT_FAMILY,
    IDLE_COLOR,
    IDLE_STATUS_TEXT,
    NO_APPS_MESSAGE,
    PRIMARY_ACCENT,
    REMOVE_BUTTON_TEXT,
    RESET_BUTTON_TEXT,
    ROOT_BG,
    SCAN_POPUP_TITLE,
    SCAN_WINDOW_GEOMETRY,
    SETTINGS_POPUP_TITLE,
    SETTINGS_WINDOW_GEOMETRY,
    TRACKER_INTERVAL_SECONDS,
    WINDOW_GEOMETRY,
    WINDOW_MIN_SIZE,
)
from .data_manager import DataManager
from .model import GameApp
from .tracker import TrackerEngine


class TrackerUI(ctk.CTk):
    """Tkinter UI for the playtime tracker application."""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_GEOMETRY)
        self.resizable(True, True)
        self.minsize(*WINDOW_MIN_SIZE)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color=ROOT_BG)

        self.data_manager = DataManager()
        self.tracker: Optional[TrackerEngine] = None
        self.app_widgets: Dict[str, Dict[str, ctk.CTkLabel]] = {}
        self.update_id = None
        self.current_accent = PRIMARY_ACCENT
        self.current_hover = ACCENT_HOVER_MAP.get(PRIMARY_ACCENT, PRIMARY_ACCENT)

        saved = self.data_manager.load_settings()
        if saved.get("accent"):
            self.current_accent = saved["accent"]
            self.current_hover = saved.get("hover", ACCENT_HOVER_MAP.get(self.current_accent, self.current_accent))

        self._build_ui()
        self._start_tracker()
        self._update_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _build_ui(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            self.main_frame,
            text=APP_TITLE,
            font=ctk.CTkFont(family=FONT_FAMILY, size=32, weight="bold"),
            text_color="#ffffff",
        )
        header.grid(row=0, column=0, pady=(24, 6), sticky="w")

        self.summary_label = ctk.CTkLabel(
            self.main_frame,
            text="Total tracked: 0h 0m",
            font=ctk.CTkFont(size=13),
            text_color=self.current_accent,
        )
        self.summary_label.grid(row=1, column=0, pady=(0, 14), sticky="e")

        action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=15)
        action_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        action_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.scan_button = ctk.CTkButton(
            action_frame,
            text=BUTTON_SCAN_TEXT,
            command=self._scan_running_apps,
            fg_color=self.current_accent,
            hover_color=self.current_hover,
            border_width=1,
            border_color=self.current_accent,
        )
        self.scan_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = ctk.CTkButton(
            action_frame,
            text=BUTTON_ADD_TEXT,
            command=self._add_app,
            fg_color=self.current_accent,
            hover_color=self.current_hover,
            border_width=1,
            border_color=self.current_accent,
        )
        self.add_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.settings_button = ctk.CTkButton(
            action_frame,
            text=BUTTON_SETTINGS_TEXT,
            command=self._open_settings,
            fg_color="transparent",
            hover_color=self.current_hover,
            border_width=1,
            border_color=self.current_accent,
            text_color="#d4d4d4",
        )
        self.settings_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.app_list_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=15, fg_color="transparent")
        self.app_list_frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.app_list_frame.grid_columnconfigure(0, weight=1)

        self._refresh_app_list()

    def _add_app(self) -> None:
        path = filedialog.askopenfilename(
            title="Select App Executable",
            filetypes=[("Windows Executable", "*.exe")],
        )
        if not path:
            return

        process_name = os.path.basename(path).lower()
        display_name = Path(path).stem
        self._track_process(process_name, display_name)

    def _scan_running_apps(self) -> None:
        process_items = self._get_running_processes()
        if not process_items:
            messagebox.showinfo(SCAN_POPUP_TITLE, "No running processes were found.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title(SCAN_POPUP_TITLE)
        popup.geometry(SCAN_WINDOW_GEOMETRY)
        popup.transient(self)
        popup.grab_set()
        popup.grid_rowconfigure(0, weight=1)
        popup.grid_columnconfigure(0, weight=1)

        list_frame = ctk.CTkScrollableFrame(popup, corner_radius=15)
        list_frame.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)

        for index, (process_name, display_name) in enumerate(process_items):
            track_button = ctk.CTkButton(
                list_frame,
                text=f"{display_name} ({process_name})",
                anchor="w",
                command=lambda p=process_name, d=display_name: self._track_process(p, d, popup),
                fg_color=self.current_accent,
                hover_color=self.current_hover,
                border_width=1,
                border_color=self.current_accent,
            )
            track_button.grid(row=index, column=0, sticky="ew", pady=4, padx=8)

    def _get_running_processes(self) -> list[tuple[str, str]]:
        processes: Dict[str, str] = {}
        for proc in psutil.process_iter(["name"]):
            try:
                name = proc.info.get("name")
                if name:
                    key = name.lower()
                    processes[key] = Path(name).stem
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return sorted(processes.items(), key=lambda item: item[1].lower())

    def _build_process_exe_map(self) -> Dict[str, str]:
        process_exes: Dict[str, str] = {}
        for proc in psutil.process_iter(["name", "exe"]):
            try:
                name = proc.info.get("name")
                exe_path = proc.info.get("exe")
                if name and exe_path:
                    lower_name = name.lower()
                    if lower_name not in process_exes:
                        process_exes[lower_name] = exe_path
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return process_exes

    def _open_settings(self) -> None:
        popup = ctk.CTkToplevel(self)
        popup.title(SETTINGS_POPUP_TITLE)
        popup.geometry(SETTINGS_WINDOW_GEOMETRY)
        popup.transient(self)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Accent Colour", font=ctk.CTkFont(size=13)).pack(pady=(20, 4))
        accent_var = ctk.StringVar(value=next((k for k, v in ACCENT_NAMES.items() if v == self.current_accent), "Purple"))
        accent_menu = ctk.CTkOptionMenu(popup, values=list(ACCENT_NAMES.keys()), variable=accent_var)
        accent_menu.pack(pady=4)

        def apply() -> None:
            chosen = ACCENT_NAMES[accent_var.get()]
            self.current_accent = chosen
            self.current_hover = ACCENT_HOVER_MAP.get(chosen, chosen)
            self.data_manager.save_settings({
                "accent": self.current_accent,
                "hover": self.current_hover,
            })
            self._update_accent_ui()
            self._refresh_app_list()
            popup.destroy()

        ctk.CTkButton(
            popup,
            text="Apply",
            command=apply,
            fg_color=self.current_accent,
            hover_color=self.current_hover,
        ).pack(pady=20)

    def _remove_app(self, process_name: str) -> None:
        self.data_manager.remove_app(process_name)
        self._refresh_app_list()
        if self.tracker:
            self.tracker.update_apps(self.data_manager.get_tracked_apps())

    def _get_app_icon(self, process_name: str, process_exe_map: Dict[str, str]) -> Optional[ctk.CTkImage]:
        if not ICON_SUPPORT:
            return None
        exe_path = process_exe_map.get(process_name.lower())
        if not exe_path:
            return None
        try:
            extractor = IconExtractor(exe_path)
            data = extractor.get_icon()
            image_data = data if hasattr(data, "read") else io.BytesIO(data)
            img = Image.open(image_data).convert("RGBA").resize((24, 24), Image.LANCZOS)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
        except Exception as exc:
            print(f"[icon] failed for {process_name}: {exc}")
            return None

    def _update_accent_ui(self) -> None:
        for btn in [self.scan_button, self.add_button]:
            btn.configure(
                fg_color=self.current_accent,
                hover_color=self.current_hover,
                border_color=self.current_accent,
            )
        self.settings_button.configure(
            hover_color=self.current_hover,
            border_color=self.current_accent,
        )
        self.summary_label.configure(text_color=self.current_accent)

    def _reset_timer(self, process_name: str) -> None:
        app = self.data_manager.apps.get(process_name)
        if not app:
            return
        app.total_time = 0
        self.data_manager.save()
        if process_name in self.app_widgets:
            self.app_widgets[process_name]["time_label"].configure(text=self._format_seconds(app.total_time))

    def _track_process(self, process_name: str, display_name: Optional[str] = None, popup=None) -> None:
        self.data_manager.add_or_track_app(process_name, display_name, category=CATEGORY_OPTIONS[0], color_tag=self.current_accent)
        self._refresh_app_list()
        if self.tracker:
            self.tracker.update_apps(self.data_manager.get_tracked_apps())
        if popup:
            popup.destroy()

    def _refresh_app_list(self) -> None:
        for widget in self.app_list_frame.winfo_children():
            widget.destroy()
        self.app_widgets.clear()

        apps = self.data_manager.get_tracked_apps()
        if not apps:
            empty = ctk.CTkLabel(self.app_list_frame, text=NO_APPS_MESSAGE, fg_color="transparent")
            empty.grid(padx=20, pady=20)
            return

        process_exe_map = self._build_process_exe_map()
        for row_index, (process_name, app) in enumerate(sorted(apps.items())):
            self.create_app_card(process_name, app, row_index, process_exe_map)

    def create_app_card(self, process_name: str, app: GameApp, row_index: int, process_exe_map: Dict[str, str]) -> None:
        time_str = self._format_seconds(app.total_time)
        row = ctk.CTkFrame(
            self.app_list_frame,
            fg_color=CARD_BG,
            border_width=1,
            border_color=self.current_accent,
            corner_radius=25,
        )
        row.grid(row=row_index, column=0, padx=12, pady=10, sticky="ew")
        row.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        row.grid_rowconfigure(1, minsize=24)

        name_label = ctk.CTkLabel(
            row,
            text=app.display,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff",
        )
        icon_image = self._get_app_icon(process_name, process_exe_map)
        if icon_image:
            icon_label = ctk.CTkLabel(row, text="", image=icon_image)
            icon_label.grid(row=0, column=0, padx=(14, 4), pady=16, sticky="w")
            name_label.grid(row=0, column=0, padx=(46, 0), pady=16, sticky="w")
        else:
            name_label.grid(row=0, column=0, padx=18, pady=16, sticky="w")

        time_label = ctk.CTkLabel(row, text=time_str, font=ctk.CTkFont(size=15), text_color="#d4d4d4")
        time_label.grid(row=0, column=2, padx=18, pady=16, sticky="e")

        category_label = ctk.CTkLabel(
            row,
            text=f"#{app.category.lower()}",
            font=ctk.CTkFont(size=10),
            text_color="#666666",
        )
        category_label.grid(row=1, column=0, padx=18, pady=(0, 16), sticky="w")

        status_label = ctk.CTkLabel(row, text=IDLE_STATUS_TEXT, font=ctk.CTkFont(size=11), text_color=IDLE_COLOR)
        status_label.grid(row=1, column=2, columnspan=2, padx=10, pady=(0, 14), sticky="e")

        reset_button = ctk.CTkButton(
            row,
            text=RESET_BUTTON_TEXT,
            width=70,
            height=30,
            command=lambda p=process_name: self._reset_timer(p),
            fg_color="transparent",
            hover_color="#444444",
            text_color="#d4d4d4",
        )
        reset_button.grid(row=0, column=3, padx=(0, 4), pady=16, sticky="e")

        remove_button = ctk.CTkButton(
            row,
            text=REMOVE_BUTTON_TEXT,
            width=30,
            height=30,
            command=lambda p=process_name: self._remove_app(p),
            fg_color="transparent",
            hover_color="#ff4444",
            text_color="#ff6666",
        )
        remove_button.grid(row=0, column=4, padx=(0, 10), pady=16, sticky="e")

        self.app_widgets[process_name] = {"time_label": time_label, "status_label": status_label}

    def _update_ui(self) -> None:
        active_map = self.tracker.get_active_state() if self.tracker else {}
        for process_name, widgets in self.app_widgets.items():
            app = self.data_manager.apps.get(process_name)
            if not app:
                continue
            widgets["time_label"].configure(text=self._format_seconds(app.total_time))
            if active_map.get(process_name):
                widgets["status_label"].configure(text=ACTIVE_STATUS_TEXT, text_color=ACTIVE_COLOR)
            else:
                widgets["status_label"].configure(text=IDLE_STATUS_TEXT, text_color=IDLE_COLOR)

        total_tracked = sum(app.total_time for app in self.data_manager.get_tracked_apps().values())
        self.summary_label.configure(text=f"Total tracked: {self._format_seconds(total_tracked)}")
        self.update_id = self.after(TRACKER_INTERVAL_SECONDS * 1000, self._update_ui)

    def _format_seconds(self, seconds: int) -> str:
        """Format seconds into seconds/minutes/hours for display.

        - Under 60 seconds: show seconds only.
        - Under one hour: show minutes and seconds.
        - One hour or more: show hours and minutes.
        """
        # TODO: Consider returning "–" for 0 seconds to make never-run apps visually clearer.
        if seconds < 60:
            return f"{seconds}s"

        minutes = seconds // 60
        hours = minutes // 60
        minutes = minutes % 60
        if hours == 0:
            return f"{minutes}m {seconds % 60}s"
        return f"{hours}h {minutes}m"

    def _start_tracker(self) -> None:
        tracking_apps = self.data_manager.get_tracked_apps()
        self.tracker = TrackerEngine(tracking_apps)
        self.tracker.start()

    def on_closing(self) -> None:
        if hasattr(self, "update_id") and self.update_id:
            self.after_cancel(self.update_id)
        if self.tracker:
            self.tracker.stop()
        self.data_manager.save()
        self.destroy()
