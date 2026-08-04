# HOB/HOC load guards (45 files, ENABLED)

`hobhoc_loadguard_01..45.txt` put all 265 HOB/HOC permanents into play in batches
of 6, referenced by **card id** (many HOB/HOC names contain commas and the zone
parser splits on commas).

They exist to catch the *fatal* failure mode: a malformed card that yields a null
pointer and kills the engine while the card is being parsed or resolved, rather
than merely behaving wrongly.

## They are assertion-recorded, not rules-verified

The asserted zone counts / life totals are **recorded current behaviour**, taken
from an actual run. They prove "this batch loads, resolves and leaves a stable
board", not "these cards follow the rules". A card can pass its guard and still
be wrong (Little Bear passed everything while putting counters on non-Bears).

## Engine bugs these found

Enabling them exposed five separate crashes, each a null dereference on a path
that assumed parsing had succeeded:

1. `TestSuiteAI.cpp` initGame — `putInZone()` returns NULL when the card is not in
   that library (`getCardByMTGId` searches *both* players and *all* zones, so an
   earlier card's ETB can move a later INIT card out first). Fed straight into
   `Spell(observer, NULL)`.
2. `MTGAbility.cpp` parseMagicLine — `createTargetChooser()` returns NULL for an
   unparseable selector; `tc->targetter` was dereferenced regardless.
3. `MTGAbility.cpp` — an empty `transforms(())` split to an empty vector and
   `effectParameters[0]` read off the end.
4. `AllAbilities.cpp` GenericPaidAbility::resolve — used the result of
   `parseMagicLine` unchecked (the code even carried a comment calling itself
   "dangerous ... not fixing this").
5. `MTGAbility.cpp` parseTrigger/parseMagicLine — `parseTrigger()` returns NULL for
   an unrecognised trigger name, but the two `restriction{}` assignments ran
   *before* the existing `if (trigger)` check, so any card pairing an unknown
   trigger with a restriction killed the engine.

Net effect: one malformed card used to take down the entire game. It now degrades
to that card not working.

## Card bugs these found

* `*[a,b]` — comma as a type separator inside a selector. Zero uses in mtg.txt;
  `;` is the separator (251 uses). 14 occurrences across 13 HOB/HOC cards, each a
  hard crash.
* `@activate`, `@leaves`, `@seconddrawofturn` — invented triggers, zero uses
  anywhere. Removed; affected cards carry a `missing=` note.
