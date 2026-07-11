# ECL — Lorwyn Eclipsed — Coverage Audit

Audited 2026-07-11 against Scryfall ground truth; **corrected 2026-07-11 after body inspection.**
See [audits/README.md](audits/README.md) for grade tiers, the two gap types (UNWRITTEN vs
UNREGISTERED), and exclusion-reason buckets.

> **CORRECTION.** The first pass reported "278/278, 100% implemented" because every ECL card
> resolves to a primitive that lives in `mtg.txt` (which the audit's file-based heuristic grades
> `supported`). Inspecting the actual primitive **bodies** shows this overstates coverage: ECL was
> hand-authored on this branch, but **many of the new-mechanic cards ship as approximations with the
> new keyword stripped out.** The set is fully *registered and playable*, but not faithfully
> complete. "Resolves to a supported primitive" means *a primitive of that name exists* — it does
> **not** mean the printed rules are implemented. See the mechanic map below for the real numbers.

## Headline numbers

| Metric | Count |
|---|---|
| True cards (Scryfall, `lang:en`, deduped by name) | **278** |
| `_cards.dat` `primitive=` entries | 274 |
| Registered + a primitive of that name exists (loads & plays) | **278 / 278** |
| Registered but **UNWRITTEN** (no primitive) | **0** |
| True cards **UNREGISTERED** (absent from `_cards.dat`) | **0** |
| **New-mechanic cards that STRIP the mechanic (playable but unfaithful)** | **~26** (verified by body inspection) |

So ECL has **no missing/unregistered cards** — its gap is *faithfulness*, not *presence*. Roughly 26
of ~50 new-mechanic cards are approximations. The signature offender is **vivid** (0 of 14 faithful).

### Why 274 entries cover 278 cards

- **7 transform (DFC) cards** each register only their **front face** as a single `primitive=`
  entry; the back face is defined inside that same primitive (Wagic's normal DFC pattern), not as a
  separate top-level entry. So 7 logical cards → 7 entries, but 14 face-names.
- **5 "shocklands"** (Blood Crypt, Steam Vents, Hallowed Fountain, Overgrown Tomb, Temple Garden,
  Watery Grave-style) carry an identical `Name // Name` layout in the bulk dump; they collapse to
  one card and one entry each — no gap.
- Net: 271 single-face entries + 7 transform-front entries − ... balances to 274 entries covering
  all 278 true cards. No true card is left unregistered.

### One entry that isn't a true ECL card — FLAG

- **`Mistbind Clique`** — a classic original-Lorwyn Faerie. It has a `primitive=` line in
  `sets/ECL/_cards.dat` but is **not** in the 278-card deduped ECL true list (not printed in ECL, or
  a card cut/renamed late). It resolves supported (the old Lorwyn primitive exists), so it is
  harmless at runtime, but it is a stray registration. Worth removing or confirming its collector
  number. Everything else in `_cards.dat` maps 1:1 to a real ECL card or DFC front face.

## Exclusion-reason buckets

By the strict README definition (no primitive at all) there is nothing UNWRITTEN or UNREGISTERED.
But body inspection reveals a **faithfulness backlog** — cards that load and play but silently drop
their printed new mechanic. These belong in BACKLOG-MEDIUM (the mechanic must be authored into the
existing primitive), not "done":

| Bucket | Count | Notes |
|---|---|---|
| UNWRITTEN / UNREGISTERED | 0 | every card registered + has a primitive |
| **FAITHFULNESS-BACKLOG (mechanic stripped)** | **~26** | vivid 14, behold 10, blight 5 (see below) |
| Verified-faithful new-mechanic cards | ~24 | blight 19, behold 2 |

Method: for each true ECL card whose oracle uses blight/behold/vivid, its front-face primitive body
in `mtg.txt` was searched for the mechanic's signature (the `blight`/`behold` cost token, a `-1/-1`
counter cost, or a colors-among-permanents `X`). "Stripped" = the body implements a plainer effect
with the keyword removed. Spot-checked by hand (examples below).

## Mechanic map (returning-Lorwyn + new)

