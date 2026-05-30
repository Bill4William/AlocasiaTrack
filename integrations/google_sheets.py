"""
Google Sheets integration — OAuth2 auth and bi-directional data push.

Auth flow:
  1. User supplies credentials.json (downloaded from Google Cloud Console).
  2. First connect: InstalledAppFlow opens a browser tab for consent.
  3. Token saved to AppData/Local/AlocasiaTrack/google_token.json.
  4. Subsequent syncs use the saved (auto-refreshed) token.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from integrations.config import CONFIG_DIR, get as cfg_get, set_value as cfg_set

TOKEN_PATH = CONFIG_DIR / "google_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]

# Lazy imports so missing packages give a clean error message instead of
# crashing at app start.
def _imports():
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import gspread
        return Credentials, InstalledAppFlow, Request, gspread
    except ImportError as e:
        raise RuntimeError(
            f"Google integration packages not installed.\n"
            f"Run:  pip install gspread google-auth google-auth-oauthlib\n"
            f"({e})"
        )


# ------------------------------------------------------------------ auth

def is_connected() -> bool:
    return TOKEN_PATH.exists()


def get_credentials(credentials_path: str):
    Credentials, InstalledAppFlow, Request, _ = _imports()
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN_PATH.write_text(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            TOKEN_PATH.write_text(creds.to_json())
    return creds


def connect(credentials_path: str) -> str:
    """Run OAuth consent flow. Returns the authenticated email address."""
    Credentials, InstalledAppFlow, Request, gspread = _imports()
    creds = get_credentials(credentials_path)
    # Fetch the user's email via People API lite endpoint
    import urllib.request, urllib.error
    try:
        req = urllib.request.Request(
            "https://www.googleapis.com/oauth2/v1/userinfo?alt=json",
            headers={"Authorization": f"Bearer {creds.token}"},
        )
        with urllib.request.urlopen(req) as resp:
            info = json.loads(resp.read())
        email = info.get("email", "Connected")
    except Exception:
        email = "Connected"
    cfg_set("google_connected", True)
    return email


def disconnect():
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
    cfg_set("google_connected", False)


def get_client(credentials_path: str):
    _, _, _, gspread = _imports()
    creds = get_credentials(credentials_path)
    return gspread.Client(auth=creds)


# ------------------------------------------------------------------ spreadsheet helpers

def create_spreadsheet(credentials_path: str,
                        title: str = "AlocasiaTrack Inventory") -> str:
    client = get_client(credentials_path)
    sh = client.create(title)
    sh.sheet1.update_title("Inventory")
    sh.add_worksheet(title="Sales",         rows=2000, cols=20)
    sh.add_worksheet(title="Species",       rows=500,  cols=10)
    sh.add_worksheet(title="Mother Plants", rows=500,  cols=10)
    cfg_set("google_spreadsheet_id", sh.id)
    return sh.id


def spreadsheet_url(spreadsheet_id: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"


# ------------------------------------------------------------------ sync

def sync_all(credentials_path: str, spreadsheet_id: str) -> dict[str, int]:
    from database.models import SpeciesModel, PlantsModel, StockModel, SalesModel

    client = get_client(credentials_path)
    sh     = client.open_by_key(spreadsheet_id)

    results = {
        "inventory": _sync_inventory(sh),
        "sales":     _sync_sales(sh),
        "species":   _sync_species(sh),
        "plants":    _sync_plants(sh),
    }
    cfg_set("last_sync", datetime.now().strftime("%Y-%m-%d %H:%M"))
    return results


# ---- per-sheet writers ----

def _ws(sh, title: str):
    """Get worksheet by title, create if missing."""
    try:
        return sh.worksheet(title)
    except Exception:
        return sh.add_worksheet(title=title, rows=1000, cols=20)


_GREEN_HDR = {
    "backgroundColor":  {"red": 0.133, "green": 0.420, "blue": 0.180},
    "textFormat": {
        "bold": True,
        "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
    },
}


def _write(ws, data: list[list]) -> int:
    ws.clear()
    if data:
        ws.update(data, "A1", value_input_option="USER_ENTERED")
        ws.format(f"A1:{_col_letter(len(data[0]))}1", _GREEN_HDR)
    return max(0, len(data) - 1)


def _col_letter(n: int) -> str:
    result = ""
    while n:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result


def _sync_inventory(sh) -> int:
    import json as _json
    from database.models import StockModel
    rows = StockModel.get_all()
    headers = ["SKU", "Type", "Species", "Growth Stage", "Condition",
               "Pot Size", "Asking Price ($)", "Cost Basis ($)", "Status",
               "Parent Plant", "Date Added", "Photo Links", "Notes"]

    def _photo_links(photo_paths_json: str) -> str:
        try:
            photos = _json.loads(photo_paths_json or "[]")
            return "  |  ".join(
                p["drive_url"] for p in photos
                if isinstance(p, dict) and p.get("drive_url")
            )
        except Exception:
            return ""

    data = [headers] + [
        [
            r["sku"] or "",
            r["item_type"] or "",
            r["species_name"] or "",
            r["growth_stage"] or "",
            r["condition"] or "",
            r["pot_size"] or "",
            r["asking_price"] if r["asking_price"] is not None else "",
            r["cost_basis"] if r["cost_basis"] is not None else "",
            r["status"] or "",
            r["parent_nickname"] or "",
            (r["date_added"] or "")[:10],
            _photo_links(r["photo_paths"]),
            r["notes"] or "",
        ]
        for r in rows
    ]
    return _write(_ws(sh, "Inventory"), data)


def _sync_sales(sh) -> int:
    from database.models import SalesModel
    rows = SalesModel.get_all()
    headers = ["Date", "SKU", "Type", "Species", "Sale Price ($)", "Profit ($)",
               "Platform", "Buyer", "Contact", "Shipping Method",
               "Shipping Cost ($)", "Notes"]
    data = [headers] + [
        [
            (r["sale_date"] or "")[:10],
            r["sku"] or "",
            r["item_type"] or "",
            r["species_name"] or "",
            r["sale_price"] if r["sale_price"] is not None else "",
            r["profit"] if r["profit"] is not None else "",
            r["platform"] or "",
            r["buyer_name"] or "",
            r["buyer_contact"] or "",
            r["shipping_method"] or "",
            r["shipping_cost"] if r["shipping_cost"] is not None else "",
            r["notes"] or "",
        ]
        for r in rows
    ]
    return _write(_ws(sh, "Sales"), data)


def _sync_species(sh) -> int:
    from database.models import SpeciesModel
    rows   = SpeciesModel.get_all()
    counts = SpeciesModel.get_stock_counts()
    headers = ["Name", "Care Level", "Price Min ($)", "Price Max ($)",
               "Active Stock", "Notes"]
    data = [headers] + [
        [
            r["name"] or "",
            r["care_level"] or "",
            r["price_min"] if r["price_min"] is not None else "",
            r["price_max"] if r["price_max"] is not None else "",
            counts.get(r["id"], 0),
            r["notes"] or "",
        ]
        for r in rows
    ]
    return _write(_ws(sh, "Species"), data)


def _sync_plants(sh) -> int:
    from database.models import PlantsModel
    rows = PlantsModel.get_all()
    headers = ["Nickname", "Species", "Pot Size", "Health Status",
               "Location", "Date Acquired", "Notes"]
    data = [headers] + [
        [
            r["nickname"] or "",
            r["species_name"] or "",
            r["pot_size"] or "",
            r["health_status"] or "",
            r["location"] or "",
            r["acquired_date"] or "",
            r["notes"] or "",
        ]
        for r in rows
    ]
    return _write(_ws(sh, "Mother Plants"), data)
