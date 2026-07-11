# OLD-02 — Late-90s Sets Coverage Audit (1997–2000)

> **CORRECTION (2026-07-11):** this doc's treatment of **UGL (Unglued)** as wholesale
> out-of-scope is superseded. Un-sets are NOT out-of-scope — see
> [UNSETS_AUDIT.md](UNSETS_AUDIT.md), which reclassifies un-cards by real reason (~⅓ physically
> impossible, ~⅓ new-subsystem, ~⅓ implementable-today). Non-UGL findings below stand.

Cross-set audit of missing / unsupported cards for the late-90s era.
Generated 2026-07-06. See [`audits/README.md`](README.md) for grade tiers and
exclusion-reason bucket definitions.

Sets in scope (release order): **VIS 5ED WTH TMP STH EXO P02 UGL USG ULG 6ED UDS
S99 PTK MRQ NMS**.

Source for each excluded card: `Res/missing_cards_by_sets/<CODE>.txt`
(full oracle text). Staleness cross-checked against `grade_index.json`
(28,570 primitives; the four `core.zip/sets/primitives/*.txt` files).

## Headline numbers

| Metric | Count |
|---|---|
| Distinct missing card names (deduped across all 16 sets) | **205** |
| **STALE** (listed missing but actually implemented `supported`/`borderline`) | **2** |
| Genuinely excluded (unsupported / truly-absent) | **203** |

Every non-stale name here resolves only to an `unsupported.txt` entry (or, in one
UGL case, is absent from the index entirely). None are `supported`/`borderline`,
so the "missing" list for this era is accurate apart from the two stale rows.

### STALE — remove from the missing list (already implemented)

| Card | Set(s) | Actual grade | File |
|---|---|---|---|
| Crown of the Ages | 5ED | borderline | borderline.txt |
| Necromancy | VIS | borderline | borderline.txt |

Both are real, playable primitives today; the per-set `missing_cards` file is out
of date for them. (Necromancy also reprinted in later sets; Crown of the Ages is
the Aura-mover.)

---

## Engine-support findings (probed against `grade_index.json`)

These determine ENGINE-BLOCKED vs BACKLOG for whole mechanic groups:

| Mechanic | Wagic support? | Evidence (implemented examples) | Verdict |
|---|---|---|---|
| **Phasing** | **Supported** | Teferi's Veil, Reality Ripple, Frenetic Efreet, Breezekeeper (all `supported`) | BACKLOG, not blocked |
| **Cumulative upkeep** | **Supported** | Mystic Remora, Braid of Fire, Drop of Honey (all `supported`) | BACKLOG |
| **Coin flip** | **Partial** | Frenetic Efreet, Aleatory, Goblin Archaeologist `supported`; Krark's Thumb, Fiery Gambit, Karplusan Minotaur `unsupported` | BACKLOG-MEDIUM |
| **Banding** | **Not supported** | Icatian Infantry, Master of the Hunt, Camel, Benalish Hero all `unsupported`; no faithful banding primitive | **ENGINE-BLOCKED** |
| **Dice / un-card physical & meta effects** | **No** | — | ENGINE-BLOCKED / OUT-OF-SCOPE |

So for this era the only true hard engine wall is **banding** (plus the Unglued
physical/meta silver-border cards, which are out of scope by design).

---

## By exclusion reason (main deliverable, deduped)

Each distinct card appears once, tagged with the set code(s) it is missing from.

### ENGINE-BLOCKED

#### Banding — Wagic has no banding combat model (11)
Bands-attack / damage-assignment rules are not modeled. Grants-banding artifacts
are equally blocked.

| Card | Set(s) | Note |
|---|---|---|
| Benalish Hero | 5ED | vanilla banding |
| Icatian Phalanx | 5ED | vanilla banding |
| Pikemen | 5ED | first strike + banding |
| Shield Bearer | 5ED | banding wall |
| Mesa Pegasus | 5ED | flying + banding |
| Kjeldoran Skycaptain | 5ED | flying/first strike/banding |
| Benalish Infantry | WTH | vanilla banding |
| Volunteer Reserves | WTH | banding + cumulative upkeep |
| Helm of Chatzuk | 5ED | artifact that *grants* banding |
| Battering Ram | 5ED | gains banding each combat |
| — | — | (Kjeldoran Royal Guard / Personal Incarnation etc. are NOT banding — see below) |

#### UN-CARD / non-functional silver-border (Unglued) — OUT-OF-SCOPE by design (57)
Unglued (UGL) is a silver-border joke set. The great majority rely on physical
dexterity, real-world social/meta actions, dice, coin flips, cross-game state, or
un-modelable rules text. Classified OUT-OF-SCOPE (a few are dice/coin, noted).

