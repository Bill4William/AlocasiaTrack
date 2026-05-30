"""
Migration: add common_name column and normalise care_level values.
Safe to re-run.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.connection import get_connection, initialize_db

def run():
    initialize_db()
    with get_connection() as conn:
        # Add common_name if missing
        cols = [r[1] for r in conn.execute("PRAGMA table_info(species)").fetchall()]
        if "common_name" not in cols:
            conn.execute("ALTER TABLE species ADD COLUMN common_name TEXT")
            print("Added column: common_name")
        else:
            print("Column common_name already exists — skipped.")

        # Normalise legacy care_level values
        changes = conn.execute("""
            UPDATE species
            SET care_level = CASE care_level
                WHEN 'Medium'       THEN 'Moderate'
                WHEN 'Intermediate' THEN 'Moderate'
                WHEN 'Advanced'     THEN 'Difficult'
                ELSE care_level
            END
            WHERE care_level IN ('Medium', 'Intermediate', 'Advanced')
        """).rowcount
        print(f"Normalised {changes} care_level value(s).")

if __name__ == "__main__":
    run()
