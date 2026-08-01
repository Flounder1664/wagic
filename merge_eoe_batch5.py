#!/usr/bin/env python3
"""
Merge EOE Batch 5 primitives into mtg.txt.
~15 remaining MEDIUM EOE cards (warp stripped, effects simplified).
"""
import re

MTG_TXT = r"M:\Claude_projects\wagic\projects\mtg\bin\Res\sets\primitives\mtg.txt"

EOE_CARDS_B5 = r"""
[card]
name=All-Fates Stalker
auto=(blink)forsrc target(creature|opponentbattlefield)
text=When this creature enters, exile up to one target creature an opponent controls until this creature leaves the battlefield.
mana={3}{W}
type=Creature
subtype=Drix Assassin
power=2
toughness=3
[/card]

[card]
name=Haliya, Guided by Light
auto=@movedTo(creature,artifact|mybattlefield):life:1
text=Whenever Haliya or another creature or artifact you control enters, you gain 1 life.
mana={2}{W}
type=Legendary Creature
subtype=Human Soldier
power=3
toughness=3
[/card]

[card]
name=Mechanozoa
auto=@movedTo(this|myBattlefield):tap target(*[artifact;creature]|opponentbattlefield)
text=When this creature enters, tap target artifact or creature an opponent controls.
mana={4}{U}{U}
type=Artifact Creature
subtype=Robot Jellyfish
power=5
toughness=5
[/card]

[card]
name=Perigee Beckoner
auto=@movedTo(this|myBattlefield):pump(2/0) target(creature|mybattlefield) ueot
text=When this creature enters, until end of turn, another target creature you control gets +2/+0.
mana={4}{B}
type=Creature
subtype=Horror
power=4
toughness=5
[/card]

[card]
name=Quantum Riddler
abilities=flying
auto=@movedTo(this|myBattlefield):draw:1
text=Flying. When this creature enters, draw a card.
mana={3}{U}{U}
type=Creature
subtype=Sphinx
power=4
toughness=6
[/card]

[card]
name=Reroute Systems
auto=indestructible target(*[artifact;creature]|mybattlefield) ueot
text=Target artifact or creature you control gains indestructible until end of turn.
mana={W}
type=Instant
[/card]

[card]
name=Scrounge for Eternity
auto=moveto(mybattlefield) target(creature|mygraveyard) where(converted<=5) && _LANDERTOKEN_
text=As an additional cost to cast this spell, sacrifice an artifact or creature. Return target creature card with mana value 5 or less from your graveyard to the battlefield. Then create a Lander token.
mana={2}{B}{S(artifact,creature|mybattlefield)}
type=Sorcery
[/card]

[card]
name=Starfield Shepherd
abilities=flying
text=Flying. When this creature enters, search your library for a basic Plains card or a creature card with mana value 1 or less. (Search not supported)
mana={3}{W}{W}
type=Creature
subtype=Angel
power=3
toughness=2
[/card]

[card]
name=Starwinder
auto=@combatdamaged(player) from(creature|mybattlefield):may draw:1 controller
text=Whenever a creature you control deals combat damage to a player, you may draw a card.
mana={5}{U}{U}
type=Creature
subtype=Leviathan
power=7
toughness=7
[/card]

[card]
name=Tannuk, Steadfast Second
auto=all(other creature|mybattlefield) haste
text=Other creatures you control have haste.
mana={2}{R}{R}
type=Legendary Creature
subtype=Kavu Pilot
power=3
toughness=5
[/card]

[card]
name=Timeline Culler
abilities=haste
text=Haste.
mana={B}{B}
type=Creature
subtype=Drix Warlock
power=2
toughness=2
[/card]

[card]
name=Vaultguard Trooper
auto=@each my end:draw:2
text=At the beginning of your end step, draw two cards.
mana={4}{R}
type=Creature
subtype=Kavu Soldier
power=5
toughness=5
[/card]

[card]
name=Weftstalker Ardent
auto=@movedTo(other creature|mybattlefield):damage:1 all(opponent)
text=Whenever another creature or artifact you control enters, this creature deals 1 damage to each opponent.
mana={2}{R}
type=Creature
subtype=Drix Artificer
power=2
toughness=3
[/card]
"""


def parse_cards(text):
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

    new_cards = parse_cards(EOE_CARDS_B5)
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
