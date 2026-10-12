"""RIV-xb-1 checks (round 29): the lookup's search retries a vendor 5xx or a transport failure, at most twice with backoff,
never a 4xx, and a final failure records its class and the vendor's message.

    cd data/etfs/scripts && python -m pytest -q <this file>

Offline: `serp_search(query, _call=<fake>, _sleep=<recorder>)` -- no key read, no network, no real sleep.
`_call(query)` stands for `serp.serp_brightdata_records(query, max_pages=1, gl="us", hl="en")`: it returns that function's dict
({"status": "OK"|"FAILED", "records": [{"title","link","snippet"}], "failure": {"kind","http_status","brd_status",
"brd_error_code","brd_error"}}).
"""
import pytest

from rivalfunds import dramatic_move as dm

OK = {"status": "OK", "records": [{"title": "T", "link": "https://example.test/x", "snippet": "S"}], "failure": None}


def _fail(kind, http=200, brd="502", code="expect_element", msg='waiting for selector "#main" failed: timeout 30000ms exceeded'):
    return {"status": "FAILED", "records": [], "failure": {"kind": kind, "http_status": http, "brd_status": brd,
                                                           "brd_error_code": code, "brd_error": msg}}


class Plan:
    def __init__(self, *results):
        self.results, self.calls = list(results), []

    def __call__(self, query):
        self.calls.append(query)
        return self.results[min(len(self.calls) - 1, len(self.results) - 1)]


def _run(plan):
    slept = []
    return slept, lambda: dm.serp_search("Q", _call=plan, _sleep=slept.append)


def test_ac1_a_planted_vendor_502_then_success_ends_in_success():
    plan = Plan(_fail("VENDOR"), OK)
    slept, go = _run(plan)
    assert go() == [{"title": "T", "url": "https://example.test/x", "snippet": "S"}]
    assert len(plan.calls) == 2 and slept == [1.0]


def test_ac1_a_transport_failure_is_retried_too_and_two_retries_are_the_most():
    plan = Plan(_fail("TRANSPORT", http=None, brd=None, code=None, msg=None), _fail("VENDOR"), OK)
    slept, go = _run(plan)
    assert go()[0]["url"] == "https://example.test/x"
    assert len(plan.calls) == 3 and slept == [1.0, 2.0]


def test_ac2_a_persistent_502_records_its_class_its_attempts_and_the_vendors_message():
    plan = Plan(_fail("VENDOR"))
    slept, go = _run(plan)
    with pytest.raises(RuntimeError) as e:
        go()
    msg = str(e.value)
    assert "SERP FAILED" in msg and "VENDOR" in msg and "3 attempts" in msg
    assert "expect_element" in msg and "waiting for selector" in msg
    assert len(plan.calls) == 3 and slept == [1.0, 2.0]


def test_ac3_a_4xx_is_never_retried():
    plan = Plan(_fail("CONFIG", http=403, brd=None, code=None, msg="forbidden"), OK)
    slept, go = _run(plan)
    with pytest.raises(RuntimeError) as e:
        go()
    assert "CONFIG" in str(e.value) and "1 attempt" in str(e.value)
    assert len(plan.calls) == 1 and slept == []


def test_ac4_a_captcha_is_left_to_the_client_and_not_retried_again():
    """`serp.serp_brightdata_records` already retries a captcha (`brd_error_code == "captcha"`) and a 5xx itself; the lookup's
    outer retry must not multiply those (up to 9 requests for one search): a captcha failure is raised after ONE attempt."""
    plan = Plan(_fail("VENDOR", brd=None, code="captcha", msg="captcha"), OK)
    slept, go = _run(plan)
    with pytest.raises(RuntimeError) as e:
        go()
    assert "VENDOR" in str(e.value) and "captcha" in str(e.value) and "1 attempt" in str(e.value)
    assert len(plan.calls) == 1 and slept == []


def test_a_first_try_success_sleeps_and_retries_nothing():
    plan = Plan(OK)
    slept, go = _run(plan)
    assert len(go()) == 1 and len(plan.calls) == 1 and slept == []


def test_run_for_day_counts_a_persistent_failure_once_and_goes_on(tmp_path):
    import pandas as pd
    from rivalfunds import sinks
    g4 = pd.DataFrame([{"security_id": "T US Equity", "security_name": "Tokio Marine Holdings Inc", "date": d, "px_close": px}
                       for d, px in (("2026-10-07", 7500.0), ("2026-10-08", 500.0))])
    plan = Plan(_fail("VENDOR"))
    rep = dm.run_for_day("2026-10-08", sinks.LocalSink(str(tmp_path)), g4=g4, actions=pd.DataFrame(),
                         search=lambda q: dm.serp_search(q, _call=plan, _sleep=lambda s: None))
    assert len(plan.calls) == 3                      # the retries happen INSIDE the one counted search
    assert rep["failed"] == 1 and rep["written"] == 0 and rep["calls"] == 1
