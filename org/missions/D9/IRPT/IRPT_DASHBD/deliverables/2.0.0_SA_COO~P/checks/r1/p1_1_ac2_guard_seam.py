"""IRPT_DASHBD round 1 AC (DB-b-1, FWD-8 C-GUARD / C-VALUE) -- the seam against the REAL neighbour, and the guard as PRD v0.4
rulings 17-19 state it: the guard never substitutes, it grades only inside the comparability domain, and the EMITTED value is the
value checked. Rewritten counterexample-first (TO-DB-b-1 issuer amendment 5 (i); rows IRPT_DASHBD-S5, S6 limb d, S7).

Usage: python p1_1_ac2_guard_seam.py <worktree root>
       python p1_1_ac2_guard_seam.py --self-test        (no AWS: the counterexamples below must each FAIL, the good rows PASS)

On S3 through lib.opal_naming.address(): reads dim_return_method/method_version=1 (tolerance, plausibility_band_low/high,
comparability_max_excluded_weight), then 40 evenly spaced date partitions of account_return_daily, each with the partition before
it (for V_(t-1)) and IRPT_BCKEND's holdings_performance_daily partition of the same date. Every sampled row is graded by
`grade_row`, which is the whole rule and is what --self-test exercises:

  SEAM       holdings_price_return equals the holdings gold daily_return (1e-12) where that row is OK; where no OK holdings row
             exists it is null AND holdings_price_return_reason is not.
  NEVER      return_basis HOLDINGS_INCOME_FALLBACK appears on no row (ruling 17).
  EMITTED    a non-null total_return_daily is finite and inside the plausibility band; a null one carries return_basis
             NOT_MEASURABLE, and NOT_MEASURABLE carries a null (ruling 19: the band is on the value that is emitted).
  DOMAIN     the comparability domain is RECOMPUTED here from the holdings row (status OK, not leveraged, no negative value,
             excluded_weight at or below the method row's ceiling), never read from the row's own claim.
  GRADED     in the domain: MEASURED means |total - (price + income)| <= tolerance; a difference above it means FLOW_UNRECONCILED.
  NOT GRADED outside the domain or with no comparison return: MEASURED means |F_t| / V_(t-1) <= tolerance (ruling 18). A null
             comparison return is NEVER read as 0.0.
  UNRECONCILED  FLOW_UNRECONCILED carries a null total_return_daily and return_basis NOT_MEASURABLE (ruling 17).
  VALUE      market_value_eod > 0 on every MEASURED day (C-VALUE).

NOT graded here, and said so: that the holdings return and the adapter span the same valuation interval (the fifth domain
member); the row carries no column this check can recompute it from.
Denominators printed: partitions sampled, rows checked, rows per day_quality, rows graded in and out of the domain.
Pass line: DB-1-AC2 PASS. Base (at the cut): FAIL -- the adapter's gold does not exist.
"""
import io
import math
import sys
from pathlib import Path


def _num(value):
    """A finite float, or None. Never a default: a null stays a null."""
    if value is None:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return float("nan")
    return out


def in_domain(hold, max_excluded_weight):
    """The comparability domain, recomputed from the holdings gold row (ruling 18)."""
    if hold is None or hold.get("status") != "OK":
        return False
    if hold.get("leveraged") or hold.get("negative_value"):
        return False
    ew = _num(hold.get("excluded_weight"))
    if ew is None or math.isnan(ew) or ew > max_excluded_weight:
        return False
    return hold.get("daily_return") is not None


