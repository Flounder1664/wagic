# Teenage Mutant Ninja Turtles (TMT) - Implementation Backlog

Set code `tmt` - Universes Beyond expansion, 2026-03-06. Source: Scryfall bulk dump, deduped by
English card name (`tmt_clean.json`, 195 unique cards). This is notably lower than
SET_BACKLOG.md's earlier "320" estimate -- that figure counted alternate-art/showcase/borderless
variants Scryfall lists separately; 195 is the true unique-card count for the main set.

TMT is Universes Beyond: TMNT IP names and flavour are painted over ordinary Magic rules text.
Every card below is classified on its **underlying rules**, not its cartoon dressing.

Assessment generated 2026-07-11. Supersedes the rough "Sample Set Analysis" that previously
lived in `SET_BACKLOG.md` (which estimated three engine walls -- **Sneak / Disappear / Alliance**;
only Sneak survives verification, see the mechanics section).

## Status

| Metric | Count |
|---|---|
| True unique cards (Scryfall, deduped) | 195 |
| Really implemented (name resolves `supported`/`borderline` in the master primitive index) | 16 |
| Excluded (need work) | 179 |

| Really-implemented split | Count |
|---|---|
| supported | 13 |
| borderline | 3 |

| Bucket (mutually exclusive, all 179 excluded cards) | Count |
|---|---|
| ENGINE-BLOCKED (Sneak) | 26 |
| BACKLOG-EASY | 101 |
| BACKLOG-MEDIUM | 52 |
| OUT-OF-SCOPE | 0 |
| **Total** | **179** |

The 16 really-implemented cards are the 5 basic lands plus 11 names that happen to collide with,
or reuse, primitives already authored for other sets: **Death in the Family**, **Donatello,
Turtle Techie**, **Escape Tunnel** _(borderline)_, **Make Your Move**, **Mouser Mark III**,
**Negate**, **Oroku Saki, Shredder Rising** _(borderline)_, **Rock Soldiers**, **Squirrelanoids**,
**Technodrome** _(borderline)_, **Tunnel Rats**. Everything else in the set is unwritten.

---

## `_cards.dat` bookkeeping notes (not card-count issues)

`projects/mtg/bin/Res/sets/TMT/_cards.dat` declares `total=200` and carries **200 `primitive=`
lines with no duplicate names**. Reconciling against the 195 true cards:

- **All 195 true cards are registered** -- there are **zero UNREGISTERED cards**. TMT's set
  skeleton is 100% built out; every true card has an `id=` and will surface in draft pools /
  deck imports.
