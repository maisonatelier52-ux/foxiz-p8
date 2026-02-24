
import json
import random
import os

# New official categories from the user
categories_map = {
    "opinion": "Opinion",
    "economic": "Economic",
    "featured": "Featured",
    "global-affairs": "Global Affairs",
    "climate": "Climate Change",
    "renewable": "Renewable Energy",
    "politics": "Politics",
    "research": "Research"
}

authors = [
    {"name": "David Smith", "image": "https://i.pravatar.cc/150?u=david"},
    {"name": "Sarah Jenkins", "image": "https://i.pravatar.cc/150?u=sarah"},
    {"name": "Michael Chen", "image": "https://i.pravatar.cc/150?u=michael"},
    {"name": "Emily Rodriguez", "image": "https://i.pravatar.cc/150?u=emily"},
    {"name": "Jessica Wu", "image": "https://i.pravatar.cc/150?u=jessica"},
    {"name": "Alex Thorne", "image": "https://i.pravatar.cc/150?u=alex"},
    {"name": "Maria Sanchez", "image": "https://i.pravatar.cc/150?u=maria"},
    {"name": "James O'Connor", "image": "https://i.pravatar.cc/150?u=james"},
    {"name": "Robert Miller", "image": "https://i.pravatar.cc/150?u=robert"}
]

