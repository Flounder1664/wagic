# Feature Request: In-game Card Verification Mode ("does this card actually work?")

**Status:** proposal
**Related:** the `T` bug-flag hotkey (in `DuelLayers`), the set-coverage audit in `projects/mtg/audits/` (`SUMMARY.md`, `master_grade_table.tsv`, `README.md`).

## Summary

Extend the existing in-duel **bug-flag hotkey** into a small set of **card-status hotkeys** so a human playtester can, while playing, mark the card under the cursor as **works 100%**, **mostly works** (with a note), or **broken** (the existing bug flag). Each press appends a per-card status record. The goal is to make it practical for a person to walk the whole card pool and record the *behavioural* status of every card that isn't already known-good, and to see at a glance what still needs checking.

## Motivation

The audit (`projects/mtg/audits/SUMMARY.md`) measures **presence, not faithfulness**: a primitive existing in `mtg.txt` counts as "supported" even when it strips the card's mechanic. That correction (2026-07-11) is the whole point here — the fork's hand-authored new-mechanic cards are exactly where "supported" lies (ECL vivid 0/14 faithful, EOE warp 4/50, Rescue Skiff shipping as a vanilla 5/6, etc.). The only way to know a card is *actually* correct is for a human to see it resolve in a real game.

Today we have half of that loop: the `T` key flags a **broken** card with full context (name, id, set, zone, current-vs-printed P/T, turn/phase) to `User/bugreports.txt`. What's missing is the **positive** and **partial** signals and a durable per-card record — so there's no way to know:

- which cards a human has actually confirmed correct,
- which "work but with a caveat,"
- and therefore **what's left to test**.

Without that, verification isn't resumable or shareable, and testers re-check the same trivial cards while genuinely risky ones go unexamined.

## Goal

Let a human systematically test **every card not already expected or noted to be 100%**, recording status as they go, with the trivially-correct cards pre-marked so effort focuses on the risky ones (hand-authored new-mechanic cards per the audit).

## Proposed solution

### 1. Status model

Per card (keyed by `set` + `id` + `name`):

