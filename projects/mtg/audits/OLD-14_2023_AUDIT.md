# Old-Era Coverage Audit — 2023 (5 sets)

Cross-set audit of missing / unsupported cards for the release-order run
**MUL · MAT · LTR · LTC · CMM**
(Multiverse Legends, March of the Machine: The Aftermath, The Lord of the Rings: Tales of
Middle-earth, Tales of Middle-earth Commander, Commander Masters).

Generated 2026-07-11. Method per [`README.md`](README.md): each name from
`Res/missing_cards_by_sets/<CODE>.txt` was cross-checked against `grade_index.json`
(the union of the four `core.zip` primitive files). Classification is by **oracle text**, never
substring — same discipline as the SOS backlog and the peer
[`OLD-08_2014-2016_AUDIT.md`](OLD-08_2014-2016_AUDIT.md). Before any card was tagged
ENGINE-BLOCKED, the underlying mechanic was **probed** against the index to confirm no supported
example exists.

> Note: the batch token `missingCardList` is **not a set** and is ignored — there is no
> `missing_cards_by_sets/missingCardList.txt` to read.

## Headline numbers

| Metric | Count |
|---|---|
| Distinct missing cards (deduped across all 5 sets) | **51** |
| STALE (name already resolves to `supported`/`borderline`) | **2** |
| Genuinely excluded (catalogued-unsupported) | **49** |
| Catalogued-unsupported (registered w/ oracle text in `unsupported.txt`) | **49** |
| Truly-absent (no entry anywhere) | **0** |

Across the 5 files there are ~90 raw `[card]` blocks; every file lists most of its cards twice
(and MUL/CMM/LTC are heavy reprint products), so dedup collapses to **51 distinct names**. Two of
those already resolve to `borderline.txt` and **should be dropped from the missing-lists** — they
load and work today. The remaining **49** are all catalogued-unsupported: upstream registered them
with full oracle text inside `sets/primitives/unsupported.txt` (grade *unsupported* → does not
load, not AI-deck safe) but never wrote a working primitive. None are true dangling references
outside the catalogue. So the excluded population is "known-broken, documented" — the same shape
as every prior era.

### STALE — already implemented, remove from missing-list (2)

Both resolve to `borderline.txt` and load by default. Their presence in `missing_cards_by_sets`
is a stale artifact; they are **not** counted among the 49 excluded.

| Card | Set(s) | Grade / file | Why it's fine now |
|---|---|---|---|
| Tempt with Vengeance | CMM | borderline / borderline.txt | X haste-Elemental token maker resolves (the tempting-offer bonus is approximated/ignored, hence borderline) |
| Oreskos Explorer | CMM | borderline / borderline.txt | search-up-to-X-Plains by player-land-count works (same borderline entry flagged in OLD-08) |

### Mechanic-support probes (what shapes the classification below)

The 2023 sets are dominated by two things: **multiplayer voting** (LTC/CMM Commander decks) and
**LTR's own keyword suite**. The probe results split them cleanly:

