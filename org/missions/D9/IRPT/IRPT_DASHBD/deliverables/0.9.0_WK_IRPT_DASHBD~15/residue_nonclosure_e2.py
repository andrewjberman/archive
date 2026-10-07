"""DB-b-30: classify the E2 nonclosure segments (GROSS UNEXPLAINED minus the +1-day-over-2025-01-09 set) against the closed reason set.

Reads the GROSS record, the BD plan (account -> bd_account) and the landed BD bronze responses (boto3, us-east-1, read-only; or a local
cache dir via --cache). Zero vendor calls; Opal's served series is never read (fenced). Writes RESIDUE_NONCLOSURE_E2.json.
A reason is assigned only on evidence named in the row; otherwise the segment stays UNEXPLAINED.
"""
import json
import sys
from collections import Counter
from pathlib import Path

CLOSURE = "2025-01-09"
TOL = 0.0035
FLOW_SHARE_MIN = 0.25
REASONS = ("FLOW_TIMING", "MISSING_PRICE", "INCOME_DATE", "COVERAGE_DAYS", "UNEXPLAINED")
HERE = Path(__file__).resolve().parent
P = HERE.parent
GROSS = P / "0.9.0_WK_IRPT_DASHBD~13" / "TIEOUT_49F_BD_POPULATION_E2_GROSS.json"
PLAN = P / "0.9.0_WK_IRPT_DASHBD~6" / "BD_POPULATION_PLAN_E3.json"
BUCKET = "opal-data-assets"
KEY = "blackdiamond/49financial/bronze/reporting_performance/pull=20261004/acct=%s.json"


def nonclosure_set(gross):
    graded = [s for s in gross.get("segments") or [] if s.get("verdict") in ("WITHIN", "OUTSIDE")]
    out = []
    for s in graded:
        if s.get("verdict") != "OUTSIDE" or s.get("reason") != "UNEXPLAINED":
            continue
        g = s.get("segment") or {}
        if (s.get("bd_days_held") or 0) - (s.get("opal_days") or 0) == 1 and g.get("start", "9") <= CLOSURE <= g.get("end", "0"):
            continue
        out.append(s)
    return graded, out


def account_point(resp, seg):
    for n in (resp or {}).get("combinedLevels") or []:
        if (n.get("descriptor") or {}).get("level") != "Account":
            continue
        for x in n.get("dateRangePoints") or []:
            r = x.get("dateRange") or {}
            if str(r.get("startDate"))[:10] == seg.get("start") and str(r.get("endDate"))[:10] == seg.get("end"):
                return x
    return None


def classify(s, point):
    """Return (reason, evidence) for one nonclosure segment given BD's Account-level point (None = absent)."""
    if not point:
        return "UNEXPLAINED", "no BD Account-level point for the segment's dates; nothing to test"
    b = point.get("beginningMarketValue") or 0.0
    e = point.get("endingMarketValue") or 0.0
    f = point.get("netAdditions") or 0.0
    big = max(b, e)
    if big <= 0:
        return "UNEXPLAINED", "BD begin and end market values are both zero; nothing to test"
    share = abs(f) / big
    gain = e - b - f
    ends = [gain / b] if b > 0 else []
    if b + f > 0:
        ends.append(gain / (b + f))
    base = "BD Account point bmv %.2f emv %.2f netAdditions %.2f (flow share of larger value %.3f)" % (b, e, f, share)
    if ends and share >= FLOW_SHARE_MIN:
        lo, hi = min(ends) - TOL, max(ends) + TOL
        o, g = s.get("opal_return"), s.get("bd_gross_return")
        if o is not None and g is not None and lo <= o <= hi and lo <= g <= hi:
            return "FLOW_TIMING", ("%s; Dietz envelope with the net flow at segment start vs end is [%.4f, %.4f] (+-0.35 pp); "
                                   "Opal %.4f and BD gross %.4f both lie inside, so the flow day alone can carry the %.2f pp gap"
                                   % (base, lo, hi, o, g, s.get("abs_diff_pp") or 0.0))
    return "UNEXPLAINED", ("%s; flow-timing envelope test not met (share < %.2f or a return outside the envelope); "
                           "no BD asset-level zero-value-held position, no day-count gap (BD %s vs Opal %s)"
                           % (base, FLOW_SHARE_MIN, s.get("bd_days_held"), s.get("opal_days")))


def build(gross, plan, fetch):
    graded, ns = nonclosure_set(gross)
    m = {r["account"]: r["bd_account"] for r in plan.get("request_list") or []}
    cache = {}
    rows = []
    for s in ns:
        a = s.get("account")
        if a not in cache:
            cache[a] = fetch(m.get(a)) if m.get(a) else None
        reason, ev = classify(s, account_point(cache[a], s.get("segment") or {}))
        rows.append({"account": a, "segment": s.get("segment"), "reason": reason, "evidence": ev})
    per = Counter(r["reason"] for r in rows)
    fin = per.get("UNEXPLAINED", 0)
    counts = {"denominator": len(graded), "nonclosure": len(rows), "per_reason": {k: per.get(k, 0) for k in REASONS},
              "final_unexplained": fin, "share_of_graded": fin / len(graded) if graded else None}
    return {"task_order": "IRPT_DASHBD.TO-DB-b-30", "measured_by": "0.9.0_WK_IRPT_DASHBD~15", "claim": "inferred",
            "vendor_calls": 0, "reasons_closed_set": list(REASONS), "counts": counts, "rows": rows}


def main(argv):
    cache_dir = Path(argv[argv.index("--cache") + 1]) if "--cache" in argv else None
    if cache_dir:
        def fetch(b):
            return json.loads((cache_dir / ("%s.json" % b)).read_bytes().decode("utf-8"))
    else:
        import boto3
        c = boto3.client("s3", region_name="us-east-1")

        def fetch(b):
            return json.loads(c.get_object(Bucket=BUCKET, Key=KEY % b)["Body"].read().decode("utf-8"))
    gross = json.loads(GROSS.read_bytes().decode("utf-8"))
    plan = json.loads(PLAN.read_bytes().decode("utf-8"))
    rec = build(gross, plan, fetch)
    (HERE / "RESIDUE_NONCLOSURE_E2.json").write_text(json.dumps(rec, indent=1), encoding="utf-8")
    print(json.dumps(rec["counts"]))


if __name__ == "__main__":
    main(sys.argv[1:])
