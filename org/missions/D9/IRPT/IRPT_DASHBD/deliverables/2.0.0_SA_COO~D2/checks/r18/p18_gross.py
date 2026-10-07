"""IRPT_DASHBD round 18 (workstream B, issuer 2.0.0_SA_COO~D2) -- the CTO's round-15..17 analysis items E1 and E2
(org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_ROUNDS_15_17_20261007.md @e363a194ed, W12-S1 ruled):
re-grade the E2 tie-out on ONE gross basis (BD's own reported fee added back to BD's net return), then read the residue.
Zero vendor calls.

Usage: python <this file> <repo_root> <criterion_id>
  DB18-1-AC1  the GROSS record exists and reconciles: basis GROSS, tolerance 0.35, vendor_calls 0; planned = graded +
              not_gradable = the plan's segment count; within + outside = graded; every graded row carries the keys
              bd_fee_addback and bd_gross_return; every outside row carries a reason from the UNCHANGED closed set; every
              not_gradable row a why. Base: FAIL (no record).
  DB18-1-AC2  bd_fee_addback is null exactly where bd_fees_reported is null or zero, and non-null everywhere else; the
              tests pass (at least 4, naming bd_fee_addback). Base: FAIL.
  DB18-1-AC3  no net-of-fee Opal figure: no segment key names opal together with net or fee, and every graded row's
              opal_return equals the round-17 record's opal_return for the same account and segment (the served figure
              is compared unchanged). Base: FAIL (no record).
  DB18-2-AC1  the RESIDUE record's counts are re-derived from the GROSS record: denominator = graded; unexplained =
              the GROSS record's UNEXPLAINED count; plus_one_day = graded rows with bd_days_held - opal_days == 1 whose
              segment spans 2025-01-09; overlap = their intersection. Base: FAIL.
  DB18-2-AC2  one residue row per segment in the union of the two sets; each carries a reason from the closed set and
              a non-empty evidence string. Base: FAIL.
  DB18-2-AC3  the residue tests pass (at least 4, naming overlap). Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
W = P + "0.9.0_WK_IRPT_DASHBD~13/"
GROSS = W + "TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
RESIDUE = W + "RESIDUE_E2_GROSS.json"
TESTS_GROSS = W + "tests/test_tieout_e2_gross.py"
TESTS_RESIDUE = W + "tests/test_residue_e2_gross.py"
R17 = P + "0.9.0_WK_IRPT_DASHBD~12/TIEOUT_49F_BD_POPULATION_E2.json"
PLAN = P + "0.9.0_WK_IRPT_DASHBD~6/BD_POPULATION_PLAN_E3.json"
REASONS = {"FLOW_TIMING", "MISSING_PRICE", "INCOME_DATE", "COVERAGE_DAYS", "UNEXPLAINED"}
CLOSURE = "2025-01-09"


def _load(root, rel, fail):
    p = root / rel
    if not p.is_file():
        fail("no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def _key(s):
    seg = s.get("segment") or {}
    return (s.get("account"), seg.get("start"), seg.get("end"))


def _pytest(root, rel, words, fail):
    t = root / rel
    if not t.is_file():
        fail("no %s" % rel)
    src = t.read_bytes().decode("utf-8")
    for w in words:
        if w not in src:
            fail("tests never name %r" % w)
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
        print("%s FAIL" % (cid or "DB18"))
        sys.exit(1)

    if cid == "DB18-1-AC1":
        r = _load(root, GROSS, fail)
        plan = _load(root, PLAN, fail)
        want = sum(len(x.get("segments") or []) for x in plan.get("request_list") or [])
        c = r.get("counts") or {}
        if r.get("basis") != "GROSS":
            fail("basis %r" % r.get("basis"))
        if r.get("vendor_calls") != 0 or float(r.get("tolerance_pp", -1)) != 0.35:
            fail("vendor_calls %r tolerance_pp %r" % (r.get("vendor_calls"), r.get("tolerance_pp")))
        if c.get("segments_planned") != want or c.get("graded", -1) + c.get("not_gradable", -1) != want:
            fail("planned/graded/not_gradable do not reconcile to the plan's %d" % want)
        if c.get("within_tolerance", -1) + c.get("outside_tolerance", -1) != c.get("graded"):
            fail("within + outside != graded")
        segs = r.get("segments") or []
        graded = [s for s in segs if s.get("verdict") in ("WITHIN", "OUTSIDE")]
        if len(graded) != c.get("graded"):
            fail("%d graded rows, counts say %r" % (len(graded), c.get("graded")))
        miss = [s for s in graded if "bd_fee_addback" not in s or "bd_gross_return" not in s]
        if miss:
            fail("%d graded rows lack bd_fee_addback or bd_gross_return" % len(miss))
        bad = [s for s in segs if s.get("verdict") == "OUTSIDE" and s.get("reason") not in REASONS]
        if bad:
            fail("%d outside rows carry a reason outside the closed set" % len(bad))
        if [s for s in segs if s.get("verdict") == "NOT_GRADABLE" and not s.get("why")]:
            fail("a not_gradable row lacks a why")
        print("OK: GROSS basis; %d planned = %d graded + %d not gradable; %d within, %d outside" % (
            want, c["graded"], c["not_gradable"], c["within_tolerance"], c["outside_tolerance"]))
    elif cid == "DB18-1-AC2":
        r = _load(root, GROSS, fail)
        graded = [s for s in r.get("segments") or [] if s.get("verdict") in ("WITHIN", "OUTSIDE")]
        wrong = [s for s in graded
                 if (s.get("bd_fees_reported") in (None, 0, 0.0)) != (s.get("bd_fee_addback") is None)]
        if wrong:
            fail("%d rows where bd_fee_addback's nullness disagrees with bd_fees_reported" % len(wrong))
        n = _pytest(root, TESTS_GROSS, ("bd_fee_addback",), fail)
        nulls = sum(1 for s in graded if s.get("bd_fee_addback") is None)
        print("OK: addback null on %d of %d graded rows, exactly where BD reported no fee; %d tests passed" % (
            nulls, len(graded), n))
    elif cid == "DB18-1-AC3":
        r = _load(root, GROSS, fail)
        old = {_key(s): s.get("opal_return") for s in _load(root, R17, fail).get("segments") or []}
        segs = r.get("segments") or []
        keys = set(k for s in segs for k in s)
        netty = sorted(k for k in keys if "opal" in k.lower() and ("net" in k.lower() or "fee" in k.lower()))
        if netty:
            fail("segment keys name a net-of-fee Opal figure: %s" % netty)
        graded = [s for s in segs if s.get("verdict") in ("WITHIN", "OUTSIDE")]
        moved = [s for s in graded if old.get(_key(s)) != s.get("opal_return")]
        if moved:
            fail("%d graded rows carry an opal_return that differs from the round-17 record" % len(moved))
        print("OK: %d graded rows compare the served Opal figure unchanged; no net-of-fee Opal key" % len(graded))
    elif cid in ("DB18-2-AC1", "DB18-2-AC2"):
        g = _load(root, GROSS, fail)
        res = _load(root, RESIDUE, fail)
        graded = [s for s in g.get("segments") or [] if s.get("verdict") in ("WITHIN", "OUTSIDE")]
        unexp = {_key(s) for s in graded if s.get("verdict") == "OUTSIDE" and s.get("reason") == "UNEXPLAINED"}
        plus1 = {_key(s) for s in graded
                 if (s.get("bd_days_held") or 0) - (s.get("opal_days") or 0) == 1
                 and (s.get("segment") or {}).get("start", "9") <= CLOSURE <= (s.get("segment") or {}).get("end", "0")}
        c = res.get("counts") or {}
        if cid == "DB18-2-AC1":
            got = (c.get("denominator"), c.get("unexplained"), c.get("plus_one_day"), c.get("overlap"))
            exp = (len(graded), len(unexp), len(plus1), len(unexp & plus1))
            if got != exp:
                fail("counts (denominator, unexplained, plus_one_day, overlap) = %r, re-derived %r" % (got, exp))
            print("OK: denominator %d; unexplained %d; plus_one_day %d; overlap %d" % exp)
        else:
            rows = res.get("rows") or []
            union = unexp | plus1
            ks = [_key(x) for x in rows]
            if len(ks) != len(set(ks)) or set(ks) != union:
                fail("%d residue rows (%d distinct) against a union of %d" % (len(ks), len(set(ks)), len(union)))
            bad = [x for x in rows if x.get("reason") not in REASONS or not str(x.get("evidence") or "").strip()]
            if bad:
                fail("%d residue rows lack a closed-set reason or evidence" % len(bad))
            print("OK: %d residue rows, each with a closed-set reason and evidence" % len(rows))
    elif cid == "DB18-2-AC3":
        n = _pytest(root, TESTS_RESIDUE, ("overlap",), fail)
        print("OK: %d residue tests passed" % n)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
