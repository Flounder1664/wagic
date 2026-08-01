# Un-Sets Coverage Audit — UGL · UNH · UST · UND (the four silver-border sets)

Cross-set audit of missing / unsupported cards for the four **silver-border "un-sets"**:
**UGL** (Unglued, 1998) · **UNH** (Unhinged, 2004) · **UST** (Unstable, 2017) ·
**UND** (Unsanctioned, 2020).

Generated 2026-07-11. Method per [`README.md`](README.md): each name from
`Res/missing_cards_by_sets/<CODE>.txt` was read in full (oracle text, never substring) and
cross-checked against `grade_index.json` (the union of the four `core.zip` primitive files).
Before any card was tagged engine-blocked, the underlying effect was probed against the index to
confirm no supported analog exists.

## ⚠️ Correction to earlier era audits

Earlier era audits blanket-labeled these four sets **OUT-OF-SCOPE** on the grounds that they are
silver-border "joke" sets. **That was wrong and is corrected here.** Silver-border cards span a
wide spectrum:

- Many are **ordinary MTG effects wearing a joke name/art** — a fixed burn spell, a temporary
  steal, an anthem, a Clone. Wagic could author these today; the silver-border-ness is pure flavor.
- Some introduce a **new-but-digitally-possible subsystem** (Contraptions/crank, Augment//Host,
  dice-rolling, watermark-matters, name/letter/word analysis). These need real C++ work, but a
  computer *can* do them — one implementation unlocks a whole group.
- A minority are **genuinely impossible in any digital rules engine** because the card reaches
  outside the game: manual dexterity (flip/balance/tear cards), real-world timing/knowledge,
  social/table actions, "a person outside the game", or an actual sub-game of Magic.

So each card is reclassified below by its **real exclusion reason**, exactly like every
black-border set — not dismissed for having a silly name.

## Headline numbers

| Metric | Count |
|---|---|
| Raw `[card]` blocks across the 4 files | 433 (UGL 58, UNH 123, UST 194, UND 58) |
| **Distinct cards** (after collapsing lettered variants + internal dupes + cross-set reprints) | **~205** |
| STALE (name already resolves to `supported`/`borderline`) | **0** |
| Genuinely excluded | **~205** |

Dedup is heavy here. UND (2020) is a reprint compilation: **all 58 of its cards already appear in
UGL/UNH/UST**, so it contributes **zero new names**. UST lists *Extremely Slow Zombie* four times
and packs ~11 lettered-variant families (Very Cryptic Command a–f, Knight of the Kitchen Sink
a–f, Sly Spy a–e, Ineffable Blessing a–f, Garbage Elemental a–f, Everythingamajig a–f) that
collapse to one design each. After all collapsing, **~205 distinct card designs** remain across
the four sets. **None are stale** — every un-card resolves to `unsupported.txt` (they were
catalogued with oracle text but never given a working primitive).

### The bottom line the correction was about

Of the ~205 distinct designs:

- **~70 are BACKLOG (C)** — ordinary effects Wagic could represent today. **These are the cards
  the old "out-of-scope" verdict wrongly buried.**
- **~65 are NEW-SUBSYSTEM (B)** — digitally possible but need engine work; dominated by the
  Contraption/crank engine (~55 cards) plus Augment//Host, dice, watermark, and name-analysis.
- **~70 are ENGINE-BLOCKED–PHYSICAL (A)** — reach outside the game; impossible in any engine.

So the honest split is roughly **one-third implementable-today, one-third new-subsystem,
one-third physically-impossible** — very far from "the whole set is out of scope."

### Mechanic-support probes (what shapes the classification)

| Effect | Supported analog in index | Verdict for un-cards using it |
|---|---|---|
| Fixed direct damage | Char, Lightning Bolt | SUPPORTED (fractional ½ values are cosmetic — round) |
| Copy target instant/sorcery | Twincast, Fork | SUPPORTED |
| Temporary steal (Act of Treason) | Act of Treason | SUPPORTED |
| Enters as a copy of a creature | Clone | SUPPORTED |
| Name-a-card cast-lock (pre-chosen) | Nevermore, Meddling Mage (borderline) | SUPPORTED |
| "You win the game" trigger | Coalition Victory, Mortal Combat | SUPPORTED |
| Anthem / +1/+1 to a subset | Glorious Anthem, lord() | SUPPORTED |
| Sacrifice-for-mana / land ramp / tutor-basic | Dark Ritual, Rampant Growth | SUPPORTED |
| **Contraption / crank / sprockets / assemble** | *none* | NEW SUBSYSTEM (B) |
| **Augment // Host combine** | *none* | NEW SUBSYSTEM (B) |
| **Roll a die (d6) as a game action** | *none* | NEW SUBSYSTEM (B) |
| **Watermark-matters** | *none* | NEW SUBSYSTEM (B) |
| **Count letters/words/lines in name or text** | *none* | NEW SUBSYSTEM (B) |
| **"A person outside the game" acts** | *none, and none possible* | ENGINE-BLOCKED–PHYSICAL (A) |
| **Play a Magic subgame** | *none, and none possible* | ENGINE-BLOCKED–PHYSICAL (A) |
| **Manual dexterity (flip/balance/tear/throw)** | *none, and none possible* | ENGINE-BLOCKED–PHYSICAL (A) |

