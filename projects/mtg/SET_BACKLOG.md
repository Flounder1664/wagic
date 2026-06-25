# Wagic Set Backlog

## Current Status
Wagic includes 336 sets. Most recent: **Tarkir: Dragonstorm (TDM/TDC)** — April 11, 2025.

---

## Missing Sets

| Code | Name | Release Date | Base Card Count | Type |
|------|------|--------------|-----------------|------|
| FIN  | Magic: The Gathering — Final Fantasy | 2025-06-13 | ~309 (681 with variants) | Universes Beyond |
| EOE  | Edge of Eternities | 2025-08-01 | ~374 | Standard Expansion |
| SPM  | Marvel's Spider-Man | 2025-09-26 | 300 | Universes Beyond |
| TLA  | Avatar: The Last Airbender | 2025-11-21 | 414 | Universes Beyond |
| ECL  | Lorwyn Eclipsed | 2026-01-23 | ~408 | Standard Expansion |
| TMT  | Teenage Mutant Ninja Turtles | 2026-03-06 | 320 | Universes Beyond |
| SOS  | Secrets of Strixhaven | 2026-04-24 | 271 unique (368 prints) | Standard Expansion — **assessed: see [SOS_BACKLOG.md](SOS_BACKLOG.md)** (67 easy / 148 medium / 56 hard) |

**Total new unique cards (rough): ~2,430**

### Notes
- Universes Beyond sets use IP-owned card names — artwork and flavour text are licensed
- EOE, ECL, SOS are set in the Magic universe so use standard MTG card names and mechanics
- Companion commander sets (FCA, FIC, ECC, ELC, SOC, etc.) not listed — lower priority

---

## Sample Set Analysis: Teenage Mutant Ninja Turtles (TMT)

**195 unique cards** (base set, excluding alternate-art variants)

### Primitive Coverage

| Category | Count | Notes |
|----------|-------|-------|
| Already in Wagic primitives | 8 | Swamp, Forest, Mountain, Island, Plains, Negate, Escape Tunnel, Make Your Move |
| Need new primitive entry | 187 | All TMNT-named cards are new |

### Effort Classification of the 187 New Cards

#### SIMPLE — Primitive exists, just needs `_cards.dat` entry: **8 cards**
The 5 basic lands, Negate, Escape Tunnel, and Make Your Move are all in mtg.txt already.
Only requires adding to a TMT `_cards.dat`. Zero effort per card.

---

#### HARD — Mechanic exists in Wagic, needs a new primitive written: **~105 cards (est.)**

Covers cards using only already-implemented mechanics:

| Mechanic | Wagic Status | Example cards |
|----------|-------------|---------------|
| +1/+1 counters | ✅ Fully implemented | Most creature cards in the set |
| Affinity for Artifacts | ✅ `affinityartifacts` keyword | Metalhead, Buzz Bots, Henchbots |
| Flying, Trample, Haste, Menace, etc. | ✅ All standard keywords | Throughout the set |
| ETB / death triggers | ✅ Standard trigger framework | Most creature abilities |
| Draw, damage, life gain/loss | ✅ Standard effects | Instants and sorceries |
| Food tokens (Pizza-themed) | ✅ Food primitive in ELD | Omni-Cheese Pizza, Everything Pizza cycle |
| Mutagen tokens (tap+sac for +1/+1) | ✅ Within existing token+activated ability framework | Michelangelo, Improviser; The Ooze |
| Class enchantments (Technique cycle) | ✅ Level-counter system in borderline.txt | 11 Technique cards (Leonardo's, Raphael's etc.) |

Effort per card: 30 min – 2 hours to write and test the primitive.

---

#### REALLY HARD — New C++ ability class required: **~75 cards (est.)**

Three new mechanics that have no equivalent in Wagic:

**1. Sneak** (~15–20 cards)
> Cast during the declare blockers step as an alternative cost. Return an unblocked attacker to hand; creature enters tapped and attacking the same target.

- Similar to Ninjutsu (which IS in Wagic) but fundamentally different: it's a *cast* (goes through the stack) rather than an activated ability, and triggers a replacement effect on entry. New C++ class needed in AllAbilities.h + parseMagicLine registration.
- Affects all cards that explicitly use the `sneak` keyword — primarily the ninja-type creatures.

**2. Disappear** (~15–20 cards)
> Ability word: triggers when a permanent leaves the battlefield under your control.

- "Leaves the battlefield" triggers exist in Wagic (`@movedTo`, `@movedFrom`), but Disappear is a *cumulative* within-turn tracker ("how many permanents left this turn"). Cards like Krang & Shredder scale with the count. This requires a new counter/state tracker in the game observer.
- Simpler Disappear cards that just fire once per departure may be achievable with existing triggers.

**3. Alliance** (~10–15 cards)
> "Whenever another creature enters the battlefield under your control."

- ETB triggers exist in Wagic but Alliance specifically requires "another creature" (not self) ETB. Search of SNC primitives and AllAbilities.h found zero Alliance implementation. Needs a new trigger class or extension of the existing ETB trigger filter.
- Once implemented for one card it covers all Alliance cards — shared C++ cost.

**Remaining Really Hard** (~25 cards): Unique per-card effects with no analog in the ability language — complex replacement effects, multi-zone interactions, unusual win conditions.

---

### TMT Implementation Roadmap (rough effort)

| Phase | Scope | Estimated Effort |
|-------|-------|-----------------|
| 1. Set skeleton | Create TMT `_cards.dat`, add 8 existing primitives | 2 hours |
| 2. Hard cards | Write ~105 new primitives, test each | 4–8 weeks (1 person) |
| 3. Alliance C++ | Implement Alliance trigger, ~15 primitive entries | 3–5 days |
| 4. Disappear C++ | Implement Disappear trigger/counter, ~20 primitive entries | 1–2 weeks |
| 5. Sneak C++ | Implement Sneak mechanic, ~20 primitive entries | 2–3 weeks |
| 6. Remaining | Complex per-card abilities | Varies (2–4 weeks) |

**Total rough estimate for TMT: 8–14 weeks (1 developer)**

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
