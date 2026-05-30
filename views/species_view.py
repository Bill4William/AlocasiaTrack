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


class SpeciesView(ctk.CTkFrame):
    COLS = ("Common Name", "Scientific / Cultivar Name", "Care Level", "Price Min", "Price Max", "In Stock", "Notes")

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        _apply_tree_style()
        self._build()
        self.refresh()

    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))
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

        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 16))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(tree_frame, style="Species.Treeview",
                                  columns=self.COLS, show="headings",
                                  selectmode="browse")
        widths = [150, 200, 100, 80, 80, 70, 220]
        for col, w in zip(self.COLS, widths):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, minwidth=40, anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        self._tree.bind("<Double-1>", lambda _: self._edit())

        self._status_bar = ctk.CTkLabel(self, text="", anchor="w",
                                        text_color=("gray50", "gray60"))
        self._status_bar.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 8))

    def refresh(self):
        rows = SpeciesModel.get_all()
        counts = SpeciesModel.get_stock_counts()
        self._tree.delete(*self._tree.get_children())
        for row in rows:
            pmin = f"${row['price_min']:.2f}" if row["price_min"] is not None else "—"
            pmax = f"${row['price_max']:.2f}" if row["price_max"] is not None else "—"
            self._tree.insert("", "end", iid=str(row["id"]), values=(
                row["common_name"] or "—",
                row["name"],
                row["care_level"] or "—",
                pmin,
                pmax,
                counts.get(row["id"], 0),
                (row["notes"] or "")[:60],
            ))
        n = len(rows)
        self._status_bar.configure(text=f"{n} cultivar{'s' if n != 1 else ''}")

    def _selected_id(self):
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
        row = SpeciesModel.get_by_id(id_)
        dlg = SpeciesDialog(self, species_row=row)
        self.wait_window(dlg)
        if dlg.result is not None:
            self.refresh()

    def _delete(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        row = SpeciesModel.get_by_id(id_)
        cnt = SpeciesModel.get_stock_counts().get(id_, 0)
        display = row["common_name"] or row["name"]
        msg = f"Delete '{display}'?"
        if cnt:
            msg += f"\n\n{cnt} stock item(s) reference this species and will lose their species link."
        if not messagebox.askyesno("Delete Species", msg):
            return
        SpeciesModel.delete(id_)
        self.refresh()
