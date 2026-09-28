"""AC2 -- HVST-w-3: A FAILED CALL IS UNREACHABLE TO THE EMPTY-ARRAY ENCODING.

Exercises each of the three routes under THREE injected failures (a raised exception inside the
route, a timeout, and a malformed/unparseable upstream body) -- 9 cases -- then the CONTRAST that
makes it a real test: successful calls over an honest-empty range/day, whose `series`/`events`/
`articles` arrays are empty with `error` absent. Prints the exact predicate a caller uses to tell
the two shapes apart.

No S3, no network, no vendor call: every failure is INJECTED by a loader this script writes.

Run: python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~24/scripts/ac2_failure_never_reads_as_data.py
"""

import datetime
import os
import sys

sys.path.insert(0, os.getcwd())

import lib.research.harvest.timeline_api as timeline_api

UTC = datetime.timezone.utc
SECURITY_KEY = "TEST_HK_Equity"


# --------------------------------------------------------------------------
# the three failure injections -- each a loader that raises instead of returning rows
# --------------------------------------------------------------------------

def raise_exception(*_args, **_kwargs):
    raise RuntimeError("a raised exception inside the route")


def raise_timeout(*_args, **_kwargs):
    raise timeline_api.UpstreamTimeout("upstream call exceeded its deadline")


def raise_malformed(*_args, **_kwargs):
    raise timeline_api.UpstreamMalformed("upstream body could not be parsed as JSON")


FAILURE_INJECTIONS = [
    ("raised-exception", raise_exception),
    ("timeout", raise_timeout),
    ("malformed-upstream-body", raise_malformed),
]


def _ok(*_args, **_kwargs):
    return []


def _check_error_case(label, body, expected_absent_key):
    print("  [%s] body: %r" % (label, body))
    is_error = timeline_api.is_error_body(body)
    has_error_code = bool(body.get("error_code"))
    has_data_key = expected_absent_key in body
    print("    error is True: %s | error_code non-empty: %s (%r) | carries %r key: %s"
          % (is_error, has_error_code, body.get("error_code"), expected_absent_key, has_data_key))
    ok = is_error and has_error_code and not has_data_key
    return ok


def main():
    cases_ok = 0
    cases_total = 0
    failures = []

    print("=== 9 INJECTED FAILURES (3 routes x 3 failure types) ===")

    for label, failing_loader in FAILURE_INJECTIONS:
        cases_total += 1
        body = timeline_api.get_timeline(
            SECURITY_KEY, "2026-01-01", "2026-01-10", failing_loader, _ok,
        )
        ok = _check_error_case("timeline/%s" % label, body, "series")
        cases_ok += int(ok)
        if not ok:
            failures.append("timeline/%s" % label)

    for label, failing_loader in FAILURE_INJECTIONS:
        cases_total += 1
        body = timeline_api.get_timeline_day(
            SECURITY_KEY, "2026-01-01", failing_loader, _ok,
        )
        ok = _check_error_case("timeline/day/%s" % label, body, "articles")
        cases_ok += int(ok)
        if not ok:
            failures.append("timeline/day/%s" % label)

    for label, failing_loader in FAILURE_INJECTIONS:
        cases_total += 1
        body = timeline_api.get_timeline_event(
            SECURITY_KEY, "2026-01-01", failing_loader, _ok,
        )
        ok = _check_error_case("timeline/event/%s" % label, body, "articles")
        cases_ok += int(ok)
        if not ok:
            failures.append("timeline/event/%s" % label)

    print()
    print("  %d of %d failure cases present (error:true, non-empty error_code, no data key)"
          % (cases_ok, cases_total))

    print()
    print("=== THE CONTRAST: a SUCCESSFUL call over an honest-empty range/day ===")

    def empty_daily_loader(_security_key):
        return []

    def empty_event_loader(_security_key):
        return []

    honest_range = timeline_api.get_timeline(
        SECURITY_KEY, "2026-06-01", "2026-06-05", empty_daily_loader, empty_event_loader,
    )
    print("  [honest-empty range] body: %r" % (honest_range,))
    range_is_error = timeline_api.is_error_body(honest_range)
    range_series_empty = honest_range.get("series") == []
    range_events_empty = honest_range.get("events") == []
    range_has_error_key = "error" in honest_range
    print("    error present: %s | series == []: %s | events == []: %s"
          % (range_has_error_key, range_series_empty, range_events_empty))
    honest_ok = (not range_is_error) and range_series_empty and range_events_empty and not range_has_error_key
    if not honest_ok:
        failures.append("honest-empty range control did not read as honest-empty")

    # A day route contrast too: a day that DOES exist (COMPLETE, articles_total=0) is honest-empty
    # articles, never an error -- the same distinction the error envelope exists to preserve for
    # the `articles` array, not only `series`/`events`.
    quiet_day_row = {
        "security_key": SECURITY_KEY, "day": datetime.date(2026, 1, 1), "data_status": "COMPLETE",
        "articles_total": 0,
    }

    def quiet_daily_loader(_security_key):
        return [quiet_day_row]

    def quiet_article_loader(_security_key, _day):
        return []

    honest_day = timeline_api.get_timeline_day(
        SECURITY_KEY, "2026-01-01", quiet_daily_loader, quiet_article_loader,
    )
    print("  [honest-empty day] body: %r" % (honest_day,))
    day_is_error = timeline_api.is_error_body(honest_day)
    day_articles_empty = honest_day.get("articles") == []
    day_has_error_key = "error" in honest_day
    print("    error present: %s | articles == []: %s" % (day_has_error_key, day_articles_empty))
    honest_day_ok = (not day_is_error) and day_articles_empty and not day_has_error_key
    if not honest_day_ok:
        failures.append("honest-empty day control did not read as honest-empty")

    print()
    print("=== THE PREDICATE a consumer uses, with no knowledge of the request ===")
    print("  def is_error_body(body):")
    print("      return body.get('error') is True")
    print("  applied to an injected-failure body -> True; applied to an honest-empty body -> False.")
    sample_failure_body = timeline_api.get_timeline(
        SECURITY_KEY, "2026-01-01", "2026-01-10", raise_exception, _ok,
    )
    print("  predicate(failure body)     = %s" % timeline_api.is_error_body(sample_failure_body))
    print("  predicate(honest-empty body) = %s" % timeline_api.is_error_body(honest_range))
    if timeline_api.is_error_body(sample_failure_body) is not True:
        failures.append("predicate did not read the failure body as an error")
    if timeline_api.is_error_body(honest_range) is not False:
        failures.append("predicate misread the honest-empty body as an error")

    print()
    if failures or cases_ok != cases_total:
        print("FAIL: %d of %d failure cases present; failures=%s" % (cases_ok, cases_total, failures))
        return 1
    print("PASS: 9 of 9 failure cases present (error:true, non-empty error_code, no data key); "
          "honest-empty range AND honest-empty day controls both present with error absent; "
          "the predicate distinguishes both.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
