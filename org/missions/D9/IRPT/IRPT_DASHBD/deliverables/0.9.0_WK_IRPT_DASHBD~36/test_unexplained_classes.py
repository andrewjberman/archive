"""Tests for unexplained_classes.py. Synthetic account only (no client data)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import unexplained_classes as u


def days(mvs):
    return [{"date": "2025-01-%02d" % (i + 1), "r": 0.0, "mv": m, "flow": 0.0, "inc": 0.0} for i, m in enumerate(mvs)]


def test_fee_base_is_the_mean_daily_value():
    d = days([100.0, 200.0, 300.0])
    assert abs(u.fee_base_gross(0.10, 20.0, d) - (1.10 * (1.0 + 20.0 / 200.0) - 1.0)) < 1e-12


def test_no_fee_or_no_value_leaves_the_net():
    assert u.fee_base_gross(0.05, None, days([100.0])) == 0.05
    assert u.fee_base_gross(0.05, 10.0, days([0.0, 0.0])) == 0.05


def test_top_prefix_is_the_smallest_prefix_reaching_80_percent():
    top, run = u.top_prefix({"A": 60, "B": 25, "C": 10, "D": 5}, 100)
    assert [k for k, _ in top] == ["A", "B"] and run == 85
    top, run = u.top_prefix({"A": 80, "B": 20}, 100)
    assert [k for k, _ in top] == ["A"] and run == 80
