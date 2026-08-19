# Plan: actioning the `missing=` notes

Written 2026-08-19. A full read of every `missing=` note in the collection, grouped by
what actually blocks the card, with an order of work chosen by cards-fixed-per-unit-of-effort.

## What is there

447 notes across 446 cards, all in `borderline.txt`. Nothing in `mtg.txt`,
`planeswalkers.txt` or `unsupported.txt` carries one.

Two cuts matter more than the note text itself.

**How much of the card is missing:**

| | cards |
|---|---:|
| Partially written (a real body, one clause short) | 185 |
| **No `auto=` at all — the card does nothing** | **70** (31 tokens, 39 cards) |

**How many cards share a root cause.** 20 causes account for 191 cards; the other 255 are
one-off clauses on individual cards.

| root cause | cards |
|---|---:|
| dynamic amount / X (a count the DSL can't express) | 24 |
| cost reduction, conditional | 19 |
| bargain may also be paid by sacrificing a creature token | 19 |
| damage can't be prevented | 18 |
| sneak technique: `{n}` extra cost needs COMBATBLOCKERS | 12 |
| firebending / airbend / waterbend / earthbend | 10 |
| read ahead (Sagas) | 10 |
| "equipped creature is a `<type>` in addition" | 10 |
| restricted mana ("spend only on…") | 10 |
| Pilot token's "crews as though power were 2 greater" | 8 |
| trigger an additional time | 7 |
| Map / Mutagen token does not exist in the collection | 7 |
| Avatar Saga ch III transform (crashed on an imageless back) | 6 |
| saddler untrackable | 6 |
| start your engines / max speed | 5 |
| cast-from-graveyard predicate | 5 |
| Role replacement rule | 4 |
| "has all activated abilities of…" | 4 |
| copy effects | 4 |
| "second card you draw each turn" trigger | 3 |

## Order of work

**Phase 0 — data only, no engine, ~60 cards.** Nothing here needs a build.

1. **Author the Map and Mutagen token primitives** (+ registration + art). Seven cards
   currently substitute a Clue or a Food and say so. This is one intake run.
2. **The 31 inert token bodies.** Their whole note *is* the rules text, because the token
   was registered with no abilities. Most are one line: `Ultramarines Honour Guard` is
   `lord(other creature|mybattlefield) 1/1`, `Vanguard Suppressor` is
   `@combatdamaged(player) from(this):draw:1`, `Alien Salamander` is `islandwalk`.
   A handful (`Manifest`, `A Mysterious Creature`, face-down) are genuinely blocked.
3. **The 39 inert cards**, same idea — mostly the Marvel and 40K intakes. Roughly
   two-thirds are ordinary triggers and activated abilities; the rest
   (`Torpor Orb`, `Vexilus Praetor`, `March from Velis Vel`) are blocked and should be
   left with a note.

Phase 0 is where the player-visible return is: a card with no `auto=` is a blank in a deck,
which is worse than a card that is one clause short.

**Phase 0.5 — verify the 15 self-declared guesses.** Fifteen notes admit to an unverified
or guessed keyword (`copysourcept`, `lifelostamount`, `sevenormorecards`, `manaspentx`,
`sourcept`-based `changecost`, …). Because an unparsed ability fails silently, each of
these is a card that may be inert *while looking written*. Cheap to settle in the WSL
harness, and it should happen before more cards are authored on the same patterns.
Cards: Roadside Assistance, Summon: Knights of Round, Summon: Brynhildr, Torch the Tower,
The Fire Nation Drill, Beorn's Hospitality, Galion, Bilbo's Gambit, Uncover the
Moon-Letters, The Master of Lake-town, Desert Were-Worm, Desolation of Smaug, Glamdring,
Gandalf Goblins' Bane, Thorin Mountain-king.

**Phase 1 — "damage can't be prevented", 18 cards, one engine change.** The single
biggest cause with a single fix. `Isengard Unleashed`'s note already locates it:
prevention is applied inside `Damage::resolve` as an `REDamagePrevention` replacement,
so this wants a flag on `Damage` that the replacement honours, plus a DSL keyword to set
it. 18 cards including Skullcrack, Wild Slash, Urza's Rage, Questing Beast, Flames of the
Blood Hand.

**Phase 2 — the bargain extra-cost parser bug, 19 cards.** The notes say a third comma
clause in an extra-cost `S()` silently breaks the ability, which is why bargain only ever
offers artifacts and enchantments and never creature tokens. That is a parser limit, not
a card limit, and it is the same one line copied across 19 cards.

**Phase 3 — read ahead, 10 Sagas.** One mechanic, ten cards, and the group is already
identified.

**Phase 4 — the Avatar Saga backs, 6 cards.** Chapter III should transform; it sacrifices
instead because the flip crashed on an imageless back face. Check first whether the art
now exists after the token/art passes — if it does, this may be a data fix rather than a
render fix, which would make it the cheapest mechanic in the list.

**Phase 5 — the vehicle/mount family.** Pilot crew rider (8), saddler tracking (6),
start-your-engines (5). Related engine work around tracking *which* creature did a thing.

**Not planned.** Voting (`Model of Unity`); hidden simultaneous choice
(`Prisoner's Dilemma`); opponent-splits-the-piles (`Fact or Fiction`, `Riddles in the
Dark`); face-down permanents (`Cyber Conversion`, `Nosy Goblin`, `Manifest`); per-turn
mode exclusion (`Galadriel`, `Gollum`); deck-construction rules (`Nazgul`). These are
architectural, and the notes on them are already accurate — they should stay as notes.

## Conventions this plan assumes

- A `missing=` note is a promise that the rest of the card is right. When a phase closes a
  cause, delete the note — a stale note is worse than none, because it hides that the card
  is now correct (`Consult the Star Charts` carried one for a deviation that was, in the
  end, a bug).
- Nothing ships without a harness run; the suite baseline is 977/977.
