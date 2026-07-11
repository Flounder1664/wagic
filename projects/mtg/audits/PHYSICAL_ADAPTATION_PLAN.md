# Physical / social cards — adaptation plan (case-by-case)

Supersedes the "never-implementable / permanently excluded" framing in earlier docs. Per direction
(2026-07-11): **the end goal is to get as many of these into Wagic as possible.** Wagic is a video
game, not paper, so most "physical" cards have a *conceivable digital analogue*. Where one exists we
plan a **cheap approximation** (the most practical path); a residue with no reasonable analogue stays
lowest-priority / possibly-never. Decisions are **case-by-case**; the table below is the starting map.
The black-border cards (Chaos Orb, Falling Star, Shahrazad, ante) get the **same treatment** as the
un-cards — no special-casing.

Card lists & counts come from [UNSETS_AUDIT.md](UNSETS_AUDIT.md) §A (81 un-cards) plus the
black-border physical cards from the OLD-01/02/03 era docs.

## Decided priorities (2026-07-11) — see [ROADMAP.md](ROADMAP.md)

All categories set to **LOW** with these agreed approaches (refinements to the proposals below):
- **A3 dexterity → probability-WEIGHTED target**, not uniform random (model real-flip odds: favor
  clustered / larger / central permanents).
- **A1 person-outside → AI pilots with DEGRADED/confused priorities** (a disruptive outsider plays
  badly, not to win); reusable for Mindslaver.
- **A2 subgame** → coin-flip approx. **A8 ante** → within-game zone. **A4+A5** → UI button/toggle.
  **A6 timing** → countdown timer.
- **A7** → menu-pick the ~4 "name a card" cards (lowest); the ~10 true trivia/body/contest cards are
  **NEVER**. **A9 cross-game → SKIP/NEVER** (user chose skip over drop-rider/same-game).

## Priority key
- **P2 (low)** — reasonable cheap analogue exists; author when convenient.
- **P3 (lowest)** — analogue is awkward/partial; do opportunistically.
- **NEVER** — no digital analogue conceivable (real-world trivia/body); leave excluded but listed.

## The map

| Cat | Scenario | Cards | Proposed cheap analogue | Verdict |
|---|---|---|---|---|
| **A1** | "A person outside the game controls a player" (Kindslaver, Sacrifice Play…) | 7 un | **AI pilots the target player** that turn (reuse Mindslaver-style control, routed to the AI = the "outside" controller) | **P2** |
| **A2** | Play a Magic sub-game (Shahrazad, Enter the Dungeon…) | 3 un + Shahrazad | **Coin-flip a winner, apply the life/again rider** (skip the nested game). Faithful recursive duel = someday-P3 | **P2** (approx) |
| **A3** | Manual dexterity — flip/throw/drop/spin/stack (Chaos Orb, Falling Star, Ol' Buzzbark, Orcish Paratroopers…) | 13 un + Chaos Orb + Falling Star | **Random target(s)** — engine destroys/damages a random permanent (or random N for area cards). This is the established MTGO Chaos Orb adaptation | **P2** |
| **A4** | Balance / touch / hold the card on your body ("as long as you balance ~ on your head…") | 10 un | **Toggle or always-on** — treat the upkeep condition as satisfied (or a click-to-hold button). Cheapest: condition always true | **P3** |
| **A5** | Say a word / make a sound / speak / stay silent — "Gotcha" (Free-Range Chicken, Carnivorous Death-Parrot…) | 24 un | **UI button** ("Gotcha!" / "Say it") the opponent can trigger; or auto-resolve the condition on a timer/random | **P3** |
| **A6** | Real-world timing — wait N real seconds / act within a limit (Time Out, Just Desserts…) | 6 un | **Digital countdown timer** — genuinely easy in a video game (this is arguably *not* even a blocker) | **P2** |
| **A7** | Real-world knowledge / trivia / body / physical contest (name-a-card-from-memory, quote flavor, arm-wrestle) | 14 un | **Split:** "name/pick a card" → menu picker (**P3**, ~3-4 cards); true trivia/body/contest → **NEVER** (~10) | **P3 / NEVER** |
| **A8** | Ante / gambling / open-a-booster / real money (Contract from Below, Jeweled Bird, Amulet of Quoz…) | 9 un + 9 black-border | **Within-game ante zone** — cards function mechanically; no persistent collection loss (returned after the duel). Booster/money riders ignored | **P3** |
| **A9** | Cross-game persistence — "in your next game…" (next-game riders) | 5 un | **Apply within the current game** or drop the cross-game clause (Wagic duels are one-off) | **P3** |

## What this changes about the counts

- The old "~90–150 never-implementable" figure collapses to a **true NEVER residue of only ~10**
  (real-world trivia / body / physical contests in A7).
- Everything else — **~120 cards** including the iconic black-border trio and all ante cards — moves
  into **P2/P3 low-priority adaptation backlog** with a concrete cheap analogue above.
- Two engine hooks unlock the most here: **(i) random-target resolution** (A3 — dexterity, ~15
  cards) and **(ii) AI-controls-a-player** (A1 — ~7 cards, also reusable for Mindslaver/Kindslaver).
  Both are modest, self-contained additions.

## Case-by-case note

These are starting recommendations, not commitments — each card is decided on its own when picked up.
Some (A4/A5/A7/A8/A9) may sit at P3 indefinitely. The point of this doc is that the door is **open**:
none of these should be recorded as flatly "out of scope" except the ~10 true-trivia/body residue.