- **5 of the 200 `primitive=` lines are not TMT set cards at all.** They sit in a leading block
  with out-of-range ids (`910xxx`) and names that don't appear anywhere in the 195: **April
  O'Neil, Live on the Scene**; **Leonardo, Tactical Leader**; **Pizza Party**; **Sewer Pipe
  Omenpath**; **Splinter's Wisdom**. All five *do* resolve to `supported` primitives in `mtg.txt`
  (they belong to a sibling TMNT product -- Commander / Secret Lair -- with "Omenpath" and "Live
  on the Scene" style names). In TMT's `_cards.dat` they are **stray registrations**: they inflate
  the raw "supported" count but add nothing to TMT's own coverage, so they are excluded from the
  195-card math above. Cleanup item: strip them, or leave them as harmless cross-product entries.

So: 200 registered = 195 true TMT cards + 5 foreign strays. Of the 195 true cards, 16 really
resolve and **179 are UNWRITTEN** (registered with an id, but no primitive with that name exists
in `mtg.txt` / `borderline.txt` / `planeswalkers.txt`).

---

## Cross-cutting finding: all 179 excluded cards are dangling `_cards.dat` references (live bug)

Exactly as with SPM, every one of the 179 excluded cards is simultaneously an **UNWRITTEN**
dangling reference. Each has an `id=` + `primitive=<name>` block in `_cards.dat`, but none of the
179 names resolve in the master implemented-primitives index. That means these cards already have
a card id and will appear in draft pools, deck imports, and card lookups, but **the primitive text
backing them was never authored** -- resolving one at runtime fails to find a matching primitive.

TMT is therefore the SPM shape, not the SOS shape: nothing is "missing from `_cards.dat`"; the
gap is entirely un-authored primitives behind pre-assigned ids. Until a card is authored, its
`_cards.dat` entry is a landmine -- strip the entry or add a placeholder `text=` line so the set
doesn't ship with silently-unresolvable references. The mechanic-grouped classification below is
meant to guide that authoring pass.

---

## New TMT keywords vs. the three predicted engine walls

The prior rough analysis guessed **Sneak**, **Disappear**, and **Alliance** were each a new C++
wall. Probing `grade_index.json` for cards Wagic *already* implements settles it:

### Alliance -- NOT engine-blocked (fully supported today)

> **Alliance** -- "Whenever another creature you control enters, ..."

This is a plain ETB-of-another-creature trigger, which Wagic supports and ships in quantity:
**Impact Tremors**, **Cathars' Crusade**, **Champion of Lambholt**, **Purphoros, God of the
Forge**, **Cryptolith Rite** (all `supported`) fire on exactly this event. Alliance is a renamed,
already-solved trigger. The 10 Alliance cards split by *body* complexity, not by the keyword:
7 are BACKLOG-EASY (simple pump / counter / damage riders), 3 are BACKLOG-MEDIUM (modal choice
or exile-top-of-library riders).

### Disappear -- NOT engine-blocked, but MEDIUM (needs a per-turn LTB tracker)

> **Disappear** -- "At the beginning of your end step, if a permanent left the battlefield under
> your control this turn, ..." (also appears as an ETB / enters-with-counters conditional)

The building blocks exist: Wagic already implements morbid-style "left the battlefield this turn"
checks and death triggers -- **Tragic Slip**, **Blood Artist**, **Zulaport Cutthroat**,
**Brimstone Volley** are all `supported`. Disappear needs the specific per-turn "did *any*
permanent I control leave this turn" state, evaluated at the end step / on ETB. That is a careful
DSL wiring job, not a missing engine capability, so all 9 Disappear cards are BACKLOG-MEDIUM
(grouped below). Not an engine wall.

### Sneak -- CONFIRMED the one genuine engine wall

> **Sneak {cost}** -- "You may cast this spell for {cost} if you also return an unblocked
> attacker you control to hand during the declare blockers step. (A creature) enters tapped and
> attacking."

Sneak is Ninjutsu reframed as an **alternative casting cost**. Wagic's closest analog is
Ninjutsu, which *is* fully supported (**Ninja of the Deep Hours**, **Higure, the Still Wind**,
**Ink-Eyes**, **Skullsnatcher**, **Throat Slitter** -- all `supported`), but that support is a
bespoke C++ ability class (`ANinja` / `TrCardNinja` in `MTGAbility.cpp`), keyed off the literal
`ninjutsu` keyword. There is **no generic "return an unblocked attacker as an alternative cost"
hook** in the DSL, and Sneak differs from Ninjutsu in two load-bearing ways:

1. It is a **cast** (it uses the stack and can be countered), not an activated ability.
2. It appears on **instants and sorceries** too (the entire "Technique" cycle), where "enters
   tapped and attacking" is meaningless -- Sneak just acts as a conditional cost reduction.

So Sneak needs a new alt-cost class (realistically an extension of `ANinja`, since the
return-attacker + enter-tapped-attacking machinery already exists there). This is the single
engine-blocked mechanic in TMT. **26 cards print Sneak** and are bucketed ENGINE-BLOCKED below.

_Note: 11 of the 26 are the "Technique" instant/sorcery cycle, where the underlying effect
(tutor, removal, pump, etc.) is itself trivial. Those bodies could be authored today with the
Sneak alt-cost simply dropped -- the same "approximate the mechanic away" simplification SPM's
existing Web-Slinger primitive uses -- if a partial-fidelity pass is acceptable._

### Other named TMT keywords -- all reachable with existing DSL

- **Saga** (2: The Cloning of Shredder, The Last Ronin) -- Sagas are `borderline` and shipped
  (History of Benalia, Phyrexian Scriptures). MEDIUM.
- **Class** (4: Cool but Rude, Does Machines, Leader's Talent, Party Dude) -- Class enchantments
  are `borderline` and shipped (Ranger/Barbarian/Cleric Class). MEDIUM. _(A 5th Class card,
  Ninja Teen, also prints Sneak and is bucketed under ENGINE-BLOCKED.)_
- **Channel** (1: Action News Crew) -- `borderline`/shipped (Boseiju, Otawara). EASY.
- **Enrage** (Raphael, Ninja Destroyer), **Affinity for artifacts**, **type-cycling**
  (Plains/Swamp/etc.-cycling), **extra combat phases**, **"from outside the game"** wishes
  (North Wind Avatar, Turtles Forever) -- all verified `supported` elsewhere. No new wall.

---

## ENGINE-BLOCKED (26) - Sneak

Alt-cost "return an unblocked attacker; if a creature, it enters tapped and attacking." No DSL
hook; needs a new/extended C++ alt-cost class (see mechanics section). Grouped as one mechanic.

- **Dark Leo & Shredder** _Legendary Creature - Mutant Ninja Turtle Human_
- **Donatello's Technique** _Sorcery_
- **Donatello, Gadget Master** _Legendary Creature - Mutant Ninja Turtle_
- **Foot Ninjas** _Creature - Human Ninja_
- **Jennika's Technique** _Instant_
- **Karai's Technique** _Sorcery_
- **Karai, Future of the Foot** _Legendary Creature - Human Ninja_
- **Kitsune's Technique** _Instant_
- **Leonardo's Technique** _Sorcery_
- **Leonardo, Big Brother** _Legendary Creature - Mutant Ninja Turtle_
- **Leonardo, Cutting Edge** _Legendary Creature - Mutant Ninja Turtle_
- **Leonardo, Leader in Blue** _Legendary Creature - Mutant Ninja Turtle_
- **Leonardo, Sewer Samurai** _Legendary Creature - Mutant Ninja Turtle Samurai_
- **Michelangelo's Technique** _Sorcery_
- **Michelangelo, Improviser** _Legendary Creature - Mutant Ninja Turtle_
- **New Generation's Technique** _Sorcery_
- **Ninja Teen** _Enchantment - Class_ (also grants Sneak to graveyard creatures)
- **Raphael's Technique** _Instant_
- **Raphael, the Nightwatcher** _Legendary Creature - Mutant Ninja Turtle_
- **Shark Shredder, Killer Clone** _Legendary Creature - Shark Octopus Ninja_
- **Shredder's Technique** _Sorcery_
- **Shredder, Unrelenting** _Legendary Creature - Human Ninja_
- **Splinter's Technique** _Sorcery_
- **Splinter, Hamato Yoshi** _Legendary Creature - Mutant Ninja Rat_
- **The Last Ronin's Technique** _Instant_
- **Turncoat Kunoichi** _Creature - Mutant Ninja Fox_

_(The 11 "...'s Technique" instants/sorceries in this list are only engine-blocked at full
fidelity; their base effects are EASY-MEDIUM if Sneak is dropped.)_

---

## BACKLOG-EASY (101)

Uses only mechanics Wagic already fully supports (standard keywords; ETB / death / attack
triggers; +1/+1 counters; Food and Mutagen artifact tokens = existing token+activated-ability
framework; tap-lands with ETB lifegain; Equipment/equip; Crew/Vehicle; type-cycling; Channel;
fight; modal choose-one). Short, single-or-double-clause bodies with no nested conditionals,
copy effects, or library-scaling.

### Alliance sub-bucket (7) - "whenever another creature you control enters" rider, simple payoff

- **EPF Point Squad** _Creature - Human Soldier_
- **East Wind Avatar** _Creature - Bird Spirit Avatar_
- **Mighty Mutanimals** _Creature - Mutant Rebel_
- **Mutant Town Musicians** _Creature - Mutant Bard Performer_
- **Raphael, Tough Turtle** _Legendary Creature - Mutant Ninja Turtle_
- **Slash, Reptile Rampager** _Legendary Creature - Mutant Berserker Turtle_
- **Wingnut, Bat on the Belfry** _Legendary Creature - Bat Mutant_

### Everything else EASY (94)

- **Action News Crew** _Creature - Human Citizen_ (Channel)
- **Agent Bishop, Man in Black** _Legendary Creature - Human Soldier_
- **Anchovy & Banana Pizza** _Artifact - Food_
- **April, Reporter of the Weird** _Legendary Creature - Human Detective_
- **Armaggon, Future Shark** _Legendary Creature - Shark Horror Mutant_
- **Baxter Stockman** _Legendary Creature - Human Scientist_
- **Bebop & Rocksteady** _Legendary Creature - Boar Rhino Mutant_
- **Bebop, Warthog Warrior** _Legendary Creature - Boar Mutant Warrior_ (Swampcycling)
- **Bespoke Bō** _Artifact - Equipment_
- **Bot Bashing Time** _Sorcery_
- **Brilliance Unleashed** _Sorcery_
- **Broadcast Takeover** _Sorcery_
- **Buzz Bots** _Artifact Creature - Robot Insect_
- **Casey Jones, Vigilante** _Legendary Creature - Human Berserker_
- **Crustacean Commando** _Creature - Crab Mutant Soldier_
- **Dimension X** _Land_
- **Donatello, Mutant Mechanic** _Legendary Creature - Mutant Ninja Turtle_
- **Donatello, Way with Machines** _Legendary Creature - Mutant Ninja Turtle_
- **Featherbrained Filcher** _Creature - Bird Mutant_
- **Foot Elite** _Creature - Human Ninja_
- **Foot Headquarters** _Land_
- **Frog Butler** _Creature - Frog Spirit_
- **Fugitive Droid** _Artifact Creature - Robot Scientist_
- **General Traag, Heart of Stone** _Legendary Artifact Creature - Elemental Soldier_
- **Genghis Frog** _Legendary Creature - Frog Mutant Rogue_
- **Groundchuck & Dirtbag** _Legendary Creature - Ox Mole Mutant_
- **Grounded for Life** _Instant_
- **Guac & Marshmallow Pizza** _Artifact - Food_
- **Hard-Won Jitte** _Artifact - Equipment_
- **High-Flying Ace** _Creature - Bird Mutant_
- **Ice Cream Kitty** _Artifact Creature - Food Cat Mutant_
- **Illegitimate Business** _Land_
- **Jennika, Bad Apple Big Sister** _Legendary Creature - Mutant Ninja Turtle_ (Plainscycling)
- **Kitsune, Dragon's Daughter** _Legendary Creature - Fox Warlock Avatar_
- **Krang, Utrom Warlord** _Legendary Artifact Creature - Utrom Robot_
- **Leatherhead, Swamp Stalker** _Legendary Creature - Crocodile Mutant Rogue_
- **Lessons from Life** _Sorcery_
- **Madame Null, Power Broker** _Legendary Creature - Demon Advisor_
- **Mechanized Ninja Cavalry** _Artifact Creature - Robot Ninja_
- **Metalhead** _Legendary Artifact Creature - Robot Turtle_
- **Michelangelo, Mutant BFF** _Legendary Creature - Mutant Ninja Turtle_
- **Michelangelo, Weirdness to 11** _Legendary Creature - Mutant Ninja Turtle_
- **Mikey & Leo, Chaos & Order** _Legendary Creature - Mutant Ninja Turtle_
- **Mind Transfer Protocol** _Instant_
- **Mona Lisa, Science Geek** _Legendary Creature - Lizard Mutant_
- **Mouser Attack!** _Instant_
- **Mouser Foundry** _Artifact_
- **Mutagen Man, Living Ooze** _Legendary Creature - Ooze Mutant_
- **Mutant Chain Reaction** _Sorcery_
- **Mutant Town** _Land_
- **Novel Nunchaku** _Artifact - Equipment_
- **Null Group Biological Assets** _Creature - Mutant Mercenary_
- **Old Hob, Alleycat Blues** _Legendary Creature - Cat Mutant Rebel_
- **Omni-Cheese Pizza** _Artifact - Food_
- **Ooze Spill** _Instant_
- **Pain 101** _Instant_
- **Prehistoric Pet** _Creature - Dinosaur Ninja_
- **Primordial Pachyderm** _Creature - Elephant Avatar_
- **Purple Dragon Punks** _Creature - Human Rogue_
- **Quintessential Katana** _Artifact - Equipment_
- **Raph & Leo, Sibling Rivals** _Legendary Creature - Mutant Ninja Turtle_
- **Raphael, Ninja Destroyer** _Legendary Creature - Mutant Ninja Turtle_ (Enrage)
- **Ravenous Robots** _Artifact Creature - Robot_
- **Ray Fillet, Man Ray** _Legendary Creature - Fish Mutant_
- **Renet, Temporal Apprentice** _Legendary Creature - Human Wizard_
- **Retro-Mutation** _Enchantment - Aura_
- **Rocksteady, Crash Courser** _Legendary Creature - Rhino Mutant_ (Forestcycling)
- **Sally Pride, Lioness Leader** _Legendary Creature - Cat Mutant Rebel_
- **Savanti Romero, Time's Exile** _Legendary Creature - Demon Wizard_
- **Saved by the Shell** _Instant_
- **Sewer-veillance Cam** _Artifact_
- **Shredder's Armor** _Artifact - Equipment_
- **Shredder's Revenge** _Sorcery_
- **Skateboard** _Artifact - Equipment_
- **Slithering Cryptid** _Creature - Fish Mutant_
- **South Wind Avatar** _Creature - Snake Spirit Avatar_
- **Spicy Oatmeal Pizza** _Artifact - Food_
- **Splinter, Radical Rat** _Legendary Creature - Mutant Ninja Rat_
- **Stockman, Mad Fly-entist** _Legendary Creature - Insect Mutant Scientist_ (Islandcycling)
- **Stomped by the Foot** _Instant_ (Kicker)
- **Super Shredder** _Legendary Creature - Mutant Ninja Human_
- **TCRI Building** _Land_
- **Tainted Treats** _Instant_
- **Tenderize** _Instant_
- **Transdimensional Bovine** _Creature - Ox Avatar_
- **Triceraton Commander** _Creature - Dinosaur Soldier_
- **Turtle Blimp** _Artifact - Vehicle_ (Crew)
- **Turtle Lair** _Land_
- **Turtle Power!** _Enchantment_
- **Uneasy Alliance** _Enchantment - Aura_
- **Utrom Scientists** _Artifact Creature - Utrom Robot Scientist_ (stun counter)
- **Venus, Torn Between Worlds** _Legendary Creature - Mutant Frog Turtle_
- **Zog, Triceraton Castaway** _Legendary Creature - Dinosaur Soldier_ (Mountaincycling)
- **Zoo Escapees** _Creature - Boar Rhino_

---

## BACKLOG-MEDIUM (52)

Supported mechanics, but multi-clause / conditional / "for each"-scaling text, copy effects,
library manipulation, exile-and-return delays, top-of-library play, or the Disappear/Saga/Class
frameworks that need careful DSL wiring -- same bar as SOS/SPM MEDIUM.

### Disappear sub-bucket (9) - per-turn "a permanent left the battlefield under your control" tracker

- **Foot Mystic** _Creature - Human Ninja Warlock_
- **Insectoid Exterminator** _Creature - Insect Mutant_
- **Krang & Shredder** _Legendary Creature - Utrom Human Ninja_ (Disappear + free-cast-from-exile)
- **Lord Dregg, Insect Invader** _Legendary Creature - Insect Warrior_
- **Michelangelo, Game Master** _Legendary Creature - Mutant Ninja Turtle_
- **Pizza Face, Gastromancer** _Legendary Artifact Creature - Food Mutant_
- **Putrid Pals** _Creature - Human Ooze Mutant_ (enters-with-counters conditional)
- **Rat King, Verminister** _Legendary Creature - Rat Avatar_
- **West Wind Avatar** _Creature - Cat Spirit Avatar_

### Saga sub-bucket (2)

- **The Cloning of Shredder** _Enchantment - Saga_ (copy from exile chapters)
- **The Last Ronin** _Enchantment - Saga_ (wrath / mill+return / attack-alone chapters)

### Class sub-bucket (4)

- **Cool but Rude** _Enchantment - Class_
- **Does Machines** _Enchantment - Class_
- **Leader's Talent** _Enchantment - Class_
- **Party Dude** _Enchantment - Class_

### Alliance sub-bucket (3) - Alliance + a nontrivial rider (modal / exile-top / return-and-attack)

- **Lita, Little Orphan Amphibian** _Legendary Creature - Mutant Ninja Turtle_ (modal, once-per-turn choice)
- **Raphael, Most Attitude** _Legendary Creature - Mutant Ninja Turtle_ (exile-top + play-exiled)
- **The Neutrinos** _Legendary Creature - Elf Rebel_ (Alliance + flicker-and-attack)

### Everything else MEDIUM (34)

- **April O'Neil, Hacktivist** _Legendary Creature - Human Scientist_ (draw per card-type cast this turn)
- **April O'Neil, Kunoichi Trainee** _Legendary Creature - Human Ninja_ (scry + power-based evasion)
- **Casey Jones, Jury-Rig Justiciar** _Legendary Creature - Human Berserker_ (look-4, reveal artifact)
- **Chrome Dome** _Artifact Creature - Robot Ninja_ (copy-an-artifact token)
- **Courier of Comestibles** _Creature - Human Citizen_ (tutor-Food-or-make-Food)
- **Cowabunga!** _Sorcery_ (look-4, reveal type)
- **Dimensional Exile** _Enchantment - Aura_ (Oblivion-Ring on basic-land-enchant)
- **Don & Leo, Problem Solvers** _Legendary Creature - Mutant Ninja Turtle_ (end-step flicker two permanents)
- **Don & Raph, Hard Science** _Legendary Creature - Mutant Ninja Turtle_ (grant affinity to next spell)
- **Dream Beavers** _Creature - Beaver Nightmare_ (drain + scry)
- **Everything Pizza** _Artifact - Food_ (tutor basic + multi-effect sac)
- **Go Ninja Go** _Sorcery_ (modal flicker / greatest-power damage)
- **Hamato Guardian Stance** _Instant_ (pump + scry)
- **Henchbots** _Artifact Creature - Robot_ (exile-tapped-until-LTB)
- **Improvised Arsenal** _Artifact - Equipment_ (per-artifact buff + self-copy)
- **Koya, Death from Above** _Legendary Creature - Mutant Ninja Bird_ (exile + pay-or-return delayed)
- **Krang, Master Mind** _Legendary Artifact Creature - Utrom Warrior_ (affinity + draw-to-hand-size + per-artifact buff)
- **Manhole Missile** _Instant_ (damage + loot)
- **Mikey & Don, Party Planners** _Legendary Creature - Mutant Ninja Turtle_ (play from top of library)
- **Mondo Gecko** _Legendary Creature - Lizard Mutant_ (color-change hexproof + draw-per-color)
- **Nobody** _Artifact Creature - Human Hero_ (bounce + scry)
- **North Wind Avatar** _Creature - Dragon Spirit Avatar_ (card from outside the game / wish)
- **Northampton Farm** _Land_ (exile-own + sac-to-return package)
- **Paramecia Coloniex** _Creature - Zombie Worm_ (mill + death-exile self to top-deck a creature)
- **Punk Frogs** _Creature - Frog Mutant Rebel_ (Ward)
- **Ragamuffin Raptor** _Creature - Dinosaur_ (return creature/Food from graveyard)
- **Raph & Mikey, Troublemakers** _Legendary Creature - Mutant Ninja Turtle_ (reveal-until-creature, cheat into play attacking)
- **Return to the Sewers** _Instant_ (top/bottom-of-library + Mutagen)
- **The Ooze** _Legendary Artifact_ (Mutagen-per-counter on counter-creature LTB)
- **Tokka & Rahzar, Terrible Twos** _Legendary Creature - Turtle Wolf Mutant_ (mana-spent-vs-MV punisher)
- **Turtle Van** _Artifact - Vehicle_ (Crew + counter-doubling for Mutant/Ninja/Turtle)
- **Turtles Forever** _Instant_ (tutor 4 legends incl. outside the game, opponent chooses)
- **Turtles in Time** _Sorcery_ (mass bounce + optional shuffle-and-draw-7)
- **Weather Maker** _Artifact_ (Landfall charge counters + tiered activations)

---

## OUT-OF-SCOPE (0)

All 195 true cards are real, distinct, playable set members. The deduped list carried no promos,
alternate arts, or stray tokens. (The 5 non-TMT `_cards.dat` strays noted above are a bookkeeping
issue, not out-of-scope *cards*.)

---

## Summary

| True cards | Really implemented (S / B) | Excluded | Engine-blocked (Sneak) | Easy | Medium | Out-of-scope |
|---|---|---|---|---|---|---|
| 195 | 16 (13 / 3) | 179 | 26 | 101 | 52 | 0 |

All 179 excluded cards are simultaneously UNWRITTEN dangling references in `_cards.dat`
(registered with an id, primitive text never authored). Of the three engine walls the prior
rough analysis predicted, only **Sneak** survives: **Alliance** is an already-supported ETB
trigger and **Disappear** is a MEDIUM-difficulty per-turn tracker built from supported parts.
