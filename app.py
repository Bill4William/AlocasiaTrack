import os
import sys
import webbrowser

import customtkinter as ctk
from views.dashboard   import DashboardView
from views.stock_view  import StockView
from views.plants_view import PlantsView
from views.species_view import SpeciesView
from views.sales_view  import SalesView
from views.settings_view import SettingsView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

NAV_ITEMS = [
    ("Dashboard",     "dashboard"),
    ("Stock",         "stock"),
    ("Mother Plants", "plants"),
    ("Species",       "species"),
    ("Sales",         "sales"),
]

VIEW_MAP = {
    "dashboard": DashboardView,
    "stock":     StockView,
    "plants":    PlantsView,
    "species":   SpeciesView,
    "sales":     SalesView,
    "settings":  SettingsView,
}


class AlocasiaTrackApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AlocasiaTrack")
        self.geometry("1280x800")
        self.minsize(1000, 640)
        self._set_icon()

        self._setup_layout()
        self._create_sidebar()
        self._create_content_area()
        self._show_view("dashboard")

    # ----------------------------------------------------------------- layout
    def _setup_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=210, corner_radius=0,
                               fg_color=("gray92", "gray14"))
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # Logo
        logo = ctk.CTkLabel(
            sidebar,
            text="AlocasiaTrack",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=("gray20", "white"),
        )
        logo.grid(row=0, column=0, padx=20, pady=(22, 4), sticky="w")

        sub = ctk.CTkLabel(
            sidebar,
            text="Plant Inventory",
            font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray55"),
        )
        sub.grid(row=1, column=0, padx=20, pady=(0, 16), sticky="w")

        sep = ctk.CTkFrame(sidebar, height=1, fg_color=("gray80", "gray30"))
        sep.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 8))

        self._nav_btns: dict[str, ctk.CTkButton] = {}
        for i, (label, key) in enumerate(NAV_ITEMS, start=3):
            btn = ctk.CTkButton(
                sidebar, text=label, anchor="w",
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                hover_color=("gray80", "gray28"),
                text_color=("gray20", "gray90"),
                corner_radius=8,
                command=lambda k=key: self._show_view(k),
            )
            btn.grid(row=i, column=0, padx=10, pady=2, sticky="ew")
            self._nav_btns[key] = btn

        # Separator before Settings
        sep2 = ctk.CTkFrame(sidebar, height=1, fg_color=("gray80", "gray30"))
        sep2.grid(row=len(NAV_ITEMS) + 3, column=0, sticky="ew",
                  padx=12, pady=(8, 4))

        settings_btn = ctk.CTkButton(
            sidebar, text="Settings", anchor="w",
            font=ctk.CTkFont(size=13),
            fg_color="transparent",
            hover_color=("gray80", "gray28"),
            text_color=("gray20", "gray90"),
            corner_radius=8,
            command=lambda: self._show_view("settings"),
        )
        settings_btn.grid(row=len(NAV_ITEMS) + 4, column=0,
                          padx=10, pady=2, sticky="ew")
        self._nav_btns["settings"] = settings_btn

        # Spacer
        sidebar.grid_rowconfigure(len(NAV_ITEMS) + 5, weight=1)

        # Help button
        ctk.CTkButton(
            sidebar, text="? Help / Manual", anchor="w",
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color=("gray80", "gray28"),
            text_color=("gray40", "gray60"),
            corner_radius=8,
            command=self._open_manual,
        ).grid(row=len(NAV_ITEMS) + 6, column=0, padx=10, pady=(0, 2), sticky="ew")

        ver = ctk.CTkLabel(
            sidebar, text="v1.0",
            font=ctk.CTkFont(size=10),
            text_color=("gray60", "gray50"),
        )
        ver.grid(row=len(NAV_ITEMS) + 7, column=0, padx=20, pady=(0, 16), sticky="w")

    def _create_content_area(self):
        self._content = ctk.CTkFrame(self, corner_radius=0,
                                     fg_color=("gray95", "gray13"))
        self._content.grid(row=0, column=1, sticky="nsew")
        self._content.grid_columnconfigure(0, weight=1)
        self._content.grid_rowconfigure(0, weight=1)

        self._views:       dict[str, ctk.CTkFrame] = {}
        self._current_key: str | None = None

    # ----------------------------------------------------------------- icon
    def _set_icon(self):
        try:
            if hasattr(sys, "_MEIPASS"):
                path = os.path.join(sys._MEIPASS, "icon.ico")
            else:
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "icon.ico")
            if os.path.exists(path):
                self.iconbitmap(path)
        except Exception:
            pass  # non-fatal — fall back to default CTk icon

    # ----------------------------------------------------------------- help
    def _open_manual(self):
        if hasattr(sys, "_MEIPASS"):
            path = os.path.join(sys._MEIPASS, "docs", "manual.html")
        else:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "docs", "manual.html")
        webbrowser.open(f"file:///{path.replace(os.sep, '/')}")

    # ----------------------------------------------------------------- routing
    def _show_view(self, key: str):
        # Highlight active nav button
        active_color = ("gray78", "gray30")
        for k, btn in self._nav_btns.items():
            btn.configure(fg_color=active_color if k == key else "transparent")

        # Hide current view
        if self._current_key and self._current_key in self._views:
            self._views[self._current_key].grid_remove()

        # Create view on first visit
        if key not in self._views and key in VIEW_MAP:
            view = VIEW_MAP[key](self._content)
            view.grid(row=0, column=0, sticky="nsew")
            self._views[key] = view

        # Show and refresh
        if key in self._views:
            self._views[key].grid()
            if hasattr(self._views[key], "refresh"):
                self._views[key].refresh()

        self._current_key = key
