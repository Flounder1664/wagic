# PORTABILITY_NOTES.md — wagic (main game project)

Handoff brief for portability tidy-up and ongoing build/deploy work.

---

## 1. What this project is

Fork of **Wagic, the Homebrew** (C++ MTG-like card game engine). Target platforms for *this* user are Android (Retroid Pocket 5 handheld) and Windows only — PSP, iOS, Linux/Qt, macOS are intentionally skipped.

The deploy loop is:

```
Edit C++ / card data on PC
  → NDK build produces libmain.so
  → patch_apk.py swaps libmain.so into APK, zipaligns, re-signs
  → adb install -r to device
  → (separately) patch_core_zip.py re-packs core.zip
  → adb push to device at versioned name
```

---

## 2. Hardcoded-path hotspots

These are the files whose portability needs fixing. Anything not on this list is already portable (uses relative paths or standard locations).

### `patch_apk.py`

All absolute Windows paths. These are the candidates to parameterise:

| Constant | Current value | Kind |
|---|---|---|
| `APK_IN` | `M:\Claude_projects\wagic\projects\mtg\Android\bin\Wagic-debug.apk` | repo-relative |
| `APK_WORK` | `…\Wagic-debug-patched.apk` | repo-relative (derivable) |
| `APK_ALIGNED` | `…\Wagic-debug-aligned.apk` | repo-relative (derivable) |
| `LIBMAIN` | `M:\Claude_projects\wagic\projects\mtg\Android\libs\arm64-v8a\libmain.so` | repo-relative |
| `BUILD_TOOLS` | `C:\Android-SDK\build-tools\26.0.3` | machine-specific (Android SDK) |
| `APKSIGNER` | `…\apksigner.bat` | derived from BUILD_TOOLS |
| `ZIPALIGN` | `…\zipalign.exe` | derived from BUILD_TOOLS |
| `DEBUG_KEY` | `C:\Users\john\.android\debug.keystore` | user-profile-specific |
| keystore pass | hardcoded string `"android"` | safe default but still config |

### `patch_core_zip.py`

| Constant | Current value | Kind |
|---|---|---|
| `CORE_ZIP` | `M:/Claude_projects/wagic/projects/mtg/bin/Res/core.zip` | repo-relative |
| `CORE_TMP` | `…/core_tmp.zip` | derivable |
| `REPLACEMENTS` map | two `M:/…` paths under `projects/mtg/bin/Res/sets/primitives/` | repo-relative |

### `CLAUDE.md` (repo root)

Generic build docs — no absolute paths baked in, but assumes `android-ndk-r22`, `C:\Android-SDK`, and qt5 are findable. Worth adding a "Prerequisites / toolchain locations" section.

### `C:\Users\john\.claude\projects\M--Claude-projects-wagic\memory\` (user memory)

These files belong to the Claude Code session, not the repo, so the tidy-upper shouldn't rewrite them — but they DOCUMENT the user-specific paths and should be consulted so the new parameterisation lines up with reality:

- `project_wagic_structure.md` — device paths, ADB commands, build/deploy workflow
- `project_android_build.md` — NDK/SDK/Java tool locations, APK signing notes
- `project_completed_changes.md` — what's already been modified and tested
- `user_platforms.md` — "only Android and Windows, skip the rest"
- `MEMORY.md` — index of the above

---

## 3. Machine / device / user specifics to parameterise

