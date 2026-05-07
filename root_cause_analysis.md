# Wagic — Unsupported / Borderline Root Cause Analysis

Cards grouped by the **engine limitation** that blocks them, not by set or mechanic name.
Goal: estimate the value (cards unlocked) of fixing any given root cause.

---

## U3 — Unsupported cards that have auto= fields (57 total)

These are the cards in `unsupported.txt` that have some implementation attempt.
Two have already been promoted to `new_sets.txt`: Gimbal, Gremlin Prodigy ✅ / Slippery Bogbonder ✅

---

### Group A — Planechase format (23 cards)
Plane cards from the Planechase game format. Require a dice-rolling subsystem,
shared planar deck, "when you planeswalk to X" triggers, and "chaos ensues" events.
No individual card fix helps — the whole format subsystem would need building.

Cards: Enigma Ridges, Esper, Ghirapur, Inys Haen, Ketria, Littjara,
Megaflora Jungle, Naktamun, New Argive, Norn's Seedcore, Nyx, Riptide Island,
Strixhaven, Ten Wizards Mountain, The Caldaia, The Fertile Lands of Saulvinia,
The Golden City of Orazca, The Great Aerie, The Pit, The Western Cloud,
The Wilds, Unyaro, Valor's Reach

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Very Hard — new game format | 23 here + more from other files |

---

### Group B — No valid primitives (English text in auto=) (4 cards)
auto= contains English sentences, not Wagic syntax. Completely non-functional.
Even if the mechanics were supported, each card needs individual implementation.

| Card | Mechanic needed |
|------|----------------|
| Begin the Invasion | Battle card tutor (Battle type not in Wagic) |
| Blight Titan | Incubate (Phyrexian Incubator token that transforms) |
| Dance with Calamity | Free-cast from exile, total MV ≤ 13 |
| Rashmi and Ragavan | Cast from opponent top card if MV < artifacts you control |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard each — all unique mechanics | Very Low individually |

---

### Group C — Copy spell / ability (3 cards)
No `copy(ability)` or `copy(spell)` primitive exists.

| Card | What it copies |
|------|---------------|
| Aboleth Spawn | Triggered ability of creature entering opponent's battlefield |
| Weaver of Harmony | Activated or triggered ability from enchantment source |
| Rowan's Talent | Loyalty ability of enchanted planeswalker |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard — new primitive | 3 here + Fire Lord Azula (TLA) + Peter Parker's Camera (SPM) = **5 new-set cards** |

---

### Group D — Planeswalker / PW auras (4 cards)
Loyalty abilities can't be modified or triggered off.
PW auras granting loyalty abilities, or reacting to loyalty activations, are engine-blocked.

| Card | Blocker |
|------|---------|
| Dungeon Master | Planeswalker with d20 roll mechanics and complex loyalty abilities |
| Elspeth's Talent | PW aura that grants a loyalty ability to enchanted planeswalker |
| Teferi's Talent | PW aura that triggers whenever a loyalty ability activates |
| Rowan's Talent | PW aura + copy loyalty ability (also Group C) |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard — loyalty-ability hook needed | 4 here + other PW-modifier cards in borderline |

---

### Group E — Backup mechanic (3 cards)
Backup N = ETB puts N +1/+1 counters on target creature; if that's **another** creature,
it gains the listed abilities until EOT. The "if another creature" conditional
ability-grant is the blocker — ETB counter placement itself is fine.

| Card | Detail |
|------|--------|
| Bright-Palm, Soul Awakener | Backup 1 + attack trigger doubles counters on target |
| Conclave Sledge-Captain | Backup 1×3 (three separate triggers) + combat damage counter |
| Emergent Woodwurm | Backup 3 + attack trigger: look at top-X, put permanent onto battlefield |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Medium — ETB counter OK; conditional ability grant needs primitiving | 3 here + B2/B3 borderline cards |

---

### Group F — Convoke grant (3 cards)
"The next spell you cast this turn has convoke" — no primitive for granting
convoke to a future spell.

| Card | Detail |
|------|--------|
| Flockchaser Phantom | Attack trigger: next spell has convoke |
| Wand of the Worldsoul | Activated ability: next spell has convoke |
| Kasla, the Broken Halo | Trigger when you cast a convoke spell: scry 2 + draw |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard | 3 here + Saint Traft and Rem Karolus (partial) |

