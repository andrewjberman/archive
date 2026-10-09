"""TO-DB-b-58 (IRPT_DASHBD round 31, DB-b-58, E2): the 1,203 UNEXPLAINED misses of the compounded tie-out, each given ONE cause class.

Population: rows of round 30's TIEOUT_COMPOUND_E1.json with abs_diff_pp > 0.35 and reason UNEXPLAINED (read from the record).
Method: a decision list, first match wins; every class carries the number that decided it (the evidence).
  1 FEE_BASE_AVG_BALANCE         the fee add-back re-formed on the MEAN DAILY served market value (instead of (bmv+emv)/2) lands within 0.35 pp
  2 FEE_ADDBACK_NOT_APPLICABLE   BD's net return, with no add-back, lands within 0.35 pp of Opal
  3 FLOW_TIMING_AFTER_FEE_BASE   under the corrected fee base, a START or MID flow convention lands within 0.35 pp
  4 SEGMENT_FIRST_DAY            under the corrected fee base, linking without the segment's first day lands within 0.35 pp
  5 INCOME_TIMING                under the corrected fee base, the price-only link (income removed) lands within 0.35 pp
  6 VALUATION_BOUNDARY_MISMATCH  BD's beginning or ending market value differs from the served value at the boundary by more than 0.5%
  7 NEAR_ZERO_BALANCE            a daily value, or BD's beginning or ending value, below 1% / 2% of the segment's mean daily value
  8 LARGE_FLOW_DAY               a flow of at least 25% of the prior day's value
  9 NO_SINGLE_CAUSE_RESIDUAL     none of the above
The ONE correction (class 1) is `fee_base_gross` below; `regrade_all` states its effect on every graded segment of the 9,078.
Round 17/18/30 readers are imported and used as they are; only the bronze point parser is wrapped (to also keep netAdditions and income).
READ-ONLY: S3 GETs/LISTs only; zero vendor calls.

Usage: python unexplained_classes.py <repo_root> [--cache <pickle>]
Writes UNEXPLAINED_CLASSES_E2.json and UNEXPLAINED_CLASSES_E2.md beside this file.
"""
import functools
import importlib.util
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEL = HERE.parent
_spec = importlib.util.spec_from_file_location("tieout_compound_r30", str(DEL / "0.9.0_WK_IRPT_DASHBD~34" / "tieout_compound.py"))
tc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tc)
r18, r17 = tc.r18, tc.r17
# the daily-mean fee base (daily_mean_value, fee_base_gross) is defined once, in the project's reader of record (round 32, DB-b-60)
_rspec = importlib.util.spec_from_file_location("tieout_reader", str(DEL.parent / "tieout" / "tieout_reader.py"))
reader = importlib.util.module_from_spec(_rspec)
_rspec.loader.exec_module(reader)
# this classifier's mean keeps negative daily values (positive_only=False), as it always has, so its recorded output is unchanged
daily_mean_value = functools.partial(reader.daily_mean_value, positive_only=False)
fee_base_gross = functools.partial(reader.fee_base_gross, positive_only=False)

COMPOUND_REC = DEL / "0.9.0_WK_IRPT_DASHBD~34" / "TIEOUT_COMPOUND_E1.json"
OUT_JSON, OUT_MD = "UNEXPLAINED_CLASSES_E2.json", "UNEXPLAINED_CLASSES_E2.md"
TOL = tc.TOLERANCE_PP
SHARE = 0.80
BOUNDARY_GAP = 0.005
NEAR_ZERO_DAY, NEAR_ZERO_BOUNDARY, LARGE_FLOW = 0.01, 0.02, 0.25
CLASSES = ("FEE_BASE_AVG_BALANCE", "FEE_ADDBACK_NOT_APPLICABLE", "FLOW_TIMING_AFTER_FEE_BASE", "SEGMENT_FIRST_DAY", "INCOME_TIMING",
           "VALUATION_BOUNDARY_MISMATCH", "NEAR_ZERO_BALANCE", "LARGE_FLOW_DAY", "NO_SINGLE_CAUSE_RESIDUAL")

_orig_bd_points = r17.bd_points


