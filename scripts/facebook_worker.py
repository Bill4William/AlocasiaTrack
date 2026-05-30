"""
AlocasiaTrack — Facebook Marketplace playwright worker.

Runs as a SUBPROCESS outside the PyInstaller bundle so that playwright
(which cannot be bundled) can still be used from the installed exe.

Called by integrations/facebook.py when sys._MEIPASS is set.

Usage:
    python facebook_worker.py connect <session_path>
    python facebook_worker.py create_listing <session_path> <listing_json_path>

On success : exits 0, prints a single result line to stdout.
On failure : exits 1, prints error message to stderr.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


# ── helpers ──────────────────────────────────────────────────────────────────

def _load_cookies(ctx, session_path: Path):
    if session_path.exists():
        try:
            ctx.add_cookies(json.loads(session_path.read_text()))
        except Exception:
            pass


def _save_cookies(ctx, session_path: Path):
    session_path.parent.mkdir(parents=True, exist_ok=True)
    session_path.write_text(json.dumps(ctx.cookies()))


def _is_logged_in(page) -> bool:
    try:
        page.wait_for_selector('[aria-label="Facebook"]', timeout=3000)
        return "login" not in page.url and "checkpoint" not in page.url
    except Exception:
        return False


def _wait_for_login(page, timeout_ms: int = 180_000):
    page.wait_for_function(
        "() => !window.location.href.includes('/login') "
        "&& !window.location.href.includes('/checkpoint') "
        "&& document.title !== ''",
        timeout=timeout_ms,
    )


def _fill_field(page, labels: list, value: str):
    for label in labels:
        try:
            f = page.get_by_label(label, exact=False).first
            if f.is_visible():
                f.click()
                f.fill(value)
                return
        except Exception:
            continue
    for label in labels:
        try:
            f = page.get_by_placeholder(label, exact=False).first
            if f.is_visible():
                f.click()
                f.fill(value)
                return
        except Exception:
            continue


# ── commands ─────────────────────────────────────────────────────────────────

def cmd_connect(session_path: Path):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=200)
        ctx = browser.new_context()
        _load_cookies(ctx, session_path)
        page = ctx.new_page()

        page.goto("https://www.facebook.com/", wait_until="domcontentloaded")
        if not _is_logged_in(page):
            _wait_for_login(page)

        _save_cookies(ctx, session_path)
        browser.close()

    print("Session saved — you are now connected to Facebook.")


def cmd_create_listing(session_path: Path, listing_data: dict):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=400)
        ctx = browser.new_context()
        _load_cookies(ctx, session_path)
        page = ctx.new_page()

        page.goto("https://www.facebook.com/marketplace/create/item",
                  wait_until="domcontentloaded")

        if not _is_logged_in(page):
            _wait_for_login(page)
            page.goto("https://www.facebook.com/marketplace/create/item",
                      wait_until="domcontentloaded")

        page.wait_for_load_state("networkidle", timeout=15_000)

        # Photos
        photo_paths = [p for p in listing_data.get("photo_paths", [])
                       if Path(p).exists()]
        if photo_paths:
            try:
                page.locator("input[accept*='image']").first.set_input_files(photo_paths[:10])
                page.wait_for_timeout(2500)
            except Exception:
                pass

        _fill_field(page, ["Title", "What are you selling?"], listing_data["title"])
        _fill_field(page, ["Price"], str(int(listing_data.get("price") or 0)))

        # Category
        try:
            page.get_by_label("Category").click()
            page.wait_for_timeout(800)
            for cat in ["Garden & Outdoor", "Plants & Seedlings", "Garden"]:
                opt = page.get_by_text(cat, exact=False).first
                if opt.is_visible():
                    opt.click()
                    break
            page.wait_for_timeout(600)
        except Exception:
            pass

        # Condition
        try:
            page.get_by_label("Condition").click()
            page.wait_for_timeout(600)
            page.get_by_text(listing_data.get("condition", "Used - Good"),
                             exact=True).first.click()
            page.wait_for_timeout(400)
        except Exception:
            pass

        _fill_field(page, ["Description"], listing_data.get("description", ""))

        page.wait_for_timeout(500)
        try:
            page.get_by_role("button", name="Next").click()
            page.wait_for_timeout(2000)
        except Exception:
            pass
        try:
            page.get_by_role("button", name="Publish").click()
            page.wait_for_timeout(4000)
        except Exception:
            pass

        listing_url = page.url
        _save_cookies(ctx, session_path)
        browser.close()

    print(listing_url)


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            f"Usage: {sys.argv[0]} connect|create_listing <session_path> [listing_json_path]",
            file=sys.stderr,
        )
        sys.exit(1)

    command      = sys.argv[1]
    session_path = Path(sys.argv[2])

    try:
        if command == "connect":
            cmd_connect(session_path)

        elif command == "create_listing":
            if len(sys.argv) < 4:
                raise ValueError("create_listing requires a listing JSON path argument")
            listing_data = json.loads(Path(sys.argv[3]).read_text())
            cmd_create_listing(session_path, listing_data)

        else:
            raise ValueError(f"Unknown command: {command!r}")

    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