---

### Group G — Counter operations: move / double (3 cards)
Moving a counter from one permanent to another, or placing one extra counter
as a replacement effect.

| Card | Blocker |
|------|---------|
| Nesting Grounds | `{1}{T}`: Move a counter from one permanent you control to another |
| Dismantle | Destroy artifact; if it had counters, put that many onto another artifact |
| Pir, Imaginative Rascal | Replacement: if counters placed on permanent, place one extra of each type |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard for Pir (replacement); Medium for Nesting Grounds/Dismantle if `movecounter` added | 3 here + borderline counter-manipulation cards |

---

### Group H — Damage prevention / redirection (2 cards)
`prevent:X` exists but redirecting prevented damage to a specific permanent does not.

| Card | Detail |
|------|--------|
| Beacon of Destiny | Tap: next damage source you choose deals its damage to Beacon instead |
| Cho-Arrim Alchemist | Discard: prevent next damage to you; gain life equal to prevented amount |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard — needs `redirect(damage)` primitive | 2 here + other damage-redirect cards in borderline |

---

### Group I — Phase / combat manipulation (2 cards)

| Card | Blocker |
|------|---------|
| Mandate of Peace | End the combat phase mid-combat + opponents can't cast spells this turn |
| Portal Mage | ETB during declare-attackers: redirect which player/planeswalker a creature attacks |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard each — different engine hooks | 2 here, limited broader unlock |

---

### Group J — Sequential conditional triggers (1 card)

| Card | Blocker |
|------|---------|
| Saint Traft and Rem Karolus | "1st tap → Human; 2nd tap → Spirit; 3rd tap → Angel" + convoke untap trigger |

No primitive for tracking "Nth time this ability has resolved this turn".

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard | 1 card |

---

### Group K — Bolster mechanic (1 card)

| Card | Blocker |
|------|---------|
| Sandsteppe War Riders | Bolster X at combat begin (put X counters on your creature with least toughness) |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Medium if `bolster(X)` primitive added | 1 here + several in borderline |

---

### Group L — Damage doubling (1 card)

| Card | Blocker |
|------|---------|
| Uncivil Unrest | Creatures with +1/+1 counters deal double damage (replacement effect on output) |

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard — replacement effect on damage dealt | 1 here + Doubling Season equivalents in borderline |

---

### Group M — Goad mechanic (1 card)

| Card | Blocker |
|------|---------|
| Bloodthirsty Blade | Equipped creature must attack AND must attack a player other than you |

`mustattack` exists; "must attack player other than controller" does not.

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Medium | 1 here + other goaded cards in borderline |

---

### Group N — Token with embedded triggered ability (1 card)

| Card | Blocker |
|------|---------|
| Wildfire Awakener | Creates X tokens with "Whenever this creature becomes tapped, deal 1 damage to target player" |

Token definition syntax has no slot for triggered abilities.

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard | 1 card |

---

### Group O — Art-based mechanic (1 card)

| Card | Blocker |
|------|---------|
| Garbage Elemental (e) | "Art menace" — unblockable except by creatures with 2+ visible figures in art |

Depends on card artwork metadata. Not implementable in any practical sense.

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Impossible | 0 |

---

### Group P — Conditional graveyard return, power comparison (1 card)

| Card | Blocker |
|------|---------|
| Vulpine Harvester | Return artifact from graveyard if MV ≤ total power of attacking Phyrexians you control |

Needs dynamic sum of a filtered creature set compared against a card property.

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard | 1 card |

---

### Group Q — Parley mechanic (1 card)

| Card | Blocker |
|------|---------|
| Cutthroat Negotiator | Parley: everyone reveals top card; Treasure per nonland; everyone draws |

Multi-player simultaneous reveal + conditional Treasure creation.

| Fix complexity | Cards unlocked if fixed |
|---------------|------------------------|
| Hard | 1 here + other Parley cards |

---

## Priority Summary — U3

