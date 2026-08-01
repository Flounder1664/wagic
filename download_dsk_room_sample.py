"""
Download the Bottomless Pool // Locker Room (DSK) sample card image
from Scryfall and save it in Wagic format.

Full image -> Res/sets/DSK/673448.jpg
Thumbnail  -> Res/sets/DSK/thumbnails/673448.jpg (45x64)
"""
import io
import json
import os
import subprocess

from PIL import Image

DSK_DIR = r"M:\Claude_projects\wagic\projects\mtg\bin\Res\sets\DSK"
THUMB_DIR = os.path.join(DSK_DIR, "thumbnails")
CARD_ID = "673448"
CARD_NAME = "Bottomless Pool"
SET_CODE = "dsk"

os.makedirs(THUMB_DIR, exist_ok=True)

api_url = f"https://api.scryfall.com/cards/named?exact={CARD_NAME.replace(' ', '+')}&set={SET_CODE}"
proc = subprocess.run(
    ["curl", "-sL", "-A", "Wagic-Set-Tool/1.0", api_url],
    capture_output=True, check=True,
)
card = json.loads(proc.stdout)

if "image_uris" in card:
    img_url = card["image_uris"].get("normal", "")
elif "card_faces" in card and "image_uris" in card["card_faces"][0]:
    img_url = card["card_faces"][0]["image_uris"].get("normal", "")
else:
    raise SystemExit("No image found for card")

print(f"Downloading {img_url}")
img_proc = subprocess.run(
    ["curl", "-sL", "-A", "Wagic-Set-Tool/1.0", img_url],
    capture_output=True, check=True,
)
img_data = img_proc.stdout

full_path = os.path.join(DSK_DIR, f"{CARD_ID}.jpg")
with open(full_path, "wb") as f:
    f.write(img_data)
print(f"Saved {full_path} ({len(img_data)} bytes)")

img = Image.open(io.BytesIO(img_data))
thumb = img.resize((45, 64), Image.LANCZOS)
thumb_path = os.path.join(THUMB_DIR, f"{CARD_ID}.jpg")
thumb.save(thumb_path, "JPEG", quality=85)
print(f"Saved {thumb_path}")
