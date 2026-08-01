# Wagic Set Coverage Audit

Cross-set audit of missing / unsupported cards. Started 2026-07-06.

> **⚠ Data moved (2026-07-15):** the machine-readable tables
> (`master_grade_table.tsv`, `gap_per_set.tsv`, `testing_worklist.*`) now live
> in the **wagic-tools** repo under `audits/`, regenerated reproducibly by
> `audits/build_audit.py` from this repo's `_cards.dat` + primitives +
> `missing_cards_by_sets/` ground truth. This directory keeps the narrative
> analysis docs only. The `*_BACKLOG.md` files in `projects/mtg/` are frozen
> history — the card-work registry in wagic-tools supersedes them.

## What "excluded" means — two distinct gap types

A card can be absent from real play for two structurally different reasons. Keep them separate:

1. **UNWRITTEN** (a.k.a. dangling reference) — the card *is* registered in the set's
   `sets/<CODE>/_cards.dat` (it has an `id=` and a `primitive=` name, so it appears in
   draft pools / deck imports), but **no primitive with that name exists** in any of the
   primitive files. At runtime the card cannot resolve — a latent correctness bug, not just
   backlog. Catalog-wide there are **~4,871** of these.
2. **UNREGISTERED** — a real card (per Scryfall) that is **not in `_cards.dat` at all**, so
   the set is simply incomplete. Upstream tracked these in
   `Res/missing_cards_by_sets/<CODE>.txt` (with full oracle text) until ~2021, when the habit
   lapsed; sets added since have no such file.

## Implementation grade (per the upstream CardCode wiki)

`grade=` "gives a hint on the quality of the code of the card, how well the card respects the
actual rules printed on it." A grade can be set per-card or as a file-level default (before the
first `[card]`). The five tiers:

| Grade | Meaning | Loads by default? | AI-deck safe? |
|---|---|---|---|
| **Supported** | Handled 100% correctly, or issues are minor | Yes | Yes |
| **Borderline** | Correct in most cases; some edge cases misbehave but "shouldn't be too much of an issue" | Yes (default cutoff) | Yes |
| **Unofficial** | Coder claims it works as advertised | — | — |
| **Crappy** | Handled, but side effects can make it "completely unbalanced" — **do not** put in an AI deck | No | No |
| **Unsupported** | "Doesn't work, mostly" — **do not** put in an AI deck | No | No |

Source: https://github.com/WagicProject/wagic/wiki/CardCode

In this fork the grade signal is carried almost entirely by **which file** a primitive lives in
(inside `Res/core.zip` → `sets/primitives/`):

- `mtg.txt` — **supported** (~14,700 cards)
- `borderline.txt` — **borderline** (~11,900). 51 carry an inline `#MISSING:` note naming the
  exact clause not faithfully implemented (e.g. "damage can't be prevented", "can't be copied").
- `planeswalkers.txt` — supported planeswalkers (~300; loyalty abilities ARE supported)
- `unsupported.txt` — **unsupported** (~1,700; catalogued with oracle text but do not work)

A set card that resolves only to an `unsupported.txt` entry is effectively **not playable** and
is counted as excluded, not implemented.

### ⚠️ Grade measures PRESENCE, not FAITHFULNESS

The audit's grade = *which file the primitive lives in*. That tells you a primitive of that name
**exists and loads** — it does **not** verify the primitive faithfully implements the printed card.
A primitive can sit in `mtg.txt` (graded "supported") yet be an **approximation that strips a
mechanic**. This is **systemic in this fork's hand-authored recent standard sets**, confirmed by body
inspection of both:

- **ECL** — first reported "278/278, 100%"; ~26 new-mechanic cards ship with the keyword removed
  (**vivid 0/14** faithful, behold 2/12, blight 19/24). See `../ECL_BACKLOG.md`.
- **EOE** — of cards that have a primitive body, **warp 4/50**, **station 5/28**, **void 4/14** are
  faithful; the rest are playable approximations (e.g. Rescue Skiff ships as a vanilla 5/6 with the
  Station mechanic gone). EOE's own batch notes admit "warp stripped, effects simplified."

So "implemented" counts across this audit are an **upper bound on presence, not a guarantee of
correctness** — especially for the fork's own new-set work (ECL, EOE; and by extension any
hand-authored new-mechanic cards in SOS/TLA/TMT/FIN/SPM that resolve to a primitive). Reprints reusing
long-existing primitives are lower-risk. Verifying faithfulness requires reading primitive bodies
against oracle text, done exhaustively only for ECL and spot-checked for EOE. Borderline cards
additionally carry known-approximate `#MISSING:` notes.

## Exclusion-reason buckets (qualitative)

For each excluded card (UNWRITTEN or UNREGISTERED):

- **ENGINE-BLOCKED** — needs a mechanic Wagic has no analog for. Name the specific mechanic and
  group same-mechanic cards. (Classic examples: ante, manual dexterity, subgames.)
- **BACKLOG-EASY** — uses only mechanics fully supported elsewhere; trivial to author.
- **BACKLOG-MEDIUM** — supported mechanics, but needs careful multi-clause / conditional DSL.
- **OUT-OF-SCOPE** — not a distinct playable paper card (digital-only/Alchemy rebalance, pure
  alternate-art variant of an already-implemented name, etc.).

## Method

- Ground truth for a set's true card list: Scryfall bulk dump
  (`all-cards-YYYYMMDD.json`), filtered by set code, `lang:en`, deduped by name.
- "Really implemented" = the `_cards.dat` `primitive=` name resolves to a `supported` or
  `borderline` grade in `grade_index.json` (built from the four primitive files).
- Terminology is normalized here: what one early per-set doc called "DANGLING-REFERENCE" and
  another called "backlog, 0 dangling" are both **UNWRITTEN** as defined above.

## Artifacts

- [`master_grade_table.tsv`](master_grade_table.tsv) — every set: registered / supported /
  borderline / unsupported / unwritten counts. The mechanical backbone; consistent across all
  343 sets.
- Per-set / per-era qualitative docs: `../<CODE>_BACKLOG.md`, `../SET_BACKLOG.md` (index),
  and grouped-era docs in this folder.

## Status

| Set | True | Implemented | Excluded | Notes |
|---|---|---|---|---|
| FIN | 313 | 137 | 176 | all excluded are UNWRITTEN; 11 engine-blocked (MDFC/meld) — `../FIN_BACKLOG.md` |
| EOE | 266 | 203* | 63 | *many "implemented" are approximations — warp 4/50, station 5/28, void 4/14 faithful (bodies stripped); Dominion Bracelet engine-blocked — `../EOE_TODO.md` |
| SPM | 193 | 110 | 83 | all excluded are UNWRITTEN; 1 engine-blocked (Web-slinging) — `../SPM_BACKLOG.md` |
| SOS | 271 | 49 | 209 | +5 engine basics, +8 written-but-not-wired (cheap); 0 dangling/0 unsupported; 52 engine-blocked (copy-split 36, converge 9, paradigm 5, pw 2) — `../SOS_BACKLOG.md` |
| TLA | 286 | 49 | 237 | all excluded UNWRITTEN; 4 new keyword walls (Waterbend/Earthbend/Airbend/Exhaust) — `../TLA_BACKLOG.md` |
| ECL | 278 | 278* | 0 | *registered & playable but NOT faithful: ~26 new-mechanic cards strip the keyword (vivid 0/14, behold 2/12, blight 19/24) — `../ECL_BACKLOG.md` |
| TMT | 195 | 16 | 179 | all excluded UNWRITTEN; only Sneak (26) a real wall; Alliance/Disappear refuted — `../TMT_BACKLOG.md` |
