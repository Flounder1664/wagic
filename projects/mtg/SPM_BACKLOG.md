# Marvel's Spider-Man (SPM) - Implementation Backlog

Set code `spm` - Universes Beyond expansion, 2025-09-26. Source: Scryfall bulk dump, deduped by
English card name (`spm_clean.json`, 193 unique cards). This is notably lower than
SET_BACKLOG.md's earlier "~300" estimate -- that figure counted alternate-art/showcase variants
Scryfall lists separately; 193 is the true unique-card count for the set.

Assessment generated 2026-07-06.

## Status

| Metric | Count |
|---|---|
| True unique cards (Scryfall, deduped) | 193 |
| Really implemented (name resolves in the master implemented-primitives list) | 110 |
| Excluded (need work) | 83 |

| Bucket (mutually exclusive, all 83 excluded cards) | Count |
|---|---|
| ENGINE-BLOCKED | 1 |
| BACKLOG-EASY | 24 |
| BACKLOG-MEDIUM | 58 |
| OUT-OF-SCOPE | 0 |
| **Total** | **83** |

### `_cards.dat` bookkeeping notes (not card-count issues)

`_cards.dat` has 195 `primitive=` lines against 193 true unique cards. The 2 extra entries are
exact duplicate registrations -- **"J. Jonah Jameson"** and **"Electro, Assaulting Battery"**
each appear twice (same name, two different `id=` blocks). Both names are genuinely implemented
(in the 110), so this doesn't affect the exclusion math; it's just a duplicate-id cleanup item.

---

## Cross-cutting finding: every excluded card is also a dangling `_cards.dat` reference (live bug)

`projects/mtg/bin/Res/sets/SPM/_cards.dat` pre-registers **all 83** excluded cards with an
`id=` + `primitive=<name>` block (for the 5 MDFCs, only under their front-face name -- e.g.
`primitive=Peter Parker`, not the Scryfall-canonical combined name `Peter Parker // Amazing
Spider-Man`). None of these 83 names -- front or back face -- resolve anywhere in the master
implemented-primitives list (mtg.txt + borderline.txt + planeswalkers.txt union). That means
**these 83 cards already have a card id and will surface in draft pools, deck imports, and card
lookups, but the primitive text backing them was never authored.** Resolving one of these names
at runtime will fail to find a matching primitive.

This is a different shape of gap than other unfinished sets (e.g. SOS, where most of the gap was
"card not yet added to `_cards.dat` at all"). SPM's set skeleton is already 100% built out --
every true card has an id -- only the primitive authoring is missing. None of the 83 excluded
names were found in `unsupported_names.txt` (the known-catalogued-but-intentionally-unsupported
list) either, so this isn't an intentional exclusion list; it looks like the set was scaffolded
(ids assigned) ahead of the authoring pass, and the authoring pass never happened for these 83.

**Practical implication:** until a card is actually authored, its `_cards.dat` entry is a
landmine -- either strip the entry or add a placeholder `text=` line, so the set doesn't ship
with silently-unresolvable card references. The mechanic-based classification below is meant to
guide that authoring pass, batched by mechanic the way SOS's MEDIUM tier was batched.

---

## ENGINE-BLOCKED (1)

**Web-slinging** -- the alternate cost "cast this spell for {X} if you also return a tapped
creature you control to its owner's hand" has no Wagic analog for tying an alt-cost to
returning a permanent. Confirmed by inspecting the one Web-slinging card Wagic *already*
implements -- "Spider-Man, Web-Slinger" (already registered and authored, part of the 110) --
which approximates the mechanic away entirely: it replaces the alt-cost with a flat ETB token
trigger and drops Web-slinging altogether. That's the strongest evidence available that the
engine has no path to this mechanic, rather than it merely being unauthored.

- **Arachne, Psionic Weaver** _(Legendary Creature — Spider Human Hero)_ -- Web-slinging alt-cost is the card's core hook

_Six other excluded cards also print Web-slinging text (Spider-Man, Brooklyn Visionary;
Spider-Man India; Spiders-Man, Heroic Horde; Silk, Web Weaver -- already implemented, not
excluded; Spider-Sense) -- these are bucketed as BACKLOG-MEDIUM below instead of
ENGINE-BLOCKED, since each has enough of a static/ETB body that the card is still worth writing
with the alt-cost dropped, the same simplification Wagic's existing Web-Slinger primitive
already uses. Only Arachne has literally nothing else to the card._

