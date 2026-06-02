import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from database.models import SpeciesModel, StockModel
from dialogs.stock_dialog import StockDialog
from dialogs.sale_dialog import SaleDialog
from dialogs.listing_dialog import ListingDialog


def _apply_tree_style():
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Stock.Treeview",
        background="#2b2b2b", foreground="white",
        rowheight=30, fieldbackground="#2b2b2b",
        borderwidth=0, font=("Segoe UI", 10))
    style.configure("Stock.Treeview.Heading",
        background="#1a1a1a", foreground="#aaaaaa",
        relief="flat", font=("Segoe UI", 10, "bold"))
    style.map("Stock.Treeview",
        background=[("selected", "#1f6aa5")],
        foreground=[("selected", "white")])
    style.map("Stock.Treeview.Heading",
        background=[("active", "#2c2c2c")],
        foreground=[("active", "#ffffff")])


STATUS_COLORS = {
    "Available": "#2a7a3a",
    "Listed":    "#b87c1a",
    "Sold":      "#6a3a9a",
    "Traded":    "#1f6aa5",
    "Died":      "#8a3a3a",
}


class StockView(ctk.CTkFrame):
    COLS = ("SKU", "Type", "Species", "Stage", "Condition", "Pot",
            "Price", "Cost", "Status", "Added")
    _COL_WIDTHS = [80, 70, 160, 100, 90, 60, 70, 70, 90, 90]

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)   # row 3 = treeview
        _apply_tree_style()

        # State
        self._raw: list[dict] = []
        self._search_q    = ""
        self._sort_col: str | None = None
        self._sort_rev    = False
        self._col_filters: dict[int, set] = {}
        self._filter_popup: tk.Toplevel | None = None

        self._build()
        self.refresh()

    # ── build ──────────────────────────────────────────────────────────────────

    def _build(self):
        # ── Row 0: title + action buttons ──────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 4))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(hdr, text="Stock Inventory",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     anchor="w").grid(row=0, column=0, sticky="w")

        btn_row = ctk.CTkFrame(hdr, fg_color="transparent")
        btn_row.grid(row=0, column=1)
        self._add_btn = ctk.CTkButton(btn_row, text="+ Add Item", width=100,
                                      command=self._add)
        self._add_btn.pack(side="left", padx=4)
        self._edit_btn = ctk.CTkButton(btn_row, text="Edit", width=80,
                                       fg_color="gray40", command=self._edit)
        self._edit_btn.pack(side="left", padx=4)
        self._del_btn = ctk.CTkButton(btn_row, text="Delete", width=80,
                                      fg_color="#8a3a3a", hover_color="#6a2a2a",
                                      command=self._delete)
        self._del_btn.pack(side="left", padx=4)
        self._sale_btn = ctk.CTkButton(btn_row, text="Record Sale", width=110,
                                       fg_color="#2a7a3a", hover_color="#1e5e2c",
                                       command=self._record_sale)
        self._sale_btn.pack(side="left", padx=4)
        self._fb_btn = ctk.CTkButton(btn_row, text="Post to FB", width=100,
                                     fg_color="#1877F2", hover_color="#1155CC",
                                     command=self._post_to_fb)
        self._fb_btn.pack(side="left", padx=4)
        self._shopify_btn = ctk.CTkButton(btn_row, text="Shopify", width=80,
                                          fg_color="#96bf48", hover_color="#7aab2e",
                                          text_color="#1a1a1a",
                                          command=self._sync_to_shopify)
        self._shopify_btn.pack(side="left", padx=4)

        # ── Row 1: existing dropdown filters (keep as-is) ──────────────────────
        flt = ctk.CTkFrame(self, fg_color="transparent")
        flt.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 4))

        ctk.CTkLabel(flt, text="Type:").pack(side="left", padx=(0, 4))
        self._type_var = ctk.StringVar(value="All")
        ctk.CTkOptionMenu(flt, variable=self._type_var,
                          values=["All", "Plant", "Pup", "Corm"],
                          width=100, command=lambda _: self.refresh()
                          ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(flt, text="Status:").pack(side="left", padx=(0, 4))
        self._status_var = ctk.StringVar(value="All")
        ctk.CTkOptionMenu(flt, variable=self._status_var,
                          values=["All"] + StockModel.STATUSES,
                          width=120, command=lambda _: self.refresh()
                          ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(flt, text="Species:").pack(side="left", padx=(0, 4))
        self._species_var = ctk.StringVar(value="All")
        self._species_menu = ctk.CTkOptionMenu(
            flt, variable=self._species_var,
            values=["All"], width=160,
            command=lambda _: self.refresh(),
        )
        self._species_menu.pack(side="left")

        # ── Row 2: search bar ──────────────────────────────────────────────────
        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 6))
        search_row.grid_columnconfigure(0, weight=1)

        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", self._on_search_change)
        ctk.CTkEntry(
            search_row,
            textvariable=self._search_var,
            placeholder_text="Search SKU, species, condition, notes...",
            height=32,
        ).grid(row=0, column=0, sticky="ew")

        self._clear_search_btn = ctk.CTkButton(
            search_row, text="X", width=32, height=32,
            fg_color="gray38", hover_color="gray28",
            command=lambda: self._search_var.set(""),
        )

        ctk.CTkLabel(
            search_row,
            text="Left-click column to sort  ·  Right-click to filter",
            font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray55"),
            anchor="e",
        ).grid(row=0, column=2, padx=(10, 0))

        # ── Row 3: treeview ────────────────────────────────────────────────────
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 4))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(tree_frame, style="Stock.Treeview",
                                  columns=self.COLS, show="headings",
                                  selectmode="browse")
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

        # ── Row 4: status bar ──────────────────────────────────────────────────
        self._status_bar = ctk.CTkLabel(
            self, text="", anchor="w",
            text_color=("gray50", "gray60"),
        )
        self._status_bar.grid(row=4, column=0, sticky="w", padx=20, pady=(0, 8))

    # ── data ───────────────────────────────────────────────────────────────────

    def refresh(self):
        """Re-query DB (respects dropdown filters), cache, then render."""
        # Update species dropdown
        species_names = ["All"] + SpeciesModel.get_names()
        self._species_menu.configure(values=species_names)
        if self._species_var.get() not in species_names:
            self._species_var.set("All")

        type_filter   = self._type_var.get()   if self._type_var.get()   != "All" else None
        status_filter = self._status_var.get() if self._status_var.get() != "All" else None
        sp_name       = self._species_var.get()
        species_filter = None
        if sp_name != "All":
            smap = SpeciesModel.get_name_id_map()
            species_filter = smap.get(sp_name)

        rows = StockModel.get_all(item_type=type_filter, status=status_filter,
                                  species_id=species_filter)
        self._raw = []
        for row in rows:
            price = f"${row['asking_price']:.2f}" if row["asking_price"] is not None else ""
            cost  = f"${row['cost_basis']:.2f}"   if row["cost_basis"]  is not None else ""
            self._raw.append({
                "id":     row["id"],
                "status": row["status"] or "Available",
                "values": (
                    row["sku"] or "",
                    row["item_type"] or "",
                    row["species_name"] or "",
                    row["growth_stage"] or "",
                    row["condition"] or "",
                    row["pot_size"] or "",
                    price,
                    cost,
                    row["status"] or "",
                    (row["date_added"] or "")[:10],
                ),
            })
        self._render()

    def _render(self):
        """Apply search + column filters + sort; repopulate tree."""
        q = self._search_q.lower().strip()

        visible = []
        for item in self._raw:
            vals = item["values"]
            if q and q not in " ".join(str(v) for v in vals).lower():
                continue
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
                v = str(item["values"][ci])
                if v.startswith("$"):
                    try:
                        return (0, float(v[1:]))
                    except ValueError:
                        pass
                return (1, v.lower())

            visible.sort(key=_key, reverse=self._sort_rev)

        # Rebuild tree
        self._tree.delete(*self._tree.get_children())
        for item in visible:
            self._tree.insert("", "end", iid=str(item["id"]),
                               tags=(item["status"],),
                               values=item["values"])

        for status, color in STATUS_COLORS.items():
            self._tree.tag_configure(status, foreground=color)

        # Update column headings
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
                text=f"Showing {shown} of {total} item{'s' if total != 1 else ''}",
                text_color=("#b87c1a", "#d49a20"),
            )
        else:
            self._status_bar.configure(
                text=f"{total} item{'s' if total != 1 else ''}",
                text_color=("gray50", "gray60"),
            )

    # ── event: search ──────────────────────────────────────────────────────────

    def _on_search_change(self, *_):
        self._search_q = self._search_var.get()
        if self._search_q:
            self._clear_search_btn.grid(row=0, column=1, padx=(4, 0))
        else:
            self._clear_search_btn.grid_remove()
        self._render()

    # ── event: sort ────────────────────────────────────────────────────────────

    def _on_header_left_click(self, col: str):
        if self._sort_col == col:
            self._sort_rev = not self._sort_rev
        else:
            self._sort_col = col
            self._sort_rev = False
        self._render()

    # ── event: column filter popup ─────────────────────────────────────────────

    def _on_header_right_click(self, event):
        region = self._tree.identify_region(event.x, event.y)
        if region != "heading":
            return
        col_id  = self._tree.identify_column(event.x)
        col_idx = int(col_id.lstrip("#")) - 1
        if not (0 <= col_idx < len(self.COLS)):
            return
        self._open_filter_popup(col_idx, event.x_root, event.y_root)

    def _open_filter_popup(self, col_idx: int, rx: int, ry: int):
        if self._filter_popup and self._filter_popup.winfo_exists():
            self._filter_popup.destroy()

        col_name       = self.COLS[col_idx]
        all_vals       = sorted(
            set(str(r["values"][col_idx]) for r in self._raw if str(r["values"][col_idx])),
            key=lambda v: v.lower(),
        )
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

        ctk.CTkLabel(
            outer,
            text=f"Filter  ·  {col_name}",
            font=ctk.CTkFont(size=12, weight="bold"), anchor="w",
        ).pack(fill="x", padx=14, pady=(12, 4))

        list_h = min(len(all_vals) + 1, 12) * 28 + 8
        scroll = ctk.CTkScrollableFrame(outer, height=list_h,
                                         fg_color=("gray88", "gray16"))
        scroll.pack(fill="x", padx=10, pady=(0, 6))

        check_vars: dict[str, ctk.BooleanVar] = {}
        none_filter = not current_filter
        all_var = ctk.BooleanVar(value=none_filter)

        def _toggle_all():
            for cv in check_vars.values():
                cv.set(all_var.get())

        ctk.CTkCheckBox(scroll, text="(Select All)", variable=all_var,
                        command=_toggle_all,
                        font=ctk.CTkFont(slant="italic")).pack(anchor="w", padx=8, pady=2)

        for val in all_vals:
            cv = ctk.BooleanVar(value=none_filter or val in current_filter)
            check_vars[val] = cv

            def _on_check(v=val):
                if not check_vars[v].get():
                    all_var.set(False)
                elif all(c.get() for c in check_vars.values()):
                    all_var.set(True)

            ctk.CTkCheckBox(scroll, text=val, variable=cv,
                            command=_on_check).pack(anchor="w", padx=8, pady=1)

        btn_row = ctk.CTkFrame(outer, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(2, 12))

        def _apply():
            selected = {v for v, cv in check_vars.items() if cv.get()}
            if len(selected) == len(all_vals):
                self._col_filters.pop(col_idx, None)
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
        root = self.winfo_toplevel()

        def _outside(e):
            if not popup.winfo_exists():
                return
            px, py = popup.winfo_rootx(), popup.winfo_rooty()
            pw, ph = popup.winfo_width(), popup.winfo_height()
            if not (px <= e.x_root <= px + pw and py <= e.y_root <= py + ph):
                popup.destroy()

        tag = root.bind("<Button-1>", _outside, add="+")
        popup.bind("<Destroy>", lambda _: root.unbind("<Button-1>", tag))

    # ── selected id ────────────────────────────────────────────────────────────

    def _selected_id(self):
        sel = self._tree.selection()
        return int(sel[0]) if sel else None

    # ── CRUD / integrations ────────────────────────────────────────────────────

    def _add(self):
        dlg = StockDialog(self)
        self.wait_window(dlg)
        if dlg.result is not None:
            self.refresh()
            qty  = dlg.result.get("_qty", 1)
            skus = dlg.result.get("_skus", [])
            if qty > 1:
                self._status_bar.configure(
                    text=f"Added {qty} items: {skus[0]} - {skus[-1]}"
                )

    def _edit(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        dlg = StockDialog(self, stock_row=StockModel.get_by_id(id_))
        self.wait_window(dlg)
        if dlg.result is not None:
            self.refresh()

    def _delete(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        row = StockModel.get_by_id(id_)
        if not messagebox.askyesno(
            "Delete Item",
            f"Delete {row['sku']} ({row['item_type']})? This cannot be undone.",
        ):
            return
        StockModel.delete(id_)
        self.refresh()

    def _record_sale(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        row = StockModel.get_by_id(id_)
        if row["status"] == "Sold":
            messagebox.showinfo("Already Sold", f"{row['sku']} is already marked as sold.")
            return
        dlg = SaleDialog(self, stock_row=row)
        self.wait_window(dlg)
        if dlg.result:
            self.refresh()

    def _post_to_fb(self):
        id_ = self._selected_id()
        if id_ is None:
            messagebox.showinfo("Select Item", "Select a stock item first.")
            return
        row = StockModel.get_by_id(id_)
        if row["status"] == "Sold":
            messagebox.showinfo("Already Sold", f"{row['sku']} is already sold.")
            return
        dlg = ListingDialog(self, stock_row=row)
        self.wait_window(dlg)
        self.refresh()

    def _sync_to_shopify(self):
        import threading
        from integrations.shopify_store import is_configured, sync_item
        import integrations.config as cfg

        id_ = self._selected_id()
        if id_ is None:
            self._status_bar.configure(text="Select a stock item first.")
            return
        if not is_configured():
            self._status_bar.configure(
                text="Shopify not configured - see Settings > Shopify."
            )
            return

        row      = StockModel.get_by_id(id_)
        shop_url = cfg.get("shopify_shop_url")
        token    = cfg.get("shopify_access_token")
        self._shopify_btn.configure(state="disabled", text="Syncing...")
        self._status_bar.configure(text=f"Syncing {row['sku']} to Shopify...")

        def _worker():
            try:
                url = sync_item(shop_url, token, row)
                self.after(0, lambda: self._on_shopify_done(row["sku"], url))
            except Exception as exc:
                self.after(0, lambda e=str(exc): self._on_shopify_error(e))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_shopify_done(self, sku: str, url: str):
        self._shopify_btn.configure(state="normal", text="Shopify")
        self._status_bar.configure(
            text=f"{sku} synced to Shopify.  {url[:70]}{'...' if len(url) > 70 else ''}"
        )

    def _on_shopify_error(self, err: str):
        self._shopify_btn.configure(state="normal", text="Shopify")
        self._status_bar.configure(text=f"Shopify error: {err[:100]}")