| Group | Cards | Fix complexity | Unlock value |
|-------|-------|----------------|-------------|
| A — Planechase | 23 | Very Hard (new format) | High (23+) |
| C — Copy ability | 3 | Hard | Medium (3 + 5 new-set cards) |
| D — PW auras | 4 | Hard | Medium |
| E — Backup | 3 | Medium | Medium |
| F — Convoke grant | 3 | Hard | Low–Medium |
| G — Counter ops | 3 | Hard/Medium | Medium |
| H — Damage redirect | 2 | Hard | Low–Medium |
| K — Bolster | 1 | Medium | Low–Medium |
| M — Goad | 1 | Medium | Low |
| B — English text | 4 | Hard (unique each) | Very Low |
| I,J,L,N,P,Q — misc | 7 | Hard/Impossible | Very Low |
| O — Art mechanic | 1 | Impossible | 0 |

---

## Borderline — Root Cause Analysis

`borderline.txt`: **11,878 total cards**. Scanned by automated pattern matching
against all `auto=`/`autohand=`/`autoexile=`/`autograveyard=` lines, `text=` fields,
and structural features.

---

### Keyword support audit — what's actually in the engine

A full scan of `_macros.txt` revealed that many keywords flagged as "missing" are
**fully implemented** via macros. Cards using old/pre-macro patterns may work correctly
but could be simplified.

**Fully implemented in engine (macros exist and work):**
`goad` (_GOAD_), `amass` (_AMASSZOMBIE/ORC/SLIVER_), `crew` (_CREW1/2_),
`ring tempts` (_RINGTEMPTS_), `foretell` (_FORETELL_), `plot` (_PLOT_/_PLOTCAST_),
`initiative` (_INITIATIVE_), `manifest dread` (_MANIFEST_DREAD_), `explore` (_EXPLORES_),
`connive` (_CONNIVES_), `eternalize` (_ETERNALIZE_), `surveil` (_SURVEIL1/2/3_),
`mentor` (_MENTOR_), `enlist` (_ENLIST_), `training` (_TRAINING_), `adapt` (_ADAPT1/2/3/4_),
`enrage` (_ENRAGE_), `fabricate` (_FABRICATE_), `battalion` (_BATTALION_),
`proliferate` (_PROLIFERATE_), `populate` (_POPULATE_), `learn` (_LEARN_),
`suspect` (_SUSPECT_IT_), `afterlife` (_AFTERLIFETOKEN_), `adventure` (_ADVENTURE_),
`ascend` (_ASCEND_), `monarch` (_MONARCH_), `renown` (_RENOWN_), `scavenge` (_SCAVENGE_),
`ferocious` (_FEROCIOUS_), `threshold` (_THRESHOLD_), `extort` (_EXTORT_),
`heroic` (_HEROIC_), `explore` (_EXPLORES_), `ripple` (_RIPPLE_), `recover` (_RECOVER_)

**Prowess:** fully implemented. Correct pattern is `@movedTo(*[-creature]|mystack):1/1 ueot`
(no `all(this)` needed — confirmed against Stormwing Entity and others). All borderline
prowess cards verified to have this trigger; no fixes needed.

**Commented out in macros (engine stubs exist but unfinished):**
`echo` (_ECHO_ commented), `splice onto arcane` (_SPLICEARCANE_ commented),
`champion` (_CHAMPION_ commented), `metalcraft` (_METALCRAFT_ commented)

**Genuinely missing (no macro, no workaround):**
`partner/commander` (format), `gift`, `level up`, `suspend`, `bestow`,
`megamorph`, `prototype`, `affinity`, `cleave`, `overload`, `encore`, `ninjutsu`, `blitz`

---

### Cards using old patterns instead of macros

After checking all zone-auto fields (`autohand=`, `autoexile=`, etc.), the actual
upgrade candidates are smaller than first estimated. Most foretell/plot cards DO use
`autohand=_FORETELL_` / `autohand=_PLOT_` correctly. Most surveil cards use the old
`reveal:psurveiloffset...` pattern which is the same underlying implementation as the
`_SURVEIL_` macros — functionally equivalent.

Genuinely improvable cards (macro exists, card uses wrong/partial pattern):

