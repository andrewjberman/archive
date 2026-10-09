"""Offline tests for large_flow_e3.py (synthetic values only)."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("lf", str(Path(__file__).resolve().parent / "large_flow_e3.py"))
lf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lf)


def day(d, mv, flow, r):
    return {"date": d, "mv": mv, "flow": flow, "r": r, "inc": 0.0}


def test_end_relink_equals_served_when_no_override():
    days = [day("2025-01-02", 110.0, 0.0, 0.10), day("2025-01-03", 121.0, 0.0, 0.10)]
    assert abs(lf.relink(days, 100.0, "END", set()) - 0.21) < 1e-12


def test_start_timing_on_first_day_flow():
    # prior 100, flow +100 on day 0, ending 210: END r = (210-100)/100-1 = 0.10; START r = 210/200-1 = 0.05
    days = [day("2025-01-02", 210.0, 100.0, 0.10)]
    assert abs(lf.relink(days, 100.0, "START", {0}) - 0.05) < 1e-12
    assert abs(lf.relink(days, 100.0, "END", {0}) - 0.10) < 1e-12


def test_fee_field_is_flow_class():
    days = [day("2025-01-02", 10.0, 0.0, 0.0), day("2025-01-03", 50.0, 40.0, 0.0)]
    series = {"2025-01-01": {"mv": 10.0}}
    seg = {"segment": {"start": "2025-01-02", "end": "2025-01-03"}}
    bd = {"twr": 0.5, "fees": -40.0, "net_additions": 40.0, "bmv": 10.0, "emv": 50.0}
    assert lf.classify(seg, days, series, bd)[0] == "BD_FEE_FIELD_IS_FLOW"
