import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from database.models import SalesModel


def _apply_tree_style():
    style = ttk.Style()
    style.configure("Sales.Treeview",
        background="#2b2b2b", foreground="white",
        rowheight=30, fieldbackground="#2b2b2b",
        borderwidth=0, font=("Segoe UI", 10))
    style.configure("Sales.Treeview.Heading",
        background="#1a1a1a", foreground="#aaaaaa",
        relief="flat", font=("Segoe UI", 10, "bold"))
    style.map("Sales.Treeview",
        background=[("selected", "#1f6aa5")],
        foreground=[("selected", "white")])


class SalesView(ctk.CTkFrame):
    COLS = ("Date", "SKU", "Type", "Species", "Sale Price", "Profit",
            "Platform", "Buyer", "Shipping")

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        _apply_tree_style()
        self._build()
        self.refresh()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 4))
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hdr, text="Sales History",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     anchor="w").grid(row=0, column=0, sticky="w")

        # Summary strip
        self._summary = ctk.CTkFrame(self, fg_color=("gray85", "gray20"))
        self._summary.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 8))
        self._total_lbl  = ctk.CTkLabel(self._summary, text="Total Sales: 0",
                                         font=ctk.CTkFont(weight="bold"))
        self._total_lbl.pack(side="left", padx=16, pady=8)
        self._rev_lbl   = ctk.CTkLabel(self._summary, text="Revenue: $0.00",
                                        text_color="#2a7a3a",
                                        font=ctk.CTkFont(weight="bold"))
        self._rev_lbl.pack(side="left", padx=16)
        self._profit_lbl = ctk.CTkLabel(self._summary, text="Profit: $0.00",
                                         text_color="#2a7a3a",
                                         font=ctk.CTkFont(weight="bold"))
        self._profit_lbl.pack(side="left", padx=16)

        # Tree
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 16))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(tree_frame, style="Sales.Treeview",
                                  columns=self.COLS, show="headings",
                                  selectmode="browse")
        widths = [100, 90, 70, 140, 90, 80, 100, 130, 110]
        for col, w in zip(self.COLS, widths):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, minwidth=40, anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        self._status_bar = ctk.CTkLabel(self, text="", anchor="w",
                                        text_color=("gray50", "gray60"))
        self._status_bar.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 8))

    def refresh(self):
        rows = SalesModel.get_all()
        totals = SalesModel.get_all_time_stats()

        self._total_lbl.configure(text=f"Total Sales: {totals['total_sales']}")
        self._rev_lbl.configure(text=f"Revenue: ${totals['total_revenue']:.2f}")
        self._profit_lbl.configure(text=f"Profit: ${totals['total_profit']:.2f}")

        self._tree.delete(*self._tree.get_children())
        for row in rows:
            profit = f"${row['profit']:.2f}" if row["profit"] is not None else "—"
            self._tree.insert("", "end", values=(
                (row["sale_date"] or "")[:10],
                row["sku"] or "—",
                row["item_type"] or "—",
                row["species_name"] or "—",
                f"${row['sale_price']:.2f}",
                profit,
                row["platform"] or "—",
                row["buyer_name"] or "—",
                row["shipping_method"] or "—",
            ))
        n = len(rows)
        self._status_bar.configure(text=f"{n} sale{'s' if n != 1 else ''} recorded")
