# Avatar: The Last Airbender (TLA) - Implementation Backlog

Set code `tla` - Universes Beyond expansion, 2025-11-21. Source: Scryfall bulk data, deduplicated to
**286 unique English cards** (`tla_clean.json`).

Assessment generated 2026-07-11. Cross-checked `projects/mtg/bin/Res/sets/TLA/_cards.dat` against the
live primitive grade index (`grade_index.json`, 28,570 primitive names across `mtg.txt` /
`borderline.txt` / `planeswalkers.txt` / `unsupported.txt`). Registration in `_cards.dat` only assigns a
card an id/rarity - it does **not** mean the card's rules text was ever authored as a primitive.

This is a Universes Beyond set: the Avatar IP supplies the card names and flavour, but every card is
classified here on its **underlying MTG rules text**, not its flavour.

## Status

| Bucket | Count | Notes |
|---|---|---|
| Really implemented | 49 | Registered in `_cards.dat` **and** the name resolves to a `supported`/`borderline` grade. Playable today. (47 supported + 2 borderline.) |
| UNWRITTEN (excluded) | 237 | Registered in `_cards.dat` with a real id/rarity, but **no primitive with that name exists** in any primitive file. A name+id shell with no rules text behind it - 83% of the set. |
| - of which ENGINE-BLOCKED | 59 | Uses a TLA-specific keyword (bending / Exhaust) or a DFC transform layout with no Wagic analog; needs new engine/C++ work first. |
| - of which BACKLOG-MEDIUM | 118 | Existing mechanics, but needs careful multi-clause / conditional DSL authoring. |
| - of which BACKLOG-EASY | 60 | Existing mechanics only; trivial to write. |
| - of which OUT-OF-SCOPE | 0 | No digital-only rebalances or pure variants in the deduped list. |
| UNREGISTERED | 0 | Every one of the 286 true cards is present in `_cards.dat`. The set is fully registered; it is the *primitives* that are missing. |

**286 total = 49 really implemented + 237 UNWRITTEN.** 237 = 59 + 118 + 60 + 0.

`_cards.dat` holds **290 `primitive=` entries**, but the first four (ids 950201-950204: Badgermole Cub,
Wan Shi Tong Librarian, Long Feng Grand Secretariat, The Walls of Ba Sing Se) are **exact duplicates**
of entries re-registered under the 15100xx id range, so there are exactly 286 unique names - matching the
286 true cards one-for-one. No `_cards.dat` name fails to match a real TLA card.

All 237 UNWRITTEN names were also checked against `unsupported.txt`: **zero matches**. These aren't
previously-triaged known gaps - they are specific to TLA never having been authored.

---

## ENGINE-BLOCKED (59)

TLA introduces four keyword mechanics plus a transform DFC layout that have no existing analog in Wagic.
Cost is roughly one-time per mechanic, not per card. Several cards carry more than one of these; each is
listed once, under its most-blocking mechanic.

### Waterbend {N} (22)
_[A convoke-like alternative/additional cost: "while paying a waterbend cost, you may tap your artifacts
and creatures to help; each pays for {1}." No existing keyword taps arbitrary permanents to fund a
generic activated-ability or additional spell cost.]_

- Spirit Water Revival _(Sorcery)_
- Ruinous Waterbending _(Sorcery - Lesson)_
- Watery Grasp _(Enchantment - Aura)_
- Foggy Swamp Vinebender _(Creature - Human Plant Ally)_
- Secret of Bloodbending _(Sorcery - Lesson)_
- Waterbending Lesson _(Sorcery - Lesson)_
- Benevolent River Spirit _(Creature - Spirit)_
- Hama, the Bloodbender _(Legendary Creature - Human Warlock)_
- Flexible Waterbender _(Creature - Human Warrior Ally)_
- Waterbender Ascension _(Enchantment)_
- Crashing Wave _(Sorcery)_
- Invasion Submersible _(Artifact - Vehicle)_
- Katara, Bending Prodigy _(Legendary Creature - Human Warrior Ally)_
- The Unagi of Kyoshi Island _(Legendary Creature - Serpent)_
- Katara, Water Tribe's Hope _(Legendary Creature - Human Warrior Ally)_
- Water Tribe Rallier _(Creature - Human Soldier Ally)_
- Foggy Swamp Visions _(Sorcery)_
- Geyser Leaper _(Creature - Human Warrior Ally)_
- Yue, the Moon Spirit _(Legendary Creature - Spirit Ally)_
- North Pole Patrol _(Creature - Human Soldier Ally)_
- Giant Koi _(Creature - Fish)_
- Aang's Iceberg _(Enchantment)_