def _bd_points_plus(resp, bd_account):
    """round 17's parser, plus netAdditions and income of the same account-level point."""
    out = _orig_bd_points(resp, bd_account)
    for lv in resp.get("levels") or []:
        desc = lv.get("descriptor") or {}
        if desc.get("level") != "Account" or str(desc.get("levelId")) != str(bd_account):
            continue
        for p in lv.get("dateRangePoints") or []:
            dr = p.get("dateRange") or {}
            k = (str(dr.get("startDate"))[:10], str(dr.get("endDate"))[:10])
            if k in out:
                out[k]["net_additions"] = r17._num(p.get("netAdditions"))
                out[k]["income"] = r17._num(p.get("income"))
    return out


r17.bd_points = _bd_points_plus


# ----------------------------------------------------------------------------------------------------------------- the correction
def regrade_all(plan, bronze, gold):
    """Re-grade every gradable segment on the corrected fee base. Returns counts against round 30's compounded verdict (re-derived here)."""
    c = {"graded": 0, "within_round30": 0, "within_fee_base": 0, "outside_to_within": 0, "within_to_outside": 0}
    for req in plan["request_list"]:
        a, bd_acct = req["account"], str(req["bd_account"])
        pts = bronze.get(bd_acct)
        for seg in req["segments"]:
            bd = pts.get((seg["start"], seg["end"])) if isinstance(pts, dict) else None
            days = r17.segment_days(gold.get(a), seg)
            if not days or bd is None or bd.get("twr") is None:
                continue
            opal = r17.link([d["r"] for d in days])
            _fees, add = r18.fee_addback(bd)
            old = abs(tc.compound_gross(bd["twr"], add) - opal) * 100.0 <= TOL
            new = abs(fee_base_gross(bd["twr"], bd.get("fees"), days) - opal) * 100.0 <= TOL
            c["graded"] += 1
            c["within_round30"] += old
            c["within_fee_base"] += new
            c["outside_to_within"] += (new and not old)
            c["within_to_outside"] += (old and not new)
    return c


# ----------------------------------------------------------------------------------------------------------------- the classifier
def _pp(x):
    return "%.3f" % (x * 100.0)


