# Audit progress tracker

Cross-set missing/unsupported audit. Resumable — this file tracks what's done vs pending.
Method + definitions in [README.md](README.md). Master mechanical table:
[master_grade_table.tsv](master_grade_table.tsv) (all 343 sets, done).

Pre-staged data (in scratchpad, survives between runs unless temp is cleared):
`.../scratchpad/grade_index.json` (name→grade/notes), `.../scratchpad/scryfall_sets/*_clean.json`
(deduped true card lists for the 7 flagship sets).

## Flagship sets (registered-but-unwritten focus)

| Set | Status | True | Impl | Excluded | Doc |
|---|---|---|---|---|---|
| FIN | ✅ done | 313 | 137 | 176 | ../FIN_BACKLOG.md |
| EOE | ✅ done | 266 | 203 | 63 | ../EOE_TODO.md |
| SPM | ✅ done | 193 | 110 | 83 | ../SPM_BACKLOG.md |
| SOS | ⬜ pending | 271 | ~? | ~? | ../SOS_BACKLOG.md (update in place) |
| TLA | ⬜ pending | 286 | 53 | ~237 | new TLA_BACKLOG.md |
| ECL | ✅ done (corrected) | 278 | 278* | 0 | *playable but NOT faithful: ~26 cards strip new mechanic (vivid 0/14, behold 2/12, blight 19/24) — ../ECL_BACKLOG.md |
| TMT | ✅ done | 195 | 16 | 179 | only Sneak is a real engine wall (26); Alliance/Disappear refuted; 5 stray registrations — ../TMT_BACKLOG.md |
| TLA | ✅ done | 286 | 49 | 237 | 4 new keywords engine-blocked (Waterbend/Earthbend/Airbend/Exhaust); 4 dup registrations — ../TLA_BACKLOG.md |
| SOS | ✅ done | 271 | 49 | 209 | +8 written-but-not-wired (cheap wins); 22 doc-drift cards reconciled; 52 engine-blocked — ../SOS_BACKLOG.md |

(Impl/excluded for pending sets are from the mechanical master table; qualitative bucketing still needed.)

## Old-era batches (missing_cards_by_sets → grouped by exclusion reason)

| Batch | Era | Sets | Status | Distinct missing / excluded |
|---|---|---|---|---|
| OLD-01 | 1993-96 | LEA LEB 2ED ARN ATQ RV LEG DRK PHPR FEM 4ED ICE CHR HML ALL MIR | ✅ done | 245 / 243 (2 stale) |
| OLD-02 | 1997-2000 | VIS 5ED WTH TMP STH EXO P02 UGL USG ULG 6ED UDS S99 PTK MRQ NMS | ✅ done | 205 / 203 (2 stale; UGL 57 out-of-scope) |
| OLD-03 | 2000-03 | PCY BTD INV PLS 7ED APC ODY DM TOR JUD PRM ONS LGN SCG 8ED MRD | ✅ done | 194 / 194 |
| OLD-04 | 2004-07 | PAL04 DST 5DN CHK UNH BOK SOK 9ED PSAL RAV GPT DIS CSP TSB TSP PLC | ✅ done | 291 (UNH 123 out-of-scope; splice 34) |
| OLD-05 | 2007-09 | FUT 10E ME1 LRW MOR SHM EVE ME2 ALA CFX ARB M10 FVE HOP ME3 PDS | ✅ done | 160 / 160 (0 stale; clash-riders biggest) |
| OLD-06 | 2010-12 | WWK ROE M11 SOM TD0 PS11 ME4 MBS KVD NPH CMD M12 ISD DKA VVK AVR | ✅ done | 98 / 98 (0 stale; transform/infect confirmed supported) |
| OLD-07 | 2012-14 | PC2 M13 IVG RTR CM1 PI13 GTC DGM MMA M14 THS C13 BNG JOU CNS VMA | ✅ done | 112 / 110 (2 stale; Conspiracy voting/draft-matters the gaps) |
| OLD-08 | 2014-16 | M15 DDN KTK C14 JVC FRF DTK TPR MM2 ORI BFZ C15 PZ1 OGW SOI EMA | ✅ done | 112 / 109 (3 stale; Willbender-effect biggest blocker) |
| OLD-09 | 2016-17 | EMN CN2 MPS KLD C16 PZ2 PCA AER MM3 DDS AKH MP2 CMA E01 HOU C17 | ✅ done | 105 / 103 (2 stale; Conspiracy draft-matters/voting gaps) |
| OLD-10 | 2017-18 | H17 HTR DDT IMA UST A25 DDU DOM BBD CM2 SS1 M19 C18 GRN GK1 PUMA | ✅ done | 251 / 250 (1 stale; 191 UST out-of-scope, 59 real gaps) |
| OLD-11 | 2018-20 | UMA RNA GK2 WAR MH1 M20 C19 ELD MB1 THB UND C20 IKO M21 2XM AKR | ✅ done | see doc |
| OLD-12 | 2020-22 | ZNC PLIST KLR CMR KHM HA4 TSR C21 STA HA5 MH2 MIC MID Q06 VOC DBL | ✅ done | 74 / 71 (3 stale; voting dominant; era mechanics all supported) |
| OLD-13 | 2022-23 | NEC NEO NCC CLB 2X2 DMC BRC BRR J22 DMR ONC ONE SIR SIS MOC MOM | ✅ done | 141 / 139 (2 stale; 45 Planechase OOS; copy-ability biggest engine group) |
| OLD-14 | 2023+ | MUL MAT LTC LTR CMM | ✅ done | 51 / 49 (2 stale; voting dominant gap; Ring/amass/companion supported) |

## Sets with a real gap but NO missing_cards file (post-2020, need Scryfall diff)

These lack an upstream missing-cards list, so need the flagship-style Scryfall-vs-`_cards.dat`
method. From the earlier gap scan: ZNR, STX(2021), AFR, VOW, SNC, DMU, BRO, WOE/WOC/WOT, LCI/LCC,
MKM/MKC, MH3/M3C, DSK/DSC, BLB/BLC, TDM/TDC, DFT/DRC, FDN, RVR, OTJ/OTC/OTP/BIG, CLU, REX, SPG,
and various Alchemy/promo sets (many likely OUT-OF-SCOPE digital-only). Not yet started.

## Known interruption history
Session limit / PC-sleep killed background agents on 3 prior waves. Mitigation in place:
expensive data pre-staged to disk; agents write incrementally; batches kept to 3 concurrent.
Next session-limit reset: 12:50am Europe/London (as of 2026-07-07).
