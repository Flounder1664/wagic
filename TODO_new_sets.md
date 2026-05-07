# Wagic — Remaining Cards TODO

Cards from the 8 new/recent sets not yet implemented.
Difficulty: Easy = direct Wagic primitives; Medium = approximation needed; Hard = requires engine work or DFC.

---

## FIN — Magic: The Gathering — Final Fantasy

### Easy
| Card | ID | Notes |
|------|----|-------|
| ~~Sephiroth's Intervention~~ | 1140917 | ✅ Done |
| ~~Coeurl~~ | 1140941 | ✅ Done |
| ~~Dwarven Castle Guard~~ | 1140957 | ✅ Done |
| ~~Scorpion Sentinel~~ | 1141071 | ✅ Done |
| ~~Fight On!~~ | 1141129 | ✅ Done |
| ~~Hecteyes~~ | 1141135 | ✅ Done |
| ~~Overkill~~ | 1141149 | ✅ Done |
| ~~Blitzball Shot~~ | 1141291 | ✅ Done |
| ~~Gigantoad~~ | 1141315 | ✅ Done |
| ~~Goobbue Gardener~~ | 1141317 | ✅ Done |
| ~~Iron Giant~~ | 1141487 | ✅ Done |

### Medium
| Card | ID | Notes |
|------|----|-------|
| ~~Sephiroth, Planet's Heir~~ | 1142125 | ✅ Done |

### Hard
| Card | ID | Blocker |
|------|-----|---------|
| Cloud, Midgar Mercenary // Cloud, Planet's Champion | — | ETB tutor Equipment is fine; "triggered abilities trigger an additional time while equipped" has no Wagic equivalent. |
| Sephiroth, Fabled SOLDIER // Sephiroth, One-Winged Angel | — | DFC + emblem on transform; emblem support not in engine. |

---

## TLA — Avatar: The Last Airbender

### Easy
| Card | ID | Notes |
|------|----|-------|
| ~~Avatar Enthusiasts~~ | 1510011 | ✅ Done |
| ~~Fancy Footwork~~ | 1510019 | ✅ Done (single-target approx) |
| ~~Jeong Jeong's Deserters~~ | 1510025 | ✅ Done |
| ~~Kyoshi Warriors~~ | 1510026 | ✅ Done |
| ~~Water Tribe Captain~~ | 1510041 | ✅ Done |
| ~~It'll Quench Ya!~~ | 1510058 | ✅ Done |
| ~~Epic Downfall~~ | 1510096 | ✅ Done |
| ~~Merchant of Many Hats~~ | 1510110 | ✅ Done |
| ~~Ozai's Cruelty~~ | 1510113 | ✅ Done |
| ~~Boar-q-pine~~ | 1510124 | ✅ Done |
| ~~Pillar Launch~~ | 1510189 | ✅ Done |
| ~~Turtle-Duck~~ | 1510200 | ✅ Done |
| ~~Abandon Attachments~~ | 1510205 | ✅ Done |
| ~~Pretending Poxbearers~~ | 1510237 | ✅ Done |

### Hard
| Card | ID | Blocker |
|------|-----|---------|
| Fire Lord Azula | — | "Copy that spell" while attacking — no spell-copy primitive in Wagic. |
| Appa, Loyal Sky Bison | — | Airbend mechanic (exile permanent → owner may recast for {2}) — exile-and-recast not supported. |
| Appa, Steadfast Guardian | — | Same airbend blocker; also triggers on casting from exile. |
| Avatar Aang // Aang, Master of Elements | — | DFC; front requires tracking four different bend-types in one turn. |

---

## SPM — Marvel's Spider-Man

### Easy
| Card | ID | Notes |
|------|----|-------|
| ~~Sudden Strike~~ | 1500019 | ✅ Done |
| ~~Oscorp Research Team~~ | 1500040 | ✅ Done |
| ~~Scorpion's Sting~~ | 1500065 | ✅ Done |
| ~~Romantic Rendezvous~~ | 1500086 | ✅ Done |
| ~~Taxi Driver~~ | 1500097 | ✅ Done |
| ~~Supportive Parents~~ | 1500119 | ✅ Done |
| ~~Gallant Citizen~~ | 1500129 | ✅ Done |

