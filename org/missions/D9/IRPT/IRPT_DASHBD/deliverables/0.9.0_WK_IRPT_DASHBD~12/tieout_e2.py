"""TO-DB-b-26 (IRPT_DASHBD round 17, E2 / P-5): the 0.35 pp tie-out of the 49 Financial SERVED total return against Black Diamond's own
performancePeriod return, per account and per Opal gap-free segment. READ-ONLY: S3 GETs/LISTs only; zero vendor calls; no write but
the local record.

Usage: python tieout_e2.py <repo_root> [--cache <pickle>]
  Reads  (1) the plan BD_POPULATION_PLAN_E3.json (the segments and each account's bd id),
         (2) every landed BD response under the bronze prefix (the account-level dateRangePoints, one per planned range),
         (3) the served daily-TWR gold (s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/date=*/data.parquet,
             the table the Performance tab reads), linked geometrically over exactly the segment's days.
  Writes TIEOUT_49F_BD_POPULATION_E2.json beside this file.

Method (precedent TIEOUT_49F_BLACKDIAMOND_R1.md): Opal's link EXCLUDES days it withheld while BD covers its full daysHeld, so the
reading is per segment: COVERAGE_DAYS is assigned only on a named day-count excess. A reason is assigned only on evidence written in the
row's `evidence`; otherwise UNEXPLAINED.
"""
import io
import json
import math
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_NAME = "TIEOUT_49F_BD_POPULATION_E2.json"
PLAN_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~6/BD_POPULATION_PLAN_E3.json"
TOLERANCE_PP = 0.35
REASONS = ("FLOW_TIMING", "MISSING_PRICE", "INCOME_DATE", "COVERAGE_DAYS", "UNEXPLAINED")
BRONZE_BUCKET = "opal-data-assets"
BRONZE_PREFIX = "blackdiamond/49financial/bronze/reporting_performance/pull=20261004/"
GOLD_BUCKET = "opal-data-49financial"
GOLD_PREFIX = "irpt/49financial/gold/account_return_daily/"


# ----------------------------------------------------------------------------------------------------------------- pure grading
def link(returns):
    """Geometric link of daily returns: prod(1 + r) - 1."""
    p = 1.0
    for r in returns:
        p *= 1.0 + r
    return p - 1.0


def link_alt_flow(days, convention):
    """Re-link the segment from market value and external flow under another flow-timing convention.
    END (served): r = (V_t - F_t) / V_(t-1) - 1; START: r = V_t / (V_(t-1) + F_t) - 1; MID: r = (V_t - F_t/2) / (V_(t-1) + F_t/2) - 1.
    The first day of the segment has no in-segment prior value, so its served return is kept as it is."""
    p = 1.0
    for i, d in enumerate(days):
        if i == 0 or not d.get("mv") or not days[i - 1].get("mv") or d.get("flow") is None:
            p *= 1.0 + d["r"]
            continue
        v0, v1, f = days[i - 1]["mv"], d["mv"], d["flow"]
        if convention == "START":
            den = v0 + f
            r = v1 / den - 1.0 if den else d["r"]
        elif convention == "MID":
            den = v0 + f / 2.0
            r = (v1 - f / 2.0) / den - 1.0 if den else d["r"]
        else:
            r = (v1 - f) / v0 - 1.0
        p *= 1.0 + r
    return p - 1.0


