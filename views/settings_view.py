"""
Settings view — Google Sheets integration setup and sync controls.

Setup flow (3 steps shown sequentially):
  Step 1  →  Browse for credentials.json
  Step 2  →  Connect Google Account (OAuth browser flow in thread)
  Step 3  →  Enter / create spreadsheet, then Sync Now
"""

from __future__ import annotations

import threading
import webbrowser
import customtkinter as ctk
from tkinter import filedialog

import integrations.config as cfg
from integrations.google_sheets import (
    is_connected, connect, disconnect,
    create_spreadsheet, sync_all, spreadsheet_url,
)


# ══════════════════════════════════════════════════════════════════════════════
class SettingsView(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self._build()

    # ---------------------------------------------------------------- build
    def _build(self):
        ctk.CTkLabel(
            self, text="Settings",
            font=ctk.CTkFont(size=22, weight="bold"), anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 4))

        tabs = ctk.CTkTabview(self)
        tabs.grid(row=1, column=0, sticky="nsew", padx=20, pady=(4, 20))
        self.grid_rowconfigure(1, weight=1)

        tabs.add("General")
        tabs.add("Google Sheets")
        tabs.add("Gmail Alerts")
        tabs.add("Facebook")
        tabs.add("Shopify")
        tabs.add("About")

        self._build_general_tab(tabs.tab("General"))
        self._build_sheets_tab(tabs.tab("Google Sheets"))
        self._build_gmail_tab(tabs.tab("Gmail Alerts"))
        self._build_facebook_tab(tabs.tab("Facebook"))
        self._build_shopify_tab(tabs.tab("Shopify"))
        self._build_about_tab(tabs.tab("About"))

    # ── General tab ───────────────────────────────────────────────────────
    def _build_general_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        s = self._section(parent, 0, "Pot Sizes")
        ctk.CTkLabel(
            s, text="Customise the pot sizes available when adding stock or mother plants.",
            anchor="w", wraplength=480, text_color=("gray50", "gray60"),
        ).pack(fill="x", padx=16, pady=(0, 10))

        # Scrollable list of current pot sizes
        list_frame = ctk.CTkScrollableFrame(s, height=180, fg_color=("gray90", "gray17"))
        list_frame.pack(fill="x", padx=16, pady=(0, 8))
        list_frame.grid_columnconfigure(0, weight=1)
        self._pot_list_frame = list_frame
        self._refresh_pot_list()

        # Add new size row
        add_row = ctk.CTkFrame(s, fg_color="transparent")
        add_row.pack(fill="x", padx=16, pady=(0, 8))
        self._new_pot_entry = ctk.CTkEntry(add_row, placeholder_text='e.g. 14"')
        self._new_pot_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(add_row, text="+ Add", width=80,
                      command=self._add_pot_size).pack(side="left")

        # Reset button
        ctk.CTkButton(
            s, text="Reset to Defaults", width=140,
            fg_color="gray40", hover_color="gray30",
            command=self._reset_pot_sizes,
        ).pack(anchor="w", padx=16, pady=(0, 12))

    def _refresh_pot_list(self):
        from integrations.config import get_pot_sizes
        for w in self._pot_list_frame.winfo_children():
            w.destroy()
        sizes = get_pot_sizes()
        for i, size in enumerate(sizes):
            row = ctk.CTkFrame(self._pot_list_frame, fg_color="transparent")
            row.pack(fill="x", pady=1)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(row, text=size, anchor="w").pack(side="left", padx=(8, 0))
            ctk.CTkButton(
                row, text="↑", width=28, height=24,
                fg_color="gray35", hover_color="gray25",
                command=lambda idx=i: self._move_pot_size(idx, -1),
            ).pack(side="right", padx=2)
            ctk.CTkButton(
                row, text="↓", width=28, height=24,
                fg_color="gray35", hover_color="gray25",
                command=lambda idx=i: self._move_pot_size(idx, 1),
            ).pack(side="right", padx=2)
            ctk.CTkButton(
                row, text="✕", width=28, height=24,
                fg_color="#6a2020", hover_color="#4a1010",
                command=lambda idx=i: self._remove_pot_size(idx),
            ).pack(side="right", padx=(2, 4))

    def _add_pot_size(self):
        val = self._new_pot_entry.get().strip()
        if not val:
            return
        from integrations.config import get_pot_sizes
        sizes = get_pot_sizes()
        if val not in sizes:
            sizes.append(val)
            cfg.set_value("pot_sizes", sizes)
        self._new_pot_entry.delete(0, "end")
        self._refresh_pot_list()

    def _remove_pot_size(self, index: int):
        from integrations.config import get_pot_sizes
        sizes = get_pot_sizes()
        if 0 <= index < len(sizes):
            sizes.pop(index)
            cfg.set_value("pot_sizes", sizes)
        self._refresh_pot_list()

    def _move_pot_size(self, index: int, direction: int):
        from integrations.config import get_pot_sizes
        sizes = get_pot_sizes()
        new_idx = index + direction
        if 0 <= new_idx < len(sizes):
            sizes[index], sizes[new_idx] = sizes[new_idx], sizes[index]
            cfg.set_value("pot_sizes", sizes)
        self._refresh_pot_list()

    def _reset_pot_sizes(self):
        from integrations.config import DEFAULT_POT_SIZES
        cfg.set_value("pot_sizes", list(DEFAULT_POT_SIZES))
        self._refresh_pot_list()

    # ── Google Sheets tab ─────────────────────────────────────────────────
    def _build_sheets_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        # ── Step 1: Credentials ──────────────────────────────────────────
        s1 = self._section(parent, 0, "Step 1 — Google Cloud Credentials")

        ctk.CTkLabel(
            s1,
            text=(
                "1. Go to console.cloud.google.com\n"
                "2. Create a project → Enable 'Google Sheets API' and 'Google Drive API'\n"
                "3. APIs & Services → Credentials → Create OAuth 2.0 Client ID (Desktop app)\n"
                "4. Download the JSON file and select it below."
            ),
            justify="left",
            text_color=("gray40", "gray70"),
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=16, pady=(6, 8))

        creds_row = ctk.CTkFrame(s1, fg_color="transparent")
        creds_row.pack(fill="x", padx=16, pady=(0, 10))

        self._creds_entry = ctk.CTkEntry(
            creds_row, placeholder_text="Path to credentials.json", width=420
        )
        self._creds_entry.pack(side="left", padx=(0, 8))
        saved = cfg.get("google_credentials_path")
        if saved:
            self._creds_entry.insert(0, saved)

        ctk.CTkButton(
            creds_row, text="Browse…", width=90,
            command=self._browse_credentials,
        ).pack(side="left")

        # ── Step 2: Connect ───────────────────────────────────────────────
        s2 = self._section(parent, 1, "Step 2 — Connect Google Account")

        self._connect_status = ctk.CTkLabel(
            s2, text="", font=ctk.CTkFont(size=13), anchor="w"
        )
        self._connect_status.pack(anchor="w", padx=16, pady=(6, 6))

        connect_row = ctk.CTkFrame(s2, fg_color="transparent")
        connect_row.pack(anchor="w", padx=16, pady=(0, 10))

        self._connect_btn = ctk.CTkButton(
            connect_row, text="Connect Google Account", width=200,
            command=self._connect,
        )
        self._connect_btn.pack(side="left", padx=(0, 8))

        self._disconnect_btn = ctk.CTkButton(
            connect_row, text="Disconnect", width=110,
            fg_color="gray40", hover_color="gray30",
            command=self._disconnect,
        )
        self._disconnect_btn.pack(side="left")

        # ── Step 3: Spreadsheet ───────────────────────────────────────────
        s3 = self._section(parent, 2, "Step 3 — Spreadsheet")

        ctk.CTkLabel(
            s3,
            text="Paste a Google Sheets ID (the part between /d/ and /edit in the URL),\nor click 'Create New Sheet' to generate one automatically.",
            justify="left",
            text_color=("gray40", "gray70"),
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=16, pady=(6, 8))

        sheet_row = ctk.CTkFrame(s3, fg_color="transparent")
        sheet_row.pack(fill="x", padx=16, pady=(0, 6))

        self._sheet_entry = ctk.CTkEntry(
            sheet_row, placeholder_text="Spreadsheet ID", width=360
        )
        self._sheet_entry.pack(side="left", padx=(0, 8))
        saved_id = cfg.get("google_spreadsheet_id")
        if saved_id:
            self._sheet_entry.insert(0, saved_id)

        ctk.CTkButton(
            sheet_row, text="Save ID", width=80,
            command=self._save_sheet_id,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            sheet_row, text="Create New Sheet", width=140,
            fg_color="gray40",
            command=self._create_sheet,
        ).pack(side="left")

        self._sheet_link_btn = ctk.CTkButton(
            s3, text="Open in Browser", width=140,
            fg_color="transparent", hover_color=("gray80", "gray30"),
            text_color=("#1f6aa5", "#4da6ff"),
            command=self._open_sheet,
        )
        self._sheet_link_btn.pack(anchor="w", padx=16, pady=(0, 4))

        # ── Sync ──────────────────────────────────────────────────────────
        s4 = self._section(parent, 3, "Sync")

        self._sync_status = ctk.CTkLabel(
            s4, text="", font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"), anchor="w",
        )
        self._sync_status.pack(anchor="w", padx=16, pady=(6, 4))

        sync_row = ctk.CTkFrame(s4, fg_color="transparent")
        sync_row.pack(anchor="w", padx=16, pady=(0, 12))

        self._sync_btn = ctk.CTkButton(
            sync_row, text="Sync All to Google Sheets", width=220,
            fg_color="#2a7a3a", hover_color="#1e5e2c",
            command=self._sync,
        )
        self._sync_btn.pack(side="left", padx=(0, 8))

        self._sync_progress = ctk.CTkProgressBar(sync_row, width=180, mode="indeterminate")

        self._refresh_ui()

    # ── Gmail Alerts tab ──────────────────────────────────────────────────
    def _build_gmail_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        # ── Scope status ─────────────────────────────────────────────────
        s1 = self._section(parent, 0, "Gmail Authorization")

        self._gmail_scope_lbl = ctk.CTkLabel(
            s1, text="", anchor="w", font=ctk.CTkFont(size=12)
        )
        self._gmail_scope_lbl.pack(anchor="w", padx=16, pady=(6, 4))

        ctk.CTkLabel(
            s1,
            text="Gmail requires re-authorization if you connected before Phase 4.\n"
                 "Click Re-authorize below — your browser will open once.",
            justify="left",
            text_color=("gray45", "gray65"),
            font=ctk.CTkFont(size=11),
        ).pack(anchor="w", padx=16, pady=(0, 4))

        reauth_row = ctk.CTkFrame(s1, fg_color="transparent")
        reauth_row.pack(anchor="w", padx=16, pady=(0, 10))
        ctk.CTkButton(
            reauth_row, text="Re-authorize (add Gmail scope)", width=230,
            command=self._reauthorize,
        ).pack(side="left", padx=(0, 8))
        self._reauth_status = ctk.CTkLabel(
            reauth_row, text="", font=ctk.CTkFont(size=12)
        )
        self._reauth_status.pack(side="left")

        # ── Alert destination ─────────────────────────────────────────────
        s2 = self._section(parent, 1, "Alert Destination")

        ctk.CTkLabel(s2, text="Send alerts to:", anchor="w").pack(
            anchor="w", padx=16, pady=(6, 2)
        )
        dest_row = ctk.CTkFrame(s2, fg_color="transparent")
        dest_row.pack(fill="x", padx=16, pady=(0, 10))

        self._alert_email_entry = ctk.CTkEntry(
            dest_row, placeholder_text="your@email.com", width=300
        )
        self._alert_email_entry.pack(side="left", padx=(0, 8))
        saved_email = cfg.get("gmail_alert_email") or ""
        if saved_email:
            self._alert_email_entry.insert(0, saved_email)

        ctk.CTkButton(
            dest_row, text="Save", width=70,
            command=self._save_alert_email,
        ).pack(side="left")

        # ── Alert toggles ─────────────────────────────────────────────────
        s3 = self._section(parent, 2, "Alert Types")

        self._sale_alerts_var = ctk.BooleanVar(
            value=bool(cfg.get("gmail_sale_alerts"))
        )
        ctk.CTkCheckBox(
            s3,
            text="Sale confirmation  (sent when you record a sale)",
            variable=self._sale_alerts_var,
            command=lambda: cfg.set_value("gmail_sale_alerts",
                                          self._sale_alerts_var.get()),
        ).pack(anchor="w", padx=16, pady=(8, 4))

        self._lowstock_var = ctk.BooleanVar(
            value=bool(cfg.get("gmail_low_stock_alerts"))
        )
        ctk.CTkCheckBox(
            s3,
            text="Low stock alert  (sent when a species drops to or below threshold)",
            variable=self._lowstock_var,
            command=lambda: cfg.set_value("gmail_low_stock_alerts",
                                          self._lowstock_var.get()),
        ).pack(anchor="w", padx=16, pady=(0, 6))

        thresh_row = ctk.CTkFrame(s3, fg_color="transparent")
        thresh_row.pack(anchor="w", padx=32, pady=(0, 10))
        ctk.CTkLabel(thresh_row, text="Threshold:").pack(side="left", padx=(0, 8))
        self._thresh_entry = ctk.CTkEntry(thresh_row, width=60)
        self._thresh_entry.insert(0, str(cfg.get("gmail_low_stock_threshold") or 2))
        self._thresh_entry.pack(side="left", padx=(0, 8))
        ctk.CTkLabel(thresh_row, text="available items",
                     text_color=("gray50", "gray60")).pack(side="left")
        ctk.CTkButton(
            thresh_row, text="Save", width=60,
            command=self._save_threshold,
        ).pack(side="left", padx=(8, 0))

        # ── Test ──────────────────────────────────────────────────────────
        s4 = self._section(parent, 3, "Test")

        test_row = ctk.CTkFrame(s4, fg_color="transparent")
        test_row.pack(anchor="w", padx=16, pady=(8, 12))

        ctk.CTkButton(
            test_row, text="Send Test Email", width=150,
            command=self._send_test,
        ).pack(side="left", padx=(0, 12))

        self._test_status = ctk.CTkLabel(
            test_row, text="", font=ctk.CTkFont(size=12)
        )
        self._test_status.pack(side="left")

        self._refresh_gmail_ui()

    # ── Facebook tab ──────────────────────────────────────────────────────
    def _build_facebook_tab(self, parent):
        from integrations.facebook import is_session_saved, clear_session, CONDITIONS

        parent.grid_columnconfigure(0, weight=1)

        # ── How it works ─────────────────────────────────────────────────
        s0 = self._section(parent, 0, "How It Works")
        ctk.CTkLabel(
            s0,
            text=(
                "AlocasiaTrack opens a real Chrome window to post listings.\n"
                "No passwords are stored — your login session is saved as cookies.\n\n"
                "1. Click 'Login to Facebook' below.\n"
                "2. Log in manually in the browser (handles 2FA automatically).\n"
                "3. The browser closes and saves your session.\n"
                "4. Use 'Post to FB' on any stock item to create a listing."
            ),
            justify="left",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
        ).pack(anchor="w", padx=16, pady=(6, 10))

        # ── Session status ────────────────────────────────────────────────
        s1 = self._section(parent, 1, "Facebook Session")

        self._fb_session_lbl = ctk.CTkLabel(
            s1, text="", font=ctk.CTkFont(size=13), anchor="w"
        )
        self._fb_session_lbl.pack(anchor="w", padx=16, pady=(6, 6))

        fb_btn_row = ctk.CTkFrame(s1, fg_color="transparent")
        fb_btn_row.pack(anchor="w", padx=16, pady=(0, 10))

        self._fb_login_btn = ctk.CTkButton(
            fb_btn_row, text="Login to Facebook", width=170,
            fg_color="#1877F2", hover_color="#1155CC",
            command=self._fb_login,
        )
        self._fb_login_btn.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            fb_btn_row, text="Clear Session", width=120,
            fg_color="gray40", hover_color="gray30",
            command=self._fb_clear_session,
        ).pack(side="left")

        self._fb_login_status = ctk.CTkLabel(
            s1, text="", font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"), anchor="w",
        )
        self._fb_login_status.pack(anchor="w", padx=16, pady=(0, 8))

        # ── Listing defaults ──────────────────────────────────────────────
        s2 = self._section(parent, 2, "Listing Defaults")

        ctk.CTkLabel(s2, text="Default Location (city or zip)",
                     anchor="w").pack(anchor="w", padx=16, pady=(6, 2))
        loc_row = ctk.CTkFrame(s2, fg_color="transparent")
        loc_row.pack(fill="x", padx=16, pady=(0, 8))
        self._fb_loc_entry = ctk.CTkEntry(loc_row, placeholder_text="e.g. Nashville, TN", width=280)
        saved_loc = cfg.get("fb_default_location") or ""
        if saved_loc:
            self._fb_loc_entry.insert(0, saved_loc)
        self._fb_loc_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(loc_row, text="Save", width=70,
                      command=self._save_fb_location).pack(side="left")

        ctk.CTkLabel(s2, text="Hashtags (appended to every description)",
                     anchor="w").pack(anchor="w", padx=16, pady=(4, 2))
        tag_row = ctk.CTkFrame(s2, fg_color="transparent")
        tag_row.pack(fill="x", padx=16, pady=(0, 10))
        self._fb_tags_entry = ctk.CTkEntry(tag_row, width=360)
        saved_tags = cfg.get("fb_default_hashtags") or ""
        if saved_tags:
            self._fb_tags_entry.insert(0, saved_tags)
        self._fb_tags_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(tag_row, text="Save", width=70,
                      command=self._save_fb_hashtags).pack(side="left")

        # ── Playwright install check ──────────────────────────────────────
        s3 = self._section(parent, 3, "Browser Requirement")

        self._pw_status_lbl = ctk.CTkLabel(
            s3, text="", font=ctk.CTkFont(size=12), anchor="w"
        )
        self._pw_status_lbl.pack(anchor="w", padx=16, pady=(6, 4))

        pw_btn_row = ctk.CTkFrame(s3, fg_color="transparent")
        pw_btn_row.pack(anchor="w", padx=16, pady=(0, 10))

        self._pw_install_btn = ctk.CTkButton(
            pw_btn_row, text="Install Playwright + Chromium", width=230,
            command=self._install_playwright,
        )
        self._pw_install_btn.pack(side="left", padx=(0, 10))

        self._pw_progress = ctk.CTkProgressBar(pw_btn_row, width=160, mode="indeterminate")

        ctk.CTkLabel(
            s3,
            text="Or install manually in a terminal:\n\n"
                 "   pip install playwright\n"
                 "   playwright install chromium",
            justify="left", font=ctk.CTkFont(family="Consolas", size=11),
            text_color=("gray40", "gray70"),
        ).pack(anchor="w", padx=16, pady=(0, 10))

        self._refresh_pw_ui()

        self._refresh_fb_ui()

    # ── Shopify tab ───────────────────────────────────────────────────────
    def _build_shopify_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        # ── Setup instructions ────────────────────────────────────────────
        s0 = self._section(parent, 0, "How to Get an Access Token")
        ctk.CTkLabel(
            s0,
            text=(
                "1. Go to your Shopify Admin → Settings → Apps and sales channels\n"
                "2. Click 'Develop apps' → 'Create an app'\n"
                "3. Under 'Configuration', grant the 'products' Admin API scope\n"
                "   (write_products + read_products)\n"
                "4. Click 'Install app' → copy the Admin API access token\n"
                "5. Paste the token and your store URL below."
            ),
            justify="left",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
        ).pack(anchor="w", padx=16, pady=(6, 10))

        # ── Credentials ───────────────────────────────────────────────────
        s1 = self._section(parent, 1, "Store Credentials")

        ctk.CTkLabel(s1, text="Shop URL (e.g. mystore.myshopify.com)",
                     anchor="w").pack(anchor="w", padx=16, pady=(6, 2))
        url_row = ctk.CTkFrame(s1, fg_color="transparent")
        url_row.pack(fill="x", padx=16, pady=(0, 8))
        self._shop_url_entry = ctk.CTkEntry(
            url_row, placeholder_text="mystore.myshopify.com", width=320
        )
        saved_url = cfg.get("shopify_shop_url") or ""
        if saved_url:
            self._shop_url_entry.insert(0, saved_url)
        self._shop_url_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(url_row, text="Save", width=70,
                      command=self._save_shopify_url).pack(side="left")

        ctk.CTkLabel(s1, text="Admin API Access Token",
                     anchor="w").pack(anchor="w", padx=16, pady=(4, 2))
        token_row = ctk.CTkFrame(s1, fg_color="transparent")
        token_row.pack(fill="x", padx=16, pady=(0, 8))
        self._shop_token_entry = ctk.CTkEntry(
            token_row, placeholder_text="shpat_…", width=320, show="*"
        )
        saved_token = cfg.get("shopify_access_token") or ""
        if saved_token:
            self._shop_token_entry.insert(0, saved_token)
        self._shop_token_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(token_row, text="Save", width=70,
                      command=self._save_shopify_token).pack(side="left")

        # Test button + status
        test_row = ctk.CTkFrame(s1, fg_color="transparent")
        test_row.pack(anchor="w", padx=16, pady=(0, 12))
        self._shopify_test_btn = ctk.CTkButton(
            test_row, text="Test Connection", width=150,
            command=self._shopify_test,
        )
        self._shopify_test_btn.pack(side="left", padx=(0, 10))
        self._shopify_conn_lbl = ctk.CTkLabel(
            test_row, text="", font=ctk.CTkFont(size=12)
        )
        self._shopify_conn_lbl.pack(side="left")

        # ── Sync ──────────────────────────────────────────────────────────
        s2 = self._section(parent, 2, "Sync Available Inventory")

        ctk.CTkLabel(
            s2,
            text=(
                "Pushes every 'Available' stock item to your Shopify store as a product.\n"
                "Items already synced are updated rather than duplicated.\n"
                "When you record a sale, the product is automatically unpublished."
            ),
            justify="left",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
        ).pack(anchor="w", padx=16, pady=(6, 8))

        self._shopify_sync_status = ctk.CTkLabel(
            s2, text="", font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"), anchor="w",
        )
        self._shopify_sync_status.pack(anchor="w", padx=16, pady=(0, 4))

        sync_row = ctk.CTkFrame(s2, fg_color="transparent")
        sync_row.pack(anchor="w", padx=16, pady=(0, 12))

        self._shopify_sync_btn = ctk.CTkButton(
            sync_row, text="Sync All Available to Shopify", width=230,
            fg_color="#96bf48", hover_color="#7aab2e", text_color="#1a1a1a",
            command=self._shopify_sync_all,
        )
        self._shopify_sync_btn.pack(side="left", padx=(0, 8))

        self._shopify_progress = ctk.CTkProgressBar(
            sync_row, width=160, mode="indeterminate"
        )

        self._refresh_shopify_ui()

    # ── About tab ─────────────────────────────────────────────────────────
    def _build_about_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            parent,
            text="AlocasiaTrack\nv1.0",
            font=ctk.CTkFont(size=14, weight="bold"),
            justify="center",
        ).pack(pady=(30, 4))
        ctk.CTkLabel(
            parent,
            text=(
                "Integrations:\n"
                "  - Google Sheets sync\n"
                "  - Google Drive photo storage\n"
                "  - Gmail alerts\n"
                "  - Facebook Marketplace listings\n"
                "  - Shopify storefront inventory sync"
            ),
            justify="left",
            text_color=("gray45", "gray65"),
        ).pack(pady=12)

    # ---------------------------------------------------------------- helpers
    def _section(self, parent, row: int, title: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(parent, corner_radius=8)
        frame.grid(row=row, column=0, sticky="ew", padx=0, pady=(0, 12))
        frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            frame, text=title,
            font=ctk.CTkFont(size=13, weight="bold"), anchor="w",
        ).pack(anchor="w", padx=16, pady=(12, 0))
        return frame

    def _refresh_ui(self):
        connected = is_connected()
        last_sync = cfg.get("last_sync")
        sheet_id  = cfg.get("google_spreadsheet_id")

        if connected:
            self._connect_status.configure(
                text="Connected", text_color="#3a9a4a"
            )
            self._connect_btn.configure(state="disabled")
            self._disconnect_btn.configure(state="normal")
        else:
            self._connect_status.configure(
                text="Not connected", text_color=("gray50", "gray60")
            )
            self._connect_btn.configure(state="normal")
            self._disconnect_btn.configure(state="disabled")

        if last_sync:
            self._sync_status.configure(text=f"Last sync: {last_sync}")
        else:
            self._sync_status.configure(text="Never synced")

        if sheet_id:
            self._sheet_link_btn.configure(state="normal")
        else:
            self._sheet_link_btn.configure(state="disabled")

    # ---------------------------------------------------------------- actions
    def _browse_credentials(self):
        path = filedialog.askopenfilename(
            title="Select credentials.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if path:
            self._creds_entry.delete(0, "end")
            self._creds_entry.insert(0, path)
            cfg.set_value("google_credentials_path", path)

    def _connect(self):
        creds_path = self._creds_entry.get().strip()
        if not creds_path:
            self._connect_status.configure(
                text="Select credentials.json first.", text_color="#c05020"
            )
            return

        self._connect_btn.configure(state="disabled",
                                    text="Opening browser…")
        self._connect_status.configure(
            text="Waiting for Google sign-in…",
            text_color=("gray50", "gray60"),
        )
        cfg.set_value("google_credentials_path", creds_path)

        def _worker():
            try:
                email = connect(creds_path)
                self.after(0, lambda: self._on_connected(email))
            except Exception as e:
                self.after(0, lambda err=str(e): self._on_connect_error(err))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_connected(self, email: str):
        self._connect_status.configure(
            text=f"Connected as {email}", text_color="#3a9a4a"
        )
        self._connect_btn.configure(state="disabled", text="Connect Google Account")
        self._disconnect_btn.configure(state="normal")

    def _on_connect_error(self, err: str):
        self._connect_status.configure(
            text=f"Error: {err[:80]}", text_color="#c05020"
        )
        self._connect_btn.configure(state="normal", text="Connect Google Account")

    def _disconnect(self):
        disconnect()
        self._refresh_ui()

    def _save_sheet_id(self):
        id_ = self._sheet_entry.get().strip()
        if id_:
            cfg.set_value("google_spreadsheet_id", id_)
            self._sheet_link_btn.configure(state="normal")

    def _create_sheet(self):
        creds_path = cfg.get("google_credentials_path")
        if not creds_path or not is_connected():
            self._sync_status.configure(
                text="Connect your Google account first.", text_color="#c05020"
            )
            return

        self._sync_btn.configure(state="disabled")
        self._sync_status.configure(text="Creating spreadsheet…",
                                    text_color=("gray50", "gray60"))

        def _worker():
            try:
                sid = create_spreadsheet(creds_path)
                self.after(0, lambda: self._on_sheet_created(sid))
            except Exception as e:
                self.after(0, lambda err=str(e): self._on_sync_error(err))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_sheet_created(self, sheet_id: str):
        self._sheet_entry.delete(0, "end")
        self._sheet_entry.insert(0, sheet_id)
        self._sheet_link_btn.configure(state="normal")
        self._sync_btn.configure(state="normal")
        self._sync_status.configure(
            text="Spreadsheet created. Click 'Sync All' to push your data.",
            text_color="#3a9a4a",
        )

    def _open_sheet(self):
        sid = cfg.get("google_spreadsheet_id")
        if sid:
            webbrowser.open(spreadsheet_url(sid))

    def _sync(self):
        creds_path = cfg.get("google_credentials_path")
        sheet_id   = self._sheet_entry.get().strip() or cfg.get("google_spreadsheet_id")

        if not creds_path:
            self._sync_status.configure(
                text="Set up credentials first.", text_color="#c05020"
            )
            return
        if not is_connected():
            self._sync_status.configure(
                text="Connect your Google account first.", text_color="#c05020"
            )
            return
        if not sheet_id:
            self._sync_status.configure(
                text="Enter or create a spreadsheet ID first.", text_color="#c05020"
            )
            return

        cfg.set_value("google_spreadsheet_id", sheet_id)
        self._sync_btn.configure(state="disabled")
        self._sync_progress.pack(side="left")
        self._sync_progress.start()
        self._sync_status.configure(text="Syncing…",
                                    text_color=("gray50", "gray60"))

        def _worker():
            try:
                results = sync_all(creds_path, sheet_id)
                self.after(0, lambda r=results: self._on_sync_done(r))
            except Exception as e:
                self.after(0, lambda err=str(e): self._on_sync_error(err))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_sync_done(self, results: dict):
        self._sync_progress.stop()
        self._sync_progress.pack_forget()
        self._sync_btn.configure(state="normal")
        parts = ", ".join(f"{v} {k}" for k, v in results.items())
        last  = cfg.get("last_sync")
        self._sync_status.configure(
            text=f"Sync complete ({parts})  —  {last}",
            text_color="#3a9a4a",
        )

    def _on_sync_error(self, err: str):
        self._sync_progress.stop()
        self._sync_progress.pack_forget()
        self._sync_btn.configure(state="normal")
        self._sync_status.configure(
            text=f"Error: {err[:120]}", text_color="#c05020"
        )

    # ---------------------------------------------------------------- Gmail helpers
    def _refresh_gmail_ui(self):
        from integrations.gmail import has_gmail_scope
        if has_gmail_scope():
            self._gmail_scope_lbl.configure(
                text="Gmail scope: authorized",
                text_color="#3a9a4a",
            )
        else:
            self._gmail_scope_lbl.configure(
                text="Gmail scope: not yet authorized — click Re-authorize",
                text_color="#b87c1a",
            )

    def _reauthorize(self):
        creds_path = cfg.get("google_credentials_path")
        if not creds_path:
            self._reauth_status.configure(
                text="Set credentials.json in Google Sheets tab first.",
                text_color="#c05020",
            )
            return

        from integrations.google_sheets import TOKEN_PATH, disconnect
        disconnect()  # deletes token, clears connected flag

        self._reauth_status.configure(
            text="Opening browser…", text_color=("gray50", "gray60")
        )

        def _worker():
            try:
                email = connect(creds_path)
                self.after(0, lambda: self._on_reauth_done(email))
            except Exception as e:
                self.after(0, lambda err=str(e): self._on_reauth_error(err))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_reauth_done(self, email: str):
        self._reauth_status.configure(
            text=f"Re-authorized as {email}", text_color="#3a9a4a"
        )
        self._refresh_gmail_ui()
        self._refresh_ui()

    def _on_reauth_error(self, err: str):
        self._reauth_status.configure(
            text=f"Error: {err[:80]}", text_color="#c05020"
        )

    def _save_alert_email(self):
        email = self._alert_email_entry.get().strip()
        cfg.set_value("gmail_alert_email", email)

    def _save_threshold(self):
        try:
            val = int(self._thresh_entry.get().strip())
            cfg.set_value("gmail_low_stock_threshold", val)
        except ValueError:
            pass

    def _send_test(self):
        from integrations.gmail import has_gmail_scope, send_test_email

        creds = cfg.get("google_credentials_path")
        to    = self._alert_email_entry.get().strip()

        if not creds or not is_connected():
            self._test_status.configure(
                text="Connect Google account first.", text_color="#c05020"
            )
            return
        if not to:
            self._test_status.configure(
                text="Enter an alert email address first.", text_color="#c05020"
            )
            return
        if not has_gmail_scope():
            self._test_status.configure(
                text="Click Re-authorize first.", text_color="#c05020"
            )
            return

        self._test_status.configure(
            text="Sending…", text_color=("gray50", "gray60")
        )

        def _worker():
            try:
                send_test_email(creds, to)
                self.after(0, lambda: self._test_status.configure(
                    text=f"Sent to {to}", text_color="#3a9a4a"
                ))
            except Exception as e:
                self.after(0, lambda err=str(e): self._test_status.configure(
                    text=f"Error: {err[:160]}", text_color="#c05020"
                ))

        threading.Thread(target=_worker, daemon=True).start()

    # ---------------------------------------------------------------- Facebook helpers
    def _refresh_fb_ui(self):
        from integrations.facebook import is_session_saved
        if is_session_saved():
            self._fb_session_lbl.configure(
                text="Session saved — you are connected to Facebook.",
                text_color="#3a9a4a",
            )
        else:
            self._fb_session_lbl.configure(
                text="No session — click 'Login to Facebook' to connect.",
                text_color="#b87c1a",
            )

    def _fb_login(self):
        self._fb_login_btn.configure(state="disabled", text="Opening browser…")
        self._fb_login_status.configure(
            text="Log in to Facebook in the browser window that opens.",
            text_color=("gray50", "gray60"),
        )

        from integrations.facebook import connect as fb_connect

        def _on_done(msg):
            self.after(0, lambda: self._fb_login_status.configure(
                text=msg, text_color="#3a9a4a"
            ))
            self.after(0, lambda: self._fb_login_btn.configure(
                state="normal", text="Login to Facebook"
            ))
            self.after(0, self._refresh_fb_ui)

        def _on_error(err):
            self.after(0, lambda: self._fb_login_status.configure(
                text=f"Error: {err[:80]}", text_color="#c05020"
            ))
            self.after(0, lambda: self._fb_login_btn.configure(
                state="normal", text="Login to Facebook"
            ))

        fb_connect(_on_done, _on_error)

    def _fb_clear_session(self):
        from integrations.facebook import clear_session
        clear_session()
        self._refresh_fb_ui()
        self._fb_login_status.configure(
            text="Session cleared.", text_color=("gray50", "gray60")
        )

    def _refresh_pw_ui(self):
        from dialogs.playwright_install_dialog import playwright_ready
        if playwright_ready():
            self._pw_status_lbl.configure(
                text="Playwright + Chromium installed.",
                text_color="#3a9a4a",
            )
            self._pw_install_btn.configure(state="disabled", text="Installed")
        else:
            self._pw_status_lbl.configure(
                text="Playwright not installed — required for Facebook login.",
                text_color="#b87c1a",
            )
            self._pw_install_btn.configure(state="normal",
                                           text="Install Playwright + Chromium")

    def _install_playwright(self):
        from dialogs.playwright_install_dialog import PlaywrightInstallDialog
        dlg = PlaywrightInstallDialog(self.winfo_toplevel())
        self.winfo_toplevel().wait_window(dlg)
        self._refresh_pw_ui()
        if dlg.result == "installed":
            from integrations.config import set_value
            set_value("playwright_dont_ask", True)

    def _save_fb_location(self):
        cfg.set_value("fb_default_location", self._fb_loc_entry.get().strip())

    def _save_fb_hashtags(self):
        cfg.set_value("fb_default_hashtags", self._fb_tags_entry.get().strip())

    # ---------------------------------------------------------------- Shopify helpers
    def _refresh_shopify_ui(self):
        from integrations.shopify_store import is_configured
        if is_configured():
            self._shopify_conn_lbl.configure(
                text="Credentials saved.", text_color="#3a9a4a"
            )
        else:
            self._shopify_conn_lbl.configure(
                text="Not configured.", text_color=("gray50", "gray60")
            )

    def _save_shopify_url(self):
        cfg.set_value("shopify_shop_url", self._shop_url_entry.get().strip())
        self._refresh_shopify_ui()

    def _save_shopify_token(self):
        cfg.set_value("shopify_access_token", self._shop_token_entry.get().strip())
        self._refresh_shopify_ui()

    def _shopify_test(self):
        shop_url = self._shop_url_entry.get().strip()
        token    = self._shop_token_entry.get().strip()
        if not shop_url or not token:
            self._shopify_conn_lbl.configure(
                text="Enter shop URL and access token first.", text_color="#c05020"
            )
            return

        self._shopify_test_btn.configure(state="disabled", text="Testing…")
        self._shopify_conn_lbl.configure(
            text="Connecting…", text_color=("gray50", "gray60")
        )

        def _worker():
            try:
                from integrations.shopify_store import test_connection
                name = test_connection(shop_url, token)
                self.after(0, lambda: self._on_shopify_connected(name))
            except Exception as e:
                self.after(0, lambda err=str(e): self._on_shopify_error(err))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_shopify_connected(self, shop_name: str):
        self._shopify_conn_lbl.configure(
            text=f"Connected: {shop_name}", text_color="#3a9a4a"
        )
        self._shopify_test_btn.configure(state="normal", text="Test Connection")

    def _on_shopify_error(self, err: str):
        self._shopify_conn_lbl.configure(
            text=f"Error: {err[:90]}", text_color="#c05020"
        )
        self._shopify_test_btn.configure(state="normal", text="Test Connection")

    def _shopify_sync_all(self):
        shop_url = cfg.get("shopify_shop_url") or self._shop_url_entry.get().strip()
        token    = cfg.get("shopify_access_token") or self._shop_token_entry.get().strip()

        if not shop_url or not token:
            self._shopify_sync_status.configure(
                text="Save your shop URL and access token first.", text_color="#c05020"
            )
            return

        self._shopify_sync_btn.configure(state="disabled")
        self._shopify_progress.pack(side="left")
        self._shopify_progress.start()
        self._shopify_sync_status.configure(
            text="Syncing…", text_color=("gray50", "gray60")
        )

        from integrations.shopify_store import sync_all_available
        sync_all_available(
            shop_url, token,
            on_progress = lambda msg: self.after(
                0, lambda m=msg: self._shopify_sync_status.configure(
                    text=m, text_color=("gray50", "gray60")
                )
            ),
            on_done  = lambda r: self.after(0, lambda res=r: self._on_shopify_sync_done(res)),
            on_error = lambda e: self.after(0, lambda err=e: self._on_shopify_sync_error(err)),
        )

    def _on_shopify_sync_done(self, results: dict):
        self._shopify_progress.stop()
        self._shopify_progress.pack_forget()
        self._shopify_sync_btn.configure(state="normal")
        synced = results.get("synced", 0)
        errors = results.get("errors", 0)
        msg = f"Done — {synced} product{'s' if synced != 1 else ''} synced"
        if errors:
            msg += f", {errors} error{'s' if errors != 1 else ''}"
        self._shopify_sync_status.configure(text=msg, text_color="#3a9a4a")

    def _on_shopify_sync_error(self, err: str):
        self._shopify_progress.stop()
        self._shopify_progress.pack_forget()
        self._shopify_sync_btn.configure(state="normal")
        self._shopify_sync_status.configure(
            text=f"Error: {err[:120]}", text_color="#c05020"
        )

    def refresh(self):
        self._refresh_ui()
        self._refresh_gmail_ui()
        self._refresh_fb_ui()
        self._refresh_pw_ui()
        self._refresh_shopify_ui()
