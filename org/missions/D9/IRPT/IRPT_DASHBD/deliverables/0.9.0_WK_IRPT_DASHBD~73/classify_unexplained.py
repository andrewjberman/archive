"""TO-DB-b-98 (IRPT_DASHBD round 48, DB-b-98): classify each of the 510 UNEXPLAINED outside segments of TIEOUT_COMPOUND_V2.json by a named
reason from a declared set, or as DEFECT. READ-ONLY: S3 GETs only; zero vendor calls; writes UNEXPLAINED_CLASSIFIED.json beside this file.

Usage: python classify_unexplained.py <repo_root> [--cache <pickle of tieout_compound_v2.load>]

Inputs per segment: the V2 row; the served daily gold series (market value, external flow, income, daily return); Black Diamond's landed
account-level point for the same range (beginning/ending market value, netAdditions, netGains, daysHeld). Reasons are tested in a fixed
order, first match wins, so the set is exclusive by construction (see REASON_SET_RULE24.md). No client identifier beyond the account key is kept.
"""
import importlib.util
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
V2_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~35/TIEOUT_COMPOUND_V2.json"
V2PY_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~35/tieout_compound_v2.py"
OUT = HERE / "UNEXPLAINED_CLASSIFIED.json"
TOL_PP = 0.35
DOLLAR_ABS, DOLLAR_REL = 1.0, 0.001
NZ_FRAC = 0.01
EXISTING = ["FLOW_TIMING", "INCOME_DATE", "MISSING_PRICE", "COVERAGE_DAYS"]
NEW = ["BOUNDARY_VALUE_GAP", "NEAR_ZERO_BASE", "ZERO_GAIN_VENDOR_TWR", "FLOW_CONVENTION_ENVELOPE", "WINDOW_ONE_DAY_SHIFT"]
REASON_SET = EXISTING + NEW
DEFECT_ROWS = {"DOLLARS_DIFFER_NO_RECONCILIATION": "IRPT_DASHBD-D2-W73-S1",
               "DOLLARS_TIE_RETURN_DIFFERS_NO_NAMED_CAUSE": "IRPT_DASHBD-D2-W73-S2"}


def tie(a, b):
    return abs(a - b) <= max(DOLLAR_ABS, DOLLAR_REL * max(abs(a), abs(b)))


def link(rs):
    p = 1.0
    for r in rs:
        p *= 1.0 + r
    return p - 1.0


def relink(days, conv):
    """Re-link under a flow-timing convention (END is the served one); the first day keeps its served return (round 17 rule)."""
    p = 1.0
    for i, d in enumerate(days):
        if i == 0 or not d.get("mv") or not days[i - 1].get("mv") or d.get("flow") is None:
            p *= 1.0 + d["r"]
            continue
        v0, v1, f = days[i - 1]["mv"], d["mv"], d["flow"]
        if conv == "START":
            den = v0 + f
            r = v1 / den - 1.0 if den else d["r"]
        elif conv == "MID":
            den = v0 + f / 2.0
            r = (v1 - f / 2.0) / den - 1.0 if den else d["r"]
        else:
            r = (v1 - f) / v0 - 1.0
        p *= 1.0 + r
    return p - 1.0


def bd_fields(s3, bd_acct, wanted):
    key = "blackdiamond/49financial/bronze/reporting_performance/pull=20261004/acct=%s.json" % bd_acct
    b = json.loads(s3.get_object(Bucket="opal-data-assets", Key=key)["Body"].read().decode("utf-8"))
    out = {}
    for lv in b.get("levels") or []:
        d = lv.get("descriptor") or {}
        if d.get("level") != "Account" or str(d.get("levelId")) != bd_acct:
            continue
        for p in lv.get("dateRangePoints") or []:
            dr = p["dateRange"]
            k = (dr["startDate"][:10], dr["endDate"][:10])
            if k in wanted:
                out[k] = {"bmv": p.get("beginningMarketValue") or 0.0, "emv": p.get("endingMarketValue") or 0.0,
                          "net_additions": p.get("netAdditions") or 0.0, "net_gains": p.get("netGains") or 0.0,
                          "days_held": p.get("daysHeld")}
    return out


