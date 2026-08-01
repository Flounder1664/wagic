#!/usr/bin/env python3
"""
Merge EOE Easy card primitives alphabetically into mtg.txt.
Run from any directory; paths are absolute.
"""

import re, sys

MTG_TXT = r"M:\Claude_projects\wagic\projects\mtg\bin\Res\sets\primitives\mtg.txt"

# ---------------------------------------------------------------------------
# All EOE EASY card primitives (alphabetical by name)
# ---------------------------------------------------------------------------
EOE_CARDS = r"""
[card]
name=All-Fates Scroll
auto={T}:_MANAOFANYCOLOR_
text={T}: Add one mana of any color.
mana={3}
type=Artifact
[/card]

[card]
name=Atmospheric Greenhouse
auto=counter(1/1) all(creature|mybattlefield)
text=When this Spacecraft enters, put a +1/+1 counter on each creature you control.
mana={4}{G}
type=Artifact
subtype=Spacecraft
power=5
toughness=4
[/card]

[card]
name=Beamsaw Prospector
auto=_DIES__LANDERTOKEN_
text=When this creature dies, create a Lander token.
mana={1}{B}
type=Creature
subtype=Human Artificer
power=2
toughness=1
[/card]

[card]
name=Biosynthic Burst
target=creature|mybattlefield
auto=counter(1/1)
auto=reach ueot
auto=trample ueot
auto=indestructible ueot
auto=untap
text=Put a +1/+1 counter on target creature you control. It gains reach, trample, and indestructible until end of turn. Untap it.
mana={1}{G}
type=Instant
[/card]

[card]
name=Biomechan Engineer
auto=_LANDERTOKEN_
auto={8}:draw:2 && _ROBOTTOKEN_
text=When this creature enters, create a Lander token. -- {8}: Draw two cards and create a 2/2 colorless Robot artifact creature token.
mana={G}{U}
type=Creature
subtype=Insect Artificer
power=2
toughness=2
[/card]

[card]
name=Biotech Specialist
auto=_LANDERTOKEN_
auto=@movedTo(artifact|mygraveyard) from(mybattlefield):damage:2 opponent
text=When this creature enters, create a Lander token. -- Whenever you sacrifice an artifact, this creature deals 2 damage to target opponent.
mana={R}{G}
type=Creature
subtype=Insect Scientist
power=1
toughness=3
[/card]

[card]
name=Chrome Companion
auto=@tapped(this):life:1 controller
auto={2}{T}:moveto(ownerlibrary) target(*|graveyard)
text=Whenever this creature becomes tapped, you gain 1 life. -- {2}, {T}: Put target card from a graveyard on the bottom of its owner's library.
mana={2}
type=Artifact Creature
subtype=Dog
power=2
toughness=1
[/card]

[card]
name=Comet Crawler
abilities=lifelink
auto=@combat(attacking) source(this):may name(Sacrifice) name(Sacrifice) target(other creature,artifact|mybattlefield) reject && all(this) 2/0 ueot
text=Lifelink -- Whenever this creature attacks, you may sacrifice another creature or artifact. If you do, this creature gets +2/+0 until end of turn.
mana={2}{B}
type=Creature
subtype=Insect Horror
power=2
toughness=3
[/card]

[card]
name=Cut Propulsion
target=creature
auto=_PUNCH_
text=Target creature deals damage to itself equal to its power. If that creature has flying, it deals twice that much damage to itself instead.
mana={2}{R}
type=Instant
[/card]

[card]
name=Dark Endurance
target=creature
auto=2/0 ueot
auto=indestructible ueot
text=Target creature gets +2/+0 and gains indestructible until end of turn.
mana={1}{B}
type=Instant
[/card]

[card]
name=Dauntless Scrapbot
auto=all(*|opponentgraveyard) moveto(exile)
auto=_LANDERTOKEN_
text=When this creature enters, exile each opponent's graveyard. Create a Lander token.
mana={3}
type=Artifact Creature
subtype=Robot
power=3
toughness=1
[/card]

[card]
name=Decode Transmissions
auto=draw:2
auto=life:-2 controller
text=You draw two cards and lose 2 life.
mana={2}{B}
type=Sorcery
[/card]

[card]
name=Depressurize
target=creature
auto=-3/0 ueot
text=Target creature gets -3/-0 until end of turn.
mana={1}{B}
type=Instant
[/card]

[card]
name=Diplomatic Relations
target=creature|mybattlefield
auto=1/0 ueot
auto=vigilance ueot
auto=_FIGHT_
text=Target creature you control gets +1/+0 and gains vigilance until end of turn. It deals damage equal to its power to target creature an opponent controls.
mana={2}{G}
type=Instant
[/card]

[card]
name=Dual-Sun Adepts
abilities=double strike
auto={5}:all(creature|mybattlefield) 1/1 ueot
text=Double strike -- {5}: Creatures you control get +1/+1 until end of turn.
mana={2}{W}
type=Creature
subtype=Human Soldier
power=2
toughness=2
[/card]

[card]
name=Edge Rover
abilities=reach
auto=_DIES__LANDERTOKEN_
text=Reach -- When this creature dies, create a Lander token.
mana={G}
type=Artifact Creature
subtype=Robot Scout
power=2
toughness=2
[/card]

[card]
name=Embrace Oblivion
target=creature
auto=bury
text=As an additional cost to cast this spell, sacrifice an artifact or creature. -- Destroy target creature.
mana={B}{S(artifact,creature|mybattlefield)}
type=Sorcery
[/card]

[card]
name=Eumidian Terrabotanist
auto=_LANDFALL_life:1 controller
text=Landfall -- Whenever a land you control enters, you gain 1 life.
mana={1}{G}
type=Creature
subtype=Insect Druid
power=2
toughness=3
[/card]

[card]
name=Exosuit Savior
abilities=flying
auto=may name(Return permanent) moveto(hand) target(other *|mybattlefield)
text=Flying -- When this creature enters, return up to one other target permanent you control to its owner's hand.
mana={2}{W}
type=Creature
subtype=Human Soldier
power=2
toughness=2
[/card]

[card]
name=Frenzied Baloth
abilities=trample,haste
auto=cantbecountered
text=This spell can't be countered. -- Trample, haste -- Creature spells you control can't be countered.
mana={G}{G}
type=Creature
subtype=Beast
power=3
toughness=2
[/card]

[card]
name=Full Bore
target=creature|mybattlefield
auto=3/2 ueot
text=Target creature you control gets +3/+2 until end of turn.
mana={R}
type=Instant
[/card]

[card]
name=Galactic Wayfarer
auto=_LANDERTOKEN_
text=When this creature enters, create a Lander token.
mana={2}{G}
type=Creature
subtype=Human Scout
power=3
toughness=3
[/card]

[card]
name=Gene Pollinator
auto={T}:_MANAOFANYCOLOR_
text={T}: Add one mana of any color.
mana={G}
type=Artifact Creature
subtype=Robot Insect
power=1
toughness=2
[/card]

[card]
name=Gigastorm Titan
auto=@movedto(*|mystack) restriction{thisturn(*|mystack)~equalto~1}:3/0 ueot
text=This spell costs {3} less to cast if you've cast another spell this turn. (Approximated: gets +3/+0 ueot on second spell cast instead.)
mana={4}{U}
type=Creature
subtype=Elemental
power=4
toughness=4
[/card]

[card]
name=Glacier Godmaw
abilities=trample
auto=_LANDERTOKEN_
auto=_LANDFALL_all(creature|mybattlefield) 1/1 ueot && all(creature|mybattlefield) vigilance ueot && all(creature|mybattlefield) haste ueot
text=Trample -- When this creature enters, create a Lander token. -- Landfall -- Whenever a land you control enters, creatures you control get +1/+1 and gain vigilance and haste until end of turn.
mana={5}{G}{G}
type=Creature
subtype=Leviathan
power=6
toughness=6
[/card]

[card]
name=Gravkill
target=creature
auto=exile
text=Exile target creature.
mana={3}{B}
type=Instant
[/card]

[card]
name=Gravpack Monoist
abilities=flying
auto=_DIES__ROBOTTOKEN_
text=Flying -- When this creature dies, create a tapped 2/2 colorless Robot artifact creature token.
mana={2}{B}
type=Creature
subtype=Human Scout
power=2
toughness=1
[/card]

[card]
name=Honor
target=creature
auto=counter(1/1)
auto=draw:1 controller
text=Put a +1/+1 counter on target creature. Draw a card.
mana={W}
type=Sorcery
[/card]

[card]
name=Hullcarver
abilities=deathtouch
text=Deathtouch
mana={B}
type=Artifact Creature
subtype=Robot Assassin
power=1
toughness=1
[/card]

[card]
name=Hymn of the Faller
auto=_SURVEIL1_
auto=draw:1
auto=life:-1 controller
text=Surveil 1, then you draw a card and lose 1 life.
mana={1}{B}
type=Sorcery
[/card]

[card]
name=Icecave Crasher
abilities=trample
auto=_LANDFALL_1/0 ueot
text=Trample -- Landfall -- Whenever a land you control enters, this creature gets +1/+0 until end of turn.
mana={3}{G}
type=Creature
subtype=Beast
power=4
toughness=4
[/card]

[card]
name=Icetill Explorer
auto=_LANDFALL_mill:1 controller
text=Landfall -- Whenever a land you control enters, mill a card.
mana={2}{G}{G}
type=Creature
subtype=Insect Scout
power=2
toughness=4
[/card]

[card]
name=Illvoi Galeblade
abilities=flying,flash
auto={2}{S}:draw:1 controller
text=Flash -- Flying -- {2}, Sacrifice this creature: Draw a card.
mana={U}
type=Creature
subtype=Jellyfish Warrior
power=1
toughness=1
[/card]

[card]
name=Illvoi Operative
auto=@movedto(*|mystack) restriction{thisturn(*|mystack)~equalto~1}:counter(1/1)
text=Whenever you cast your second spell each turn, put a +1/+1 counter on this creature.
mana={1}{U}
type=Creature
subtype=Jellyfish Rogue
power=2
toughness=1
[/card]

[card]
name=Insatiable Skittermaw
abilities=menace
text=Menace
mana={2}{B}
type=Creature
subtype=Insect Horror
power=2
toughness=2
[/card]

[card]
name=Intrepid Tenderfoot
auto={3}:counter(1/1) asSorcery
text={3}: Put a +1/+1 counter on this creature. Activate only as a sorcery.
mana={1}{G}
type=Creature
subtype=Insect Citizen
power=2
toughness=2
[/card]

[card]
name=Kavaron Skywarden
abilities=reach
text=Reach
mana={4}{R}
type=Creature
subtype=Kavu Soldier
power=4
toughness=5
[/card]

[card]
name=Kavaron Turbodrone
auto={T}:target(creature|mybattlefield) 1/1 ueot && target(creature|mybattlefield) haste ueot asSorcery
text={T}: Target creature you control gets +1/+1 and gains haste until end of turn. Activate only as a sorcery.
mana={2}{R}
type=Artifact Creature
subtype=Robot Scout
power=2
toughness=3
[/card]

[card]
name=Lashwhip Predator
abilities=reach
text=Reach
mana={4}{G}{G}
type=Creature
subtype=Plant Beast
power=5
toughness=7
[/card]

[card]
name=Mechan Navigator
auto=@tapped(this):_LOOT_
text=Whenever this creature becomes tapped, draw a card, then discard a card.
mana={1}{U}
type=Artifact Creature
subtype=Robot Pilot
power=2
toughness=1
[/card]

[card]
name=Melded Moxite
auto=may name(Discard for draw 2) name(Discard for draw 2) target(*|myhand) reject && draw:2 controller
auto={3}{S}:_ROBOTTOKEN_ tapped
text=When this artifact enters, you may discard a card. If you do, draw two cards. -- {3}, Sacrifice this artifact: Create a tapped 2/2 colorless Robot artifact creature token.
mana={1}{R}
type=Artifact
[/card]

[card]
name=Meltstrider Eulogist
auto=@movedTo(creature[counter{1/1}>=1]|mygraveyard) from(mybattlefield):draw:1 controller
text=Whenever a creature you control with a +1/+1 counter on it dies, draw a card.
mana={2}{G}
type=Creature
subtype=Insect Soldier
power=3
toughness=3
[/card]

[card]
name=Meltstrider's Gear
auto=teach(creature) 2/1
auto=teach(creature) reach
auto={5}:equip
text=When this Equipment enters, attach it to target creature you control. -- Equipped creature gets +2/+1 and has reach. -- Equip {5}
mana={G}
type=Artifact
subtype=Equipment
[/card]

[card]
name=Mental Modulation
target=artifact,creature
auto=tap
auto=draw:1 controller
text=Tap target artifact or creature. Draw a card.
mana={1}{U}
type=Instant
[/card]

[card]
name=Molecular Modifier
auto=@each my combatbegins:target(creature|mybattlefield) 1/0 ueot && target(creature|mybattlefield) first strike ueot
text=At the beginning of combat on your turn, target creature you control gets +1/+0 and gains first strike until end of turn.
mana={2}{R}
type=Creature
subtype=Kavu Artificer
power=2
toughness=2
[/card]

[card]
name=Monoist Sentry
abilities=defender
text=Defender
mana={B}
type=Artifact Creature
subtype=Robot
power=4
toughness=1
[/card]

[card]
name=Nanoform Sentinel
auto=@tapped(this):untap target(*[-this])
text=Whenever this creature becomes tapped, untap another target permanent.
mana={2}{U}
type=Artifact Creature
subtype=Robot
power=3
toughness=2
[/card]

[card]
name=Nebula Dragon
abilities=flying
auto=damage:3 target(anytarget)
text=Flying -- When this creature enters, it deals 3 damage to any target.
mana={6}{R}
type=Creature
subtype=Dragon
power=4
toughness=4
[/card]

[card]
name=Nutrient Block
abilities=indestructible
auto={2}{T}{S}:life:3 controller
auto=_DIES_draw:1 controller
text=Indestructible -- {2}, {T}, Sacrifice this artifact: You gain 3 life. -- When this artifact is put into a graveyard from the battlefield, draw a card.
mana={1}
type=Artifact
subtype=Food
[/card]

[card]
name=Oreplate Pangolin
auto=@movedTo(other artifact|mybattlefield):may pay({1}) name(Put counter) counter(1/1)
text=Whenever another artifact you control enters, you may pay {1}. If you do, put a +1/+1 counter on this creature.
mana={1}{R}
type=Artifact Creature
subtype=Robot Pangolin
power=2
toughness=2
[/card]

[card]
name=Plasma Bolt
target=anytarget
auto=damage:2
text=Plasma Bolt deals 2 damage to any target.
mana={R}
type=Sorcery
[/card]

[card]
name=Radiant Strike
target=artifact,creature[tapped]
auto=bury
auto=life:3 controller
text=Destroy target artifact or tapped creature. You gain 3 life.
mana={3}{W}
type=Instant
[/card]

[card]
name=Remnant Elemental
abilities=reach
auto=_LANDFALL_2/0 ueot
text=Reach -- Landfall -- Whenever a land you control enters, this creature gets +2/+0 until end of turn.
mana={1}{R}
type=Creature
subtype=Elemental
power=0
toughness=4
[/card]

[card]
name=Rig for War
target=creature|mybattlefield
auto=3/0 ueot
auto=first strike ueot
auto=reach ueot
text=Target creature gets +3/+0 and gains first strike and reach until end of turn.
mana={1}{R}
type=Instant
[/card]

[card]
name=Sami's Curiosity
auto=life:2 controller
auto=_LANDERTOKEN_
text=You gain 2 life. Create a Lander token.
mana={G}
type=Sorcery
[/card]

[card]
name=Seedship Agrarian
auto=@tapped(this):_LANDERTOKEN_
auto=_LANDFALL_counter(1/1)
text=Whenever this creature becomes tapped, create a Lander token. -- Landfall -- Whenever a land you control enters, put a +1/+1 counter on this creature.
mana={3}{G}
type=Creature
subtype=Insect Scientist
power=3
toughness=3
[/card]

[card]
name=Selfcraft Mechan
auto=may name(Sacrifice artifact) name(Sacrifice artifact) target(artifact|mybattlefield) reject && counter(1/1) target(creature|mybattlefield) && draw:1 controller
text=When this creature enters, you may sacrifice an artifact. When you do, put a +1/+1 counter on target creature and draw a card.
mana={3}{U}
type=Artifact Creature
subtype=Robot Artificer
power=3
toughness=4
[/card]

[card]
name=Skystinger
abilities=reach
auto=@combat(blocked,turnlimited) source(this) restriction{type(creature[flying]|opponentbattlefield)~morethan~0}:5/0 ueot
text=Reach -- Whenever this creature blocks a creature with flying, this creature gets +5/+0 until end of turn.
mana={2}{G}
type=Creature
subtype=Insect Warrior
power=3
toughness=3
[/card]

[card]
name=Slagdrill Scrapper
auto={2}{T}{S}:draw:1 controller
text={2}, {T}, Sacrifice another artifact or land: Draw a card.
mana={R}
type=Artifact Creature
subtype=Robot Scout
power=1
toughness=2
[/card]

[card]
name=Squire's Lightblade
abilities=flash
auto=teach(creature) 1/0
auto=teach(creature) first strike ueot
auto={3}:equip
text=Flash -- When this Equipment enters, attach it to target creature you control. That creature gains first strike until end of turn. -- Equipped creature gets +1/+0. -- Equip {3}
mana={W}
type=Artifact
subtype=Equipment
[/card]

[card]
name=Starfighter Pilot
auto=@tapped(this):_SURVEIL1_
text=Whenever this creature becomes tapped, surveil 1.
mana={1}{W}
type=Creature
subtype=Human Pilot
power=2
toughness=2
[/card]

[card]
name=Sunstar Expansionist
auto=_LANDERTOKEN_
auto=_LANDFALL_1/0 ueot
text=When this creature enters, create a Lander token. -- Landfall -- Whenever a land you control enters, this creature gets +1/+0 until end of turn.
mana={1}{W}
type=Creature
subtype=Human Knight
power=2
toughness=3
[/card]

[card]
name=Sunstar Lightsmith
auto=@movedto(*|mystack) restriction{thisturn(*|mystack)~equalto~1}:counter(1/1) && draw:1 controller
text=Whenever you cast your second spell each turn, put a +1/+1 counter on this creature and draw a card.
mana={3}{W}
type=Creature
subtype=Human Artificer
power=3
toughness=3
[/card]

[card]
name=Swarm Culler
abilities=flying
auto=@tapped(this):may name(Sacrifice) name(Sacrifice) target(other creature,artifact|mybattlefield) reject && draw:1 controller
text=Flying -- Whenever this creature becomes tapped, you may sacrifice another creature or artifact. If you do, draw a card.
mana={3}{B}
type=Creature
subtype=Insect Warrior
power=2
toughness=4
[/card]

[card]
name=Thawbringer
auto=_SURVEIL1_
auto=_DIES__SURVEIL1_
text=When this creature enters or dies, surveil 1.
mana={2}{G}
type=Creature
subtype=Insect Scout
power=4
toughness=2
[/card]

[card]
name=Tragic Trajectory
target=creature
auto=-2/-2 ueot
text=Target creature gets -2/-2 until end of turn.
mana={B}
type=Sorcery
[/card]

[card]
name=Unravel
target=*|stack
auto=fizzle
text=Counter target spell.
mana={1}{U}{U}
type=Instant
[/card]

[card]
name=Voidforged Titan
text=
mana={4}{B}
type=Artifact Creature
subtype=Robot Warrior
power=5
toughness=4
[/card]

[card]
name=Zealous Display
auto=all(creature|mybattlefield) 2/0 ueot
text=Creatures you control get +2/+0 until end of turn.
mana={2}{W}
type=Instant
[/card]

[card]
name=Zookeeper Mechan
auto={T}:Add{R}
auto={6}{R}:target(creature|mybattlefield) 4/0 ueot asSorcery
text={T}: Add {R}. -- {6}{R}: Target creature you control gets +4/+0 until end of turn. Activate only as a sorcery.
mana={1}{R}
type=Artifact Creature
subtype=Robot
power=1
toughness=3
[/card]
"""

