# Wagic — EOE (Edge of Eternities) TODO

Cards from Edge of Eternities — all new MTG mechanics, standard set (no IP licensing).
Release: August 1, 2025. **Total: 266 unique English cards**.

**Tracked in GitHub:** [Flounder1664/wagic#7](https://github.com/Flounder1664/wagic/issues/7)

## Status
- ✅ `sets/EOE/_cards.dat` created — all 266 cards allocated IDs **1530001–1530398** (= 1530000 + collector_number)
- ✅ 15 cards already playable (have existing primitives): basic lands, shock lands, Annul, Bombard, Banishing Light, Blooming Stinger
- ✅ **Batch 1 (70 cards)** written — commit `5a94d4363` — EASY creatures, instants, sorceries, equipment, artifact creatures
- ✅ New token macros: `_LANDERTOKEN_`, `_ROBOTTOKEN_`, `_DRONETOKEN_` added to `_macros.txt`
- ✅ **Batch 2 (51 cards)** written — creatures, Spacecraft, lands, multi-color, removal (see list below)
- ✅ **Batch 3 (18 cards)** written — commit `ed160f100` — remaining straightforward EASY cards
- ✅ `core.zip` rebuilt to include batch 1 + batch 2 + batch 3 + macros
- ✅ **154 cards** now implemented (15 pre-existing + 70 + 51 + 18)
- ✅ **Batch 4 (36 cards)** written — commit `40fc996bf` — MEDIUM cards (warp stripped, effects simplified)
- ✅ **Batch 5 (13 cards)** written — MEDIUM cards: blink-exile, static haste grant, sacrifice-cost reanimate, combat-damage draw
- ✅ **203 cards** now implemented (15 pre-existing + 70 + 51 + 18 + 36 + 13)
- ✅ `core.zip` rebuilt + deployed to `G:\Wagic-windows\Res\` for PC testing
- ⏳ ~63 cards remain (mostly complex/warp-dependent mechanics)
- ⏳ 1 HARD card: Tezzeret, Cruel Captain (planeswalker — blocked until engine support)

### Batch 5 cards written (13, 2026-05-25)
All-Fates Stalker, Haliya Guided by Light, Mechanozoa, Perigee Beckoner,
Quantum Riddler, Reroute Systems, Scrounge for Eternity, Starfield Shepherd,
Starwinder, Tannuk Steadfast Second, Timeline Culler, Vaultguard Trooper,
Weftstalker Ardent

### Batch 4 cards written (36, 2026-05-25)
Bioengineered Future, Blade of the Swarm, Brightspear Zealot, Bygone Colossus,
Cloudsculpt Technician, Codecracker Hound, Cosmogrand Zenith, Dawnstrike Vanguard,
Drill Too Deep, Drix Fatemaker, Eusocial Engineering, Fell Gravship,
Flight-Deck Coordinator, Frontline War-Rager, Germinating Wurm, Gravblade Heavy,
Interceptor Mechan, Invasive Maneuvers, Knight Luminary, Nova Hellkite,
Rayblade Trooper, Red Tiger Mechan, Rescue Skiff, Ruinous Rampage,
Sami Ship's Engineer, Scour for Scrap, Seedship Broodtender, Sinister Cryologist,
Starport Security, Starbreach Whale, Susurian Voidborn, Syr Vondam Sunstar Exemplar,
Uthros Titanic Godcore, Vote Out, Weftblade Enhancer, Xu-Ifit Osteoharmonist

### Batch 3 cards written (18, 2026-05-25)
Alpharael Stonechosen, Atomic Microsizer, Auxiliary Boosters, Cryogen Relic,
Cryoshatter, Faller's Faithful, Hardlight Containment, Hylderblade,
Illvoi Infiltrator, Kavaron Harrier, Lumen-Class Frigate, Monoist Circuit-Feeder,
Secluded Starforge, Specimen Freighter, Systems Override, Terrapact Intimidator,
Virulent Silencer, Wedgelight Rammer

### Batch 2 cards written (51, 2026-05-25)
Adagia Windswept Bastion, Alpharael Dreaming Acolyte, Beyond the Quiet,
Cerebral Download, Command Bridge, Dawnsire Sunstar Dreadnought,
Debris Field Crusher, Desculpting Blast, Divert Disaster, Dockworker Drone,
Dual-Sun Technique, Dubious Delicacy, Elegy Acolyte, Emergency Eject,
Fungal Colossus, Galvanizing Sawship, Haliya Ascendant Cadet,
Honored Knight-Captain, Illvoi Light Jammer, Kav Landseeker,
Kavaron Memorial World, Larval Scoutlander, Lightless Evangel,
Lithobraking, Lost in Space, Mechan Assembler, Mechan Shieldmate,
Meltstrider's Resolve, Mm'menon Uthros Exile, Mouth of the Storm,
Orbital Plunge, Pinnacle Kill-Ship, Seam Rip, Seedship Impact,
Shattered Wings, Singularity Rupture, Station Monitor, Steelswarm Operator,
Susurian Dirgecraft, Sunset Saboteur, Survey Mechan, Susur Secundi Void Altar,
Syr Vondam the Lucent, Tannuk Memorial Ensign, Temporal Intervention,
The Eternity Elevator, The Seriema, Thaumaton Torpedo, Umbral Collar Zealot,
Uthros Scanship, Wurmwall Sweeper

### Batch 1 cards written (70, 2026-05-25)
All-Fates Scroll, Atmospheric Greenhouse, Beamsaw Prospector, Biosynthic Burst,
Biomechan Engineer, Biotech Specialist, Chrome Companion, Comet Crawler,
Cut Propulsion, Dark Endurance, Dauntless Scrapbot, Decode Transmissions,
Depressurize, Diplomatic Relations, Dual-Sun Adepts, Edge Rover,
Embrace Oblivion, Eumidian Terrabotanist, Exosuit Savior, Frenzied Baloth,
Full Bore, Galactic Wayfarer, Gene Pollinator, Gigastorm Titan,
Glacier Godmaw, Gravkill, Gravpack Monoist, Honor, Hullcarver,
Hymn of the Faller, Icecave Crasher, Icetill Explorer, Illvoi Galeblade,
Illvoi Operative, Insatiable Skittermaw, Intrepid Tenderfoot, Kavaron Skywarden,
Kavaron Turbodrone, Lashwhip Predator, Mechan Navigator, Melded Moxite,
Meltstrider Eulogist, Meltstrider's Gear, Mental Modulation, Molecular Modifier,
Monoist Sentry, Nanoform Sentinel, Nebula Dragon, Nutrient Block,
Oreplate Pangolin, Plasma Bolt, Radiant Strike, Remnant Elemental,
Rig for War, Sami's Curiosity, Seedship Agrarian, Selfcraft Mechan,
Skystinger, Slagdrill Scrapper, Squire's Lightblade, Starfighter Pilot,
Sunstar Expansionist, Sunstar Lightsmith, Swarm Culler, Thawbringer,
Tragic Trajectory, Unravel, Voidforged Titan, Zealous Display, Zookeeper Mechan

Difficulty: Easy = direct Wagic primitives; Medium = approximation needed; Hard = requires engine work.

---

## Card Breakdown by Type

| Type | Count | Est. Easy | Est. Medium | Est. Hard | Notes |
|------|-------|-----------|------------|----------|-------|
| **Creatures** | 139 | ~95 | ~35 | ~9 | Most are straightforward; some have complex ETB/triggers or equipment interactions |
| **Artifacts** | 74 | ~60 | ~14 | ~0 | Includes equipment + artifact creatures (Robots, etc.) |
| **Instants** | 30 | ~20 | ~8 | ~2 | Mostly removal, draw, burn; some choice/conditional effects |
| **Sorceries** | 23 | ~15 | ~6 | ~2 | Tutors, board wipes, ramp |
| **Enchantments** | 16 | ~12 | ~3 | ~1 | Auras, static effects, likely some with choice mechanics |
| **Lands** | 17 | ~15 | ~2 | ~0 | Planet lands + basic lands (vanilla or +1/+1) |
| **Planeswalkers** | 1 | 0 | 0 | 1 | Tezzeret, Cruel Captain — **Hard** (planeswalker engine limitation) |
| **TOTAL** | **266** | ~217 (81%) | ~68 (26%) | ~15 (6%) | *Rough estimates; actual counts depend on detailed card scan* |

**Confidence:** 80–85% of EOE is **Easy** (can be primitived directly from existing patterns).

---

## Classification Framework

### Easy — Straightforward, no approximation needed

✅ Basic stats + keywords (flying, haste, menace, trample, deathtouch, vigilance, lifelink, etc.)
✅ Simple ETB triggers ("when ~ enters, draw a card", "when ~ enters, deal 2 damage")
✅ Death triggers ("when ~ dies, return a creature from your graveyard")
✅ Tap/untap mechanics
✅ Token generation (Goblin, Insect, Robot, Food, etc.)
✅ Draw, discard, mill, damage, life gain/loss
✅ Mana ramp (ramp creatures, signets, land fetch)
✅ Single-target removal (burn, destroy, bounce, exile)
✅ Basic equipment (Equip cost → +X/+X or keyword)

**Estimated count: ~217 cards**

---

### Medium — Existing mechanics but needs careful primitivization

⚠️ Choice mechanics ("choose one —")
⚠️ Multi-branch ETB triggers ("if X, do Y; if Z, do W")
⚠️ Conditions ("only if", "when", "whenever" with restrictions)
⚠️ Land/graveyard plays ("play lands from graveyard" — uses `canplayfromexile` pattern)
⚠️ Equipment interactions (equipped creatures get +X/+X or new ability)
⚠️ Aura enchantments (attach to creature/permanent + grant ability)
⚠️ Sacrifice mechanics with restrictions
⚠️ Combat-phase conditional effects ("at combat begins, if...")

**Estimated count: ~68 cards**

---

### Hard — Requires C++ engine support

❌ **Planeswalkers** (loyalty abilities, planeswalker uniqueness rule, +/–/0 loyalty costs) — **1 card: Tezzeret, Cruel Captain**
❌ DFC / flip mechanics (transform) — **0 cards in EOE sample** (but watch for variants)
❌ Copy spells / copy abilities — unlikely in standard set
❌ Exchange life totals — unlikely
❌ Counter triggered abilities — unlikely in standard set
❌ Completely unique mechanics (need research per card)

**Estimated count: ~15 cards** (mostly edge cases within Medium categories)

---

## Sample Cards by Category

### Easy Creatures (majority pattern)
```
Ragost, Deft Gastronaut — Legendary Creature — Lobster Citizen
(Expected: simple keyword/ETB, likely culinary theme)

Honored Knight-Captain — Creature — Human Advisor Knight
(Expected: keyword + maybe ETB draw or token generation)

Broodguard Elite — Creature — Insect Knight
(Expected: flying/menace + maybe +1/+1 counter trigger)

Thawbringer — Creature — Insect Scout
(Expected: creature with simple ETB or damage effect)

Quantum Riddler — Creature — Sphinx
(Expected: flying + draw/loot on ETB)

Starfield Shepherd — Creature — Angel
(Expected: flying + life gain or token generation)
```

### Easy Artifacts (Equipment + Token Generators)
```
Lumen-Class Frigate — Artifact — Spacecraft
(Expected: artifact token or simple tap ability)

Thaumaton Torpedo — Artifact
(Expected: {T}, sac: deal damage to creature or player)

The Eternity Elevator — Legendary Artifact — Spacecraft
(Expected: mana ramp or creature recursion)

Dubious Delicacy — Artifact — Food
(Expected: {T}, sac: gain 3 life or draw a card)
```

### Easy Instants/Sorceries
```
Annul — Instant
(Expected: counter target spell or destroy target artifact)

Bombard — Instant
(Expected: deal damage, possibly multimodal)

Biosynthic Burst — Instant
(Expected: creature enters tapped or gets +X/+X temporarily)

Radiant Strike — Instant
(Expected: damage to creature/player, possibly with life gain)

Consult the Star Charts — Sorcery
(Expected: draw or tutor effect)
```

---

## Estimated Implementation Effort

### Phase 1: Easy Cards (~217 cards, ~4–6 weeks @ 1 dev)
- Batch primitives by mechanic type (keywords, ETB, death, token gen, removal)
- Test in groups of 10–20 per batch
- Low complexity, high coverage

### Phase 2: Medium Cards (~68 cards, ~3–4 weeks @ 1 dev)
- Audit each card for engine support (choice syntax, conditional triggers, etc.)
- Prioritize high-value cards (Rares, Legendaries, popular mechanics)
- Some may be downgradeable to Easy upon inspection

### Phase 3: Hard Cards (~15 cards, varies)
- Planeswalker (Tezzeret) — **Postponed** (needs planeswalker engine support)
- Others — **Research** to determine if approximation is viable

**Total rough estimate: 7–10 weeks (1 developer, full-time)**

---

## Quick Wins (Immediate)

Cards to implement first (easy, high-value):

1. **Icetill Explorer** (EOE 192) — Creature, {2}{G}{G}, 2/4
   - "You may play an additional land on each of your turns"
   - "You may play lands from your graveyard" (use `canplayfromexile` pattern)
   - "Landfall — Whenever a land you control enters, mill a card" (standard trigger)
   - **Classification: Medium** (all mechanics exist; needs testing)
   - **Value: High** (constructed-playable land ramp)

2. **Robot creatures** (Dauntless Scrapbot, Roving Actuator, etc.)
   - Expected: stats + simple keywords + tap abilities
   - **Classification: Easy**
   - **Value: Medium** (tribal support for Robot deck)

3. **Removal spells** (Depressurize, Gravkill, Unravel, Radiant Strike, etc.)
   - **Classification: Easy** (direct damage, creature removal, bounce)
   - **Value: High** (utility for all decks)

4. **Token generators** (Food tokens, Insect tokens, etc.)
   - **Classification: Easy** (standard `_*TOKEN_` macro)
   - **Value: Medium** (support for sacrifice synergies)

---

## Data Source

**File:** `M:\Claude_projects\wagic\all-cards-20260430092244.json` (Scryfall dump, April 30, 2026)
**Total cards in dump:** 38,733
**EOE English subset:** 266 unique cards
**Deduped by name:** Yes (only latest printing per card)

---

## Next Actions

- [ ] **Full card scan:** Iterate all 266 cards and extract oracle text details
- [ ] **Keyword audit:** List all unique abilities in EOE; cross-ref vs. Wagic primitives
- [ ] **Create detailed card list:** One row per card with Easy/Medium/Hard + blockers
- [ ] **Identify engine blockers:** Any new mechanics without Wagic equivalent?
- [ ] **Batch primitives:** Group cards by mechanic; write primitives in batches
- [ ] **Test in-game:** Validate each batch (20+ card chunks) on Android/Windows

**Owner:** *(TBD — pick up when FIN/TLA/SPM/TMT backlog is clear)*
**Priority:** Medium (after current feature branches merge; before Rooms/Aetherdrift work)
