# HOB/HOC load guards (generated, NOT enabled in _tests.txt)

45 generated files `hobhoc_loadguard_01..45.txt` put all 265 HOB/HOC permanents
into play in batches of 6, referenced by **card id** (many HOB/HOC names contain
commas and the zone parser splits on commas).

They are deliberately **not listed in `_tests.txt`**. Enabling them makes the
suite abort with a SIGSEGV in `TestSuiteGame::initGame`:

    putInZone(card, library, stack) -> NULL
    Spell::Spell(observer, _source = NULL)
    MTGCardInstance::getCurrentZone(this = 0x0)

Why they are parked rather than fixed:

* Every card passes **individually** — all six cards of the batch that aborted
  (guard 04) run clean as solo tests, and as two separate triples.
* The same six cards in one test crash in one ordering and pass in another.
  Reproduced with `thread_count = 1`, so it is **not** a worker-thread race.
* That leaves cross-test state leaking between games — consistent with the
  existing comment in `TestSuiteAI.cpp` about "random 'end of suite' segfaults"
  and the `joinWorkers()` fix for discarded/corrupted teardown.

So the abort is a harness defect exposed by adding many init-heavy tests, not a
defect in the HOB/HOC cards. Fixing it means fixing collection/game teardown
between tests, which is a separate piece of work.

What they DID establish: no HOB/HOC card is fatally malformed in the way Beorn
the Fierce was (`@each my combatbegin:` — an unrecognised phase inside a valid
trigger — yielded a null card and killed the engine at load). That class of bug
is now covered by the hand-written `hob_invented_syntax_load_guard.txt`, which
IS enabled and passing.

To re-enable for a debugging session, append the 45 filenames to `_tests.txt`.
