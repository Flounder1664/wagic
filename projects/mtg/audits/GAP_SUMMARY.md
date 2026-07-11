# Gap Summary — by set state, + implementation plan by blocker

Answers two questions: **(1)** where the gap is, per set, across five states; **(2)** how to reach
complete coverage, with the approximate/partial/todo work grouped by the blocker that gates it.
Companion to [SUMMARY.md](SUMMARY.md) (narrative) and [README.md](README.md) (definitions).

## The five states

| State | Meaning | How measured |
|---|---|---|
| **DONE** | primitive present *and* faithfully implements the printed card | presence = which file; **faithfulness only verified for ECL/EOE** |
| **APPROX / PARTIAL** | loads & plays but a clause/mechanic is stripped or edge-cases misbehave | `borderline` grade + measured mechanic-stripping (ECL/EOE) |
| **EXCLUDED** | can't be made faithful without a new engine capability (or never — ante/dexterity) | qualitative per-set/era classification |
| **TODO** | implementable with existing engine, just not written yet | UNWRITTEN (registered, no primitive) + UNREGISTERED (missing-cards) minus engine-blocked |

> ⚠️ **DONE is an upper bound.** Grade = which primitive file a card lives in, not whether the code
> is faithful. Body inspection shows the fork's hand-authored sets ship many "supported" cards as
> approximations (ECL vivid 0/14 faithful; EOE warp 4/50, station 5/28). So real DONE < presence-DONE
> for any set with hand-authored new mechanics. Full detail: README faithfulness caveat.

## Catalog aggregate (all 343 sets — card *slots*, reprints counted per set)

| State | Slots | Notes |
|---|---|---|
| Presence-DONE (supported) | 44,795 | upper bound; faithfulness unverified except ECL/EOE |
| APPROX/PARTIAL (borderline) | 24,090 | "works in most cases" per the wiki grade |
| EXCLUDED (registered→unsupported) | 2,653 | registered but resolves to a non-working stub |
| TODO — unwritten (registered, no primitive) | 4,871 | dangling refs; latent runtime bugs |
| TODO — unregistered (missing-cards files) | 2,547 | real cards absent from `_cards.dat` |
| **TODO total** | **7,418** | the authoring backlog |

Full machine-readable per-set breakdown: [gap_per_set.tsv](gap_per_set.tsv) (343 rows:
year, set, true_est, done_sup, partial_bl, excluded_unsup, todo_unwritten, todo_unregistered).
Caveats: slots double-count reprints across sets; `true_est = registered + missing-file count`, so
the 7 recent flagships (no missing-file) read low there — use the flagship table below for those.

## Flagship sets (recent — precise, Scryfall-derived)

| Set | True | DONE (present) | APPROX/PARTIAL | EXCLUDED (engine) | TODO (backlog) |
|---|---|---|---|---|---|
| FIN | 313 | 137 | unmeasured¹ | 11 (MDFC/meld) | 165 (143 med, 21 easy, 1 OOS) |
| EOE | 266 | 203 *(few faithful)* | **~150+ stripped²** | 2 (Dominion Bracelet) | 61 (50 med, 11 easy) |
| SPM | 193 | 110 | unmeasured¹ | 1 (Web-slinging) | 82 (58 med, 24 easy) |
| TLA | 286 | 49 | 2 borderline | 59 (bending kws) | 178 (118 med, 60 easy) |
| ECL | 278 | **~252 faithful** | **~26 stripped** (vivid 14, behold 10, blight 5·partial²) | 0 | 0 |
| TMT | 195 | 16 | 3 borderline | 26 (Sneak) | 153 (52 med, 101 easy) |
| SOS | 271 | 49 (+8 unwired³) | unmeasured¹ | 52 (copy-split 36, converge 9, paradigm 5, pw 2) | 157 (149 med, 8 easy) |

¹ *unmeasured* = these are mostly UB reprints / standard cards reusing existing primitives (lower
faithfulness risk), but the hand-authored new-mechanic cards among the DONE count were not body-checked.
² measured by body inspection (see ECL_BACKLOG / EOE_TODO).
³ SOS has 8 cards whose primitive already exists but that were never added to `sets/SOS/_cards.dat` — add the rows.

## Old / mid-era sets (1993–2023, 336 sets)

These are near-complete on *registered* cards; the gap is **UNREGISTERED** (missing-cards files). Raw
distinct-missing per era (from the OLD-01…14 docs), split engine-blocked vs backlog vs out-of-scope:

| Era | Distinct missing | Engine-blocked | Backlog (todo) | Out-of-scope |
|---|---|---|---|---|
| 1993-96 (OLD-01) | 245 | ~97 (banding 41, ante, dexterity…) | ~143 | 3 |
| 1997-00 (OLD-02) | 205 | ~10 (banding) | ~136 | 57 (UGL→reclassified, see UNSETS) |
| 2000-03 (OLD-03) | 194 | ~63 | ~118 | 6 planes |
| 2004-07 (OLD-04) | 291 | ~40 (splice 34) | ~34 | 123 (UNH→reclassified) |
| 2007-09 (OLD-05) | 160 | ~34 | ~123 | 0 |
| 2010-12 (OLD-06) | 98 | ~19 | ~75 | 0 |
| 2012-14 (OLD-07) | 112 | ~41 (voting 10) | ~55 | 13 draft |
| 2014-16 (OLD-08) | 112 | ~34 (Willbender) | ~74 | 0 |
| 2016-17 (OLD-09) | 105 | ~40 (Conspiracy) | ~63 | 0 |
| 2017-18 (OLD-10) | 251 | ~24 | ~34 | 191 (UST→reclassified) |
| 2018-20 (OLD-11) | 170 | ~50 | ~50 | 58 (UND→reclassified) |
| 2020-22 (OLD-12) | 74 | ~34 (voting) | ~36 | 0 |
| 2022-23 (OLD-13) | 141 | ~27 (copy-ability) | ~67 | 45 planes |
| 2023 (OLD-14) | 51 | ~24 (voting) | ~25 | 0 |