### Earthbend N (19)
_[Turns a target land you control into a 0/0 haste creature that is still a land, puts N +1/+1 counters
on it, and returns it tapped when it dies or is exiled. A combined land-animation + counter +
death-replacement package with no single analog.]_

- Earth Kingdom General _(Creature - Human Soldier Ally)_
- Bumi, Unleashed _(Legendary Creature - Human Noble Ally)_
- Toph, the First Metalbender _(Legendary Creature - Human Warrior Ally)_
- Toph, Hardheaded Teacher _(Legendary Creature - Human Warrior Ally)_
- Beifong's Bounty Hunters _(Creature - Human Mercenary)_
- Bumi, King of Three Trials _(Legendary Creature - Human Noble Ally)_
- Toph, the Blind Bandit _(Legendary Creature - Human Warrior Ally)_
- The Boulder, Ready to Rumble _(Legendary Creature - Human Warrior Performer)_
- Dai Li Agents _(Creature - Human Soldier)_
- Ba Sing Se _(Land)_
- Fatal Fissure _(Instant)_
- Sandbenders' Storm _(Instant)_
- Rebellious Captives _(Creature - Human Peasant Ally)_
- Earth Rumble _(Sorcery)_
- Haru, Hidden Talent _(Legendary Creature - Human Peasant Ally)_
- Earth Village Ruffians _(Creature - Human Soldier Rogue)_
- The Cave of Two Lovers _(Enchantment - Saga)_
- Bitter Work _(Enchantment)_
- Dai Li Indoctrination _(Sorcery - Lesson)_

### Airbend (8)
_[Exile a permanent; while exiled its owner may recast it for {2} rather than its mana cost. A
foretell/adventure-style exile-and-recast that can target any nonland permanent, including ones you do
not own.]_

- Airbender Ascension _(Enchantment)_
- Airbending Lesson _(Instant - Lesson)_
- Avatar's Wrath _(Sorcery)_
- Glider Staff _(Artifact - Equipment)_
- Aang, the Last Airbender _(Legendary Creature - Human Avatar Ally)_
- Appa, Loyal Sky Bison _(Legendary Creature - Bison Ally)_
- Appa, Steadfast Guardian _(Legendary Creature - Bison Ally)_
- Airbender's Reversal _(Instant - Lesson)_

### Exhaust (2)
_["Exhaust - <cost>: ... (Activate each exhaust ability only once.)" - a once-per-game activated-ability
tracker with no existing state in the engine.]_

- Mai, Jaded Edge _(Legendary Creature - Human Noble)_
- Hog-Monkey _(Creature - Boar Monkey)_

### Saga // creature transform DFC (8)
_[Double-faced "The Legend of X // Avatar X" Sagas that transform on their final chapter, plus the three
Aang creature-transform DFCs. Wagic supports Sagas and transform individually, but not the DFC-transform
*layout* these ship as. These faces also carry bending/Exhaust costs, so they are doubly blocked.]_

- The Legend of Yangchen // Avatar Yangchen _(Enchantment - Saga // Legendary Creature - Avatar)_
- The Rise of Sozin // Fire Lord Sozin _(Enchantment - Saga // Legendary Creature - Human Noble)_
- The Legend of Kuruk // Avatar Kuruk _(Enchantment - Saga // Legendary Creature - Avatar)_
- Avatar Aang // Aang, Master of Elements _(Legendary Creature - Human Avatar Ally // Legendary Creature - Avatar Ally)_
- The Legend of Roku // Avatar Roku _(Enchantment - Saga // Legendary Creature - Avatar)_
- The Legend of Kyoshi // Avatar Kyoshi _(Enchantment - Saga // Legendary Creature - Avatar)_
- Aang, at the Crossroads // Aang, Destined Savior _(Legendary Creature - Human Avatar Ally // Legendary Creature - Avatar Ally)_
- Aang, Swift Savior // Aang and La, Ocean's Fury _(Legendary Creature - Human Avatar Ally // Legendary Creature - Avatar Spirit Ally)_

---

## BACKLOG-MEDIUM (118)

