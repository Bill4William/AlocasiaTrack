"""
SearchableDropdown — a CustomTkinter compound widget.

Replaces CTkOptionMenu wherever a large list needs to be searchable.
Supports:
  • Type-ahead filtering (substring match, case-insensitive)
  • Up/Down arrow key navigation
  • Enter to confirm, Escape to close
  • Click-outside to close
  • Optional "none" placeholder entry

Usage:
    dd = SearchableDropdown(parent, options={"Amazonica": 1, "Polly": 2},
                            placeholder="Search species…")
    dd.pack(fill="x")
    name = dd.get()       # display text currently shown
    id_  = dd.get_id()    # associated value (dict key → value)
    dd.set("Amazonica")   # pre-select by name
"""

from __future__ import annotations

import tkinter as tk
import customtkinter as ctk
from typing import Callable, Optional


class SearchableDropdown(ctk.CTkFrame):

    # ── construction ──────────────────────────────────────────────────────────

    def __init__(
        self,
        parent,
        options: dict | list | None = None,
        placeholder: str = "Search or select…",
        none_label: str | None = "— none —",
        on_select: Optional[Callable] = None,
        **frame_kwargs,
    ):
        super().__init__(parent, fg_color="transparent", **frame_kwargs)

        self._on_select   = on_select
        self._none_label  = none_label
        self._popup: Optional[tk.Toplevel] = None
        self._all_opts: dict = {}      # {display_name: id_value}
        self._filtered: list[str] = []
        self._list_btns: list[ctk.CTkButton] = []
        self._active_idx = -1

        # Current selection
        self._sel_text: str = none_label or ""
        self._sel_id          = None

        self.set_options(options or {})
        self._build(placeholder)
        self._bind_events()

    # ── public API ────────────────────────────────────────────────────────────

    def set_options(self, options: dict | list):
        if isinstance(options, dict):
            self._all_opts = dict(options)
        else:
            self._all_opts = {k: k for k in options}
        if self._none_label and self._none_label not in self._all_opts:
            self._all_opts = {self._none_label: None, **self._all_opts}

    def get(self) -> str:
        """Return the currently displayed/selected text."""
        return self._entry_var.get().strip()

    def get_id(self):
        """Return the ID associated with the current selection (None for 'none' entry)."""
        return self._sel_id

    def set(self, text: str, id_val=None):
        """Programmatically select an item by its display text."""
        self._sel_text = text
        self._sel_id   = id_val if id_val is not None else self._all_opts.get(text)
        self._entry_var.set(text)

    def clear(self):
        self._sel_text = self._none_label or ""
        self._sel_id   = None
        self._entry_var.set(self._sel_text)

    # ── internal build ────────────────────────────────────────────────────────

    def _build(self, placeholder: str):
        self.grid_columnconfigure(0, weight=1)

        self._entry_var = ctk.StringVar(value=self._sel_text)
        self._entry = ctk.CTkEntry(
            self,
            textvariable=self._entry_var,
            placeholder_text=placeholder,
        )
        self._entry.grid(row=0, column=0, sticky="ew")

        self._arrow_btn = ctk.CTkButton(
            self, text="▾", width=34,
            fg_color=("gray78", "gray28"),
            hover_color=("gray68", "gray22"),
            command=self._toggle_popup,
        )
        self._arrow_btn.grid(row=0, column=1, padx=(2, 0))

    def _bind_events(self):
        self._entry_var.trace_add("write", self._on_type)
        self._entry.bind("<FocusIn>",  self._on_focus_in)
        self._entry.bind("<FocusOut>", self._on_focus_out)
        self._entry.bind("<Escape>",   lambda _: self._close_popup())
        self._entry.bind("<Down>",     self._on_arrow_down)
        self._entry.bind("<Up>",       self._on_arrow_up)
        self._entry.bind("<Return>",   self._on_enter)

    # ── popup ─────────────────────────────────────────────────────────────────

    def _open_popup(self):
        if self._popup and self._popup.winfo_exists():
            self._reposition_popup()
            return

        self._refresh_filtered()
        if not self._filtered:
            return

        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 2
        w = self.winfo_width()
        rows = min(len(self._filtered), 10)
        h    = rows * 30 + 12

        self._popup = tk.Toplevel(self)
        self._popup.wm_overrideredirect(True)
        self._popup.wm_attributes("-topmost", True)
        self._popup.wm_geometry(f"{w}x{h}+{x}+{y}")

        # Outer border frame
        border = ctk.CTkFrame(self._popup, corner_radius=8, border_width=1,
                               border_color=("gray70", "gray30"))
        border.pack(fill="both", expand=True, padx=0, pady=0)

        # Scrollable inner list
        self._list_frame = ctk.CTkScrollableFrame(
            border, fg_color=("gray92", "gray14"),
            height=rows * 30, scrollbar_button_color=("gray70", "gray35"),
        )
        self._list_frame.pack(fill="both", expand=True, padx=1, pady=1)

        self._populate_list()
        self._active_idx = -1

        # Close when anything else in the root is clicked
        root = self.winfo_toplevel()
        self._click_tag = root.bind("<Button-1>", self._on_root_click, add="+")

    def _close_popup(self):
        if self._popup and self._popup.winfo_exists():
            try:
                root = self.winfo_toplevel()
                root.unbind("<Button-1>", self._click_tag)
            except Exception:
                pass
            self._popup.destroy()
            self._popup = None
        self._active_idx = -1

    def _toggle_popup(self):
        if self._popup and self._popup.winfo_exists():
            self._close_popup()
        else:
            self._open_popup()
        self._entry.focus_set()

    def _reposition_popup(self):
        """Keep popup aligned if parent dialog is moved."""
        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 2
        w = self.winfo_width()
        rows = min(len(self._filtered), 10)
        h    = rows * 30 + 12
        self._popup.wm_geometry(f"{w}x{h}+{x}+{y}")

    def _populate_list(self):
        for w in self._list_frame.winfo_children():
            w.destroy()
        self._list_btns = []
        for name in self._filtered:
            is_none = (name == self._none_label)
            btn = ctk.CTkButton(
                self._list_frame,
                text=name,
                anchor="w",
                fg_color="transparent",
                hover_color=("gray80", "gray25"),
                text_color=("gray50", "gray55") if is_none else ("gray10", "gray90"),
                height=28,
                font=ctk.CTkFont(slant="italic") if is_none else ctk.CTkFont(),
                command=lambda n=name: self._select(n),
            )
            btn.pack(fill="x", padx=4, pady=1)
            self._list_btns.append(btn)

    def _refresh_filtered(self):
        q = self._entry_var.get().strip().lower()
        # When query is empty or matches the none-label, show all
        if not q or q == (self._none_label or "").lower():
            self._filtered = list(self._all_opts.keys())
        else:
            self._filtered = [
                k for k in self._all_opts
                if q in k.lower() and k != self._none_label
            ]
            # Always keep none-label at top if it exists
            if self._none_label:
                self._filtered = [self._none_label] + self._filtered

    def _select(self, name: str):
        self._sel_text = name
        self._sel_id   = self._all_opts.get(name)
        self._entry_var.set(name)
        self._close_popup()
        if self._on_select:
            self._on_select(name, self._sel_id)

    # ── event handlers ────────────────────────────────────────────────────────

    def _on_type(self, *_):
        typed = self._entry_var.get()
        # If text differs from the last confirmed selection, reset selection state
        if typed != self._sel_text:
            # Don't clear _sel_text if user is backspacing into a valid name
            if typed not in self._all_opts:
                self._sel_id = None
            self._refresh_filtered()
            if self._filtered:
                if self._popup and self._popup.winfo_exists():
                    self._populate_list()
                    self._reposition_popup()
                else:
                    self._open_popup()
            else:
                self._close_popup()

    def _on_focus_in(self, _event):
        self._open_popup()

    def _on_focus_out(self, _event):
        # Delay close so popup button clicks can register first
        self.after(150, self._maybe_close)

    def _maybe_close(self):
        # Only close if focus has truly left our widget AND the popup
        focused = self.focus_get()
        if focused is None:
            self._close_popup()
            return
        # Check if focused widget is inside our popup
        if self._popup and self._popup.winfo_exists():
            try:
                if str(focused).startswith(str(self._popup)):
                    return
            except Exception:
                pass
        self._close_popup()

    def _on_root_click(self, event):
        """Close popup when user clicks outside both the entry and the popup."""
        if self._popup and self._popup.winfo_exists():
            px, py = self._popup.winfo_rootx(), self._popup.winfo_rooty()
            pw, ph = self._popup.winfo_width(), self._popup.winfo_height()
            in_popup = (px <= event.x_root <= px + pw and
                        py <= event.y_root <= py + ph)
            in_self  = (self.winfo_rootx() <= event.x_root <= self.winfo_rootx() + self.winfo_width() and
                        self.winfo_rooty() <= event.y_root <= self.winfo_rooty() + self.winfo_height())
            if not in_popup and not in_self:
                self._close_popup()

    def _on_arrow_down(self, _event):
        if not (self._popup and self._popup.winfo_exists()):
            self._open_popup()
            return "break"
        self._active_idx = min(self._active_idx + 1, len(self._filtered) - 1)
        self._highlight()
        return "break"

    def _on_arrow_up(self, _event):
        self._active_idx = max(self._active_idx - 1, 0)
        self._highlight()
        return "break"

    def _on_enter(self, _event):
        if 0 <= self._active_idx < len(self._filtered):
            self._select(self._filtered[self._active_idx])
        return "break"

    def _highlight(self):
        for i, btn in enumerate(self._list_btns):
            if i == self._active_idx:
                btn.configure(fg_color=("gray70", "gray32"))
            else:
                btn.configure(fg_color="transparent")
