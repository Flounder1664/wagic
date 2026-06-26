# Secrets of Strixhaven (SOS) - Implementation Backlog

Set code `sos` - Standard expansion, 2026-04-24. Source: Scryfall `set:sos&unique=cards` (271 unique cards).

Assessment generated 2026-06-25, **re-bucketed 2026-06-26** after authoring. The original heuristic over-counted EASY; cards needing leave-graveyard triggers (no Wagic impl), X-scaling, cost-reduction, token-with-ability, fight, or cast-from-exile were moved to MEDIUM.

## Status

| Bucket | Count | Notes |
|---|---|---|
| EASY | 32 | **ALL IMPLEMENTED** (26 new primitives ids 697001-697027 + 5 basic lands + Last Gasp reprint). WSL TestSuiteAI 817/0. |
| MEDIUM | 183 | Supported mechanics needing careful DSL, incl. 35 re-bucketed from EASY. |
| HARD | 56 | Engine-blocked / no analog: Prepared split (36), Converge (9), Paradigm (5), copy (4), planeswalkers (2). |

## MEDIUM - Implementation Batch Plan

183 MEDIUM cards grouped into 16 mechanic-coherent batches. Order is a suggestion: Tier A builds the 4 new SOS keyword patterns; Tier B is standard DSL; Tier C is engine/variable-scaling-gated; Tier D is per-card cleanup. Each batch builds one reusable pattern, then applies it across the batch.

