# Plan: token identity and art

Written 2026-08-17, after a session that fixed token art three different ways and had to
walk two of them back. The point of this note is to settle the mechanism *before* touching
1,300 cards, because the failure mode here is silent — a token with the wrong id looks
exactly like a token with the right one until you see it in play.

## The problem

A token needs three things to render: a **primitive** (its body), a **registration** in a
set's `_cards.dat` at a negative id, and an **image** in that set's zip under the positive
id. What decides which id a token actually gets is *how the card creates it*, and that is
where it goes wrong.

## The four mechanisms, as the engine actually implements them

**1. Inline — `token(Wolf,Creature Wolf,2/2,green)` / `create(Robot:Artifact Creature Robot:2/2)`**

`Token::Token()` (Token.cpp) defaults the id to `-source->getMTGId()` — the id of the card
that created it. The body is correct (it is right there in the call); only the identity is
derived. Consequences:

- Two different tokens from one card collide on one id, so they share one picture.
- If the ability was *granted* to another permanent — `lord(land|myBattlefield) {T}:_TREASURE_`,
  or a `transforms()` applied to a targeted card — `source` is the permanent that acted, not
  the card that granted it. Confirmed in game: Squirrel Nest enchanting Rogue's Passage
  produced a Squirrel at `id:-720283`, Rogue's Passage's own id. **No image can ever be
  pre-staged for this class**, because the id changes with whatever got enchanted.

**2. Inline + `,tnum.N`**

`AllAbilities.h:4052` string-appends the suffix to the creator-derived id:
`720157` + `2` → token id `-7201572`. This is the "card id + X" scheme.

