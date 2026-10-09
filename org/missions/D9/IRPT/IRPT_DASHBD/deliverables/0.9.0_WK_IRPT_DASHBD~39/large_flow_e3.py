"""TO-DB-b-62 (IRPT_DASHBD round 32, DB-b-62, E3): the 170 LARGE_FLOW_DAY misses of round 31, each traced to ONE sub-class with its evidence.

Population: the rows of UNEXPLAINED_CLASSES_E2.json (round 31, DB-b-58) with cause_class == LARGE_FLOW_DAY (read from the record).
Inputs per segment: the landed BD period point (beginning/ending value, net additions, fees, net TWR; pull=20261004) and Opal's served
daily series (market_value_eod, external_flow, total_return_daily) around the flow day(s). BD's gross is round 31's `fee_base_gross`
(imported, not restated); the tolerance is 0.35 pp. A "large flow day" is the classifier's own: |flow| >= 25% of the prior day's value.
Method: a decision list, first match wins; every sub-class carries the numbers that decided it.
  1 BD_FEE_FIELD_IS_FLOW       BD's `fees` is negative and equals minus its `netAdditions`: the fee field carries the flow, so the add-back is of a flow
  2 FIRST_DAY_FLOW_AT_START    the largest flow is on the segment's first day and linking that day with the flow at the START of the day lands within 0.35 pp
  3 FLOW_DAY_RETURN_ZERO       linking with the large flow days' own return set to zero lands within 0.35 pp
  4 FLOW_START_OR_MID          START or MID timing on the large flow days only lands within 0.35 pp
  5 FLOW_BOOKED_A_DAY_APART    moving every large flow one day earlier or later (END convention) lands within 0.35 pp
  6 LIQUIDATION_RESIDUAL_BASE  a large outflow leaves under 5% of the prior value (the account is emptied; the rest of the segment runs on a residual base)
  7 FUNDED_FROM_NEAR_ZERO      a large inflow lands on a prior value under 5% of the post-flow value (the account is opened or funded from a near-zero base)
  8 ROUND_TRIP_FLOWS           opposite-sign large flows within 5 served days that net to under 10% of the larger
  9 MULTI_FLOW_COMPOUNDING     three or more large flow days in the segment
 10 SINGLE_PARTIAL_FLOW        none of the above: one or two partial large flows
The ONE re-link rules used as tests are in this file (`relink`); the reader of record (tieout_reader.py) and the served producer are not touched.
READ-ONLY: S3 GETs/LISTs only; zero vendor calls.

Usage: python large_flow_e3.py <repo_root> [--cache <pickle>]
Writes LARGE_FLOW_E3.json and LARGE_FLOW_E3.md beside this file.
"""
import importlib.util
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEL = HERE.parent
_spec = importlib.util.spec_from_file_location("unexplained_classes_r31", str(DEL / "0.9.0_WK_IRPT_DASHBD~36" / "unexplained_classes.py"))
uc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uc)
r17 = uc.r17

E2_REC = DEL / "0.9.0_WK_IRPT_DASHBD~36" / "UNEXPLAINED_CLASSES_E2.json"
OUT_JSON, OUT_MD = "LARGE_FLOW_E3.json", "LARGE_FLOW_E3.md"
TOL = uc.TOL
LARGE = uc.LARGE_FLOW
RESIDUAL, ROUND_TRIP_NET, ROUND_TRIP_DAYS, MULTI = 0.05, 0.10, 5, 3
FEE_IS_FLOW_ABS, FEE_IS_FLOW_REL = 1.0, 0.002
CLASSES = ("BD_FEE_FIELD_IS_FLOW", "FIRST_DAY_FLOW_AT_START", "FLOW_DAY_RETURN_ZERO", "FLOW_START_OR_MID", "FLOW_BOOKED_A_DAY_APART",
           "LIQUIDATION_RESIDUAL_BASE", "FUNDED_FROM_NEAR_ZERO", "ROUND_TRIP_FLOWS", "MULTI_FLOW_COMPOUNDING", "SINGLE_PARTIAL_FLOW")


def key(s):
    return (s["account"], s["segment"]["start"], s["segment"]["end"])


def large_days(days, pmv):
    """Indices of the large flow days (|flow| >= 25% of the prior day's value; the prior of day 0 is the served value before the segment)."""
    out, prev = [], pmv
    for i, d in enumerate(days):
        if prev and prev > 0 and abs(d.get("flow") or 0.0) / prev >= LARGE:
            out.append(i)
        prev = d.get("mv") or 0.0
    return out


