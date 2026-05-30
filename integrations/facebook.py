"""
Facebook Marketplace integration — Playwright browser automation.

No credentials are stored. Authentication uses saved session cookies.
The browser runs headed so the user can handle 2FA / CAPTCHA / review.

Public API (all non-blocking — run in daemon threads, fire callbacks):
  connect(on_done, on_error)          → save session via manual browser login
  create_listing(data, on_done, on_error)  → fill & submit a Marketplace listing
  is_session_saved() → bool
  clear_session()
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Callable

from integrations.config import CONFIG_DIR, get as cfg_get

SESSION_PATH = CONFIG_DIR / "fb_session.json"

# FB Marketplace condition labels (what the UI shows in the dropdown)
CONDITIONS = [
    "New",
    "Used - Like New",
    "Used - Good",
    "Used - Fair",
    "Used - Poor",
]

# Map from our stock conditions to FB conditions
CONDITION_MAP = {
    "Excellent":  "Used - Like New",
    "Good":       "Used - Good",
    "Fair":       "Used - Fair",
    "Needs TLC":  "Used - Poor",
}


# ------------------------------------------------------------------ session

def is_session_saved() -> bool:
    return SESSION_PATH.exists()


def clear_session():
    if SESSION_PATH.exists():
        SESSION_PATH.unlink()


def _load_cookies(context):
    if SESSION_PATH.exists():
        try:
            cookies = json.loads(SESSION_PATH.read_text())
            context.add_cookies(cookies)
        except Exception:
            pass


def _save_cookies(context):
    SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    SESSION_PATH.write_text(json.dumps(context.cookies()))


# ------------------------------------------------------------------ helpers

def _imports():
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
        return sync_playwright, PWTimeout
    except ImportError:
        raise RuntimeError(
            "Playwright is not installed.\n"
            "Run:  pip install playwright\n"
            "Then: playwright install chromium"
        )


def _is_logged_in(page) -> bool:
    try:
        page.wait_for_selector('[aria-label="Facebook"]', timeout=3000)
        return "login" not in page.url and "checkpoint" not in page.url
    except Exception:
        return False


def _wait_for_login(page, timeout_ms: int = 180_000):
    """Block until the user completes manual login (up to timeout_ms ms)."""
    page.wait_for_function(
        "() => !window.location.href.includes('/login') "
        "&& !window.location.href.includes('/checkpoint') "
        "&& document.title !== ''",
        timeout=timeout_ms,
    )


# ------------------------------------------------------------------ public API

def connect(on_done: Callable[[str], None],
            on_error: Callable[[str], None]):
    """Open a visible browser for manual FB login, then save the session."""

    def _worker():
        sync_playwright, PWTimeout = _imports()
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=False, slow_mo=200)
                ctx     = browser.new_context()
                _load_cookies(ctx)
                page    = ctx.new_page()

                page.goto("https://www.facebook.com/", wait_until="domcontentloaded")

                if not _is_logged_in(page):
                    # Let user log in manually
                    _wait_for_login(page)

                _save_cookies(ctx)
                browser.close()
                on_done("Session saved — you are now connected to Facebook.")
        except Exception as e:
            on_error(str(e))

    threading.Thread(target=_worker, daemon=True).start()


def create_listing(listing_data: dict,
                   on_done: Callable[[str], None],
                   on_error: Callable[[str], None]):
    """
    Fill a Marketplace listing form and attempt to publish it.

    listing_data keys:
      title, price, description, condition, photo_paths (list of local paths)

    on_done receives the listing URL (or the final page URL if capture fails).
    The browser stays open briefly after publish so cookies can be saved.
    """

    def _worker():
        sync_playwright, PWTimeout = _imports()
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=False, slow_mo=400)
                ctx     = browser.new_context()
                _load_cookies(ctx)
                page    = ctx.new_page()

                page.goto("https://www.facebook.com/marketplace/create/item",
                          wait_until="domcontentloaded")

                # Handle login wall
                if not _is_logged_in(page):
                    _wait_for_login(page)
                    page.goto("https://www.facebook.com/marketplace/create/item",
                              wait_until="domcontentloaded")

                page.wait_for_load_state("networkidle", timeout=15_000)

                # ── Photos ──────────────────────────────────────────────
                photo_paths = [
                    p for p in listing_data.get("photo_paths", [])
                    if Path(p).exists()
                ]
                if photo_paths:
                    try:
                        file_input = page.locator("input[accept*='image']").first
                        file_input.set_input_files(photo_paths[:10])
                        page.wait_for_timeout(2500)
                    except Exception:
                        pass

                # ── Title ───────────────────────────────────────────────
                _fill_field(page, ["Title", "What are you selling?"],
                            listing_data["title"])

                # ── Price ───────────────────────────────────────────────
                _fill_field(page, ["Price"],
                            str(int(listing_data.get("price") or 0)))

                # ── Category ────────────────────────────────────────────
                try:
                    page.get_by_label("Category").click()
                    page.wait_for_timeout(800)
                    # Try Garden & Outdoor first, fallback to general search
                    for cat_text in ["Garden & Outdoor", "Plants & Seedlings", "Garden"]:
                        opt = page.get_by_text(cat_text, exact=False).first
                        if opt.is_visible():
                            opt.click()
                            break
                    page.wait_for_timeout(600)
                except Exception:
                    pass

                # ── Condition ───────────────────────────────────────────
                try:
                    page.get_by_label("Condition").click()
                    page.wait_for_timeout(600)
                    cond_text = listing_data.get("condition", "Used - Good")
                    page.get_by_text(cond_text, exact=True).first.click()
                    page.wait_for_timeout(400)
                except Exception:
                    pass

                # ── Description ─────────────────────────────────────────
                _fill_field(page, ["Description"], listing_data.get("description", ""))

                # ── Next ────────────────────────────────────────────────
                page.wait_for_timeout(500)
                try:
                    page.get_by_role("button", name="Next").click()
                    page.wait_for_timeout(2000)
                except Exception:
                    pass

                # ── Publish (attempt auto-click; user can also click manually) ──
                try:
                    page.get_by_role("button", name="Publish").click()
                    page.wait_for_timeout(4000)
                except Exception:
                    pass

                listing_url = page.url
                _save_cookies(ctx)
                browser.close()
                on_done(listing_url)

        except Exception as e:
            on_error(str(e))

    threading.Thread(target=_worker, daemon=True).start()


# ------------------------------------------------------------------ helpers

def _fill_field(page, label_variants: list[str], value: str):
    """Try multiple label variants to find and fill a form field."""
    for label in label_variants:
        try:
            field = page.get_by_label(label, exact=False).first
            if field.is_visible():
                field.click()
                field.fill(value)
                return
        except Exception:
            continue
    # Fallback: use placeholder
    for label in label_variants:
        try:
            field = page.get_by_placeholder(label, exact=False).first
            if field.is_visible():
                field.click()
                field.fill(value)
                return
        except Exception:
            continue


# ------------------------------------------------------------------ listing helpers

def build_listing_data(stock_row: dict) -> dict:
    """Auto-generate listing fields from a stock row."""
    species = stock_row.get("species_name") or "Alocasia"
    kind    = stock_row.get("item_type", "Plant")
    stage   = stock_row.get("growth_stage") or ""
    cond    = stock_row.get("condition") or "Good"
    pot     = stock_row.get("pot_size") or ""
    notes   = stock_row.get("notes") or ""
    price   = stock_row.get("asking_price") or 0
    hashtags = cfg_get("fb_default_hashtags") or ""
    sp_tag  = "#alocasia" + species.lower().replace(" ", "").replace("-", "")

    lines = [f"Alocasia {species} — {kind}", ""]
    if stage:
        lines.append(f"- Stage: {stage}")
    lines.append(f"- Condition: {cond}")
    if pot and pot != "No pot":
        lines.append(f"- Pot size: {pot}")
    if notes:
        lines += ["", notes]
    lines += [
        "",
        "Local pickup preferred. Shipping available — please message to arrange.",
        "",
        f"{sp_tag} {hashtags}",
    ]

    return {
        "title":       f"Alocasia {species} {kind}",
        "price":       price,
        "description": "\n".join(lines),
        "condition":   CONDITION_MAP.get(cond, "Used - Good"),
        "photo_paths": _extract_local_paths(stock_row.get("photo_paths") or "[]"),
    }


def _extract_local_paths(photo_paths_json: str) -> list[str]:
    import json as _json
    try:
        items = _json.loads(photo_paths_json)
        return [
            item["local"] for item in items
            if isinstance(item, dict) and item.get("local")
            and Path(item["local"]).exists()
        ]
    except Exception:
        return []
