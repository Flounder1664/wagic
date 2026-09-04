# FR: choose which art a card uses, by card name

**Raised by John, 2026-09-04.** Not started - this is a placeholder with the findings that
prompted it, so the work can begin without re-deriving them.

## Why

A card name can legitimately own several images. Basic lands carry many arts (HOB registers
`Plains` ten times), and alt-art / showcase / borderless printings are separate Scryfall
printings of the same card. Measured 2026-09-04:

| set | id rows | distinct names | names with >1 id |
|---|---:|---:|---:|
| HOB | 317 | 195 | 77 |
| HOC | 122 | 119 | 3 |
| MSC, MSH, SOC, EOC | - | same as ids | 0 |

Today those extra ids exist but there is no way to pick between them: Wagic resolves art
by card name, so whichever id the lookup lands on is what you see, for every copy, forever.

## What is wanted

1. **In-game deck editor** - selecting a card should let the player choose which printing's
   art that card uses, and remember it per deck (or per profile).
2. **The tools app deck editor** (wagic-tools) - the same choice, so a deck built in the app
   carries its art choices into the game.

Both halves need the same underlying thing: a stable way to say "this card name, that
image", surviving a rebuild of `core.zip` and a re-intake of the set.

## Open questions to settle first

- **Where the choice is stored.** Per deck file is simplest and travels with the deck; per
  profile is fewer keystrokes for a player with a favourite art. Deck file is probably right.
- **What identifies the art.** The Wagic id is stable today but is assigned by the intake
  ledger; a Scryfall printing id would survive re-intake but means carrying a second key.
- **Intake policy, which is currently drifting.** HOB/HOC were intaken per printing,
  everything since per name. Per-printing intake is what makes alternates *exist* at all, so
  this FR only has material to work with in sets intaken that way. Decide the policy before
  building the picker, or it will have nothing to pick from in most sets.

## Related

- `wagic-tools/audits/README.md` - "Per-set gap: count DISTINCT NAMES, never id rows"
- The art pipeline that stages images: `wagic-tools/check_new_sets.py`
