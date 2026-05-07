"""
Download card art from Scryfall and package into per-set zips.
Image path in zip: {ID}.jpg  (matches Wagic's getImageName() == "{mtgid}.jpg")
Zip path:         Res/sets/{SET}/{SET}.zip
"""

import os, time, zipfile, io, requests

SETS_DIR = "M:/Claude_projects/wagic/projects/mtg/bin/Res/sets"
IMAGE_SIZE = "normal"   # 488×680 — good balance for Wagic

# ── Card manifest ────────────────────────────────────────────────────────────
# (set_code, wagic_id, scryfall_name, scryfall_set_hint)
# scryfall_set_hint=None → search any printing
CARDS = [
    # FIN — Magic: The Gathering — Final Fantasy
    ("FIN", 950001, "Starting Town",               "fin"),
    ("FIN", 950002, "Buster Sword",                "fin"),
    ("FIN", 950003, "Vivi Ornitier",               "fin"),
    ("FIN", 950004, "The Earth Crystal",           "fin"),
    ("FIN", 950005, "Summon: Bahamut",             "fin"),

    # SPM — Marvel's Spider-Man
    ("SPM", 950101, "J. Jonah Jameson",            "spm"),
    ("SPM", 950102, "Electro, Assaulting Battery", "spm"),

    # TLA — Avatar: The Last Airbender
    ("TLA", 950201, "Badgermole Cub",              "tla"),
    ("TLA", 950202, "Wan Shi Tong, Librarian",     "tla"),
    ("TLA", 950203, "Long Feng, Grand Secretariat","tla"),
    ("TLA", 950204, "The Walls of Ba Sing Se",     "tla"),

    # TMT — Teenage Mutant Ninja Turtles (not indexed on Scryfall — try any printing)
    ("TMT", 910114, "Leonardo, Tactical Leader",   None),
    ("TMT", 910188, "April O'Neil, Live on the Scene", None),
    ("TMT", 910382, "Splinter's Wisdom",           None),
    ("TMT", 910412, "Pizza Party",                 None),
    ("TMT", 910500, "Sewer Pipe Omenpath",         None),

    # DFT — Aetherdrift new cards (not indexed on Scryfall — try any printing)
    ("DFT", 904105, "Finish Line Finisher",        None),
    ("DFT", 904218, "Speedway Siphon",             None),
    ("DFT", 904321, "Nitrous Blast",               None),
    ("DFT", 904330, "Gearshift Gremlins",          None),
    ("DFT", 904552, "High-Octane Harvester",       None),

    # ECL — Lorwyn Eclipsed (Mistbind Clique reprinted from LRW)
    ("ECL", 696873, "Mistbind Clique",             None),

    # INR — corrected IDs (use INR printing art where possible)
    ("INR", 892245, "Griselbrand",                 "inr"),
    ("INR", 892112, "Avacyn, Angel of Hope",       "inr"),
]

# ── Scryfall helpers ──────────────────────────────────────────────────────────

def fetch_card(name, set_hint):
    """Return Scryfall card JSON, trying set_hint first then any printing."""
    base = "https://api.scryfall.com/cards/named"
    if set_hint:
        r = requests.get(base, params={"exact": name, "set": set_hint}, timeout=15)
        if r.status_code == 200:
            return r.json()
    # fallback: any printing
    r = requests.get(base, params={"fuzzy": name}, timeout=15)
    if r.status_code == 200:
        return r.json()
    return None


def image_url(card_json):
    """Extract the best available image URL from a card JSON blob."""
    uris = card_json.get("image_uris")
    if uris:
        return uris.get(IMAGE_SIZE) or uris.get("normal") or uris.get("large")
    # double-faced card — use front face
    faces = card_json.get("card_faces", [])
    if faces:
        face_uris = faces[0].get("image_uris", {})
        return face_uris.get(IMAGE_SIZE) or face_uris.get("normal")
    return None


def download_image(url):
    """Download image bytes from url. Returns bytes or None."""
    r = requests.get(url, timeout=30)
    if r.status_code == 200 and "image" in r.headers.get("Content-Type", ""):
        return r.content
    return None

# ── Main ──────────────────────────────────────────────────────────────────────

# Collect images grouped by set
results = {}   # set_code -> [(wagic_id, image_bytes_or_None, card_name)]
failures = []

for (set_code, wagic_id, card_name, set_hint) in CARDS:
    print(f"  {set_code}/{wagic_id}  {card_name} ...", end=" ", flush=True)

    card = fetch_card(card_name, set_hint)
    if not card:
        print("NOT FOUND on Scryfall")
        failures.append((set_code, wagic_id, card_name, "card not found"))
        results.setdefault(set_code, []).append((wagic_id, None, card_name))
        continue

    url = image_url(card)
    if not url:
        print(f"no image URL (type={card.get('layout')})")
        failures.append((set_code, wagic_id, card_name, "no image URL"))
        results.setdefault(set_code, []).append((wagic_id, None, card_name))
        continue

    img = download_image(url)
    if not img:
        print("download failed")
        failures.append((set_code, wagic_id, card_name, "download failed"))
        results.setdefault(set_code, []).append((wagic_id, None, card_name))
        continue

    print(f"OK ({len(img)//1024}KB, set={card.get('set','?')})")
    results.setdefault(set_code, []).append((wagic_id, img, card_name))
    time.sleep(0.1)   # Scryfall rate limit: ~10 req/s

# ── Write per-set zips ────────────────────────────────────────────────────────
print()
for set_code, entries in results.items():
    zip_path = os.path.join(SETS_DIR, set_code, f"{set_code}.zip")
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)

    # Open existing zip for append, or create new
    mode = "a" if os.path.exists(zip_path) else "w"
    written = 0
    skipped = 0
    with zipfile.ZipFile(zip_path, mode, zipfile.ZIP_STORED) as zf:
        existing = set(zf.namelist())
        for (wagic_id, img_bytes, card_name) in entries:
            fname = f"{wagic_id}.jpg"
            if img_bytes is None:
                skipped += 1
                continue
            if fname in existing:
                print(f"  {set_code}/{fname}  already in zip, skipping")
                skipped += 1
                continue
            zf.writestr(fname, img_bytes)
            written += 1

    print(f"{set_code}.zip  written={written}  skipped/missing={skipped}  path={zip_path}")

# ── Summary ───────────────────────────────────────────────────────────────────
print()
if failures:
    print(f"FAILURES ({len(failures)}):")
    for (sc, wid, name, reason) in failures:
        print(f"  {sc}/{wid}  {name}  — {reason}")
else:
    print("All images fetched successfully.")
