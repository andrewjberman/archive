"""TO-DB-b-51 (IRPT_DASHBD round 29, DB-b-51): the shape of the right-half gap for the E2 set, from Opal's side only, with a left-half
control. READ-ONLY: S3 GETs/LISTs on the served gold only; zero vendor calls. Populations are read from DB-b-49's record, never re-derived.
Round 18's served-series reader (tieout_e2_gross -> r17) is imported for the bucket/prefix, number coercion and the segment rule
(`r17.segment_days`); its read_gold fixes its column list, so this script reads the same partitions with the further columns it needs.

Usage: python right_gap_e2.py <repo_root> [--cache <pickle>]
Writes RIGHT_GAP_E2.json and RIGHT_GAP_E2.md beside this file. The .md is counts and statistics only.
"""
import importlib.util
import io
import json
import math
import pickle
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
_spec = importlib.util.spec_from_file_location("tieout_e2_gross_r18", str(D / "0.9.0_WK_IRPT_DASHBD~13" / "tieout_e2_gross.py"))
r18 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r18)
r17 = r18.r17
TIEOUT_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~28/TIEOUT_SPLIT_E1.json"
COLS = ["account_id", "business_date", "market_value_eod", "external_flow", "income_received", "total_return_daily", "fee_amount",
        "day_quality", "carried_days"]
COMPONENTS = ["external_flow", "income_received", "fee_amount", "market_value_eod", "day_quality", "carried_days"]
CLEAN = "MEASURED"


def read_gold(s3, accounts):
    import pyarrow.parquet as pq
    from concurrent.futures import ThreadPoolExecutor
    dates = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=r17.GOLD_BUCKET, Prefix=r17.GOLD_PREFIX, Delimiter="/"):
        for cp in p.get("CommonPrefixes", []):
            seg = cp["Prefix"].rstrip("/").rsplit("/", 1)[1]
            if seg.startswith("date="):
                dates.append(seg[5:])
    dates.sort()
    want = set(accounts)

    def one(d):
        for attempt in range(6):
            try:
                body = s3.get_object(Bucket=r17.GOLD_BUCKET, Key="%sdate=%s/data.parquet" % (r17.GOLD_PREFIX, d))["Body"].read()
                break
            except Exception:
                if attempt == 5:
                    raise
        return pq.read_table(io.BytesIO(body), columns=COLS).to_pylist()

    out = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for rows in ex.map(one, dates):
            for r in rows:
                if r["account_id"] in want:
                    out.setdefault(r["account_id"], {})[r["business_date"]] = {
                        "date": r["business_date"], "r": r17._num(r["total_return_daily"]), "mv": r17._num(r["market_value_eod"]),
                        "flow": r17._num(r["external_flow"]) or 0.0, "inc": r17._num(r["income_received"]) or 0.0,
                        "fee": r17._num(r["fee_amount"]) or 0.0, "dq": r["day_quality"], "carried": r["carried_days"] or 0}
    return out, dates


def pearson(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None and math.isfinite(x) and math.isfinite(y)]
    n = len(pairs)
    if n < 3:
        return None, n
    mx, my = sum(p[0] for p in pairs) / n, sum(p[1] for p in pairs) / n
    sxx = sum((p[0] - mx) ** 2 for p in pairs)
    syy = sum((p[1] - my) ** 2 for p in pairs)
    if sxx <= 0 or syy <= 0:
        return None, n
    return sum((p[0] - mx) * (p[1] - my) for p in pairs) / math.sqrt(sxx * syy), n


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def stats_for(series, seg):
    """Per-account component statistics over the range's served days (non-null total return), or None when no days."""
    days = r17.segment_days(series, seg)
    if not days:
        return None
    mv0 = days[0]["mv"]
    div = mv0 if mv0 and mv0 > 0 else None
    mvs = [d["mv"] for d in days if d["mv"] is not None]
    return {"external_flow": (sum(d["flow"] for d in days) / div) if div else None,
            "income_received": (sum(d["inc"] for d in days) / div) if div else None,
            "fee_amount": (sum(d["fee"] for d in days) / div) if div else None,
            "market_value_eod": (sum(mvs) / len(mvs)) if mvs else None,
            "day_quality": float(sum(1 for d in days if d["dq"] != CLEAN)),
            "carried_days": float(sum(d["carried"] for d in days)),
            "_days": len(days)}