Everything in this table currently appears as a hardcoded literal somewhere in the repo or in ADB commands documented in CLAUDE.md / memory files. All of it needs to move to a single config (env vars, `.env`, `config.yaml`, CLI args — user's call).

| Name | Current value | Where it appears |
|---|---|---|
| Repo root on PC | `M:\Claude_projects\wagic\` | patch_*.py, docs |
| User home | `C:\Users\john\` | debug keystore path |
| Android SDK | `C:\Android-SDK\` | patch_apk.py, ADB commands |
| Android SDK build-tools version | `26.0.3` | patch_apk.py |
| Android NDK | `C:\android-ndk-r22\` | build commands |
| Device ADB serial (RP5) | `d15e0854` | every ADB command in docs |
| Device ADB serial (S9 Tablet) | `R52X10ACZCW` | captured 2026-05-07; not yet referenced in §6 — substitute when running S9-only commands |
| Device SD card UUID | `3963-3235` | device push targets |
| Android app package | `net.wagic.app` | device paths, adb install |
| Active player profile | `Maxglee` | collection.dat and deck file location |
| Versioned core zip filename | `Wagic-core-0255.zip` | device push target |
| Debug keystore password | `android` | patch_apk.py |

The SD card UUID is the one that'll hurt most — it changes per-device and per-SD-card. A portable script should either discover it at runtime (`adb shell sm list-disks` / `sm list-volumes`) or accept it as a parameter.

---

## 4. Device-side paths (verified 2026-04-19)

These are correct and must be preserved by any refactor. Note the SD card prefix — earlier assumptions about `/sdcard/` were wrong.

```
/storage/3963-3235/Android/data/net.wagic.app/files/Wagic/
├── Res/
│   ├── Wagic-core-0255.zip      ← VERSIONED name, not core.zip
│   └── rules/
└── User/
    ├── sets/ECL/ECL.zip
    └── profiles/Maxglee/
        ├── collection.dat        ← format: "#NAME:collection" header + one ID per line × N copies
        ├── collection.dat.bak
        ├── options.txt
        ├── deck1.txt … deck32.txt
        └── stats/
```

`/sdcard/Android/data/net.wagic.app/…` and `/sdcard/Wagic/` both exist but are **empty and unused** — do not push there.

---

## 5. Cross-project dependencies (important — don't refactor in isolation)

Under `M:\Claude_projects\Wagic-Profile\` the user has three related projects. They all touch the same data shapes as this repo:

| Project | Shares with this repo |
|---|---|
| Web deck-builder | `collection.dat` format, card IDs, deck file format (`deckN.txt`) |
| Gemini prompt generator | card IDs, card names from `mtg.txt` / `planeswalkers.txt`, set info from `_cards.dat` |
| Collection dedup tool | `collection.dat` (reads + writes), `Wagic-core-0255.zip` (reads), deck files (rewrites IDs), `Maxglee` profile name |

**Before changing the collection.dat format, filename conventions, or the versioned core-zip name, check the other three projects' `PORTABILITY_NOTES.md`.** The dedup tool in particular reads this repo's core zip and rewrites the player's collection and decks — if you change the file layout assumed by this repo, you break it.

---

## 6. Build & deploy cheat-sheet (for when you do the build work)

Device serial is currently `d15e0854`. Substitute yours.

### Android C++ change → deploy

```powershell
# 1. NDK build
C:\android-ndk-r22\ndk-build.cmd -C M:\Claude_projects\wagic\projects\mtg\Android

# 2. Patch the existing debug APK (replaces libmain.so, zipalign, re-sign)
python M:\Claude_projects\wagic\patch_apk.py

# 3. Install over existing (preserves save data)
C:\Android-SDK\platform-tools\adb.exe -s d15e0854 install -r `
  M:\Claude_projects\wagic\projects\mtg\Android\bin\Wagic-debug.apk
```

### Card-data change (mtg.txt, planeswalkers.txt, _cards.dat) → deploy

```powershell
# 1. Edit source under projects/mtg/bin/Res/sets/...
# 2. Rebuild core.zip on PC
python M:\Claude_projects\wagic\patch_core_zip.py

# 3. Push with the VERSIONED name (not core.zip!) to the SD card path
C:\Android-SDK\platform-tools\adb.exe -s d15e0854 push `
  M:\Claude_projects\wagic\projects\mtg\bin\Res\core.zip `
  /storage/3963-3235/Android/data/net.wagic.app/files/Wagic/Res/Wagic-core-0255.zip
```

### Windows C++ change → deploy

The Windows binary is built from `projects/mtg/template.vcxproj` (NOT the stale `mtg_vs2010.sln`) using the VS2022 BuildTools install + the v145 toolset (Win32 / Release):

```powershell
# 1. Build Wagic.exe
& 'C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\MSBuild\Current\Bin\MSBuild.exe' `
  'M:\Claude_projects\wagic\projects\mtg\template.vcxproj' `
  /p:Configuration=Release /p:Platform=Win32 /p:PlatformToolset=v145 /m /nologo

# Output → M:\Claude_projects\wagic\projects\mtg\bin\Wagic.exe

# 2. Back up the previous Wagic.exe (rolling-old convention on G:\)
copy 'G:\Wagic-windows\Wagic.exe' "G:\Wagic-windows\Wagic.exe.old.$(Get-Date -Format yyyyMMdd)"

# 3. Deploy
copy 'M:\Claude_projects\wagic\projects\mtg\bin\Wagic.exe' 'G:\Wagic-windows\Wagic.exe'
```

Engine source (e.g. `JGE/src/SDLmain.cpp`, `projects/mtg/src/*`) lives on `wagic-v145-windows`. Any feature branch that needs a Windows binary should be cut off that branch so the v145 toolset config in `projects/mtg/mtg.props` is in scope. Verbose output: append `/verbosity:detailed`.

### Windows card-data change → deploy

```powershell
# 1. Patch the in-tree core.zip with the latest primitives/cards
python M:\Claude_projects\wagic\patch_core_zip.py

# 2. Deploy with the VERSIONED name expected by Wagic_Version.h
copy 'M:\Claude_projects\wagic\projects\mtg\bin\Res\core.zip' `
     'G:\Wagic-windows\Res\Wagic-core-0256.zip'
```

The current resource version is `0256` (see `WAGIC_RESOURCE_*` in [projects/mtg/include/Wagic_Version.h](projects/mtg/include/Wagic_Version.h:21)). On Windows, `JGE/src/zipFS/zfsystem.cpp:50` globs every `*.zip` in `Res\` alphabetically and the alphabetically-last entry wins for duplicate filenames — so rename any stale `core.zip` / `Wagic-core-0255.zip` in `G:\Wagic-windows\Res\` to `*.zip.old.<date>` before deploying, otherwise the new zip is silently shadowed. (Burned 90 minutes on this on 2026-05-10.)

Zips also need explicit directory marker entries (zero-byte `sets/`, `sets/DSK/`, etc.) — without them `scanfolder` returns empty and Wagic loads zero sets from the zip. `patch_core_zip.py` was updated 2026-05-11 to emit these markers regardless of the source zip's quirks.

### Verifying a push landed

MTP / Windows Explorer often caches file timestamps. Verify via adb:

```powershell
C:\Android-SDK\platform-tools\adb.exe -s d15e0854 shell `
  ls -la /storage/3963-3235/Android/data/net.wagic.app/files/Wagic/Res/
```

---

## 7. Gotchas (things that cost hours if you don't know them)

1. **SD card vs internal storage.** Previous sessions pushed to `/sdcard/Android/data/net.wagic.app/files/Wagic/` and wondered why changes didn't take effect. The game runs from `/storage/3963-3235/` (SD card). Internal is empty.
2. **Versioned zip filename.** The game loads `Wagic-core-0255.zip`, not `core.zip`. Patching the PC's `core.zip` and pushing it without renaming silently changes nothing.
3. **Profile name is `Maxglee`, not `0`.** collection.dat and all deck files live under `profiles/Maxglee/`.
4. **MTP timestamps lie.** If you transferred a file via Explorer and the date didn't change, that doesn't mean the transfer failed — MD5 it via `adb pull` to be sure.
5. **`android-ndk-r22` specifically.** Newer NDKs have broken the build in past sessions. Stick with r22 unless explicitly upgrading.
6. **MTE on Android 13.** The Retroid Pocket 5 runs Android 13 with Memory Tagging Extension active. Use-after-free shows up as SIGSEGV with tagged fault addresses like `0x6a000000078107` — the top byte is the tag, not part of the address. Null-checks (`== NULL`) pass on tagged pointers; the crash happens on the first actual dereference.
7. **Debug keystore default.** `C:\Users\john\.android\debug.keystore` with password `android` is Android's standard debug key — nothing sensitive, but any re-sign needs to match what's already installed or adb install will refuse the upgrade.

---

## 8. Suggested shape for parameterisation (non-binding)

Whichever approach you pick, keep all the variables from §3 in **one** place, not scattered. Options the user will accept:

- A `.env` at repo root + `python-dotenv` in the scripts
- A `config.yaml` consumed by both `patch_apk.py` and `patch_core_zip.py`
- CLI `argparse` args with sensible defaults
- A tiny `wagic_paths.py` module the scripts both import

The user's preference is for something portable between *their* Windows PC and any other dev's setup — a colleague cloning the repo should be able to run the scripts after editing one file.

---

## 9. What's NOT in scope for portability work (don't touch)

- Anything under `JGE/` or `projects/mtg/src/` (engine/game source). These are fine as-is.
- `CLAUDE.md` and `.claude/` session configuration — leave those alone.
- `projects/mtg/bin/Res/` game assets — these are data, not code.
- ~~The crash investigation currently underway~~ **Resolved Apr 2026.** The ECL deck-editor crash was root-caused and fixed in `ManaCost.cpp` + `CardGui.cpp`. See `project_completed_changes.md` §4. The earlier "don't touch `projects/mtg/src/`" fence is lifted.

## 9a. Open follow-up issues (NOT portability work — separate dev tasks)

These are live bugs/gaps the next dev session should pick up after portability is done. They are documented here so they don't get lost; they do NOT block the tidy-up.

### ECL card images not showing in deck editor — RESOLVED (Apr 30 2026)
ECL cards now render correctly in the deck editor. See `project_completed_changes.md` for details. The earlier diagnostic trace through `MTGCard::getImageName` / `WCachedTexture::Attempt` / `ResourceManagerImpl::cardFile` / `JFileSystem::AttachZipFile` is no longer relevant.

### Image downloader crashes the game
Low priority. User confirmed acceptable — the CSV-based downloader isn't
needed for ECL since images ship locally. If someone wants to fix it
anyway, repro is: launch game → trigger image-download option → crash.
Pull logcat during the crash to start.

---

## 10. After tidy-up: build work

Expect the user to ask you to run the Android NDK build + APK patch + install loop after you've made scripts portable. §6 above is your runbook. Before your first build, verify:

- `C:\android-ndk-r22\` exists
- `C:\Android-SDK\build-tools\26.0.3\` exists
- `C:\Users\john\.android\debug.keystore` exists
- `adb devices` shows `d15e0854`
- Device is unlocked and USB debugging authorised

If any of those fail, surface it immediately rather than plowing ahead — fixing toolchain issues is a separate task from portability.