| Card | Reason class |
|---|---|
| Spatula of the Ages | fetches "Unglued supplement" cards — meta |
| Strategy, Schmategy | six-sided die table |
| Charm School | balance-on-head physical |
| Landfill | drop cards from a height — physical |
| Jalum Grifter | shell-game physical |
| Burning Cinder Fury of Crimson Chaos Fire | meta control-swap on tap |
| Prismatic Wardrobe | "clothing worn by controller" — real-world |
| Ghazban Ogress | "player who won most games that day" — meta |
| Miss Demeanor | "compliment the player" — social |
| Squirrel Farm | "name the artist" — meta trivia |
| Goblin Bookie | reflip coin / reroll die |
| Knight of the Hokey Pokey | dance to activate — physical |
| Get a Life | teammate life-swap (multiplayer meta) |
| Mine, Mine, Mine! | joke library-to-hand engine |
| B.F.M. | two-card 15-black creature — joke |
| Ow | say "Ow" — social |
| Infernal Spawn of Evil | say "It's coming" — social |
| Jester's Sombrero | remove sideboard cards for match — meta |
| Handcuffs | keep hands together — physical |
| Free-Range Chicken | two-dice roll |
| Goblin Tutor | die-roll tutor |
| Ricochet | per-player die roll redirect |
| Volrath's Motion Sensor | balance-on-hand physical |
| Spark Fiend | craps dice engine |
| Gus | cross-game win/loss counters — meta |
| Common Courtesy | "ask permission" — social |
| Checks and Balances | multiplayer social counter |
| Censorship | say a censored word — social |
| Clam Session | sing a song — social |
| Cardboard Carapace | counts physical copies "with you" — meta |
| Lexivore | "most lines of text" — trivia/meta |
| Gerrymandering | joke land-shuffle (multiplayer) |
| Clay Pigeon | throw & catch card — physical |
| Blacker Lotus | tear the card up — physical |
| Mirror Mirror | swap entire game state |
| Deadhead | "loses contact with hand" trigger — physical |
| Temp of the Damned | die-roll funk counters |
| Flock of Rabid Sheep | X coin flips |
| Sex Appeal | "players of opposite sex in the room" — social |
| The Ultimate Nightmare of Wizards of the Coast® Customer Service | joke X/Y/Z targeting (not in index due to ® encoding) |
| Chaos Confetti | tear & throw — physical |
| Hurloon Wrangler | "denimwalk" — real-world clothing |
| Bronze Calendar | "speak in a different voice" — social |
| Double Play | cross-game land search — meta |
| I'm Rubber, You're Glue | speak in rhyme — social |
| Look at Me, I'm the DCI | ban a card for the match — meta |
| Once More with Feeling | restart the game — meta |
| Psychic Network | card on forehead — physical |
| Bureaucracy | action-queue social ritual |
| Free-for-All | joke random-creature multiplayer engine |
| Sorry | say "Sorry" — social |
| Urza's Contact Lenses | clap hands — physical |
| Ashnod's Coupon | "get you a drink" — real-world |
| Denied! | look at hand + counter (borderline playable but silver-border joke) |
| Double Cross | cross-game discard — meta |
| Mesa Chicken | flap arms + cluck — physical |
| Giant Fan | counter-mover (one of the few mechanically-clean UGL cards) |

> Note: **all 57 distinct UGL cards are OUT-OF-SCOPE**. The set has no
> non-silver-border reprints in its missing list. Treated as a single OUT-OF-SCOPE
> block. (B.F.M. appears twice in the source file — the two physical halves — hence
> 58 card-blocks but 57 distinct names.)

### BACKLOG — mechanics Wagic supports elsewhere

#### PHASING (engine supports it; authoring needed) — BACKLOG-MEDIUM (6)
| Card | Set(s) | Note |
|---|---|---|
| Shimmering Efreet | VIS | self-phasing + phase-out a creature on phase-in |
| Ertai's Familiar | WTH | phasing + mill on phase-out; {U} lock |
| Time and Tide | VIS | mass phase in/out toggle |
| Vision Charm | VIS | modal, one mode phases an artifact out |
| Equipoise | VIS | per-upkeep symmetric phase-out by permanent type |
| Sands of Time | VIS | untap-step replacement (phasing-adjacent timing) |

#### CUMULATIVE UPKEEP one-offs — BACKLOG-MEDIUM (2)
| Card | Set(s) | Note |
|---|---|---|
| Corrosion | VIS | cumulative upkeep + rust-counter artifact destruction (also multi-clause) |
| Volunteer Reserves | WTH | *also banding → ENGINE-BLOCKED wins* (listed under Banding) |

