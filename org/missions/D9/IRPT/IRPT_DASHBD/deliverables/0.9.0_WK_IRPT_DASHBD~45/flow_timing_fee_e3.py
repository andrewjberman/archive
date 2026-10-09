"""E3 (TO-DB-b-68): trace the 116 FLOW_TIMING_AFTER_FEE_BASE rows of round 31 under the reader of record.

Reads only: round 31's record (~36 UNEXPLAINED_CLASSES_E2.json) and round 33's record (~40 REGRADE_FIXES_E1.json, every segment's
abs_diff_pp under the reader of record) plus round 32's (~38 REGRADE_FLOWSTART_E2.json) for the trace of rows still outside.
Writes FLOW_TIMING_FEE_E3.json and FLOW_TIMING_FEE_E3.md (counts only) beside this file. No vendor call, no S3, no reader edit.

sub_class (first match wins), from the round-33 per-segment fields:
  STILL_OUT_FLOW_EXCEEDS_BALANCE  verdict OUTSIDE and max_flow_ratio > 1 (a flow larger than the value before it)
  STILL_OUT_GUARD_DAY             verdict OUTSIDE and guard_days > 0
  STILL_OUT_OTHER                 verdict OUTSIDE, neither of the above
  RESOLVED_FIRST_DAY_START        verdict WITHIN and first_day_flow_start
  RESOLVED_WITH_GUARD_DAY         verdict WITHIN and guard_days > 0
  RESOLVED_BY_FLOW_START          verdict WITHIN, no special rule fired
"""
import json
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
D = PROJ + "deliverables/"
UNEX = D + "0.9.0_WK_IRPT_DASHBD~36/UNEXPLAINED_CLASSES_E2.json"
R33 = D + "0.9.0_WK_IRPT_DASHBD~40/REGRADE_FIXES_E1.json"
R32 = D + "0.9.0_WK_IRPT_DASHBD~38/REGRADE_FLOWSTART_E2.json"
R31E = D + "0.9.0_WK_IRPT_DASHBD~38/REGRADE_E1.json"
OUT = D + "0.9.0_WK_IRPT_DASHBD~45/"
TOL = 0.35


def key(a, seg):
    return (a, seg["start"], seg["end"])


def classify(s):
    if s["verdict"] != "WITHIN":
        if (s.get("max_flow_ratio") or 0) > 1:
            return "STILL_OUT_FLOW_EXCEEDS_BALANCE"
        if s["guard_days"] > 0:
            return "STILL_OUT_GUARD_DAY"
        return "STILL_OUT_OTHER"
    if s["first_day_flow_start"]:
        return "RESOLVED_FIRST_DAY_START"
    if s["guard_days"] > 0:
        return "RESOLVED_WITH_GUARD_DAY"
    return "RESOLVED_BY_FLOW_START"


DISP = {
    "RESOLVED_BY_FLOW_START": ("resolved_by_reader", "the reader of record adopted flow-START (round 32); the segment's flow timing now ties BD with no special rule firing",
                               "within 0.35 pp under the reader of record at round 33; nothing further to fix"),
    "RESOLVED_WITH_GUARD_DAY": ("resolved_by_reader", "flow-START plus the round-32 guard (a day whose V_(t-1)+F_t < 2% of |V_(t-1)| keeps its served return) puts the segment within 0.35 pp",
                                "a guard day is counted in the segment and the segment still ties"),
    "RESOLVED_FIRST_DAY_START": ("resolved_by_reader", "round 33's first_day_flow_start predicate links the first day's flow at START and the segment ties BD",
                                 "within 0.35 pp under the reader of record at round 33"),
    "STILL_OUT_GUARD_DAY": ("named_cause", "a full-balance flow (max_flow_ratio 1.0) leaves one guard day; the guard keeps the served return on that day and the segment lands outside 0.35 pp (round 31's START without the guard read it as within)",
                            "inferred from guard_days 1 and the abs_diff delta against round 31's START figure; the cause is the guard rule, no module change is made here"),
    "STILL_OUT_FLOW_EXCEEDS_BALANCE": ("named_cause", "a flow of about three times the value before it (max_flow_ratio above 1): the reader's START timing and BD's timing differ on that flow, so the segment sits outside 0.35 pp; round 31's START figure read it as within",
                                       "round 32 and round 33 agree on the same abs_diff, so no reader fix since round 32 moved it; a fix would need BD's own flow date for that flow, which is a vendor read, out of this order's bounds"),
    "STILL_OUT_OTHER": ("named_cause", "outside 0.35 pp with neither a guard day nor a flow above the prior balance", "not traced"),
}