Existing mechanics, but each needs careful multi-clause or conditional DSL. Grouped into mechanic-coherent
batches; build the shared pattern once per batch, then apply across it.

### X / for-each dynamic scaling (13)
- Avatar Destiny _(Enchantment - Aura)_
- Crescent Island Temple _(Legendary Enchantment - Shrine)_
- Diligent Zookeeper _(Creature - Human Citizen Ally)_
- Gather the White Lotus _(Sorcery)_
- Kyoshi Island Plaza _(Legendary Enchantment - Shrine)_
- Master Pakku _(Legendary Creature - Human Advisor Ally)_
- Northern Air Temple _(Legendary Enchantment - Shrine)_
- Obsessive Pursuit _(Enchantment)_
- Seismic Sense _(Sorcery - Lesson)_
- Southern Air Temple _(Legendary Enchantment - Shrine)_
- Team Avatar _(Enchantment)_
- The Spirit Oasis _(Legendary Enchantment - Shrine)_
- White Lotus Tile _(Artifact)_

### Draw-count / second-card / trigger-count trackers (12)
- Foggy Swamp Hunters _(Creature - Human Ranger Ally)_
- Foggy Swamp Spirit Keeper _(Creature - Human Druid Ally)_
- June, Bounty Hunter _(Legendary Creature - Human Mercenary)_
- Katara, the Fearless _(Legendary Creature - Human Warrior Ally)_
- Knowledge Seeker _(Creature - Fox Spirit)_
- Messenger Hawk _(Creature - Bird Scout)_
- Otter-Penguin _(Creature - Otter Bird)_
- Raven Eagle _(Creature - Bird Assassin)_
- South Pole Voyager _(Creature - Human Scout Ally)_
- Suki, Courageous Rescuer _(Legendary Creature - Human Warrior Ally)_
- Tiger-Seal _(Creature - Cat Seal)_
- Tolls of War _(Enchantment)_

### Lesson-in-graveyard conditional (7)
- Accumulate Wisdom _(Instant - Lesson)_
- Combustion Technique _(Instant - Lesson)_
- Dragonfly Swarm _(Creature - Dragon Insect)_
- First-Time Flyer _(Creature - Human Pilot Ally)_
- Platypus-Bear _(Creature - Platypus Bear)_
- The Lion-Turtle _(Legendary Creature - Elder Cat Turtle)_
- Walltop Sentries _(Creature - Human Soldier Ally)_

### Prowess / cast-trigger payoffs (6)
- Iguana Parrot _(Creature - Lizard Bird Pirate)_
- Sokka, Bold Boomeranger _(Legendary Creature - Human Warrior Ally)_
- Sokka, Tenacious Tactician _(Legendary Creature - Human Warrior Ally)_
- The Mechanist, Aerial Artisan _(Legendary Creature - Human Artificer Ally)_
- Ty Lee, Artful Acrobat _(Legendary Creature - Human Performer)_
- Ty Lee, Chi Blocker _(Legendary Creature - Human Performer Ally)_

### Modal choose-one/one-or-both (6)
- Azula Always Lies _(Instant - Lesson)_
- Bumi Bash _(Sorcery)_
- Iroh's Demonstration _(Sorcery - Lesson)_
- Momo, Playful Pet _(Legendary Creature - Lemur Bat Ally)_
- Origin of Metalbending _(Instant - Lesson)_
- Zuko, Conflicted _(Legendary Creature - Human Rogue)_

### Copy / cast-without-paying / cast-from-zone (5)
- Ember Island Production _(Sorcery)_
- Hakoda, Selfless Commander _(Legendary Creature - Human Warrior Ally)_
- Joo Dee, One of Many _(Creature - Human Advisor)_
- Planetarium of Wan Shi Tong _(Legendary Artifact)_
- Serpent of the Pass _(Creature - Serpent)_

### Firebending token generation (5)
- Cruel Administrator _(Creature - Human Soldier)_
- Fire Nation Palace _(Land)_
- Uncle Iroh _(Legendary Creature - Human Noble Ally)_
- Vindictive Warden _(Creature - Human Soldier)_
- Zhao, Ruthless Admiral _(Legendary Creature - Human Soldier)_

