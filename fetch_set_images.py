"""
Fetch card art for new Wagic sets and write into per-set zip files.

Structure inside each {SET}.zip:
  {id}.jpg            — full card image  (618×882)
  thumbnails/{id}.jpg — thumbnail        (120×172)

Zip location: G:/Wagic-windows/User/sets/{SET}/{SET}.zip

Sources (in priority order):
  1. Scryfall API (multi-strategy search)
  2. Gatherer image endpoint (using official multiverse IDs)
  3. Skipped with a report
"""

import io, os, time, zipfile, requests
from PIL import Image

SETS_DIR     = "G:/Wagic-windows/User/sets"
CARD_W, CARD_H   = 618, 882
THUMB_W, THUMB_H = 120, 172
JPEG_QUALITY     = 88
SCRYFALL_DELAY   = 0.12   # ~8 req/s

# ── Card manifest ─────────────────────────────────────────────────────────────
# (set_code, wagic_id, card_name, scryfall_set_hint, gatherer_id)
# gatherer_id: official multiverse ID for Gatherer fallback (None = unknown)
CARDS = [
    # FIN — Magic: The Gathering — Final Fantasy
    ("FIN", 950001, "Starting Town",                "fin",  None),
    ("FIN", 950002, "Buster Sword",                 "fin",  None),
    ("FIN", 950003, "Vivi Ornitier",                "fin",  None),
    ("FIN", 950004, "The Earth Crystal",            "fin",  None),
    ("FIN", 950005, "Summon: Bahamut",              "fin",  None),

    # SPM — Marvel's Spider-Man
    ("SPM", 950101, "J. Jonah Jameson",             "spm",  None),
    ("SPM", 950102, "Electro, Assaulting Battery",  "spm",  None),

    # TLA — Avatar: The Last Airbender
    ("TLA", 950201, "Badgermole Cub",               "tla",  None),
    ("TLA", 950202, "Wan Shi Tong, Librarian",      "tla",  None),
    ("TLA", 950203, "Long Feng, Grand Secretariat", "tla",  None),
    ("TLA", 950204, "The Walls of Ba Sing Se",      "tla",  None),

    # TMT — Teenage Mutant Ninja Turtles (official Gatherer IDs provided)
    ("TMT", 910114, "Leonardo, Tactical Leader",    None,   910114),
    ("TMT", 910188, "April O'Neil, Live on the Scene", None, 910188),
    ("TMT", 910382, "Splinter's Wisdom",            None,   910382),
    ("TMT", 910412, "Pizza Party",                  None,   910412),
    ("TMT", 910500, "Sewer Pipe Omenpath",          None,   910500),

    # DFT — Aetherdrift new cards (official Gatherer IDs provided)
    ("DFT", 904105, "Finish Line Finisher",         None,   904105),
    ("DFT", 904218, "Speedway Siphon",              None,   904218),
    ("DFT", 904321, "Nitrous Blast",                None,   904321),
    ("DFT", 904330, "Gearshift Gremlins",           None,   904330),
    ("DFT", 904552, "High-Octane Harvester",        None,   904552),

    # ECL — Lorwyn Eclipsed (Mistbind Clique from LRW)
    ("ECL", 696873, "Mistbind Clique",              None,   None),

    # INR — corrected IDs; use INR-specific art
    ("INR", 892245, "Griselbrand",                  "inr",  892245),
    ("INR", 892112, "Avacyn, Angel of Hope",        "inr",  892112),
]

# ── Scryfall helpers ──────────────────────────────────────────────────────────

SF_NAMED  = "https://api.scryfall.com/cards/named"
SF_SEARCH = "https://api.scryfall.com/cards/search"

def _best_image_url(card_json, preferred_name=None):
    """Extract the best large image URL from a Scryfall card blob."""
    def pick(uris):
        return uris.get("large") or uris.get("normal") or uris.get("png")
    uris = card_json.get("image_uris")
    if uris:
        return pick(uris)
    faces = card_json.get("card_faces", [])
    if faces and preferred_name:
        pn = preferred_name.lower()
        for face in faces:
            if pn in face.get("name", "").lower() and "image_uris" in face:
                return pick(face["image_uris"])
    for face in faces:
        if "image_uris" in face:
            return pick(face["image_uris"])
    return None

def _sf_named(session, name, preferred=None):
    time.sleep(SCRYFALL_DELAY)
    r = session.get(SF_NAMED, params={"exact": name}, timeout=15)
    if r.status_code == 200:
        return _best_image_url(r.json(), preferred or name)
    return None

def _sf_search(session, query, preferred=None):
    time.sleep(SCRYFALL_DELAY)
    r = session.get(SF_SEARCH, params={"q": query, "unique": "cards"}, timeout=15)
    if r.status_code == 200:
        cards = r.json().get("data", [])
        if cards:
            return _best_image_url(cards[0], preferred)
    return None

