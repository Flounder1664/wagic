# Wagic — P1 Plan: Adopt upstream engine/rules fixes (InquiringMinds-AI batch)

Status: planning — not started. Tracked at [Flounder1664/wagic#8](https://github.com/Flounder1664/wagic/issues/8).
Last reviewed: 2026-06-16. Branch for work: cut from `wagic-v146-windows`.

## Context

P1 adopts the ~13 engine/rules/AI fixes from the 2026-06-10 InquiringMinds-AI
PR burst (self-closed upstream, fork at `InquiringMinds-AI/wagicGPT`). Unlike
Phase 0 (content-only), **every P1 item is C++ and changes engine behaviour**,
so each needs a compile + regression test before it can be trusted.

**Phase 0 lesson (load-bearing):** of four "easy" PRs, two were inert/wrong
against our fork — PR #1172's mana fix was a verified **no-op** (our
`AManaProducer` never populates `castRestriction`), and #1163 leaned on a
keyword our own code flags as buggy. The diffs looked clean. **Verify every
symbol against our tree and run the test before adopting.** Do not trust.

---

## ⚠ THE GATING PROBLEM — we cannot run the test suite on Windows today

`TestSuiteAI` only compiles under `-DTESTSUITE`. **There is no TESTSUITE
configuration in `projects/mtg/template.vcxproj` / `mtg.props`** — our Windows
build never defines it. `PLAYER_TYPE_TESTSUITE` (MTGDefinitions.h:39) and
`rules/testsuite.txt` exist, but PR #1155's headless runner is `#ifdef
TESTSUITE`-guarded, so it is unreachable in our shipping build. Per platform
memory we don't maintain a Qt/Linux build either.

**Without a working test harness, the behaviour-changing fixes below cannot be
safely verified.** This must be solved FIRST. Three options:

| Option | Effort | Notes |
|---|---|---|
| **(A) WSL + qt5 console build, tests only** | Low–med | Tests are platform-agnostic C++. Build `wagic-qt.pro CONFIG+=console CONFIG+=debug DEFINES+=CAPTURE_STDERR` in WSL purely as a test harness; never ship it. Cleanest separation; doesn't touch the Windows project. **Recommended.** |
| **(B) Add a TESTSUITE config to the Windows vcxproj** | Med | Net-new build config (define `TESTSUITE`, wire `WAGIC_TESTSUITE` headless exit from #1155). Keeps everything on one toolchain but adds a config we must maintain. |
| **(C) Manual in-game verification only** | High per-fix | No harness. Eyeball each fix in a Baka game on Windows. Infeasible for timing fixes (#1158) and AI ranking (#1166). Last resort. |

**Decision needed from user before P1 execution.** This plan assumes (A).

---

## Prerequisite Tier — stand up the test harness (do before any fix)

Adopt the test-infra PRs first; they are the foundation that lets every later
fix ship with a green regression run.

- **#1155 `feat/headless-test-suite`** — `WAGIC_TESTSUITE=1` env → auto-run suite,
  exit non-zero on failure (GameStateDuel.cpp, GameStateMenu.cpp, both
  `#ifdef TESTSUITE`). Verify: `PLAYER_TYPE_TESTSUITE`, `testsuite.txt`,
  `testSuite->nbTests/nbFailed/nbAITests/nbAIFailed` fields exist in our fork.
- **#1168 `fix/testsuite-reliability`** — **7-commit branch**, all test-harness
  hardening (seed honoring, serialize file loading across workers, ignore
  out-of-range menu clicks, reveal-zone clickable, report typo'd state keys,
  FORCEABILITY forces AI cast). Cherry-pick the whole branch range
  `2627822d7..4ea0e4da6` (+ `355ef5b6c`). High value: makes the suite
  deterministic and non-crashing.