| Status | Meaning |
|---|---|
| `UNTESTED` | default — no human has confirmed behaviour |
| `VERIFIED` | confirmed 100% correct in a real game |
| `PARTIAL` | functions but with a known caveat (rendering, a rider ignored, timing, etc.) — **requires a short note** |
| `BROKEN` | does not work / wrong behaviour (today's bug flag) — note encouraged |

Latest record per card wins. This is a *faithfulness* layer that sits on top of the audit's *presence* grade — a card can be `supported` in the grade table yet `BROKEN`/`PARTIAL` here.

### 2. Hotkeys (reuse the `T` infrastructure)

Three keys active in a **test/verification mode**, bound at runtime (per the keybinding-reset gotcha — saved `keybindings_sdl` wipe SDLmain defaults, so bind in the `DuelLayers` ctor):

- **V** → `VERIFIED`
- **P** → `PARTIAL` (prompt/queue a short note)
- **T** → `BROKEN` (existing bug flag, unchanged)

All three reuse the card resolution already built for `T`: hand + battlefield cards, and the highlighted card inside an opened pile (graveyard/exile/library/command zone/sideboard). Each press shows the same on-screen toast confirmation.

### 3. Persistence

Append to `User/card_status.tsv` (tab-separated to match `master_grade_table.tsv`), one row per press:

```
set  id  name  status  note  tested_by(profile)  date  turn/phase  cur_pt/printed_pt
```

A small tool in `projects/mtg/audits/` consolidates to a latest-status-per-card table and can **join it against `master_grade_table.tsv`** to produce a single "state of every card": exists? registered? written? graded? **verified?**

### 4. Pre-seed the "already expected 100%" set

So testers skip the trivial mass and focus on risk, auto-mark as `VERIFIED` (or a distinct `TRIVIAL`) the cards that are mechanically incapable of being wrong:

- basic lands and tokens,
- French-vanilla cards (primitive is only mana cost + type + P/T, no `auto=` / `text=` ability body),
- reprints reusing a long-proven primitive (audit notes these are low-risk).

This is derivable from the core.zip primitive files (same source the audit's `grade_index.json` came from). The remaining `UNTESTED` set is then exactly "cards a human still needs to look at" — and the audit already tells us to prioritise hand-authored new-mechanic cards within it.

### 5. On-screen status indicator

While hovering/selecting a card, show its current status (UNTESTED / VERIFIED / PARTIAL / BROKEN) as a small badge, so the tester sees what's already been done without leaving the game.

### 6. Test-mode gating

Gate the V/P keys behind a "Verification mode" (a `GameOptions` toggle, or the existing test/sandbox context) so normal play can't accidentally mark cards. `T` can stay always-on as it is now. This also fits naturally on `feature/draft-mode`, which is already a testing-oriented context.

## Surfacing the cards that need testing (decided plan: #1 + #3 + #6)

Closed loop: **#1** produces the ordered worklist → **#6** serves the next untested card → the V/P/T keys write `card_status.tsv` → **#1** re-reads to update → **#3** reflects current status in-game.

### #1 — Worklist tool (keystone, out-of-game, build first)

A script in `projects/mtg/audits/`. **Inputs:** `User/card_status.tsv` (statuses) + `master_grade_table.tsv` / primitive `grade_index.json` (universe + grade) + trivial-detection (basic lands, tokens, French-vanilla primitives). **Output:** the remaining `UNTESTED` non-trivial cards as a ranked TSV + Markdown checklist, plus per-set verified %. **Default rank:** risk-first (hand-authored new-mechanic cards per the audit), with `--by-set` / `--grade` sort options. Everything else consumes its output. Nearly free — reuses the audit pipeline.

### #3 — In-game status badge (small)

On the hovered/selected card, a small badge/tint driven by a status map loaded at startup from `card_status.tsv` (keyed set+id): `UNTESTED` neutral / `VERIFIED` green / `PARTIAL` amber / `BROKEN` red. Reuses the `CardGui` render path. Makes remaining work visible where the tester already is.

### #6 — Spawn-next / verification queue (most work, directed sweep)

A verification-mode command that instantiates the next `UNTESTED` card (in worklist order) directly into hand/play via the testsuite / debug-summon path, with a small on-screen queue of the upcoming few that advances as you mark V/P/T. The fastest way to walk the whole pool — no deck-building, no waiting to draw. **Caveat:** interaction-heavy cards still need manual board setup (a legal target, a creature to enchant); `PARTIAL`+note absorbs those cleanly.

**Build order:** #1 (free keystone) → #3 (small, independently useful) → #6 (needs the spawn path). #1 and #3 both deliver value before #6 exists.

## Phasing

- **P1 (small — reuses everything `T` already has):** V + P keys, `card_status.tsv` logging, toast, note capture for P/T. Immediately useful.
- **P2:** pre-seed trivial cards; hovered-card status badge; verification-mode toggle.
- **P3:** spawn-arbitrary-card + "next untested" navigation; audit-side consolidation tool joining status ↔ `master_grade_table.tsv`; per-set verification % in reports.

## Open questions / decisions

- **Keys:** V / P chosen for mnemonics — confirm no clash with duel actions; bind at runtime regardless.
- **Storage:** single `card_status.tsv` vs per-set; how to merge multiple testers/profiles (Bob, Maxglee, …). Latest-wins vs keep history.
- **"Trivial" definition:** which primitive shapes auto-qualify as pre-verified (and whether to use a separate `TRIVIAL` status so it's distinguishable from human-`VERIFIED`).
- **Faithfulness bar:** does `VERIFIED` mean "matches Oracle text exactly" or "played without a visible problem"? (Suggest: matches Oracle intent; anything short = `PARTIAL` + note.)
- **Gating:** verification-mode toggle vs always-on.

## Non-goals

- Not a replacement for the automated `TestSuiteAI` (scripted assertions). This is **human spot-verification** of real behaviour — it catches rendering, timing, UI, and interaction faithfulness that scripts don't, and it produces the faithfulness signal the presence-based grade can't.

## Why now / fit

- Reuses the just-built `T` machinery (`DuelLayers::TagBuggyCard` hook, hand/battlefield + opened-pile card resolution, runtime key bind, toast) — P1 is a genuinely small change.
- Directly fills the audit's faithfulness gap and turns "read every primitive body vs Oracle" (manual, static) into "confirm it in a game" (empirical, resumable, shareable).
- Natural home: `feature/draft-mode` (a testing context), alongside the bug-flag hotkey already there.
