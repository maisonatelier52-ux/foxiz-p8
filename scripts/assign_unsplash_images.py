"""
Assign curated, topic-matched Unsplash URLs to every article slug,
then update ALL JSON data files (data/*.json + data/articles/*.json).
No downloading - uses live Unsplash URLs directly.
"""
import json, os, re, glob

BASE_DIR     = r'c:\Users\progr\OneDrive\Desktop\foxiz-p8'
DATA_DIR     = os.path.join(BASE_DIR, 'public', 'data')
ARTICLES_DIR = os.path.join(DATA_DIR, 'articles')

# ── Master slug → Unsplash URL map ───────────────────────────────────────────
# Every URL uses ?q=80&w=1200&auto=format&fit=crop for full quality
W = '?q=80&w=1200&auto=format&fit=crop'
W_sm = '?q=80&w=600&auto=format&fit=crop'

SLUG_IMAGES = {
    # Technology / AI / Quantum
    'quantum-computing-breakthrough-2026':      f'https://images.unsplash.com/photo-1635070041078-e363dbe005cb{W}',
    'quantum-supremacy-real-world-applications': f'https://images.unsplash.com/photo-1518770660439-4636190af475{W}',
    'the-neural-interface-breakthrough':         f'https://images.unsplash.com/photo-1559757175-0eb30cd8c063{W}',
    'the-ethics-of-artificial-consciousness':    f'https://images.unsplash.com/photo-1677442135703-1787eea5ce01{W}',
    'ai-governance-summit-geneva':               f'https://images.unsplash.com/photo-1550751827-4bd374c3f58b{W}',
    'sociology-of-the-metaverse-interaction':    f'https://images.unsplash.com/photo-1593508512255-86ab42a8e620{W}',
    'the-silicon-desert-arizona-semiconductors': f'https://images.unsplash.com/photo-1518770660439-4636190af475{W}',

    # Space / Astronomy
    'asteroid-mining-pioneer-returns':           f'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa{W}',
    'space-exploration-priority-vs-earth-issues':f'https://images.unsplash.com/photo-1446941611757-91d2c3bd3d45{W}',
    'space-archaeology-orbital-perspectives':    f'https://images.unsplash.com/photo-1614728894747-a83421e2b9c9{W}',
    'space-treaty-2026-mining-rights':           f'https://images.unsplash.com/photo-1457364887197-9150188c107b{W}',
    'deep-space-telescope-exoplanet-biomarkers': f'https://images.unsplash.com/photo-1502134249126-9f3755a50d78{W}',
    'dark-matter-detection-milestone-results':   f'https://images.unsplash.com/photo-1462331940025-496dfbfc7564{W}',

    # Energy / Fusion / Renewable
    'fusion-energy-grid-connection':             f'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e{W}',
    'fusion-energy-pilot-plants-2030-goals':     f'https://images.unsplash.com/photo-1527689368864-3a821dbccc34{W}',
    'perovskite-solar-cells-efficiency-record':  f'https://images.unsplash.com/photo-1509391366360-2e959784a276{W}',
    'offshore-wind-expansion-floating-turbines': f'https://images.unsplash.com/photo-1466611653911-b1a9ea6a7a62{W}',
    'hydrogen-economy-industrial-decarbonize':   f'https://images.unsplash.com/photo-1615811361523-6bd03d7748e7{W}',
    'solid-state-grid-batteries-stability':      f'https://images.unsplash.com/photo-1558618666-fcd25c85cd64{W}',
    'geothermal-innovations-deep-borehole-heat': f'https://images.unsplash.com/photo-1536183922588-166604504d5e{W}',
    'tidal-power-predictable-ocean-turbines':    f'https://images.unsplash.com/photo-1505118380757-91f5f5632de0{W}',
    'smart-grids-ai-optimization-energy-flow':   f'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13{W}',
    'the-green-transition-economic-winners':     f'https://images.unsplash.com/photo-1473081556163-2a17de81fc2b{W}',

    # Climate / Environment
    'carbon-capture-scaling-2026-milestone':     f'https://images.unsplash.com/photo-1532408840957-031d8034aeef{W}',
    'ocean-acidification-mitigation-coral-reef': f'https://images.unsplash.com/photo-1582967788606-a171c1080cb0{W}',
    'glacier-retreat-water-security-impact':     f'https://images.unsplash.com/photo-1519681393784-d120267933ba{W}',
    'climate-migration-urban-planning-adapts':   f'https://images.unsplash.com/photo-1573167243872-43c6433b9d40{W}',
    'methane-emissions-tracking-satellite-data': f'https://images.unsplash.com/photo-1504700610630-ac6aba3536d3{W}',
    'reforestation-biodiversity-soil-carbon-sink':f'https://images.unsplash.com/photo-1448375240586-882707db888b{W}',
    'extreme-weather-predictive-ai-models':      f'https://images.unsplash.com/photo-1527482797697-8795b05a13fe{W}',
    'climate-policy-shift-in-major-economies':   f'https://images.unsplash.com/photo-1498408040764-ab6eb772a145{W}',
    'economics-of-climate-change':               f'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e{W}',
    'the-great-rewilding-europe-success-stories':f'https://images.unsplash.com/photo-1474511320723-9a56873867b5{W}',

    # Ocean / Maritime
    'inside-the-deep-sea-mining-race':           f'https://images.unsplash.com/photo-1628349932168-0b5e3fac0428{W}',
    'ocean-governance-high-seas-protection':     f'https://images.unsplash.com/photo-1505118380757-91f5f5632de0{W}',
    'ocean-territory-disputes-new-treaties':     f'https://images.unsplash.com/photo-1436262513933-a0b06755c784{W}',
    'arctic-silk-road-shipping-boom':            f'https://images.unsplash.com/photo-1511884642898-4c92249e20b6{W}',
    'arctic-exploration-new-frontier-2026':      f'https://images.unsplash.com/photo-1517694712202-14dd9538aa97{W}',

    # Global Affairs / Diplomacy / Geopolitics
    'leaders-rival-factions-agree-peace-talks':  f'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620{W}',
    'peace-talks-middle-east-2026-prospects':    f'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620{W}',
    'diplomacy-in-the-digital-age-sovereignty':  f'https://images.unsplash.com/photo-1522202176988-66273c2fd55f{W}',
    'the-future-of-global-diplomacy-2026':       f'https://images.unsplash.com/photo-1524492412937-b28074a5d7da{W}',
    'global-health-cooperation-pandemic-prevent':f'https://images.unsplash.com/photo-1584036561566-baf8f5f1b144{W}',
    'cyberwarfare-defense-strategies-nato':      f'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5{W}',
    'human-rights-digital-surveillance-laws':    f'https://images.unsplash.com/photo-1545987796-200677ee1011{W}',
    'the-new-silk-road-infrastructure-update':   f'https://images.unsplash.com/photo-1504711434969-e33886168f5c{W}',
    'trans-atlantic-trade-partnership-renewal':  f'https://images.unsplash.com/photo-1499244571948-7ccddb3583f1{W}',

    # Politics / Governance
    'midterm-shift-2026-analysis':               f'https://images.unsplash.com/photo-1529101091760-61df6be24296{W}',
    'the-impact-of-midterm-elections-on-policy': f'https://images.unsplash.com/photo-1615461066841-6116e61058f4{W}',
    'electoral-reforms-digital-voting-security': f'https://images.unsplash.com/photo-1568822617270-2c1b12a5dec0{W}',
    'global-democracy-index-2026-results':       f'https://images.unsplash.com/photo-1605810230434-7631ac76ec81{W}',
    'un-security-council-expansion-debate':      f'https://images.unsplash.com/photo-1612831455359-970e23a1e4e9{W}',
    'the-rise-of-decentralized-governance':      f'https://images.unsplash.com/photo-1451187580459-43490279c0fa{W}',
    'global-tax-alignment-for-multi-nationals':  f'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3{W}',
    'tax-policy-inequality-global-prospects':    f'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3{W}',

    # Economics / Business / Finance
    'inflation-management-strategies-2026':      f'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3{W}',
    'labor-market-shifts-automation-impact':     f'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d{W}',
    'global-supply-chain-disruptions':           f'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d{W}',
    'global-supply-chain-rebalancing-act':       f'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d{W}',
    'consumer-spending-patterns-post-recession': f'https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da{W}',
    'fdi-trends-emerging-tech-hubs-asia':        f'https://images.unsplash.com/photo-1474314170901-f351b68f544f{W}',
    'the-future-of-commercial-real-estate':      f'https://images.unsplash.com/photo-1486325212027-8081e485255e{W}',
    'cbdc-global-adoption-milestone':            f'https://images.unsplash.com/photo-1621761191319-c6fb62004040{W}',
    'the-rise-of-digital-sovereign-currencies':  f'https://images.unsplash.com/photo-1621761191319-c6fb62004040{W}',
    'cryptocurrency-vs-traditional-banking':     f'https://images.unsplash.com/photo-1621761191319-c6fb62004040{W}',
    'universal-basic-income-the-looming-necessity':f'https://images.unsplash.com/photo-1532629345422-7515f3d16bb6{W}',
    'universal-basic-income-bold-idea':          f'https://images.unsplash.com/photo-1532629345422-7515f3d16bb6{W}',
    'youth-unemployment-silent-crisis':          f'https://images.unsplash.com/photo-1541844053589-346841d0b34c{W}',

    # Research / Science / Medicine
    'genomic-editing-precision-medicine-2026':   f'https://images.unsplash.com/photo-1530026405186-ed1f139313f8{W}',
    'materials-science-room-temp-superconduct':  f'https://images.unsplash.com/photo-1507668077129-56e32842fceb{W}',
    'cognitive-science-memory-enhancement-study':f'https://images.unsplash.com/photo-1559757148-5c350d0d3c56{W}',
    'paleontology-dna-extraction-extinct-mammals':f'https://images.unsplash.com/photo-1605792657660-596af9009e82{W}',
    'artificial-organs-longevity-breakthrough':  f'https://images.unsplash.com/photo-1530026405186-ed1f139313f8{W}',
    'the-lost-cities-of-the-amazon-discovered':  f'https://images.unsplash.com/photo-1518623489648-a173ef7824f3{W}',
    'mental-health-infrastructure-social-priority':f'https://images.unsplash.com/photo-1493836512294-502baa1986e2{W}',

    # Featured / Long-form
    'inside-the-deep-sea-mining-race':           f'https://images.unsplash.com/photo-1628349932168-0b5e3fac0428{W}',
    'the-silicon-desert-arizona-semiconductors': f'https://images.unsplash.com/photo-1518770660439-4636190af475{W}',
    'arctic-exploration-new-frontier-2026':      f'https://images.unsplash.com/photo-1517694712202-14dd9538aa97{W}',
    'quantum-supremacy-real-world-applications': f'https://images.unsplash.com/photo-1635070041078-e363dbe005cb{W}',
    'space-archaeology-orbital-perspectives':    f'https://images.unsplash.com/photo-1614728894747-a83421e2b9c9{W}',
    'the-great-rewilding-europe-success-stories':f'https://images.unsplash.com/photo-1474511320723-9a56873867b5{W}',

    # Opinion / Society
    'globalization-vs-localization-economic-debate':f'https://images.unsplash.com/photo-1558618666-fcd25c85cd64{W}',
    'educational-reform-skill-based-learning':   f'https://images.unsplash.com/photo-1522202176988-66273c2fd55f{W}',
    'the-future-of-privacy-is-it-already-gone':  f'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5{W}',
    'journalism-and-truth-in-the-post-deep-fake-era':f'https://images.unsplash.com/photo-1504711434969-e33886168f5c{W}',
}

