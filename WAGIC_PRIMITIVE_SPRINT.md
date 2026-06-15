# Wagic — Primitive-Writing Sprint Plan

Status: planning — work not started.
Source data: `wagic_gap_SOS_2026.csv` (run `gap_analysis.py` to regenerate).
Last reviewed: 2026-05-26.

**Tracked in GitHub:**
- Vehicles → [Flounder1664/wagic#4](https://github.com/Flounder1664/wagic/issues/4)
- Ward → [Flounder1664/wagic#5](https://github.com/Flounder1664/wagic/issues/5)
- Planeswalkers → [Flounder1664/wagic#6](https://github.com/Flounder1664/wagic/issues/6) (21 DFC PWs blocked on [wagic#2](https://github.com/Flounder1664/wagic/issues/2))

## Why this document exists

The gap analysis found four categories of "missing" cards that don't actually
require any C++ engine work — the engine already supports the mechanics, the
primitives just haven't been written. This is a pure data sprint: write
`[card]...[/card]` blocks following established patterns.

| Category | Cards to write | Engine state |
|---|---|---|
| **Vehicles / Crew** | 112 | `_CREW1_` macro and crew syntax already work |
| **Ward** | ~154 | `_WARD1_`, `_WARD2_` macros exist; 48 ward cards in mtg.txt today |
| **Planeswalkers** (single-face) | 30 | `planeswalkers.txt` has 296 working entries |
| **Battles** (non-DFC) | 1 (*Occupation of Llanowar*) | 36 battles already in borderline.txt |

**Total: ~297 cards** addable without touching C++. Sprint can run in
parallel with engine work in `WAGIC_ENGINE_WORK.md`.

---

## 1. Vehicles / Crew — 112 cards

### Existing pattern

Crew works in Wagic today. Two existing syntaxes (both in `mtg.txt`):

```
auto=_CREW1_                                              ← macro form
auto={crew(other creature[power>=4]|myBattlefield)}:name(creature ...) ← long form
```

Macros to verify / extend in `_macros.txt`: `_CREW1_`, `_CREW2_`, `_CREW3_`, etc.
(Check what exists; define missing ones.)

### Sample primitive (template)

```
[card]
name=Aradara Express
mana={6}
type=Artifact
subtype=Vehicle
power=7
toughness=5
auto={crew(other creature[power>=4]|myBattlefield)}:name(creature) transforms((,,creature,subtype[Vehicle])) ueot
text=Crew 4 (Tap any number of creatures you control with total power 4 or more: This Vehicle becomes an artifact creature until end of turn.)
[/card]
```

For simple crew-N cases, just `auto=_CREW{N}_` should work.

### Workload breakdown by set (top 10)

| Set | Vehicles missing |
|---|---|
| DFT | 15 |
| BOT | 13 |
| UNK | 8 |
| FIN | 7 |
| 40K | 7 |
| TLA | 5 |
| SNC | 4 |
| WHO | 4 |
| LCI | 4 |
| PIP | 3 |

Difficulty mix: 55 Easy, 35 Medium, 22 Hard (the Hard ones are usually DFC
vehicles or vehicles with non-standard abilities — defer those).

### Output file

Add to `projects/mtg/bin/Res/sets/primitives/mtg.txt` if straightforward; use
`borderline.txt` if any approximation is required (e.g., conditional crew costs).

---

## 2. Ward — ~154 cards

### Cost breakdown

| Ward variant | Count | Pattern |
|---|---|---|
| `ward {1}` | 20 | `auto=_WARD1_` |
| `ward {2}` | 73 | `auto=_WARD2_` |
| `ward {3}` | 8 | `auto=_WARD3_` (verify macro exists) |
| `ward {4}` | 1 | `auto=_WARD4_` |
| `ward—pay 2 life` | 4 | New macro `_WARDLIFE2_` (proposal) |
| `ward—pay 3 life` | 5 | New macro `_WARDLIFE3_` |
| `ward—pay 5 life` | 1 | New macro `_WARDLIFE5_` |
| `ward—discard a card` | 5 | New macro `_WARDDISCARD_` |
| `ward—sacrifice a creature` | 1 | New macro `_WARDSACCRE_` |
| `ward—sacrifice 2 permanents` | 1 | _ |
| `ward—sacrifice 3 nonland permanents` | 1 | _ |
| `ward—collect evidence 4` | 1 | needs evidence engine — defer |
| `ward—you get two poison counters` | 1 | new macro `_WARDPOISON2_` |
| `ward—blight 2` | 1 | needs blight engine — defer |

### Existing pattern (verify these macros)

Check `projects/mtg/bin/Res/sets/primitives/_macros.txt` for current `_WARD*_`
definitions. Example existing usage from mtg.txt:

```
[card]
name=Armguard Familiar
auto=_WARD2_
...
[/card]
```

### Sprint plan

**Phase A — Simple mana wards (~102 cards):**
1. Verify `_WARD1_`, `_WARD2_`, `_WARD3_`, `_WARD4_` macros exist; add missing
2. Bulk-write the 102 cards using the appropriate macro
3. ~30 minutes of mechanical work

**Phase B — Life-cost wards (~10 cards):**
1. Define `_WARDLIFE2_`, `_WARDLIFE3_`, `_WARDLIFE5_` macros
2. Write the 10 cards
3. Validate one (cast it in-game, attack with opponent, verify life-pay trigger)

**Phase C — Discard / sacrifice wards (~9 cards):**
1. Define `_WARDDISCARD_`, `_WARDSACCRE_` macros
2. Write cards. The "sac 2 permanents" / "sac 3 nonland" variants might need
   case-specific syntax — fall back to `borderline.txt`

**Phase D — Defer:**
- ward—collect evidence (needs evidence keyword in engine)
- ward—blight 2 (PIO mechanic, niche)
- Mark these in `borderline.txt` with text-only approximation

### Output file

Phase A → `mtg.txt`. Phases B and C → `mtg.txt` if a macro covers them cleanly,
else `borderline.txt`.

---

## 3. Planeswalkers — 30 single-face cards

### Existing pattern

`planeswalkers.txt` has 296 working entries. The format is similar to a normal
card but with loyalty handling. Inspect a few entries before writing — look at
how `loyalty=` and `+1`, `-2`, `-7` ability lines are encoded.

### Cards to write (chronological)

Single-face planeswalkers missing, excluding Arena variants (`A-…` prefix)
and DFC ("X // Y" cards):

```
2014  Garruk the Slayer                    PPC1   (no mana cost — special)
2018  Rowan Kenrith                        PBBD   {4}{R}{R}
2019  Kaya, Ghost Haunter                  CMB1   {2}{W}{B}
2019  Tibalt the Chaotic                   CMB1   {1}{R}{R}
2022  Elspeth Resplendent                  SNC    {3}{W}{W}
2022  Ob Nixilis, the Adversary            PSNC   {1}{B}{R}
2022  Vivien on the Hunt                   SNC    {4}{G}{G}
2022  Tasha, Unholy Archmage               HBG    {2}{U}{B}
2022  Ersta, Friend to All                 PH21   {W}{U}{B}{R}{G}
2022  Ajani, Sleeper Agent                 DMU    {1}{G}{G/W/P}{W}
2022  Jaya, Fiery Negotiator               DMU    {2}{R}{R}
2022  Karn, Living Legacy                  PDMU   {4}
2022  Sivitri, Dragon Master               DMC    {2}{U}{B}
2022  Comet, Stellar Pup                   UNF    {2}{R}{W}
2022  Space Beleren                        UNF    {2}{W}{U}
2023  Heroes of Kamigawa                   PH22   {1}{W}{U}{B}
2023  Svega, the Unconventional            PH22   {1}{G}{W}{U}
2023  Ashiok, Wicked Manipulator           PWOE   {3}{B}{B}
2023  Quintorius Kand                      LCI    {3}{R}{W}
2024  Kaya, Spirits' Justice               PMKM   {2}{W}{B}
2024  Jace Reawakened                      POTJ   {U}{U}
2024  Oko, the Ringleader                  OTJ    {2}{G}{U}
2024  Deb Thomas                           PCEL   {3}{R}     (Celebration promo)
2024  Wrenn and One                        MB2    (no cost — special)
2024  Luxior, Ignited                      MB2    {4}        (equipment-PW)
2025  The Aetherspark                      DFT    {4}        (artifact-PW)
2025  Tezzeret, Cruel Captain              EOE    {3}        (artifact-PW)
2026  Professor Dellian Fel                PSOS   {2}{B}{G}
2026  Quintorius, History Chaser           SOC    {2}{R}{W}
2026  Ral Zarek, Guest Lecturer            SOS    {1}{B}{B}
```

### Recommended order

1. **Start with standard ones** (Elspeth Resplendent, Vivien on the Hunt,
   Jaya Fiery Negotiator) — vanilla loyalty PWs, validate the format works
2. **Then weird ones** — equipment/artifact-PWs (Luxior, The Aetherspark,
   Tezzeret EOE) — these add a planeswalker subtype to non-PW card; verify
   Wagic supports
3. **Then promo / special-format** (Wrenn and One, Garruk the Slayer,
   Comet Stellar Pup) — may need approximation

### Output file

`projects/mtg/bin/Res/sets/primitives/planeswalkers.txt`

---

## 4. Battles — 1 non-DFC card

Only one non-DFC battle missing: **Occupation of Llanowar** (UNK).

Add following the pattern of the 36 existing battle approximations in
`borderline.txt`. Probably 5 minutes of work.

---

## Workflow for the sprint

### Per-card process

1. Open `wagic_gap_SOS_2026.csv`, filter to the category
2. Pick the next card (start with Easy ones)
3. Look at oracle text, P/T, mana cost, keywords
4. Find a similar existing primitive in mtg.txt to copy the pattern
5. Write the `[card]` block
6. Insert alphabetically in mtg.txt (or planeswalkers.txt / borderline.txt)
7. Repeat for the batch

### Batching strategy

Match the existing EOE workflow (see `EOE_TODO.md`):
- 15–50 cards per batch
- One Python merge script per batch (e.g. `merge_vehicles_b1.py`) that follows
  the `merge_eoe_batchN.py` pattern: parses new `[card]` blocks, deduplicates
  against existing names, inserts alphabetically
- One git commit per batch
- Rebuild `core.zip` after each batch
- Optional: deploy to `G:\Wagic-windows\Res\` for spot-check testing

### Acceptance per batch

- Run `python merge_<batch>.py` — see expected card-add count
- `core.zip` rebuilds without primitive parse errors
- Spot-check 2–3 cards in deck editor (PC build at G:)
- Cast 1 card in a Baka AI game; verify abilities fire
- `git commit` with descriptive message

### Acceptance per category complete

- Re-run `python gap_analysis.py` — confirm the category's missing-count
  drops to expected residual (DFC blockers + defer items)
- Update `WAGIC_PRIMITIVE_SPRINT.md` status section

---

## Effort estimate

| Category | Cards | Hours estimate | Notes |
|---|---|---|---|
| Vehicles | 112 | 6–8h | Many are very similar; batch by set |
| Ward | 154 | 4–6h | Mostly trivial macro use |
| Planeswalkers | 30 | 3–5h | More careful; non-trivial format |
| Battles | 1 | 15 min | Trivial |
| **Total** | **~297** | **~14–20h** | One developer, ~2–3 working days |

---

## Status tracking

Update this section as work progresses.

- [ ] Vehicles — 0/112 written
- [ ] Ward — 0/154 written
  - [ ] Phase A (simple mana) — 0/102
  - [ ] Phase B (life cost) — 0/10
  - [ ] Phase C (discard/sac) — 0/9
- [ ] Planeswalkers — 0/30 written
- [ ] Battles — 0/1 written
- [ ] `core.zip` updated and deployed
- [ ] Gap analysis re-run; numbers updated in this file
