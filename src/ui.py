import os
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from .config import FONT_FAMILY, NO_APPS_MESSAGE, WINDOW_GEOMETRY
from .data_manager import DataManager
from .tracker import TrackerEngine

PRIMARY_ACCENT = "#7b2cbf"
HOVER_ACCENT = "#5a189a"
CARD_BG = "#0a0a0a"
ROOT_BG = "#000000"


class TrackerUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Game & App Playtime Tracker")
        self.geometry(WINDOW_GEOMETRY)
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color=ROOT_BG)

        self.data_manager = DataManager()
        self.tracker = None
        self.app_widgets = {}
        self.update_id = None

        self._build_ui()
        self._start_tracker()
        self._update_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=24, pady=24, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            self.main_frame,
            text="Game & App Playtime Tracker",
            font=ctk.CTkFont(family=FONT_FAMILY, size=32, weight="bold"),
            text_color="#ffffff",
        )
        header.grid(row=0, column=0, pady=(24, 20), sticky="w")

        action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", corner_radius=15)
        action_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        action_frame.grid_columnconfigure((0, 1), weight=1)

        self.scan_button = ctk.CTkButton(
            action_frame,
            text="Scan Running Processes",
            command=self._scan_running_apps,
            fg_color=PRIMARY_ACCENT,
            hover_color=HOVER_ACCENT,
            border_width=1,
            border_color=PRIMARY_ACCENT,
        )
        self.scan_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = ctk.CTkButton(
            action_frame,
            text="Add App Path",
            command=self._add_app,
            fg_color=PRIMARY_ACCENT,
            hover_color=HOVER_ACCENT,
            border_width=1,
            border_color=PRIMARY_ACCENT,
        )
        self.add_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.app_list_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=15, fg_color="transparent")
        self.app_list_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.app_list_frame.grid_columnconfigure(0, weight=1)

        self._refresh_app_list()

    def _add_app(self):
        path = filedialog.askopenfilename(
            title="Select App Executable",
            filetypes=[("Windows Executable", "*.exe")],
        )
        if not path:
            return

        process_name = os.path.basename(path).lower()
        display_name = Path(path).stem
        self._track_process(process_name, display_name)

    def _scan_running_apps(self):
        process_items = self._get_running_processes()
        if not process_items:
            messagebox.showinfo("Scan Running Processes", "No running processes were found.")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Scan Running Processes")
        popup.geometry("560x520")
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
                fg_color=PRIMARY_ACCENT,
                hover_color=HOVER_ACCENT,
                border_width=1,
                border_color=PRIMARY_ACCENT,
            )
            track_button.grid(row=index, column=0, sticky="ew", pady=4, padx=8)

    def _get_running_processes(self):
        import psutil

        processes = {}
        for proc in psutil.process_iter(["name"]):
            try:
                name = proc.info.get("name")
                if name:
                    key = name.lower()
                    display_name = Path(name).stem
                    processes[key] = display_name
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return sorted(processes.items(), key=lambda item: item[1].lower())

    def _remove_app(self, process_name: str) -> None:
        self.data_manager.remove_app(process_name)
        self._refresh_app_list()
        if self.tracker:
            self.tracker.update_apps(self.data_manager.get_tracked_apps())

    def _track_process(self, process_name: str, display_name: str | None = None, popup=None) -> None:
        self.data_manager.add_or_track_app(process_name, display_name)
        self._refresh_app_list()
        if self.tracker:
            self.tracker.update_apps(self.data_manager.get_tracked_apps())
        if popup:
            popup.destroy()

    def _refresh_app_list(self):
        for widget in self.app_list_frame.winfo_children():
            widget.destroy()
        self.app_widgets.clear()

        apps = self.data_manager.get_tracked_apps()
        if not apps:
            empty = ctk.CTkLabel(self.app_list_frame, text=NO_APPS_MESSAGE, fg_color="transparent")
            empty.grid(padx=20, pady=20)
            return

        row_index = 0
        for process_name, app in sorted(apps.items()):
            self.create_app_card(process_name, app, row_index)
            row_index += 1

    def create_app_card(self, process_name: str, app, row_index: int) -> None:
        time_str = self._format_seconds(app.total_time)
        row = ctk.CTkFrame(
            self.app_list_frame,
            fg_color=CARD_BG,
            border_width=1,
            border_color=PRIMARY_ACCENT,
            corner_radius=25,
        )
        row.grid(row=row_index, column=0, padx=12, pady=10, sticky="ew")
        row.grid_columnconfigure((0, 1), weight=1)

        name_label = ctk.CTkLabel(
            row,
            text=app.display,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff",
        )
        name_label.grid(row=0, column=0, padx=18, pady=16, sticky="w")

        time_label = ctk.CTkLabel(row, text=time_str, font=ctk.CTkFont(size=15), text_color="#d4d4d4")
        time_label.grid(row=0, column=1, padx=18, pady=16, sticky="e")

        process_label = ctk.CTkLabel(
            row,
            text=process_name,
            font=ctk.CTkFont(size=11),
            text_color="#cbd5e1",
        )
        process_label.grid(row=1, column=0, padx=18, pady=(0, 16), sticky="w")

        status_label = ctk.CTkLabel(row, text="Idle", font=ctk.CTkFont(size=11), text_color="#9d4edd")
        status_label.grid(row=1, column=1, padx=18, pady=(0, 16), sticky="e")

        remove_button = ctk.CTkButton(
            row,
            text="X",
            width=30,
            height=30,
            command=lambda p=process_name: self._remove_app(p),
            fg_color="transparent",
            hover_color="#ff4444",
            text_color="#ff6666",
        )
        remove_button.grid(row=0, column=2, padx=10, pady=16, sticky="e")

        self.app_widgets[process_name] = {"time_label": time_label, "status_label": status_label}

    def _update_ui(self):
        active_map = self.tracker.active if self.tracker else {}
        for process_name, widgets in self.app_widgets.items():
            app = self.data_manager.apps.get(process_name)
            if not app:
                continue
            widgets["time_label"].configure(text=self._format_seconds(app.total_time))
            if active_map.get(process_name):
                widgets["status_label"].configure(text="● Active", text_color=PRIMARY_ACCENT)
            else:
                widgets["status_label"].configure(text="Idle", text_color="#9d4edd")

        self.update_id = self.after(1000, self._update_ui)

    def _format_seconds(self, seconds: int) -> str:
        minutes = seconds // 60
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}h {minutes}m"

    def _start_tracker(self):
        tracking_apps = self.data_manager.get_tracked_apps()
        self.tracker = TrackerEngine(tracking_apps)
        self.tracker.start()

    def on_closing(self):
        if hasattr(self, "update_id") and self.update_id:
            self.after_cancel(self.update_id)
        if self.tracker:
            self.tracker.stop()
        self.data_manager.save()
        self.destroy()
