# Adding New Sets to Wagic — Session Briefing

Self-contained reference for a new session picking up set-addition work.
Repo: `M:\Claude_projects\wagic\` / GitHub: https://github.com/WagicProject/wagic

---

## How Sets Work (Architecture)

### Two-layer system

**Layer 1 — Primitives** (`Res/sets/primitives/`)
Global card definitions. Shared across all sets. One entry per unique card name.
Files (load order doesn't matter — all loaded at startup):
- `mtg.txt` — main supported cards (~25,785 card names)
- `borderline.txt` — complex/partially working cards
- `unsupported.txt` — not playable
- `planeswalkers.txt` — planeswalker cards
- `_macros.txt` — ability shorthand macros

**Layer 2 — Set folders** (`Res/sets/SETCODE/`)
Set-specific metadata. References primitives by name. Auto-discovered — no registration needed.

### File structure per set
```
Res/sets/TMT/
  _cards.dat          ← required; metadata + card list
  1234.jpg            ← optional; full-size card art (cardId.jpg)
  thumbnails/
    1234.jpg          ← optional; thumbnail (45x64px)
```

### `_cards.dat` format
```
[meta]
name=Teenage Mutant Ninja Turtles
author=Your Name
orderindex=UBY-ZZ1.TMT
year=2026-03-06
total=195
[/meta]
[card]
primitive=Leonardo, Sewer Samurai
id=700001
rarity=R
[/card]
[card]
primitive=Negate
id=700002
rarity=C
[/card]
```
- `primitive=` must exactly match `name=` in a primitives file
- `id=` is unique numeric ID — used for image filenames; pick a range not used by other sets
- `rarity=` C / U / R / M

### Primitive format
```
[card]
name=Leatherhead, Swamp Stalker
auto=trample
auto=@movedTo(this|mybattlefield):damage:3 target(player|opponentbattlefield)
text=Trample -- When Leatherhead enters, it deals 3 damage to target player.
mana={3}{B}{G}
type=Creature
subtype=Crocodile Mutant
power=5
toughness=4
[/card]
```

**Key fields:**
- `name=` — unique, must match primitive= in _cards.dat
- `mana=` — `{W}{U}{B}{R}{G}` for colours, `{1}{2}` for generic, `{X}`, `{T}`
- `type=` — Creature / Instant / Sorcery / Enchantment / Artifact / Land / Planeswalker
- `subtype=` — space-separated (e.g. `Human Ninja`)
- `power=` / `toughness=` — creatures only; `*` for variable
- `abilities=` — comma-separated keywords (flying, trample, haste, menace, vigilance, deathtouch, lifelink, reach, first strike, double strike, hexproof, indestructible, ward, etc.)
- `auto=` — ability language (see below); multiple lines allowed
- `text=` — display text only, no game effect

### Ability language quick reference
```
# Mana abilities
{T}: Add {G}                     → auto={T}:Add{G}

# Damage
damage:3 target(creature|any)   → auto=damage:3 target(creature|any)
damage:2 target(player)

# Counters
counter(1/1)                     → put +1/+1 counter on this
counter(1/1) target(creature|mybattlefield)

# Draw / discard
draw:1                           → draw 1 card
discard:1 target(player)

# Life
life:3 controller                → gain 3 life
life:-2 target(player)

# Zone movement
moveto(graveyard)
moveto(mybattlefield) target(creature|mygraveyard)
moveto(exile)

# Triggers
@movedTo(this|mybattlefield):   → when this enters the battlefield (ETB)
@movedTo(*|graveyard):          → when any permanent goes to graveyard
@movedTo(creature[-this]|mybattlefield):  → when another creature ETBs
@attacking(this):               → when this attacks
@damaged(this):                 → when this takes damage

# Conditions
if type(creature|mybattlefield)~morethan~2 then draw:1
restriction{compare(hascntlevel)~equalto~2}

