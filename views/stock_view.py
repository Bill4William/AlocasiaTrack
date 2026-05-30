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
        background=[("active", "#333333")])


STATUS_COLORS = {
    "Available": "#2a7a3a",
    "Listed":    "#b87c1a",
    "Sold":      "#6a3a9a",
    "Traded":    "#1f6aa5",
    "Died":      "#8a3a3a",
}


class StockView(ctk.CTkFrame):
    COLS = ("SKU", "Type", "Species", "Stage", "Condition", "Pot", "Price", "Cost", "Status", "Added")

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        _apply_tree_style()
        self._build()
        self.refresh()

    # ------------------------------------------------------------ build UI
    def _build(self):
        # Header row
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

        # Filter bar
        flt = ctk.CTkFrame(self, fg_color="transparent")
        flt.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))

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
        self._species_menu = ctk.CTkOptionMenu(flt, variable=self._species_var,
                                               values=["All"], width=160,
                                               command=lambda _: self.refresh())
        self._species_menu.pack(side="left")

        # Tree
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 16))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(tree_frame, style="Stock.Treeview",
                                  columns=self.COLS, show="headings",
                                  selectmode="browse")
        widths = [80, 70, 140, 100, 90, 60, 70, 70, 90, 90]
        for col, w in zip(self.COLS, widths):
            self._tree.heading(col, text=col,
                               command=lambda c=col: self._sort_by(c))
            self._tree.column(col, width=w, minwidth=40, anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self._tree.bind("<Double-1>", lambda _: self._edit())

        # Status bar
        self._status_bar = ctk.CTkLabel(self, text="", anchor="w",
                                        text_color=("gray50", "gray60"))
        self._status_bar.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 8))

    # ------------------------------------------------------------ data
    def refresh(self):
        species_names = ["All"] + SpeciesModel.get_names()
        self._species_menu.configure(values=species_names)
        if self._species_var.get() not in species_names:
            self._species_var.set("All")

        type_filter    = self._type_var.get() if self._type_var.get() != "All" else None
        status_filter  = self._status_var.get() if self._status_var.get() != "All" else None
        sp_name        = self._species_var.get()
        species_filter = None
        if sp_name != "All":
            smap = SpeciesModel.get_name_id_map()
            species_filter = smap.get(sp_name)

        rows = StockModel.get_all(item_type=type_filter, status=status_filter,
                                  species_id=species_filter)
        self._tree.delete(*self._tree.get_children())
        for row in rows:
            price = f"${row['asking_price']:.2f}" if row["asking_price"] is not None else "—"
            cost  = f"${row['cost_basis']:.2f}"   if row["cost_basis"]  is not None else "—"
            tag   = row["status"] or "Available"
            self._tree.insert("", "end", iid=str(row["id"]), tags=(tag,), values=(
                row["sku"] or "—",
                row["item_type"],
                row["species_name"] or "—",
                row["growth_stage"] or "—",
                row["condition"] or "—",
                row["pot_size"] or "—",
                price,
                cost,
                row["status"],
                (row["date_added"] or "")[:10],
            ))

        for status, color in STATUS_COLORS.items():
            self._tree.tag_configure(status, foreground=color)

        count = len(rows)
        self._status_bar.configure(text=f"{count} item{'s' if count != 1 else ''}")

    def _selected_id(self):
        sel = self._tree.selection()
        return int(sel[0]) if sel else None

    def _sort_by(self, col):
        items = [(self._tree.set(k, col), k) for k in self._tree.get_children()]
        items.sort(key=lambda x: x[0].lower())
        for i, (_, k) in enumerate(items):
            self._tree.move(k, "", i)

    # ------------------------------------------------------------ actions
    def _add(self):
        dlg = StockDialog(self)
        self.wait_window(dlg)
        if dlg.result is not None:
            self.refresh()
            qty = dlg.result.get("_qty", 1)
            skus = dlg.result.get("_skus", [])
            if qty > 1:
                self._status_bar.configure(
                    text=f"Added {qty} items: {skus[0]} – {skus[-1]}"
                )

    def _edit(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        row = StockModel.get_by_id(id_)
        dlg = StockDialog(self, stock_row=row)
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
                text="Shopify not configured — see Settings > Shopify."
            )
            return

        row      = StockModel.get_by_id(id_)
        shop_url = cfg.get("shopify_shop_url")
        token    = cfg.get("shopify_access_token")

        self._shopify_btn.configure(state="disabled", text="Syncing…")
        self._status_bar.configure(text=f"Syncing {row['sku']} to Shopify…")

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
            text=f"{sku} synced to Shopify.  {url[:70]}{'…' if len(url) > 70 else ''}"
        )

    def _on_shopify_error(self, err: str):
        self._shopify_btn.configure(state="normal", text="Shopify")
        self._status_bar.configure(text=f"Shopify error: {err[:100]}")