| Batch | Mechanic | Cards | Pattern to build | Risk |
|---|---|---|---|---|
| M1 | Infusion | 12 | build the gained-life-this-turn condition once | Low-Med |
| M2 | Repartee | 12 | cast-trigger + "targets a creature" filter | Med |
| M3 | Opus | 9 | cast-trigger + mana-spent threshold | HIGH - mana-spent tracking uncertain |
| M4 | Increment | 9 | per-cast mana-vs-P/T compare | HIGH - may need engine work |
| M5 | Flashback | 9 | native flashback= field | Low |
| M6 | Modal / College Charms | 11 | choice name(...) ... name(...) form | Low-Med |
| M7 | Nonbasic lands | 13 | land DSL (ETB tapped, tap-for-mana, fetch) | Low-Med |
| M8 | Activated creatures & artifacts | 17 | activated-ability forms | Low-Med |
| M9 | Leave-graveyard trigger | 8 | GATED: build the trigger first (no Wagic impl) | HIGH - new shared mechanic, unlocks all 8 |
| M10 | Variable scaling | 12 | X handling + dynamic counts (some #20-blocked) | Med-High |
| M11 | Misc one-off mechanics | 14 | one pattern per mechanic | Mixed |
| M12 | Multi-clause spells A | 11 | per-card, existing DSL | Med |
| M13 | Multi-clause spells B | 11 | per-card, existing DSL | Med |
| M14 | Multi-clause spells C | 9 | per-card, existing DSL | Med |
| M15 | Multi-clause permanents A | 13 | per-card, existing DSL | Med |
| M16 | Multi-clause permanents B | 13 | per-card, existing DSL | Med |

### M1 - Infusion (12)  _["if you gained life this turn" rider]_

- Tragedy Feaster _(Creature — Demon)_
- Thornfist Striker _(Creature — Elf Druid)_
- Ulna Alley Shopkeep _(Creature — Goblin Warlock)_
- Poisoner's Apprentice _(Creature — Orc Warlock)_
- Old-Growth Educator _(Creature — Treefolk Druid)_
- Tenured Concocter _(Creature — Troll Druid)_
- Efflorescence _(Instant)_
- Foolish Fate _(Instant)_
- Lumaret's Favor _(Instant)_
- Moseo, Vein's New Dean _(Legendary Creature — Bird Skeleton Warlock)_
- Follow the Lumarets _(Sorcery)_
- Withering Curse _(Sorcery)_

### M2 - Repartee (12)  _[cast an instant/sorcery that targets a creature]_

- Stirring Hopesinger _(Creature — Bird Bard)_
- Rehearsed Debater _(Creature — Djinn Bard)_
- Scolding Administrator _(Creature — Dwarf Cleric)_
- Inkshape Demonstrator _(Creature — Elephant Cleric)_
- Melancholic Poet _(Creature — Elf Bard)_
- Snooping Page _(Creature — Human Cleric)_
- Lecturing Scornmage _(Creature — Human Warlock)_
- Informed Inkwright _(Creature — Human Wizard)_
- Inkling Mascot _(Creature — Inkling Cat)_
- Conciliator's Duelist _(Creature — Kor Warlock)_
- Forum Necroscribe _(Creature — Troll Warlock)_
- Graduation Day _(Enchantment)_

### M3 - Opus (9)  _[cast-trigger + "5+ mana spent"]_

- Exhibition Tidecaller _(Creature — Djinn Wizard)_
- Thunderdrum Soloist _(Creature — Dwarf Bard)_
- Elemental Mascot _(Creature — Elemental Bird)_
- Spectacular Skywhale _(Creature — Elemental Whale)_
- Muse Seeker _(Creature — Elf Wizard)_
- Molten-Core Maestro _(Creature — Goblin Bard)_
- Expressive Firedancer _(Creature — Human Sorcerer)_
- Deluge Virtuoso _(Creature — Human Wizard)_
- Tackle Artist _(Creature — Orc Sorcerer)_

### M4 - Increment (9)  _[mana spent vs this creature P/T -> +1/+1]_

- Tester of the Tangential _(Creature — Djinn Wizard)_
- Topiary Lecturer _(Creature — Elf Druid)_
- Fractal Tender _(Creature — Elf Wizard)_
- Textbook Tabulator _(Creature — Frog Wizard)_
- Hungry Graffalon _(Creature — Giraffe)_
- Pensive Professor _(Creature — Human Wizard)_
- Cuboid Colony _(Creature — Insect)_
- Ambitious Augmenter _(Creature — Turtle Wizard)_
- Berta, Wise Extrapolator _(Legendary Creature — Frog Druid)_

### M5 - Flashback (9)  _[graveyard recast]_

- Flashback _(Instant)_
- Antiquities on the Loose _(Sorcery)_
- Daydream _(Sorcery)_
- Dig Site Inventory _(Sorcery)_
- Duel Tactics _(Sorcery)_
- Group Project _(Sorcery)_
- Practiced Offense _(Sorcery)_
- Pursue the Past _(Sorcery)_
- Tome Blast _(Sorcery)_

### M6 - Modal / College Charms (11)  _[choose one / two]_

- Biblioplex Tomekeeper _(Artifact Creature — Construct)_
- Choreographed Sparks _(Instant)_
- Glorious Decay _(Instant)_
- Lorehold Charm _(Instant)_
- Prismari Charm _(Instant)_
- Quandrix Charm _(Instant)_
- Silverquill Charm _(Instant)_
- Witherbloom Charm _(Instant)_
- Artistic Process _(Sorcery)_
- Moment of Reckoning _(Sorcery)_
- Splatter Technique _(Sorcery)_

### M7 - Nonbasic lands (13)  _[duals / utility / fetch lands]_

- Deathcap Glade _(Land)_
- Dreamroot Cascade _(Land)_
- Fields of Strife _(Land)_
- Forum of Amity _(Land)_
- Great Hall of the Biblioplex _(Land)_
- Paradox Gardens _(Land)_
- Petrified Hamlet _(Land)_
- Shattered Sanctum _(Land)_
- Skycoach Waypoint _(Land)_
- Spectacle Summit _(Land)_
- Stormcarved Coast _(Land)_
- Sundown Pass _(Land)_
- Titan's Grave _(Land)_

### M8 - Activated creatures & artifacts (17)  _[{cost}: / {T}: abilities]_

- Cauldron of Essence _(Artifact)_
- Potioner's Trove _(Artifact)_
- Resonating Lute _(Artifact)_
- Tablet of Discovery _(Artifact)_
- Mindful Biomancer _(Creature — Dryad Druid)_
- Shattered Acolyte _(Creature — Dwarf Warlock)_
- Burrog Banemaker _(Creature — Frog Warlock)_
- Hydro-Channeler _(Creature — Merfolk Wizard)_
- Noxious Newt _(Creature — Salamander)_
- Teacher's Pest _(Creature — Skeleton Pest)_
- Summoned Dromedary _(Creature — Spirit Camel)_
- Stone Docent _(Creature — Spirit Chimera)_
- Eternal Student _(Creature — Zombie Warlock)_
- Postmortem Professor _(Creature — Zombie Warlock)_
- Page, Loose Leaf _(Legendary Artifact Creature — Construct)_
- Emil, Vastlands Roamer _(Legendary Creature — Elf Druid)_
- Visionary's Dance _(Sorcery)_

### M9 - Leave-graveyard trigger (8)  _["whenever cards leave your graveyard"]_

- Ark of Hunger _(Artifact)_
- Hardened Academic _(Creature — Bird Cleric)_
- Owlin Historian _(Creature — Bird Cleric)_
- Garrison Excavator _(Creature — Orc Sorcerer)_
- Spirit Mascot _(Creature — Spirit Ox)_
- Living History _(Enchantment)_
- Primary Research _(Enchantment)_
- Wilt in the Heat _(Instant)_

### M10 - Variable scaling (12)  _[X-cost / "for each" dynamic counts]_

- Pterafractyl _(Creature — Dinosaur Fractal)_
- Slumbering Trudge _(Creature — Plant Beast)_
- Divergent Equation _(Instant)_
- Fractalize _(Instant)_
- Suspend Aggression _(Instant)_
- Borrowed Knowledge _(Sorcery)_
- Mathemagics _(Sorcery)_
- Mind into Matter _(Sorcery)_
- Molten Note _(Sorcery)_
- Procrastinate _(Sorcery)_
- Steal the Show _(Sorcery)_
- Wild Hypothesis _(Sorcery)_

### M11 - Misc one-off mechanics (14)  _[cost-reduction, fight, doubling counters, multicolored-cast, cast-from-exile, token-with-ability, Ward]_

- Diary of Dreams _(Artifact — Book)_
- Mage Tower Referee _(Artifact Creature — Construct)_
- Essenceknit Scholar _(Creature — Dryad Warlock)_
- Practiced Scrollsmith _(Creature — Dwarf Cleric)_
- Ajani's Response _(Instant)_
- Run Behind _(Instant)_
- The Dawning Archaic _(Legendary Creature — Avatar)_
- Prismari, the Inspiration _(Legendary Creature — Elder Dragon)_
- Witherbloom, the Balancer _(Legendary Creature — Elder Dragon)_
- Nita, Forum Conciliator _(Legendary Creature — Human Advisor)_
- Orysa, Tide Choreographer _(Legendary Creature — Merfolk Bard)_
- Chelonian Tackle _(Sorcery)_
- Growth Curve _(Sorcery)_
- Send in the Pest _(Sorcery)_

### M12 - Multi-clause spells A (11)  _[instants / sorceries]_

- Brush Off _(Instant)_
- Burrog Barrage _(Instant)_
- Dina's Guidance _(Instant)_
- Dissection Practice _(Instant)_
- Erode _(Instant)_
- Essence Scatter _(Instant)_
- Fractal Anomaly _(Instant)_
- Harsh Annotation _(Instant)_
- Heated Argument _(Instant)_
- Homesickness _(Instant)_
- Mana Sculpt _(Instant)_

### M13 - Multi-clause spells B (11)  _[instants / sorceries]_

- Proctor's Gaze _(Instant)_
- Rabid Attack _(Instant)_
- Rapier Wit _(Instant)_
- Stress Dream _(Instant)_
- Ancestral Anger _(Sorcery)_
- Cost of Brilliance _(Sorcery)_
- End of the Hunt _(Sorcery)_
- Fix What's Broken _(Sorcery)_
- Flow State _(Sorcery)_
- Impractical Joke _(Sorcery)_
- Killian's Confidence _(Sorcery)_

### M14 - Multi-clause spells C (9)  _[instants / sorceries]_

- Mind Roots _(Sorcery)_
- Planar Engineering _(Sorcery)_
- Pox Plague _(Sorcery)_
- Render Speechless _(Sorcery)_
- Root Manipulation _(Sorcery)_
- Social Snub _(Sorcery)_
- Vicious Rivalry _(Sorcery)_
- Wisdom of Ages _(Sorcery)_
- Zimone's Experiment _(Sorcery)_

### M15 - Multi-clause permanents A (13)  _[creatures / legendaries / artifacts]_

- Strixhaven Skycoach _(Artifact — Vehicle)_
- Colossus of the Blood Age _(Artifact Creature — Construct)_
- Abstract Paintmage _(Creature — Djinn Sorcerer)_
- Rubble Rouser _(Creature — Dwarf Sorcerer)_
- Soaring Stoneglider _(Creature — Elephant Cleric)_
- Paradox Surveyor _(Creature — Elf Druid)_
- Geometer's Arthropod _(Creature — Fractal Crab)_
- Fractal Mascot _(Creature — Fractal Elk)_
- Environmental Scientist _(Creature — Human Druid)_
- Matterbending Mage _(Creature — Human Wizard)_
- Ascendant Dustspeaker _(Creature — Orc Cleric)_
- Pestbrood Sloth _(Creature — Plant Sloth)_
- Stirring Honormancer _(Creature — Rhino Bard)_

### M16 - Multi-clause permanents B (13)  _[creatures / legendaries / artifacts]_

- Startled Relic Sloth _(Creature — Sloth Beast)_
- Charging Strifeknight _(Creature — Spirit Knight)_
- Aberrant Manawurm _(Creature — Wurm)_
- Additive Evolution _(Enchantment)_
- Comforting Counsel _(Enchantment)_
- Terramorphic Expanse _(Land)_
- Lorehold, the Historian _(Legendary Creature — Elder Dragon)_
- Quandrix, the Proof _(Legendary Creature — Elder Dragon)_
- Silverquill, the Disputant _(Legendary Creature — Elder Dragon)_
- Zaffai and the Tempests _(Legendary Creature — Human Bard Sorcerer)_
- Ennis, Debate Moderator _(Legendary Creature — Human Cleric)_
- Blech, Loafing Pest _(Legendary Creature — Pest)_
- Arnyn, Deathbloom Botanist _(Legendary Creature — Vampire Druid)_



## HARD (56)


**Converge: variable mana-color scaling (#20)**

- Arcane Omens _(Sorcery)_
- Archaic's Agony _(Sorcery)_
- Magmablood Archaic _(Creature — Avatar)_
- Rancorous Archaic _(Creature — Avatar)_
- Snarl Song _(Sorcery)_
- Sundering Archaic _(Creature — Avatar)_
- Together as One _(Sorcery)_
- Transcendent Archaic _(Creature — Avatar)_
- Wildgrowth Archaic _(Creature — Avatar)_

**Copy effect (#19)**

- Abigale, Poet Laureate // Heroic Stanza _(Legendary Creature — Bird Bard // Sorcery)_
- Adventurous Eater // Have a Bite _(Creature — Human Warlock // Sorcery)_
- Applied Geometry _(Sorcery)_
- Aziza, Mage Tower Captain _(Legendary Creature — Djinn Sorcerer)_
- Blazing Firesinger // Seething Song _(Creature — Dwarf Bard // Instant)_
- Campus Composer // Aqueous Aria _(Creature — Merfolk Bard // Sorcery)_
- Cheerful Osteomancer // Raise Dead _(Creature — Orc Warlock // Sorcery)_
- Colorstorm Stallion _(Creature — Elemental Horse)_
- Elite Interceptor // Rejoinder _(Creature — Human Wizard // Sorcery)_
- Emeritus of Abundance // Regrowth _(Creature — Elf Druid // Sorcery)_
- Emeritus of Conflict // Lightning Bolt _(Creature — Human Wizard // Instant)_
- Emeritus of Ideation // Ancestral Recall _(Creature — Human Wizard // Instant)_
- Emeritus of Truce // Swords to Plowshares _(Creature — Cat Cleric // Instant)_
- Emeritus of Woe // Demonic Tutor _(Creature — Vampire Warlock // Sorcery)_
- Encouraging Aviator // Jump _(Creature — Bird Wizard // Instant)_
- Goblin Glasswright // Craft with Pride _(Creature — Goblin Sorcerer // Sorcery)_
- Grave Researcher // Reanimate _(Creature — Troll Warlock // Sorcery)_
- Harmonized Trio // Brainstorm _(Creature — Merfolk Bard Wizard // Instant)_
- Honorbound Page // Forum's Favor _(Creature — Cat Cleric // Sorcery)_
- Infirmary Healer // Stream of Life _(Creature — Cat Cleric // Sorcery)_
- Jadzi, Steward of Fate // Oracle's Gift _(Legendary Creature — Human Wizard // Sorcery)_
- Joined Researchers // Secret Rendezvous _(Creature — Human Cleric Wizard // Sorcery)_
- Kirol, History Buff // Pack a Punch _(Legendary Creature — Vampire Cleric // Sorcery)_
- Landscape Painter // Vibrant Idea _(Creature — Merfolk Wizard // Sorcery)_
- Leech Collector // Bloodletting _(Creature — Human Warlock // Sorcery)_
- Lluwen, Exchange Student // Pest Friend _(Legendary Creature — Elf Druid // Sorcery)_
- Maelstrom Artisan // Rocket Volley _(Creature — Minotaur Sorcerer // Sorcery)_
- Mica, Reader of Ruins _(Legendary Creature — Human Artificer)_
- Pigment Wrangler // Striking Palette _(Creature — Orc Sorcerer // Sorcery)_
- Quill-Blade Laureate // Twofold Intent _(Creature — Human Cleric // Sorcery)_
- Sanar, Unfinished Genius // Wild Idea _(Legendary Creature — Goblin Sorcerer // Sorcery)_
- Scathing Shadelock // Venomous Words _(Creature — Snake Warlock // Sorcery)_
- Scheming Silvertongue // Sign in Blood _(Creature — Vampire Warlock // Sorcery)_
- Skycoach Conductor // All Aboard _(Creature — Bird Pilot // Instant)_
- Spellbook Seeker // Careful Study _(Creature — Bird Wizard // Sorcery)_
- Spiritcall Enthusiast // Scrollboost _(Creature — Cat Cleric // Sorcery)_
- Strife Scholar // Awaken the Ages _(Creature — Orc Sorcerer // Sorcery)_
- Studious First-Year // Rampant Growth _(Creature — Bear Wizard // Sorcery)_
- Tam, Observant Sequencer // Deep Sight _(Legendary Creature — Gorgon Wizard // Sorcery)_
- Vastlands Scavenger // Bind to Life _(Creature — Bear Druid // Instant)_

**Paradigm: cast-a-copy from exile (#19)**

- Decorum Dissertation _(Sorcery — Lesson)_
- Echocasting Symposium _(Sorcery — Lesson)_
- Germination Practicum _(Sorcery — Lesson)_
- Improvisation Capstone _(Sorcery — Lesson)_
- Restoration Seminar _(Sorcery — Lesson)_

**Planeswalker (#6)**

- Professor Dellian Fel _(Legendary Planeswalker — Dellian)_
- Ral Zarek, Guest Lecturer _(Legendary Planeswalker — Ral)_

## MEDIUM (183)


**"for each" scaling**

- Borrowed Knowledge _(Sorcery)_
- Steal the Show _(Sorcery)_
- Suspend Aggression _(Instant)_

**activated ability**

- Burrog Banemaker _(Creature — Frog Warlock)_
- Deathcap Glade _(Land)_
- Dreamroot Cascade _(Land)_
- Emil, Vastlands Roamer _(Legendary Creature — Elf Druid)_
- Eternal Student _(Creature — Zombie Warlock)_
- Fields of Strife _(Land)_
- Forum of Amity _(Land)_
- Great Hall of the Biblioplex _(Land)_
- Hydro-Channeler _(Creature — Merfolk Wizard)_
- Mindful Biomancer _(Creature — Dryad Druid)_
- Noxious Newt _(Creature — Salamander)_
- Page, Loose Leaf _(Legendary Artifact Creature — Construct)_
- Paradox Gardens _(Land)_
- Petrified Hamlet _(Land)_
- Postmortem Professor _(Creature — Zombie Warlock)_
- Potioner's Trove _(Artifact)_
- Resonating Lute _(Artifact)_
- Shattered Acolyte _(Creature — Dwarf Warlock)_
- Shattered Sanctum _(Land)_
- Skycoach Waypoint _(Land)_
- Spectacle Summit _(Land)_
- Stone Docent _(Creature — Spirit Chimera)_
- Stormcarved Coast _(Land)_
- Summoned Dromedary _(Creature — Spirit Camel)_
- Sundown Pass _(Land)_
- Tablet of Discovery _(Artifact)_
- Teacher's Pest _(Creature — Skeleton Pest)_
- Titan's Grave _(Land)_

**conditional cost reduction**

- Diary of Dreams _(Artifact — Book)_
- Run Behind _(Instant)_
- The Dawning Archaic _(Legendary Creature — Avatar)_
- Witherbloom, the Balancer _(Legendary Creature — Elder Dragon)_

**flashback + body**

- Antiquities on the Loose _(Sorcery)_
- Daydream _(Sorcery)_
- Dig Site Inventory _(Sorcery)_
- Duel Tactics _(Sorcery)_
- Flashback _(Instant)_
- Group Project _(Sorcery)_
- Practiced Offense _(Sorcery)_
- Pursue the Past _(Sorcery)_
- Tome Blast _(Sorcery)_

**Increment (mana-spent vs P/T)**

- Ambitious Augmenter _(Creature — Turtle Wizard)_
- Berta, Wise Extrapolator _(Legendary Creature — Frog Druid)_
- Cuboid Colony _(Creature — Insect)_
- Fractal Tender _(Creature — Elf Wizard)_
- Hungry Graffalon _(Creature — Giraffe)_
- Pensive Professor _(Creature — Human Wizard)_
- Tester of the Tangential _(Creature — Djinn Wizard)_
- Textbook Tabulator _(Creature — Frog Wizard)_
- Topiary Lecturer _(Creature — Elf Druid)_

**Infusion (gained-life-this-turn rider)**

- Efflorescence _(Instant)_
- Follow the Lumarets _(Sorcery)_
- Foolish Fate _(Instant)_
- Lumaret's Favor _(Instant)_
- Moseo, Vein's New Dean _(Legendary Creature — Bird Skeleton Warlock)_
- Old-Growth Educator _(Creature — Treefolk Druid)_
- Poisoner's Apprentice _(Creature — Orc Warlock)_
- Tenured Concocter _(Creature — Troll Druid)_
- Thornfist Striker _(Creature — Elf Druid)_
- Tragedy Feaster _(Creature — Demon)_
- Ulna Alley Shopkeep _(Creature — Goblin Warlock)_
- Withering Curse _(Sorcery)_

**leave-graveyard trigger (no Wagic impl)**

- Ark of Hunger _(Artifact)_
- Living History _(Enchantment)_
- Owlin Historian _(Creature — Bird Cleric)_
- Primary Research _(Enchantment)_

**modal**

- Artistic Process _(Sorcery)_
- Biblioplex Tomekeeper _(Artifact Creature — Construct)_
- Choreographed Sparks _(Instant)_
- Glorious Decay _(Instant)_
- Lorehold Charm _(Instant)_
- Moment of Reckoning _(Sorcery)_
- Prismari Charm _(Instant)_
- Quandrix Charm _(Instant)_
- Silverquill Charm _(Instant)_
- Splatter Technique _(Sorcery)_
- Witherbloom Charm _(Instant)_

**multi-clause / needs careful DSL**

- Aberrant Manawurm _(Creature — Wurm)_
- Abstract Paintmage _(Creature — Djinn Sorcerer)_
- Additive Evolution _(Enchantment)_
- Ancestral Anger _(Sorcery)_
- Ascendant Dustspeaker _(Creature — Orc Cleric)_
- Brush Off _(Instant)_
- Charging Strifeknight _(Creature — Spirit Knight)_
- Colossus of the Blood Age _(Artifact Creature — Construct)_
- Dina's Guidance _(Instant)_
- Dissection Practice _(Instant)_
- End of the Hunt _(Sorcery)_
- Ennis, Debate Moderator _(Legendary Creature — Human Cleric)_
- Environmental Scientist _(Creature — Human Druid)_
- Essence Scatter _(Instant)_
- Fix What's Broken _(Sorcery)_
- Flow State _(Sorcery)_
- Fractal Anomaly _(Instant)_
- Geometer's Arthropod _(Creature — Fractal Crab)_
- Killian's Confidence _(Sorcery)_
- Lorehold, the Historian _(Legendary Creature — Elder Dragon)_
- Mana Sculpt _(Instant)_
- Matterbending Mage _(Creature — Human Wizard)_
- Mind Roots _(Sorcery)_
- Paradox Surveyor _(Creature — Elf Druid)_
- Planar Engineering _(Sorcery)_
- Pox Plague _(Sorcery)_
- Proctor's Gaze _(Instant)_
- Quandrix, the Proof _(Legendary Creature — Elder Dragon)_
- Render Speechless _(Sorcery)_
- Rubble Rouser _(Creature — Dwarf Sorcerer)_
- Silverquill, the Disputant _(Legendary Creature — Elder Dragon)_
- Soaring Stoneglider _(Creature — Elephant Cleric)_
- Social Snub _(Sorcery)_
- Startled Relic Sloth _(Creature — Sloth Beast)_
- Stirring Honormancer _(Creature — Rhino Bard)_
- Strixhaven Skycoach _(Artifact — Vehicle)_
- Terramorphic Expanse _(Land)_
- Vicious Rivalry _(Sorcery)_
- Wisdom of Ages _(Sorcery)_
- Zaffai and the Tempests _(Legendary Creature — Human Bard Sorcerer)_
- Zimone's Experiment _(Sorcery)_

**Opus (cast-trigger + 5+ mana spent)**

- Deluge Virtuoso _(Creature — Human Wizard)_
- Elemental Mascot _(Creature — Elemental Bird)_
- Exhibition Tidecaller _(Creature — Djinn Wizard)_
- Expressive Firedancer _(Creature — Human Sorcerer)_
- Molten-Core Maestro _(Creature — Goblin Bard)_
- Muse Seeker _(Creature — Elf Wizard)_
- Spectacular Skywhale _(Creature — Elemental Whale)_
- Tackle Artist _(Creature — Orc Sorcerer)_
- Thunderdrum Soloist _(Creature — Dwarf Bard)_

**re-bucketed: activated ability**

- Cauldron of Essence _(Artifact)_
- Visionary's Dance _(Sorcery)_

**re-bucketed: cast-from-exile/graveyard**

- Nita, Forum Conciliator _(Legendary Creature — Human Advisor)_
- Practiced Scrollsmith _(Creature — Dwarf Cleric)_

**re-bucketed: conditional cost reduction**

- Ajani's Response _(Instant)_
- Orysa, Tide Choreographer _(Legendary Creature — Merfolk Bard)_

**re-bucketed: doubling counters**

- Growth Curve _(Sorcery)_

**re-bucketed: fight**

- Chelonian Tackle _(Sorcery)_

**re-bucketed: leave-graveyard trigger (no Wagic impl)**

- Garrison Excavator _(Creature — Orc Sorcerer)_
- Hardened Academic _(Creature — Bird Cleric)_
- Spirit Mascot _(Creature — Spirit Ox)_
- Wilt in the Heat _(Instant)_

**re-bucketed: multi-clause / needs careful DSL**

- Arnyn, Deathbloom Botanist _(Legendary Creature — Vampire Druid)_
- Blech, Loafing Pest _(Legendary Creature — Pest)_
- Burrog Barrage _(Instant)_
- Comforting Counsel _(Enchantment)_
- Cost of Brilliance _(Sorcery)_
- Erode _(Instant)_
- Fractal Mascot _(Creature — Fractal Elk)_
- Harsh Annotation _(Instant)_
- Heated Argument _(Instant)_
- Homesickness _(Instant)_
- Impractical Joke _(Sorcery)_
- Pestbrood Sloth _(Creature — Plant Sloth)_
- Rabid Attack _(Instant)_
- Rapier Wit _(Instant)_
- Root Manipulation _(Sorcery)_
- Stress Dream _(Instant)_

**re-bucketed: multicolored-cast trigger**

- Mage Tower Referee _(Artifact Creature — Construct)_

**re-bucketed: token with granted triggered ability**

- Send in the Pest _(Sorcery)_

**re-bucketed: X-cost / variable scaling**

- Mathemagics _(Sorcery)_
- Mind into Matter _(Sorcery)_
- Procrastinate _(Sorcery)_
- Pterafractyl _(Creature — Dinosaur Fractal)_
- Wild Hypothesis _(Sorcery)_

**Repartee (cast-targets-creature trigger)**

- Conciliator's Duelist _(Creature — Kor Warlock)_
- Forum Necroscribe _(Creature — Troll Warlock)_
- Graduation Day _(Enchantment)_
- Informed Inkwright _(Creature — Human Wizard)_
- Inkling Mascot _(Creature — Inkling Cat)_
- Inkshape Demonstrator _(Creature — Elephant Cleric)_
- Lecturing Scornmage _(Creature — Human Warlock)_
- Melancholic Poet _(Creature — Elf Bard)_
- Rehearsed Debater _(Creature — Djinn Bard)_
- Scolding Administrator _(Creature — Dwarf Cleric)_
- Snooping Page _(Creature — Human Cleric)_
- Stirring Hopesinger _(Creature — Bird Bard)_

**token with granted ability**

- Essenceknit Scholar _(Creature — Dryad Warlock)_

**Ward + other text**

- Prismari, the Inspiration _(Legendary Creature — Elder Dragon)_

**X-cost / variable scaling**

- Divergent Equation _(Instant)_
- Fractalize _(Instant)_
- Molten Note _(Sorcery)_
- Slumbering Trudge _(Creature — Plant Beast)_

## EASY (32)

_All implemented. (D) = new primitive this cycle; (R) = existing reprint/basic._

- [x] Forest _(Basic Land — Forest)_ (R)
- [x] Island _(Basic Land — Island)_ (R)
- [x] Mountain _(Basic Land — Mountain)_ (R)
- [x] Plains _(Basic Land — Plains)_ (R)
- [x] Swamp _(Basic Land — Swamp)_ (R)
- [x] Shopkeeper's Bane _(Creature — Badger Pest)_ (D)
- [x] Eager Glyphmage _(Creature — Cat Cleric)_ (D)
- [x] Stadium Tidalmage _(Creature — Djinn Sorcerer)_ (D)
- [x] Zealous Lorecaster _(Creature — Giant Sorcerer)_ (D)
- [x] Rearing Embermare _(Creature — Horse Beast)_ (D)
- [x] Imperious Inkmage _(Creature — Orc Warlock)_ (D)
- [x] Pest Mascot _(Creature — Pest Ape)_ (D)
- [x] Bogwater Lumaret _(Creature — Spirit Frog)_ (D)
- [x] Sneering Shadewriter _(Creature — Vampire Warlock)_ (D)
- [x] Banishing Betrayal _(Instant)_ (D)
- [x] Chase Inspiration _(Instant)_ (D)
- [x] Embrace the Paradox _(Instant)_ (D)
- [x] Interjection _(Instant)_ (D)
- [x] Last Gasp _(Instant)_ (R)
- [x] Masterful Flourish _(Instant)_ (D)
- [x] Muse's Encouragement _(Instant)_ (D)
- [x] Quick Study _(Instant)_ (D)
- [x] Stand Up for Yourself _(Instant)_ (D)
- [x] Traumatic Critique _(Instant)_ (D)
- [x] Unsubtle Mockery _(Instant)_ (D)
- [x] Vibrant Outburst _(Instant)_ (D)
- [x] Wander Off _(Instant)_ (D)
- [x] Grapple with Death _(Sorcery)_ (D)
- [x] Oracle's Restoration _(Sorcery)_ (D)
- [x] Pull from the Grave _(Sorcery)_ (D)
- [x] Rapturous Moment _(Sorcery)_ (D)
- [x] Seize the Spoils _(Sorcery)_ (D)