def cal_days(seg):
    from datetime import date
    a, b = date.fromisoformat(seg["start"]), date.fromisoformat(seg["end"])
    return (b - a).days + 1


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    rec_in = json.loads((root / TIEOUT_REL).read_bytes().decode("utf-8"))
    rows = rec_in["rows"]
    e2 = [x for x in rows if not x["right"]["tied"] and x["recompose"]["within"]]
    ctl = [x for x in rows if x["left"]["tied"]]
    accts = sorted({x["account"] for x in e2} | {x["account"] for x in ctl})
    if cache and Path(cache).is_file():
        with open(cache, "rb") as f:
            gold, dates = pickle.load(f)
    else:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", region_name="us-east-1", config=Config(
            read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))
        gold, dates = read_gold(s3, accts)
        if cache:
            with open(cache, "wb") as f:
                pickle.dump((gold, dates), f)

    gaps = [(x["right"]["opal_return"] - x["right"]["bd_return"]) * 100.0 for x in e2]
    right_days = [float(cal_days(x["right"]["range"])) for x in e2]
    ls, ls_n = pearson(gaps, right_days)
    st = [stats_for(gold.get(x["account"]), x["right"]["range"]) for x in e2]
    drivers, undefined = [], []
    for c in COMPONENTS:
        corr, n = pearson([s[c] if s else None for s in st], gaps)
        if corr is None:
            undefined.append({"component": c, "corr": None, "n_accounts": n, "reason": "constant across the population (zero variance)"})
        else:
            drivers.append({"component": c, "corr": corr, "n_accounts": n})
    top = max(drivers, key=lambda d: abs(d["corr"]))
    tc = top["component"]
    cgaps = [(x["left"]["opal_return"] - x["left"]["bd_return"]) * 100.0 for x in ctl]
    cst = [stats_for(gold.get(x["account"]), x["left"]["range"]) for x in ctl]
    ccorr, cn = pearson([s[tc] if s else None for s in cst], cgaps)
    absent = abs(ccorr) < abs(top["corr"]) / 2
    dq_vals = {}
    for a in accts:
        for r in gold.get(a, {}).values():
            dq_vals[str(r["dq"])] = dq_vals.get(str(r["dq"]), 0) + 1
    out = {
        "measured_by": "0.9.0_WK_IRPT_DASHBD~30", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-51", "vendor_calls": 0,
        "population": [x["account"] for x in e2],
        "population_count": len(e2),
        "gap_pp": {"median": statistics.median(gaps), "p10": pct(gaps, 0.10), "p90": pct(gaps, 0.90), "n": len(gaps),
                   "definition": "(right.opal_return - right.bd_return) * 100 per E2 account; percentiles linear-interpolated",
                   "share_positive": sum(1 for g in gaps if g > 0) / len(gaps)},
        "length_scaling": {"corr_with_right_days": ls, "n": ls_n,
                           "right_days": "calendar days in right.range, inclusive (start..end)",
                           "right_days_median": statistics.median(right_days)},
        "drivers": drivers, "drivers_undefined": undefined, "top_driver": tc,
        "statistic": {
            "population": "E2 set: right.tied == false and recompose.within == true, from TIEOUT_SPLIT_E1.json",
            "window": "the right-half range; the account's served gold days in [start, end] with non-null total_return_daily",
            "external_flow": "sum(external_flow) / first-day market_value_eod",
            "income_received": "sum(income_received) / first-day market_value_eod",
            "fee_amount": "sum(fee_amount) / first-day market_value_eod",
            "market_value_eod": "mean(market_value_eod) over the window days",
            "day_quality": "count of window days whose day_quality is not %s" % CLEAN,
            "carried_days": "sum(carried_days) over the window days",
            "null_handling": "null external_flow / income_received / fee_amount count as 0",
            "first_day": "the first window day; a ratio is undefined (account excluded from that corr) when its market_value_eod is null or <= 0",
            "corr": "Pearson correlation of the per-account statistic with the signed gap (pp)",
            "day_quality_values_seen_in_series": dq_vals},
        "control": {"population_count": len(ctl), "component": tc, "corr": ccorr, "n_accounts_with_statistic": cn,
                    "top_corr": top["corr"],
                    "rule": "signature_absent = |control corr| < |top corr| / 2",
                    "signature_absent": absent,
                    "window": "the left-half range of each left.tied account; gap = (left.opal_return - left.bd_return) * 100"},
        "files_read": {"tieout_record": TIEOUT_REL,
                       "served_series": "s3://%s/%sdate=<YYYY-MM-DD>/data.parquet (%d partitions listed; columns %s)" % (
                           r17.GOLD_BUCKET, r17.GOLD_PREFIX, len(dates), ", ".join(COLS)),
                       "reader_imported": "0.9.0_WK_IRPT_DASHBD~13/tieout_e2_gross.py (r17 constants, _num, segment_days)",
                       "accounts_with_served_rows": len(gold), "accounts_requested": len(accts)}}
    (HERE / "RIGHT_GAP_E2.json").write_bytes((json.dumps(out, indent=1) + "\n").encode("utf-8"))
    g = out["gap_pp"]
    md = ["# RIGHT_GAP_E2 -- the shape of the right-half gap for the E2 set (counts and statistics only)", "",
          "Measured by 0.9.0_WK_IRPT_DASHBD~30 for TO-DB-b-51. Zero vendor calls; S3 reads of the served gold only.", "",
          "- E2 population: %d accounts (right.tied false, recompose.within true). Control population: %d left-half ties." % (len(e2), len(ctl)),
          "- Signed gap (pp), right half: median %.3f, p10 %.3f, p90 %.3f; share positive %.3f." % (g["median"], g["p10"], g["p90"], g["share_positive"]),
          "- Length scaling: Pearson corr of gap with right-half calendar days = %.3f (n %d; median %d days)." % (ls, ls_n, statistics.median(right_days)),
          "", "| component | corr with gap | n |", "|---|---|---|"]
    for d in drivers:
        md.append("| %s | %.3f | %d |" % (d["component"], d["corr"], d["n_accounts"]))
    for d in undefined:
        md.append("| %s | undefined (%s) | %d |" % (d["component"], d["reason"], d["n_accounts"]))
    md += ["", "- Top driver: %s (corr %.3f)." % (tc, top["corr"]),
           "- Control (%s over the %d left-half ties, n with statistic %d): corr %.3f; rule |control| < |top|/2; signature_absent = %s." % (
               tc, len(ctl), cn, ccorr, absent),
           "- day_quality values seen in the series for these accounts: %s; clean = %s." % (json.dumps(dq_vals, sort_keys=True), CLEAN),
           "- Statistic definitions are in RIGHT_GAP_E2.json `statistic`."]
    (HERE / "RIGHT_GAP_E2.md").write_bytes(("\n".join(md) + "\n").encode("utf-8"))
    print("OK: population %d control %d; gap median %.3f p10 %.3f p90 %.3f; len corr %.3f; top %s %.3f; control %.3f absent %s" % (
        len(e2), len(ctl), g["median"], g["p10"], g["p90"], ls, tc, top["corr"], ccorr, absent))
    print(json.dumps(drivers))
    print(dq_vals)


if __name__ == "__main__":
    main()