Investigated whether the returning-Lorwyn keywords Wagic historically supports still resolve, using
exemplar cards from prior sets in `grade_index`:

| Mechanic | grade_index probe | Result | In ECL? |
|---|---|---|---|
| Convoke | Chord of Calling | borderline | 16 cards |
| Changeling | Woodland Changeling | supported | 18 cards |
| Persist | Kitchen Finks | supported | 2 cards |
| Wither | Boggart Ram-Gang | supported | 2 cards |
| Evoke | Mulldrifter | supported | 5 cards |
| Prowl | Oona's Blackguard | supported | 0 in ECL |
| Hideaway | Windbrisk Heights | borderline | 0 in ECL |
| **Clash** | Ringskipper | **unsupported** | **0 in ECL** |
| Tribal / Kindred | Nameless Inversion | supported | (Kindred types present) |

ECL notably **drops clash** (the one returning-Lorwyn mechanic Wagic grades `unsupported`), so no
ECL card is engine-blocked on it. Prowl and hideaway are also absent from ECL.

### New mechanic — Blight (24 cards) — mostly faithful (19/24)

"Blight N" = put N -1/-1 counters on a creature you control (a self-inflicted cost). Wagic models
-1/-1 counters, so most blight cards implement it. **19 faithful, 5 stripped.** Stripped (the blight
cost is dropped — the effect happens for free or the recursion has no cost):

> Evershrike's Gift *(real: "{1}{W}, Blight 2: return from graveyard" → primitive makes it free)*;
> Pyrrhic Strike; Spiral into Solitude; Wild Unraveling; Dose of Dawnglow

### New mechanic — Behold (12 cards) — mostly STRIPPED (only 2/12 faithful)

"Behold a <type>" = as an additional cost, choose/reveal (and sometimes exile) a permanent of that
type. **Only 2 implement the behold cost; 10 strip it** — the card is authored as if it had no
additional cost, often with a compensating mana bump. Stripped examples:

> Champion of the Clachan *(real: Flash + "behold a Kithkin and exile it" cost → primitive is plain
> Flash anthem, mana bumped {3}{W}, behold cost gone)*; Champions of the Shoal; Silvergill Mentor;
> Champion of the Weird; Mudbutton Cursetosser; + 5 more of the 12.

### New mechanic — Vivid (14 cards) — FULLY STRIPPED (0/14 faithful)

"Vivid —" scales an effect by the number of colors among permanents you control (an X / cost-
reduction / ETB rider). **None of the 14 implement the color-count scaling** — every one hardcodes a
fixed value. Example:

> Kithkeeper *(real: "create X 1/1 Kithkin where X = colors among permanents" → primitive hardcodes
> exactly 3 tokens)*; Rime Chill; Shinestriker; Shimmercreep; Explosive Prodigy; + 9 more.

Vivid is the biggest faithfulness gap in the set. The color-count-of-permanents variable may need a
new DSL count (probe: does any existing card scale off "colors among permanents you control"?).

### Transform DFC (7 cards)

Front faces all resolve `supported`; back-face names are intentionally absent from `grade_index`
(defined inside the front primitive, per Wagic's DFC convention — not a gap):

> Ashling, Rekindled // Ashling, Rimebound; Brigid, Clachan's Heart // Brigid, Doun's Mind; Eirdu,
> Carrier of Dawn // Isilu, Carrier of Twilight; Grub, Storied Matriarch // Grub, Notorious Auntie;
> Oko, Lorwyn Liege // Oko, Shadowmoor Scion; Sygg, Wanderwine Wisdom // Sygg, Wanderbrine Shield;
> Trystan, Callous Cultivator // Trystan, Penitent Culler

## Loose WIP state

The loose `projects/mtg/ecl_*.txt` files are **STALE — superseded by the shipped implementation**.
`ecl_new_primitives.txt` claims "257 cards needing new primitives" and `ecl_missing_cards.txt` lists
99 `name=` blocks as missing; both predate the completed ECL primitive work (all 278 now resolve
supported). `ecl_blight_cards.txt` (24 cards) is a useful *content* reference for the blight
QA-watch group above but its framing as "unsupported" is obsolete. Safe to delete or archive.
