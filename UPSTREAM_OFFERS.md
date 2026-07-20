# Work available to upstream — a shopping list

This fork ([Flounder1664/wagic](https://github.com/Flounder1664/wagic)) has accumulated ~250 commits beyond `WagicProject/wagic` master. This document groups that work into logical collections that upstream (or anyone else) is welcome to take, ranked by how objective the benefit is. Everything listed is pushed to this fork; nothing here requires access to my machine.

**How to read this list**

- **Tier A** — makes Wagic play more like real Magic: the Gathering, fixes crashes/bugs, or fixes builds. Objective benefit.
- **Tier B** — developer-facing infrastructure: testing, tooling, audits. Objective, but only pays off if you use the workflow.
- **Tier C** — subjective/preference changes. I've recorded *why I* wanted each one; take or leave.
- A final section covers **provenance** (work in this fork that is *not* mine to offer) and **what's deliberately excluded**.

**Where the work lives**

| Branch | What it is |
|---|---|
| [`wagic-v146-windows`](https://github.com/Flounder1664/wagic/tree/wagic-v146-windows) | Main integrated branch — everything up to late June 2026, built and played on Windows + Android |
| [`docs/set-coverage-audit`](https://github.com/Flounder1664/wagic/tree/docs/set-coverage-audit) | Superset of the above plus July 2026 work (saddle/crewN, FIN/TLA batches, exhaust/sneak, Android 16 KB) |
| [`feature/duskmourn-rooms`](https://github.com/Flounder1664/wagic/tree/feature/duskmourn-rooms) | Rooms engine work in isolation (also merged into the branches above) |

Tested-on status below comes from the fork's [`LOCAL_CHANGES.md`](https://github.com/Flounder1664/wagic/blob/docs/set-coverage-audit/LOCAL_CHANGES.md) ledger, which is kept honest per change. "Windows + Android" means built and played on Windows 11, a Retroid Pocket 5, and a Galaxy Tab S9.

---

## Tier A — rules correctness, real-MtG features, stability, buildability

### A1. Duskmourn Rooms — engine support + 13 Room cards

Split-unlock Room enchantments: a `WEventRoomFullyUnlocked` event, an `@roomfullyunlocked` trigger, and an `unlockdoor:N` ability, plus ~13 DSK Rooms written against them (sample: Bottomless Pool // Locker Room).

- Where: [`965de3d1f`](https://github.com/Flounder1664/wagic/commit/965de3d1f) engine support, [`23db3072a`](https://github.com/Flounder1664/wagic/commit/23db3072a) 12 more Rooms, [`6f24cdbe1`](https://github.com/Flounder1664/wagic/commit/6f24cdbe1) bug fixes from play-testing. Files: `WEvent.{h,cpp}`, `AllAbilities.{h,cpp}`, `MTGAbility.cpp`, `borderline.txt`.
- Value: DSK is a real set upstream can't represent without this mechanic.
- Readiness: Windows-built and play-tested; Android build untested. Small, self-contained C++ footprint.
- Suggested shape: one feature PR (engine + sample cards).

### A2. crewN — multi-creature crew / saddle

Upstream's `crew()` taps one creature. `crewN` implements the real rule: tap any number of untapped creatures whose **total power** meets the threshold. Includes migration of existing crew/saddle primitive lines and 30 Mount (saddle) cards built on it.

- Where: [`60aa35fc8`](https://github.com/Flounder1664/wagic/commit/60aa35fc8) engine, [`96f172d0c`](https://github.com/Flounder1664/wagic/commit/96f172d0c) DSL migration, [`05dc5d3c2`](https://github.com/Flounder1664/wagic/commit/05dc5d3c2) + [`e85dc35f9`](https://github.com/Flounder1664/wagic/commit/e85dc35f9) Mounts (on `docs/set-coverage-audit`).
- Value: every Vehicle and Mount in the game gets closer to real rules.
- Readiness: Windows-tested in play; needs an Android rebuild (engine + core.zip must ship together, since old exes can't parse the new syntax).
- Suggested shape: engine PR first, primitive migration PR second.

### A3. Emblems and the command zone

Planeswalker emblems as visible, persistent cards in the command zone: an `emblem("text")` primitive marker, generic emblem frame art, persistence across turns, and ~75 curated planeswalker emblems (including a fix for Jace, Unraveler of Secrets' -8 actually countering spells — that one authored by InquiringMinds-AI, see provenance).

- Where: [`883107019`](https://github.com/Flounder1664/wagic/commit/883107019), [`c46e85b8f`](https://github.com/Flounder1664/wagic/commit/c46e85b8f), [`81d2a88f0`](https://github.com/Flounder1664/wagic/commit/81d2a88f0), [`d59a057a5`](https://github.com/Flounder1664/wagic/commit/d59a057a5), [`f7db69473`](https://github.com/Flounder1664/wagic/commit/f7db69473). Design trail in fork issue [#23](https://github.com/Flounder1664/wagic/issues/23).
- Value: emblems currently work invisibly (or not at all); this makes a whole planeswalker mechanic behave and *look* like real Magic.
- Readiness: Windows + Android tested in play.
- Suggested shape: one feature PR + one data PR (the 75 curated emblems).

### A4. London mulligan + opening-hand fixes

- London mulligan done properly: redraw a full hand, then put N cards on the bottom on keep, with highlighting and auto-keep on phase advance ([`1ecf7bc5f`](https://github.com/Flounder1664/wagic/commit/1ecf7bc5f), [`6a4f30f8a`](https://github.com/Flounder1664/wagic/commit/6a4f30f8a)).
- Leylines can start on the battlefield for the player on the draw too ([`535a35175`](https://github.com/Flounder1664/wagic/commit/535a35175)).
- Value: the mulligan is the first thing every player touches every game; this is the current real rule.
- Readiness: Windows + Android tested in play. Suggested shape: two small PRs.

### A5. Booster Draft mode

A complete draft-and-play loop: pick a format/set (single set, three different sets, or random/era-filtered) → draft a pod against 7 bot drafters (pack rotation + pick heuristic) → adjust the auto-built deck in a draft-scoped deck editor → play a best-of-3 knockout bracket. ~35 commits; new files `MTGDraft.{h,cpp}`, `GameStateDraft.{h,cpp}` plus wiring in `GameStateDuel`/`GameApp`/`GameStateMenu`.

- Where: [`b4b06b3a7`](https://github.com/Flounder1664/wagic/commit/b4b06b3a7)..[`e05361f4d`](https://github.com/Flounder1664/wagic/commit/e05361f4d) on `wagic-v146-windows`. Full design/debugging trail in fork issue [#27](https://github.com/Flounder1664/wagic/issues/27).
- Value: booster draft is a real, popular MtG format Wagic has never had.
- Readiness: **Windows only** so far — never built for Android; `draft_booster.txt` is still a loose Res file. Known gaps documented honestly in [#27](https://github.com/Flounder1664/wagic/issues/27)/[#28](https://github.com/Flounder1664/wagic/issues/28) (no sideboarding between games yet; bot decks use fixed high-numbered `ai/baka/` slots because `AIPlayerFactory` hardcodes deck paths).
- Suggested shape: discussion issue first (it's big), then a feature-branch PR.

### A6. Set content — roughly 1,000 new card registrations

All real, Scryfall-listed sets, written as primitives + `_cards.dat` entries in the standard format:

| Set | Scope | Where |
|---|---|---|
| EOE (Edge of Eternities) | Full set skeleton (398 IDs), ~190 primitives incl. Lander/Robot/Drone token macros, plus a systemic ETB-trigger fix affecting 32 cards | [`c9282fb26`](https://github.com/Flounder1664/wagic/commit/c9282fb26) and the `EOE:` batch commits; fix [`7a1d0127d`](https://github.com/Flounder1664/wagic/commit/7a1d0127d) |
| SOS (Secrets of Strixhaven) | ~56 cards (easy bucket + Flashback/Infusion/Charm batches), incl. a Lorehold Charm crash fix with regression tests | `SOS:` commits on `wagic-v146-windows`, e.g. [`f88dde772`](https://github.com/Flounder1664/wagic/commit/f88dde772), [`4d285c00e`](https://github.com/Flounder1664/wagic/commit/4d285c00e) |
| FIN (Final Fantasy) | ~70 cards across 7 slices: Vehicles, Job-select Equipment, Town lands, Summon sagas | `FIN slice` commits on `docs/set-coverage-audit` |
| TLA (Avatar: The Last Airbender) | 8 saga-transform DFCs done without new C++ | [`3137252ae`](https://github.com/Flounder1664/wagic/commit/3137252ae) |
| TMT | 23 Sneak cards via ninjutsu reuse + alt-cost approximation, pure DSL | [`122d0c4b8`](https://github.com/Flounder1664/wagic/commit/122d0c4b8) |
| Exhaust mechanic | Pure-DSL counter pattern — 15 new cards, 14 retrofitted | [`0663d5a9f`](https://github.com/Flounder1664/wagic/commit/0663d5a9f) |
| DFT / WOE / MKM / DSK / BLB | Borderline-primitive batches with harness tests | `batch 1` commits on `docs/set-coverage-audit` |
| Six missing sets | 595 reprint registrations against existing primitives | [`2ccf9c29c`](https://github.com/Flounder1664/wagic/commit/2ccf9c29c) |
| ECL | Full new-set support (cards, images pipeline, `_cards.dat`) | [`f5a1e295c`](https://github.com/Flounder1664/wagic/commit/f5a1e295c) and follow-ups |

- Value: straight coverage of sets upstream doesn't have. Play-tested to varying degrees — the fork tracks a per-card grade (see B2), so I can say *which* cards were actually verified in game.
- Caveat: card IDs were allocated in this fork's ranges; upstream would want to review ID allocation before merging `_cards.dat` files.
- Suggested shape: one PR per set, data-only.

### A7. Android modernization

- **16 KB page-size alignment** for native libs — required on Android 15+ devices ([`221569608`](https://github.com/Flounder1664/wagic/commit/221569608)).
- **Scoped-storage fixes**: `MANAGE_EXTERNAL_STORAGE` handling, unreliable `canWrite()` under FUSE, SD-card-root support, removal of `requestLegacyExternalStorage` (unsupported at the current API target) ([`d54a8b628`](https://github.com/Flounder1664/wagic/commit/d54a8b628), [`0ad0ded6f`](https://github.com/Flounder1664/wagic/commit/0ad0ded6f), [`c7e628e55`](https://github.com/Flounder1664/wagic/commit/c7e628e55)).
- **Image-downloader crash fix**: jsoup was never packaged into the APK (only the app's own `classes.dex` shipped), so the slow scrape path died with `NoClassDefFoundError` — an `Error` that bypassed `catch(Exception)` and killed the app. Fix bundles libs as secondary dex and degrades failures to per-set errors ([`885ab5be9`](https://github.com/Flounder1664/wagic/commit/885ab5be9)).
- **Touch-input regression fix**: opening SDL joysticks on Android starves touch dispatch; scoped `#ifndef ANDROID` ([`e1db9f205`](https://github.com/Flounder1664/wagic/commit/e1db9f205)) — diagnosis written up in `LOCAL_CHANGES.md`.
- Value: keeps the Android port alive on current devices. All tested on real Android 14–16 hardware.
- Suggested shape: separate small PRs; the 16 KB and scoped-storage ones are the urgent pair.

### A8. Windows buildability (modern MSVC)

Master does not build under current Visual Studio 2022 (MSVC 14.4x/14.5x) out of the box. This fork's `wagic-v146-windows` builds clean: project/props fixes, source-level compatibility, and JGE `zipFS` support for **compressed** zip entries ([`7a32a6f30`](https://github.com/Flounder1664/wagic/commit/7a32a6f30), [`b81231d43`](https://github.com/Flounder1664/wagic/commit/b81231d43)).

- Value: anyone trying to build Wagic on Windows today hits this wall first.
- Caveat: [`7a32a6f30`](https://github.com/Flounder1664/wagic/commit/7a32a6f30) also enabled SDL gamepad input on desktop; the Android-breaking part of that was later fixed by [`e1db9f205`](https://github.com/Flounder1664/wagic/commit/e1db9f205) — take them together.
- Suggested shape: one build-fix PR.

---

## Tier B — developer infrastructure (objective, but workflow-dependent)

### B1. Headless test suite runner + regression tests

`WAGIC_TESTSUITE=1` runs the in-game TestSuite from a console build with worker threads, seed pinning, better failure reporting, and many new regression tests. **Authored by InquiringMinds-AI** (see provenance) — integrated and used heavily here; my own additions are harness fixes and a WSL build recipe. On top of it I run a 720-test baseline before every deploy.

- Where: [`81a091e42`](https://github.com/Flounder1664/wagic/commit/81a091e42) and the `Test suite:` commits.
- Value: upstream currently has no fast, scriptable regression gate; this catches real crashes (it caught several in the EOE/SOS work).

### B2. Card-verification pipeline (grades as data)

A per-card grade (`tested / verified / problem`) recorded to `card_grades.tsv`, merged into a testing worklist with test-case coverage columns. The point: "is this card actually correct in game?" becomes queryable data instead of folklore. Direct support for upstream-style card-fixing efforts (e.g. issue lists like WagicProject#1085). The in-game UI half of this is Tier C (C4) — the data format and worklist tooling stand alone.

- Where: [`edb91260e`](https://github.com/Flounder1664/wagic/commit/edb91260e), [`58902f668`](https://github.com/Flounder1664/wagic/commit/58902f668), [`39fceafc0`](https://github.com/Flounder1664/wagic/commit/39fceafc0); reconciliation design in fork issue [#30](https://github.com/Flounder1664/wagic/issues/30).

### B3. Crash diagnostics

- Windows: `CrashLog.{h,cpp}` — an unhandled-exception handler that appends turn/phase/resolving-ability breadcrumbs to `crash_log.txt`, so a card-ability crash in a Release build is no longer silent ([`7d1e2c278`](https://github.com/Flounder1664/wagic/commit/7d1e2c278)).
- Handler compiles and is wired in; not yet proven against a live crash.

### B4. Build & packaging tooling

`patch_apk.py` (rebuild native libs into an existing APK — now replacing *all* built libs), `patch_core_zip.py` (surgical core.zip updates incl. new-set files and directory markers), `assemble_apk.py` secondary-dex support, a portable `wagic_build_config` module replacing hardcoded paths, `gap_analysis.py` (Scryfall-vs-Wagic set coverage). All in the repo root / `projects/mtg/Android` on the fork branches.

### B5. Set-coverage audit + new-set guide

A 343-set audit of what's missing/unsupported and why (recurring engine walls identified), plus [`NEW_SET_GUIDE.md`](https://github.com/Flounder1664/wagic/blob/docs/set-coverage-audit/projects/mtg/NEW_SET_GUIDE.md) — an end-to-end "how to add a set" written from doing it several times. Machine-readable audit tables (per-card registry, mechanics dashboard, per-set gap counts) live in a companion repo, **wagic-tools** — currently private; I'm happy to publish it or export the audit tables into the fork if there's interest.

---

## Tier C — subjective / preference changes (recorded honestly)

These made *my* builds nicer on *my* devices. None claim rules accuracy; benefit as stated.

| Change | Where | Subjective benefit |
|---|---|---|
| Delete Deck menu option (with confirm) | [`1a6f14a59`](https://github.com/Flounder1664/wagic/commit/1a6f14a59) | Deck cleanup without filesystem access — matters on Android where the files are hard to reach |
| In-game version display | [`21a63aad0`](https://github.com/Flounder1664/wagic/commit/21a63aad0) | Knowing which build a device is running; invaluable when juggling devices, invisible otherwise |
| Demo-mode menu entry removed | in [`64833c619`](https://github.com/Flounder1664/wagic/commit/64833c619) | I never used it and mis-hit it on touch screens |
| Touch swipe-threshold + scroll-speed tuning | in [`64833c619`](https://github.com/Flounder1664/wagic/commit/64833c619) | Feel preference, tuned for RP5/S9 screens; other devices may prefer upstream values |
| 6th menu-icon column (Quick Game land sprite) | [`6a26c874d`](https://github.com/Flounder1664/wagic/commit/6a26c874d) | Cosmetic menu-icon change |
| In-duel verification hotkeys + status badges | [`a4feadd9b`](https://github.com/Flounder1664/wagic/commit/a4feadd9b), [`498acdef7`](https://github.com/Flounder1664/wagic/commit/498acdef7) | My QA workflow made visible in game (grade a card mid-duel with one key). The *data* side is B2; the badges/hotkeys are only useful if you adopt the workflow |

---

## Provenance — what is in this fork but not mine to offer

Authorship is preserved in git throughout; nothing was squashed under my name.

- **InquiringMinds-AI** ([wagicGPT fork](https://github.com/InquiringMinds-AI/wagicGPT)) — 77 commits integrated here: the headless test-suite runner and test hardening (B1), a block of engine rules-correctness fixes (delayed phase actions firing a turn late, deathtouch/lifelink/wither ignoring taught-ability damage, countered flashback spells exiling, asymmetric two-target spells, target criteria evaluated at match time instead of parse time, proliferate not being a target, silent spell fizzles, Serum Powder, copy exile-riders, and more), AI decision fixes, and card-list batches 1–50 against WagicProject issue [#1085](https://github.com/WagicProject/wagic/issues/1085). These are excellent candidates for upstream — **coordinate with/credit InquiringMinds-AI**; my contribution is integration and months of play-testing on top.
- **BobCyril / upstream PRs** — deck updates and primitive fixes from WagicProject PRs #1147, #1148, #1156, #1162, #1176 were cherry-picked *into* this fork. Already upstream or upstream-authored; listed only so nobody double-counts them.

## Deliberately not offered

Fork-specific configuration: download URLs repointed at this fork, device serials/paths, `BUILD_LOG.md` entries, deploy scripts for my local drives, and planning/backlog docs that only make sense inside this fork's workflow.

---

*Questions / cherry-pick requests: open an issue on [Flounder1664/wagic](https://github.com/Flounder1664/wagic/issues) or comment on the linked issues above. — John (Flounder1664), 2026-07-20*
