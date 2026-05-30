"""
Seed script — inserts / updates popular Alocasia cultivars.

Safe to re-run:
  - NEW names are inserted.
  - EXISTING names receive a common_name update if they don't have one yet.

Usage:
    python scripts/seed_species.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.connection import get_connection, initialize_db

# ──────────────────────────────────────────────────────────────────────────────
# (scientific_name, common_name, care_level, price_min, price_max, notes)
#   price_min  ≈ lowest typical asking price (small pup or corm)
#   price_max  ≈ highest typical asking price (mature specimen)
# ──────────────────────────────────────────────────────────────────────────────
SPECIES = [

    # ── Easy ─────────────────────────────────────────────────────────────────
    (
        "amazonica 'Polly'",
        "African Mask Plant",
        "Easy", 8, 30,
        "Best-selling alocasia. Compact dark glossy leaves with bright white veins. "
        "Tolerates lower light than most. Corms: $3-8, Pups: $8-20, Plants: $15-30.",
    ),
    (
        "amazonica 'Bambino'",
        "Bambino",
        "Easy", 5, 25,
        "Compact dwarf version of Polly; stays under 12 in. Ideal for desks and shelves. "
        "Very popular gift plant. Corms: $3-7, Pups: $7-15, Plants: $12-25.",
    ),
    (
        "amazonica 'Ivory Coast'",
        "Ivory Coast",
        "Easy", 10, 45,
        "Safari Series hybrid (parented by Pink Dragon). Pink stems with glossy green "
        "leaves; rapid grower. Corms: $6-14, Pups: $14-28, Plants: $26-45.",
    ),
    (
        "macrorrhiza",
        "Giant Taro",
        "Easy", 8, 55,
        "Massive lime-green arrow-shaped leaves; can hit 5 ft indoors. Very fast-growing "
        "and forgiving. Corms: $5-12, Pups: $12-25, Plants: $25-55.",
    ),
    (
        "macrorrhiza 'Variegated'",
        "Variegated Giant Taro",
        "Easy", 50, 800,
        "Each leaf uniquely splashed or sectored with white/cream. Highly coveted; "
        "very limited supply. Corms: $40-100, Pups: $100-300, Plants: $250-800.",
    ),
    (
        "macrorrhizos 'New Guinea Gold'",
        "New Guinea Gold",
        "Easy", 12, 55,
        "Dark green leaves on striking yellow-gold petioles. Coloring intensifies "
        "with bright light. Corms: $8-18, Pups: $18-35, Plants: $30-55.",
    ),
    (
        "odora",
        "Night-Scented Lily",
        "Easy", 8, 45,
        "Night-fragrant flowers; large upright paddle leaves. Extremely forgiving — "
        "one of the best alocasias for beginners. Corms: $4-10, Pups: $10-22, Plants: $20-45.",
    ),
    (
        "odora 'Variegata'",
        "Variegated Fragrant Alocasia",
        "Difficult", 40, 300,
        "Rare variegated form of odora; cream-and-green sectored leaves. "
        "Much harder to find than the species. Corms: $30-70, Pups: $70-180, Plants: $150-300.",
    ),
    (
        "cucullata",
        "Chinese Taro",
        "Easy", 5, 25,
        "Heart-shaped glossy leaves. Most resilient alocasia available — tolerates "
        "drought and low humidity. Corms: $3-7, Pups: $7-15, Plants: $12-25.",
    ),
    (
        "'Calidora'",
        "Persian Palm",
        "Easy", 10, 55,
        "Enormous paddle-shaped leaves on tall upright stems. Fast-growing statement "
        "plant; easy care. Corms: $6-12, Pups: $12-28, Plants: $28-55.",
    ),
    (
        "'Portora'",
        "Portora Elephant Ear",
        "Easy", 10, 60,
        "Large hybrid with dramatic wavy-edged leaves; rich dark green. Quick grower, "
        "great for outdoor patios in summer. Corms: $6-14, Pups: $14-30, Plants: $30-60.",
    ),
    (
        "'Regal Shields'",
        "Regal Shields",
        "Easy", 10, 55,
        "Deep olive-purple leaves with silver veining underneath. One of the most popular "
        "large indoor hybrids. Corms: $6-12, Pups: $12-28, Plants: $25-55.",
    ),
    (
        "wentii",
        "Hardy Elephant Ear",
        "Easy", 6, 40,
        "Large leaves with glossy dark-green tops and deep purple undersides. "
        "Handles humidity swings well. Corms: $4-10, Pups: $10-20, Plants: $20-40.",
    ),
    (
        "'Sarian'",
        "Sarian",
        "Easy", 8, 50,
        "Zebrina x micholitziana hybrid. Zebra-striped petioles with large glossy leaves. "
        "Faster-growing and more forgiving than either parent. Corms: $5-12, Pups: $12-25, Plants: $25-50.",
    ),
    (
        "'Serendipity'",
        "Serendipity",
        "Easy", 5, 30,
        "Compact dwarf hybrid; stays under 18 in. Very beginner-friendly with reliable "
        "growth. Great for small spaces. Corms: $3-8, Pups: $8-16, Plants: $14-30.",
    ),
    (
        "robusta",
        "Robust Elephant Ear",
        "Easy", 10, 55,
        "Very large bold leaves; heavy structural presence. Fast-growing and tough. "
        "Great landscape or statement indoor plant. Corms: $6-14, Pups: $14-30, Plants: $28-55.",
    ),
    (
        "gageana",
        "Yellow Stem Elephant Ear",
        "Easy", 8, 40,
        "Glossy green leaves on distinctive yellow-green petioles. Clumping habit; "
        "very reliable grower. Corms: $5-12, Pups: $12-22, Plants: $20-40.",
    ),

    # ── Moderate ─────────────────────────────────────────────────────────────
    (
        "zebrina",
        "Zebra Alocasia",
        "Moderate", 10, 75,
        "Iconic yellow-and-black zebra-striped petioles. Prefers consistent humidity "
        "(50%+) and bright indirect light. Corms: $6-14, Pups: $14-35, Plants: $30-75.",
    ),
    (
        "micholitziana 'Frydek'",
        "Green Velvet",
        "Moderate", 12, 80,
        "Deep-green velvety leaves with glowing white veins. Very popular; prone to "
        "spider mites in dry air. Corms: $8-18, Pups: $18-42, Plants: $38-80.",
    ),
    (
        "'Stingray'",
        "Stingray Alocasia",
        "Moderate", 10, 65,
        "Distinctive stingray-shaped leaves with a raised tail tip. Reliable moderate "
        "grower; always a conversation piece. Corms: $6-14, Pups: $14-32, Plants: $28-65.",
    ),
    (
        "lauterbachiana",
        "Purple Sword",
        "Moderate", 10, 60,
        "Long narrow wavy-edged leaves with reddish undersides. Upright habit; prefers "
        "55%+ humidity. Corms: $6-12, Pups: $12-28, Plants: $26-60.",
    ),
    (
        "'Pink Dragon'",
        "Pink Dragon",
        "Moderate", 12, 70,
        "Pale pink petioles mottled with silver and green. Eye-catching color; medium "
        "humidity needs (50%+). Corms: $8-16, Pups: $16-36, Plants: $32-70.",
    ),
    (
        "longiloba",
        "Tiger Taro",
        "Moderate", 8, 50,
        "Long lobed leaves with a pale midrib and silver-grey veins. Dependable grower; "
        "tolerates brief dry periods. Corms: $5-12, Pups: $12-24, Plants: $22-50.",
    ),
    (
        "'Jacklyn'",
        "Jacklyn",
        "Moderate", 12, 75,
        "Deeply lobed multi-tone leaves with striped petioles and fine hair texture. "
        "Trending variety; strong seller. Corms: $8-18, Pups: $18-40, Plants: $34-75.",
    ),
    (
        "'Morocco'",
        "Morocco",
        "Moderate", 12, 65,
        "Deeply ridged and quilted dark-green leaves with prominent veining. Slower "
        "grower but very striking. Corms: $8-16, Pups: $16-34, Plants: $30-65.",
    ),
    (
        "scalprum",
        "Scalprum Alocasia",
        "Moderate", 15, 90,
        "Thick, leathery, blade-like leaves with wavy edges. Unusual narrow form; "
        "collector favourite. Corms: $10-22, Pups: $22-48, Plants: $42-90.",
    ),
    (
        "'Maharani'",
        "Grey Dragon",
        "Moderate", 18, 110,
        "Thick waxy grey-green textured leaves; slow-growing but extremely structural. "
        "Corms: $12-28, Pups: $28-60, Plants: $52-110.",
    ),
    (
        "sanderiana",
        "Sanderiana",
        "Moderate", 15, 100,
        "Narrow deeply-lobed dark metallic-green leaves with bright white veins. "
        "Philippine native; moderate humidity (55%+). Corms: $10-22, Pups: $22-50, Plants: $45-100.",
    ),
    (
        "lowii",
        "Lowii Alocasia",
        "Moderate", 12, 70,
        "Glossy dark-green leaves with striking silvery undersides. Compact and "
        "manageable; rewarding grower. Corms: $8-18, Pups: $18-36, Plants: $32-70.",
    ),
    (
        "'Dark Star'",
        "Dark Star",
        "Moderate", 12, 70,
        "Near-black leaves with subtle silver veining. Increasingly popular collector "
        "variety. Corms: $8-18, Pups: $18-36, Plants: $32-70.",
    ),
    (
        "'California'",
        "California Elephant Ear",
        "Moderate", 10, 60,
        "Deeply lobed olive-green leaves with prominent veins. Vigorous grower; handles "
        "typical indoor humidity well. Corms: $6-14, Pups: $14-30, Plants: $26-60.",
    ),
    (
        "'Sumo'",
        "Sumo Alocasia",
        "Moderate", 12, 65,
        "Broad, thick, deeply wrinkled leaves. Compact habit; dramatic texture. "
        "Good seller in the collector market. Corms: $8-16, Pups: $16-34, Plants: $30-65.",
    ),
    (
        "reversa",
        "Reversa",
        "Moderate", 10, 60,
        "Thick oval leaves; undersides are more silvery than the tops. Unusual and "
        "underrated. Corms: $6-14, Pups: $14-28, Plants: $24-60.",
    ),
    (
        "'Ninja'",
        "Ninja Alocasia",
        "Moderate", 12, 70,
        "Very dark, almost black glossy leaves. A striking alternative to Black Velvet "
        "for growers who want less fuss. Corms: $8-16, Pups: $16-36, Plants: $30-70.",
    ),
    (
        "'Hilo Beauty'",
        "Hilo Beauty",
        "Moderate", 10, 60,
        "Mottled green-and-cream variegation on rounded leaves. Vigorous and more "
        "forgiving than most variegated forms. Corms: $6-14, Pups: $14-30, Plants: $26-60.",
    ),
    (
        "'Tiny Dancer'",
        "Tiny Dancer",
        "Moderate", 10, 50,
        "Unique cup-shaped leaves on slim upright stems. Very popular novelty variety; "
        "susceptible to overwatering — needs fast-draining aroid mix. "
        "Corms: $6-14, Pups: $14-28, Plants: $24-50.",
    ),
    (
        "macrorrhizos 'Flying Squid'",
        "Flying Squid",
        "Moderate", 15, 80,
        "Long tubular stems with a small pointed leaf tip giving a squid appearance. "
        "Deep green and burgundy tones. Needs excellent drainage. "
        "Corms: $10-22, Pups: $22-45, Plants: $40-80.",
    ),
    (
        "clypeolata",
        "Green Shield",
        "Moderate", 12, 65,
        "Round shield-shaped glossy leaves (Latin: clypeolata = little shield). "
        "Philippine native; reliable moderate grower. Corms: $8-16, Pups: $16-34, Plants: $30-65.",
    ),
    (
        "brancifolia",
        "Pink Passion",
        "Moderate", 15, 80,
        "Dramatic split and divided frond-like leaves; becomes more dramatic with age. "
        "Uncommon indoor plant from New Guinea. Corms: $10-22, Pups: $22-45, Plants: $38-80.",
    ),
    (
        "jacksoniana",
        "Jacksoniana",
        "Moderate", 12, 70,
        "Deeply lobed leaves with contrasting light veins on dark green. "
        "Collector favourite; less commonly available. Corms: $8-18, Pups: $18-36, Plants: $32-70.",
    ),
    (
        "'Corazon'",
        "Corazon",
        "Moderate", 12, 65,
        "Heart-shaped leaves with deep veining and a velvety surface. Compact and "
        "well-suited to terrariums. Corms: $8-16, Pups: $16-34, Plants: $28-65.",
    ),

    # ── Difficult ─────────────────────────────────────────────────────────────
    (
        "baginda 'Dragon Scale'",
        "Dragon Scale",
        "Difficult", 15, 140,
        "Emerald-green leaves with a pronounced dragon-scale pattern and dark veins. "
        "Needs 65%+ humidity. Corms: $12-30, Pups: $30-65, Plants: $60-140.",
    ),
    (
        "baginda 'Silver Dragon'",
        "Silver Dragon",
        "Difficult", 12, 110,
        "Silver-grey textured leaves with deep green veins on a compact plant. Stunning; "
        "needs stable humidity (65%+). Corms: $10-24, Pups: $24-55, Plants: $48-110.",
    ),
    (
        "reginula 'Black Velvet'",
        "Black Velvet",
        "Difficult", 15, 150,
        "Velvety near-black leaves with bold silver veins; very compact. Slow-growing "
        "jewel alocasia — highly coveted. Corms: $12-30, Pups: $30-70, Plants: $60-150.",
    ),
    (
        "cuprea 'Red Secret'",
        "Red Secret",
        "Difficult", 15, 150,
        "Metallic copper-red sheen on thick waxy leaves. One of the most visually "
        "striking alocasias; needs 65%+ humidity. Corms: $12-30, Pups: $30-70, Plants: $60-150.",
    ),
    (
        "nebula 'Imperialis'",
        "Imperialis",
        "Difficult", 25, 250,
        "Thick silvery-grey leaves with deep veins and a matte texture. Very rare and "
        "slow-growing. Corms: $20-55, Pups: $55-120, Plants: $100-250.",
    ),
    (
        "melo",
        "Melo Alocasia",
        "Difficult", 20, 200,
        "Deeply ridged cement-grey leaves with extraordinary texture. Extremely rare and "
        "highly sought-after. Corms: $16-45, Pups: $45-100, Plants: $80-200.",
    ),
    (
        "azlanii",
        "Rainbow Alocasia",
        "Difficult", 22, 200,
        "Iridescent blue-purple leaves with red veining. Extremely popular Malaysian "
        "native; limited supply drives premium prices. Corms: $18-50, Pups: $50-110, Plants: $88-200.",
    ),
    (
        "'Platinum'",
        "Platinum Alocasia",
        "Difficult", 15, 130,
        "Blue-green metallic leaves with waxy texture. Notably resistant to spider mites "
        "— a practical plus for a difficult variety. Corms: $10-28, Pups: $28-60, Plants: $55-130.",
    ),
    (
        "platyphylla",
        "Platyphylla",
        "Difficult", 20, 160,
        "Huge rounded leaves with bold contrasting veination. Rare outside specialist "
        "collections. Corms: $14-38, Pups: $38-80, Plants: $70-160.",
    ),
    (
        "micholitziana 'Frydek Variegata'",
        "Variegated Green Velvet",
        "Difficult", 80, 600,
        "Each leaf uniquely marbled with white/cream. Premium collector plant; extremely "
        "limited availability. Corms: $60-140, Pups: $140-350, Plants: $280-600.",
    ),
    (
        "baginda 'Dragon Scale Variegata'",
        "Variegated Dragon Scale",
        "Difficult", 100, 700,
        "Rare mint or cream sectors on the iconic scale-texture leaves. "
        "Investment-grade collector specimen. Corms: $80-180, Pups: $180-450, Plants: $350-700.",
    ),
    (
        "bisma",
        "Bisma",
        "Difficult", 18, 160,
        "Narrow, elongated leaves with bold silver veining on dark green. Rare Indonesian "
        "native increasingly sought by collectors. Corms: $12-35, Pups: $35-80, Plants: $65-160.",
    ),
    (
        "princeps 'Purple Cloak'",
        "Purple Cloak",
        "Difficult", 20, 150,
        "Dark purple-backed leaves with a dramatic near-black upper surface. "
        "Rare Philippine native. Corms: $14-36, Pups: $36-80, Plants: $65-150.",
    ),
]


def seed():
    initialize_db()
    inserted = 0
    updated  = 0
    skipped  = 0

    with get_connection() as conn:
        existing = {
            r[0].lower(): r[1]   # name.lower() -> id
            for r in conn.execute("SELECT name, id FROM species").fetchall()
        }

        for name, common_name, care_level, price_min, price_max, notes in SPECIES:
            key = name.lower()
            if key in existing:
                # Back-fill common_name if the row doesn't have one yet
                row = conn.execute(
                    "SELECT common_name FROM species WHERE id=?",
                    (existing[key],)
                ).fetchone()
                if not row["common_name"]:
                    conn.execute(
                        "UPDATE species SET common_name=?, care_level=? WHERE id=?",
                        (common_name, care_level, existing[key]),
                    )
                    updated += 1
                else:
                    skipped += 1
            else:
                conn.execute(
                    "INSERT INTO species "
                    "(name, common_name, care_level, price_min, price_max, notes) "
                    "VALUES (?,?,?,?,?,?)",
                    (name, common_name, care_level, price_min, price_max, notes),
                )
                inserted += 1

    print(
        f"Done. {inserted} new cultivar{'s' if inserted != 1 else ''} added, "
        f"{updated} common name{'s' if updated != 1 else ''} back-filled, "
        f"{skipped} already complete."
    )


if __name__ == "__main__":
    seed()
