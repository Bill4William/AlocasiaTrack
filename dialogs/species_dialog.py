import customtkinter as ctk
from database.models import SpeciesModel


class SpeciesDialog(ctk.CTkToplevel):
    CARE_LEVELS = ["Easy", "Moderate", "Difficult"]

    def __init__(self, parent, species_row=None):
        super().__init__(parent)
        self.result = None
        self._row = species_row

        self.title("Edit Species" if species_row else "Add Species")
        self.geometry("440x500")
        self.minsize(440, 380)
        self.resizable(False, True)
        self.grab_set()

        self._build()
        if species_row:
            self._populate(species_row)

        self.after(100, self.lift)

    def _build(self):
        pad = {"padx": 20, "pady": 6}

        # Buttons pinned to bottom
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=(4, 16))
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray40",
                      command=self.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btn_frame, text="Save", command=self._save).pack(side="right")

        ctk.CTkFrame(self, height=1, fg_color=("gray80", "gray30")).pack(
            side="bottom", fill="x", padx=20, pady=(0, 4)
        )

        # Scrollable form fields
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        f = scroll

        ctk.CTkLabel(f, text="Scientific / Cultivar Name *",
                     anchor="w").pack(fill="x", **pad)
        self.name_entry = ctk.CTkEntry(
            f, placeholder_text="e.g. baginda 'Dragon Scale'"
        )
        self.name_entry.pack(fill="x", **pad)

        ctk.CTkLabel(f, text="Common Name",
                     anchor="w").pack(fill="x", **pad)
        self.common_name_entry = ctk.CTkEntry(
            f, placeholder_text="e.g. Dragon Scale"
        )
        self.common_name_entry.pack(fill="x", **pad)

        ctk.CTkLabel(f, text="Care Level", anchor="w").pack(fill="x", **pad)
        self.care_var = ctk.StringVar(value="Moderate")
        self.care_menu = ctk.CTkOptionMenu(f, variable=self.care_var,
                                           values=self.CARE_LEVELS)
        self.care_menu.pack(fill="x", **pad)

        ctk.CTkLabel(f, text="Typical Price Range",
                     anchor="w").pack(fill="x", **pad)
        price_frame = ctk.CTkFrame(f, fg_color="transparent")
        price_frame.pack(fill="x", **pad)
        self.price_min = ctk.CTkEntry(price_frame, placeholder_text="Min $", width=140)
        self.price_min.pack(side="left", padx=(0, 8))
        ctk.CTkLabel(price_frame, text="—").pack(side="left")
        self.price_max = ctk.CTkEntry(price_frame, placeholder_text="Max $", width=140)
        self.price_max.pack(side="left", padx=(8, 0))

        ctk.CTkLabel(f, text="Notes", anchor="w").pack(fill="x", **pad)
        self.notes_box = ctk.CTkTextbox(f, height=110)
        self.notes_box.pack(fill="x", **pad)

    def _populate(self, row):
        self.name_entry.insert(0, row["name"] or "")
        self.common_name_entry.insert(0, row["common_name"] or "")
        care = row["care_level"] or "Moderate"
        # Normalise legacy values on display
        care = {"Medium": "Moderate", "Intermediate": "Moderate",
                "Advanced": "Difficult"}.get(care, care)
        if care not in self.CARE_LEVELS:
            care = "Moderate"
        self.care_var.set(care)
        if row["price_min"] is not None:
            self.price_min.insert(0, str(row["price_min"]))
        if row["price_max"] is not None:
            self.price_max.insert(0, str(row["price_max"]))
        if row["notes"]:
            self.notes_box.insert("0.0", row["notes"])

    def _save(self):
        name = self.name_entry.get().strip()
        if not name:
            ctk.CTkLabel(self, text="Name is required.", text_color="red").pack()
            return

        def _float(widget):
            try:
                return float(widget.get().strip())
            except (ValueError, AttributeError):
                return None

        self.result = {
            "name":        name,
            "common_name": self.common_name_entry.get().strip() or "",
            "care_level":  self.care_var.get(),
            "price_min":   _float(self.price_min),
            "price_max":   _float(self.price_max),
            "notes":       self.notes_box.get("0.0", "end").strip(),
        }

        if self._row:
            SpeciesModel.update(self._row["id"], **self.result)
        else:
            SpeciesModel.create(**self.result)

        self.destroy()
