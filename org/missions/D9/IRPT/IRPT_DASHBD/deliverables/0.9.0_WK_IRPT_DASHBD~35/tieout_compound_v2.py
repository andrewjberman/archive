"""TO-DB-b-57 (IRPT_DASHBD round 31, DB-b-57): the compounded tie-out of round 30 with ONE override -- the balance the fee add-back is
measured against. Round 30 forms add_back = fees / ((bmv + emv) / 2). When the balance moves through the segment (flows, an account
funded or drained part-way) that two-point average is not the average balance the fee was charged on. v2 uses the mean of the served
daily market_value_eod over the segment's linked days instead; the compounding itself (1 + net) * (1 + add_back) - 1 is round 30's,
imported unchanged (compound_gross). Everything else (not-gradable paths, reasons, tolerance, tally) is round 18's / round 17's, imported.
A segment with no fee, or with no positive daily value, keeps round 30's add-back.
READ-ONLY: S3 GETs/LISTs only; zero vendor calls.

Usage: python tieout_compound_v2.py <repo_root> [--cache <pickle>]      Writes TIEOUT_COMPOUND_V2.json beside this file.
"""
import importlib.util
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R30_PATH = HERE.parent / "0.9.0_WK_IRPT_DASHBD~34" / "tieout_compound.py"
_spec = importlib.util.spec_from_file_location("tieout_compound_r30", str(R30_PATH))
r30 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r30)
r18 = r30.r18
r17 = r30.r17
OUT_NAME = "TIEOUT_COMPOUND_V2.json"
TOLERANCE_PP = r30.TOLERANCE_PP


def daily_mean_value(days):
    """Mean of the positive served market_value_eod over the linked days; None when there is none."""
    mvs = [d["mv"] for d in days if d.get("mv") and d["mv"] > 0]
    return sum(mvs) / len(mvs) if mvs else None


def fee_addback_v2(bd, days):
    """(fees_reported, addback): fees / daily-mean value; round 30's add-back when there is no fee or no daily value."""
    fees = bd.get("fees")
    base = daily_mean_value(days)
    if not fees or base is None:
        return r18.fee_addback(bd)
    return fees, fees / base


def grade_segment(acct, seg, days, bd, tolerance_pp=TOLERANCE_PP):
    if days is None or not days or bd is None or bd.get("twr") is None:
        return r30.grade_segment(acct, seg, days, bd, tolerance_pp)       # not-gradable paths unchanged
    row = {"account": acct, "segment": {"start": seg["start"], "end": seg["end"]}}
    opal = r17.link([d["r"] for d in days])
    fees, add = fee_addback_v2(bd, days)
    gross = r30.compound_gross(bd["twr"], add)
    diff = abs(gross - opal) * 100.0
    row.update(bd_return=bd["twr"], opal_return=opal, opal_days=len(days), bd_days_held=bd.get("days_held"),
               bd_fees_reported=fees, bd_fee_addback=add, bd_gross_return=gross, abs_diff_pp=diff)
    if diff <= tolerance_pp:
        row["verdict"] = "WITHIN"
    else:
        row["verdict"] = "OUTSIDE"
        row["reason"], row["evidence"] = r17.explain(days, bd, gross, opal)
    return row


r18.grade_segment = grade_segment          # round 18's build() resolves grade_segment in its own globals at call time


def load(root, cache):
    plan = json.loads((root / r17.PLAN_REL).read_bytes().decode("utf-8"))
    if cache and Path(cache).is_file():
        with open(cache, "rb") as f:
            n_obj, bronze, gold, n_part, n_gold_accts = pickle.load(f)
    else:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", region_name="us-east-1", config=Config(
            read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))
        n_obj, bronze = r17.read_bronze(s3, [r["bd_account"] for r in plan["request_list"]])
        gold, n_part, n_gold_accts = r17.read_gold(s3, [r["account"] for r in plan["request_list"]])
        if cache:
            with open(cache, "wb") as f:
                pickle.dump((n_obj, bronze, gold, n_part, n_gold_accts), f)
    return plan, (n_obj, bronze, gold, n_part, n_gold_accts)


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    plan, (n_obj, bronze, gold, n_part, n_gold_accts) = load(root, cache)
    rows, planned = r18.build(plan, bronze, gold)
    graded = [x for x in rows if x["verdict"] in ("WITHIN", "OUTSIDE")]
    within = sum(1 for x in graded if x["abs_diff_pp"] <= TOLERANCE_PP)
    by_reason = {}
    for x in graded:
        if x["abs_diff_pp"] > TOLERANCE_PP:
            by_reason[x["reason"]] = by_reason.get(x["reason"], 0) + 1
    r30_rec = json.loads((HERE.parent / "0.9.0_WK_IRPT_DASHBD~34" / r30.OUT_NAME).read_bytes().decode("utf-8"))
    old_v = {(s["account"], s["segment"]["start"], s["segment"]["end"]): s["verdict"] for s in r30_rec["segments"]}
    moved = {"unchanged": 0, "OUTSIDE_to_WITHIN": 0, "WITHIN_to_OUTSIDE": 0}
    for x in graded:
        o, n = old_v[(x["account"], x["segment"]["start"], x["segment"]["end"])], x["verdict"]
        moved["unchanged" if o == n else "%s_to_%s" % (o, n)] += 1
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~35", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-57",
           "basis": "GROSS, COMPOUNDED, fee base = mean daily market_value_eod over the linked days",
           "tolerance_pp": TOLERANCE_PP, "vendor_calls": 0, "segments_planned": planned, "graded": len(graded),
           "within": within, "outside": len(graded) - within, "outside_by_reason": by_reason,
           "verdict_moves_vs_round30": moved, "segments": graded}
    (HERE / OUT_NAME).write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print("OK: planned %d graded %d within %d outside %d; moves vs round 30 %s" % (planned, len(graded), within, len(graded) - within, moved))


if __name__ == "__main__":
    main()
