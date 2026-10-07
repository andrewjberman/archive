import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import residue_nonclosure_e2 as m  # noqa: E402


def seg(acct, start, end, bdd, od, **kw):
    d = {"account": acct, "segment": {"start": start, "end": end}, "bd_days_held": bdd, "opal_days": od,
         "verdict": "OUTSIDE", "reason": "UNEXPLAINED", "opal_return": 0.10, "bd_gross_return": 0.10, "abs_diff_pp": 0.5}
    d.update(kw)
    return d


def test_nonclosure_set_drops_plus_one_over_closure():
    g = {"segments": [seg("a", "2024-12-01", "2025-02-01", 11, 10), seg("b", "2025-02-01", "2025-03-01", 11, 10),
                      seg("c", "2024-12-01", "2025-02-01", 10, 10),
                      seg("d", "2024-12-01", "2025-02-01", 10, 10, reason="FLOW_TIMING"),
                      seg("e", "2024-12-01", "2025-02-01", None, None, verdict="NOT_GRADABLE")]}
    graded, ns = m.nonclosure_set(g)
    assert len(graded) == 4
    assert sorted(s["account"] for s in ns) == ["b", "c"]


def test_nonclosure_flow_timing_needs_envelope():
    s = seg("a", "2025-02-01", "2025-03-01", 5, 5, opal_return=0.10, bd_gross_return=0.101)
    pt = {"beginningMarketValue": 1000.0, "endingMarketValue": 1500.0, "netAdditions": 400.0}
    r, ev = m.classify(s, pt)
    assert r == "FLOW_TIMING" and "envelope" in ev


def test_nonclosure_small_flow_stays_unexplained():
    s = seg("a", "2025-02-01", "2025-03-01", 5, 5)
    pt = {"beginningMarketValue": 1000.0, "endingMarketValue": 1100.0, "netAdditions": 1.0}
    r, ev = m.classify(s, pt)
    assert r == "UNEXPLAINED" and ev


def test_nonclosure_missing_point_and_counts():
    g = {"segments": [seg("a", "2025-02-01", "2025-03-01", 5, 5), seg("b", "2025-02-01", "2025-03-01", 5, 5)]}
    plan = {"request_list": [{"account": "a", "bd_account": "1"}, {"account": "b", "bd_account": "2"}]}
    resp = {"combinedLevels": [{"descriptor": {"level": "Account"}, "dateRangePoints": [
        {"dateRange": {"startDate": "2025-02-01T00:00:00", "endDate": "2025-03-01T00:00:00"},
         "beginningMarketValue": 1000.0, "endingMarketValue": 1500.0, "netAdditions": 400.0}]}]}
    rec = m.build(g, plan, lambda b: resp if b == "1" else {})
    c = rec["counts"]
    assert c["denominator"] == 2 and c["nonclosure"] == 2
    assert sum(c["per_reason"].values()) == 2 and c["final_unexplained"] == 1 and c["share_of_graded"] == 0.5
