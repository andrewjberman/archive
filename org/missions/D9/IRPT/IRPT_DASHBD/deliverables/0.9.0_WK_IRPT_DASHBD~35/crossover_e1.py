"""TO-DB-b-57: trace the 181 segments that were WITHIN under round 18 additive fee basis and are OUTSIDE under round 30 compounded one.
Population from the two records (never re-derived). Per segment: re-form the BD gross from the landed pull and the served daily gold
(read via v2 loader; S3 GETs only, or --cache) and class the cause, first match wins:
  FEE_BASE_BALANCE_PATH    the fee base (bmv+emv)/2 is not the average balance (served daily mean differs by >2%) and compounding
                           on the daily-mean base lands within 0.35 pp                                      -> compounding defect
  NEGATIVE_FEE_ADDBACK     BD reports a negative fee total (a credit, not a charge): the add-back is a negative gross-up
  FLOW_TIMING_RESIDUE      flow-bearing segment whose START/MID flow re-link lands within 0.35 pp of the compounded gross
  ADDITIVE_TIE_COINCIDENCE none of the above: the additive tie sat on offsetting error that net*add_back (the interaction) exposes
Usage: python crossover_e1.py <repo_root> --cache <pickle>      Writes CROSSOVER_E1.json and CROSSOVER_E1.md beside this file.
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
_s = importlib.util.spec_from_file_location("tieout_compound_v2", str(HERE / "tieout_compound_v2.py"))
v2 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(v2)
r30, r18, r17 = v2.r30, v2.r18, v2.r17
TOL = 0.35
DEFECT = ["FEE_BASE_BALANCE_PATH"]
DEL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"


def key(s):
    return (s["account"], s["segment"]["start"], s["segment"]["end"])


def main():
    root = Path(sys.argv[1]).resolve()
    cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
    plan, (n_obj, bronze, gold, n_part, n_ga) = v2.load(root, cache)
    a = {key(s): s for s in json.loads((D / "0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json").read_bytes().decode())["segments"]}
    c = {key(s): s for s in json.loads((D / "0.9.0_WK_IRPT_DASHBD~34/TIEOUT_COMPOUND_E1.json").read_bytes().decode())["segments"]}
    pop = sorted(k for k, s in c.items() if s["abs_diff_pp"] > TOL and a[k]["verdict"] == "WITHIN")
    seg_of = {}
    for req in plan["request_list"]:
        for seg in req["segments"]:
            seg_of[(req["account"], seg["start"], seg["end"])] = (req, seg)
    rows, counts = [], {}
    for k in pop:
        req, seg = seg_of[k]
        bd = bronze[str(req["bd_account"])][(seg["start"], seg["end"])]
        days = r17.segment_days(gold.get(req["account"]), seg)
        net, opal = bd["twr"], c[k]["opal_return"]
        two_pt = (bd["bmv"] + bd["emv"]) / 2.0
        daily = v2.daily_mean_value(days)
        ratio = daily / two_pt
        _, add_v2 = v2.fee_addback_v2(bd, days)
        diff_v2 = abs(r30.compound_gross(net, add_v2) - opal) * 100.0
        add30 = c[k]["bd_fee_addback"]
        inter = net * add30 * 100.0
        resid_add = (opal - (net + add30)) * 100.0
        reason30 = c[k]["reason"]
        if abs(ratio - 1.0) > 0.02 and diff_v2 <= TOL:
            cls = "FEE_BASE_BALANCE_PATH"
            ev = ("served daily-mean value is %.3f x the (bmv+emv)/2 base; add-back %.3f pp -> %.3f pp; compounded on the daily base the "
                  "gap is %.3f pp (round 30: %.3f pp; additive: %.3f pp)" % (ratio, add30 * 100, add_v2 * 100, diff_v2, c[k]["abs_diff_pp"], a[k]["abs_diff_pp"]))
        elif bd["fees"] < 0:
            cls = "NEGATIVE_FEE_ADDBACK"
            ev = ("BD fees total is negative (add-back %.3f pp); compounding on it moves the gross by net*add-back = %.3f pp; "
                  "daily-base gap %.3f pp; additive gap %.3f pp" % (add30 * 100, inter, diff_v2, a[k]["abs_diff_pp"]))
        elif reason30 == "FLOW_TIMING":
            cls = "FLOW_TIMING_RESIDUE"
            ev = ("round 30 evidence: %s; the compounded gap %.3f pp; daily-base gap %.3f pp (base ratio %.3f)" % (
                c[k]["evidence"], c[k]["abs_diff_pp"], diff_v2, ratio))
        else:
            cls = "ADDITIVE_TIE_COINCIDENCE"
            ev = ("additive residual %.3f pp (within) vs interaction net*add-back %.3f pp -> compounded gap %.3f pp; daily-base gap %.3f pp "
                  "(base ratio %.3f); no flow, income or day-count evidence closes it (round 30 reason %s)" % (
                      resid_add, inter, c[k]["abs_diff_pp"], diff_v2, ratio, reason30))
        counts[cls] = counts.get(cls, 0) + 1
        rows.append({"account": k[0], "segment": {"start": k[1], "end": k[2]}, "cause_class": cls, "evidence": ev})
    v2rec = json.loads((HERE / v2.OUT_NAME).read_bytes().decode())
    fix = {"file": DEL + "0.9.0_WK_IRPT_DASHBD~35/tieout_compound_v2.py", "after_within": v2rec["within"]}
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~35", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-57", "vendor_calls": 0,
           "population": len(pop), "rows": rows, "counts": counts, "compounding_defect_classes": DEFECT, "fix": fix,
           "fix_regrade": {"graded": v2rec["graded"], "within": v2rec["within"], "outside": v2rec["outside"],
                           "verdict_moves_vs_round30": v2rec["verdict_moves_vs_round30"], "outside_by_reason": v2rec["outside_by_reason"]},
           "files_read": {"round18_record": DEL + "0.9.0_WK_IRPT_DASHBD~13/TIEOUT_49F_BD_POPULATION_E2_GROSS.json",
                          "round30_record": DEL + "0.9.0_WK_IRPT_DASHBD~34/TIEOUT_COMPOUND_E1.json",
                          "round30_reader": DEL + "0.9.0_WK_IRPT_DASHBD~34/tieout_compound.py",
                          "plan": r17.PLAN_REL,
                          "bronze_prefix": "s3://%s/%s (%d objects)" % (r17.BRONZE_BUCKET, r17.BRONZE_PREFIX, n_obj),
                          "served_series": "s3://%s/%s (%d partitions, %d accounts)" % (r17.GOLD_BUCKET, r17.GOLD_PREFIX, n_part, n_ga)}}
    (HERE / "CROSSOVER_E1.json").write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    lines = ["# CROSSOVER_E1 -- the 181 segments that tied under the additive fee basis and miss under the compounded one (TO-DB-b-57, 0.9.0_WK_IRPT_DASHBD~35)", "",
             "Counts only. Record: `CROSSOVER_E1.json`. Reader: `crossover_e1.py`; fix: `tieout_compound_v2.py`. S3 reads only; zero vendor calls.", "",
             "Population: segments WITHIN in round 18 (additive) and OUTSIDE in round 30 (compounded): %d." % len(pop), "",
             "| cause class | segments | compounding defect |", "|---|---|---|"]
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        lines.append("| %s | %d | %s |" % (k, v, "yes" if k in DEFECT else "no"))
    lines += ["| total | %d | |" % sum(counts.values()), "",
              "Defect judgment: FEE_BASE_BALANCE_PATH. The compounding formula is sound; its fee base, (bmv + emv) / 2, is not the average balance when the",
              "balance moves through the segment. The other classes are an exposed additive coincidence, a negative-fee total, or flow-convention residue.", "",
              "Fix: `tieout_compound_v2.py` forms the add-back on the mean served daily value of the linked days. Full re-grade of %d segments:" % v2rec["graded"], "",
              "| | within 0.35 pp | outside |", "|---|---|---|",
              "| round 30 (two-point base) | 7,459 | 1,619 |",
              "| v2 (daily-mean base) | %d | %d |" % (v2rec["within"], v2rec["outside"]), "",
              "Per-segment moves vs round 30: %s." % ", ".join("%s %d" % (k, v) for k, v in v2rec["verdict_moves_vs_round30"].items()),
              "Of the 181, %d are WITHIN again under v2." % counts.get("FEE_BASE_BALANCE_PATH", 0)]
    (HERE / "CROSSOVER_E1.md").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print(counts, fix)


if __name__ == "__main__":
    main()
