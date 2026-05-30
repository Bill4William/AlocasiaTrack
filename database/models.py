from database.connection import get_connection


class SpeciesModel:
    @staticmethod
    def get_all():
        with get_connection() as conn:
            return conn.execute("SELECT * FROM species ORDER BY name").fetchall()

    @staticmethod
    def get_by_id(id):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM species WHERE id=?", (id,)).fetchone()

    @staticmethod
    def get_names() -> list[str]:
        with get_connection() as conn:
            rows = conn.execute("SELECT name FROM species ORDER BY name").fetchall()
            return [r["name"] for r in rows]

    @staticmethod
    def get_name_id_map() -> dict:
        with get_connection() as conn:
            rows = conn.execute("SELECT id, name FROM species ORDER BY name").fetchall()
            return {r["name"]: r["id"] for r in rows}

    @staticmethod
    def create(name, notes="", care_level="Moderate", price_min=None, price_max=None,
               common_name=""):
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO species (name, common_name, notes, care_level, price_min, price_max) "
                "VALUES (?,?,?,?,?,?)",
                (name, common_name or None, notes, care_level, price_min, price_max),
            )

    @staticmethod
    def update(id, name, notes, care_level, price_min, price_max, common_name=""):
        with get_connection() as conn:
            conn.execute(
                "UPDATE species SET name=?, common_name=?, notes=?, care_level=?, "
                "price_min=?, price_max=? WHERE id=?",
                (name, common_name or None, notes, care_level, price_min, price_max, id),
            )

    @staticmethod
    def delete(id):
        with get_connection() as conn:
            conn.execute("DELETE FROM species WHERE id=?", (id,))

    @staticmethod
    def get_stock_counts() -> dict:
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT sp.id, COUNT(st.id) as cnt
                FROM species sp
                LEFT JOIN stock st ON st.species_id = sp.id AND st.status != 'Sold'
                GROUP BY sp.id
            """).fetchall()
            return {r["id"]: r["cnt"] for r in rows}


class PlantsModel:
    @staticmethod
    def get_all():
        with get_connection() as conn:
            return conn.execute("""
                SELECT p.*, s.name AS species_name, s.common_name AS species_common_name
                FROM plants p
                LEFT JOIN species s ON p.species_id = s.id
                ORDER BY p.created_at DESC
            """).fetchall()

    @staticmethod
    def get_by_id(id):
        with get_connection() as conn:
            return conn.execute("""
                SELECT p.*, s.name AS species_name, s.common_name AS species_common_name
                FROM plants p
                LEFT JOIN species s ON p.species_id = s.id
                WHERE p.id=?
            """, (id,)).fetchone()

    @staticmethod
    def get_dropdown_options() -> list[tuple]:
        """Returns list of (id, display_label) for dropdowns."""
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT p.id, p.nickname, s.name AS species_name, s.common_name AS species_common_name
                FROM plants p
                LEFT JOIN species s ON p.species_id = s.id
                ORDER BY s.name, p.nickname
            """).fetchall()
            return [(r["id"], f"{r['nickname'] or 'Unnamed'} ({r['species_name'] or '?'})") for r in rows]

    @staticmethod
    def create(species_id, nickname, acquired_date, pot_size, health_status,
               location, notes, photo_paths="[]"):
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO plants
                   (species_id, nickname, acquired_date, pot_size, health_status,
                    location, notes, photo_paths)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (species_id, nickname, acquired_date, pot_size, health_status,
                 location, notes, photo_paths),
            )

    @staticmethod
    def update(id, species_id, nickname, acquired_date, pot_size, health_status,
               location, notes, photo_paths="[]"):
        with get_connection() as conn:
            conn.execute(
                """UPDATE plants SET species_id=?, nickname=?, acquired_date=?, pot_size=?,
                   health_status=?, location=?, notes=?, photo_paths=? WHERE id=?""",
                (species_id, nickname, acquired_date, pot_size, health_status,
                 location, notes, photo_paths, id),
            )

    @staticmethod
    def update_photos(id, photo_paths_json: str):
        with get_connection() as conn:
            conn.execute("UPDATE plants SET photo_paths=? WHERE id=?",
                         (photo_paths_json, id))

    @staticmethod
    def delete(id):
        with get_connection() as conn:
            conn.execute("DELETE FROM plants WHERE id=?", (id,))


