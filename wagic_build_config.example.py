import os

# Copy this file to wagic_build_config.py and edit for your machine.
# wagic_build_config.py is gitignored — never commit it.
#
# All values can also be set as environment variables of the same name.

# Path to your Android SDK build-tools directory.
# Example: C:/Android-SDK/build-tools/26.0.3
BUILD_TOOLS = os.environ.get("ANDROID_BUILD_TOOLS", r"C:\Android-SDK\build-tools\26.0.3")

# Path to the debug keystore used to sign the APK.
# The default below works on most machines without any change.
DEBUG_KEY = os.environ.get(
    "ANDROID_DEBUG_KEY",
    os.path.join(os.path.expanduser("~"), ".android", "debug.keystore")
)

# Keystore password — "android" is Android's standard debug key default.
DEBUG_KEY_PASS = os.environ.get("ANDROID_DEBUG_KEY_PASS", "android")