def classify(seg, days, series, bd):
    """(cause_class, evidence) for one UNEXPLAINED segment. days = served rows in the segment; series = the account's {date: row}."""
    st, en = seg["segment"]["start"], seg["segment"]["end"]
    opal = seg["opal_return"]
    fees = bd.get("fees")
    gross = fee_base_gross(bd["twr"], fees, days)
    avg = daily_mean_value(days) or 0.0
    d_new = abs(gross - opal) * 100.0
    if d_new <= TOL:
        return CLASSES[0], "fee add-back on mean daily value %.0f (not (bmv+emv)/2 = %.0f) gives abs_diff %.4f pp (round 30: %.4f pp)" % (
            avg, ((bd.get("bmv") or 0.0) + (bd.get("emv") or 0.0)) / 2.0, d_new, seg["abs_diff_pp"])
    d_net = abs(bd["twr"] - opal) * 100.0
    if d_net <= TOL:
        na = bd.get("net_additions")
        flow_note = "BD netAdditions equals minus the fee (fee taken as a flow)" if (na is not None and fees is not None and abs(na + fees) <= 1.0) \
            else "BD netAdditions does not equal minus the fee"
        return CLASSES[1], "BD net return without add-back gives abs_diff %.4f pp; %s" % (d_net, flow_note)
    best = min((abs(gross - tc.r17.link_alt_flow(days, cv)) * 100.0, cv) for cv in ("START", "MID"))
    if best[0] <= TOL:
        return CLASSES[2], "under the corrected fee base, %s flow timing gives abs_diff %.4f pp (END: %.4f pp)" % (best[1], best[0], d_new)
    d_first = abs(gross - r17.link([d["r"] for d in days[1:]])) * 100.0
    if d_first <= TOL:
        return CLASSES[3], "linking without the first day (%s) gives abs_diff %.4f pp (with it: %.4f pp)" % (days[0]["date"], d_first, d_new)
    d_px = abs(gross - r17.link([d["r"] - d["inc"] for d in days])) * 100.0
    if d_px <= TOL:
        return CLASSES[4], "price-only link (income removed) gives abs_diff %.4f pp (with income: %.4f pp)" % (d_px, d_new)
    prior = [d for d in sorted(series) if d < st]
    pmv = series[prior[-1]]["mv"] if prior else None
    emv_o = series[en]["mv"] if en in series else None

    def rel(x, y):
        return abs(x - y) / max(abs(y), 1.0)
    gap_b = rel(bd.get("bmv") or 0.0, pmv) if pmv is not None else 0.0
    gap_e = rel(bd.get("emv") or 0.0, emv_o) if emv_o is not None else 0.0
    if max(gap_b, gap_e) > BOUNDARY_GAP:
        return CLASSES[5], "BD begin value differs from the served prior-day value by %.2f%%, end value from the served end value by %.2f%% (gap > 0.5%%)" % (
            gap_b * 100.0, gap_e * 100.0)
    mvs = [d["mv"] or 0.0 for d in days]
    lo = min(mvs)
    prev, ratio = pmv or 0.0, 0.0
    for d in days:
        if prev > 0:
            ratio = max(ratio, abs(d["flow"] or 0.0) / prev)
        prev = d["mv"] or 0.0
    if avg > 0 and (lo < NEAR_ZERO_DAY * avg or (bd.get("bmv") or 0.0) < NEAR_ZERO_BOUNDARY * avg or (bd.get("emv") or 0.0) < NEAR_ZERO_BOUNDARY * avg):
        return CLASSES[6], "min daily value %.4f of the mean daily value; BD begin %.4f and end %.4f of it; largest flow %.2f of the prior day's value; abs_diff %.4f pp" % (
            lo / avg, (bd.get("bmv") or 0.0) / avg, (bd.get("emv") or 0.0) / avg, ratio, d_new)
    if ratio >= LARGE_FLOW:
        return CLASSES[7], "largest flow is %.2f of the prior day's value; abs_diff %.4f pp on the corrected fee base" % (ratio, d_new)
    return CLASSES[8], "no class evidence: largest flow %.2f of the prior day's value, min daily value %.2f of the mean; abs_diff %.4f pp" % (
        ratio, (lo / avg) if avg > 0 else 0.0, d_new)


def top_prefix(counts, total, share=SHARE):
    """The smallest prefix of classes by descending count (ties by name) whose cumulative count reaches share * total."""
    out, run = [], 0
    for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        if run >= share * total:
            break
        out.append((k, v))
        run += v
    return out, run


NOTES = {
    "FEE_BASE_AVG_BALANCE": ("fixed", "round 18/30 formed the fee add-back on (beginning + ending value) / 2; on a segment whose value moves with flows that is not "
                             "the average balance the fee was charged on. fee_base_gross() uses the mean daily served value; effect in `fix`."),
    "LARGE_FLOW_DAY": ("named_cause", "the segment holds a flow of at least 25% of the prior day's value; the segment return is then set by the valuation "
                       "of that flow day and BD's per-flow valuation is not in the landed period point, so the miss is not re-derivable from the landed files."),
    "NEAR_ZERO_BALANCE": ("named_cause", "the account is funded from, or emptied to, a near-zero value inside the segment; the compounded return on a near-zero "
                          "base is set by cents of value and the two systems value those days differently; not re-derivable from the landed files."),
    "FLOW_TIMING_AFTER_FEE_BASE": ("named_cause", "once the fee base is corrected, a START or MID flow convention reaches BD within 0.35 pp where the served END "
                                   "convention does not; BD's flow date is not landed, so no date is adopted here (graded both ways by the E3 cell)."),
}


