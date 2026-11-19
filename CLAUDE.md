# CLAUDE.md

Guidance for Claude Code sessions working in this repository. This is John's fork of
Wagic; the work here is mostly writing card primitives, fixing the engine so they work,
and shipping one Windows build (plus Android when asked).

## First thing every session: get onto trunk

New session worktrees have been cut from `master` (the upstream mirror), which has none of
this fork's work: no fork card data, no build fixes, and not even this file. Before
anything else:

```bash
git fetch origin
git merge --ff-only origin/wagic-v146-windows     # a fresh session branch has no commits, so this is safe
sh tools/check-branch-divergence.sh               # must print "nothing unmerged"
```

If the fast-forward refuses, the branch already has work on it: merge trunk in instead.
If `tools/check-branch-divergence.sh` does not exist, you are still on `master`.

## Fork branch map

**`wagic-v146-windows` is the trunk. There is exactly one build, and it comes from trunk.**

- `master`                = upstream `WagicProject/wagic` (GitHub's default branch, by John's choice)
- `wagic-v146-windows`    = **trunk** - the only branch anything is ever built or deployed from
- `feature/*`, `claude/*` = short-lived: branch from trunk, merge back the same session
- `wip/*`                 = deliberately parked, each one commit of unlanded work

### Rules that keep it that way

1. **Branch from trunk, merge to trunk, same session.** A branch that outlives the work
   becomes a second game. On 2026-08-15 two lines had run in parallel for six weeks -
   131 and 120 commits - and John ended up with features in one build that were missing
   from the other.
2. **Merge; never re-port by hand.** Cherry-picking a fix "across" instead of merging is
   how the crash handler and the TestSuite null-guard each got written twice, differently.
3. **Build only from trunk**, and only after merging your branch into it.
4. **Before finishing a session, run `tools/check-branch-divergence.sh`** and commit or
   park anything uncommitted. Its exit code is the number of branches trunk lacks.
5. **Card data merges semantically, not textually.** A `borderline.txt` conflict is usually
   two different new cards appended at the same place; resolve by `[card]` block keyed on
   `name=`, never by picking a side.

Commit as each piece works, one logical change per commit. `origin` is a **public** repo:
scan commits for secrets before pushing.

## Where things live

