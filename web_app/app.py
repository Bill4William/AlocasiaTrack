"""
AlocasiaTrack — Flask PWA
Reuses all existing database models and integrations from the desktop app.

Run with:
    cd AlocasiaTrack
    python web_app/run.py

Then open http://localhost:5000 in any browser (or on your phone via your LAN IP).
"""
from __future__ import annotations

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# ── Make sure the project root is on sys.path so we can import database/ etc. ─
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import (
    Flask, render_template, request, redirect, url_for,
    jsonify, flash, abort,
)

from database.connection import initialize_db
from database.models import (
    StockModel, SalesModel, SpeciesModel, PlantsModel,
)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "alocasia-pwa-dev"   # change for production

initialize_db()


# ────────────────────────────────────────────────── template helpers
@app.template_filter("money")
def money_filter(val):
    try:
        return f"${float(val):.2f}"
    except (TypeError, ValueError):
        return "—"


@app.template_filter("date_short")
def date_short_filter(val):
    if not val:
        return "—"
    return str(val)[:10]


@app.context_processor
def inject_now():
    return {"now": datetime.now()}


# ════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ════════════════════════════════════════════════════════════════════

@app.route("/")
def dashboard():
    now   = datetime.now()
    stock = StockModel.get_dashboard_stats()
    month = SalesModel.get_monthly_stats(now.year, now.month)
    alltime = SalesModel.get_all_time_stats()
    recent  = SalesModel.get_all()[:8]
    return render_template(
        "dashboard.html",
        stock=stock, month=month, alltime=alltime,
        recent=recent, now=now,
    )


# ════════════════════════════════════════════════════════════════════
#  STOCK
# ════════════════════════════════════════════════════════════════════

@app.route("/stock")
def stock_list():
    item_type  = request.args.get("type")
    status     = request.args.get("status")
    species_id = request.args.get("species_id", type=int)
    q          = request.args.get("q", "").strip().lower()

    items = StockModel.get_all(item_type=item_type, status=status,
                               species_id=species_id)

    if q:
        items = [
            i for i in items
            if q in (i["sku"] or "").lower()
            or q in (i["species_name"] or "").lower()
            or q in (i["species_common_name"] or "").lower()
            or q in (i["notes"] or "").lower()
            or q in (i["growth_stage"] or "").lower()
            or q in (i["condition"] or "").lower()
        ]

    species = SpeciesModel.get_all()
    return render_template(
        "stock.html",
        items=items, species=species,
        filter_type=item_type, filter_status=status,
        filter_species=species_id, query=q,
    )


@app.route("/stock/add", methods=["GET", "POST"])
def stock_add():
    species = SpeciesModel.get_all()
    plants  = PlantsModel.get_all()

    if request.method == "POST":
        f = request.form
        qty = max(1, int(f.get("quantity") or 1))
        for _ in range(qty):
            StockModel.create(
                item_type      = f["item_type"],
                species_id     = f.get("species_id") or None,
                parent_plant_id= f.get("parent_plant_id") or None,
                growth_stage   = f.get("growth_stage", ""),
                condition      = f.get("condition", "Good"),
                pot_size       = f.get("pot_size", ""),
                asking_price   = float(f.get("asking_price") or 0),
                cost_basis     = float(f.get("cost_basis") or 0),
                notes          = f.get("notes", ""),
            )
        flash(f"Added {qty} stock item{'s' if qty > 1 else ''}.", "success")
        return redirect(url_for("stock_list"))

    return render_template(
        "stock_form.html",
        item=None, species=species, plants=plants,
        title="Add Stock Item",
        StockModel=StockModel,
    )


@app.route("/stock/<int:id>")
def stock_detail(id):
    item = StockModel.get_by_id(id)
    if not item:
        abort(404)
    return render_template("stock_detail.html", item=item,
                           StockModel=StockModel)


@app.route("/stock/<int:id>/edit", methods=["GET", "POST"])
def stock_edit(id):
    item    = StockModel.get_by_id(id)
    if not item:
        abort(404)
    species = SpeciesModel.get_all()
    plants  = PlantsModel.get_all()

    if request.method == "POST":
        f = request.form
        StockModel.update(
            id             = id,
            item_type      = f["item_type"],
            species_id     = f.get("species_id") or None,
            parent_plant_id= f.get("parent_plant_id") or None,
            growth_stage   = f.get("growth_stage", ""),
            condition      = f.get("condition", "Good"),
            pot_size       = f.get("pot_size", ""),
            asking_price   = float(f.get("asking_price") or 0),
            cost_basis     = float(f.get("cost_basis") or 0),
            status         = f.get("status", "Available"),
            notes          = f.get("notes", ""),
        )
        flash("Item updated.", "success")
        return redirect(url_for("stock_detail", id=id))

    return render_template(
        "stock_form.html",
        item=item, species=species, plants=plants,
        title="Edit Stock Item",
        StockModel=StockModel,
    )


@app.route("/stock/<int:id>/delete", methods=["POST"])
def stock_delete(id):
    StockModel.delete(id)
    flash("Item deleted.", "info")
    return redirect(url_for("stock_list"))


@app.route("/stock/<int:id>/status", methods=["POST"])
def stock_status(id):
    """Quick status update — used from detail page buttons."""
    status = request.form.get("status")
    if status in StockModel.STATUSES:
        StockModel.update_status(id, status)
    return redirect(url_for("stock_detail", id=id))


