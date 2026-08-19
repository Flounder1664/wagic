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

## Progress, 2026-08-19

| phase | outcome |
|---|---|
| 0 — token bodies | 22 of 31 written, 15 complete. Verified by assertion, not by a passing suite. |
| 0 — inert cards | 7 of 39 written. |
| 0 — Map / Mutagen | **done.** Both are real registered tokens now (`-637012` in LCI, `-910900` in TMT) and the seven cards create them by name. Mutagen is exact; Map is the +1/+1 half, because `explore` appears **zero** times in the engine. |
| 0.5 — the 15 guesses | **done, and worse than expected.** Twelve keywords they used exist nowhere in the engine and nowhere in upstream: `addmulti`, `controlledlands`, `copysourcept`, `countbattlefieldcreature`, `gifted`, `lifelostamount`, `manaspentx`, `mytgt2`, `sevenormorecards`, `sourcept`, `spendonly`, `targetpower`. Thirteen lines across ten cards were dead and are removed. |
| 1 — damage can't be prevented | **done.** Two new basic abilities, `noprevention` and `nopreventionall`, and one early-out in `REDamagePrevention::replace`. 17 cards. Six keep a narrowed note for the turn-wide half. |
| 2 — bargain | **fixed.** New `ortoken` filter attribute; all 16 cards now accept a token as fodder. See below. |
| 3 — read ahead | **blocked, and measured.** A modal `choice` ETB on a permanent adds nothing, and `counter(0/0,N,Lore)` adds the counters but fires no chapter, because chapter triggers are `@counteradded(0/0,1,Lore)`. All ten notes now carry that. |
| 4 — Avatar Saga backs | **done.** All six back faces already had art in TLA.zip, so the crash that caused the disable was gone. The five Legend Sagas transform on chapter III again, and Aang, at the Crossroads transforms when another creature leaves. Verified in the harness. |

### Bargain: fixed with an `ortoken` filter attribute

Bargain takes an artifact, an enchantment **or a token**. The cards only offered
`S(artifact,enchantment|myBattlefield)`, and `otherrestriction` gated the cast menu on the
same filter, so a board of only tokens was not offered Bargain at all.

**The blocker was the restriction, not the fodder.** With a trivially-true restriction and
`S(*[token])`, bargain worked immediately. The restriction failed because `isToken` is
checked unconditionally at `CardDescriptor.cpp:579`, outside the `CD_OR` branch, so
`type(*[artifact;enchantment;token]|...)` means "(artifact OR enchantment) AND is-a-token"
- zero on any board. `match_or` only ORs over *types*, and being a token is not a type, so
there was no way to spell "artifact, enchantment or token".

**The fix** is additive rather than a change to `isToken`, because 154 existing brackets
pair `token` with `;` (`[token;fresh]` x20, `[-token;...]`) and rely on the AND behaviour.
A new attribute `ortoken` sets `CardDescriptor::orToken`, and `match()` lets a token
satisfy the filter on its own:

```cpp
if (orToken == 1 && card->isToken)
    match = card;
```

parsed in `TargetChooser.cpp` *before* the `token` branch, which it contains as a
substring. All 16 cards now read
`S(*[artifact;enchantment;ortoken]|myBattlefield)` with a matching restriction.

Both paths are asserted in the suite: `bargain_torch_the_tower_paid.txt` (sacrifice an
Ornithopter) and `bargain_token_fodder.txt` (a board of nothing but Dragon Fodder's
Goblins). `token_sac_control.txt` guards the assumption underneath, that a Goblin can pay
a `{S(*[token])}` cost at all.

**Two traps this cost me.** `WAGIC_TESTSUITE_ONLY` silently runs nothing when the test is
not in `_tests.txt`, and `grep -c "Test Failed"` then returns 0 - identical to a pass. A
whole round of "this works" readings was void that way; always confirm
`failed test: N out of 1 total`. And a bug in the *gate* can look exactly like a bug in the
*payment*: three separate mechanisms were blamed before the trivially-true restriction
isolated it.

### The reveal audit had a hole

The stranding sweep only looked at lines containing `revealend`, so it never saw reveal
blocks that were missing their terminator entirely - which is a worse bug, since
`parseBetween(s, "reveal:", " revealend")` cannot match and the whole construct fails to
parse. Six cards were in that state, one of them upstream's (Expressive Iteration, House
Cartographer, Kethek, Moment of Truth, Aang at the Crossroads, and mtg.txt's Moment of
Truth twin). All six are terminated now, and both audits report zero.

Lesson: an audit keyed on a token can only find lines that already have it. Ask instead
which lines *should* have it.

### A caution about the keyword audit

Checking a card's ability tokens against the engine source is cheap and it worked on the
15 that *admitted* to guessing. Run against all 12,800 cards it returns 919 "absent"
tokens and is mostly noise — counter names (`saddled`, `incubate`) and strings the engine
builds at runtime (`hascnt<counter>`, `mybattlefieldplus<type>`). It needs a filter that
knows where in a line a real keyword can appear before it is worth running wholesale.

## Multikicker: known behaviour, deliberately not fixed (2026-08-19)

Wagic only ever spends mana already in the pool - it does not tap lands for you. On top of
that, `MTGRules.cpp:544` discards the player's answer (`card->kicked = 0`) and then kicks as
many times as the pool can afford, paying for every one.

The two facts together mean **the kick count is chosen by how much mana you tap before
casting**, and it is exact and repeatable. Verified in game on both cards:

| tapped | Apex Hawks ({2}{W}, printed 2/2) | Marshal's Anthem ({2}{W}{W}) |
|---:|---|---|
| 6 Plains | 3/3 - one kick | one creature returned |
| 8 Plains | 4/4 - two kicks | both creatures returned |

So multikicker is **not broken**, and neither is Marshal's Anthem - the earlier suspicion
was wrong. The real gap is only that the engine never *asks*: float spare mana and it gets
spent on kicks you did not request, and you cannot kick fewer times than your pool allows.

Fixing that properly means adding "Kick x1 / x2 / ... xN" entries to the cast menu, because
casting with kicker is a menu entry (`MTGKickerRule`), not a count prompt. That touches the
cast path for every kicker card in the game, for a usability gain over a workaround that
already works precisely. John's call, 2026-08-19: leave it and record it. Do not "fix" this
without asking again.

Two measurement notes worth keeping:

* The WSL harness **requires** a `manapool:` line and will not tap lands; the GUI scenario
  handover **drops** the pool and expects you to tap. A scenario written with `manapool:`
  and no lands has no mana at all.
* The harness AI auto-declines optional `<upto:>` targets, so it can never confirm an
  optional-target ability. `Marshals_Anthem_MULTIKICKER.txt` failed for exactly that reason
  and was deleted rather than left standing as a false accusation.

## Conventions this plan assumes

- A `missing=` note is a promise that the rest of the card is right. When a phase closes a
  cause, delete the note — a stale note is worse than none, because it hides that the card
  is now correct (`Consult the Star Charts` carried one for a deviation that was, in the
  end, a bug).
- Nothing ships without a harness run; the suite baseline is 977/977.