| Mechanic | Cards to fix | Nature of fix |
|----------|-------------|---------------|
| **Goad** | 19 ✅ fixed Apr 30 2026 | Updated cleanup to `myupkeep`/`hascntgoaded`/`notrg`; added upkeep re-apply to 5 Impetus auras |
| **Prowess** | 0 ✅ already correct | All borderline prowess cards have working trigger; root cause was wrong |
| **Surveil** | ~16 | Manual `reveal:psurveiloffset` pattern instead of `_SURVEIL1_` (cosmetic only — identical behaviour) |

---

### Cross-cutting summary — combined totals (U3 + Borderline)

Root causes where a **single engine fix** unlocks the most cards across both files.

| Group | Root cause | U3 | Borderline | **Total** | Fix complexity |
|-------|-----------|-----|-----------|----------|----------------|
| C | Copy spell/ability | 3 | 169 | **172** | Hard |
| B4 | Incomplete choice implementation | 0 | 1,062 | **1,062** | Medium (per card) |
| B5 | Single auto= vs complex text | 0 | ~1,039 | **~1,039** | Medium (per card) |
| B3 | No auto= at all (non-functional) | 0 | 665 | **665** | Medium (per card) |
| B6 | Search/library partial | 0 | 316 | **316** | Medium (per card) |
| H | Damage prevention/redirect | 2 | 39 | **41** | Hard |
| G | Counter double (replacement) | 1 | 24 | **25** | Hard |
| E | Backup mechanic | 3 | 23 | **26** | Medium |
| L | Damage doubling | 1 | 18 | **19** | Hard |
| G | Counter move | 2 | 13 | **15** | Medium |
| M | Goad (partial impls) | 1 | ~10 | **~11** | Easy — macro exists |
| A | Planechase format | 23 | 0 | **23** | Very Hard |
| D | PW / PW auras | 4 | 2 | **6** | Hard |
| F | Convoke grant | 3 | 3 | **6** | Hard |
| K | Bolster | 1 | 0 | **1** | Medium |

**Notes on B3/B4/B5/B6:** These are card-by-card issues, not a single engine primitive gap.
Each card needs individual review. But the counts show the scale of what's non-functional.

**Revised view:** The keyword audit confirmed most mechanics ARE in the engine.
The copy-ability gap (172 cards) remains the single highest-value engine improvement.
After that, B3 (665 non-functional borderline cards) is the largest body of work —
card-by-card implementations grouped by mechanic type.

---

### B3 — No auto= field (665 borderline cards, completely non-functional)

Cards in borderline.txt with no `auto=` line at all. When borderline is enabled
these cards load but do nothing — they have stats and type but no abilities fire.

*Sample (first 20):*
Abomination of Llanowar, Adorned Pouncer, Adriana's Valor, Adult Gold Dragon,
Aegis Turtle, Ageless Guardian, Agent of Kotis, Agonasaur Rex, Akoum Warrior,
Alabaster Host Sanctifier, Alchemist's Assistant, Aloe Alchemist, Alpine Watchdog,
Ancient Brontodon, Angel Ang, Angel Dec, Angel of the God-Pharaoh, Angelic Observer,
Ankle Biter, Annoyed Altisaur … (645 more)

**Fix approach:** Implement each individually. Group by mechanic type
(lord effects, triggered draw, etb counters, etc.) for batch implementation.

---

### B4 — Incomplete choice implementation (1,062 borderline cards)

Cards that have `choice` in their auto= but where only one branch or a simplified
version fires. Text says "Choose one —" but only one option is wired up, or
the wrong branch is the default.

**Fix approach:** For each card, add separate `auto=choice name(X) effect` lines
for each branch. Known pattern — batch-fixable once identified.
Sample: Abiding Grace, Abrade, Abundant Harvest, Academic Dispute, Acererak the Archlich…

---

### B5 — Simplified triggers (cards with 1 auto= line but complex text, ~1,039)

Heuristic: has exactly one auto= line but text= is >200 chars (suggesting multiple
effects). Many of these are probably fine; some will have missing clauses.
Needs manual spot-check rather than bulk fix.

---

### B6 — Search/library partial implementation (316 borderline cards)