# Timing modifiers
ueot                             → until end of turn
asSorcery                       → can only activate at sorcery speed

# Tokens
token(1/1,creature,Soldier,white)
token(0/0,artifact,Mutagen,colorless)

# Affinity
abilities=affinityartifacts      → affinity for artifacts
abilities=affinityswamps

# Copy
copy target(spell|stack)

# Selectors
mybattlefield / opponentbattlefield / mygraveyard / myhand / mylibrary
target(creature) / target(player) / target(any)
all(creature|mybattlefield)
*[-creature]                     → non-creature
*[instant;sorcery]              → instant or sorcery
```

### Class cards (level-up enchantments)
Already implemented in borderline.txt using level counters:
```
auto=counter(0/0,1,Level)
auto=this(variable{hascntlevel}=1) {COST}:name(Level 2) counter(0/0,1,Level) asSorcery
auto=this(variable{hascntlevel}=2) {COST}:name(Level 3) counter(0/0,1,Level) asSorcery
auto=@counteradded(0/0,1,Level) from(this) restriction{compare(hascntlevel)~equalto~3}:EFFECT
type=Enchantment
subtype=Class
```
TMT's 11 Technique cards (Leonardo's Technique, Raphael's Technique, etc.) use this pattern.

### Macros (`_macros.txt`)
Check for existing shorthand before writing long `auto=` chains:
```
AUTO_DEFINE _LANDFALL_ @movedTo(land|mybattlefield):
AUTO_DEFINE _HEROIC_   @targeted(this) from(*[instant;sorcery;aura]|myCastingzone):
AUTO_DEFINE _SCRY1_    scry:1 ...
```

---

## Effort Classification

### Simple — primitive already exists
Just add a `[card]` block to `_cards.dat`. No new code.
Check with:
```python
import re
names = set()
for f in ['Res/sets/primitives/mtg.txt', 'Res/sets/primitives/borderline.txt']:
    for line in open(f, encoding='utf-8', errors='ignore'):
        m = re.match(r'^name=(.+)', line.strip())
        if m: names.add(m.group(1).lower())
