"""
Shopify integration — Admin REST API.

No OAuth required.  Uses a Private/Custom App access token stored in config.
The browser is never opened.  All calls are direct HTTPS requests.

Public API:
  is_configured() -> bool
  test_connection(shop_url, access_token) -> shop name str  (raises on failure)
  sync_item(shop_url, access_token, stock_row) -> product storefront URL
  unpublish_item(shop_url, access_token, stock_id)
  sync_all_available(shop_url, access_token, on_progress, on_done, on_error)

Product IDs are persisted locally so the same stock item is updated rather
than duplicated on subsequent syncs.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from typing import Callable

from integrations.config import CONFIG_DIR

API_VERSION       = "2024-01"
PRODUCTS_MAP_PATH = CONFIG_DIR / "shopify_products.json"


# ─────────────────────────────────────── local stock_id → product_id cache

def _load_map() -> dict:
    try:
        if PRODUCTS_MAP_PATH.exists():
            return json.loads(PRODUCTS_MAP_PATH.read_text())
    except Exception:
        pass
    return {}


def _save_map(m: dict):
    PRODUCTS_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    PRODUCTS_MAP_PATH.write_text(json.dumps(m, indent=2))


def get_product_id(stock_id: int) -> int | None:
    """Return the Shopify product ID for a stock item, or None if not synced."""
    return _load_map().get(str(stock_id))


# ─────────────────────────────────────────────────────────────── API helper

def _normalise_url(shop_url: str) -> str:
    url = shop_url.strip().rstrip("/")
    if not url.startswith("http"):
        url = "https://" + url
    return url


def _api(method: str, shop_url: str, token: str, path: str,
         body: dict | None = None) -> dict:
    url  = f"{_normalise_url(shop_url)}/admin/api/{API_VERSION}/{path}"
    data = json.dumps(body).encode() if body else None
    req  = urllib.request.Request(
        url, data=data, method=method,
        headers={
            "X-Shopify-Access-Token": token,
            "Content-Type":           "application/json",
            "Accept":                 "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()[:300]
        raise RuntimeError(f"Shopify {exc.code}: {detail}")


# ─────────────────────────────────────────── HTML description builder

def _build_body_html(stock_row: dict) -> str:
    species = stock_row.get("species_name") or "Alocasia"
    kind    = stock_row.get("item_type",   "Plant")
    stage   = stock_row.get("growth_stage") or ""
    cond    = stock_row.get("condition")    or "Good"
    pot     = stock_row.get("pot_size")     or ""
    notes   = stock_row.get("notes")        or ""

    lines = [f"<p><strong>Alocasia {species} &mdash; {kind}</strong></p>", "<ul>"]
    if stage:
        lines.append(f"<li>Stage: {stage}</li>")
    lines.append(f"<li>Condition: {cond}</li>")
    if pot and pot != "No pot":
        lines.append(f"<li>Pot size: {pot}</li>")
    lines.append("</ul>")
    if notes:
        lines.append(f"<p>{notes}</p>")
    lines.append(
        "<p>Local pickup preferred. Shipping available &mdash; "
        "please message to arrange.</p>"
    )
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────── public API

def is_configured() -> bool:
    from integrations.config import get as cfg_get
    return bool(cfg_get("shopify_shop_url") and cfg_get("shopify_access_token"))


def test_connection(shop_url: str, access_token: str) -> str:
    """Verify credentials. Returns the shop name on success, raises on failure."""
    resp = _api("GET", shop_url, access_token, "shop.json")
    return resp["shop"]["name"]


def sync_item(shop_url: str, access_token: str, stock_row: dict) -> str:
    """
    Create or update a Shopify product for the given stock item.
    Returns the storefront product URL.
    """
    product_map = _load_map()
    stock_id    = str(stock_row["id"])
    existing_id = product_map.get(stock_id)

    species = stock_row.get("species_name") or "Alocasia"
    kind    = stock_row.get("item_type",   "Plant")
    price   = float(stock_row.get("asking_price") or 0)
    sku     = stock_row.get("sku") or ""
    tags    = (
        f"alocasia, {species.lower()}, {kind.lower()}, "
        f"houseplant, tropical plant, sku:{sku}"
    )

    payload: dict = {
        "product": {
            "title":        f"Alocasia {species} {kind}",
            "body_html":    _build_body_html(stock_row),
            "product_type": f"Alocasia {kind}",
            "tags":         tags,
            "published":    True,
            "variants": [{
                "price":                str(round(price, 2)),
                "inventory_management": None,
                "sku":                  sku,
            }],
        }
    }

    if existing_id:
        resp    = _api("PUT", shop_url, access_token,
                       f"products/{existing_id}.json", payload)
        product = resp["product"]
    else:
        resp    = _api("POST", shop_url, access_token, "products.json", payload)
        product = resp["product"]
        product_map[stock_id] = product["id"]
        _save_map(product_map)

    return f"{_normalise_url(shop_url)}/products/{product['handle']}"


def unpublish_item(shop_url: str, access_token: str, stock_id: int):
    """Unpublish a product from the storefront (called when the item is sold)."""
    product_id = _load_map().get(str(stock_id))
    if not product_id:
        return
    _api("PUT", shop_url, access_token, f"products/{product_id}.json",
         {"product": {"id": product_id, "published": False}})


def sync_all_available(shop_url: str, access_token: str,
                       on_progress: Callable[[str], None],
                       on_done:     Callable[[dict], None],
                       on_error:    Callable[[str], None]):
    """Sync every Available stock item to Shopify. Runs in a daemon thread."""

    def _worker():
        try:
            from database.models import StockModel
            rows    = StockModel.get_all(status="Available")
            results = {"synced": 0, "errors": 0}
            for row in rows:
                try:
                    on_progress(f"Syncing {row['sku']}…")
                    sync_item(shop_url, access_token, row)
                    results["synced"] += 1
                except Exception:
                    results["errors"] += 1
            on_done(results)
        except Exception as exc:
            on_error(str(exc))

    threading.Thread(target=_worker, daemon=True).start()
