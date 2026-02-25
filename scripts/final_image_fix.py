"""
Final cleanup: 
- Re-download all remaining corrupt images (avatars + article images)
- Skip locked files gracefully
- Update all JSON paths
"""
from PIL import Image
import os, json, time, requests, glob, re
from io import BytesIO

BASE_DIR  = r'c:\Users\progr\OneDrive\Desktop\foxiz-p8'
NEWS_DIR  = os.path.join(BASE_DIR, 'public', 'images', 'news')
DATA_DIR  = os.path.join(BASE_DIR, 'public', 'data')
AVATAR_DIR = os.path.join(BASE_DIR, 'public', 'images', 'authors')
os.makedirs(AVATAR_DIR, exist_ok=True)

GOOD_AVATAR_URLS = [
    'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=200&auto=format&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=200&auto=format&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=200&auto=format&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=200&auto=format&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1568602471122-7832951cc4c5?q=80&w=200&auto=format&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=200&auto=format&fit=crop&crop=face',
    'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=200&auto=format&fit=crop&crop=face',
]
avatar_idx = 0

GOOD_NEWS_URLS = [
    'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1521791136064-7986c2923216?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1589254065878-42c9da997008?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1573143733357-e50c5c5e8a1c?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1529101091760-61df6be24296?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1200&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1200&auto=format&fit=crop',
]
news_idx = 0

def next_avatar_url():
    global avatar_idx
    u = GOOD_AVATAR_URLS[avatar_idx % len(GOOD_AVATAR_URLS)]
    avatar_idx += 1
    return u

def next_news_url():
    global news_idx
    u = GOOD_NEWS_URLS[news_idx % len(GOOD_NEWS_URLS)]
    news_idx += 1
    return u

def is_corrupt(filepath):
    try:
        sz = os.path.getsize(filepath)
        if sz < 8000:
            return True
        img = Image.open(filepath)
        w, h = img.size
        if w <= 200 and h <= 300 and sz < 8000:
            return True
        return False
    except:
        return True

def download_webp(url, out_path, is_avatar=False):
    time.sleep(1.2)
    try:
        resp = requests.get(url, timeout=25, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content)).convert('RGB')
        w, h = img.size
        if w <= 150 and h <= 150:
            raise ValueError('Got rate-limit placeholder again')
        img.save(out_path, 'WEBP', quality=85, method=6)
        print(f'  [ok] {os.path.basename(out_path)}  {img.size}')
        return True
    except Exception as e:
        print(f'  [FAIL] {url[:60]}: {e}')
        return False

def try_delete(path):
    try:
        os.remove(path)
        return True
    except PermissionError:
        print(f'  [locked] Cannot delete {os.path.basename(path)}, skipping')
        return False

# ── Scan all news images for corrupt ones ────────────────────────────────────
all_files = [f for f in os.listdir(NEWS_DIR) if f.endswith('.webp')]
corrupt = [f for f in all_files if is_corrupt(os.path.join(NEWS_DIR, f))]
print(f'Corrupt/blank news images: {len(corrupt)}')

# ── Build mapping old -> new for corrupt news images ─────────────────────────
replace_map = {}   # '/images/news/OLD.webp' -> '/images/news/NEW.webp'

# Avatar files are identified by small pixel dimensions  
# Re-download avatars with proper face-crop variant
# We'll put fixed avatars in /images/authors/
author_names = ['james-sinclair','leo-sterling','sarah-jenkins','robert-miller',
                'david-smith','emily-rodriguez','michael-chen','jessica-wu',
                'alex-thorne','james-oconnor','maria-sanchez']
author_map = {}  # author name fragment -> webp path

print('\nDownloading author avatars...')
for i, name in enumerate(author_names):
    out_path = os.path.join(AVATAR_DIR, f'{name}.webp')
    pub_path = f'/images/authors/{name}.webp'
    if os.path.exists(out_path) and not is_corrupt(out_path):
        author_map[name] = pub_path
        print(f'  [skip] {name}.webp (already ok)')
        continue
    url = GOOD_AVATAR_URLS[i % len(GOOD_AVATAR_URLS)]
    if download_webp(url, out_path, is_avatar=True):
        author_map[name] = pub_path

