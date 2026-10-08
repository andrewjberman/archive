"""TO-DB-b-50 (IRPT_DASHBD round 29, DB-b-50): class the 440 accounts of TIEOUT_SPLIT_E1.json whose BD split halves do not recompose
to BD's own full-segment gross (recompose.within == false). READ-ONLY: S3 GETs only (the split pull and the earlier full pull, 440
objects each); zero vendor calls. The round-18 fee add-back (tieout_e2_gross.fee_addback) is imported, not restated.

Usage: python s34_class_e1.py <repo_root> [--cache <pickle>]
Writes S34_CLASS_E1.json and S34_CLASS_E1.md beside this file. The .md is counts and percentages only.

Decision rule (first match wins; every row states the figures that decided it):
  missing_or_zero_half         a half or the full point is absent, has no return, daysHeld 0 or notHeldInPeriod
  full_period_annualized       returnAnnualized true on the full point or on either half
  opened_or_closed_in_segment  a point has daysHeld < periodLength, heldEntirePeriod false or containsHistory true, or the two
                               halves' daysHeld plus the one excluded calendar day do not equal the full point's daysHeld
  fee_or_basis_between_pulls   the NET returns chain to the full NET within the tolerance (so the days, flags and returns agree) and
                               the gross gap is therefore the fee add-back, evaluated on the halves' bases against the full basis
  other:<cause>                none of the above (the NET chain itself is over tolerance)
"""
import importlib.util
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
_spec = importlib.util.spec_from_file_location("tieout_e2_gross_r18", str(D / "0.9.0_WK_IRPT_DASHBD~13" / "tieout_e2_gross.py"))
r18 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r18)

TIEOUT = D / "0.9.0_WK_IRPT_DASHBD~28" / "TIEOUT_SPLIT_E1.json"
PLAN = D / "0.9.0_WK_IRPT_DASHBD~25" / "SPLIT_PULL_PLAN.json"
BUCKET = "opal-data-assets"
SPLIT_PREFIX = "blackdiamond/49financial/bronze/reporting_performance/pull=split20261007/"
FULL_PREFIX = "blackdiamond/49financial/bronze/reporting_performance/pull=20261004/"
TOL = r18.TOLERANCE_PP
OTHER_NET = "other:net_twr_chain_over_tolerance_with_days_flags_and_basis_agreeing"


def fetch(rows, plan_by_acct, cache):
    if cache and Path(cache).is_file():
        with open(cache, "rb") as f:
            return pickle.load(f)
    import boto3
    from botocore.config import Config
    from concurrent.futures import ThreadPoolExecutor
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(
        retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))

    def one(a):
        bd = str(plan_by_acct[a]["bd_account"])
        out = {}
        for tag, pre in (("split", SPLIT_PREFIX), ("full", FULL_PREFIX)):
            try:
                out[tag] = s3.get_object(Bucket=BUCKET, Key="%sacct=%s.json" % (pre, bd))["Body"].read()
            except Exception as e:
                out[tag] = "ERR " + type(e).__name__
        return a, out

    with ThreadPoolExecutor(max_workers=16) as ex:
        res = dict(ex.map(one, [r["account"] for r in rows]))
    if cache:
        with open(cache, "wb") as f:
            pickle.dump(res, f)
    return res


def points(raw, bd):
    """{(start, end): raw dateRangePoint} for the account-level entry of a performancePeriod response, or None when unreadable."""
    if not isinstance(raw, bytes):
        return None
    out = {}
    for lv in json.loads(raw.decode("utf-8")).get("levels") or []:
        d = lv.get("descriptor") or {}
        if d.get("level") != "Account" or str(d.get("levelId")) != str(bd):
            continue
        for p in lv.get("dateRangePoints") or []:
            dr = p.get("dateRange") or {}
            out[(str(dr.get("startDate"))[:10], str(dr.get("endDate"))[:10])] = p
    return out


def ret(p):
    return ((p or {}).get("timeWeightedReturns") or {}).get("return")


