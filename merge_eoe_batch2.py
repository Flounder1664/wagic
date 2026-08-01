#!/usr/bin/env python3
"""
Merge EOE Easy card primitives (Batch 2) alphabetically into mtg.txt.
Run from any directory; paths are absolute.
Batch 2 adds 52 new EOE cards not covered in Batch 1.
"""

import re, sys

MTG_TXT = r"M:\Claude_projects\wagic\projects\mtg\bin\Res\sets\primitives\mtg.txt"

# ---------------------------------------------------------------------------
# All EOE EASY Batch 2 card primitives (alphabetical by name)
# ---------------------------------------------------------------------------
EOE_CARDS_B2 = r"""
[card]
name=Adagia, Windswept Bastion
auto=@movedTo(this|myBattlefield):tap(noevent)
auto={T}:Add{W}
text=This land enters tapped. {T}: Add {W}.
type=Land
subtype=Planet
[/card]

[card]
name=Alpharael, Dreaming Acolyte
auto=draw:2
auto=discard:2
text=When Alpharael enters, draw two cards. Then discard two cards unless you discard an artifact card.
mana={1}{U}{B}
type=Legendary Creature
subtype=Human Cleric
power=2
toughness=3
[/card]

[card]
name=Beyond the Quiet
auto=bury all(creature)
text=Exile all creatures and Spacecraft. (Approximation: destroys all creatures.)
mana={3}{W}{W}
type=Sorcery
[/card]

[card]
name=Cerebral Download
auto=_SURVEIL3_
auto=draw:3
text=Surveil 3, then draw three cards. (Approximation: always surveil 3 regardless of artifact count.)
mana={4}{U}
type=Instant
[/card]

[card]
name=Command Bridge
auto=@movedTo(this|myBattlefield):tap(noevent)
auto={T}:_MANAOFANYCOLOR_
text=This land enters tapped. {T}: Add one mana of any color.
type=Land
[/card]

[card]
name=Dawnsire, Sunstar Dreadnought
text=Station -- Tap another creature you control: Put charge counters equal to its power on this Spacecraft. It's an artifact creature at 10+ and gains abilities at 10+ and 20+.
mana={5}
type=Legendary Artifact Creature
subtype=Spacecraft
power=20
toughness=20
[/card]

[card]
name=Debris Field Crusher
target=anytarget
auto=damage:3
text=When this Spacecraft enters, it deals 3 damage to any target.
mana={4}{R}
type=Artifact Creature
subtype=Spacecraft
power=1
toughness=5
[/card]

[card]
name=Desculpting Blast
target=*[-land]
auto=bounce
text=Return target nonland permanent to its owner's hand.
mana={1}{U}
type=Instant
[/card]

[card]
name=Divert Disaster
target=spell
auto=countertarget unless(pay:2)
text=Counter target spell unless its controller pays {2}. If they do, you create a Lander token.
mana={1}{U}
type=Instant
[/card]

[card]
name=Dockworker Drone
auto=counter(1/1)
auto=_DIES_counter(1/1) target(creature|mybattlefield)
text=This creature enters with a +1/+1 counter on it. When this creature dies, put a +1/+1 counter on target creature you control.
mana={1}{W}
type=Artifact Creature
subtype=Robot
power=1
toughness=1
[/card]

[card]
name=Dual-Sun Technique
target=creature|mybattlefield
auto=doublestrike ueot
text=Target creature you control gains double strike until end of turn. If it has a +1/+1 counter on it, draw a card.
mana={1}{W}
type=Instant
[/card]

[card]
name=Dubious Delicacy
abilities=flash
auto=power:-3 target(creature) ueot
auto=toughness:-3 target(creature) ueot
auto={2}{T}{S}:life:3
auto={2}{T}{S}:life:-3 target(player)
text=Flash. When this artifact enters, up to one target creature gets -3/-3 until end of turn. {2}, {T}, Sacrifice this artifact: You gain 3 life. {2}, {T}, Sacrifice this artifact: Target opponent loses 3 life.
mana={2}{B}
type=Artifact
subtype=Food
[/card]

[card]
name=Elegy Acolyte
abilities=lifelink
auto=@combatdamaged(player) from(this):draw:1 && life:-1 controller
auto=@endOfTurn(_):_ROBOTTOKEN_
text=Lifelink. Whenever one or more creatures you control deal combat damage to a player, you draw a card and lose 1 life. Void -- At the beginning of your end step, if a nonland permanent left the battlefield this turn or a spell was warped this turn, create a 2/2 colorless Robot artifact creature token.
mana={2}{B}{B}
type=Creature
subtype=Human Cleric
power=4
toughness=4
[/card]

[card]
name=Emergency Eject
target=*[-land]
auto=bury
text=Destroy target nonland permanent. Its controller creates a Lander token.
mana={2}{W}
type=Instant
[/card]

[card]
name=Fungal Colossus
text=This spell costs {X} less to cast, where X is the number of differently named lands you control.
mana={6}{G}
type=Creature
subtype=Fungus Beast
power=5
toughness=5
[/card]

[card]
name=Galvanizing Sawship
abilities=flying,haste
text=Station -- Tap another creature you control: Put charge counters on this Spacecraft. At 3+ counters: Flying, haste.
mana={5}{R}
type=Artifact Creature
subtype=Spacecraft
power=6
toughness=5
[/card]

[card]
name=Haliya, Ascendant Cadet
auto=counter(1/1) target(creature|mybattlefield)
auto=@attacking(this):counter(1/1) target(creature|mybattlefield)
auto=@combatdamaged(player) from(this):draw:1
text=Whenever Haliya enters or attacks, put a +1/+1 counter on target creature you control. Whenever one or more creatures you control with +1/+1 counters on them deal combat damage to a player, draw a card.
mana={2}{G}{W}{W}
type=Legendary Creature
subtype=Human Soldier
power=3
toughness=3
[/card]

[card]
name=Honored Knight-Captain
auto=_HUMANSOLDIERTOKEN_
text=When this creature enters, create a 1/1 white Human Soldier creature token.
mana={1}{W}
type=Creature
subtype=Human Advisor Knight
power=1
toughness=1
[/card]

[card]
name=Illvoi Light Jammer
abilities=flash
auto={3}:equip
auto=@movedTo(this|myBattlefield):hexproof ueot target(creature|mybattlefield)
auto=teach(creature) +1/+2
text=Flash. When this Equipment enters, attach it to target creature you control. That creature gains hexproof until end of turn. Equipped creature gets +1/+2. Equip {3}.
mana={1}{U}
type=Artifact
subtype=Equipment
[/card]

[card]
name=Kav Landseeker
abilities=menace
auto=_LANDERTOKEN_
text=Menace. When this creature enters, create a Lander token.
mana={3}{R}
type=Creature
subtype=Kavu Soldier
power=4
toughness=3
[/card]

[card]
name=Kavaron, Memorial World
auto=@movedTo(this|myBattlefield):tap(noevent)
auto={T}:Add{R}
text=This land enters tapped. {T}: Add {R}.
type=Land
subtype=Planet
[/card]

[card]
name=Larval Scoutlander
auto=_LANDERTOKEN_
auto=_LANDERTOKEN_
text=When this Spacecraft enters, you may sacrifice a land or Lander. If you do, search your library for up to two basic land cards, put them onto the battlefield tapped, then shuffle. (Approximation: creates two Lander tokens.)
mana={2}{G}
type=Artifact Creature
subtype=Spacecraft
power=3
toughness=3
[/card]

[card]
name=Lightless Evangel
auto=@movedTo(other creature,artifact|mygraveyard) from(mybattlefield):counter(1/1)
text=Whenever you sacrifice another creature or artifact, put a +1/+1 counter on this creature.
mana={1}{B}
type=Creature
subtype=Vampire Cleric
power=2
toughness=2
[/card]

[card]
name=Lithobraking
auto=_LANDERTOKEN_
auto=damage:2 all(creature)
text=Create a Lander token. Then you may sacrifice an artifact. When you do, Lithobraking deals 2 damage to each creature. (Approximation: always deals 2 damage to each creature.)
mana={2}{R}
type=Instant
[/card]

[card]
name=Lost in Space
target=artifact,creature
auto=bounce
auto=_SURVEIL1_
text=Target artifact or creature's owner puts it on top or bottom of their library. Surveil 1. (Approximation: returns to hand instead of library.)
mana={3}{U}
type=Instant
[/card]

[card]
name=Mechan Assembler
auto=@movedTo(other artifact|myBattlefield):_ROBOTTOKEN_
text=Whenever another artifact you control enters, create a 2/2 colorless Robot artifact creature token. This ability triggers only once each turn.
mana={4}{U}
type=Artifact Creature
subtype=Robot Artificer
power=4
toughness=4
[/card]

[card]
name=Mechan Shieldmate
abilities=defender
text=Defender. As long as an artifact entered the battlefield under your control this turn, this creature can attack as though it didn't have defender. (Approximation: permanent Defender, no conditional attack.)
mana={1}{U}
type=Artifact Creature
subtype=Robot Soldier
power=3
toughness=2
[/card]

[card]
name=Meltstrider's Resolve
auto=teach(creature) +0/+2
text=Enchant creature you control. When this Aura enters, enchanted creature fights up to one target creature an opponent controls. Enchanted creature gets +0/+2 and can't be blocked by more than one creature. (Approximation: only +0/+2 static bonus implemented.)
mana={G}
type=Enchantment
subtype=Aura
[/card]

[card]
name=Mm'menon, Uthros Exile
abilities=flying
auto=@movedTo(artifact|myBattlefield):counter(1/1) target(creature|mybattlefield)
text=Flying. Whenever an artifact you control enters, put a +1/+1 counter on target creature.
mana={1}{U}{R}
type=Legendary Creature
subtype=Jellyfish Advisor
power=1
toughness=3
[/card]

[card]
name=Mouth of the Storm
abilities=flying,ward:2
auto=power:-3 all(creature|opponentbattlefield) ueot
text=Flying. Ward {2}. When this creature enters, creatures your opponents control get -3/-0 until your next turn.
mana={6}{U}
type=Creature
subtype=Elemental
power=6
toughness=6
[/card]

[card]
name=Orbital Plunge
target=creature
auto=damage:6
text=Orbital Plunge deals 6 damage to target creature.
mana={3}{R}
type=Sorcery
[/card]

[card]
name=Pinnacle Kill-Ship
target=creature
auto=damage:10
text=When this Spacecraft enters, it deals 10 damage to up to one target creature.
mana={7}
type=Artifact Creature
subtype=Spacecraft
power=7
toughness=7
[/card]

[card]
name=Seam Rip
target=*[-land,manacost<=2]|opponentbattlefield
auto=(blink)forsrc
text=When this enchantment enters, exile target nonland permanent an opponent controls with mana value 2 or less until this enchantment leaves the battlefield.
mana={W}
type=Enchantment
[/card]

[card]
name=Seedship Impact
target=artifact,enchantment
auto=bury
text=Destroy target artifact or enchantment. If its mana value was 2 or less, create a Lander token.
mana={1}{G}
type=Instant
[/card]

[card]
name=Shattered Wings
target=artifact,enchantment,creature[flying]
auto=bury
auto=_SURVEIL1_
text=Destroy target artifact, enchantment, or creature with flying. Surveil 1.
mana={2}{G}
type=Sorcery
[/card]

[card]
name=Singularity Rupture
auto=bury all(creature)
text=Destroy all creatures, then any number of target players each mill half their library, rounded down. (Approximation: board wipe only; mill not implemented.)
mana={3}{U}{B}{B}
type=Sorcery
[/card]

[card]
name=Station Monitor
auto=@movedto(*|mystack) restriction{thisturn(*|mystack)~equalto~1}:_DRONETOKEN_
text=Whenever you cast your second spell each turn, create a 1/1 colorless Drone artifact creature token with flying.
mana={W}{U}
type=Creature
subtype=Lizard Artificer
power=2
toughness=2
[/card]

[card]
name=Steelswarm Operator
abilities=flying
auto={T}:Add{U}
text=Flying. {T}: Add {U}. Spend this mana only to cast an artifact spell. {T}: Add {U}{U}. Spend this mana only to activate abilities of artifact sources. (Approximation: unrestricted {U} tap.)
mana={1}{U}
type=Artifact Creature
subtype=Robot Soldier
power=1
toughness=1
[/card]

[card]
name=Susurian Dirgecraft
auto=sacrifice target(creature[-token]|opponentbattlefield)
text=When this Spacecraft enters, each opponent sacrifices a nontoken creature of their choice.
mana={4}{B}
type=Artifact Creature
subtype=Spacecraft
power=4
toughness=3
[/card]

[card]
name=Sunset Saboteur
abilities=menace
auto=@attacking(this):counter(1/1) target(creature|opponentbattlefield)
text=Menace. Ward -- Discard a card. Whenever this creature attacks, put a +1/+1 counter on target creature an opponent controls.
mana={1}{B}
type=Creature
subtype=Human Rogue
power=4
toughness=1
[/card]

[card]
name=Survey Mechan
abilities=flying,hexproof
text=Flying. Hexproof. {10}, Sacrifice: Deal 3 damage to any target. Target player draws three cards and gains 3 life. This ability costs {X} less where X is the number of differently named lands you control.
mana={4}
type=Artifact Creature
subtype=Robot
power=1
toughness=3
[/card]

[card]
name=Susur Secundi, Void Altar
auto=@movedTo(this|myBattlefield):tap(noevent)
auto={T}:Add{B}
text=This land enters tapped. {T}: Add {B}.
type=Land
subtype=Planet
[/card]

[card]
name=Syr Vondam, the Lucent
abilities=deathtouch,lifelink
auto=deathtouch ueot all(other creature|mybattlefield)
auto=@attacking(this):deathtouch ueot all(other creature|mybattlefield)
text=Deathtouch, lifelink. Whenever Syr Vondam enters or attacks, other creatures you control get +1/+0 and gain deathtouch until end of turn.
mana={2}{W}{B}{B}
type=Legendary Creature
subtype=Human Knight
power=4
toughness=4
[/card]

[card]
name=Tannuk, Memorial Ensign
auto=_LANDFALL_damage:1 opponent
text=Landfall -- Whenever a land you control enters, Tannuk deals 1 damage to each opponent.
mana={1}{R}{G}
type=Legendary Creature
subtype=Kavu Pilot
power=2
toughness=4
[/card]

[card]
name=Temporal Intervention
target=player
auto=discard:1
text=Void -- This spell costs {2} less to cast if a nonland permanent left the battlefield this turn or a spell was warped this turn. Target opponent reveals their hand. You choose a nonland card from it. That player discards that card.
mana={2}{B}
type=Sorcery
[/card]

[card]
name=The Eternity Elevator
auto={T}:Add{C}{C}{C}
text={T}: Add {C}{C}{C}. Station -- Tap another creature you control: Put charge counters on this Spacecraft.
mana={5}
type=Legendary Artifact
subtype=Spacecraft
[/card]

[card]
name=The Seriema
auto=moveto(myhand) target(creature[legendary]|mylibrary) && shuffle
text=When The Seriema enters, search your library for a legendary creature card, reveal it, put it into your hand, then shuffle. Station. 7+ | Flying. Other tapped legendary creatures you control have indestructible.
mana={1}{W}{W}
type=Legendary Artifact Creature
subtype=Spacecraft
power=5
toughness=5
[/card]

[card]
name=Thaumaton Torpedo
auto={6}{T}{S}:bury target(*[-land])
text={6}, {T}, Sacrifice this artifact: Destroy target nonland permanent. This ability costs {3} less if you attacked with a Spacecraft this turn.
mana={1}
type=Artifact
[/card]

[card]
name=Umbral Collar Zealot
auto={S}:_SURVEIL1_
text=Sacrifice another creature or artifact: Surveil 1.
mana={1}{B}
type=Creature
subtype=Human Cleric
power=3
toughness=2
[/card]

[card]
name=Uthros Scanship
auto=draw:2
auto=discard:1
text=When this Spacecraft enters, draw two cards, then discard a card.
mana={3}{U}
type=Artifact Creature
subtype=Spacecraft
power=4
toughness=4
[/card]

[card]
name=Wurmwall Sweeper
auto=_SURVEIL2_
text=When this Spacecraft enters, surveil 2.
mana={2}
type=Artifact Creature
subtype=Spacecraft
power=2
toughness=2
[/card]
"""