- **#1170 `test/maxcast-land-zerodrop-pin`** — pure regression test (issue #689).
- **#1157 `test/entomb-library-graveyard`** — pure regression test for the
  library→graveyard EOT crash (matches our upstream-observed #1120). Test-only,
  no engine change — adopt to lock the behaviour.

Exit criteria for this tier: `WAGIC_TESTSUITE=1 ./wagic` (option A build) runs
the existing suite to completion and reports pass/fail counts.

---

## Fix Tier — per-PR triage

Risk legend: 🟢 self-contained/additive · 🟡 net-new symbols to verify · 🔴 changes
existing behaviour (regression risk — needs suite green before+after).

| PR | Branch / fix commit | Touches | Risk | Verify before adopting | Deps |
|---|---|---|---|---|---|
| **#1161** Proliferate doesn't target | `fix/proliferate-does-not-target` | TargetChooser.cpp | 🔴 | Pure deletion of shroud/hexproof/protection checks in `ProliferateChooser::canTarget`. Correct per CR 701.27a. Confirm `ProliferateChooser` signature matches. | — |
| **#1174** Countered flashback → exile | `fix/countered-flashback-exile` | ActionStack.cpp | 🟡 | Confirm `ManaCost::MANA_PAID_WITH_FLASHBACK`, `Constants::TEMPFLASHBACK`, `putInExile()` exist. 10 lines, clean. | — |
| **#1159** Kathari Bomber sacrifice | fix commit `475c5e0a6` (NOT tip) | primitives + test | 🟢 | Tip `290c2cf0c` is a *Defense of the Heart* test — take both commits but know which is which. | — |
| **#1160** Gulf Squid tap lands | `fix/gulf-squid-target-player` | primitive + TestSuiteAI | 🟢 | Adds `tappedinplay:` assertion to harness (needs prereq tier) + card fix. | prereq |
| **#1167** AI targets by effect not source | fix commit `98388f8d5` (NOT tip) | AIPlayerBaka | 🟡🔴 | Tip `f53d94aa4` is RNG-seed pin. AI-only, no rules risk. | — |
| **#1166** AI ranking: keep ties, prefer kills | `fix/ai-ranking-dropped-actions` | AIPlayerBaka.{h,cpp} | 🔴 | Deterministic comparator + damage-eval heuristic change. AI-only. Run AI tests before/after. | — |
| **#1154** Deathtouch via taught damage | `fix/deathtouch-taught-damage` | AllAbilities.h, MTGAbility.{h,cpp} | 🟡 | New `MTGAbility::propagateSource`. **Verify `NestedAbility::ability` and `MultiAbility::abilities` members exist** in our fork (the dynamic_casts depend on them). | — |
| **#1164** Copies drop exile riders | `fix/populate-exile-riders` | MTGCardInstance.{h,cpp}, AllAbilities.cpp | 🟡 | New `exileRiderSuppressed` member. **Verify `Constants::UNEARTH/EXILEDEATH/GAINEDEXILEDEATH` and `AACloner::resolve`** exist. Fixes the Populate/Zektar bug (#1145). | — |
| **#1171** Dynamic manacost criterion | `fix/dynamic-manacost-criterion` | CardDescriptor.{h,cpp}, TargetChooser.cpp | 🟡 | New members + `currentManacostCriterion()`. Verify `convertedManacost`, `manacostComparisonMode`, `valueInRange`, `WParsedInt`. Fixes Dreadhorde Arcanist (#1125). | — |
| **#1158** Delayed phase actions timing | `fix/delayed-phaseaction-timing` | AllAbilities.cpp, MTGAbility.cpp | 🔴 | Changes `APhaseAction::Update` + `parsePhaseActionAbility` (the `next`-guard + NULL-target handling). Broad — many delayed triggers. Suite green mandatory. Fixes Arcane Denial (#1126). | — |
| **#1173** Asymmetric two-target spells | `fix/asymmetric-two-target-spells` | MTGAbility.cpp | 🔴 | New control flow in spell-line parsing; re-parses via `GenericTargetAbility`. Confirm that ctor signature. Regression risk on spell parsing broadly. | — |
| **#1175** Bare moveto() fizzle | `fix/spell-line-moveto-chooser` | MTGAbility.cpp | 🔴 | **Extends the exact code block #1173 adds** (`plainMove` next to `plainDamage/plainPT`). **MUST adopt #1173 first.** | **#1173** |

---

## Sequencing

1. **Decide harness option (A/B/C)** — user call. Assume (A): stand up WSL qt5
   console test build.
2. **Prerequisite tier**: #1155 → #1168 → #1157, #1170. Get a green baseline run.
3. **Low-risk rules fixes** (🟢/🟡, isolated, each ships with its `*_i1085`/regression
   test from the batch): #1174, #1159, #1160, #1164, #1171, #1154.
   - For each 🟡: grep-verify the named symbols in our tree FIRST (Phase 0 lesson).
4. **Behaviour-changing fixes** (🔴, suite must be green before+after each):
   #1161, then #1173 → #1175 (ordered), then #1158.
5. **AI fixes** (🔴 AI-only): #1167, #1166 — run the AI test subset; accept if no
   regressions and they don't make Baka obviously worse.
6. **Revisit #1172** (the no-op): only if we choose to write the missing
   mana-parser change (`MTGAbility.cpp:~5432` extract `restriction{...}` →
   `castRestriction`). Separate task; not part of this batch.

One git commit per PR (or per coherent multi-commit branch), each message
recording the upstream PR # and the symbols we verified. Rebuild core.zip only
for fixes that touch primitives (#1159, #1160). Deploy to `G:\` after the tier
completes, not per-fix.

---

## Per-fix verification method

For every fix:
1. **Symbol check** — grep our `src/`+`include/` for each new type/member/constant
   the diff references. If any is missing → STOP, reclassify (this is the #1172
   trap).
2. **Apply** — cherry-pick the specific commit(s) (mind multi-commit branches:
   #1159 fix=`475c5e0a6`, #1167 fix=`98388f8d5`, #1168=range).
3. **Build** — Windows Release (ship build) + the test harness build (option A).
4. **Test** — `WAGIC_TESTSUITE=1` run; the fix's own regression test must pass and
   no previously-passing test may regress.
5. **Spot-play** (🔴 only) — one Baka game exercising the card/interaction.
6. **Commit** — record PR # + verified symbols + test result.

---

## Open decisions for the user

1. **Test harness: option A (WSL qt5), B (Windows TESTSUITE config), or C
   (manual)?** Gates everything. (A) recommended.
2. **AI heuristic changes (#1166, #1167)** — adopt, or hold? They change Baka's
   play and have no regression test that proves "better", only "different".
3. **#1172 mana-parser completion** — write the missing piece, or leave Adarkar
   Unicorn-class cards as known-broken and move on?
