import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import residue_e2_gross as m


def seg(acct, start, end, bd, op, verdict="OUTSIDE", reason="UNEXPLAINED"):
    return {"account": acct, "segment": {"start": start, "end": end}, "bd_days_held": bd, "opal_days": op,
            "verdict": verdict, "reason": reason if verdict == "OUTSIDE" else None, "evidence": "ev", "abs_diff_pp": 0.1}


def run(segs):
    return m.residue({"segments": segs})


def test_overlap_segment_in_both_sets():
    r = run([seg("a", "2024-12-01", "2025-02-01", 11, 10)])
    assert r["counts"]["overlap"] == 1 and r["rows"][0]["sets"] == ["UNEXPLAINED", "PLUS_ONE_DAY"]
    assert r["rows"][0]["reason"] == "UNEXPLAINED"


def test_plus_one_not_spanning_closure_left_out_of_overlap_and_union():
    r = run([seg("a", "2025-02-01", "2025-03-01", 11, 10, "WITHIN")])
    assert r["counts"]["overlap"] == 0 and r["counts"]["plus_one_day"] == 0 and r["rows"] == []


def test_unexplained_kept_with_evidence():
    r = run([seg("a", "2025-02-01", "2025-03-01", 10, 10)])
    assert r["counts"]["unexplained"] == 1 and r["counts"]["overlap"] == 0
    assert r["rows"][0]["reason"] == "UNEXPLAINED" and r["rows"][0]["evidence"].strip()


def test_counts_reconcile_with_overlap():
    r = run([seg("a", "2024-12-01", "2025-02-01", 11, 10),
             seg("b", "2025-02-01", "2025-03-01", 10, 10),
             seg("c", "2024-12-01", "2025-02-01", 11, 10, "WITHIN"),
             seg("d", "2024-12-01", "2025-02-01", 10, 10, "WITHIN"),
             {"account": "e", "verdict": "NOT_GRADABLE", "segment": {"start": "x", "end": "y"}}])
    c = r["counts"]
    assert c["denominator"] == 4 and c["unexplained"] == 2 and c["plus_one_day"] == 2 and c["overlap"] == 1
    assert c["union"] == len(r["rows"]) == c["unexplained"] + c["plus_one_day"] - c["overlap"] == 3
    assert sum(c["residue_per_reason"].values()) == 3
    assert {x["account"]: x["reason"] for x in r["rows"]}["c"] == "COVERAGE_DAYS"
