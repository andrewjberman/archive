"""TO-DB-b-53 (IRPT_DASHBD round 30, DB-b-53, re-cut): the 49F tie-out re-graded with BD's gross formed by COMPOUNDING the fee add-back:
BD gross = (1 + bd_net_twr) * (1 + add_back) - 1, add_back = fees / ((bmv + emv) / 2) unchanged. Round 18 added it (net + add_back), which
omits the fee-times-return interaction over long positive periods (row IRPT_DASHBD-S35). Only the gross formation is overridden: round 18's
reader (tieout_e2_gross.py) and, through it, round 17's readers, reason logic and tally are imported and used as they are.
READ-ONLY: S3 GETs/LISTs only; zero vendor calls.

Usage: python tieout_compound.py <repo_root> [--cache <pickle>]
Writes TIEOUT_COMPOUND_E1.json beside this file.
"""
import importlib.util
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R18_PATH = HERE.parent / "0.9.0_WK_IRPT_DASHBD~13" / "tieout_e2_gross.py"
R18_REC_NAME = "TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
_spec = importlib.util.spec_from_file_location("tieout_e2_gross_r18", str(R18_PATH))
r18 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r18)
r17 = r18.r17
_r18_grade_segment = r18.grade_segment

OUT_NAME = "TIEOUT_COMPOUND_E1.json"
TOLERANCE_PP = r18.TOLERANCE_PP
REASONS = r18.REASONS


def compound_gross(net, add_back):
    """BD gross from BD net TWR: (1 + net) * (1 + add_back) - 1; a null add-back leaves the net as it is."""
    return net if add_back is None else (1.0 + net) * (1.0 + add_back) - 1.0


def additive_gross(net, add_back):
    """Round 18's formation (kept only so a test can show it does not chain)."""
    return net + (add_back if add_back is not None else 0.0)


def grade_segment(acct, seg, days, bd, tolerance_pp=TOLERANCE_PP):
    if days is None or not days or bd is None or bd.get("twr") is None:
        return _r18_grade_segment(acct, seg, days, bd, tolerance_pp)     # not-gradable paths are round 18's, unchanged
    row = {"account": acct, "segment": {"start": seg["start"], "end": seg["end"]}}
    opal = r17.link([d["r"] for d in days])
    fees, add = r18.fee_addback(bd)
    gross = compound_gross(bd["twr"], add)
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
    rows, planned = r18.build(plan, bronze, gold)
    graded = [x for x in rows if x["verdict"] in ("WITHIN", "OUTSIDE")]
    old = json.loads((HERE.parent / "0.9.0_WK_IRPT_DASHBD~13" / R18_REC_NAME).read_bytes().decode("utf-8"))
    before = {"within": old["counts"]["within_tolerance"], "outside": old["counts"]["outside_tolerance"]}
    within = sum(1 for x in graded if x["abs_diff_pp"] <= TOLERANCE_PP)
    outside = len(graded) - within
    by_reason = {}
    for x in graded:
        if x["abs_diff_pp"] > TOLERANCE_PP:
            by_reason[x["reason"]] = by_reason.get(x["reason"], 0) + 1
    # per-segment MATCH/DIFF against round 18's verdict (same key)
    old_v = {(s["account"], s["segment"]["start"], s["segment"]["end"]): s["verdict"] for s in old["segments"]}
    moved = {"OUTSIDE_to_WITHIN": 0, "WITHIN_to_OUTSIDE": 0, "unchanged": 0}
    for x in graded:
        o, n = old_v[(x["account"], x["segment"]["start"], x["segment"]["end"])], x["verdict"]
        moved["unchanged" if o == n else ("%s_to_%s" % (o, n))] += 1
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~34", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-53",
           "basis": "GROSS, COMPOUNDED: bd_gross = (1 + bd_net_twr) * (1 + fees/((bmv+emv)/2)) - 1; null add-back -> net as it is",
           "tolerance_pp": TOLERANCE_PP, "vendor_calls": 0, "segments_planned": planned,
           "before": before, "after": {"within": within, "outside": outside},
           "share_within_after": within / len(graded), "share_within_before": before["within"] / (before["within"] + before["outside"]),
           "after_outside_by_reason": by_reason, "before_outside_by_reason": old["counts"]["outside_by_reason"],
           "verdict_moves_vs_round18": moved, "reasons_closed_set": list(REASONS),
           "files_read": {"reader": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~13/tieout_e2_gross.py",
                          "round18_record": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~13/" + R18_REC_NAME,
                          "plan": r17.PLAN_REL,
                          "bronze_prefix": "s3://%s/%s" % (r17.BRONZE_BUCKET, r17.BRONZE_PREFIX), "bronze_object_count": n_obj,
                          "served_series": "s3://%s/%sdate=<YYYY-MM-DD>/data.parquet (%d partitions; column total_return_daily)" % (
                              r17.GOLD_BUCKET, r17.GOLD_PREFIX, n_part),
                          "served_accounts": n_gold_accts},
           "segments": graded}
    (HERE / OUT_NAME).write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print("OK: planned %d graded %d (before %d/%d -> after within %d outside %d) share %.4f" % (
        planned, len(graded), before["within"], before["outside"], within, outside, within / len(graded)))
    print(json.dumps({"by_reason": by_reason, "moves": moved}, indent=1))


if __name__ == "__main__":
    main()
