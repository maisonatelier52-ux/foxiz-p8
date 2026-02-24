
import json
import os

# Load articles
with open('c:/Users/progr/OneDrive/Desktop/foxiz-p8/public/data/all-articles-index.json', 'r') as f:
    articles = json.load(f)

# Group by category
categorized = {}
for a in articles:
    cat = a['category'].lower()
    if cat not in categorized:
        categorized[cat] = []
    categorized[cat].append(a)

# Save to public/data/categoryNews/
output_dir = 'c:/Users/progr/OneDrive/Desktop/foxiz-p8/public/data/categoryNews/'
os.makedirs(output_dir, exist_ok=True)

for cat, posts in categorized.items():
    output_path = os.path.join(output_dir, f"{cat}.json")
    with open(output_path, 'w') as f:
        json.dump(posts, f, indent=4)
    print(f"Generated {output_path} with {len(posts)} articles.")

print("Finished splitting articles into categoryNews files.")
