# Wagic Set Backlog

## Current Status
Wagic includes 336 sets. Most recent: **Tarkir: Dragonstorm (TDM/TDC)** — April 11, 2025.

---

## Missing Sets

| Code | Name | Release Date | Base Card Count | Type |
|------|------|--------------|-----------------|------|
| FIN  | Magic: The Gathering — Final Fantasy | 2025-06-13 | 313 unique | Universes Beyond — **audited**, see [FIN_BACKLOG.md](FIN_BACKLOG.md) (137 really implemented / 176 dangling refs: 11 engine-blocked, 143 medium, 21 easy, 1 out-of-scope) |
| EOE  | Edge of Eternities | 2025-08-01 | 266 unique | Standard Expansion — **203/266 registered-playable but many APPROXIMATE**, see [EOE_TODO.md](../../EOE_TODO.md) (warp 4/50, station 5/28, void 4/14 faithful — bodies strip the new mechanic; 63 excluded: 11 easy / 50 medium / 2 engine-blocked) |
| SPM  | Marvel's Spider-Man | 2025-09-26 | 193 unique | Universes Beyond — **audited**, see [SPM_BACKLOG.md](SPM_BACKLOG.md) (110 really implemented / 83 excluded: 1 engine-blocked, 24 easy, 58 medium — all 83 also dangling `_cards.dat` refs) |
| TLA  | Avatar: The Last Airbender | 2025-11-21 | 286 unique | Universes Beyond — **audited**, see [TLA_BACKLOG.md](TLA_BACKLOG.md) (49 really implemented / 237 UNWRITTEN: 59 engine-blocked [Waterbend 22, Earthbend 19, Airbend 8, Exhaust 2, Saga//creature-transform DFC 8], 118 medium, 60 easy — all 237 also dangling `_cards.dat` refs; 0 unregistered) |
| ECL  | Lorwyn Eclipsed | 2026-01-23 | 278 unique | Standard Expansion — **registered & playable (278/278) but NOT faithfully complete**, see [ECL_BACKLOG.md](ECL_BACKLOG.md) (0 missing/unregistered, BUT ~26 new-mechanic cards ship with the keyword stripped: **vivid 0/14 faithful**, behold 2/12, blight 19/24; 1 stray entry "Mistbind Clique") |
| TMT  | Teenage Mutant Ninja Turtles | 2026-03-06 | 195 unique | Universes Beyond — **audited**, see [TMT_BACKLOG.md](TMT_BACKLOG.md) (16 really implemented / 179 excluded: 26 engine-blocked [Sneak], 101 easy, 52 medium, 0 out-of-scope — all 179 also dangling `_cards.dat` refs; 0 unregistered; only Sneak of the 3 predicted walls survives) |
| SOS  | Secrets of Strixhaven | 2026-04-24 | 271 unique (368 prints) | Standard Expansion — **audited & reconciled 2026-07-11**, see [SOS_BACKLOG.md](SOS_BACKLOG.md) (49 really implemented [registered, 0 dangling] + 5 engine basics / 8 written-but-not-wired [cheap wins] / 209 excluded: 149 medium, 52 hard [copy-split 36, converge 9, paradigm 5, pw 2], 8 easy lands; 0 unsupported) |

**Total new unique cards (rough): ~2,430**

### Notes
- Universes Beyond sets use IP-owned card names — artwork and flavour text are licensed
- EOE, ECL, SOS are set in the Magic universe so use standard MTG card names and mechanics
- Companion commander sets (FCA, FIC, ECC, ELC, SOC, etc.) not listed — lower priority

---

## Teenage Mutant Ninja Turtles (TMT) — audited

The rough "Sample Set Analysis" that previously sat here (estimating 8 simple / ~105 hard /
~75 really-hard, with **Sneak / Disappear / Alliance** as three separate engine walls) has been
superseded by a full audit against `grade_index.json`. See **[TMT_BACKLOG.md](TMT_BACKLOG.md)** for
the per-card classification. Corrected numbers:

- **195 true unique cards** (not 320 — the earlier figure counted alternate-art/showcase prints).
- **16 really implemented** (13 supported + 3 borderline): the 5 basic lands plus 11 names
  reusing primitives authored for other products.
- **179 excluded**, and every one is also an **UNWRITTEN dangling `_cards.dat` reference** —
  the set skeleton is 100% built out (all 195 true cards registered, **0 unregistered**), but the
  primitive text behind 179 of them was never authored.
- Buckets: **26 ENGINE-BLOCKED (Sneak)** · **101 BACKLOG-EASY** · **52 BACKLOG-MEDIUM** ·
  **0 OUT-OF-SCOPE**.
- **Only Sneak of the three predicted walls survives.** Sneak is an alt-cost variant of Ninjutsu
  (whose bespoke `ANinja` C++ class it would extend). **Alliance** is a plain "another creature
  you control enters" ETB trigger already shipped in quantity (Impact Tremors, Cathars' Crusade)
  — not blocked. **Disappear** ("a permanent left the battlefield under your control this turn")
  is built from supported morbid-style parts — MEDIUM, not blocked.
- Bookkeeping: `_cards.dat` has 200 `primitive=` lines = 195 true cards + **5 foreign strays**
  (April O'Neil, Live on the Scene; Leonardo, Tactical Leader; Pizza Party; Sewer Pipe Omenpath;
  Splinter's Wisdom — sibling-product entries with `910xxx` ids) to clean up.

---

## Priority Order Recommendation

For pure MTG-universe sets (ECL, EOE, SOS), most mechanics will be existing MTG mechanics already in Wagic — lower effort than IP-based sets. These are likely to have far more "Hard" cards than "Really Hard" cards.

Suggested order:
1. **ECL** (Lorwyn Eclipsed) — Returns to established Lorwyn plane; likely ~60–70% Hard, lower C++ work
2. **SOS** (Secrets of Strixhaven) — Familiar Strixhaven setting; similar profile
3. **EOE** (Edge of Eternities) — New plane but standard MTG mechanics
4. **TMT / SPM / TLA / FIN** — IP sets; unique mechanics + licensing considerations

---

*Generated: April 2026*
