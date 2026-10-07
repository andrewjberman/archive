"""RIV-ab-1 AC2 (row Z-S54; ROUND_ANALYSIS.round13.md ADDENDUM 1 @594d1be8f8 (A)): the sweep refreshes the A1 tables BEFORE the AI
step, so an account is written against the build the page serves.

Measured 2026-10-06: `sweep.run_ai_step` ran `ai_stage.run_for_day` at 13:00:20Z against the 11:03Z tables; only the republish
that follows it (publish_page.produce_a1's stale rebuild) rebuilt holding_contribution and buying_trend, at 13:05-13:06Z.

Interface (prescribed): `sweep.run_ai_step` calls `publish_page.produce_a1(<sink object>, <sink spec>, <date>)` (the stale-table
refresh: it rebuilds a table only when an input is newer, and SKIPS otherwise) BEFORE `ai_stage.run_for_day`, and records its
result under `a1_refresh` in the step's return value. A refresh that raises is recorded and the AI step still runs (the account
is optional, the page is not). When the AI step does not apply (gate off, no page marker, no time left) nothing is refreshed.
Offline: `ai_stage.run_for_day`, `publish_page.produce_a1`, the markers and the publish-page runner are stubbed and record calls.
  - (a) with the gate on and a page marker: the call order is produce_a1, then run_for_day, then the republish; the result
    carries `a1_refresh`;
  - (b) a produce_a1 that raises is recorded under `a1_refresh` and run_for_day still runs;
  - (c) control: with the gate off, run_ai_step returns None and calls nothing.
FAIL at base: (a), (b) FAIL (no refresh before the AI step); (c) PASSES."""
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


class Marks:
    def has_marker(self, stage, date, sink):
        return True


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import ai_stage, publish_page, sweep

    spec = f"local:{c.tmpdir('rv_ab1_')}"
    ev = {"date": "2026-10-06", "sink": spec, "mode": "daily", "run_path": "scheduled"}
    calls = []

    def runner(e):
        calls.append("republish")
        return {"status": "OK", "outputs": [], "batch_id": e.get("batch_id")}

    def ai(sink, date, run_path=None, deadline_s=None):
        calls.append("ai")
        return {"status": "OK", "reason": None, "run_id": "r1", "run_path": run_path}

    def refresh_ok(s, sink_spec, day, refresh=False):
        calls.append("refresh")
        return {"holding_contribution": {"status": "OK", "stale_rebuilt": True}}

    def refresh_bad(s, sink_spec, day, refresh=False):
        calls.append("refresh")
        raise RuntimeError("planted refresh failure")

    sweep._ai_deadline_s = lambda e, ctx: 100.0
    ai_stage.run_for_day = ai
    old_env = os.environ.get(ai_stage.ENABLE_ENV)
    try:
        os.environ[ai_stage.ENABLE_ENV] = "1"
        publish_page.produce_a1 = refresh_ok
        r = sweep.run_ai_step(dict(ev), None, {"publish-page": runner}, markers=Marks())
        print("(a) calls:", calls, "| a1_refresh in result:", isinstance(r, dict) and "a1_refresh" in r)
        v.check(calls == ["refresh", "ai", "republish"] and isinstance(r, dict) and "a1_refresh" in r,
                "(a) the table refresh runs before the AI step, then the republish; the result carries a1_refresh")

        calls.clear()
        publish_page.produce_a1 = refresh_bad
        r2 = sweep.run_ai_step(dict(ev), None, {"publish-page": runner}, markers=Marks())
        print("(b) calls:", calls, "| a1_refresh:", (r2 or {}).get("a1_refresh"))
        v.check(calls[:2] == ["refresh", "ai"] and isinstance(r2, dict) and r2.get("a1_refresh") is not None,
                "(b) a failing refresh is recorded and the AI step still runs")

        calls.clear()
        os.environ[ai_stage.ENABLE_ENV] = "0"
        publish_page.produce_a1 = refresh_ok
        r3 = sweep.run_ai_step(dict(ev), None, {"publish-page": runner}, markers=Marks())
        print("(c) gate off ->", r3, calls)
        v.check(r3 is None and calls == [], "(c) control: with the gate off nothing runs")
    finally:
        if old_env is None:
            os.environ.pop(ai_stage.ENABLE_ENV, None)
        else:
            os.environ[ai_stage.ENABLE_ENV] = old_env


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
