"""
Patch Wagic-debug.apk by replacing lib/arm64-v8a/libmain.so,
then zipalign and re-sign with debug key.
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
LIBMAIN     = os.path.join(_ANDROID, "libs", "arm64-v8a", "libmain.so")

ZIPALIGN  = os.path.join(BUILD_TOOLS, "zipalign.exe")
APKSIGNER = os.path.join(BUILD_TOOLS, "apksigner.bat")

REPLACE_ENTRY = "lib/arm64-v8a/libmain.so"

# Step 1: Read new libmain.so bytes
print("Reading new libmain.so...")
with open(LIBMAIN, "rb") as f:
    new_so_bytes = f.read()
print(f"  {len(new_so_bytes):,} bytes")

# Step 2: Rebuild APK zip, replacing libmain.so
print(f"Rebuilding APK, replacing {REPLACE_ENTRY}...")
with zipfile.ZipFile(APK_IN, 'r') as zin, \
     zipfile.ZipFile(APK_WORK, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename == REPLACE_ENTRY:
            print(f"  Replacing: {item.filename}")
            zout.writestr(item, new_so_bytes)
        else:
            # Preserve original compression
            data = zin.read(item.filename)
            zout.writestr(item, data)
print("  Done rebuilding.")

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