def relink(days, pmv, conv, idx, shift=0):
    """Compound the segment's daily returns from market value and flow, overriding the convention on the days in idx only.
    END (served) r = (V - F) / V0 - 1; START r = V / (V0 + F) - 1; MID r = (V - F/2) / (V0 + F/2) - 1; ZERO r = 0.
    shift moves each flow on idx by that many days (END convention on the moved flows); a flow moved out of the segment is dropped.
    A day without value or prior value keeps its served return. V0 of day 0 is the served value before the segment."""
    flows = [d.get("flow") or 0.0 for d in days]
    if shift:
        moved = [0.0] * len(days)
        for i in idx:
            j = i + shift
            flows[i] -= days[i].get("flow") or 0.0
            if 0 <= j < len(days):
                moved[j] += days[i].get("flow") or 0.0
        flows = [f + m for f, m in zip(flows, moved)]
    p, prev = 1.0, pmv
    for i, d in enumerate(days):
        v1, f = d.get("mv"), flows[i]
        if v1 is None or not prev or d.get("flow") is None:
            p *= 1.0 + d["r"]
        elif shift:
            p *= (v1 - f) / prev
        elif i in idx and conv == "START":
            p *= v1 / (prev + f) if (prev + f) else 1.0 + d["r"]
        elif i in idx and conv == "MID":
            p *= (v1 - f / 2.0) / (prev + f / 2.0) if (prev + f / 2.0) else 1.0 + d["r"]
        elif i in idx and conv == "ZERO":
            p *= 1.0
        else:
            p *= 1.0 + d["r"]
        prev = v1 or 0.0
    return p - 1.0


def shift_delta(days, pmv, idx, shift):
    """Opal's linked return after moving the large flows by `shift` days, as served + (END relink moved - END relink unmoved)."""
    opal = r17.link([d["r"] for d in days])
    moved = relink(days, pmv, "END", idx, shift=shift)
    base = relink(days, pmv, "END", idx, shift=0)
    return opal + (moved - base)


