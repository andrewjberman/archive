"""DB-b-28: read the residue of the E2 gross re-grade. Offline; reads the GROSS record, writes RESIDUE_E2_GROSS.json."""
import json
import sys
from collections import Counter
from pathlib import Path

CLOSURE = "2025-01-09"
REASONS = ("FLOW_TIMING", "MISSING_PRICE", "INCOME_DATE", "COVERAGE_DAYS", "UNEXPLAINED")
HERE = Path(__file__).resolve().parent


def _key(s):
    g = s.get("segment") or {}
    return (s.get("account"), g.get("start"), g.get("end"))


def is_unexplained(s):
    return s.get("verdict") == "OUTSIDE" and s.get("reason") == "UNEXPLAINED"


def is_plus_one(s):
    g = s.get("segment") or {}
    return ((s.get("bd_days_held") or 0) - (s.get("opal_days") or 0) == 1
            and g.get("start", "9") <= CLOSURE <= g.get("end", "0"))


def residue(gross):
    graded = [s for s in gross.get("segments") or [] if s.get("verdict") in ("WITHIN", "OUTSIDE")]
    rows = []
    n_un = n_p1 = n_ov = 0
    for s in graded:
        un, p1 = is_unexplained(s), is_plus_one(s)
        if not (un or p1):
            continue
        sets = [n for n, f in (("UNEXPLAINED", un), ("PLUS_ONE_DAY", p1)) if f]
        n_un += un
        n_p1 += p1
        n_ov += un and p1
        g = s["segment"]
        days = "BD %s days vs Opal %s days (+1) over the %s closure, segment %s..%s" % (
            s.get("bd_days_held"), s.get("opal_days"), CLOSURE, g.get("start"), g.get("end"))
        if un:
            reason = "UNEXPLAINED"
            ev = "kept UNEXPLAINED (a +1-day gap is residue, never agreement; PRD ruling 23). Checked: %s" % s.get("evidence")
            if p1:
                ev = days + "; " + ev
        elif s.get("verdict") == "OUTSIDE":
            reason = s.get("reason")
            ev = "%s; reason from the gross record: %s" % (days, s.get("evidence"))
        else:
            reason = "COVERAGE_DAYS"
            ev = "%s; WITHIN tolerance (abs_diff_pp %s) but the day counts differ by one" % (days, s.get("abs_diff_pp"))
        rows.append({"account": s.get("account"), "segment": g, "sets": sets, "reason": reason, "evidence": ev})
    per = Counter(r["reason"] for r in rows)
    counts = {"denominator": len(graded), "unexplained": n_un, "plus_one_day": n_p1, "overlap": n_ov,
              "union": len(rows), "residue_per_reason": {k: per.get(k, 0) for k in REASONS}}
    return {"task_order": "IRPT_DASHBD.TO-DB-b-28", "source": "TIEOUT_49F_BD_POPULATION_E2_GROSS.json",
            "closure_date": CLOSURE, "vendor_calls": 0, "reasons_closed_set": list(REASONS),
            "counts": counts, "rows": rows}


def main():
    g = json.loads((HERE / "TIEOUT_49F_BD_POPULATION_E2_GROSS.json").read_bytes().decode("utf-8"))
    out = residue(g)
    (HERE / "RESIDUE_E2_GROSS.json").write_bytes((json.dumps(out, indent=1) + "\n").encode("utf-8"))
    print(json.dumps(out["counts"]))


if __name__ == "__main__":
    sys.exit(main())
