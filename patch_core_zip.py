"""
Patch core.zip to update sets/primitives/mtg.txt and sets/primitives/planeswalkers.txt
with the locally-modified versions.
"""
import zipfile, os, shutil

_REPO = os.path.dirname(os.path.abspath(__file__))
_RES  = os.path.join(_REPO, "projects", "mtg", "bin", "Res")

CORE_ZIP = os.path.join(_RES, "core.zip")
CORE_TMP = os.path.join(_RES, "core_tmp.zip")

REPLACEMENTS = {
    'sets/primitives/mtg.txt':
        os.path.join(_RES, "sets", "primitives", "mtg.txt"),
    'sets/primitives/planeswalkers.txt':
        os.path.join(_RES, "sets", "primitives", "planeswalkers.txt"),
    'sets/primitives/borderline.txt':
        os.path.join(_RES, "sets", "primitives", "borderline.txt"),
    'sets/primitives/unsupported.txt':
        os.path.join(_RES, "sets", "primitives", "unsupported.txt"),
    'sets/primitives/_macros.txt':
        os.path.join(_RES, "sets", "primitives", "_macros.txt"),
}

print(f'Rebuilding {CORE_ZIP} with updated primitives...')
replaced = set()

with zipfile.ZipFile(CORE_ZIP, 'r') as zin, \
     zipfile.ZipFile(CORE_TMP, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename in REPLACEMENTS:
            local_path = REPLACEMENTS[item.filename]
            with open(local_path, 'rb') as f:
                data = f.read()
            zout.writestr(item, data)
            replaced.add(item.filename)
            print(f'  Replaced: {item.filename} ({len(data):,} bytes)')
        else:
            data = zin.read(item.filename)
            zout.writestr(item, data)

os.replace(CORE_TMP, CORE_ZIP)
print(f'Done. Replaced {len(replaced)} file(s).')
print(f'New core.zip size: {os.path.getsize(CORE_ZIP):,} bytes')
