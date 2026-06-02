import customtkinter as ctk
from database.models import SpeciesModel, PlantsModel, StockModel
from components.photo_panel import PhotoPanel
from components.searchable_dropdown import SearchableDropdown


class StockDialog(ctk.CTkToplevel):
    def __init__(self, parent, stock_row=None):
        super().__init__(parent)
        self.result = None
        self._row = stock_row

        self.title("Edit Stock Item" if stock_row else "Add Stock Item")
        self.geometry("480x680")
        self.resizable(False, False)
        self.grab_set()

        self._species_map  = SpeciesModel.get_name_id_map()
        self._plant_opts   = PlantsModel.get_dropdown_options()  # [(id, label), ...]
        from integrations.config import get_pot_sizes
        self._pot_sizes    = get_pot_sizes()

        self._build()
        if stock_row:
            self._populate(stock_row)

        self.after(100, self.lift)

    # ------------------------------------------------------------------ build
    def _build(self):
        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=0, pady=0)
        self._f = scroll
        pad = {"padx": 20, "pady": 5}

        # Type
        ctk.CTkLabel(self._f, text="Item Type *", anchor="w").pack(fill="x", **pad)
        self.type_var = ctk.StringVar(value="Plant")
        type_frame = ctk.CTkFrame(self._f, fg_color="transparent")
        type_frame.pack(fill="x", **pad)
        for t in ["Plant", "Pup", "Corm"]:
            ctk.CTkRadioButton(type_frame, text=t, variable=self.type_var, value=t,
                               command=self._on_type_change).pack(side="left", padx=8)

        # Quantity (add mode only)
        if not self._row:
            qty_frame = ctk.CTkFrame(self._f, fg_color="transparent")
            qty_frame.pack(fill="x", **pad)
            ctk.CTkLabel(qty_frame, text="Quantity", anchor="w", width=90).pack(side="left")
            ctk.CTkButton(qty_frame, text="−", width=32, height=28,
                          fg_color="gray35", hover_color="gray25",
                          command=self._qty_dec).pack(side="left", padx=(8, 2))
            self._qty_var = ctk.StringVar(value="1")
            self._qty_entry = ctk.CTkEntry(qty_frame, textvariable=self._qty_var,
                                           width=52, justify="center")
            self._qty_entry.pack(side="left", padx=2)
            ctk.CTkButton(qty_frame, text="+", width=32, height=28,
                          fg_color="gray35", hover_color="gray25",
                          command=self._qty_inc).pack(side="left", padx=(2, 0))
            ctk.CTkLabel(qty_frame, text="identical items will be created",
                         text_color=("gray50", "gray55"),
                         font=ctk.CTkFont(size=12)).pack(side="left", padx=(10, 0))

        # Species
        ctk.CTkLabel(self._f, text="Species / Cultivar", anchor="w").pack(fill="x", **pad)
        self.species_dd = SearchableDropdown(
            self._f,
            options=self._species_map,
            placeholder="Search species…",
            none_label="— none —",
        )
        self.species_dd.pack(fill="x", **pad)

        # Parent plant
        ctk.CTkLabel(self._f, text="Parent Plant (optional)", anchor="w").pack(fill="x", **pad)
        plant_opts = {lbl: pid for pid, lbl in self._plant_opts}
        self.parent_dd = SearchableDropdown(
            self._f,
            options=plant_opts,
            placeholder="Search mother plants…",
            none_label="— none —",
        )
        self.parent_dd.pack(fill="x", **pad)

        # Growth Stage
        ctk.CTkLabel(self._f, text="Growth Stage", anchor="w").pack(fill="x", **pad)
        self.stage_var = ctk.StringVar(value=StockModel.GROWTH_STAGES["Plant"][0])
        self.stage_menu = ctk.CTkOptionMenu(self._f, variable=self.stage_var,
                                            values=StockModel.GROWTH_STAGES["Plant"])
        self.stage_menu.pack(fill="x", **pad)

        # Condition
        ctk.CTkLabel(self._f, text="Condition", anchor="w").pack(fill="x", **pad)
        self.cond_var = ctk.StringVar(value="Good")
        ctk.CTkOptionMenu(self._f, variable=self.cond_var,
                          values=StockModel.CONDITIONS).pack(fill="x", **pad)

        # Pot Size
        ctk.CTkLabel(self._f, text="Pot Size", anchor="w").pack(fill="x", **pad)
        default_pot = '4"' if '4"' in self._pot_sizes else self._pot_sizes[0]
        self.pot_var = ctk.StringVar(value=default_pot)
        ctk.CTkOptionMenu(self._f, variable=self.pot_var,
                          values=self._pot_sizes).pack(fill="x", **pad)

        # Prices
        price_frame = ctk.CTkFrame(self._f, fg_color="transparent")
        price_frame.pack(fill="x", **pad)
        left = ctk.CTkFrame(price_frame, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=(0, 6))
        right = ctk.CTkFrame(price_frame, fg_color="transparent")
        right.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(left, text="Asking Price ($)", anchor="w").pack(fill="x")
        self.price_entry = ctk.CTkEntry(left, placeholder_text="0.00")
        self.price_entry.pack(fill="x")

        ctk.CTkLabel(right, text="Cost Basis ($)", anchor="w").pack(fill="x")
        self.cost_entry = ctk.CTkEntry(right, placeholder_text="0.00")
        self.cost_entry.pack(fill="x")

        # Status (edit only)
        self.status_label = ctk.CTkLabel(self._f, text="Status", anchor="w")
        self.status_var = ctk.StringVar(value="Available")
        self.status_menu = ctk.CTkOptionMenu(self._f, variable=self.status_var,
                                             values=StockModel.STATUSES)
        if self._row:
            self.status_label.pack(fill="x", **pad)
            self.status_menu.pack(fill="x", **pad)

        # Notes
        ctk.CTkLabel(self._f, text="Notes", anchor="w").pack(fill="x", **pad)
        self.notes_box = ctk.CTkTextbox(self._f, height=80)
        self.notes_box.pack(fill="x", **pad)

        # Photos
        ctk.CTkLabel(self._f, text="", anchor="w").pack(fill="x")  # spacer
        existing_photos = PhotoPanel.parse(
            self._row["photo_paths"] if self._row else None
        )
        sku_label = self._row["sku"] if self._row else "new-item"
        self.photo_panel = PhotoPanel(
            self._f, photos=existing_photos,
            item_label=sku_label,
            fg_color="transparent",
        )
        self.photo_panel.pack(fill="x", padx=20, pady=(0, 4))

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(8, 16))
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray40",
                      command=self.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btn_frame, text="Save", command=self._save).pack(side="right")

    def _qty_dec(self):
        try:
            v = max(1, int(self._qty_var.get()) - 1)
        except ValueError:
            v = 1
        self._qty_var.set(str(v))

    def _qty_inc(self):
        try:
            v = int(self._qty_var.get()) + 1
        except ValueError:
            v = 1
        self._qty_var.set(str(v))

    def _on_type_change(self):
        t = self.type_var.get()
        stages = StockModel.GROWTH_STAGES.get(t, ["—"])
        self.stage_var.set(stages[0])
        self.stage_menu.configure(values=stages)
        if t == "Corm":
            self.pot_var.set("No pot")

    # ------------------------------------------------------------------ populate
    def _populate(self, row):
        self.type_var.set(row["item_type"])
        self._on_type_change()

        if row["species_name"] and row["species_name"] in self._species_map:
            self.species_dd.set(row["species_name"])

        if row["parent_nickname"]:
            for pid, lbl in self._plant_opts:
                if row["parent_nickname"] in lbl:
                    self.parent_dd.set(lbl, pid)
                    break

        if row["growth_stage"]:
            self.stage_var.set(row["growth_stage"])
        if row["condition"]:
            self.cond_var.set(row["condition"])
        if row["pot_size"]:
            self.pot_var.set(row["pot_size"])
        if row["asking_price"] is not None:
            self.price_entry.insert(0, str(row["asking_price"]))
        if row["cost_basis"] is not None:
            self.cost_entry.insert(0, str(row["cost_basis"]))
        if row["status"]:
            self.status_var.set(row["status"])
        if row["notes"]:
            self.notes_box.insert("0.0", row["notes"])

    # ------------------------------------------------------------------ save
    def _save(self):
        def _float(widget):
            try:
                return float(widget.get().strip())
            except (ValueError, AttributeError):
                return None

        item_type       = self.type_var.get()
        species_id      = self.species_dd.get_id()
        parent_plant_id = self.parent_dd.get_id()

        photo_json = self.photo_panel.get_photos_json()

        data = {
            "item_type":       item_type,
            "species_id":      species_id,
            "parent_plant_id": parent_plant_id,
            "growth_stage":    self.stage_var.get(),
            "condition":       self.cond_var.get(),
            "pot_size":        self.pot_var.get(),
            "asking_price":    _float(self.price_entry),
            "cost_basis":      _float(self.cost_entry) or 0,
            "notes":           self.notes_box.get("0.0", "end").strip() or None,
            "photo_paths":     photo_json,
        }

        if self._row:
            StockModel.update(self._row["id"], status=self.status_var.get(), **data)
            self.result = data
        else:
            try:
                qty = max(1, int(self._qty_var.get()))
            except (ValueError, AttributeError):
                qty = 1
            skus = []
            for _ in range(qty):
                sku = StockModel.create(**data)
                skus.append(sku)
            self.result = {**data, "_skus": skus, "_qty": qty}

        self.destroy()
