import customtkinter as ctk
from datetime import datetime
from database.models import StockModel, SalesModel


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        # Header
        header = ctk.CTkLabel(
            self, text="Dashboard",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        header.grid(row=0, column=0, sticky="w", padx=24, pady=(20, 4))

        now = datetime.now()
        self._month_label = ctk.CTkLabel(
            self, text=now.strftime("%B %Y"),
            text_color=("gray50", "gray60"), anchor="w",
        )
        self._month_label.grid(row=1, column=0, sticky="w", padx=24, pady=(0, 16))

        # Stat cards container
        self._cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._cards_frame.grid(row=2, column=0, sticky="ew", padx=20)
        for i in range(4):
            self._cards_frame.grid_columnconfigure(i, weight=1, uniform="card")

        self._stock_cards  = {}
        self._sales_labels = {}
        self._recent_frame = None
        self.refresh()

    # ----------------------------------------------------------------- helpers
    def _stat_card(self, parent, col, title, value, color="#1f6aa5"):
        frame = ctk.CTkFrame(parent, corner_radius=10)
        frame.grid(row=0, column=col, padx=6, pady=4, sticky="ew")
        ctk.CTkLabel(frame, text=title, text_color=("gray55", "gray65"),
                     font=ctk.CTkFont(size=12)).pack(pady=(12, 2))
        lbl = ctk.CTkLabel(frame, text=value,
                           font=ctk.CTkFont(size=26, weight="bold"),
                           text_color=color)
        lbl.pack(pady=(0, 12))
        return lbl

    def _section_title(self, row, text):
        ctk.CTkLabel(
            self, text=text,
            font=ctk.CTkFont(size=14, weight="bold"), anchor="w",
        ).grid(row=row, column=0, sticky="w", padx=24, pady=(16, 4))

    # ----------------------------------------------------------------- refresh
    def refresh(self):
        # Clear cards
        for w in self._cards_frame.winfo_children():
            w.destroy()

        stock  = StockModel.get_dashboard_stats()
        now    = datetime.now()
        month  = SalesModel.get_monthly_stats(now.year, now.month)
        totals = SalesModel.get_all_time_stats()

        # Row 1 — inventory counts
        self._stat_card(self._cards_frame, 0, "Total Stock",   str(stock["total"]))
        self._stat_card(self._cards_frame, 1, "Available",     str(stock["available"]), "#2a7a3a")
        self._stat_card(self._cards_frame, 2, "Listed",        str(stock["listed"]),    "#b87c1a")
        self._stat_card(self._cards_frame, 3, "Sold (all)",    str(stock["sold"]),      "#6a3a9a")

        # Row 2 — type breakdown
        if not hasattr(self, "_types_frame") or not self._types_frame.winfo_exists():
            self._section_title(3, "Stock by Type")
            self._types_frame = ctk.CTkFrame(self, fg_color="transparent")
            self._types_frame.grid(row=4, column=0, sticky="ew", padx=20)
            for i in range(3):
                self._types_frame.grid_columnconfigure(i, weight=1, uniform="type")

        for w in self._types_frame.winfo_children():
            w.destroy()

        colors = {"Plant": "#1f6aa5", "Pup": "#2a7a3a", "Corm": "#b87c1a"}
        for i, kind in enumerate(["Plant", "Pup", "Corm"]):
            cnt = stock["by_type"].get(kind, 0)
            self._stat_card(self._types_frame, i, f"{kind}s", str(cnt), colors[kind])

        # Row 3 — financials
        if not hasattr(self, "_fin_frame") or not self._fin_frame.winfo_exists():
            self._section_title(5, "Financials")
            self._fin_frame = ctk.CTkFrame(self, fg_color="transparent")
            self._fin_frame.grid(row=6, column=0, sticky="ew", padx=20)
            for i in range(4):
                self._fin_frame.grid_columnconfigure(i, weight=1, uniform="fin")

        for w in self._fin_frame.winfo_children():
            w.destroy()

        self._stat_card(self._fin_frame, 0,
                        f"Sales This Month", str(month["count"]))
        self._stat_card(self._fin_frame, 1,
                        "Revenue This Month", f"${month['revenue']:.2f}", "#2a7a3a")
        self._stat_card(self._fin_frame, 2,
                        "Profit This Month",  f"${month['profit']:.2f}",  "#2a7a3a")
        self._stat_card(self._fin_frame, 3,
                        "Available Value",    f"${stock['available_value']:.2f}", "#b87c1a")

        # Recent sales
        if not hasattr(self, "_recent_title_drawn"):
            self._section_title(7, "Recent Sales")
            self._recent_title_drawn = True

        if self._recent_frame and self._recent_frame.winfo_exists():
            self._recent_frame.destroy()

        self._recent_frame = ctk.CTkScrollableFrame(self, height=180)
        self._recent_frame.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 20))
        self._recent_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        headers = ["Date", "SKU", "Type", "Species", "Sale Price", "Profit"]
        for c, h in enumerate(headers):
            ctk.CTkLabel(
                self._recent_frame, text=h,
                font=ctk.CTkFont(weight="bold"),
                text_color=("gray50", "gray60"),
            ).grid(row=0, column=c, padx=8, pady=(4, 2), sticky="w")

        sales = SalesModel.get_all()[:10]
        if not sales:
            ctk.CTkLabel(self._recent_frame, text="No sales recorded yet.",
                         text_color=("gray55", "gray65")).grid(
                row=1, column=0, columnspan=6, pady=12)
        else:
            for r, sale in enumerate(sales, start=1):
                vals = [
                    (sale["sale_date"] or "")[:10],
                    sale["sku"] or "—",
                    sale["item_type"] or "—",
                    sale["species_name"] or "—",
                    f"${sale['sale_price']:.2f}",
                    f"${sale['profit']:.2f}" if sale["profit"] is not None else "—",
                ]
                for c, v in enumerate(vals):
                    ctk.CTkLabel(self._recent_frame, text=v, anchor="w").grid(
                        row=r, column=c, padx=8, pady=2, sticky="w"
                    )