### Vehicle / Crew (5)
- Fire Nation Warship _(Artifact - Vehicle)_
- Phoenix Fleet Airship _(Artifact - Vehicle)_
- The Fire Nation Drill _(Legendary Artifact - Vehicle)_
- Tundra Tank _(Artifact - Vehicle)_
- War Balloon _(Artifact - Vehicle)_

### Conditional cost reduction (5)
- Allies at Last _(Instant)_
- Gran-Gran _(Legendary Creature - Human Peasant Ally)_
- Momo, Friendly Flier _(Legendary Creature - Lemur Bat Ally)_
- Swampsnare Trap _(Enchantment - Aura)_
- Waterbending Scroll _(Artifact)_

### Custom / special counters (fire, conqueror, stun, finality, quest) (5)
- Fated Firepower _(Enchantment)_
- Rowdy Snowballers _(Creature - Human Peasant Ally)_
- Vengeful Villagers _(Creature - Human Citizen)_
- Wolfbat _(Creature - Wolf Bat)_
- Zhao, the Moon Slayer _(Legendary Creature - Human Soldier)_

### Typecycling (4)
- Canyon Crawler _(Creature - Spider Beast)_
- Mongoose Lizard _(Creature - Mongoose Lizard)_
- Rabaroo Troop _(Creature - Rabbit Kangaroo)_
- Saber-Tooth Moose-Lion _(Creature - Elk Cat)_

### Kicker (3)
- Aang's Journey _(Sorcery - Lesson)_
- Jet's Brainwashing _(Sorcery)_
- Zuko's Conviction _(Instant)_

### Flashback (2)
- Fire Nation Attacks _(Instant)_
- Solstice Revelations _(Instant - Lesson)_

### Saga (single-face) (2)
- Guru Pathik _(Legendary Creature - Human Monk Ally)_
- Leaves from the Vine _(Enchantment - Saga)_

### Fight / redirect / excess-damage (3)
- Razor Rings _(Instant)_
- Redirect Lightning _(Instant - Lesson)_
- The Last Agni Kai _(Instant)_

### Grant-all-abilities / characteristic-setting (3)
- Day of Black Sun _(Sorcery)_
- Honest Work _(Enchantment - Aura)_
- Koh, the Face Stealer _(Legendary Creature - Shapeshifter Spirit)_

### Graveyard recursion / reanimation (1)
- Sandbender Scavengers _(Creature - Human Rogue)_

### Gain-control effects (1)
- Iroh, Tea Master _(Legendary Creature - Human Citizen Ally)_

### Other multi-clause (per-card DSL) (30)
- Air Nomad Legacy _(Enchantment)_
- Beetle-Headed Merchants _(Creature - Human Citizen)_
- Buzzard-Wasp Colony _(Creature - Bird Insect)_
- Callous Inspector _(Creature - Human Soldier)_
- Combustion Man _(Legendary Creature - Human Assassin)_
- Cunning Maneuver _(Instant)_
- Destined Confrontation _(Sorcery)_
- Earth Kingdom Jailer _(Creature - Human Soldier Ally)_
- Elemental Teachings _(Instant - Lesson)_
- Fire Nation Engineer _(Creature - Human Artificer)_
- Fire Nation Raider _(Creature - Human Soldier)_
- Fire Navy Trebuchet _(Artifact Creature - Wall)_
- Hei Bai, Spirit of Balance _(Legendary Creature - Bear Spirit)_
- Invasion Tactics _(Enchantment)_
- Jasmine Dragon Tea Shop _(Land)_
- Jet, Freedom Fighter _(Legendary Creature - Human Rebel Ally)_
- Kyoshi Battle Fan _(Artifact - Equipment)_
- Lo and Li, Twin Tutors _(Legendary Creature - Human Advisor)_
- Master Piandao _(Legendary Creature - Human Warrior Ally)_
- Ostrich-Horse _(Creature - Bird Horse)_
- Path to Redemption _(Enchantment - Aura)_
- Pirate Peddlers _(Creature - Human Pirate)_
- Professor Zei, Anthropologist _(Legendary Creature - Human Advisor Ally)_
- Sold Out _(Instant)_
- Sparring Dummy _(Artifact Creature - Scarecrow)_
- Teo, Spirited Glider _(Legendary Creature - Human Pilot Ally)_
- The Earth King _(Legendary Creature - Human Noble Ally)_
- True Ancestry _(Sorcery - Lesson)_
- Unlucky Cabbage Merchant _(Creature - Human Citizen)_
- White Lotus Hideout _(Land)_

