import customtkinter as ctk
from datetime import date
from database.models import SpeciesModel, PlantsModel
from components.photo_panel import PhotoPanel
from components.searchable_dropdown import SearchableDropdown
from components.date_picker import DatePickerEntry


class PlantDialog(ctk.CTkToplevel):
    HEALTH_STATUSES = ["Thriving", "Healthy", "Fair", "Stressed", "Recovering"]

    def __init__(self, parent, plant_row=None):
        super().__init__(parent)
        self.result = None
        self._row = plant_row

        self.title("Edit Mother Plant" if plant_row else "Add Mother Plant")
        self.geometry("460x740")
        self.minsize(460, 500)
        self.resizable(False, True)
        self.grab_set()

        self._species_map = SpeciesModel.get_name_id_map()
        from integrations.config import get_pot_sizes
        self._pot_sizes = get_pot_sizes()

        self._build()
        if plant_row:
            self._populate(plant_row)

        self.after(100, self.lift)

    def _build(self):
        # Save/Cancel pinned at the bottom, always visible
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=(4, 16))
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray40",
                      command=self.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btn_frame, text="Save", command=self._save).pack(side="right")

        ctk.CTkFrame(self, height=1, fg_color=("gray80", "gray30")).pack(
            side="bottom", fill="x", padx=20, pady=(0, 4)
        )

        # Scrollable area for all form fields
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        scroll.grid_columnconfigure(0, weight=1)

        pad = {"padx": 20, "pady": 5}

        ctk.CTkLabel(scroll, text="Species *", anchor="w").pack(fill="x", **pad)
        self.species_dd = SearchableDropdown(
            scroll,
            options=self._species_map,
            placeholder="Search species…",
            none_label=None,  # species is required for mother plants
        )
        if self._species_map:
            self.species_dd.set(next(iter(self._species_map)))
        self.species_dd.pack(fill="x", **pad)

        ctk.CTkLabel(scroll, text="Nickname / Label", anchor="w").pack(fill="x", **pad)
        self.nick_entry = ctk.CTkEntry(scroll, placeholder_text="e.g. Big Mama #1")
        self.nick_entry.pack(fill="x", **pad)

        ctk.CTkLabel(scroll, text="Date Acquired", anchor="w").pack(fill="x", **pad)
        self.date_entry = DatePickerEntry(scroll)
        self.date_entry.pack(fill="x", **pad)

        ctk.CTkLabel(scroll, text="Pot Size", anchor="w").pack(fill="x", **pad)
        self.pot_var = ctk.StringVar(value=self._pot_sizes[1] if len(self._pot_sizes) > 1 else "")
        self.pot_menu = ctk.CTkOptionMenu(scroll, variable=self.pot_var, values=self._pot_sizes)
        self.pot_menu.pack(fill="x", **pad)

        ctk.CTkLabel(scroll, text="Health Status", anchor="w").pack(fill="x", **pad)
        self.health_var = ctk.StringVar(value="Healthy")
        self.health_menu = ctk.CTkOptionMenu(scroll, variable=self.health_var,
                                             values=self.HEALTH_STATUSES)
        self.health_menu.pack(fill="x", **pad)

        ctk.CTkLabel(scroll, text="Location (shelf, room, etc.)", anchor="w").pack(fill="x", **pad)
        self.loc_entry = ctk.CTkEntry(scroll, placeholder_text="e.g. Shelf A, Greenhouse")
        self.loc_entry.pack(fill="x", **pad)

        ctk.CTkLabel(scroll, text="Notes", anchor="w").pack(fill="x", **pad)
        self.notes_box = ctk.CTkTextbox(scroll, height=70)
        self.notes_box.pack(fill="x", **pad)

        # Photos
        ctk.CTkFrame(scroll, height=1, fg_color=("gray80", "gray30")).pack(
            fill="x", padx=20, pady=(8, 4)
        )
        existing_photos = PhotoPanel.parse(
            self._row["photo_paths"] if self._row else None
        )
        nick = self._row["nickname"] if self._row else "new-plant"
        self.photo_panel = PhotoPanel(
            scroll, photos=existing_photos,
            item_label=nick or "plant",
            fg_color="transparent",
        )
        self.photo_panel.pack(fill="x", padx=20, pady=(0, 8))

    def _populate(self, row):
        if row["species_name"] and row["species_name"] in self._species_map:
            self.species_dd.set(row["species_name"])
        self.nick_entry.insert(0, row["nickname"] or "")
        self.date_entry.insert(0, row["acquired_date"] or "")
        if row["pot_size"] and row["pot_size"] in self._pot_sizes:
            self.pot_var.set(row["pot_size"])
        if row["health_status"]:
            self.health_var.set(row["health_status"])
        self.loc_entry.insert(0, row["location"] or "")
        if row["notes"]:
            self.notes_box.insert("0.0", row["notes"])

    def _save(self):
        species_id = self.species_dd.get_id()

        data = {
            "species_id":    species_id,
            "nickname":      self.nick_entry.get().strip() or None,
            "acquired_date": self.date_entry.get().strip() or None,
            "pot_size":      self.pot_var.get(),
            "health_status": self.health_var.get(),
            "location":      self.loc_entry.get().strip() or None,
            "notes":         self.notes_box.get("0.0", "end").strip() or None,
            "photo_paths":   self.photo_panel.get_photos_json(),
        }

        if self._row:
            PlantsModel.update(self._row["id"], **data)
        else:
            PlantsModel.create(**data)

        self.result = data
        self.destroy()
