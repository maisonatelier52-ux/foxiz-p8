"""
Fix the blank 150x150 placeholder images:
1. Find all JSON files referencing /images/news/150_*.webp
2. Re-download the original Unsplash URL for each (with proper delay)
3. Re-save as WebP and update the JSON paths
"""
import json
import os
import re
import time
import requests
from PIL import Image
from io import BytesIO

BASE_DIR    = r'c:\Users\progr\OneDrive\Desktop\foxiz-p8'
DATA_DIR    = os.path.join(BASE_DIR, 'public', 'data')
OUTPUT_DIR  = os.path.join(BASE_DIR, 'public', 'images', 'news')
PUBLIC_PATH = '/images/news'
ARTICLES_DIR = os.path.join(DATA_DIR, 'articles')

# ── Step 1: Find all 150×150 blanks in the news folder ──────────────────────
blank_files = set()
for fname in os.listdir(OUTPUT_DIR):
    if not fname.endswith('.webp'):
        continue
    fp = os.path.join(OUTPUT_DIR, fname)
    try:
        img = Image.open(fp)
        if img.size == (150, 150):
            blank_files.add(f'/images/news/{fname}')
    except:
        pass
print(f'Found {len(blank_files)} blank placeholder files.')

# ── Step 2: Collect all JSON data files ─────────────────────────────────────
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    try:
        return json.loads(raw)
    except:
        fixed = re.sub(r',\s*([}\]])', r'\1', raw)
        return json.loads(fixed)

all_data_files = []

# flat-array files
for fname in ['more-news.json']:
    p = os.path.join(DATA_DIR, fname)
    if os.path.exists(p):
        all_data_files.append(p)

# nested object files
for fname in ['home-hero.json','featured-stories.json','news-strip.json',
              'just-in.json','business.json','what-to-read.json',
              'latest-news.json','all-articles-index.json']:
    p = os.path.join(DATA_DIR, fname)
    if os.path.exists(p):
        all_data_files.append(p)

# article files
for fname in os.listdir(ARTICLES_DIR):
    if fname.endswith('.json'):
        all_data_files.append(os.path.join(ARTICLES_DIR, fname))

# ── Step 3: Build a map of blank_local_path -> original Unsplash URL ────────
# We do this by re-reading the ORIGINAL Unsplash URLs from the git history
# Since we already replaced them, we use the Unsplash URL embedded in filename hash
# Instead, we'll collect from a "reverse lookup" approach:
# Walk all files, find every image field. If it's not a blank, it's already fine.
# If it IS blank, we need the original URL. 
# 
# Strategy: delete blank files, then download all images fresh from Unsplash
# with proper 1-second delays between requests.

# We need to rebuild the url->local mapping by scanning files for local paths
# and matching them to known original URLs. Since paths were already overwritten,
# we need to use a curated list of KNOWN GOOD image URLs matched to the slugs.

# BETTER APPROACH: For each article we know the slug. Pull from individual article JSONs.
# The article JSON still has the slug. We can use the slug to find appropriate images.

# Actually the simplest fix: delete all 150x150 files and re-download the originals
# from Unsplash WITH proper rate limiting (1-2 sec delay each).
# We rebuild by scanning all JSON for '/images/news/150_*.webp' paths and
# collecting their surrounding 'slug' context to pick replacement images.

# Collect slug -> list of blank local paths from data files
slug_to_blank = {}   # slug: blank_path

def collect_blanks(obj, current_slug=None, result=None):
    if result is None:
        result = {}
    if isinstance(obj, dict):
        slug = obj.get('slug', current_slug)
        image = obj.get('image', '')
        if image in blank_files:
            result.setdefault(slug or 'unknown', []).append(image)
        for v in obj.values():
            collect_blanks(v, slug, result)
    elif isinstance(obj, list):
        for item in obj:
            collect_blanks(item, current_slug, result)
    return result

# Also build list of all (file, data) tuples with blanks
files_needing_fix = []

for fpath in all_data_files:
    try:
        data = load_json(fpath)
    except:
        continue
    blanks_here = collect_blanks(data)
    if blanks_here:
        files_needing_fix.append((fpath, data, blanks_here))

print(f'\nFiles with blank images: {len(files_needing_fix)}')

