"""
assemble_apk.py  —  Assembles Wagic-unsigned.apk from ant + ndk-build outputs.

Run AFTER:
  1. ndk_build.bat  (produces libs/arm64-v8a/*.so)
  2. ant debug      (produces bin/Wagic.ap_ and bin/classes.dex — fails on APK step, that's OK)

Then run:
  python assemble_apk.py

Then sign with sign_apk.bat.
"""

import zipfile
import shutil
import os

BASE    = os.path.dirname(os.path.abspath(__file__))
BIN     = os.path.join(BASE, "bin")
LIBS    = os.path.join(BASE, "libs", "arm64-v8a")
DEXLIBS = os.path.join(BIN,  "dexedLibs")
WORK    = os.path.join(BIN,  "apk_work")
OUT     = os.path.join(WORK, "Wagic-unsigned.apk")

RES_APK  = os.path.join(BIN,  "Wagic.ap_")
DEX      = os.path.join(BIN,  "classes.dex")
LIBSDL   = os.path.join(LIBS, "libSDL.so")
LIBMAIN  = os.path.join(LIBS, "libmain.so")

for path, label in [(RES_APK, "Wagic.ap_"), (DEX, "classes.dex"),
                    (LIBSDL, "libSDL.so"), (LIBMAIN, "libmain.so")]:
    if not os.path.exists(path):
        print(f"ERROR: missing {label} at {path}")
        raise SystemExit(1)

os.makedirs(WORK, exist_ok=True)

# Remove old unsigned APK so we always produce a fresh file
if os.path.exists(OUT):
    os.remove(OUT)

print("Assembling", OUT)
with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as apk:
    # Resources (copy all entries from Wagic.ap_)
    with zipfile.ZipFile(RES_APK, "r") as res:
        for entry in res.infolist():
            apk.writestr(entry, res.read(entry.filename))
    print(f"  + resources from Wagic.ap_ ({len(zipfile.ZipFile(RES_APK).namelist())} entries)")

    # Dex (app classes)
    apk.write(DEX, "classes.dex")
    print(f"  + classes.dex")

    # Third-party library dex files (jsoup, json-simple, zip4j, ...).
    # ant pre-dexes each jar into bin/dexedLibs/<name>.jar with an internal
    # classes.dex.  ant's own apkbuilder step (which we replace here) is what
    # normally folds these in, so we must add them ourselves or their classes
    # (e.g. org.jsoup.*) are missing at runtime -> NoClassDefFoundError ->
    # the image downloader's slow scrape path crashes the whole app.
    # ART (API 21+) auto-loads secondary classes2.dex, classes3.dex, ...
    dex_index = 2
    if os.path.isdir(DEXLIBS):
        for jar in sorted(os.listdir(DEXLIBS)):
            if not jar.endswith(".jar"):
                continue
            jar_path = os.path.join(DEXLIBS, jar)
            with zipfile.ZipFile(jar_path, "r") as lib:
                if "classes.dex" not in lib.namelist():
                    print(f"  ! {jar} has no classes.dex, skipping")
                    continue
                entry = f"classes{dex_index}.dex"
                apk.writestr(entry, lib.read("classes.dex"))
                print(f"  + {entry}  (from {jar})")
                dex_index += 1
    if dex_index == 2:
        print("  ! WARNING: no dexedLibs added - jsoup/etc will be missing, "
              "the slow image-download path will fail at runtime")

    # Native libs
    apk.write(LIBSDL,  "lib/arm64-v8a/libSDL.so")
    apk.write(LIBMAIN, "lib/arm64-v8a/libmain.so")
    print(f"  + lib/arm64-v8a/libSDL.so")
    print(f"  + lib/arm64-v8a/libmain.so")

print(f"Done. Size: {os.path.getsize(OUT):,} bytes")
print(f"Now run sign_apk.bat to produce Wagic-debug.apk")