| Mechanic | Supported example(s) in index | Verdict |
|---|---|---|
| **the-Ring-tempts-you / Ring-bearer emblem** (LTR marquee) | Frodo Adventurous Hobbit, Call of the Ring, Sauron the Dark Lord, The Ring Goes South, Orcish Bowmasters — all **borderline** | **SUPPORTED** (not the blocker for any LTR/LTC card) |
| **Amass Orc / Food** (LTR) | Fell, Lobelia Sackville-Baggins, Samwise the Stouthearted — borderline | SUPPORTED |
| **Companion** (MUL) | Lurrus, Yorion, Kaheera, Umori, Lutri, Keruga — all borderline | SUPPORTED (the companion clause itself is fine) |
| **Voting: Will of the council / Council's dilemma / Secret council / Tempting offer / Join forces** | **none** — Council's Judgment, Expropriate, Coercive Portal, Split Decision, Magister of Worth, Collective Voyage, all Tempt-with-* cards, Minds Aglow: **every one unsupported** | **ENGINE-BLOCKED** |
| **Copy an activated/triggered ability** | **none** — Rings of Brighthearth, Strionic Resonator, Illusionist's Bracers, Kurkesh all unsupported; only Lithoform Engine borderline | **ENGINE-BLOCKED** |
| **"has all activated abilities of…" grant** | **none** — Experiment Kraj, Mairsil, Soulflayer all unsupported | **ENGINE-BLOCKED** |
| **Change the target of a spell** (Imp's Mischief) | **none** — Imp's Mischief, Willbender, Spellskite, Mizzium Meddler unsupported; only fixed Redirect borderline | **ENGINE-BLOCKED** |
| **Gain control of a spell on the stack** (Commandeer) | **none** — Commandeer, Aethersnatch, Desertion all unsupported | **ENGINE-BLOCKED** |
| **Extra loyalty-activation / loyalty re-enable** (Oath of Teferi, Chain Veil) | **none** — both unsupported (loyalty abilities themselves are supported, but not doubling/re-activating them) | **ENGINE-BLOCKED** |
| **Opponent-partitions-two-piles secret pile** (Atris) | Fact or Fiction borderline, but Sphinx of Uthuun unsupported; the opponent-splits-face-up/face-down partition has no UI | **ENGINE-BLOCKED** |
| **Damage-doubling replacement** (Gisela, Obosh) | Furnace of Rath / Gratuitous Violence / Fiery Emancipation are only *borderline global* statics; the one-sided / conditional bodies (Gisela, Obosh) are unsupported | **ENGINE-BLOCKED** (as a card body; see OLD-08 E8) |
| **Activated-ability cost reduction** (Training Grounds, Zirda) | **none** — Training Grounds, Zirda, Biomancer's Familiar, Heartstone all unsupported (spell-cost reduction *is* supported: Goblin Electromancer) | **ENGINE-BLOCKED** for the activated-ability variant |
| **Reveal-top-and-cast** (Yennett) | Etali Primal Storm, Bloodbraid Elf, Genesis Ultimatum — supported/borderline | SUPPORTED (frame); the odd-CMC gate is a rider |
| **Reveal-until-creature → into play** (Divergent Transformations) | **none** — Oath of Druids unsupported | ENGINE-BLOCKED-ish → filed MEDIUM |
| **Counter relocation / proliferate / Ozolith** | Fathom Mage, Vorel, Contagion Clasp supported; Corpsejack/Hardened Scales/Doubling Season borderline | SUPPORTED (base); mass counter-relocation is a rider |
| **Replicate** (Hatchery Sliver) | Shattering Spree, Pyromatics — borderline | SUPPORTED (base); *granting* replicate is the rider |
| **Must-pay-to-attack tax** (Norn's Annex) | Propaganda, Ghostly Prison — supported | SUPPORTED (base); the Phyrexian-mana {P/W} payment is the rider |
| **Improvise** (Inspiring Statuary grants it) | Reverse Engineer (has improvise) — supported | SUPPORTED (base); *granting* improvise to nonartifact spells is the rider |
| **Prevent-all-damage-to-you** (Selfless Squire) | Riot Control supported; Comeuppance unsupported | SUPPORTED as a flat prevent; the "count prevented → +1/+1 counters" payoff is the rider |

### Reprint overlap (deduped — each card listed once below, tagged with all its sets)

Only **one** name appears in more than one of the 5 files:

| Card | Sets |
|---|---|
| Zada, Hedron Grinder | MUL, CMM |

Every other duplicate is a *within-file* repeat (each list prints its cards twice). So 51 distinct
names come from: MUL 8, MAT 2, LTR 2, LTC 12, CMM 28 — with Zada shared MUL∩CMM (counted once).

**Note on LTR/LTC and the Ring:** although the-Ring-tempts-you is LTR's headline mechanic, it is
**already supported** (borderline) and is **not** the blocker for any missing card here. Galadriel,
Elven-Queen's "the Ring tempts you, then +1/+1 on your Ring-bearer" clause would resolve fine — she
is blocked by the **voting** wrapped around it. So there is **no Ring-emblem ENGINE-BLOCKED bucket**
in this era; the planar/emblem subsystem gap does not surface.

---

## By exclusion reason (main deliverable)

Grouped by the mechanic/pattern that blocks each card, deduped, with per-card set tags. Tier tags:
**ENGINE-BLOCKED** (no Wagic analog) · **BACKLOG-EASY** · **BACKLOG-MEDIUM** · **OUT-OF-SCOPE**.

### E1 — Multiplayer voting (Will of the council / Council's dilemma / Secret council)  · ENGINE-BLOCKED  (9)

The single largest group in the era. Wagic has **no voting subsystem** — no primitive gathers a
per-player secret/open vote, tallies it, and branches on the tally. Every probed voting card in the
whole catalogue (Council's Judgment, Expropriate, Coercive Portal, Split Decision, Magister of
Worth) is unsupported. The LTC "council" cards and CMM's Custodi Squire all fail here regardless of
what their *winning*-branch effect is.

- Elrond of the White Council (LTC) — secret council: fellowship/aid, gain control per fellowship vote, +1/+1 per aid vote
- Cirdan the Shipwright (LTC) — secret council: vote-for-a-player, draw per vote, no-votes → permanent into play
- Erestor of the Council (LTC) — "whenever players finish voting" Treasure + scry payoff (a vote-*payoff*, still needs the vote engine)
- Galadriel, Elven-Queen (LTC) — will of the council: dominion/guidance; dominion → Ring tempts you + Ring-bearer counter (Ring part is supported; the **vote** is the blocker)
- Sail into the West (LTC) — will of the council: return/embark
- Plea for Power (LTC) — will of the council: time (extra turn) / knowledge (draw 3)
- Travel Through Caradhras (LTC) — council's dilemma: Redhorn Pass / Mines of Moria
- Trap the Trespassers (LTC) — secret council: vote a creature, stun-counter + tap per vote
- Custodi Squire (CMM) — will of the council: vote a card in your GY, return the most-voted

### E2 — "Tempting offer" / "Join forces" multiplayer group-pay votes  · ENGINE-BLOCKED  (1)

Same missing machinery as E1 — a group offer where each other player opts in and a payoff scales
with participation. Every Tempt-with-* and Join-forces card in the catalogue is unsupported.
*(Tempt with Vengeance is the STALE borderline exception — its token count resolves but the offer
is not honored — and is not counted here.)*

- Minds Aglow (CMM) — join forces: each player may pay mana, everyone draws X = total paid

### E3 — Copy an activated/triggered ability (choose new targets)  · ENGINE-BLOCKED  (5)

No primitive can duplicate an ability already on the stack and re-target the copy. Every catalogue
example (Rings of Brighthearth, Strionic Resonator, Illusionist's Bracers, Kurkesh) is unsupported;
only Lithoform Engine is borderline. Several 2023 designs are variants of this.

- Rings of Brighthearth (LTC) — pay {2}: copy a non-mana activated ability
- Abstruse Archaic (CMM) — {1},{T}: copy a colorless activated/triggered ability
- Jaya's Phoenix (CMM) — copy the next loyalty ability you activate this turn
- Leori, Sparktouched Hunter (CMM) — copy each activated ability of a chosen planeswalker type this turn
- Experiment Kraj (CMM) — "has all activated abilities of each other creature with a +1/+1 counter" (the ability-grafting variant; all-abilities-of is equally unsupported)

### E4 — Extra loyalty-activation / loyalty re-enable  · ENGINE-BLOCKED  (2)

Loyalty abilities themselves are supported, but **granting extra activations** or re-enabling an
already-used one per turn needs per-turn loyalty-activation bookkeeping the engine doesn't keep
(the OLD-08 "Chain Veil" group, now with its actual namesake).

- The Chain Veil (CMM) — {4},{T}: re-enable one loyalty ability on each planeswalker; end-step life loss if none used
- Oath of Teferi (CMM) — activate loyalty abilities twice each turn (+ a blink ETB)

### E5 — Change the target of a spell  · ENGINE-BLOCKED  (1)

The "Willbender effect" — the single biggest engine group in OLD-08. No primitive retargets an
object already on the stack; every example is unsupported.

- Imp's Mischief (CMM) — change the target of a single-target spell; lose life = its CMC

### E6 — Gain control of a spell on the stack  · ENGINE-BLOCKED  (1)

No primitive can seize an object off the stack (Commandeer/Aethersnatch both unsupported).

- Commandeer (CMM) — gain control of target noncreature spell, may choose new targets

### E7 — Opponent-partitions-two-piles secret pile  · ENGINE-BLOCKED  (1)

The opponent splits revealed cards into face-up / face-down piles and you pick one — the same
missing partition UI that blocks Sphinx of Uthuun / Steam Augury (Fact or Fiction is only
borderline).

- Atris, Oracle of Half-Truths (MUL) — opponent splits your top 3 into a face-down and face-up pile; you take one, other to GY

### E8 — Damage-doubling replacement (one-sided / conditional)  · ENGINE-BLOCKED  (2)

"If a source would deal damage … it deals double instead" as a *card body* — the global static
(Furnace of Rath) is only borderline; these one-sided / cost-gated variants are unsupported (OLD-08 E8).

- Gisela, Blade of Goldnight (CMM) — double damage to opponents, halve damage to you
- Obosh, the Preypiercer (MUL) — sources you control with odd CMC deal double damage (companion clause itself is fine; the double-damage replacement is the blocker)

### E9 — Activated-ability cost reduction  · ENGINE-BLOCKED  (2)

Spell-cost reduction is supported (Goblin Electromancer), but reducing the cost of **activated
abilities** has no analog — Training Grounds, Zirda, Biomancer's Familiar, Heartstone are all
unsupported.

- Training Grounds (MAT) — activated abilities of your creatures cost up to {2} less (floor 1 mana)
- Zirda, the Dawnwaker (MUL) — non-mana activated abilities you activate cost {2} less (companion clause is fine; the cost-reduction static is the blocker; also carries a can't-block ability)

### E10 — Reveal-until-creature → onto battlefield (Oath of Druids family)  · BACKLOG-MEDIUM  (1)

Reveal from the top until a creature, put it into play — Oath of Druids is unsupported, so no
exemplar, but it is a bounded dig with no partition/vote and is authorable with care.

- Divergent Transformations (CMM) — exile two creatures; each controller digs to a creature and puts it into play (has Undaunted, which is a plain per-opponent cost reducer)

### E11 — Reveal-top-and-cast gated on CMC parity  · BACKLOG-MEDIUM  (1)

Reveal-and-cast is supported (Etali, Bloodbraid); the odd-CMC gate + "else draw" is the rider.

- Yennett, Cryptic Sovereign (CMM) — on attack, reveal top; cast free if CMC odd, else draw

### E12 — Counter relocation / accumulation riders  · BACKLOG-MEDIUM  (2)

Proliferate and single counter-moves are supported (Fathom Mage, Vorel, Contagion Clasp); these
need "move a counter of *each kind*" / "accumulate all counters from creatures that left, then
redistribute" bookkeeping.

- Goldberry, River-Daughter (LTR) — move one counter of each kind between permanents; bulk-move off her to draw
- The Ozolith (LTC) — accumulate counters from creatures that leave; move all to a creature each combat

### E13 — Grant a keyword-with-payload to a whole card group  · BACKLOG-MEDIUM  (2)

The base keyword works, but *granting* it across a type (with its own cost math) is the rider —
mirrors OLD-08's Falkenrath Gorger "grant madness" group.

- Hatchery Sliver (CMM) — every Sliver spell you cast gains replicate = its mana cost
- Inspiring Statuary (CMM) — your nonartifact spells gain improvise

### E14 — Mill-then-exile-then-scaled-token  · BACKLOG-MEDIUM  (1)

Mill + exile-picked-cards + make an X/X where X = total power exiled (OLD-08 already filed this
exact card at MEDIUM).

- Stitcher Geralf (CMM) — mill 3 each, exile up to 2, make an X/X Zombie = total power exiled

### E15 — Must-pay-to-attack tax with Phyrexian mana  · BACKLOG-MEDIUM  (1)

The pay-to-attack tax is supported (Propaganda, Ghostly Prison); the {P/W} (pay-with-life)
component is the rider.

- Norn's Annex (CMM) — creatures can't attack you/your PW unless controller pays {P/W} each

### E16 — Prevent-all-damage-to-you → scaled counter payoff  · BACKLOG-MEDIUM  (1)

Flat "prevent all damage to you this turn" is supported (Riot Control); the "count what was
prevented, add that many +1/+1 counters" replacement-watcher is the rider.

- Selfless Squire (LTC) — prevent all damage to you this turn; +1/+1 counter per damage prevented

### E17 — Miscellaneous single-card riders on supported mechanics  · BACKLOG-MEDIUM / EASY  (mixed, 13)

Marquee mechanic supported; a specific rider blocks the card. Grouped here to avoid a bucket per card.

- Baral, Chief of Compliance (MUL) — instant/sorcery cost reducer (Goblin Electromancer works) + counter-a-spell → loot trigger · MEDIUM (the counter-trigger loot is the gap)
- Jegantha, the Wellspring (MUL) — companion (fine) + {T}: add WUBRG that can't pay generic · MEDIUM (restricted-mana pool)
- Gyruda, Doom of Depths (MUL) — companion (fine) + ETB each player mills 4, reanimate an even-CMC creature under your control · MEDIUM (mill-all-players then conditional reanimate)
- Yarok, the Desecrated (MUL) — ETB triggers of your permanents trigger an additional time · MEDIUM (global ETB-trigger doubling)
- Harsh Mentor (LTC) — opponent activates a non-mana ability of an artifact/creature/land → 2 damage · MEDIUM (activation-watcher punisher, like Aven Mindcensor which is only borderline)
- Sharkey, Tyrant of the Shire (LTR) — shut off + steal opponents' land activated abilities · MEDIUM (ability-grafting + any-mana-spend rider)
- Mizzix of the Izmagnus (CMM) — experience counters (supported) + {1}-less-per-experience scaling · MEDIUM (the per-experience cost scaling is the gap; OLD-08 filed the same card MEDIUM)
- Aminatou's Augury (CMM) — exile top 8; cast one spell of each card type free · MEDIUM (per-type cast-from-exile, like OLD-08 Epic Experiment)
- Alms Collector (CMM) — replacement: opponent drawing 2+ instead you and they each draw 1 · MEDIUM (draw-replacement watcher)
- Day's Undoing (CMM) — everyone shuffles hand+GY, draws 7; if your turn, end the turn · MEDIUM/ENGINE (the "end the turn" truncation is the hard part — OLD-08 filed it ENGINE-BLOCKED under E11; the wheel half is easy)
- Portal Mage (CMM) — reselect which player/PW an attacker is attacking (has partial `auto=phasealter` primitives already sketched in the file) · MEDIUM (retarget-attacker)
- Tromokratis (CMM) — hexproof-unless-attacking/blocking + can't-be-blocked-unless-all-block · MEDIUM (all-must-block evasion)
- Deification (MAT) — choose a planeswalker type; grant hexproof + a loyalty-loss-prevention replacement to your PWs of that type · MEDIUM (choose-a-subtype static + loyalty replacement)

*(E17 is a catch-all; where a card has two riders it is counted once, at its hardest blocker, in
the roll-up. Day's Undoing straddles ENGINE-BLOCKED via its "end the turn" clause — see note.)*

---

## Tier roll-up (deduped, best-fit primary tier per card, of the 49 excluded)

| Tier | Count | Dominant blockers |
|---|---|---|
| ENGINE-BLOCKED | ~24 | **multiplayer voting (Will of the council / dilemma / secret council — the biggest single engine group, 9 LTC/CMM cards)**, tempting-offer/join-forces, copy-an-ability (Rings of Brighthearth family, 5 cards), extra-loyalty-activation (Chain Veil / Oath of Teferi), change-target (Imp's Mischief), gain-control-of-spell (Commandeer), two-pile secret (Atris), damage-doubling replacement (Gisela/Obosh), activated-ability cost reduction (Training Grounds/Zirda) |
| BACKLOG-MEDIUM | ~25 | reveal-until-creature, reveal-and-cast-on-parity, counter relocation (Ozolith/Goldberry), grant-keyword (replicate/improvise), mill-then-scaled-token, pay-to-attack-with-life, prevent→counter payoff, and the E17 single-card rider tail |
| BACKLOG-EASY | 0 | — (no card here reduces to only proven primitives) |
| OUT-OF-SCOPE | 0 | no digital-only / pure-variant cards in these lists |

(Tiers are best-fit: several cards touch two buckets — e.g. Galadriel is a Ring card wrapped in a
vote; Zirda/Obosh/Gyruda/Jegantha are companions whose companion clause is fine but whose *other*
clause blocks them; Day's Undoing is a wheel + turn-truncation. Each is counted once at its hardest
blocker. Counts are indicative, not exhaustive-orthogonal.)

---

## Per-set quick table

| Set | Missing (distinct) | Distinct excluded here | Notes |
|---|---|---|---|
| MUL (Multiverse Legends) | 8 | 8 | **companions** (Jegantha, Gyruda, Zirda, Obosh) — companion clause is supported, blocked by their *other* clause; Atris (two-pile), Yarok (ETB-double), Zada (copy-for-each, shared w/ CMM) |
| MAT (March of the Machine: Aftermath) | 2 | 2 | Training Grounds (activated-ability cost reduction), Deification (choose-PW-type static + loyalty replacement) — both MEDIUM/ENGINE, no MAT-specific mechanic surfaces |
| LTR (Tales of Middle-earth) | 2 | 2 | Goldberry (counter relocation), Sharkey (ability-grafting) — **the-Ring / amass / food are all supported**, so LTR's marquee keywords do NOT appear here |
| LTC (Tales of Middle-earth Commander) | 12 | 12 | **voting flood** (Elrond, Cirdan, Erestor, Galadriel, Sail, Plea, Travel, Trap, + CMM's Custodi) — the era's dominant engine gap; plus Rings of Brighthearth (copy-ability), Ozolith, Selfless Squire, Harsh Mentor |
| CMM (Commander Masters) | 28 | 28 | reprint anthology: Chain Veil / Oath of Teferi (loyalty), Gisela (double dmg), Commandeer (steal spell), Imp's Mischief (retarget), Experiment Kraj, Day's Undoing; Tempt with Vengeance & Oreskos Explorer are **STALE** |

*(Distinct-excluded columns sum to 52 because Zada, Hedron Grinder is shared MUL∩CMM and CMM's
count includes the two STALE cards; the deduped genuinely-excluded total across all 5 sets is
**49** — 51 distinct names minus 2 STALE.)*

## Confidence & caveats

- 100% of the 49 excluded names resolve to `unsupported.txt` — this audit measures the *documented*
  unsupported set for the era, not raw Scryfall completeness. The bulk of each set (everything Wagic
  *does* implement, including all the LTR keyword commons) never appears in `missing_cards_by_sets`
  and is out of scope.
- **The 2023 era's defining gap is multiplayer VOTING.** Will of the council, council's dilemma,
  secret council, tempting offer, and join forces have **zero** supported examples anywhere in the
  catalogue. This is a genuine engine gap (no vote-tally subsystem) and accounts for the single
  largest reason group (10 cards across E1+E2). It is a natural consequence of LTC/CMM being
  Commander products.
- **LTR's marquee mechanics are SUPPORTED and are not blockers here.** the-Ring-tempts-you,
  Ring-bearer emblem tracking, amass Orc, and Food all resolve to `borderline` primitives
  (Frodo, Call of the Ring, Sauron, Orcish Bowmasters, etc.). Galadriel, Elven-Queen's Ring clause
  would work — she is blocked by the *vote* wrapped around it, not the Ring. So, unlike what the
  prompt hypothesized, there is **no Ring-emblem ENGINE-BLOCKED bucket** in this era.
- **Companion is supported** (Lurrus, Yorion, Kaheera, Umori, Lutri, Keruga all borderline), so
  MUL's four companion legends (Jegantha, Gyruda, Zirda, Obosh) are excluded for their *second*
  clause — restricted mana pool, mill-and-reanimate, activated-ability cost reduction, and
  damage-doubling respectively — not for being companions.
- **CMM is a pure reprint anthology** and its missing-list is dominated by long-standing
  engine-blocked designs already catalogued in earlier eras: The Chain Veil, Gisela, Commandeer,
  Imp's Mischief (Willbender effect), Experiment Kraj, Day's Undoing, Mizzix, Stitcher Geralf. Two
  of its entries are STALE (Tempt with Vengeance, Oreskos Explorer) and should be pulled from the
  list — no CMM-specific new mechanic exists to implement.
- **Only one cross-set reprint** (Zada, Hedron Grinder, MUL∩CMM). Unlike the OLD-08 era there is no
  heavy cross-file duplication — the doubling in each file is a within-list artifact, not genuine
  reprint overlap.
- Tier assignment is a text-based judgment call; several cards sit on an ENGINE-BLOCKED / MEDIUM
  boundary (noted inline — e.g. Day's Undoing's turn-truncation, Divergent Transformations'
  reveal-until-creature). No card was moved to EASY: every excluded card carries at least one clause
  that needs new DSL, so BACKLOG-EASY is empty for this era.
