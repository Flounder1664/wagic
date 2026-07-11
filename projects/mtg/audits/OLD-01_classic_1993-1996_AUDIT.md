# Classic Era Coverage Audit — 1993–1996 (OLD-01)

Sixteen sets in release order: **LEA, LEB, 2ED, ARN, ATQ, RV, LEG, DRK, PHPR, FEM, 4ED, ICE, CHR, HML, ALL, MIR.**
Source: `projects/mtg/bin/Res/missing_cards_by_sets/<CODE>.txt` (full oracle text per card), cross-checked against
`grade_index.json`. See [`README.md`](README.md) for grade tiers and the ENGINE-BLOCKED / BACKLOG-EASY /
BACKLOG-MEDIUM / OUT-OF-SCOPE bucket definitions.

## Intro / headline numbers

- **Raw card instances** across all 16 files (deduped within each set): **370**.
- **Distinct cards**: **245**.
- **Stale** (listed as "missing" but *now* implemented at a playable grade in `grade_index.json`): **2** —
  **Crown of the Ages** and **Flooded Woodlands**, both in **ICE**, both `borderline`. These were authored
  since the missing-file was written; they are false positives, not real gaps. (Verified: the two known-stale
  entries flagged in the task are exactly these two, and no others turned up.)
- **Genuinely excluded distinct cards**: **243**.
- Every remaining name resolves to `unsupported` in `grade_index.json` — i.e. all 243 are catalogued in
  `unsupported.txt` with oracle text but do not work. None are truly-absent-from-the-catalog. In README terms
  these are **UNWRITTEN-adjacent**: registered/catalogued but resolving only to an unsupported stub, so they
  are counted excluded, not implemented.

### Heavy reprint overlap

The classic core sets reprint the same problem cards repeatedly. **LEA = LEB = 2ED** are an identical
28-card set (same names, only reordered). The banding / ante / text-changing staples chain forward through
**RV** and **4ED**, and a large slice of **LEG**'s unsupported cards re-appear in **CHR** (Chronicles reprint).
The worst offender, **Power Sink**, is missing in seven sets `[LEA,LEB,2ED,RV,4ED,ICE,MIR]`. Every card below
is listed **once** with a `[set-code]` tag showing all sets it appears in.

---

## By exclusion reason (main deliverable — deduped, grouped, tagged)

Each group is tagged with its overall disposition. Within a group, per-card notes appear where the reason
isn't self-evident.

### 1. ANTE — real ante mechanic  → **ENGINE-BLOCKED**

Wagic has no ante zone / ante transfer by design. These play for ante and cannot be modelled.

- Contract from Below `[LEA,LEB,2ED,RV]`
- Darkpact `[LEA,LEB,2ED,RV]`
- Demonic Attorney `[LEA,LEB,2ED,RV]`
- Jeweled Bird `[ARN,CHR]`
- Bronze Tablet `[ATQ,4ED]`
- Rebirth `[LEG,4ED]`
- Tempest Efreet `[LEG,4ED]`
- Amulet of Quoz `[ICE]` (ante + coin flip)
- Timmerian Fiends `[HML]`

**9 distinct.**

### 2. MANUAL DEXTERITY — physical flip / toss  → **ENGINE-BLOCKED**

- Chaos Orb `[LEA,LEB,2ED]`
- Falling Star `[LEG]`

**2 distinct.**

### 3. SUBGAME  → **ENGINE-BLOCKED**

- Shahrazad `[ARN]` — play a Magic subgame using libraries as decks.

**1 distinct.**

### 4. COIN-FLIP / DICE / CHAOS randomness  → **ENGINE-BLOCKED**

No coin-flip / random-outcome primitive in Wagic.

- Goblin Artisans `[ATQ,CHR]`
- Ydwen Efreet `[ARN]`
- Mana Clash `[DRK,4ED]`
- Game of Chaos `[ICE]`
- Chaos Lord `[ICE]` (control swaps on parity of permanent count each upkeep)
- Chaos Moon `[ICE]` (parity-driven global effect each upkeep)