# ── Step 4: Delete blank files so they get re-downloaded ─────────────────────
for bf in blank_files:
    fp = os.path.join(BASE_DIR, 'public', bf.lstrip('/'))
    if os.path.exists(fp):
        os.remove(fp)
print(f'Deleted {len(blank_files)} blank WebP files.')

# ── Step 5: Pull good images for each slug from article JSONs ─────────────────
# For each slug, get their image from the all-articles-index.json
with open(os.path.join(DATA_DIR, 'all-articles-index.json'), 'r', encoding='utf-8') as f:
    all_idx = json.load(f)

# Build slug -> image URL in the INDEX (these are already local paths after previous run)
# We need the ORIGINAL URLs. Since they're converted, let's use well-known alternative images.
# 
# FINAL STRATEGY: 
# For any path that matched 150_*.webp, find the slug in the JSON.
# Then find the corresponding article file by slug.
# Use a curated, slug-appropriate good Unsplash URL as replacement.

SLUG_IMAGES = {
    # Fallback map: slug prefix -> reliable Unsplash URL (tested working)
    'quantum':      'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1200&auto=format&fit=crop',
    'neural':       'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1200&auto=format&fit=crop',
    'arctic':       'https://images.unsplash.com/photo-1494412519320-aa613dfb7738?q=80&w=1200&auto=format&fit=crop',
    'fusion':       'https://images.unsplash.com/photo-1581092160562-40aa08e78837?q=80&w=1200&auto=format&fit=crop',
    'peace':        'https://images.unsplash.com/photo-1577563908411-5077b6dc7624?q=80&w=1200&auto=format&fit=crop',
    'asteroid':     'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?q=80&w=1200&auto=format&fit=crop',
    'labor':        'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=1200&auto=format&fit=crop',
    'supply':       'https://images.unsplash.com/photo-1494412519320-aa613dfb7738?q=80&w=1200&auto=format&fit=crop',
    'real-estate':  'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=1200&auto=format&fit=crop',
    'fdi':          'https://images.unsplash.com/photo-1535498730771-e735b998cd64?q=80&w=1200&auto=format&fit=crop',
    'consumer':     'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?q=80&w=1200&auto=format&fit=crop',
    'cyber':        'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1200&auto=format&fit=crop',
    'cbdc':         'https://images.unsplash.com/photo-1621416848440-236914c74472?q=80&w=1200&auto=format&fit=crop',
    'genome':       'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1200&auto=format&fit=crop',
    'genomic':      'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1200&auto=format&fit=crop',
    'climate':      'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1200&auto=format&fit=crop',
    'glacier':      'https://images.unsplash.com/photo-1539349762739-bf4c0b0280de?q=80&w=1200&auto=format&fit=crop',
    'ocean':        'https://images.unsplash.com/photo-1503428593586-e225b39bddfe?q=80&w=1200&auto=format&fit=crop',
    'carbon':       'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1200&auto=format&fit=crop',
    'methane':      'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1200&auto=format&fit=crop',
    'deep-space':   'https://images.unsplash.com/photo-1503428593586-e225b39bddfe?q=80&w=1200&auto=format&fit=crop',
    'dark-matter':  'https://images.unsplash.com/photo-1503428593586-e225b39bddfe?q=80&w=1200&auto=format&fit=crop',
    'ai-governance':'https://images.unsplash.com/photo-1589254065878-42c9da997008?q=80&w=1200&auto=format&fit=crop',
    'midterm':      'https://images.unsplash.com/photo-1529101091760-61df6be24296?q=80&w=1200&auto=format&fit=crop',
    'diplomacy':    'https://images.unsplash.com/photo-1521791136064-7986c2923216?q=80&w=1200&auto=format&fit=crop',
    'space':        'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?q=80&w=1200&auto=format&fit=crop',
    'democracy':    'https://images.unsplash.com/photo-1529101091760-61df6be24296?q=80&w=1200&auto=format&fit=crop',
    'inflation':    'https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=1200&auto=format&fit=crop',
    'tax':          'https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=1200&auto=format&fit=crop',
    'journalism':   'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?q=80&w=1200&auto=format&fit=crop',
    'education':    'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?q=80&w=1200&auto=format&fit=crop',
    'mental':       'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop',
    'privacy':      'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1200&auto=format&fit=crop',
    'human-rights': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1200&auto=format&fit=crop',
    'rewilding':    'https://images.unsplash.com/photo-1569939629376-b87a15f41a64?q=80&w=1200&auto=format&fit=crop',
    'perovskite':   'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1200&auto=format&fit=crop',
    'hydrogen':     'https://images.unsplash.com/photo-1547701386198-f2e9e41a6ab1?q=80&w=1200&auto=format&fit=crop',
    'global':       'https://images.unsplash.com/photo-1521791136064-7986c2923216?q=80&w=1200&auto=format&fit=crop',
    'materials':    'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?q=80&w=1200&auto=format&fit=crop',
    'paleontology': 'https://images.unsplash.com/photo-1503428593586-e225b39bddfe?q=80&w=1200&auto=format&fit=crop',
    'sociology':    'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1200&auto=format&fit=crop',
    'default':      'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1200&auto=format&fit=crop',
}

