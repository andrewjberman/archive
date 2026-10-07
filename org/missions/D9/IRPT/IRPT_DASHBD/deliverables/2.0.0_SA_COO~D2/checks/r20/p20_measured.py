"""IRPT_DASHBD round 20 (workstream B, issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-19 analysis @b402b7b2e3 with its E1
method ruling (msg 400): E1 MEASURES the 226 inferred FLOW_TIMING segments (a Modified Dietz of Opal's dated flows over BD's own
bmv/emv/netAdditions, with a midpoint negative control and a flow-totals guard); E2 re-reads the 754 non-closure UNEXPLAINED segments
with Opal's served daily series, now readable on dell2. Zero vendor calls.

Usage: python <this file> <repo_root> <criterion_id>
  DB20-1-AC1  E1 record: one row per FLOW = round-19 E2 rows with reason FLOW_TIMING (re-derived), each with dietz_return,
              abs_diff_pp_dietz, flows_match (bool) and verdict (MEASURED_FLOW_TIMING | UNEXPLAINED); counts.measured and
              counts.returned_unexplained equal the rows; counts.unexplained_measured_basis == 3,053 + returned_unexplained.
              Base: FAIL.
  DB20-1-AC2  the guards: every row carries abs_diff_pp_midpoint; counts.negative_control_within equals the rows within 0.35 pp
              at the midpoint; no row is MEASURED_FLOW_TIMING with flows_match false or abs_diff_pp_dietz above 0.35. Base: FAIL.
  DB20-1-AC3  the E1 tests pass (at least 4, naming midpoint). Base: FAIL.
  DB20-2-AC1  E2 record: denominator == |RESIDUE = round-19 E2 rows with reason UNEXPLAINED| (re-derived); per_reason sums to it;
              final_unexplained equals the UNEXPLAINED rows. Base: FAIL.
  DB20-2-AC2  one row per RESIDUE segment, each with a closed-set reason and non-empty evidence. Base: FAIL.
  DB20-2-AC3  the E2 tests pass (at least 4, naming residue). Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R19 = P + "0.9.0_WK_IRPT_DASHBD~15/RESIDUE_NONCLOSURE_E2.json"
W1 = P + "0.9.0_WK_IRPT_DASHBD~16/"
W2 = P + "0.9.0_WK_IRPT_DASHBD~17/"
E1R = W1 + "FLOW_MEASURED_E1.json"
E2R = W2 + "RESIDUE_754_E2.json"
T1 = W1 + "tests/test_flow_measured_e1.py"
T2 = W2 + "tests/test_residue_754_e2.py"
REASONS = {"FLOW_TIMING", "MISSING_PRICE", "INCOME_DATE", "COVERAGE_DAYS", "UNEXPLAINED"}
TOL = 0.35
BASE_UNEXPLAINED = 3053  # round 19: 754 non-closure + 2,299 closure


def _load(root, rel, fail):
    p = root / rel
    if not p.is_file():
        fail("no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def _key(s):
    seg = s.get("segment") or {}
    return (s.get("account"), seg.get("start"), seg.get("end"))


def _pytest(root, rel, word, fail):
    t = root / rel
    if not t.is_file():
        fail("no %s" % rel)
    if word not in t.read_bytes().decode("utf-8"):
        fail("tests never name %r" % word)
    rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(t)], cwd=str(root),
                        capture_output=True, text=True, timeout=110)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
    m = re.search(r"(\d+) passed", out)
    if rr.returncode or not m or int(m.group(1)) < 4:
        fail("pytest: %s" % out[-300:])
    return int(m.group(1))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB20"))
        sys.exit(1)

    if cid in ("DB20-1-AC1", "DB20-1-AC2"):
        r19 = [r for r in _load(root, R19, fail).get("rows") or [] if r.get("reason") == "FLOW_TIMING"]
        flow = {_key(r) for r in r19}
        rec = _load(root, E1R, fail)
        rows = rec.get("rows") or []
        c = rec.get("counts") or {}
        if cid == "DB20-1-AC1":
            ks = [_key(r) for r in rows]
            if len(ks) != len(set(ks)) or set(ks) != flow:
                fail("%d rows (%d distinct) against a FLOW set of %d" % (len(ks), len(set(ks)), len(flow)))
            need = {"dietz_return", "abs_diff_pp_dietz", "flows_match", "verdict"}
            bad = [r for r in rows if not need <= set(r) or r.get("verdict") not in ("MEASURED_FLOW_TIMING", "UNEXPLAINED")
                   or not isinstance(r.get("flows_match"), bool)]
            if bad:
                fail("%d rows lack the E1 fields or carry a verdict outside the two values" % len(bad))
            meas = sum(1 for r in rows if r["verdict"] == "MEASURED_FLOW_TIMING")
            ret = len(rows) - meas
            got = (c.get("measured"), c.get("returned_unexplained"), c.get("unexplained_measured_basis"))
            exp = (meas, ret, BASE_UNEXPLAINED + ret)
            if got != exp:
                fail("counts (measured, returned_unexplained, unexplained_measured_basis) = %r, re-derived %r" % (got, exp))
            print("OK: %d of %d FLOW_TIMING segments measured; UNEXPLAINED on a measured basis %d" % (meas, len(rows), exp[2]))
        else:
            if [r for r in rows if "abs_diff_pp_midpoint" not in r]:
                fail("a row lacks abs_diff_pp_midpoint")
            mid = sum(1 for r in rows if r.get("abs_diff_pp_midpoint") is not None and r["abs_diff_pp_midpoint"] <= TOL)
            if c.get("negative_control_within") != mid:
                fail("negative_control_within %r, re-derived %d" % (c.get("negative_control_within"), mid))
            wrong = [r for r in rows if r.get("verdict") == "MEASURED_FLOW_TIMING"
                     and (r.get("flows_match") is not True or r.get("abs_diff_pp_dietz") is None or r["abs_diff_pp_dietz"] > TOL)]
            if wrong:
                fail("%d rows MEASURED while flows_match is false or the Dietz gap exceeds 0.35 pp" % len(wrong))
            print("OK: negative control (flows at the midpoint) keeps %d of %d within 0.35 pp; the guards hold" % (mid, len(rows)))
    elif cid == "DB20-1-AC3":
        print("OK: %d E1 tests passed" % _pytest(root, T1, "midpoint", fail))
    elif cid in ("DB20-2-AC1", "DB20-2-AC2"):
        res = {_key(r) for r in _load(root, R19, fail).get("rows") or [] if r.get("reason") == "UNEXPLAINED"}
        rec = _load(root, E2R, fail)
        rows = rec.get("rows") or []
        if cid == "DB20-2-AC1":
            c = rec.get("counts") or {}
            per = c.get("per_reason") or {}
            final = sum(1 for r in rows if r.get("reason") == "UNEXPLAINED")
            if c.get("denominator") != len(res) or sum(per.values()) != len(res) or c.get("final_unexplained") != final:
                fail("denominator %r, per_reason sum %d, final_unexplained %r; re-derived %d / %d" % (
                    c.get("denominator"), sum(per.values()), c.get("final_unexplained"), len(res), final))
            print("OK: residue %d; final UNEXPLAINED %d" % (len(res), final))
        else:
            ks = [_key(r) for r in rows]
            if len(ks) != len(set(ks)) or set(ks) != res:
                fail("%d rows (%d distinct) against a residue of %d" % (len(ks), len(set(ks)), len(res)))
            bad = [r for r in rows if r.get("reason") not in REASONS or not str(r.get("evidence") or "").strip()]
            if bad:
                fail("%d rows lack a closed-set reason or evidence" % len(bad))
            print("OK: %d residue rows, each with a closed-set reason and evidence" % len(rows))
    elif cid == "DB20-2-AC3":
        print("OK: %d E2 tests passed" % _pytest(root, T2, "residue", fail))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
