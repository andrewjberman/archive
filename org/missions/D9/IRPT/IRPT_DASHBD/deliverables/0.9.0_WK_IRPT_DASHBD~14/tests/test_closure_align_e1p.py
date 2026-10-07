"""Offline tests for closure_align_e1p.py (TO-DB-b-29): synthetic series, the 2025-01-09 closure day; no S3."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import closure_align_e1p as c  # noqa: E402

SEG = {"start": "2025-01-06", "end": "2025-01-14"}


def seg(opal, bd, **kw):
    s = {"account": "A1", "segment": SEG, "opal_return": opal, "bd_gross_return": bd, "opal_days": 5, "bd_days_held": 6,
         "verdict": "OUTSIDE", "reason": "UNEXPLAINED"}
    s.update(kw)
    return s


def days(n, inc):
    return [{"date": "d%d" % i, "r": 0.0, "inc": inc} for i in range(n)]


def test_lands_within_once_2025_01_09_is_held():
    # served 1.00% vs BD 1.60%: 0.60 pp out; a held 2025-01-09 carrying 0.60% accrual closes it
    s = seg(0.01, 0.0160)
    row = c.align_row(s, days(5, 0.006))
    assert row["abs_diff_pp_bd_convention"] < 0.35
    assert row["verdict_bd_convention"] == "WITHIN"
    assert row["opal_return"] == 0.01  # served figure untouched


def test_stays_outside_for_2025_01_09():
    row = c.align_row(seg(0.01, 0.05), days(5, 0.0001))
    assert row["verdict_bd_convention"] == "OUTSIDE"
    assert row["abs_diff_pp_bd_convention"] > 0.35


def test_zero_accrual_day_leaves_return_unchanged():
    row = c.align_row(seg(0.02, 0.02), days(5, 0.0))
    assert row["accrual_on_closure_day"] == 0.0
    assert abs(row["opal_return_bd_convention"] - 0.02) < 1e-12
    assert row["verdict_bd_convention"] == "WITHIN"


def test_counts_reconcile_and_set_selection():
    gross = {"segments": [
        seg(0.01, 0.016),
        seg(0.01, 0.05),
        seg(0.01, 0.02, bd_days_held=5),                                       # not +1 day
        seg(0.01, 0.02, segment={"start": "2025-01-10", "end": "2025-01-20"}),  # does not span 2025-01-09
        seg(0.01, 0.02, verdict="WITHIN"),
    ]}
    cs = c.closure_set(gross)
    assert len(cs) == 2
    rows = [c.align_row(cs[0], days(5, 0.006)), c.align_row(cs[1], days(5, 0.0))]
    n = c.tally(rows)
    assert n["denominator"] == 2 and n["within_bd_convention"] + n["outside_bd_convention"] == 2
    assert n["within_bd_convention"] == 1
