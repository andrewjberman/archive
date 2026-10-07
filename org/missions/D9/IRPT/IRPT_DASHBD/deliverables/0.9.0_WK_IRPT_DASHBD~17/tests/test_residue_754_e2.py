import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import residue_754_e2 as m  # noqa: E402

R17 = m.load_r17()


def day(i, r=0.001, mv=100.0, flow=None, inc=0.0, pr=None):
    return {"date": "2025-01-%02d" % i, "r": r, "mv": mv, "flow": flow, "inc": inc, "price_reason": pr}


def g(gross, held):
    return {"bd_gross_return": gross, "bd_days_held": held, "bd_fees_reported": None}


def test_residue_set_picks_only_unexplained():
    rows = [{"reason": "UNEXPLAINED"}, {"reason": "FLOW_TIMING"}]
    assert len(m.residue_set({"rows": rows})) == 1


def test_residue_coverage_days():
    days = [day(i) for i in range(1, 6)]
    reason, ev = m.grade_residue(R17, g(0.02, 9), days)
    assert reason == "COVERAGE_DAYS" and "daysHeld 9" in ev


def test_residue_missing_price():
    days = [day(i, pr="NO_PRICE" if i == 2 else None) for i in range(1, 6)]
    reason, ev = m.grade_residue(R17, g(0.02, 5), days)
    assert reason == "MISSING_PRICE" and "1 of 5" in ev


def test_residue_income_date():
    days = [day(i, r=0.002, inc=0.002 if i == 3 else 0.0) for i in range(1, 6)]
    gross = R17.link([d["r"] - d["inc"] for d in days])
    reason, ev = m.grade_residue(R17, g(gross, 5), days)
    assert reason == "INCOME_DATE"


def test_residue_unexplained_and_empty():
    days = [day(i) for i in range(1, 6)]
    assert m.grade_residue(R17, g(0.5, 5), days)[0] == "UNEXPLAINED"
    reason, ev = m.grade_residue(R17, g(0.5, 5), [])
    assert reason == "UNEXPLAINED" and ev.strip()
