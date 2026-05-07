"""
build_full_sets.py
==================
For each new set (FIN, TLA, SPM, TMT):
  1. Fetch the complete card list from Scryfall (all pages)
  2. Assign IDs:
       • FIN  — match Scryfall UUID to CardImageLinks.csv (real Gatherer IDs)
       • Others — allocate sequential placeholder IDs above FIN range
  3. Download card art at 618×882, generate 120×172 thumbnails
  4. Write images into G:/Wagic-windows/User/sets/{SET}/{SET}.zip
  5. Append new rows to CardImageLinks.csv
  6. Update Res/sets/{SET}/_cards.dat with the full card list
       - uses existing primitive if name found in mtg.txt; else the name itself
       - updates placeholder IDs we assigned earlier (950xxx etc.) to real IDs
"""

import io, os, re, time, zipfile, csv as csvmod, requests
from PIL import Image
from collections import defaultdict

# ── Config ────────────────────────────────────────────────────────────────────

SETS_DIR_GAME  = "G:/Wagic-windows/User/sets"          # zips written here
SETS_DIR_RES   = "M:/Claude_projects/wagic/projects/mtg/bin/Res/sets"
CSV_PATH       = "M:/Claude_projects/wagic-tools/CardImageLinks.csv"
PRIMITIVES_TXT = f"{SETS_DIR_RES}/primitives/mtg.txt"
PW_TXT         = f"{SETS_DIR_RES}/primitives/planeswalkers.txt"

CARD_W, CARD_H   = 618, 882
THUMB_W, THUMB_H = 120, 172
JPEG_Q           = 88
SF_DELAY         = 0.12

# Placeholder ID bases for sets without Gatherer IDs
# (above FIN's ~1141500 range; below Arena 2B range)
PLACEHOLDER_BASE = {
    "SPM": 1_500_001,   # 193 cards -> up to ~1500386
    "TLA": 1_510_001,   # 286 cards -> up to ~1510572
    "TMT": 1_520_001,   # 195 cards -> up to ~1520390
}

# Rarity map: Scryfall -> Wagic
RARITY = {"common": "C", "uncommon": "U", "rare": "R", "mythic": "M", "special": "R", "bonus": "R"}

# ── Scryfall ──────────────────────────────────────────────────────────────────

def fetch_all_cards(set_code):
    """Fetch every card (unique=cards) from a Scryfall set, all pages."""
    cards = []
    url = "https://api.scryfall.com/cards/search"
    params = {"q": f"set:{set_code}", "unique": "cards", "order": "set"}
    while url:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        d = r.json()
        cards.extend(d.get("data", []))
        url = d.get("next_page")
        params = {}
        time.sleep(SF_DELAY)
    return cards

def card_image_url(card):
    """Best large image URL from a Scryfall card JSON."""
    def pick(u): return u.get("large") or u.get("normal") or u.get("png")
    if "image_uris" in card:
        return pick(card["image_uris"])
    for face in card.get("card_faces", []):
        if "image_uris" in face:
            return pick(face["image_uris"])
    return None

def scryfall_uuid(card):
    """Scryfall card UUID (matches UUID in CDN URL)."""
    return card.get("id", "")

# ── CSV ───────────────────────────────────────────────────────────────────────

def load_csv_uuid_index(csv_path):
    """Returns dict: scryfall_uuid -> (wagic_id, url)  for all entries."""
    idx = {}
    with open(csv_path, encoding="utf-8") as f:
        next(f)  # header
        for line in f:
            parts = line.rstrip("\n").split(";")
            if len(parts) < 3:
                continue
            url = parts[2]
            uuid = url.rstrip("/").split("/")[-1].replace(".jpg", "")
            try:
                idx[uuid] = (int(parts[1]), parts[0], url)
            except ValueError:
                pass
    return idx

