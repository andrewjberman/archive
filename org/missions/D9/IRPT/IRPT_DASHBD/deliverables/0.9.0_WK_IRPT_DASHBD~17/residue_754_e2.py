"""TO-DB-b-32 (IRPT_DASHBD round 20, DB-b-32): re-read the 754 round-19 UNEXPLAINED nonclosure segments with Opal's served daily series.
READ-ONLY: S3 list/get only; zero vendor calls. Applies the round-17 rules (tieout_e2.explain) against BD's GROSS figure.
Usage: python residue_754_e2.py <repo_root> [--cache <pickle>]   Writes RESIDUE_754_E2.json beside this file.
"""
import importlib.util
import json
import pickle
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parent
REASONS = ("FLOW_TIMING", "MISSING_PRICE", "INCOME_DATE", "COVERAGE_DAYS", "UNEXPLAINED")
R19 = P / "0.9.0_WK_IRPT_DASHBD~15" / "RESIDUE_NONCLOSURE_E2.json"
GROSS = P / "0.9.0_WK_IRPT_DASHBD~13" / "TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
R17 = P / "0.9.0_WK_IRPT_DASHBD~12" / "tieout_e2.py"


def load_r17():
    spec = importlib.util.spec_from_file_location("tieout_e2_r17", str(R17))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def key(a, seg):
    return (a, seg["start"], seg["end"])


def residue_set(r19):
    return [r for r in r19.get("rows") or [] if r.get("reason") == "UNEXPLAINED"]


def grade_residue(r17, g, days):
    """One residue row from the GROSS record segment `g` and the served days (None/[] = series lacks the segment)."""
    if not days:
        return "UNEXPLAINED", "served series carries no daily return inside the segment's dates; nothing to test"
    gross = g.get("bd_gross_return")
    if gross is None:
        return "UNEXPLAINED", "no BD gross figure for the segment"
    opal = r17.link([d["r"] for d in days])
    bd = {"days_held": g.get("bd_days_held"), "fees": g.get("bd_fees_reported"), "bmv": None, "emv": None}
    reason, ev = r17.explain(days, bd, gross, opal)
    return reason, "[opal side, %d served days] %s" % (len(days), ev)


def build(r19, gross, gold):
    r17 = load_r17()
    gm = {key(s["account"], s["segment"]): s for s in gross.get("segments") or []}
    rows = []
    for r in residue_set(r19):
        k = key(r["account"], r["segment"])
        g = gm[k]
        series = gold.get(r["account"])
        days = r17.segment_days(series, r["segment"])
        reason, ev = grade_residue(r17, g, days)
        rows.append({"account": r["account"], "segment": r["segment"], "reason": reason, "evidence": ev})
    per = Counter(x["reason"] for x in rows)
    counts = {"denominator": len(rows), "per_reason": {k: per.get(k, 0) for k in REASONS}, "final_unexplained": per.get("UNEXPLAINED", 0)}
    return {"task_order": "IRPT_DASHBD.TO-DB-b-32", "measured_by": "0.9.0_WK_IRPT_DASHBD~17", "claim": "measured",
            "vendor_calls": 0, "basis": "GROSS", "reasons_closed_set": list(REASONS), "counts": counts, "rows": rows}


def main(argv):
    r19 = json.loads(R19.read_bytes().decode("utf-8"))
    gross = json.loads(GROSS.read_bytes().decode("utf-8"))
    accts = sorted({r["account"] for r in residue_set(r19)})
    cache = argv[argv.index("--cache") + 1] if "--cache" in argv else None
    if cache and Path(cache).is_file():
        with open(cache, "rb") as f:
            gold = pickle.load(f)
    else:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", region_name="us-east-1", config=Config(
            read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))
        gold = load_r17().read_gold(s3, accts)[0]
        if cache:
            with open(cache, "wb") as f:
                pickle.dump(gold, f)
    rec = build(r19, gross, gold)
    (HERE / "RESIDUE_754_E2.json").write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print(json.dumps(rec["counts"]))


if __name__ == "__main__":
    main(sys.argv[1:])
