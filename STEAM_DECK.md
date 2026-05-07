# Wagic on Steam Deck

Native x86_64 Linux build of Wagic, packaged as an AppImage suitable for the
Steam Deck. Reuses the existing SDL 1.2 main-loop (`JGE/src/SDLmain.cpp`)
which already has gamepad support; renders the original 480×272 design
resolution **letterboxed** at 2× scale (960×544) inside a 1280×800 fullscreen
window.

## Build (do this on Linux / WSL2 / a Linux VM — not on the Deck itself)

Wagic's main loop is written against the SDL **1.2** API (`SDL_SetVideoMode`,
etc.). Ubuntu 22.04 still ships `libsdl1.2-dev`; **Ubuntu 24.04+ removed it**.
Use the helper script to install everything (apt deps + builds `sdl12-compat`
from source into `~/.local` if SDL 1.2 isn't available):

```sh
./tools/linux/setup-deps-ubuntu.sh
```

Then:

```sh
# from repo root — only needed if setup-deps installed sdl12-compat
export PKG_CONFIG_PATH="$HOME/.local/lib/pkgconfig:$PKG_CONFIG_PATH"
export LD_LIBRARY_PATH="$HOME/.local/lib:$LD_LIBRARY_PATH"

mkdir -p build-linux && cd build-linux
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
```

If you're on an older distro that has `libsdl1.2-dev` available natively,
just install that plus `cmake g++ pkg-config libgl-dev libglu1-mesa-dev
zlib1g-dev libboost-system-dev libboost-thread-dev` and skip the helper.

Output: `build-linux/wagic` (also copied to `projects/mtg/bin/wagic` for ad-hoc
runs from the asset directory).

### Smoke test

```sh
cd projects/mtg/bin && ./wagic
```

You should see a 960×544 SDL window. User data is written to
`~/.local/share/Wagic/User/` — verify after first launch:

```sh
ls ~/.local/share/Wagic/User/
```

## Package as AppImage

Requires [`appimagetool`](https://github.com/AppImage/AppImageKit/releases) on
your `$PATH`.

```sh
./tools/appimage/build-appimage.sh
```

Output: `Wagic-x86_64.AppImage` in the repo root.

## Install on Steam Deck

1. Boot the Deck into **Desktop Mode** (hold power → Switch to Desktop).
2. Copy `Wagic-x86_64.AppImage` to the Deck (e.g. via `scp`, USB, or
   `~/Downloads/`).
3. Make it executable:
   ```sh
   chmod +x ~/Applications/Wagic-x86_64.AppImage
   ```
4. Double-click to test it launches in Desktop Mode.
5. In **Steam → Games → Add a Non-Steam Game to My Library** → browse to the
   AppImage → add.
6. **Important:** Right-click the new entry → Properties → **Controller** →
   set **"Disable Steam Input"** for this shortcut. The native SDL gamepad
   mapping at `JGE/src/SDLmain.cpp:71-80` (A/B/X/Y, shoulders, Start) handles
   the Deck pad directly. Steam Input on top of that double-maps inputs.
7. Launch from the library — works in Gaming Mode via Gamescope.

## Where data lives

| Path                            | Purpose                                     |
|---------------------------------|---------------------------------------------|
| `<AppImage mount>/usr/share/wagic/Res/` | Read-only shipped assets (cards, art, rules) |
| `~/.local/share/Wagic/User/`            | Decks, save state, downloaded sets, settings |

Set downloads land in `~/.local/share/Wagic/User/sets/` — same shape as the
Windows and Android builds. AppImage updates won't touch user data.

## Troubleshooting

- **Black screen on launch in Gaming Mode**: try Desktop Mode first. If it
  works there but not in Gaming Mode, the issue is Gamescope's display
  handling — try forcing windowed mode (omit fullscreen flag) for the
  initial launch and confirm via `journalctl --user -e`.
- **No controller input**: confirm Steam Input is disabled (see step 6 above)
  and that `/dev/input/js0` exists when running the AppImage from a terminal.
- **"Res not found"**: you ran the bare `wagic` binary outside its asset
  directory. The AppImage's `AppRun` does `cd` into the right place; for
  ad-hoc runs use `cd projects/mtg/bin && ./wagic`.
- **Networking / LAN play**: `JNetwork` already supports `LINUX` via plain BSD
  sockets — no extra setup. The Deck must be on the same LAN as the host.

## Files added by this work

- `CMakeLists.txt` (repo root) — Linux SDL build
- `tools/linux/setup-deps-ubuntu.sh` — apt deps + sdl12-compat from source
- `tools/appimage/AppRun`, `wagic.desktop`, `build-appimage.sh`
- `JGE/src/SDLmain.cpp` — added Linux user-path init block (`#ifdef LINUX`)

## When packaging the AppImage on Ubuntu 24.04+

`sdl12-compat` is a shim on top of SDL2, so the AppImage must bundle:

- `libSDL-1.2.so.0` (from `~/.local/lib/`, built by setup-deps-ubuntu.sh)
- `libSDL2-2.0.so.0` (from `/usr/lib/x86_64-linux-gnu/`)

Easiest way: use [`linuxdeploy`](https://github.com/linuxdeploy/linuxdeploy)
before `appimagetool`. It walks the binary's `NEEDED` entries and copies
the .so files into `AppDir/usr/lib/` automatically. Add to
`build-appimage.sh` if needed:

```sh
linuxdeploy --appdir "${APPDIR}" --executable "${BIN}" \
    --library "$HOME/.local/lib/libSDL-1.2.so.0"
```
