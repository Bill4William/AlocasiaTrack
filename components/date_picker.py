"""
DatePickerEntry — a CustomTkinter compound widget.

Provides a text entry + calendar-icon button that opens a month-view
calendar popup for picking a date.

Usage:
    dp = DatePickerEntry(parent)
    dp.pack(fill="x")
    dp.set("2025-06-15")   # pre-populate
    value = dp.get()       # "YYYY-MM-DD" string, or "" if blank
    dp.insert(0, "2025-01-01")  # compatible with CTkEntry interface
    dp.delete(0, "end")
"""

from __future__ import annotations

import calendar
import tkinter as tk
import customtkinter as ctk
from datetime import date, datetime


_MONTH_NAMES  = [calendar.month_name[m] for m in range(1, 13)]
_DAY_ABBREVS  = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


class DatePickerEntry(ctk.CTkFrame):

    # ── construction ──────────────────────────────────────────────────────────

    def __init__(self, parent, **frame_kwargs):
        super().__init__(parent, fg_color="transparent", **frame_kwargs)
        self._popup: tk.Toplevel | None = None
        self._view_year  = date.today().year
        self._view_month = date.today().month
        self._build()

    # ── public API (mirrors CTkEntry interface) ────────────────────────────────

    def get(self) -> str:
        return self._var.get().strip()

    def set(self, value: str):
        self._var.set(value or "")

    def insert(self, _index, value: str):
        self._var.set(value or "")

    def delete(self, _first, _last=None):
        self._var.set("")

    def configure(self, **kw):
        # Forward state/width changes to the inner entry
        if "state" in kw:
            self._entry.configure(state=kw.pop("state"))
        super().configure(**kw)

    # ── build ─────────────────────────────────────────────────────────────────

    def _build(self):
        self.grid_columnconfigure(0, weight=1)

        self._var = ctk.StringVar()
        self._entry = ctk.CTkEntry(
            self,
            textvariable=self._var,
            placeholder_text="YYYY-MM-DD",
        )
        self._entry.grid(row=0, column=0, sticky="ew")

        self._btn = ctk.CTkButton(
            self, text="📅", width=36,
            fg_color=("gray78", "gray28"),
            hover_color=("gray68", "gray22"),
            command=self._toggle_calendar,
        )
        self._btn.grid(row=0, column=1, padx=(2, 0))

    # ── calendar popup ────────────────────────────────────────────────────────

    def _toggle_calendar(self):
        if self._popup and self._popup.winfo_exists():
            self._close()
            return
        self._open_calendar()

    def _open_calendar(self):
        # Seed viewing position from current value if valid
        try:
            d = datetime.strptime(self._var.get().strip(), "%Y-%m-%d").date()
            self._view_year  = d.year
            self._view_month = d.month
        except ValueError:
            today = date.today()
            self._view_year  = today.year
            self._view_month = today.month

        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 4

        self._popup = tk.Toplevel(self)
        self._popup.wm_overrideredirect(True)
        self._popup.wm_attributes("-topmost", True)
        self._popup.wm_geometry(f"+{x}+{y}")
        self._popup.configure(bg="#1e1e1e")

        self._cal_root = ctk.CTkFrame(
            self._popup, corner_radius=10,
            border_width=1, border_color=("gray70", "gray30"),
        )
        self._cal_root.pack(padx=2, pady=2)

        self._draw_month()

        # Click-outside to close
        root = self.winfo_toplevel()
        self._click_tag = root.bind("<Button-1>", self._on_root_click, add="+")

    def _close(self):
        if self._popup and self._popup.winfo_exists():
            try:
                self.winfo_toplevel().unbind("<Button-1>", self._click_tag)
            except Exception:
                pass
            self._popup.destroy()
            self._popup = None

    def _draw_month(self):
        for w in self._cal_root.winfo_children():
            w.destroy()

        month_lbl = f"{_MONTH_NAMES[self._view_month - 1]}  {self._view_year}"

        # ── header row ───────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self._cal_root, fg_color="transparent")
        hdr.pack(fill="x", padx=10, pady=(10, 4))

        ctk.CTkButton(
            hdr, text="◀", width=28, height=28,
            fg_color="transparent",
            hover_color=("gray80", "gray28"),
            command=self._prev_month,
        ).pack(side="left")

        ctk.CTkLabel(
            hdr, text=month_lbl,
            font=ctk.CTkFont(size=13, weight="bold"),
            width=160, anchor="center",
        ).pack(side="left", expand=True, fill="x")

        ctk.CTkButton(
            hdr, text="▶", width=28, height=28,
            fg_color="transparent",
            hover_color=("gray80", "gray28"),
            command=self._next_month,
        ).pack(side="right")

        # ── day-of-week header ────────────────────────────────────────────────
        dow_row = ctk.CTkFrame(self._cal_root, fg_color="transparent")
        dow_row.pack(fill="x", padx=8, pady=(0, 2))
        for abbr in _DAY_ABBREVS:
            ctk.CTkLabel(
                dow_row, text=abbr,
                width=34, height=22, anchor="center",
                font=ctk.CTkFont(size=11),
                text_color=("gray55", "gray55"),
            ).pack(side="left")

        # ── day grid ──────────────────────────────────────────────────────────
        grid = ctk.CTkFrame(self._cal_root, fg_color="transparent")
        grid.pack(fill="x", padx=8, pady=(0, 10))

        today = date.today()
        try:
            sel = datetime.strptime(self._var.get().strip(), "%Y-%m-%d").date()
        except ValueError:
            sel = None

        for week in calendar.monthcalendar(self._view_year, self._view_month):
            row = ctk.CTkFrame(grid, fg_color="transparent")
            row.pack()
            for day in week:
                if day == 0:
                    ctk.CTkLabel(row, text="", width=34, height=32).pack(side="left")
                    continue

                d = date(self._view_year, self._view_month, day)
                is_sel   = sel is not None and d == sel
                is_today = d == today

                if is_sel:
                    fg    = "#2a7a3a"
                    hover = "#1e5e2c"
                    tc    = "white"
                elif is_today:
                    fg    = ("gray75", "gray32")
                    hover = ("gray65", "gray28")
                    tc    = ("#1f6aa5", "#6ab8ff")
                else:
                    fg    = "transparent"
                    hover = ("gray80", "gray26")
                    tc    = ("gray10", "gray90")

                ctk.CTkButton(
                    row, text=str(day), width=34, height=32,
                    fg_color=fg, hover_color=hover, text_color=tc,
                    corner_radius=6,
                    font=ctk.CTkFont(weight="bold" if is_sel or is_today else "normal"),
                    command=lambda _d=d: self._pick(_d),
                ).pack(side="left", padx=0, pady=1)

        # ── "Today" shortcut ─────────────────────────────────────────────────
        ctk.CTkButton(
            self._cal_root, text="Today",
            fg_color="transparent",
            hover_color=("gray80", "gray26"),
            text_color=("gray45", "gray65"),
            height=26,
            font=ctk.CTkFont(size=11),
            command=lambda: self._pick(date.today()),
        ).pack(pady=(0, 6))

        self._popup.update_idletasks()

    def _prev_month(self):
        if self._view_month == 1:
            self._view_month = 12
            self._view_year -= 1
        else:
            self._view_month -= 1
        self._draw_month()

    def _next_month(self):
        if self._view_month == 12:
            self._view_month = 1
            self._view_year += 1
        else:
            self._view_month += 1
        self._draw_month()

    def _pick(self, d: date):
        self._var.set(d.strftime("%Y-%m-%d"))
        self._close()

    def _on_root_click(self, event):
        if not (self._popup and self._popup.winfo_exists()):
            return
        px, py = self._popup.winfo_rootx(), self._popup.winfo_rooty()
        pw, ph = self._popup.winfo_width(), self._popup.winfo_height()
        bx, by = self._btn.winfo_rootx(), self._btn.winfo_rooty()
        bw, bh = self._btn.winfo_width(), self._btn.winfo_height()
        in_popup = px <= event.x_root <= px + pw and py <= event.y_root <= py + ph
        in_btn   = bx <= event.x_root <= bx + bw and by <= event.y_root <= by + bh
        if not in_popup and not in_btn:
            self._close()
