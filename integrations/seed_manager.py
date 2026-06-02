"""
Species seed manager — discovers, previews, and imports seed packs.

A seed pack is any .py file in the species_seeds/ folder that contains:
    METADATA = { "name": ..., "genus": ..., "emoji": ..., "description": ...,
                 "version": ..., "source": ..., "author": ... }
    SPECIES   = [ (name, common_name, display_name, care_level,
                   price_min, price_max, notes), ... ]

Just drop a new .py file in species_seeds/ and it automatically appears
in the Import Species List dialog.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import NamedTuple


# ── locate the seeds directory ────────────────────────────────────────────────

def _seeds_dir() -> Path:
    """Return the species_seeds directory, whether running from source or bundle."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "species_seeds"
    return Path(__file__).parent.parent / "species_seeds"


# ── pack type ─────────────────────────────────────────────────────────────────

class SeedPack(NamedTuple):
    metadata: dict       # METADATA dict from the file
    species:  list       # SPECIES list from the file
    path:     Path       # absolute path to the .py file


# ── discovery ─────────────────────────────────────────────────────────────────

def discover() -> list[SeedPack]:
    """Return all valid seed packs found in species_seeds/, sorted by name."""
    seeds_dir = _seeds_dir()
    if not seeds_dir.exists():
        return []

    packs = []
    for py_file in sorted(seeds_dir.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        try:
            spec = importlib.util.spec_from_file_location(
                f"_seed_{py_file.stem}", py_file
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)                  # type: ignore[union-attr]
            if hasattr(mod, "METADATA") and hasattr(mod, "SPECIES"):
                packs.append(SeedPack(
                    metadata=mod.METADATA,
                    species=mod.SPECIES,
                    path=py_file,
                ))
        except Exception as exc:
            print(f"[seed_manager] Warning: could not load {py_file.name}: {exc}")

    return packs


# ── preview ───────────────────────────────────────────────────────────────────

def preview(pack: SeedPack) -> dict:
    """
    Return a dict with counts of what would happen if this pack were imported.
    Does NOT touch the database.

    Returns:
        { "total": int, "new": int, "update": int, "skip": int }
    """
    from database.connection import get_connection

    with get_connection() as conn:
        existing = {
            r[0].lower()
            for r in conn.execute("SELECT name FROM species").fetchall()
        }

    new = update = skip = 0
    for entry in pack.species:
        name = entry[0]
        if name.lower() in existing:
            # Would update if display_name is missing or common_name has "Alocasia"
            row = None
            try:
                from database.connection import get_connection as gc
                with gc() as conn:
                    row = conn.execute(
                        "SELECT display_name, common_name FROM species WHERE LOWER(name)=?",
                        (name.lower(),)
                    ).fetchone()
            except Exception:
                pass

            if row:
                needs = (
                    not row["display_name"]
                    or (row["common_name"] and
                        "alocasia" in row["common_name"].lower())
                )
                if needs:
                    update += 1
                else:
                    skip += 1
            else:
                skip += 1
        else:
            new += 1

    return {"total": len(pack.species), "new": new, "update": update, "skip": skip}


# ── import ────────────────────────────────────────────────────────────────────

def import_pack(
    pack: SeedPack,
    on_progress: "Callable[[str], None] | None" = None,
) -> dict:
    """
    Import a seed pack into the database.
    Returns { "inserted": int, "updated": int, "skipped": int }.
    Calls on_progress(message) periodically if provided.
    """
    from database.connection import get_connection

    inserted = updated = skipped = 0

    with get_connection() as conn:
        existing = {
            r[0].lower(): r[1]
            for r in conn.execute("SELECT name, id FROM species").fetchall()
        }

        total = len(pack.species)
        for i, entry in enumerate(pack.species):
            name, common_name, display_name, care_level, price_min, price_max, notes = entry
            key = name.lower()

            if on_progress and i % 10 == 0:
                on_progress(f"Processing {i + 1}/{total}…")

            if key in existing:
                row = conn.execute(
                    "SELECT common_name, display_name FROM species WHERE id=?",
                    (existing[key],)
                ).fetchone()

                needs_update = (
                    not row["display_name"]
                    or (row["common_name"] and
                        "alocasia" in row["common_name"].lower())
                )
                if needs_update:
                    conn.execute(
                        "UPDATE species SET "
                        "  common_name=?, display_name=?, care_level=?, "
                        "  price_min=?, price_max=?, notes=? "
                        "WHERE id=?",
                        (common_name, display_name, care_level,
                         price_min, price_max, notes, existing[key]),
                    )
                    updated += 1
                else:
                    # Still back-fill display_name if blank
                    if not row["display_name"]:
                        conn.execute(
                            "UPDATE species SET display_name=? WHERE id=?",
                            (display_name, existing[key]),
                        )
                        updated += 1
                    else:
                        skipped += 1
            else:
                conn.execute(
                    "INSERT INTO species "
                    "(name, common_name, display_name, care_level, "
                    " price_min, price_max, notes) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (name, common_name, display_name, care_level,
                     price_min, price_max, notes),
                )
                inserted += 1
                existing[key] = None   # prevent duplicate on same name in pack

    if on_progress:
        on_progress(f"Done — {inserted} added, {updated} updated, {skipped} unchanged.")

    return {"inserted": inserted, "updated": updated, "skipped": skipped}
