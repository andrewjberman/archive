import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import flow_measured_e1 as m

SEG = {"start": "2025-01-01", "end": "2025-01-11"}  # 10 days; midpoint weight 0.5
PT = {"bmv": 100.0, "emv": 210.0, "na": 100.0}


def _gross_for(flows, midpoint=False):
    return m.dietz(100.0, 210.0, 100.0, flows, SEG["start"], SEG["end"], midpoint=midpoint)


def test_dated_flow_reproduces_bd_and_midpoint_control_fails():
    flows = [("2025-01-01", 100.0)]  # at start: weight 1
    r = m.grade("A", SEG, _gross_for(flows), PT, flows)
    assert r["verdict"] == "MEASURED_FLOW_TIMING" and r["abs_diff_pp_dietz"] < 1e-9
    assert r["abs_diff_pp_midpoint"] > m.TOL  # the midpoint control fails to reproduce it


def test_midpoint_flow_passes_midpoint_control():
    flows = [("2025-01-06", 100.0)]
    r = m.grade("A", SEG, _gross_for(flows, midpoint=True), PT, flows)
    assert r["abs_diff_pp_midpoint"] < 1e-9 and r["verdict"] == "MEASURED_FLOW_TIMING"


def test_flows_mismatch_forces_unexplained_midpoint_still_printed():
    flows = [("2025-01-01", 50.0)]
    g = m.dietz(100.0, 210.0, 100.0, flows, SEG["start"], SEG["end"])
    r = m.grade("A", SEG, g, PT, flows)
    assert r["flows_match"] is False and r["verdict"] == "UNEXPLAINED"
    assert r["abs_diff_pp_midpoint"] is not None


def test_dietz_gap_above_tolerance_unexplained():
    flows = [("2025-01-01", 100.0)]
    r = m.grade("A", SEG, 0.9, PT, flows)
    assert r["flows_match"] is True and r["verdict"] == "UNEXPLAINED"


def test_counts_reconcile_with_midpoint_count():
    ok = [("2025-01-01", 100.0)]
    rows = [m.grade("A", SEG, _gross_for(ok), PT, ok), m.grade("B", SEG, 0.9, PT, ok), m.grade("C", SEG, None, None, [])]
    c = m.tally(rows)
    assert (c["measured"], c["returned_unexplained"], c["unexplained_measured_basis"]) == (1, 2, 3055)
    assert c["negative_control_within"] == 0
