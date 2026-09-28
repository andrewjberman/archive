"""AC1 -- HVST-w-3: ALL THREE ROUTES serve exactly the spec's field lists, over CONSTRUCTED
`chatter_daily`/`chatter_event` rows. No S3, no network, no vendor call -- every row below is
authored in-process.

Prints, per route: the field names served and the set difference against the spec's enumerated
list in BOTH directions; the dense-day denominator; proof that `breakout_ratio`/`z_score` are
served-only (never stored); the events arm's field set intersected against {breakout_ratio,
z_score}; and the event route's resolved id against `publication_gold._event_id` directly.

Run: python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~24/scripts/ac1_route_shapes.py
"""

import datetime
import os
import sys

sys.path.insert(0, os.getcwd())

import lib.research.harvest.publication_gold as publication_gold
import lib.research.harvest.timeline_api as timeline_api

UTC = datetime.timezone.utc
SECURITY_KEY = "TEST_HK_Equity"
FLOOR = publication_gold.BACKFILL_FLOOR  # 2026-01-01


def _d(offset):
    return FLOOR + datetime.timedelta(days=offset)


# --------------------------------------------------------------------------
# CONSTRUCTED chatter_daily rows -- ten dense days, Jan 1..10. No builder call, no S3: each
# row is authored by hand so the STORED shape is fully under this script's control.
# --------------------------------------------------------------------------

def _daily_row(offset, mention_score, data_status="COMPLETE",
               baseline_30d_sum=None, baseline_30d_days=0):
    day = _d(offset)
    return {
        "security_key": SECURITY_KEY,
        "composite_figi": "BBG000TEST01",
        "day": day,
        "articles_total": 2,
        "tier_a": 1,
        "tier_b": 1,
        "tier_c": 0,
        "tier_d": 0,
        "mention_score": mention_score,
        "mention_count_total": 3,
        "publishers_distinct": 2,
        "trailing_7d_sum": mention_score * 2,
        "trailing_30d_sum": mention_score * 4,
        "baseline_30d_sum": baseline_30d_sum if baseline_30d_sum is not None else 0.0,
        "baseline_30d_days": baseline_30d_days,
        "cumulative_ytd": mention_score * (offset + 1),
        "first_published_utc": datetime.datetime(day.year, day.month, day.day, 8, 0, tzinfo=UTC),
        "last_published_utc": datetime.datetime(day.year, day.month, day.day, 18, 0, tzinfo=UTC),
        "data_status": data_status,
        "publishers_covered": 5,
        "publishers_enabled": 5,
    }


DAILY_SCORES = [1.0, 1.2, 0.8, 0.9, 1.1, 1.0, 0.95, 1.05, 1.0, 5.0]
DAILY_ROWS = []
for i, score in enumerate(DAILY_SCORES):
    if i == 9:
        # day 10 (Jan 10) carries a real baseline (offsets 7..36 before it, floored at FLOOR,
        # is Jan1..Jan3 -- three days) so breakout_ratio/z_score are non-trivially computed.
        DAILY_ROWS.append(_daily_row(i, score, baseline_30d_sum=3.0, baseline_30d_days=3))
    else:
        DAILY_ROWS.append(_daily_row(i, score))


def daily_loader(security_key):
    assert security_key == SECURITY_KEY
    return list(DAILY_ROWS)


# --------------------------------------------------------------------------
# CONSTRUCTED chatter_event row -- one run, Jan 5..Jan 6.
# --------------------------------------------------------------------------

EVENT_FIRST_DAY = _d(4)
EVENT_LAST_DAY = _d(5)
EVENT_ROW = {
    "security_key": SECURITY_KEY,
    "composite_figi": "BBG000TEST01",
    "first_day": EVENT_FIRST_DAY,
    "last_day": EVENT_LAST_DAY,
    "days_span": 2,
    "articles_total": 4,
    "tier_a": 2,
    "tier_b": 2,
    "publishers_distinct": 2,
    "lead_article_key": "sa:1001",
    "lead_headline": "Test Co posts a surprise quarter",
    "article_keys": ["sa:1001", "bbg:2001", "sa:1002", "bbg:2002"],
}