class StockModel:
    GROWTH_STAGES = {
        "Plant":  ["Juvenile", "Intermediate", "Mature", "Specimen"],
        "Pup":    ["Offset", "Juvenile", "Established"],
        "Corm":   ["Dormant", "Sprouting", "Rooted"],
    }
    CONDITIONS = ["Excellent", "Good", "Fair", "Needs TLC"]
    STATUSES   = ["Available", "Listed", "Sold", "Traded", "Died"]

    @staticmethod
    def get_pot_sizes() -> list[str]:
        from integrations.config import get_pot_sizes
        return get_pot_sizes()

    # Static fallback used by any code that references StockModel.POT_SIZES directly
    POT_SIZES  = ["No pot", '2"', '4"', '6"', '8"', '10"', '12"+']

    @staticmethod
    def _next_sku(item_type: str, conn) -> str:
        prefix = {"Plant": "PLT", "Pup": "PUP", "Corm": "CRM"}.get(item_type, "ITM")
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM stock WHERE item_type=?", (item_type,)
        ).fetchone()
        return f"{prefix}-{(row['cnt'] or 0) + 1:04d}"

    @staticmethod
    def get_all(item_type=None, status=None, species_id=None):
        q = """
            SELECT st.*, sp.name AS species_name, sp.common_name AS species_common_name,
                   pl.nickname AS parent_nickname
            FROM stock st
            LEFT JOIN species sp ON st.species_id = sp.id
            LEFT JOIN plants  pl ON st.parent_plant_id = pl.id
            WHERE 1=1
        """
        params = []
        if item_type:
            q += " AND st.item_type=?";  params.append(item_type)
        if status:
            q += " AND st.status=?";     params.append(status)
        if species_id:
            q += " AND st.species_id=?"; params.append(species_id)
        q += " ORDER BY st.date_added DESC"
        with get_connection() as conn:
            return conn.execute(q, params).fetchall()

    @staticmethod
    def get_by_id(id):
        with get_connection() as conn:
            return conn.execute("""
                SELECT st.*, sp.name AS species_name, sp.common_name AS species_common_name,
                       pl.nickname AS parent_nickname
                FROM stock st
                LEFT JOIN species sp ON st.species_id = sp.id
                LEFT JOIN plants  pl ON st.parent_plant_id = pl.id
                WHERE st.id=?
            """, (id,)).fetchone()

    @staticmethod
    def create(item_type, species_id, parent_plant_id, growth_stage,
               condition, pot_size, asking_price, cost_basis, notes,
               photo_paths="[]") -> str:
        with get_connection() as conn:
            sku = StockModel._next_sku(item_type, conn)
            conn.execute(
                """INSERT INTO stock
                   (sku, item_type, species_id, parent_plant_id, growth_stage,
                    condition, pot_size, asking_price, cost_basis, notes, photo_paths)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (sku, item_type, species_id or None, parent_plant_id or None,
                 growth_stage, condition, pot_size, asking_price, cost_basis,
                 notes, photo_paths),
            )
            return sku

    @staticmethod
    def update(id, item_type, species_id, parent_plant_id, growth_stage,
               condition, pot_size, asking_price, cost_basis, status, notes,
               photo_paths="[]"):
        with get_connection() as conn:
            conn.execute(
                """UPDATE stock SET item_type=?, species_id=?, parent_plant_id=?,
                   growth_stage=?, condition=?, pot_size=?, asking_price=?,
                   cost_basis=?, status=?, notes=?, photo_paths=? WHERE id=?""",
                (item_type, species_id or None, parent_plant_id or None, growth_stage,
                 condition, pot_size, asking_price, cost_basis, status, notes,
                 photo_paths, id),
            )

    @staticmethod
    def update_status(id, status):
        with get_connection() as conn:
            conn.execute("UPDATE stock SET status=? WHERE id=?", (status, id))

    @staticmethod
    def update_photos(id, photo_paths_json: str):
        with get_connection() as conn:
            conn.execute("UPDATE stock SET photo_paths=? WHERE id=?",
                         (photo_paths_json, id))

    @staticmethod
    def delete(id):
        with get_connection() as conn:
            conn.execute("DELETE FROM stock WHERE id=?", (id,))

    @staticmethod
    def get_available_count_for_species(species_id: int) -> int:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM stock WHERE species_id=? AND status='Available'",
                (species_id,),
            ).fetchone()
            return row[0] if row else 0

    @staticmethod
    def get_dashboard_stats() -> dict:
        with get_connection() as conn:
            stats = {}
            stats["total"]     = conn.execute("SELECT COUNT(*) FROM stock").fetchone()[0]
            stats["available"] = conn.execute("SELECT COUNT(*) FROM stock WHERE status='Available'").fetchone()[0]
            stats["listed"]    = conn.execute("SELECT COUNT(*) FROM stock WHERE status='Listed'").fetchone()[0]
            stats["sold"]      = conn.execute("SELECT COUNT(*) FROM stock WHERE status='Sold'").fetchone()[0]
            by_type = conn.execute(
                "SELECT item_type, COUNT(*) AS cnt FROM stock GROUP BY item_type"
            ).fetchall()
            stats["by_type"] = {r["item_type"]: r["cnt"] for r in by_type}
            stats["available_value"] = conn.execute(
                "SELECT COALESCE(SUM(asking_price),0) FROM stock WHERE status='Available'"
            ).fetchone()[0]
            return stats


class ListingsModel:
    @staticmethod
    def create(stock_id: int, platform: str, listed_price: float,
               listing_url: str = "", notes: str = "") -> int:
        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO listings
                   (stock_id, platform, listed_price, listing_url, notes)
                   VALUES (?,?,?,?,?)""",
                (stock_id, platform, listed_price, listing_url, notes),
            )
            conn.execute("UPDATE stock SET status='Listed' WHERE id=?", (stock_id,))
            return cur.lastrowid

    @staticmethod
    def update_url(id: int, listing_url: str):
        with get_connection() as conn:
            conn.execute(
                "UPDATE listings SET listing_url=?, last_updated=datetime('now') WHERE id=?",
                (listing_url, id),
            )

    @staticmethod
    def get_by_stock(stock_id: int):
        with get_connection() as conn:
            return conn.execute(
                "SELECT * FROM listings WHERE stock_id=? ORDER BY date_posted DESC",
                (stock_id,),
            ).fetchall()

    @staticmethod
    def get_active(platform: str | None = None):
        q = """
            SELECT l.*, st.sku, st.item_type, sp.name AS species_name,
                   sp.common_name AS species_common_name
            FROM listings l
            LEFT JOIN stock   st ON l.stock_id  = st.id
            LEFT JOIN species sp ON st.species_id = sp.id
            WHERE l.is_active=1
        """
        params = []
        if platform:
            q += " AND l.platform=?"; params.append(platform)
        q += " ORDER BY l.date_posted DESC"
        with get_connection() as conn:
            return conn.execute(q, params).fetchall()

    @staticmethod
    def mark_inactive(id: int):
        with get_connection() as conn:
            conn.execute("UPDATE listings SET is_active=0 WHERE id=?", (id,))


