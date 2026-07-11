# Wagic — EOE (Edge of Eternities) TODO

Cards from Edge of Eternities — all new MTG mechanics, standard set (no IP licensing).
Release: August 1, 2025. **Total: 266 unique English cards.**

**Tracked in GitHub:** [Flounder1664/wagic#7](https://github.com/Flounder1664/wagic/issues/7)

> **⚠️ FAITHFULNESS CAVEAT (added 2026-07-11).** The "203 implemented" figure counts cards that
> *load and play*, not cards that faithfully implement their printed rules. Body inspection shows
> many EOE cards ship as **approximations with the new mechanic stripped**: of cards that have a
> primitive, only **warp 4/50, station 5/28, void 4/14** are faithful (e.g. Rescue Skiff ships as a
> vanilla 5/6 with Station gone; the batch notes below already say "warp stripped, effects
> simplified"). So the real "faithfully complete" count is well under 203. Same pattern as ECL — see
> [audits/README.md](projects/mtg/audits/README.md) faithfulness caveat.

## Status (re-audited 2026-07-06)

- ✅ `sets/EOE/_cards.dat` has a `primitive=` entry for **all 266/266 cards** — IDs 1530001–1530398 (= 1530000 + collector_number)
- ✅ **203/266 cards (76%) are really implemented** — verified by cross-checking every `_cards.dat` primitive name against Wagic's full implemented-primitive corpus (mtg.txt + borderline.txt + planeswalkers.txt, ~26,874 names), not just presence in `_cards.dat`
- ⏳ **63/266 cards (24%) are excluded** — a `_cards.dat` row exists (registering the name+ID) but the primitive text itself was never written
- ✅ **0 dangling references** — every `_cards.dat` entry maps to a real EOE card; every excluded card has a `_cards.dat` row waiting for its primitive. No stale/orphaned entries found.
- ✅ **0 out-of-scope cards** — all 266 are real, distinct, Scryfall-listed playable cards (no test/marketing/joke cards in this set)

This audit corrects the prior "203 implemented, ~63 remain" note (from 2026-05-25) from an estimate into a verified, per-card number — it turns out the estimate was already exactly right, but the bucket breakdown below is new.

### Bucket breakdown of the 63 excluded cards

| Bucket | Count | Meaning |
|---|---|---|
| **BACKLOG-EASY** | 11 | Uses only mechanics Wagic already fully supports elsewhere; straightforward to primitive |
| **BACKLOG-MEDIUM** | 50 | Supported mechanics, but needs careful multi-clause/conditional DSL work (incl. several needing a new but precedented pattern: Station/Vehicle-style, Void-tracker, replacement-effect doubling) |
| **DANGLING-REFERENCE** | 0 | None found |
| **ENGINE-BLOCKED** | 2 | Tezzeret, Cruel Captain (planeswalker card not authored); The Dominion Bracelet (Mindslaver-style full-turn control-take-over — confirmed absent from the engine, and explicitly catalogued as unsupported) |
| **OUT-OF-SCOPE** | 0 | None found |

**Correcting the old planeswalker assumption:** the previous note flagged Tezzeret, Cruel Captain as blocked "until engine support" for planeswalkers. That's no longer accurate as a blanket statement — Wagic's planeswalker corpus (`planeswalkers.txt`) has **296 working planeswalkers**, including 8 other Tezzeret versions (Tezzeret the Schemer, Tezzeret the Seeker, Tezzeret, Agent of Bolas, Tezzeret, Artifice Master, Tezzeret, Betrayer of Flesh, Tezzeret, Cruel Machinist, Tezzeret, Master of Metal, Tezzeret, Master of the Bridge). The loyalty-ability engine mechanism itself works fine. "Tezzeret, Cruel Captain" specifically has just never been authored as a card — same situation as any other unwritten card, not a fundamental engine gap. It's kept in ENGINE-BLOCKED here only because authoring a new loyalty-ability card is a materially bigger lift than a normal primitive (needs a planeswalker template, not a same-day batch card).

### New mechanic notes surfaced by this audit

- **Station / Spacecraft charge counters** — genuinely unimplemented as a generic keyword (zero hits anywhere in engine source). 8 of the 63 excluded cards are Station Spacecraft/Planets (Synthesizer Labship, Entropic Battlecruiser, Sledge-Class Seedship, Warmaker Gunship, Infinite Guideline Station, Extinguisher Battleship, Evendo Waking Haven, and Tapestry Warden's stationing clause). Wagic's Vehicle/Crew mechanic (Smuggler's Copter, Heart of Kiran, Skysovereign) is a close structural analog — tap-a-creature to power up a noncreature into a creature — so these are BACKLOG-MEDIUM (adapt the Crew pattern) rather than engine-blocked, but it's real per-card design work, not a batch pattern yet.
- **Void (ability word)** — the "if a nonland permanent left the battlefield this turn or a spell was warped this turn" turn-tracker has no engine equivalent (confirmed: no such state tracking exists). Affects Chorale of the Void and Roving Actuator among the excluded cards, and is also referenced as flavor text on some already-implemented Void cards (those got the non-Void baseline effect only). BACKLOG-MEDIUM once/if a shared tracker is built — same shape as the SOS set's "leave-graveyard trigger" gated mechanic.
- **Devour, Kicker, token-copy effects, Mind Control-style control-change, Affinity** — all confirmed genuinely supported already via existing implemented cards (Skinthinner/Deranged Hermit for Devour, Sea Gate Restoration for Kicker, Rite of Replication/Progenitor Mimic for token-copy, Mind Control/Control Magic for control-change, existing Affinity cards). Cards using these mechanics were classified BACKLOG-EASY/MEDIUM, not engine-blocked.
- **"Second spell each turn" trigger** — already used by several implemented EOE cards (Cosmogrand Zenith, Illvoi Operative, Sunstar Lightsmith). Uthros Psionicist's cost-reduction variant of the same trigger is BACKLOG-MEDIUM, not a new mechanic.

### Full list of the 63 excluded cards by bucket

**BACKLOG-EASY (11)**
- Focus Fire — X damage to attacking/blocking creature, X = 2 + creatures/Spacecraft you control
- Harmonious Grovestrider — P/T = lands you control, plus Ward
- Hemosymbic Mite — whenever tapped, another target creature gets +X/+X (X = this creature's power)
- Luxknight Breacher — ETB with counters equal to other creatures/artifacts you control
- Memorial Team Leader — static anthem during your turn + warp
- Mightform Harmonizer — Landfall doubles target creature's power until EOT + warp
- Pinnacle Emissary — cast-artifact-spell trigger makes a flying-restricted Drone token + warp
- Pull Through the Weft — two-mode graveyard recursion (permanents to hand / lands to battlefield)
- Sami, Wildcat Captain — double strike, vigilance, affinity for artifacts on your spells
- Space-Time Anomaly — mill equal to caster's life total
- Terrasymbiosis — whenever counters placed on a creature you control, draw that many (once/turn)

**BACKLOG-MEDIUM (50)**
- Anticausal Vestige, Archenemy's Charm, Astelli Reclaimer, Broodguard Elite, Chorale of the Void,
  Close Encounter, Consult the Star Charts, Cosmogoyf, Devastating Onslaught, Dyadrine Synthesis Amalgam,
  Emissary Escort, Entropic Battlecruiser, Evendo Waking Haven, Exalted Sunborn, Extinguisher Battleship,
  Famished Worldsire, Genemorph Imago, Infinite Guideline Station, Lightstall Inquisitor, Loading Zone,
  Memorial Vault, Mm'menon the Right Hand, Moonlit Meditation, Mutinous Massacre, Ouroboroid,
  Pain for All, Pinnacle Starcage, Possibility Technician, Pulsar Squadron Ace, Ragost Deft Gastronaut,
  Requiem Monolith, Roving Actuator, Rust Harvester, Scout for Survivors, Sledge-Class Seedship,
  Sothera the Supervoid, Starfield Vocalist, Sunstar Chaplain, Synthesizer Labship, Tapestry Warden,
  Terminal Velocity, Territorial Bruntar, The Endstone, Thrumming Hivepool, Tractor Beam,
  Uthros Psionicist, Warmaker Gunship, Weapons Manufacturing, Weftwalking, Zero Point Ballad

**ENGINE-BLOCKED (2)**
- Tezzeret, Cruel Captain — planeswalker card not authored (engine supports planeswalkers generally)
- The Dominion Bracelet — Mindslaver-style "control target opponent during their next turn"; confirmed unimplemented and explicitly catalogued unsupported

**DANGLING-REFERENCE (0)** · **OUT-OF-SCOPE (0)**

---

## Batches written so far (203 cards, chronological)

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

## Next Actions

- [ ] **Batch 6 (BACKLOG-EASY, 11 cards):** write the 11 straightforward remaining cards listed above
- [ ] **Batch 7+ (BACKLOG-MEDIUM, 50 cards):** group by shared mechanic pattern before writing:
  - Station/Spacecraft group (8 cards): adapt from Vehicle/Crew pattern — build once, apply across all 8
  - Void-tracker group (2 cards): needs the shared turn-state tracker built first (same shape as SOS's leave-graveyard-trigger gate)
  - Remaining ~40: per-card multi-clause DSL, similar effort profile to SOS's M11–M16 batches
- [ ] **Planeswalker (1 card):** author Tezzeret, Cruel Captain once a planeswalker card is next up in the schedule (engine support already exists — see other 296 PWs)
- [ ] **The Dominion Bracelet:** deprioritize — no Mindslaver-style control-take-over analog anywhere in Wagic; would need new engine work disproportionate to a single card
- [ ] `core.zip` rebuild + Windows/Android deploy once Batch 6 lands

**Owner:** *(TBD — pick up when FIN/TLA/SPM/TMT backlog is clear)*
**Priority:** Medium (after current feature branches merge; before Rooms/Aetherdrift work)
