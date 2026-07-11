# Implementation Roadmap — prioritized (decided 2026-07-11)

Priorities set with the user, tier by tier, over the blockers in [GAP_SUMMARY.md](GAP_SUMMARY.md)
Part 2 and the physical categories in [PHYSICAL_ADAPTATION_PLAN.md](PHYSICAL_ADAPTATION_PLAN.md).
"Unlocks" = approximate cards made faithfully-DONE.

## HIGH — build first

| Item | Tier | Unlocks | Approach |
|---|---|---|---|
| **Copy a triggered/activated ability** | A | 25–30 (catalog-wide) | shared ability-on-stack copy; borderline.txt already flags the gap |
| **EOE Warp** (faithfulness) | B | ~46 | alt cast-from-exile hook, then repair the 46 stripped cards |
| **ECL Vivid** (faithfulness) | B | 14 | new "colors among your permanents" count var; worst offender (0/14) |
| **ECL Behold** (faithfulness) | B | 10 | additional-cost hook |
| **TLA bending keywords** (Waterbend/Earthbend/Airbend/Exhaust) | B | 59 | 4 new keywords; biggest single step to make TLA real |
| **TMT Sneak** | B | 26 | extend the existing Ninjutsu alt-cost C++ class |
| **SOS Prepared copy-split + Paradigm** | C | 41 | split-card / cast-copy-from-exile mechanic |
| **Converge / variable-mana-color scaling** | C | 9+ (reusable) | mana-spent color tracking (also older sunburst) |
| **Dice-rolling (d6/d20)** | D | 14+ (reusable) | extend coin-flip; reused by future real dice sets (AFR) + Ol' Buzzbark |

## MEDIUM — planned

| Item | Tier | Unlocks | Approach |
|---|---|---|---|
| **Splice onto Arcane** | A | 34 | cast-time text-append (Kamigawa block) |
| **EOE Station** (faithfulness) | B | ~23 | charge-counter threshold state |
| **EOE Void** (faithfulness) | B | ~8 | per-turn "something left the battlefield" tracker |
| **ETB-trigger doubling** (Panharmonicon/Yarok) | C | recurring | shared trigger-multiplier hook |
| **Augment // Host** | D | ~20 | **reuse the existing Mutate merge system** (241 cards); only half-card repr + augment cost are new |

## LOW — someday / opportunistic

| Item | Tier | Notes |
|---|---|---|
| Contraptions (assemble/crank/sprockets) | A | 55 cards but all silver-border UST; big subsystem |
| Multiplayer voting / will-of-council | A | 40–50; functions in 1v1 but mostly Commander flavor |
| Banding / bands-with-other | A | 41 classic vanilla creatures; fiddly combat rework |
| Draft-matters / hidden-agenda | A | 28; needs a draft-time layer, narrow pool |
| Stack one-offs cluster | C | Willbender/change-target, Fact-or-Fiction two-pile, Commandeer, Mairsil "has all abilities", Time Stop "end the turn", copy-for-each-target, exchange-control — tackle individually when one is worth it |
| Watermark-matters | D | 11 un-cards; data plumbing |
| Name/letter/word/artist analysis | D | 20 un-cards; string helpers |
| Fractional ½ values | D | 12 un-cards; could cheat (round / ×2) |
| Planar subsystem (Planechase) | E | ~50; needs a whole planar format + die + game mode |
| **Physical adaptations** (all) | — | see the dedicated table below |

## Physical / social adaptations — LOW (approaches decided)

| Cat | Cards | Approach (decided) |
|---|---|---|
| A3 Manual dexterity (Chaos Orb, Falling Star, Ol' Buzzbark) | ~15 | **Probability-WEIGHTED target** (not uniform random) — model real-flip odds: favor clustered / larger / central permanents |
| A1 Person outside the game (Kindslaver) | ~7 | **AI pilots the player**, but with **degraded/confused priorities** (disruptive outsider plays badly, not to win); reusable for Mindslaver |
| A2 Subgames (Shahrazad) | ~4 | **Coin-flip a winner** + apply life rider (skip nested game) |
| A8 Ante / gambling | ~18 | **Within-game ante zone** (functions, no real collection loss) |
| A4+A5 Balance-on-body + say-a-word/Gotcha | ~34 | **UI button / toggle** stand-in |
| A6 Real-world timing | ~6 | **Countdown timer** (nearly free digitally) |
| A7 "name a card" subset | ~4 | **Menu picker**, lowest priority |

## SKIP / NEVER (excluded from any "100%" target)

| Item | Cards | Why |
|---|---|---|
| A7 real-world trivia / body / physical contest | ~10 | no digital analogue (arm-wrestle, quote-from-memory, real-world facts) |
| A9 cross-game "next game" riders | ~5 | one-off duels; user chose to skip rather than drop-rider or same-game |

## Parallel track — pure-DSL backlog authoring (NO engine work, HIGH value)

Independent of every blocker above: the recent sets have large **UNWRITTEN backlogs that need only DSL
authoring** (existing primitives/patterns), fully parallelizable:

- TLA ~178 (118 med, 60 easy) · TMT ~153 (52 med, 101 easy) · SOS ~157 (149 med, 8 easy) ·
  FIN ~165 (143 med, 21 easy) · SPM ~82 (58 med, 24 easy) · EOE ~61 (50 med, 11 easy).
- **SOS quick win:** 8 cards whose primitive already exists but aren't wired into `sets/SOS/_cards.dat` — just add the rows.
- **Housekeeping:** 26 stale `missing_cards_by_sets` entries to delete; stray registrations in TLA(4)/TMT(5)/ECL(1)/SPM(2); loose `ecl_*.txt` WIP to archive.

## Suggested execution order

1. **ECL/EOE faithfulness (HIGH Tier B): vivid, behold, warp** — the fork already ships these as
   "done"; correctness first, and vivid/behold are small.
2. **Copy-triggered-ability + Dice + Converge** — reusable engine capabilities that pay off catalog-wide.
3. **TLA bending keywords + TMT Sneak + SOS Prepared** — make the barely-implemented recent sets real.
4. **Pure-DSL backlog authoring** (parallel track) — ~735 cards, no engine work, farm out anytime.
5. **MEDIUM** items (splice, station, void, trigger-doubling, augment/host) as capacity allows.
6. **LOW** subsystems + physical adaptations opportunistically.
7. Leave SKIP/NEVER (~15 cards) permanently excluded.
