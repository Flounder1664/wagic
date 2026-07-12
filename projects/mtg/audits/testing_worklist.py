#!/usr/bin/env python3
"""
Card verification worklist (#1 of FR_card-verification-mode.md).

Reconstructs a PER-CARD testing worklist from source:
  registered cards (each set's _cards.dat)
    x grade + body   (Res/sets/primitives/*.txt)
    x trivial-detection (basic land / French-vanilla = "expected 100%")
    x current status (User/card_status.tsv, if present; else all UNTESTED)

Emits the remaining non-trivial, playable, UNTESTED cards ranked by risk, plus a
per-set coverage summary. This is the keystone the #3 badge and #6 spawn-next
consume. No engine build needed.

Usage:
    python testing_worklist.py [--res <path>] [--status <card_status.tsv>]
                               [--by set|risk] [--out-prefix testing_worklist]
Outputs (next to this script): <prefix>.tsv (all testable cards) and
<prefix>.md (per-set summary + top untested-by-risk checklist).
"""
import argparse, os, sys, glob, csv, re
from collections import defaultdict


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_testcases(tests_index, prim_names):
    """Set of primitive names that already have a Wagic TestSuite script.

    TestSuite scripts are named after the card under test (e.g.
    `agony_warp_i1085.txt`, `Angel_of_Vitality_2.txt`). Match each registered
    test filename to a card by longest-prefix against the primitive-name
    universe, both reduced to lowercase-alphanumeric so apostrophes/underscores/
    suffixes don't matter. Heuristic (filename-based) — good enough to flag
    already-covered cards. Returns (tested_names, num_registered_tests)."""
    by_norm = {}
    for n in prim_names:
        by_norm.setdefault(_norm(n), n)           # any winner on collision
    tested = set()
    if not tests_index or not os.path.isfile(tests_index):
        return tested, 0
    n_tests = 0
    with open(tests_index, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            e = line.strip()
            if not e or e.startswith("#") or e.startswith("+"):
                continue                          # comment / section directive
            n_tests += 1
            s = _norm(os.path.splitext(os.path.basename(e))[0])
            for L in range(len(s), 2, -1):        # longest match wins
                hit = by_norm.get(s[:L])
                if hit:
                    tested.add(hit)
                    break
    return tested, n_tests

# The fork's hand-authored, new-mechanic sets — the audit's identified risk
# (grade "supported" can still strip a mechanic). Edit as new fork sets land.
FORK_SETS = {"ECL", "EOE", "TLA", "TMT", "SOS", "FIN", "SPM"}

# grade precedence: a name present in a higher file "wins" (that's what loads).
GRADE_FILES = [  # (filename, grade)
    ("mtg.txt", "supported"),
    ("planeswalkers.txt", "supported"),
    ("borderline.txt", "borderline"),
    ("unsupported.txt", "unsupported"),
]


def parse_primitives(prim_dir):
    """name -> dict(grade, has_auto, has_abilities, has_text, has_target,
                    is_basic_land, missing)."""
    prims = {}
    for fname, grade in GRADE_FILES:
        path = os.path.join(prim_dir, fname)
        if not os.path.isfile(path):
            print(f"  (skip missing {fname})", file=sys.stderr)
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            cur = None
            for line in fh:
                s = line.strip()
                if s == "[card]":
                    cur = {"grade": grade, "has_auto": False, "has_abilities": False,
                           "has_text": False, "has_target": False,
                           "is_basic_land": False, "missing": ""}
                    cur["name"] = None
                elif s == "[/card]":
                    if cur and cur["name"]:
                        # keep only if not already seen at higher precedence
                        prev = prims.get(cur["name"])
                        if prev is None:
                            prims[cur["name"]] = cur
                        # (higher-precedence files are parsed first, so first wins)
                    cur = None
                elif cur is not None:
                    if s.startswith("name="):
                        cur["name"] = s[5:].strip()
                    elif s.startswith("auto="):
                        cur["has_auto"] = True
                    elif s.startswith("abilities="):
                        cur["has_abilities"] = True
                    elif s.startswith("text="):
                        cur["has_text"] = True
                    elif s.startswith("target="):
                        cur["has_target"] = True
                    elif s.startswith("type="):
                        if "Basic" in s and "Land" in s:
                            cur["is_basic_land"] = True
                    elif s.startswith("#MISSING"):
                        cur["missing"] = s.lstrip("#").strip()
    return prims


def parse_cards_dat(path):
    """yield (id, primitive_name, rarity) for each [card] block."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        cur = None
        for line in fh:
            s = line.strip()
            if s == "[card]":
                cur = {"id": "", "primitive": "", "rarity": ""}
            elif s == "[/card]":
                if cur and cur["primitive"]:
                    yield cur
                cur = None
            elif cur is not None and "=" in s:
                k, _, v = s.partition("=")
                k = k.strip()
                if k in ("id", "primitive", "rarity"):
                    cur[k] = v.strip()


def load_status(path):
    """primitive name -> status (latest row wins). Behaviour is per primitive,
    so verification status is keyed by name, not by printing. Tolerates absent
    file/columns."""
    status = {}
    if not path or not os.path.isfile(path):
        return status
    with open(path, encoding="utf-8", errors="replace", newline="") as fh:
        rd = csv.DictReader(fh, delimiter="\t")
        for row in rd:
            name = (row.get("name", "") or "").strip()
            st = (row.get("status", "") or "").strip().upper()
            if name and st:
                status[name] = st         # later rows overwrite → latest wins
    return status


def is_trivial(p):
    return p["is_basic_land"] or (
        not p["has_auto"] and not p["has_abilities"] and not p["has_text"])


def risk(fork_exclusive, p):
    score, reasons = 0, []
    if fork_exclusive:      # appears ONLY in fork sets → hand-authored-new (the risk)
        score += 3; reasons.append("fork-new")
    if p["grade"] == "unsupported":
        score += 3; reasons.append("unsupported")
    elif p["grade"] == "borderline":
        score += 2; reasons.append("borderline")
    if p["missing"]:
        score += 2; reasons.append("MISSING-note")
    if p["has_target"]:
        score += 1; reasons.append("targets")
    return score, ",".join(reasons)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", default=os.path.normpath(
        os.path.join(here, "..", "bin", "Res")), help="path to Res/")
    ap.add_argument("--status", default=os.path.normpath(
        os.path.join(here, "..", "bin", "Res", "..", "..", "..",
                     "User", "card_status.tsv")),
        help="card_status.tsv (optional)")
    ap.add_argument("--tests", default=os.path.normpath(
        os.path.join(here, "..", "bin", "Res", "test", "_tests.txt")),
        help="TestSuite index (_tests.txt) for the has_testcase column")
    ap.add_argument("--by", choices=["set", "risk"], default="risk")
    ap.add_argument("--out-prefix", default="testing_worklist")
    args = ap.parse_args()

    prim_dir = os.path.join(args.res, "sets", "primitives")
    print(f"reading primitives from {prim_dir} ...", file=sys.stderr)
    prims = parse_primitives(prim_dir)
    print(f"  {len(prims)} distinct primitives", file=sys.stderr)

    status = load_status(args.status)
    print(f"status rows: {len(status)} "
          f"({'found' if status else 'no card_status.tsv → all UNTESTED'})",
          file=sys.stderr)

    tested_names, n_tests = load_testcases(args.tests, prims.keys())
    print(f"testsuite: {n_tests} registered scripts → matched "
          f"{len(tested_names)} distinct cards", file=sys.stderr)

    # Aggregate registrations by DISTINCT primitive name (behaviour is per name).
    cards = {}                       # name -> aggregate dict
    per_set = defaultdict(lambda: defaultdict(int))
    for dat in sorted(glob.glob(os.path.join(args.res, "sets", "*", "_cards.dat"))):
        setcode = os.path.basename(os.path.dirname(dat))
        if setcode == "primitives":
            continue
        for c in parse_cards_dat(dat):
            name, cid = c["primitive"], c["id"]
            p = prims.get(name)
            per_set[setcode]["reg"] += 1
            if p is None:
                per_set[setcode]["unwritten"] += 1        # dangling, can't test
                continue
            if is_trivial(p):
                per_set[setcode]["trivial"] += 1          # expected 100%
                continue
            per_set[setcode]["testable_reg"] += 1
            per_set[setcode].setdefault("_names", set()).add(name)
            a = cards.get(name)
            if a is None:
                a = cards[name] = {"name": name, "grade": p["grade"],
                                   "missing": p["missing"], "prim": p,
                                   "printings": 0, "sets": set(),
                                   "ex_set": setcode, "ex_id": cid}
            a["printings"] += 1
            a["sets"].add(setcode)

    # finalise per-name rows
    rows = []
    for a in cards.values():
        fork_excl = bool(a["sets"] and a["sets"] <= FORK_SETS)
        score, reasons = risk(fork_excl, a["prim"])
        st = status.get(a["name"], "UNTESTED")
        rows.append({
            "name": a["name"], "grade": a["grade"], "status": st,
            "risk": score, "risk_reasons": reasons, "missing": a["missing"],
            "has_testcase": a["name"] in tested_names,
            "printings": a["printings"], "sets": len(a["sets"]),
            "example_set": a["ex_set"], "example_id": a["ex_id"],
        })

    # Within a risk tier, surface cards WITHOUT an automated test first
    # (has_testcase False sorts before True) — already-guarded cards deprioritised.
    if args.by == "set":
        rows.sort(key=lambda r: (r["example_set"], -r["risk"],
                                 r["has_testcase"], r["name"]))
    else:
        rows.sort(key=lambda r: (-r["risk"], r["has_testcase"], r["name"]))

    # ---- TSV: one row per distinct testable card (primitive name) ----
    tsv_path = os.path.join(here, args.out_prefix + ".tsv")
    cols = ["name", "grade", "status", "has_testcase", "risk", "risk_reasons",
            "missing", "printings", "sets", "example_set", "example_id"]
    with open(tsv_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    # per-set verified / scripted name counts
    for s, d in per_set.items():
        names = d.get("_names", set())
        d["names"] = len(names)
        d["ver_names"] = sum(1 for n in names if status.get(n) == "VERIFIED")
        d["scripted"] = sum(1 for n in names if n in tested_names)

    untested = [r for r in rows if r["status"] == "UNTESTED"]
    n_scripted = sum(1 for r in rows if r["has_testcase"])
    md_path = os.path.join(here, args.out_prefix + ".md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write("# Card verification worklist\n\n")
        fh.write(f"- distinct testable cards (written, non-trivial): "
                 f"**{len(rows)}**\n")
        fh.write(f"- still `UNTESTED`: **{len(untested)}**\n")
        fh.write(f"- already have a Wagic TestSuite script: **{n_scripted}** "
                 f"(~{100*n_scripted/len(rows):.0f}%) — automated regression; "
                 "still worth a human faithfulness pass.\n")
        fh.write("- trivial (basic land / French-vanilla) and unwritten "
                 "(dangling) cards are excluded from testing.\n")
        fh.write("- risk: fork-new (card exists only in the fork's hand-authored "
                 "sets) + grade + `#MISSING` note + targets. Within a tier, cards "
                 "with no TestSuite script come first.\n\n")
        fh.write("## Top 100 untested by risk\n\n")
        fh.write("| name | grade | risk | why | script? | note |\n"
                 "|---|---|---|---|---|---|\n")
        for r in untested[:100]:
            fh.write(f"| {r['name']} | {r['grade']} | {r['risk']} | "
                     f"{r['risk_reasons']} | {'✓' if r['has_testcase'] else '—'} "
                     f"| {r['missing']} |\n")
        fh.write("\n## Per-set coverage (registrations)\n\n")
        fh.write("| set | reg | trivial | unwritten | testable | "
                 "distinct-names | scripted | verified-names | %verified |\n")
        fh.write("|---" * 9 + "|\n")
        for s in sorted(per_set):
            d = per_set[s]
            nm = d.get("names", 0)
            vn = d.get("ver_names", 0)
            pct = f"{100*vn/nm:.0f}%" if nm else "-"
            fh.write(f"| {s} | {d.get('reg',0)} | {d.get('trivial',0)} | "
                     f"{d.get('unwritten',0)} | {d.get('testable_reg',0)} | "
                     f"{nm} | {d.get('scripted',0)} | {vn} | {pct} |\n")

    print(f"\nwrote {tsv_path}\nwrote {md_path}")
    print(f"distinct-testable={len(rows)}  untested={len(untested)}  "
          f"scripted={n_scripted}  sets={len(per_set)}")


if __name__ == "__main__":
    main()