- **Solves** the multiple-tokens-per-card collision.
- **Does not solve** the granted-ability case: still derived from whichever permanent acted.
- In use on 6 cards / 14 call sites, and correctly so — Somberwald Beastmaster (Wolf + two
  sizes of Beast), Fable of Wolf and Owl, Decree of Justice (Angels on cast, Soldiers on
  cycling), Sylvan Offering, Nahiri's Stoneforged Blade. All self-sourced, all making
  several distinct tokens. **These are not obsolete. Leave them alone.**
  (Urza, Planeswalker's emblem is the one flagged as targeted — worth a separate look.)

**3. By name — `token(Clue)`**

`ATokenCreator`'s by-name constructor calls `getCardByName(_cardName, _source->setId)`,
which resolves to a **registered card**: stable id, art from that set's registration,
preferring the creating card's own set and falling back to an all-sets search. Independent
of which permanent acted, so it fixes the granted case too. This is why Clue is the only
token with a picture in a deck full of blank ones, and it is what the
`_TREASURE_`/`_FOOD_`/`_CLUE_`/`_BLOOD_` macro conversion used for ~566 usages.

**4. By id — `token(-720504)`**

`getCardById(tokenId)` — the same destination as by-name, addressed explicitly. Fixes both
problems. Costs the automatic per-set preference: a card printed in five sets pins one
set's art.

## The measurement that decides it

Across all 29,520 card blocks:

| | |
|---|---:|
| Inline calls needing migration | **2,141** across **1,332 cards** |
| Already by-name | 354 |
| Already by-id | 19 |
| Distinct inline bodies | **1,043** (729 appear exactly once) |
| Cards making 2+ inline tokens | 193 |
| Inline calls inside a *granted* ability | **416** |

And the split that settles the mechanism — grouping inline calls by token **name**:

| | names | calls |
|---|---:|---:|
| Name maps to **one** body | 237 | 560 (26%) |
| Name maps to **several** bodies | **128** | **1,581 (74%)** |

`Elemental` has 48 distinct bodies. `Minion` 39, `Ooze` 27, `Zombie` 26, `Construct` 25,
`Hydra` 23, `Spirit` 21, `Bird` 17, `Soldier` 10 (74 calls).

## Decision

**By id by default. By name only where the body is fixed by the rules of the game.**

- **Predefined resource tokens → by name**: Treasure, Clue, Food, Blood, Gold, Powerstone,
  Incubator, Map, Junk. These have one body defined by the game itself, so the name is a
  stable key and `getCardByName(name, setId)` gives the creating card's own set art for
  free. Treasure/Food/Clue/Blood are already converted.
- **Everything else → by id** (`token(-<id>)`). 
- **Low-priority tail → leave inline**, and stage art at `<creator id>t.jpg` in that card's
  own set zip. No primitive, no registration, no card edit.

Two things force this, and the second one overturned the first draft of this plan.

**First:** once a name needs disambiguating, by-name degenerates into by-id with a worse
key. By-name's only advantage is the per-set preference, and that only works while the bare
name is unambiguous. Invent `Elemental Soc 4/4` and it exists in one set, resolving to
exactly one registration — that is by-id, spelled as a made-up string.

**Second — the one that matters more: a name that is unambiguous today is not a stable
key.** Any future set can print a differently-statted token of the same name, and the
binding lives in a single shared primitive, so whoever intakes that set either overwrites
the shared body (silently changing every existing card that makes one) or invents a
suffix (at which point see above). The measurement shows how thin the "unambiguous" class
really is: of 237 such names, **155 (65%) appear in exactly one call site** — unambiguous
because rare, not because stable — and only 15 appear five or more times. Those 15 are
creature tokens (Fractal, Orc Army, Monkey, Goat, Pilot, Wurm, Sliver…), and nothing in the
rules fixes a Monkey token at 2/2 green. Only the predefined artifact tokens carry a
guarantee, and of the unambiguous names exactly three are in that class: Clue, Food, Shard.

**Enforcement**: `intake_tokens.py` already refuses to register a token against an existing
primitive whose body differs, and refuses to author a second primitive under a name already
taken. That check is what keeps the by-name list honest as sets arrive; it must not be
loosened.

## Order of work

1. **The eleven newly intaken sets' tokens** — the ones actually being played.
2. **The 416 granted calls.** Nothing else fixes them; they are wrong *in play*, not merely
   missing art, and that is true however old or low-priority the card is.
3. **Top 20 bodies by call count, by id** — 508 calls (Orc Army ×64, Wolf ×51, Fractal ×74
   across two spellings, Bird ×32, Saproling ×27, Devil ×27, Inkling ×26). Best breadth per
   unit of work. By id, not by name, even where the name looks unambiguous today.
4. **The 729 singleton bodies** — probably never worth a primitive each. Art staging at the
   creator id if anything at all.

## Explicitly not doing

- Converting all 1,332 cards. The tail is 729 one-off bodies and the cards mostly work.
- Touching the 14 `,tnum.` sites.
- Editing shared macros such as `_DRAGONTOKEN_` (= `create(Dragon:Creature Dragon:5/5:red:flying)`).
  Its body is already correct; only art is missing, and art staging fixes that without a
  change that reaches every Dragon-making card in the game.

## TODO carried in

**Radiation (`scryfall.com/card/tpip/22`) needs the marker-card treatment.** It is layout
`token`, type `Card`, and carries the rad-counter rules text: "At the beginning of your
precombat main phase, if you have any rad counters, mill that many cards. For each nonland
card milled this way, you lose 1 life and a rad counter." `intake_tokens.py` skipped it as
"not a creatable token", which is right for a creature-token pass and wrong for this card.

It is the same shape as The Monarch (CN2, LTC) and Enduring Story (HOB), which Wagic
already registers as real command-zone marker cards — a designation with no board presence
otherwise. So Radiation wants a primitive, a registration, art, and a drop into the command
zone when a player first gets a rad counter. That last part is the display half of the rad
counter mechanic, which is engine work and is why 22 Fallout cards are still unwritten.
Energy Reserve (tpip #21) is the same class.

## Lessons this note exists to prevent repeating

- **"Unambiguous today" is not a stable key.** The first draft of this plan split the work
  by whether a token name currently maps to one body. John's question — "surely any named
  token may become ambiguous with a new set release?" — is correct, and the numbers agreed:
  65% of the unambiguous names appear exactly once. Design against the invariant the rules
  guarantee, not against the shape of today's data.
- **"An image exists at this id" is not "the right image."** 1,687 card images were
  downloaded by name, unscoped, so every reprint got its *default* printing — Fallout's
  Impassioned Orator carried M20 art. Every audit passed. Only playing the game showed it.
  Pin art by set + collector number (`fix_set_art.py`).
- **Audit the question you mean.** The token audit asked "which staged thumbnails lack a
  full-size image", which can only find ids that already had art. Cards with no token art
  at all were invisible to it. Ask "which token-creating cards have no art at their own id".
- **Check the card's own oracle token before calling a card broken.** Vernal Sovereign's
  bare `create(Elemental)` was declared a bug; its real token *is* a green-white `*/*`
  "P/T equal to the number of creatures you control", exactly the shared primitive. Reading
  the shared primitive and inferring a bug got two working cards flagged.
- **Repointing an inline call hits every card sharing that call string** — six intended
  repoints touched 23 sites.
