# Wagic — Engine Work Plan (DFC, Sagas, Classes)

Status: planning — work not started.
Source data: `wagic_gap_SOS_2026.csv` (run `gap_analysis.py` to regenerate).
Last reviewed: 2026-05-26.

**Tracked in GitHub:**
- Sagas → [Flounder1664/wagic#1](https://github.com/Flounder1664/wagic/issues/1)
- DFC → [Flounder1664/wagic#2](https://github.com/Flounder1664/wagic/issues/2)
- Classes → [Flounder1664/wagic#3](https://github.com/Flounder1664/wagic/issues/3) (blocked by #1)

## Why this document exists

A gap analysis against the Scryfall dataset (cards released up to SOS, 2026-04-24)
identified three engine subsystems with significant unlock value that Wagic does
not currently implement at all. These are real C++ engine work, not primitive-writing.

| Subsystem | Cards unlocked | Wagic primitives today |
|---|---|---|
| **DFC family** (transform / MDFC / reversible / flip / meld) | **576 missing** | None of these card layouts work |
| **Sagas** | **145 missing** | 0 sagas in mtg.txt, borderline.txt, or unsupported.txt |
| **Classes** | **16 missing** | 0 classes in any primitives file |

DFC additionally unblocks:
- ~21 missing DFC planeswalkers ("Invasion of X // Teferi") — otherwise the PW
  engine works fine, see `WAGIC_PRIMITIVE_SPRINT.md`.
- ~37 missing DFC battles ("Invasion of X // Y") — non-DFC battles already have
  36 borderline approximations.
- 44 DFC sagas ("X // Y") — depend on both Saga and DFC subsystems.

So DFC is **the single biggest engine investment**: ~576 direct cards plus
unblocks DFCs in three other mechanics + every future set since DFC is now
table-stakes (DSK, DFT, FIN, EOE all use it).

---

## 1. Sagas — 145 cards, fully green-field

### What needs building

Sagas are an enchantment subtype with:
- ETB places a **lore counter** on the saga
- At **the beginning of your precombat main phase**, place another lore counter
- Each chapter triggers when the saga **gains** that many lore counters
- **Sacrifice** the saga after the final chapter's ability resolves

Example: *The Elder Dragon War* (DMU, single-face) has three chapters:
```
I — Deal 2 damage to each creature without flying.
II — Discard your hand, then draw three cards.
III — Create three 4/4 red Dragon creature tokens with flying.
```

### Subsystem design notes

- New card type **Saga** (subtype of Enchantment) — Wagic already has Enchantment
  card handling; this is adding a subtype with structured triggers.
- A **lore counter** is just an integer state on the card. Wagic already supports
  +1/+1 counters, charge counters, etc. — saga counters fit the same pattern.
- The chapter triggers are essentially "when counter reaches N" — that pattern
  may already exist for cards like *Renowned* or *Devotion*.
- The auto-sacrifice trigger: "When the last chapter resolves" is a
  state-based-action variant.

### Suggested primitive syntax (proposal)

```
[card]
name=The Elder Dragon War
mana={2}{R}
type=Enchantment
subtype=Saga
auto=@chapter(1):damage:2 all(creature[-flying]|battlefield)
auto=@chapter(2):discard hand controller && draw:3 controller
auto=@chapter(3):_DRAGONTOKEN_ && _DRAGONTOKEN_ && _DRAGONTOKEN_
text=(Saga — III chapters; sacrifice after final chapter resolves.)
[/card]
```

Needs new auto-trigger primitive `@chapter(N)` that hooks the lore-counter
system. Final-chapter sacrifice should be automatic from `subtype=Saga` +
chapter count.

### Target test cards (start small, easy chapter effects)

1. *Founding the Third Path* (DMU) — simple draw / scry
2. *The Elder Dragon War* (DMU) — damage + draw + tokens
3. *The Cruelty of Gix* (DMU) — modal-ish reanimation
4. *Phyrexian Scriptures* (DOM) — was the very first Saga set's first card
5. *History of Benalia* (DOM) — token-then-pump (validates chapter timing)

### Files likely to touch

- `projects/mtg/include/AllAbilities.h` — new `MTGChapterTrigger` class
- `projects/mtg/include/AbilityParser.h` — parse `@chapter(N):...`
- `projects/mtg/src/MTGAbility.cpp` — chapter event dispatch
- `projects/mtg/include/MTGCardInstance.h` — `loreCounters` field, or piggyback
  on existing counter map
- `projects/mtg/src/MTGCardInstance.cpp` — auto-sacrifice on chapter exhaustion
- `projects/mtg/include/Rules.h` — main-phase tick to add lore counter
- `projects/mtg/bin/Res/sets/primitives/mtg.txt` — actual saga primitives

### Out of scope (defer)

- DFC sagas (44 cards, e.g. *Crystal Fragments // Summon: Alexander*) — blocked
  on DFC infrastructure
- Read-ahead sagas (you choose chapter count on cast — newer mechanic)

---

## 2. DFC / Transform Family — 576 cards

### What needs building

A card with two faces, where one face is active at a time. Variants:
- **Transform** (Innistrad-style) — has a condition that flips the face
- **Modal DFC** (MDFC, ZNR-style) — cast either face from hand; the face you
  picked is the only one that exists
- **Reversible** — symmetrical printed-on-both-sides cards (mostly token cards)
- **Flip** (Kamigawa-style) — same physical card; flips when condition met
  (functionally identical to transform from engine perspective)
- **Meld** — two cards combine into one larger card (Brisela, etc.) — rare,
  defer

### Subsystem design notes

- Each card needs **two `[card]` definitions in primitives**, linked by a
  shared identifier
- New `[card]` field `dfc=other-face-name` (proposal) or shared block syntax
- The active face determines: name, type, P/T, abilities, mana cost
- Transform trigger fires on a state event ("When ~, transform it")
- MDFC casting needs to pick a face at cast time; once cast, the face is fixed
  for that instance
- Combat / targeting / abilities all reference the **currently active** face
- Reanimation / move-to-zone: front face is always the "canonical" name; the
  back face only exists when transformed

### Suggested primitive syntax (proposal)

```
[card]
name=Delver of Secrets
mana={U}
type=Creature
subtype=Human Wizard
power=1
toughness=1
dfc=Insectile Aberration
auto=@each my upkeep:may transform({revealed top:1 is(instant,sorcery)})
[/card]

[card]
name=Insectile Aberration
type=Creature
subtype=Human Insect
power=3
toughness=2
abilities=flying
dfc=Delver of Secrets
dfc_back=true
[/card]
```

### Existing infrastructure to investigate first

- Wagic already has `transforms((...))` syntax used by *Systems Override*
  (EOE Batch 3) to temporarily turn an opponent's permanent into something
  else for one turn. That's an in-game state-change mechanism — likely some
  of the plumbing is reusable but it's a temporary modifier, not a real
  two-faced card.
- Search `AbilityParser.cpp` for `transform` to find existing handling.

### Target test cards (start small)

1. *Delver of Secrets // Insectile Aberration* (ISD) — the iconic simple transform
2. *Akoum Warrior // Akoum Teeth* (ZNR) — simplest MDFC (creature or land)
3. *Sea Gate Restoration // Sea Gate, Reborn* (ZNR) — MDFC with cost reduction
4. *Garruk Relentless // Garruk, the Veil-Cursed* (ISD) — DFC planeswalker
5. *Bruna, the Fading Light // Brisela, Voice of Nightmares* (EMN) — meld (defer)

### Files likely to touch

- `projects/mtg/include/MTGCardInstance.h` — `currentFace`, `backFace` fields,
  transform() method
- `projects/mtg/include/MTGCard.h` — card-data side: link to other face
- `projects/mtg/include/AbilityParser.h` — `dfc=` parsing, `transform(...)` auto
- `projects/mtg/src/CardGui.cpp` — render correct face
- `projects/mtg/src/MTGGameZones.cpp` — when a DFC leaves the battlefield,
  reset to front face
- `projects/mtg/src/Player.cpp` (or wherever casting is) — MDFC face-selection
  at cast time
- `projects/mtg/bin/Res/sets/primitives/mtg.txt` — two primitives per card

### Risk

- Highest C++ surface area of the three subsystems
- Touches casting, zones, rendering, abilities, AI
- Strong recommendation: get *Delver of Secrets* alone working end-to-end first
  before scaling

---

## 3. Classes — 16 cards, share Saga infra

### What needs building

Class enchantments (AFR onwards) work like a levelled enchantment:
- ETB at Level 1
- Activate a level-up cost (mana, sorcery-speed) to advance to Level 2, then 3
- At each level, gain a new ability — abilities are **cumulative**
- Each higher level has a higher activation cost

Example: *Pirate Class* (AFR):
```
Level 1: Whenever you attack with a Pirate, gain treasure
{2}: Level 2 — Pirates you control get +1/+1
{6}: Level 3 — Whenever a Pirate enters, draw a card
```

### Subsystem design notes

- Functionally a Saga that you advance manually instead of automatically
- Shares "tiered ability stack" with Sagas; differs in advancement trigger
- Level abilities are static (not triggered each level-up) so simpler than
  Saga chapter triggers in some ways
- Activation must be **sorcery-speed only** — Wagic already has
  `restriction{sorcery}` etc.

### Suggested primitive syntax (proposal)

```
[card]
name=Pirate Class
mana={1}{B}
type=Enchantment
subtype=Class
auto=@level(1):@attacking(pirate|mybattlefield):_TREASURETOKEN_
auto={2}{Sorcery}:level(2)
auto=@level(2):all(pirate|mybattlefield) +1/+1
auto={6}{Sorcery}:level(3)
auto=@level(3):@movedTo(pirate|mybattlefield):draw:1
[/card]
```

### Target test cards

- *Druid Class* (AFR) — green ramp/draw
- *Pirate Class* (AFR) — treasure + buff
- *Builder's Talent* (BLB) — the "Talent" Class variants

### Verdict

Build **after Sagas land**. ~70% of the engine is shared (tiered abilities,
level state). The 16 cards barely justify a dedicated subsystem but they
fall in line cheaply once Sagas exist.

---

## Sequencing recommendation

1. **Sagas first** (smallest, most self-contained, cleanest spec)
   — proves the "tiered ability" pattern with mostly static state
2. **DFC second** (biggest, highest risk, but unlocks the most)
   — start with *Delver of Secrets*, prove the loop, then scale
3. **Classes third** (smallest, piggyback on saga infra)
   — should be a 1-week task after Sagas

Each subsystem can ship independently. Sagas + Classes together unlock
~161 cards; DFC alone unlocks 576 + ~100 more from DFC PWs/battles/sagas.

---

## Verification (per subsystem)

- Primitive parses without errors (load mtg.txt, check log)
- Target test card appears in deck editor
- Cast / play target card in a Baka AI game
- All listed abilities fire correctly (saga chapter advances; DFC transforms;
  class levels up)
- Re-run `gap_analysis.py` — count of relevant `effort_reason` rows drops
- No regression on existing card behaviour (run TestSuiteAI)

---

## Open questions to resolve before starting

1. **Sagas:** does Wagic already have an "N counters reached" trigger? Check
   `AllAbilities.h` for counter-threshold patterns
2. **DFC:** does the existing `transforms((...))` syntax in EOE primitives
   (e.g. *Systems Override*) cover any of the rendering / two-state machinery
   we'd need to reuse?
3. **Classes:** is there a "level up" precedent in existing primitives, even
   for old Lorwyn-era *Level Up* creatures (which were never implemented)?
