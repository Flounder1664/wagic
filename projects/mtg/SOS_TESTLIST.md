# SOS in-game test list (deploy z_sos_fixes_20260626c.zip)

49 cards live. Priorities: **P1** = couldn't verify headless / approximations / new mechanics (test first); **P2** = modal modes & untested branches; **P3** = harness-passed (quick confidence). No images ship — cards render as text.

## P1 — highest value (headless-unverifiable / approximations)

### Infusion (M1) — these need you to GAIN LIFE this turn first, then play the card
- [ ] **Poisoner's Apprentice** — gain life, then play it: ETB should give an opponent creature -4/-4. (ETB-target couldn't be driven headless.)
- [ ] **Old-Growth Educator** — gain life, then play it: enters with **two +1/+1 counters** (4/4 → 6/6).
- [ ] **Ulna Alley Shopkeep** — is 2/3; after you gain life this turn it should be **4/3** (+2/+0).
- [ ] **Tenured Concocter** — 4/5; after you gain life it should be **6/5**; also: when an opponent targets it, you may draw.
- [ ] **Efflorescence** — put 2 counters on a creature; if you gained life, it also gets **trample + indestructible** that turn.
- [ ] **Tragedy Feaster** — 7/6 trample; at your end step, **sacrifice a permanent unless you gained life** this turn. (Ward—discard is omitted.)
- [ ] **Foolish Fate** / **Withering Curse** — harness-verified, but sanity-check the infused branch (lose 3 / destroy-all).

### Flashback (M5) — cast from hand, then later cast again from the graveyard
- [ ] **Group Project** — flashback cost is **tap three creatures** (not mana). Verify the recast works.
- [ ] **Pursue the Past** — gain 2; **may discard → draw 2**; then flashback {2}{R}{W}.
- [ ] **Dig Site Inventory** — +1/+1 counter + vigilance; flashback {W}.
- [ ] **Tome Blast / Duel Tactics** — verify the graveyard recast (Flashback) actually works.
- [ ] **Antiquities on the Loose** — makes 2 Spirits. NOTE: its "+1/+1 on each Spirit if cast from non-hand" rider is **not implemented** (approximation).

### Other headless-unverifiable
- [ ] **Zealous Lorecaster** — ETB: return an instant/sorcery from your graveyard to hand (ETB-target couldn't be driven headless).
- [ ] **Prismari Charm — mode "Surveil 2, then draw"** — approximated (surveil macro juxtaposed with draw). Confirm it surveils + draws and doesn't hiccup.

### Discard fixes from last round — please re-confirm
- [ ] **Stadium Tidalmage** — on enter AND on attack: may draw a card, and if you do, **discard** one.
- [ ] **Rapturous Moment** — draw 3, **discard 2**, add {U}{U}{R}{R}{R}.
- [ ] **Traumatic Critique** — X damage, draw 2, **discard 1**.

## P2 — modal cards, verify the untested modes
- [ ] **Quandrix Charm** — mode 0 **counter unless pay {2}**; mode 2 **base 5/5**.
- [ ] **Lorehold Charm** — mode 0 **each opponent sacrifices a nontoken artifact** (complex form); mode 1 reanimate ≤2; mode 2 team +1/+1 trample.
- [ ] **Witherbloom Charm** — mode 0 **sacrifice a permanent → draw 2**; mode 2 destroy nonland ≤2.
- [ ] **Artistic Process** — all 3 modes (6 dmg / 2 dmg each opposing creature / 3-3 Elemental w/ haste).
- [ ] **Glorious Decay** — mode 1 (4 dmg to a **flyer**), mode 2 (exile from a graveyard + draw).
- [ ] **Silverquill Charm** — mode 0 (2 counters), mode 1 (exile power ≤2).

## P3 — harness-passed (quick confidence only)
- [ ] Tome Blast (2 dmg any target) · Duel Tactics (1 dmg + can't block) · Group Project / Antiquities (token counts)
- [ ] Foolish Fate base (destroy, no -3) · Withering Curse base (-2/-2 all)
- [ ] Silverquill drain (mode 2) · Splatter draw-4 (mode 0) · Glorious destroy-artifact (mode 0) · Prismari bounce (mode 2)

---
*If any P1 card crashes or does nothing, note which — especially the surveil/ETB-target ones, since those are the patterns the headless harness can't cover.*
