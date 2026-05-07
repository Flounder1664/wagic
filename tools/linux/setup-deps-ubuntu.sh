#!/usr/bin/env bash
# setup-deps-ubuntu.sh — install Linux build deps for Wagic.
#
# Wagic's SDLmain.cpp originally targeted the bundled SDL 1.3 (transitional).
# The CMake build targets system SDL2 directly, with the SDL 1.2-only call
# sites in SDLmain.cpp wrapped in `#if defined(LINUX) && !defined(ANDROID)`
# branches that use SDL2 idioms (SDL_CreateWindow, SDL_GL_SwapWindow, etc).
# So we just need libsdl2-dev — no sdl12-compat needed.
#
# Usage:
#     ./tools/linux/setup-deps-ubuntu.sh

set -euo pipefail

echo "==> Installing apt packages..."
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    build-essential cmake pkg-config git ca-certificates \
    libsdl2-dev libgl-dev libglu1-mesa-dev zlib1g-dev \
    libgif-dev libfreetype-dev libpng-dev libjpeg-dev \
    libboost-system-dev libboost-thread-dev

echo
echo "==> Done. Now build:"
echo "    mkdir -p build-linux && cd build-linux"
echo "    cmake -DCMAKE_BUILD_TYPE=Release .."
echo "    make -j\$(nproc)"
