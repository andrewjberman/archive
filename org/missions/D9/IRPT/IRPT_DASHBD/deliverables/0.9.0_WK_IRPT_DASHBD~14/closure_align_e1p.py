"""TO-DB-b-29 (IRPT_DASHBD round 19, E1'): does Black Diamond's day-count convention explain the 2025-01-09 closure-segment gap?

2025-01-09 was an NYSE closure. Opal's calendar is right and its served figure never moves. Black Diamond counts the day as held
(daysHeld = Opal linked days + 1). For each OUTSIDE/UNEXPLAINED GROSS segment with bd_days_held - opal_days == 1 that spans the day,
this recomputes Opal's return as if 2025-01-09 were a held day: the served linked return plus one day with zero price return that
carries the daily income accrual, graded against bd_gross_return at 0.35 pp.

Accrual column: `income_return` of the served gold series (the column the round-17 INCOME_DATE rule reads). Accrual on the closure day =
the mean of income_return over the segment's linked days (total income / linked days): income_return is lumpy on pay dates, so the
per-day accrual is its average; a segment with no income days carries 0.

Usage: python closure_align_e1p.py <repo_root>   (read-only: S3 list/get only; one local output file CLOSURE_ALIGN_E1P.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
GROSS_REL = P + "0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
TIEOUT_REL = P + "0.9.0_WK_IRPT_DASHBD~12/tieout_e2.py"
CLOSURE_DAY = "2025-01-09"
TOLERANCE_PP = 0.35
OUT_NAME = "CLOSURE_ALIGN_E1P.json"


def key(s):
    seg = s.get("segment") or {}
    return (s.get("account"), seg.get("start"), seg.get("end"))


def closure_set(gross):
    """UNEXPLAINED OUTSIDE segments with bd_days_held - opal_days == 1 spanning the closure day."""
    return [s for s in gross["segments"]
            if s.get("verdict") == "OUTSIDE" and s.get("reason") == "UNEXPLAINED"
            and (s.get("bd_days_held") or 0) - (s.get("opal_days") or 0) == 1
            and s["segment"]["start"] <= CLOSURE_DAY <= s["segment"]["end"]]


def accrual_on_closure_day(days):
    """Daily income accrual for the closure day: mean income_return over the segment's linked days (0 when none)."""
    if not days:
        return 0.0
    return sum(d.get("inc") or 0.0 for d in days) / len(days)


def recompute(opal_return, accrual):
    """Served linked return plus one closure day (zero price return, `accrual` income): (1+R)(1+a)-1."""
    return (1.0 + opal_return) * (1.0 + accrual) - 1.0


def align_row(seg, days):
    acc = accrual_on_closure_day(days)
    new = recompute(seg["opal_return"], acc)
    diff = abs(seg["bd_gross_return"] - new) * 100.0
    return {"account": seg["account"], "segment": seg["segment"], "bd_gross_return": seg["bd_gross_return"],
            "opal_return": seg["opal_return"], "opal_return_bd_convention": new, "abs_diff_pp_bd_convention": diff,
            "verdict_bd_convention": "WITHIN" if diff <= TOLERANCE_PP else "OUTSIDE", "accrual_on_closure_day": acc}


def tally(rows):
    w = sum(1 for r in rows if r["verdict_bd_convention"] == "WITHIN")
    return {"denominator": len(rows), "within_bd_convention": w, "outside_bd_convention": len(rows) - w}


def main():
    root = Path(sys.argv[1]).resolve()
    import importlib.util
    spec = importlib.util.spec_from_file_location("tieout_e2", str(root / TIEOUT_REL))
    t = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(t)
    import boto3
    from botocore.config import Config
    gross = json.loads((root / GROSS_REL).read_bytes().decode("utf-8"))
    cset = closure_set(gross)
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(
        read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))
    gold, n_part, _ = t.read_gold(s3, sorted({s["account"] for s in cset}))
    rows = [align_row(s, t.segment_days(gold.get(s["account"]), s["segment"])) for s in cset]
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~14", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-29",
           "tolerance_pp": TOLERANCE_PP, "vendor_calls": 0, "counts": tally(rows),
           "inputs": {"gross_record": GROSS_REL, "gold_prefix": "s3://%s/%s" % (t.GOLD_BUCKET, t.GOLD_PREFIX),
                      "gold_partitions": n_part, "accrual_column": "income_return (mean over the segment's linked days)"},
           "rows": rows}
    (HERE / OUT_NAME).write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print("OK: %s" % json.dumps(rec["counts"]))


if __name__ == "__main__":
    main()