---

## BACKLOG-EASY (24)

Uses only mechanics Wagic already fully supports elsewhere (confirmed directly against
mtg.txt/borderline.txt: Convoke = `abilities=convoke`; Connive = `_CONNIVES_` macro, used 10+
times; Crew/Vehicle = `crew(...)` DSL, used repeatedly; Flashback = native `flashback=` cost
field; Ward = native keyword; "modified creature" tracking = `ismodified`/`compare(modified)`,
89 uses; land ETB-tapped/surveil/fetch templates = dozens of existing uses; modal choice syntax
= widely used). These have short, single-or-double-clause text with no nested conditionals or
"for each"/library-scaling complexity.

- **Amazing Acrobatics** _(Instant)_ -- modal: counter spell / tap creatures
- **Flash Thompson, Spider-Fan** _(Legendary Creature — Human Citizen)_ -- modal ETB, tap/untap target
- **Heroes' Hangout** _(Sorcery)_ -- modal: exile-2-choose-1-play / pump two creatures
- **Kraven, Proud Predator** _(Legendary Creature — Human Warrior Villain)_ -- vigilance + power = greatest MV among permanents (characteristic-defining)
- **Living Brain, Mechanical Marvel** _(Legendary Artifact Creature — Robot Villain)_ -- combat-trigger animate-target-artifact + untap
- **Masked Meower** _(Creature — Spider Cat Hero)_ -- haste + discard/sac: draw
- **Multiversal Passage** _(Land)_ -- choose-basic-type + pay-life-or-enters-tapped
- **Ominous Asylum** _(Land)_ -- dual land, enters tapped, surveil activated (existing template)
- **Pumpkin Bombardment** _(Sorcery)_ -- additional-cost choice (discard or pay) + damage
- **Rent Is Due** _(Enchantment)_ -- end-step tap-2-or-sacrifice, single conditional
- **Robotics Mastery** _(Enchantment — Aura)_ -- flash aura, ETB tokens, static buff
- **Savage Mansion** _(Land)_ -- dual land, enters tapped, surveil activated (existing template)
- **School Daze** _(Instant)_ -- modal: draw three / counter+draw
- **Scorpion, Seething Striker** _(Legendary Creature — Scorpion Human Villain)_ -- deathtouch + conditional end-step connive
- **Shocker, Unshakable** _(Legendary Creature — Human Rogue Villain)_ -- conditional first strike + ETB double damage
- **Sinister Hideout** _(Land)_ -- dual land, enters tapped, surveil activated (existing template)
- **Spider-Girl, Legacy Hero** _(Legendary Creature — Spider Human Hero)_ -- conditional flying during your turn + LTB token
- **Spider-Man No More** _(Enchantment — Aura)_ -- aura sets base P/T + defender, strips abilities
- **Spider-Woman, Stunning Savior** _(Legendary Creature — Spider Human Hero)_ -- flying + static enters-tapped for opponents' artifacts/creatures
- **Suburban Sanctuary** _(Land)_ -- dual land, enters tapped, surveil activated (existing template)
- **Sun-Spider, Nimble Webber** _(Legendary Creature — Spider Human Hero)_ -- conditional flying + ETB tutor Aura/Equipment to hand
- **University Campus** _(Land)_ -- dual land, enters tapped, surveil activated (existing template)
- **Vibrant Cityscape** _(Land)_ -- sac-land: fetch basic tapped (existing template)
- **Wisecrack** _(Instant)_ -- self-damage-equal-to-power + conditional extra damage

---

## BACKLOG-MEDIUM (58)

Supported mechanics, but multi-clause, conditional, "for each"/scaling text, or genuinely
intricate wiring (copy effects, Sagas, MDFCs, Web-slinging-plus-body) that needs careful DSL
construction -- same bar as SOS's MEDIUM tier.

