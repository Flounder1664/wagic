"""
Patch core.zip to update sets/primitives/mtg.txt and sets/primitives/planeswalkers.txt
with the locally-modified versions.
"""
import zipfile, os, shutil

CORE_ZIP = 'M:/Claude_projects/wagic/projects/mtg/bin/Res/core.zip'
CORE_TMP = 'M:/Claude_projects/wagic/projects/mtg/bin/Res/core_tmp.zip'

REPLACEMENTS = {
    'sets/primitives/mtg.txt':
        'M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/primitives/mtg.txt',
    'sets/primitives/planeswalkers.txt':
        'M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/primitives/planeswalkers.txt',
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
