"""
Gmail integration — transactional alerts sent via the Gmail API.

Uses the same OAuth token as Sheets/Drive (gmail.send scope must be present).
Call has_gmail_scope() before sending to check whether re-auth is needed.
"""

from __future__ import annotations

import base64
import json
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from integrations.config import get as cfg_get
from integrations.google_sheets import TOKEN_PATH, get_credentials

GMAIL_SCOPE = "https://www.googleapis.com/auth/gmail.send"


# ------------------------------------------------------------------ scope check

def has_gmail_scope() -> bool:
    """Return True if the saved token includes the gmail.send scope."""
    if not TOKEN_PATH.exists():
        return False
    try:
        data = json.loads(TOKEN_PATH.read_text())
        scopes = data.get("scopes", [])
        if isinstance(scopes, str):
            scopes = scopes.split()
        return GMAIL_SCOPE in scopes
    except Exception:
        return False


# ------------------------------------------------------------------ low-level send

def _service(credentials_path: str):
    from googleapiclient.discovery import build
    creds = get_credentials(credentials_path)
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def _send(credentials_path: str, to: str, subject: str, html: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["To"]      = to
    msg["From"]    = "me"
    msg.attach(MIMEText(html, "html"))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    _service(credentials_path).users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()


# ------------------------------------------------------------------ alert senders

def send_test_email(credentials_path: str, to: str):
    _send(
        credentials_path, to,
        subject="AlocasiaTrack — Test Email",
        html=_template(
            title="Test Email",
            body="<p style='color:#ccc;'>Your Gmail alerts are configured correctly. "
                 "You will receive sale confirmations and low-stock notices at this address.</p>",
        ),
    )


def send_sale_alert(credentials_path: str, to: str,
                    sale: dict, stock: dict):
    profit       = sale.get("profit") or 0
    profit_color = "#3a9a4a" if profit >= 0 else "#c05020"
    sign         = "+" if profit >= 0 else ""

    rows = [
        ("SKU",          stock.get("sku", "—")),
        ("Type",         stock.get("item_type", "—")),
        ("Species",      stock.get("species_name", "—")),
        ("Sale Price",   f"${sale.get('sale_price', 0):.2f}"),
        ("Cost Basis",   f"${stock.get('cost_basis', 0):.2f}"),
        ("Platform",     sale.get("platform", "—")),
        ("Buyer",        sale.get("buyer_name") or "—"),
        ("Shipping",     f"{sale.get('shipping_method','—')}  "
                         f"(${sale.get('shipping_cost', 0):.2f})"),
        ("Date",         (sale.get("sale_date") or datetime.now().strftime("%Y-%m-%d"))[:10]),
    ]

    table = "".join(
        f"<tr>"
        f"<td style='padding:7px 14px;color:#999;border-bottom:1px solid #3a3a3a;'>{k}</td>"
        f"<td style='padding:7px 14px;color:white;border-bottom:1px solid #3a3a3a;'>{v}</td>"
        f"</tr>"
        for k, v in rows
    )

    body = f"""
    <p style='color:#aaa;margin-bottom:16px;'>A sale has been recorded in AlocasiaTrack.</p>
    <table style='border-collapse:collapse;width:100%;background:#222;border-radius:8px;
                  overflow:hidden;margin-bottom:20px;'>
      {table}
    </table>
    <div style='text-align:center;padding:16px;background:#1e2e1e;border-radius:8px;'>
      <div style='color:#aaa;font-size:13px;margin-bottom:4px;'>Profit</div>
      <div style='font-size:32px;font-weight:bold;color:{profit_color};'>
        {sign}${profit:.2f}
      </div>
    </div>
    """

    _send(
        credentials_path, to,
        subject=f"Sale: {stock.get('sku','?')}  {stock.get('species_name','')}  "
                f"${sale.get('sale_price',0):.2f}",
        html=_template(title="Sale Recorded", body=body),
    )


def send_low_stock_alert(credentials_path: str, to: str,
                          species_name: str, count: int, threshold: int):
    bar_pct  = max(0, min(100, int(count / max(threshold, 1) * 100)))
    bar_color = "#3a9a4a" if count > threshold else ("#b87c1a" if count > 0 else "#8a3a3a")

    body = f"""
    <p style='color:#aaa;margin-bottom:16px;'>Available stock is at or below your alert threshold.</p>
    <div style='background:#222;border-radius:8px;padding:20px;text-align:center;
                margin-bottom:20px;'>
      <div style='font-size:14px;color:#aaa;margin-bottom:8px;'>Species</div>
      <div style='font-size:22px;font-weight:bold;color:white;
                  margin-bottom:16px;'>{species_name}</div>
      <div style='font-size:48px;font-weight:bold;color:{bar_color};
                  line-height:1;'>{count}</div>
      <div style='color:#aaa;font-size:13px;margin-top:4px;'>
        item{'s' if count != 1 else ''} available
      </div>
      <div style='background:#333;border-radius:4px;height:8px;
                  margin:16px 0 6px;overflow:hidden;'>
        <div style='background:{bar_color};height:100%;width:{bar_pct}%;'></div>
      </div>
      <div style='color:#666;font-size:11px;'>Alert threshold: {threshold}</div>
    </div>
    <p style='color:#aaa;font-size:13px;'>
      Consider taking cuttings or separating pups from your {species_name} mother plants
      to restock soon.
    </p>
    """

    _send(
        credentials_path, to,
        subject=f"Low Stock: {species_name} — {count} available",
        html=_template(title="Low Stock Alert", body=body),
    )


# ------------------------------------------------------------------ HTML shell

def _template(title: str, body: str) -> str:
    stamp = datetime.now().strftime("%B %d, %Y  %H:%M")
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
</head>
<body style="margin:0;padding:0;background:#141414;
             font-family:'Segoe UI',Arial,sans-serif;">
  <div style="max-width:540px;margin:32px auto 48px;">
    <div style="background:linear-gradient(135deg,#1a4a28,#2a6a3a);
                padding:22px 28px;border-radius:10px 10px 0 0;">
      <div style="font-size:11px;color:#a0dfa8;letter-spacing:2px;
                  text-transform:uppercase;margin-bottom:4px;">AlocasiaTrack</div>
      <div style="font-size:22px;font-weight:bold;color:white;">{title}</div>
    </div>
    <div style="background:#2b2b2b;padding:28px;border-radius:0 0 10px 10px;">
      {body}
      <hr style="border:none;border-top:1px solid #3a3a3a;margin:24px 0 16px;">
      <div style="color:#555;font-size:11px;">{stamp}</div>
    </div>
  </div>
</body>
</html>"""