def grade_row(row, hold, prior_value, method):
    """Every way one emitted account-day can be wrong. Returns a list of sentences; empty = the row holds."""
    out = []
    tol = float(method["tolerance"])
    lo, hi = float(method["plausibility_band_low"]), float(method["plausibility_band_high"])
    quality, basis = row.get("day_quality"), row.get("return_basis")
    total = _num(row.get("total_return_daily"))
    hpr = _num(row.get("holdings_price_return"))
    income = _num(row.get("income_return"))

    if hold is not None and hold.get("status") == "OK":
        want = _num(hold.get("daily_return"))
        if hpr is None or want is None or math.isnan(hpr) or abs(hpr - want) > 1e-12:
            out.append("holdings_price_return %r != holdings gold daily_return %r" % (row.get("holdings_price_return"), hold.get("daily_return")))
    else:
        if hpr is not None:
            out.append("holdings_price_return %r with no OK holdings row" % row.get("holdings_price_return"))
        if row.get("holdings_price_return_reason") is None:
            out.append("no OK holdings row and no holdings_price_return_reason")

    if basis == "HOLDINGS_INCOME_FALLBACK":
        out.append("return_basis HOLDINGS_INCOME_FALLBACK is never emitted (PRD v0.4 ruling 17)")
    if total is None:
        if basis != "NOT_MEASURABLE":
            out.append("null total_return_daily with return_basis %r" % basis)
    else:
        if basis == "NOT_MEASURABLE":
            out.append("return_basis NOT_MEASURABLE carries a number %r" % total)
        if math.isnan(total) or math.isinf(total):
            out.append("total_return_daily is not finite: %r" % row.get("total_return_daily"))
        elif total < lo or total > hi:
            out.append("emitted total_return_daily %.6g is outside the plausibility band [%.6g, %.6g]" % (total, lo, hi))

    if quality == "FLOW_UNRECONCILED" and total is not None:
        out.append("FLOW_UNRECONCILED carries a number %r (ruling 17: null, the link breaks)" % total)

    graded = in_domain(hold, float(method["comparability_max_excluded_weight"])) and hpr is not None and not math.isnan(hpr)
    if quality == "MEASURED":
        mv = _num(row.get("market_value_eod"))
        if mv is None or math.isnan(mv) or mv <= 0:
            out.append("MEASURED with market_value_eod %r" % row.get("market_value_eod"))
        if total is None or math.isnan(total):
            out.append("MEASURED with no usable total_return_daily")
        elif graded:
            if income is None or math.isnan(income):
                out.append("MEASURED and graded, but income_return is %r" % row.get("income_return"))
            elif abs(total - (hpr + income)) > tol:
                out.append("MEASURED inside the comparability domain but |total - (price + income)| = %.6g > tolerance %.6g"
                           % (abs(total - (hpr + income)), tol))
        else:
            flow = _num(row.get("external_flow"))
            if prior_value is None or prior_value <= 0:
                out.append("MEASURED, not graded by the guard, and no positive prior value to bound the flow by")
            elif flow is None or math.isnan(flow):
                out.append("MEASURED, not graded by the guard, and external_flow is %r" % row.get("external_flow"))
            elif abs(flow) / prior_value > tol:
                out.append("MEASURED though the guard did not grade the day and |F_t| / V_(t-1) = %.6g > tolerance %.6g (ruling 18)"
                           % (abs(flow) / prior_value, tol))
    return out, graded


def self_test():
    method = {"tolerance": 0.001, "plausibility_band_low": -0.5, "plausibility_band_high": 0.5,
              "comparability_max_excluded_weight": 0.05}
    ok_hold = {"status": "OK", "daily_return": 0.004, "excluded_weight": 0.01, "leveraged": False, "negative_value": False}
    wide_hold = dict(ok_hold, excluded_weight=0.9)
    base = {"day_quality": "MEASURED", "return_basis": "TWR", "total_return_daily": 0.0045, "holdings_price_return": 0.004,
            "holdings_price_return_reason": None, "income_return": 0.0005, "external_flow": 0.0, "market_value_eod": 100000.0}
    cases = [
        ("good: graded and agreeing", base, ok_hold, 100000.0, False),
        ("good: guard disagreement emitted as null / NOT_MEASURABLE",
         dict(base, day_quality="FLOW_UNRECONCILED", return_basis="NOT_MEASURABLE", total_return_daily=None), ok_hold, 100000.0, False),
        ("good: outside the domain, tiny flow, MEASURED", dict(base, total_return_daily=0.03, external_flow=50.0), wide_hold, 100000.0, False),
        ("good: no holdings row, reason stated, no flow",
         dict(base, holdings_price_return=None, holdings_price_return_reason="NO_HOLDINGS_ROW"), None, 100000.0, False),
        ("COUNTER: an emitted +60% against a +/-50% band (review finding; the old check passed it)",
         dict(base, day_quality="FLOW_UNRECONCILED", return_basis="HOLDINGS_INCOME_FALLBACK", total_return_daily=0.60), ok_hold, 100000.0, True),
        ("COUNTER: MEASURED with a null comparison return and a 5% flow (the old check read the null as 0.0)",
         dict(base, holdings_price_return=None, holdings_price_return_reason="NO_HOLDINGS_ROW", total_return_daily=0.0003,
              external_flow=5000.0), None, 100000.0, True),
        ("COUNTER: FLOW_UNRECONCILED still carrying a number",
         dict(base, day_quality="FLOW_UNRECONCILED", return_basis="NOT_MEASURABLE", total_return_daily=0.02), ok_hold, 100000.0, True),
        ("COUNTER: a non-finite emitted value on a MEASURED day", dict(base, total_return_daily=float("nan")), ok_hold, 100000.0, True),
        ("COUNTER: graded, MEASURED, and 4.5 points from price plus income", dict(base, total_return_daily=0.0495), ok_hold, 100000.0, True),
        ("COUNTER: outside the domain (excluded weight 0.9), MEASURED, with a 5% flow",
         dict(base, total_return_daily=0.03, external_flow=5000.0), wide_hold, 100000.0, True),
        ("COUNTER: the adapter's price return differs from the neighbour's", dict(base, holdings_price_return=0.0041), ok_hold, 100000.0, True),
    ]
    bad = 0
    for name, row, hold, prior, must_fail in cases:
        failures, _graded = grade_row(row, hold, prior, method)
        verdict = bool(failures) == must_fail
        bad += not verdict
        print("  %s %-96s -> %s" % ("ok " if verdict else "BAD", name, failures[0] if failures else "holds"))
    print("SELF-TEST %s: %d of %d cases behave as declared (%d counterexamples must fail, %d good rows must hold)"
          % ("PASS" if not bad else "FAIL", len(cases) - bad, len(cases), sum(c[4] for c in cases), sum(not c[4] for c in cases)))
    return 1 if bad else 0