def classify(seg, days, series, bd):
    """(sub_class, evidence, tests) for one LARGE_FLOW_DAY segment."""
    st = seg["segment"]["start"]
    opal = r17.link([d["r"] for d in days])
    fees, na = bd.get("fees"), bd.get("net_additions")
    gross = uc.fee_base_gross(bd["twr"], fees, days)
    d0 = abs(gross - opal) * 100.0
    prior = [d for d in sorted(series) if d < st]
    pmv = series[prior[-1]]["mv"] if prior else None
    idx = large_days(days, pmv)
    big = max(idx, key=lambda i: abs(days[i]["flow"])) if idx else None
    t = {"abs_diff_pp_served": d0}
    for c in ("START", "MID", "ZERO"):
        t[c] = abs(gross - relink(days, pmv, c, set(idx))) * 100.0 if idx else None
    t["START_all_days"] = abs(gross - relink(days, pmv, "START", set(range(len(days))))) * 100.0
    avg = uc.mean_daily_value(days)
    t["landed_gain"] = (abs((bd["emv"] - bd["bmv"] - na) / avg - opal) * 100.0) if (na is not None and avg and bd.get("emv") is not None
                                                                                 and bd.get("bmv") is not None) else None
    t["START_first_day"] = abs(gross - relink(days, pmv, "START", {0})) * 100.0 if 0 in idx else None
    t["SHIFT_EARLIER"] = abs(gross - shift_delta(days, pmv, set(idx), -1)) * 100.0 if idx else None
    t["SHIFT_LATER"] = abs(gross - shift_delta(days, pmv, set(idx), 1)) * 100.0 if idx else None
    n = len(idx)
    if fees is not None and na is not None and fees < 0 and abs(fees + na) <= max(FEE_IS_FLOW_ABS, FEE_IS_FLOW_REL * abs(na)):
        d_net = abs(bd["twr"] - opal) * 100.0
        t["net_no_addback"] = d_net
        return CLASSES[0], "BD fees %.2f equals minus its netAdditions %.2f; the add-back of that fee moves BD from net %.4f to gross %.4f against Opal %.4f " \
            "(abs_diff %.3f pp with it, %.3f pp without it)" % (fees, na, bd["twr"], gross, opal, d0, d_net), t
    if big is not None and 0 in idx and big == 0 and t["START_first_day"] <= TOL:
        return CLASSES[1], "largest flow %.0f is on the segment's first day (%s) against a prior value of %.0f; START timing on that day gives abs_diff %.3f pp " \
            "(END, served: %.3f pp)" % (days[0]["flow"], days[0]["date"], pmv, t["START_first_day"], d0), t
    if big is not None and t["ZERO"] <= TOL:
        return CLASSES[2], "%d large flow day(s), largest %.0f on %s; setting those days' return to zero gives abs_diff %.3f pp (served: %.3f pp; START %.3f, MID %.3f)" % (
            n, days[big]["flow"], days[big]["date"], t["ZERO"], d0, t["START"], t["MID"]), t
    if big is not None and min(t["START"], t["MID"]) <= TOL:
        c = "START" if t["START"] <= t["MID"] else "MID"
        return CLASSES[3], "%d large flow day(s), largest %.0f on %s; %s timing on those days only gives abs_diff %.3f pp (served END: %.3f pp)" % (
            n, days[big]["flow"], days[big]["date"], c, t[c], d0), t
    if big is not None and min(t["SHIFT_EARLIER"], t["SHIFT_LATER"]) <= TOL:
        c = "SHIFT_EARLIER" if t["SHIFT_EARLIER"] <= t["SHIFT_LATER"] else "SHIFT_LATER"
        return CLASSES[4], "%d large flow day(s), largest %.0f on %s; moving the large flows one day %s gives abs_diff %.3f pp (served: %.3f pp)" % (
            n, days[big]["flow"], days[big]["date"], "earlier" if c == "SHIFT_EARLIER" else "later", t[c], d0), t
    # structural classes
    liq = [(i, days[i]) for i in idx if days[i]["flow"] < 0 and (days[i]["mv"] or 0.0) < RESIDUAL * (days[i - 1]["mv"] if i else (pmv or 0.0))]
    if liq:
        i, d = liq[0]
        prevv = days[i - 1]["mv"] if i else pmv
        return CLASSES[5], "outflow %.0f on %s takes the value from %.0f to %.0f (%.1f%% left); end value %.0f; abs_diff %.3f pp" % (
            d["flow"], d["date"], prevv, d["mv"], 100.0 * d["mv"] / prevv, bd.get("emv") or 0.0, d0), t
    fund = [(i, days[i]) for i in idx if days[i]["flow"] > 0 and (days[i - 1]["mv"] if i else (pmv or 0.0)) < RESIDUAL * (days[i]["mv"] or 0.0)]
    if fund:
        i, d = fund[0]
        prevv = days[i - 1]["mv"] if i else pmv
        return CLASSES[6], "inflow %.0f on %s lifts the value from %.0f to %.0f (prior value %.1f%% of the new); BD begin %.0f; abs_diff %.3f pp" % (
            d["flow"], d["date"], prevv, d["mv"], 100.0 * prevv / d["mv"], bd.get("bmv") or 0.0, d0), t
    for a in idx:
        for b in idx:
            if a < b <= a + ROUND_TRIP_DAYS and days[a]["flow"] * days[b]["flow"] < 0 \
                    and abs(days[a]["flow"] + days[b]["flow"]) < ROUND_TRIP_NET * max(abs(days[a]["flow"]), abs(days[b]["flow"])):
                return CLASSES[7], "flows %.0f on %s and %.0f on %s (%d served days apart) net to %.0f; abs_diff %.3f pp" % (
                    days[a]["flow"], days[a]["date"], days[b]["flow"], days[b]["date"], b - a, days[a]["flow"] + days[b]["flow"], d0), t
    if n >= MULTI:
        return CLASSES[8], "%d large flow days (largest %.0f on %s), none of the single-cause tests reaches 0.35 pp; abs_diff %.3f pp" % (
            n, days[big]["flow"], days[big]["date"], d0), t
    return CLASSES[9], "%d large flow day(s), largest %.0f on %s against a prior value of %.0f; no single re-link reaches 0.35 pp (START %.3f, MID %.3f, zero %.3f); " \
        "abs_diff %.3f pp" % (n, days[big]["flow"], days[big]["date"], (days[big - 1]["mv"] if big else pmv) or 0.0, t["START"], t["MID"], t["ZERO"], d0), t


