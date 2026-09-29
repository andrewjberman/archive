"""AMGT_RESAPP round 47, AMGT-vv-2 AC1 -- THE SCOPED API CARRIES THE TEAM'S CASES, CITED, BY CASE, BESIDE (NEVER REPLACING) THE RULE'S BASE.

CTO round-46 analysis ruling 3 (@0e405cc330) + CORPUS round-9 ruling 1 (CTO msg 26430). For each name below, the served payload
function `scoped_amgt._team_cases(security_key)` must equal, case by case (base, upside, downside), what the ONE dossier read
`lib.research.corpus.dossier.read_dossier(security_key)["document"]["fields"]["cases"]` holds NOW:
  - a case whose dossier `value` is not null -> {"status": "SERVED", "table": <dossier value, unchanged>, "citation": <dossier
    citation, unchanged>, and EVERY unit/currency key the dossier case carries (e.g. `unit`, `unit_as_written`, `currency`),
    copied as-is -- a null stays null, nothing is converted or inferred};
  - a case whose dossier `value` is null -> {"status": "ABSENT", "reason": <the dossier's `absent` text, unchanged>};
The /thesis carriage (`model.team_cases` beside an unchanged `model.cases`) is graded on the served plane at vv-4 AC3, not here.
Names: ASML_NA_Equity (carries cases at the cut), AMD_US_Equity (absent at the cut).
usage: python <this>   (from the repo root; reads S3 read-only)"""
import os
import sys

sys.path.insert(0, os.getcwd())
from lib.research.api import scoped_amgt as sa  # noqa: E402
from lib.research.corpus import dossier  # noqa: E402

NAMES = ["ASML_NA_Equity", "AMD_US_Equity"]
UNIT_KEYS = ("unit", "unit_as_written", "currency")


def expected(case):
    case = case or {}
    if case.get("value") is None:
        return {"status": "ABSENT", "reason": case.get("absent")}
    out = {"status": "SERVED", "table": case.get("value"), "citation": case.get("citation")}
    for k in UNIT_KEYS:
        if k in case:
            out[k] = case[k]
    return out


def main():
    ok = 0
    if not hasattr(sa, "_team_cases"):
        print("scoped_amgt has no _team_cases")
        print("TEAM CASES CARRIED AS THE DOSSIER HOLDS THEM: 0 of %d names" % len(NAMES))
        return 1
    for key in NAMES:
        want_cases = (dossier.read_dossier(key)["document"].get("fields") or {}).get("cases") or {}
        got = sa._team_cases(key) or {}
        bad = []
        for name in ("base", "upside", "downside"):
            w, g = expected(want_cases.get(name)), got.get(name) or {}
            for k, v in w.items():
                if g.get(k) != v:
                    bad.append("%s.%s differs" % (name, k))
        print("%s: %s" % (key, "OK" if not bad else "; ".join(bad[:4])))
        ok += not bad
    print("TEAM CASES CARRIED AS THE DOSSIER HOLDS THEM: %d of %d names" % (ok, len(NAMES)))
    return 0 if ok == len(NAMES) else 1


if __name__ == "__main__":
    sys.exit(main())