def fail(msg):
    print("DB-1-AC2 FAIL: " + msg)
    sys.exit(1)


def main(root):
    sys.path.insert(0, str(root))
    from lib import opal_naming as on
    import boto3
    import pyarrow.parquet as pq

    s3 = boto3.client("s3", region_name="us-east-1")

    def split(uri):
        bucket, key = uri[5:].split("/", 1)
        return bucket, key

    def read(uri):
        bucket, key = split(uri)
        return pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=key)["Body"].read())).to_pylist()

    try:
        method = read(on.address("irpt", "49financial", "gold", "dim_return_method", "method_version=1") + "/data.parquet")[0]
    except Exception as exc:  # noqa: BLE001
        fail("dim_return_method/method_version=1 unreadable: %s" % str(exc)[:120])
    for col in ("tolerance", "plausibility_band_low", "plausibility_band_high", "comparability_max_excluded_weight"):
        if method.get(col) is None:
            fail("dim_return_method lacks %s (ruling 18: the domain's bounds are written beside the tolerance)" % col)

    bucket, k0 = split(on.address("irpt", "49financial", "gold", "account_return_daily", "date=2000-01-01"))
    prefix = k0.rsplit("date=2000-01-01", 1)[0]
    pag = s3.get_paginator("list_objects_v2")
    dates = sorted({k.split("date=")[1][:10] for page in pag.paginate(Bucket=bucket, Prefix=prefix)
                    for k in [o["Key"] for o in page.get("Contents", [])] if "date=" in k})
    if not dates:
        fail("no account_return_daily partitions under %s" % prefix)
    step = max(1, len(dates) // 40)
    sample = dates[::step][:40]
    checked, n_graded, by_q = 0, 0, {}
    for d in sample:
        rows = read(on.address("irpt", "49financial", "gold", "account_return_daily", "date=%s" % d) + "/data.parquet")
        i = dates.index(d)
        prior = {}
        if i > 0:
            prior = {str(r["account_id"]): r for r in read(
                on.address("irpt", "49financial", "gold", "account_return_daily", "date=%s" % dates[i - 1]) + "/data.parquet")}
        try:
            hold = {str(r["account_id"]): r for r in read(
                on.address("irpt", "49financial", "gold", "holdings_performance_daily", "date=%s" % d) + "/data.parquet")}
        except s3.exceptions.NoSuchKey:
            hold = {}
        for r in rows:
            acct = str(r["account_id"])
            by_q[r.get("day_quality")] = by_q.get(r.get("day_quality"), 0) + 1
            pv = _num((prior.get(acct) or {}).get("market_value_eod"))
            failures, graded = grade_row(r, hold.get(acct), pv, method)
            if failures:
                fail("date=%s account %s: %s" % (d, acct, "; ".join(failures)))
            n_graded += graded
            checked += 1
    if checked == 0:
        fail("0 rows checked over %d sampled partitions" % len(sample))
    print("  sampled partitions %d of %d; rows checked %d; by day_quality %s; graded inside the comparability domain %d of %d; "
          "tolerance %.6g, band [%.6g, %.6g], excluded-weight ceiling %.6g"
          % (len(sample), len(dates), checked, by_q, n_graded, checked, float(method["tolerance"]),
             float(method["plausibility_band_low"]), float(method["plausibility_band_high"]),
             float(method["comparability_max_excluded_weight"])))
    print("DB-1-AC2 PASS")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve())
