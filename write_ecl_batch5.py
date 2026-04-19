primitives = """
[card]
name=Abigale, Eloquent First-Year
abilities=flying,first strike,lifelink
auto=@movedTo(this|mybattlefield):target(creature[-this]|mybattlefield) effect(+0/+0) ueot
mana={W/B}{W/B}
type=Creature
subtype=Bird Bard
power=1
toughness=1
text=Flying, first strike, lifelink -- When Abigale enters, another target creature gains flying, first strike, and lifelink until end of turn.
[/card]

[card]
name=Adept Watershaper
auto=all(creature[-this]|mybattlefield):abilities=indestructible
mana={2}{W}
type=Creature
subtype=Merfolk Cleric
power=3
toughness=4
text=Other creatures you control have indestructible.
[/card]

[card]
name=Ashling, Rekindled
auto=@movedTo(this|mybattlefield):choice name(loot) discard:1 && draw:1 name(pass)
mana={1}{R}
type=Creature
subtype=Elemental Sorcerer
power=1
toughness=3
text=When this creature enters, you may discard a card. If you do, draw a card.
[/card]

[card]
name=Aurora Awakener
abilities=trample
auto=@movedTo(this|mybattlefield):moveto(mybattlefield) target(creature[manacost<=4]|mylibrary)
mana={6}{G}
type=Creature
subtype=Giant Druid
power=7
toughness=7
text=Trample -- When this creature enters, you may put a creature card with mana value 4 or less from the top of your library onto the battlefield.
[/card]

[card]
name=Blighted Blackthorn
auto=@movedTo(this|mybattlefield):choice name(blight 2) counter(-1/-1,2) && draw:1 && life:-1 controller name(skip)
auto=@attacking(this):choice name(blight 2) counter(-1/-1,2) && draw:1 && life:-1 controller name(skip)
mana={4}{B}
type=Creature
subtype=Treefolk Warlock
power=3
toughness=7
text=Whenever this creature enters or attacks, you may blight 2. If you do, draw a card and lose 1 life.
[/card]

[card]
name=Bre of Clan Stoutarm
auto={1}{W}{T}:target(creature[-this]|mybattlefield) effect(+0/+0,flying,lifelink) ueot
mana={2}{R}{W}
type=Creature
subtype=Giant Warrior
power=4
toughness=4
text={1}{W}, {T}: Another target creature you control gains flying and lifelink until end of turn.
[/card]

[card]
name=Brigid, Clachan's Heart
auto=@movedTo(this|mybattlefield):token(Kithkin,creature kithkin,1/1,green white)
mana={2}{W}
type=Creature
subtype=Kithkin Warrior
power=3
toughness=2
text=Whenever this creature enters, create a 1/1 green and white Kithkin creature token.
[/card]

[card]
name=Bristlebane Outrider
mana={3}{G}
type=Creature
subtype=Kithkin Knight
power=3
toughness=5
text=This creature can't be blocked by creatures with power 2 or less.
[/card]

[card]
name=Catharsis
auto=@movedTo(this|mybattlefield):choice name(kithkin) token(Kithkin,creature kithkin,1/1,green white) && token(Kithkin,creature kithkin,1/1,green white) name(haste) all(creature|mybattlefield) effect(+1/+1,haste) ueot
abilities=evoke{R/W}{R/W}
mana={4}{R/W}{R/W}
type=Creature
subtype=Elemental Incarnation
power=3
toughness=4
text=When this creature enters, choose: create two 1/1 Kithkin tokens; or creatures you control get +1/+1 and haste until end of turn. Evoke {R/W}{R/W}.
[/card]

[card]
name=Champion of the Clachan
abilities=flash
auto=all(creature[kithkin][-this]|mybattlefield):effect(+1/+1)
mana={3}{W}
type=Creature
subtype=Kithkin Knight
power=4
toughness=5
text=Flash -- Other Kithkin you control get +1/+1.
[/card]

[card]
name=Champion of the Path
auto=@movedTo(creature[elemental][-this]|mybattlefield):damage:* target(player|opponentbattlefield)
mana={3}{R}
type=Creature
subtype=Elemental Sorcerer
power=7
toughness=3
text=Whenever another Elemental you control enters, it deals damage equal to its power to each opponent.
[/card]

[card]
name=Champion of the Weird
auto={B}:counter(-1/-1,2) && target(player|opponentbattlefield) counter(-1/-1,2) asSorcery
mana={3}{B}
type=Creature
subtype=Goblin Berserker
power=5
toughness=5
text=Pay 1 life, Blight 2: Target opponent blights 2. Activate only as a sorcery.
[/card]

[card]
name=Champions of the Perfect
auto=@movedTo(creature|myCastingzone):draw:1
mana={3}{G}
type=Creature
subtype=Elf Warrior
power=6
toughness=6
text=Whenever you cast a creature spell, draw a card.
[/card]

[card]
name=Champions of the Shoal
auto=@movedTo(this|mybattlefield):tap target(creature|opponentbattlefield)
auto=@tapped(this):tap target(creature|opponentbattlefield)
mana={3}{U}
type=Creature
subtype=Merfolk Soldier
power=4
toughness=6
text=Whenever this creature enters or becomes tapped, tap up to one target creature an opponent controls.
[/card]

[card]
name=Chaos Spewer
auto=@movedTo(this|mybattlefield):choice name(pay) effect(+0/+0) name(blight 2) counter(-1/-1,2)
mana={2}{B/R}
type=Creature
subtype=Goblin Warlock
power=5
toughness=4
text=When this creature enters, you may pay {2}. If you do not, blight 2.
[/card]

[card]
name=Curious Colossus
auto=@movedTo(this|mybattlefield):all(creature|opponentbattlefield) effect(-10/-10) ueot
mana={5}{W}{W}
type=Creature
subtype=Giant Warrior
power=7
toughness=7
text=When this creature enters, each creature target opponent controls becomes a 1/1 creature.
[/card]

[card]
name=Dawnhand Dissident
auto={T}{C(-1/-1,1)}:_SCRY1_
auto={T}{C(-1/-1,1)}{C(-1/-1,1)}:moveto(exile) target(*|graveyard)
mana={B}
type=Creature
subtype=Elf Warlock
power=1
toughness=2
text={T}, Blight 1: Surveil 1. -- {T}, Blight 2: Exile target card from a graveyard.
[/card]

[card]
name=Deceit
auto=@movedTo(this|mybattlefield):choice name(bounce) moveto(myhand) target(*[-land]|opponentbattlefield) name(discard) discard:1 target(player|opponentbattlefield)
abilities=evoke{U/B}{U/B}
mana={4}{U/B}{U/B}
type=Creature
subtype=Elemental Incarnation
power=5
toughness=5
text=When this creature enters, choose: return target nonland permanent to hand; or target opponent discards a card. Evoke {U/B}{U/B}.
[/card]

[card]
name=Deepway Navigator
abilities=flash
auto=@movedTo(this|mybattlefield):untap all(creature[merfolk][-this]|mybattlefield)
mana={W}{U}
type=Creature
subtype=Merfolk Wizard
power=2
toughness=2
text=Flash -- When this creature enters, untap each other Merfolk you control.
[/card]

[card]
name=Doran, Besieged by Time
mana={1}{W}{B}{G}
type=Creature
subtype=Treefolk Druid
power=0
toughness=5
text=Each creature spell you cast with toughness greater than its power costs {1} less. Creatures you control get +X/+X when attacking, where X is the difference between toughness and power.
[/card]

[card]
name=Eirdu, Carrier of Dawn
abilities=flying,lifelink,convoke
mana={3}{W}{W}
type=Creature
subtype=Elemental God
power=5
toughness=5
text=Flying, lifelink -- Creature spells you cast have convoke.
[/card]

[card]
name=Emptiness
auto=@movedTo(this|mybattlefield):choice name(reanimate) moveto(mybattlefield) target(creature[manacost<=3]|mygraveyard) name(wither) counter(-1/-1,3) target(creature|opponentbattlefield)
abilities=evoke{W/B}{W/B}
mana={4}{W/B}{W/B}
type=Creature
subtype=Elemental Incarnation
power=3
toughness=5
text=When this creature enters, choose: return target creature mana value 3 or less from graveyard to battlefield; or put three -1/-1 counters on a creature. Evoke {W/B}{W/B}.
[/card]

[card]
name=Explosive Prodigy
auto=@movedTo(this|mybattlefield):damage:3 target(creature|opponentbattlefield)
mana={1}{R}
type=Creature
subtype=Elemental Sorcerer
power=1
toughness=1
text=When this creature enters, it deals 3 damage to target creature an opponent controls.
[/card]

[card]
name=Figure of Fable
auto=this(variable{hascntlevel}=0) {G/W}:name(Scout) counter(0/0,1,Level) asSorcery
auto=this(variable{hascntlevel}=1) {1}{G/W}{G/W}:name(Soldier) counter(0/0,1,Level) asSorcery
auto=this(variable{hascntlevel}=2) {3}{G/W}{G/W}{G/W}:name(Avatar) counter(0/0,1,Level) asSorcery
auto=restriction{compare(hascntlevel)~equalto~0}:+1/+1
auto=restriction{compare(hascntlevel)~equalto~1}:+3/+4
auto=restriction{compare(hascntlevel)~equalto~2}:+6/+7
auto=counter(0/0,1,Level)
mana={G/W}
type=Creature
subtype=Kithkin
power=1
toughness=1
text={G/W}: Becomes a 2/3 Kithkin Scout. -- {1}{G/W}{G/W}: Becomes a 4/5 Kithkin Soldier. -- {3}{G/W}{G/W}{G/W}: Becomes a 7/8 Kithkin Avatar.
[/card]

[card]
name=Flitterwing Nuisance
abilities=flying
auto=@movedTo(this|mybattlefield):counter(-1/-1,1)
mana={U}
type=Creature
subtype=Faerie Rogue
power=2
toughness=2
text=Flying -- This creature enters with a -1/-1 counter on it.
[/card]

[card]
name=Glister Bairn
auto=@each my combat:target(creature[-this]|mybattlefield) effect(+3/+3) ueot
mana={2}{G/U}{G/U}{G/U}
type=Creature
subtype=Ouphe
power=1
toughness=4
text=At the beginning of combat on your turn, another target creature you control gets +3/+3 until end of turn.
[/card]

[card]
name=Gloom Ripper
auto=@movedTo(this|mybattlefield):target(creature|mybattlefield) effect(+4/+0) ueot && target(creature|opponentbattlefield) effect(-0/-4) ueot
mana={3}{B}{B}
type=Creature
subtype=Elf Assassin
power=4
toughness=4
text=When this creature enters, target creature you control gets +4/+0 until end of turn and target creature an opponent controls gets -4/-0 until end of turn.
[/card]

[card]
name=Goliath Daydreamer
auto=@attacking(this):moveto(myCastingzone) target(*|myexile)
mana={2}{R}{R}
type=Creature
subtype=Giant Wizard
power=4
toughness=4
text=When this creature attacks, you may cast a spell from among cards you own in exile without paying its mana cost.
[/card]

[card]
name=Gravelgill Scoundrel
abilities=vigilance
mana={1}{U}
type=Creature
subtype=Merfolk Rogue
power=1
toughness=3
text=Vigilance -- Whenever this creature attacks, you may tap another creature you control. If you do, this creature is unblockable this turn.
[/card]

[card]
name=Grub, Storied Matriarch
abilities=menace
auto=@movedTo(this|mybattlefield):moveto(myhand) target(creature[goblin]|mygraveyard)
mana={2}{B}
type=Creature
subtype=Goblin Warlock
power=2
toughness=1
text=Menace -- When this creature enters, return up to one target Goblin card from your graveyard to your hand.
[/card]

[card]
name=Kirol, Attentive First-Year
mana={1}{R/W}{R/W}
type=Creature
subtype=Vampire Cleric
power=3
toughness=3
text=Tap two untapped creatures you control: Copy target triggered ability you control. Activate only once each turn.
[/card]

[card]
name=Kithkeeper
auto=@movedTo(this|mybattlefield):token(Kithkin,creature kithkin,1/1,green white) && token(Kithkin,creature kithkin,1/1,green white) && token(Kithkin,creature kithkin,1/1,green white)
auto={T}{T}{T}:this effect(+3/+0,flying) ueot
mana={6}{W}
type=Creature
subtype=Elemental
power=3
toughness=3
text=When this creature enters, create three 1/1 green and white Kithkin creature tokens. -- Tap three creatures: This creature gets +3/+0 and gains flying until end of turn.
[/card]

[card]
name=Luminollusk
abilities=deathtouch
auto=@movedTo(this|mybattlefield):life:3 controller
mana={3}{G}
type=Creature
subtype=Elemental
power=2
toughness=4
text=Deathtouch -- When this creature enters, you gain 3 life.
[/card]

[card]
name=Maralen, Fae Ascendant
abilities=flying
auto=@movedTo(creature|mybattlefield):mill:2 target(player|opponentbattlefield)
mana={2}{B}{G}{U}
type=Creature
subtype=Elf Faerie Noble
power=4
toughness=5
text=Flying -- Whenever an Elf or Faerie you control enters, mill two cards of target opponent.
[/card]

[card]
name=Mutable Explorer
abilities=changeling
mana={2}{G}
type=Creature
subtype=Shapeshifter
power=1
toughness=1
text=Changeling (This card is every creature type.)
[/card]

[card]
name=Omni-Changeling
abilities=changeling,convoke
mana={3}{U}{U}
type=Creature
subtype=Shapeshifter
power=0
toughness=0
text=Changeling -- Convoke.
[/card]

[card]
name=Prismabasher
abilities=trample
auto=@movedTo(this|mybattlefield):all(creature|mybattlefield) effect(+3/+3) ueot
mana={4}{G}{G}
type=Creature
subtype=Elemental
power=6
toughness=6
text=Trample -- When this creature enters, creatures you control get +3/+3 until end of turn.
[/card]

[card]
name=Sanar, Innovative First-Year
auto=@each my mainphase:draw:1
mana={2}{U/R}{U/R}
type=Creature
subtype=Goblin Sorcerer
power=2
toughness=4
text=At the beginning of your first main phase, draw a card.
[/card]

[card]
name=Shimmercreep
abilities=menace
auto=@movedTo(this|mybattlefield):life:-3 target(player|opponentbattlefield) && life:3 controller
mana={4}{B}
type=Creature
subtype=Elemental
power=3
toughness=5
text=Menace -- When this creature enters, each opponent loses 3 life and you gain 3 life.
[/card]

[card]
name=Shinestriker
abilities=flying
auto=@movedTo(this|mybattlefield):draw:3
mana={4}{U}{U}
type=Creature
subtype=Elemental
power=3
toughness=3
text=Flying -- When this creature enters, draw three cards.
[/card]

[card]
name=Squawkroaster
abilities=double strike
mana={3}{R}
type=Creature
subtype=Elemental
power=4
toughness=4
text=Double strike.
[/card]

[card]
name=Sygg, Wanderwine Wisdom
mana={1}{U}
type=Creature
subtype=Merfolk Wizard
power=2
toughness=2
text=Sygg cannot be blocked. -- When this creature enters, target creature you control gains "Whenever this creature deals combat damage to a player, draw a card" until end of turn.
[/card]

[card]
name=Taster of Wares
auto=@movedTo(this|mybattlefield):target(player|opponentbattlefield) discard:1
mana={2}{B}
type=Creature
subtype=Goblin Warlock
power=3
toughness=2
text=When this creature enters, target opponent discards a card.
[/card]

[card]
name=Trystan, Callous Cultivator
abilities=deathtouch
auto=@movedTo(this|mybattlefield):mill:3 && life:2 controller
mana={2}{G}
type=Creature
subtype=Elf Druid
power=3
toughness=4
text=Deathtouch -- When this creature enters, mill three cards and gain 2 life.
[/card]

[card]
name=Twinflame Travelers
abilities=flying
mana={2}{U}{R}
type=Creature
subtype=Elemental Sorcerer
power=3
toughness=3
text=Flying -- If a triggered ability of another Elemental you control triggers, it triggers an additional time.
[/card]

[card]
name=Barbed Bloodletter
abilities=flash
auto=equipped(this):+1/+2
auto={2}:equip target(creature|mybattlefield)
mana={1}{B}
type=Artifact
subtype=Equipment
text=Flash -- Equipped creature gets +1/+2. Equip {2}.
[/card]

[card]
name=Bark of Doran
auto=equipped(this):+0/+1
auto={1}:equip target(creature|mybattlefield)
mana={1}{W}
type=Artifact
subtype=Equipment
text=Equipped creature gets +0/+1. Equip {1}.
[/card]

[card]
name=Chronicle of Victory
mana={6}
type=Artifact
text=As this enters, choose a creature type. Creatures you control of the chosen type get +2/+2 and have first strike and trample. Whenever you cast a spell of the chosen type, draw a card.
[/card]

[card]
name=Dawn-Blessed Pennant
auto=@movedTo(*|mybattlefield):life:1 controller
auto={2}{T}:moveto(myhand) target(*|mygraveyard)
mana={1}
type=Artifact
text=Whenever a permanent you control enters, you gain 1 life. -- {2}, {T}, Sacrifice this: Return target card from your graveyard to your hand.
[/card]

[card]
name=Foraging Wickermaw
auto=@movedTo(this|mybattlefield):_SCRY1_
auto={1}:Add{W}
auto={1}:Add{U}
auto={1}:Add{B}
auto={1}:Add{R}
auto={1}:Add{G}
mana={2}
type=Artifact Creature
subtype=Scarecrow
power=1
toughness=3
text=When this creature enters, surveil 1. -- {1}: Add one mana of any color.
[/card]

[card]
name=Gathering Stone
auto=@each my upkeep:_SCRY1_
mana={4}
type=Artifact
text=Spells you cast of the chosen type cost {1} less. At the beginning of your upkeep, surveil 1.
[/card]

[card]
name=Mirrormind Crown
auto=equipped(this):+0/+0
auto={2}:equip target(creature|mybattlefield)
mana={4}
type=Artifact
subtype=Equipment
text=The first time you create tokens each turn, you may instead create that many tokens that are copies of equipped creature. Equip {2}.
[/card]

[card]
name=Puca's Eye
auto=@movedTo(this|mybattlefield):draw:1
auto={3}{T}:draw:1
mana={2}
type=Artifact
text=When this artifact enters, draw a card. -- {3}, {T}: Draw a card.
[/card]

[card]
name=Rimefire Torque
auto=@movedTo(*|mybattlefield):counter(charge,1)
auto={T}{C(charge,-3)}:copy target(spell|stack)
mana={1}{U}
type=Artifact
text=Whenever a permanent you control enters, put a charge counter on this. -- {T}, Remove three charge counters: Copy target instant or sorcery spell.
[/card]

[card]
name=Stalactite Dagger
auto=@movedTo(this|mybattlefield):token(Shapeshifter,creature shapeshifter,1/1,colorless)
auto=equipped(this):+1/+1
auto={2}:equip target(creature|mybattlefield)
mana={2}
type=Artifact
subtype=Equipment
text=When this Equipment enters, create a 1/1 colorless Shapeshifter creature token with changeling. -- Equipped creature gets +1/+1. Equip {2}.
[/card]

[card]
name=Assert Perfection
auto=target(creature|mybattlefield) effect(+1/+0) ueot
mana={1}{G}
type=Sorcery
text=Target creature you control gets +1/+0 until end of turn. It deals damage equal to its power to up to one target creature an opponent controls.
[/card]

[card]
name=Auntie's Sentence
auto=choice name(discard) target(player|opponentbattlefield) discard:1 name(weaken) target(creature|opponentbattlefield) effect(-2/-2) ueot
mana={1}{B}
type=Sorcery
text=Choose one: target opponent discards a card; or target creature gets -2/-2 until end of turn.
[/card]

[card]
name=Bloodline Bidding
abilities=convoke
auto=moveto(mybattlefield) target(creature|mygraveyard) && moveto(mybattlefield) target(creature|mygraveyard)
mana={6}{B}{B}
type=Sorcery
text=Convoke -- Return up to two creature cards from your graveyard to the battlefield.
[/card]

[card]
name=Bogslither's Embrace
auto=moveto(exile) target(creature|opponentbattlefield)
mana={1}{B}
type=Sorcery
text=As an additional cost to cast this spell, blight 1 or pay {3}. Exile target creature.
[/card]

[card]
name=Boulder Dash
auto=damage:2 target(any) && damage:1 target(any)
mana={1}{R}
type=Sorcery
text=Boulder Dash deals 2 damage to any target and 1 damage to any other target.
[/card]

[card]
name=Burning Curiosity
auto=choice name(blight 1) counter(-1/-1,1) && draw:1 && draw:1 && draw:1 name(skip) draw:1 && draw:1
mana={2}{R}
type=Sorcery
text=As an additional cost, you may blight 1. Exile the top two cards of your library (three if you blighted). You may play those cards until your next turn ends.
[/card]

[card]
name=Celestial Reunion
auto=moveto(myhand) target(creature|mylibrary)
mana={X}{G}
type=Sorcery
text=Search your library for a creature card with mana value X or less, reveal it, put it into your hand, then shuffle.
[/card]

[card]
name=Cinder Strike
auto=choice name(blight 1) counter(-1/-1,1) && damage:4 target(creature|any) name(skip) damage:2 target(creature|any)
mana={R}
type=Sorcery
text=As an additional cost, you may blight 1. Cinder Strike deals 2 damage to target creature (4 damage instead if you blighted).
[/card]

[card]
name=Darkness Descends
auto=all(*|mybattlefield) counter(-1/-1,2) && all(*|opponentbattlefield) counter(-1/-1,2)
mana={2}{B}{B}
type=Sorcery
text=Put two -1/-1 counters on each creature.
[/card]

[card]
name=Dream Harvest
auto=draw:3 && target(player|opponentbattlefield) discard:3
mana={5}{U/B}{U/B}
type=Sorcery
text=Draw three cards. Each opponent discards three cards.
[/card]

[card]
name=Impolite Entrance
auto=target(creature|mybattlefield) effect(+0/+0,trample,haste) ueot && draw:1
mana={R}
type=Sorcery
text=Target creature gains trample and haste until end of turn. Draw a card.
[/card]

[card]
name=Morningtide's Light
auto=moveto(exile) target(creature|opponentbattlefield) && moveto(opponentbattlefield) target(creature|myexile)
mana={3}{W}
type=Sorcery
text=Exile any number of target creatures. At the beginning of the next end step, return those cards to the battlefield tapped.
[/card]

[card]
name=Perfect Intimidation
auto=choice name(exile) moveto(exile) target(*[-land]|opponenthand) && moveto(exile) target(*[-land]|opponenthand) name(counters) target(creature|opponentbattlefield) effect(-10/-0) ueot
mana={3}{B}
type=Sorcery
text=Choose one: target opponent exiles two cards from their hand; or remove all counters from target creature.
[/card]

[card]
name=Soul Immolation
auto=counter(-1/-1,3) && damage:3 target(player|opponentbattlefield) && all(creature|opponentbattlefield) damage:3
mana={3}{R}{R}
type=Sorcery
text=As an additional cost, blight X. Soul Immolation deals X damage to each opponent and each creature they control.
[/card]

[card]
name=Spry and Mighty
auto=draw:3 && all(creature|mybattlefield) effect(+3/+3,trample) ueot
mana={4}{G}
type=Sorcery
text=Draw three cards. Creatures you control get +3/+3 and gain trample until end of turn.
[/card]

[card]
name=Tend the Sprigs
auto=moveto(mybattlefield) target(land[basic]|mylibrary) && token(Treefolk,creature treefolk,3/4,reach green)
mana={2}{G}
type=Sorcery
text=Search your library for a basic land card, put it onto the battlefield tapped, then shuffle. Then create a 3/4 green Treefolk creature token with reach.
[/card]

[card]
name=Winnowing
abilities=convoke
auto=all(creature|opponentbattlefield) moveto(mygraveyard)
mana={4}{W}{W}
type=Sorcery
text=Convoke -- Each opponent sacrifices all but one creature they control.
[/card]

[card]
name=Ashling's Command
auto=choice name(copy) copy target(creature[elemental]|mybattlefield) name(draw) draw:2 name(damage) all(creature|opponentbattlefield) damage:2 name(treasure) _TREASURE_ && _TREASURE_
mana={3}{U}{R}
type=Instant
text=Choose two: copy target Elemental you control; or draw two cards; or deal 2 damage to each creature an opponent controls; or create two Treasure tokens.
[/card]

[card]
name=Brigid's Command
auto=choice name(copy) copy target(creature[kithkin]|mybattlefield) name(buff) target(creature|mybattlefield) effect(+3/+3) ueot name(kithkin) token(Kithkin,creature kithkin,1/1,green white) name(fight) target(creature|mybattlefield) fight target(creature|opponentbattlefield)
mana={1}{G}{W}
type=Sorcery
text=Choose two: copy target Kithkin you control; or target creature gets +3/+3 until end of turn; or create a 1/1 Kithkin token; or target creature you control fights target creature an opponent controls.
[/card]

[card]
name=Clachan Festival
auto=@movedTo(this|mybattlefield):token(Kithkin,creature kithkin,1/1,green white) && token(Kithkin,creature kithkin,1/1,green white)
auto={4}{W}:token(Kithkin,creature kithkin,1/1,green white)
mana={2}{W}
type=Enchantment
text=When this enchantment enters, create two 1/1 green and white Kithkin creature tokens. -- {4}{W}: Create a 1/1 green and white Kithkin creature token.
[/card]

[card]
name=Firdoch Core
abilities=changeling
auto={T}:Add{W}
auto={T}:Add{U}
auto={T}:Add{B}
auto={T}:Add{R}
auto={T}:Add{G}
mana={3}
type=Artifact
text=Changeling (This card is every creature type.) -- {T}: Add one mana of any color.
[/card]

[card]
name=Grub's Command
auto=choice name(copy) copy target(creature[goblin]|mybattlefield) name(destroy) moveto(mygraveyard) target(*[creature;artifact]|opponentbattlefield) name(buff) all(creature|mybattlefield) effect(+1/+1,haste) ueot name(mill) mill:5 target(player|opponentbattlefield)
mana={3}{B}{R}
type=Sorcery
text=Choose two: copy target Goblin you control; or destroy target artifact or creature; or creatures get +1/+1 and haste until end of turn; or target player mills five cards.
[/card]

[card]
name=Kindle the Inner Flame
auto=copy target(creature|mybattlefield)
mana={3}{R}
type=Sorcery
text=Create a token that is a copy of target creature you control, except it has haste and is sacrificed at the beginning of the end step.
[/card]

[card]
name=Morcant's Eyes
auto=@each my upkeep:_SCRY1_
auto={4}{G}{G}:token(Elf,creature elf,2/2,black green) && token(Elf,creature elf,2/2,black green) && token(Elf,creature elf,2/2,black green) asSorcery
mana={1}{G}
type=Enchantment
text=At the beginning of your upkeep, surveil 1. -- {4}{G}{G}, Sacrifice this: Create three 2/2 black and green Elf creature tokens.
[/card]

[card]
name=Sygg's Command
auto=choice name(copy) copy target(creature[merfolk]|mybattlefield) name(lifelink) all(creature|mybattlefield) effect(+0/+0,lifelink) ueot name(draw) draw:1 name(tap) tap target(creature|opponentbattlefield)
mana={1}{W}{U}
type=Sorcery
text=Choose two: copy target Merfolk you control; or creatures you control gain lifelink until end of turn; or draw a card; or tap target creature.
[/card]

[card]
name=Trystan's Command
auto=choice name(copy) copy target(creature[elf]|mybattlefield) name(reanimate) moveto(mybattlefield) target(*|mygraveyard) name(destroy) moveto(mygraveyard) target(*[creature;enchantment]|opponentbattlefield) name(buff) all(creature|mybattlefield) effect(+3/+3) ueot
mana={4}{B}{G}
type=Sorcery
text=Choose two: copy target Elf you control; or return a permanent card from your graveyard to the battlefield; or destroy target creature or enchantment; or creatures you control get +3/+3 until end of turn.
[/card]

[card]
name=Wanderwine Farewell
abilities=convoke
auto=moveto(myhand) target(*[-land]|opponentbattlefield) && moveto(myhand) target(*[-land]|opponentbattlefield) && token(Merfolk,creature merfolk,1/1,white blue) && token(Merfolk,creature merfolk,1/1,white blue)
mana={5}{U}{U}
type=Sorcery
text=Convoke -- Return up to two target nonland permanents to their owners' hands. Then create a 1/1 white and blue Merfolk creature token for each permanent returned.
[/card]

[card]
name=Collective Inferno
abilities=convoke
mana={3}{R}{R}
type=Enchantment
text=Convoke -- As this enchantment enters, choose a creature type. Double all damage that sources you control of the chosen type would deal.
[/card]

[card]
name=Prismatic Undercurrents
auto=@movedTo(this|mybattlefield):moveto(myhand) target(land[basic]|mylibrary) && moveto(myhand) target(land[basic]|mylibrary) && moveto(myhand) target(land[basic]|mylibrary)
mana={3}{G}
type=Enchantment
text=When this enchantment enters, search your library for up to three basic land cards and put them into your hand, then shuffle. You may play an additional land on each of your turns.
[/card]

[card]
name=Raiding Schemes
mana={3}{R}{G}
type=Enchantment
text=Each noncreature spell you cast has conspire.
[/card]

[card]
name=Shimmerwilds Growth
mana={1}{G}
type=Enchantment
subtype=Aura
text=Enchant land. Whenever enchanted land is tapped for mana, its controller adds an additional one mana of the chosen color.
[/card]

[card]
name=End-Blaze Epiphany
auto=damage:* target(creature|any) && draw:1
mana={X}{R}
type=Instant
text=End-Blaze Epiphany deals X damage to target creature. Draw a card.
[/card]

[card]
name=Harmonized Crescendo
abilities=convoke
auto=draw:3
mana={4}{U}{U}
type=Instant
text=Convoke -- Draw cards equal to the number of permanents you control of the chosen type.
[/card]

[card]
name=Mirrorform
auto=copy target(*[-land]|opponentbattlefield)
mana={4}{U}{U}
type=Instant
text=Each nonland permanent you control becomes a copy of target non-Aura permanent.
[/card]

[card]
name=Rime Chill
auto=tap target(creature|opponentbattlefield) && tap target(creature|opponentbattlefield) && draw:1
mana={6}{U}
type=Instant
text=Tap up to two target creatures. Draw a card.
[/card]

[card]
name=Swat Away
auto=moveto(mylibrary) target(*[-land]|opponentbattlefield)
mana={2}{U}{U}
type=Instant
text=The owner of target permanent puts it on top of their library.
[/card]

[card]
name=Eclipsed Realms
auto={T}:Add{C}
auto={T}:Add{W}
auto={T}:Add{U}
auto={T}:Add{B}
auto={T}:Add{R}
auto={T}:Add{G}
mana=
type=Land
text=As this land enters, choose a creature type. {T}: Add {C}. {T}: Add one mana of any color.
[/card]

"""

with open("M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/primitives/mtg.txt", "a", encoding="utf-8") as f:
    f.write(primitives)

print("Done - wrote", primitives.count("[card]"), "card blocks")
