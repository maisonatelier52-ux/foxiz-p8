import json
import os

data_dir = r'c:\Users\progr\OneDrive\Desktop\foxiz-p8\public\data'
index_path = os.path.join(data_dir, 'all-articles-index.json')

files_to_check = [
    'home-hero.json',
    'featured-stories.json',
    'news-strip.json',
    'just-in.json',
    'business.json',
    'what-to-read.json',
    'latest-news.json',
    'more-news.json'
]

with open(index_path, 'r', encoding='utf-8') as f:
    all_articles = json.load(f)

used_slugs = set()
duplicates = {}

def get_slugs(data):
    slugs = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k == 'slug':
                slugs.append(v)
            else:
                slugs.extend(get_slugs(v))
    elif isinstance(data, list):
        for item in data:
            slugs.extend(get_slugs(item))
    return slugs

for filename in files_to_check:
    path = os.path.join(data_dir, filename)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    slugs = get_slugs(data)
    file_dupes = []
    for slug in slugs:
        if slug in used_slugs:
            file_dupes.append(slug)
        else:
            used_slugs.add(slug)
    if file_dupes:
        duplicates[filename] = file_dupes

print("Duplicates found:")
for file, dupes in duplicates.items():
    print(f"  {file}: {dupes}")

print(f"\nTotal unique slugs used: {len(used_slugs)}")
