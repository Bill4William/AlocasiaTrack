"""
Seed script — imports the built-in Alocasia species pack into the database.

This is now a thin wrapper around the seed_manager + species_seeds/alocasia.py.
The full species data lives in species_seeds/alocasia.py; this script is kept
for backward compatibility and CI/CD pipelines.

Usage:
    python scripts/seed_species.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.connection import initialize_db
from integrations.seed_manager import discover, import_pack


def seed():
    initialize_db()
    packs = discover()
    if not packs:
        print("No seed packs found in species_seeds/")
        return

    total_ins = total_upd = total_skip = 0
    for pack in packs:
        name = pack.metadata.get("name", pack.path.stem)
        result = import_pack(pack)
        total_ins  += result["inserted"]
        total_upd  += result["updated"]
        total_skip += result["skipped"]
        print(
            f"  {name}: {result['inserted']} added, "
            f"{result['updated']} updated, {result['skipped']} unchanged"
        )

    print(
        f"\nDone.  {total_ins} new cultivar{'s' if total_ins != 1 else ''} added, "
        f"{total_upd} row{'s' if total_upd != 1 else ''} updated, "
        f"{total_skip} already complete."
    )


if __name__ == "__main__":
    seed()
