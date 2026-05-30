import threading
import customtkinter as ctk
from datetime import date
from database.models import SalesModel, StockModel


class SaleDialog(ctk.CTkToplevel):
    PLATFORMS        = ["Facebook", "Shopify", "In Person", "Other"]
    SHIP_METHODS     = ["Local Pickup", "Shipped", "Delivered"]

    def __init__(self, parent, stock_row):
        super().__init__(parent)
        self.result = None
        self._stock = stock_row

        self.title(f"Record Sale — {stock_row['sku']}")
        self.geometry("440x560")
        self.minsize(440, 420)
        self.resizable(False, True)
        self.grab_set()

        self._build()
        self.after(100, self.lift)

    def _build(self):
        pad = {"padx": 20, "pady": 6}

        # Buttons pinned to bottom
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=(4, 16))
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray40",
                      command=self.destroy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btn_frame, text="Record Sale",
                      fg_color="#2a7a3a", hover_color="#1e5e2c",
                      command=self._save).pack(side="right")

        ctk.CTkFrame(self, height=1, fg_color=("gray80", "gray30")).pack(
            side="bottom", fill="x", padx=20, pady=(0, 4)
        )

        # Info banner (fixed at top)
        info = ctk.CTkFrame(self, fg_color=("gray80", "gray25"))
        info.pack(fill="x", padx=20, pady=(16, 4))
        sp = self._stock["species_name"] or "Unknown species"
        ctk.CTkLabel(
            info,
            text=f"{self._stock['sku']}  ·  {self._stock['item_type']}  ·  {sp}",
            font=ctk.CTkFont(weight="bold"),
        ).pack(padx=12, pady=8)

        # Scrollable form fields
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        f = scroll

        # Sale price
        ctk.CTkLabel(f, text="Sale Price ($) *", anchor="w").pack(fill="x", **pad)
        self.price_entry = ctk.CTkEntry(f, placeholder_text="0.00")
        self.price_entry.pack(fill="x", **pad)
        if self._stock["asking_price"]:
            self.price_entry.insert(0, str(self._stock["asking_price"]))

        # Platform
        ctk.CTkLabel(f, text="Platform", anchor="w").pack(fill="x", **pad)
        self.platform_var = ctk.StringVar(value="Facebook")
        ctk.CTkOptionMenu(f, variable=self.platform_var,
                          values=self.PLATFORMS).pack(fill="x", **pad)

        # Sale date
        ctk.CTkLabel(f, text="Sale Date (YYYY-MM-DD)", anchor="w").pack(fill="x", **pad)
        self.date_entry = ctk.CTkEntry(f)
        self.date_entry.insert(0, str(date.today()))
        self.date_entry.pack(fill="x", **pad)

        # Buyer
        ctk.CTkLabel(f, text="Buyer Name", anchor="w").pack(fill="x", **pad)
        self.buyer_entry = ctk.CTkEntry(f, placeholder_text="Optional")
        self.buyer_entry.pack(fill="x", **pad)

        ctk.CTkLabel(f, text="Buyer Contact (email / phone)", anchor="w").pack(fill="x", **pad)
        self.contact_entry = ctk.CTkEntry(f, placeholder_text="Optional")
        self.contact_entry.pack(fill="x", **pad)

        # Shipping
        ship_row = ctk.CTkFrame(f, fg_color="transparent")
        ship_row.pack(fill="x", **pad)
        left = ctk.CTkFrame(ship_row, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=(0, 6))
        right = ctk.CTkFrame(ship_row, fg_color="transparent")
        right.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(left, text="Shipping Method", anchor="w").pack(fill="x")
        self.ship_var = ctk.StringVar(value="Local Pickup")
        ctk.CTkOptionMenu(left, variable=self.ship_var,
                          values=self.SHIP_METHODS).pack(fill="x")

        ctk.CTkLabel(right, text="Shipping Cost ($)", anchor="w").pack(fill="x")
        self.ship_cost_entry = ctk.CTkEntry(right, placeholder_text="0.00")
        self.ship_cost_entry.insert(0, "0.00")
        self.ship_cost_entry.pack(fill="x")

        # Notes
        ctk.CTkLabel(f, text="Notes", anchor="w").pack(fill="x", **pad)
        self.notes_box = ctk.CTkTextbox(f, height=70)
        self.notes_box.pack(fill="x", **pad)

    def _save(self):
        try:
            sale_price = float(self.price_entry.get().strip())
        except ValueError:
            return

        def _float(widget):
            try:
                return float(widget.get().strip())
            except (ValueError, AttributeError):
                return 0.0

        sale_data = dict(
            stock_id        = self._stock["id"],
            listing_id      = None,
            sale_price      = sale_price,
            platform        = self.platform_var.get(),
            sale_date       = self.date_entry.get().strip() or str(date.today()),
            buyer_name      = self.buyer_entry.get().strip() or None,
            buyer_contact   = self.contact_entry.get().strip() or None,
            shipping_method = self.ship_var.get(),
            shipping_cost   = _float(self.ship_cost_entry),
            cost_basis      = self._stock["cost_basis"] or 0,
            notes           = self.notes_box.get("0.0", "end").strip() or None,
        )
        SalesModel.create(**sale_data)

        # Fire Gmail alerts in background — errors are silent (don't block the UI)
        threading.Thread(
            target=self._send_alerts,
            args=(sale_data,),
            daemon=True,
        ).start()

        self.result = True
        self.destroy()

    def _send_alerts(self, sale_data: dict):
        import integrations.config as cfg
        from integrations.gmail import (
            has_gmail_scope, send_sale_alert, send_low_stock_alert
        )

        creds     = cfg.get("google_credentials_path")
        to        = cfg.get("gmail_alert_email", "")
        if not creds or not to or not has_gmail_scope():
            return

        stock = dict(self._stock)
        # Compute profit for the sale_data dict (mirrors SalesModel.create logic)
        sale_data["profit"] = (
            (sale_data.get("sale_price") or 0)
            - (sale_data.get("cost_basis") or 0)
            - (sale_data.get("shipping_cost") or 0)
        )

        try:
            if cfg.get("gmail_sale_alerts"):
                send_sale_alert(creds, to, sale_data, stock)
        except Exception:
            pass

        try:
            if cfg.get("gmail_low_stock_alerts") and stock.get("species_id"):
                threshold = int(cfg.get("gmail_low_stock_threshold") or 2)
                remaining = StockModel.get_available_count_for_species(
                    stock["species_id"]
                )
                if remaining <= threshold:
                    send_low_stock_alert(
                        creds, to,
                        stock.get("species_name") or "Unknown",
                        remaining, threshold,
                    )
        except Exception:
            pass

        try:
            from integrations.shopify_store import is_configured, unpublish_item
            if is_configured():
                shop_url = cfg.get("shopify_shop_url")
                token    = cfg.get("shopify_access_token")
                unpublish_item(shop_url, token, sale_data["stock_id"])
        except Exception:
            pass