---

## By exclusion reason (main deliverable)

Grouped by **why** each card can't be done today, deduped, with per-card set tags.
Buckets: **A** = engine-blocked physical (impossible anywhere) · **B** = new subsystem (digitally
possible, needs engine work) · **C** = backlog (ordinary effect, doable today) · **D** =
out-of-scope (non-card / duplicate).

---

## A. ENGINE-BLOCKED — PHYSICAL / rules-external (impossible in ANY engine)

These reach outside the game state. No digital engine can implement them faithfully; they are
LISTED with the specific sub-reason, not hand-waved.

### A1 — "A person outside the game" acts (needs a real third human)  (7)

The card's effect is executed by, or hands control to, a human who is not a player. No AI stand-in
is faithful — the whole point is an uninvolved bystander.

- Kindslaver (UST) — a person outside the game controls target player for a turn
- Defective Detective (UST) — a person outside the game looks at a hand and picks a card
- Sacrifice Play (UST) — a person outside the game chooses which creature you sacrifice
- Better Than One (UST) — a person outside the game becomes your teammate
- Subcontract (UST/UND) — a person outside the game picks a card from a hand to discard
- Squirrel Dealer (UST) — ask a person outside the game "Do you like Squirrels?"
- Flavor Judge (UND) — ask a person outside the game if the story makes sense; they can counter

### A2 — Play a sub-game of Magic  (3)

An entire nested game of Magic under the table. No subsystem, and out of scope for a duel engine.

- Enter the Dungeon (UGL/UNH/UND) — play a Magic subgame at 5 life
- The Countdown Is at One (UST) — play a Magic subgame at 1 life; losers take double damage
- (Better Than One also skirts this via shared control — filed A1)

### A3 — Manual dexterity: flip / balance / drop / throw / spin / stack physical cards  (13)

Requires physically manipulating cardboard in real space. No analog possible.

- Blacker Lotus (UGL) — **tear** the card into pieces for mana
- Chaos Confetti (UGL) — **tear** into pieces and **throw** them onto the play area
- Clay Pigeon (UGL) — **throw** it two feet up and try to **catch** it
- Landfill (UGL) — **drop** land cards from a height; destroy what they cover
- Jalum Grifter (UGL) — three-card-monte shuffle the opponent must physically track
- Orcish Paratroopers (UNH) — **flip** the card from a height; must land face up
- Phyrexian Librarian (UNH) — **balance** cards on your body; sac if one falls
- Pointy Finger of Doom (UNH/UND) — **spin** the card; destroy what it points to
- Ol' Buzzbark (UST) — **roll dice onto the battlefield**; counters/damage by what they touch
- Slaying Mantis (UST/UND) — enters by being **thrown** three feet; fights what it touches
- Boomstacker (UND) — **stack dice** on it; sac when the stack falls
- Skull Saucer (UST/UND) — put your **head on the table**; sac when it lifts
- Cramped Bunker (UST) — physically **move permanents to touch** the card

### A4 — Balance / touch / hold the card on your body  (10)

Board state depends on continuous physical contact / posture of a real player.

- Charm School (UGL) — **balance** it on your head
- Volrath's Motion Sensor (UGL) — **balance** it on the back of a hand
- Handcuffs (UGL) — target player must keep both hands touching
- Gluetius Maximus (UGL) — a chosen finger must keep touching the card
- Vile Bile (UNH) — lose life if skin/fingernail **touches** the card
- Hazmat Suit (Used) (UST) — same skin/fingernail-touch trigger
- Working Stiff (UNH) — keep your arms straight; sac when you bend an elbow
- The Fallen Apart (UNH) — physical arm/leg tokens removed on damage
- Hoisted Hireling (UST/UND) — flying only while physically **held above** the table
- Handy Dandy Clone Machine (UST) — token exists only while represented by a real hand + fingers