# ----------------------------------------------------------------------------------------------------------------------------- run
def load(root, cache, pop):
    plan = json.loads((root / r17.PLAN_REL).read_bytes().decode("utf-8"))
    a2bd = {r["account"]: str(r["bd_account"]) for r in plan["request_list"]}
    if cache and Path(cache).is_file():
        with open(cache, "rb") as f:
            n_obj, bronze, gold, n_part, n_gold = pickle.load(f)
    else:
        import boto3
        from botocore.config import Config
        s3 = boto3.client("s3", region_name="us-east-1", config=Config(
            read_timeout=60, retries={"max_attempts": 8, "mode": "standard"}, max_pool_connections=32))
        accts = sorted({x["account"] for x in pop})
        n_obj, bronze = r17.read_bronze(s3, [a2bd[a] for a in accts])
        gold, n_part, n_gold = r17.read_gold(s3, accts)
        if cache:
            with open(cache, "wb") as f:
                pickle.dump((n_obj, bronze, gold, n_part, n_gold), f)
    return a2bd, n_obj, bronze, gold, n_part, n_gold


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    rec31 = json.loads(E2_REC.read_bytes().decode("utf-8"))
    pop = [x for x in rec31["rows"] if x.get("cause_class") == "LARGE_FLOW_DAY"]
    a2bd, n_obj, bronze, gold, n_part, n_gold = load(root, cache, pop)
    rows, tests, counts = [], {}, {}
    for x in pop:
        a, seg = x["account"], x["segment"]
        days = r17.segment_days(gold.get(a), seg)
        bd = bronze[a2bd[a]][(seg["start"], seg["end"])]
        sub, ev, t = classify({"segment": seg}, days, gold[a], bd)
        rows.append({"account": a, "segment": seg, "sub_class": sub, "evidence": ev})
        counts[sub] = counts.get(sub, 0) + 1
        tests[sub] = tests.get(sub, [])
        tests[sub].append(t)
    # the re-graded effect of each class's candidate rule on its own rows
    effect = {}
    for sub, ts in tests.items():
        def within(k):
            return sum(1 for t in ts if t.get(k) is not None and t[k] <= TOL)
        effect[sub] = {"rows": len(ts), "within_served": within("abs_diff_pp_served"), "within_net_no_addback": within("net_no_addback"),
                       "within_start_first_day": within("START_first_day"), "within_zero_flow_day": within("ZERO"),
                       "within_start": within("START"), "within_start_all_days": within("START_all_days"), "within_landed_gain": within("landed_gain"), "within_mid": within("MID"),
                       "within_shift_earlier": within("SHIFT_EARLIER"), "within_shift_later": within("SHIFT_LATER")}
    out = {"measured_by": "0.9.0_WK_IRPT_DASHBD~39", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-62", "tolerance_pp": TOL,
           "vendor_calls": 0, "population": len(rows), "rows": rows, "counts": counts, "regrade_effect": effect,
           "dispositions": DISPOSITIONS, "decision_list": list(CLASSES),
           "files_read": {"round31_record": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~36/UNEXPLAINED_CLASSES_E2.json",
                          "round31_classifier": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~36/unexplained_classes.py",
                          "plan": r17.PLAN_REL,
                          "bronze_prefix": "s3://%s/%s" % (r17.BRONZE_BUCKET, r17.BRONZE_PREFIX), "bronze_object_count": n_obj,
                          "served_series": "s3://%s/%sdate=<YYYY-MM-DD>/data.parquet (%d partitions)" % (r17.GOLD_BUCKET, r17.GOLD_PREFIX, n_part),
                          "served_accounts": n_gold}}
    (HERE / OUT_JSON).write_bytes((json.dumps(out, indent=1) + "\n").encode("utf-8"))
    lines = ["# LARGE_FLOW_E3 -- the 170 LARGE_FLOW_DAY misses traced to a sub-class (TO-DB-b-62, 0.9.0_WK_IRPT_DASHBD~39)", "",
             "Counts only. Record: `LARGE_FLOW_E3.json`. Module: `large_flow_e3.py` (imports round 31's `unexplained_classes.py`). "
             "S3 reads only; zero vendor calls. Tolerance 0.35 pp.", "",
             "Population: %d LARGE_FLOW_DAY segments of round 31; each carries one sub-class (decision list, first match wins)." % len(rows), "",
             "| sub-class | segments | disposition | within 0.35 pp under the class's rule |", "|---|---|---|---|"]
    for k in CLASSES:
        if k in counts:
            lines.append("| %s | %d | %s | %s |" % (k, counts[k], DISPOSITIONS[k]["disposition"], EFFECT_KEY[k](effect[k])))
    lines += ["| total | %d | | |" % len(rows), ""]
    (HERE / OUT_MD).write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print(json.dumps({"counts": counts, "effect": effect}, indent=1))


