"""
Database migrations that run automatically at startup.

Each migration is idempotent — safe to run on every launch.
New migrations are added to the MIGRATIONS list in order.
"""

from __future__ import annotations
from database.connection import get_connection


# ── Individual migration functions ────────────────────────────────────────────

def _fix_macrorrhiza_spelling(conn):
    """Rename the old misspelled 'macrorrhiza' entries to 'macrorrhizos'."""
    misspelled = [
        ("macrorrhiza",             "macrorrhizos"),
        ("macrorrhiza 'Variegated'","macrorrhizos 'Variegated'"),
    ]
    for bad, good in misspelled:
        bad_row = conn.execute(
            "SELECT id FROM species WHERE LOWER(name)=?", (bad.lower(),)
        ).fetchone()
        good_row = conn.execute(
            "SELECT id FROM species WHERE LOWER(name)=?", (good.lower(),)
        ).fetchone()
        if bad_row and good_row:
            # Both exist — remap references and delete the bad one
            bad_id, good_id = bad_row[0], good_row[0]
            conn.execute("UPDATE stock  SET species_id=? WHERE species_id=?", (good_id, bad_id))
            conn.execute("UPDATE plants SET species_id=? WHERE species_id=?", (good_id, bad_id))
            conn.execute("DELETE FROM species WHERE id=?", (bad_id,))
        elif bad_row:
            # Only bad spelling exists — rename it
            conn.execute(
                "UPDATE species SET name=? WHERE id=?", (good, bad_row[0])
            )