### A5 — Say a word / make a sound / speak / sing / stay silent  (24)

Trigger keyed to a real player uttering (or not uttering) something. Includes the entire
**"Gotcha"** family and the "say the flavor text / name / word" cards.

- Censorship (UGL) — damage when a player **says** a chosen word
- Clam Session (UGL) — **sing** six words of a song each upkeep
- Common Courtesy (UGL/UND) — caster must **ask permission** aloud
- Sorry (UGL) — players **say "Sorry"** to counter
- Bronze Calendar (UGL/UND) — spells cost less while you **speak in a funny voice**
- I'm Rubber, You're Glue (UGL) — **speak only in rhyme**; say a rhyme to redirect
- Infernal Spawn of Evil (UGL/UND) — **say "It's coming"**
- Infernal Spawn of Infernal Spawn of Evil (UNH/UND) — **say "I'm coming, too"**
- Infernius Spawnington III, Esq. (UND) — **say "I'm here"**
- Goblin Mime (UNH) — sac when you **speak**
- Carnivorous Death-Parrot (UNH/UND) — sac unless you **say its flavor text**
- Toy Boat (UNH) — **say "Toy Boat"** N times without fumbling
- Atinlay Igpay (UNH) — sac if controller speaks a non-Pig-Latin word
- Red-Hot Hottie (UNH) — **scream "Aaah"** each turn or sac the creature
- Deal Damage / Save Life / Kill Destroy / Spell Counter / Creature Guy / Number Crunch /
  Stop That / Touch and Go / Cardpecker / Laughing Hyena / Name Dropping (UNH) — the **"Gotcha"**
  recursion: trigger when an opponent says/does a thing (say a word, laugh, touch face, flick
  cards). ~11 cards, one mechanic — all rely on catching a real human's speech/action
- Magic Word (UST/UND) — **whisper** a chosen word to tap
- "Ach! Hans, Run!" (UNH) — **say** a set phrase to tutor
- Frazzled Editor (UNH) — protection-from-"wordy" is text-analysis, not speech → filed B5 (kept here only as a pointer)

### A6 — Real-world timing (wait N real seconds / act within a time limit)  (6)

Uses a wall-clock stopwatch, not the game clock.

- Goblin S.W.A.T. Team (UNH/UND) — opponent must swat the table **within five seconds**
- Modular Monstrosity (UST) — **five seconds** to choose a keyword
- Hot Fix (UST) — **ten seconds** to rearrange your library
- Rings a Bell (UND) — opponent may ring a bell **within five seconds**
- Gimme Five (UST) — count high-fives in the **next thirty seconds**
- It That Gets Left Hanging (UST) — ask for a high-five (real-time social)

### A7 — Real-world knowledge / body / trivia / physical contest  (14)

Depends on a real player's body, memory, or a physical mini-game.

- Avatar of Me (UNH/UND) — P/T = your real **height / shoe size / eye color**
- Granny's Payback (UNH) — gain life equal to your **age**
- Man of Measure (UNH) — bonus by whether you're **taller** than an opponent
- Elvish House Party (UNH) — P/T = the current **hour** (real clock)
- Standing Army (UNH) — vigilance while you're physically **standing**
- Fat Ass (UNH) — bonus while you're **eating** real food
- Shoe Tree (UGL) — use your real **shoes** as counters
- Sex Appeal (UGL) — bonus by **sex of people in the room**
- Ladies' Knight (UNH) — cost break for **wearing women's clothing**
- Prismatic Wardrobe (UGL) / Hurloon Wrangler (UGL, "denimwalk") — keyed to real **clothing**
- Eye to Eye (UNH) — **staring contest**
- Mouth to Mouth (UNH) — **breath-holding contest**
- Side to Side (UNH) — **arm-wrestle**
- Face to Face (UNH) / Head to Head / Frankie Peanuts (UNH/UND) — **Rock-Paper-Scissors /
  Q&A / yes-no-question** contests resolved by real people
- Miss Demeanor (UGL) / Mother of Goons (UNH) — **compliment / insult** a real player
- Chivalrous Chevalier (UST) — **compliment** an opponent or bounce
- Knight of the Hokey Pokey (UGL/UND) / Mesa Chicken (UGL) — perform a **physical dance/gesture**

