"""IRPT_DASHBD round 30, amendment 1 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling on row IRPT_DASHBD-S35 (msg 1660):
DB-b-53 and DB-b-54 are CANCELLED; ONE replacement cell re-grades the whole tie-out on the COMPOUNDED fee basis. S35 (3.0.0_SA_CVO)
measured that round 18's additive add-back (gross = net + fees/avg balance) is the right-half gap: compounding moves the median from
+0.567 pp to +0.043 pp, and the tied count from 0 to 1,334 of 1,527.

The re-graded population is round 18's record (TIEOUT_49F_BD_POPULATION_E2_GROSS.json): 9,082 planned, 9,078 graded (5,416 within
0.35 pp, 3,662 outside), 4 not gradable. Its reasons closed set is {FLOW_TIMING, MISSING_PRICE, INCOME_DATE, COVERAGE_DAYS, UNEXPLAINED}.

Usage: python <this file> <repo_root> <criterion_id>
  DB30-4-AC1  the worker's tests file TIEOUT_COMPOUND_TEST (below) holds a test whose name contains "chain" (two adjacent ranges chain
              to the whole on the compounded basis), and pytest on that file passes. Base: FAIL.
  DB30-4-AC2  TIEOUT_COMPOUND_E1.json: `segments` cover exactly round 18's 9,078 graded (account, segment start, end); `before`
              equals round 18's counts {within: 5,416, outside: 3,662}; `after` {within, outside} sums to 9,078 and equals the row
              tally (abs_diff_pp <= 0.35 -> within); `share_within_after` == after.within / 9,078. Base: FAIL.
  DB30-4-AC3  every after-OUTSIDE row carries a `reason` from round 18's closed set, and `after_outside_by_reason` equals the tally and
              sums to after.outside -- the misses are named, never forced. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R18 = D + "0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
W = D + "0.9.0_WK_IRPT_DASHBD~34/"
REC = W + "TIEOUT_COMPOUND_E1.json"
TIEOUT_COMPOUND_TEST = W + "test_tieout_compound.py"
TOL_PP = 0.35


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB30-4"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB30-4-AC1":
        p = root / TIEOUT_COMPOUND_TEST
        t = p.read_bytes().decode("utf-8") if p.is_file() else ""
        if not re.search(r"^def test_\w*chain\w*\(", t, re.M):
            fail("no test whose name contains 'chain' in %s" % TIEOUT_COMPOUND_TEST)
        rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(p)], cwd=str(root),
                            capture_output=True, text=True, timeout=300)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
        m = re.search(r"(\d+) passed", out)
        if rr.returncode or not m:
            fail("pytest: %s" % out[-300:])
        print("OK: %s tests pass, a 'chain' test included" % m.group(1))
        print("%s PASS" % cid)
        return

    r18 = load(R18)
    graded = {(s["account"], s["segment"]["start"], s["segment"]["end"]) for s in r18["segments"] if s["verdict"] in ("WITHIN", "OUTSIDE")}
    want_before = {"within": r18["counts"]["within_tolerance"], "outside": r18["counts"]["outside_tolerance"]}
    closed = set(r18["reasons_closed_set"])
    r = load(REC)
    segs = r.get("segments") or []
    keys = {(s.get("account"), (s.get("segment") or {}).get("start"), (s.get("segment") or {}).get("end")) for s in segs}
    if keys != graded or len(segs) != len(graded):
        fail("%d segments; equal to round 18's %d graded: %s" % (len(segs), len(graded), keys == graded))
    if [s for s in segs if not isinstance(s.get("abs_diff_pp"), (int, float))]:
        fail("a segment without a numeric abs_diff_pp")
    within = sum(1 for s in segs if s["abs_diff_pp"] <= TOL_PP)
    outside = len(segs) - within
    if cid == "DB30-4-AC2":
        if {k: (r.get("before") or {}).get(k) for k in want_before} != want_before:
            fail("before %r, round 18 records %r" % (r.get("before"), want_before))
        after = r.get("after") or {}
        if after.get("within") != within or after.get("outside") != outside:
            fail("after %r, the row tally gives within %d outside %d" % (after, within, outside))
        share = within / len(graded)
        if not isinstance(r.get("share_within_after"), (int, float)) or abs(r["share_within_after"] - share) > 1e-9:
            fail("share_within_after %r, recomputed %.4f" % (r.get("share_within_after"), share))
        print("OK: %d segments; within before %d -> after %d (share %.4f); outside %d -> %d" % (
            len(graded), want_before["within"], within, share, want_before["outside"], outside))
    elif cid == "DB30-4-AC3":
        tally = {}
        for s in segs:
            if s["abs_diff_pp"] > TOL_PP:
                if s.get("reason") not in closed:
                    fail("an after-OUTSIDE row with reason %r outside the closed set %s" % (s.get("reason"), sorted(closed)))
                tally[s["reason"]] = tally.get(s["reason"], 0) + 1
        if (r.get("after_outside_by_reason") or {}) != tally or sum(tally.values()) != outside:
            fail("after_outside_by_reason %r, the tally %r over %d" % (r.get("after_outside_by_reason"), tally, outside))
        print("OK: %d misses named: %s" % (outside, tally))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
