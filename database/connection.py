import sqlite3
import os
from pathlib import Path

DB_DIR = Path(os.path.expanduser("~")) / "AppData" / "Local" / "AlocasiaTrack"
DB_PATH = DB_DIR / "inventory.db"


def get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS species (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL UNIQUE,
                common_name TEXT,
                notes       TEXT,
                care_level  TEXT DEFAULT 'Moderate',
                price_min   REAL,
                price_max   REAL,
                created_at  TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS plants (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                species_id    INTEGER REFERENCES species(id) ON DELETE SET NULL,
                nickname      TEXT,
                acquired_date TEXT,
                pot_size      TEXT,
                health_status TEXT DEFAULT 'Healthy',
                location      TEXT,
                notes         TEXT,
                photo_paths   TEXT DEFAULT '[]',
                created_at    TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS stock (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                sku             TEXT UNIQUE,
                item_type       TEXT NOT NULL CHECK(item_type IN ('Plant', 'Pup', 'Corm')),
                species_id      INTEGER REFERENCES species(id) ON DELETE SET NULL,
                parent_plant_id INTEGER REFERENCES plants(id) ON DELETE SET NULL,
                growth_stage    TEXT,
                condition       TEXT DEFAULT 'Good',
                pot_size        TEXT,
                asking_price    REAL,
                cost_basis      REAL DEFAULT 0,
                status          TEXT DEFAULT 'Available'
                                CHECK(status IN ('Available', 'Listed', 'Sold', 'Traded', 'Died')),
                photo_paths     TEXT DEFAULT '[]',
                date_added      TEXT DEFAULT (datetime('now')),
                notes           TEXT
            );

            CREATE TABLE IF NOT EXISTS listings (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_id            INTEGER REFERENCES stock(id) ON DELETE CASCADE,
                platform            TEXT NOT NULL
                                    CHECK(platform IN ('Facebook', 'Shopify', 'Other')),
                listing_url         TEXT,
                listed_price        REAL,
                date_posted         TEXT DEFAULT (datetime('now')),
                last_updated        TEXT,
                is_active           INTEGER DEFAULT 1,
                platform_listing_id TEXT,
                notes               TEXT
            );

            CREATE TABLE IF NOT EXISTS sales (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_id        INTEGER REFERENCES stock(id),
                listing_id      INTEGER REFERENCES listings(id),
                sale_price      REAL NOT NULL,
                platform        TEXT,
                sale_date       TEXT DEFAULT (datetime('now')),
                buyer_name      TEXT,
                buyer_contact   TEXT,
                shipping_method TEXT DEFAULT 'Local Pickup',
                shipping_cost   REAL DEFAULT 0,
                profit          REAL,
                notes           TEXT
            );
        """)

    # Inline migrations — safe to re-run on every launch.
    with get_connection() as conn:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(species)").fetchall()]
        if "common_name" not in cols:
            conn.execute("ALTER TABLE species ADD COLUMN common_name TEXT")
        # display_name: "Alocasia Polly" style trade name (genus always included)
        # common_name is now the nickname only, e.g. "Polly" / "African Mask Plant"
        if "display_name" not in cols:
            conn.execute("ALTER TABLE species ADD COLUMN display_name TEXT")
