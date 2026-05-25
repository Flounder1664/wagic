#!/usr/bin/env python3
"""
Merge EOE Batch 3 primitives into mtg.txt.
~18 EASY EOE cards not covered in Batch 1 or Batch 2.
"""
import re

MTG_TXT = r"M:\Claude_projects\wagic\projects\mtg\bin\Res\sets\primitives\mtg.txt"

EOE_CARDS_B3 = r"""
[card]
name=Alpharael, Stonechosen
mana={3}{B}{B}
type=Legendary Creature
subtype=Human Cleric
power=3
toughness=3
text=Ward—Discard a card at random. Void — Whenever Alpharael attacks, if a nonland permanent left the battlefield this turn or a spell was warped this turn, defending player loses half their life, rounded up.
[/card]

[card]
name=Atomic Microsizer
auto={2}:equip
auto=teach(creature) +1/+0
text=Equipped creature gets +1/+0. Equip {2}
mana={U}
type=Artifact
subtype=Equipment
[/card]

[card]
name=Auxiliary Boosters
auto=@movedTo(this|myBattlefield):_ROBOTTOKEN_
auto={3}:equip
auto=teach(creature) +1/+2,flying
text=When this Equipment enters, create a 2/2 colorless Robot artifact creature token. Equipped creature gets +1/+2 and has flying. Equip {3}
mana={4}{W}
type=Artifact
subtype=Equipment
[/card]

[card]
name=Cryogen Relic
auto=@movedTo(this|myBattlefield):draw:1
auto=@movedTo(this|graveyard) from(battlefield):draw:1
text=When this artifact enters or leaves the battlefield, draw a card.
mana={1}{U}
type=Artifact
[/card]

[card]
name=Cryoshatter
target=creature|opponentbattlefield
auto=teach(creature) -5/-0
text=Enchant creature. Enchanted creature gets -5/-0. When enchanted creature becomes tapped or is dealt damage, destroy it. (Destroy trigger not supported)
mana={U}
type=Enchantment
subtype=Aura
[/card]

[card]
name=Faller's Faithful
auto=@movedTo(this|myBattlefield):bury target(creature|opponentbattlefield)
text=When this creature enters, destroy up to one other target creature.
mana={2}{B}
type=Creature
subtype=Human Wizard
power=3
toughness=1
[/card]

[card]
name=Hardlight Containment
auto=(blink)forsrc target(creature|opponentbattlefield)
text=When this Aura enters, exile target creature an opponent controls until this Aura leaves the battlefield.
mana={W}
type=Enchantment
[/card]

[card]
name=Hylderblade
auto={4}:equip
auto=teach(creature) +3/+1
text=Equipped creature gets +3/+1. Equip {4}
mana={B}
type=Artifact
subtype=Equipment
[/card]

[card]
name=Illvoi Infiltrator
auto=@combatdamaged(player) from(this):draw:1 controller
text=Whenever this creature deals combat damage to a player, draw a card.
mana={2}{U}
type=Creature
subtype=Jellyfish Rogue
power=1
toughness=3
[/card]

[card]
name=Kavaron Harrier
auto=@attacking(this):_ROBOTTOKEN_
text=Whenever this creature attacks, create a 2/2 colorless Robot artifact creature token.
mana={R}
type=Artifact Creature
subtype=Robot Soldier
power=2
toughness=1
[/card]

[card]
name=Lumen-Class Frigate
text=2+ | Other creatures you control get +1/+1. 12+ | Flying, lifelink. (Station not supported)
mana={1}{W}
type=Artifact Creature
subtype=Spacecraft
power=3
toughness=5
[/card]

[card]
name=Monoist Circuit-Feeder
abilities=flying
text=Flying.
mana={4}{B}{B}
type=Artifact Creature
subtype=Nautilus
power=4
toughness=4
[/card]

[card]
name=Secluded Starforge
auto={T}:Add{C}
auto={5}{T}:_ROBOTTOKEN_
text={T}: Add {C}. {5}, {T}: Create a 2/2 colorless Robot artifact creature token.
type=Land
[/card]

[card]
name=Specimen Freighter
auto=@movedTo(this|myBattlefield):bounce target(creature|opponentbattlefield)
text=When this Spacecraft enters, return up to one target creature to its owner's hand.
mana={5}{U}
type=Artifact Creature
subtype=Spacecraft
power=4
toughness=7
[/card]

[card]
name=Systems Override
auto=name(gain control) target(*|opponentbattlefield) transforms((,newability[moveTo(opponentbattlefield)],newability[@next end:moveTo(ownerbattlefield)],newability[untap],haste)) ueot
text=Gain control of target artifact or creature until end of turn. Untap that permanent. It gains haste until end of turn.
mana={2}{R}
type=Sorcery
[/card]

[card]
name=Terrapact Intimidator
auto=@movedTo(this|myBattlefield):_LANDERTOKEN_
auto=@movedTo(this|myBattlefield):_LANDERTOKEN_
text=When this creature enters, create two Lander tokens.
mana={1}{R}
type=Creature
subtype=Kavu Scout
power=2
toughness=1
[/card]

[card]
name=Virulent Silencer
auto=@combatdamaged(player) from(this):alterpoison:2 opponent
text=Whenever this creature deals combat damage to a player, that player gets two poison counters.
mana={3}
type=Artifact Creature
subtype=Robot Assassin
power=2
toughness=3
[/card]

[card]
name=Wedgelight Rammer
auto=@movedTo(this|myBattlefield):_ROBOTTOKEN_
text=When this Spacecraft enters, create a 2/2 colorless Robot artifact creature token.
mana={3}{W}
type=Artifact Creature
subtype=Spacecraft
power=3
toughness=4
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
            # Ensure exactly one [/card] at end
            full_block = re.sub(r'(\[/card\]\s*)+$', '', full_block).rstrip()
            full_block += '\n[/card]\n'
            cards.append((name.lower(), name, full_block))
    return cards


def main():
    with open(MTG_TXT, 'r', encoding='utf-8') as f:
        existing = f.read()

    # Extract header (everything before first [card])
    first_card_idx = existing.find('[card]')
    if first_card_idx == -1:
        print("ERROR: no [card] found in mtg.txt")
        return
    header = existing[:first_card_idx]

    # Parse existing cards
    existing_cards = parse_cards(existing)
    existing_names = {name_lower for name_lower, _, _ in existing_cards}
    print(f"Existing card blocks: {len(existing_cards)}")

    # Parse new cards
    new_cards = parse_cards(EOE_CARDS_B3)
    print(f"New cards to evaluate: {len(new_cards)}")

    # Filter out already-present cards
    to_add = []
    for name_lower, name, block in new_cards:
        if name_lower in existing_names:
            print(f"  SKIP (already exists): {name}")
        else:
            print(f"  ADD: {name}")
            to_add.append((name_lower, name, block))

    print(f"\nAdding {len(to_add)} new cards.")

    # Merge and sort all cards
    all_cards = existing_cards + to_add
    all_cards.sort(key=lambda x: x[0])

    # Reconstruct file
    rebuilt = header
    for _, _, block in all_cards:
        rebuilt += block

    # Clean up any accidental double [/card] tags
    rebuilt = re.sub(r'(\[/card\]\s*){2,}', '[/card]\n', rebuilt)

    with open(MTG_TXT, 'w', encoding='utf-8') as f:
        f.write(rebuilt)

    # Verify
    with open(MTG_TXT, 'r', encoding='utf-8') as f:
        verify = f.read()
    card_count = verify.count('[/card]')
    print(f"\nDone. [/card] tags in file: {card_count}")
    print(f"File size: {len(verify):,} bytes")


if __name__ == '__main__':
    main()
