"""TO-DB-b-111 (IRPT_DASHBD round 55): re-grade the 990 outside segments on one restated convention, by RESTATEMENT_RULE.md.

READ-ONLY on local private evidence; no S3, no vendor call. Writes the per-segment record OUTSIDE the repo and the counts-only record beside this file.

Usage: python restated_tieout.py <repo_root> <rule_commit> <output_commit>
"""
import collections
import hashlib
import json
import sys
from pathlib import Path

PRIV = "C:/dev/_irpt_private_evidence_20261009/"
E = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~"
OUT_DIR = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~86/"
REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~86/"
TOL_PP = 0.35
WINDOW_END = "2026-08-20"
NC_KEY = "BD_RECORD_ENDS_2026-08-20"


def jload(p):
    return json.loads(Path(p).read_bytes().decode("utf-8"))


def key(x):
    return (x["account"], x["segment"]["start"], x["segment"]["end"])


def main():
    root = Path(sys.argv[1]).resolve()
    rule_commit, output_commit = sys.argv[2], sys.argv[3]
    v2 = jload(E + "35/TIEOUT_COMPOUND_V2.json")
    cls = jload(E + "73/UNEXPLAINED_CLASSIFIED.json")
    d106 = jload(E + "81/BD_DATES_TWO_SIDED.json")
    ev = jload(PRIV + "~75/W73_S1_EVIDENCE.json")

    outside = [s for s in v2["segments"] if s["verdict"] == "OUTSIDE"]
    assert len(outside) == 990, len(outside)
    c73 = {key(x): x["reason"] for x in cls["classified"]}
    g106 = {key(x): x for x in d106["segments"]}
    s1 = {key(x): x["return_read"] for x in ev["segments"]}
    assert len(c73) == 510 and len(g106) == 475 and len(s1) == 74

    rows = []
    for s in outside:
        k = key(s)
        cur = c73.get(k) or s["reason"]
        if cur == "ZERO_GAIN_VENDOR_TWR":
            cur = "UNEXPLAINED"
        row = {"account": k[0], "segment": s["segment"], "reason_before": cur,
               "bd_gross_return": s["bd_gross_return"], "opal_return": s["opal_return"],
               "v2_abs_diff_pp": s["abs_diff_pp"]}
        row["d106_verdict"] = g106[k]["verdict"] if k in g106 else None
        row["end_after_window"] = s["segment"]["end"] > WINDOW_END
        if k in s1:
            r = s1[k]
            assert abs(r["bd_gross_return"] - s["bd_gross_return"]) < 1e-9 and abs(r["opal_return_served"] - s["opal_return"]) < 1e-9
            shift = r["restated_return"] - s["opal_return"]
            bd_restated = s["bd_gross_return"] - shift
            row.update({"restated": True, "restated_return": r["restated_return"], "shift": shift, "bd_restated": bd_restated,
                        "restated_diff_pp": abs(bd_restated - s["opal_return"]) * 100.0})
            row["within_after_restatement"] = row["restated_diff_pp"] <= TOL_PP
        else:
            row.update({"restated": False, "restated_diff_pp": None, "within_after_restatement": False})
        # classification order (RESTATEMENT_RULE.md section 3)
        if row["end_after_window"]:
            final, why = NC_KEY, "end after %s" % WINDOW_END
        elif row["within_after_restatement"]:
            final, why = "CONVENTION", "within %.2f pp after restatement" % TOL_PP
        elif cur in ("FLOW_TIMING", "INCOME_DATE"):
            final, why = "UNEXPLAINED", "ruling 1: %s refuted (DB-b-106 %s); not within after restatement" % (cur, row["d106_verdict"])
        else:
            final, why = cur, "keeps DB-b-99 final reason"
        row["reason_after"] = final
        row["why"] = why
        row["claim"] = "confirmed" if final == "CONVENTION" else ("inferred" if row["restated"] else "held")
        rows.append(row)

    by = collections.Counter(r["reason_after"] for r in rows)
    assert sum(by.values()) == 990
    within_all = sum(1 for r in rows if r["within_after_restatement"])
    within_in = sum(1 for r in rows if r["within_after_restatement"] and not r["end_after_window"])
    flagged319 = {k for k, x in g106.items() if x["verdict"] == "UNEXPLAINED"}
    after = {key(s) for s in outside if s["segment"]["end"] > WINDOW_END}
    nc_overlap = {
        "date_test_count": len(after),
        "d106_flagged_count": len(flagged319),
        "both": len(after & flagged319),
        "date_test_only": len(after - flagged319),
        "d106_flagged_end_on_or_before_window": len(flagged319 - after),
        "d106_confirmed_with_end_after_window": sum(1 for k, x in g106.items() if x["verdict"] == "confirmed" and k in after),
    }
    restated_n = sum(1 for r in rows if r["restated"])
    restated_in = sum(1 for r in rows if r["restated"] and not r["end_after_window"])
    before_by = collections.Counter(r["reason_before"] for r in rows)
    d106_refuted = sum(1 for r in rows if r["d106_verdict"] == "confirmed" and not r["end_after_window"] and r["reason_after"] == "UNEXPLAINED")

    OUT = Path(OUT_DIR)
    OUT.mkdir(parents=True, exist_ok=True)
    priv = OUT / "RESTATED_TIEOUT.json"
    body = {"measured_by": "0.9.0_WK_IRPT_DASHBD~86", "task_order": "IRPT_DASHBD.TO-DB-b-111", "tolerance_pp": TOL_PP,
            "comparison_window_end": WINDOW_END, "n": len(rows), "segments": rows}
    priv.write_bytes((json.dumps(body, indent=1) + "\n").encode("utf-8"))
    sha = hashlib.sha256(priv.read_bytes()).hexdigest()

    rec = {
        "measured_by": "0.9.0_WK_IRPT_DASHBD~86",
        "claim": "inferred",
        "task_order": "IRPT_DASHBD.TO-DB-b-111",
        "vendor_calls": 0,
        "s3_reads": 0,
        "tolerance_pp": TOL_PP,
        "comparison_window_end": WINDOW_END,
        "n_outside_before": 990,
        "by_reason_before": dict(before_by),
        "by_reason": dict(sorted(by.items(), key=lambda kv: (-kv[1], kv[0]))),
        "within_after_restatement": within_all,
        "within_after_restatement_inside_window": within_in,
        "restated_segments": restated_n,
        "restated_segments_inside_window": restated_in,
        "not_restated_segments": 990 - restated_n,
        "not_comparable_key": NC_KEY,
        "not_comparable_count": by.get(NC_KEY, 0),
        "not_comparable_vs_d106_flagged": nc_overlap,
        "flow_income_refuted_to_unexplained_inside_window": d106_refuted,
        "rulings_applied": [
            "ADDENDUM 21 (1.0.0_SA_CTO~DELL2, relayed by 2.0.0_SA_COO~D2) ruling 1: matching dates refute FLOW_TIMING and INCOME_DATE; the DB-b-106 confirmed segments are UNEXPLAINED unless CONVENTION",
            "ruling 2: a segment ending after 2026-08-20 is NOT_COMPARABLE, reason %s, used as the by_reason key (the rule file's text names the key NOT_COMPARABLE; the ruling's key prevails)" % NC_KEY,
            "ruling 3: comparison_window_end = 2026-08-20",
            "ruling 4: CONVENTION only within 0.35 pp after the pre-registered restatement",
        ],
        "private_record": {"path": str(priv).replace("\\", "/"), "sha256": sha},
        "preregistration": {"restatement_rule_file": REL + "RESTATEMENT_RULE.md", "rule_commit": rule_commit, "output_commit": output_commit,
                            "output_commit_is": "the commit carrying restated_tieout.py, the producer of this record; this record lands in a later commit"},
    }
    (root / REL / "RESTATED_TIEOUT.json").write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
    print(json.dumps({k: rec[k] for k in ("by_reason", "within_after_restatement", "within_after_restatement_inside_window",
                                         "restated_segments", "not_comparable_count", "not_comparable_vs_d106_flagged")}, indent=1))
    print("private sha256", sha)


if __name__ == "__main__":
    main()