# then: card_name.lower() in names
```

### Hard — mechanic exists, write new primitive
The ability language can express it. No C++ needed.
Most standard MTG mechanics are covered:
- All keyword abilities (flying, trample, etc.)
- +1/+1 counters
- ETB / death / attack triggers
- Draw, damage, life gain/loss effects
- Food tokens, Treasure tokens, Clue tokens
- Affinity (affinityartifacts, affinityswamps, etc.)
- Class / level-up enchantments
- Mutagen tokens (colorless artifact token with tap+sac ability)

Time per card: 30 min – 2 hours to write and verify.

### Really Hard — new C++ class required
Mechanics with no existing Wagic equivalent. Each requires:
1. New subclass of `MTGAbility` in `AllAbilities.h`
2. Registration in `parseMagicLine()` in `MTGAbility.cpp` (8500-line function)
3. Then primitives can use the new keyword

**Currently unimplemented mechanics needed for TMT:**

| Mechanic | Description | C++ Complexity |
|----------|-------------|----------------|
| **Sneak** | Cast during declare-blockers for alt cost; return unblocked attacker to hand; creature enters tapped and attacking same target | Medium-High — similar to Ninjutsu (already in Wagic) but cast-based not activated; study `NinjutsuAbility` class as starting point |
| **Disappear** | Ability word: triggers when permanents leave the battlefield under your control; some cards track cumulative count within a turn | Medium — LTB triggers exist (`@movedFrom`) but per-turn cumulative tracking needs a new state counter in GameObserver |
| **Alliance** | "Whenever another creature enters the battlefield under your control" | Low-Medium — ETB triggers exist but Alliance needs a "not-self" another-creature filter; check `TrCardAddedToZone` in AllAbilities.h as starting point |

---

## Missing Sets Backlog

| Code | Name | Release | Base Cards | MTG Universe? |
|------|------|---------|------------|---------------|
| FIN | Final Fantasy | 2025-06-13 | ~309 | No (IP) |
| EOE | Edge of Eternities | 2025-08-01 | ~374 | Yes |
| SPM | Marvel's Spider-Man | 2025-09-26 | 300 | No (IP) |
| TLA | Avatar: The Last Airbender | 2025-11-21 | 414 | No (IP) |
| ECL | Lorwyn Eclipsed | 2026-01-23 | ~408 | Yes |
| TMT | Teenage Mutant Ninja Turtles | 2026-03-06 | 320 | No (IP) |
| SOS | Secrets of Strixhaven | 2026-04-24 | ~305 | Yes |

**Recommended order:** ECL → SOS → EOE first (MTG-universe, mostly existing mechanics). IP sets (TMT, SPM, TLA, FIN) after.

---

## TMT Detailed Analysis (sample set)

195 unique cards (base set excluding alt-art variants).

| Category | Count | Details |
|----------|-------|---------|
| Simple | 8 | Swamp, Forest, Mountain, Island, Plains, Negate, Escape Tunnel, Make Your Move |
| Hard | ~105 | Standard keywords, +1/+1 counters, ETB/death triggers, Food/Pizza tokens, Mutagen tokens, Class/Technique cycle (11 cards), Affinity |
| Really Hard | ~75 | Alliance (~15), Disappear (~20), Sneak (~20), complex one-offs (~20) |

Once Alliance, Disappear, and Sneak are implemented in C++, all cards using those mechanics become Hard.

---

## Key File Paths

```
Res/sets/primitives/mtg.txt          main card definitions
Res/sets/primitives/borderline.txt   complex cards (Class, etc.)
Res/sets/primitives/_macros.txt      ability macros
Res/sets/SETCODE/_cards.dat          set metadata + card list
Res/ai/baka/deck1.txt               AI deck format (for new decks)
SET_BACKLOG.md                       this project's set backlog
```

**C++ ability files (Really Hard work):**
```
projects/mtg/include/AllAbilities.h          ability subclasses (~200 classes)
projects/mtg/src/MTGAbility.cpp              parseMagicLine() dispatcher (8500 lines)
projects/mtg/src/AbilityParser.cpp           macro expansion
```

## AI Deck Format
```
#NAME:My Deck
#DESC:Deck description
CardName (SETCODE) (*) * 2
AnotherCard (SETCODE) (*) * 4
```
Place in `Res/ai/baka/deckN.txt`. Game auto-discovers by number.

## Workflow for a New Set

1. **Check existing primitives** — run the Python name-check script above
2. **Create `Res/sets/SETCODE/_cards.dat`** — meta block + one [card] per existing primitive
3. **Write new primitives** — add to `mtg.txt` (or `borderline.txt` if complex)
4. **Build and test** — ndk-build + ant + assemble_apk.py + sign_apk.bat (Android)
5. **Push modrules.xml / resource update** — push_modrules.bat for menu changes; for primitives changes, resource zip must be rebuilt: `cd Res && python createResourceZip.py -p android -n core.zip`
6. **Deploy** — copy updated zip to device or use push_modrules.bat pattern for individual files

## Build Scripts (Android)
```
Android/ndk_build.bat         → compile C++ → libs/arm64-v8a/*.so
Android/assemble_apk.py       → assemble APK from Wagic.ap_ + classes.dex + .so
Android/sign_apk.bat          → sign with debug keystore → Wagic-debug.apk
Android/push_modrules.bat     → push single resource file to device
```
Resource zip rebuild (needed when adding/editing primitives or set files):
```bash
cd projects/mtg/bin/Res
python createResourceZip.py -p android -n core.zip
# Then push core.zip to device at Wagic/Res/ path
```
Note: C++ changes (new abilities) require ndk-build + APK reinstall.
Resource-only changes (primitives, set files) only require zip rebuild + push to device.
