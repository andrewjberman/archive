"""Offline tests for crossover_e1.py (synthetic values only; no client data, no S3)."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("ce", str(Path(__file__).resolve().parent / "crossover_e1.py"))
ce = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ce)


def day(d, mv):
    return {"date": d, "mv": mv, "flow": 0.0, "r": 0.0, "inc": 0.0}


def test_caller_uses_reader_mean():
    # the repaired call path: the base ratio is the reader of record's daily mean over (bmv+emv)/2
    days = [day("2025-01-02", 100.0), day("2025-01-03", 200.0), day("2025-01-06", 300.0)]
    bd = {"bmv": 100.0, "emv": 300.0}
    assert abs(ce.base_ratio(days, bd) - 1.0) < 1e-12
    assert ce.reader.daily_mean_value(days) == 200.0


def test_caller_mean_is_positive_only():
    # a negative served value is left out of the mean (positive_only=True), as the trace always did
    days = [day("2025-01-02", -50.0), day("2025-01-03", 100.0), day("2025-01-06", 300.0)]
    bd = {"bmv": 100.0, "emv": 300.0}
    assert abs(ce.base_ratio(days, bd) - 1.0) < 1e-12


def test_caller_defines_no_fee_base_function():
    src = Path(ce.__file__).read_text(encoding="utf-8")
    assert "def daily_mean_value" not in src and "def mean_daily_value" not in src
    assert not hasattr(ce.v2, "daily_mean_value")
