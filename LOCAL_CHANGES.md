# Local changes (this fork)

Tracks changes made on `Flounder1664/wagic` that are not in upstream `WagicProject/wagic`. One row per logical change. The "Tested on" column is the truth, not the commit message — keep it honest.

| Date       | Branch                     | Commit     | Files / area                                                          | Tested on            | Status |
|------------|----------------------------|------------|-----------------------------------------------------------------------|----------------------|--------|
| 2026-04-14 | john/android-rp5           | (in 64833c619) | GameStateMenu.cpp                                                  | RP5, S9              | OK — Demo menu removed |
| 2026-04-14 | john/android-rp5           | (in 64833c619) | SDLActivity.java, GameStateDeckViewer.cpp                          | RP5, S9              | OK — vertical swipe Y threshold raised to 800 |
| 2026-04-14 | john/android-rp5           | (in 64833c619) | GameStateDeckViewer.cpp                                            | RP5, S9              | OK — horizontal scroll divisor 500 → 300 |
| 2026-04-19 | john/android-rp5           | 64833c619  | ManaCost.cpp, CardGui.cpp, JGfx.cpp + ECL primitives + gamepad     | RP5, S9              | OK — bundled commit; tagged `verified-android-2026-04-19` |
| 2026-04-24 | wagic-v145-windows         | 7a32a6f30  | SDLmain.cpp, mtg.props, vcxproj                                    | Windows              | **NOT tested on Android — suspect for S9 input regression** |
| 2026-04-24 | wagic-v145-windows         | b81231d43  | JFileSystem.cpp, zfsystem.{cpp,h}                                  | Windows              | **NOT tested on Android — suspect for S9 input regression** |
| 2026-04-24 | wagic-v145-windows         | (cherry-picks) | deck files, CardImageLinks.csv                                  | —                    | data-only |
| 2026-05-07 | feature/deck-editor-delete | 1a6f14a59  | GameStateDeckViewer.{cpp,h}, MenuItem.cpp, DeckMenuItem.cpp, GameStateMenu.h | needs build & test | Feature complete in code |
| 2026-05-07 | feature/version-display    | 21a63aad0  | build.number.properties, Wagic_Version.h                           | needs build & test   | In-game version display |
| 2026-05-07 | wip/steam-deck-linux       | 472a3b4a9  | SDLmain.cpp Linux blocks, JNetwork.cpp, mtg.props NETWORK_SUPPORT, CMakeLists.txt, STEAM_DECK.md, tools/linux/ | not yet successful | parked |
| 2026-05-07 | wip/s9-fix-attempts        | 49b99371e  | SDLActivity.java flipEGL try/catch + brightness; GameStateMenu.cpp bgTexture lock | inconclusive | review in Phase 1 of S9-fix work |
| 2026-05-07 | wip/card-data-may          | 58a8423a3  | DFT/INR _cards.dat, primitives, wallpapers, modrules, Rules/GameObserver/GameState.cpp | partial — per-card validation pending | needs validation |
| 2026-05-07 | wip/build-tooling          | 3163558d9  | patch_*.py, fetch_*.py, build_full_sets.py, push_*.bat, new_set_cards.json | dev-only            | utility scripts |
| 2026-05-07 | wip/uncategorized-may      | 2dc9b3c16  | CLAUDE.md, JGE/test_jlogger_usage.cpp, TODO_new_sets.md, root_cause_analysis.md, ndk_build_log2.txt | N/A | notes/scratch |
| 2026-05-07 | wagic-v145-windows         | 246f729aa  | .gitignore additions for build outputs and Scryfall dumps          | N/A                  | hygiene |
| 2026-05-07 | john/android-s9-fix        | 9de163a7a  | LOCAL_CHANGES.md, BUILD_LOG.md, CLAUDE.md branch-map, PORTABILITY_NOTES.md S9 serial | N/A | housekeeping; bug-hunt branch |
| 2026-05-07 | john/android-s9-fix        | (next commit) | SDLActivity.java flipEGL try/catch + GameStateMenu.cpp bgTexture lock fix (cherry-picked safe parts of wip/s9-fix-attempts) | needs build & test on RP5 + S9 + Windows | defensive; not yet known to fix S9 regression — bisect of 24 Apr suspects still required |
