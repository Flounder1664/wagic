#!/usr/bin/env python3
"""
Wagic Gap Analysis — Cards missing up to Secrets of Strixhaven (SOS, 2021-04-23).

Compares Scryfall's full card database against Wagic's three primitives files
(mtg.txt = supported, borderline.txt = approximation, unsupported.txt = impossible)
and produces a prioritised CSV of everything not yet playably implemented.

Usage:
    python gap_analysis.py

Output:
    wagic_gap_SOS.csv  — one row per missing/unsupported card, sorted Easy→Medium→Hard
"""

import csv
import json
import os
import re
import sys
from collections import defaultdict

# ── Paths ────────────────────────────────────────────────────────────────────

SCRYFALL_JSON = r"M:\Claude_projects\wagic\all-cards-20260430092244.json"
PRIMITIVES_DIR = r"M:\Claude_projects\wagic\projects\mtg\bin\Res\sets\primitives"
MTG_TXT       = os.path.join(PRIMITIVES_DIR, "mtg.txt")
BORDER_TXT    = os.path.join(PRIMITIVES_DIR, "borderline.txt")
UNSUP_TXT     = os.path.join(PRIMITIVES_DIR, "unsupported.txt")
OUTPUT_CSV    = r"M:\Claude_projects\wagic\wagic_gap_SOS_2026.csv"

CUTOFF_DATE   = "2026-04-24"   # SOS (Secrets of Strixhaven) release date

# ── Constants ────────────────────────────────────────────────────────────────

BASIC_LAND_NAMES = {"Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes",
                    "Snow-Covered Plains", "Snow-Covered Island", "Snow-Covered Swamp",
                    "Snow-Covered Mountain", "Snow-Covered Forest"}

EXCLUDE_LAYOUTS = {
    "token", "emblem", "art_series", "double_faced_token",
}

# Layouts that are Hard regardless of oracle text
HARD_LAYOUTS = {
    "transform", "modal_dfc", "flip", "split", "adventure",
    "reversible_card", "meld",
}

# Oracle text patterns (lowercase) → Hard
HARD_PATTERNS = [
    r"copy of",
    r"copies of",
    r"become a copy",
    r"\bmorph\b",
    r"\bmegamorph\b",
    r"\bmutate\b",
    r"\boffering\b",
    r"\bhaunt\b",
    r"\bbanding\b",
    r"\bninjutsu\b",
    r"\bsuspend\b",
    r"\bchampion\b",
    r"\bprowl\b",
    r"\bevoke\b",
    r"\blevel up\b",
    r"\bunderground\b.*\bunderworld\b",  # too niche
    r"\bgraft\b",
    r"\bdredge\b",
    r"\bruneclaw\b",
    r"imprint",
    r"\bsplice\b",
    r"\bforecast\b",
    r"\bheroic\b",
    r"\bbuyback\b",
    r"\bkicker\b",         # variable kicker approximations are hard
    r"\bstrive\b",
    r"\bconspire\b",
    r"\boverload\b",
    r"\bfusion\b",
    r"\bbloodthirst\b",    # conditional P/T on ETB — medium-ish but complex
]
HARD_RE = re.compile("|".join(HARD_PATTERNS), re.IGNORECASE)

# Oracle text patterns (lowercase) → Medium
MEDIUM_PATTERNS = [
    r"choose one",
    r"choose two",
    r"choose an opponent",
    r"choose a ",
    r"\bwould\b.*\binstead\b",
    r"\binstead\b.*\bwould\b",
    r"protection from",
    r"enchant (?!creature)",      # non-creature aura
    r"whenever .{0,60} if ",      # conditional trigger
    r"\bfor each\b",
    r"\bflashback\b",
    r"\bescape\b",
    r"\bforetell\b",
    r"\bdisturb\b",
    r"\bcycling\b",
    r"\btransmute\b",
    r"\bchroma\b",
    r"\blandfall\b",              # some landfall is easy, but leave as medium for safety
    r"\bfading\b",
    r"\bvanishing\b",
    r"\bfear\b",
    r"\bprowess\b",
    r"\bripple\b",
    r"\bstorm\b",
    r"\bcascade\b",
    r"\bwild\b",
    r"\binfect\b",
    r"\bwither\b",
    r"\battach\b",
    r"\bcounters? on\b",          # complex counter manipulation
    r"\bproliferate\b",
    r"return .{0,40} to (?:its|the) owner",   # conditional bounce
    r"whenever you cast .{0,40} second",       # spell-count triggers
    r"if an opponent controls",
    r"at the beginning of each .{0,20}'s",    # each-player triggers
    r"\bdouble\b.*\bpower\b",
    r"\bdouble\b.*\btoughness\b",
    r"becomes? the target",
]
MEDIUM_RE = re.compile("|".join(MEDIUM_PATTERNS), re.IGNORECASE)