topics = {
    "Opinion": [
        ("the-ethics-of-artificial-consciousness", "The Ethics of AI: When Does a Model Deserve Rights?", "As AI becomes indistinguishable from human intelligence, we must face difficult moral questions."),
        ("globalization-vs-localization-economic-debate", "The Case for Local: Why Resilience Might Matter More than Efficiency", "The pandemic-era supply chain shock has led to a major rethink of the globalized economic model."),
        ("educational-reform-skill-based-learning", "Degrees or Skills? Why the Future of Education is Modular", "Traditional universities face disruption as employers shift focus toward verified skill badges over diplomas."),
        ("the-future-of-privacy-is-it-already-gone", "The Illusion of Privacy: Can We Ever Truly Disconnect?", "An exploration of the social and psychological impact of living in a state of constant digital surveillance."),
        ("space-exploration-priority-vs-earth-issues", "The Mars Dilemma: Why Exploration Inspires Solutions for Earth", "Defending the multi-planetary dream as a driver for sustainable technology here at home."),
        ("universal-basic-income-the-looming-necessity", "The AI Safety Net: Why UBI is No Longer an Option, but a Necessity", "Preparing for a world where automation significantly reduces the total number of human-held jobs."),
        ("mental-health-infrastructure-social-priority", "The Silent Crisis: Why Mental Health must be the Priority of 2026", "Investing in psychological infrastructure is as critical as building roads and bridges."),
        ("journalism-and-truth-in-the-post-deep-fake-era", "Guardians of Fact: The Critical Role of Journalism in an AI-Driven World", "Why authentic, human-verified reporting is the only defense against a flood of synthetic misinformation.")
    ],
    "Economic": [
        ("inflation-management-strategies-2026", "Managing Inflation: Strategies for a Polarized Global Economy", "How central banks are navigating the thin line between growth and stability in 2026."),
        ("the-rise-of-digital-sovereign-currencies", "Digital Gold: The Rise of Sovereign Cryptocurrencies", "National governments begin adopting digital formats for their currencies in earnest."),
        ("labor-market-shifts-automation-impact", "Automation and the Labor Market: A 2026 Status Report", "The evolving relationship between human workers and autonomous systems in heavy industry."),
        ("global-supply-chain-rebalancing-act", "Resilience Over Speed: The New Global Supply Chain Standard", "Companies prioritize safety stocks and local sourcing in a volatile trade environment."),
        ("the-future-of-commercial-real-estate", "Repurposing the City: The Future of Commercial Real Estate", "How vacant office spaces are being transformed into residential and communal hubs."),
        ("fdi-trends-emerging-tech-hubs-asia", "Asia's New Tech Corridors: Where FDI is Flowing in 2026", "Vietnam and Indonesia emerge as the primary beneficiaries of the latest manufacturing shift."),
        ("consumer-spending-patterns-post-recession", "The New Consumer: Spending Patterns in a High-Efficiency Era", "Analyzing how households are prioritizing services over goods in the mid-2020s."),
        ("tax-policy-inequality-global-prospects", "Addressing the Gap: Global Tax Policies for a New Decade", "A review of the latest international efforts to modernize wealth and corporate taxation.")
    ],
    "Featured": [
        ("inside-the-deep-sea-mining-race", "The Deep Blue Gold Rush: Inside the Race for Seabed Minerals", "A investigative look at the companies and nations battling for control of the ocean floor."),
        ("the-lost-cities-of-the-amazon-discovered", "History Reclaimed: LIDAR Uncovers Lost Civilizations in the Amazon", "How laser technology is rewriting the history of human settlement in South America."),
        ("artificial-organs-longevity-breakthrough", "The Bionic Heart: How 3D-Bioprinting is Solving the Organ Crisis", "A feature story on the first successful long-term transplants of fully synthetic organs."),
        ("the-silicon-desert-arizona-semiconductors", "The Silicon Desert: Arizona's Transformation into a Chip Giant", "Inside the massive semiconductor fabs reshaping the American Southwest."),
        ("arctic-exploration-new-frontier-2026", "The Melting Frontier: A Journey Through the New Arctic Passages", "Following the explorers and scientists documenting the transformation of the North Pole."),
        ("quantum-supremacy-real-world-applications", "Beyond Theory: First Practical Uses of Quantum Computers in Drug Discovery", "How specialized quantum processors are cutting years off medical research timelines."),
        ("space-archaeology-orbital-perspectives", "Eyes in the Sky: Space Archaeology and the Discovery of Ancient Roads", "Using high-resolution satellite imagery to uncover forgotten terrestrial networks."),
        ("the-great-rewilding-europe-success-stories", "Nature Bounces Back: The Success of Europe's Master Rewilding Plan", "Documenting the return of keystone species to the European wilderness after a century of absence.")
    ],
    "Global Affairs": [
        ("diplomacy-in-the-digital-age-sovereignty", "Digital Diplomacy: Sovereignty in the Age of Global Networks", "How nations are negotiating the boundaries of the internet as a physical territory."),
        ("the-new-silk-road-infrastructure-update", "Connectivity Reimagined: The Latest Status of the New Silk Road", "A comprehensive update on the world's largest infrastructure project."),
        ("peace-talks-middle-east-2026-prospects", "A New Framework for Peace: Assessing Middle East Stability in 2026", "Analyzing the latest diplomatic breakthroughs in the region."),
        ("space-treaty-2026-mining-rights", "Ownership in Orbit: The Global Treaty for Space Mining Rights", "International law catches up with technology as nations agree on lunar resource management."),
        ("cyberwarfare-defense-strategies-nato", "The Fifth Domain: NATO's New Strategies for Cyber Defenses", "How modern alliances are preparing for non-physical conflicts."),
        ("global-health-cooperation-pandemic-prevent", "Viral Sentinels: The Global Network for Pandemic Prevention", "Inside the real-time monitoring systems designed to catch the next outbreak early."),
        ("ocean-governance-high-seas-protection", "Blue Diplomacy: The Battle to Protect the High Seas", "Negotiating the management of international waters beyond national jurisdictions."),
        ("human-rights-digital-surveillance-laws", "Rights in the Machine: Protecting Privacy Under Global Surveillance", "The legal battle to define human rights in a world of constant digital tracking.")
    ],
    "Climate Change": [
        ("carbon-capture-scaling-2026-milestone", "Scaling the Sky: Carbon Capture Hits Megaton Milestones in 2026", "A look at the technology finally making a dent in atmospheric CO2 levels."),
        ("ocean-acidification-mitigation-coral-reef", "Saving the Reefs: New Strategies for Ocean Acidification Mitigation", "How scientists are using chemistry and biology to protect vulnerable marine ecosystems."),
        ("glacier-retreat-water-security-impact", "The Thirst of Nations: Glacier Retreat and Global Water Security", "Modeling the long-term impact of losing the world's mountain water towers."),
        ("climate-migration-urban-planning-adapts", "The Resilient City: How Urban Planning is Adapting to Climate Migration", "Managing the influx of populations as environmental conditions shift globally."),
        ("methane-emissions-tracking-satellite-data", "Methane Hunters: Using Satellites to Trace Invisible Emissions", "How precise orbital data is forcing industrial emitters to clean up their act."),
        ("reforestation-biodiversity-soil-carbon-sink", "More Than Just Trees: Restoring Soil as the Ultimate Carbon Sink", "Integrating regenerative agriculture into global reforestation efforts."),
        ("extreme-weather-predictive-ai-models", "Knowing the Storm: How AI is Revolutionizing Extreme Weather Prediction", "Using machine learning to provide weeks of warning for cyclones and heatwaves."),
        ("the-green-transition-economic-winners", "The New Green Titans: Which Economies are Winning the Transition?", "Analyzing the shift in global power as the fossil fuel era begins to sunset.")
    ],
    "Renewable Energy": [
        ("perovskite-solar-cells-efficiency-record", "The Solar Breakthrough: Perovskite Cells Hit 35% Efficiency", "Next-generation solar tech prepares for mass market deployment."),
        ("offshore-wind-expansion-floating-turbines", "Wind at Sea: The Rise of Floating Deep-Water Wind Farms", "Unlocking the massive wind potential of the deep oceans with new platform tech."),
        ("hydrogen-economy-industrial-decarbonize", "Green Hydrogen: The Key to Decarbonizing Heavy Industry", "How hydrogen is replacing coal and gas in steel and cement production."),
        ("solid-state-grid-batteries-stability", "Stabilizing the Grid: Solid-State Batteries for Mega-Scale Storage", "The infrastructure allowing 100% renewable grids to function 24/7."),
        ("geothermal-innovations-deep-borehole-heat", "Tapping the Core: Revolutionary Deep Borehole Geothermal Energy", "Accessing constant, clean energy anywhere on Earth by drilling deeper than ever."),
        ("fusion-energy-pilot-plants-2030-goals", "Ignition Achieved: First Commercial Fusion Pilot Plants Break Ground", "The dream of limitless clean energy takes a major step toward reality."),
        ("tidal-power-predictable-ocean-turbines", "Lunar Power: Tapping the Reliable Energy of the Tides", "New turbine designs prove that the ocean's rhythm is a viable baseload power source."),
        ("smart-grids-ai-optimization-energy-flow", "Thinking Power: How AI is Optimizing National Energy Grids", "Reducing waste and improving efficiency through real-time, intelligent distribution.")
    ],
    "Politics": [
        ("midterm-shift-2026-analysis", "The 2026 Midterm Shift: A Deep Dive into the Battle for the House", "As the 2026 midterm elections approach, political analysts are witnessing a seismic shift."),
        ("the-future-of-global-diplomacy-2026", "The Future of Global Diplomacy: Beyond Traditional Borders", "A look at how digital sovereignty is reshaping international relations."),
        ("electoral-reforms-digital-voting-security", "Electoral Reforms: Can Digital Voting Ever Be Truly Secure?", "Checking the progress of blockchain-based voting trials."),
        ("climate-policy-shift-in-major-economies", "Climate Policy Shift: Economic Giants Align on Carbon Taxes", "A major breakthrough in international climate cooperation."),
        ("the-rise-of-decentralized-governance", "The Rise of DAOs: Could Decentralized Governance Replace City Councils?", "Exploring community-led smart contract governance."),
        ("global-tax-alignment-for-multi-nationals", "Taxing the Giants: Global Minimum Tax Reaches 20%", "The latest on international tax reform."),
        ("the-impact-of-midterm-elections-on-policy", "Midterm Impact: The Legislative Gridlock or a Path to Progress?", "Analyzing the post-election landscape."),
        ("ocean-territory-disputes-new-treaties", "The High Seas Treaty: Resolving Arctic Territory Disputes", "New laws for the changing north.")
    ],
    "Research": [
        ("genomic-editing-precision-medicine-2026", "CRISPR 2.0: The Era of Error-Free Genomic Editing Begins", "New research shows how to fix genetic disorders with 100% precision."),
        ("the-neural-interface-breakthrough", "Mind to Machine: The Latest Breakthroughs in Neural Interfaces", "Recovering mobility and communication for paralyzed patients through direct brain links."),
        ("dark-matter-detection-milestone-results", "Hunting the Invisible: New Results from the Most Sensitive Dark Matter Detector", "Physics enters a new era as we get closer to understanding the universe's missing mass."),
        ("materials-science-room-temp-superconduct", "The Holy Grail: Room-Temperature Superconductors and Their Impact", "Material scientists announce a stable, practical superconductor for electrical lines."),
        ("cognitive-science-memory-enhancement-study", "Enhancing Memory: A Landmark Study on Targeted Neural Stimulation", "How specific frequencies can help recover lost memories in Alzheimer's patients."),
        ("paleontology-dna-extraction-extinct-mammals", "Resurrecting the Past: DNA Extraction from 2-Million-Year-Old Permafrost", "A breakthrough in paleogenetics reveals the ecosystem of the ancient north."),
        ("sociology-of-the-metaverse-interaction", "Social 3.0: A Longitudinal Study of Human Interaction in Virtual Space", "How digital living is reshaping our fundamental social structures."),
        ("deep-space-telescope-exoplanet-biomarkers", "Signs of Life? Deep-Space Telescope Identifies Oxygen on a Nearby Exoplanet", "The search for extraterrestrial life hits a significant milestone.")
    ]
}