# For corrupt NEWS images (not avatars), build replacement map
print('\nFixing corrupt news images...')
for fname in corrupt:
    old_path = os.path.join(NEWS_DIR, fname)
    old_pub  = f'/images/news/{fname}'

    # Determine if it's an avatar-sized image
    try:
        img = Image.open(old_path)
        w, h = img.size
        is_avatar_size = (w <= 200 and h <= 350)
    except:
        is_avatar_size = False

    if is_avatar_size:
        # These are author avatars stored in news dir by mistake
        # Replace with the first available author avatar
        new_pub = f'/images/authors/{author_names[0]}.webp'
        replace_map[old_pub] = new_pub
        try_delete(old_path)
        print(f'  [avatar-fix] {fname} -> {author_names[0]}.webp')
    else:
        # Replace with a good news image
        new_fname = f'news-fix-{len(replace_map):03d}.webp'
        new_path  = os.path.join(NEWS_DIR, new_fname)
        new_pub   = f'/images/news/{new_fname}'
        url = next_news_url()
        if os.path.exists(new_path) and not is_corrupt(new_path):
            replace_map[old_pub] = new_pub
            try_delete(old_path)
        elif download_webp(url, new_path):
            replace_map[old_pub] = new_pub
            try_delete(old_path)

print(f'\nBuilt replace_map with {len(replace_map)} entries')

# ── Also fix avatar fields in article JSONs to point to /images/authors/ ─────
AUTHOR_NAME_TO_FILE = {
    'James Sinclair': 'james-sinclair',
    'Leo Sterling':   'leo-sterling',
    'Sarah Jenkins':  'sarah-jenkins',
    'Robert Miller':  'robert-miller',
    'David Smith':    'david-smith',
    'Emily Rodriguez':'emily-rodriguez',
    'Michael Chen':   'michael-chen',
    'Jessica Wu':     'jessica-wu',
    'Alex Thorne':    'alex-thorne',
    "James O'Connor": 'james-oconnor',
    'Maria Sanchez':  'maria-sanchez',
}

def fix_obj(obj):
    if isinstance(obj, dict):
        # Fix corrupt image paths
        if 'image' in obj and isinstance(obj['image'], str) and obj['image'] in replace_map:
            obj['image'] = replace_map[obj['image']]
        # Fix avatars by author name
        if 'author' in obj and isinstance(obj['author'], dict):
            author = obj['author']
            aname  = author.get('name', '')
            afile  = AUTHOR_NAME_TO_FILE.get(aname)
            if afile:
                new_av = f'/images/authors/{afile}.webp'
                if os.path.exists(os.path.join(AVATAR_DIR, f'{afile}.webp')):
                    author['avatar'] = new_av
        # Fix avatar field directly if it's a corrupt path
        if 'avatar' in obj and isinstance(obj['avatar'], str) and obj['avatar'] in replace_map:
            obj['avatar'] = replace_map[obj['avatar']]
        for v in obj.values():
            fix_obj(v)
    elif isinstance(obj, list):
        for item in obj:
            fix_obj(item)

# ── Apply fixes to all JSON files ─────────────────────────────────────────────
all_json = glob.glob(os.path.join(DATA_DIR, '**', '*.json'), recursive=True)
print(f'\nPatching {len(all_json)} JSON files...')
patched = 0
for jf in all_json:
    try:
        with open(jf, 'r', encoding='utf-8') as fh:
            raw = fh.read()
        try:
            data = json.loads(raw)
        except:
            data = json.loads(re.sub(r',\s*([}\]])', r'\1', raw))
        fix_obj(data)
        with open(jf, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, indent=4, ensure_ascii=False)
        patched += 1
    except Exception as e:
        print(f'  [skip] {os.path.basename(jf)}: {e}')

# Final tally
remaining = [f for f in os.listdir(NEWS_DIR) if f.endswith('.webp') and is_corrupt(os.path.join(NEWS_DIR, f))]
print(f'\nPatched {patched} files.')
print(f'Remaining corrupt news images: {len(remaining)}')
if remaining:
    for r in remaining:
        print(f'  {r} (may be locked by dev server - restart Next.js)')
else:
    print('All images are clean!')
