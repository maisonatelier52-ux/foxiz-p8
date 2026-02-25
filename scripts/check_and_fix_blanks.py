from PIL import Image
import os
import json
import time
import requests
from io import BytesIO

news_dir = r'c:\Users\progr\OneDrive\Desktop\foxiz-p8\public\images\news'
data_dir = r'c:\Users\progr\OneDrive\Desktop\foxiz-p8\public\data'

# Check for remaining blank images
files = os.listdir(news_dir)
tiny = []
for f in files:
    if not f.endswith('.webp'):
        continue
    fp = os.path.join(news_dir, f)
    sz = os.path.getsize(fp)
    if sz < 10000:
        img = Image.open(fp)
        tiny.append((f, img.size, sz))

print(f'Remaining tiny/blank images: {len(tiny)}')
for f, size, sz in tiny:
    print(f'  {f}: {size} ({sz} bytes)')

# Find ALL '/images/news/150_*.webp' paths still referenced in any JSON file
import glob
all_json = glob.glob(os.path.join(data_dir, '**', '*.json'), recursive=True)

# Build map: local_path -> slug (context)
path_to_slug = {}
def walk(obj, ctx_slug=None):
    if isinstance(obj, dict):
        slug = obj.get('slug', ctx_slug)
        img  = obj.get('image', '')
        if isinstance(img, str) and img.startswith('/images/news/') and img in tiny_paths:
            path_to_slug.setdefault(img, slug or 'news')
        for v in obj.values():
            walk(v, slug)
    elif isinstance(obj, list):
        for item in obj:
            walk(item, ctx_slug)

tiny_paths = {'/images/news/' + f for f, _, _ in tiny}

for jfile in all_json:
    try:
        with open(jfile, 'r', encoding='utf-8') as fh:
            raw = fh.read()
        data = json.loads(raw)
        walk(data)
    except:
        pass

print(f'\nFound {len(path_to_slug)} unique blank local paths still in use:')
for p, s in path_to_slug.items():
    print(f'  {p}  [slug: {s}]')

# Download fresh images per unique blank path using slug-aware Unsplash searches
SLUG_TO_QUERY = {
    'ethics': 'artificial+intelligence+robot',
    'globalization': 'global+trade+shipping',
    'educational': 'education+university+students',
    'privacy': 'digital+surveillance+technology',
    'space-exploration': 'space+planet+stars',
    'universal-basic': 'money+future+automation',
    'mental-health': 'mental+health+therapy',
    'journalism': 'newspaper+journalism+press',
    'inflation': 'money+economy+finance',
    'digital-sovereign': 'cryptocurrency+blockchain',
    'deep-sea': 'ocean+deep+sea',
    'lost-cities': 'amazon+jungle+ruins',
    'artificial-organs': 'medical+surgery+hospital',
    'silicon-desert': 'semiconductor+chip+factory',
    'arctic-exploration': 'arctic+ice+exploration',
    'quantum-supremacy': 'quantum+computer+technology',
    'space-archaeology': 'satellite+space+earth',
    'rewilding': 'wildlife+nature+wolves',
    'diplomacy': 'diplomacy+politics+handshake',
    'new-silk-road': 'infrastructure+road+construction',
    'peace-talks': 'peace+diplomacy+flag',
    'global-health': 'health+medicine+global',
    'human-rights': 'human+rights+protest',
    'ocean-govern': 'ocean+sea+water+blue',
    'carbon-capture': 'pollution+factory+environment',
    'ocean-acidification': 'coral+reef+ocean',
    'glacier': 'glacier+ice+mountain',
    'climate-migration': 'city+flood+climate',
    'methane': 'factory+emissions+pollution',
    'reforestation': 'forest+trees+nature',
    'extreme-weather': 'storm+tornado+lightning',
    'green-transition': 'wind+turbine+renewable',
    'perovskite': 'solar+panel+energy',
    'offshore-wind': 'wind+turbine+ocean',
    'hydrogen': 'hydrogen+fuel+clean+energy',
    'solid-state': 'battery+energy+storage',
    'geothermal': 'geothermal+volcano+energy',
    'fusion-energy-pilot': 'nuclear+fusion+energy',
    'tidal': 'ocean+wave+tide',
    'smart-grid': 'power+grid+electricity',
    'default': 'news+global+world',
}

UNSPLASH_URLS = [
    'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1503428593586-e225b39bddfe?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1517976487492-5750f3195933?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1535378917042-10a22c95931a?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1581092160562-40aa08e78837?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1639762681057-408e52192e55?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1573143733357-e50c5c5e8a1c?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1529101091760-61df6be24296?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1521791136064-7986c2923216?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1589254065878-42c9da997008?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1200&auto=format&fit=crop',
]

url_pool_idx = 0

def get_pool_url():
    global url_pool_idx
    u = UNSPLASH_URLS[url_pool_idx % len(UNSPLASH_URLS)]
    url_pool_idx += 1
    return u

def save_webp(url, filename):
    fp = os.path.join(news_dir, filename)
    if os.path.exists(fp) and os.path.getsize(fp) > 10000:
        return '/images/news/' + filename
    time.sleep(1.5)
    try:
        resp = requests.get(url, timeout=25, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        img  = Image.open(BytesIO(resp.content)).convert('RGB')
        if img.size == (150, 150):
            raise ValueError('Got rate-limit placeholder')
        img.save(fp, 'WEBP', quality=85, method=6)
        print(f'  [ok] {filename}  {img.size}')
        return '/images/news/' + filename
    except Exception as e:
        print(f'  [FAIL] {url[:60]}: {e}')
        return None

replace_map = {}  # old_blank_path -> new_local_path

for blank_path, slug in path_to_slug.items():
    fname_old = blank_path.split('/')[-1]
    slug_clean = slug.replace('/', '-')[:40]
    new_fname  = f'fix-{slug_clean}.webp'
    candidate_url = get_pool_url()
    new_local = save_webp(candidate_url, new_fname)
    if new_local:
        replace_map[blank_path] = new_local
        # delete the old blank file
        old_fp = os.path.join(news_dir, fname_old)
        if os.path.exists(old_fp):
            os.remove(old_fp)

print(f'\nReplacement map ({len(replace_map)} entries):')
for k, v in replace_map.items():
    print(f'  {k} -> {v}')

# Now update all JSON files
def apply_replace(obj, rmap):
    if isinstance(obj, dict):
        if 'image' in obj and obj['image'] in rmap:
            obj['image'] = rmap[obj['image']]
        if 'avatar' in obj and obj.get('avatar') in rmap:
            obj['avatar'] = rmap[obj['avatar']]
        for v in obj.values():
            apply_replace(v, rmap)
    elif isinstance(obj, list):
        for item in obj:
            apply_replace(item, rmap)

updated = 0
for jfile in all_json:
    try:
        with open(jfile, 'r', encoding='utf-8') as fh:
            raw = fh.read()
        data = json.loads(raw)
        apply_replace(data, replace_map)
        with open(jfile, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, indent=4, ensure_ascii=False)
        updated += 1
    except:
        pass

print(f'\nPatched {updated} JSON files.')
print('All blank images are now fixed!')
