"""Tests for tieout_compound.py. Synthetic account only (no client data): constant daily net return and constant daily fee rate."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tieout_compound as c

NET = 0.0004         # constant daily net return
FEE = 0.00004        # constant daily fee rate (about 1% a year)
BAL = 1_000_000.0


def range_inputs(n_days):
    """(bd net twr, add_back) for an n_days range of the synthetic account. The reported fees are the range's compounded daily fee
    drag, ((1 + FEE) ** n - 1) * average balance, so that the add-back the reader forms (fees / average balance) is that drag."""
    net = (1.0 + NET) ** n_days - 1.0
    bd = {"twr": net, "fees": ((1.0 + FEE) ** n_days - 1.0) * BAL, "bmv": BAL, "emv": BAL}
    _fees, add = c.r18.fee_addback(bd)
    return net, add


def gross(n_days, fn):
    net, add = range_inputs(n_days)
    return fn(net, add)


def test_compounded_gross_of_adjacent_ranges_chains_to_the_whole():
    a, b = gross(120, c.compound_gross), gross(130, c.compound_gross)
    whole = gross(250, c.compound_gross)
    assert abs(((1.0 + a) * (1.0 + b) - 1.0) - whole) < 1e-9
    # and the whole is the daily gross, compounded: (1 + NET)^n * (1 + FEE)^n - 1
    assert abs(whole - (((1.0 + NET) * (1.0 + FEE)) ** 250 - 1.0)) < 1e-9


def test_additive_gross_does_not_chain():
    a, b = gross(120, c.additive_gross), gross(130, c.additive_gross)
    whole = gross(250, c.additive_gross)
    assert abs(((1.0 + a) * (1.0 + b) - 1.0) - whole) > 1e-6


def test_null_add_back_leaves_net_as_it_is():
    assert c.compound_gross(0.05, None) == 0.05 and c.additive_gross(0.05, None) == 0.05


def test_compounded_gross_is_above_the_additive_for_a_positive_net():
    assert c.compound_gross(0.10, 0.01) > c.additive_gross(0.10, 0.01)
    assert abs(c.compound_gross(0.10, 0.01) - (1.10 * 1.01 - 1.0)) < 1e-15


def test_grade_segment_uses_the_compounded_basis():
    seg = {"start": "2025-01-02", "end": "2025-01-03"}
    days = [{"date": "d%d" % i, "r": 0.05, "mv": 100.0, "flow": 0.0, "inc": 0.0, "price_reason": None} for i in range(2)]
    opal = c.r17.link([d["r"] for d in days])
    net = (1.0 + opal) / 1.01 - 1.0      # net such that net compounded with a 1% add-back is exactly Opal's
    row = c.grade_segment("A", seg, days, {"twr": net, "days_held": 2, "note": None, "fees": 1.0, "bmv": 100.0, "emv": 100.0})
    assert row["verdict"] == "WITHIN" and row["abs_diff_pp"] < 1e-9
    assert abs(row["bd_gross_return"] - opal) < 1e-12