# ----------------------------------------------------------------------------------------------------------------------------- run
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
    rec30 = json.loads(COMPOUND_REC.read_bytes().decode("utf-8"))
    a2bd = {r["account"]: str(r["bd_account"]) for r in plan["request_list"]}
    pop = [s for s in rec30["segments"] if s["abs_diff_pp"] > TOL and s.get("reason") == "UNEXPLAINED"]
    rows = []
    for s in pop:
        a, seg = s["account"], s["segment"]
        days = r17.segment_days(gold.get(a), seg)
        bd = bronze[a2bd[a]][(seg["start"], seg["end"])]
        cls, ev = classify(s, days, gold[a], bd)
        rows.append({"account": a, "segment": seg, "cause_class": cls, "evidence": ev})
    counts = {}
    for x in rows:
        counts[x["cause_class"]] = counts.get(x["cause_class"], 0) + 1
    top, covered = top_prefix(counts, len(rows))
    top_classes = []
    for k, v in top:
        disp, note = NOTES[k]
        top_classes.append({"class": k, "disposition": disp, "count": v, "note": note})
    eff = regrade_all(plan, bronze, gold)
    # control: the baseline re-derived here equals round 30's record
    assert eff["within_round30"] == rec30["after"]["within"], (eff, rec30["after"])
    in_pop_to_within = counts.get("FEE_BASE_AVG_BALANCE", 0)
    fix = {"file": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~36/unexplained_classes.py", "function": "fee_base_gross",
           "class": "FEE_BASE_AVG_BALANCE", "population_rows_moved_to_within": in_pop_to_within,
           "regrade_all_segments": eff, "round30_within": rec30["after"]["within"], "round30_graded": len(rec30["segments"])}
    out = {"measured_by": "0.9.0_WK_IRPT_DASHBD~36", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-58", "tolerance_pp": TOL,
           "vendor_calls": 0, "population": len(rows), "share_required": SHARE, "top_covered": covered,
           "rows": rows, "counts": counts, "top_classes": top_classes, "fix": fix,
           "decision_list": list(CLASSES),
           "files_read": {"round30_record": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~34/TIEOUT_COMPOUND_E1.json",
                          "round30_reader": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~34/tieout_compound.py",
                          "round18_reader": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~13/tieout_e2_gross.py",
                          "plan": r17.PLAN_REL,
                          "bronze_prefix": "s3://%s/%s" % (r17.BRONZE_BUCKET, r17.BRONZE_PREFIX), "bronze_object_count": n_obj,
                          "served_series": "s3://%s/%sdate=<YYYY-MM-DD>/data.parquet (%d partitions)" % (r17.GOLD_BUCKET, r17.GOLD_PREFIX, n_part),
                          "served_accounts": n_gold_accts}}
    (HERE / OUT_JSON).write_bytes((json.dumps(out, indent=1) + "\n").encode("utf-8"))
    lines = ["# UNEXPLAINED_CLASSES_E2 -- the 1,203 UNEXPLAINED compounded misses, classed by cause (TO-DB-b-58, 0.9.0_WK_IRPT_DASHBD~36)", "",
             "Counts only. Record: `UNEXPLAINED_CLASSES_E2.json`. Module: `unexplained_classes.py` (imports round 30's `tieout_compound.py`). "
             "S3 reads only; zero vendor calls. Tolerance 0.35 pp.", "",
             "Population: %d compounded segments outside 0.35 pp with reason UNEXPLAINED; each carries one cause class (decision list, first match wins)." % len(rows), "",
             "| cause class | segments |", "|---|---|"]
    for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append("| %s | %d |" % (k, v))
    lines += ["| total | %d |" % len(rows), "",
              "Top classes (smallest prefix reaching 80%% = %.1f of %d): covered %d (%.1f%%)." % (SHARE * len(rows), len(rows), covered, 100.0 * covered / len(rows)), "",
              "| top class | disposition | segments |", "|---|---|---|"]
    for t in top_classes:
        lines.append("| %s | %s | %d |" % (t["class"], t["disposition"], t["count"]))
    lines += ["", "Fix (FEE_BASE_AVG_BALANCE): fee add-back on the mean daily served value. Over all %d graded segments: within 0.35 pp %d -> %d "
              "(OUTSIDE to WITHIN %d, WITHIN to OUTSIDE %d). Of the %d, %d move to within." % (
                  eff["graded"], eff["within_round30"], eff["within_fee_base"], eff["outside_to_within"], eff["within_to_outside"],
                  len(rows), in_pop_to_within), ""]
    (HERE / OUT_MD).write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print(json.dumps({"counts": counts, "top": [(t["class"], t["count"], t["disposition"]) for t in top_classes], "covered": covered,
                      "fix": fix["regrade_all_segments"]}, indent=1))


if __name__ == "__main__":
    main()