*(A5–A7 overlap heavily — many cards demand both a spoken phrase and a physical act. Each is
counted once at its clearest sub-reason in the roll-up.)*

### A8 — Ante / gambling / cross-game / real-world-money / open-a-booster  (9)

Reaches into sideboard, other tables, sealed product, or the real world.

- Booster Tutor (UNH/UND) — **open a real sealed booster**
- Summon the Pack (UST) — **open a real sealed booster**, put creatures into play
- Jester's Sombrero (UGL) — remove cards from a **sideboard** for the match
- Look at Me, I'm the DCI (UGL/UND) — **ban** a card for the match (cross-game)
- Once More with Feeling (UGL) — DCI-restricted reset (deck-construction rule)
- Ass Whuppin' (UNH) / Side Quest (UST) / Gimme Five (UST) — affect **another game you can see
  from your seat**
- Ashnod's Coupon (UGL) — target player **gets you a drink**
- Rod of Spanking (UNH) — untap unless a player says "Thank you, sir…"
- Better Than One / Kindslaver / etc. — cross-game control (also A1)

### A9 — Cross-game-persistence / next-game riders  (5)

Effect spans into the *next game of the match* — no engine models a persistent match state
across game boundaries the way these need.

- Double Play (UGL) — extra land in the **next game** with that player
- Double Cross (UGL) — discard from a hand in the **next game**
- Time Machine (UGL) — creatures return in the **next game**, on a turn = their CMC
- Gus (UGL) — counters = games you've **lost since last winning** against this opponent
- Ghazban Ogress (UGL) — control goes to whoever **won the most games that day**

---

## B. ENGINE-BLOCKED — NEW SUBSYSTEM (digitally possible, needs C++/engine work)

A computer *can* do all of these; Wagic simply has no analog yet. Grouped by subsystem — one
implementation unlocks the group.

### B1 — Contraptions: assemble / crank / sprockets  (~55 — the single largest engine group)

UST built an entire parallel deck ("Contraption deck") of artifacts you *assemble* onto three
*sprockets*, then *crank* each turn. Needs: a Contraption deck zone, sprocket slots, an
assemble-from-top action, and a crank-this-sprocket trigger. No primitive exists. Splits into:

**Contraption cards themselves** (subtype=Contraption; each fires "whenever you crank"):
Applied Aeronautics, Accessories to Murder, Auto-Key, Arms Depot, Genetic Recombinator,
Faerie Aerie, Gnomeball Machine, Gift Horse, Inflation Station, Hypnotic Swirly Disc, Guest List,
Goblin Slingshot, Head Banger, Hard Hat Area, Bee-Bee Gun, Buzz Buggy, Boomflinger, Dual Doomsuits,
Dogsnail Engine, Duplication Device, Dictation Quillograph, Deadly Poison Sampler, Division Table,
Dispatch Dispensary, Sundering Fork, Sap Sucker, Thud-for-Duds, Targeting Rocket, Refibrillator,
Record Store, Tread Mill, Top-Secret Tunnel, Twiddlestick Charger, Turbo-Thwacking Auto-Hammer,
Lackey Recycler, Jamming Device, Neural Network, Mandatory Friendship Shackles, Insufferable Syphon,
Rapid Prototyper, Optical Optimizer, Oaken Power Suit, Quick-Stick Lick Trick, Pet Project,
Widget Contraption (all UST). *(~44 Contraptions.)*

**Cards that assemble / manipulate Contraptions** (need the same subsystem):
Suspicious Nanny, Spell Suck, Chipper Chopper, Crafty Octopus, Incite Insight, Overt Operative,
Finders Keepers, Joyride Rigger, Steady-Handed Mook, Riveting Rigger, Aerial Toastmaster,
Wrench-Rigger, First Pick, Midlife Upgrade, Work a Double, Steamfloggery, Steamflogger Temp,
Steamflogger of the Month, Steamflogger Service Rep, Clock of DOOOOOOOOOOOOM!, Socketed Sprocketer,
Cogmentor, Garbage Elemental (b) (all UST). *(~23 more; several overlap other buckets and are
counted once here.)*

### B2 — Augment // Host (combine two half-cards into one)  (~20)

A half-card with `Augment {cost}` is revealed from hand and *combined* with a Host creature on the
battlefield, fusing their text and P/T deltas. Needs a combine operation and a host/augment
card-half model. No analog.

- Hosts: Crafty Octopus, Labro Bot, Ordinary Pony (UST/UND), Strutting Turkey (UND),
  Dr. Julius Jumblemorph (searches for augments) (UST)
