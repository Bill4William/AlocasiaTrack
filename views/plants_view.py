import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from database.models import PlantsModel
from dialogs.plant_dialog import PlantDialog


def _apply_tree_style():
    style = ttk.Style()
    style.configure("Plants.Treeview",
        background="#2b2b2b", foreground="white",
        rowheight=30, fieldbackground="#2b2b2b",
        borderwidth=0, font=("Segoe UI", 10))
    style.configure("Plants.Treeview.Heading",
        background="#1a1a1a", foreground="#aaaaaa",
        relief="flat", font=("Segoe UI", 10, "bold"))
    style.map("Plants.Treeview",
        background=[("selected", "#1f6aa5")],
        foreground=[("selected", "white")])


HEALTH_COLORS = {
    "Thriving":   "#2a7a3a",
    "Healthy":    "#3a9a4a",
    "Fair":       "#b87c1a",
    "Stressed":   "#c05020",
    "Recovering": "#1f6aa5",
}


class PlantsView(ctk.CTkFrame):
    COLS = ("#", "Species", "Nickname", "Pot", "Health", "Location", "Acquired")

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        _apply_tree_style()
        self._build()
        self.refresh()

    def _build(self):
        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(hdr, text="Mother Plants",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     anchor="w").grid(row=0, column=0, sticky="w")

        btn_row = ctk.CTkFrame(hdr, fg_color="transparent")
        btn_row.grid(row=0, column=1)
        ctk.CTkButton(btn_row, text="+ Add Plant", width=110,
                      command=self._add).pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="Edit", width=80, fg_color="gray40",
                      command=self._edit).pack(side="left", padx=4)
        ctk.CTkButton(btn_row, text="Delete", width=80,
                      fg_color="#8a3a3a", hover_color="#6a2a2a",
                      command=self._delete).pack(side="left", padx=4)

        # Tree
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 16))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._tree = ttk.Treeview(tree_frame, style="Plants.Treeview",
                                  columns=self.COLS, show="headings",
                                  selectmode="browse")
        widths = [40, 160, 140, 70, 100, 140, 100]
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
        rows = PlantsModel.get_all()
        self._tree.delete(*self._tree.get_children())
        for i, row in enumerate(rows, 1):
            health = row["health_status"] or "Healthy"
            self._tree.insert("", "end", iid=str(row["id"]),
                              tags=(health,), values=(
                i,
                row["species_name"] or "—",
                row["nickname"] or "—",
                row["pot_size"] or "—",
                health,
                row["location"] or "—",
                (row["acquired_date"] or "")[:10],
            ))
        for h, c in HEALTH_COLORS.items():
            self._tree.tag_configure(h, foreground=c)
        n = len(rows)
        self._status_bar.configure(text=f"{n} mother plant{'s' if n != 1 else ''}")

    def _selected_id(self):
        sel = self._tree.selection()
        return int(sel[0]) if sel else None

    def _add(self):
        dlg = PlantDialog(self)
        self.wait_window(dlg)
        if dlg.result is not None:
            self.refresh()

    def _edit(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        row = PlantsModel.get_by_id(id_)
        dlg = PlantDialog(self, plant_row=row)
        self.wait_window(dlg)
        if dlg.result is not None:
            self.refresh()

    def _delete(self):
        id_ = self._selected_id()
        if id_ is None:
            return
        row = PlantsModel.get_by_id(id_)
        name = row["nickname"] or f"Plant #{id_}"
        if not messagebox.askyesno(
            "Delete Plant",
            f"Delete '{name}'? Stock items linked to this plant will lose their parent reference.",
        ):
            return
        PlantsModel.delete(id_)
        self.refresh()
