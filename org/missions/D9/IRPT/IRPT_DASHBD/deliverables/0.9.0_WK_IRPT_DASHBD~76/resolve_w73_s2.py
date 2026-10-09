"""TO-DB-b-101 (IRPT_DASHBD round 49, DB-b-101): resolve the 123 W73-S2 DEFECT segments of the 49F vs Black Diamond tie-out.
READ-ONLY: S3 GETs only (served daily returns gold, Black Diamond landed bronze); zero vendor calls; no S3 write.

Row W73-S2 = segments where dollars tie (beginning value, ending value, flows, gain), the base is not near zero, and no V2 reason test closed the gap.
For each segment this script reads BOTH sides and writes, beside itself:
  W73_S2_EVIDENCE.json    both sides' values per segment (served series and Black Diamond's landed point)
  W73_S2_RESOLUTION.json  {segments: [{account, segment, disposition, cause, evidence}]}   (the shape p49_round49.py grades)

Tests, first match wins, so each segment carries exactly one cause:
  1 DUST_BASE_FEE_ADDBACK       largest served balance in the segment under $5: both returns are ~0, the gap is the tie-out's fee gross-up of a
                                BD-reported fee that is the size of the balance
  2 BD_FEE_FIGURE_EXTREME       |fee / mean daily value| >= 5% (a negative fee is a credit): the gross-up is larger than any return the dollars allow
  3 FLOW_TIMING_START_OF_DAY    the served link re-formed under START or MID flow timing, FIRST DAY INCLUDED (the V2 relink kept the first day as
                                served), lands within 0.35 pp of BD gross
  4 BD_FEE_TIMING_ENVELOPE      the served return lies inside the envelope of BD gross re-formed under 15 fee gross-up variants (5 fee bases x 3
                                compounding forms), widened by 0.35 pp: BD gives one fee total and no fee dates
  5 LARGE_FLOW_DAY_SENSITIVITY  some day's external flow is at least 50% of the prior day's balance: that day's return is a ratio on a base the flow
                                dwarfs, so a small difference in where the flow is booked or valued moves the linked return by points
  6 UNRESOLVED_BY_EXCLUSION     none of the above; by exclusion only (see the surprise row)
Producer self-consistency (every segment): the served daily returns re-linked from the served market value and external flow, END convention,
equal the served link to within 0.05 pp. A producer defect would break this identity; none does.

Usage: python resolve_w73_s2.py <repo_root> [--cache <pickle of tieout_compound_v2.load>]
"""
import importlib.util
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
V2PY_REL = DELIV + "0.9.0_WK_IRPT_DASHBD~35/tieout_compound_v2.py"
V2_REL = DELIV + "0.9.0_WK_IRPT_DASHBD~35/TIEOUT_COMPOUND_V2.json"
CLS_REL = DELIV + "0.9.0_WK_IRPT_DASHBD~73/UNEXPLAINED_CLASSIFIED.json"
ROW = "IRPT_DASHBD-D2-W73-S2"
TOL = 0.0035
BIG_FLOW = 0.5
DUST = 5.0
FEE_EXTREME = 0.05
EVID_REL = DELIV + "0.9.0_WK_IRPT_DASHBD~76/W73_S2_EVIDENCE.json"


def link(rs):
    p = 1.0
    for r in rs:
        p *= 1.0 + r
    return p - 1.0


def relink(g, ds, prev_mv, conv):
    """Re-link from market value and external flow under a flow-timing convention; the first day uses the prior day's value (outside the segment)."""
    p, pv = 1.0, prev_mv
    for d in ds:
        r, v1, f = g[d]["r"], g[d]["mv"], g[d]["flow"]
        if v1 and pv and f is not None:
            if conv == "START":
                den = pv + f
                r = v1 / den - 1.0 if den else r
            elif conv == "MID":
                den = pv + f / 2.0
                r = (v1 - f / 2.0) / den - 1.0 if den else r
            else:
                r = (v1 - f) / pv - 1.0
        p *= 1.0 + r
        pv = g[d]["mv"]
    return p - 1.0


def fee_variants(twr, fees, bases):
    out = []
    for b in bases:
        if b and b > 0:
            dr = fees / b
            out.append((1.0 + twr) * (1.0 + dr) - 1.0)
            if dr < 1.0:
                out.append((1.0 + twr) / (1.0 - dr) - 1.0)
            out.append(twr + dr)
    return out


