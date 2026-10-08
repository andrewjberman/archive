"""IRPT_DASHBD round 30 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-29 analysis @72ae174b3c as corrected by msg 1641
(E1 recast: the analysis's E1 was an identity, max |residual - recorded gap| 1.8e-12 over 1,527, 0 within 0.35 pp before any work).
The advisory-fee lead: Opal's served return is gross of advisory fees by design (account_return_daily.py, FEE-MANAGEMENT crosses the
account boundary as external flow), BD's is net. If the right-half gap is the fee, Opal's NET-basis gap equals the fee drag Opal itself
can measure.

Population (fixed by DB-b-49's record TIEOUT_SPLIT_E1.json, merged @a556d87e79): rows with right.tied false AND recompose.within true
(1,528 at issue). net_gap_pp = (right.opal_return - right.bd_net_return) * 100.

Usage: python <this file> <repo_root> <criterion_id>
  DB30-1-AC1  FEE_CENSUS_E2.json: `population` is exactly the population; `census.by_key` rows {key, partition, final_class, rows,
              amount} sum to `census.rows_total` and `census.amount_total` (amount within 0.01); every by_key final_class is one of
              FEE-MANAGEMENT / FEE-ADMIN. Base: FAIL.
  DB30-1-AC2  `classification` maps FEE-MANAGEMENT and FEE-ADMIN each to "external_flow" or "return", with `source_lines` [{file,
              line, text}] whose cited line at HEAD contains its quoted text (the check reads the bytes). Base: FAIL.
  DB30-1-AC3  `trace`: one account of the population, >= 1 fee day, each {business_date, fee_amount, served_external_flow,
              served_total_return_daily} numeric. Base: FAIL.
  DB30-2-AC1  FEE_DRAG_E1.json: `rows` cover exactly the population, each {account, net_gap_pp, fee_drag_pp, residual_pp, fee_days};
              net_gap_pp equals this script's recomputation from DB-b-49's record (within 1e-6); residual_pp == net_gap_pp -
              fee_drag_pp (within 1e-6); fee_drag_pp numeric and >= 0. Base: FAIL.
  DB30-2-AC2  `share_within` == count(|residual_pp| <= 0.35) / population, and `verdict` == CONFIRMED iff share_within >= 0.80, else
              REFUTED -- the rule stated here before the run. The verdict is printed, not graded. Base: FAIL.
  DB30-3-AC1  LOTS_P95_E3.json: population_count >= 7,000; >= 5 `runs` at one batch size equal to the producer's DEFAULT_BATCH_SIZE at
              HEAD, each with lots_stage_completed true and total wall_seconds numeric. Base: FAIL.
  DB30-3-AC2  the p95 of those runs' total wall_seconds (linear interpolation, computed here) is <= 750 s. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
TIEOUT = D + "0.9.0_WK_IRPT_DASHBD~28/TIEOUT_SPLIT_E1.json"
CENSUS = D + "0.9.0_WK_IRPT_DASHBD~32/FEE_CENSUS_E2.json"
DRAG = D + "0.9.0_WK_IRPT_DASHBD~32/FEE_DRAG_E1.json"
P95 = D + "0.9.0_WK_IRPT_DASHBD~33/LOTS_P95_E3.json"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_activity_lots.py"
FEE_CLASSES = ("FEE-MANAGEMENT", "FEE-ADMIN")
TREATMENTS = ("external_flow", "return")
TOL_PP = 0.35
CONFIRM_SHARE = 0.80
LIMIT_S = 750.0


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB30"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    rows = load(TIEOUT)["rows"]
    pop = {x["account"]: x["right"] for x in rows if not x["right"]["tied"] and x["recompose"]["within"]}

    if cid in ("DB30-1-AC1", "DB30-1-AC2", "DB30-1-AC3"):
        r = load(CENSUS)
        if cid == "DB30-1-AC1":
            got = r.get("population") or []
            if set(got) != set(pop) or len(got) != len(pop):
                fail("population of %d; equal to the %d: %s" % (len(got), len(pop), set(got) == set(pop)))
            c = r.get("census") or {}
            bk = c.get("by_key") or []
            if [x for x in bk if x.get("final_class") not in FEE_CLASSES or not isinstance(x.get("rows"), int) or not num(x.get("amount"))]:
                fail("a by_key row outside %s or without integer rows / numeric amount" % (FEE_CLASSES,))
            if not isinstance(c.get("rows_total"), int) or not num(c.get("amount_total")):
                fail("rows_total %r, amount_total %r" % (c.get("rows_total"), c.get("amount_total")))
            if sum(x["rows"] for x in bk) != c["rows_total"] or abs(sum(x["amount"] for x in bk) - c["amount_total"]) > 0.01:
                fail("by_key does not sum to the totals (%d rows, %.2f)" % (c["rows_total"], c["amount_total"]))
            print("OK: %d accounts; %d fee keys, %d rows, amount %.2f" % (len(got), len(bk), c["rows_total"], c["amount_total"]))
        elif cid == "DB30-1-AC2":
            cl = r.get("classification") or {}
            if [k for k in FEE_CLASSES if cl.get(k) not in TREATMENTS]:
                fail("classification %r: each of %s must be one of %s" % (cl, FEE_CLASSES, TREATMENTS))
            sl = r.get("source_lines") or []
            if not sl:
                fail("no source_lines")
            for s in sl:
                p = root / str(s.get("file") or "")
                if not p.is_file() or not isinstance(s.get("line"), int) or not str(s.get("text") or "").strip():
                    fail("source line %r unreadable" % s)
                lines = p.read_bytes().decode("utf-8").splitlines()
                if not 1 <= s["line"] <= len(lines) or s["text"] not in lines[s["line"] - 1]:
                    fail("%s:%s does not contain %r at HEAD" % (s["file"], s["line"], s["text"]))
            print("OK: %s; %d source line(s) verified at HEAD" % ({k: cl[k] for k in FEE_CLASSES}, len(sl)))
        else:
            t = r.get("trace") or {}
            days = t.get("fee_days") or []
            if t.get("account") not in pop or not days:
                fail("trace account in population: %s, fee days %d" % (t.get("account") in pop, len(days)))
            keys = ("fee_amount", "served_external_flow", "served_total_return_daily")
            if [d for d in days if not d.get("business_date") or [k for k in keys if not num(d.get(k))]]:
                fail("a traced fee day lacks a date or a numeric %s" % (keys,))
            print("OK: one account traced over %d fee day(s)" % len(days))
    elif cid in ("DB30-2-AC1", "DB30-2-AC2"):
        r = load(DRAG)
        got = r.get("rows") or []
        if {x.get("account") for x in got} != set(pop) or len(got) != len(pop):
            fail("%d rows; equal to the population of %d: %s" % (len(got), len(pop), {x.get("account") for x in got} == set(pop)))
        if cid == "DB30-2-AC1":
            bad = 0
            for x in got:
                want = (pop[x["account"]]["opal_return"] - pop[x["account"]]["bd_net_return"]) * 100
                if not all(num(x.get(k)) for k in ("net_gap_pp", "fee_drag_pp", "residual_pp")) or x["fee_drag_pp"] < 0 \
                        or abs(x["net_gap_pp"] - want) > 1e-6 or abs(x["residual_pp"] - (x["net_gap_pp"] - x["fee_drag_pp"])) > 1e-6 \
                        or not isinstance(x.get("fee_days"), int):
                    bad += 1
            if bad:
                fail("%d rows off the arithmetic (net gap from DB-b-49, residual = net gap - drag, drag >= 0, fee_days int)" % bad)
            print("OK: %d rows; net gap recomputed, residual = net gap - fee drag on every row" % len(got))
        else:
            within = sum(1 for x in got if abs(x["residual_pp"]) <= TOL_PP)
            share = within / len(pop)
            want = "CONFIRMED" if share >= CONFIRM_SHARE else "REFUTED"
            if not num(r.get("share_within")) or abs(r["share_within"] - share) > 1e-9 or r.get("verdict") != want:
                fail("share_within %r verdict %r; recomputed %.4f -> %s" % (r.get("share_within"), r.get("verdict"), share, want))
            print("OK: %d of %d within %.2f pp (share %.4f); verdict %s (rule: CONFIRMED iff >= %.2f; printed, not graded)" % (
                within, len(pop), TOL_PP, share, want, CONFIRM_SHARE))
    elif cid in ("DB30-3-AC1", "DB30-3-AC2"):
        r = load(P95)
        m = re.search(rb"^DEFAULT_BATCH_SIZE\s*=\s*(\d+)", (root / PRODUCER).read_bytes(), re.M)
        size = int(m.group(1)) if m else None
        runs = [x for x in (r.get("runs") or []) if x.get("batch_size") == size and x.get("lots_stage_completed") is True
                and num((x.get("total") or {}).get("wall_seconds"))]
        if not isinstance(r.get("population_count"), int) or r["population_count"] < 7000 or len(runs) < 5:
            fail("population %r; %d completed runs at DEFAULT_BATCH_SIZE %r (need >= 5)" % (r.get("population_count"), len(runs), size))
        ts = [x["total"]["wall_seconds"] for x in runs]
        if cid == "DB30-3-AC1":
            print("OK: %d runs at batch %s over %d accounts; totals %s" % (len(runs), size, r["population_count"], [round(t, 1) for t in ts]))
        else:
            p = pct(ts, 0.95)
            if p > LIMIT_S:
                fail("p95 total %.1f s > %.0f over %d runs at batch %s" % (p, LIMIT_S, len(runs), size))
            print("OK: p95 total %.1f s <= %.0f over %d runs at batch %s (max %.1f)" % (p, LIMIT_S, len(runs), size, max(ts)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
