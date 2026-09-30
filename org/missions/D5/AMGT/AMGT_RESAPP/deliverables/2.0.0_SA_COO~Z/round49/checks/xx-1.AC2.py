"""AMGT_RESAPP round 49, AMGT-xx-1 AC2 -- the grade's `reason` names the class that differs, CASES included (CTO round-48 ruling 2).

`sweep.compare_facts(page, rich)` takes two dicts of sets keyed "FIGURES", "CITES", "ABSENCES", "CASES" and returns a dict with
`verdict` ("OK" | "NOT_OK") and `reason` naming EVERY class that differs and no other ("" when OK). Four planted pairs:
equal -> OK / ""; cases-only -> NOT_OK naming CASES only; absences-only -> ABSENCES only; figures+cases -> both, not the others.
usage: python <this>   (from the repo root)"""
import importlib.util
import sys

SWEEP = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round45/checks/sweep.py"
CLASSES = ("FIGURES", "CITES", "ABSENCES", "CASES")


def facts(**over):
    base = {"FIGURES": {"f1", "f2"}, "CITES": {"c1"}, "ABSENCES": {"a1", "a2"}, "CASES": {"base", "upside"}}
    base.update(over)
    return base


def main():
    sys.path.insert(0, ".")
    spec = importlib.util.spec_from_file_location("sweep", SWEEP)
    sweep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sweep)
    if not hasattr(sweep, "compare_facts"):
        print("sweep.py has no compare_facts")
        print("THE REASON NAMES THE CLASS THAT DIFFERS: NO")
        return 1
    plants = [
        ("equal", facts(), facts(), set()),
        ("cases-only", facts(), facts(CASES={"base", "downside"}), {"CASES"}),
        ("absences-only", facts(), facts(ABSENCES={"a1"}), {"ABSENCES"}),
        ("figures+cases", facts(), facts(FIGURES={"f1"}, CASES={"base"}), {"FIGURES", "CASES"}),
    ]
    bad = 0
    for label, page, rich, want in plants:
        got = sweep.compare_facts(page, rich) or {}
        named = {c for c in CLASSES if c in str(got.get("reason") or "")}
        verdict_ok = got.get("verdict") == ("OK" if not want else "NOT_OK")
        good = verdict_ok and named == want
        bad += not good
        print("%-14s verdict %-7s reason %r -> %s" % (label, got.get("verdict"), got.get("reason"), "ok" if good else "WRONG"))
    ok = bad == 0
    print("THE REASON NAMES THE CLASS THAT DIFFERS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
