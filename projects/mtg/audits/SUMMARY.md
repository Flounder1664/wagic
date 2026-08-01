# Wagic Set Coverage Audit — Consolidated Summary

Full-catalog audit of missing / unsupported cards, all 343 registered sets, oldest→newest.
Completed 2026-07-11. Method, grade definitions, and the two gap-types are in [README.md](README.md).
**Per-set state table + plan-by-blocker: [GAP_SUMMARY.md](GAP_SUMMARY.md). Prioritized roadmap
(decided with the user): [ROADMAP.md](ROADMAP.md).**
Per-era docs: `OLD-01`…`OLD-14`. Per-flagship docs: `../<CODE>_BACKLOG.md`. Live tracker:
[PROGRESS.md](PROGRESS.md). Mechanical backbone: [master_grade_table.tsv](master_grade_table.tsv).

## Catalog-wide numbers (mechanical, from master_grade_table.tsv)

| Metric | Count |
|---|---|
| Sets scanned | 343 |
| Card registrations (`primitive=` rows across all `_cards.dat`) | 76,409 |
| Resolve to **supported** primitive | 44,795 |
| Resolve to **borderline** primitive | 24,090 |
| **Playable (supported + borderline)** | **68,885 (90.2%)** |
| Resolve only to **unsupported** (registered but doesn't work) | 2,653 |
| **UNWRITTEN** (registered, no primitive anywhere — dangling) | **4,871** |

So catalog-wide, ~9.8% of registered cards don't actually play: ~6.4% dangling (no primitive)
and ~3.5% resolving to an unsupported stub.

**⚠️ These counts measure PRESENCE, not FAITHFULNESS.** "Playable" = a primitive of that name exists
and loads; it does not verify the printed rules are implemented. Body inspection found this is
**systemic in the fork's hand-authored recent standard sets**: **ECL** ships ~26 new-mechanic cards
with the keyword stripped (vivid 0/14 faithful, behold 2/12), and **EOE** is the same (warp 4/50,
station 5/28, void 4/14 faithful; e.g. Rescue Skiff ships as a vanilla 5/6 with Station gone). So the
"playable/implemented" figures are an **upper bound** — reprints reusing old primitives are
low-risk, but hand-authored new-mechanic cards across ECL/EOE (and likely SOS/TLA/TMT to the extent
they authored new keywords) may be approximations. Faithfulness was exhaustively checked only for ECL
and spot-checked for EOE.

## Flagship sets (recent; audited by Scryfall-vs-`_cards.dat` diff)

| Set | Year | True | Playable | Excluded | Headline |
|---|---|---|---|---|---|
| FIN | 2025 | 313 | 137 | 176 | all excluded are UNWRITTEN; 11 engine-blocked (Land//Adventure MDFC, meld) |
| EOE | 2025 | 266 | 203* | 63 | *many "implemented" are approximations (warp 4/50, station 5/28, void 4/14 faithful); Dominion Bracelet engine-blocked |
| SPM | 2025 | 193 | 110 | 83 | all excluded are UNWRITTEN; only Web-slinging engine-blocked (1) |
| TLA | 2025 | 286 | 49 | 237 | **4 new keyword walls**: Waterbend/Earthbend/Airbend/Exhaust (59); 118 medium, 60 easy; 4 dup registrations |
| ECL | 2026 | 278 | 278* | 0 | *registered & playable but **NOT faithful** — ~26 new-mechanic cards strip the keyword (**vivid 0/14** faithful, behold 2/12, blight 19/24); loose `ecl_*.txt` WIP stale; 1 stray reg |
| TMT | 2026 | 195 | 16 | 179 | only **Sneak** a real wall (26); Alliance/Disappear refuted (already supported); 5 stray regs |
| SOS | 2026 | 271 | 49 | 209 | **+8 written-but-not-wired cheap wins**; 22 doc-drift cards reconciled; 52 engine-blocked |

## Old / mid-era sets (audited from upstream `missing_cards_by_sets` + staleness recheck)

Distinct = per-era deduped (cross-era reprint overlap not removed). "OOS" = out-of-scope
(silver-border un-sets / Planechase planes).

| Batch | Era | Sets | Distinct missing | Stale | Notable OOS | Dominant real engine gap |
|---|---|---|---|---|---|---|
| OLD-01 | 1993-96 | 16 | 245 | 2 | — | **banding (41)**, ante, dexterity, subgame |
| OLD-02 | 1997-00 | 16 | 205 | 2 | UGL 57 | banding (phasing/cum.upkeep confirmed *supported*) |
| OLD-03 | 2000-03 | 16 | 194 | 0 | 6 planes | splice, two-pile, copy/counter-ability |
| OLD-04 | 2004-07 | 16 | 291 | 1 | UNH 123 | **splice-onto-Arcane (34)**, cumulative upkeep |
| OLD-05 | 2007-09 | 16 | 160 | 0 | — | clash-riders (mechanics themselves supported) |
| OLD-06 | 2010-12 | 16 | 98 | 0 | — | join forces (transform/infect confirmed supported) |
| OLD-07 | 2012-14 | 16 | 112 | 2 | 13 draft | **Conspiracy voting/draft-matters** |
| OLD-08 | 2014-16 | 16 | 112 | 3 | — | **Willbender / change-target-of-spell** |
| OLD-09 | 2016-17 | 16 | 105 | 2 | — | Conspiracy draft-matters/voting |
| OLD-10 | 2017-18 | 16 | 251 | 1 | **UST 191** | copy-ability (only 59 real non-UST gaps) |
| OLD-11 | 2018-20 | 16 | 170 | 4 | UND 58 | splice, voting, copy-effects |
| OLD-12 | 2020-22 | 16 | 74 | 3 | — | voting (era mechanics all supported) |
| OLD-13 | 2022-23 | 16 | 141 | 2 | **45 planes** | **copy a triggered/activated ability** |
| OLD-14 | 2023 | 5 | 51 | 2 | — | multiplayer voting |

Stale entries (cards listed missing but actually implemented today) total **26** across the old
sets — these are safe to delete from `missing_cards_by_sets`.

## The recurring engine walls (cross-cutting synthesis)

The same short list of missing mechanics explains most *real* (non-OOS) exclusions catalog-wide.
Implementing any one unlocks cards across many sets:

1. **Multiplayer voting / will-of-the-council / council's dilemma** — the single most common
   modern engine gap; recurs in CN2, CNS, CMR, CLB, C13-C21, LTC, CMM, MOC. No supported example anywhere.
2. **Copy a triggered or activated ability** (Strionic Resonator / Rings of Brighthearth /
   Lithoform Engine family) — `borderline.txt` even carries the note `#MISSING: No copy for
   triggered abilities ATM`. Blocks a steady trickle in every Commander-adjacent product.
3. **Splice onto Arcane** — ~34 cards in Kamigawa block (OLD-04) plus reprints.
4. **Change the target of a spell** (Willbender / Imp's Mischief / Spellskite).
5. **Banding / bands-with-other** — the dominant *classic-era* wall (OLD-01/02), ~41 cards.
6. **Copy-for-each-target, gain-control-of-a-spell, ETB-trigger-doubling (Panharmonicon/Yarok),
   "has all activated abilities", "end the turn"** — smaller but recurring stack/replacement gaps.
7. **Physical / social cards** — ante, manual dexterity (Chaos Orb/Falling Star), subgames
   (Shahrazad), Gotcha/say-a-word, person-outside-the-game. **Not "never"** — reframed as a
   low-priority adaptation backlog (cheap analogues: random-target, AI-control, coin-flip, within-game
   ante zone). Only ~10 real-world-trivia/body cards have no analogue. See
   [PHYSICAL_ADAPTATION_PLAN.md](PHYSICAL_ADAPTATION_PLAN.md).
8. **New Universes-Beyond keywords** in unported recent sets — TLA's Waterbend/Earthbend/Airbend/
   Exhaust (59 cards) and TMT's Sneak (26). Set-specific, not catalog-wide.

Notably **not** walls (verified supported, so their absence is only ever a *rider* on a second
clause): transform/DFC, infect/proliferate, phasing, cumulative upkeep, snow/foretell/disturb/
daybound, cascade/devour/clash, cipher/extort/evolve, devotion/bestow/heroic, energy/crew/embalm,
morph/manifest/delve/prowess, the-Ring/amass/Food, companion, initiative/dungeon/venture,
battle-type DFCs (Sieges), sagas, planeswalker loyalty.

## Out-of-scope volume — CORRECTED

An earlier version of this summary called ~480 cards out-of-scope, "dominated by silver-border joke
sets." **That was wrong** (the un-sets were blanket-dismissed). After proper reclassification —
[UNSETS_AUDIT.md](UNSETS_AUDIT.md) — the un-sets are ~205 distinct designs split roughly in thirds:

- **~70 physically impossible** in any digital engine (say-a-word/Gotcha, manual dexterity, subgames,
  "a person outside the game", real-world knowledge/timing) — engine-blocked *by nature*, but now
  listed with a specific reason rather than hand-waved.
- **~65 need a new but digitally-possible subsystem** — the **Contraption/crank/sprockets engine (~55,
  all UST) is the single biggest unlock in the whole audit**; plus Augment//Host (~20), name/letter/
  word/artist analysis (~20), dice-rolling (~14), watermark-matters (~11).
- **~70 are implementable today** — ordinary MTG effects wrongly dismissed for their jokey names
  (Crow Storm, Earl of Squirrel, the modal split cards, lords minus their joke rider). ~22 EASY, ~48 MEDIUM.

So genuinely out-of-scope is only **~2 un-cards** (a literal web-service card + a duplicate) plus the
**~50 Planechase `type=Plane`/`Phenomenon`** cards (a planar-deck subsystem, absent). UND contributes
**zero** new designs (100% reprints of the other three un-sets).

## Actionable findings (bugs & cheap wins surfaced in passing)

- **Stray `_cards.dat` registrations** (registered but not real cards of that set; resolve to a
  foreign primitive, harmless but wrong): TLA ×4 (Badgermole Cub, Wan Shi Tong Librarian, Long Feng,
  The Walls of Ba Sing Se — dup id ranges), TMT ×5 (April O'Neil, Leonardo, Pizza Party, Sewer Pipe
  Omenpath, Splinter's Wisdom — `910xxx`/sibling-product ids), ECL ×1 (Mistbind Clique), SPM ×2
  (J. Jonah Jameson, Electro — registered twice).
- **SOS written-but-not-wired (8 cheap wins)** — primitives already exist but the cards aren't in
  `sets/SOS/_cards.dat`: Essence Scatter, Terramorphic Expanse, Ancestral Anger, and 5 dual lands
  (Deathcap Glade, Dreamroot Cascade, Shattered Sanctum, Stormcarved Coast, Sundown Pass). Just add rows.
- **26 stale `missing_cards_by_sets` entries** across old sets already work — delete to declutter.
- **Loose `ecl_*.txt` WIP files** at repo root are stale (predate ECL's completed implementation) —
  safe to archive/delete.
- **Biggest ROI backlog targets** if resuming card authoring: TLA (237), SOS (209), TMT (179),
  FIN (176), SPM (83) among recent sets; and for the whole catalog, the recurring-wall list above.
