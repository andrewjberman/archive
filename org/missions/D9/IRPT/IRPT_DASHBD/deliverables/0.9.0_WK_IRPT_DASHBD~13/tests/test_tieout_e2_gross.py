import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tieout_e2_gross as g

SEG = {"start": "2025-01-02", "end": "2025-01-03"}


def days(r=0.02, n=2):
    return [{"date": "d%d" % i, "r": r / n, "mv": 100.0, "flow": 0.0, "inc": 0.0, "price_reason": None} for i in range(n)]


def bd(twr, fees=None, bmv=100.0, emv=100.0, held=2):
    return {"twr": twr, "days_held": held, "note": None, "fees": fees, "bmv": bmv, "emv": emv}


def test_bd_fee_addback_brings_segment_within():
    d = days()
    opal = g.r17.link([x["r"] for x in d])
    row = g.grade_segment("A", SEG, d, bd(opal - 0.01, fees=1.0))   # addback 1/100 = 0.01
    assert abs(row["bd_fee_addback"] - 0.01) < 1e-12
    assert row["verdict"] == "WITHIN" and abs(row["bd_gross_return"] - opal) < 1e-12


def test_null_bd_fee_addback_stays_unexplained_when_outside():
    d = days()
    opal = g.r17.link([x["r"] for x in d])
    row = g.grade_segment("A", SEG, d, bd(opal - 0.01, fees=None))
    assert row["bd_fee_addback"] is None and row["bd_gross_return"] == row["bd_return"]
    assert row["verdict"] == "OUTSIDE" and row["reason"] == "UNEXPLAINED"
    assert g.grade_segment("A", SEG, d, bd(opal - 0.01, fees=0.0))["bd_fee_addback"] is None


def test_non_positive_average_value_gives_null_bd_fee_addback():
    fees, add = g.fee_addback(bd(0.0, fees=5.0, bmv=0.0, emv=0.0))
    assert fees == 5.0 and add is None


def test_counts_reconcile_with_bd_fee_addback_rows():
    d = days()
    opal = g.r17.link([x["r"] for x in d])
    rows = [g.grade_segment("A", SEG, d, bd(opal - 0.01, fees=1.0)),
            g.grade_segment("B", SEG, d, bd(opal - 0.01)),
            g.grade_segment("C", SEG, d, None),
            g.grade_segment("D", SEG, None, None)]
    c = g.r17.tally(rows, 4)
    assert c["segments_planned"] == 4 and c["graded"] == 2 and c["not_gradable"] == 2
    assert c["within_tolerance"] + c["outside_tolerance"] == c["graded"]
    assert c["outside_by_reason"]["UNEXPLAINED"] == 1
    assert all("bd_fee_addback" in r for r in rows)