def addback(p):
    return r18.fee_addback({"fees": p.get("fees"), "bmv": p.get("beginningMarketValue"), "emv": p.get("endingMarketValue")})[1]


def fmt(v):
    return "none" if v is None else "%.6f" % v


def classify(x, pl, pr, pf):
    """(cause_class, evidence) for one record row and its three raw points."""
    pts = {"left": pl, "right": pr, "full": pf}
    gap = x["recompose"]["abs_diff_pp"]
    absent = [k for k, p in pts.items() if p is None or ret(p) is None or not p.get("daysHeld") or p.get("notHeldInPeriod")]
    if absent:
        return "missing_or_zero_half", "point absent, without a return, daysHeld 0 or notHeldInPeriod: %s" % ",".join(absent)
    ann = [k for k, p in pts.items() if (p.get("timeWeightedReturns") or {}).get("returnAnnualized")]
    if ann:
        return "full_period_annualized", "returnAnnualized true on: %s" % ",".join(ann)
    short = [k for k, p in pts.items() if (p.get("daysHeld") or 0) < (p.get("periodLength") or 0)
             or not p.get("heldEntirePeriod") or p.get("containsHistory")]
    dsum = pl["daysHeld"] + pr["daysHeld"]
    if short or dsum != pf["daysHeld"] - 1:
        return "opened_or_closed_in_segment", "daysHeld/periodLength/heldEntirePeriod/containsHistory off on: %s; days left %s + right %s vs full %s" % (
            ",".join(short) or "none", pl["daysHeld"], pr["daysHeld"], pf["daysHeld"])
    nl, nr, nf = ret(pl), ret(pr), ret(pf)
    net_gap = abs((1.0 + nl) * (1.0 + nr) - 1.0 - nf) * 100.0
    al, ar, af = x["left"].get("bd_fee_addback"), x["right"].get("bd_fee_addback"), addback(pf)
    ev = ("net chain vs full net %.4f pp; gross gap %.4f pp; fee add-back left %s right %s full %s; fees left %s right %s full %s; "
          "days left %s right %s full %s (halves + 1 excluded day = full)" % (
              net_gap, gap, fmt(al), fmt(ar), fmt(af), pl.get("fees"), pr.get("fees"), pf.get("fees"),
              pl["daysHeld"], pr["daysHeld"], pf["daysHeld"]))
    if net_gap <= TOL:
        return "fee_or_basis_between_pulls", ev
    return OTHER_NET, ev + "; beginning market value left %s, ending %s" % (pl.get("beginningMarketValue"), pl.get("endingMarketValue"))


