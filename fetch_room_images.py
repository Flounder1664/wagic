"""
Fetch all DSK + DSC Room cards from Scryfall: oracle text JSON dump + images.

Maps each `primitive=<Name>` entry in projects/mtg/bin/Res/sets/<SET>/_cards.dat
to its Scryfall record, then:

  - Saves card data (both faces, oracle text, mana cost, image URLs) to
    `room_card_data.json` for later use when encoding primitives.
  - Downloads `image_uris.normal` (front face for split cards) to
    `Res/sets/<SET>/<id>.jpg` and a 45x64 thumbnail to
    `Res/sets/<SET>/thumbnails/<id>.jpg`.

Uses curl via subprocess because the bundled Python 3.14 urllib has TLS
handshake quirks against api.scryfall.com (same workaround as
`download_dsk_room_sample.py`).
"""
import io
import json
import os
import re
import subprocess
import time

from PIL import Image

REPO = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(REPO, "projects", "mtg", "bin", "Res")

# Which sets to scan _cards.dat for Room entries.
SETS = ["DSK", "DSC"]

UA = "Wagic-Set-Tool/1.0"
OUT_JSON = os.path.join(REPO, "room_card_data.json")


def list_rooms(set_code):
    """Return list of (id, primitive_name) for Rooms (split-name cards) in <set>/_cards.dat."""
    path = os.path.join(RES, "sets", set_code, "_cards.dat")
    with open(path, "rb") as f:
        text = f.read().decode("utf-8", errors="ignore")
    rooms = []
    for block in re.findall(r"\[card\](.+?)\[/card\]", text, re.DOTALL):
        m_prim = re.search(r"primitive=([^\r\n]+)", block)
        m_id = re.search(r"id=(\d+)", block)
        if not (m_prim and m_id):
            continue
        name = m_prim.group(1).strip()
        if " // " not in name:
            continue  # not a split card; skip
        rooms.append((m_id.group(1).strip(), name))
    # Dedupe (DSK has the same Room listed forward and back-face)
    seen = set()
    unique = []
    for cid, name in rooms:
        front = name.split(" // ")[0].strip().lower()
        if front in seen:
            continue
        seen.add(front)
        unique.append((cid, name))
    return unique


def scryfall_named(front_name, set_code):
    url = (
        "https://api.scryfall.com/cards/named?exact="
        + front_name.replace(" ", "+").replace("'", "%27")
        + "&set="
        + set_code.lower()
    )
    proc = subprocess.run(
        ["curl", "-sL", "-A", UA, url], capture_output=True, check=True
    )
    return json.loads(proc.stdout)


def download(url):
    proc = subprocess.run(
        ["curl", "-sL", "-A", UA, url], capture_output=True, check=True
    )
    return proc.stdout


def main():
    all_data = {}
    for set_code in SETS:
        rooms = list_rooms(set_code)
        print(f"\n=== {set_code}: {len(rooms)} Rooms in _cards.dat ===")
        set_dir = os.path.join(RES, "sets", set_code)
        thumb_dir = os.path.join(set_dir, "thumbnails")
        os.makedirs(thumb_dir, exist_ok=True)

        for cid, name in rooms:
            front = name.split(" // ")[0].strip()
            try:
                card = scryfall_named(front, set_code)
            except Exception as e:
                print(f"  [{cid}] {name}: FETCH ERROR {e}")
                continue
            if card.get("object") == "error":
                print(f"  [{cid}] {name}: Scryfall says {card.get('details')}")
                continue

            # Capture both faces' oracle text + costs
            faces = []
            if "card_faces" in card:
                for face in card["card_faces"]:
                    faces.append({
                        "name": face.get("name", ""),
                        "mana_cost": face.get("mana_cost", ""),
                        "oracle_text": face.get("oracle_text", ""),
                        "type_line": face.get("type_line", ""),
                    })
            else:
                faces.append({
                    "name": card.get("name", ""),
                    "mana_cost": card.get("mana_cost", ""),
                    "oracle_text": card.get("oracle_text", ""),
                    "type_line": card.get("type_line", ""),
                })

            # Image URL: prefer card-level image_uris, fall back to front face
            img_url = ""
            if "image_uris" in card:
                img_url = card["image_uris"].get("normal", "")
            elif "card_faces" in card and "image_uris" in card["card_faces"][0]:
                img_url = card["card_faces"][0]["image_uris"].get("normal", "")

            all_data[cid] = {
                "set": set_code,
                "primitive": name,
                "scryfall_name": card.get("name", ""),
                "faces": faces,
                "image_url": img_url,
            }

            full_path = os.path.join(set_dir, f"{cid}.jpg")
            thumb_path = os.path.join(thumb_dir, f"{cid}.jpg")

            if os.path.exists(full_path) and os.path.exists(thumb_path):
                print(f"  [{cid}] {name}: data captured, image already present")
            elif img_url:
                try:
                    img_data = download(img_url)
                    with open(full_path, "wb") as f:
                        f.write(img_data)
                    img = Image.open(io.BytesIO(img_data))
                    thumb = img.resize((45, 64), Image.LANCZOS)
                    thumb.save(thumb_path, "JPEG", quality=85)
                    print(f"  [{cid}] {name}: downloaded {len(img_data)} bytes")
                    time.sleep(0.1)  # Scryfall etiquette
                except Exception as e:
                    print(f"  [{cid}] {name}: IMAGE ERROR {e}")
            else:
                print(f"  [{cid}] {name}: no image URL")

            time.sleep(0.05)  # request throttle

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {OUT_JSON} ({len(all_data)} cards)")


if __name__ == "__main__":
    main()
