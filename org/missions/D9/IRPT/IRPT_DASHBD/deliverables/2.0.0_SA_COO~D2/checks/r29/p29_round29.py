"""IRPT_DASHBD round 29 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-28 analysis @e9b17e6e75: E1 classes S34's 440
non-recomposing accounts, E2 shapes the right-half gap from Opal's side, E3 brings the lots stage to <= 750 s at full scale.

The populations are fixed by DB-b-49's record (TIEOUT_SPLIT_E1.json, merged @a556d87e79), read here, never re-derived by a worker:
  S34 set      rows whose recompose.within is false                         (440 at issue)
  E2 set       rows whose right.tied is false AND recompose.within is true  (1,528 at issue)
  control set  rows whose left.tied is true                                 (2,220 at issue)
Signed gap (pp) = (opal_return - bd_return) * 100 on the right half; its absolute value equals the record's abs_diff_pp.

Usage: python <this file> <repo_root> <criterion_id>
  DB29-1-AC1  S34_CLASS_E1.json: `rows` cover exactly the S34 set, each with one `cause_class` from the closed set
              {opened_or_closed_in_segment, fee_or_basis_between_pulls, missing_or_zero_half, full_period_annualized} or a string
              beginning "other:" naming the cause; `counts` per class equal the row tally and sum to the set's size. Base: FAIL.
  DB29-1-AC2  `outlier`: the S34 row with the largest recompose abs_diff_pp (724.16 pp at issue, within 0.01) traced with its three
              BD figures {bd_left, bd_right, bd_full} and `chained`, each numeric. Base: FAIL.
  DB29-1-AC3  `overlap` {right_misses, in_s34, outside_s34} equals this script's own count from DB-b-49's record. Base: FAIL.
  DB29-2-AC1  RIGHT_GAP_E2.json: `population` is exactly the E2 set; `gap_pp` {median, p10, p90} equals this script's recomputation
              from DB-b-49's signed gaps (within 0.01); `length_scaling` {corr_with_right_days} is numeric. Base: FAIL.
  DB29-2-AC2  `drivers` holds >= 3 Opal components from {external_flow, income_received, fee_amount, market_value_eod, day_quality,
              carried_days}, each {component, corr} with corr numeric; `top_driver` is the one with the largest |corr|. Base: FAIL.
  DB29-2-AC3  `control` is computed on exactly the control set with the same statistic for `top_driver`: {population_count, corr,
              signature_absent}; signature_absent == (|control corr| < |top corr| / 2), the rule stated here before the run. The
              verdict is printed, not graded. Base: FAIL.
  DB29-3-AC1  LOTS_750_E3.json: population_count >= 7,000 and accounts_run equal to it; lots_stage_completed true; >= 1 run whose
              total wall_seconds <= 750 with lots peak_mb printed; `chosen_batch_size` is that run's batch size. Base: FAIL.
  DB29-3-AC2  the producer's DEFAULT_BATCH_SIZE at HEAD equals chosen_batch_size; `default_run` (batch_size_arg null) reads total
              wall_seconds <= 750 with lots_stage_completed true; producer_sha256 and handler_sha256 equal HEAD's bytes. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
TIEOUT = D + "0.9.0_WK_IRPT_DASHBD~28/TIEOUT_SPLIT_E1.json"
E1 = D + "0.9.0_WK_IRPT_DASHBD~29/S34_CLASS_E1.json"
E2 = D + "0.9.0_WK_IRPT_DASHBD~30/RIGHT_GAP_E2.json"
E3 = D + "0.9.0_WK_IRPT_DASHBD~31/LOTS_750_E3.json"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py"
HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
CLASSES = {"opened_or_closed_in_segment", "fee_or_basis_between_pulls", "missing_or_zero_half", "full_period_annualized"}
COMPONENTS = {"external_flow", "income_received", "fee_amount", "market_value_eod", "day_quality", "carried_days"}
LIMIT_S = 750.0


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB29"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    rows = load(TIEOUT)["rows"]
    s34 = {x["account"] for x in rows if x["recompose"]["within"] is False}
    e2set = {x["account"] for x in rows if not x["right"]["tied"] and x["recompose"]["within"]}
    ctl = {x["account"] for x in rows if x["left"]["tied"]}
    misses = {x["account"] for x in rows if not x["right"]["tied"]}

    if cid == "DB29-1-AC1":
        r = load(E1)
        got = r.get("rows") or []
        if {x.get("account") for x in got} != s34 or len(got) != len(s34):
            fail("%d rows; equal to the S34 set of %d: %s" % (len(got), len(s34), {x.get("account") for x in got} == s34))
        tally = {}
        for x in got:
            c = str(x.get("cause_class") or "")
            if c not in CLASSES and not (c.startswith("other:") and len(c) > 6):
                fail("cause_class %r outside the closed set" % c)
            tally[c] = tally.get(c, 0) + 1
        counts = r.get("counts") or {}
        if counts != tally or sum(counts.values()) != len(s34):
            fail("counts %r against the row tally %r over %d" % (counts, tally, len(s34)))
        print("OK: %d of %d classed; %s" % (len(got), len(s34), tally))
    elif cid == "DB29-1-AC2":
        r = load(E1)
        top = max((x for x in rows if x["account"] in s34), key=lambda x: x["recompose"]["abs_diff_pp"])
        o = r.get("outlier") or {}
        if [k for k in ("bd_left", "bd_right", "bd_full", "chained") if not num(o.get(k))]:
            fail("outlier %r lacks a numeric figure" % o)
        if not num(o.get("abs_diff_pp")) or abs(o["abs_diff_pp"] - top["recompose"]["abs_diff_pp"]) > 0.01:
            fail("outlier abs_diff_pp %r, the record's largest is %.2f" % (o.get("abs_diff_pp"), top["recompose"]["abs_diff_pp"]))
        print("OK: outlier %.2f pp traced (left %s, right %s, full %s, chained %s)" % (
            o["abs_diff_pp"], o["bd_left"], o["bd_right"], o["bd_full"], o["chained"]))
    elif cid == "DB29-1-AC3":
        r = load(E1)
        want = {"right_misses": len(misses), "in_s34": len(misses & s34), "outside_s34": len(misses - s34)}
        ov = r.get("overlap") or {}
        if {k: ov.get(k) for k in want} != want:
            fail("overlap %r, DB-b-49's record gives %r" % (ov, want))
        print("OK: overlap %s" % want)
    elif cid in ("DB29-2-AC1", "DB29-2-AC2", "DB29-2-AC3"):
        r = load(E2)
        if cid == "DB29-2-AC1":
            pop = r.get("population") or []
            if set(pop) != e2set or len(pop) != len(e2set):
                fail("population of %d; equal to the E2 set of %d: %s" % (len(pop), len(e2set), set(pop) == e2set))
            gaps = [(x["right"]["opal_return"] - x["right"]["bd_return"]) * 100 for x in rows if x["account"] in e2set]
            want = {"median": statistics.median(gaps), "p10": pct(gaps, 0.10), "p90": pct(gaps, 0.90)}
            g = r.get("gap_pp") or {}
            if [k for k in want if not num(g.get(k)) or abs(g[k] - want[k]) > 0.01]:
                fail("gap_pp %r, recomputed %r" % (g, {k: round(v, 4) for k, v in want.items()}))
            ls = (r.get("length_scaling") or {}).get("corr_with_right_days")
            if not num(ls):
                fail("length_scaling.corr_with_right_days %r" % ls)
            print("OK: %d misses outside S34; gap pp median %.3f p10 %.3f p90 %.3f; corr with right-half days %.3f" % (
                len(pop), want["median"], want["p10"], want["p90"], ls))
        else:
            dr = r.get("drivers") or []
            comps = [x.get("component") for x in dr]
            if len(set(comps) & COMPONENTS) < 3 or [x for x in dr if not num(x.get("corr"))]:
                fail("drivers %r: need >= 3 named components with a numeric corr" % dr)
            best = max(dr, key=lambda x: abs(x["corr"]))
            if r.get("top_driver") != best["component"]:
                fail("top_driver %r, the largest |corr| is %r" % (r.get("top_driver"), best["component"]))
            if cid == "DB29-2-AC2":
                print("OK: top driver %s (corr %.3f) of %s" % (best["component"], best["corr"], comps))
            else:
                c = r.get("control") or {}
                if c.get("population_count") != len(ctl) or not num(c.get("corr")):
                    fail("control %r; the control set is %d" % (c, len(ctl)))
                rule = abs(c["corr"]) < abs(best["corr"]) / 2
                if c.get("signature_absent") is not rule:
                    fail("signature_absent %r, the stated rule gives %r" % (c.get("signature_absent"), rule))
                print("OK: control over %d left-half ties: %s corr %.3f vs %.3f; signature_absent %s (printed, not graded)" % (
                    len(ctl), best["component"], c["corr"], best["corr"], rule))
    elif cid in ("DB29-3-AC1", "DB29-3-AC2"):
        r = load(E3)
        pop, run = r.get("population_count"), r.get("accounts_run")
        if not isinstance(pop, int) or pop < 7000 or run != pop or r.get("lots_stage_completed") is not True:
            fail("population %r, accounts_run %r, lots_stage_completed %r" % (pop, run, r.get("lots_stage_completed")))
        if cid == "DB29-3-AC1":
            ok = [x for x in (r.get("runs") or []) if num((x.get("total") or {}).get("wall_seconds"))
                  and x["total"]["wall_seconds"] <= LIMIT_S and num((x.get("lots") or {}).get("peak_mb"))]
            pick = [x for x in ok if x.get("batch_size") == r.get("chosen_batch_size")]
            if not pick:
                fail("no run at chosen_batch_size %r with total <= %.0f s (runs under the limit: %d)" % (
                    r.get("chosen_batch_size"), LIMIT_S, len(ok)))
            x = pick[0]
            print("OK: %d accounts; batch %s total %.1f s, lots %.1f s, lots peak %.1f MB" % (
                pop, x["batch_size"], x["total"]["wall_seconds"], x["lots"]["wall_seconds"], x["lots"]["peak_mb"]))
        else:
            src = (root / PRODUCER).read_bytes()
            m = re.search(rb"^DEFAULT_BATCH_SIZE\s*=\s*(\d+)", src, re.M)
            if not m or int(m.group(1)) != r.get("chosen_batch_size"):
                fail("producer DEFAULT_BATCH_SIZE %r, chosen %r" % (m and int(m.group(1)), r.get("chosen_batch_size")))
            dr = r.get("default_run") or {}
            t = (dr.get("total") or {}).get("wall_seconds")
            if dr.get("batch_size_arg", "absent") is not None or not num(t) or t > LIMIT_S or dr.get("lots_stage_completed") is not True:
                fail("default_run %r" % dr)
            shas = {"producer_sha256": hashlib.sha256(src).hexdigest(),
                    "handler_sha256": hashlib.sha256((root / HANDLER).read_bytes()).hexdigest()}
            if [k for k in shas if r.get(k) != shas[k]]:
                fail("sha256 differs from HEAD's bytes: %r" % [k for k in shas if r.get(k) != shas[k]])
            print("OK: DEFAULT_BATCH_SIZE %s; default run total %.1f s <= %.0f; producer and handler bytes equal HEAD" % (
                m.group(1).decode(), t, LIMIT_S))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