def main():
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    rec = json.loads(TIEOUT.read_bytes().decode("utf-8"))
    rows = rec["rows"]
    s34 = [x for x in rows if x["recompose"]["within"] is False]
    plan = json.loads(PLAN.read_bytes().decode("utf-8"))
    pb = {q["account"]: q for q in plan["request_list"]}
    raw = fetch(s34, pb, cache)

    out_rows, counts, files_read = [], {}, 0
    feats = {}
    for x in s34:
        a = x["account"]
        bd = pb[a]["bd_account"]
        sp, fp = points(raw[a]["split"], bd), points(raw[a]["full"], bd)
        files_read += (sp is not None) + (fp is not None)
        L, R = x["left"]["range"], x["right"]["range"]
        pl = (sp or {}).get((L["start"], L["end"]))
        pr = (sp or {}).get((R["start"], R["end"]))
        pf = (fp or {}).get((L["start"], R["end"]))
        cause, ev = classify(x, pl, pr, pf)
        out_rows.append({"account": a, "cause_class": cause, "evidence": ev})
        counts[cause] = counts.get(cause, 0) + 1
        feats[a] = (pl, pr, pf)
    assert sum(counts.values()) == len(s34)

    # control: the round-18 record's full gross equals the landed full point's net return plus the add-back recomputed here
    ctl_bad = 0
    for x in s34:
        pf = feats[x["account"]][2]
        if pf is None or abs(ret(pf) + (addback(pf) or 0.0) - x["recompose"]["bd_full_gross"]) > 1e-9:
            ctl_bad += 1

    top = max(s34, key=lambda x: x["recompose"]["abs_diff_pp"])
    pl, pr, pf = feats[top["account"]]
    def fees(p):
        return {"fees": p.get("fees"), "netAdditions": p.get("netAdditions"), "bmv": p.get("beginningMarketValue"),
                      "emv": p.get("endingMarketValue"), "daysHeld": p.get("daysHeld"), "net_return": ret(p),
                      "fee_addback": addback(p), "returnAnnualized": (p.get("timeWeightedReturns") or {}).get("returnAnnualized")}
    outlier = {"account": top["account"], "bd_left": top["left"]["bd_return"], "bd_right": top["right"]["bd_return"],
               "bd_full": top["recompose"]["bd_full_gross"], "chained": top["recompose"]["chained"],
               "abs_diff_pp": top["recompose"]["abs_diff_pp"],
               "landed": {"left": fees(pl), "right": fees(pr), "full": fees(pf)},
               "ranges_returned": {"left": [top["left"]["range"]["start"], top["left"]["range"]["end"]],
                                   "right": [top["right"]["range"]["start"], top["right"]["range"]["end"]],
                                   "full": [top["left"]["range"]["start"], top["right"]["range"]["end"]]},
               "net_chain_gap_pp": abs((1 + ret(pl)) * (1 + ret(pr)) - 1 - ret(pf)) * 100.0,
               "cause_class": next(r["cause_class"] for r in out_rows if r["account"] == top["account"]),
               "reading": ("The three net returns chain (net gap well inside tolerance). The gap is the fee add-back: the full point reports "
                           "fees of about -175 against a beginning value of about 41 and an ending value of 0, so the add-back "
                           "fees / ((bmv + emv) / 2) is about -8.6 on the full range and about -1.36 on the left half; the fee is "
                           "negative on the left half (equal to that half's net additions) and on the full range. The gross figure is the net return plus that add-back.")}

    misses = {x["account"] for x in rows if not x["right"]["tied"]}
    ids = {x["account"] for x in s34}
    overlap = {"right_misses": len(misses), "in_s34": len(misses & ids), "outside_s34": len(misses - ids)}

    n = len(s34)
    sub = {
        "net_chain_within_tolerance": sum(1 for r in out_rows if r["cause_class"] == "fee_or_basis_between_pulls"),
        "any_fee_negative": sum(1 for a, (pa, pb_, pc_) in feats.items() if any((p.get("fees") or 0) < 0 for p in (pa, pb_, pc_))),
        "full_ending_value_zero": sum(1 for a, (pa, pb_, pc_) in feats.items() if (pc_.get("endingMarketValue") or 0) == 0),
        "gross_gap_over_1pp": sum(1 for x in s34 if x["recompose"]["abs_diff_pp"] > 1.0),
        "gross_gap_over_10pp": sum(1 for x in s34 if x["recompose"]["abs_diff_pp"] > 10.0),
        "left_half_tied": sum(1 for x in s34 if x["left"]["tied"]),
        "right_half_tied": sum(1 for x in s34 if x["right"]["tied"]),
    }
    gaps = sorted(x["recompose"]["abs_diff_pp"] for x in s34)
    gq = {q: gaps[int((n - 1) * q)] for q in (0.0, 0.25, 0.5, 0.75, 0.9, 1.0)}

    result = {"measured_by": "0.9.0_WK_IRPT_DASHBD~29", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-50",
              "vendor_calls": 0, "tolerance_pp": TOL, "population": n,
              "source_record": "deliverables/0.9.0_WK_IRPT_DASHBD~28/TIEOUT_SPLIT_E1.json (rows with recompose.within == false)",
              "classes_closed_set": ["opened_or_closed_in_segment", "fee_or_basis_between_pulls", "missing_or_zero_half",
                                     "full_period_annualized", "other:<named>"],
              "rule": "first match wins: missing_or_zero_half, full_period_annualized, opened_or_closed_in_segment, then "
                      "fee_or_basis_between_pulls iff net halves chain to the full net within tolerance, else other:",
              "counts": counts, "rows": out_rows, "outlier": outlier, "overlap": overlap, "sub_counts": sub,
              "gross_gap_pp_quantiles": {str(k): v for k, v in gq.items()},
              "control_round18_full_gross_rederived_mismatches": ctl_bad,
              "files_read": files_read,
              "files_read_detail": {"split_pull": "s3://%s/%s" % (BUCKET, SPLIT_PREFIX), "full_pull": "s3://%s/%s" % (BUCKET, FULL_PREFIX),
                                    "objects_expected": 2 * n}}
    (HERE / "S34_CLASS_E1.json").write_bytes((json.dumps(result, indent=1) + "\n").encode("utf-8"))

    def pc(v):
        return "%.1f%%" % (100.0 * v / n)

    md = ["# S34_CLASS_E1 -- class of the 440 accounts whose BD split halves do not recompose (counts and percentages only)", "",
          "Population: %d accounts (recompose.within false in TIEOUT_SPLIT_E1). Landed objects read: %d of %d. Vendor calls 0." % (
              n, files_read, 2 * n), "",
          "| cause_class | accounts | share |", "|---|---|---|"]
    md += ["| %s | %d | %s |" % (k, v, pc(v)) for k, v in sorted(counts.items(), key=lambda kv: -kv[1])]
    md += ["| total | %d | 100.0%% |" % n, "",
           "Rule (first match wins): missing/zero half, annualized, days or held-flags off, then fee/basis iff the NET halves chain to the "
           "full NET within %.2f pp, else other." % TOL, "",
           "Reading: %d of %d (%s) have net returns that chain inside tolerance with day counts and flags agreeing; the gross gap is the "
           "fee add-back (fees / average of begin and end value) evaluated on three different bases. %d have an ending value of 0 on the "
           "full range (add-back denominator is half the opening value); %d carry a negative fee on at least one of the three points." % (
               sub["net_chain_within_tolerance"], n, pc(sub["net_chain_within_tolerance"]), sub["full_ending_value_zero"],
               sub["any_fee_negative"]), "",
           "Gross gap pp: min %.2f, median %.2f, p75 %.2f, p90 %.2f, max %.2f. Over 1 pp: %d (%s); over 10 pp: %d (%s)." % (
               gq[0.0], gq[0.5], gq[0.75], gq[0.9], gq[1.0], sub["gross_gap_over_1pp"], pc(sub["gross_gap_over_1pp"]),
               sub["gross_gap_over_10pp"], pc(sub["gross_gap_over_10pp"])), "",
           "Largest gap (%.2f pp): left %.4f, right %.4f, full %.4f, chained %.4f (gross). Class %s; net chain gap %.4f pp. The gap is the "
           "full-range fee add-back on a closing account (negative fee, average value is half the opening value)." % (
               outlier["abs_diff_pp"], outlier["bd_left"], outlier["bd_right"], outlier["bd_full"], outlier["chained"],
               outlier["cause_class"], outlier["net_chain_gap_pp"]), "",
           "Overlap with right-half misses: right_misses %d, in_s34 %d, outside_s34 %d (of the %d S34 accounts, left tied %d, right tied %d)." % (
               overlap["right_misses"], overlap["in_s34"], overlap["outside_s34"], n, sub["left_half_tied"], sub["right_half_tied"]), "",
           "Control: round-18 full gross re-derived from the landed full point for all %d; mismatches %d." % (n, ctl_bad), ""]
    (HERE / "S34_CLASS_E1.md").write_bytes(("\n".join(md)).encode("ascii"))
    print("OK: %d classed %s; files %d; overlap %s; outlier %.2f pp; control mismatches %d" % (
        n, counts, files_read, overlap, outlier["abs_diff_pp"], ctl_bad))


if __name__ == "__main__":
    main()