EFFORT_ORDER = {"Easy": 0, "Medium": 1, "Hard": 2}


# ── Helper functions ─────────────────────────────────────────────────────────

def parse_primitive_names(filepath):
    """Extract all name= values from a Wagic [card]...[/card] file."""
    names = set()
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.match(r"^name=(.+)", line)
                if m:
                    names.add(m.group(1).strip())
    except FileNotFoundError:
        print(f"WARNING: {filepath} not found", file=sys.stderr)
    return names


def classify_effort(card):
    """Return (effort, reason) for a card dict."""
    oracle  = (card.get("oracle_text") or "").lower()
    layout  = (card.get("layout") or "").lower()
    type_ln = (card.get("type_line") or "").lower()

    # ── Hard ──────────────────────────────────────────────────────────────────
    if "planeswalker" in type_ln:
        return "Hard", "planeswalker"
    if layout in HARD_LAYOUTS:
        return "Hard", f"layout:{layout}"
    if "saga" in type_ln:
        return "Hard", "saga chapter triggers"
    if oracle:
        m = HARD_RE.search(oracle)
        if m:
            return "Hard", f"oracle:{m.group(0)[:30]}"

    # ── Medium ────────────────────────────────────────────────────────────────
    if oracle:
        m = MEDIUM_RE.search(oracle)
        if m:
            return "Medium", f"oracle:{m.group(0)[:30]}"
        word_count = len(oracle.split())
        if word_count > 80:
            return "Medium", f"complex text ({word_count} words)"

    return "Easy", ""


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    # 1. Parse primitive files
    print("Loading primitives...", flush=True)
    supported   = parse_primitive_names(MTG_TXT)
    borderline  = parse_primitive_names(BORDER_TXT)
    unsupported = parse_primitive_names(UNSUP_TXT)

    supported_lower   = {n.lower(): n for n in supported}
    borderline_lower  = {n.lower(): n for n in borderline}
    unsupported_lower = {n.lower(): n for n in unsupported}

    print(f"  mtg.txt:        {len(supported):,} cards")
    print(f"  borderline.txt: {len(borderline):,} cards")
    print(f"  unsupported.txt:{len(unsupported):,} cards")

    # 2. Load and deduplicate Scryfall JSON
    print(f"\nLoading Scryfall JSON ({SCRYFALL_JSON})...", flush=True)
    print("  (this may take a moment for 529K entries)", flush=True)

    # We keep the earliest-released printing per oracle_id
    # dict: oracle_id → card_dict
    canonical = {}

    with open(SCRYFALL_JSON, "r", encoding="utf-8") as f:
        all_cards = json.load(f)

    print(f"  Loaded {len(all_cards):,} raw entries", flush=True)

    skipped_lang    = 0
    skipped_layout  = 0
    skipped_date    = 0
    skipped_basic   = 0

    for card in all_cards:
        # English only
        if card.get("lang") != "en":
            skipped_lang += 1
            continue

        # Exclude unwanted layouts
        layout = (card.get("layout") or "").lower()
        if layout in EXCLUDE_LAYOUTS:
            skipped_layout += 1
            continue

        # Date filter — must have at least one printing by cutoff
        released = card.get("released_at", "9999-99-99")
        if released > CUTOFF_DATE:
            skipped_date += 1
            continue

        name = card.get("name", "")

        # Exclude basic lands
        if name in BASIC_LAND_NAMES and "Basic" in (card.get("type_line") or ""):
            skipped_basic += 1
            continue

        oracle_id = card.get("oracle_id") or name  # fallback to name if no oracle_id

        if oracle_id not in canonical or released < canonical[oracle_id]["released_at"]:
            canonical[oracle_id] = {
                "name":         name,
                "oracle_id":    oracle_id,
                "layout":       card.get("layout", ""),
                "type_line":    card.get("type_line", ""),
                "mana_cost":    card.get("mana_cost", ""),
                "cmc":          card.get("cmc", ""),
                "rarity":       card.get("rarity", ""),
                "set":          card.get("set", ""),
                "released_at":  released,
                "oracle_text":  card.get("oracle_text", ""),
                "keywords":     ", ".join(card.get("keywords") or []),
            }

    print(f"  Skipped: {skipped_lang:,} non-English, {skipped_layout:,} excluded layouts, "
          f"{skipped_date:,} post-cutoff, {skipped_basic:,} basic lands")
    print(f"  Unique oracle_id cards up to {CUTOFF_DATE}: {len(canonical):,}", flush=True)

    # Second dedup pass: some cards (e.g. Un-set variants) have different oracle_ids
    # but the same name — Wagic matches by name, so keep only one per name.
    by_name = {}
    for card in canonical.values():
        name = card["name"]
        if name not in by_name or card["released_at"] < by_name[name]["released_at"]:
            by_name[name] = card
    canonical = by_name
    print(f"  Unique named cards up to {CUTOFF_DATE}:    {len(canonical):,}", flush=True)

    # 3. Classify each card
    print("\nClassifying gaps...", flush=True)

    rows = []
    counts = {
        "supported":  0,
        "borderline": 0,
        "unsupported": 0,
        "missing_easy":   0,
        "missing_medium": 0,
        "missing_hard":   0,
    }

    for card in canonical.values():
        name_lower = card["name"].lower()

        if name_lower in supported_lower:
            counts["supported"] += 1
            continue
        if name_lower in borderline_lower:
            counts["borderline"] += 1
            continue

        if name_lower in unsupported_lower:
            # Already flagged as impossible — include as Hard
            effort, reason = "Hard", "in unsupported.txt"
            status = "unsupported"
            counts["unsupported"] += 1
        else:
            effort, reason = classify_effort(card)
            status = "missing"
            counts[f"missing_{effort.lower()}"] += 1

        rows.append({
            "name":          card["name"],
            "status":        status,
            "effort":        effort,
            "type_line":     card["type_line"],
            "mana_cost":     card["mana_cost"],
            "cmc":           card["cmc"],
            "rarity":        card["rarity"],
            "first_set":     card["set"],
            "first_released":card["released_at"],
            "keywords":      card["keywords"],
            "oracle_text":   card["oracle_text"],
            "effort_reason": reason,
        })

    # 4. Sort: Easy → Medium → Hard, then type_line, then name
    rows.sort(key=lambda r: (EFFORT_ORDER[r["effort"]], r["type_line"], r["name"]))

    # 5. Write CSV
    fieldnames = ["name", "status", "effort", "type_line", "mana_cost", "cmc",
                  "rarity", "first_set", "first_released", "keywords",
                  "oracle_text", "effort_reason"]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # 6. Summary
    total = len(canonical)
    missing_total = counts["missing_easy"] + counts["missing_medium"] + counts["missing_hard"]
    gap_total = missing_total + counts["unsupported"]

    print(f"\n{'='*55}")
    print(f"Wagic Gap Analysis — up to SOS ({CUTOFF_DATE})")
    print(f"{'='*55}")
    print(f"Total unique cards in scope:   {total:>7,}")
    print(f"  Supported (mtg.txt):         {counts['supported']:>7,}")
    print(f"  Borderline (approximation):  {counts['borderline']:>7,}")
    print(f"  Unsupported (blocked):       {counts['unsupported']:>7,}")
    print(f"  Missing (not in any file):   {missing_total:>7,}")
    print(f"    -> Easy:                   {counts['missing_easy']:>7,}")
    print(f"    -> Medium:                 {counts['missing_medium']:>7,}")
    print(f"    -> Hard:                   {counts['missing_hard']:>7,}")
    print(f"{'-'*55}")
    print(f"Total gap (missing+unsup):     {gap_total:>7,}")
    print(f"\nCSV written to: {OUTPUT_CSV}")
    print(f"Rows in CSV: {len(rows):,}")


if __name__ == "__main__":
    main()