def append_csv(csv_path, rows):
    """Append (set_code, id, url) rows to CSV. Skips already-present IDs."""
    existing_ids = set()
    with open(csv_path, encoding="utf-8") as f:
        next(f)
        for line in f:
            parts = line.strip().split(";")
            if len(parts) >= 2:
                existing_ids.add(parts[1])

    added = 0
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        for (set_code, wagic_id, url) in rows:
            key = str(wagic_id)
            if key not in existing_ids:
                f.write(f"{set_code};{wagic_id};{url}\n")
                existing_ids.add(key)
                added += 1
    return added

# ── Primitives ────────────────────────────────────────────────────────────────

def load_primitive_names():
    """Return set of lowercase card names defined in mtg.txt / planeswalkers.txt."""
    names = set()
    pat = re.compile(r'^name=(.+)', re.IGNORECASE)
    for fpath in [PRIMITIVES_TXT, PW_TXT]:
        try:
            with open(fpath, encoding="utf-8", errors="ignore") as f:
                for line in f:
                    m = pat.match(line.strip())
                    if m:
                        names.add(m.group(1).strip().lower())
        except FileNotFoundError:
            pass
    return names

# ── Images ────────────────────────────────────────────────────────────────────

def download_resize(url, w, h, session):
    for attempt in range(3):
        try:
            r = session.get(url, timeout=30, headers={"User-Agent": "WagicImageTool/1.0"})
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 5)))
                continue
            if r.status_code != 200:
                return None
            ct = r.headers.get("Content-Type", "")
            if "html" in ct:
                return None
            img = Image.open(io.BytesIO(r.content)).convert("RGB")
            img = img.resize((w, h), Image.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=JPEG_Q)
            return buf.getvalue()
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
    return None

def update_zip(zip_path, entries):
    """entries: list of (filename_in_zip, bytes). Append mode."""
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    mode = "a" if os.path.exists(zip_path) else "w"
    with zipfile.ZipFile(zip_path, mode, zipfile.ZIP_STORED) as zf:
        existing = set(zf.namelist())
        for fname, data in entries:
            if fname not in existing:
                zf.writestr(fname, data)

# ── _cards.dat ────────────────────────────────────────────────────────────────