def classify(s, g, bd):
    """(reason | 'DEFECT', test evidence, defect cause | None) for one V2 UNEXPLAINED OUTSIDE segment."""
    seg = s["segment"]
    allds = sorted(g)
    ds = [d for d in allds if seg["start"] <= d <= seg["end"]]
    prev = [d for d in allds if d < seg["start"]]
    days = [g[d] for d in ds if g[d]["r"] is not None]
    mvs = [d["mv"] or 0.0 for d in days]
    mv_prev = (g[prev[-1]]["mv"] or 0.0) if prev else (days[0]["mv"] or 0.0)
    mv_end = mvs[-1]
    flow = sum(d["flow"] or 0.0 for d in days)
    gain = mv_end - mv_prev - flow
    peak = max(mvs + [mv_prev]) or 1e-9
    mean = sum(mvs) / len(mvs)
    gross, opal = s["bd_gross_return"], s["opal_return"]
    signed = gross - opal
    ties = {"bmv": tie(bd["bmv"], mv_prev), "emv": tie(bd["emv"], mv_end), "flow": tie(bd["net_additions"], flow),
            "gain": tie(bd["net_gains"], gain)}
    dollars_tie = all(ties.values())
    gap = bd["net_gains"] - gain
    pred = gap / mean if mean > 0 else 0.0
    # 1 BOUNDARY_VALUE_GAP
    if not dollars_tie and abs(signed - pred) * 100.0 <= TOL_PP:
        return ("BOUNDARY_VALUE_GAP", "BD boundary/gain dollars differ from served (tie flags %s); gain gap over mean value = %.4f pp "
                "vs observed signed gap %.4f pp (residual %.4f pp)" % (ties, pred * 100, signed * 100, abs(signed - pred) * 100), None)
    # 2 NEAR_ZERO_BASE
    low = min(bd["bmv"], bd["emv"], min(mvs + [mv_prev]))
    if dollars_tie and low <= NZ_FRAC * peak:
        return ("NEAR_ZERO_BASE", "dollars tie (bmv, emv, flows, gain); lowest balance is %.4f of peak (limit %.2f)" % (low / peak, NZ_FRAC), None)
    # 3 ZERO_GAIN_VENDOR_TWR
    if dollars_tie and abs(bd["net_gains"]) < DOLLAR_ABS and abs(gain) < DOLLAR_ABS and abs(s["bd_return"]) * 100.0 > TOL_PP:
        return ("ZERO_GAIN_VENDOR_TWR", "BD netGains and served gain are both under $%.0f while BD TWR is %.4f" % (
            DOLLAR_ABS, s["bd_return"]), None)
    # 4 FLOW_CONVENTION_ENVELOPE
    if dollars_tie and any(d.get("flow") for d in days):
        alts = [relink(days, c) for c in ("START", "MID", "END")]
        lo, hi = min(alts) - TOL_PP / 100.0, max(alts) + TOL_PP / 100.0
        if lo <= gross <= hi:
            return ("FLOW_CONVENTION_ENVELOPE", "dollars tie; BD gross %.6f lies inside the Opal link under START/MID/END flow timing [%.6f, %.6f] +/- %.2f pp" % (
                gross, min(alts), max(alts), TOL_PP), None)
    # 5 WINDOW_ONE_DAY_SHIFT
    if len(days) > 1 and isinstance(bd["days_held"], int) and bd["days_held"] != len(days):
        for nm, sub in (("first", days[1:]), ("last", days[:-1])):
            if abs(gross - link([d["r"] for d in sub])) * 100.0 <= TOL_PP:
                return ("WINDOW_ONE_DAY_SHIFT", "BD daysHeld %d vs linked %d; link with the %s day dropped is within %.2f pp of BD gross" % (
                    bd["days_held"], len(days), nm, TOL_PP), None)
    cause = "DOLLARS_DIFFER_NO_RECONCILIATION" if not dollars_tie else "DOLLARS_TIE_RETURN_DIFFERS_NO_NAMED_CAUSE"
    return "DEFECT", "no reason test holds; dollar ties %s" % ties, cause


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    sp = importlib.util.spec_from_file_location("v2", str(root / V2PY_REL))
    v2m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(v2m)
    plan, (n_obj, bronze, gold, n_part, n_gold_accts) = v2m.load(root, cache)
    v2 = json.loads((root / V2_REL).read_bytes().decode("utf-8"))
    outside = [x for x in v2["segments"] if x["verdict"] == "OUTSIDE"]
    unexp = [x for x in outside if x["reason"] == "UNEXPLAINED"]
    bdacct = {r["account"]: str(r["bd_account"]) for r in plan["request_list"]}
    if len(unexp) != int(v2["outside_by_reason"]["UNEXPLAINED"]) or len(unexp) != 510:
        print("STOP: UNEXPLAINED re-derived %d vs V2 summary %s" % (len(unexp), v2["outside_by_reason"]["UNEXPLAINED"]))
        sys.exit(2)
    import boto3
    from botocore.config import Config
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=32, retries={"max_attempts": 8, "mode": "standard"}))
    need = {}
    for x in unexp:
        need.setdefault(bdacct[x["account"]], set()).add((x["segment"]["start"], x["segment"]["end"]))
    with ThreadPoolExecutor(16) as ex:
        bdx = dict(ex.map(lambda a: (a, bd_fields(s3, a, need[a])), list(need)))
    classified, defects = [], {}
    for x in unexp:
        bd = bdx[bdacct[x["account"]]][(x["segment"]["start"], x["segment"]["end"])]
        reason, ev, cause = classify(x, gold[x["account"]], bd)
        c = {"account": x["account"], "segment": x["segment"], "reason": reason, "evidence": ev}
        if cause:
            c["defect_cause"] = cause
            c["row"] = DEFECT_ROWS[cause]
            defects.setdefault(cause, []).append(c)
        classified.append(c)
    by = {}
    for x in outside:
        if x["reason"] != "UNEXPLAINED":
            by[x["reason"]] = by.get(x["reason"], 0) + 1
    for c in classified:
        by[c["reason"]] = by.get(c["reason"], 0) + 1
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~73", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-98", "vendor_calls": 0,
           "source": V2_REL, "denominator_outside": len(outside), "unexplained_rederived": len(unexp), "reason_set": REASON_SET,
           "thresholds": {"tolerance_pp": TOL_PP, "dollar_tie": "max(%.0f, %.1f%% of the larger)" % (DOLLAR_ABS, DOLLAR_REL * 100),
                          "near_zero_fraction_of_peak": NZ_FRAC},
           "by_reason": by, "classified": classified, "defect_causes": {k: len(v) for k, v in defects.items()},
           "rule24_record": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~73/REASON_SET_RULE24.md"}
    OUT.write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print("OK: outside %d; unexplained %d; by_reason %s; defect causes %s" % (len(outside), len(unexp), by, rec["defect_causes"]))


if __name__ == "__main__":
    main()
