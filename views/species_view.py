import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from database.models import SpeciesModel
from dialogs.species_dialog import SpeciesDialog


def _apply_tree_style():
    style = ttk.Style()
    style.configure("Species.Treeview",
        background="#2b2b2b", foreground="white",
        rowheight=30, fieldbackground="#2b2b2b",
        borderwidth=0, font=("Segoe UI", 10))
    style.configure("Species.Treeview.Heading",
        background="#1a1a1a", foreground="#aaaaaa",
        relief="flat", font=("Segoe UI", 10, "bold"))
    style.map("Species.Treeview",
        background=[("selected", "#1f6aa5")],
        foreground=[("selected", "white")])
    style.map("Species.Treeview.Heading",
        background=[("active", "#2c2c2c")],
        foreground=[("active", "#ffffff")])


class SpeciesView(ctk.CTkFrame):

    COLS = (
        "Common Name",
        "Scientific / Cultivar Name",
        "Care Level",
        "Price Min",
        "Price Max",
        "In Stock",
        "Notes",
    )
    _COL_WIDTHS = [150, 210, 100, 85, 85, 70, 220]

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        _apply_tree_style()

        # ── state ──────────────────────────────────────────────────────────────
        self._raw: list[dict] = []      # full dataset, refreshed from DB
        self._search_q    = ""
        self._sort_col: str | None = None
        self._sort_rev    = False
        self._col_filters: dict[int, set] = {}   # {col_idx: {allowed_values}}
        self._filter_popup: tk.Toplevel | None = None

        self._build()
        self.refresh()

    # ── build ──────────────────────────────────────────────────────────────────

    def _build(self):
        # ── title + buttons ────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 6))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(hdr, text="Species & Cultivars",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     anchor="w").grid(row=0, column=0, sticky="w")

        btn_row = ctk.CTkFrame(hdr, fg_color="transparent")
        btn_row.grid(row=0, column=1)
        ctk.CTkButton(btn_row, text="+ Add Species", width=120,
                      command=self._add).pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="Edit", width=80, fg_color="gray40",
                      command=self._edit).pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="Delete", width=80,
                      fg_color="#8a3a3a", hover_color="#6a2a2a",
                      command=self._delete).pack(side="left", padx=4)

        # ── search bar ─────────────────────────────────────────────────────────
        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))
        search_row.grid_columnconfigure(0, weight=1)

        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", self._on_search_change)

        ctk.CTkEntry(
            search_row,
            textvariable=self._search_var,
            placeholder_text="🔍  Search name, common name, notes…",
            height=34,
        ).grid(row=0, column=0, sticky="ew")

        self._clear_search_btn = ctk.CTkButton(
            search_row, text="✕", width=34, height=34,
            fg_color="gray38", hover_color="gray28",
            command=lambda: self._search_var.set(""),
        )
        # shown dynamically when there is text

        hint = ctk.CTkLabel(
            search_row,
            text="Left-click column header to sort  ·  Right-click to filter",
            font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray55"),
            anchor="e",
        )
        hint.grid(row=0, column=2, padx=(10, 0))

        # ── treeview ───────────────────────────────────────────────────────────
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 4))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(
            tree_frame, style="Species.Treeview",
            columns=self.COLS, show="headings",
            selectmode="browse",
        )
        for col, w in zip(self.COLS, self._COL_WIDTHS):
            self._tree.heading(col, text=col,
                               command=lambda c=col: self._on_header_left_click(c))
            self._tree.column(col, width=w, minwidth=40, anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self._tree.bind("<Double-1>", lambda _: self._edit())
        self._tree.bind("<Button-3>", self._on_header_right_click)

        # ── status bar ─────────────────────────────────────────────────────────
        self._status_bar = ctk.CTkLabel(
            self, text="", anchor="w",
            text_color=("gray50", "gray60"),
        )
        self._status_bar.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 8))

    # ── data ───────────────────────────────────────────────────────────────────

    def refresh(self):
        rows   = SpeciesModel.get_all()
        counts = SpeciesModel.get_stock_counts()
        self._raw = []
        for r in rows:
            pmin = f"${r['price_min']:.2f}" if r["price_min"] is not None else "—"
            pmax = f"${r['price_max']:.2f}" if r["price_max"] is not None else "—"
            self._raw.append({
                "id":     r["id"],
                "values": (
                    r["common_name"] or "—",
                    r["name"],
                    r["care_level"] or "—",
                    pmin,
                    pmax,
                    str(counts.get(r["id"], 0)),
                    (r["notes"] or "")[:60],
                ),
            })
        self._render()

    # ── filtering / sorting ────────────────────────────────────────────────────

    def _render(self):
        """Apply search, column filters, and sort; then repopulate the tree."""
        q = self._search_q.lower().strip()

        visible = []
        for item in self._raw:
            vals = item["values"]

            # Global text search (all columns)
            if q:
                if q not in " ".join(str(v) for v in vals).lower():
                    continue

            # Per-column value filters
            skip = False
            for ci, allowed in self._col_filters.items():
                if allowed and str(vals[ci]) not in allowed:
                    skip = True
                    break
            if skip:
                continue

            visible.append(item)

        # Sort
        if self._sort_col is not None:
            ci = self.COLS.index(self._sort_col)

            def _key(item):
                v = item["values"][ci]
                s = str(v)
                if s.startswith("$"):
                    try:
                        return (0, float(s[1:]))
                    except ValueError:
                        pass
                try:
                    return (0, float(s))
                except (ValueError, TypeError):
                    return (1, s.lower())

            visible.sort(key=_key, reverse=self._sort_rev)

        # Rebuild tree
        self._tree.delete(*self._tree.get_children())
        for item in visible:
            self._tree.insert("", "end", iid=str(item["id"]),
                               values=item["values"])

        # Update column header labels (sort arrow + filter indicator)
        for i, col in enumerate(self.COLS):
            label = col
            if self._sort_col == col:
                label += "  ▲" if not self._sort_rev else "  ▼"
            if self._col_filters.get(i):
                label += "  ⊘"
            self._tree.heading(col, text=label,
                               command=lambda c=col: self._on_header_left_click(c))

        # Status bar
        total  = len(self._raw)
        shown  = len(visible)
        active = bool(q) or any(self._col_filters.values())
        if active:
            self._status_bar.configure(
                text=f"Showing {shown} of {total} cultivar{'s' if total != 1 else ''}"
                     + ("  —  search active" if q else "")
                     + (f"  —  {sum(1 for v in self._col_filters.values() if v)} column filter(s) active"
                        if any(self._col_filters.values()) else ""),
                text_color=("#b87c1a", "#d49a20"),
            )
        else:
            self._status_bar.configure(
                text=f"{total} cultivar{'s' if total != 1 else ''}",
                text_color=("gray50", "gray60"),
            )

    # ── event: search ──────────────────────────────────────────────────────────

    def _on_search_change(self, *_):
        self._search_q = self._search_var.get()
        # Show/hide ✕ clear button
        if self._search_q:
            self._clear_search_btn.grid(row=0, column=1, padx=(4, 0))
        else:
            self._clear_search_btn.grid_remove()
        self._render()

    # ── event: sort (left-click heading) ──────────────────────────────────────

    def _on_header_left_click(self, col: str):
        if self._sort_col == col:
            self._sort_rev = not self._sort_rev
        else:
            self._sort_col = col
            self._sort_rev = False
        self._render()

    # ── event: filter popup (right-click heading) ──────────────────────────────

    def _on_header_right_click(self, event):
        region = self._tree.identify_region(event.x, event.y)
        if region != "heading":
            return
        col_id  = self._tree.identify_column(event.x)   # "#1", "#2", …
        col_idx = int(col_id.lstrip("#")) - 1
        if not (0 <= col_idx < len(self.COLS)):
            return
        self._open_filter_popup(col_idx, event.x_root, event.y_root)

    def _open_filter_popup(self, col_idx: int, rx: int, ry: int):
        # Close existing popup first
        if self._filter_popup and self._filter_popup.winfo_exists():
            self._filter_popup.destroy()

        col_name       = self.COLS[col_idx]
        all_vals       = sorted(set(str(r["values"][col_idx]) for r in self._raw),
                                key=lambda v: (v == "—", v.lower()))
        current_filter = self._col_filters.get(col_idx, set())

        popup = tk.Toplevel(self)
        popup.wm_overrideredirect(True)
        popup.wm_attributes("-topmost", True)
        popup.wm_geometry(f"+{rx}+{ry}")
        popup.configure(bg="#111111")
        self._filter_popup = popup

        outer = ctk.CTkFrame(popup, corner_radius=10,
                              border_width=1, border_color=("gray65", "gray32"))
        outer.pack(padx=2, pady=2)

        # Title
        ctk.CTkLabel(
            outer,
            text=f"Filter  ·  {col_name}",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=14, pady=(12, 2))

        ctk.CTkLabel(
            outer,
            text="Right-click any column heading to filter  ·  Left-click to sort",
            font=ctk.CTkFont(size=10),
            text_color=("gray55", "gray55"),
            anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 6))

        # Scrollable checkbox list
        list_h = min(len(all_vals) + 1, 12) * 28 + 8
        scroll = ctk.CTkScrollableFrame(outer, height=list_h,
                                         fg_color=("gray88", "gray16"))
        scroll.pack(fill="x", padx=10, pady=(0, 6))

        check_vars: dict[str, ctk.BooleanVar] = {}
        none_filter = not current_filter          # True → all values allowed

        # "Select All" master checkbox
        all_var = ctk.BooleanVar(value=none_filter)

        def _toggle_all():
            state = all_var.get()
            for cv in check_vars.values():
                cv.set(state)

        ctk.CTkCheckBox(scroll, text="(Select All)",
                        variable=all_var, command=_toggle_all,
                        font=ctk.CTkFont(slant="italic")).pack(anchor="w", padx=8, pady=2)

        for val in all_vals:
            cv = ctk.BooleanVar(value=none_filter or val in current_filter)
            check_vars[val] = cv

            def _on_check(v=val):
                # If any box is unticked, untick "Select All" too
                if not check_vars[v].get():
                    all_var.set(False)
                elif all(cv.get() for cv in check_vars.values()):
                    all_var.set(True)

            ctk.CTkCheckBox(scroll, text=val, variable=cv,
                            command=_on_check).pack(anchor="w", padx=8, pady=1)

        # Apply / Clear / Cancel buttons
        btn_row = ctk.CTkFrame(outer, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(2, 12))

        def _apply():
            selected = {v for v, cv in check_vars.items() if cv.get()}
            if len(selected) == len(all_vals):
                self._col_filters.pop(col_idx, None)   # all selected = no filter
            else:
                self._col_filters[col_idx] = selected
            popup.destroy()
            self._render()

        def _clear():
            self._col_filters.pop(col_idx, None)
            popup.destroy()
            self._render()

        ctk.CTkButton(btn_row, text="Apply", width=80,
                      command=_apply).pack(side="right", padx=(4, 0))
        ctk.CTkButton(btn_row, text="Clear Filter", width=100,
                      fg_color="gray38", hover_color="gray28",
                      command=_clear).pack(side="right", padx=(4, 0))
        ctk.CTkButton(btn_row, text="Cancel", width=75,
                      fg_color="gray38", hover_color="gray28",
                      command=popup.destroy).pack(side="right")

        popup.update_idletasks()

        # Close when user clicks outside the popup
        root = self.winfo_toplevel()

        def _outside_click(e):
            if not popup.winfo_exists():
                return
            px, py = popup.winfo_rootx(), popup.winfo_rooty()
            pw, ph = popup.winfo_width(), popup.winfo_height()
            if not (px <= e.x_root <= px + pw and py <= e.y_root <= py + ph):
                popup.destroy()

        tag = root.bind("<Button-1>", _outside_click, add="+")
        popup.bind("<Destroy>", lambda _: root.unbind("<Button-1>", tag))

    # ── CRUD actions ───────────────────────────────────────────────────────────

    def _selected_id(self) -> int | None:
        sel = self._tree.selection()
        return int(sel[0]) if sel else None

    def _add(self):
        dlg = SpeciesDialog(self)
        self.wait_window(dlg)
        if dlg.result is not None:
            self.refresh()

    def _edit(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        dlg = SpeciesDialog(self, species_row=SpeciesModel.get_by_id(id_))
        self.wait_window(dlg)
        if dlg.result is not None:
            self.refresh()

    def _delete(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        row  = SpeciesModel.get_by_id(id_)
        cnt  = SpeciesModel.get_stock_counts().get(id_, 0)
        name = row["common_name"] or row["name"]
        msg  = f"Delete '{name}'?"
        if cnt:
            msg += (f"\n\n{cnt} stock item(s) reference this species "
                    "and will lose their species link.")
        if not messagebox.askyesno("Delete Species", msg):
            return
        SpeciesModel.delete(id_)
        self.refresh()
