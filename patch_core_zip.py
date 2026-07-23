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

# Brand-new entries to inject (files that don't yet exist in core.zip, e.g.
# a new set's _cards.dat). Directory markers for their parents are emitted
# automatically below so JGE scanfolder finds the set.
ADD_FILES = {
    'sets/SOS/_cards.dat':
        os.path.join(_RES, "sets", "SOS", "_cards.dat"),
    'packs/draft_booster.txt':
        os.path.join(_RES, "packs", "draft_booster.txt"),
}
# 2026-07-19 intake: 6 previously-missing sets, register-only reprints.
for _code in ("FIC", "UNF", "EOC", "EOS", "GN3", "FCA", "HOB", "HOC"):
    ADD_FILES['sets/%s/_cards.dat' % _code] = os.path.join(_RES, "sets", _code, "_cards.dat")

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
# Also collect parents for the brand-new files we're injecting.
for arcname in ADD_FILES:
    parts = arcname.split('/')
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
        if item.filename in REPLACEMENTS or item.filename in ADD_FILES:
            local_path = REPLACEMENTS.get(item.filename) or ADD_FILES[item.filename]
            with open(local_path, 'rb') as f:
                data = f.read()
            zout.writestr(item, data)
            replaced.add(item.filename)
            written.add(item.filename)  # so ADD_FILES doesn't double-write
            print(f'  Replaced: {item.filename} ({len(data):,} bytes)')
        else:
            data = zin.read(item.filename)
            zout.writestr(item, data)
    # Inject brand-new files that weren't already present in core.zip.
    added = set()
    for arcname, local_path in ADD_FILES.items():
        if arcname in written:
            continue
        with open(local_path, 'rb') as f:
            data = f.read()
        zout.writestr(arcname, data)
        added.add(arcname)
        print(f'  Added: {arcname} ({len(data):,} bytes)')

os.replace(CORE_TMP, CORE_ZIP)
print(f'Done. Replaced {len(replaced)} file(s). Added {len(added)} new file(s). {len(parents)} dir markers.')
print(f'New core.zip size: {os.path.getsize(CORE_ZIP):,} bytes')