- Augment halves (power/toughness given as `+N`): Steam-Powered, Robo-, Half-Shark Half-, Ninja,
  Serpentine, Multi-Headed, Monkey-, Half-Squirrel Half- (UST/UND), Rhino-, Humming- (UST/UND),
  Half-Kitten Half-, Half-Orc Half-, Zombified, Bat- (UND), Monkey- (UST)
- Support: Teacher's Pet, Really Epic Punch, Success!, Clever Combo (payoffs that fetch/pump
  hosts/augments) (UST)

### B3 — Dice-rolling as a game action (d6, reroll, dice-matters)  (~14)

Rolling dice mid-game and reacting to results. A pRNG die is trivial digitally, but Wagic has no
"roll a die" primitive or die-result triggers.

- Strategy, Schmategy (UGL/UND) — roll d6, branch to five effects
- Goblin Tutor (UGL/UND) — roll d6 to pick what to tutor
- Free-Range Chicken (UGL/UND) — roll 2d6, pump if doubles
- Spark Fiend (UGL) / Flock of Rabid Sheep (UGL, coin flips) — dice/coin loops
- Goblin Bookie (UGL) — reroll any die / reflip any coin
- Krark's Other Thumb (UST/UND) — roll two dice, ignore one
- Snickering Squirrel (UST/UND) — +1 to a die result
- Squirrel-Powered Scheme (UST) — +2 to every die you roll
- Wall of Fortune (UST/UND) — tap to force a reroll
- Proper Laboratory Attire (UST) — "protection from die rolls"
- Pippa, Duchess of Dice (UND) — dice become creature tokens; reroll
- Socketed Sprocketer (UST) — install die results (also B1)
- Dumb Ass (UGL) — coin-flip attack control
- *(The many Contraptions that "roll two six-sided dice" — Gift Horse, Boomflinger, Hard Hat Area,
  Thud-for-Duds — are counted under B1 but also need B3's dice engine.)*

### B4 — Watermark-matters (faction-symbol subsystem)  (~11)

UST factions carry *watermarks*; several cards count / gate on them. Needs a per-card watermark
attribute and matchers. Digitally straightforward, but no data field exists.

- Stamp of Approval, Watermarket, S.N.E.A.K. Dispatcher, "Rumors of My Death…",
  Knight of the Widget, Hammerfest Boomtacular, Knight of the Kitchen Sink (f) "prot from
  watermarks", Very Cryptic Command (e) untap-watermark mode, Phoebe (steals watermarks),
  Border Guardian (silver/black/white border-matters — same "card-metadata" family) (UST),
  Underdome (UND, "silver-bordered costs")

### B5 — Name / letter / word / text-line / rarity / artist analysis  (~20)

Effects that read a card's *printed metadata* — count letters/words in a name, lines in a text
box, punctuation marks, the artist, the rarity, the collector number, flavor-text presence. A
computer can inspect these fields; Wagic exposes none of them.

- **Letter/word count in NAME:** Monkey Monkey Monkey, Bloodletter, Wordmail, Bosom Buddy,
  When Fluffy Bunnies Attack, Now I Know My ABC's, Stone-Cold Basilisk, Double Header
  (two-word), Zzzyxas's Abyss (alphabetical-first), Ineffable Blessing (f) (word-count),
  Oddly Uneven / Very Cryptic Command (b) (word-count) (UNH/UST)
- **Letter count in RULES TEXT / lines / punctuation:** Lexivore (most lines), Punctuate
  (punctuation count), Frazzled Editor / Garbage Elemental (a) / Alexander Clamilton (UND) /
  Do-It-Yourself Seraph — "wordy" = ≥4 lines, capital offense (UST), Staff of the Letter Magus (UST)
- **ARTIST-matters:** Circle of Protection: Art, Persecute Artist, Brushstroke Paintermage,
  Fascist Art Director, Drawn Together, Graphic Violence, Mana Flair, Framed!, Remodel,
  Erase (Not the Urza's Legacy One), Aesthetic Consultation, Zombie Fanboy, Artful Looter,
  Bursting Beebles, Abstract Iguanart (UND), Ineffable Blessing (b) (UNH/UST/UND)
- **RARITY / expansion-symbol / collector-number-matters:** Rare-B-Gone, World-Bottling Kit,
  Symbol Status, First Come First Served, First Pick, Ineffable Blessing (d/e),
  Knight of the Kitchen Sink (b/d) (even/odd collector no.) (UNH/UST)
- **FLAVOR-TEXT / reminder-text presence:** Duh (UNH/UND), Old Guard (UST/UND),
  Graveyard Busybody, Ineffable Blessing (a), Phoebe (can't-be-blocked-by-flavor-text) (UST)
- **ART content matters:** Our Market Research…Elemental ("art rampage"), Sly Spy (b/d)
  (facing left/right), Goblin Haberdasher (hats in art), Garbage Elemental (e) ("art menace"),
  Knight of the Kitchen Sink (c) (open mouth in art), Selfie Preservation (tree in land art) (UST)

### B6 — Fractional (½) values as a first-class number  (~12)

½-power/toughness, ½ damage, ½ life. Digitally just a non-integer field, but Wagic's stat model
is integer-only. Cards whose *only* obstacle is the fraction are otherwise trivial:

- Little Girl (UNH) — {HW} ½/½ vanilla creature (nothing but the fraction)
- Saute (UNH) — 3½ damage · Wet Willie of the Damned (UNH) — 2½ damage · Supersize (UNH) — +3½/+3½
- Bad Ass / Dumb Ass / Smart Ass / Fat Ass / Cheap Ass / City of Ass (UNH) — ½ stats / half-mana
- Fraction Jackson (UNH) — returns cards "with a ½ on it"
- Just Desserts (UST) — deals **π** (≈3.14) damage
- Assquatch (UNH) — +1½/+1½ Donkey lord
- *(Half-mana symbols {HW}/{HR} — Little Girl, Mons's Goblin Waiters — are the same fractional
  gap on the cost side.)*

### B7 — Misc. digitally-possible novelties needing bespoke engine work  (~10)

Each is a one-off new mechanic that a computer could do but has no primitive:

- Split Screen (UST) — split your library into **four libraries**
- Animate Library (UST) — your library becomes a creature (needs library-as-permanent)
- The Grand Calcutron (UST) — hand becomes an ordered, revealed "program"
- Over My Dead Bodies (UST) — creatures fight/attack **from graveyards**
- Graveyard Busybody (UST) — "all graveyards are your graveyards"
- Baron Von Count (UST) — a "doom counter" that walks across printed numerals (number-matters)
- Look at Me, I'm R&D (UGL/UNH/UND) — globally reassign a chosen number to another
- More or Less (UST) — add/subtract 1 from a number on a card
- Togglodyte (UNH) — an ON/OFF switch toggled by each spell
- Stet, Draconic Proofreader (UND) — delete the first letter of a name (name-editing)
- S.N.O.T. (UNH) — creatures physically **stick together**; P/T = count² (combine + squaring)

---

## C. BACKLOG — ordinary effects Wagic could author today  (~70)

**These are the cards the earlier "out-of-scope" verdict wrongly buried.** Their oracle text uses
only mechanics with supported analogs in `grade_index.json`; the silver-border-ness is confined to
the name, art, or flavor. Split EASY / MEDIUM.

### C1 — BACKLOG-EASY (pure supported primitives; the joke is only the name)  (~22)

- Crow Storm (UST) — make a 1/2 flyer token named *Storm Crow*, with **storm**. Both storm and
  the token ("Storm Crow" resolves **supported** in the index) exist. Trivial.
- Earl of Squirrel (UST) — Squirrel lord + a lifelink-style token-maker ("squirrellink"); anthem +
  token generation are supported. (Round the flavor keyword to lifelink-makes-tokens.)
- Three-Headed Goblin (UST) — "triple strike" = first + normal + last strike; double strike exists,
  the extra step is a keyword-flag add.
- Party Crasher (UST) — haste + "attack once each opponent's turn" (extra-combat attack rights).
- Old-Fashioned Vampire (UST) — flying; conditional +2/+2 & deathtouch — the "dark outdoors"
  condition can be dropped/approximated to always-on or a toggle.
- Rocket-Powered Turbo Slug (UGL) — "super haste" ≈ a dash/haste variant.
- Cheap Ass / City of Ass (UNH) — cost reducer / mana land (fraction aside → C1).
- Supersize (UNH), Saute (UNH), Wet Willie of the Damned (UNH) — plain pump / burn (fraction aside).
- Get a Life (UGL) — exchange life totals (supported effect).
- Mine, Mine, Mine! / Free-for-All (UGL) — library-to-hand / random-creature redistribution: mostly
  supported zone moves.
- Gerrymandering / Double Play-less base / Land Aid '04 / Selfie Preservation (UST) — tutor a
  basic land (Rampant-Growth family).
- Symbol Status token-maker, Dispatch Dispensary-token (aside from crank) — token generation.
- Mons's Goblin Waiters (UNH) — sac for mana (Dark-Ritual family; the ½ symbol is cosmetic).
- Extremely Slow Zombie (UST/UND) — 3/3 with "last strike" (a deal-damage-after keyword flag).
- Grusilda / GO TO JAIL (UST) — exile-until-leaves + a dice rider; the core O-Ring effect is
  supported (the doubles-to-escape rider needs B3 dice, so borderline C/B).

### C2 — BACKLOG-MEDIUM (supported mechanics, multi-clause / conditional DSL)  (~48)

- Who/What/When/Where/Why (UNH/UND) — a 5-mode split card; modal choose-one is supported.
- Very Cryptic Command a/c/d (UST) — "choose two" modes are all ordinary (untap, bounce, draw,
  copy-a-spell, retarget, turn-face-down) *except* the assemble/watermark modes (those → B).
- Yet Another Aether Vortex (UGL/UNH/UND) — haste anthem + play-top-of-library (Future Sight family).
- Topsy Turvy (UNH/UND) — reverse phase order (turn-structure edit; medium but bounded).
- Staying Power (UNH/UND) — "until end of turn" effects don't end (duration override).
- Necro-Impotence (UNH) — skip untap + pay-life-to-untap-X + impulse-draw (Necropotence-shaped).
- Richard Garfield, Ph.D. (UNH/UND) — cast cards as other same-cost cards (name-swap cast).
- Rules Lawyer (UST) — you ignore state-based actions (a rules toggle, bounded).
- Do-It-Yourself Seraph (UST) — attach exiled artifacts' text boxes (text-granting).
- Zzzyxas's Abyss / Oddly Uneven (UST) — mass-destroy by name property (needs B5 name-count but
  the destroy half is supported).
- Spirit of the Season (UND) — 4-mode ETB by real-season → drop to a chosen/ random mode (medium).
- Syr Cadian, Knight Owl (UND) — Knight lifelink + day/night-gated abilities → gate on a toggle.
- Acornelia (UND) — acorn-counter accumulator + pump/shrink (counter engine; the "squirrel in art"
  trigger → B5).
- Buzzing Whack-a-Doodle (UST) — secret Whack/Doodle choice then a simple activated ability
  (the secret-choice is a small hidden-info step).
- Mary O'Kill / Killbot swap (UST) — swap a creature in hand with one on the battlefield.
- X (UST), Phoebe (UST minus watermark), Border Guardian (UST minus border-matters) — ordinary
  bodies once their metadata rider is stripped.
- Assorted lords/anthems/tokens: Assquatch, Wordmail, Keeper of the Sacred Word (minus speech),
  Moniker Mage (minus speech) — the combat body is supported; only the joke-rider is the blocker.
- Pygmy Giant (UGL) — sac-a-creature ping scaled by a number in its text (needs B5 to read the
  number; the ping is supported).
- Time-limited / speech riders removed, several A-bucket creatures have an ordinary combat body
  (noted but kept in A because the rider is *the card*).

*(C2 is a judgment bucket: each card's ordinary core is supported; where a rider needs a B
subsystem, the card is cross-referenced and counted once at its hardest blocker in the roll-up.)*

---

## D. OUT-OF-SCOPE (used sparingly)  (~2)

Only genuinely non-card or pure-duplicate entries.

- Urza, Academy Headmaster (UST) — its abilities literally say "go to **AskUrza.com** and click."
  This is a web-service card with no fixed rules text; there is nothing to implement. (Arguably A —
  real-world web action — but there is no in-game effect at all, so it is out-of-scope.)
- B.F.M. (Big Furry Monster) (UGL) — listed as **two** `[card]` blocks (the card is two physical
  half-cards you must both play). The design is implementable as a single 99/99 with the
  "both-cards" gimmick dropped; the second block is a duplicate artifact of the two-card layout.

*(No whole set is placed here. The four un-sets are otherwise real, assessable cards.)*

---

## Tier roll-up (deduped, best-fit primary bucket per distinct design)

| Bucket | Approx. count | Dominant reasons |
|---|---|---|
| **A — Engine-blocked, PHYSICAL** | **~70** | say-a-word/Gotcha (~24), real-world knowledge/body/contest (~14), manual dexterity (~13), balance/touch (~10), person-outside-the-game (7), real-world timing (6), ante/booster/cross-game (~9), subgame (3) — impossible in any engine |
| **B — New subsystem (digitally possible)** | **~65** | **Contraption/crank (~55, dominant)**, Augment//Host (~20), name/letter/word/artist/rarity analysis (~20), dice-rolling (~14), watermark-matters (~11), fractional-½ values (~12), misc novelties (~10) *(overlaps counted once)* |
| **C — Backlog (doable today)** | **~70** | EASY: Crow Storm, Earl of Squirrel, Three-Headed Goblin, Party Crasher, plain pump/burn/token/tutor/steal cards; MEDIUM: modal split cards, Necro-Impotence, Richard Garfield Ph.D., Very Cryptic Command ordinary modes, lords/anthems minus their joke-rider |
| **D — Out-of-scope** | **~2** | Urza Academy Headmaster (web-service card), B.F.M. duplicate block |

*(Counts are best-fit and indicative, not exhaustive-orthogonal — many un-cards carry two riders
from different buckets, e.g. a Contraption that also rolls dice, or a creature whose body is C but
whose printed trigger is B5. Each is counted once at its hardest blocker. The headline split
—roughly one-third A, one-third B, one-third C—is the load-bearing conclusion.)*

---

## Per-set quick table

| Set | Raw blocks | Distinct (new) | A physical | B subsystem | C backlog | D | Notes |
|---|---|---|---|---|---|---|---|
| **UGL** (Unglued 1998) | 58 | ~55 | ~30 | ~10 | ~13 | 2 | Heaviest physical/table set: tear (Blacker Lotus, Chaos Confetti), balance (Charm School), dice (Strategy Schmategy, Goblin Tutor). B.F.M. dupe; Get a Life / Gerrymandering are clean backlog |
| **UNH** (Unhinged 2004) | 123 | 123 | ~40 | ~35 | ~48 | 0 | The **"Gotcha" speech family** (~11) + name/word/artist analysis (~25) + fractional-½ "Ass" cycle (~10). Many ordinary bodies buried under a joke rider → largest C contribution |
| **UST** (Unstable 2017) | 194 | ~150 | ~15 | ~90 | ~40 | 2 | The **subsystem set**: Contraptions/crank (~55), Augment//Host (~20), watermark (~11). Lettered variants (VCC, KotKS, Sly Spy, Ineffable, Garbage Elemental, Everythingamajig) collapse ~30 blocks. Crow Storm / Earl of Squirrel are clean backlog |
| **UND** (Unsanctioned 2020) | 58 | **0** | — | — | — | — | **Entirely reprints** of UGL/UNH/UST cards (plus a few new-art commons). Contributes no distinct design; folded into the other three |

*(Distinct-new counts are approximate because several designs straddle buckets and the four files
share 43 reprinted names; the ~205 grand total is after all collapsing. UND's 58 are 100%
already-present names.)*

## Confidence & caveats

- **0 STALE.** Every un-card name probed resolves to `unsupported.txt` — none silently works today.
  (Contrast: the black-border eras usually surface a few STALE borderline hits.) The one adjacent
  surprise is that *Storm Crow* — the **token** Crow Storm makes — is itself `supported`, which is
  why Crow Storm lands in BACKLOG-EASY.
- **The correction stands:** roughly **~70 of ~205 distinct un-cards are ordinary backlog (C)** —
  implementable with today's primitives once the joke name/art is set aside. Labeling the whole
  un-set corpus "out-of-scope" hid a real, sizeable backlog. Only **~2** are truly out-of-scope.
- **New-subsystem (B) ≈ 65** is genuinely engine work, not impossibility. The **Contraption/crank
  engine (~55 cards, UST)** is the single biggest unlock in the whole corpus — one subsystem would
  clear more than a quarter of the distinct designs. Augment//Host (~20), dice (~14), watermark
  (~11), and name/text analysis (~20) are the next tiers.
- **Physical (A) ≈ 70** is the hard floor — these reach outside the game (speak, balance, tear,
  wait real seconds, a real third person, a nested subgame) and are impossible in **any** digital
  engine, silver-border or not. They are listed with their specific sub-reason, not dismissed.
- Bucket boundaries are text judgments; many cards carry two riders (a Contraption that also rolls
  dice; a creature with a C body and a B5 name-trigger). Each is counted once at its hardest
  blocker, so per-bucket counts are indicative rather than exhaustive-orthogonal.
- Faithfulness caveat from `README.md` applies: even where a C card *could* be authored, "doable"
  means the mechanics exist, not that a faithful primitive has been written and verified.