Un-set "out-of-scope" figures above are **superseded** by [UNSETS_AUDIT.md](UNSETS_AUDIT.md): ~205
distinct un-designs are actually ⅓ physically-impossible / ⅓ new-subsystem / ⅓ implementable-today.

---

# Part 2 — Plan to complete all sets, grouped by blocker

Each row is an implementation blocker. "Unlocks" = approximate count of APPROX/PARTIAL + TODO cards
that become faithfully-DONE once that blocker is built. Ordered by ROI (cards-per-unit-effort).

## Tier A — highest ROI (one engine capability unlocks a large group)

| Blocker | Unlocks (~) | Where | Effort |
|---|---|---|---|
| **Contraptions** (assemble / crank / sprockets) | 55 | UST | new subsystem (C++) |
| **Multiplayer voting** (will-of-council / council's dilemma) | 40–50 | CN2, CNS, CMR, CLB, C13–C21, LTC, CMM, MOC | new trigger + choice UI |
| **Copy a triggered/activated ability** (Strionic/Rings/Lithoform) | 25–30 | catalog-wide; note `#MISSING` in borderline.txt | ability-on-stack copy |
| **Splice onto Arcane** | ~34 | Kamigawa (OLD-03/04) | cast-time text-append |
| **Banding / bands-with-other** | ~41 | classic (OLD-01/02) | combat-assignment rework |
| **Draft-matters / hidden-agenda** | ~28 | CN2, CNS | draft-time layer |

## Tier B — faithfulness fixes for the fork's own hand-authored sets (bodies exist, mechanic stripped)

| Blocker | Unlocks (~) | Where | Effort |
|---|---|---|---|
| **Warp** (alt cast-from-exile cost) | ~46 | EOE | alt-cost hook + exile recast |
| **Station** (charge counters → becomes creature) | ~23 | EOE | charge-counter threshold state |
| **Vivid** (X = colors among permanents) | 14 | ECL | new dynamic count |
| **Behold** (reveal/exile a type as additional cost) | 10 | ECL | additional-cost hook |
| **Void** (bonus if a permanent left this turn) | ~8 | EOE | per-turn LTB tracker |
| **Waterbend / Earthbend / Airbend / Exhaust** | 59 | TLA | 4 new keywords (C++/DSL) |
| **Sneak** (alt cast during declare-blockers) | 26 | TMT | extend Ninjutsu alt-cost class |

## Tier C — recurring stack/replacement gaps (smaller groups, shared code)

Change-target-of-spell (Willbender ~10) · copy-spell-for-each-target (Precursor/Zada) ·
ETB-trigger-doubling (Panharmonicon/Yarok) · gain-control-of-a-spell (Commandeer) ·
"has all activated abilities" (Mairsil/Kraj) · "end the turn" (Time Stop) ·
exchange-control-of-two · two-pile secret partition (Fact or Fiction) ·
copy-split / converge / paradigm-cast-from-exile (SOS 50).

## Tier D — un-set subsystems (digitally possible, isolated)

Augment // Host (~20) · dice-rolling d6/d20 (~14) · watermark-matters (~11) ·
name/letter/word/artist analysis (~20) · fractional ½ power/toughness (~12). See UNSETS_AUDIT.

## Tier E — planar subsystem

Planechase `type=Plane` / `Phenomenon` + planar die (~50 across HOP/PC2/PZ1/PZ2/PCA/MOC/PRM).

## Physical / social cards — LOW-PRIORITY adaptation backlog (not "never")

Reframed per direction: the goal is to get as many of these into Wagic as possible via cheap digital
analogues, case-by-case. Full plan: [PHYSICAL_ADAPTATION_PLAN.md](PHYSICAL_ADAPTATION_PLAN.md).
- Ante (~18), manual dexterity (Chaos Orb/Falling Star + ~13 un), subgames (Shahrazad + un),
  say-a-word/Gotcha (~24 un), balance-on-body (~10), real-world timing (~6), cross-game (~5), person-
  outside-the-game (~7). **~120 cards → P2/P3 low-priority backlog** with a proposed analogue each
  (dexterity→random target; person-outside→AI control; subgame→coin-flip; ante→within-game zone;
  timing→countdown; Gotcha→UI button).
- Two small engine hooks unlock most of it: **random-target resolution** and **AI-controls-a-player**.
- **True NEVER residue: only ~10** — real-world trivia / body / physical contests (no analogue). These
  are the only cards excluded from a realistic "100%" target.

## Suggested sequence

1. **Tier B faithfulness fixes first** — the fork already shipped ECL/EOE as "done"; making them
   faithful is the highest-value correctness work and the bodies already exist to edit.
2. **Tier A Contraptions + voting** — biggest single unlocks catalog-wide.
3. **TODO backlog authoring** for the recent UB sets (TLA 178, TMT 153, SOS 157, FIN 165, SPM 82) —
   pure DSL, no engine work, parallelizable.
4. **Tier C/D/E** subsystems as appetite allows.
5. Treat the never-implementable set as permanently excluded when computing "% complete."
