"""IRPT_DASHBD round 19 (workstream B, issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-18 analysis @62026ca511 as ruled in
msg 308: E1' tests a hypothesis about Black Diamond's day count on Opal's side (the 2,299 UNEXPLAINED segments spanning the
2025-01-09 NYSE closure); E2 reads the UNEXPLAINED segments that do not span it. Zero vendor calls; Opal's served figure never moves.

Usage: python <this file> <repo_root> <criterion_id>
  DB19-1-AC1  E1' record: one row per segment of CLOSURE = GROSS UNEXPLAINED rows that are +1-day over 2025-01-09 (re-derived here),
              each with opal_return_bd_convention, abs_diff_pp_bd_convention and verdict_bd_convention (WITHIN | OUTSIDE);
              counts.denominator == |CLOSURE| and counts.within_bd_convention == the WITHIN rows. Base: FAIL.
  DB19-1-AC2  the served figure is untouched: every row's opal_return equals the GROSS record's for that segment, and no key other
              than the three *_bd_convention keys carries a recomputed figure. Base: FAIL.
  DB19-1-AC3  the E1' tests pass (at least 4, naming 2025-01-09). Base: FAIL.
  DB19-2-AC1  E2 record: counts re-derived from the GROSS record -- denominator 9078, nonclosure == |UNEXPLAINED minus PLUS_ONE_DAY|,
              per-reason counts sum to nonclosure, final_unexplained == the UNEXPLAINED rows, share_of_graded printed. Base: FAIL.
  DB19-2-AC2  one row per NONCLOSURE segment, each with a closed-set reason and non-empty evidence. Base: FAIL.
  DB19-2-AC3  the E2 tests pass (at least 4, naming nonclosure). Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
GROSS = P + "0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
W1 = P + "0.9.0_WK_IRPT_DASHBD~14/"
W2 = P + "0.9.0_WK_IRPT_DASHBD~15/"
E1P = W1 + "CLOSURE_ALIGN_E1P.json"
E2R = W2 + "RESIDUE_NONCLOSURE_E2.json"
T1 = W1 + "tests/test_closure_align_e1p.py"
T2 = W2 + "tests/test_residue_nonclosure_e2.py"
REASONS = {"FLOW_TIMING", "MISSING_PRICE", "INCOME_DATE", "COVERAGE_DAYS", "UNEXPLAINED"}
CLOSURE_DAY = "2025-01-09"
BDC = {"opal_return_bd_convention", "abs_diff_pp_bd_convention", "verdict_bd_convention"}


def _load(root, rel, fail):
    p = root / rel
    if not p.is_file():
        fail("no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def _key(s):
    seg = s.get("segment") or {}
    return (s.get("account"), seg.get("start"), seg.get("end"))


def _sets(g):
    graded = [s for s in g.get("segments") or [] if s.get("verdict") in ("WITHIN", "OUTSIDE")]
    unexp = {_key(s) for s in graded if s.get("verdict") == "OUTSIDE" and s.get("reason") == "UNEXPLAINED"}
    plus1 = {_key(s) for s in graded
             if (s.get("bd_days_held") or 0) - (s.get("opal_days") or 0) == 1
             and (s.get("segment") or {}).get("start", "9") <= CLOSURE_DAY <= (s.get("segment") or {}).get("end", "0")}
    return graded, unexp, plus1


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
        print("%s FAIL" % (cid or "DB19"))
        sys.exit(1)

    if cid in ("DB19-1-AC1", "DB19-1-AC2"):
        rec = _load(root, E1P, fail)
        graded, unexp, plus1 = _sets(_load(root, GROSS, fail))
        closure = unexp & plus1
        rows = rec.get("rows") or []
        if cid == "DB19-1-AC1":
            ks = [_key(r) for r in rows]
            if len(ks) != len(set(ks)) or set(ks) != closure:
                fail("%d rows (%d distinct) against a closure set of %d" % (len(ks), len(set(ks)), len(closure)))
            bad = [r for r in rows if not BDC <= set(r) or r.get("verdict_bd_convention") not in ("WITHIN", "OUTSIDE")]
            if bad:
                fail("%d rows lack the bd_convention fields or a WITHIN/OUTSIDE verdict" % len(bad))
            c = rec.get("counts") or {}
            within = sum(1 for r in rows if r.get("verdict_bd_convention") == "WITHIN")
            if c.get("denominator") != len(closure) or c.get("within_bd_convention") != within:
                fail("counts %r; re-derived denominator %d, within %d" % (
                    {k: c.get(k) for k in ("denominator", "within_bd_convention")}, len(closure), within))
            print("OK: %d of %d closure segments land within 0.35 pp under BD's day-count convention" % (within, len(closure)))
        else:
            served = {_key(s): s.get("opal_return") for s in graded}
            moved = [r for r in rows if served.get(_key(r)) != r.get("opal_return")]
            if moved:
                fail("%d rows carry an opal_return that differs from the GROSS record" % len(moved))
            extra = sorted(k for r in rows for k in r if "opal" in k.lower() and k not in BDC and k != "opal_return")
            if extra:
                fail("recomputed Opal figure outside the *_bd_convention keys: %s" % sorted(set(extra))[:5])
            print("OK: %d rows keep the served opal_return; the recomputation lives only in *_bd_convention" % len(rows))
    elif cid == "DB19-1-AC3":
        print("OK: %d E1' tests passed" % _pytest(root, T1, CLOSURE_DAY, fail))
    elif cid in ("DB19-2-AC1", "DB19-2-AC2"):
        rec = _load(root, E2R, fail)
        graded, unexp, plus1 = _sets(_load(root, GROSS, fail))
        nonclosure = unexp - plus1
        rows = rec.get("rows") or []
        if cid == "DB19-2-AC1":
            c = rec.get("counts") or {}
            per = c.get("per_reason") or {}
            final = sum(1 for r in rows if r.get("reason") == "UNEXPLAINED")
            if c.get("denominator") != len(graded) or c.get("nonclosure") != len(nonclosure):
                fail("denominator %r / nonclosure %r; re-derived %d / %d" % (
                    c.get("denominator"), c.get("nonclosure"), len(graded), len(nonclosure)))
            if sum(per.values()) != len(nonclosure) or c.get("final_unexplained") != final:
                fail("per_reason sums to %d, final_unexplained %r vs %d rows" % (sum(per.values()), c.get("final_unexplained"), final))
            if c.get("share_of_graded") is None:
                fail("no share_of_graded")
            print("OK: nonclosure %d of %d graded; final UNEXPLAINED %d" % (len(nonclosure), len(graded), final))
        else:
            ks = [_key(r) for r in rows]
            if len(ks) != len(set(ks)) or set(ks) != nonclosure:
                fail("%d rows (%d distinct) against a nonclosure set of %d" % (len(ks), len(set(ks)), len(nonclosure)))
            bad = [r for r in rows if r.get("reason") not in REASONS or not str(r.get("evidence") or "").strip()]
            if bad:
                fail("%d rows lack a closed-set reason or evidence" % len(bad))
            print("OK: %d nonclosure rows, each with a closed-set reason and evidence" % len(rows))
    elif cid == "DB19-2-AC3":
        print("OK: %d E2 tests passed" % _pytest(root, T2, "nonclosure", fail))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
