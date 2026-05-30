"""
Facebook Marketplace listing dialog.

Pre-fills title / price / description / condition from the stock row,
lets the user edit, then launches Playwright to post. Saves the listing
URL to the database on success.
"""

from __future__ import annotations

import customtkinter as ctk
from database.models import ListingsModel, StockModel
from integrations.facebook import (
    CONDITIONS, CONDITION_MAP, build_listing_data, create_listing
)


class ListingDialog(ctk.CTkToplevel):

    def __init__(self, parent, stock_row):
        super().__init__(parent)
        self._stock = stock_row
        self._listing_id: int | None = None

        self.title(f"Post to FB Marketplace — {stock_row['sku']}")
        self.geometry("520x720")
        self.minsize(520, 480)
        self.resizable(False, True)
        self.grab_set()

        self._prefill = build_listing_data(stock_row)
        self._build()
        self.after(100, self.lift)

    # ----------------------------------------------------------------- build
    def _build(self):
        pad = {"padx": 20, "pady": 6}

        # Buttons pinned to bottom
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=(4, 16))
        ctk.CTkButton(
            btn_frame, text="Cancel", width=90,
            fg_color="gray40", command=self.destroy,
        ).pack(side="right", padx=(8, 0))
        self._post_btn = ctk.CTkButton(
            btn_frame,
            text="Post to Marketplace",
            width=180,
            fg_color="#1877F2", hover_color="#1155CC",
            command=self._post,
        )
        self._post_btn.pack(side="right")

        # Status label pinned above buttons
        self._status_lbl = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12), anchor="w",
            text_color=("gray50", "gray60"),
        )
        self._status_lbl.pack(side="bottom", fill="x", padx=20, pady=(0, 2))

        ctk.CTkFrame(self, height=1, fg_color=("gray80", "gray30")).pack(
            side="bottom", fill="x", padx=20, pady=(0, 4)
        )

        # Info banner fixed at top
        banner = ctk.CTkFrame(self, fg_color=("gray80", "gray25"))
        banner.pack(fill="x", padx=20, pady=(16, 4))
        sp = self._stock.get("species_name") or "?"
        ctk.CTkLabel(
            banner,
            text=f"{self._stock['sku']}  ·  {self._stock['item_type']}  ·  {sp}",
            font=ctk.CTkFont(weight="bold"),
        ).pack(padx=12, pady=8)

        # Scroll container
        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=0, pady=0)
        f = scroll

        # Title
        ctk.CTkLabel(f, text="Listing Title *", anchor="w").pack(fill="x", **pad)
        self._title_entry = ctk.CTkEntry(f, placeholder_text="Listing title")
        self._title_entry.insert(0, self._prefill["title"])
        self._title_entry.pack(fill="x", **pad)

        # Price
        ctk.CTkLabel(f, text="Price ($) *", anchor="w").pack(fill="x", **pad)
        self._price_entry = ctk.CTkEntry(f, placeholder_text="0")
        if self._prefill["price"]:
            self._price_entry.insert(0, str(int(self._prefill["price"])))
        self._price_entry.pack(fill="x", **pad)

        # Condition
        ctk.CTkLabel(f, text="Condition", anchor="w").pack(fill="x", **pad)
        self._cond_var = ctk.StringVar(value=self._prefill.get("condition", "Used - Good"))
        ctk.CTkOptionMenu(f, variable=self._cond_var, values=CONDITIONS).pack(fill="x", **pad)

        # Description
        ctk.CTkLabel(f, text="Description", anchor="w").pack(fill="x", **pad)
        self._desc_box = ctk.CTkTextbox(f, height=200)
        self._desc_box.insert("0.0", self._prefill.get("description", ""))
        self._desc_box.pack(fill="x", **pad)

        # Photo count note
        n_photos = len(self._prefill.get("photo_paths", []))
        ctk.CTkLabel(
            f,
            text=f"Photos: {n_photos} local image{'s' if n_photos != 1 else ''} will be uploaded."
                 if n_photos else "Photos: none — add photos in the stock edit dialog first.",
            text_color=("#2a7a3a" if n_photos else "#b87c1a"),
            font=ctk.CTkFont(size=11), anchor="w",
        ).pack(fill="x", padx=20, pady=(2, 8))

    # ----------------------------------------------------------------- post
    def _post(self):
        title = self._title_entry.get().strip()
        if not title:
            self._status("Title is required.", error=True)
            return

        try:
            price = float(self._price_entry.get().strip())
        except ValueError:
            self._status("Enter a valid price.", error=True)
            return

        listing_data = {
            "title":       title,
            "price":       price,
            "description": self._desc_box.get("0.0", "end").strip(),
            "condition":   self._cond_var.get(),
            "photo_paths": self._prefill["photo_paths"],
        }

        # Pre-save a listing record so we have an ID to update with the URL
        self._listing_id = ListingsModel.create(
            stock_id    = self._stock["id"],
            platform    = "Facebook",
            listed_price= price,
            listing_url = "",
        )

        self._post_btn.configure(state="disabled", text="Browser opening…")
        self._status(
            "A browser window is opening. Log in if prompted, "
            "then review the form and click Publish.",
            error=False,
        )

        create_listing(
            listing_data,
            on_done  = self._on_posted,
            on_error = self._on_error,
        )

    def _on_posted(self, url: str):
        if self._listing_id:
            ListingsModel.update_url(self._listing_id, url)
        self.after(0, lambda: self._status(
            f"Posted! URL saved.  {url[:60]}…" if len(url) > 60 else f"Posted! {url}",
            error=False,
        ))
        self.after(0, lambda: self._post_btn.configure(
            state="normal", text="Post Again"
        ))

    def _on_error(self, err: str):
        if self._listing_id:
            # Keep the listing record but without a URL
            pass
        self.after(0, lambda: self._status(f"Error: {err[:100]}", error=True))
        self.after(0, lambda: self._post_btn.configure(
            state="normal", text="Retry"
        ))

    def _status(self, msg: str, error: bool = False):
        self._status_lbl.configure(
            text=msg,
            text_color="#c05020" if error else "#3a9a4a",
        )
