APP_PROJECT_PATH := $(call my-dir)/..
APP_CPPFLAGS += -frtti -fexceptions
APP_ABI := arm64-v8a
APP_PLATFORM := android-21
# Baseline ARMv8.0: armv8.1-a + forced LSE emitted LDADD/CAS atomics that SIGILL
# on pre-v8.1 cores (Galaxy Tab S4 / Snapdragon 835 crashed at startup).
APP_CFLAGS += -march=armv8-a
#APP_ABI := x86 # mainly for emulators
APP_STL := c++_static
APP_MODULES := libpng libjpeg main SDL

# Android 15+ (S9 is on 16) requires native libs aligned to 16KB pages.
# NDK r22's lld defaults LOAD segments to 4KB; force 16KB for every module.
APP_LDFLAGS += -Wl,-z,max-page-size=16384 -Wl,-z,common-page-size=16384

#APP_OPTIM is 'release' by default
APP_OPTIM := release