def scryfall_url(session, name, set_hint=None):
    """Multi-strategy Scryfall image URL search."""
    # 1. Exact name with set hint
    if set_hint:
        r = session.get(SF_NAMED, params={"exact": name, "set": set_hint}, timeout=15)
        time.sleep(SCRYFALL_DELAY)
        if r.status_code == 200:
            return _best_image_url(r.json(), name)

    # 2. Exact name (any set)
    url = _sf_named(session, name)
    if url: return url

    # 3. First face of DFC
    if " // " in name:
        url = _sf_named(session, name.split(" // ")[0].strip(), name)
        if url: return url

    # 4. Strip commas/apostrophes
    import re
    clean = re.sub(r"[,'\u2019]", "", name)
    if clean != name:
        url = _sf_named(session, clean, name)
        if url: return url

    # 5. Fuzzy search
    url = _sf_search(session, f'name:"{name}"', name)
    if url: return url

    # 6. Set-scoped search
    if set_hint:
        url = _sf_search(session, f'name:"{name}" set:{set_hint}', name)
        if url: return url

    return None

def gatherer_url(gatherer_id):
    return (f"https://gatherer.wizards.com/Handlers/Image.ashx"
            f"?multiverseid={gatherer_id}&type=card")

# ── Image processing ──────────────────────────────────────────────────────────

def fetch_and_encode(url, session, target_w, target_h):
    """Download image, resize to target, return JPEG bytes or None."""
    try:
        r = session.get(url, timeout=30, headers={"User-Agent": "WagicImageTool/1.0"})
        if r.status_code != 200:
            return None
        ct = r.headers.get("Content-Type", "")
        if "html" in ct:      # Gatherer returns HTML error pages
            return None
        img = Image.open(io.BytesIO(r.content)).convert("RGB")
        img = img.resize((target_w, target_h), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=JPEG_QUALITY)
        return buf.getvalue()
    except Exception:
        return None

# ── Zip writer ────────────────────────────────────────────────────────────────

def write_to_zip(zip_path, entries):
    """entries: list of (filename_in_zip, bytes). Creates or appends."""
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    mode = "a" if os.path.exists(zip_path) else "w"
    with zipfile.ZipFile(zip_path, mode, zipfile.ZIP_STORED) as zf:
        existing = set(zf.namelist())
        for fname, data in entries:
            if fname not in existing:
                zf.writestr(fname, data)

# ── Main ──────────────────────────────────────────────────────────────────────

session = requests.Session()
session.headers.update({"User-Agent": "WagicImageTool/1.0"})

# Collect by set
by_set = {}   # set_code -> [(wagic_id, card_data, thumb_data)]
failures = []

for (set_code, wagic_id, name, sf_hint, gatherer_id) in CARDS:
    print(f"  {set_code}/{wagic_id}  {name} ...", end=" ", flush=True)

    # — Source 1: Scryfall —
    url = scryfall_url(session, name, sf_hint)
    source = "scryfall"

    # — Source 2: Gatherer (for cards with official IDs not yet on Scryfall) —
    if not url and gatherer_id:
        url = gatherer_url(gatherer_id)
        source = f"gatherer/{gatherer_id}"

    if not url:
        print("NO SOURCE FOUND")
        failures.append((set_code, wagic_id, name))
        continue

    # Download full card
    card_data = fetch_and_encode(url, session, CARD_W, CARD_H)
    if not card_data:
        # Gatherer may have blocked — log and skip
        print(f"download failed ({source})")
        failures.append((set_code, wagic_id, name))
        continue

    # Make thumbnail from same source
    thumb_data = fetch_and_encode(url, session, THUMB_W, THUMB_H)
    if not thumb_data:
        thumb_data = card_data   # fallback: resize the already-fetched card

    print(f"OK ({len(card_data)//1024}KB  {source})")
    by_set.setdefault(set_code, []).append((wagic_id, card_data, thumb_data))
    time.sleep(0.05)

# — Write zips —
print()
for set_code, entries in by_set.items():
    zip_path = os.path.join(SETS_DIR, set_code, f"{set_code}.zip")
    items = []
    for (wagic_id, card_data, thumb_data) in entries:
        items.append((f"{wagic_id}.jpg",            card_data))
        items.append((f"thumbnails/{wagic_id}.jpg", thumb_data))
    write_to_zip(zip_path, items)
    print(f"{set_code}.zip  {len(entries)} cards  -> {zip_path}")

# — Summary —
print()
if failures:
    print(f"FAILED ({len(failures)}):")
    for sc, wid, name in failures:
        print(f"  {sc}/{wid}  {name}")
else:
    print("All images written successfully.")