### Hard
| Card | ID | Blocker |
|------|-----|---------|
| Spider-Sense | — | "Counter target triggered ability" — Wagic cannot put triggered abilities on the stack as fizzle targets. |
| Peter Parker's Camera | — | Film counters + "copy target activated or triggered ability" — copy-ability mechanic absent. |
| Mister Negative | — | "Exchange life totals" — no swap primitive; draw-cards-equal-to-life-lost also complex. |

---

## TMT — Teenage Mutant Ninja Turtles

### Easy
| Card | ID | Notes |
|------|----|-------|
| ~~Make Your Move~~ | 1520020 | ✅ Done |
| ~~Donatello, Turtle Techie~~ | 1520037 | ✅ Done |
| ~~Death in the Family~~ | 1520061 | ✅ Done |
| ~~Squirrelanoids~~ | 1520081 | ✅ Done |
| ~~Tunnel Rats~~ | 1520084 | ✅ Done |
| ~~Rock Soldiers~~ | 1520107 | ✅ Done |
| ~~Mouser Mark III~~ | 1520159 | ✅ Done |

### Medium
| Card | ID | Notes |
|------|-----|-------|
| ~~Oroku Saki, Shredder Rising~~ | 1520068 | ✅ Done (Sneak not implemented; combat damage draw+life) |
| ~~Technodrome~~ | 1520179 | ✅ Done (reach/trample/activated ability; cantattack/cantblock < power 6 approx) |

---

## DFT — Aetherdrift (new cards portion)
*(Not on Scryfall; card text unknown)*

### Hard (from original scoring)
| Card | ID | Blocker |
|------|-----|---------|
| The Great Aether Race | 904560 | Unknown text; scored Hard |
| Daretti, Scrap Metal King | 904480 | Unknown text; scored Hard (Planeswalker) |

---

## INR — Innistrad: Remastered
*(Set already complete; IDs corrected. No outstanding scored cards.)*

## ECL — Lorwyn Eclipsed
*(Set complete at 274 cards. Retched Wretch is vanilla — no text needed.)*

---

---

## Core Set Borderline / Unsupported Audit

**Scale:** `borderline.txt` = 11,878 cards; `unsupported.txt` = 1,710 cards.
Based on a sample analysis of both files.

---

### Unsupported (1,710 cards) — by reason

| Group | Count | Reason | Fix complexity |
|-------|-------|--------|----------------|
| **U1** | ~1,596 (93%) | **No primitive at all** — complex/unique mechanics with no existing model. Includes named-card interactions, artist-name mechanics, meta effects. | Hard — requires new engine primitives per mechanic. Low priority unless a specific popular card is requested. |
| **U2** | ~45 (3%) | **Scheme cards** (Archenemy format) — trigger on "set scheme in motion" event, no equivalent in standard Magic. | Hard — entire Scheme subsystem would need building. |
| **U3** | ~53 (3%) | **Partial implementations** — have some `auto=` but still unplayable. Sub-issues: goad mechanic, damage redirection (Beacon of Destiny style), Backup counters, Ward/Protect partial. | Medium — these *can* use existing primitives; just need finishing. Best candidates for quick wins. |
| **U4** | ~6 (0.4%) | **DFC / Split cards** — transform or flip mechanics. | Hard — engine DFC limitation (same as our new sets). |
| **U5** | ~12 (0.7%) | **Planeswalker-modifying cards** — enchantments/effects that modify loyalty abilities or count activations. | Hard — no loyalty-ability hook in the primitive system. |
| **U6** | ~1 | **Conspiracy format** (hidden agenda mechanic). | Hard — format-specific, very low priority. |

**Priority action:** Focus on U3 (~53 cards) — these are closest to working.

---

### Borderline (11,878 cards) — by reason

