
import json

# Load articles
with open('c:/Users/progr/OneDrive/Desktop/foxiz-p8/public/data/all-articles-index.json', 'r') as f:
    articles = json.load(f)

# Count by category
counts = {}
for a in articles:
    cat = a['category'].lower()
    counts[cat] = counts.get(cat, 0) + 1

# Load categories
with open('c:/Users/progr/OneDrive/Desktop/foxiz-p8/public/data/categories.json', 'r') as f:
    categories = json.load(f)

# Update counts (and add missing categories if any)
for cat_id, details in categories.items():
    if cat_id in counts:
        details['count'] = counts[cat_id]

# Save updated categories
with open('c:/Users/progr/OneDrive/Desktop/foxiz-p8/public/data/categories.json', 'w') as f:
    json.dump(categories, f, indent=4)

print("Updated categories.json with new counts.")
for cat, count in counts.items():
    print(f"{cat}: {count}")