def main():
    root = Path(__file__).resolve().parents[7]
    u = json.loads((root / UNEX).read_bytes().decode("utf-8"))
    r33 = json.loads((root / R33).read_bytes().decode("utf-8"))
    r32 = json.loads((root / R32).read_bytes().decode("utf-8"))
    r31e = json.loads((root / R31E).read_bytes().decode("utf-8"))
    i33 = {key(s["account"], s["segment"]): s for s in r33["segments"]}
    i32 = {key(s["account"], s["segment"]): s for s in r32["segments"]}
    i31e = {key(s["account"], s["segment"]): s for s in r31e["segments"]}
    pop = [x for x in u["rows"] if x.get("cause_class") == "FLOW_TIMING_AFTER_FEE_BASE"]
    rows = []
    for x in pop:
        k = key(x["account"], x["segment"])
        s = i33[k]
        sc = classify(s)
        ev = ("round 31: %s; round 33 under the reader of record: abs_diff %.4f pp, %s, flow_days %d, max_flow_ratio %.3f, guard_days %d, first_day_flow_start %s"
              % (x["evidence"], s["abs_diff_pp"], s["verdict"], s["flow_days"], s["max_flow_ratio"], s["guard_days"], s["first_day_flow_start"]))
        if sc.startswith("STILL_OUT"):
            ev += "; round 31 END basis %.4f pp, round 32 START %.4f pp" % (i31e[k]["abs_diff_pp"], i32[k]["abs_diff_pp"])
        rows.append({"account": x["account"], "segment": x["segment"], "sub_class": sc,
                     "round31_convention": "MID" if " MID flow" in x["evidence"] else "START",
                     "abs_diff_pp_now": s["abs_diff_pp"], "evidence": ev})
    counts = {}
    for x in rows:
        counts[x["sub_class"]] = counts.get(x["sub_class"], 0) + 1
    within = sum(1 for x in rows if x["abs_diff_pp_now"] <= TOL)
    disp = {k: {"disposition": DISP[k][0], "cause": DISP[k][1], "note": DISP[k][2]} for k in counts}
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~45", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-68", "vendor_calls": 0,
           "tolerance_pp": TOL, "reader_sha256": r33["reader_sha256"], "population": len(rows), "rows": rows, "counts": counts,
           "within_now": within, "outside_now": len(rows) - within,
           "by_round31_convention": {c: sum(1 for x in rows if x["round31_convention"] == c) for c in ("START", "MID")},
           "dispositions": disp,
           "files_read": [UNEX, R33, R32, R31E, PROJ + "tieout/tieout_reader.py (via the round-33 record's reader_sha256, not re-run)"]}
    (root / OUT / "FLOW_TIMING_FEE_E3.json").write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    md = ["# E3 -- FLOW_TIMING_AFTER_FEE_BASE (counts only)", "",
          "Population: %d rows of round 31's record. Tolerance %.2f pp. Read under the reader of record (round 33, reader sha256 %s)."
          % (len(rows), TOL, r33["reader_sha256"][:12]), "",
          "Within now: %d of %d. Outside now: %d." % (within, len(rows), len(rows) - within), "",
          "| sub_class | count | disposition |", "|---|---|---|"]
    for k, n in sorted(counts.items(), key=lambda t: -t[1]):
        md.append("| %s | %d | %s |" % (k, n, disp[k]["disposition"]))
    md += ["", "Round 31 convention: START %d, MID %d." % (rec["by_round31_convention"]["START"], rec["by_round31_convention"]["MID"]), ""]
    (root / OUT / "FLOW_TIMING_FEE_E3.md").write_bytes("\n".join(md).encode("utf-8"))
    print("wrote %d rows; counts %s; within %d" % (len(rows), counts, within))


if __name__ == "__main__":
    main()