| Group | Count | Reason | Fix complexity |
|-------|-------|--------|----------------|
| **B1** | ~7,993 (67%) | **Well-implemented** — the implementation is actually correct or close enough. These cards are in `borderline.txt` as an organisational convention, not because they're broken. | Easy — audit and move the working ones to `mtg.txt`. Large batch job but straightforward. |
| **B2** | ~1,936 (16%) | **Partial auto= vs complex text** — core effect automated, but edge cases, additional clauses, or conditional branches are missing. E.g. text says "whenever X, if Y, also do Z" but auto= only handles "whenever X". | Medium — each card needs individual review. Some fixable with `if condition then effect`, some need new primitives. |
| **B3** | ~641 (5%) | **No auto= at all** — card has been placed in borderline but never implemented. Many are standard mechanics that *could* be primitived (e.g. "gets +N/+N where N equals number of creatures you control"). | Medium — these are probably the best batch fix target. Existing primitives cover most of the patterns. |
| **B4** | ~618 (5%) | **Complex choice mechanics simplified** — multi-branch choose-one/choose-X effects where the auto= only handles one branch or uses a generic choice macro. | Medium — known pattern (separate `auto=choice name(A)` lines). Most fixable with the correct choice syntax. |
| **B5** | ~451 (4%) | **Simplified triggered effects** — chained triggers, conditional triggers, or "you may also" clauses that fire together but are implemented as a single simpler trigger. | Medium–Hard — depends on the trigger. Some fixable with `&&` or separate trigger lines; others need new primitives. |
| **B6** | ~214 (2%) | **Search / library mechanics** — using approximate search patterns that don't match all filter criteria. | Medium — known patterns exist (`Reveal:type:*:mylibrary...`); each needs case-by-case rewrite. |

**Priority actions (assuming borderline enabled in options — promotion to supported is low priority):**
1. **B3** — borderline cards with no `auto=` are completely non-functional. Generate a list; implement in batches by mechanic type. These are broken, not just approximate.
2. **B4** — choices where only one branch fires behave wrongly in-game. Scan for "Choose one" in text where auto= has only one option; fix with separate `auto=choice` lines.
3. **B5** — simplified triggers that fire incorrectly (not just incompletely). Worth fixing if the wrong behaviour causes AI or gameplay issues.
4. **B2** — partial implementations with missing clauses. Lower priority — card plays, just missing edge-case behaviour.
5. **B1** (promotion) — skip for now; cards already visible and functional.

---

## Borderline / Unsupported Review (New Sets)

Review each implemented card set for quality issues. Cards already tagged `grade=borderline` are listed here with fix assessment. Unimplemented Hard cards are grouped by the engine blocker.

---

### Group 1 — Likely fixable (Easy/Medium)

These borderline cards probably have a correct Wagic pattern available.

| Card | Set | Issue | Fix approach | Complexity |
|------|-----|-------|--------------|------------|
| Behold the Sinister Six! | SPM | Text says "approx 3 targets" but code already uses `<upto:6>`. Missing constraint is "different names" — engine can't filter by that. | Remove borderline grade; update text to say "different names not enforced" | Easy |
| Evil Reawakened | FIN | `counter(1/1,2) moveto(mybattlefield)` — counters applied in graveyard then moved. Pattern confirmed working (from session notes). | Test in game; if it works correctly, upgrade to supported | Easy |
| Spider-Punk | SPM | Riot = choose haste OR +1/+1 counter on ETB. Currently gives both. | Use `auto=choice name(Counter) counter(1/1) all(this)` + `auto=choice name(Haste) haste all(this) ueot` separate lines | Medium |
| Mob Lookout | SPM | Connive = draw, discard, then if nonland discarded get +1/+1 counter. Current impl `draw:1 && {D}:life:0` looks broken. | Rewrite as `draw:1 controller && discard:1 controller`; counter-on-nonland-discard remains unapproximatable | Medium |
| Swarm, Being of Bees | SPM | Mayhem: missing "only if opponent lost life this turn" restriction on graveyard cast. | Add `restriction{compare(oplifelost)~morethan~0}` to `autograveyard` line | Medium |
| Spider-Islanders | SPM | Same Mayhem restriction missing. | Same fix as Swarm | Medium |
| Technodrome | TMT | cantattack/cantblock applied at `@each my combatbegins` if power < 6. Needs in-game test to confirm it actually prevents attacks. | Test in game; if it works, upgrade to supported | Medium |

---

### Group 2 — Engine-limited (best approximation, keep borderline)

These cannot be improved without engine changes. Current implementation is the best possible.