def generate_content(title, category, shortdescription):
    return [
        {
            "type": "intro",
            "text": f"In a rapidly evolving global landscape, {title} stands as a pivotal development in {category}. {shortdescription}. This news piece delves into the layers of this story, exploring the motivations, the technology, and the far-reaching consequences of this event.",
            "hasDropCap": True
        },
        {
            "type": "paragraph",
            "text": "The details emerging from recent reports suggest that we are entering a new phase of international cooperation and technological integration. Experts argue that the previous frameworks are no longer sufficient to handle the complexity of modern systems. As we look toward the end of the decade, the decisions made today will echo through the next century of development."
        },
        {
            "type": "heading",
            "text": "The Core of the Transformation"
        },
        {
            "type": "paragraph",
            "text": "At the heart of this issue is a fundamental shift in how we perceive value and accessibility. By leveraging decentralized networks and advanced AI models, stakeholders are finding ways to bridge gaps that have existed for decades. This isn't just about efficiency; it's about a complete reimagining of the social and economic contract."
        },
        {
            "type": "quote",
            "text": "We are not just witnessing history; we are building the platforms that will define the next millennium. The era of traditional boundaries is giving way to a more fluid, interconnected world."
        },
        {
            "type": "paragraph",
            "text": "As the situation continues to unfold, we will remain dedicated to providing the most accurate and in-depth analysis. The intersection of policy, innovation, and human ambition continues to be the most exciting frontier of our time."
        }
    ]

