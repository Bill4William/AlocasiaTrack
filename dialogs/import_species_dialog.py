"""
Import Species List dialog.

Shows all available seed packs from species_seeds/, previews what each
would add/update, and lets the user pick which ones to import.

Adding a new genus pack is as simple as dropping a .py file into
species_seeds/ — no code changes required.
"""

from __future__ import annotations

import threading
import customtkinter as ctk
from integrations.seed_manager import discover, preview, import_pack, SeedPack


class ImportSpeciesDialog(ctk.CTkToplevel):

    def __init__(self, parent, on_complete=None):
        super().__init__(parent)
        self._on_complete = on_complete
        self._packs:  list[SeedPack] = []
        self._checks: list[ctk.BooleanVar] = []
        self._previews: list[dict] = []
        self._busy   = False

        self.title("Import Species Lists")
        self.geometry("560x520")
        self.minsize(480, 360)
        self.resizable(True, True)
        self.grab_set()

        self._build_loading()
        self.after(80, self._load_packs)
        self.after(100, self.lift)

    # ── initial loading screen ────────────────────────────────────────────────

    def _build_loading(self):
        self._loading_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._loading_frame.pack(fill="both", expand=True)
        ctk.CTkLabel(
            self._loading_frame,
            text="Scanning for available species lists…",
            text_color=("gray55", "gray60"),
        ).pack(expand=True)

    def _load_packs(self):
        """Discover packs in a background thread then build the real UI."""
        def _worker():
            packs    = discover()
            previews = [preview(p) for p in packs]
            self.after(0, lambda: self._build_ui(packs, previews))
        threading.Thread(target=_worker, daemon=True).start()

    # ── main UI ───────────────────────────────────────────────────────────────

    def _build_ui(self, packs: list[SeedPack], previews: list[dict]):
        self._loading_frame.destroy()
        self._packs    = packs
        self._previews = previews

        # ── Header ────────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=24, pady=(20, 8))
        ctk.CTkLabel(
            hdr, text="Import Species Lists",
            font=ctk.CTkFont(size=20, weight="bold"), anchor="w",
        ).pack(fill="x")
        ctk.CTkLabel(
            hdr,
            text="Select one or more lists to add to your species database.\n"
                 "New species are added; existing entries have blank fields back-filled.",
            justify="left", anchor="w",
            text_color=("gray50", "gray60"),
            font=ctk.CTkFont(size=12),
        ).pack(fill="x", pady=(4, 0))

        # ── Pack cards ────────────────────────────────────────────────────────
        if not packs:
            self._build_empty()
            return

        self._checks = []
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(4, 0))
        scroll.grid_columnconfigure(0, weight=1)

        for i, (pack, prev) in enumerate(zip(packs, previews)):
            var = ctk.BooleanVar(value=True)
            self._checks.append(var)
            self._pack_card(scroll, i, pack, prev, var)

        # ── tip ───────────────────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="💡  Add more genus packs by dropping a .py file into the  species_seeds/  folder",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray55"),
            anchor="w",
        ).pack(fill="x", padx=24, pady=(6, 2))

        # ── buttons ───────────────────────────────────────────────────────────
        self._build_buttons()

    def _pack_card(self, parent, idx: int, pack: SeedPack,
                   prev: dict, var: ctk.BooleanVar):
        """One card per seed pack."""
        meta = pack.metadata
        card = ctk.CTkFrame(parent, corner_radius=10, border_width=1,
                             border_color=("gray75", "gray28"))
        card.grid(row=idx, column=0, sticky="ew", pady=(0, 8))
        card.grid_columnconfigure(1, weight=1)

        # Checkbox column
        ctk.CTkCheckBox(
            card, text="", variable=var, width=24,
            command=self._refresh_import_btn,
        ).grid(row=0, column=0, rowspan=3, padx=(14, 0), pady=14, sticky="n")

        # Emoji + name
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.grid(row=0, column=1, sticky="ew", padx=(8, 14), pady=(12, 2))
        top_row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            top_row, text=meta.get("emoji", "📦"),
            font=ctk.CTkFont(size=22), width=32,
        ).grid(row=0, column=0, padx=(0, 8))

        ctk.CTkLabel(
            top_row,
            text=meta.get("name", pack.path.stem.title()),
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
        ).grid(row=0, column=1, sticky="w")

        # Version + source
        sub = f"v{meta.get('version', '?')}  ·  {meta.get('author', '')}"
        ctk.CTkLabel(
            top_row, text=sub,
            font=ctk.CTkFont(size=11),
            text_color=("gray55", "gray55"),
            anchor="w",
        ).grid(row=0, column=2, sticky="e", padx=(8, 0))

        # Description
        ctk.CTkLabel(
            card,
            text=meta.get("description", ""),
            justify="left", anchor="w",
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray65"),
            wraplength=440,
        ).grid(row=1, column=1, sticky="ew", padx=(8, 14), pady=(0, 6))

        # Counts bar
        counts_frame = ctk.CTkFrame(card, fg_color=("gray88", "gray18"),
                                     corner_radius=6)
        counts_frame.grid(row=2, column=1, sticky="ew",
                           padx=(8, 14), pady=(0, 12))

        def _chip(parent, label, value, color):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(f, text=str(value),
                         font=ctk.CTkFont(size=15, weight="bold"),
                         text_color=color).pack()
            ctk.CTkLabel(f, text=label,
                         font=ctk.CTkFont(size=10),
                         text_color=("gray55", "gray55")).pack()

        _chip(counts_frame, "Total",    prev["total"],  ("gray20", "gray80"))
        _chip(counts_frame, "New",      prev["new"],    "#2a7a3a")
        _chip(counts_frame, "Updates",  prev["update"], "#b87c1a")
        _chip(counts_frame, "No change",prev["skip"],   ("gray55", "gray55"))

    def _build_empty(self):
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(fill="both", expand=True)
        ctk.CTkLabel(
            f, text="No seed packs found.",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("gray50", "gray60"),
        ).pack(pady=(0, 8))
        ctk.CTkLabel(
            f,
            text="Drop a .py file with METADATA and SPECIES into:\n"
                 "  species_seeds/",
            justify="center",
            text_color=("gray55", "gray60"),
            font=ctk.CTkFont(family="Courier", size=12),
        ).pack()
        ctk.CTkButton(self, text="Close", command=self.destroy,
                      fg_color="gray40").pack(pady=16)

    def _build_buttons(self):
        sep = ctk.CTkFrame(self, height=1, fg_color=("gray80", "gray30"))
        sep.pack(fill="x", padx=20, pady=(4, 0))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=(8, 16))

        ctk.CTkButton(
            btn_row, text="Cancel", fg_color="gray40", hover_color="gray30",
            command=self.destroy, width=90,
        ).pack(side="right", padx=(8, 0))

        self._import_btn = ctk.CTkButton(
            btn_row, text="Import Selected",
            fg_color="#2a7a3a", hover_color="#1e5e2c",
            command=self._start_import, width=160,
        )
        self._import_btn.pack(side="right")

        self._select_all_btn = ctk.CTkButton(
            btn_row, text="Select All", fg_color="gray38", hover_color="gray28",
            command=self._select_all, width=90,
        )
        self._select_all_btn.pack(side="left")

        # Progress / status label
        self._progress_lbl = ctk.CTkLabel(
            btn_row, text="", font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"), anchor="w",
        )
        self._progress_lbl.pack(side="left", padx=(10, 0))

        self._refresh_import_btn()

    # ── helpers ───────────────────────────────────────────────────────────────

    def _refresh_import_btn(self):
        selected = [p for p, v in zip(self._packs, self._checks) if v.get()]
        total_new = sum(
            self._previews[i]["new"] + self._previews[i]["update"]
            for i, v in enumerate(self._checks) if v.get()
        )
        if selected:
            self._import_btn.configure(
                text=f"Import Selected  ({total_new} changes)",
                state="normal",
            )
        else:
            self._import_btn.configure(
                text="Import Selected", state="disabled"
            )

    def _select_all(self):
        all_checked = all(v.get() for v in self._checks)
        for v in self._checks:
            v.set(not all_checked)
        self._select_all_btn.configure(
            text="Deselect All" if not all_checked else "Select All"
        )
        self._refresh_import_btn()

    # ── import ────────────────────────────────────────────────────────────────

    def _start_import(self):
        if self._busy:
            return
        selected = [(p, self._previews[i])
                    for i, (p, v) in enumerate(zip(self._packs, self._checks))
                    if v.get()]
        if not selected:
            return

        self._busy = True
        self._import_btn.configure(state="disabled", text="Importing…")

        def _worker():
            total_ins = total_upd = total_skip = 0
            for pack, _prev in selected:
                name = pack.metadata.get("name", pack.path.stem)
                self.after(0, lambda n=name: self._progress_lbl.configure(
                    text=f"Importing {n}…"
                ))
                result = import_pack(pack)
                total_ins  += result["inserted"]
                total_upd  += result["updated"]
                total_skip += result["skipped"]

            self.after(0, lambda: self._on_import_done(total_ins, total_upd, total_skip))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_import_done(self, inserted: int, updated: int, skipped: int):
        self._busy = False

        summary = []
        if inserted:
            summary.append(f"{inserted} added")
        if updated:
            summary.append(f"{updated} updated")
        if skipped:
            summary.append(f"{skipped} unchanged")

        self._progress_lbl.configure(
            text="✓  " + ", ".join(summary) if summary else "✓  Nothing to change",
            text_color=("#2a7a3a", "#4caf50"),
        )
        self._import_btn.configure(
            text="Done — Close",
            state="normal",
            fg_color="gray38", hover_color="gray28",
            command=self._finish,
        )

        if self._on_complete:
            self._on_complete()

    def _finish(self):
        self.destroy()