| Card | Set | Issue | Why it can't be fixed |
|------|-----|-------|-----------------------|
| Fancy Footwork | TLA | "Up to 2 targets each get +2/+2 and untap" → double-prompt (player selects targets twice). | No single-pass way to apply N effects to same `<upto:2>` selection. |
| Oroku Saki, Shredder Rising | TMT | Sneak = alternative cast by returning unblocked attacker during declare-blockers step. | No primitive for intercepting declare-blockers step to change a card's cast zone. |
| Encumbered Reejerey | ECL | Triggered remove-counter when tapped → approximated as activated `{T}:counter(-1/-1,-1)`. | `@tapped(this)` trigger would be more accurate but activating for free vs triggered is a meaningful difference. Investigate if `@tapped(this) restriction{...}` works. |
| Spider-Man, Web-Slinger | SPM | Web-slinging real text unknown — needs verification. Current impl is "attack trigger → Spider token". | Verify actual card text; may be correct or may need upgrade/downgrade. |

---

### Group 3 — Unimplemented Hard cards (engine blockers)

Grouped by the underlying engine limitation.

#### 3a. Double-Faced Cards (DFC / transform)
Engine has no flip/transform support for primitives.

| Card | Set |
|------|-----|
| Cloud, Midgar Mercenary // Cloud, Planet's Champion | FIN |
| Sephiroth, Fabled SOLDIER // Sephiroth, One-Winged Angel | FIN |
| Avatar Aang // Aang, Master of Elements | TLA |

**Fix complexity:** Hard. Would require engine-level DFC support. Single-faced approximation possible for the front face only but loses the transform entirely.

#### 3b. Copy spells / abilities
No `copy(spell)` or `copy(ability)` primitive exists.

| Card | Set | Detail |
|------|-----|--------|
| Fire Lord Azula | TLA | Copy target instant or sorcery you control while attacking |
| Peter Parker's Camera | SPM | Copy target activated or triggered ability |

**Fix complexity:** Hard. No copy-spell or copy-ability primitives in engine.

#### 3c. Stack interaction — counter a triggered ability
Triggered abilities don't go on the stack as targetable objects in Wagic.

| Card | Set | Detail |
|------|-----|--------|
| Spider-Sense | SPM | Counter target triggered ability |

**Fix complexity:** Hard. Engine limitation.

#### 3d. Exile-and-recast mechanic (Airbend)
No primitive for "exile a permanent; owner may recast it for {2}".

| Card | Set | Detail |
|------|-----|--------|
| Appa, Loyal Sky Bison | TLA | Airbend: exile, owner may recast for {2} |
| Appa, Steadfast Guardian | TLA | Same airbend + triggers on cast from exile |

**Fix complexity:** Hard. `moveto(exile)` + `canplayfromexile` exists but the "recast for alternate cost {2}" part does not.

#### 3e. Exchange life totals
No swap/exchange primitive.

| Card | Set | Detail |
|------|-----|--------|
| Mister Negative | SPM | Exchange life totals with target player |

**Fix complexity:** Hard. Could approximate with `damage:lifetotal opponent && life:opponentlifetotal controller` but would give wrong result (cumulative not swap).

#### 3f. Trigger-extra-time mechanic
No "triggered abilities trigger an additional time" primitive.

| Card | Set | Detail |
|------|-----|--------|
| Cloud, Midgar Mercenary (front face) | FIN | While equipped, triggered abilities trigger an additional time |

**Fix complexity:** Hard. Engine limitation; no doubling-season equivalent for triggers.

#### 3g. Unknown card text (DFT)
| Card | ID | Notes |
|------|-----|-------|
| The Great Aether Race | 904560 | Not on Scryfall; text unknown |
| Daretti, Scrap Metal King | 904480 | Not on Scryfall; Planeswalker; text unknown |

---

## Quick wins done
~~1. Sephiroth's Intervention~~ ✅
~~2. Sephiroth, Planet's Heir~~ ✅
~~3–40. 38 Easy cards (FIN ×10, TLA ×14, SPM ×7, TMT ×7)~~ ✅
~~41–59. Batch 2 (FIN ×12, SPM ×9) + Batch 3 (FIN ×10, SPM ×9)~~ ✅
