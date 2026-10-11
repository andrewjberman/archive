"""IRPT_BCKEND round 123 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one read-only DIRECT-ACT order:
  IB123-1  IB-pr-425  row S252 measured on EVERY trading-day partition of Cottonwood's declared silver holdings source
                      (CTO msg 4729): which securities carry the prior day's close, on how many days.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB123-1-AC1  the day table covers every trading-day partition listed (graded + first-day-no-prior + ungradeable ==
               listed, each ungradeable day with its reason), and each graded day's counts add up. Base: FAIL (no file).
  IB123-1-AC2  the security table: one row per security ever read at the prior close, each with days_lagged <= days_moved,
               a class, and totals equal to the day table's. Base: FAIL (no file).
  IB123-1-AC3  the control: on a planted fixture the instrument reports the planted lagged security and no other.
               Base: FAIL (no file).
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~284/"
OUT = D + "IB123-1_s252_all_partitions.json"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB123"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    days = a.get("days") or []
    graded = [d for d in days if d.get("state") == "GRADED"]

    if cid == "IB123-1-AC1":
        listed = a.get("trading_day_partitions_listed")
        if not isinstance(listed, int) or listed < 80:
            fail("trading_day_partitions_listed %r" % listed)
        states = {}
        for d in days:
            states[d.get("state")] = states.get(d.get("state"), 0) + 1
        if set(states) - {"GRADED", "FIRST_DAY_NO_PRIOR", "UNGRADEABLE"}:
            fail("unknown day state(s) %r" % sorted(states))
        if len(days) != listed or len({d.get("date") for d in days}) != listed:
            fail("%d day rows (%d distinct) for %d partitions listed" % (len(days), len({d.get('date') for d in days}), listed))
        if states.get("FIRST_DAY_NO_PRIOR", 0) > 1:
            fail("more than one first day")
        for d in days:
            if d.get("state") == "UNGRADEABLE" and not d.get("reason"):
                fail("%s is UNGRADEABLE with no reason" % d.get("date"))
            if d.get("state") == "GRADED":
                m, o, p, n = d.get("moved"), d.get("own_close"), d.get("prior_close"), d.get("neither")
                if not all(isinstance(x, int) for x in (m, o, p, n)) or o + p + n != m:
                    fail("%s counts do not add up: moved %r own %r prior %r neither %r" % (d.get("date"), m, o, p, n))
        print("OK: %d of %d trading-day partitions accounted for (%s); every graded day's counts add up" % (len(days), listed, states))
    elif cid == "IB123-1-AC2":
        secs = a.get("lagged_securities") or []
        if not graded:
            fail("no graded day")
        total_prior = sum(d["prior_close"] for d in graded)
        if sum(s.get("days_lagged", 0) for s in secs) != total_prior:
            fail("security table sums to %d lagged security-days, the day table to %d" % (sum(s.get('days_lagged', 0) for s in secs), total_prior))
        for s in secs:
            if not s.get("security") or not s.get("class") or not isinstance(s.get("days_lagged"), int) \
                    or not isinstance(s.get("days_moved"), int) or not 1 <= s["days_lagged"] <= s["days_moved"]:
                fail("security row %r" % s)
        if len({s["security"] for s in secs}) != len(secs):
            fail("a security appears twice")
        by = a.get("lagged_by_class") or {}
        if sum(by.values()) != len(secs):
            fail("lagged_by_class sums to %d, %d securities listed" % (sum(by.values()), len(secs)))
        print("OK: %d securities ever at the prior close, %d lagged security-days over %d graded days; classes %s" % (
            len(secs), total_prior, len(graded), by))
    elif cid == "IB123-1-AC3":
        c = a.get("control") or {}
        if c.get("planted") is None or c.get("reported") != [c.get("planted")] or c.get("clean_fixture_reported") != []:
            fail("control %r" % c)
        print("OK: the planted lagged security is reported alone; the clean fixture reports none")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
