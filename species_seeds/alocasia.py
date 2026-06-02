"""
Alocasia species seed pack for AlocasiaTrack.

Drop any .py file with METADATA + SPECIES into the species_seeds/ folder
and it will automatically appear in the Import Species List dialog.

Tuple format per entry:
  (scientific_name, common_name, display_name, care_level, price_min, price_max, notes)

  scientific_name  Epithet only — "Alocasia" genus prefix is NOT included.
                   e.g.  amazonica 'Polly'
  common_name      Nickname with NO genus prefix.  e.g.  Polly
  display_name     Full trade name WITH genus.     e.g.  Alocasia Polly
"""

# ── Pack metadata — shown in the Import dialog ────────────────────────────────
METADATA = {
    "name":        "Alocasia",
    "genus":       "Alocasia",
    "emoji":       "🌿",
    "description": "327 Alocasia species, cultivars and hybrids — "
                   "Full Aroidpedia species, cultivars and hybrids lists. "
                   "Easy through Difficult care levels.",
    "version":     "1.1",
    "source":      "https://www.aroidpedia.com/alocasia",
    "author":      "AlocasiaTrack built-in",
}

# ── Species data ──────────────────────────────────────────────────────────────
SPECIES = [

    # ════════════════════ EASY ════════════════════════════════════════════════

    (
        "amazonica 'Polly'",
        "Polly",
        "Alocasia Polly",
        "Easy", 8, 30,
        "Best-selling alocasia worldwide. Compact, dark glossy leaves with bright white "
        "veins. Tolerates lower light better than most. A smaller mutant of Amazonica, "
        "created at Amazon Nurseries, Miami in the 1950s. Corms: $3-8, Pups: $8-20, Plants: $15-30.",
    ),
    (
        "amazonica",
        "Amazon Elephant Ear",
        "Alocasia Amazonica",
        "Easy", 10, 45,
        "The original hybrid (A. sanderiana × A. longiloba 'Watsoniana') bred in the 1950s. "
        "Larger and more dramatic than 'Polly'. Note: despite the name, Alocasia is strictly "
        "Asian — 'Amazonica' refers to Amazon Nurseries in Miami, not the Amazon rainforest. "
        "Corms: $6-15, Pups: $15-30, Plants: $28-45.",
    ),
    (
        "amazonica 'Bambino'",
        "Bambino",
        "Alocasia Bambino",
        "Easy", 5, 25,
        "Dwarf version of Polly; stays under 12 in. Ideal for desks and shelves. "
        "Very popular gift plant. Corms: $3-7, Pups: $7-15, Plants: $12-25.",
    ),
    (
        "amazonica 'Ivory Coast'",
        "Ivory Coast",
        "Alocasia Ivory Coast",
        "Easy", 10, 45,
        "Safari Series hybrid, parented by Pink Dragon. Pink stems with glossy green "
        "leaves; rapid grower. Corms: $6-14, Pups: $14-28, Plants: $26-45.",
    ),
    (
        "macrorrhizos",
        "Giant Taro",
        "Alocasia Macrorrhizos",
        "Easy", 8, 55,
        "Massive lime-green arrow-shaped leaves; can reach 5 ft indoors. Very fast-growing "
        "and forgiving. One of the most widely cultivated Alocasias globally. "
        "Corms: $5-12, Pups: $12-25, Plants: $25-55.",
    ),
    (
        "macrorrhizos 'Variegated'",
        "Variegated Giant Taro",
        "Alocasia Macrorrhizos Variegated",
        "Easy", 50, 800,
        "Each leaf uniquely splashed or sectored with white and cream. Highly coveted; "
        "very limited supply. Corms: $40-100, Pups: $100-300, Plants: $250-800.",
    ),
    (
        "macrorrhizos 'New Guinea Gold'",
        "New Guinea Gold",
        "Alocasia New Guinea Gold",
        "Easy", 12, 55,
        "Dark green leaves on striking yellow-gold petioles. Coloring intensifies "
        "with bright light. Corms: $8-18, Pups: $18-35, Plants: $30-55.",
    ),
    (
        "macrorrhizos 'Borneo Giant'",
        "Borneo Giant",
        "Alocasia Borneo Giant",
        "Easy", 15, 70,
        "One of the largest Alocasia cultivars — leaves can exceed 6 ft outdoors. "
        "Impressive landscape statement plant. Corms: $10-20, Pups: $20-40, Plants: $35-70.",
    ),
    (
        "macrorrhizos 'Black Stem'",
        "Black Stem",
        "Alocasia Black Stem",
        "Easy", 10, 50,
        "Characteristic near-black petioles contrast with large green upright leaves. "
        "Striking colour contrast; vigorous grower. Corms: $6-14, Pups: $14-28, Plants: $25-50.",
    ),
    (
        "macrorrhizos 'Baby Ray'",
        "Baby Ray",
        "Alocasia Baby Ray",
        "Easy", 10, 45,
        "Compact macrorrhizos cultivar with smaller, rounder leaves on shorter stems. "
        "Better suited to indoor spaces than the full species. Corms: $6-14, Pups: $14-28, Plants: $22-45.",
    ),
    (
        "macrorrhizos 'Big Mac'",
        "Big Mac",
        "Alocasia Big Mac",
        "Easy", 12, 55,
        "Exceptionally broad paddle-shaped leaves with a thick, robust structure. "
        "Fast-growing landscape or patio showpiece. Corms: $8-16, Pups: $16-32, Plants: $28-55.",
    ),
    (
        "macrorrhizos 'Rubra'",
        "Rubra",
        "Alocasia Rubra",
        "Easy", 12, 55,
        "Rich red-purple leaf undersides and reddish petioles. Bold color contrast; "
        "vigorous grower. Corms: $8-16, Pups: $16-32, Plants: $28-55.",
    ),
    (
        "macrorrhizos 'Plumbea'",
        "Plumbea",
        "Alocasia Plumbea",
        "Easy", 12, 55,
        "Blue-grey tinted leaves with a matte, lead-like sheen (plumbea = lead-coloured). "
        "Unusual colouring for a large alocasia. Corms: $8-16, Pups: $16-32, Plants: $28-55.",
    ),
    (
        "macrorrhizos 'Lutea'",
        "Lutea",
        "Alocasia Lutea",
        "Easy", 12, 55,
        "Creamy yellow-green leaves and pale petioles; a softer, golden-toned form. "
        "Vigorous and easy to grow like the base species. Corms: $8-16, Pups: $16-32, Plants: $28-55.",
    ),
    (
        "macrorrhizos 'Stingray'",
        "Stingray",
        "Alocasia Stingray",
        "Moderate", 10, 65,
        "Distinctive stingray-shaped leaves with an elongated raised tail tip. Reliable "
        "moderate grower; always a conversation piece. Corms: $6-14, Pups: $14-32, Plants: $28-65.",
    ),
    # Legacy standalone 'Stingray' entry removed — use macrorrhizos 'Stingray'
    (
        "macrorrhizos 'Shock Treatment'",
        "Shock Treatment",
        "Alocasia Shock Treatment",
        "Moderate", 15, 75,
        "Highly variegated cultivar with irregular white and green sectoring on large "
        "leaves. Eye-catching and rare. Corms: $10-20, Pups: $20-40, Plants: $38-75.",
    ),
    (
        "macrorrhizos 'Flying Squid'",
        "Flying Squid",
        "Alocasia Flying Squid",
        "Moderate", 15, 80,
        "Long tubular stems terminate in a small leaf tip, giving a squid-like silhouette. "
        "Deep green and burgundy tones; needs excellent drainage. "
        "Corms: $10-22, Pups: $22-45, Plants: $40-80.",
    ),
    (
        "odora",
        "Night-Scented Lily",
        "Alocasia Odora",
        "Easy", 8, 45,
        "Night-fragrant flowers; large upright paddle-shaped leaves. Extremely forgiving — "
        "one of the best Alocasias for beginners. Corms: $4-10, Pups: $10-22, Plants: $20-45.",
    ),
    (
        "odora 'Variegata'",
        "Variegated Night-Scented Lily",
        "Alocasia Odora Variegata",
        "Difficult", 40, 300,
        "Rare cream-and-green sectored variegated form of odora. Much harder to find "
        "than the species. Corms: $30-70, Pups: $70-180, Plants: $150-300.",
    ),
    (
        "cucullata",
        "Chinese Taro",
        "Alocasia Cucullata",
        "Easy", 5, 25,
        "Heart-shaped glossy leaves. Most resilient Alocasia — tolerates drought and "
        "low humidity. Corms: $3-7, Pups: $7-15, Plants: $12-25.",
    ),
    (
        "cucullata 'Yellow Tail'",
        "Yellow Tail",
        "Alocasia Yellow Tail",
        "Easy", 8, 35,
        "Compact cucullata with distinctive yellow-tipped leaves. Cheerful coloring; "
        "shares the tough-as-nails constitution of the base species. "
        "Corms: $5-12, Pups: $12-22, Plants: $18-35.",
    ),
    (
        "'Calidora'",
        "Persian Palm",
        "Alocasia Calidora",
        "Easy", 10, 55,
        "Enormous paddle-shaped leaves on tall upright stems. Fast-growing statement "
        "plant; easy care. Corms: $6-12, Pups: $12-28, Plants: $28-55.",
    ),
    (
        "'Portora'",
        "Portora Elephant Ear",
        "Alocasia Portora",
        "Easy", 10, 60,
        "Large hybrid with dramatic wavy-edged leaves; rich dark green. Quick grower, "
        "great for outdoor patios in summer. Corms: $6-14, Pups: $14-30, Plants: $30-60.",
    ),
    (
        "'Regal Shields'",
        "Regal Shields",
        "Alocasia Regal Shields",
        "Easy", 10, 55,
        "Deep olive-purple leaves with silver veining on the underside. One of the most "
        "popular large indoor hybrids. Corms: $6-12, Pups: $12-28, Plants: $25-55.",
    ),
    (
        "wentii",
        "Hardy Elephant Ear",
        "Alocasia Wentii",
        "Easy", 6, 40,
        "Large leaves with glossy dark-green tops and deep purple undersides. "
        "Handles humidity swings well. Corms: $4-10, Pups: $10-20, Plants: $20-40.",
    ),
    (
        "'Sarian'",
        "Sarian",
        "Alocasia Sarian",
        "Easy", 8, 50,
        "Zebrina × micholitziana hybrid. Zebra-striped petioles with large glossy leaves. "
        "Faster-growing and more forgiving than either parent. Corms: $5-12, Pups: $12-25, Plants: $25-50.",
    ),
    (
        "'Serendipity'",
        "Serendipity",
        "Alocasia Serendipity",
        "Easy", 5, 30,
        "Compact dwarf hybrid; stays under 18 in. Very beginner-friendly with reliable "
        "growth. Great for small spaces. Corms: $3-8, Pups: $8-16, Plants: $14-30.",
    ),
    (
        "robusta",
        "Robust Elephant Ear",
        "Alocasia Robusta",
        "Easy", 10, 55,
        "Very large bold leaves; heavy structural presence. Fast-growing and tough. "
        "Great landscape or statement indoor plant. Corms: $6-14, Pups: $14-30, Plants: $28-55.",
    ),
    (
        "gageana",
        "Yellow Stem Elephant Ear",
        "Alocasia Gageana",
        "Easy", 8, 40,
        "Glossy green leaves on distinctive yellow-green petioles. Clumping habit; "
        "very reliable grower. Corms: $5-12, Pups: $12-22, Plants: $20-40.",
    ),
    (
        "brisbanensis",
        "Cunjevoi",
        "Alocasia Brisbanensis",
        "Easy", 6, 35,
        "Australian native species with large dark-green upright leaves. Extremely "
        "robust; handles lower temperatures than most Alocasias. "
        "Corms: $4-10, Pups: $10-20, Plants: $18-35.",
    ),
    (
        "longiloba",
        "Tiger Taro",
        "Alocasia Longiloba",
        "Moderate", 8, 50,
        "Long lobed leaves with a pale midrib and silver-grey veins. Dependable grower; "
        "tolerates brief dry periods. Corms: $5-12, Pups: $12-24, Plants: $22-50.",
    ),
    (
        "longiloba 'Purple'",
        "Purple Longiloba",
        "Alocasia Purple Longiloba",
        "Moderate", 10, 55,
        "Rich purple undersides and stems on the classic longiloba leaf form. "
        "Striking colour; similar care to the base species. "
        "Corms: $6-14, Pups: $14-28, Plants: $26-55.",
    ),
    (
        "sakonakhonensis",
        "Sakonakhon Taro",
        "Alocasia Sakonakhonensis",
        "Moderate", 15, 80,
        "Rare Thai native with distinctive matte green arrowhead leaves and prominent "
        "white veins. Sought-after collector species. Corms: $10-22, Pups: $22-45, Plants: $40-80.",
    ),

    # ════════════════════ MODERATE ════════════════════════════════════════════

    (
        "zebrina",
        "Zebra Plant",
        "Alocasia Zebrina",
        "Moderate", 10, 75,
        "Iconic yellow-and-black zebra-striped petioles. Native to the Philippines. "
        "Prefers consistent humidity (50%+) and bright indirect light. "
        "Corms: $6-14, Pups: $14-35, Plants: $30-75.",
    ),
    (
        "micholitziana",
        "Green Velvet",
        "Alocasia Micholitziana",
        "Moderate", 12, 70,
        "Philippine native with deep-green leaves and bright white veins. Parent of the "
        "widely sold 'Frydek' cultivar. "
        "Corms: $8-18, Pups: $18-38, Plants: $34-70.",
    ),
    (
        "micholitziana 'Frydek'",
        "Green Velvet Frydek",
        "Alocasia Frydek",
        "Moderate", 12, 80,
        "Deep-green velvety leaves with glowing white veins. Very popular; prone to "
        "spider mites in dry air. Corms: $8-18, Pups: $18-42, Plants: $38-80.",
    ),
    (
        "micholitziana 'London Eye'",
        "London Eye",
        "Alocasia London Eye",
        "Moderate", 15, 90,
        "Dramatic cultivar with huge circular-lobed leaves and pronounced veining. "
        "Named for the distinctive eye-like leaf form. Corms: $10-22, Pups: $22-48, Plants: $42-90.",
    ),
    (
        "micholitziana 'Emerald Tide'",
        "Emerald Tide",
        "Alocasia Emerald Tide",
        "Moderate", 15, 85,
        "Deeply ruffled emerald-green leaves with a wavy, tide-like leaf margin. "
        "Unique texture among micholitziana cultivars. Corms: $10-20, Pups: $20-45, Plants: $40-85.",
    ),
    (
        "micholitziana 'Gigantea'",
        "Giant Green Velvet",
        "Alocasia Micholitziana Gigantea",
        "Moderate", 18, 100,
        "Oversized form of Green Velvet — leaves can reach 3 ft on mature plants. "
        "Corms: $12-26, Pups: $26-55, Plants: $48-100.",
    ),
    (
        "'Pink Dragon'",
        "Pink Dragon",
        "Alocasia Pink Dragon",
        "Moderate", 12, 70,
        "Pale pink petioles mottled with silver and green. Eye-catching color; medium "
        "humidity needs (50%+). Corms: $8-16, Pups: $16-36, Plants: $32-70.",
    ),
    (
        "'Jacklyn'",
        "Jacklyn",
        "Alocasia Jacklyn",
        "Moderate", 12, 75,
        "Deeply lobed multi-tone leaves with striped petioles and fine hair texture. "
        "Trending variety; strong seller. Corms: $8-18, Pups: $18-40, Plants: $34-75.",
    ),
    (
        "'Morocco'",
        "Morocco",
        "Alocasia Morocco",
        "Moderate", 12, 65,
        "Deeply ridged and quilted dark-green leaves with prominent veining. Slower "
        "grower but very striking. Corms: $8-16, Pups: $16-34, Plants: $30-65.",
    ),
    (
        "scalprum",
        "Dagger",
        "Alocasia Scalprum",
        "Moderate", 15, 90,
        "Thick, leathery, blade-like leaves with wavy edges (scalprum = knife/scalpel). "
        "Unusual narrow form; collector favourite from Borneo. "
        "Corms: $10-22, Pups: $22-48, Plants: $42-90.",
    ),
    (
        "'Maharani'",
        "Grey Dragon",
        "Alocasia Maharani",
        "Moderate", 18, 110,
        "Thick waxy grey-green textured leaves; slow-growing but extremely structural. "
        "Also called 'Grey Dragon'. Corms: $12-28, Pups: $28-60, Plants: $52-110.",
    ),
    (
        "sanderiana",
        "Kris Plant",
        "Alocasia Sanderiana",
        "Moderate", 15, 100,
        "Narrow deeply-lobed dark metallic-green leaves with bright white veins. Philippine "
        "native and parent of the Amazonica hybrids. Needs moderate humidity (55%+). "
        "Corms: $10-22, Pups: $22-50, Plants: $45-100.",
    ),
    (
        "lowii",
        "Lowii",
        "Alocasia Lowii",
        "Moderate", 12, 70,
        "Glossy dark-green leaves with striking silvery undersides. Compact and "
        "manageable; rewarding grower. Corms: $8-18, Pups: $18-36, Plants: $32-70.",
    ),
    (
        "'Dark Star'",
        "Dark Star",
        "Alocasia Dark Star",
        "Moderate", 12, 70,
        "Near-black leaves with subtle silver veining. Increasingly popular collector "
        "variety. Corms: $8-18, Pups: $18-36, Plants: $32-70.",
    ),
    # (standalone 'California' entry removed — use odora 'California' below)
    (
        "'Sumo'",
        "Sumo",
        "Alocasia Sumo",
        "Moderate", 12, 65,
        "Broad, thick, deeply wrinkled leaves. Compact habit; dramatic texture. "
        "Corms: $8-16, Pups: $16-34, Plants: $30-65.",
    ),
    (
        "reversa",
        "Reversa",
        "Alocasia Reversa",
        "Moderate", 10, 60,
        "Thick oval leaves; undersides are more silvery-green than the tops. "
        "Corms: $6-14, Pups: $14-28, Plants: $24-60.",
    ),
    (
        "'Ninja'",
        "Ninja",
        "Alocasia Ninja",
        "Moderate", 12, 70,
        "Very dark, almost black glossy leaves. A striking alternative to Black Velvet "
        "for growers who want less fuss. Corms: $8-16, Pups: $16-36, Plants: $30-70.",
    ),
    (
        "'Hilo Beauty'",
        "Hilo Beauty",
        "Alocasia Hilo Beauty",
        "Moderate", 10, 60,
        "Mottled green-and-cream variegation on rounded leaves. Vigorous and more "
        "forgiving than most variegated forms. Corms: $6-14, Pups: $14-30, Plants: $26-60.",
    ),
    # ('Tiny Dancer' removed — merged into 'Tiny Dancers' which is the correct Aroidpedia name)
    (
        "'Tiny Dancers'",
        "Tiny Dancers",
        "Alocasia Tiny Dancers",
        "Moderate", 10, 50,
        "Unique cup-shaped leaves on slim upright stems. Very popular novelty variety; "
        "susceptible to overwatering — needs fast-draining aroid mix. "
        "Corms: $6-14, Pups: $14-28, Plants: $24-50.",
    ),
    (
        "clypeolata",
        "Green Shield",
        "Alocasia Clypeolata",
        "Moderate", 12, 65,
        "Round shield-shaped glossy leaves (Latin: clypeolata = little shield). "
        "Philippine native; reliable moderate grower. Corms: $8-16, Pups: $16-34, Plants: $30-65.",
    ),
    (
        "brancifolia",
        "Cut-Leaf",
        "Alocasia Brancifolia",
        "Moderate", 15, 80,
        "Dramatic split and divided frond-like leaves that become increasingly "
        "dissected with age. Uncommon indoor plant from New Guinea. "
        "Corms: $10-22, Pups: $22-45, Plants: $38-80.",
    ),
    (
        "jacksoniana",
        "Jacksoniana",
        "Alocasia Jacksoniana",
        "Moderate", 12, 70,
        "Deeply lobed leaves with contrasting light veins on dark green. "
        "Collector favourite; less commonly available. Corms: $8-18, Pups: $18-36, Plants: $32-70.",
    ),
    (
        "'Corazon'",
        "Corazon",
        "Alocasia Corazon",
        "Moderate", 12, 65,
        "Heart-shaped leaves with deep veining and a velvety surface. Compact and "
        "well-suited to terrariums. Corms: $8-16, Pups: $16-34, Plants: $28-65.",
    ),
    (
        "heterophylla 'Dragon's Breath'",
        "Dragon's Breath",
        "Alocasia Dragon's Breath",
        "Moderate", 15, 85,
        "Bold arrowhead leaves with rich burgundy-red undersides and dark green tops. "
        "Corms: $10-22, Pups: $22-45, Plants: $40-85.",
    ),
    (
        "heterophylla 'Shattered Glass'",
        "Shattered Glass",
        "Alocasia Shattered Glass",
        "Moderate", 18, 100,
        "Highly variegated heterophylla with irregular white and green fragmentation "
        "on each leaf — no two leaves alike. "
        "Corms: $12-26, Pups: $26-55, Plants: $48-100.",
    ),
    (
        "epilithica",
        "Rock-Dweller",
        "Alocasia Epilithica",
        "Moderate", 18, 90,
        "Unusual lithophytic species that grows on rocky outcrops in the wild. "
        "Thick, leathery leaves; tolerates drier conditions than most. "
        "Corms: $12-24, Pups: $24-50, Plants: $42-90.",
    ),
    (
        "roseus",
        "Rosy",
        "Alocasia Roseus",
        "Moderate", 18, 95,
        "Notable for its pink-flushed petioles and pale leaf undersides. "
        "Increasingly popular in the collector trade. "
        "Corms: $12-25, Pups: $25-52, Plants: $44-95.",
    ),
    (
        "'Sabrina'",
        "Sabrina",
        "Alocasia Sabrina",
        "Moderate", 15, 80,
        "Compact cultivar with rounded, deeply veined leaves and a glossy finish. "
        "A newer introduction gaining popularity in the collector community. "
        "Corms: $10-22, Pups: $22-45, Plants: $38-80.",
    ),
    (
        "'Macan'",
        "Macan",
        "Alocasia Macan",
        "Moderate", 18, 100,
        "Macan means 'tiger' in Indonesian — bold striped or mottled patterning. "
        "Not yet fully described botanically. Corms: $12-26, Pups: $26-55, Plants: $48-100.",
    ),
    (
        "'Bogani'",
        "Bogani",
        "Alocasia Bogani",
        "Moderate", 18, 100,
        "Named after the Bogani Nani Wartabone National Park in Sulawesi. "
        "Dark, textured leaves; not yet fully described. "
        "Corms: $12-26, Pups: $26-55, Plants: $48-100.",
    ),
    (
        "'Crux'",
        "Crux",
        "Alocasia Crux",
        "Moderate", 20, 110,
        "Compact cultivar with cross-shaped veination pattern on thick textured leaves. "
        "Not yet fully described; popular with collectors. "
        "Corms: $14-28, Pups: $28-58, Plants: $52-110.",
    ),
    (
        "'Surigao del Norte'",
        "Surigao",
        "Alocasia Surigao del Norte",
        "Moderate", 20, 110,
        "Named after the Surigao del Norte province in the Philippines. "
        "Not yet formally described. Corms: $14-28, Pups: $28-58, Plants: $52-110.",
    ),
    (
        "'Samar'",
        "Samar",
        "Alocasia Samar",
        "Moderate", 18, 100,
        "Named after Samar Island in the Philippines. Striking lobed leaves; "
        "not yet formally described botanically. "
        "Corms: $12-26, Pups: $26-55, Plants: $48-100.",
    ),
    (
        "'Green Djhono'",
        "Green Djhono",
        "Alocasia Green Djhono",
        "Moderate", 20, 110,
        "Distinctive cultivar with rich green textured leaves and prominent ribbing. "
        "Not yet formally described; Indonesian collector variety. "
        "Corms: $14-28, Pups: $28-58, Plants: $52-110.",
    ),
    (
        "'Pawitra'",
        "Pawitra",
        "Alocasia Pawitra",
        "Moderate", 18, 100,
        "Named after Gunung Pawitra in East Java, Indonesia. Compact form with "
        "heavily textured dark leaves. Not yet formally described. "
        "Corms: $12-26, Pups: $26-55, Plants: $48-100.",
    ),
    (
        "'Rudus'",
        "Rudus",
        "Alocasia Rudus",
        "Moderate", 20, 110,
        "Rudus means 'rubble' in Latin, referencing the rough, uneven leaf texture. "
        "Collector plant; not yet formally described. "
        "Corms: $14-28, Pups: $28-58, Plants: $52-110.",
    ),
    (
        "'Sintang'",
        "Sintang",
        "Alocasia Sintang",
        "Moderate", 18, 100,
        "Named after Sintang Regency in Indonesian Borneo. Striking leaf form; "
        "not yet formally described botanically. "
        "Corms: $12-26, Pups: $26-55, Plants: $48-100.",
    ),
    (
        "'Dragon Tooth'",
        "Dragon Tooth",
        "Alocasia Dragon Tooth",
        "Moderate", 12, 70,
        "Long, narrow, serrated leaves resembling a dragon's tooth. Unusual and "
        "distinctive form; collector favourite. Corms: $8-18, Pups: $18-36, Plants: $32-70.",
    ),
    (
        "perakensis",
        "Perak Taro",
        "Alocasia Perakensis",
        "Moderate", 20, 120,
        "Montane species from the highlands of Perak, Malaysia. Thick, leathery leaves "
        "adapted to cooler highland conditions. Collector rarity. "
        "Corms: $14-30, Pups: $30-65, Plants: $55-120.",
    ),
    (
        "kerinciensis",
        "Kerinci Taro",
        "Alocasia Kerinciensis",
        "Moderate", 20, 120,
        "Rare montane species from the Kerinci highlands of Sumatra. Adapted to cool, "
        "misty growing conditions. Collector rarity. "
        "Corms: $14-30, Pups: $30-65, Plants: $55-120.",
    ),
    (
        "princeps",
        "Prince's",
        "Alocasia Princeps",
        "Moderate", 18, 100,
        "Compact species from the Philippines with thick, glossy leaves and a "
        "regal upright habit. Prefers well-drained substrate. "
        "Corms: $12-26, Pups: $26-55, Plants: $48-100.",
    ),
    (
        "lauterbachiana",
        "Purple Sword",
        "Alocasia Lauterbachiana",
        "Moderate", 10, 60,
        "Long narrow wavy-edged leaves with reddish undersides. Upright habit; "
        "prefers 55%+ humidity. Corms: $6-12, Pups: $12-28, Plants: $26-60.",
    ),

    # ════════════════════ DIFFICULT ═══════════════════════════════════════════

    (
        "princeps 'Purple Cloak'",
        "Purple Cloak",
        "Alocasia Purple Cloak",
        "Difficult", 20, 150,
        "Dark purple-backed leaves with a dramatic near-black upper surface. "
        "Rare Philippine native. Corms: $14-36, Pups: $36-80, Plants: $65-150.",
    ),
    (
        "baginda",
        "Baginda",
        "Alocasia Baginda",
        "Difficult", 15, 100,
        "Parent species of Dragon Scale and Silver Dragon. Small, robust herb from "
        "Eastern Kalimantan. The name means 'King' or 'Majesty' in Bahasa Indonesian. "
        "Corms: $10-24, Pups: $24-52, Plants: $45-100.",
    ),
    (
        "baginda 'Dragon Scale'",
        "Dragon Scale",
        "Alocasia Dragon Scale",
        "Difficult", 15, 140,
        "Emerald-green leaves with a pronounced dragon-scale bullate pattern and dark veins. "
        "Needs 65%+ humidity. Corms: $12-30, Pups: $30-65, Plants: $60-140.",
    ),
    (
        "baginda 'Silver Dragon'",
        "Silver Dragon",
        "Alocasia Silver Dragon",
        "Difficult", 12, 110,
        "Silver-grey textured leaves with deep green veins on a compact plant. "
        "Needs stable humidity (65%+). Corms: $10-24, Pups: $24-55, Plants: $48-110.",
    ),
    (
        "baginda 'Green Dragon'",
        "Green Dragon",
        "Alocasia Green Dragon",
        "Difficult", 12, 100,
        "Deep green form of the baginda cultivar group with characteristic "
        "scale-like bullate leaf texture. Needs consistent humidity. "
        "Corms: $10-22, Pups: $22-50, Plants: $44-100.",
    ),
    (
        "baginda 'Dragon Scale Variegata'",
        "Variegated Dragon Scale",
        "Alocasia Variegated Dragon Scale",
        "Difficult", 100, 700,
        "Rare mint or cream sectors on the iconic scale-texture leaves. "
        "Investment-grade collector specimen. Corms: $80-180, Pups: $180-450, Plants: $350-700.",
    ),
    (
        "reginula 'Black Velvet'",
        "Black Velvet",
        "Alocasia Black Velvet",
        "Difficult", 15, 150,
        "Velvety near-black leaves with bold silver veins; very compact jewel alocasia. "
        "Slow-growing — highly coveted. Corms: $12-30, Pups: $30-70, Plants: $60-150.",
    ),
    (
        "cuprea",
        "Copper Leaf",
        "Alocasia Cuprea",
        "Difficult", 12, 120,
        "Thick, leathery copper-tinted leaves with a breastplate-like texture. "
        "Native to limestone karst terrain in Borneo. Parent of 'Red Secret'. "
        "Corms: $10-25, Pups: $25-58, Plants: $50-120.",
    ),
    (
        "cuprea 'Red Secret'",
        "Red Secret",
        "Alocasia Red Secret",
        "Difficult", 15, 150,
        "Metallic copper-red sheen on thick waxy leaves. One of the most visually "
        "striking Alocasias; needs 65%+ humidity. Corms: $12-30, Pups: $30-70, Plants: $60-150.",
    ),
    (
        "nebula 'Imperialis'",
        "Imperialis",
        "Alocasia Imperialis",
        "Difficult", 25, 250,
        "Thick silvery-grey leaves with deep veins and a matte texture. Very rare and "
        "slow-growing jewel alocasia. Corms: $20-55, Pups: $55-120, Plants: $100-250.",
    ),
    (
        "nebula",
        "Nebula",
        "Alocasia Nebula",
        "Difficult", 20, 180,
        "Parent of 'Imperialis' — similar silver-grey matte leaf texture but slightly "
        "less extreme. Very rare collector species from Borneo. "
        "Corms: $16-40, Pups: $40-95, Plants: $80-180.",
    ),
    (
        "melo",
        "Melo",
        "Alocasia Melo",
        "Difficult", 20, 200,
        "Extraordinarily textured cement-grey leaves with deep ridging — like a melon skin. "
        "Restricted to ultramafic substrates in Borneo. Extremely rare. "
        "Corms: $16-45, Pups: $45-100, Plants: $80-200.",
    ),
    (
        "azlanii",
        "Rainbow",
        "Alocasia Azlanii",
        "Difficult", 22, 200,
        "Iridescent blue-purple leaves with red veining. Extremely popular Malaysian "
        "native; limited supply drives premium prices. Corms: $18-50, Pups: $50-110, Plants: $88-200.",
    ),
    (
        "'Platinum'",
        "Platinum",
        "Alocasia Platinum",
        "Difficult", 15, 130,
        "Blue-green metallic leaves with waxy texture. Notably resistant to spider mites. "
        "Corms: $10-28, Pups: $28-60, Plants: $55-130.",
    ),
    (
        "platyphylla",
        "Flat-Leaved Taro",
        "Alocasia Platyphylla",
        "Difficult", 20, 160,
        "Huge rounded leaves with bold contrasting veination. Rare outside specialist "
        "collections. Corms: $14-38, Pups: $38-80, Plants: $70-160.",
    ),
    (
        "micholitziana 'Frydek Variegata'",
        "Variegated Green Velvet",
        "Alocasia Frydek Variegata",
        "Difficult", 80, 600,
        "Each leaf uniquely marbled with white or cream. Premium collector plant; "
        "extremely limited availability. Corms: $60-140, Pups: $140-350, Plants: $280-600.",
    ),
    (
        "bisma",
        "Bisma",
        "Alocasia Bisma",
        "Difficult", 18, 160,
        "Narrow, elongated leaves with bold silver veining on dark green. Rare Indonesian "
        "native. Corms: $12-35, Pups: $35-80, Plants: $65-160.",
    ),
    (
        "sinuata",
        "Quilted Hearts",
        "Alocasia Sinuata",
        "Difficult", 18, 150,
        "Compact jewel alocasia with deeply quilted, bullate leaves and prominent white "
        "veins on dark green. Needs stable high humidity (65%+). "
        "Corms: $12-32, Pups: $32-75, Plants: $60-150.",
    ),
    (
        "puber",
        "Swamp Taro",
        "Alocasia Puber",
        "Difficult", 20, 130,
        "Naturally inhabits swampy, waterlogged sites. Requires consistently moist "
        "substrate; unusual growing requirements. "
        "Corms: $14-30, Pups: $30-68, Plants: $58-130.",
    ),

    # ══════════════ HYBRIDS — from Aroidpedia Hybrids page ════════════════════
    # A–B

    ("'Albatuwan'", "Albatuwan", "Alocasia Albatuwan",
     "Moderate", 12, 60,
     "Indonesian hybrid with compact arrowhead leaves and pale vein patterning."),
    ("'Alexandra Regina'", "Alexandra Regina", "Alocasia Alexandra Regina",
     "Moderate", 14, 70,
     "Elegant elongated leaves with prominent white veins on dark green. Named after the plant breeder."),
    ("'Andromeda'", "Andromeda", "Alocasia Andromeda",
     "Moderate", 12, 60,
     "Compact hybrid with bold dark-green leaves and contrasting pale veination."),
    ("'Antasena'", "Antasena", "Alocasia Antasena",
     "Moderate", 14, 65,
     "Named after the Javanese mythological hero. Bold lobed leaves; Indonesian collector hybrid."),
    ("'Argyrea'", "Argyrea", "Alocasia Argyrea",
     "Moderate", 12, 60,
     "Argyrea means 'silvery' — leaves show a pronounced silver sheen over dark green."),
    ("'Aurora'", "Aurora", "Alocasia Aurora",
     "Moderate", 12, 55,
     "Light-toned hybrid with glowing, pale-veined leaves. Subtle and elegant."),
    ("'Bachii'", "Bachii", "Alocasia Bachii",
     "Moderate", 12, 55,
     "Compact hybrid with deeply veined leaves. Reliable moderate grower."),
    ("'Ballon Heart'", "Ballon Heart", "Alocasia Ballon Heart",
     "Moderate", 10, 50,
     "Rounded, heart-shaped leaves with a slightly inflated appearance. Compact grower."),
    ("'Bambino Arrow'", "Bambino Arrow", "Alocasia Bambino Arrow",
     "Easy", 8, 40,
     "Dwarf Amazonica relative with distinctly arrow-shaped leaves. Compact and very popular."),
    ("'Bimasena'", "Bimasena", "Alocasia Bimasena",
     "Moderate", 14, 65,
     "Named after the powerful Javanese warrior-hero Bima. Bold, dramatic foliage; Indonesian hybrid."),
    ("'Black Cobra'", "Black Cobra", "Alocasia Black Cobra",
     "Moderate", 14, 75,
     "Near-black glossy leaves on arching petioles that curve like a cobra's raised hood. "
     "Very popular dark hybrid. Corms: $8-20, Pups: $20-45, Plants: $38-75."),
    ("'Black Dragon'", "Black Dragon", "Alocasia Black Dragon",
     "Moderate", 14, 75,
     "Deep, almost black glossy leaves with subtle dark veining. Bold and dramatic collector hybrid."),
    ("'Black Knight'", "Black Knight", "Alocasia Black Knight",
     "Moderate", 14, 70,
     "Near-black shiny leaves on upright stems. Compact and striking dark hybrid."),
    ("'Black Suhita'", "Black Suhita", "Alocasia Black Suhita",
     "Moderate", 14, 70,
     "Dark form of the Suhita hybrid line. Very deep green to near-black foliage."),
    ("'Black Tortoise'", "Black Tortoise", "Alocasia Black Tortoise",
     "Moderate", 14, 70,
     "Rounded, domed dark leaves resembling a tortoise shell. Compact and unusual form."),
    ("'Blue Blush Odora'", "Blue Blush Odora", "Alocasia Blue Blush Odora",
     "Easy", 10, 50,
     "Odora hybrid with a distinctive blue-grey blush on large paddle-shaped leaves."),
    ("'Brisbane Blue'", "Brisbane Blue", "Alocasia Brisbane Blue",
     "Easy", 10, 50,
     "Australian hybrid with pronounced blue-green tones on large upright leaves."),
    ("'Brisbane Tigress'", "Brisbane Tigress", "Alocasia Brisbane Tigress",
     "Easy", 10, 50,
     "Australian hybrid with tiger-like striped patterning on petioles or leaf surfaces."),
    ("'Brisbane Waves'", "Brisbane Waves", "Alocasia Brisbane Waves",
     "Easy", 10, 50,
     "Australian hybrid with distinctly wavy, ruffled leaf margins on large green leaves."),

    # C

    ("'Chantrieri'", "Chantrieri", "Alocasia Chantrieri",
     "Moderate", 10, 55,
     "Classic Victorian-era hybrid (A. lowii × A. sanderiana), first documented in the 1880s. "
     "Narrow, deeply veined dark leaves. One of the original ornamental Alocasia hybrids."),
    ("'Chelsonii'", "Chelsonii", "Alocasia Chelsonii",
     "Moderate", 10, 55,
     "Victorian-era hybrid with glossy dark-green leaves and white veins. "
     "A historical cultivar that remains popular with collectors."),
    ("'Conspicua'", "Conspicua", "Alocasia Conspicua",
     "Moderate", 12, 60,
     "Conspicua means 'conspicuous' — bold, eye-catching leaf patterning with strong vein contrast."),
    ("'Copper Latte'", "Copper Latte", "Alocasia Copper Latte",
     "Moderate", 14, 65,
     "Warm copper-brown and latte-toned foliage with a soft metallic sheen. Unique colouring."),
    ("'Corrugate Shield'", "Corrugate Shield", "Alocasia Corrugate Shield",
     "Moderate", 15, 70,
     "Corrugated, deeply ridged shield-shaped leaves with a pronounced textured surface."),

    # D

    ("'Dark Butterfly'", "Dark Butterfly", "Alocasia Dark Butterfly",
     "Moderate", 14, 65,
     "Dark leaves with a spread-wing butterfly-like form. Compact and dramatic."),
    ("'Dragon Claw'", "Dragon Claw", "Alocasia Dragon Claw",
     "Moderate", 14, 70,
     "Narrow, curved leaves with pointed tips resembling dragon claws. Unusual and striking."),
    ("'Dragon Moon'", "Dragon Moon", "Alocasia Dragon Moon",
     "Moderate", 14, 65,
     "Rounded dark leaves with a luminous quality reminiscent of moonlit dragon scales."),
    ("'Dragon Wings'", "Dragon Wings", "Alocasia Dragon Wings",
     "Easy", 12, 65,
     "Large, spreading leaves held horizontally like dragon wings. Fast-growing and bold. "
     "One of the larger hybrid forms."),

    # E–G

    ("'Ebony'", "Ebony", "Alocasia Ebony",
     "Moderate", 14, 70,
     "Exceptionally dark, near-black glossy leaves. One of the darkest Alocasia hybrids."),
    ("'Emerald Shield'", "Emerald Shield", "Alocasia Emerald Shield",
     "Moderate", 12, 60,
     "Bright emerald-green, shield-shaped leaves with a glossy surface."),
    ("'Faizah'", "Faizah", "Alocasia Faizah",
     "Moderate", 12, 60,
     "Indonesian hybrid with compact, well-formed leaves. Named for a person of significance."),
    ("'Frydek-Bullata'", "Frydek-Bullata", "Alocasia Frydek-Bullata",
     "Difficult", 18, 110,
     "Cross between the Frydek (micholitziana) line and a bullate-leafed species. "
     "Features the velvety Frydek texture with added surface depth."),
    ("'Gajahmada'", "Gajahmada", "Alocasia Gajahmada",
     "Moderate", 14, 65,
     "Named after Gajah Mada, the legendary 14th-century Javanese prime minister. "
     "Bold, commanding foliage — an Indonesian collector hybrid."),
    ("'Gaulainii'", "Gaulainii", "Alocasia Gaulainii",
     "Moderate", 12, 60,
     "Named hybrid with glossy, broadly arrowhead-shaped leaves."),
    ("'Giant Shield'", "Giant Shield", "Alocasia Giant Shield",
     "Easy", 12, 65,
     "Very large, broad shield-shaped leaves on tall upright stems. Impressive landscape plant."),
    ("'Giant Zebra'", "Giant Zebra", "Alocasia Giant Zebra",
     "Easy", 14, 70,
     "Large-scale zebra hybrid with bold striped petioles and oversized glossy leaves."),
    ("'Gibba'", "Gibba", "Alocasia Gibba",
     "Moderate", 12, 55,
     "Compact hybrid with distinctly domed or humped leaf surfaces (gibba = hump)."),
    ("'Golden Bone'", "Golden Bone", "Alocasia Golden Bone",
     "Moderate", 14, 65,
     "Cream-to-gold veining in a bone-like pattern on glossy dark leaves. Striking contrast."),
    ("'Gold Magnet'", "Gold Magnet", "Alocasia Gold Magnet",
     "Moderate", 12, 60,
     "Golden-toned foliage with yellow-green highlights. Eye-catching warm colouring."),
    ("'Great Humongous'", "Great Humongous", "Alocasia Great Humongous",
     "Easy", 14, 70,
     "One of the largest Alocasia hybrids — leaves grow to impressive proportions. "
     "Fast-growing statement plant for large spaces."),
    ("'Green Body'", "Green Body", "Alocasia Green Body",
     "Easy", 10, 50,
     "Lush, deeply saturated solid green hybrid. Vigorous and reliable grower."),
    ("'Green Pegasus'", "Green Pegasus", "Alocasia Green Pegasus",
     "Moderate", 12, 60,
     "Bright green hybrid with a somewhat winged, upswept leaf form."),
    ("'Green Unicorn'", "Green Unicorn", "Alocasia Green Unicorn",
     "Moderate", 12, 60,
     "Unusual hybrid with a distinctive, singular horn-like growth characteristic."),
    ("'Grim Reaper'", "Grim Reaper", "Alocasia Grim Reaper",
     "Moderate", 14, 70,
     "Dark, scythe-shaped narrow leaves on arching stems. Dramatic and collector-favourite."),

    # I–J

    ("'Imperial Dark'", "Imperial Dark", "Alocasia Imperial Dark",
     "Moderate", 14, 70,
     "Dark-toned member of the Imperial hybrid series. Large, commanding leaves with deep colouring."),
    ("'Imperial Giant'", "Imperial Giant", "Alocasia Imperial Giant",
     "Easy", 14, 75,
     "The largest member of the Imperial series — impressive scale and bold green leaves."),
    ("'Imperial Knight'", "Imperial Knight", "Alocasia Imperial Knight",
     "Moderate", 14, 70,
     "Imperial series hybrid with dark, knightly-deep foliage and a commanding presence."),
    ("'Imperial Red'", "Imperial Red", "Alocasia Imperial Red",
     "Moderate", 15, 75,
     "Imperial hybrid with red-toned stems and leaf undersides. Bold colour contrast."),
    ("'Java Miracle'", "Java Miracle", "Alocasia Java Miracle",
     "Moderate", 12, 60,
     "Javanese hybrid celebrated for its unusual leaf form and robust growth habit."),
    ("'Jean Merkel'", "Jean Merkel", "Alocasia Jean Merkel",
     "Moderate", 12, 60,
     "Amazonica descendant with bold white veins on dark lobed leaves. "
     "Named after Jean Merkel, an early American Alocasia enthusiast."),

    # K–L

    ("'Kalila'", "Kalila", "Alocasia Kalila",
     "Moderate", 12, 60,
     "Compact hybrid with attractive dark leaves and white vein patterning."),
    ("'Katya'", "Katya", "Alocasia Katya",
     "Moderate", 12, 55,
     "Compact, well-formed hybrid with glossy dark-green leaves."),
    ("'Kencana'", "Kencana", "Alocasia Kencana",
     "Moderate", 14, 65,
     "Kencana means 'gold' or 'treasure' in Javanese. Golden-accented hybrid "
     "with warm-toned foliage."),
    ("'Kerchoveana'", "Kerchoveana", "Alocasia Kerchoveana",
     "Moderate", 10, 55,
     "Classic Victorian-era hybrid named after Oswald de Kerchove de Denterghem. "
     "Glossy dark leaves with prominent pale veins. A historic collector cultivar."),
    ("'Kuching Mask'", "Kuching Mask", "Alocasia Kuching Mask",
     "Moderate", 14, 70,
     "From Kuching, Sarawak (Borneo). Bold mask-like leaf patterning with contrasting veins."),
    ("'Kutawatu'", "Kutawatu", "Alocasia Kutawatu",
     "Moderate", 14, 65,
     "Indonesian hybrid. Kutawatu references a place in Java. Attractive lobed foliage."),
    ("'Licosta'", "Licosta", "Alocasia Licosta",
     "Moderate", 12, 60,
     "Compact hybrid with well-defined vein patterning on dark-green leaves."),
    ("'Loco'", "Loco", "Alocasia Loco",
     "Moderate", 12, 55,
     "Unpredictable, energetic grower with unusual leaf form. Lives up to its name."),
    ("'Louisville'", "Louisville", "Alocasia Louisville",
     "Moderate", 10, 55,
     "Named after Louisville, Kentucky. Compact hybrid originating from American collections."),
    ("'Low Rider'", "Low Rider", "Alocasia Low Rider",
     "Easy", 10, 50,
     "Compact, low-growing hybrid that stays close to the ground. Great for shelves and tables."),
    ("'Luciani'", "Luciani", "Alocasia Luciani",
     "Moderate", 12, 60,
     "Named hybrid with attractive arrowhead leaves and good vein definition."),
    ("'Lukiwan'", "Lukiwan", "Alocasia Lukiwan",
     "Moderate", 12, 60,
     "Indonesian hybrid with compact form and bold leaf patterning."),

    # M

    ("'Maanfah'", "Maanfah", "Alocasia Maanfah",
     "Moderate", 14, 65,
     "Thai hybrid — Maanfah means 'sky' or 'heaven' in Thai. Elegant, upward-reaching leaves."),
    ("'Maharani Moonlight'", "Maharani Moonlight", "Alocasia Maharani Moonlight",
     "Moderate", 18, 110,
     "Lighter, silver-toned variant of the Maharani line. Pale grey-green textured "
     "leaves with a moonlit sheen. Corms: $12-28, Pups: $28-60, Plants: $52-110."),
    ("'Mandalay'", "Mandalay", "Alocasia Mandalay",
     "Moderate", 12, 60,
     "Named after Mandalay, Myanmar. Compact hybrid with glossy dark leaves."),
    ("'Mandala'", "Mandala", "Alocasia Mandala",
     "Moderate", 12, 60,
     "Intricate mandala-like vein patterning radiating from the midrib on broad leaves."),
    ("'Manta Ray'", "Manta Ray", "Alocasia Manta Ray",
     "Moderate", 14, 65,
     "Wide, flat leaves spread horizontally like manta ray wings. Dramatic in silhouette."),
    ("'Mark Campbell'", "Mark Campbell", "Alocasia Mark Campbell",
     "Moderate", 12, 60,
     "Named after plant collector and enthusiast Mark Campbell. Bold arrowhead hybrid."),
    ("'Maroon Shield'", "Maroon Shield", "Alocasia Maroon Shield",
     "Moderate", 14, 65,
     "Deep maroon-toned shield-shaped leaves. Rich colour intensity increases in bright light."),
    ("'Martin Cahuzac'", "Martin Cahuzac", "Alocasia Martin Cahuzac",
     "Moderate", 12, 60,
     "Named after French botanist Martin Cahuzac. Victorian-era or early-modern hybrid."),
    ("'Mayan Mask'", "Mayan Mask", "Alocasia Mayan Mask",
     "Moderate", 14, 65,
     "Leaf patterning resembles the decorative masks of Mesoamerican cultures. "
     "Bold, geometric vein arrangement."),
    ("'Metalhead'", "Metalhead", "Alocasia Metalhead",
     "Moderate", 15, 75,
     "Strong metallic sheen across the leaf surface. Silver and copper tones "
     "that intensify in certain light conditions."),
    ("'Microdora'", "Microdora", "Alocasia Microdora",
     "Moderate", 10, 50,
     "Miniature odora hybrid. Compact version of the night-scented lily with smaller leaves."),
    ("'Mindanao'", "Mindanao", "Alocasia Mindanao",
     "Moderate", 12, 60,
     "Named after Mindanao Island in the Philippines. Robust hybrid with bold leaf form."),
    ("'Moresby'", "Moresby", "Alocasia Moresby",
     "Easy", 10, 55,
     "Named after Port Moresby, Papua New Guinea. Large, vigorous tropical hybrid."),
    ("'Mortefontanensis'", "Mortefontanensis", "Alocasia Mortefontanensis",
     "Moderate", 10, 55,
     "Named after the Mortefontaine estate gardens in France where it was first cultivated. "
     "Classic Victorian hybrid with glossy dark leaves and white veins."),

    # N–O

    ("'Nadoon'", "Nadoon", "Alocasia Nadoon",
     "Moderate", 12, 60,
     "Thai hybrid name. Compact form with attractive vein patterning."),
    ("'Nairobi Nights'", "Nairobi Nights", "Alocasia Nairobi Nights",
     "Moderate", 14, 70,
     "Dark, dramatic hybrid — deep colours evoke the night sky over Nairobi."),
    ("'Neo Moon'", "Neo Moon", "Alocasia Neo Moon",
     "Moderate", 14, 65,
     "Rounded, lunar-inspired leaves with a glowing pale quality in indirect light."),
    ("'Nile High'", "Nile High", "Alocasia Nile High",
     "Easy", 12, 65,
     "Tall, upright hybrid inspired by the Nile River. Bold, large leaves on tall stems."),
    ("'Nyctedora'", "Nyctedora", "Alocasia Nyctedora",
     "Easy", 10, 50,
     "Nocturnal odora hybrid (nycto = night) — fragrant night-blooming flowers. "
     "Large paddle leaves; very forgiving grower."),
    ("'Orchid Jungle'", "Orchid Jungle", "Alocasia Orchid Jungle",
     "Moderate", 12, 60,
     "Lush tropical hybrid with layered, jungle-like leaf arrangements."),
    ("'Overra'", "Overra", "Alocasia Overra",
     "Moderate", 12, 60,
     "Hybrid with attractive broad arrowhead leaves and good constitution."),
    ("'Oviek 2'", "Oviek 2", "Alocasia Oviek 2",
     "Moderate", 14, 65,
     "Second in the Oviek Indonesian hybrid series. Compact with bold leaf form."),
    ("'Oviek 3'", "Oviek 3", "Alocasia Oviek 3",
     "Moderate", 14, 65,
     "Third in the Oviek Indonesian hybrid series. Slightly larger than Oviek 2."),

    # P

    ("'Paul Fernandez'", "Paul Fernandez", "Alocasia Paul Fernandez",
     "Moderate", 12, 60,
     "Named hybrid with bold arrowhead leaves and strong vein contrast."),
    ("'Pink Otea'", "Pink Otea", "Alocasia Pink Otea",
     "Moderate", 14, 65,
     "Pink-stemmed form of the Otea hybrid line. Warm pink petioles contrast with dark-green leaves."),
    ("'Pixie\\'s Teardrops'", "Pixie's Teardrops", "Alocasia Pixie's Teardrops",
     "Moderate", 12, 60,
     "Delicate teardrop-shaped small leaves on slender stems. Compact, whimsical form."),
    ("'Platinum Star'", "Platinum Star", "Alocasia Platinum Star",
     "Difficult", 18, 120,
     "Platinum-silver leaf surfaces with a star-like spreading form. Metallic and highly ornamental."),
    ("'Pucciana'", "Pucciana", "Alocasia Pucciana",
     "Moderate", 12, 60,
     "Named hybrid with glossy, well-formed arrowhead leaves."),
    ("'Purple Dragon'", "Purple Dragon", "Alocasia Purple Dragon",
     "Moderate", 14, 70,
     "Rich purple undertones on dark dragon-like leaves. Petioles often show deep purple colouring."),
    ("'Purpley'", "Purpley", "Alocasia Purpley",
     "Moderate", 12, 60,
     "Amazonica descendant with a distinct purple flush on the leaf undersides and petioles. "
     "Compact and popular."),

    # R

    ("'Raven'", "Raven", "Alocasia Raven",
     "Moderate", 14, 70,
     "Exceptionally dark near-black leaves with a satin sheen. Named for the jet-black bird."),
    ("'Reticulate Giant'", "Reticulate Giant", "Alocasia Reticulate Giant",
     "Easy", 14, 70,
     "Large hybrid with pronounced reticulate (net-like) vein patterning across broad leaves."),
    ("'Reversil'", "Reversil", "Alocasia Reversil",
     "Moderate", 12, 60,
     "The silvery underside is the dominant visual feature — a reversal of the typical "
     "dark-top, pale-bottom pattern."),
    ("'Ripple Effect'", "Ripple Effect", "Alocasia Ripple Effect",
     "Moderate", 14, 65,
     "Strongly ruffled and rippling leaf margins create a wave-like visual effect."),
    ("'Robudora'", "Robudora", "Alocasia Robudora",
     "Easy", 10, 55,
     "Robust odora hybrid. Large paddle-shaped leaves; very forgiving and fast-growing."),
    ("'Rodan'", "Rodan", "Alocasia Rodan",
     "Easy", 12, 65,
     "Named after the giant flying kaiju — this large hybrid lives up to the name "
     "with impressively sized leaves."),
    ("'Rodigasiana'", "Rodigasiana", "Alocasia Rodigasiana",
     "Moderate", 10, 55,
     "Named after Belgian botanist Édouard Rodigas. Victorian-era hybrid with "
     "elegant dark arrowhead leaves."),
    ("'Royal Sarawak'", "Royal Sarawak", "Alocasia Royal Sarawak",
     "Moderate", 15, 75,
     "From Sarawak, Malaysian Borneo. Regal appearance with large, richly coloured leaves."),

    # S

    ("'Sanderidora'", "Sanderidora", "Alocasia Sanderidora",
     "Moderate", 12, 65,
     "Cross between sanderiana and odora lines. Combines the Kris Plant's dramatic lobing "
     "with the odora's vigour."),
    ("'Saridora'", "Saridora", "Alocasia Saridora",
     "Moderate", 12, 60,
     "Cross hybrid with bold leaf form combining characteristics of its parent species."),
    ("'Sedenii'", "Sedenii", "Alocasia Sedenii",
     "Moderate", 10, 55,
     "Named after Victorian hybridizer J.G. Seden. Classic 19th-century hybrid with "
     "elegant dark-green, white-veined leaves."),
    ("'Serengeti'", "Serengeti", "Alocasia Serengeti",
     "Easy", 12, 60,
     "Robust, vigorous hybrid named after the African savanna. Large, bold leaves; "
     "reliable grower."),
    ("'Silver Armor'", "Silver Armor", "Alocasia Silver Armor",
     "Moderate", 15, 80,
     "Heavy silver overlay across dark leaf surfaces — like armour plating. "
     "Very ornamental. Corms: $10-22, Pups: $22-48, Plants: $42-80."),
    ("'Silver Arrow'", "Silver Arrow", "Alocasia Silver Arrow",
     "Moderate", 14, 70,
     "Narrow, arrow-shaped leaves with a dominant silver midrib and vein structure."),
    ("'Silver King'", "Silver King", "Alocasia Silver King",
     "Moderate", 15, 80,
     "Predominantly silver foliage with a commanding presence. Large and ornamental."),
    ("'Silver Monarch'", "Silver Monarch", "Alocasia Silver Monarch",
     "Moderate", 15, 80,
     "Large hybrid with dominant silver tones across broad, regal leaves."),
    ("'Silver Streak'", "Silver Streak", "Alocasia Silver Streak",
     "Moderate", 12, 65,
     "Dramatic silver streak runs along the midrib against dark green leaf surfaces."),
    ("'Simba Blue'", "Simba Blue", "Alocasia Simba Blue",
     "Moderate", 14, 65,
     "Blue-toned member of the Simba hybrid line. Cool blue-green colouring with bold leaves."),
    ("'Simpo'", "Simpo", "Alocasia Simpo",
     "Moderate", 10, 50,
     "Compact, sim-sized hybrid. Easy to manage in smaller spaces."),
    ("'Sinuate Mac'", "Sinuate Mac", "Alocasia Sinuate Mac",
     "Moderate", 14, 65,
     "Sinuate (wavy-edged) leaves in the Mac hybrid series. Attractive undulating margins."),
    ("'Splendida'", "Splendida", "Alocasia Splendida",
     "Moderate", 12, 60,
     "Splendida means 'splendid' — showy, eye-catching hybrid with bold patterned leaves."),
    ("'Subodora'", "Subodora", "Alocasia Subodora",
     "Easy", 8, 45,
     "Sub-odora hybrid with a gentler fragrance and slightly smaller stature than the full odora."),
    ("'Suhita'", "Suhita", "Alocasia Suhita",
     "Moderate", 14, 65,
     "Named after the historical Javanese queen Tribhuwana Wijayatunggadewi, also called Suhita. "
     "Bold Indonesian hybrid."),

    # T–Z

    ("'Thunder Waves'", "Thunder Waves", "Alocasia Thunder Waves",
     "Moderate", 14, 65,
     "Bold, dramatically wavy leaf margins with strong structural presence."),
    ("'Tiny Dancers'", "Tiny Dancers", "Alocasia Tiny Dancers",
     "Moderate", 10, 50,
     "Delicate cup-shaped leaves on slim upright stems. Small, whimsical, and popular."),
    ("'Titan'", "Titan", "Alocasia Titan",
     "Easy", 14, 75,
     "One of the largest Alocasia hybrids — truly titan-sized leaves on tall stems. "
     "Bold landscape statement."),
    ("'Tyaga'", "Tyaga", "Alocasia Tyaga",
     "Moderate", 14, 65,
     "Indonesian hybrid. Tyaga means 'sacrifice' or 'devotion' in Sanskrit — "
     "a name fitting for a dedicated collector plant."),
    ("'Tyrion'", "Tyrion", "Alocasia Tyrion",
     "Moderate", 12, 60,
     "Compact, stout hybrid that punches above its size. Dense, robust foliage."),
    ("'Uhinkii'", "Uhinkii", "Alocasia Uhinkii",
     "Moderate", 14, 65,
     "Javanese or Balinese hybrid with compact, attractively patterned foliage."),
    ("'Ulla'", "Ulla", "Alocasia Ulla",
     "Moderate", 10, 55,
     "Compact, manageable hybrid with clean, well-defined leaf form."),
    ("'V-Storm'", "V-Storm", "Alocasia V-Storm",
     "Moderate", 14, 65,
     "V-shaped dramatic leaves angled like a storm front. Dynamic, energetic growth habit."),
    ("'Vangigo'", "Vangigo", "Alocasia Vangigo",
     "Moderate", 14, 65,
     "Van Gogh-inspired name — swirling, dynamic leaf texture and colouring."),
    ("'Venom'", "Venom", "Alocasia Venom",
     "Moderate", 12, 65,
     "Amazonica descendant with very dark, near-black glossy leaves and bold white veins. "
     "Compact and striking. Corms: $8-18, Pups: $18-38, Plants: $30-65."),
    ("'Verta'", "Verta", "Alocasia Verta",
     "Moderate", 12, 60,
     "Compact hybrid with attractive, vertically oriented leaf form."),
    ("'Victory'", "Victory", "Alocasia Victory",
     "Moderate", 12, 60,
     "Bold, triumphant-looking hybrid with large, well-formed leaves and strong presence."),
    ("'Violet Blade'", "Violet Blade", "Alocasia Violet Blade",
     "Moderate", 14, 65,
     "Narrow, blade-shaped leaves with violet to purple undertones. Elegant and unusual."),
    ("'Wanda'", "Wanda", "Alocasia Wanda",
     "Moderate", 10, 55,
     "Classic, reliable hybrid with glossy dark-green leaves. "
     "Well-established in cultivation."),
    ("'Watson\\'s Giant'", "Watson's Giant", "Alocasia Watson's Giant",
     "Easy", 14, 70,
     "Large hybrid named after Watson. Impressive scale with bold, spreading leaves."),
    ("'White Dragon'", "White Dragon", "Alocasia White Dragon",
     "Moderate", 14, 70,
     "Striking white-to-cream vein pattern on dark leaves — the inverse of the typical "
     "dark-on-dark pattern."),
    ("'White Walker'", "White Walker", "Alocasia White Walker",
     "Moderate", 14, 70,
     "Pale, almost ghostly silver-white leaf tones. One of the lightest-coloured hybrids."),
    ("'Wyvern Moon'", "Wyvern Moon", "Alocasia Wyvern Moon",
     "Moderate", 15, 75,
     "Mythical dragon (wyvern) inspired hybrid with lunar silver tones on dramatic leaves."),
    ("'Yusuf 1'", "Yusuf 1", "Alocasia Yusuf 1",
     "Moderate", 14, 65,
     "Indonesian collector hybrid, first in the Yusuf series. Compact with distinctive leaf form."),
    ("'Zulu Mask'", "Zulu Mask", "Alocasia Zulu Mask",
     "Moderate", 14, 65,
     "Named for the decorative masks of Zulu culture. Bold, mask-like leaf patterning."),

    # ══ SPECIES & CULTIVARS — from Aroidpedia Species & Cultivars page ════════
    # A

    ("acuminata", "Acuminata", "Alocasia Acuminata",
     "Moderate", 10, 55,
     "Compact species with pointed (acuminate) arrowhead leaves. "
     "Native to Southeast Asia; grows well in shaded, humid conditions."),
    ("aequiloba", "Aequiloba", "Alocasia Aequiloba",
     "Moderate", 12, 60,
     "Equal-lobed leaves (aequiloba = equal lobes). Philippine native with "
     "symmetrical, well-balanced leaf form."),
    ("aequiloba 'Gold Dust'", "Gold Dust", "Alocasia Gold Dust",
     "Moderate", 14, 70,
     "Gold-speckled cultivar of aequiloba. Yellow flecks across dark-green leaves "
     "give a gold-dusted appearance."),
    ("alba", "White Taro", "Alocasia Alba",
     "Moderate", 10, 55,
     "Alba means 'white' — notable for pale leaf coloring or white-marked stems. "
     "Compact and manageable Southeast Asian species."),
    ("alba 'Silver'", "Silver Alba", "Alocasia Alba Silver",
     "Moderate", 12, 60,
     "Silver-toned form of alba with enhanced metallic sheen across the leaf surfaces."),
    ("ampunganensis", "Ampungan Taro", "Alocasia Ampunganensis",
     "Moderate", 15, 75,
     "From the Ampungan region of Sumatra, Indonesia. Relatively rare collector species."),
    ("arifolia", "Arum-Leaf", "Alocasia Arifolia",
     "Moderate", 10, 55,
     "Arum-shaped (arifolia = arum-leaved) compact leaves. Reliable Southeast Asian species."),
    ("atropurpurea", "Dark Purple", "Alocasia Atropurpurea",
     "Moderate", 14, 70,
     "Atropurpurea means 'dark purple' — deep purple-toned leaves and petioles. "
     "Bold colour that intensifies in bright indirect light."),

    # B

    ("balgooyi", "Balgooy's", "Alocasia Balgooyi",
     "Moderate", 15, 75,
     "Named after Dutch botanist M.M.J. van Balgooy. Compact Borneo native with "
     "distinctive thick leathery leaves."),
    ("becarii", "Beccari's", "Alocasia Becarii",
     "Moderate", 15, 75,
     "Named after Italian botanist Odoardo Beccari, who collected extensively in Borneo. "
     "Glossy arrowhead leaves with prominent veins."),
    ("boa", "Boa", "Alocasia Boa",
     "Easy", 12, 65,
     "Dramatically thick, snake-like petioles (named after the boa constrictor). "
     "Large tropical leaves on robust constricted stems."),
    ("boyceana", "Boyce's", "Alocasia Boyceana",
     "Moderate", 15, 75,
     "Named after Aroid specialist Peter Boyce. Distinctive species with uniquely "
     "shaped leaves; relatively rare in cultivation."),

    # C

    ("cadieri", "Cadiere's", "Alocasia Cadieri",
     "Moderate", 12, 60,
     "Named after Léopold Cadière, French missionary and naturalist in Vietnam. "
     "Vietnamese native with elegant arrowhead leaves."),
    ("celebica", "Sulawesi Taro", "Alocasia Celebica",
     "Moderate", 12, 60,
     "From Sulawesi (historically Celebes). Upright growing species with bold "
     "glossy leaves; reliable moderate grower."),
    ("chaii", "Chai's", "Alocasia Chaii",
     "Moderate", 14, 70,
     "Named after Malaysian botanist S.C. Chai. Compact Malaysian native with "
     "attractive patterned foliage."),
    ("cucullata 'Banana Split'", "Banana Split", "Alocasia Banana Split",
     "Easy", 8, 40,
     "Cucullata cultivar with cream-and-green variegation resembling banana coloring. "
     "Cheerful and compact; shares the easy care of the base species."),
    ("cucullata 'Crinkles'", "Crinkles", "Alocasia Crinkles",
     "Easy", 8, 40,
     "Cucullata cultivar with distinctly crinkled, ruffled leaf margins. "
     "Very compact and easy to grow."),
    ("cucullata 'Moon Landing'", "Moon Landing", "Alocasia Moon Landing",
     "Easy", 10, 45,
     "Cucullata cultivar with unusual silvery or pale-toned leaves suggesting a "
     "moonlit surface. Compact and reliable."),
    ("cucullata 'White Lace'", "White Lace", "Alocasia White Lace",
     "Easy", 10, 45,
     "Cucullata cultivar with delicate white edging or lace-like variegation on "
     "the leaf margins. Elegant and compact."),
    ("culionensis", "Culion", "Alocasia Culionensis",
     "Moderate", 14, 70,
     "From Culion Island in the Philippines. Compact Philippine endemic with "
     "attractive lobed leaves."),

    # D

    ("decipiens", "Deceptive", "Alocasia Decipiens",
     "Moderate", 12, 60,
     "Decipiens means 'deceptive' — resembles other species closely. "
     "Compact Southeast Asian native."),
    ("decumbens", "Decumbent", "Alocasia Decumbens",
     "Moderate", 12, 60,
     "Decumbens means lying down — grows with a prostrate or low-spreading habit "
     "rather than upright. Unusual growth form."),
    ("devansayana", "Devansayan", "Alocasia Devansayana",
     "Moderate", 14, 70,
     "Philippine or Indonesian species with well-defined lobed leaves. "
     "Named after a plant collector or botanist."),

    # E–F

    ("evrardii", "Evrard's", "Alocasia Evrardii",
     "Moderate", 12, 60,
     "Named after French botanist M. Evrard. Vietnamese native with compact "
     "arrowhead leaves."),
    ("fallax", "Fallax", "Alocasia Fallax",
     "Moderate", 12, 60,
     "Fallax means 'deceptive' or 'misleading' — resembles a different genus "
     "at first glance. Compact and unusual."),
    ("farisii", "Faris's", "Alocasia Farisii",
     "Moderate", 14, 70,
     "Named after Faris; Malaysian native with attractive glossy leaves."),
    ("flabellifera", "Fan", "Alocasia Flabellifera",
     "Moderate", 12, 60,
     "Flabellifera means 'fan-bearing' — leaves or leaf arrangement has a "
     "distinctive fan-like spread."),
    ("flemingiana", "Fleming's", "Alocasia Flemingiana",
     "Moderate", 12, 60,
     "Named after Fleming. Philippine native with compact, elegant leaf form."),
    ("fornicata", "Arched", "Alocasia Fornicata",
     "Easy", 10, 50,
     "Fornicata means 'arched' — petioles curve in a pronounced arch. "
     "Vigorous, easy-to-grow tropical species."),

    # G–H

    ("grata", "Grata", "Alocasia Grata",
     "Moderate", 12, 60,
     "Grata means 'pleasing' or 'grateful' — an attractive Southeast Asian species "
     "with glossy, well-formed leaves."),
    ("hainanica", "Hainan", "Alocasia Hainanica",
     "Moderate", 12, 60,
     "From Hainan Island, southern China. One of the few Chinese Alocasia species; "
     "handles slightly cooler temperatures than most."),
    ("hararganjensis", "Hararganj", "Alocasia Hararganjensis",
     "Moderate", 12, 60,
     "From the Hararganj region of South Asia. Compact species with broad "
     "arrowhead leaves."),
    ("heterophylla", "Variable-Leaf", "Alocasia Heterophylla",
     "Moderate", 12, 65,
     "Heterophylla means 'variable leaves' — different leaves on the same plant "
     "can look quite distinct. Parent of Dragon's Breath and Shattered Glass."),
    ("heterophylla 'Bahamut'", "Bahamut", "Alocasia Bahamut",
     "Moderate", 15, 80,
     "Named after the mythical dragon Bahamut. Large-form heterophylla cultivar "
     "with imposing, bold leaves."),
    ("heterophylla 'Green Veins'", "Green Veins", "Alocasia Green Veins",
     "Moderate", 12, 65,
     "Heterophylla cultivar with especially prominent, bright green vein patterning "
     "against dark leaf surfaces."),
    ("heterophylla 'Green'", "Solid Green", "Alocasia Heterophylla Green",
     "Moderate", 12, 60,
     "Solid green form of heterophylla without the burgundy undersides. "
     "Bold and vigorous."),
    ("heterophylla 'Silver Kris'", "Silver Kris", "Alocasia Silver Kris",
     "Moderate", 15, 75,
     "Named after the kris (Javanese ceremonial dagger). Silver-toned heterophylla "
     "cultivar with metallic leaf surfaces."),
    ("heterophylla 'Silver'", "Silver Heterophylla", "Alocasia Heterophylla Silver",
     "Moderate", 14, 70,
     "Silver-toned heterophylla cultivar with a pronounced metallic sheen across "
     "the leaf surfaces."),
    ("hollrungii", "Hollrung's", "Alocasia Hollrungii",
     "Moderate", 12, 60,
     "Named after German botanist M. Hollrung. New Guinea native with tropical, "
     "robust arrowhead leaves."),
    ("hypoleuca", "Pale-Backed", "Alocasia Hypoleuca",
     "Moderate", 12, 60,
     "Hypoleuca means 'pale below' — the leaf undersides are noticeably lighter or "
     "whitish compared to the dark upper surfaces."),
    ("hypoleuca 'Mahaphetra'", "Mahaphetra", "Alocasia Mahaphetra",
     "Moderate", 14, 70,
     "Cultivar of hypoleuca with distinctive features named 'Mahaphetra'. "
     "Enhanced pale-backed character with collector appeal."),

    # I–J

    ("indica", "Indian Taro", "Alocasia Indica",
     "Easy", 8, 45,
     "Large species from India and South Asia. Historically used as a food crop. "
     "Note: the name indica is disputed and may represent multiple species."),
    ("infernalis", "Black Magic", "Alocasia Infernalis",
     "Difficult", 20, 180,
     "Infernalis means 'infernal' — one of the darkest Alocasias in existence. "
     "Near-black velvet leaves on a compact jewel plant. Extremely collectible; "
     "needs 65%+ humidity. Corms: $15-45, Pups: $45-100, Plants: $85-180."),
    ("inornata", "Plain", "Alocasia Inornata",
     "Moderate", 10, 55,
     "Inornata means 'unadorned' — simple, elegant plain leaves without dramatic "
     "markings. Clean and architectural."),
    ("jiewhoei", "Jiewhoei's", "Alocasia Jiewhoei",
     "Difficult", 18, 120,
     "Named after J.W. Jiewhoei, a renowned Borneo plant collector. Compact "
     "jewel-type species with distinctive textured leaves. "
     "Corms: $12-30, Pups: $30-65, Plants: $55-120."),

    # L

    ("lancifolia", "Lance-Leaf Taro", "Alocasia Lancifolia",
     "Moderate", 10, 55,
     "Lancifolia means 'lance-shaped leaves' — long, narrow, pointed arrowhead "
     "leaves on tall upright stems. Elegant Philippine native."),
    ("lecomtei", "Lecomte's", "Alocasia Lecomtei",
     "Moderate", 12, 60,
     "Named after French botanist Henri F. Lecomte, who botanised in Indochina. "
     "Vietnamese native with well-formed arrowhead leaves."),
    ("lihengiae", "Li Heng's", "Alocasia Lihengiae",
     "Moderate", 14, 70,
     "Named after Chinese botanist Li Heng. One of the Chinese Alocasia species; "
     "relatively rare in cultivation."),

    # M

    ("maquilingensis", "Maquiling", "Alocasia Maquilingensis",
     "Moderate", 15, 75,
     "From Mount Maquiling, Laguna, Philippines — one of the most biodiverse "
     "areas in Southeast Asia. Compact Philippine endemic."),
    ("megawatiae", "Megawati's", "Alocasia Megawatiae",
     "Moderate", 15, 80,
     "Named after Indonesian President Megawati Sukarnoputri. Indonesian endemic "
     "with bold, commanding foliage — a regal species."),
    ("micholitziana 'Green Velvet'", "Green Velvet", "Alocasia Green Velvet",
     "Moderate", 12, 75,
     "The standard trade name for the deep-green velvety form of micholitziana. "
     "Deep-green leaves with glowing white veins; widely sold as 'Green Velvet' "
     "rather than 'Frydek'. Corms: $8-18, Pups: $18-40, Plants: $35-75."),
    ("minuscula", "Miniature", "Alocasia Minuscula",
     "Difficult", 18, 130,
     "Minuscula means 'very small' — one of the tiniest Alocasia species. "
     "Tiny jewel form; highly collectible and needs expert humid conditions. "
     "Corms: $12-30, Pups: $30-68, Plants: $58-130."),
    ("monticola", "Mountain", "Alocasia Monticola",
     "Moderate", 14, 70,
     "Monticola means 'mountain-dwelling' — grows at higher elevations. "
     "Handles slightly cooler conditions than lowland species."),

    # N

    ("navicularis", "Boat", "Alocasia Navicularis",
     "Difficult", 20, 150,
     "Navicularis means 'boat-shaped' — leaves fold into a distinct boat form. "
     "Unusual jewel species from Borneo. "
     "Corms: $14-36, Pups: $36-80, Plants: $65-150."),
    ("nicolsonii", "Nicolson's", "Alocasia Nicolsonii",
     "Moderate", 14, 70,
     "Named after botanist D.H. Nicolson, who contributed significantly to "
     "Araceae taxonomy. Southeast Asian native."),
    ("nycteris", "Bat-Ear", "Alocasia Nycteris",
     "Moderate", 15, 75,
     "Nycteris means 'bat' — the leaf shape resembles bat ears. "
     "Unusual and collectible compact species."),

    # O (odora cultivars)

    ("odora 'Blue'", "Blue Odora", "Alocasia Blue Odora",
     "Easy", 10, 50,
     "Odora cultivar with a distinctive blue-grey cast to the large paddle-shaped leaves. "
     "Retains the vigour and fragrant flowers of the base species."),
    ("odora 'California'", "California Odora", "Alocasia California",
     "Moderate", 10, 55,
     "Deeply lobed odora cultivar with olive-green leaves and prominent veins. "
     "Vigorous and easy to manage; developed in California."),
    ("odora 'Indian/Architecture'", "Indian Architecture Odora", "Alocasia Indian Architecture",
     "Easy", 10, 50,
     "Architectural odora cultivar with especially bold, upright structure. "
     "Well-suited to large interior spaces."),
    ("odora 'Okinawa Silver'", "Okinawa Silver", "Alocasia Okinawa Silver",
     "Easy", 12, 55,
     "Odora cultivar from Okinawa with silvery-grey leaf tones. "
     "Hardy and vigorous like the base species."),

    # P

    ("pangeran", "Prince", "Alocasia Pangeran",
     "Moderate", 14, 70,
     "Pangeran means 'prince' in Indonesian/Malay. Regal-looking compact species "
     "with bold foliage."),
    ("peltata", "Shield Taro", "Alocasia Peltata",
     "Moderate", 12, 65,
     "Peltata means 'shield-shaped' — leaves attach at or near the centre "
     "(peltate attachment) rather than at the base. Unusual and elegant."),
    ("peltata 'Silver Grey'", "Silver Grey", "Alocasia Silver Grey",
     "Moderate", 15, 75,
     "Peltata cultivar with silver-grey leaf tones. "
     "The peltate attachment combined with metallic colouring is striking."),
    ("perakensis 'Silver Giant'", "Silver Giant", "Alocasia Silver Giant",
     "Moderate", 18, 100,
     "Large cultivar of perakensis with pronounced silver-grey leaf tones. "
     "Combines the cool highland constitution of perakensis with impressive scale."),
    ("portei", "Porte's", "Alocasia Portei",
     "Easy", 12, 60,
     "Named after Porte. Large tropical species with deeply lobed, dramatic leaves. "
     "Fast-growing and bold."),
    ("princeps 'Candy Sticks'", "Candy Sticks", "Alocasia Candy Sticks",
     "Moderate", 15, 80,
     "Princeps cultivar with distinctive candy-striped petioles — alternating "
     "bands of light and dark on the stem. Unique and collectible."),
    ("principiculus", "Little Prince", "Alocasia Principiculus",
     "Moderate", 14, 70,
     "Principiculus means 'little prince' — compact species related to princeps. "
     "Smaller, more manageable form of the princeps type."),
    ("pseudosanderiana", "False Kris Plant", "Alocasia Pseudosanderiana",
     "Moderate", 15, 80,
     "Pseudo-sanderiana means 'false sanderiana' — resembles the Kris Plant "
     "closely but is a distinct species."),
    ("puncakborneensis", "Borneo Peak", "Alocasia Puncakborneensis",
     "Difficult", 20, 140,
     "From the mountain peaks (puncak) of Borneo. Montane species adapted to "
     "cool, misty conditions. Rare collector species."),
    ("puteri", "Princess", "Alocasia Puteri",
     "Moderate", 14, 70,
     "Puteri means 'princess' in Malay. Malaysian native with elegant, "
     "well-formed arrowhead leaves."),
    ("pyrospatha", "Fire-Spathe", "Alocasia Pyrospatha",
     "Moderate", 15, 75,
     "Pyrospatha means 'fire-spathe' — the inflorescence spathe has vivid "
     "red or orange tones. Ornamental both for leaves and blooms."),

    # R

    ("ramosii", "Ramos's", "Alocasia Ramosii",
     "Moderate", 14, 70,
     "Named after Filipino botanist Maximo Ramos. Philippine endemic with "
     "compact, well-defined lobed leaves."),
    ("reginae", "Queen", "Alocasia Reginae",
     "Difficult", 22, 200,
     "Reginae means 'of the queen' — one of the most spectacular jewel Alocasias. "
     "Velvety, deeply ribbed dark leaves with a regal bearing. "
     "From Sarawak, Borneo. Needs 65%+ humidity. "
     "Corms: $18-50, Pups: $50-110, Plants: $90-200."),
    ("reginae 'Elaine'", "Elaine", "Alocasia Reginae Elaine",
     "Difficult", 22, 180,
     "Named cultivar of reginae. Same spectacular velvety dark leaves with "
     "a slightly different form or leaf texture."),
    ("reginae 'Miri'", "Miri", "Alocasia Reginae Miri",
     "Difficult", 22, 180,
     "Named after Miri, Sarawak — the city near the reginae's natural habitat. "
     "Jewel collector cultivar with deeply ridged leaves."),
    ("reginula 'Black Ninja'", "Black Ninja", "Alocasia Black Ninja",
     "Difficult", 15, 150,
     "Very dark form of the reginula group, slightly more vigorous than Black Velvet. "
     "Near-black velvety leaves with bold silver veins. "
     "Corms: $12-30, Pups: $30-70, Plants: $60-150."),
    ("reginula 'Silver Velvet'", "Silver Velvet", "Alocasia Silver Velvet",
     "Difficult", 15, 150,
     "Silver-toned reginula cultivar — pale silver-grey velvety leaves with "
     "a moonlit appearance. Compact jewel alocasia. "
     "Corms: $12-30, Pups: $30-70, Plants: $60-150."),
    ("ridleyi", "Ridley's", "Alocasia Ridleyi",
     "Moderate", 14, 75,
     "Named after H.N. Ridley, first Director of Singapore Botanic Gardens "
     "and Rubber industry pioneer. Malaysian endemic."),
    ("rivularis", "Stream", "Alocasia Rivularis",
     "Moderate", 12, 60,
     "Rivularis means 'of streams' — naturally grows along stream banks. "
     "Tolerates more moisture than most Alocasias."),

    # S

    ("salarkhanii", "Salarkhan's", "Alocasia Salarkhanii",
     "Moderate", 15, 75,
     "Named after Salarkhan. Malaysian endemic with compact, distinctively "
     "patterned foliage."),
    ("sarawakensis", "Sarawak", "Alocasia Sarawakensis",
     "Moderate", 15, 80,
     "From Sarawak, Malaysian Borneo. Named for its biodiverse origin; "
     "compact with attractive foliage."),
    ("scabriuscula", "Rough", "Alocasia Scabriuscula",
     "Moderate", 12, 60,
     "Scabriuscula means 'slightly rough' — leaf surface has a subtle texture "
     "rather than being completely smooth."),
    ("simonsiana", "Simon's", "Alocasia Simonsiana",
     "Moderate", 14, 70,
     "Named after Nanna Simons. Compact species with attractive vein patterning; "
     "lesser-known but appealing collector plant."),
    ("suhirmaniana", "Suhirman's", "Alocasia Suhirmaniana",
     "Moderate", 14, 70,
     "Named after Suhirman; Indonesian endemic with compact, well-formed leaves."),

    # T–Z

    ("tandurusa", "Tandurusa", "Alocasia Tandurusa",
     "Moderate", 14, 70,
     "Named after a location in Indonesia (Tandurusa, North Sulawesi). "
     "Sulawesi endemic with distinctive leaf form."),
    ("venusta", "Beautiful", "Alocasia Venusta",
     "Moderate", 15, 80,
     "Venusta means 'beautiful' or 'charming' — exceptionally attractive "
     "species with elegant, graceful foliage."),
    ("vietnamensis", "Vietnamese", "Alocasia Vietnamensis",
     "Moderate", 12, 65,
     "From Vietnam. Compact species with well-formed arrowhead leaves; "
     "tolerates slightly cooler conditions than tropical species."),
    ("wongii", "Wong's", "Alocasia Wongii",
     "Moderate", 14, 70,
     "Named after Malaysian botanist S.Y. Wong. Malaysian endemic with "
     "compact, attractive foliage."),
    ("yunqiana", "Yunqi's", "Alocasia Yunqiana",
     "Moderate", 14, 70,
     "Named after Chinese botanist Yun Qi. One of the Chinese Alocasia species; "
     "relatively rare in cultivation outside Asia."),

    # Undescribed / not-yet-accepted cultivars (*)

    ("'Chienlii'", "Chienlii", "Alocasia Chienlii",
     "Moderate", 15, 80,
     "Not yet fully described botanically. Indonesian or Southeast Asian collector cultivar."),
    ("'Claytonoides'", "Claytonoides", "Alocasia Claytonoides",
     "Moderate", 15, 80,
     "Not yet fully described. Name suggests resemblance to another species. "
     "Collector cultivar."),
    ("'Inopinata'", "Inopinata", "Alocasia Inopinata",
     "Moderate", 15, 80,
     "Inopinata means 'unexpected' or 'unforeseen'. Not yet fully described; "
     "an unusually formed collector cultivar."),
    ("'Kulat'", "Kulat", "Alocasia Kulat",
     "Moderate", 15, 80,
     "Kulat means 'mushroom' in Malay — an unusual growth form or rounded leaf "
     "shape. Not yet formally described."),
    ("'Olanii'", "Olanii", "Alocasia Olanii",
     "Moderate", 15, 80,
     "Not yet fully described botanically. Indonesian collector cultivar."),
    ("'Pasappa'", "Pasappa", "Alocasia Pasappa",
     "Moderate", 15, 80,
     "Not yet fully described. Indonesian collector cultivar with attractive foliage."),
    ("'Pawitira'", "Pawitira", "Alocasia Pawitira",
     "Moderate", 15, 80,
     "Not yet fully described. Indonesian collector cultivar; "
     "possibly a variant of or related to 'Pawitra'."),
    ("'Prince of Curup'", "Prince of Curup", "Alocasia Prince of Curup",
     "Moderate", 18, 100,
     "Named after Curup, a town in Bengkulu, Sumatra. Not yet formally described; "
     "Indonesian collector cultivar with princely foliage."),
    ("'Yucatan Princess'", "Yucatan Princess", "Alocasia Yucatan Princess",
     "Moderate", 15, 80,
     "Unusual name for an Asian genus. Not yet fully described; "
     "compact cultivar with elegant leaf form."),
]
