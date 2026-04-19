"""
Download ECL card images from Scryfall and save them in Wagic format.
Full size -> Res/sets/ECL/<id>.jpg
Thumbnails -> Res/sets/ECL/thumbnails/<id>.jpg (45x64)
"""
import json
import os
import re
import time
import urllib.request
from PIL import Image
import io

# --- Load Scryfall card data ---
cards = []
for f in ["M:/Claude_projects/wagic/ecl_scryfall_p1.json",
          "M:/Claude_projects/wagic/ecl_scryfall_p2.json"]:
    with open(f, encoding="utf-8") as fp:
        data = json.load(fp)
    cards.extend(data["data"])

# Build map: lowercase front name -> image URLs
scryfall_map = {}
for c in cards:
    name = c["name"].split(" // ")[0].strip().lower()
    if "image_uris" in c:
        scryfall_map[name] = {
            "normal": c["image_uris"].get("normal", ""),
            "small":  c["image_uris"].get("small", ""),
        }
    elif "card_faces" in c:
        # DFC: front face image
        face = c["card_faces"][0]
        if "image_uris" in face:
            scryfall_map[name] = {
                "normal": face["image_uris"].get("normal", ""),
                "small":  face["image_uris"].get("small", ""),
            }

print(f"Scryfall image map: {len(scryfall_map)} cards")

# --- Load _cards.dat: id -> primitive name ---
dat_path = "M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/ECL/_cards.dat"
with open(dat_path, "rb") as f:
    content = f.read().decode("utf-8", errors="ignore")

# Parse blocks
id_to_name = {}
blocks = re.findall(r'\[card\](.*?)\[/card\]', content, re.DOTALL)
for block in blocks:
    m_id = re.search(r'id=(\d+)', block)
    m_prim = re.search(r'primitive=(.+)', block)
    if m_id and m_prim:
        cid = m_id.group(1).strip()
        prim = m_prim.group(1).strip()
        # Front face name only
        front = prim.split(" // ")[0].strip()
        id_to_name[cid] = front

print(f"_cards.dat entries: {len(id_to_name)}")

# --- Set up output dirs ---
ecl_dir = "M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/ECL"
thumb_dir = os.path.join(ecl_dir, "thumbnails")
os.makedirs(thumb_dir, exist_ok=True)

# --- Download ---
headers = {"User-Agent": "Wagic-Set-Tool/1.0"}
downloaded = 0
skipped = 0
not_found = []

for cid, prim_name in sorted(id_to_name.items(), key=lambda x: int(x[0])):
    name_lower = prim_name.lower()

    # Check if already downloaded
    full_path = os.path.join(ecl_dir, f"{cid}.jpg")
    thumb_path = os.path.join(thumb_dir, f"{cid}.jpg")

    if os.path.exists(full_path) and os.path.exists(thumb_path):
        skipped += 1
        continue

    if name_lower not in scryfall_map:
        not_found.append(prim_name)
        continue

    img_url = scryfall_map[name_lower]["normal"]
    if not img_url:
        not_found.append(prim_name)
        continue

    try:
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            img_data = resp.read()

        # Save full size
        with open(full_path, "wb") as f:
            f.write(img_data)

        # Create thumbnail (45x64)
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((45, 64), Image.LANCZOS)
        img.save(thumb_path, "JPEG", quality=85)

        downloaded += 1
        if downloaded % 10 == 0:
            print(f"  [{downloaded}] Downloaded {prim_name} -> {cid}.jpg")

        time.sleep(0.05)  # 50ms between requests, ~20/sec

    except Exception as e:
        print(f"  ERROR {prim_name}: {e}")
        not_found.append(prim_name)

print(f"\nDone!")
print(f"  Downloaded: {downloaded}")
print(f"  Already existed (skipped): {skipped}")
print(f"  Not found / errors: {len(not_found)}")
if not_found:
    print("  Not found list:")
    for n in not_found:
        print(f"    {n}")
