"""
Reusable photo management widget.

photos format (JSON-serialisable list of dicts):
  [
    {"local": "C:/path/to/photo.jpg", "drive_id": "1abc…", "drive_url": "https://…"},
    ...
  ]
drive_id / drive_url are None until uploaded.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk

try:
    from PIL import Image
    PIL_OK = True
except ImportError:
    PIL_OK = False

THUMB   = 80
IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}


# ══════════════════════════════════════════════════════════════════════════════
class PhotoPanel(ctk.CTkFrame):
    """Thumbnail strip with add / remove / Drive-upload controls."""

    def __init__(self, parent, photos: list[dict] | None = None,
                 item_label: str = "item", **kwargs):
        super().__init__(parent, **kwargs)
        self._photos:       list[dict]              = list(photos or [])
        self._item_label:   str                     = item_label
        self._cache:        dict[str, ctk.CTkImage] = {}
        self._build()
        self._refresh()

    # ----------------------------------------------------------------- build
    def _build(self):
        self.grid_columnconfigure(0, weight=1)

        # ── header ────────────────────────────────────────────────────────
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 4))

        self._count_lbl = ctk.CTkLabel(
            hdr, text="Photos (0)",
            font=ctk.CTkFont(size=12, weight="bold"), anchor="w",
        )
        self._count_lbl.pack(side="left")

        self._upload_btn = ctk.CTkButton(
            hdr, text="Upload to Drive", width=130, height=26,
            font=ctk.CTkFont(size=11),
            fg_color="gray40", hover_color="gray30",
            state="disabled",
            command=self._start_upload,
        )
        self._upload_btn.pack(side="right", padx=(4, 0))

        ctk.CTkButton(
            hdr, text="+ Add Photos", width=100, height=26,
            font=ctk.CTkFont(size=11),
            command=self._add_photos,
        ).pack(side="right", padx=(4, 0))

        # ── thumbnail strip ───────────────────────────────────────────────
        self._strip = ctk.CTkScrollableFrame(
            self, height=THUMB + 52, orientation="horizontal",
            fg_color=("gray85", "gray20"),
        )
        self._strip.grid(row=1, column=0, sticky="ew")

        # ── upload status bar ─────────────────────────────────────────────
        self._status_lbl = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"), anchor="w",
        )
        self._status_lbl.grid(row=2, column=0, sticky="w", pady=(2, 0))

    # ----------------------------------------------------------------- refresh
    def _refresh(self):
        for w in self._strip.winfo_children():
            w.destroy()

        for i, photo in enumerate(self._photos):
            self._make_cell(i, photo)

        n = len(self._photos)
        self._count_lbl.configure(text=f"Photos ({n})")

        unsynced = sum(1 for p in self._photos if not p.get("drive_id"))
        if unsynced:
            self._upload_btn.configure(
                text=f"Upload {unsynced} to Drive", state="normal"
            )
        else:
            self._upload_btn.configure(text="Upload to Drive", state="disabled")

    def _make_cell(self, idx: int, photo: dict):
        cell = ctk.CTkFrame(self._strip, width=THUMB + 12, corner_radius=6,
                            fg_color=("gray78", "gray28"))
        cell.pack(side="left", padx=4, pady=4)
        cell.pack_propagate(False)

        local = photo.get("local", "")
        ctkimg = self._thumb(local)

        if ctkimg:
            ctk.CTkLabel(cell, image=ctkimg, text="",
                         width=THUMB, height=THUMB).pack(pady=(4, 0))
        else:
            name = Path(local).stem[:9] if local else "?"
            ctk.CTkLabel(
                cell, text=name, width=THUMB, height=THUMB,
                font=ctk.CTkFont(size=9),
                fg_color=("gray68", "gray35"), corner_radius=4,
            ).pack(pady=(4, 0))

        synced = bool(photo.get("drive_id"))
        ctk.CTkLabel(
            cell, text="☁ synced" if synced else "local",
            font=ctk.CTkFont(size=9),
            text_color="#3a9a4a" if synced else ("gray55", "gray60"),
        ).pack()

        ctk.CTkButton(
            cell, text="✕", width=22, height=18,
            font=ctk.CTkFont(size=10),
            fg_color="#8a3a3a", hover_color="#6a2a2a",
            command=lambda i=idx: self._remove(i),
        ).pack(pady=(2, 4))

    def _thumb(self, path: str) -> ctk.CTkImage | None:
        if not PIL_OK or not path:
            return None
        if path in self._cache:
            return self._cache[path]
        try:
            img = Image.open(path).copy()
            img.thumbnail((THUMB, THUMB), Image.LANCZOS)
            ctkimg = ctk.CTkImage(img, size=(THUMB, THUMB))
            self._cache[path] = ctkimg
            return ctkimg
        except Exception:
            return None

    # ----------------------------------------------------------------- actions
    def _add_photos(self):
        paths = filedialog.askopenfilenames(
            title="Select Photos",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.webp *.tiff"),
                ("All files", "*.*"),
            ],
        )
        existing = {p.get("local") for p in self._photos}
        for p in paths:
            if Path(p).suffix.lower() in IMG_EXT and p not in existing:
                self._photos.append({"local": p, "drive_id": None, "drive_url": None})
                existing.add(p)
        self._refresh()

    def _remove(self, idx: int):
        if 0 <= idx < len(self._photos):
            self._photos.pop(idx)
            self._refresh()

    def _start_upload(self):
        import integrations.config as cfg
        from integrations.google_sheets import is_connected

        creds = cfg.get("google_credentials_path")
        if not creds or not is_connected():
            self._status_lbl.configure(
                text="Connect Google in Settings first.", text_color="#c05020"
            )
            return

        self._upload_btn.configure(state="disabled", text="Uploading…")
        self._status_lbl.configure(text="Uploading photos to Drive…",
                                   text_color=("gray50", "gray60"))

        def _worker():
            try:
                from integrations import google_drive
                folder_id = google_drive.get_item_folder(
                    creds, "Photos", self._item_label
                )
                uploaded = 0
                for photo in self._photos:
                    if photo.get("drive_id"):
                        continue
                    local = photo.get("local", "")
                    if not local or not Path(local).exists():
                        continue
                    result = google_drive.upload_photo(creds, folder_id, local)
                    photo["drive_id"]  = result["drive_id"]
                    photo["drive_url"] = result["drive_url"]
                    uploaded += 1
                self.after(0, lambda n=uploaded: self._on_upload_done(n))
            except Exception as e:
                self.after(0, lambda err=str(e): self._on_upload_error(err))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_upload_done(self, n: int):
        self._status_lbl.configure(
            text=f"{n} photo{'s' if n != 1 else ''} uploaded to Drive.",
            text_color="#3a9a4a",
        )
        self._refresh()

    def _on_upload_error(self, err: str):
        self._status_lbl.configure(
            text=f"Upload failed: {err[:80]}", text_color="#c05020"
        )
        self._upload_btn.configure(state="normal", text="Retry Upload")

    # ----------------------------------------------------------------- I/O
    def get_photos(self) -> list[dict]:
        return list(self._photos)

    def get_photos_json(self) -> str:
        return json.dumps(self._photos)

    # ── static helpers ─────────────────────────────────────────────────────
    @staticmethod
    def parse(json_str: str | None) -> list[dict]:
        """Parse stored photo_paths JSON, handles both old (str list) and new (dict list) formats."""
        if not json_str:
            return []
        try:
            data = json.loads(json_str)
            if not isinstance(data, list):
                return []
            out = []
            for item in data:
                if isinstance(item, str):
                    out.append({"local": item, "drive_id": None, "drive_url": None})
                elif isinstance(item, dict):
                    out.append(item)
            return out
        except (json.JSONDecodeError, TypeError):
            return []
