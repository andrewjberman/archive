"""TO-DB-b-27 (IRPT_DASHBD round 18, DB-b-27): the E2 tie-out re-graded on ONE basis, GROSS of fees. The served 49F return is gross,
so Black Diamond's net figure is compared after adding back BD's own reported fee for the segment (fees / ((bmv + emv) / 2)).
A segment with no BD fee gets a null add-back and is compared as it is. No FEES reason; closed set unchanged. READ-ONLY, zero vendor calls.

Usage: python tieout_e2_gross.py <repo_root> [--cache <pickle>]
Writes TIEOUT_49F_BD_POPULATION_E2_GROSS.json beside this file. Reuses the round-17 readers and grading helpers unchanged.
"""
import importlib.util
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R17_PATH = HERE.parent / "0.9.0_WK_IRPT_DASHBD~12" / "tieout_e2.py"
_spec = importlib.util.spec_from_file_location("tieout_e2_r17", str(R17_PATH))
r17 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r17)
r17.fee_observation = lambda bd, bd_ret, opal_ret: ""   # the BD_FEES observation clause is dropped: the basis carries it

OUT_NAME = "TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
TOLERANCE_PP = r17.TOLERANCE_PP
REASONS = r17.REASONS


def fee_addback(bd):
    """(fees_reported, addback): addback = fees / ((bmv + emv) / 2); None when fees is None/zero or the average value is not positive."""
    fees, b, e = bd.get("fees"), bd.get("bmv"), bd.get("emv")
    if not fees or b is None or e is None or (b + e) <= 0:
        return fees, None
    return fees, fees / ((b + e) / 2.0)


def grade_segment(acct, seg, days, bd, tolerance_pp=TOLERANCE_PP):
    row = {"account": acct, "segment": {"start": seg["start"], "end": seg["end"]}}
    if days is None or not days or bd is None or bd.get("twr") is None:
        base = r17.grade_segment(acct, seg, days, bd, tolerance_pp)
        base.update(bd_fees_reported=None, bd_fee_addback=None, bd_gross_return=None)
        return base
    opal = r17.link([d["r"] for d in days])
    fees, add = fee_addback(bd)
    gross = bd["twr"] + (add if add is not None else 0.0)
    diff = abs(gross - opal) * 100.0
    row.update(bd_return=bd["twr"], opal_return=opal, opal_days=len(days), bd_days_held=bd.get("days_held"),
               bd_fees_reported=fees, bd_fee_addback=add, bd_gross_return=gross, abs_diff_pp=diff)
    if diff <= tolerance_pp:
        row["verdict"] = "WITHIN"
    else:
        row["verdict"] = "OUTSIDE"
        row["reason"], row["evidence"] = r17.explain(days, bd, gross, opal)
    return row


def build(plan, bronze, gold):
    rows = []
    planned = 0
    for req in plan["request_list"]:
        a, bd_acct = req["account"], str(req["bd_account"])
        pts = bronze.get(bd_acct)
        for seg in req["segments"]:
            planned += 1
            bd = pts.get((seg["start"], seg["end"])) if isinstance(pts, dict) else None
            row = grade_segment(a, seg, r17.segment_days(gold.get(a), seg), bd)
            if row["verdict"] == "NOT_GRADABLE" and row["why"].startswith("BD_NO_RESPONSE"):
                if isinstance(pts, str):
                    row["why"] = "BD_NO_RESPONSE: " + pts
                elif pts is None:
                    row["why"] = "BD_NO_RESPONSE: no landed object for bd account %s" % bd_acct
                else:
                    row["why"] = "BD_NO_RESPONSE: the landed response holds no account-level point for this range"
            rows.append(row)
    return rows, planned


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
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
    rows, planned = build(plan, bronze, gold)
    counts = r17.tally(rows, planned)
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~13", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-27",
           "basis": "GROSS", "tolerance_pp": TOLERANCE_PP, "vendor_calls": 0,
           "inputs": {"bronze_prefix": "s3://%s/%s" % (r17.BRONZE_BUCKET, r17.BRONZE_PREFIX), "bronze_object_count": n_obj,
                      "served_series": "s3://%s/%sdate=<YYYY-MM-DD>/data.parquet (%d partitions; column total_return_daily)" % (
                          r17.GOLD_BUCKET, r17.GOLD_PREFIX, n_part),
                      "served_accounts": n_gold_accts, "plan": r17.PLAN_REL,
                      "plan_accounts_requested": len(plan["request_list"])},
           "counts": counts, "reasons_closed_set": list(REASONS), "segments": rows}
    (HERE / OUT_NAME).write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print("OK: planned %d graded %d (within %d, outside %d) not_gradable %d" % (
        planned, counts["graded"], counts["within_tolerance"], counts["outside_tolerance"], counts["not_gradable"]))
    print(json.dumps(counts, indent=1))


if __name__ == "__main__":
    main()