def explain(days, bd, bd_ret, opal_ret):
    """(reason, evidence) for an OUTSIDE segment. Closed set; evidence is the number or flag that was read; else UNEXPLAINED."""
    n = len(days)
    held = bd.get("days_held")
    # COVERAGE_DAYS: BD counted days Opal's link did not (named day-count excess; one day is the start-day convention, not a withheld day)
    if isinstance(held, int) and abs(held - n) >= 2:
        return "COVERAGE_DAYS", "BD daysHeld %d vs Opal linked days %d (BD counted %d %s days than Opal linked)" % (
            held, n, abs(held - n), "more" if held > n else "fewer")
    # MISSING_PRICE: the served series itself flags days whose price return it could not source
    miss = [d for d in days if d.get("price_reason")]
    if miss:
        reasons = sorted(set(d["price_reason"] for d in miss))
        return "MISSING_PRICE", "%d of %d linked days carry holdings_price_return_reason %s" % (len(miss), n, ",".join(reasons))
    # FLOW_TIMING: a flow-bearing segment whose re-link under another flow convention lands within tolerance of BD
    flows = [d for d in days if d.get("flow")]
    if flows:
        best = None
        for conv in ("START", "MID"):
            alt = link_alt_flow(days, conv)
            diff = abs(bd_ret - alt) * 100.0
            if best is None or diff < best[1]:
                best = (conv, diff)
        if best[1] <= TOLERANCE_PP:
            return "FLOW_TIMING", "%d flow-bearing days; re-link under %s flow timing gives abs_diff %.4f pp (served END gives %.4f pp)" % (
                len(flows), best[0], best[1], abs(bd_ret - opal_ret) * 100.0)
    # INCOME_DATE: income days in the segment and the price-only link (income removed) lands within tolerance of BD
    inc = [d for d in days if d.get("inc")]
    if inc:
        px = link([d["r"] - d["inc"] for d in days])
        diff = abs(bd_ret - px) * 100.0
        if diff <= TOLERANCE_PP:
            return "INCOME_DATE", "%d income-bearing days; link with the income_return removed gives abs_diff %.4f pp (served gives %.4f pp)" % (
                len(inc), diff, abs(bd_ret - opal_ret) * 100.0)
    return "UNEXPLAINED", "no named evidence in the closed set: day counts BD %s vs Opal %d; %d flow days; %d income days; %d price-flag days%s" % (
        held, n, len(flows), len(inc), len(miss), fee_observation(bd, bd_ret, opal_ret))


def fee_observation(bd, bd_ret, opal_ret):
    """An OBSERVATION, not a reason (fees are not in the closed set): BD's request is NetOfFees and the served series carries no fee
    (fee_amount_reason FEE_RAIL_UNUSED). Reports whether Opal's link net of BD's own reported fees lands within tolerance of BD."""
    fees, b, e = bd.get("fees"), bd.get("bmv"), bd.get("emv")
    if not fees or b is None or e is None or (b + e) <= 0:
        return ""
    drag = fees / ((b + e) / 2.0)
    net = (1.0 + opal_ret) * (1.0 - drag) - 1.0
    diff = abs(bd_ret - net) * 100.0
    return "; OBSERVATION BD_FEES: BD reports fees %.2f = %.4f pp of average value; Opal net of that gives abs_diff %.4f pp%s" % (
        fees, drag * 100.0, diff, " (WITHIN tolerance)" if diff <= TOLERANCE_PP else "")


def grade_segment(acct, seg, days, bd, tolerance_pp=TOLERANCE_PP):
    """One row. `days` = the served daily rows inside the segment ([{date, r, mv, flow, inc, price_reason}], r not None), or None when the
    served series lacks the account; `bd` = {'twr': float|None, 'days_held': int|None} or None when BD's response held no point."""
    row = {"account": acct, "segment": {"start": seg["start"], "end": seg["end"]}}
    if days is None:
        row.update(bd_return=None, opal_return=None, abs_diff_pp=None, verdict="NOT_GRADABLE",
                   why="SERVED_SERIES_LACKS_ACCOUNT: the served series carries no rows for this account")
        return row
    if not days:
        row.update(bd_return=None, opal_return=None, abs_diff_pp=None, verdict="NOT_GRADABLE",
                   why="SERVED_SERIES_LACKS_SEGMENT: no served daily return inside the segment's dates")
        return row
    opal = link([d["r"] for d in days])
    if bd is None:
        row.update(bd_return=None, opal_return=opal, abs_diff_pp=None, verdict="NOT_GRADABLE",
                   why="BD_NO_RESPONSE: no landed Black Diamond response / no point for this range")
        return row
    if bd.get("twr") is None:
        row.update(bd_return=None, opal_return=opal, abs_diff_pp=None, verdict="NOT_GRADABLE",
                   why="BD_NO_VALUE: Black Diamond returned no time-weighted return for the range (%s)" % (
                       bd.get("note") or "daysHeld %s" % bd.get("days_held")))
        return row
    diff = abs(bd["twr"] - opal) * 100.0
    row.update(bd_return=bd["twr"], opal_return=opal, abs_diff_pp=diff, opal_days=len(days), bd_days_held=bd.get("days_held"))
    if diff <= tolerance_pp:
        row["verdict"] = "WITHIN"
    else:
        row["verdict"] = "OUTSIDE"
        row["reason"], row["evidence"] = explain(days, bd, bd["twr"], opal)
    return row