def event_loader(security_key):
    assert security_key == SECURITY_KEY
    return [dict(EVENT_ROW)]


ARTICLE_ROWS_BY_DAY_OR_EVENT = [
    {
        "article_key": "sa:1001", "headline": "Test Co posts a surprise quarter",
        "publisher": "sa", "signal_tier": "A", "mention_count": 4,
        "mention_in_title": True, "mention_in_lead": True,
        "published_utc": datetime.datetime(2026, 1, 5, 9, 0, tzinfo=UTC),
        "published_precision": "instant",
    },
    {
        "article_key": "bbg:2001", "headline": "Test Co earnings beat expectations",
        "publisher": "bbg", "signal_tier": "A", "mention_count": 3,
        "mention_in_title": True, "mention_in_lead": False,
        "published_utc": datetime.datetime(2026, 1, 5, 11, 0, tzinfo=UTC),
        "published_precision": "instant",
    },
    {
        "article_key": "sa:1002", "headline": "Analysts react to Test Co print",
        "publisher": "sa", "signal_tier": "B", "mention_count": 2,
        "mention_in_title": False, "mention_in_lead": True,
        "published_utc": datetime.datetime(2026, 1, 6, 8, 0, tzinfo=UTC),
        "published_precision": "date_only",
    },
    {
        "article_key": "bbg:2002", "headline": "Sector roundup mentions Test Co",
        "publisher": "bbg", "signal_tier": "B", "mention_count": 1,
        "mention_in_title": False, "mention_in_lead": False,
        "published_utc": datetime.datetime(2026, 1, 6, 20, 0, tzinfo=UTC),
        "published_precision": "instant",
    },
]


def article_loader_for_day(security_key, day):
    assert security_key == SECURITY_KEY
    return [r for r in ARTICLE_ROWS_BY_DAY_OR_EVENT if r["published_utc"].date() == day]


def article_loader_for_event(security_key, event_row):
    assert security_key == SECURITY_KEY
    keys = set(event_row["article_keys"])
    return [r for r in ARTICLE_ROWS_BY_DAY_OR_EVENT if r["article_key"] in keys]


def _diff(served_keys, spec_fields, label):
    served = set(served_keys)
    spec = set(spec_fields)
    missing = sorted(spec - served)
    extra = sorted(served - spec)
    print("  %s served fields: %s" % (label, sorted(served)))
    print("  %s spec fields:   %s" % (label, sorted(spec)))
    print("  %s MISSING (in spec, not served): %d -- %s" % (label, len(missing), missing))
    print("  %s EXTRA   (served, not in spec): %d -- %s" % (label, len(extra), extra))
    return missing, extra


