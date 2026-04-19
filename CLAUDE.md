# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Wagic, the Homebrew** is a C++ card game engine (Magic: The Gathering-like) targeting PSP, Android, iOS, Windows, macOS, and Linux. The codebase has two main layers:

- **JGE** (`/JGE/`) — "Jas Game Engine++", the platform-abstraction layer (~18K LOC). Handles rendering, audio, resource management, networking, XML parsing, and particle systems. Platform-specific code lives in `JGE/src/pc/`, `JGE/src/android/`, `JGE/src/qt/`.
- **MTG Game** (`/projects/mtg/`) — The game logic (~92K LOC). Cards, abilities, AI, GUI, rules, zones, deck management, and more.

## Build Commands

### Linux/Qt (primary dev target)

```bash
# GUI build (release)
mkdir qt-gui-build && cd qt-gui-build
qmake -qt=qt5 ../projects/mtg/wagic-qt.pro CONFIG+=release CONFIG+=graphics
make -j4

# Console/debug build (used for running tests)
qmake -qt=qt5 projects/mtg/wagic-qt.pro CONFIG+=console CONFIG+=debug DEFINES+=CAPTURE_STDERR
make -j4
```

### PSP

```bash
cd JGE && make -j4 && cd ..
cd projects/mtg && mkdir -p objs && make -j4
```

### Android

```bash
android-ndk-r22/ndk-build -C projects/mtg/Android -j4
ant debug -f projects/mtg/Android/build.xml
```

### Windows

Open `projects/mtg/Windows/mtg_vs2010.sln` in Visual Studio.

### Version update (required before building releases)

```bash
cd projects/mtg && ant update
```

This reads `projects/mtg/build.number.properties` (format: `major=X`, `minor=Y`, `point=Z`) and generates `Wagic_Version.h`.

## Running Tests

Tests use a custom `TestSuiteAI` framework compiled in with `-DTESTSUITE`. They run in console mode automatically after the debug Qt build:

```bash
# From repo root after console/debug build:
cd projects/mtg && ../../wagic
```

Test source: `projects/mtg/src/TestSuiteAI.cpp` / `projects/mtg/include/TestSuiteAI.h`.

## Resource Packaging

Game assets live in `projects/mtg/bin/Res/`. A Python script packages them into a zip:

```bash
cd projects/mtg/bin/Res && python2 createResourceZip.py
```

The zip must be present (or absent, depending on test mode) for the test suite to work — see `travis-script.sh` for the expected workflow.

## Architecture

### JGE (Engine)

| Component | Files | Role |
|---|---|---|
| Rendering | `JGfx.h`, `JRenderer.*` | Hardware-accelerated 2D rendering abstraction |
| Audio | `JSoundSystem.*`, `JSfx.*` | Music and sound effects |
| Resources | `JResourceManager.*` | Asset loading, zip-based packaging |
| Input | `JGameLauncher.*` | Platform-agnostic input |
| Networking | `JNetwork.*` | Network support |
| XML | `tinyxml.*` | XML parsing (vendor) |

### MTG Game (Key Subsystems)

| Subsystem | Key Files | Role |
|---|---|---|
| Card Data | `MTGCard.*`, `MTGCardInstance.*` | Card definitions and live instances |
| Card GUI | `CardGui.*` | Rendering individual cards |
| Game State | `GameObserver.*`, `GameState.*`, `GameStateDuel.*` | Top-level game flow |
| Abilities | `MTGAbility.*`, `AllAbilities.h`, `AbilityParser.*` | Comprehensive MTG ability implementation (~246KB) |
| AI | `AIPlayer.*`, `AIPlayerBaka.*`, `AIMomirPlayer.*` | Multiple AI difficulty levels |
| Rules Engine | `Rules.*`, `MTGRules.*`, `ModRules.*` | Core game rules and customizable rule mods |
| Game Zones | `MTGGameZones.*` | Hand, library, graveyard, battlefield, stack, etc. |
| Stack/Actions | `ActionStack.*`, `ActionLayer.*` | Spell stack, triggered/activated abilities |
| GUI Layers | `GuiLayers.*`, `DuelLayers.*`, `GuiCombat.*` | Layered in-game UI |
| Deck System | `MTGDeck.*`, `DeckManager.*`, `DeckView.*` | Deck loading, editing, selection |
| Player | `Player.*`, `PlayerData.*` | Player state, statistics |

### Ability System

The ability system is the most complex part of the codebase. `AllAbilities.h` defines hundreds of MTG abilities. `AbilityParser` parses text-based card definitions. When adding new card abilities, study existing ability patterns in `AllAbilities.h` and the parser.

### Resource System

`WResourceManager` handles all game assets. Assets are loaded from zip archives using JGE's zip support. The `Res/` directory structure is mirrored inside the zip. Themes override default assets by providing alternative files.

## Compiler Flags

The project builds with `-Wall -Werror -Wno-unused`. `PrecompiledHeader.h` is used for faster compilation — always include it first in `.cpp` files:

```cpp
#include "PrecompiledHeader.h"
```

## CI/CD

- **Travis CI** (`.travis.yml`): Builds PSP, Android, Qt/Linux; runs tests with gcov; uploads release zips to GitHub Releases via `tools/upload-binaries.py`.
- **AppVeyor** (`appveyor.yml`): Windows Visual Studio builds; creates ZIP archives.

Coverage is tracked via coveralls.io, configured to include only `projects/mtg/include` and `projects/mtg/src`.