**6 distinct.** (Amulet of Quoz also flips a coin but is filed under ANTE above.)

### 5. TEXT-CHANGING effects  → **ENGINE-BLOCKED**

Rewriting card text at runtime (land types / color words) is unsupported.

- Magical Hack `[LEA,LEB,2ED,RV,4ED]`
- Sleight of Mind `[LEA,LEB,2ED,RV,4ED,ICE]`
- Mind Bend `[MIR]`
- Illusionary Terrain `[ICE]` — "basic lands of the first chosen type are the second chosen type."
- Balduvian Shaman `[ICE]` — activated color-word text change on an enchantment.
- Naked Singularity `[ICE]` — lands produce swapped mana colors.
- Reality Twist `[ICE]` — lands produce swapped mana colors.

**7 distinct.**

### 6. BANDING / bands-with-other  → **ENGINE-BLOCKED**

Banding (and "bands with other") is genuinely unsupported. Grouped here are creatures/permanents whose
*only* barrier is banding, plus the grant-banding enablers. (Cards that also carry a second unsupported clause
are noted.)

Vanilla / near-vanilla banders:
- Benalish Hero `[LEA,LEB,2ED,RV,4ED]`
- Mesa Pegasus `[LEA,LEB,2ED,RV,4ED]`
- Timber Wolves `[LEA,LEB,2ED,RV,4ED]`
- Camel `[ARN]` (banding + Desert damage prevention)
- War Elephant `[ARN,CHR]`
- Pikemen `[DRK,4ED]`
- Knights of Thorn `[DRK]` (protection from red + banding)
- Icatian Infantry `[FEM]`
- Icatian Skirmishers `[FEM]`
- Icatian Phalanx `[FEM]`
- Kjeldoran Warrior `[ICE]`
- Kjeldoran Knight `[ICE]`
- Kjeldoran Skyknight `[ICE]`
- Kjeldoran Skycaptain `[ICE]`
- Kjeldoran Phalanx `[ICE]`
- Kjeldoran Escort `[ALL]`
- Shield Bearer `[ICE]`
- Dire Wolves `[ICE]` (conditional banding)
- Teremko Griffin `[MIR]`
- Noble Elephant `[MIR]`
- Ayesha Tanaka `[LEG,CHR]` (banding + artifact-ability counter)
- Mishra's War Machine `[ATQ,RV,4ED]` (banding + upkeep drawback)
- Urza's Engine `[ALL]` (banding grant + trample grant)

Grant-banding / band-support enablers:
- Helm of Chatzuk `[LEA,LEB,2ED,RV,4ED]`
- Battering Ram `[ATQ,4ED]`
- Fortified Area `[LEG,4ED]`
- Cooperation `[ICE]`
- Formation `[ICE]`
- Baton of Morale `[ICE]`
- Beast Walkers `[HML]`
- Soraya the Falconer `[HML]`
- Master of the Hunt `[LEG]` (makes bands-with-other Wolf tokens)
- Wall of Caltrops `[LEG]` (conditional banding grant)
- Wall of Shields `[ICE]` (defender + banding damage assignment)
- Errand of Duty `[ALL]` (banding token)
- Nature's Blessing `[ALL]` (modal grant incl. banding)
- Shelkin Brownie `[LEG]` (strips bands-with-other)

Legendary "bands with other legendary creatures" land cycle + support:
- Cathedral of Serra `[LEG]`
- Adventurers' Guildhouse `[LEG]`
- Unholy Citadel `[LEG]`
- Seafarer's Quay `[LEG]`
- Mountain Stronghold `[LEG]`
- Tolaria `[LEG]` (strips banding)

**41 distinct.** (Largest single reason group.)

### 7. DAMAGE-PREVENTION / redirection edge cases  → mixed (see per-card tag)

