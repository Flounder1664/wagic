#!/usr/bin/env python3
"""
Merge EOE Batch 4 primitives into mtg.txt.
~36 MEDIUM EOE cards with approximations (mostly warp-stripped, conditional effects simplified).
"""
import re

MTG_TXT = r"M:\Claude_projects\wagic\projects\mtg\bin\Res\sets\primitives\mtg.txt"

EOE_CARDS_B4 = r"""
[card]
name=Bioengineered Future
auto=@movedTo(this|myBattlefield):_LANDERTOKEN_
text=When this enchantment enters, create a Lander token.
mana={1}{G}{G}
type=Enchantment
[/card]

[card]
name=Blade of the Swarm
auto=@movedTo(this|myBattlefield):counter(1/1,2) all(this)
text=When this creature enters, put two +1/+1 counters on it.
mana={3}{B}
type=Creature
subtype=Insect Assassin
power=3
toughness=1
[/card]

[card]
name=Brightspear Zealot
abilities=vigilance
text=Vigilance. This creature gets +2/+0 as long as you've cast two or more spells this turn. (Conditional bonus not supported)
mana={2}{W}
type=Creature
subtype=Human Soldier
power=2
toughness=4
[/card]

[card]
name=Bygone Colossus
text=Warp {3} (not supported)
mana={9}
type=Artifact Creature
subtype=Robot Giant
power=9
toughness=9
[/card]

[card]
name=Cloudsculpt Technician
abilities=flying
text=Flying. As long as you control an artifact, this creature gets +1/+0. (Conditional bonus not supported)
mana={2}{U}
type=Creature
subtype=Jellyfish Artificer
power=1
toughness=4
[/card]

[card]
name=Codecracker Hound
auto=@movedTo(this|myBattlefield):draw:1 && mill:1
text=When this creature enters, draw a card and mill a card.
mana={2}{U}
type=Creature
subtype=Dog
power=2
toughness=1
[/card]

[card]
name=Cosmogrand Zenith
auto=_FLURRY_:_HUMANSOLDIERTOKEN_
auto=_FLURRY_:_HUMANSOLDIERTOKEN_
text=Whenever you cast your second spell each turn, create two 1/1 white Human Soldier creature tokens.
mana={2}{W}
type=Creature
subtype=Human Soldier
power=2
toughness=4
[/card]

[card]
name=Dawnstrike Vanguard
abilities=lifelink
auto=@each my end:counter(1/1) all(other creature|mybattlefield)
text=Lifelink. At the beginning of your end step, put a +1/+1 counter on each other creature you control.
mana={5}{W}
type=Creature
subtype=Human Knight
power=4
toughness=5
[/card]

[card]
name=Drill Too Deep
auto=bury target(artifact|opponentbattlefield)
text=Destroy target artifact.
mana={1}{R}
type=Instant
[/card]

[card]
name=Drix Fatemaker
auto=@movedTo(this|myBattlefield):counter(1/1) target(creature|mybattlefield)
text=When this creature enters, put a +1/+1 counter on target creature you control. Each creature you control with a +1/+1 counter on it has trample. (Trample static not supported)
mana={3}{G}
type=Creature
subtype=Drix Wizard
power=3
toughness=2
[/card]

[card]
name=Eusocial Engineering
auto=_LANDFALL_:_ROBOTTOKEN_
text=Landfall — Whenever a land you control enters, create a 2/2 colorless Robot artifact creature token.
mana={3}{G}{G}
type=Enchantment
[/card]

[card]
name=Fell Gravship
auto=@movedTo(this|myBattlefield):mill:3
auto=@movedTo(this|myBattlefield):moveto(hand) target(creature|mygraveyard)
text=When this Spacecraft enters, mill three cards, then return a creature card from your graveyard to your hand.
mana={2}{B}
type=Artifact Creature
subtype=Spacecraft
power=3
toughness=2
[/card]

[card]
name=Flight-Deck Coordinator
auto=@each my end:life:2
text=At the beginning of your end step, you gain 2 life.
mana={2}{W}
type=Creature
subtype=Human Soldier
power=3
toughness=3
[/card]

[card]
name=Frontline War-Rager
auto=@each my end:counter(1/1) all(this)
text=At the beginning of your end step, put a +1/+1 counter on this creature.
mana={2}{R}
type=Creature
subtype=Kavu Soldier
power=2
toughness=3
[/card]

[card]
name=Germinating Wurm
auto=@movedTo(this|myBattlefield):life:2
text=When this creature enters, you gain 2 life.
mana={4}{G}
type=Creature
subtype=Plant Wurm
power=5
toughness=5
[/card]

[card]
name=Gravblade Heavy
text=As long as you control an artifact, this creature gets +1/+0 and has deathtouch. (Conditional bonus not supported)
mana={3}{B}
type=Creature
subtype=Human Soldier
power=3
toughness=4
[/card]

[card]
name=Interceptor Mechan
abilities=flying
auto=@movedTo(this|myBattlefield):moveto(hand) target(*[creature;artifact]|mygraveyard)
auto=@endOfTurn(_):counter(1/1) all(this)
text=Flying. When this creature enters, return target artifact or creature card from your graveyard to your hand. Void — At the beginning of your end step, put a +1/+1 counter on this creature.
mana={2}{B}{R}
type=Artifact Creature
subtype=Robot
power=2
toughness=2
[/card]

[card]
name=Invasive Maneuvers
auto=damage:3 target(creature|opponentbattlefield)
text=Invasive Maneuvers deals 3 damage to target creature.
mana={1}{R}
type=Instant
[/card]

[card]
name=Knight Luminary
auto=@movedTo(this|myBattlefield):_HUMANSOLDIERTOKEN_
text=When this creature enters, create a 1/1 white Human Soldier creature token.
mana={3}{W}
type=Creature
subtype=Human Knight
power=3
toughness=2
[/card]

[card]
name=Nova Hellkite
abilities=flying,haste
auto=@movedTo(this|myBattlefield):damage:1 target(creature|opponentbattlefield)
text=Flying, haste. When this creature enters, it deals 1 damage to target creature an opponent controls.
mana={3}{R}{R}
type=Creature
subtype=Dragon
power=4
toughness=5
[/card]

[card]
name=Rayblade Trooper
auto=@movedTo(this|myBattlefield):counter(1/1) target(creature|mybattlefield)
text=When this creature enters, put a +1/+1 counter on target creature you control.
mana={2}{W}
type=Creature
subtype=Human Soldier
power=2
toughness=2
[/card]

[card]
name=Red Tiger Mechan
abilities=haste
text=Haste.
mana={3}{R}
type=Artifact Creature
subtype=Robot Cat
power=3
toughness=3
[/card]

[card]
name=Rescue Skiff
auto=@movedTo(this|myBattlefield):moveto(mybattlefield) target(creature|mygraveyard)
text=When this Spacecraft enters, return target creature card from your graveyard to the battlefield.
mana={5}{W}
type=Artifact Creature
subtype=Spacecraft
power=5
toughness=6
[/card]

[card]
name=Ruinous Rampage
auto=damage:3 all(opponent)
text=Ruinous Rampage deals 3 damage to each opponent.
mana={1}{R}{R}
type=Sorcery
[/card]

[card]
name=Sami, Ship's Engineer
auto=@each my end:_ROBOTTOKEN_
text=At the beginning of your end step, create a tapped 2/2 colorless Robot artifact creature token.
mana={2}{R}{W}
type=Legendary Creature
subtype=Human Artificer
power=2
toughness=4
[/card]

[card]
name=Scour for Scrap
auto=moveto(hand) target(artifact|mygraveyard)
text=Return target artifact card from your graveyard to your hand.
mana={3}{U}
type=Instant
[/card]

[card]
name=Seedship Broodtender
auto=@movedTo(this|myBattlefield):mill:3
auto={3}{B}{G}{S}:moveto(mybattlefield) target(creature|mygraveyard)
text=When this creature enters, mill three cards. {3}{B}{G}, Sacrifice this creature: Return target creature card from your graveyard to the battlefield.
mana={B}{G}
type=Creature
subtype=Insect Citizen
power=2
toughness=3
[/card]

[card]
name=Sinister Cryologist
auto=@movedTo(this|myBattlefield):pump(-3/0) target(creature|opponentbattlefield) ueot
text=When this creature enters, target creature an opponent controls gets -3/-0 until end of turn.
mana={2}{U}
type=Creature
subtype=Jellyfish Wizard
power=2
toughness=3
[/card]

[card]
name=Starport Security
auto={3}{W}{T}:tap target(creature|opponentbattlefield)
text={3}{W}, {T}: Tap another target creature.
mana={W}
type=Artifact Creature
subtype=Robot Soldier
power=1
toughness=1
[/card]

[card]
name=Starbreach Whale
abilities=flying
auto=@movedTo(this|myBattlefield):_SURVEIL2_
text=Flying. When this creature enters, surveil 2.
mana={4}{U}
type=Creature
subtype=Whale
power=3
toughness=5
[/card]

[card]
name=Susurian Voidborn
auto=@movedTo(creature,artifact|mygraveyard) from(battlefield):life:-1 opponent && life:1 controller
text=Whenever this creature or another creature or artifact you control dies, target opponent loses 1 life and you gain 1 life.
mana={2}{B}
type=Creature
subtype=Vampire Soldier
power=2
toughness=2
[/card]

[card]
name=Syr Vondam, Sunstar Exemplar
abilities=vigilance,menace
auto=@movedTo(other creature|mygraveyard) from(mybattlefield):counter(1/1) all(this) && life:1
text=Vigilance, menace. Whenever another creature you control dies, put a +1/+1 counter on Syr Vondam and you gain 1 life.
mana={W}{B}
type=Legendary Creature
subtype=Human Knight
power=2
toughness=2
[/card]

[card]
name=Uthros, Titanic Godcore
auto=@movedTo(this|myBattlefield):tap(noevent)
auto={T}:Add{U}
text=This land enters tapped. {T}: Add {U}.
type=Land
subtype=Planet
[/card]

[card]
name=Vote Out
abilities=convoke
auto=bury target(creature|opponentbattlefield)
text=Convoke. Destroy target creature.
mana={3}{B}
type=Sorcery
[/card]

[card]
name=Weftblade Enhancer
auto=@movedTo(this|myBattlefield):counter(1/1) target(creature|mybattlefield)
text=When this creature enters, put a +1/+1 counter on target creature you control.
mana={5}{W}
type=Creature
subtype=Drix Artificer
power=3
toughness=4
[/card]

[card]
name=Xu-Ifit, Osteoharmonist
auto={T}:moveto(mybattlefield) target(creature|mygraveyard)
text={T}: Return target creature card from your graveyard to the battlefield. It's a Skeleton with no abilities. (Type-change not supported.) Activate only as a sorcery.
mana={1}{B}{B}
type=Legendary Creature
subtype=Human Wizard
power=2
toughness=3
[/card]
"""


