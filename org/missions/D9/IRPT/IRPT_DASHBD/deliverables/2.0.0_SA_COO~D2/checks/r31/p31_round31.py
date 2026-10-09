"""IRPT_DASHBD round 31 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-30 analysis @4cfe197b0c (msg 1965): the compounded
tie-out (DB-b-53 re-cut, TIEOUT_COMPOUND_E1.json @1698740c8d, 7,459 of 9,078 within 0.35 pp) carries an unexplained regression and two
named residues. Populations are fixed by the two records and read here, never re-derived by a worker:
  E1 set   segments WITHIN in round 18's additive record and OUTSIDE (abs_diff_pp > 0.35) in the compounded record   (181 at issue)
  E2 set   compounded OUTSIDE rows with reason UNEXPLAINED                                                           (1,203 at issue)
  E3 set   compounded OUTSIDE rows with reason FLOW_TIMING                                                           (370 at issue)
A segment is keyed (account, segment.start, segment.end).

Usage: python <this file> <repo_root> <criterion_id>
  DB31-1-AC1  CROSSOVER_E1.json: `rows` cover exactly the E1 set, each {account, segment, cause_class, evidence} with a non-empty
              cause_class; `counts` equals the tally and sums to the set's size. Base: FAIL.
  DB31-1-AC2  `compounding_defect_classes` lists every class judged a compounding defect (may be empty); when it is non-empty,
              `fix` {file, after_within} is present and after_within >= 7,459; when it is empty, `fix` is null. Base: FAIL.
  DB31-2-AC1  UNEXPLAINED_CLASSES_E2.json: `rows` cover exactly the E2 set, each with a non-empty cause_class; `counts` equals the
              tally. Base: FAIL.
  DB31-2-AC2  `top_classes` is the smallest prefix of the classes by descending count whose cumulative count reaches 80% of the set
              (recomputed here); each top class carries `disposition` "fixed" or "named_cause". Base: FAIL.
  DB31-3-AC1  FLOW_TIMING_E3.json: `rows` cover exactly the E3 set, each {abs_diff_pp_flow_start, abs_diff_pp_flow_end, swing_pp}
              numeric with swing_pp == abs_diff_pp_flow_end - abs_diff_pp_flow_start (within 1e-9). Base: FAIL.
  DB31-3-AC2  `within_flow_start` and `within_flow_end` equal the row tallies at 0.35 pp, and `adopted` is null -- neither date is
              adopted by assumption (the analysis's E3). Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R18 = D + "0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
COMP = D + "0.9.0_WK_IRPT_DASHBD~34/TIEOUT_COMPOUND_E1.json"
E1 = D + "0.9.0_WK_IRPT_DASHBD~35/CROSSOVER_E1.json"
E2 = D + "0.9.0_WK_IRPT_DASHBD~36/UNEXPLAINED_CLASSES_E2.json"
E3 = D + "0.9.0_WK_IRPT_DASHBD~37/FLOW_TIMING_E3.json"
TOL = 0.35
WITHIN_FLOOR = 7459
SHARE = 0.80


def key(s):
    seg = s.get("segment") or {}
    return (s.get("account"), seg.get("start"), seg.get("end"))


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB31"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    a = {key(s): s for s in load(R18)["segments"]}
    c = {key(s): s for s in load(COMP)["segments"]}
    sets = {
        "1": {q for q, s in c.items() if s["abs_diff_pp"] > TOL and a.get(q, {}).get("verdict") == "WITHIN"},
        "2": {q for q, s in c.items() if s["abs_diff_pp"] > TOL and s.get("reason") == "UNEXPLAINED"},
        "3": {q for q, s in c.items() if s["abs_diff_pp"] > TOL and s.get("reason") == "FLOW_TIMING"},
    }
    rec = {"1": E1, "2": E2, "3": E3}
    cell = cid[5:6] if cid.startswith("DB31-") else ""
    if cell not in sets:
        fail("unknown criterion %r" % cid)
    want = sets[cell]
    r = load(rec[cell])
    rows = r.get("rows") or []
    if {key(x) for x in rows} != want or len(rows) != len(want):
        fail("%d rows; equal to the population of %d: %s" % (len(rows), len(want), {key(x) for x in rows} == want))

    if cell in ("1", "2"):
        if [x for x in rows if not str(x.get("cause_class") or "").strip()]:
            fail("a row without a cause_class")
        tally = {}
        for x in rows:
            tally[x["cause_class"]] = tally.get(x["cause_class"], 0) + 1
        if cid in ("DB31-1-AC1", "DB31-2-AC1"):
            if (r.get("counts") or {}) != tally:
                fail("counts %r, the tally %r" % (r.get("counts"), tally))
            print("OK: %d of %d classed into %d class(es): %s" % (len(rows), len(want), len(tally), tally))
        elif cid == "DB31-1-AC2":
            dc = r.get("compounding_defect_classes")
            if not isinstance(dc, list) or [k for k in dc if k not in tally]:
                fail("compounding_defect_classes %r must list classes present in the rows" % dc)
            fix = r.get("fix")
            if dc:
                if not isinstance(fix, dict) or not fix.get("file") or not isinstance(fix.get("after_within"), int) \
                        or fix["after_within"] < WITHIN_FLOOR:
                    fail("defect classes %r but fix %r (after_within must be >= %d)" % (dc, fix, WITHIN_FLOOR))
                print("OK: defect classes %s fixed in %s; within after the fix %d >= %d" % (dc, fix["file"], fix["after_within"], WITHIN_FLOOR))
            else:
                if fix is not None:
                    fail("no defect class but fix %r" % fix)
                print("OK: no class judged a compounding defect; the 181 are classed by cause")
        else:
            order = sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))
            need, run, top = SHARE * len(want), 0, []
            for k, v in order:
                if run >= need:
                    break
                top.append(k)
                run += v
            got = r.get("top_classes") or []
            names = [t.get("class") for t in got]
            if names != top:
                fail("top_classes %r; the recomputed smallest prefix to %.0f%% is %r" % (names, SHARE * 100, top))
            if [t for t in got if t.get("disposition") not in ("fixed", "named_cause")]:
                fail("a top class without disposition fixed / named_cause")
            print("OK: top %d class(es) cover %d of %d (%.1f%%): %s" % (len(top), run, len(want), 100.0 * run / len(want),
                                                                   {t["class"]: t["disposition"] for t in got}))
    else:
        if [x for x in rows if not all(num(x.get(k)) for k in ("abs_diff_pp_flow_start", "abs_diff_pp_flow_end", "swing_pp"))
                or abs(x["swing_pp"] - (x["abs_diff_pp_flow_end"] - x["abs_diff_pp_flow_start"])) > 1e-9]:
            fail("a row without numeric start/end/swing or with swing != end - start")
        if cid == "DB31-3-AC1":
            print("OK: %d of %d graded both ways; swing = end - start on every row" % (len(rows), len(want)))
        else:
            ws = sum(1 for x in rows if x["abs_diff_pp_flow_start"] <= TOL)
            we = sum(1 for x in rows if x["abs_diff_pp_flow_end"] <= TOL)
            if r.get("within_flow_start") != ws or r.get("within_flow_end") != we or r.get("adopted", "absent") is not None:
                fail("within_flow_start %r / end %r / adopted %r; tallies %d / %d, adopted must be null" % (
                    r.get("within_flow_start"), r.get("within_flow_end"), r.get("adopted", "absent"), ws, we))
            print("OK: of %d, within at flow-start %d, at flow-end %d; no date adopted" % (len(rows), ws, we))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