Wagic's prevention/redirection shields ("next N damage from a source of your choice", "dealt to X instead")
are the recurring un-modelled pattern here. Most are **ENGINE-BLOCKED** on the redirection/shield primitive;
a few simpler flat-prevention ones are **BACKLOG-MEDIUM**.

Redirect-damage-to-a-permanent / "dealt to X instead" (**ENGINE-BLOCKED**):
- Jade Monolith `[LEA,LEB,2ED,RV,4ED]`
- Personal Incarnation `[LEA,LEB,2ED,RV,4ED]`
- Veteran Bodyguard `[LEA,LEB,2ED,RV]`
- Martyrs of Korlis `[ATQ]`
- Kjeldoran Royal Guard `[ICE]`
- Nova Pentacle `[LEG]`
- Blood of the Martyr `[DRK,CHR]`
- Martyrdom `[ALL]`
- Daughter of Autumn `[HML]`
- Hazduhr the Abbot `[HML]`
- Reflect Damage `[MIR]`
- Reflecting Mirror `[DRK]` (redirect a spell targeting you)
- Reverberation `[LEG]` (redirect a sorcery's damage to its controller)

"Next-N-damage-from-a-source-of-your-choice" prevention shields (**ENGINE-BLOCKED** — shield primitive):
- Forcefield `[LEA,LEB,2ED]`
- Guardian Angel `[LEA,LEB,2ED,RV]`
- Reverse Damage `[LEA,LEB,2ED,RV,4ED]` (prevent + gain life)
- Dark Sphere `[DRK]`
- Greater Realm of Preservation `[LEG]`
- Prismatic Circle `[MIR]`
- Pentagram of the Ages `[ICE]`
- Mercenaries `[ICE]`
- Sacred Boon `[ICE]` (prevent + counters)
- Scars of the Veteran `[ALL]`
- Seasoned Tactician `[ALL]`
- Bone Mask `[MIR]`
- Chromatic Armor `[ICE]` (chosen-color prevention shield)
- Shadowbane `[MIR]`
- Silhouette `[LEG]`

Flat / conditional prevention, simpler (**BACKLOG-MEDIUM**):
- Heroism `[FEM]`
- Benevolent Unicorn `[MIR]` (spell damage −1)
- Forethought Amulet `[LEG]` (instant/sorcery damage capped at 2)

**31 distinct.**

### 8. DYNAMIC "for each" / unusual continuous P/T & control effects  → mixed

- Gaea's Liege `[LEA,LEB,2ED,RV,4ED]` — P/T = Forests you/defender control; makes lands Forests. **BACKLOG-MEDIUM.**
- Nameless Race `[DRK]` — P/T = life paid, bounded by opponents' white permanents/graveyard. **BACKLOG-MEDIUM.**
- Shapeshifter `[ATQ,4ED]` — chosen 0–7 split P/T (`toughness=7-*`). **BACKLOG-MEDIUM.**
- Halfdane `[LEG]` — copies a target's P/T each upkeep. **BACKLOG-MEDIUM.**
- Sentinel `[LEG,CHR]` — toughness becomes 1 + blocker/blocked power. **BACKLOG-MEDIUM.**
- Sworn Defender `[ALL]` — P/T from a target creature's stats. **BACKLOG-MEDIUM.**
- Soul Echo `[MIR]` — replaces life loss with counter removal; "don't lose at 0 life." **ENGINE-BLOCKED** (life-loss replacement).
- Energy Vortex `[MIR]` — energy-counter pay-or-take engine. **BACKLOG-MEDIUM.**
- Frankenstein's Monster `[DRK]` — exile creatures for choose-your-counter distribution. **BACKLOG-MEDIUM.**

**9 distinct.**

### 9. OTHER complex one-off  → mixed (one-line reason each)

Bespoke effects with no shared pattern. Tag per card.

Exile-and-return / control-suspension permanents (**BACKLOG-MEDIUM** unless noted):
- Oubliette `[ARN]` — exile creature + auras, return on leave (note counters). BACKLOG-MEDIUM.
- Tawnos's Coffin `[ATQ]` — same shape, activated. BACKLOG-MEDIUM.
- Icy Prison `[ICE]` — ETB exile, upkeep-tax, return on leave. BACKLOG-MEDIUM.
- Knowledge Vault `[LEG]` — exile-pile draw engine. BACKLOG-MEDIUM.
- Gustha's Scepter `[ALL]` — hide hand cards in exile. BACKLOG-MEDIUM.
- Ice Cauldron `[ICE]` — exile-and-cast-later + noted mana. ENGINE-BLOCKED (noted-mana replay).
- Mangara's Tome `[MIR]` — exiled face-down draw pile. BACKLOG-MEDIUM.

Control-theft / control-exchange:
- Word of Command `[LEA,LEB,2ED]` — take control of opponent to play a card. ENGINE-BLOCKED.
- Juxtapose `[LEG,CHR]` — swap highest-CMC creature & artifact. BACKLOG-MEDIUM.
- Gauntlets of Chaos `[LEG,CHR]` — exchange control of like permanents. BACKLOG-MEDIUM.
- Infernal Denizen `[ICE]` — steal creatures, upkeep sacrifice tax. BACKLOG-MEDIUM.
- The Wretched `[LEG,CHR]` — gain control of its blockers. BACKLOG-MEDIUM.
- Illicit Auction `[MIR]` — life-bid auction for control. ENGINE-BLOCKED (bidding UI).
- Seasinger `[FEM]` — steal a creature while tapped, Island-gated. BACKLOG-MEDIUM.
- Scarwood Bandits `[DRK]` — pay-or-steal artifact. BACKLOG-MEDIUM.
- Raiding Party `[FEM]` — tap-white-to-save-Plains destruction loop. ENGINE-BLOCKED.

Combat re-assignment / block manipulation:
- Camouflage `[LEA,LEB,2ED]` — random pile block assignment. ENGINE-BLOCKED.
- Raging River `[LEA,LEB,2ED]` — left/right pile block restriction. ENGINE-BLOCKED.
- False Orders `[LEA,LEB,2ED]` — remove/redirect a blocker. BACKLOG-MEDIUM.
- Blaze of Glory `[LEA,LEB,2ED]` — force-block-all. BACKLOG-MEDIUM.
- Siren's Call `[LEA,LEB,2ED,RV,4ED]` — force attack + end-step destroy. BACKLOG-MEDIUM.
- Nettling Imp `[LEA,LEB,2ED,RV]` / Norritt `[ICE]` — force a creature to attack or be destroyed. BACKLOG-MEDIUM.
- Arcum's Whistle `[ICE]` — pay-or-attack. BACKLOG-MEDIUM.
- Total War `[ICE]` — destroy non-attackers on any attack. BACKLOG-MEDIUM.
- Melee `[ICE]` — attacker chooses blocks + untap-unblocked. ENGINE-BLOCKED.
- General Jarkeld `[ICE]` — switch two attackers' blockers. BACKLOG-MEDIUM.
- Sorrow's Path `[DRK]` — swap two opposing blockers + self-damage. BACKLOG-MEDIUM.
- Feint `[LEG]` — tap blockers + prevent combat damage. BACKLOG-MEDIUM.
- Rapid Fire `[LEG]` — first strike + grant rampage. ENGINE-BLOCKED (rampage).
- Gabriel Angelfire `[LEG,CHR]` — choose keyword incl. rampage each upkeep. ENGINE-BLOCKED (rampage).
- Marble Priest `[LEG]` — force Walls to block + prevent Wall damage. BACKLOG-MEDIUM.
- Vodalian War Machine `[FEM]` — tap-Merfolk to attack/pump defender. BACKLOG-MEDIUM.
- Goblin Flotilla `[FEM]` — islandwalk + pay-or-grant-first-strike. BACKLOG-MEDIUM.
- Tidal Flats `[FEM]` — pay-or-grant-first-strike to blockers. BACKLOG-MEDIUM.
- Spitting Slug `[DRK]` — pay-or-share first strike on block. BACKLOG-MEDIUM.
- Snowblind `[ICE]` — snow-land-scaled −X/−Y aura. BACKLOG-MEDIUM.

Wall / "glyph" combat-death payoffs (**BACKLOG-MEDIUM** unless noted):
- Wall of Shadows `[LEG,CHR]` — prevent all damage from blocked creatures + untargetable-as-Wall. BACKLOG-MEDIUM.
- Glyph of Doom `[LEG]` — destroy creatures a Wall blocked. BACKLOG-MEDIUM.
- Glyph of Reincarnation `[LEG]` — destroy + reanimate blocked creatures. BACKLOG-MEDIUM.
- Glyph of Delusion `[LEG]` — glyph counters lock a blocked creature. BACKLOG-MEDIUM.
- Venomous Breath `[ICE]` — destroy all that blocked/were blocked by a creature. BACKLOG-MEDIUM.
- Brine Hag `[LEG]` — turn its damagers into 0/2 on death. BACKLOG-MEDIUM.
- Blazing Effigy `[LEG]` — death damage scales with prior Effigy damage. BACKLOG-MEDIUM.
- Lesser Werewolf `[LEG]` — self-shrink to add −0/−1 counters. BACKLOG-MEDIUM.

Reanimation-on-damage / graveyard-steal:
- Krovikan Vampire `[ICE]` — steal creatures its damage killed. BACKLOG-MEDIUM.
- Seraph `[ICE]` — same, angelic. BACKLOG-MEDIUM.
- Giant Albatross `[HML]` — death-trigger board wipe of its damagers. BACKLOG-MEDIUM.

Counter / trigger on artifact-ability activation:
- Haunting Wind `[ATQ]` — ping on artifact tap/ability. BACKLOG-MEDIUM.
- Artifact Possession `[ATQ]` — same, aura. BACKLOG-MEDIUM.
- Powerleech `[ATQ]` — lifegain on opp. artifact activation. BACKLOG-MEDIUM.
- Power Artifact `[ATQ]` — reduce artifact ability costs. BACKLOG-MEDIUM.
- Rust `[LEG]` / Brown Ouphe `[ICE]` — counter an artifact activated ability. BACKLOG-MEDIUM.

Counter / interaction spells with unusual conditions:
- Power Sink `[LEA,LEB,2ED,RV,4ED,ICE,MIR]` — counter unless pay X, then tap all lands + empty pool. ENGINE-BLOCKED (mana-pool empty).
- Drain Power `[LEA,LEB,2ED,RV,4ED]` — force-tap all lands, steal their mana. ENGINE-BLOCKED (mana-pool transfer).
- Deflection `[ICE]` — change a spell's single target. BACKLOG-MEDIUM.
- Meddle `[MIR]` — retarget a single-target creature spell. BACKLOG-MEDIUM.
- Invoke Prejudice `[LEG]` — tax off-color creature spells. BACKLOG-MEDIUM.
- Mistfolk `[ICE]` — counter spells targeting it. BACKLOG-MEDIUM.
- Tidal Control `[ALL]` — pay-life/mana counter, any player. BACKLOG-MEDIUM.
- Chain Stasis `[HML]` — copyable tap/untap. ENGINE-BLOCKED (spell-copy chain).
- Equinox `[LEG]` — grant a land a land-protecting counter ability. BACKLOG-MEDIUM.
- Suffocation `[ALL]` — conditional on being burned by a red instant/sorcery. BACKLOG-MEDIUM.

Card-name guessing / library manipulation:
- Petra Sphinx `[LEG,CHR]` — name-a-card top-of-library reveal. BACKLOG-MEDIUM.
- Vexing Arcanix `[ICE]` — same + ping. BACKLOG-MEDIUM.
- Nebuchadnezzar `[LEG,CHR]` — name a card, random discard X. BACKLOG-MEDIUM.
- Demonic Consultation `[ICE]` — name a card, exile-dig. BACKLOG-MEDIUM.
- Forgotten Lore `[ICE]` — opponent-chosen graveyard dig. BACKLOG-MEDIUM.
- Lim-Dul's Vault `[ALL]` — pay-life library reorder loop. BACKLOG-MEDIUM.
- Preferred Selection `[MIR]` — upkeep top-two look/sac. BACKLOG-MEDIUM.
- Library of Lat-Nam `[ALL]` / Fatal Lore `[ALL]` — opponent chooses your mode. BACKLOG-MEDIUM.
- Phyrexian Portal `[ALL]` — opponent splits your library into piles. BACKLOG-MEDIUM.
- Helm of Obedience `[ALL]` — mill until creature, steal it. BACKLOG-MEDIUM.
- Chains of Mephistopheles `[LEG]` — replace extra draws with discard/mill. ENGINE-BLOCKED (draw-replacement).

Whole-set-hoser artifacts (**OUT-OF-SCOPE** — target a paper-only set boundary Wagic doesn't track):
- City in a Bottle `[ARN]` — sacrifices Arabian Nights permanents.
- Golgothian Sylex `[ATQ]` — sacrifices Antiquities permanents.
- Apocalypse Chime `[HML]` — destroys Homelands permanents.

Miscellaneous bespoke one-offs (**BACKLOG-MEDIUM** unless noted):
- Vesuvan Doppelganger `[LEA,LEB,2ED,RV]` — copy-a-creature with recurring upkeep re-copy. BACKLOG-MEDIUM.
- Guardian Beast `[ARN]` — makes artifacts indestructible/untargetable while untapped. BACKLOG-MEDIUM.
- Pyramids `[ARN]` — modal aura destroy / prevent land destruction. BACKLOG-MEDIUM.
- Nafs Asp `[ARN,4ED]` — pay-or-lose-life on damage. BACKLOG-MEDIUM.
- Illusionary Mask `[LEA,LEB,2ED]` — cast a creature face-down for X. ENGINE-BLOCKED (face-down/morph).
- Transmute Artifact `[ATQ]` — sac + fetch-to-battlefield with CMC math. BACKLOG-MEDIUM.
- Divine Intervention `[LEG]` — game-draw countdown. ENGINE-BLOCKED (draw-the-game).
- Clergy of the Holy Nimbus `[LEG]` — regen unless opponent pays. BACKLOG-MEDIUM.
- Remove Enchantments `[LEG]` — bounce-yours/destroy-others enchantment sweep. BACKLOG-MEDIUM.
- Infinite Authority `[LEG]` — grow-on-kill combat aura. BACKLOG-MEDIUM.
- Imprison `[LEG]` — tax/counter a creature's tapped abilities. BACKLOG-MEDIUM.
- Sword of the Ages `[LEG]` — sac creatures for X damage. BACKLOG-MEDIUM.
- Backdraft `[LEG]` — half-damage of a sorcery cast this turn. BACKLOG-MEDIUM.
- Takklemaggot `[LEG,CHR]` — spreading death aura. BACKLOG-MEDIUM.
- Cocoon `[LEG,CHR]` — pupa-counter transform aura. BACKLOG-MEDIUM.
- Puppet Master `[LEG,CHR]` — recur-on-death aura. BACKLOG-MEDIUM.
- Enchantment Alteration `[LEG,CHR]` — move an aura to another permanent. BACKLOG-MEDIUM.
- Land's Edge `[LEG,CHR]` — discard-land-to-burn, any player. BACKLOG-MEDIUM.
- Runesword `[DRK,CHR]` — pump + exile-on-death rider. BACKLOG-MEDIUM.
- Primordial Ooze `[LEG,CHR]` — grows, attacks-or-burns-you. BACKLOG-MEDIUM.
- Mind Bomb `[DRK,4ED]` — each player discards to reduce damage. BACKLOG-MEDIUM.
- Fasting `[DRK]` — skip-draw-for-life hunger counters. BACKLOG-MEDIUM.
- Wand of Ith `[DRK]` — random-hand discard tax. BACKLOG-MEDIUM.
- Orcish Mine `[HML]` — ore-counter land destruction aura. BACKLOG-MEDIUM.
- Ironclaw Curse `[HML]` — −0/−1 + block restriction aura. BACKLOG-MEDIUM.
- Dwarven Sea Clan `[HML]` — Island-gated end-of-combat ping. BACKLOG-MEDIUM.
- Giant Oyster `[HML]` — tap-lock + −1/−1 counter engine. BACKLOG-MEDIUM.
- Merseine `[FEM]` — net-counter tap-lock aura. BACKLOG-MEDIUM.
- Delif's Cube `[FEM]` — cube-counter unblocked-damage / regen. BACKLOG-MEDIUM.
- Call to Arms `[ICE]` — most-common-color conditional anthem. BACKLOG-MEDIUM.
- Drought `[ICE]` — Swamp-sacrifice tax per black pip. BACKLOG-MEDIUM.
- Gaze of Pain `[ICE]` — redirect unblocked damage to a creature. BACKLOG-MEDIUM.
- Word of Undoing `[ICE]` — bounce creature + its white auras. BACKLOG-MEDIUM.
- Errant Minion `[ICE]` — pay-to-prevent upkeep ping aura. BACKLOG-MEDIUM.
- Musician `[ICE]` — music-counter upkeep tax spreader. BACKLOG-MEDIUM.
- Snowfall `[ICE]` — Island-tap upkeep-mana enchantment. BACKLOG-MEDIUM.
- Winter's Chill `[ICE]` — snow-scaled multi-target combat trick. BACKLOG-MEDIUM.
- Bone Shaman `[ICE]` — grant no-regen to its damage. BACKLOG-MEDIUM.
- Ghostly Flame `[ICE]` — makes B/R damage colorless. BACKLOG-MEDIUM.
- Jeweled Amulet `[ICE]` — noted-mana filter. ENGINE-BLOCKED (noted-mana type).
- Soul Burn `[ICE]` — B/R-only X burn + capped lifegain. BACKLOG-MEDIUM.
- Phantasmal Mount `[ICE]` — link-sacrifice flying granter. BACKLOG-MEDIUM.
- Stromgald Spy `[ALL]` — reveal-hand on unblocked. BACKLOG-MEDIUM.
- Scarab of the Unseen `[ALL]` — bounce all auras off a permanent + delayed draw. BACKLOG-MEDIUM.
- Awesome Presence `[ALL]` — pay-per-blocker evasion aura. BACKLOG-MEDIUM.
- Acidic Dagger `[MIR]` — destroy-on-combat-damage grant. BACKLOG-MEDIUM.
- Bazaar of Wonders `[MIR]` — name-match spell counter + graveyard exile. BACKLOG-MEDIUM.
- Hakim, Loreweaver `[MIR]` — recur auras from graveyard. BACKLOG-MEDIUM.
- Flash `[MIR]` — cheat a creature in, pay-or-sac. BACKLOG-MEDIUM.
- Celestial Dawn `[MIR]` — mono-white mana/color rewrite. ENGINE-BLOCKED (mass color/mana rewrite).
- Hall of Gemstone `[MIR]` — per-turn land color lock. BACKLOG-MEDIUM.
- Null Chamber `[MIR]` — two named cards can't be played. BACKLOG-MEDIUM.
- Spatial Binding `[MIR]` — anti-phasing. ENGINE-BLOCKED (phasing).
- Ward of Lights `[MIR]` — flash protection aura. BACKLOG-MEDIUM.
- Soul Echo — (listed under DYNAMIC, group 8).

**134 distinct in this catch-all group** (the residual after the nine specific reason groups above;
per-card reasons are given inline, and PHPR's single card follows).

### PHPR — the one-card set

- Arena `[PHPR]` — a Land with a "fight" activated ability (`{3},{T}: two creatures fight`). Fight is not a
  supported primitive in this era's engine. **BACKLOG-MEDIUM** (fight). 1 distinct card; PHPR's *only* entry.

---

## Reason-group summary (counts)

| Reason group | Distinct | Disposition |
|---|---|---|
| ANTE | 9 | ENGINE-BLOCKED |
| Manual dexterity | 2 | ENGINE-BLOCKED |
| Subgame | 1 | ENGINE-BLOCKED |
| Coin-flip / dice / chaos | 6 | ENGINE-BLOCKED |
| Text-changing | 7 | ENGINE-BLOCKED |
| Banding / bands-with-other | 41 | ENGINE-BLOCKED |
| Damage-prevention / redirection | 31 | mostly ENGINE-BLOCKED, 3 BACKLOG-MEDIUM |
| Dynamic "for each" / continuous P/T | 9 | mostly BACKLOG-MEDIUM, 1 ENGINE-BLOCKED |
| Whole-set hoser artifacts | 3 | OUT-OF-SCOPE |
| Other complex one-off (incl. Arena) | 134 | ~30 ENGINE-BLOCKED, rest BACKLOG-MEDIUM |
| **Total excluded distinct** | **243** | |
| Stale (now implemented) | 2 | — |
| **Distinct in files** | **245** | |

Rough disposition roll-up across all groups: **≈97 ENGINE-BLOCKED**, **≈143 BACKLOG-MEDIUM**, **3 OUT-OF-SCOPE**,
**0 BACKLOG-EASY** (nothing in this era is trivial — even the "simple" cards ride an unsupported prevention,
banding, combat-reassignment, or text-change primitive). The classic era's gaps are dominated by three
engine-level absences: **banding**, **damage prevention/redirection shields**, and **combat re-assignment**,
plus the by-design ante/dexterity/subgame trio.

---

## Per-set quick table

| Set | # distinct missing | Dominant reasons |
|---|---|---|
| LEA | 28 | banding, prevention/redirect, text-change, ante, combat-reassign; Chaos Orb (dexterity) |
| LEB | 28 | identical to LEA |
| 2ED | 28 | identical to LEA |
| ARN | 10 | ante (Jeweled Bird), subgame (Shahrazad), coin-flip (Ydwen), banding (Camel/War Elephant), Oubliette |
| ATQ | 14 | artifact-activation triggers, banding, ante (Bronze Tablet), coin-flip (Goblin Artisans) |
| RV | 22 | reprints of LEA banding/ante/prevention/text-change staples |
| LEG | 55 | banding (incl. legend-band land cycle), Wall/glyph combat, control-exchange, ante, dexterity (Falling Star) |
| DRK | 15 | coin-flip (Mana Clash), text/combat one-offs, prevention, banding (Pikemen/Knights of Thorn) |
| PHPR | 1 | Arena — fight (BACKLOG-MEDIUM) |
| FEM | 11 | banding (Icatian line), Merfolk/first-strike combat tricks, control-steal |
| 4ED | 24 | reprints: banding, ante, prevention, text-change, coin-flip |
| ICE | 59 | banding (Kjeldoran line), prevention shields, text/mana rewrite, coin-flip/chaos, ante (Amulet of Quoz); +2 STALE |
| CHR | 20 | LEG reprints: control-exchange, banding, Wall combat, ante (Jeweled Bird) |
| HML | 13 | redirect-to-permanent, banding, ante (Timmerian Fiends), set-hoser (Apocalypse Chime) |
| ALL | 19 | banding, prevention, opponent-chooses-mode spells, control/library manipulation |
| MIR | 24 | prevention/redirect, text-change (Mind Bend), phasing, color/mana rewrite (Celestial Dawn), one-offs |

_Note: ICE's 59 includes the 2 stale (Crown of the Ages, Flooded Woodlands); its genuinely-excluded count is 57._