def parse_cards(text):
    """Parse [card]...[/card] blocks, return list of (name_lower, name, full_block)."""
    cards = []
    blocks = re.split(r'\[card\]\s*\n', text)
    for block in blocks[1:]:
        block = block.strip()
        if not block:
            continue
        name_match = re.search(r'^name=(.+)', block, re.MULTILINE)
        if name_match:
            name = name_match.group(1).strip()
            full_block = '[card]\n' + block
            full_block = re.sub(r'(\[/card\]\s*)+$', '', full_block).rstrip()
            full_block += '\n[/card]\n'
            cards.append((name.lower(), name, full_block))
    return cards


def main():
    with open(MTG_TXT, 'r', encoding='utf-8') as f:
        existing = f.read()

    first_card_idx = existing.find('[card]')
    if first_card_idx == -1:
        print("ERROR: no [card] found in mtg.txt")
        return
    header = existing[:first_card_idx]

    existing_cards = parse_cards(existing)
    existing_names = {name_lower for name_lower, _, _ in existing_cards}
    print(f"Existing card blocks: {len(existing_cards)}")

    new_cards = parse_cards(EOE_CARDS_B4)
    print(f"New cards to evaluate: {len(new_cards)}")

    to_add = []
    for name_lower, name, block in new_cards:
        if name_lower in existing_names:
            print(f"  SKIP (already exists): {name}")
        else:
            print(f"  ADD: {name}")
            to_add.append((name_lower, name, block))

    print(f"\nAdding {len(to_add)} new cards.")

    all_cards = existing_cards + to_add
    all_cards.sort(key=lambda x: x[0])

    rebuilt = header
    for _, _, block in all_cards:
        rebuilt += block

    rebuilt = re.sub(r'(\[/card\]\s*){2,}', '[/card]\n', rebuilt)

    with open(MTG_TXT, 'w', encoding='utf-8') as f:
        f.write(rebuilt)

    with open(MTG_TXT, 'r', encoding='utf-8') as f:
        verify = f.read()
    card_count = verify.count('[/card]')
    print(f"\nDone. [/card] tags: {card_count}")
    print(f"File size: {len(verify):,} bytes")


if __name__ == '__main__':
    main()