| What | Where |
|---|---|
| Engine source | `projects/mtg/src`, `projects/mtg/include`, `JGE/` |
| Card primitives (what a card does) | `projects/mtg/bin/Res/sets/primitives/` - `mtg.txt`, `borderline.txt`, `planeswalkers.txt`, `unsupported.txt`, `_macros.txt` |
| Set registration (id, rarity, which primitive) | `projects/mtg/bin/Res/sets/<SET>/_cards.dat` |
| Harness tests | `projects/mtg/bin/Res/test/`, registered one per line in `test/_tests.txt` |
| Helper scripts, audits, worklists, art tooling | the separate private **`wagic-tools`** repo (`../wagic-tools` from the main checkout). New scripts go there, not here |
| The game John plays | `G:\Wagic-windows` (`Wagic.exe`, `Wagic-testsuite.exe`, `Res\core.zip`, `User\`) |
| Change history | `LOCAL_CHANGES.md` (one row per change), `BUILD_LOG.md` (what was installed where) |

Only Windows and Android are targets. Ignore PSP, iOS, macOS and desktop Linux; the Qt
console build under WSL exists purely to run tests.

## The working loop

A card is **done** when it is written in full, proven by a test that could have failed,
and shipped. In order:

1. **Write the primitive.** Copy the form from an existing working card rather than
   inventing one. An ability the parser does not understand does nothing and reports
   nothing, so "it loaded" is not evidence.
2. **Implement the whole card.** A `missing=` line means the card is effectively
   unsupported. Use it only when the engine truly cannot do the thing, and say so.
3. **Test in the WSL harness** (below). Pair every positive assertion with something that
   proves the ability is live: a negative twin, or a `:0` absence assertion. Then
   `wagic-tools/prove_test.py <test>` must say PROVEN: it runs the test on the card data
   from before your change and again now.
4. **If the harness cannot check it** (choosing a trigger's target, reveal windows, menus,
   anything visual), queue a hand-played scenario with the `wagic-scenario` skill. One
   scenario tests one untested feature of one card. Before queueing, run
   `wagic-tools/audit_token_art.py --card <card>`: a token or emblem with no picture is a
   defect to fix, not something for John to find.
5. **Commit, merge into trunk, build from trunk, deploy** (below). For card data only,
   `wagic-tools/ship_card_data.py` does the push, `core.zip` patch, read-back, backup
   pruning and `BUILD_LOG.md` line in one step (dry run unless `--go`).
6. On a pass in game, record `#VERIFIED IN GAME <date> ...` under the card's `name=` line.

**Card data is linted on commit.** `tools/git-hooks/pre-commit` runs
`wagic-tools/lint_primitives.py` whenever a commit touches `Res/sets` or `Res/test`
(enabled per clone by `git config core.hooksPath tools/git-hooks`). It fails only on
findings that are not in `wagic-tools/audits/lint_baseline.txt`; run it by hand with
`--all` to see the known ones. Do not bypass it with `--no-verify`: fix the finding, or if
it is a deliberate exception, `--update-baseline`. When a new kind of silent failure turns
up, add a check for it there rather than a note.

File format traps that have each cost a session (the lint catches the first two):

- Primitives and `_tests.txt` are **CRLF**. Git Bash `sed -i` strips the CRs; edit with the
  Edit tool or Python in binary mode, and check before packaging.
- Backslashes written through a shell heredoc get collapsed (a `\b` became a backspace
  byte). Build them from character codes and verify the bytes.
- A deck file loads whatever it names. Do not put rarity `T` cards (back faces, tokens)
  in a hand-written deck; name the front face.

## Testing (WSL harness)

The headless `TestSuiteAI` runs under WSL against the **loose** files in `Res/`, so
`projects/mtg/bin/Res/core.zip` must be absent while testing.

```bash
# build to a log - never pipe make through head/grep, it kills the build and leaves stale objects
wsl -e bash -lc 'cd ~/wbuild_np && make -j$(nproc) > ~/wbuild_np/build.log 2>&1; echo rc=$?; grep -c "error:" ~/wbuild_np/build.log'

# run - the working directory must be projects/mtg/bin
wsl -e bash -lc 'cd /mnt/m/Claude_projects/wagic/projects/mtg/bin && ~/wbuild_np/wagic'
# ends with: "TestSuite done: failed test: N out of M total" - N must be 0
```

- `WAGIC_TESTSUITE_ONLY=<substring>` runs only the matching tests.
- `~/wbuild_np` is configured against the main checkout. To test a worktree's changes,
  configure a build directory against that worktree, or merge first.
- If an engine change appears to do nothing, compare the `.o` timestamp with the source
  before theorising about the code.
- The harness says nothing about rendering or input. A passing suite does not mean the
  Windows GUI works.

## Building and deploying

Use the skills; they hold the full recipes and are kept current:

- **`wagic-windows-build`** - MSBuild recipe, then deploy to `G:\Wagic-windows`. Whenever
  the engine changes, rebuild **both** `Wagic.exe` and `Wagic-testsuite.exe`; a stale
  testsuite exe produces false failures in John's scenario queue.
- **`wagic-android-build`** - `libmain.so`, patched APK, per-device install. Only when John
  asks for a device build.
- **`wagic-scenario`** / **`wagic-scenario-queue`** - writing and running hand-played checks.

Rules that apply to every deploy:

- Deploy to `G:\` only by default. Devices only when John is testing on them.
- **Launch what you built before it replaces John's working copy.** Three broken builds
  shipped in one session by skipping this.
- `G:\Wagic-windows\Res\` loads every `*.zip`, alphabetically last wins. Leave exactly one
  live zip.
- After a `core.zip` deploy that adds cards, run the collection chain in `wagic-tools`
  (`build_collection`, then `fix_decks` if ids moved) or the cards never reach the deck
  editor.
- Keep the 3 newest backups of each exe and `core.zip` on G:, delete older ones.
- **Rename `G:\Wagic-windows\User` to take it out of play; never delete it.** The card
  images in it are the one thing that cannot be regenerated. Never run a destructive
  command on a path a background task may still be touching.
- Add a line to `BUILD_LOG.md` for each deploy: date, trunk commit, target, what was checked.

## Architecture

Two layers:

- **JGE** (`/JGE/`) - the platform-abstraction layer: rendering, audio, resources, input.
  Platform code is in `JGE/src/pc/`, `JGE/src/android/`, `JGE/src/qt/`.
- **MTG game** (`/projects/mtg/`) - cards, abilities, AI, GUI, rules, zones, decks.

| Subsystem | Key Files | Role |
|---|---|---|
| Card Data | `MTGCard.*`, `MTGCardInstance.*` | Card definitions and live instances |
| Card GUI | `CardGui.*` | Rendering individual cards |
| Game State | `GameObserver.*`, `GameState.*`, `GameStateDuel.*` | Top-level game flow |
| Abilities | `MTGAbility.*`, `AllAbilities.h`, `AbilityParser.*` | Ability classes and the primitive-text parser |
| AI | `AIPlayer.*`, `AIPlayerBaka.*`, `AIMomirPlayer.*` | Computer opponents |
| Rules Engine | `Rules.*`, `MTGRules.*`, `ModRules.*` | Core rules and rule mods |
| Game Zones | `MTGGameZones.*` | Hand, library, graveyard, battlefield, stack |
| Stack/Actions | `ActionStack.*`, `ActionLayer.*` | Spell stack, triggered and activated abilities |
| GUI Layers | `GuiLayers.*`, `DuelLayers.*`, `GuiCombat.*` | Layered in-game UI |
| Deck System | `MTGDeck.*`, `DeckManager.*`, `DeckView.*` | Deck loading, editing, selection |
| Test harness | `TestSuiteAI.*` | Scripted tests, compiled in with `-DTESTSUITE` |

The ability system is the most complex part. When a card needs something new, look for an
existing ability class and parser branch that does something close before adding one.

Engine code notes:

- Include `PrecompiledHeader.h` first in every `.cpp`.
- MSVC limits `else if` chain depth (error C1061) in the big parser functions; add an
  early return or a helper instead of another branch.
- On Windows `snprintf` is `sprintf_s` and aborts on overflow instead of truncating; size
  fixed buffers by hand.
- A NULL guard that returns early can be worse than the crash: fix the accessor so it
  cannot return NULL rather than bailing at one call site.
- A new in-game key needs a runtime bind after options load, not only a JGE default.

The upstream Travis and AppVeyor configs are not used by this fork.
