# Magic: The Gathering — Final Fantasy (FIN) - Implementation Backlog

Set code `fin` - Universes Beyond expansion, 2025-06-13. Source: Scryfall bulk data, deduplicated to
313 unique English cards (`fin_clean.json`).

Assessment generated 2026-07-06. Cross-checked `projects/mtg/bin/Res/sets/FIN/_cards.dat` (which
registers all 313 cards by `primitive=<name>`/`id=`/`rarity=` block) against the live primitive
source files (`Res/sets/primitives/mtg.txt`, `borderline.txt`, `planeswalkers.txt`, ~26,874 card
names total). Registration in `_cards.dat` only assigns a card an id/rarity — it does **not** mean
the card's rules text was ever authored as a primitive.

## Status

| Bucket | Count | Notes |
|---|---|---|
| Really implemented | 137 | Registered in `_cards.dat` **and** the name exists in the live primitives files. Playable today. |
| DANGLING-REFERENCE (excluded) | 176 | Registered in `_cards.dat` with a real id/rarity, but **no primitive with that name exists anywhere** in mtg.txt/borderline.txt/planeswalkers.txt. This is a live bug class — 56% of the set is a name+id shell with no rules text behind it. |
| — of which ENGINE-BLOCKED | 11 | No equivalent mechanic/combo in Wagic yet; needs new C++/engine work first. |
| — of which BACKLOG-MEDIUM | 143 | Existing mechanics, but needs careful multi-clause/conditional DSL authoring. |
| — of which BACKLOG-EASY | 21 | Existing mechanics only; trivial to write. |
| — of which OUT-OF-SCOPE | 1 | Digital-only Alchemy rebalance of an already-implemented card. |

**313 total = 137 really implemented + 176 dangling/excluded.** 176 = 11 + 143 + 21 + 1.

All 176 dangling names were also checked against `unsupported.txt` (~1,710 known-catalogued-but-not-
implemented names elsewhere in Wagic): **zero matches**. These aren't previously-triaged "known
gaps" — they're specific to FIN never having been fully authored.

---

## DANGLING-REFERENCE detail

Every one of the 176 excluded cards is, definitionally, a dangling reference: `_cards.dat` gives it
a real Wagic card id and rarity (so it will show up in deck-builder search, in draft boosters, in
card-database listings), but casting or resolving it will fall back to a blank/no-op primitive since
no `[card] name=<X> ...` block exists for it anywhere in the primitives files. This is worse than a
card simply being "missing" — it's a silent data-integrity gap that looks implemented from the
_cards.dat side. The 176 are sub-classified below by what it would take to fix each one.

---

## ENGINE-BLOCKED (11)

Mechanics/combinations with no existing analog anywhere in Wagic. Each needs new engine or C++ work
before any card using it can be authored; the cost is roughly one-time per mechanic, not per card.

**Land face // Adventure-spell face MDFC (5)**
_[Adventure engine only pairs with creature faces today (`abilities=adventure` is always attached to
a creature primitive); there is no existing Land+Adventure transform/MDFC combination]_

- Ishgard, the Holy See // Faith & Grief _(Land — Town // Sorcery — Adventure)_
- Jidoor, Aristocratic Capital // Overture _(Land — Town // Sorcery — Adventure)_
- Lindblum, Industrial Regency // Mage Siege _(Land — Town // Instant — Adventure)_
- Midgar, City of Mako // Reactor Raid _(Land — Town // Sorcery — Adventure)_
- Zanarkand, Ancient Metropolis // Lasting Fayth _(Land — Town // Sorcery — Adventure)_

**Land face // Vehicle-transform face MDFC (1)**

- Balamb Garden, SeeD Academy // Balamb Garden, Airborne _(Land — Town // Legendary Artifact — Vehicle)_

