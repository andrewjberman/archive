"""IRPT_DASHBD round 28, workstream BD (issuer 2.0.0_SA_COO~D2) -- FWD-8's split tie-out: Black Diamond's own gross returns either side of
the 2025-01-09 closure (pull=split20261007, 2,299 of 2,299 landed, DB-b-45) against Opal's served figure over the same two ranges.
Branches, stated in the round-19 analysis @b402b7b2e3 section 2 before the word was spent: (A) the split figures tie within 0.35 pp on
most of the 2,299; (B) they do not. "Most" is stated here, before the run: MORE THAN HALF (> 1,149.5) of the 2,299 tie on BOTH halves.

Usage: python <this file> <repo_root> <criterion_id>
  DB28-3-AC1  TIEOUT_SPLIT_E1.json: files_read == 2,299 (the landed objects); rows == the 2,299 accounts of the plan; each row carries
              left and right {bd_return, opal_return, abs_diff_pp, tied} with tied == (abs_diff_pp <= 0.35), or a named `reason` where a
              figure is absent; counts {tied_both, tied_left_only, tied_right_only, tied_neither, absent} summing to 2,299. Base: FAIL.
  DB28-3-AC2  the branch is graded from the counts by the rule above: branch A iff tied_both > 1,149.5, else B; `branch` agrees; the
              control `recompose` (BD's two halves chained, against BD's own full-segment gross from the round-18 GROSS record) is
              printed with its count within 0.35 pp. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
PLAN = D + "0.9.0_WK_IRPT_DASHBD~25/SPLIT_PULL_PLAN.json"
REC = D + "0.9.0_WK_IRPT_DASHBD~28/TIEOUT_SPLIT_E1.json"
TOL = 0.35
N = 2299


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB28-3"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    r = load(REC)
    rows = r.get("rows") or []
    counts = r.get("counts") or {}
    if cid == "DB28-3-AC1":
        accts = {q["account"] for q in load(PLAN)["request_list"]}
        if r.get("files_read") != N or len(rows) != N or {x.get("account") for x in rows} != accts:
            fail("files_read %r, %d rows, accounts equal plan: %s" % (r.get("files_read"), len(rows), {x.get("account") for x in rows} == accts))
        bad = 0
        for x in rows:
            for side in ("left", "right"):
                s = x.get(side) or {}
                if s.get("abs_diff_pp") is None:
                    if not str(s.get("reason") or x.get("reason") or "").strip():
                        bad += 1
                elif bool(s.get("tied")) != (float(s["abs_diff_pp"]) <= TOL):
                    bad += 1
        if bad:
            fail("%d half-rows with a tie flag against the 0.35 pp rule or an absent figure without a reason" % bad)
        keys = ("tied_both", "tied_left_only", "tied_right_only", "tied_neither", "absent")
        if [k for k in keys if not isinstance(counts.get(k), int)] or sum(counts[k] for k in keys) != N:
            fail("counts %r do not close over %d" % (counts, N))
        print("OK: %d files, %d rows; %s" % (N, len(rows), {k: counts[k] for k in keys}))
    elif cid == "DB28-3-AC2":
        want = "A" if counts.get("tied_both", 0) > N / 2 else "B"
        if r.get("branch") != want:
            fail("branch %r, the counts give %s (tied_both %r of %d)" % (r.get("branch"), want, counts.get("tied_both"), N))
        rc = r.get("recompose") or {}
        if not isinstance(rc.get("within_tolerance"), int) or not isinstance(rc.get("compared"), int):
            fail("recompose control %r incomplete" % rc)
        print("OK: branch %s (tied on both halves: %d of %d); recompose control %d of %d within 0.35 pp" % (
            want, counts["tied_both"], N, rc["within_tolerance"], rc["compared"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
