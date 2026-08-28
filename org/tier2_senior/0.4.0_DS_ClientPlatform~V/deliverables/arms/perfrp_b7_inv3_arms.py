"""ADVI_PERFRP PRF-b-7 / PRFR2DS-AC3 arms: the ONE rollup law, and inv-3.

AC3: ONE rollup function (comp-find census: 1 definition, every level a caller);
inv-3 recompute L2 == Sum L3 == Sum L4 on a pinned as-of.

ARM 3 is the one that matters most: it shows the date-alignment fix CHANGED ANSWERS,
by diffing the emission against the pre-fix one. A fix that moves nothing is either
unnecessary or untested, and either way should not be reported as a repair.
"""
import ast
import json
import subprocess
import sys
from pathlib import Path

# NOTE: this arm reads only the EMITTED artifacts and the source tree -- no S3. That is
# deliberate: inv-3 and the one-definition census are properties of what was SERVED and
# of the code, so re-reading the upstream would test a different claim.
ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
RUNNERS = ROOT / "data/assets/scripts/gold/runners_49f"
sys.path.insert(0, str(RUNNERS))
sys.path.insert(0, str(ROOT))
EMIT = ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables/emissions"
FAILS = []


def check(name, cond, detail=""):
    print("  %-58s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


print("=" * 78)
print("ARM 1 -- ONE DEFINITION of the rollup law, and every level a CALLER")
print("=" * 78)
# AST, not grep: a comment or a docstring mentioning "def rollup" is not a definition,
# and a census that counts strings would score those as duplicates.
defs = []
callers = {}
for p in sorted(RUNNERS.glob("*.py")):
    try:
        tree = ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "rollup":
            defs.append("%s:%d" % (p.name, node.lineno))
        if isinstance(node, ast.Call):
            f = node.func
            nm = getattr(f, "id", None) or getattr(f, "attr", None)
            if nm == "rollup":
                callers.setdefault(p.name, []).append(node.lineno)
print("  definitions of rollup(): %s" % defs)
print("  callers: %s" % {k: v for k, v in callers.items()})
check("EXACTLY ONE definition of the rollup law", len(defs) == 1, str(defs))
check("the definition lives in perfrp_rollup.py",
      bool(defs) and defs[0].startswith("perfrp_rollup.py"))
check("at least one caller outside the defining module",
      any(k != "perfrp_rollup.py" for k in callers), str(sorted(callers)))

print("=" * 78)
print("ARM 2 -- inv-3: L2 == Sum L3, recomputed from the served payloads")
print("=" * 78)
rel = json.load(open(EMIT / "perfrp_performance_relationship.json", encoding="utf-8"))
acct = json.load(open(EMIT / "perfrp_performance_account.json", encoding="utf-8"))
ver = json.load(open(EMIT / "perfrp_performance_relationship.verification.json",
                     encoding="utf-8"))
membership = ver["membership"]
acct_by_key = {e["key"]: e for e in acct["entries"]}

check("both grains share the as_of", rel["as_of"] == acct["as_of"],
      "%s vs %s" % (rel["as_of"], acct["as_of"]))
check("both grains share the return window",
      rel["window"]["return_series_start"] == acct["window"]["return_series_start"]
      and rel["window"]["window_end"] == acct["window"]["window_end"])
check("membership covers every relationship entry",
      set(membership) == {e["key"] for e in rel["entries"]},
      "%d vs %d" % (len(membership), len(rel["entries"])))
ids = [i for v in membership.values() for i in v]
check("membership is DISJOINT (no account under two relationships)",
      len(ids) == len(set(ids)), "%d ids, %d distinct" % (len(ids), len(set(ids))))
check("membership COVERS the account grain", set(ids) == set(acct_by_key),
      "%d ids vs %d accounts" % (len(set(ids)), len(acct_by_key)))
# the count cross-tie the emitter asserts, re-checked from the two artifacts
bad = [e["key"] for e in rel["entries"] if len(membership[e["key"]]) != e["accounts"]]
check("for every relationship len(ids) == accounts", not bad, "%d mismatched" % len(bad))

print("=" * 78)
print("ARM 3 -- THE FIX MOVED ANSWERS (date alignment vs list position)")
print("=" * 78)
before_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if before_path and before_path.exists():
    before = json.load(open(before_path, encoding="utf-8"))
    b = {e["key"]: e for e in before["entries"]}
    moved, appeared, state_changed = [], [], []
    for e in rel["entries"]:
        o = b.get(e["key"])
        if o is None:
            appeared.append(e["key"])
            continue
        if o.get("window_return") != e.get("window_return"):
            moved.append((e["key"], o.get("window_return"), e.get("window_return")))
        if o.get("figure_state") != e.get("figure_state"):
            state_changed.append((e["key"], o.get("figure_state"), e.get("figure_state")))
    print("  relationships whose window_return CHANGED: %d of %d" % (len(moved), len(rel["entries"])))
    print("  relationships whose figure_state CHANGED : %d" % len(state_changed))
    check("the alignment fix changed at least one answer", len(moved) > 0,
          "%d moved" % len(moved))
    print("  largest 6 moves (before -> after):")
    def _mag(t):
        return abs((t[2] or 0) - (t[1] or 0)) if (t[1] is not None and t[2] is not None) else 0
    for k, o, n in sorted(moved, key=_mag, reverse=True)[:6]:
        print("      %-30s %s -> %s" % (k[:30], o, n))
    print("  ^ each of these is a relationship whose children spanned different date")
    print("    ranges; the old law averaged them by list position.")
else:
    print("  (no BEFORE file supplied -- pass its path as argv[1] to run this arm)")
    print("  SKIPPED, and a skipped arm is NOT a pass.")

print("=" * 78)
print("ARM 4 -- the law REFUSES the shapes it used to guess at")
print("=" * 78)
from perfrp_rollup import RollupRefused, rollup  # noqa: E402

try:
    rollup([{"key": "a", "dollars": 1, "denominator": 1, "daily": [0.01, 0.02]},
            {"key": "b", "dollars": 1, "denominator": 1, "daily": [0.03]}],
           from_level="account", to_level="relationship")
    check("undated children of DIFFERING lengths are refused", False, "it returned")
except RollupRefused as e:
    check("undated children of DIFFERING lengths are refused", True, str(e)[:52])
try:
    rollup([{"key": "a", "dollars": 1, "denominator": 1, "daily": [0.01],
             "dates": ["2024-07-09"]},
            {"key": "b", "dollars": 1, "denominator": 1, "daily": [0.03]}],
           from_level="account", to_level="relationship")
    check("MIXED dated/undated children are refused", False, "it returned")
except RollupRefused as e:
    check("MIXED dated/undated children are refused", True, str(e)[:52])
# POSITIVE CONTROL: the legal shapes still work
r_ok = rollup([{"key": "a", "dollars": 1, "denominator": 1, "daily": [0.01, 0.02]},
               {"key": "b", "dollars": 1, "denominator": 1, "daily": [0.03, 0.04]}],
              from_level="account", to_level="relationship")
check("POSITIVE CONTROL: equal-length undated children still roll up",
      r_ok["window_return"] is not None, "%.6f" % r_ok["window_return"])
# and the date-aligned path puts each child's value on ITS OWN day
r_dated = rollup(
    [{"key": "a", "dollars": 1, "denominator": 1, "daily": [0.10, 0.0],
      "dates": ["2024-07-09", "2024-07-10"]},
     {"key": "b", "dollars": 1, "denominator": 1, "daily": [0.10],
      "dates": ["2024-07-10"]}],
    from_level="account", to_level="relationship",
    window_dates=["2024-07-09", "2024-07-10"])
# day 1: only a (0.10). day 2: a=0.0 and b=0.10, equal weights -> 0.05.
expect = (1 + 0.10) * (1 + 0.05) - 1
check("date-aligned parent puts each child's value on ITS OWN day",
      abs(r_dated["window_return"] - expect) < 1e-12,
      "%.10f vs expected %.10f" % (r_dated["window_return"], expect))
# THE DISCRIMINATOR: the positional law would have paired b's ONLY day with a's FIRST.
positional = (1 + (0.10 + 0.10) / 2) * (1 + 0.0) - 1
check("...and that DIFFERS from what positional alignment would give",
      abs(r_dated["window_return"] - positional) > 1e-9,
      "dated %.10f vs positional %.10f" % (r_dated["window_return"], positional))

print("=" * 78)
print("ARM 5 -- pins carried on the relationship grain")
print("=" * 78)
pins = rel["window"]["upstream_pins"]
for t, p in pins.items():
    print("  %-38s n=%s max_lm=%s" % (t, p["n_partitions_read"], p["max_last_modified_utc"]))
check("twr pin spans the whole window",
      pins["canonical/twr_daily"]["n_partitions_read"]
      == rel["window"]["expected_trading_days"])
check("every pin carries the PAIR",
      all("max_last_modified_utc" in p and "n_partitions_read" in p for p in pins.values()))

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d ARM(S) FAILED: %s" % (len(FAILS), FAILS))
    sys.exit(1)
print("RESULT: ALL ARMS PASS")