class SalesModel:
    @staticmethod
    def get_all():
        with get_connection() as conn:
            return conn.execute("""
                SELECT sa.*, st.sku, st.item_type, sp.name AS species_name,
                       sp.common_name AS species_common_name
                FROM sales sa
                LEFT JOIN stock   st ON sa.stock_id = st.id
                LEFT JOIN species sp ON st.species_id = sp.id
                ORDER BY sa.sale_date DESC
            """).fetchall()

    @staticmethod
    def create(stock_id, listing_id, sale_price, platform, sale_date,
               buyer_name, buyer_contact, shipping_method, shipping_cost, cost_basis, notes):
        profit = (sale_price or 0) - (cost_basis or 0) - (shipping_cost or 0)
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO sales
                   (stock_id, listing_id, sale_price, platform, sale_date, buyer_name,
                    buyer_contact, shipping_method, shipping_cost, profit, notes)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (stock_id, listing_id, sale_price, platform, sale_date, buyer_name,
                 buyer_contact, shipping_method, shipping_cost, profit, notes),
            )
            conn.execute("UPDATE stock SET status='Sold' WHERE id=?", (stock_id,))

    @staticmethod
    def get_monthly_stats(year: int, month: int) -> dict:
        with get_connection() as conn:
            row = conn.execute("""
                SELECT COALESCE(SUM(sale_price), 0) AS revenue,
                       COALESCE(SUM(profit),     0) AS profit,
                       COUNT(*)                      AS count
                FROM sales
                WHERE strftime('%Y', sale_date) = ?
                  AND strftime('%m', sale_date) = ?
            """, (str(year), f"{month:02d}")).fetchone()
            return dict(row)

    @staticmethod
    def get_all_time_stats() -> dict:
        with get_connection() as conn:
            row = conn.execute("""
                SELECT COALESCE(SUM(sale_price), 0) AS total_revenue,
                       COALESCE(SUM(profit),     0) AS total_profit,
                       COUNT(*)                      AS total_sales
                FROM sales
            """).fetchone()
            return dict(row)
