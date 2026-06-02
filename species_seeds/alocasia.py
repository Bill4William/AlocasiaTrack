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
    "description": "100 popular Alocasia species, cultivars and hybrids — "
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
    # Legacy standalone name kept for backward-compatibility
    (
        "'Stingray'",
        "Stingray",
        "Alocasia Stingray",
        "Moderate", 10, 65,
        "Distinctive stingray-shaped leaves with an elongated raised tail tip. "
        "Corms: $6-14, Pups: $14-32, Plants: $28-65.",
    ),
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
    (
        "'California'",
        "California Elephant Ear",
        "Alocasia California",
        "Moderate", 10, 60,
        "Deeply lobed olive-green leaves with prominent veins. Vigorous grower; handles "
        "typical indoor humidity well. Corms: $6-14, Pups: $14-30, Plants: $26-60.",
    ),
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
    (
        "'Tiny Dancer'",
        "Tiny Dancer",
        "Alocasia Tiny Dancer",
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
]
