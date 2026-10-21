"""AR-y-498 check: the Overview's replaced-in-all-figures line, built through layout_overview's own functions (offline).

Run from the worktree root:
    python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~370/check_replaced_line.py
    python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~370/check_replaced_line.py --selftest

Stdlib only. Offline: no AWS, no network, no model call. The module is imported BY PATH from this worktree.
--selftest mutates the module text in memory four ways and prints CONTROL-FIRES only when all four read BAD.
"""
import copy
import importlib.util
import json
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
RESEARCH = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "research"
MODULE = RESEARCH / "layout_overview.py"
FIXTURES = RESEARCH / "tests" / "fixtures"

# The spec strings, written here apart from the module's constants, so a changed constant cannot pass unnoticed.
E_ONE = "Replaced in all figures: BREIT by CTO (same asset class and sub asset class)."
E_TWO = ("Replaced in all figures: BREIT by CTO (same asset class and sub asset class); "
         "XYZ by DDD (same asset class and sub asset class, a low-confidence match).")
E_LOW = "Replaced in all figures: XYZ by DDD (same asset class and sub asset class, a low-confidence match)."
E_ESC = "Replaced in all figures: &lt;b&gt;X&amp;Y by D&amp;D (same asset class and sub asset class)."

MUTANTS = [
    ("join", 'REPLACED_JOIN = "; "', 'REPLACED_JOIN = ", "'),
    ("low_suffix", 'REPLACED_LOW = ", a low-confidence match"', 'REPLACED_LOW = ""'),
    ("prefix", 'REPLACED_PREFIX = "Replaced in all figures: "', 'REPLACED_PREFIX = "Replaced: "'),
    ("filter", 'if rec.get("status") == "REPLACED"]', 'if rec.get("status") == "NEVER"]'),
]


def _rec(ticker, proxy, low=False):
    return {"proxy_for": ticker, "proxy": proxy, "status": "REPLACED", "why": None, "low_confidence": low}


def _left(ticker):
    return {"proxy_for": ticker, "proxy": None, "status": "NO_REPLACEMENT", "why": "NO_CLASS"}


# six fixture swap lists: name -> swaps
CASES = {
    "one": [_rec("BREIT", "CTO")],
    "two": [_rec("BREIT", "CTO"), _rec("XYZ", "DDD", True)],
    "low": [_rec("XYZ", "DDD", True)],
    "left_only": [_left("ZQXWVK")],
    "none": [],
    "mixed_amount": [_left("ZQXWVK"), dict(_rec("BREIT", "CTO"), amount=250000.0)],
}


def load_module(text=None):
    """The layout module by path: the file when text is None, else the given (mutated) source text."""
    if text is None:
        spec = importlib.util.spec_from_file_location("layout_overview_under_check", MODULE)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    mod = types.ModuleType("layout_overview_under_check")
    mod.__file__ = str(MODULE)
    exec(compile(text, str(MODULE), "exec"), mod.__dict__)
    return mod


def _escaped_ok(mod):
    """A replaced row whose ticker and proxy carry HTML symbols prints the escaped line, as the left-out line does."""
    run = json.loads((FIXTURES / "run.json").read_text(encoding="utf-8"))
    map_doc = json.loads((FIXTURES / "map.json").read_text(encoding="utf-8"))
    kept = mod.load_kept(FIXTURES / "kept")
    run = copy.deepcopy(run)
    run["swaps"] = [{"proxy_for": "<b>X&Y", "proxy": "D&D", "status": "REPLACED", "why": None, "low_confidence": False}]
    html = mod.build(run, kept, copy.deepcopy(map_doc), mod.load_brand())
    return ('<p class="na">%s</p>' % E_ESC) in html and "<b>X&Y" not in html


def evaluate(mod):
    """-> (flags, failures): each flag True or False; failures names every flag that reads no."""
    got = {name: mod._replaced_line({"swaps": swaps}) for name, swaps in CASES.items()}
    flags = {
        "exact_text": got["one"] == E_ONE and got["mixed_amount"] == E_ONE,
        "join": got["two"] == E_TWO,
        "low_conf": got["low"] == E_LOW and "low-confidence" not in (got["one"] or ""),
        "no_line_when_none": got["left_only"] is None and got["none"] is None,
        "escaped": _escaped_ok(mod),
    }
    failures = ["%s=no" % name for name, value in flags.items() if not value]
    return flags, failures


def run_check(text=None):
    """-> (ok, line): the one verdict line the check prints for the module built from `text` (the file when None)."""
    try:
        flags, failures = evaluate(load_module(text))
    except Exception as exc:  # a module that will not import or build reads BAD, named
        return False, "REPLACED-LINE-BAD %s: %s" % (type(exc).__name__, exc)
    if failures:
        return False, "REPLACED-LINE-BAD " + "; ".join(failures)
    body = " ".join("%s=%s" % (name, "yes") for name in flags)
    return True, "REPLACED-LINE-OK cases=%d %s" % (len(CASES), body)


def selftest():
    source = MODULE.read_text(encoding="utf-8")
    base_ok, base_line = run_check(None)
    print("baseline: %s" % base_line, file=sys.stderr)
    if not base_ok:
        print("CONTROL-DID-NOT-FIRE baseline-not-ok")
        return 1
    all_fire = True
    for name, old, new in MUTANTS:
        count = source.count(old)
        if count != 1:
            all_fire = False
            print("CONTROL-NOT-APPLIED %s count=%d" % (name, count), file=sys.stderr)
            continue
        ok, line = run_check(source.replace(old, new))
        print("mutant %s: %s" % (name, line), file=sys.stderr)
        if ok:
            all_fire = False
    if all_fire:
        print("CONTROL-FIRES")
        return 0
    print("CONTROL-DID-NOT-FIRE")
    return 1


def main():
    if "--selftest" in sys.argv[1:]:
        return selftest()
    ok, line = run_check(None)
    print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