# ---------------------------------------------------------------------------
# Parse a block of card text into a list of (name, block_text) tuples
# ---------------------------------------------------------------------------
def parse_cards(text):
    cards = []
    for block in re.split(r'\[card\]', text):
        block = block.strip()
        if not block or not block.startswith('name='):
            continue
        m = re.search(r'^name=(.+)$', block, re.MULTILINE)
        if m:
            name = m.group(1).strip()
            cards.append((name.lower(), name, '[card]\n' + block.rstrip('\n') + '\n[/card]\n'))
    return cards

# ---------------------------------------------------------------------------
# Parse existing mtg.txt into cards list
# ---------------------------------------------------------------------------
print(f"Reading {MTG_TXT} ...")
with open(MTG_TXT, 'r', encoding='utf-8') as f:
    existing = f.read()

existing_cards = parse_cards(existing)
print(f"  {len(existing_cards)} existing card blocks found.")

new_cards = parse_cards(EOE_CARDS)
print(f"  {len(new_cards)} new EOE cards to insert.")

# Check which names already exist
existing_names = {name_lower for name_lower, _, _ in existing_cards}
skipped = []
to_insert = []
for name_lower, name, block in new_cards:
    if name_lower in existing_names:
        skipped.append(name)
    else:
        to_insert.append((name_lower, name, block))

if skipped:
    print(f"  Skipping {len(skipped)} cards already in mtg.txt: {', '.join(skipped)}")

print(f"  Inserting {len(to_insert)} cards...")

# ---------------------------------------------------------------------------
# Merge: insert new cards at alphabetically correct positions
# ---------------------------------------------------------------------------
all_cards = existing_cards + to_insert
all_cards.sort(key=lambda x: x[0])  # sort by lowercase name

# Reassemble the file
header_end = existing.find('[card]')
header = existing[:header_end] if header_end != -1 else ''

body = '\n'.join(block for _, _, block in all_cards)
output = header + body + '\n'

print(f"Writing merged mtg.txt ...")
with open(MTG_TXT, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Done. Inserted {len(to_insert)} EOE cards into mtg.txt.")
for _, name, _ in sorted(to_insert, key=lambda x: x[0]):
    print(f"  + {name}")
