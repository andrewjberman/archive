"""RIV-d-1 AC2 -- the sweep runs exactly the stages whose input marker has no output marker, in order, then stops;
a second sweep of the same day runs nothing. Stage runners are injected; markers are RIV-c-1's real module."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

ORDER = ["fetch-holdings", "build-silver", "build-canonical-shape", "build-trade-schedule", "publish-page"]


def run(v):
    c.setup_path()
    from rivalfunds import markers, sweep

    sink = f"local:{c.tmpdir('rv_d1b_')}"
    day = "2026-09-29"
    markers.write_marker("fetch-holdings", day, "b1", sink, {"outputs": []})
    markers.write_marker("build-silver", day, "b1", sink, {"outputs": []})
    calls = []

    def runner(stage):
        def _r(event):
            calls.append(stage)
            uri = markers.write_marker(stage, event["date"], event["batch_id"], sink, {"outputs": []})
            return {"status": "OK", "batch_id": event["batch_id"], "outputs": [], "marker": uri, "detail": {}}
        return _r

    runners = {s: runner(s) for s in ORDER}
    sweep.run_sweep(day, sink, runners)
    v.check(calls == ORDER[2:], f"first sweep ran the three stages missing an output marker, in order ({calls})")
    calls.clear()
    sweep.run_sweep(day, sink, runners)
    v.check(calls == [], f"second sweep runs nothing ({calls})")
    empty = f"local:{c.tmpdir('rv_d1c_')}"
    calls.clear()
    sweep.run_sweep(day, empty, {s: runner(s) for s in ORDER})
    v.check(calls[:1] == ["fetch-holdings"], f"a day with no markers starts at fetch-holdings ({calls})")
    v.check(callable(getattr(sweep, "handler_entry", None)), "sweep.handler_entry exists for the daily Lambda")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