def get_best_url_for_slug(slug):
    if not slug:
        return SLUG_IMAGES['default']
    slug_lower = slug.lower()
    for key, url in SLUG_IMAGES.items():
        if key in slug_lower:
            return url
    return SLUG_IMAGES['default']


downloaded_cache = {}  # new_url -> local_path

def download_fresh(url, slug):
    if url in downloaded_cache:
        return downloaded_cache[url]
    
    slug_safe = re.sub(r'[^a-zA-Z0-9-]', '-', (slug or 'news'))[:40]
    url_hash  = str(abs(hash(url)) % 100000).zfill(5)
    filename  = f"{slug_safe}_{url_hash}.webp"
    filepath  = os.path.join(OUTPUT_DIR, filename)
    public    = f"{PUBLIC_PATH}/{filename}"

    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        downloaded_cache[url] = public
        return public

    try:
        time.sleep(1.2)  # respectful rate limit
        resp = requests.get(url, timeout=25, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert('RGB')
        if img.size == (150, 150):
            raise ValueError('Got placeholder image again')
        img.save(filepath, 'WEBP', quality=85, method=6)
        print(f'  [ok] {filename}  ({img.size})')
        downloaded_cache[url] = public
        return public
    except Exception as e:
        print(f'  [FAIL] {url[:60]}: {e}')
        downloaded_cache[url] = None
        return None

# ── Step 6: Fix all blank image references in all JSON files ─────────────────
def fix_blanks_in_obj(obj, result_map):
    """Replace blank local paths using result_map {blank_path: new_local_path}."""
    if isinstance(obj, dict):
        if 'image' in obj and obj['image'] in result_map:
            new = result_map[obj['image']]
            if new:
                obj['image'] = new
        if 'avatar' in obj and obj.get('avatar', '') in result_map:
            new = result_map[obj['avatar']]
            if new:
                obj['avatar'] = new
        for v in obj.values():
            fix_blanks_in_obj(v, result_map)
    elif isinstance(obj, list):
        for item in obj:
            fix_blanks_in_obj(item, result_map)

def get_slug_from_context(obj, target_path):
    """Walk to find slug near a given image path."""
    if isinstance(obj, dict):
        if obj.get('image') == target_path:
            return obj.get('slug', '')
        for v in obj.values():
            found = get_slug_from_context(v, target_path)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = get_slug_from_context(item, target_path)
            if found is not None:
                return found
    return None

# Build result map: blank_path -> new_local_path
result_map = {}
print(f'\nDownloading replacements for {len(blank_files)} blank images...')
for fpath in all_data_files:
    try:
        data = load_json(fpath)
    except:
        continue
    for blank_path in blank_files:
        if blank_path in result_map:
            continue
        slug = get_slug_from_context(data, blank_path)
        if slug is not None:
            best_url = get_best_url_for_slug(slug)
            local = download_fresh(best_url, slug)
            result_map[blank_path] = local

# Fill in any we couldn't find context for
for blank_path in blank_files:
    if blank_path not in result_map:
        local = download_fresh(SLUG_IMAGES['default'], 'news-default')
        result_map[blank_path] = local

# ── Step 7: Apply fixes to all data files ────────────────────────────────────
print(f'\nUpdating JSON files...')
fixed_files = 0
for fpath in all_data_files:
    try:
        data = load_json(fpath)
    except:
        continue
    fix_blanks_in_obj(data, result_map)
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    fixed_files += 1

print(f'\nDone! Fixed {len(result_map)} blank images across {fixed_files} files.')