def load_existing_dat_ids(dat_path):
    """Return set of int IDs already in the _cards.dat."""
    ids = set()
    try:
        with open(dat_path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("id="):
                    try:
                        ids.add(int(line[3:]))
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    return ids

def update_cards_dat(dat_path, new_entries, old_total):
    """
    Append new [card] blocks. Updates total= in [meta].
    new_entries: list of (wagic_id, card_name, rarity, primitive_name)
    """
    if not new_entries:
        return 0
    blocks = "\n".join(
        f"[card]\nprimitive={prim}\nid={wid}\nrarity={rar}\n[/card]"
        for (wid, _, rar, prim) in new_entries
    )
    with open(dat_path, "a", encoding="utf-8") as f:
        f.write("\n" + blocks + "\n")

    new_total = old_thin = old_total + len(new_entries)
    # Update total= in meta
    with open(dat_path, encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(r'total=\d+', f'total={new_total}', content, count=1)
    with open(dat_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return len(new_entries)

def replace_placeholder_ids(dat_path, old_to_new):
    """Replace placeholder IDs with real IDs in _cards.dat. old_to_new: {old_id: new_id}"""
    if not old_to_new:
        return
    with open(dat_path, encoding="utf-8") as f:
        content = f.read()
    for old_id, new_id in old_to_new.items():
        content = content.replace(f"\nid={old_id}\n", f"\nid={new_id}\n")
    with open(dat_path, "w", encoding="utf-8") as f:
        f.write(content)

# ── Main ──────────────────────────────────────────────────────────────────────

print("Loading CSV UUID index...")
csv_idx = load_csv_uuid_index(CSV_PATH)
print(f"  {len(csv_idx):,} entries indexed")

print("Loading primitive names...")
prim_names = load_primitive_names()
print(f"  {len(prim_names):,} primitives known")

session = requests.Session()
session.headers.update({"User-Agent": "WagicImageTool/1.0"})

SETS = [
    ("FIN", "fin"),
    ("TLA", "tla"),
    ("SPM", "spm"),
    ("TMT", "tmt"),
]

for (set_code, sf_code) in SETS:
    print(f"\n{'='*60}")
    print(f"Processing {set_code}...")

    # 1. Fetch all cards
    print(f"  Fetching cards from Scryfall ({sf_code})...")
    all_cards = fetch_all_cards(sf_code)
    # Filter to non-token (tokens have layout='token' or type contains 'Token')
    cards = [c for c in all_cards
             if c.get("layout") not in ("token","emblem","art_series")
             and "Token" not in c.get("type_line","")
             and "Emblem" not in c.get("type_line","")]
    tokens = [c for c in all_cards if c not in cards]
    print(f"  Cards: {len(cards)}, tokens/other: {len(tokens)}")

    # 2. Assign IDs
    placeholder_base = PLACEHOLDER_BASE.get(set_code)
    placeholder_counter = placeholder_base or 0
    card_id_map = {}     # scryfall_id -> wagic_id
    old_to_new  = {}     # old placeholder id -> new real id
    no_id_count = 0

    # Known old placeholder IDs for this set (from our earlier _cards.dat entries)
    dat_path = f"{SETS_DIR_RES}/{set_code}/_cards.dat"
    existing_dat_ids = load_existing_dat_ids(dat_path)

    for card in cards:
        uuid = scryfall_uuid(card)
        csv_entry = csv_idx.get(uuid)
        if csv_entry:
            wagic_id = csv_entry[0]
        else:
            if placeholder_base is None:
                no_id_count += 1
                wagic_id = None
            else:
                wagic_id = placeholder_counter
                placeholder_counter += 1
        card_id_map[uuid] = wagic_id

    print(f"  IDs from CSV: {sum(1 for v in card_id_map.values() if v is not None and (placeholder_base is None or v < placeholder_base))}")
    print(f"  IDs allocated: {sum(1 for v in card_id_map.values() if v is not None and placeholder_base and v >= placeholder_base)}")
    if no_id_count:
        print(f"  WARNING: {no_id_count} cards could not be assigned an ID")

    # 3. Determine which cards need to be added to _cards.dat
    new_dat_entries = []
    for card in cards:
        uuid = scryfall_uuid(card)
        wagic_id = card_id_map.get(uuid)
        if wagic_id is None:
            continue
        if wagic_id in existing_dat_ids:
            continue  # already in dat

        # Check if primitive exists
        name = card["name"].split(" // ")[0].strip()  # front face name for DFCs
        prim = name if name.lower() in prim_names else name  # always use name; flag missing
        rar  = RARITY.get(card.get("rarity", "common"), "C")
        new_dat_entries.append((wagic_id, name, rar, prim))

    # 4. Find placeholder IDs to update (old 950xxx -> real IDs)
    if set_code == "FIN":
        # Map our 5 FIN placeholder cards by name to real IDs
        placeholder_by_name = {
            "Starting Town":    950001,
            "Buster Sword":     950002,
            "Vivi Ornitier":    950003,
            "The Earth Crystal":950004,
            "Summon: Bahamut":  950005,
        }
        for card in cards:
            name = card["name"].split(" // ")[0].strip()
            old_id = placeholder_by_name.get(name)
            if old_id:
                real_id = card_id_map.get(scryfall_uuid(card))
                if real_id and real_id != old_id:
                    old_to_new[old_id] = real_id

    # 5. Download images
    zip_path_game = f"{SETS_DIR_GAME}/{set_code}/{set_code}.zip"
    zip_entries = []
    ok = fail = skip = 0

    # Open existing zip to check what's already there
    existing_in_zip = set()
    if os.path.exists(zip_path_game):
        try:
            with zipfile.ZipFile(zip_path_game) as ez:
                existing_in_zip = set(ez.namelist())
        except Exception:
            pass

    total_to_dl = sum(1 for c in cards if card_id_map.get(scryfall_uuid(c)) is not None
                       and f"{card_id_map[scryfall_uuid(c)]}.jpg" not in existing_in_zip)
    print(f"  Downloading {total_to_dl} images (618×882)...")

    csv_new_rows = []
    for i, card in enumerate(cards):
        uuid = scryfall_uuid(card)
        wagic_id = card_id_map.get(uuid)
        if wagic_id is None:
            skip += 1
            continue

        full_fname  = f"{wagic_id}.jpg"
        thumb_fname = f"thumbnails/{wagic_id}.jpg"
        if full_fname in existing_in_zip:
            skip += 1
            continue

        img_url = card_image_url(card)
        if not img_url:
            fail += 1
            continue

        card_data = download_resize(img_url, CARD_W, CARD_H, session)
        if not card_data:
            fail += 1
            if (i+1) % 50 == 0:
                print(f"    {i+1}/{len(cards)} ok={ok} fail={fail} skip={skip}")
            continue

        thumb_data = download_resize(img_url, THUMB_W, THUMB_H, session)
        zip_entries.append((full_fname, card_data))
        zip_entries.append((thumb_fname, thumb_data or card_data))
        csv_new_rows.append((set_code, wagic_id, img_url))
        ok += 1
        time.sleep(0.05)

        if (i+1) % 25 == 0 or (i+1) == len(cards):
            print(f"    {i+1}/{len(cards)}  ok={ok}  fail={fail}  skip={skip}")

    # Tokens: download but only to zip (no _cards.dat entry needed)
    print(f"  Downloading {len(tokens)} token images...")
    tok_ok = 0
    for card in tokens:
        uuid = scryfall_uuid(card)
        csv_entry = csv_idx.get(uuid)
        if not csv_entry:
            continue
        wagic_id = csv_entry[0]
        fname = f"{wagic_id}.jpg"
        if fname in existing_in_zip:
            continue
        img_url = card_image_url(card)
        if not img_url:
            continue
        data = download_resize(img_url, CARD_W, CARD_H, session)
        if data:
            zip_entries.append((fname, data))
            csv_new_rows.append((set_code, wagic_id, img_url))
            tok_ok += 1
        time.sleep(0.05)
    print(f"    Tokens: {tok_ok} downloaded")

    # 6. Write zip
    if zip_entries:
        update_zip(zip_path_game, zip_entries)
        print(f"  Wrote {len(zip_entries)//2} images to {zip_path_game}")
    else:
        print(f"  No new images to write")

    # 7. Append to CSV
    added_csv = append_csv(CSV_PATH, csv_new_rows)
    print(f"  CSV: {added_csv} new rows added")

    # 8. Replace old placeholder IDs in _cards.dat
    if old_to_new:
        replace_placeholder_ids(dat_path, old_to_new)
        print(f"  Replaced {len(old_to_new)} placeholder IDs in _cards.dat:")
        for old, new in old_to_new.items():
            print(f"    {old} -> {new}")

    # 9. Append new cards to _cards.dat
    if os.path.exists(dat_path):
        with open(dat_path, encoding="utf-8") as f:
            content = f.read()
        current_total = int(re.search(r'total=(\d+)', content).group(1))
    else:
        current_total = 0
    added_dat = update_cards_dat(dat_path, new_dat_entries, current_total)
    print(f"  _cards.dat: {added_dat} new card entries added")

    # Missing primitive report (top 10)
    missing_prims = [(wid, name) for (wid, name, _, prim) in new_dat_entries
                     if name.lower() not in prim_names]
    if missing_prims:
        print(f"  Missing primitives ({len(missing_prims)} cards — will show generic art):")
        for (wid, name) in missing_prims[:10]:
            print(f"    {wid}  {name}")
        if len(missing_prims) > 10:
            print(f"    ... and {len(missing_prims)-10} more")

print("\n\nDone.")