def _fix_stingray_duplicate(conn):
    """Merge standalone 'Stingray' into macrorrhizos 'Stingray'."""
    bad  = conn.execute("SELECT id FROM species WHERE name=?", ("'Stingray'",)).fetchone()
    good = conn.execute(
        "SELECT id FROM species WHERE name=?", ("macrorrhizos 'Stingray'",)
    ).fetchone()
    if bad and good and bad[0] != good[0]:
        conn.execute("UPDATE stock  SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("UPDATE plants SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("DELETE FROM species WHERE id=?", (bad[0],))


def _fix_california_duplicate(conn):
    """Merge standalone 'California' into odora 'California'."""
    bad  = conn.execute("SELECT id FROM species WHERE name=?", ("'California'",)).fetchone()
    good = conn.execute(
        "SELECT id FROM species WHERE name=?", ("odora 'California'",)
    ).fetchone()
    if bad and good and bad[0] != good[0]:
        conn.execute("UPDATE stock  SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("UPDATE plants SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("DELETE FROM species WHERE id=?", (bad[0],))


def _fix_tiny_dancer_duplicate(conn):
    """Merge 'Tiny Dancer' into 'Tiny Dancers' (Aroidpedia canonical name)."""
    bad  = conn.execute("SELECT id FROM species WHERE name=?", ("'Tiny Dancer'",)).fetchone()
    good = conn.execute("SELECT id FROM species WHERE name=?", ("'Tiny Dancers'",)).fetchone()
    if bad and good and bad[0] != good[0]:
        conn.execute("UPDATE stock  SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("UPDATE plants SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("DELETE FROM species WHERE id=?", (bad[0],))


def _fix_polly_duplicate(conn):
    """Remove bare 'Polly' entry — superseded by amazonica 'Polly'."""
    bad  = conn.execute("SELECT id FROM species WHERE name=?", ("Polly",)).fetchone()
    good = conn.execute(
        "SELECT id FROM species WHERE name=?", ("amazonica 'Polly'",)
    ).fetchone()
    if bad and good and bad[0] != good[0]:
        conn.execute("UPDATE stock  SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("UPDATE plants SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("DELETE FROM species WHERE id=?", (bad[0],))


def _fix_dragon_scale_duplicate(conn):
    """Remove bare 'Dragon Scale' — superseded by baginda 'Dragon Scale'."""
    bad  = conn.execute("SELECT id FROM species WHERE name=?", ("Dragon Scale",)).fetchone()
    good = conn.execute(
        "SELECT id FROM species WHERE name=?", ("baginda 'Dragon Scale'",)
    ).fetchone()
    if bad and good and bad[0] != good[0]:
        conn.execute("UPDATE stock  SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("UPDATE plants SET species_id=? WHERE species_id=?", (good[0], bad[0]))
        conn.execute("DELETE FROM species WHERE id=?", (bad[0],))


def _fix_micholitziana_common_name(conn):
    """
    micholitziana (base species) and micholitziana 'Green Velvet' (cultivar)
    both had common_name 'Green Velvet'.  Set the base species to 'Micholitziana'
    so the two entries are distinguishable.
    """
    row = conn.execute(
        "SELECT id, common_name FROM species WHERE name=?", ("micholitziana",)
    ).fetchone()
    if row and row[1] and row[1].lower() == "green velvet":
        conn.execute(
            "UPDATE species SET common_name=? WHERE id=?",
            ("Micholitziana", row[0]),
        )


def _strip_alocasia_from_common_names(conn):
    """Remove 'Alocasia' from any common_name that contains it."""
    import re
    rows = conn.execute(
        "SELECT id, common_name FROM species "
        "WHERE common_name LIKE '%alocasia%' COLLATE NOCASE"
    ).fetchall()
    for rid, cn in rows:
        new_cn = re.sub(r"\s+Alocasia$", "", cn, flags=re.IGNORECASE).strip()
        new_cn = re.sub(r"^Alocasia\s+", "", new_cn, flags=re.IGNORECASE).strip()
        if new_cn != cn:
            conn.execute("UPDATE species SET common_name=? WHERE id=?", (new_cn, rid))


def _backfill_display_names(conn):
    """
    Any species missing a display_name gets one generated from:
      'Alocasia ' + the cultivar part of the name, title-cased.
    E.g.  macrorrhizos 'Stingray'  →  'Alocasia Stingray'
          'Dark Star'              →  'Alocasia Dark Star'
          micholitziana            →  'Alocasia Micholitziana'
    """
    import re
    rows = conn.execute(
        "SELECT id, name, common_name FROM species WHERE display_name IS NULL OR display_name=''"
    ).fetchall()
    for rid, name, common_name in rows:
        # Extract the cultivar name from quotes if present
        m = re.search(r"'([^']+)'", name)
        if m:
            label = m.group(1)          # e.g. 'Stingray' → Stingray
        else:
            # Pure species — title-case the epithet
            label = name.strip("'").title()
        display = f"Alocasia {label}"
        conn.execute(
            "UPDATE species SET display_name=? WHERE id=?", (display, rid)
        )


def _fix_duplicate_display_names(conn):
    """
    After all other migrations, if any two entries still share a display_name,
    keep the one with the more-specific (longer) scientific name and remap the other.
    """
    from collections import defaultdict
    rows = conn.execute(
        "SELECT id, name, display_name FROM species ORDER BY LENGTH(name) DESC"
    ).fetchall()
    seen: dict[str, int] = {}   # display_name.lower() → canonical id
    for row in rows:
        key = (row[2] or "").lower()
        if not key:
            continue
        if key in seen:
            # This entry is a duplicate — remap and delete
            dup_id = row[0]
            keep_id = seen[key]
            conn.execute(
                "UPDATE stock  SET species_id=? WHERE species_id=?", (keep_id, dup_id)
            )
            conn.execute(
                "UPDATE plants SET species_id=? WHERE species_id=?", (keep_id, dup_id)
            )
            conn.execute("DELETE FROM species WHERE id=?", (dup_id,))
        else:
            seen[key] = row[0]


# ── Migration registry ────────────────────────────────────────────────────────

MIGRATIONS = [
    _fix_macrorrhiza_spelling,
    _fix_stingray_duplicate,
    _fix_california_duplicate,
    _fix_tiny_dancer_duplicate,
    _fix_polly_duplicate,
    _fix_dragon_scale_duplicate,
    _fix_micholitziana_common_name,
    _strip_alocasia_from_common_names,
    _backfill_display_names,
    _fix_duplicate_display_names,   # must be last
]


# ── Entry point ───────────────────────────────────────────────────────────────

def run_migrations():
    """Run all migrations in a single transaction. Called from initialize_db()."""
    with get_connection() as conn:
        for migration in MIGRATIONS:
            try:
                migration(conn)
            except Exception as exc:
                # Log but never crash the app over a migration
                print(f"[migrations] Warning: {migration.__name__} failed: {exc}")
