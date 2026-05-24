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
    'sets/primitives/_macros.txt':
        os.path.join(_RES, "sets", "primitives", "_macros.txt"),
}

print(f'Rebuilding {CORE_ZIP} with updated primitives...')
replaced = set()

# Wagic's JGE zipFS scanfolder (zfsystem.cpp:328) looks up the folder name
# as an explicit entry in the zip's filemap. If "sets/" or "sets/<SET>/"
# aren't present as directory markers, scanfolder returns empty and Wagic
# loads zero sets. Collect every implicit parent path so we can emit
# directory markers for them.
parents = set()
with zipfile.ZipFile(CORE_ZIP, 'r') as zin:
    for info in zin.infolist():
        parts = info.filename.split('/')
        for i in range(1, len(parts)):
            parents.add('/'.join(parts[:i]) + '/')

with zipfile.ZipFile(CORE_ZIP, 'r') as zin, \
     zipfile.ZipFile(CORE_TMP, 'w', zipfile.ZIP_DEFLATED) as zout:
    written = set()
    # Emit directory markers first
    for parent in sorted(parents):
        zi = zipfile.ZipInfo(parent)
        zi.external_attr = (0o40755 << 16) | 0x10
        zout.writestr(zi, b'')
        written.add(parent)
    for item in zin.infolist():
        if item.filename in written:
            continue  # already wrote this as a dir marker
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
print(f'Done. Replaced {len(replaced)} file(s). Added {len(parents)} dir markers.')
print(f'New core.zip size: {os.path.getsize(CORE_ZIP):,} bytes')
