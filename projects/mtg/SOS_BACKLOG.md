# Secrets of Strixhaven (SOS) - Implementation Backlog

Set code `sos` - Standard expansion, released 2026-04-24. Source: Scryfall `set:sos&unique=cards` (271 unique cards; the 368 print count includes showcase/borderless variants).

Assessment generated 2026-06-25 by classifying each card's Oracle text against Wagic's known mechanic support. Buckets are estimates for triage, not a guarantee - refine per card during authoring.

| Bucket | Count | Meaning |
|---|---|---|
| EASY | 67 | Primitive trivial: vanilla / evergreen-only / single simple effect or trigger. Minutes each. |
| MEDIUM | 148 | Mechanic exists in Wagic but needs careful DSL: activated/triggered abilities, modal, SOS cast-triggers, Ward/Flashback, etc. |
| HARD | 56 | Engine-blocked or no analog: Prepared split layout, copy effects, variable mana-color scaling, planeswalkers. |

## SOS mechanic support map

| Mechanic | Cards | Wagic status | Bucket impact |
|---|---|---|---|
| Prepared (`prepare` layout: Creature // Spell) | 36 | NOT supported - split/DFC layout (#22) + 'cast a copy' (#19) | HARD |
| Converge (counters per color of mana spent) | 9 | NOT supported - variable scaling (#20), no mana-color-spent tracking | HARD |
| Paradigm (recurring cast-a-copy from exile) | 5 | NOT supported - copy effects (#19) | HARD |
| Increment (mana spent vs P/T -> +1/+1) | 9 | Partial - needs mana-spent-per-spell tracking; may need approximation | MEDIUM (risk HARD) |
| Opus (cast-trigger + '5+ mana spent') | 9 | Partial - cast trigger OK, mana-spent condition uncertain | MEDIUM (risk HARD) |
| Repartee (cast instant/sorcery targeting a creature) | 12 | Supported - cast trigger + target filter | MEDIUM |
| Infusion (rider if you gained life this turn) | 12 | Supported - 'gained life this turn' condition | MEDIUM |
| Surveil | 17 | Supported (_SURVEIL1-3_ macros) | EASY/MEDIUM |
| Ward | 11 | Supported (_WARD1-8_ macros) | MEDIUM |
| Flashback | 9 | Supported (native `flashback=` field) | EASY/MEDIUM |
| Evergreen (Flying/Trample/Vigilance/Reach/Haste/Deathtouch/Menace/First strike/Double strike/Lifelink) | many | Supported | EASY |

## HARD (56)


**Converge: variable counters per color of mana spent (#20)**

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

- Applied Geometry _(Sorcery)_
- Aziza, Mage Tower Captain _(Legendary Creature — Djinn Sorcerer)_
- Colorstorm Stallion _(Creature — Elemental Horse)_
- Mica, Reader of Ruins _(Legendary Creature — Human Artificer)_

**Paradigm: recurring cast-a-copy from exile (copy #19)**

- Decorum Dissertation _(Sorcery — Lesson)_
- Echocasting Symposium _(Sorcery — Lesson)_
- Germination Practicum _(Sorcery — Lesson)_
- Improvisation Capstone _(Sorcery — Lesson)_
- Restoration Seminar _(Sorcery — Lesson)_

**Planeswalker: loyalty abilities, hand-authored (#6)**

- Professor Dellian Fel _(Legendary Planeswalker — Dellian)_
- Ral Zarek, Guest Lecturer _(Legendary Planeswalker — Ral)_

**Prepared split (Creature//Spell) + cast-a-copy: DFC/split layout (#22) + copy (#19)**

- Abigale, Poet Laureate // Heroic Stanza _(Legendary Creature — Bird Bard // Sorcery)_
- Adventurous Eater // Have a Bite _(Creature — Human Warlock // Sorcery)_
- Blazing Firesinger // Seething Song _(Creature — Dwarf Bard // Instant)_
- Campus Composer // Aqueous Aria _(Creature — Merfolk Bard // Sorcery)_
- Cheerful Osteomancer // Raise Dead _(Creature — Orc Warlock // Sorcery)_
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

## MEDIUM (148)


**Activated ability**

- Ark of Hunger _(Artifact)_
- Burrog Banemaker _(Creature — Frog Warlock)_
- Deathcap Glade _(Land)_
- Diary of Dreams _(Artifact — Book)_
- Dreamroot Cascade _(Land)_
- Emil, Vastlands Roamer _(Legendary Creature — Elf Druid)_
- Fields of Strife _(Land)_
- Forum of Amity _(Land)_
- Great Hall of the Biblioplex _(Land)_
- Hydro-Channeler _(Creature — Merfolk Wizard)_
- Mindful Biomancer _(Creature — Dryad Druid)_
- Noxious Newt _(Creature — Salamander)_
- Page, Loose Leaf _(Legendary Artifact Creature — Construct)_
- Paradox Gardens _(Land)_
- Petrified Hamlet _(Land)_
- Potioner's Trove _(Artifact)_
- Resonating Lute _(Artifact)_
- Shattered Sanctum _(Land)_
- Skycoach Waypoint _(Land)_
- Spectacle Summit _(Land)_
- Stormcarved Coast _(Land)_
- Summoned Dromedary _(Creature — Spirit Camel)_
- Sundown Pass _(Land)_
- Tablet of Discovery _(Artifact)_
- Teacher's Pest _(Creature — Skeleton Pest)_
- Titan's Grave _(Land)_

**Flashback + body**

- Antiquities on the Loose _(Sorcery)_
- Daydream _(Sorcery)_
- Dig Site Inventory _(Sorcery)_
- Duel Tactics _(Sorcery)_
- Group Project _(Sorcery)_
- Molten Note _(Sorcery)_
- Practiced Offense _(Sorcery)_
- Pursue the Past _(Sorcery)_
- Tome Blast _(Sorcery)_

**Increment: mana-spent vs P/T comparison on cast**

- Ambitious Augmenter _(Creature — Turtle Wizard)_
- Berta, Wise Extrapolator _(Legendary Creature — Frog Druid)_
- Cuboid Colony _(Creature — Insect)_
- Fractal Tender _(Creature — Elf Wizard)_
- Hungry Graffalon _(Creature — Giraffe)_
- Pensive Professor _(Creature — Human Wizard)_
- Tester of the Tangential _(Creature — Djinn Wizard)_
- Textbook Tabulator _(Creature — Frog Wizard)_
- Topiary Lecturer _(Creature — Elf Druid)_

**Infusion: rider on "gained life this turn"**

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

**Modal / alt-cost**

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

**Needs review**

- Charging Strifeknight _(Creature — Spirit Knight)_
- Eternal Student _(Creature — Zombie Warlock)_
- Shattered Acolyte _(Creature — Dwarf Warlock)_
- Slumbering Trudge _(Creature — Plant Beast)_
- Soaring Stoneglider _(Creature — Elephant Cleric)_
- Stone Docent _(Creature — Spirit Chimera)_
- Terramorphic Expanse _(Land)_
- Zaffai and the Tempests _(Legendary Creature — Human Bard Sorcerer)_

**Opus: cast-trigger + 5+ mana-spent condition**

- Deluge Virtuoso _(Creature — Human Wizard)_
- Elemental Mascot _(Creature — Elemental Bird)_
- Exhibition Tidecaller _(Creature — Djinn Wizard)_
- Expressive Firedancer _(Creature — Human Sorcerer)_
- Molten-Core Maestro _(Creature — Goblin Bard)_
- Muse Seeker _(Creature — Elf Wizard)_
- Spectacular Skywhale _(Creature — Elemental Whale)_
- Tackle Artist _(Creature — Orc Sorcerer)_
- Thunderdrum Soloist _(Creature — Dwarf Bard)_

**Repartee: cast-spell-that-targets-creature trigger**

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

**Spell (multi-clause)**

- Brush Off _(Instant)_
- Dina's Guidance _(Instant)_
- Dissection Practice _(Instant)_
- Divergent Equation _(Instant)_
- End of the Hunt _(Sorcery)_
- Essence Scatter _(Instant)_
- Fix What's Broken _(Sorcery)_
- Flashback _(Instant)_
- Flow State _(Sorcery)_
- Fractalize _(Instant)_
- Mind Roots _(Sorcery)_
- Planar Engineering _(Sorcery)_
- Pox Plague _(Sorcery)_
- Proctor's Gaze _(Instant)_
- Render Speechless _(Sorcery)_
- Run Behind _(Instant)_
- Vicious Rivalry _(Sorcery)_
- Wisdom of Ages _(Sorcery)_
- Zimone's Experiment _(Sorcery)_

**Triggered ability (multi-clause/non-trivial)**

- Abstract Paintmage _(Creature — Djinn Sorcerer)_
- Additive Evolution _(Enchantment)_
- Ascendant Dustspeaker _(Creature — Orc Cleric)_
- Colossus of the Blood Age _(Artifact Creature — Construct)_
- Ennis, Debate Moderator _(Legendary Creature — Human Cleric)_
- Environmental Scientist _(Creature — Human Druid)_
- Essenceknit Scholar _(Creature — Dryad Warlock)_
- Geometer's Arthropod _(Creature — Fractal Crab)_
- Killian's Confidence _(Sorcery)_
- Living History _(Enchantment)_
- Lorehold, the Historian _(Legendary Creature — Elder Dragon)_
- Mana Sculpt _(Instant)_
- Matterbending Mage _(Creature — Human Wizard)_
- Owlin Historian _(Creature — Bird Cleric)_
- Paradox Surveyor _(Creature — Elf Druid)_
- Postmortem Professor _(Creature — Zombie Warlock)_
- Primary Research _(Enchantment)_
- Quandrix, the Proof _(Legendary Creature — Elder Dragon)_
- Rubble Rouser _(Creature — Dwarf Sorcerer)_
- Silverquill, the Disputant _(Legendary Creature — Elder Dragon)_
- Social Snub _(Sorcery)_
- Startled Relic Sloth _(Creature — Sloth Beast)_
- Strixhaven Skycoach _(Artifact — Vehicle)_

**Variable/"for each" scaling effect**

- Aberrant Manawurm _(Creature — Wurm)_
- Ancestral Anger _(Sorcery)_
- Borrowed Knowledge _(Sorcery)_
- Fractal Anomaly _(Instant)_
- Prismari, the Inspiration _(Legendary Creature — Elder Dragon)_
- Steal the Show _(Sorcery)_
- Stirring Honormancer _(Creature — Rhino Bard)_
- Suspend Aggression _(Instant)_
- The Dawning Archaic _(Legendary Creature — Avatar)_
- Witherbloom, the Balancer _(Legendary Creature — Elder Dragon)_

## EASY (67)


**Basic land**

- Forest _(Basic Land — Forest)_
- Island _(Basic Land — Island)_
- Mountain _(Basic Land — Mountain)_
- Plains _(Basic Land — Plains)_
- Swamp _(Basic Land — Swamp)_

**Evergreen/keyword-only**

- Rearing Embermare _(Creature — Horse Beast)_

**Simple single-effect spell**

- Ajani's Response _(Instant)_
- Banishing Betrayal _(Instant)_
- Burrog Barrage _(Instant)_
- Chase Inspiration _(Instant)_
- Chelonian Tackle _(Sorcery)_
- Cost of Brilliance _(Sorcery)_
- Embrace the Paradox _(Instant)_
- Erode _(Instant)_
- Grapple with Death _(Sorcery)_
- Growth Curve _(Sorcery)_
- Harsh Annotation _(Instant)_
- Heated Argument _(Instant)_
- Homesickness _(Instant)_
- Impractical Joke _(Sorcery)_
- Interjection _(Instant)_
- Last Gasp _(Instant)_
- Masterful Flourish _(Instant)_
- Mathemagics _(Sorcery)_
- Mind into Matter _(Sorcery)_
- Muse's Encouragement _(Instant)_
- Oracle's Restoration _(Sorcery)_
- Procrastinate _(Sorcery)_
- Pull from the Grave _(Sorcery)_
- Quick Study _(Instant)_
- Rapier Wit _(Instant)_
- Rapturous Moment _(Sorcery)_
- Seize the Spoils _(Sorcery)_
- Stand Up for Yourself _(Instant)_
- Stress Dream _(Instant)_
- Traumatic Critique _(Instant)_
- Unsubtle Mockery _(Instant)_
- Vibrant Outburst _(Instant)_
- Visionary's Dance _(Sorcery)_
- Wander Off _(Instant)_
- Wild Hypothesis _(Sorcery)_
- Wilt in the Heat _(Instant)_

**Single simple triggered ability**

- Arnyn, Deathbloom Botanist _(Legendary Creature — Vampire Druid)_
- Blech, Loafing Pest _(Legendary Creature — Pest)_
- Bogwater Lumaret _(Creature — Spirit Frog)_
- Cauldron of Essence _(Artifact)_
- Comforting Counsel _(Enchantment)_
- Eager Glyphmage _(Creature — Cat Cleric)_
- Fractal Mascot _(Creature — Fractal Elk)_
- Garrison Excavator _(Creature — Orc Sorcerer)_
- Hardened Academic _(Creature — Bird Cleric)_
- Imperious Inkmage _(Creature — Orc Warlock)_
- Mage Tower Referee _(Artifact Creature — Construct)_
- Nita, Forum Conciliator _(Legendary Creature — Human Advisor)_
- Orysa, Tide Choreographer _(Legendary Creature — Merfolk Bard)_
- Pest Mascot _(Creature — Pest Ape)_
- Pestbrood Sloth _(Creature — Plant Sloth)_
- Practiced Scrollsmith _(Creature — Dwarf Cleric)_
- Pterafractyl _(Creature — Dinosaur Fractal)_
- Rabid Attack _(Instant)_
- Root Manipulation _(Sorcery)_
- Send in the Pest _(Sorcery)_
- Shopkeeper's Bane _(Creature — Badger Pest)_
- Sneering Shadewriter _(Creature — Vampire Warlock)_
- Spirit Mascot _(Creature — Spirit Ox)_
- Stadium Tidalmage _(Creature — Djinn Sorcerer)_
- Zealous Lorecaster _(Creature — Giant Sorcerer)_


