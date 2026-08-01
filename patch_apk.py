"""
Patch Wagic-debug.apk by replacing EVERY freshly-built native lib under
lib/arm64-v8a/ (libmain.so, libSDL.so, ...) with the on-disk build output,
then zipalign and re-sign with debug key.

Replacing only libmain.so (the old behaviour) left a stale libSDL.so in the
APK — which is how the Android 15+ 16KB-alignment warning survived a rebuild
of libmain even after the linker flag was added. Any lib not rebuilt on disk
is passed through unchanged.
"""
import os
import shutil
import subprocess
import zipfile
import io
from wagic_build_config import BUILD_TOOLS, DEBUG_KEY, DEBUG_KEY_PASS

_REPO    = os.path.dirname(os.path.abspath(__file__))
_ANDROID = os.path.join(_REPO, "projects", "mtg", "Android")

APK_IN      = os.path.join(_ANDROID, "bin", "Wagic-debug.apk")
APK_WORK    = os.path.join(_ANDROID, "bin", "Wagic-debug-patched.apk")
APK_ALIGNED = os.path.join(_ANDROID, "bin", "Wagic-debug-aligned.apk")
LIBDIR      = os.path.join(_ANDROID, "libs", "arm64-v8a")

ZIPALIGN  = os.path.join(BUILD_TOOLS, "zipalign.exe")
APKSIGNER = os.path.join(BUILD_TOOLS, "apksigner.bat")

# Map every built lib/arm64-v8a/*.so that also exists in the APK.
print("Reading freshly-built native libs...")
new_libs = {}
for fn in sorted(os.listdir(LIBDIR)):
    if fn.endswith(".so"):
        with open(os.path.join(LIBDIR, fn), "rb") as f:
            new_libs["lib/arm64-v8a/" + fn] = f.read()
        print(f"  {fn}: {len(new_libs['lib/arm64-v8a/' + fn]):,} bytes")

# Step 2: Rebuild APK zip, replacing each matching lib
print("Rebuilding APK...")
replaced = set()
with zipfile.ZipFile(APK_IN, 'r') as zin, \
     zipfile.ZipFile(APK_WORK, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename in new_libs:
            print(f"  Replacing: {item.filename}")
            zout.writestr(item, new_libs[item.filename])
            replaced.add(item.filename)
        else:
            # Preserve original compression
            data = zin.read(item.filename)
            zout.writestr(item, data)
missing = set(new_libs) - replaced
if missing:
    print("  NOTE: built but not present in APK (skipped):", ", ".join(sorted(missing)))
print(f"  Done rebuilding. Replaced {len(replaced)} lib(s).")

# Step 3: zipalign
if os.path.exists(APK_ALIGNED):
    os.remove(APK_ALIGNED)
print("Running zipalign...")
r = subprocess.run([ZIPALIGN, "-f", "4", APK_WORK, APK_ALIGNED],
                   capture_output=True, text=True)
if r.returncode != 0:
    print("ZIPALIGN FAILED:", r.stderr, r.stdout)
    exit(1)
print("  zipalign done.")

# Step 4: apksigner sign with debug keystore
print("Signing with debug key...")
r = subprocess.run([
    APKSIGNER, "sign",
    "--ks", DEBUG_KEY,
    "--ks-pass", f"pass:{DEBUG_KEY_PASS}",
    "--key-pass", f"pass:{DEBUG_KEY_PASS}",
    "--out", APK_IN,
    APK_ALIGNED
], capture_output=True, text=True)
print(r.stdout)
if r.returncode != 0:
    print("APKSIGNER FAILED:", r.stderr)
    exit(1)
print("  Signed APK written to:", APK_IN)

# Cleanup
os.remove(APK_WORK)
os.remove(APK_ALIGNED)

print("\nDone! APK is ready at:", APK_IN)