@app.route("/stock/<int:id>/record-sale", methods=["POST"])
def record_sale(id):
    item = StockModel.get_by_id(id)
    if not item:
        abort(404)
    f = request.form
    SalesModel.create(
        stock_id       = id,
        listing_id     = None,
        sale_price     = float(f.get("sale_price") or 0),
        platform       = f.get("platform", ""),
        sale_date      = f.get("sale_date") or datetime.now().strftime("%Y-%m-%d"),
        buyer_name     = f.get("buyer_name", ""),
        buyer_contact  = f.get("buyer_contact", ""),
        shipping_method= f.get("shipping_method", "Local Pickup"),
        shipping_cost  = float(f.get("shipping_cost") or 0),
        cost_basis     = float(item["cost_basis"] or 0),
        notes          = f.get("notes", ""),
    )
    flash(f"Sale recorded for {item['sku']}.", "success")
    return redirect(url_for("stock_list"))


# ════════════════════════════════════════════════════════════════════
#  SALES
# ════════════════════════════════════════════════════════════════════

@app.route("/sales")
def sales_list():
    now     = datetime.now()
    sales   = SalesModel.get_all()
    month   = SalesModel.get_monthly_stats(now.year, now.month)
    alltime = SalesModel.get_all_time_stats()
    return render_template("sales.html", sales=sales,
                           month=month, alltime=alltime, now=now)


# ════════════════════════════════════════════════════════════════════
#  SPECIES
# ════════════════════════════════════════════════════════════════════

@app.route("/species")
def species_list():
    items  = SpeciesModel.get_all()
    counts = SpeciesModel.get_stock_counts()
    return render_template("species.html", items=items, counts=counts)


@app.route("/species/add", methods=["GET", "POST"])
def species_add():
    if request.method == "POST":
        f = request.form
        SpeciesModel.create(
            name      = f["name"],
            common_name = f.get("common_name", ""),
            notes     = f.get("notes", ""),
            care_level= f.get("care_level", "Moderate"),
            price_min = float(f.get("price_min") or 0) or None,
            price_max = float(f.get("price_max") or 0) or None,
        )
        flash(f"Species '{f['name']}' added.", "success")
        return redirect(url_for("species_list"))
    return render_template("species_form.html", item=None, title="Add Species")


@app.route("/species/<int:id>/edit", methods=["GET", "POST"])
def species_edit(id):
    item = SpeciesModel.get_by_id(id)
    if not item:
        abort(404)
    if request.method == "POST":
        f = request.form
        SpeciesModel.update(
            id        = id,
            name      = f["name"],
            common_name = f.get("common_name", ""),
            notes     = f.get("notes", ""),
            care_level= f.get("care_level", "Moderate"),
            price_min = float(f.get("price_min") or 0) or None,
            price_max = float(f.get("price_max") or 0) or None,
        )
        flash("Species updated.", "success")
        return redirect(url_for("species_list"))
    return render_template("species_form.html", item=item, title="Edit Species")


@app.route("/species/<int:id>/delete", methods=["POST"])
def species_delete(id):
    SpeciesModel.delete(id)
    flash("Species deleted.", "info")
    return redirect(url_for("species_list"))


# ════════════════════════════════════════════════════════════════════
#  MOTHER PLANTS
# ════════════════════════════════════════════════════════════════════

@app.route("/plants")
def plants_list():
    items = PlantsModel.get_all()
    return render_template("plants.html", items=items)


@app.route("/plants/add", methods=["GET", "POST"])
def plants_add():
    species = SpeciesModel.get_all()
    if request.method == "POST":
        f = request.form
        PlantsModel.create(
            species_id    = f.get("species_id") or None,
            nickname      = f.get("nickname", ""),
            acquired_date = f.get("acquired_date", ""),
            pot_size      = f.get("pot_size", ""),
            health_status = f.get("health_status", "Healthy"),
            location      = f.get("location", ""),
            notes         = f.get("notes", ""),
        )
        flash("Mother plant added.", "success")
        return redirect(url_for("plants_list"))
    return render_template("plants_form.html", item=None, species=species,
                           title="Add Mother Plant")


# ════════════════════════════════════════════════════════════════════
#  PHOTOS
# ════════════════════════════════════════════════════════════════════

@app.route("/photos/<int:stock_id>/<int:index>")
def serve_photo(stock_id, index):
    """Serve a local photo file for a stock item."""
    from flask import send_file
    item = StockModel.get_by_id(stock_id)
    if not item:
        abort(404)
    try:
        paths = json.loads(item["photo_paths"] or "[]")
        entry = paths[index]
        local = entry["local"] if isinstance(entry, dict) else str(entry)
        if Path(local).exists():
            return send_file(local)
    except Exception:
        pass
    abort(404)


# ════════════════════════════════════════════════════════════════════
#  JSON API  (used by dynamic bits of the UI)
# ════════════════════════════════════════════════════════════════════

@app.route("/api/stats")
def api_stats():
    now   = datetime.now()
    stock = StockModel.get_dashboard_stats()
    month = SalesModel.get_monthly_stats(now.year, now.month)
    return jsonify(stock=dict(stock), month=dict(month))


@app.route("/api/growth-stages")
def api_growth_stages():
    item_type = request.args.get("type", "Plant")
    return jsonify(StockModel.GROWTH_STAGES.get(item_type, []))


@app.route("/api/server-info")
def api_server_info():
    """Return LAN address info — used by the desktop settings panel."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan_ip = s.getsockname()[0]
        s.close()
    except Exception:
        lan_ip = "127.0.0.1"
    from flask import request as req
    port = req.host.split(":")[-1] if ":" in req.host else "5000"
    return jsonify(lan_ip=lan_ip, port=port,
                   url=f"http://{lan_ip}:{port}")