# Author avatar URLs (topic: professional headshots)
AUTHOR_AVATARS = {
    'Maria Sanchez':  'https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=200&auto=format&fit=crop&crop=face',
    'Emily Rodriguez':'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=200&auto=format&fit=crop&crop=face',
    'Jessica Wu':     'https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop&crop=face',
    'Robert Miller':  'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop&crop=face',
    'Sarah Jenkins':  'https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?q=80&w=200&auto=format&fit=crop&crop=face',
    'David Smith':    'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=200&auto=format&fit=crop&crop=face',
    'Michael Chen':   'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop&crop=face',
    'Alex Thorne':    'https://images.unsplash.com/photo-1519345182560-3f2917c472ef?q=80&w=200&auto=format&fit=crop&crop=face',
    "James O'Connor": 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=200&auto=format&fit=crop&crop=face',
    'James Sinclair': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=200&auto=format&fit=crop&crop=face',
    'Leo Sterling':   'https://images.unsplash.com/photo-1568602471122-7832951cc4c5?q=80&w=200&auto=format&fit=crop&crop=face',
    'James O\'Connor':'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=200&auto=format&fit=crop&crop=face',
}

# ── Helper ────────────────────────────────────────────────────────────────────
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    try:
        return json.loads(raw)
    except:
        return json.loads(re.sub(r',\s*([}\]])', r'\1', raw))

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def apply_images(obj, parent_slug=None):
    """Recursively set image URLs based on slug context."""
    if isinstance(obj, dict):
        slug = obj.get('slug', parent_slug)

        # Set article image
        if 'image' in obj and slug and slug in SLUG_IMAGES:
            obj['image'] = SLUG_IMAGES[slug]

        # Set author avatar
        if 'author' in obj:
            author = obj['author']
            if isinstance(author, dict):
                name = author.get('name', '')
                if name in AUTHOR_AVATARS:
                    author['avatar'] = AUTHOR_AVATARS[name]
            elif isinstance(author, str) and 'image' not in obj and slug in SLUG_IMAGES:
                pass  # index-style, image already set above

        for k, v in obj.items():
            if k not in ('image', 'avatar'):
                apply_images(v, slug)

    elif isinstance(obj, list):
        for item in obj:
            apply_images(item, parent_slug)

# ── Process all data files  ───────────────────────────────────────────────────
all_json_files = (
    glob.glob(os.path.join(DATA_DIR, '*.json')) +
    glob.glob(os.path.join(ARTICLES_DIR, '*.json'))
)

updated = 0
total_images_set = 0

for jf in all_json_files:
    try:
        data = load_json(jf)
    except Exception as e:
        print(f'[skip-parse] {os.path.basename(jf)}: {e}')
        continue

    before = json.dumps(data)
    apply_images(data)
    after = json.dumps(data)

    if before != after:
        save_json(jf, data)
        updated += 1

print(f'Updated {updated} JSON files with topic-matched Unsplash images.')
print(f'Total articles with assigned images: {len(SLUG_IMAGES)}')
print(f'Author avatars mapped: {len(AUTHOR_AVATARS)}')
