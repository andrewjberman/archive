"""TO-DB-b-65 (IRPT_DASHBD round 33, DB-b-65, E3): the 153 NEAR_ZERO_BALANCE misses of round 31, each traced to ONE sub-class with its evidence.

Population: the rows of UNEXPLAINED_CLASSES_E2.json (round 31, DB-b-58) with cause_class == NEAR_ZERO_BALANCE (read from the record).
Inputs per segment: the landed BD period point (beginning/ending value, net additions, fees, net TWR; pull=20261004) and Opal's served daily
series (market_value_eod, external_flow, total_return_daily). BD's gross is the reader of record's `fee_base_gross` (not restated); the
tolerance is 0.35 pp. "Near zero" is the project's own boundary: BD's beginning or ending value under 2% of the segment's mean daily served
value (reader GUARD_FRAC = classifier NEAR_ZERO_BOUNDARY), or a served daily value under 1% of it.
Method: a decision list, first match wins; every sub-class carries the numbers that decided it.
  1 BD_FEE_FIELD_IS_FLOW         BD `fees` is negative and equals minus its `netAdditions` (round 32's rule, restated in `fee_is_flow`)
  2 GAIN_AGREES_NEAR_ZERO_BASE   BD's own landed money gain, (ending - beginning - net additions) / mean daily served value, lands within 0.35 pp of
                                 Opal's served return while BD's TWR does not: the TWR is the figure the near-zero base distorts
  3 NEGATIVE_BALANCE             a served daily value is below zero
  4 BD_TWR_SATURATED             BD's net TWR is within 6 pp of +/-100% on a near-zero base
  5 NEAR_ZERO_DIVISOR_DAY        a served daily return of at least 5% on a day whose prior-day value is under 2% of the mean
  6 BD_END_NEAR_ZERO             BD's ending value is near zero, its beginning is not (emptied; a residual tail)
  7 BD_BEGIN_NEAR_ZERO           BD's beginning value is near zero, its ending is not (funded from near zero)
  8 BD_BOTH_ENDS_NEAR_ZERO       both are near zero
  9 INTERIOR_NEAR_ZERO_RUN       neither end is near zero; served daily values dip under 1% of the mean inside the segment
 10 UNTRACED_NEAR_ZERO           none of the above
The ONE fix is `landed_gain_return` below (a grade on BD's landed values; BD's TWR is not changed and nothing served moves). The reader of record
(tieout_reader.py) and the served producer are not touched.
Overlap with round 32 is MEASURED: round 32's own `classify` (large_flow_e3.py) is run on the 153 (see `overlap_round32`); the shim it needs is stated there.
READ-ONLY: S3 GETs/LISTs only; zero vendor calls.

Usage: python near_zero_e3.py <repo_root> [--cache <pickle>]
Writes NEAR_ZERO_E3.json and NEAR_ZERO_E3.md beside this file.
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEL = HERE.parent
_spec = importlib.util.spec_from_file_location("large_flow_e3_r32", str(DEL / "0.9.0_WK_IRPT_DASHBD~39" / "large_flow_e3.py"))
lf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lf)
uc, r17 = lf.uc, lf.r17
reader = uc.reader

E2_REC = DEL / "0.9.0_WK_IRPT_DASHBD~36" / "UNEXPLAINED_CLASSES_E2.json"
R32_FLOWSTART = DEL / "0.9.0_WK_IRPT_DASHBD~38" / "REGRADE_FLOWSTART_E2.json"
R32_LARGE = DEL / "0.9.0_WK_IRPT_DASHBD~39" / "LARGE_FLOW_E3.json"
OUT_JSON, OUT_MD = "NEAR_ZERO_E3.json", "NEAR_ZERO_E3.md"
TOL = reader.TOLERANCE_PP
NEAR_BOUNDARY = reader.GUARD_FRAC        # 2% of the mean daily value
NEAR_DAY = uc.NEAR_ZERO_DAY              # 1% of the mean daily value
SATURATED = 0.94
DIVISOR_R = 0.05
FEE_IS_FLOW_ABS, FEE_IS_FLOW_REL = 1.0, 0.002
CLASSES = ("BD_FEE_FIELD_IS_FLOW", "GAIN_AGREES_NEAR_ZERO_BASE", "NEGATIVE_BALANCE", "BD_TWR_SATURATED", "NEAR_ZERO_DIVISOR_DAY",
           "BD_END_NEAR_ZERO", "BD_BEGIN_NEAR_ZERO", "BD_BOTH_ENDS_NEAR_ZERO", "INTERIOR_NEAR_ZERO_RUN", "UNTRACED_NEAR_ZERO")


def key(s):
    return (s["account"], s["segment"]["start"], s["segment"]["end"])


# ---------------------------------------------------------------------------------------------------------------------------- the fix
def landed_gain_return(bd, days):
    """The fix for the gain-agrees classes: BD's own landed money gain over the mean daily served value (the reader of record's daily mean).
    None when not computable. A grade on BD's landed values; BD's TWR is not altered."""
    avg = reader.daily_mean_value(days)
    na = bd.get("net_additions")
    if na is None or not avg or bd.get("emv") is None or bd.get("bmv") is None:
        return None
    return (bd["emv"] - bd["bmv"] - na) / avg


def within_landed_gain(bd, days, opal):
    g = landed_gain_return(bd, days)
    return g is not None and abs(g - opal) * 100.0 <= TOL


def fee_is_flow(bd):
    fees, na = bd.get("fees"), bd.get("net_additions")
    return fees is not None and na is not None and fees < 0 and abs(fees + na) <= max(FEE_IS_FLOW_ABS, FEE_IS_FLOW_REL * abs(na))


# ---------------------------------------------------------------------------------------------------------------------------- tests
def relink_tests(days, bd, avg):
    """Candidate re-links that act on the near-zero days, each as |BD - candidate| pp against BD gross and BD net (the nearer of the two)."""
    thr = NEAR_BOUNDARY * avg
    mvs = [d["mv"] or 0.0 for d in days]
    full = [i for i, m in enumerate(mvs) if m >= thr]
    gross = reader.fee_base_gross(bd["twr"], bd.get("fees"), days)
    net = bd["twr"]

    def nearest(x):
        return None if x is None else min(abs(gross - x), abs(net - x)) * 100.0

    def link(lo, hi):
        return r17.link([d["r"] for d in days[lo:hi + 1]]) if lo <= hi else None
    f0, f1 = (full[0], full[-1]) if full else (None, None)
    zero_prior = [0.0 if (i > 0 and mvs[i - 1] < thr) else d["r"] for i, d in enumerate(days)]
    return {"first_full_day": nearest(link(f0 + 1, len(days) - 1)) if f0 is not None else None,
            "tail_cut": nearest(link(0, f1)) if f1 is not None else None,
            "first_full_to_tail_cut": nearest(link(f0 + 1, f1)) if f0 is not None else None,
            "zero_after_near_zero_prior": nearest(r17.link(zero_prior)),
            "net_no_addback": abs(net - r17.link([d["r"] for d in days])) * 100.0}


def classify(seg, days, series, bd):
    """(sub_class, evidence, tests) for one NEAR_ZERO_BALANCE segment."""
    opal = r17.link([d["r"] for d in days])
    avg = reader.daily_mean_value(days)
    fees, na = bd.get("fees"), bd.get("net_additions")
    gross = reader.fee_base_gross(bd["twr"], fees, days)
    d0 = abs(gross - opal) * 100.0
    mvs = [d["mv"] or 0.0 for d in days]
    gain = landed_gain_return(bd, days)
    bnz = (bd.get("bmv") or 0.0) < NEAR_BOUNDARY * avg
    enz = (bd.get("emv") or 0.0) < NEAR_BOUNDARY * avg
    nz_days = sum(1 for m in mvs if m < NEAR_DAY * avg)
    t = {"abs_diff_pp_served": d0, "landed_gain": (abs(gain - opal) * 100.0 if gain is not None else None),
         "guard_days": len(reader.guarded_days(days))}
    t.update(relink_tests(days, bd, avg))
    facts = "BD begin %.4f and end %.4f of the mean daily value; %d of %d served days under 1%% of it; abs_diff %.3f pp" % (
        (bd.get("bmv") or 0.0) / avg, (bd.get("emv") or 0.0) / avg, nz_days, len(days), d0)
    if fee_is_flow(bd):
        return CLASSES[0], "BD fees %.2f equals minus its netAdditions %.2f; BD begin is %.4f of the mean daily value; landed gain %.4f vs Opal %.4f " \
            "(abs_diff %.3f pp, BD TWR %.4f); %s" % (fees, na, (bd.get("bmv") or 0.0) / avg, gain if gain is not None else float("nan"), opal, t["landed_gain"] or 0.0, bd["twr"], facts), t
    if t["landed_gain"] is not None and t["landed_gain"] <= TOL:
        return CLASSES[1], "BD's landed money gain %.4f is within %.3f pp of Opal's served %.4f while BD's TWR is %.4f (abs_diff %.3f pp against BD gross); %s" % (
            gain, t["landed_gain"], opal, bd["twr"], d0, facts), t
    if min(mvs) < 0:
        i = mvs.index(min(mvs))
        return CLASSES[2], "served value goes below zero on %s (%.4f of the mean daily value); landed gain %s pp off Opal; %s" % (
            days[i]["date"], mvs[i] / avg, ("%.3f" % t["landed_gain"]) if t["landed_gain"] is not None else "n/a", facts), t
    if abs(bd["twr"]) >= SATURATED:
        return CLASSES[3], "BD net TWR %.4f is within %.0f pp of +/-100%% on a near-zero base while Opal's served return is %.4f; landed gain %s pp off Opal; %s" % (
            bd["twr"], (1.0 - SATURATED) * 100.0, opal, ("%.3f" % t["landed_gain"]) if t["landed_gain"] is not None else "n/a", facts), t
    spikes = [(i, d) for i, d in enumerate(days) if i > 0 and mvs[i - 1] < NEAR_BOUNDARY * avg and d["r"] is not None and abs(d["r"]) >= DIVISOR_R]
    if spikes:
        i, d = max(spikes, key=lambda p: abs(p[1]["r"]))
        return CLASSES[4], "%d served day(s) with |return| >= 5%% on a prior value under 2%% of the mean; largest %.4f on %s over a prior value of %.4f of the mean; %s" % (
            len(spikes), d["r"], d["date"], mvs[i - 1] / avg, facts), t
    if enz and not bnz:
        return CLASSES[5], "BD ending value is %.4f of the mean daily value (beginning %.4f); the segment ends on a residual; landed gain %s pp off Opal; %s" % (
            (bd.get("emv") or 0.0) / avg, (bd.get("bmv") or 0.0) / avg, ("%.3f" % t["landed_gain"]) if t["landed_gain"] is not None else "n/a", facts), t
    if bnz and not enz:
        return CLASSES[6], "BD beginning value is %.4f of the mean daily value (ending %.4f); the segment starts from a residual; landed gain %s pp off Opal; %s" % (
            (bd.get("bmv") or 0.0) / avg, (bd.get("emv") or 0.0) / avg, ("%.3f" % t["landed_gain"]) if t["landed_gain"] is not None else "n/a", facts), t
    if bnz and enz:
        return CLASSES[7], "BD beginning %.4f and ending %.4f are both under 2%% of the mean daily value; landed gain %s pp off Opal; %s" % (
            (bd.get("bmv") or 0.0) / avg, (bd.get("emv") or 0.0) / avg, ("%.3f" % t["landed_gain"]) if t["landed_gain"] is not None else "n/a", facts), t
    if nz_days:
        return CLASSES[8], "neither BD end is near zero but %d served day(s) are under 1%% of the mean daily value (min %.4f); landed gain %s pp off Opal; %s" % (
            nz_days, min(mvs) / avg, ("%.3f" % t["landed_gain"]) if t["landed_gain"] is not None else "n/a", facts), t
    return CLASSES[9], "no near-zero evidence at this rule set; %s" % facts, t


# ---------------------------------------------------------------------------------------------------------------------------- dispositions
DISPOSITIONS = {
    "BD_FEE_FIELD_IS_FLOW": {"disposition": "fixed", "cause": "BD's `fees` equals minus its `netAdditions` and its own money gain is about zero: a contribution into a near-zero "
                             "account is booked through the fee field, BD's TWR reads it as a return on the near-zero base, and the fee add-back of that field is of a flow. Same rule and "
                             "same cause as round 32's BD_FEE_FIELD_IS_FLOW, found here on accounts opened from cents.",
                             "note": "fix = `landed_gain_return()`: grade on BD's landed money gain over the mean daily served value; effect in `fix_effect`. BD's TWR is not changed; "
                                     "the reader of record is not edited."},
    "GAIN_AGREES_NEAR_ZERO_BASE": {"disposition": "fixed", "cause": "BD's own landed money gain agrees with Opal's served return within 0.35 pp while BD's TWR is far off: the figure "
                                   "that disagrees is BD's TWR, computed on a near-zero beginning or ending value, not the account's gain.",
                                   "note": "fix = `landed_gain_return()` (as round 32's BD_FEE_FIELD_IS_FLOW fix); lands every row of the class by construction of the class rule, so the "
                                           "evidence is the rule's own test. It grades on BD's landed values and does not explain BD's TWR."},
    "NEGATIVE_BALANCE": {"disposition": "named_cause", "cause": "a served daily value is negative; the daily return on a negative or near-zero divisor is not defined the same way in the "
                         "two systems, and BD's valuation of the negative days is not in the landed period point.", "note": "re-links and the landed-gain test tried; see `tests`."},
    "BD_TWR_SATURATED": {"disposition": "named_cause", "cause": "BD's net TWR sits within 6 pp of +/-100% on a near-zero base while Opal's served return does not; the figure is set by BD's "
                         "valuation of the funding or emptying day, which is not in the landed period point, and BD's own money gain does not land within 0.35 pp.",
                         "note": "re-links and the landed-gain test tried; see `tests`."},
    "NEAR_ZERO_DIVISOR_DAY": {"disposition": "named_cause", "cause": "Opal's served daily return is 5% or more on a day whose prior-day value is under 2% of the mean: a return on a "
                              "near-zero divisor, set by cents of value; BD's per-day valuation of those days is not landed.", "note": "re-links and the landed-gain test tried; see `tests`."},
    "BD_END_NEAR_ZERO": {"disposition": "named_cause", "cause": "BD's ending value is under 2% of the mean daily value (the account is emptied; the tail runs on a residual); BD's valuation "
                         "of the emptying day and of the tail is not in the landed period point. Same shape as round 32's LIQUIDATION_RESIDUAL_BASE.",
                         "note": "re-links and the landed-gain test tried; see `tests`."},
    "BD_BEGIN_NEAR_ZERO": {"disposition": "named_cause", "cause": "BD's beginning value is under 2% of the mean daily value (the account is funded from a residual); BD's valuation of the "
                           "funding day is not in the landed period point. Same shape as round 32's FUNDED_FROM_NEAR_ZERO.",
                           "note": "re-links and the landed-gain test tried; see `tests`."},
    "BD_BOTH_ENDS_NEAR_ZERO": {"disposition": "named_cause", "cause": "both of BD's boundary values are under 2% of the mean daily value; every day's return is on a near-zero base "
                               "and BD's per-day valuation is not landed.", "note": "re-links and the landed-gain test tried; see `tests`."},
    "INTERIOR_NEAR_ZERO_RUN": {"disposition": "named_cause", "cause": "served daily values dip under 1% of the mean inside the segment while BD's boundaries are not near zero; the "
                               "compounded return through the dip is set by cents of value and BD's valuation of those days is not landed.",
                               "note": "re-links and the landed-gain test tried; see `tests`."},
    "UNTRACED_NEAR_ZERO": {"disposition": "named_cause", "cause": "no rule of the decision list matched; the round 31 near-zero rule matched on a number the sub-class rules do not use.",
                           "note": "residual of the decision list."},
}


# ---------------------------------------------------------------------------------------------------------------------------- run
def _shim_round32():
    """round 32's classify calls `uc.mean_daily_value`, a name round 32's reader promotion (DB-b-60) removed from the round 31 module (it is
    `daily_mean_value` now). The shim restores the name so round 32's classify can be RUN here; its effect is controlled in `main` by re-running
    classify on round 32's own 170 rows and comparing to LARGE_FLOW_E3.json's counts."""
    if not hasattr(uc, "mean_daily_value"):
        uc.mean_daily_value = uc.daily_mean_value
        return True
    return False


def _within(ts, k):
    return sum(1 for t in ts if t.get(k) is not None and t[k] <= TOL)


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    rec31 = json.loads(E2_REC.read_bytes().decode("utf-8"))
    pop = [x for x in rec31["rows"] if x.get("cause_class") == "NEAR_ZERO_BALANCE"]
    r32_large = json.loads(R32_LARGE.read_bytes().decode("utf-8"))
    r32_pop = [x for x in rec31["rows"] if x.get("cause_class") == "LARGE_FLOW_DAY"]
    a2bd, n_obj, bronze, gold, n_part, n_gold = lf.load(root, cache, pop + r32_pop)
    shimmed = _shim_round32()
    # control: round 32's classify, re-run on its own 170 rows, reproduces its recorded counts
    ctl = {}
    for x in r32_pop:
        a, seg = x["account"], x["segment"]
        days = r17.segment_days(gold.get(a), seg)
        bd = bronze[a2bd[a]][(seg["start"], seg["end"])]
        sub = lf.classify({"segment": seg}, days, gold[a], bd)[0]
        ctl[sub] = ctl.get(sub, 0) + 1
    control_ok = ctl == r32_large["counts"]
    rows, tests, counts, r32_sub = [], {}, {}, {}
    cross = {}
    for x in pop:
        a, seg = x["account"], x["segment"]
        days = r17.segment_days(gold.get(a), seg)
        bd = bronze[a2bd[a]][(seg["start"], seg["end"])]
        sub, ev, t = classify({"segment": seg}, days, gold[a], bd)
        rows.append({"account": a, "segment": seg, "sub_class": sub, "evidence": ev})
        counts[sub] = counts.get(sub, 0) + 1
        tests.setdefault(sub, []).append(t)
        r32s = lf.classify({"segment": seg}, days, gold[a], bd)[0]
        r32_sub[r32s] = r32_sub.get(r32s, 0) + 1
        cross.setdefault(sub, {})
        cross[sub][r32s] = cross[sub].get(r32s, 0) + 1
    # overlap with round 32's flow-start in-to-out list and its LARGE_FLOW_DAY rows
    rec_fs = json.loads(R32_FLOWSTART.read_bytes().decode("utf-8"))
    i2o = {key(s) for s in rec_fs["in_to_out"]}
    large_keys = {key(x) for x in r32_pop}
    seg_fs = {key(s): s for s in rec_fs["segments"]}
    pop_keys = {key(x) for x in pop}
    overlap = {"in_to_out_of_round32": len(pop_keys & i2o), "in_to_out_size": len(i2o),
               "large_flow_day_rows_of_round32": len(pop_keys & large_keys), "large_flow_day_size": len(large_keys),
               "outside_under_flow_start_round32": sum(1 for k in pop_keys if seg_fs.get(k, {}).get("verdict") == "OUTSIDE"),
               "graded_in_round32_flowstart": sum(1 for k in pop_keys if k in seg_fs),
               "round32_classify_on_these_153": r32_sub, "crosstab_sub_class_by_round32_class": cross,
               "shim": {"applied": shimmed, "what": "uc.mean_daily_value := uc.daily_mean_value (name removed from round 31's module by round 32's reader promotion)",
                        "control_round32_counts_reproduced": control_ok, "control_counts": ctl, "recorded_counts": r32_large["counts"]}}
    # the fix effect
    fix_rows = [c for c in CLASSES if c in counts and DISPOSITIONS[c]["disposition"] == "fixed"]
    effect = {c: {"rows": counts[c], "within_landed_gain": _within(tests[c], "landed_gain"), "within_served_gross_before": _within(tests[c], "abs_diff_pp_served")}
              for c in fix_rows}
    fix_effect = {"module": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~42/near_zero_e3.py", "function": "landed_gain_return",
                  "per_class": effect, "rows_moved_to_within": sum(e["within_landed_gain"] for e in effect.values()), "of": len(rows),
                  "scope": "these %d rows only; nothing served moves; BD's TWR is not changed; the reader of record is not edited" % len(rows)}
    for c in fix_rows:                 # a class dispositioned fixed must land every row of it
        assert effect[c]["within_landed_gain"] == counts[c], (c, effect[c])
    named = {}
    for c in counts:
        if DISPOSITIONS[c]["disposition"] == "named_cause":
            ts = tests[c]
            named[c] = {"rows": len(ts), "within_landed_gain": _within(ts, "landed_gain"), "within_first_full_day": _within(ts, "first_full_day"),
                        "within_tail_cut": _within(ts, "tail_cut"), "within_first_full_to_tail_cut": _within(ts, "first_full_to_tail_cut"),
                        "within_zero_after_near_zero_prior": _within(ts, "zero_after_near_zero_prior")}
    dispositions = {}
    for c in counts:
        d = dict(DISPOSITIONS[c])
        if c in named:
            n = named[c]
            d["note"] = "tested and not adopted: within 0.35 pp on %d of %d rows by the landed gain, %d first-full-day link, %d tail-cut link, %d both cuts, %d zero-after-near-zero-prior " \
                        "link; no test lands the whole class, so none is adopted." % (n["within_landed_gain"], n["rows"], n["within_first_full_day"], n["within_tail_cut"],
                                                             n["within_first_full_to_tail_cut"], n["within_zero_after_near_zero_prior"])
        dispositions[c] = d
    guard_rows = sum(1 for c in tests for t in tests[c] if t["guard_days"])
    out = {"measured_by": "0.9.0_WK_IRPT_DASHBD~42", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-65", "tolerance_pp": TOL, "vendor_calls": 0,
           "population": len(rows), "rows": rows, "counts": counts, "dispositions": dispositions, "fix_effect": fix_effect, "tests_named": named,
           "overlap_round32": overlap, "rows_with_a_flow_start_guard_day": guard_rows, "decision_list": list(CLASSES),
           "files_read": {"round31_record": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~36/UNEXPLAINED_CLASSES_E2.json",
                          "reader_of_record": "org/missions/D9/IRPT/IRPT_DASHBD/tieout/tieout_reader.py",
                          "round32_flowstart_record": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~38/REGRADE_FLOWSTART_E2.json",
                          "round32_large_flow_record": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~39/LARGE_FLOW_E3.json",
                          "round32_classifier": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~39/large_flow_e3.py",
                          "plan": r17.PLAN_REL,
                          "bronze_prefix": "s3://%s/%s" % (r17.BRONZE_BUCKET, r17.BRONZE_PREFIX), "bronze_object_count": n_obj,
                          "served_series": "s3://%s/%sdate=<YYYY-MM-DD>/data.parquet (%d partitions)" % (r17.GOLD_BUCKET, r17.GOLD_PREFIX, n_part),
                          "served_accounts": n_gold}}
    (HERE / OUT_JSON).write_bytes((json.dumps(out, indent=1) + "\n").encode("utf-8"))
    lines = ["# NEAR_ZERO_E3 -- the %d NEAR_ZERO_BALANCE misses traced to a sub-class (TO-DB-b-65, 0.9.0_WK_IRPT_DASHBD~42)" % len(rows), "",
             "Counts only. Record: `NEAR_ZERO_E3.json`. Module: `near_zero_e3.py` (imports round 32's `large_flow_e3.py` and the reader of record). "
             "S3 reads only; zero vendor calls. Tolerance 0.35 pp.", "",
             "Population: %d NEAR_ZERO_BALANCE segments of round 31; each carries one sub-class (decision list, first match wins)." % len(rows), "",
             "| sub-class | segments | disposition |", "|---|---|---|"]
    for k in CLASSES:
        if k in counts:
            lines.append("| %s | %d | %s |" % (k, counts[k], dispositions[k]["disposition"]))
    lines += ["| total | %d | |" % len(rows), "",
              "Fix (`landed_gain_return`, BD's landed money gain over the mean daily served value): %d of %d rows move to within 0.35 pp (%s). "
              "BD's TWR is not changed; nothing served moves." % (fix_effect["rows_moved_to_within"], len(rows),
                                                                   ", ".join("%s %d of %d" % (c, e["within_landed_gain"], e["rows"]) for c, e in effect.items())), "",
              "Overlap with round 32: %d of %d in the flow-start in-to-out list (%d); %d of the %d LARGE_FLOW_DAY rows; all %d of the %d graded in the flow-start record are OUTSIDE there too." % (
                  overlap["in_to_out_of_round32"], len(rows), overlap["in_to_out_size"], overlap["large_flow_day_rows_of_round32"], overlap["large_flow_day_size"],
                  overlap["outside_under_flow_start_round32"], overlap["graded_in_round32_flowstart"]),
              "Round 32's own classifier, run on these %d: %s (control on its 170 rows reproduces its recorded counts: %s)." % (
                  len(rows), ", ".join("%s %d" % (k, v) for k, v in sorted(r32_sub.items(), key=lambda kv: (-kv[1], kv[0]))), control_ok),
              "Rows with a flow-start guard day: %d of %d." % (guard_rows, len(rows)), ""]
    (HERE / OUT_MD).write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print(json.dumps({"counts": counts, "fix": fix_effect, "named": named, "overlap": {k: v for k, v in overlap.items() if k != "crosstab_sub_class_by_round32_class"},
                      "cross": cross, "guard_rows": guard_rows}, indent=1))


if __name__ == "__main__":
    main()