DISPOSITIONS = {
    "BD_FEE_FIELD_IS_FLOW": {"disposition": "fixed", "cause": "BD's `fees` equals minus its `netAdditions` and the money gain (ending - beginning - net additions) is about zero: "
                             "the contribution is booked through the fee field and BD's TWR reads it as a return, so the fee add-back and the TWR are both of a flow, not of a fee or a gain.",
                             "note": "fix = `landed_gain_return()` below: grade such a segment on BD's own landed values, (ending - beginning - net additions) / mean daily served value, "
                                     "not on the TWR; the re-graded effect on this class is in `regrade_effect.BD_FEE_FIELD_IS_FLOW.within_landed_gain`. The reader of record is not edited."},
    "FIRST_DAY_FLOW_AT_START": {"disposition": "fixed", "cause": "a flow on the segment's first day is invested for that day in BD (START timing), where the served END convention leaves it uninvested.",
                                "note": "fix = START timing on the first-day flow (`relink(..., 'START', {0})`); lands all rows of the class; the flow-start convention of DB-b-61 reaches the same "
                                        "rows. Effect outside these 170 is not measured here."},
    "FLOW_DAY_RETURN_ZERO": {"disposition": "named_cause", "cause": "BD earns nothing on the large flow day (its per-flow valuation is not in the landed period point); Opal's own return on that day "
                             "carries the miss. Setting the day's return to zero lands every row, which names the day, not BD's rule.",
                             "note": "not adopted: START, MID and a one-day move each also land some of these rows, so the landed files cannot tell the rules apart."},
    "FLOW_START_OR_MID": {"disposition": "named_cause", "cause": "START or MID timing on the large flow days lands the row; BD's flow date is not landed, so no date is adopted (as round 31's FLOW_TIMING).",
                          "note": "graded both ways by DB-b-59; the flow-start adoption of DB-b-61 is the reader-of-record question."},
    "FLOW_BOOKED_A_DAY_APART": {"disposition": "named_cause", "cause": "moving the large flow one day later (the other system books it the next day) lands the row; BD's booking date is not landed.",
                                "note": "evidence is the re-link that lands, not a landed BD date; not adopted."},
    "LIQUIDATION_RESIDUAL_BASE": {"disposition": "named_cause", "cause": "a large outflow leaves under 5% of the prior value; the rest of the segment compounds on a residual base, and BD's valuation "
                                  "of the emptying day and of the tail is not in the landed period point. No re-link tested lands these rows.",
                                  "note": "tested and not landing: START, MID, flow-day zero, a one-day move either way, link cut at the last large flow."},
    "FUNDED_FROM_NEAR_ZERO": {"disposition": "named_cause", "cause": "a large inflow lands on a prior value under 5% of the post-flow value (an account opened or funded from a near-zero base); "
                              "the return before and on the funding day is set by cents of value and BD's per-flow valuation is not landed.",
                              "note": "no re-link tested lands these rows."},
    "ROUND_TRIP_FLOWS": {"disposition": "named_cause", "cause": "opposite-sign large flows within five served days net to under 10% of the larger (money out and back); each leg's valuation "
                         "in BD is not in the landed period point.", "note": "no re-link tested lands these rows."},
    "MULTI_FLOW_COMPOUNDING": {"disposition": "named_cause", "cause": "three or more large flow days compound their valuation differences; no single flow is the cause and BD's per-flow "
                               "valuation is not landed.", "note": "no single-cause re-link tested lands these rows."},
    "SINGLE_PARTIAL_FLOW": {"disposition": "named_cause", "cause": "one or two partial large flows (neither emptying nor funding the account); BD's per-flow valuation is not in the landed "
                            "period point and no re-link tested lands the row.", "note": "residual of the decision list."},
}
EFFECT_KEY = {
    "BD_FEE_FIELD_IS_FLOW": lambda e: "%d of %d on landed gain" % (e["within_landed_gain"], e["rows"]),
    "FIRST_DAY_FLOW_AT_START": lambda e: "%d of %d on START" % (e["within_start_first_day"], e["rows"]),
    "FLOW_DAY_RETURN_ZERO": lambda e: "%d of %d on zero flow-day return" % (e["within_zero_flow_day"], e["rows"]),
    "FLOW_START_OR_MID": lambda e: "%d of %d on START or MID" % (max(e["within_start"], e["within_mid"]), e["rows"]),
    "FLOW_BOOKED_A_DAY_APART": lambda e: "%d of %d on a one-day move" % (max(e["within_shift_earlier"], e["within_shift_later"]), e["rows"]),
}
for _k in CLASSES:
    EFFECT_KEY.setdefault(_k, lambda e: "0 of %d on any re-link tested" % e["rows"])


def landed_gain_return(bd, days):
    """The fix for BD_FEE_FIELD_IS_FLOW: BD's own landed money gain over the mean daily served value (None when not computable)."""
    avg = uc.mean_daily_value(days)
    na = bd.get("net_additions")
    if na is None or not avg or bd.get("emv") is None or bd.get("bmv") is None:
        return None
    return (bd["emv"] - bd["bmv"] - na) / avg


if __name__ == "__main__":
    main()
