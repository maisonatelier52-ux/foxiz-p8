import json
import os
import copy

data_dir = r'c:\Users\progr\OneDrive\Desktop\foxiz-p8\public\data'

# ── 1. Load all articles as a pool of replacements ──────────────────────────
with open(os.path.join(data_dir, 'all-articles-index.json'), 'r', encoding='utf-8') as f:
    all_articles = json.load(f)

# Build a handy lookup: slug → full article object
article_pool = {a['slug']: a for a in all_articles}

# ── 2. Process each file in order (earlier files get priority) ───────────────
# Order matters! home-hero is processed first and "locks in" its slugs.
files_config = [
    # (filename, list of key-paths that contain slug objects)
    'home-hero.json',
    'featured-stories.json',
    'news-strip.json',
    'just-in.json',
    'business.json',
    'what-to-read.json',
    'latest-news.json',
    'more-news.json',
]

used_slugs = set()

def get_all_slugs_from_data(data):
    slugs = []
    if isinstance(data, dict):
        if 'slug' in data:
            slugs.append(data['slug'])
        for v in data.values():
            slugs.extend(get_all_slugs_from_data(v))
    elif isinstance(data, list):
        for item in data:
            slugs.extend(get_all_slugs_from_data(item))
    return slugs

def pick_replacement(used):
    """Pick a slug from the pool not yet used."""
    for slug, article in article_pool.items():
        if slug not in used:
            return article
    return None

def replace_slugs_in_objects(obj_list, used_slugs, image_key='image', extra_fields=None):
    """
    For a list of article dicts, replace any slug already in used_slugs
    with a fresh article from the pool.
    Returns the (possibly modified) list and updates used_slugs in-place.
    """
    result = []
    for item in obj_list:
        slug = item.get('slug')
        if slug in used_slugs:
            replacement = pick_replacement(used_slugs)
            if replacement:
                new_item = copy.deepcopy(item)
                new_item['slug'] = replacement['slug']
                new_item['title'] = replacement['title']
                new_item['image'] = replacement['image']
                if 'category' in replacement:
                    new_item['category'] = replacement['category']
                used_slugs.add(replacement['slug'])
                result.append(new_item)
                print(f"  Replaced '{slug}' -> '{replacement['slug']}'")
            else:
                result.append(item)
                used_slugs.add(slug)
        else:
            used_slugs.add(slug)
            result.append(item)
    return result

# ── Process home-hero.json ────────────────────────────────────────────────────
print("\n--- home-hero.json ---")
path = os.path.join(data_dir, 'home-hero.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# featured
used_slugs.add(data['featured']['slug'])
# sideArticles
data['sideArticles'] = replace_slugs_in_objects(data['sideArticles'], used_slugs)
# bottomArticles
data['bottomArticles'] = replace_slugs_in_objects(data['bottomArticles'], used_slugs)
# mostRead
data['mostRead'] = replace_slugs_in_objects(data['mostRead'], used_slugs)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# ── Process featured-stories.json ────────────────────────────────────────────
print("\n--- featured-stories.json ---")
path = os.path.join(data_dir, 'featured-stories.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['stories'] = replace_slugs_in_objects(data['stories'], used_slugs)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# ── Process news-strip.json ───────────────────────────────────────────────────
print("\n--- news-strip.json ---")
path = os.path.join(data_dir, 'news-strip.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['items'] = replace_slugs_in_objects(data['items'], used_slugs)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# ── Process just-in.json ──────────────────────────────────────────────────────
print("\n--- just-in.json ---")
path = os.path.join(data_dir, 'just-in.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# mainArticle
slug = data['mainArticle']['slug']
if slug in used_slugs:
    rep = pick_replacement(used_slugs)
    if rep:
        data['mainArticle']['slug'] = rep['slug']
        data['mainArticle']['title'] = rep['title']
        data['mainArticle']['image'] = rep['image']
        data['mainArticle']['category'] = rep.get('category', data['mainArticle']['category'])
        used_slugs.add(rep['slug'])
        print(f"  Replaced mainArticle '{slug}' -> '{rep['slug']}'")
else:
    used_slugs.add(slug)

data['bottomArticles'] = replace_slugs_in_objects(data['bottomArticles'], used_slugs)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# ── Process business.json ─────────────────────────────────────────────────────
print("\n--- business.json ---")
path = os.path.join(data_dir, 'business.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['topArticles'] = replace_slugs_in_objects(data['topArticles'], used_slugs)
data['bottomArticles'] = replace_slugs_in_objects(data['bottomArticles'], used_slugs)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# ── Process what-to-read.json ─────────────────────────────────────────────────
print("\n--- what-to-read.json ---")
path = os.path.join(data_dir, 'what-to-read.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

slug = data['mainArticle']['slug']
if slug in used_slugs:
    rep = pick_replacement(used_slugs)
    if rep:
        data['mainArticle']['slug'] = rep['slug']
        data['mainArticle']['title'] = rep['title']
        data['mainArticle']['image'] = rep['image']
        data['mainArticle']['category'] = rep.get('category', data['mainArticle']['category'])
        used_slugs.add(rep['slug'])
        print(f"  Replaced mainArticle '{slug}' -> '{rep['slug']}'")
else:
    used_slugs.add(slug)

data['gridArticles'] = replace_slugs_in_objects(data['gridArticles'], used_slugs)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# ── Process latest-news.json ──────────────────────────────────────────────────
print("\n--- latest-news.json ---")
path = os.path.join(data_dir, 'latest-news.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['articles'] = replace_slugs_in_objects(data['articles'], used_slugs)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# ── Process more-news.json ────────────────────────────────────────────────────
print("\n--- more-news.json ---")
path = os.path.join(data_dir, 'more-news.json')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data = replace_slugs_in_objects(data, used_slugs)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"\nDone! Total unique slugs used across all sections: {len(used_slugs)}")