Cards whose text says "search your library" but the auto= doesn't use
a `Reveal:` pattern (or uses an approximate one that doesn't match all criteria).
Existing `Reveal:type:*:mylibrary...` patterns cover many cases; each needs review.

---

### Group C — Copy spell/ability (169 borderline cards)

Same engine blocker as U3 Group C. No `copy(ability)` or `copy(spell)` primitive.

**Combined total if fixed: 172 cards** (169 borderline + 3 unsupported)
Plus 5 new-set cards (Fire Lord Azula, Peter Parker's Camera, Aboleth Spawn,
Weaver of Harmony, Rowan's Talent).

Sample: Absorb Identity, Archmage of Echoes, Artificer Class, Artisan of Forms,
Assemble from Parts, Awaken the Maelstrom, Barroom Brawl, Blade of Shared Souls,
Brenard Ginger Sculptor, Brudiclad Telchor Engineer… (139 more)

---

### Group M — Goad mechanic (44 borderline cards)

`mustattack` exists but "must attack a player other than you" direction is missing.

**Combined total if fixed: 45 cards**

Sample: Agitator Ant, Alela Cunning Conqueror, Baeloth Barrityl Entertainer,
Besmirch, Bhaal Lord of Murder, Bloodboil Sorcerer, Bothersome Quasit,
Coronation of Chaos, Coveted Peacock, Death Kiss, Disrupt Decorum…

---

### Group H — Damage prevention/redirect (39 borderline cards)

`prevent:X` exists but targeted damage prevention (prevent next N damage from source X,
or redirect to specific permanent) does not.

**Combined total if fixed: 41 cards**

Sample: Abuna's Chant, Alms, Angel of Salvation, Barbed Wire, Battletide Alchemist,
Benalish Missionary, Captain's Maneuver, Circle of Despair, Circle of Protection: Artifacts…

---

### Group G — Counter double (24 borderline cards)

Replacement effect: "if one or more counters would be placed on a permanent,
place that many plus one instead." No `replacecounters` or doubling-season primitive.

**Combined total if fixed: ~25 cards**

---

### Group E — Backup mechanic (23 borderline cards)

Same blocker as U3 Group E. ETB counter placement is fine;
"if that's another creature, it gains abilities until EOT" conditional is not.

**Combined total if fixed: 26 cards**

Full list: Archpriest of Shadows, Backup Agent, Bola Slinger, Boon-Bringer Valkyrie,
Chomping Kavu, Consuming Aetherborn, Cragsmasher Yeti, Death-Greeter's Champion,
Doomskar Warrior, Enduring Bondwarden, Fearless Skald, Gloomfang Mauler,
Golden-Scale Aeronaut, Guardian Scalelord, Hangar Scrounger, Mirror-Style Master,
Redcap Heelslasher, Saiba Cryptomancer, Scorn-Blade Berserker, Serpent-Blade Assailant,
Sigiled Sentinel, Streetwise Negotiator, Voldaren Thrillseeker

---

### Group L — Damage doubling (18 borderline cards)

Replacement: "if a creature would deal damage, it deals double instead."
No damage-output replacement primitive.

**Combined total if fixed: 19 cards**

Cards: Calamity Bearer, Chandra's Pyreling, Choose Your Weapon, Goblin Goliath,
Kellan Planar Trailblazer, Neyith of the Dire Hunt, Path of Mettle, Quest for Pure Flame
(+ 10 more)

---

### Group G — Counter move (13 borderline cards)

Moving a counter from one permanent to another. `movecounter` primitive absent.

**Combined total if fixed: 15 cards**

---

### Group A — Planechase (0 borderline, 23 unsupported)

No Plane cards in borderline.txt — all are in unsupported.txt. See U3 Group A.

---

### Group D — PW auras (2 borderline cards)

Liliana's Talent, Vivien's Talent — enchantments targeting a planeswalker
that react to loyalty ability activations.

**Combined total if fixed: 6 cards**

---

### Group F — Convoke grant (3 borderline cards)

Caetus Sea Tyrant of Segovia, Hoarding Broodlord, Joyful Stormsculptor.

**Combined total if fixed: 6 cards**

---

### Group K — Bolster (0 borderline, 1 unsupported)

No bolster cards in borderline.txt. Only Sandsteppe War Riders in unsupported.