---

## BACKLOG-EASY (60)

Uses only mechanics Wagic already fully supports; trivial primitive writes.

### Vanilla / near-vanilla keywords + one simple ETB or static (27)
- Boomerang Basics _(Sorcery - Lesson)_
- Cat-Gator _(Creature - Fish Crocodile)_
- Cat-Owl _(Creature - Cat Bird)_
- Compassionate Healer _(Creature - Human Cleric Ally)_
- Curious Farm Animals _(Creature - Boar Elk Bird Ox)_
- Cycle of Renewal _(Instant - Lesson)_
- Deadly Precision _(Sorcery)_
- Deserter's Disciple _(Creature - Human Rebel Ally)_
- Earth Kingdom Protectors _(Creature - Human Soldier Ally)_
- Earth Rumble Wrestlers _(Creature - Human Warrior Performer)_
- Energybending _(Instant - Lesson)_
- Enter the Avatar State _(Instant - Lesson)_
- Glider Kids _(Creature - Human Pilot Ally)_
- Great Divide Guide _(Creature - Human Scout Ally)_
- Hermitic Herbalist _(Creature - Human Druid Ally)_
- How to Start a Riot _(Instant - Lesson)_
- Mai, Scornful Striker _(Legendary Creature - Human Noble Ally)_
- Price of Freedom _(Sorcery - Lesson)_
- Raucous Audience _(Creature - Human Citizen)_
- Rocky Rebuke _(Instant)_
- Shared Roots _(Sorcery - Lesson)_
- Sokka's Haiku _(Instant - Lesson)_
- Sokka, Lateral Strategist _(Legendary Creature - Human Warrior Ally)_
- Tiger-Dillo _(Creature - Cat Armadillo)_
- Wandering Musicians _(Creature - Human Bard Ally)_
- Yip Yip! _(Instant - Lesson)_
- Yuyan Archers _(Creature - Human Archer)_

### Sac-for-draw dual lands (enters tapped, tap for two colors, {4} + sac: draw) (10)
- Airship Engine Room _(Land)_
- Boiling Rock Prison _(Land)_
- Foggy Bottom Swamp _(Land)_
- Kyoshi Village _(Land)_
- Meditation Pools _(Land)_
- Misty Palms Oasis _(Land)_
- North Pole Gates _(Land)_
- Omashu City _(Land)_
- Serpent's Pass _(Land)_
- Sun-Blessed Peak _(Land)_

### Simple +1/+1 counter effects (7)
- Earth King's Lieutenant _(Creature - Human Soldier Ally)_
- Earth Kingdom Soldier _(Creature - Human Soldier)_
- Flopsie, Bumi's Buddy _(Legendary Creature - Ape Goat)_
- Octopus Form _(Instant - Lesson)_
- United Front _(Sorcery)_
- Wartime Protestors _(Creature - Human Rebel Ally)_
- White Lotus Reinforcements _(Creature - Human Soldier Ally)_

### Mono-color utility lands (enters tapped unless you control a basic) (3)
- Abandoned Air Temple _(Land)_
- Agna Qel'a _(Land)_
- Realm of Koh _(Land)_

### ETB single Ally token (3)
- Invasion Reinforcements _(Creature - Human Warrior Ally)_
- Suki, Kyoshi Warrior _(Legendary Creature - Human Warrior Ally)_
- Treetop Freedom Fighters _(Creature - Human Rebel Ally)_

### Simple Clue generators (3)
- Forecasting Fortune Teller _(Creature - Human Advisor Ally)_
- Lost Days _(Instant - Lesson)_
- Zuko's Exile _(Instant - Lesson)_

### Equipment (fixed buff + equip cost) (3)
- Meteor Sword _(Artifact - Equipment)_
- Trusty Boomerang _(Artifact - Equipment)_
- Twin Blades _(Artifact - Equipment)_

### Mana artifacts (2)
- Barrels of Blasting Jelly _(Artifact)_
- Bender's Waterskin _(Artifact)_

### Utility lands (2)
- Rumble Arena _(Land)_
- Secret Tunnel _(Land - Cave)_

---

*Generated: 2026-07-11. Ground truth: Scryfall bulk data (286 unique TLA cards). Primitive coverage
checked against the four `Res/sets/primitives/*.txt` grade files via `grade_index.json` (28,570 names).*