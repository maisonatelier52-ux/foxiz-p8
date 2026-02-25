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

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Fallback image pool (known-working Unsplash IDs) ─────────────────────────
FALLBACKS = [
    "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1503428593586-e225b39bddfe?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1559027615-cd4628902d4a?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517976487492-5750f3195933?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1535378917042-10a22c95931a?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1581092160562-40aa08e78837?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1639762681057-408e52192e55?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1624996379697-f01d168b1a52?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1200&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?q=80&w=1200&auto=format&fit=crop",
]
fallback_idx = 0

# ── JSON fixer ────────────────────────────────────────────────────────────────
def load_json_lenient(path):
    """Load JSON, fixing trailing commas if needed."""
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Remove trailing commas before } or ]
        fixed = re.sub(r',\s*([}\]])', r'\1', raw)
        return json.loads(fixed)

# ── Image download & convert ──────────────────────────────────────────────────
url_cache = {}

def slug_from_url(url):
    parsed_path = [p for p in url.split('/') if p]
    name = parsed_path[-1].split('?')[0][:40] if parsed_path else 'img'
    name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
    return name or 'img'

def get_next_fallback():
    global fallback_idx
    url = FALLBACKS[fallback_idx % len(FALLBACKS)]
    fallback_idx += 1
    return url

def download_and_convert(url):
    global fallback_idx
    if url in url_cache:
        return url_cache[url]

    # Skip already-local paths
    if url.startswith('/'):
        url_cache[url] = url
        return url

    short    = slug_from_url(url)
    url_hash = str(abs(hash(url)) % 100000).zfill(5)
    filename = f"{short}_{url_hash}.webp"
    filepath = os.path.join(OUTPUT_DIR, filename)
    public   = f"{PUBLIC_PATH}/{filename}"

    if os.path.exists(filepath):
        url_cache[url] = public
        return public

    def try_download(target_url):
        resp = requests.get(target_url, timeout=20)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert('RGB')
        img.save(filepath, 'WEBP', quality=82, method=6)
        return True

    try:
        try_download(url)
        print(f"  [ok]   {filename}")
        url_cache[url] = public
        time.sleep(0.05)
        return public
    except Exception:
        # Try fallback
        fallback_url = get_next_fallback()
        fb_short    = slug_from_url(fallback_url)
        fb_hash     = str(abs(hash(fallback_url)) % 100000).zfill(5)
        fb_filename = f"{fb_short}_{fb_hash}.webp"
        fb_filepath = os.path.join(OUTPUT_DIR, fb_filename)
        fb_public   = f"{PUBLIC_PATH}/{fb_filename}"

        if not os.path.exists(fb_filepath):
            try:
                try_download(fallback_url)
                print(f"  [fallback] {url[:50]} -> {fb_filename}")
            except Exception as e2:
                print(f"  [FAIL] {url[:50]} and fallback failed: {e2}")
                url_cache[url] = url
                return url
        else:
            print(f"  [fallback-cached] {url[:50]} -> {fb_filename}")
        url_cache[url] = fb_public
        return fb_public

def replace_images(obj):
    if isinstance(obj, dict):
        if 'image' in obj and isinstance(obj['image'], str):
            obj['image'] = download_and_convert(obj['image'])
        if 'avatar' in obj and isinstance(obj['avatar'], str) and obj['avatar'].startswith('http'):
            obj['avatar'] = download_and_convert(obj['avatar'])
        for v in obj.values():
            replace_images(v)
    elif isinstance(obj, list):
        for item in obj:
            replace_images(item)

# ── Run through all data files ────────────────────────────────────────────────
DATA_FILES = [
    'more-news.json',
    'home-hero.json',
    'featured-stories.json',
    'news-strip.json',
    'just-in.json',
    'business.json',
    'what-to-read.json',
    'latest-news.json',
    'all-articles-index.json',
]

for fname in DATA_FILES:
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        continue
    print(f"\n== {fname} ==")
    data = load_json_lenient(path)
    replace_images(data)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ── Individual article files ──────────────────────────────────────────────────
print(f"\n== articles/ ==")
for fname in sorted(os.listdir(ARTICLES_DIR)):
    if not fname.endswith('.json'):
        continue
    path = os.path.join(ARTICLES_DIR, fname)
    try:
        data = load_json_lenient(path)
    except Exception as e:
        print(f"  [SKIP-PARSE] {fname}: {e}")
        continue
    replace_images(data)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

downloaded = sum(1 for v in url_cache.values() if v.startswith('/images'))
print(f"\nDone! {downloaded} images converted to WebP and saved to /public/images/news/")