def tally(rows, planned):
    """Counts block. graded = WITHIN + OUTSIDE; not_gradable per why-code; outside per reason."""
    c = {"segments_planned": planned, "graded": 0, "not_gradable": 0, "within_tolerance": 0, "outside_tolerance": 0,
         "outside_by_reason": {r: 0 for r in REASONS}, "not_gradable_by_why": {}}
    for r in rows:
        v = r["verdict"]
        if v == "NOT_GRADABLE":
            c["not_gradable"] += 1
            k = r["why"].split(":", 1)[0]
            c["not_gradable_by_why"][k] = c["not_gradable_by_why"].get(k, 0) + 1
        else:
            c["graded"] += 1
            if v == "WITHIN":
                c["within_tolerance"] += 1
            else:
                c["outside_tolerance"] += 1
                c["outside_by_reason"][r["reason"]] += 1
                if r["reason"] == "UNEXPLAINED" and "BD_FEES" in r["evidence"] and "(WITHIN tolerance)" in r["evidence"]:
                    c["unexplained_consistent_with_bd_fees"] = c.get("unexplained_consistent_with_bd_fees", 0) + 1
    return c


# ----------------------------------------------------------------------------------------------------------------------- readers
def _num(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    return float(v)


def bd_points(resp, bd_account):
    """{(start, end): {'twr', 'days_held', 'note'}} from the account-level levels[] entry of a performancePeriod response."""
    out = {}
    for lv in resp.get("levels") or []:
        desc = lv.get("descriptor") or {}
        if desc.get("level") != "Account" or str(desc.get("levelId")) != str(bd_account):
            continue
        for p in lv.get("dateRangePoints") or []:
            dr = p.get("dateRange") or {}
            key = (str(dr.get("startDate"))[:10], str(dr.get("endDate"))[:10])
            t = p.get("timeWeightedReturns") or {}
            twr = _num(t.get("return"))
            held = p.get("daysHeld")
            note = None
            if twr is None:
                note = "no timeWeightedReturns.return; daysHeld %s, notHeldInPeriod %s" % (held, p.get("notHeldInPeriod"))
            elif held == 0 or p.get("notHeldInPeriod"):
                twr, note = None, "vendor-absent range: daysHeld %s, notHeldInPeriod %s" % (held, p.get("notHeldInPeriod"))
            out[key] = {"twr": twr, "days_held": held, "note": note, "fees": _num(p.get("fees")),
                        "bmv": _num(p.get("beginningMarketValue")), "emv": _num(p.get("endingMarketValue"))}
    return out


def read_bronze(s3, plan_accts):
    """(object_count, {bd_account: {(start,end): point} | 'UNPARSEABLE: ...'}) over every object under the bronze prefix."""
    from concurrent.futures import ThreadPoolExecutor
    keys = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BRONZE_BUCKET, Prefix=BRONZE_PREFIX):
        keys += [o["Key"] for o in p.get("Contents", [])]
    want = {str(a) for a in plan_accts}

    def one(k):
        acct = k.rsplit("acct=", 1)[1][:-5] if "acct=" in k and k.endswith(".json") else None
        if acct not in want:
            return acct, None
        body = None
        for attempt in range(6):
            try:
                body = s3.get_object(Bucket=BRONZE_BUCKET, Key=k)["Body"].read()
                break
            except Exception:
                if attempt == 5:
                    return acct, "UNPARSEABLE: S3 read failed"
        try:
            return acct, bd_points(json.loads(body.decode("utf-8")), acct)
        except Exception as e:
            return acct, "UNPARSEABLE: %s" % type(e).__name__

    with ThreadPoolExecutor(max_workers=16) as ex:
        res = list(ex.map(one, keys))
    return len(keys), {a: v for a, v in res if a is not None and v is not None}