- **Black Cat, Cunning Thief** _(Legendary Creature — Human Rogue Villain)_ -- look-at-opponent-library, exile-and-play-from-exile
- **Chameleon, Master of Disguise** _(Legendary Creature — Human Shapeshifter Villain)_ -- enter-as-copy + Mayhem rider
- **Costume Closet** _(Artifact)_ -- modified-creature LTB trigger + counter-move activated ability
- **Daily Bugle Building** _(Land)_ -- colorless/any-color land + legendary-menace activated ability
- **Eddie Brock // Venom, Lethal Protector** _(Legendary Creature — Human Hero Villain // Legendary Creature — Symbiote Hero Villain)_ -- MDFC - transform supported, both faces unwritten
- **Gwen Stacy // Ghost-Spider** _(Legendary Creature — Human Performer Hero // Legendary Creature — Spider Human Hero)_ -- MDFC - transform supported, both faces unwritten
- **Gwenom, Remorseless** _(Legendary Creature — Symbiote Spider Hero)_ -- attack-trigger play-from-top-of-library paying life instead of mana
- **Hide on the Ceiling** _(Instant)_ -- X-cost exile-and-return-delayed for multiple targets
- **Hydro-Man, Fluid Felon** _(Legendary Creature — Elemental Villain)_ -- conditional pump + becomes-a-land day/night style state change
- **Impostor Syndrome** _(Enchantment)_ -- token-copy-on-combat-damage
- **Interdimensional Web Watch** _(Artifact)_ -- ETB exile-2-playable-window + restricted-mana-for-exile-spells activated ability
- **Iron Spider, Stark Upgrade** _(Legendary Artifact Creature — Spider Hero)_ -- tap-ability affecting multiple permanent types + counter-removal draw
- **Jackal, Genius Geneticist** _(Legendary Creature — Human Scientist Villain)_ -- cast-trigger conditional-on-power copy + counter
- **Kraven's Last Hunt** _(Enchantment — Saga)_ -- Saga - mill+damage-scaling, pump, regrowth chapters
- **Lady Octopus, Inspired Inventor** _(Legendary Creature — Human Scientist Villain)_ -- counter-tracking + free-cast-below-threshold activated ability
- **Lizard, Connors's Curse** _(Legendary Creature — Lizard Villain)_ -- ETB strip-abilities-and-become-4/4 on another creature
- **Madame Web, Clairvoyant** _(Legendary Creature — Mutant Advisor)_ -- play-from-top-of-library (type-restricted) + attack-trigger mill
- **Maximum Carnage** _(Enchantment — Saga)_ -- Saga - forced-attack + mana-add + damage chapters
- **Miles Morales // Ultimate Spider-Man** _(Legendary Creature — Human Citizen Hero // Legendary Creature — Spider Human Hero)_ -- MDFC - transform supported, both faces unwritten
- **Mister Negative** _(Legendary Creature — Human Villain)_ -- exchange-life-totals + conditional draw-equal-to-life-lost
- **Morlun, Devourer of Spiders** _(Legendary Creature — Vampire Villain)_ -- X-cost ETB counters + X damage
- **Mysterio, Master of Illusion** _(Legendary Creature — Human Villain)_ -- ETB token-count-scaling + LTB exile tokens
- **Norman Osborn // Green Goblin** _(Legendary Creature — Human Scientist Villain // Legendary Creature — Goblin Human Villain)_ -- MDFC - transform supported, both faces unwritten
- **Origin of Spider-Man** _(Enchantment — Saga)_ -- Saga - 3 chapter effects
- **Oscorp Industries** _(Land)_ -- tri-color land + graveyard-cast-with-life-loss + Mayhem
- **Parker Luck** _(Enchantment)_ -- two-player symmetric reveal/life-loss/draw
- **Passenger Ferry** _(Artifact — Vehicle)_ -- Crew + optional-pay attack-trigger unblockable-grant
- **Peter Parker // Amazing Spider-Man** _(Legendary Creature — Human Scientist Hero // Legendary Creature — Spider Human Hero)_ -- MDFC - transform supported, both faces unwritten
- **Peter Parker's Camera** _(Artifact)_ -- counter-based ability-copy activated ability
- **Pictures of Spider-Man** _(Artifact)_ -- look-at-5-reveal-creatures-to-hand + sac-for-Treasure
- **Prowler, Clawed Thief** _(Legendary Creature — Human Rogue Villain)_ -- menace + other-Villain-ETB-trigger connive
- **Rocket-Powered Goblin Glider** _(Artifact — Equipment)_ -- conditional-on-cast-from-graveyard ETB attach + Mayhem rider
- **SP//dr, Piloted by Peni** _(Legendary Artifact Creature — Spider Hero)_ -- ETB counter + modified-creature combat-damage draw
- **Sandman's Quicksand** _(Sorcery)_ -- Mayhem rider changes board-wipe symmetry
- **Shadow of the Goblin** _(Enchantment)_ -- two named sub-abilities, discard/draw loop + damage-on-nonhand-play
- **Shriek, Treblemaker** _(Legendary Creature — Mutant Villain)_ -- optional discard-trigger can't-block + opponent-creature-death damage
- **Spider-Man 2099** _(Legendary Creature — Spider Human Hero)_ -- can't-cast-early restriction + conditional end-step damage-equal-to-power
- **Spider-Man India** _(Legendary Creature — Spider Human Hero)_ -- Web-slinging alt-cost + cast-trigger counter+flying
- **Spider-Man, Brooklyn Visionary** _(Legendary Creature — Spider Human Hero)_ -- Web-slinging alt-cost + ETB fetch-basic-tapped
- **Spider-Mobile** _(Artifact — Vehicle)_ -- Crew + attack/block-trigger pump-per-Spider-controlled
- **Spider-Sense** _(Instant)_ -- Web-slinging alt-cost + counter-instant/sorcery/triggered-ability
- **Spider-Slayer, Hatred Honed** _(Legendary Artifact Creature — Human Villain)_ -- damage-to-Spider destroy replacement + graveyard-exile token-making
- **Spider-Verse** _(Enchantment)_ -- legend-rule exception + copy-on-cast-from-elsewhere, once/turn
- **Spiders-Man, Heroic Horde** _(Legendary Creature — Spider Hero)_ -- Web-slinging alt-cost + conditional-on-alt-cost ETB
- **Spinneret and Spiderling** _(Legendary Creature — Spider Human Hero)_ -- attack-count trigger + damage-threshold exile/play
- **Subway Train** _(Artifact — Vehicle)_ -- Crew + optional-pay ETB tutor-basic-to-hand
- **Superior Foes of Spider-Man** _(Creature — Human Rogue Villain)_ -- cast-trigger exile-and-play-until-replaced
- **Superior Spider-Man** _(Legendary Creature — Spider Human Hero)_ -- enter-as-copy-from-graveyard with name/type override
- **Symbiote Spider-Man** _(Legendary Creature — Symbiote Spider Hero)_ -- combat-damage look-X-cards-split-hand/graveyard + graveyard-exile counter-grant
- **The Clone Saga** _(Enchantment — Saga)_ -- Saga - copy + named-card draw-trigger chapters
- **The Death of Gwen Stacy** _(Enchantment — Saga)_ -- Saga - destroy/discard-or-lose/exile-graveyards chapters
- **The Soul Stone** _(Legendary Artifact — Infinity Stone)_ -- harness/counter-activation two-stage ability + recurring reanimation
- **The Spot, Living Portal** _(Legendary Creature — Human Scientist Villain)_ -- double exile (permanent + graveyard card) + death-trigger conditional return
- **Ultimate Green Goblin** _(Legendary Creature — Goblin Villain)_ -- upkeep discard+Treasure loop + Mayhem rider
- **Unstable Experiment** _(Instant)_ -- draw + conditional connive stacked
- **Urban Retreat** _(Land)_ -- tri-color land + alt-cost-from-hand-via-tapped-creature-return
- **Web of Life and Destiny** _(Enchantment)_ -- Convoke + repeating look-top-5-put-creature-onto-battlefield
- **With Great Power . . .** _(Enchantment — Aura)_ -- modified-count P/T scaling + damage redirection

---

## OUT-OF-SCOPE (0)

All 193 true cards are real, distinct, playable set members -- no promos, alternate arts, or
stray tokens leaked into the deduped list.

---

## Summary

| True cards | Really implemented | Excluded | Engine-blocked | Easy | Medium |
|---|---|---|---|---|---|
| 193 | 110 | 83 | 1 | 24 | 58 |

All 83 excluded cards are simultaneously dangling references in `_cards.dat` (registered with
an id, primitive text never authored) -- see the callout section above for the fix (author the
primitive, or strip/stub the `_cards.dat` entry until it is authored).