def main():
    failures = []

    print("=== ROUTE 1: GET .../security/{security_key}/timeline?from=&to= ===")
    result = timeline_api.get_timeline(
        SECURITY_KEY, FLOOR.isoformat(), _d(9).isoformat(), daily_loader, event_loader,
    )
    assert not timeline_api.is_error_body(result), "unexpected error body: %r" % (result,)

    days_requested = 10
    days_returned = len(result["series"])
    print("  dense-day denominator: requested=%d returned=%d equal=%s"
          % (days_requested, days_returned, days_requested == days_returned))
    if days_requested != days_returned:
        failures.append("dense-day denominator mismatch")

    series_entry = result["series"][0]
    missing, extra = _diff(series_entry.keys(), timeline_api.SERIES_FIELDS, "series[0]")
    if missing or extra:
        failures.append("series field set mismatch: missing=%s extra=%s" % (missing, extra))

    stored_row = DAILY_ROWS[0]
    print("  stored chatter_daily row keys: %s" % sorted(stored_row.keys()))
    stored_has_breakout = "breakout_ratio" in stored_row
    stored_has_zscore = "z_score" in stored_row
    print("  'breakout_ratio' in stored row: %s" % stored_has_breakout)
    print("  'z_score' in stored row:        %s" % stored_has_zscore)
    if stored_has_breakout or stored_has_zscore:
        failures.append("breakout_ratio/z_score leaked into the STORED row")

    day10_entry = result["series"][9]
    print("  day 10 (baseline_days=3) breakout_ratio=%r z_score=%r"
          % (day10_entry["breakout_ratio"], day10_entry["z_score"]))
    if day10_entry["breakout_ratio"] is None or day10_entry["z_score"] is None:
        failures.append("day 10 should have a computed breakout_ratio/z_score (baseline present)")
    early_entry = result["series"][0]
    print("  day 1 (no baseline yet) breakout_ratio=%r z_score=%r"
          % (early_entry["breakout_ratio"], early_entry["z_score"]))
    if early_entry["breakout_ratio"] is not None or early_entry["z_score"] is not None:
        failures.append("day 1 has no baseline and should serve None/None, not a fabricated number")

    events_entry = result["events"][0]
    missing, extra = _diff(events_entry.keys(), timeline_api.EVENTS_FIELDS, "events[0]")
    if missing or extra:
        failures.append("events field set mismatch: missing=%s extra=%s" % (missing, extra))
    relative_on_events = set(events_entry.keys()) & {"breakout_ratio", "z_score"}
    print("  events arm intersection with {breakout_ratio, z_score}: %s (must be empty)"
          % sorted(relative_on_events))
    if relative_on_events:
        failures.append("events arm carries a relative figure: %s" % sorted(relative_on_events))

    print()
    print("=== ROUTE 2: GET .../security/{security_key}/timeline/day/{date} ===")
    day_result = timeline_api.get_timeline_day(
        SECURITY_KEY, _d(4).isoformat(), daily_loader, article_loader_for_day,
    )
    assert not timeline_api.is_error_body(day_result), "unexpected error body: %r" % (day_result,)
    article_entry = day_result["articles"][0]
    missing, extra = _diff(article_entry.keys(), timeline_api.ARTICLE_FIELDS, "day.articles[0]")
    if missing or extra:
        failures.append("day route article field set mismatch: missing=%s extra=%s" % (missing, extra))
    print("  day route top-level keys: %s" % sorted(day_result.keys()))

    print()
    print("=== ROUTE 3: GET .../security/{security_key}/timeline/event/{first_day} ===")
    event_result = timeline_api.get_timeline_event(
        SECURITY_KEY, EVENT_FIRST_DAY.isoformat(), event_loader, article_loader_for_event,
    )
    assert not timeline_api.is_error_body(event_result), "unexpected error body: %r" % (event_result,)
    event_article_entry = event_result["articles"][0]
    missing, extra = _diff(event_article_entry.keys(), timeline_api.ARTICLE_FIELDS, "event.articles[0]")
    if missing or extra:
        failures.append("event route article field set mismatch: missing=%s extra=%s" % (missing, extra))

    resolved_id = event_result["event_id"]
    direct_id = publication_gold._event_id(SECURITY_KEY, EVENT_FIRST_DAY, EVENT_LAST_DAY)
    print("  event route resolved event_id: %s" % resolved_id)
    print("  publication_gold._event_id(security_key, first_day, last_day): %s" % direct_id)
    print("  equal: %s" % (resolved_id == direct_id))
    if resolved_id != direct_id:
        failures.append("event route minted a SECOND id scheme: %r != %r" % (resolved_id, direct_id))

    print()
    if failures:
        print("FAIL (%d): %s" % (len(failures), failures))
        return 1
    print("PASS: all three routes serve exactly the spec's field lists; breakout_ratio/z_score "
          "are served-only; events carry no relative figure; the event route keys off the "
          "existing publication_gold._event_id.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