def read_gold(s3, accounts):
    """({account: {date: row}}, partition_count, accounts_in_series) over every served partition."""
    import pyarrow.parquet as pq
    from concurrent.futures import ThreadPoolExecutor
    dates = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=GOLD_BUCKET, Prefix=GOLD_PREFIX, Delimiter="/"):
        for cp in p.get("CommonPrefixes", []):
            seg = cp["Prefix"].rstrip("/").rsplit("/", 1)[1]
            if seg.startswith("date="):
                dates.append(seg[5:])
    dates.sort()
    want = set(accounts)
    cols = ["account_id", "business_date", "market_value_eod", "external_flow", "income_return", "total_return_daily",
            "holdings_price_return_reason"]

    def one(d):
        for attempt in range(6):
            try:
                body = s3.get_object(Bucket=GOLD_BUCKET, Key="%sdate=%s/data.parquet" % (GOLD_PREFIX, d))["Body"].read()
                break
            except Exception:
                if attempt == 5:
                    raise
        return pq.read_table(io.BytesIO(body), columns=cols).to_pylist()

    out, seen = {}, set()
    with ThreadPoolExecutor(max_workers=8) as ex:
        for rows in ex.map(one, dates):
            for r in rows:
                seen.add(r["account_id"])
                if r["account_id"] in want:
                    out.setdefault(r["account_id"], {})[r["business_date"]] = {
                        "date": r["business_date"], "r": _num(r["total_return_daily"]), "mv": _num(r["market_value_eod"]),
                        "flow": _num(r["external_flow"]), "inc": _num(r["income_return"]) or 0.0,
                        "price_reason": r["holdings_price_return_reason"]}
    return out, len(dates), len(seen)


def segment_days(series, seg):
    """The served rows (non-null total return) whose business_date lies in [start, end], in date order; None when no series."""
    if not series:
        return None
    return [series[d] for d in sorted(series) if seg["start"] <= d <= seg["end"] and series[d]["r"] is not None]


# ---------------------------------------------------------------------------------------------------------------------------- run
def build(plan, bronze, gold):
    rows = []
    planned = 0
    for req in plan["request_list"]:
        a, bd_acct = req["account"], str(req["bd_account"])
        pts = bronze.get(bd_acct)
        for seg in req["segments"]:
            planned += 1
            bd = pts.get((seg["start"], seg["end"])) if isinstance(pts, dict) else None
            row = grade_segment(a, seg, segment_days(gold.get(a), seg), bd)
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
    plan = json.loads((root / PLAN_REL).read_bytes().decode("utf-8"))
    if cache and Path(cache).is_file():
        with open(cache, "rb") as f:
            n_obj, bronze, gold, n_part, n_gold_accts = pickle.load(f)
    else:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", region_name="us-east-1", config=Config(
            read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))
        n_obj, bronze = read_bronze(s3, [r["bd_account"] for r in plan["request_list"]])
        gold, n_part, n_gold_accts = read_gold(s3, [r["account"] for r in plan["request_list"]])
        if cache:
            with open(cache, "wb") as f:
                pickle.dump((n_obj, bronze, gold, n_part, n_gold_accts), f)
    rows, planned = build(plan, bronze, gold)
    counts = tally(rows, planned)
    # cross-check against the plan's own served link (read from the same gold when the plan was cut)
    plan_tw = {(r["account"], s["start"], s["end"]): s["opal_twr"] for r in plan["request_list"] for s in r["segments"]}
    counts["opal_link_differs_from_plan_opal_twr"] = sum(
        1 for x in rows if x["opal_return"] is not None and
        abs(x["opal_return"] - plan_tw[(x["account"], x["segment"]["start"], x["segment"]["end"])]) > 1e-9)
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~12", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-26",
           "tolerance_pp": TOLERANCE_PP, "vendor_calls": 0,
           "inputs": {"bronze_prefix": "s3://%s/%s" % (BRONZE_BUCKET, BRONZE_PREFIX), "bronze_object_count": n_obj,
                      "served_series": "s3://%s/%sdate=<YYYY-MM-DD>/data.parquet (%d partitions; column total_return_daily)" % (
                          GOLD_BUCKET, GOLD_PREFIX, n_part),
                      "served_accounts": n_gold_accts, "plan": PLAN_REL,
                      "plan_accounts_requested": len(plan["request_list"])},
           "counts": counts, "reasons_closed_set": list(REASONS), "segments": rows}
    (HERE / OUT_NAME).write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print("OK: planned %d graded %d (within %d, outside %d) not_gradable %d; objects %d, served accounts %d" % (
        planned, counts["graded"], counts["within_tolerance"], counts["outside_tolerance"], counts["not_gradable"], n_obj, n_gold_accts))
    print(json.dumps(counts, indent=1))


if __name__ == "__main__":
    main()