#### COIN-FLIP / DICE (partial engine support) — BACKLOG-MEDIUM (4)
| Card | Set(s) | Note |
|---|---|---|
| Desperate Gambit | WTH | flip: double or prevent next damage |
| Mogg Assassin | EXO | flip to destroy chosen creature |
| Game of Chaos | 5ED | escalating coin-flip life swing |
| Mana Clash | 5ED | repeated coin flips for damage |
| Crooked Scales | MRQ | flip to destroy, repeatable |

#### TEXT-CHANGING effects — BACKLOG-MEDIUM (4)
Change color words / land types on a spell or permanent. Niche but supported-ish
patterns exist; needs careful DSL.
| Card | Set(s) |
|---|---|
| Magical Hack | 5ED |
| Sleight of Mind | 5ED |
| Whim of Volrath | TMP (buyback + text change) |
| (Vision Charm's land-type mode) | VIS — counted under Phasing |

#### "The next time … prevent/redirect damage" shields — BACKLOG-EASY/MEDIUM (many)
A large, cohesive group: create a one-shot damage-prevention or redirection
replacement ("the next time a source of your choice…"). Common, well-trodden DSL.
| Card | Set(s) | Kind |
|---|---|---|
| Honorable Passage | VIS | prevent + reflect red |
| Righteous Aura | VIS, MRQ | prevent damage to you |
| Reverse Damage | 5ED, 6ED | prevent + gain life |
| Sacred Boon | 5ED | prevent + +0/+1 counters |
| Greater Realm of Preservation | 5ED | prevent black/red |
| Jade Monolith | 5ED, 6ED | redirect creature damage to you |
| Pentagram of the Ages | 5ED, 6ED | prevent damage to you |
| General's Regalia | MRQ | redirect to your creature |
| Story Circle | MRQ | prevent chosen-color (CircleOfProtection-like) |
| Kithkin Armor | WTH | prevent + block restriction |
| Kor Chant | EXO | redirect all damage to another creature |
| Penance | EXO | prevent black/red, hand-to-library cost |
| Martyr's Cause | ULG | sac creature to prevent |
| Invulnerability | TMP | buyback + prevent to you |
| Temper | STH | prevent X + +1/+1 counters |
| Warrior en-Kor / Shaman en-Kor / Nomads en-Kor / Spirit en-Kor / Lancers en-Kor | STH | redirect combat damage to own creature (en-Kor cycle) |
| Cho-Arrim Alchemist | MRQ | prevent + gain life (already has partial `auto=`) |

#### Combat / blocking modifiers — BACKLOG-MEDIUM
| Card | Set(s) | Note |
|---|---|---|
| High Ground | EXO | each creature blocks an extra creature |
| Crawlspace | ULG | at most two attackers |
| Defensive Formation | USG | you assign your blockers' damage |
| Invasion Plans | STH | all block; attacker chooses blocks |
| No Quarter | TMP | destroy on power-mismatch block |
| Treefolk Mystic | ULG | destroy Auras on block |
| Kjeldoran Royal Guard | 5ED, 6ED | redirect unblocked combat damage to self |
| Maddening Imp | TMP | force attacks (Lure-of-attackers) |
| Oracle en-Vec | TMP | force chosen creatures to attack next turn |
| Ogre Enforcer | VIS | "can't be destroyed by lethal damage unless single-source lethal" |
| Zhalfirin Crusader | VIS | flanking + damage redirect |
| Knight of Valor | VIS | flanking + mass -1/-1 |
| Soltari Guerrillas | TMP | shadow + redirect combat damage |

#### Control-exchange / steal effects — BACKLOG-MEDIUM (multi-clause)
| Card | Set(s) | Note |
|---|---|---|
| The Wretched | 5ED | gain control of blockers |
| Gilded Drake | USG | ETB swap control |
| Juxtapose | 5ED, 6ED | swap highest-CMC creature & artifact |
| Legerdemain | TMP | swap artifact/creature + another |
| Gauntlets of Chaos | 5ED | swap + destroy Auras |
| Illicit Auction | 6ED | bid life for control (multiplayer-ish) |
| Rootwater Matriarch | TMP | control enchanted creature |
| Seasinger | 5ED | control creature while tapped |
| Charisma | MRQ | steal on combat damage |
| Coffin Queen | TMP | reanimate under your control |
| Bone Dancer | WTH | steal from graveyard on unblocked hit |
| Liu Bei, Lord of Shu | PTK | horsemanship + conditional buff (horsemanship ≈ fear/unblockable, easy) |

#### Counter / target-changing spells — BACKLOG-MEDIUM
| Card | Set(s) | Note |
|---|---|---|
| Desertion | VIS, 6ED | counter + steal artifact/creature |
| Power Sink | 5ED, 6ED, TMP, USG | counter unless pay X + tap lands |
| Deflection | 5ED, 6ED | change target of single-target spell |
| Rebound | STH | change target (player-only) |
| Silver Wyvern | STH | change target of spell targeting it |
| Interdict | TMP | counter activated ability + draw |
| Ertai's Meddling | TMP | delay-counter re-cast (complex) |
| Flash | 6ED | put creature into play then pay-or-sacrifice |

#### Licid cycle — BACKLOG-MEDIUM (becomes-an-Aura creatures) (14)
Tempest-block "Licid" creatures: `{cost},{T}` to turn the creature into an Aura it
attaches, reversible. A single reusable pattern would unlock the whole cycle.
| Card | Set(s) | Granted effect |
|---|---|---|
| Gliding Licid | STH | flying |
| Calming Licid | STH | can't attack |
| Tempting Licid | STH | must be blocked |
| Corrupting Licid | STH | fear |
| Convulsing Licid | STH | can't block |
| Nurturing Licid | TMP | regenerate |
| Leeching Licid | TMP | upkeep damage |
| Enraging Licid | TMP | haste |
| Quickening Licid | TMP | first strike |
| Stinging Licid | TMP | damage on tap |
| Dominating Licid | EXO | control creature |
| Transmogrifying Licid | EXO | +1/+1 + artifact |

#### Mana / land manipulation — BACKLOG-MEDIUM
| Card | Set(s) | Note |
|---|---|---|
| Drain Power | 5ED | steal opponent's mana |
| Piracy | P02, S99 | tap opponents' lands for mana |
| Carpet of Flowers | USG | mana per opponent's Islands |
| Thran Turbine | USG | restricted mana |
| Mana Cache | NMS | charge-counter mana |
| Mana Web | WTH | tap all same-color lands |
| Pygmy Hippo | VIS | drain defender's mana on hit |
| Desolation | VIS | sac land if tapped for mana |
| Sulfuric Vapors | USG | +1 to red spell damage |
| Celestial Dawn | 6ED | lands→Plains, color-fixing |

#### Enchantment / world / static one-offs — BACKLOG-MEDIUM
| Card | Set(s) | Note |
|---|---|---|
| Oath of Druids | EXO | conditional reveal-to-creature |
| Oath of Scholars | EXO | conditional wheel |
| Limited Resources | EXO | land-count lock |
| Damping Engine | ULG | permanent-parity lock |
| Common Cause | MRQ | conditional +2/+2 |
| Multani's Presence | ULG | draw when countered |
| Serra's Hymn | USG | verse-counter prevention |
| Elkin Lair | VIS | world enchantment, exile-and-play |
| Duplicity | TMP | hand-swap exile engine |
| Storage Matrix | UDS | choose-a-type untap restriction |
| Sands of Time | VIS | (also under Phasing) |
| Corrosion | VIS | (also under Cumulative Upkeep) |
| Mob Mentality | VIS | attack-count pump aura |
| Ironclaw Curse | 5ED | -0/-1 + block restriction |
| Volrath's Curse | TMP | can't-attack/block + sac-to-ignore |

#### Misc spells / artifacts / creatures — BACKLOG (easy→medium)
| Card | Set(s) | Note |
|---|---|---|
| Three Wishes | VIS | impulse-draw exile |
| Song of Blood | VIS | mill + attacker pump |
| Liege of the Hollows | WTH | pay-any-mana token maker |
| Volrath's Shapeshifter | STH | copies top-of-graveyard (text-changing-ish) |
| Heartstone | STH | activated-ability cost reduction |
| Dracoplasm | TMP | sac-creatures ETB P/T |
| Flowstone Salamander | TMP | firebreathing to blocker |
| Echo Chamber | TMP | opponent-chosen copy token |
| Scroll Rack | TMP | hand↔library swap |
| Phyrexian Grimoire | TMP | opponent-choice graveyard draw |
| Booby Trap | TMP | named-card 10-damage trap |
| Shapeshifter | 5ED | choose-a-number P/T |
| Primordial Ooze | 5ED | growing must-attack |
| Mind Bomb | 5ED | discard-to-reduce damage |
| Personal Incarnation | 5ED | redirect-to-owner + lose-half-life |
| Seraph | 5ED | steal creatures it kills |
| Soul Sculptor | USG | creature→enchantment |
| Argothian Wurm | USG | ETB sac-land-or-topdeck |
| Enchantment Alteration | USG | move an Aura |
| Okk | USG | conditional attack/block |
| Defensive Formation | USG | (under Combat) |
| Library of Lat-Nam | 6ED | opponent-choice draw/tutor |
| Scrying Glass | UDS | hidden-info draw |
| Game Preserve | MRQ | symmetric reveal-to-battlefield |
| Venomous Breath | MRQ | destroy blockers/blocked |
| Wishmonger | MRQ | grant protection, any player |
| Crumbling Sanctuary | MRQ | damage→mill replacement |
| Thieves' Auction | MRQ | mass exile + draft (complex) |
| Divining Witch | NMS | name-a-card dig |
| Fog Patch | NMS | ambush block |
| Stronghold Gambit | NMS | reveal-lowest-CMC creature |
| Laccolith Rig | NMS | deal-power-on-block aura |
| Memory Crystal | EXO | buyback cost reduction |
| Kjeldoran Royal Guard | 5ED, 6ED | (under Combat) |
| Righteous Aura | VIS, MRQ | (under damage-shields) |

---

## Per-set quick table

Counts are distinct **excluded** names per set (a card missing from N sets counts
once per set here; totals across sets exceed 203 due to reprint overlap). "Stale"
counts rows that are actually implemented.

"Card blocks" = `[card]` entries in the set's missing file (before dedup). Stale
rows are counted within that number.

| Set | Card blocks | Stale | Dominant reason | Engine-blocked here |
|---|---|---|---|---|
| VIS (Visions) | 19 | 1 (Necromancy) | phasing, damage-shields, mana/land | 0 (phasing is supported) |
| 5ED (5th Edition) | 32 | 1 (Crown of the Ages) | **banding** (6), damage-shields, coin-flip | 6 banding + Helm/Battering Ram grant-banding = 8 |
| WTH (Weatherlight) | 8 | 0 | banding, coin-flip, control-steal | 2 (Benalish Infantry, Volunteer Reserves) |
| TMP (Tempest) | 25 | 0 | Licid cycle, phasing-adjacent, counters | 0 |
| STH (Stronghold) | 16 | 0 | Licid cycle, en-Kor redirect | 0 |
| EXO (Exodus) | 10 | 0 | Licid, Oaths, damage-shields | 0 |
| P02 (Portal 2) | 1 | 0 | Piracy (mana theft) | 0 |
| UGL (Unglued) | 58 (57 distinct; B.F.M. listed twice) | 0 | **silver-border un-cards** | all OUT-OF-SCOPE |
| USG (Urza's Saga) | 11 | 0 | mana/land, control-steal | 0 |
| ULG (Urza's Legacy) | 5 | 0 | static locks, combat | 0 |
| 6ED (6th Edition) | 12 | 0 | counters, damage-shields (reprints) | 0 |
| UDS (Urza's Destiny) | 2 | 0 | Scrying Glass, Storage Matrix | 0 |
| S99 (Starter 1999) | 1 | 0 | Piracy (reprint) | 0 |
| PTK (Portal 3K) | 1 | 0 | Liu Bei (horsemanship) | 0 |
| MRQ (Mercadian Masques) | 12 | 0 | damage-shields, control-steal | 0 |
| NMS (Nemesis) | 5 | 0 | mana, dig, ambush | 0 |

> Reprint overlap deduped in the "by exclusion reason" section: e.g. **Power Sink**
> (5ED/6ED/TMP/USG), **Desertion** (VIS/6ED), **Jade Monolith**, **Juxtapose**,
> **Reverse Damage**, **Pentagram of the Ages**, **Kjeldoran Royal Guard**,
> **Deflection** (all 5ED/6ED), **Righteous Aura** (VIS/MRQ), **Piracy** (P02/S99)
> each appear once above.

## Bottom line

- **203 genuinely-excluded** distinct cards; **2 stale** (Necromancy, Crown of the
  Ages — already implemented as `borderline`).
- The only true **ENGINE-BLOCKED** mechanic in this era is **banding** (~10 cards,
  concentrated in 5ED/WTH). Everything else Wagic already supports somewhere.
- **UGL (57 cards)** is wholly **OUT-OF-SCOPE** — silver-border physical/social/
  dice/meta joke cards.
- The largest *authorable* backlog clusters are the **Licid cycle** (12, one shared
  pattern), the **"next-time prevent/redirect damage" shields** (~20), and
  **control-exchange/steal** effects — all BACKLOG-MEDIUM.
- Phasing, cumulative upkeep, and (partial) coin-flip are supported, so the Visions
  phasing cards and the various coin-flip cards are backlog, **not** blocked.
</content>
</invoke>