# ---------------------------------------------------------------------------
# Parse a block of [card]...[/card] text into list of (name_lower, name, block)
# ---------------------------------------------------------------------------
def parse_cards(text):
    cards = []
    # Split on [card] boundary (keep the delimiter out)
    blocks = re.split(r'\[card\]\s*\n', text)
    for block in blocks[1:]:          # first chunk is preamble/blank
        # strip trailing whitespace but keep the [/card] tag
        block = block.rstrip()
        name_match = re.search(r'^name=(.+)$', block, re.MULTILINE)
        if name_match:
            name = name_match.group(1).strip()
            full_block = '[card]\n' + block + ('\n' if not block.endswith('\n') else '')
            # ensure [/card] is present exactly once at the end
            if not full_block.rstrip().endswith('[/card]'):
                full_block = full_block.rstrip() + '\n[/card]\n'
            else:
                full_block = full_block.rstrip() + '\n'
            cards.append((name.lower(), name, full_block))
    return cards


def main():
    print(f"Reading {MTG_TXT} ...")
    with open(MTG_TXT, 'r', encoding='utf-8') as f:
        original = f.read()

    existing = parse_cards(original)
    print(f"  Existing cards parsed: {len(existing)}")

    new_cards = parse_cards(EOE_CARDS_B2)
    print(f"  New Batch-2 cards to insert: {len(new_cards)}")

    # Build a set of existing names (lower) to avoid duplicates
    existing_names = {name_lower for name_lower, _, _ in existing}
    to_insert = [(nl, n, b) for nl, n, b in new_cards if nl not in existing_names]
    skipped   = [(nl, n, b) for nl, n, b in new_cards if nl in existing_names]

    if skipped:
        print(f"  Skipping {len(skipped)} already-present cards:")
        for nl, n, _ in skipped:
            print(f"    - {n}")

    print(f"  Inserting {len(to_insert)} new cards ...")

    # Merge and sort
    all_cards = existing + to_insert
    all_cards.sort(key=lambda x: x[0])

    # Find where the card blocks start in the original file
    first_card_pos = original.find('[card]')
    preamble = original[:first_card_pos]

    # Reconstruct the file
    rebuilt = preamble + ''.join(block for _, _, block in all_cards)

    # --- Safety: remove any accidental double [/card] sequences ---
    before_cleanup = rebuilt.count('[/card]')
    rebuilt = re.sub(r'(\[/card\]\s*){2,}', '[/card]\n', rebuilt)
    after_cleanup = rebuilt.count('[/card]')
    if before_cleanup != after_cleanup:
        print(f"  Cleaned up double [/card] tags: {before_cleanup} -> {after_cleanup}")

    print(f"Writing {MTG_TXT} ...")
    with open(MTG_TXT, 'w', encoding='utf-8') as f:
        f.write(rebuilt)

    final_cards = rebuilt.count('[/card]')
    print(f"Done. Total [/card] blocks in file: {final_cards}")
    print(f"Successfully inserted {len(to_insert)} Batch-2 EOE cards.")


if __name__ == '__main__':
    main()
