"""Offline tests for near_zero_e3.py (synthetic values only)."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("nz", str(Path(__file__).resolve().parent / "near_zero_e3.py"))
nz = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(nz)


def day(d, mv, flow, r):
    return {"date": d, "mv": mv, "flow": flow, "r": r, "inc": 0.0}


SEG = {"segment": {"start": "2025-01-02", "end": "2025-01-05"}}
SERIES = {"2025-01-01": {"mv": 0.3}}


def test_landed_gain_return_is_money_gain_over_mean_value():
    days = [day("2025-01-02", 100.0, 0.0, 0.0), day("2025-01-03", 100.0, 0.0, 0.0)]
    bd = {"bmv": 90.0, "emv": 110.0, "net_additions": 10.0}
    assert abs(nz.landed_gain_return(bd, days) - 0.10) < 1e-12


def test_fee_field_is_flow_first_on_a_near_zero_start():
    days = [day("2025-01-02", 0.3, 0.0, 0.0), day("2025-01-03", 40.3, 40.0, 0.0), day("2025-01-04", 40.3, 0.0, 0.0), day("2025-01-05", 40.3, 0.0, 0.0)]
    bd = {"twr": 0.95, "fees": -40.0, "net_additions": 40.0, "bmv": 0.3, "emv": 40.3}
    sub, _ev, t = nz.classify(SEG, days, SERIES, bd)
    assert sub == "BD_FEE_FIELD_IS_FLOW" and t["landed_gain"] <= nz.TOL


def test_gain_agrees_class_when_fee_is_not_the_flow():
    days = [day("2025-01-02", 0.3, 0.0, 0.0), day("2025-01-03", 40.3, 40.0, 0.0), day("2025-01-04", 40.3, 0.0, 0.0), day("2025-01-05", 40.3, 0.0, 0.0)]
    bd = {"twr": 0.95, "fees": 1.0, "net_additions": 40.0, "bmv": 0.3, "emv": 40.3}
    assert nz.classify(SEG, days, SERIES, bd)[0] == "GAIN_AGREES_NEAR_ZERO_BASE"


def test_negative_balance_before_the_boundary_classes():
    days = [day("2025-01-02", 100.0, 0.0, 0.01), day("2025-01-03", -1.0, 0.0, -1.01), day("2025-01-04", 100.0, 0.0, 0.5), day("2025-01-05", 100.0, 0.0, 0.0)]
    bd = {"twr": 0.1, "fees": 0.0, "net_additions": 0.0, "bmv": 100.0, "emv": 100.0}
    assert nz.classify(SEG, days, SERIES, bd)[0] == "NEGATIVE_BALANCE"