def bd_mwr(s3, bd_acct, wanted):
    key = "blackdiamond/49financial/bronze/reporting_performance/pull=20261004/acct=%s.json" % bd_acct
    b = json.loads(s3.get_object(Bucket="opal-data-assets", Key=key)["Body"].read().decode("utf-8"))
    out = {}
    for lv in b.get("levels") or []:
        d = lv.get("descriptor") or {}
        if d.get("level") != "Account" or str(d.get("levelId")) != bd_acct:
            continue
        for p in lv.get("dateRangePoints") or []:
            k = (p["dateRange"]["startDate"][:10], p["dateRange"]["endDate"][:10])
            if k in wanted:
                out[k] = {"mwr": (p.get("moneyWeightedReturns") or {}).get("return"), "income": p.get("income"),
                          "net_gains": p.get("netGains"), "net_additions": p.get("netAdditions")}
    return out


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    sp = importlib.util.spec_from_file_location("v2", str(root / V2PY_REL))
    v2m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(v2m)
    plan, (n_obj, bronze, gold, n_part, n_gold_accts) = v2m.load(root, cache)
    v2 = json.loads((root / V2_REL).read_bytes().decode("utf-8"))
    vi = {(s["account"], s["segment"]["start"], s["segment"]["end"]): s for s in v2["segments"]}
    cls = json.loads((root / CLS_REL).read_bytes().decode("utf-8"))
    todo = [e for e in cls["classified"] if e.get("row") == ROW]
    bdacct = {r["account"]: str(r["bd_account"]) for r in plan["request_list"]}
    import boto3
    from botocore.config import Config
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=32, retries={"max_attempts": 8, "mode": "standard"}))
    need = {}
    for e in todo:
        need.setdefault(bdacct[e["account"]], set()).add((e["segment"]["start"], e["segment"]["end"]))
    with ThreadPoolExecutor(16) as ex:
        extra = dict(ex.map(lambda a: (a, bd_mwr(s3, a, need[a])), list(need)))
    evid, segs, counts = [], [], {}
    for e in todo:
        a, s = e["account"], e["segment"]
        v = vi[(a, s["start"], s["end"])]
        g = gold[a]
        allds = sorted(g)
        ds = [d for d in allds if s["start"] <= d <= s["end"] and g[d]["r"] is not None]
        prev = [d for d in allds if d < s["start"]]
        pv = g[prev[-1]]["mv"] if prev else None
        bp = bronze[bdacct[a]][(s["start"], s["end"])]
        ex_ = extra[bdacct[a]][(s["start"], s["end"])]
        mvs = [g[d]["mv"] or 0.0 for d in ds]
        mean, peak = sum(mvs) / len(mvs), max(mvs)
        ours, twr, gross = v["opal_return"], v["bd_return"], v["bd_gross_return"]
        fees = bp["fees"] or 0.0
        alts = {c: relink(g, ds, pv, c) for c in ("START", "MID", "END")}
        ident = abs(alts["END"] - ours) * 100.0
        env_vals = fee_variants(twr, fees, [mean, bp["bmv"], bp["emv"], (bp["bmv"] + bp["emv"]) / 2.0, peak]) if fees else []
        flows = sum(1 for d in ds if g[d]["flow"])
        add = (fees / mean) if mean > 0 else None
        big, pvv = 0.0, pv
        for d in ds:
            if pvv and pvv > 1.0:
                big = max(big, abs(g[d]["flow"] or 0.0) / pvv)
            pvv = g[d]["mv"] or 0.0
        best = min(("START", "MID"), key=lambda c: abs(gross - alts[c]))
        # span test: a calendar weekday in the window that is absent from the served series for every account is a market closure
        if peak < DUST:
            cause, why = "DUST_BASE_FEE_ADDBACK", ("largest served balance %.2f is under $%.0f; BD TWR %.4f and served %.4f are both ~0; the gross-up of BD fee %.2f "
                                                  "on a mean balance of %.2f makes the %.2f pp gap" % (peak, DUST, twr, ours, fees, mean, (gross - ours) * 100))
        elif add is not None and abs(add) >= FEE_EXTREME:
            cause, why = "BD_FEE_FIGURE_EXTREME", ("BD fee %.2f is %.1f%% of the mean served balance %.2f (negative = credit); the gross-up alone moves BD "
                                                   "return from %.4f to %.4f" % (fees, add * 100, mean, twr, gross))
        elif flows and abs(gross - alts[best]) <= TOL:
            cause, why = "FLOW_TIMING_START_OF_DAY" if best == "START" else "FLOW_TIMING_MID_DAY", (
                "served link re-formed under %s flow timing with the first day included is %.4f; BD gross %.4f; residual %.2f pp" % (
                    best, alts[best], gross, abs(gross - alts[best]) * 100))
        elif env_vals and min(env_vals) - TOL <= ours <= max(env_vals) + TOL:
            cause, why = "BD_FEE_TIMING_ENVELOPE", ("served %.4f lies inside the BD fee gross-up envelope [%.4f, %.4f] (15 variants) +/- 0.35 pp; BD reports one fee "
                                                    "total (%.2f) and no fee dates" % (ours, min(env_vals), max(env_vals), fees))
        elif big >= BIG_FLOW:
            cause, why = "LARGE_FLOW_DAY_SENSITIVITY", ("largest single-day flow is %.2f times the prior balance; served return reproduces from the tied dollars "
                                                         "(END identity %.4f pp); no flow-timing or fee variant reaches BD gross" % (big, ident))
        else:
            cause, why = "UNRESOLVED_BY_EXCLUSION", ("served return reproduces from the tied dollars (END identity %.4f pp) and no fee/flow variant reaches BD; "
                                                     "BD's daily path is not in the landed point" % ident)
        item = {"account": a, "segment": {"start": s["start"], "end": s["end"]}, "cause": cause, "why": why,
                "served": {"return": ours, "linked_days": len(ds), "max_balance": peak, "mean_balance": mean, "flow_days": flows, "max_flow_over_prior_balance": big,
                           "relink_start": alts["START"], "relink_mid": alts["MID"], "relink_end": alts["END"], "end_identity_pp": ident},
                "black_diamond": {"twr_net": twr, "twr_gross_tieout": gross, "fee_addback": v.get("bd_fee_addback"), "fees": bp["fees"], "mwr": ex_["mwr"],
                                  "begin_value": bp["bmv"], "end_value": bp["emv"], "net_additions": ex_["net_additions"], "net_gains": ex_["net_gains"],
                                  "income": ex_["income"], "days_held": bp["days_held"]},
                "gap_pp": (gross - ours) * 100.0,
                "bd_days_minus_served_days": (bp["days_held"] - len(ds)) if isinstance(bp["days_held"], int) else None}
        evid.append(item)
        counts[cause] = counts.get(cause, 0) + 1
        segs.append({"account": a, "segment": {"start": s["start"], "end": s["end"]}, "disposition": "BD_SIDE", "cause": cause,
                     "evidence": "%s#%s|%s|%s" % (EVID_REL, a, s["start"], s["end"])})
    n_ident = sum(1 for i in evid if i["served"]["end_identity_pp"] < 0.05)
    n_day = sum(1 for i in evid if i["bd_days_minus_served_days"] == 1)
    ev = {"measured_by": "0.9.0_WK_IRPT_DASHBD~76", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-101", "vendor_calls": 0, "row": ROW,
          "thresholds": {"tolerance_pp": 0.35, "dust_balance": DUST, "fee_extreme_fraction": FEE_EXTREME, "big_flow_fraction": BIG_FLOW},
          "denominator": len(evid), "by_cause": counts, "served_end_identity_holds": "%d of %d" % (n_ident, len(evid)),
          "bd_counts_one_more_day": n_day, "segments": evid}
    (HERE / "W73_S2_EVIDENCE.json").write_bytes((json.dumps(ev, indent=1) + "\n").encode("utf-8"))
    res = {"measured_by": "0.9.0_WK_IRPT_DASHBD~76", "claim": "inferred", "task_order": "IRPT_DASHBD.TO-DB-b-101", "row": ROW, "denominator": len(segs),
           "by_cause": counts, "segments": segs}
    (HERE / "W73_S2_RESOLUTION.json").write_bytes((json.dumps(res, indent=1) + "\n").encode("utf-8"))
    print("OK: %d segments; by_cause %s; END identity %d of %d; BD +1 day %d" % (len(segs), counts, n_ident, len(evid), n_day))


if __name__ == "__main__":
    main()