**Meld into a third distinct named card (3)**
_[Wagic's `meld()` primitive exists (used by Gisela/Bruna → Brisela) but always needs the merged
result authored as its own primitive; this triad needs all three: two meld-halves plus "Ragnarok,
Divine Deliverance" as the merged card]_

- Fang, Fearless l'Cie _(Legendary Creature — Human Warrior)_
- Vanille, Cheerful l'Cie _(Legendary Creature — Human Cleric)_
- Ragnarok, Divine Deliverance _(Legendary Creature — Beast Avatar)_

**Damage/harm redirection replacement effect (1)**
_["All damage that would be dealt to you and other permanents you control is dealt to this creature
instead" — no such blanket redirection replacement effect exists in Wagic]_

- Ancient Adamantoise _(Creature — Turtle)_

**Take-control-then-benefit loop (1)**
_[Gain-control-of-a-permanent effects exist, but conditioning a card-draw reward on what the new
controller does with the gained permanent is a novel combo]_

- Stiltzkin, Moogle Merchant _(Legendary Creature — Moogle)_

---

## OUT-OF-SCOPE (1)

- A-Vivi Ornitier _(Legendary Creature — Wizard)_ — `digital: true` Alchemy rebalance of "Vivi
  Ornitier," which is already really-implemented in FIN (id 1141463/1140919). Not a distinct paper
  card; no separate primitive needed. (Note: even the paper Vivi Ornitier's self-referential mana
  ability — "Add X mana... where X is Vivi Ornitier's power" — is only partially implemented today;
  the existing primitive's text is marked "(simplified)" and the mana ability itself has no `auto=`
  line. That's a pre-existing gap on the *implemented* card, out of scope for this audit.)

---

## BACKLOG-EASY (21)

Uses only mechanics Wagic already fully supports elsewhere; trivial `_cards.dat`-adjacent primitive
writes.

- Cactuar _(Creature — Plant)_ — trample + "return to hand at end step if it didn't enter this turn"
- Elixir _(Artifact)_ — enters tapped; tap-sac to shuffle graveyard back and gain life
- Blitzball _(Artifact)_ — tap for any color; sac to draw 2 if a legendary dealt combat damage this turn
- Lunatic Pandora _(Legendary Artifact)_ — tap: surveil 1; tap-sac: destroy nonland permanent
- Excalibur II _(Legendary Artifact — Equipment)_ — lifegain-trigger charge counter, +1/+1 per counter
- The Masamune _(Legendary Artifact — Equipment)_ — static keyword grant + "triggers an additional time"
- Capital City _(Land — Town)_ — tap for C, pay 1 for any color, cycling
- Baron, Airship Kingdom _(Land — Town)_
- Gohn, Town of Ruin _(Land — Town)_
- Gongaga, Reactor Town _(Land — Town)_
- Guadosalam, Farplane Gateway _(Land — Town)_
- Insomnia, Crown City _(Land — Town)_
- Rabanastre, Royal City _(Land — Town)_
- Sharlayan, Nation of Scholars _(Land — Town)_
- Treno, Dark City _(Land — Town)_
- Vector, Imperial Capital _(Land — Town)_
- Windurst, Federation Center _(Land — Town)_ — (10 identical "enters tapped, tap for 2 colors" Town duals)
- Adventurer's Inn _(Land — Town)_ — enters, gain 2 life, tap for C
- Crossroads Village _(Land — Town)_ — enters tapped, choose a color, tap for that color
- Chocobo Kick _(Sorcery)_ — kicker + fight-like damage-equal-to-power
- Vayne's Treachery _(Instant)_ — kicker + -X/-X modal

---

## BACKLOG-MEDIUM (143)

Grouped into mechanic-coherent batches, following the same authoring order suggested by SOS_BACKLOG.md.
Order is a suggestion: build the shared pattern once per batch, then apply across the batch.

### Job select / Hero-token Equipment (12)
_[Pattern already used by FIN's own really-implemented cards, e.g. Dragoon's Lance, Paladin's Arms —
just needs the per-card equip cost/buff/subtype text]_

- Machinist's Arsenal _(Artifact — Equipment)_
- White Mage's Staff _(Artifact — Equipment)_
- Astrologian's Planisphere _(Artifact — Equipment)_
- Sage's Nouliths _(Artifact — Equipment)_
- Thief's Knife _(Artifact — Equipment)_
- Black Mage's Rod _(Artifact — Equipment)_
- Ninja's Blades _(Artifact — Equipment)_
- Red Mage's Rapier _(Artifact — Equipment)_
- Warrior's Sword _(Artifact — Equipment)_
- Monk's Fist _(Artifact — Equipment)_
- Summoner's Grimoire _(Artifact — Book Equipment)_
- Dark Knight's Greatsword _(Artifact — Equipment)_

### Standard Equipment (3)

- Aettir and Priwen _(Legendary Artifact — Equipment)_
- Magitek Scythe _(Artifact — Equipment)_
- Ultima Weapon _(Legendary Artifact — Equipment)_

### Restricted-color mana ability (1)
_["Spend this mana only to..." — existing pattern (see Cargo Ship, Freya Crescent's own artifact-only
mana restriction cousin cards elsewhere in FIN)]_

- Freya Crescent _(Legendary Creature — Rat Knight)_

### Vehicle / Crew (7)

- Magitek Armor _(Artifact — Vehicle)_
- Cargo Ship _(Artifact — Vehicle)_
- The Lunar Whale _(Legendary Artifact — Vehicle)_
- The Prima Vista _(Legendary Artifact — Vehicle)_
- Phantom Train _(Artifact — Vehicle)_
- Adventurer's Airship _(Artifact — Vehicle)_
- The Regalia _(Legendary Artifact — Vehicle)_

### Saga (14)
_[Existing chapter/lore-counter engine (`subtype=Saga`, 98 existing implementations across mtg.txt/
borderline.txt) — needs per-chapter effect authoring only]_

- Summon: Choco/Mog _(Enchantment Creature — Saga Bird Moogle)_
- Summon: Knights of Round _(Enchantment Creature — Saga Knight)_
- Summon: Primal Garuda _(Enchantment Creature — Saga Harpy)_
- Summon: Anima _(Enchantment Creature — Saga Horror)_
- Summon: Primal Odin _(Enchantment Creature — Saga Knight)_
- Summon: Brynhildr _(Enchantment Creature — Saga Knight)_
- Summon: Esper Ramuh _(Enchantment Creature — Saga Wizard)_
- Summon: G.F. Cerberus _(Enchantment Creature — Saga Dog)_
- Summon: G.F. Ifrit _(Enchantment Creature — Saga Demon)_
- Summon: Fat Chocobo _(Enchantment Creature — Saga Bird)_
- Summon: Fenrir _(Enchantment Creature — Saga Wolf)_
- Summon: Titan _(Enchantment Creature — Saga Giant)_
- Summon: Leviathan _(Enchantment Creature — Saga Leviathan)_
- Summon: Shiva _(Enchantment Creature — Saga Elemental)_

### Creature // Saga-enchantment transform (7)
_[Both "transform" and "Saga" are independently supported; the "Dominant becomes a Warden Saga"
cycle just combines the two]_

- Dion, Bahamut's Dominant // Bahamut, Warden of Light
- Jill, Shiva's Dominant // Shiva, Warden of Ice
- Clive, Ifrit's Dominant // Ifrit, Warden of Inferno
- Jecht, Reluctant Guardian // Braska's Final Aeon
- Joshua, Phoenix's Dominant // Phoenix, Warden of Fire
- Terra, Magical Adept // Esper Terra
- Esper Origins // Summon: Esper Maduin

### Creature // Creature transform (13)

- Venat, Heart of Hydaelyn // Hydaelyn, the Mothercrystal
- Cecil, Dark Knight // Cecil, Redeemed Paladin
- Vincent Valentine // Galian Beast
- Sephiroth, Fabled SOLDIER // Sephiroth, One-Winged Angel
- Zenos yae Galvus // Shinryu, Transcendent Rival
- Emet-Selch, Unsundered // Hades, Sorcerer of Eld
- The Emperor of Palamecia // The Lord Master of Hell
- Exdeath, Void Warlock // Neo Exdeath, Dimension's End
- Garland, Knight of Cornelia // Chaos, the Endless
- Kefka, Court Mage // Kefka, Ruler of Ruin
- Kuja, Genome Sorcerer // Trance Kuja, Fate Defied
- Serah Farron // Crystallized Serah
- Ultimecia, Time Sorceress // Ultimecia, Omnipotent

### Sidequest cycle: Equipment/Enchantment // Saga/Vehicle transform (6)

- Crystal Fragments // Summon: Alexander
- Sidequest: Catch a Fish // Cooking Campsite
- Sidequest: Card Collection // Magicked Card
- Sidequest: Hunt the Mark // Yiazmat, Ultimate Mark
- Sidequest: Play Blitzball // World Champion, Celestial Weapon
- Sidequest: Raise a Chocobo // Black Chocobo

### Tiered / choose-additional-cost modal (6)
_[The "Tiered" pattern is already implemented for other FIN cards elsewhere in the set]_

- Restoration Magic _(Instant)_
- Ice Magic _(Instant)_
- Fire Magic _(Instant)_
- Thunder Magic _(Instant)_
- Vincent's Limit Break _(Instant)_
- Tifa's Limit Break _(Instant)_

### Flashback (9)
_[Native `flashback=` field; per-card body + graveyard-cast rider clause]_

- From Father to Son _(Sorcery)_
- Memories Returning _(Sorcery)_
- Retrieve the Esper _(Sorcery)_
- The Final Days _(Sorcery)_
- Resentful Revelation _(Sorcery)_
- Call the Mountain Chocobo _(Sorcery)_
- Nibelheim Aflame _(Sorcery)_
- Random Encounter _(Sorcery)_
- Sorceress's Schemes _(Sorcery)_

### Copy effect (4)
_[Spell/token copy has native engine support — `copy target(...)` and `castcard(copied)` are used
throughout mtg.txt/borderline.txt already]_

- Ether _(Artifact)_
- Gogo, Master of Mimicry _(Legendary Creature — Wizard)_
- Relm's Sketching _(Sorcery)_
- The Fire Crystal _(Legendary Artifact)_

### "Cast a noncreature spell, N+ mana spent" trigger (3)
_[Pattern used elsewhere in FIN's already-implemented cards, e.g. Blazing Bomb, Prompto Argentum]_

- Ultros, Obnoxious Octopus _(Legendary Creature — Octopus)_
- Queen Brahne _(Legendary Creature — Human Noble)_
- Mysidian Elder _(Creature — Human Wizard)_

### Devotion / mana-symbol-in-cost counting (2)

- Cloud of Darkness _(Legendary Creature — Avatar)_
- Xande, Dark Mage _(Legendary Creature — Human Wizard)_

### Graveyard-size scaling / mill-based conditional (3)

- The Darkness Crystal _(Legendary Artifact)_
- Diamond Weapon _(Legendary Artifact Creature — Elemental)_
- Shambling Cie'th _(Creature — Mutant Horror)_

### Combat-damage-to-player rider effect (4)

- Kain, Traitorous Dragoon _(Legendary Creature — Human Knight)_
- Reno and Rude _(Legendary Creature — Human Assassin)_
- Vaan, Street Thief _(Legendary Creature — Human Scout)_
- Lightning, Security Sergeant _(Legendary Creature — Human Soldier)_

### Multi-clause choose-one modal (7)

- Aerith Rescue Mission _(Sorcery)_
- Poison the Waters _(Sorcery)_
- Qutrub Forayer _(Creature — Zombie Horror)_
- Gaius van Baelsar _(Legendary Creature — Human Soldier)_
- Opera Love Song _(Instant)_
- Clash of the Eikons _(Sorcery)_
- Rydia's Return _(Sorcery)_

### Misc multi-clause permanents/spells (42)
_[No shared batch pattern — per-card DSL, but every mechanic involved already exists somewhere in
Wagic]_

- Cloud, Midgar Mercenary _(Legendary Creature — Human Soldier Mercenary)_
- White Auracite _(Artifact)_
- The Wind Crystal _(Legendary Artifact)_
- Louisoix's Sacrifice _(Instant)_
- Matoya, Archon Elder _(Legendary Creature — Human Warlock)_
- Stolen Uniform _(Instant)_
- Stuck in Summoner's Sanctum _(Enchantment — Aura)_
- Swallowed by Leviathan _(Instant)_
- Travel the Overworld _(Sorcery)_
- Valkyrie Aerial Unit _(Artifact Creature — Construct)_
- The Water Crystal _(Legendary Artifact)_
- Y'shtola Rhul _(Legendary Creature — Cat Druid)_
- Ultima _(Sorcery)_
- Zodiark, Umbral God _(Legendary Creature — God)_
- Self-Destruct _(Instant)_
- Triple Triad _(Enchantment)_
- Raubahn, Bull of Ala Mhigo _(Legendary Creature — Human Warrior)_
- Tonberry _(Creature — Salamander Horror)_
- Quina, Qu Gourmet _(Legendary Creature — Qu)_
- A Realm Reborn _(Enchantment)_
- Ride the Shoopuf _(Enchantment)_
- Torgal, A Fine Hound _(Legendary Creature — Wolf)_
- Traveling Chocobo _(Creature — Bird)_
- Balthier and Fran _(Legendary Creature — Human Rabbit)_
- Choco, Seeker of Paradise _(Legendary Creature — Bird)_
- Rydia, Summoner of Mist _(Legendary Creature — Human Shaman)_
- Sin, Spira's Punishment _(Legendary Creature — Leviathan Avatar)_
- Tellah, Great Sage _(Legendary Creature — Human Wizard)_
- The Wandering Minstrel _(Legendary Creature — Human Bard)_
- Chocobo Racetrack _(Artifact)_
- Ultimecia, Temporal Threat _(Legendary Creature — Human Warlock)_
- Cloud, Planet's Champion _(Legendary Creature — Human Soldier Mercenary)_
- PuPu UFO _(Artifact Creature — Construct Alien)_
- Ring of the Lucii _(Legendary Artifact)_
- Relentless X-ATM092 _(Artifact Creature — Robot Spider)_
- Ultima, Origin of Oblivion _(Legendary Creature — God)_
- Prishe's Wanderings _(Instant)_
- Ice Flan _(Creature — Elemental Ooze)_
- Seymour Flux _(Legendary Creature — Spirit Avatar)_
- The Gold Saucer _(Land — Town)_
- Clive's Hideaway _(Land — Town)_
- Eden, Seat of the Sanctum _(Land — Town)_

---

*Generated: 2026-07-06. Ground truth: Scryfall bulk data (313 unique FIN cards). Primitive coverage
checked against `Res/sets/primitives/mtg.txt` + `borderline.txt` + `planeswalkers.txt` (~26,874 names).*
