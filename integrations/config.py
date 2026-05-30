import json
import os
from pathlib import Path

CONFIG_DIR  = Path(os.path.expanduser("~")) / "AppData" / "Local" / "AlocasiaTrack"
CONFIG_PATH = CONFIG_DIR / "config.json"

DEFAULT_POT_SIZES = ["No pot", '2"', '4"', '6"', '8"', '10"', '12"+']

_DEFAULTS = {
    "google_credentials_path":   "",
    "google_spreadsheet_id":     "",
    "google_connected":          False,
    "drive_root_folder_id":      "",
    "last_sync":                 None,
    # Gmail alerts
    "gmail_alert_email":         "",
    "gmail_sale_alerts":         True,
    "gmail_low_stock_alerts":    True,
    "gmail_low_stock_threshold": 2,
    # Facebook Marketplace
    "fb_default_location":       "",
    "fb_default_hashtags":       "#alocasia #houseplants #tropicalplants #plantsforsale #rareplants",
    # Shopify
    "shopify_shop_url":          "",
    "shopify_access_token":      "",
    # Playwright / Facebook
    "playwright_dont_ask":       False,
    # General
    "pot_sizes":                 None,   # None = use DEFAULT_POT_SIZES
}


def load() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                data = json.load(f)
            return {**_DEFAULTS, **data}
        except (json.JSONDecodeError, OSError):
            pass
    return dict(_DEFAULTS)


def save(cfg: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def get(key: str):
    return load().get(key)


def set_value(key: str, value):
    cfg = load()
    cfg[key] = value
    save(cfg)


def get_pot_sizes() -> list[str]:
    """Return the user-configured pot sizes, falling back to defaults."""
    sizes = get("pot_sizes")
    if sizes and isinstance(sizes, list):
        return sizes
    return list(DEFAULT_POT_SIZES)