all_articles_index = []
articles_dir = 'c:/Users/progr/OneDrive/Desktop/foxiz-p8/public/data/articles/'
os.makedirs(articles_dir, exist_ok=True)

# Generate Articles
for cat_id, cat_name in categories_map.items():
    topic_list = topics.get(cat_name, [])
    for slug, title, short_desc in topic_list:
        author = random.choice(authors)
        image_id = random.randint(1500000000000, 1700000000000)
        image_url = f"https://images.unsplash.com/photo-{image_id}?q=80&w=1200&auto=format&fit=crop"
        
        # Index Data
        all_articles_index.append({
            "slug": slug,
            "title": title,
            "shortdescription": short_desc,
            "category": cat_name,
            "author": author['name'],
            "date": "February 23, 2026",
            "image": image_url
        })
        
        # Detail Data
        detail_article = {
            "category": cat_name,
            "title": title,
            "author": {
                "name": author['name'],
                "image": author['image']
            },
            "date": "February 23, 2026",
            "image": image_url,
            "content": generate_content(title, cat_name, short_desc)
        }
        
        with open(os.path.join(articles_dir, f"{slug}.json"), 'w') as f:
            json.dump(detail_article, f, indent=4)

# Save all-articles-index.json
with open('c:/Users/progr/OneDrive/Desktop/foxiz-p8/public/data/all-articles-index.json', 'w') as f:
    json.dump(all_articles_index, f, indent=4)

# Split into categoryNews files with metadata
cat_news_dir = 'c:/Users/progr/OneDrive/Desktop/foxiz-p8/public/data/categoryNews/'
os.makedirs(cat_news_dir, exist_ok=True)

# Original descriptions from categories.json (cached here for the migration)
descriptions = {
    "opinion": "Expert analysis and unique perspectives on current events and global trends.",
    "economic": "In-depth coverage of global economies, fiscal policies, and macroeconomic trends.",
    "featured": "Our most impactful stories and investigative deep-dives.",
    "global-affairs": "Comprehensive reporting on international relations, diplomacy, and world events.",
    "climate": "Tracking the environmental changes and global efforts to combat climate change.",
    "renewable": "The latest in clean energy technology, infrastructure, and sustainable power.",
    "politics": "Inside coverage of governance, policy-making, and political developments.",
    "research": "Scientific breakthroughs, academic studies, and data-driven analysis."
}

# Clear first
for f in os.listdir(cat_news_dir):
    if f.endswith(".json"):
        os.remove(os.path.join(cat_news_dir, f))

for cat_id, cat_name in categories_map.items():
    posts = [a for a in all_articles_index if a['category'] == cat_name]
    
    # Self-contained Category Data
    category_data = {
        "title": cat_name,
        "id": cat_id,
        "description": descriptions.get(cat_id, f"Latest news and updates in {cat_name}."),
        "count": len(posts),
        "articles": posts
    }
    
    with open(os.path.join(cat_news_dir, f"{cat_id}.json"), 'w') as f:
        json.dump(category_data, f, indent=4)

# Remove the old method's file if it exists
categories_json_path = 'c:/Users/progr/OneDrive/Desktop/foxiz-p8/public/data/categories.json'
if os.path.exists(categories_json_path):
    os.remove(categories_json_path)

print(f"Successfully rebuilt everything: 64 index entries, 64 detail files. Switched to self-contained category files in categoryNews/ and removed categories.json.")

