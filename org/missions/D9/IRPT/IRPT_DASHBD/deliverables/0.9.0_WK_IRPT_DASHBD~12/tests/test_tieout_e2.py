"""Offline tests for tieout_e2.py (TO-DB-b-26): synthetic inputs only, no S3, no vendor."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tieout_e2 as t  # noqa: E402

SEG = {"start": "2026-01-02", "end": "2026-01-08"}


def day(i, r, mv=100.0, flow=0.0, inc=0.0, reason=None):
    return {"date": "2026-01-%02d" % (i + 2), "r": r, "mv": mv, "flow": flow, "inc": inc, "price_reason": reason}


def flat_days(n=5, r=0.001, **kw):
    return [day(i, r, **kw) for i in range(n)]


def test_within_tolerance():
    days = flat_days()
    opal = t.link([d["r"] for d in days])
    row = t.grade_segment("A1", SEG, days, {"twr": opal + 0.0001, "days_held": 5})  # 0.01 pp apart
    assert row["verdict"] == "WITHIN"
    assert row["abs_diff_pp"] < t.TOLERANCE_PP
    assert "reason" not in row


def test_outside_with_reason_coverage_days():
    days = flat_days()
    opal = t.link([d["r"] for d in days])
    row = t.grade_segment("A1", SEG, days, {"twr": opal + 0.02, "days_held": 9})  # 2 pp apart, BD counted 4 more days
    assert row["verdict"] == "OUTSIDE"
    assert row["reason"] == "COVERAGE_DAYS"
    assert "daysHeld 9" in row["evidence"]


def test_outside_reason_unexplained_when_no_evidence_and_closed_set():
    days = flat_days()
    opal = t.link([d["r"] for d in days])
    row = t.grade_segment("A1", SEG, days, {"twr": opal + 0.02, "days_held": 5})
    assert row["verdict"] == "OUTSIDE"
    assert row["reason"] == "UNEXPLAINED"
    assert row["reason"] in t.REASONS and row["evidence"]


def test_outside_reason_missing_price_names_the_flag():
    days = flat_days()
    days[2]["price_reason"] = "HOLDINGS_NOT_OK"
    row = t.grade_segment("A1", SEG, days, {"twr": t.link([d["r"] for d in days]) + 0.02, "days_held": 5})
    assert row["reason"] == "MISSING_PRICE" and "HOLDINGS_NOT_OK" in row["evidence"]


def test_not_gradable_carries_a_why():
    days = flat_days()
    no_value = t.grade_segment("A1", SEG, days, {"twr": None, "days_held": 0, "note": "vendor-absent range"})
    no_acct = t.grade_segment("A2", SEG, None, {"twr": 0.01, "days_held": 5})
    no_resp = t.grade_segment("A3", SEG, days, None)
    for row in (no_value, no_acct, no_resp):
        assert row["verdict"] == "NOT_GRADABLE"
        assert row["why"]
    assert no_value["why"].startswith("BD_NO_VALUE") and no_acct["why"].startswith("SERVED_SERIES_LACKS_ACCOUNT")


def test_counts_reconcile():
    days = flat_days()
    opal = t.link([d["r"] for d in days])
    rows = [
        t.grade_segment("A1", SEG, days, {"twr": opal, "days_held": 5}),
        t.grade_segment("A2", SEG, days, {"twr": opal + 0.05, "days_held": 5}),
        t.grade_segment("A3", SEG, days, {"twr": opal + 0.05, "days_held": 12}),
        t.grade_segment("A4", SEG, None, None),
    ]
    c = t.tally(rows, 4)
    assert c["segments_planned"] == c["graded"] + c["not_gradable"] == 4
    assert c["graded"] == c["within_tolerance"] + c["outside_tolerance"]
    assert sum(c["outside_by_reason"].values()) == c["outside_tolerance"] == 2
    assert c["not_gradable"] == 1 and sum(c["not_gradable_by_why"].values()) == 1


def test_bd_points_reads_account_level_range():
    resp = {"levels": [{"descriptor": {"level": "Account", "levelId": 7}, "dateRangePoints": [
        {"dateRange": {"startDate": "2026-01-02T00:00:00", "endDate": "2026-01-08T00:00:00"}, "daysHeld": 5,
         "timeWeightedReturns": {"return": 0.0123}, "fees": 1.0, "beginningMarketValue": 10.0, "endingMarketValue": 11.0}]}]}
    pts = t.bd_points(resp, "7")
    assert pts[("2026-01-02", "2026-01-08")]["twr"] == 0.0123
    assert t.bd_points(resp, "8") == {}
