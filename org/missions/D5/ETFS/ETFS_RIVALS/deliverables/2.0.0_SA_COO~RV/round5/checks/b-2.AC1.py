"""RIV-b-2 AC1 (row W4-S9) -- a MARKER-DRIVEN G1 run over a batch of 50 report dates is windowed and CONTINUES across invocations
from a cursor, so any batch size completes inside a per-invocation time budget.

Fixture: 50 weekdays of Bloomberg silver (TXUE, BIDD) imported and built on a local sink; ONE build-bloomberg-silver marker for
batch `b` names all 50 silver outputs. G1 is called the way the trigger calls it (mode daily, the marker's date and batch id), with
the event field `budget_s` = 0.001 (the interface this cell adds: stop starting new dates once the budget is spent).
  - the first invocation returns status PARTIAL with a cursor and writes NO output marker;
  - re-invoking the same event continues from the cursor; within 60 invocations the run returns OK and writes the marker;
  - every one of the 50 dates has exactly ONE G1 object (no date is rebuilt into a second object);
  - control: without `budget_s` the same batch completes in ONE invocation (the unbounded path is unchanged)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

N = 50


def build(tag):
    from rivalfunds import collector_bloomberg as cb
    from rivalfunds import markers, silver_bloomberg, sinks

    tmp = pathlib.Path(c.tmpdir(f"rv_b2_{tag}_"))
    days = c.weekdays_ending("2026-09-29", N)
    files = [c.bbg_capture_file(tmp, d) for d in days]
    spec = f"local:{tmp / 'sink'}"
    r = cb.handler_entry({"mode": "import", "captures": files, "batch_id": "imp", "sink": spec, "date": days[-1]})
    assert r["status"] in ("OK", "PARTIAL"), r
    r = silver_bloomberg.handler_entry({"mode": "replay", "batch_id": "sb", "sink": spec, "date": days[-1]})
    assert r["status"] == "OK", r
    s = sinks.get_sink(spec)
    outs = [u for d in days for u in s.list(silver_bloomberg.silver_uri(d, "x").rsplit("/", 1)[0] + "/") if u.endswith(".parquet")]
    markers.write_marker("build-bloomberg-silver", days[-1], "b", spec, {"outputs": outs})
    return spec, s, days, outs


def g1_objects(s, days):
    from rivalfunds import homes
    return {d: [u for u in s.list(homes.canonical_shape(d) + "/") if u.endswith(".parquet")] for d in days}


def run(v):
    c.setup_path()
    from rivalfunds import gold_canonical_shape as g
    from rivalfunds import markers

    c.fake_crosswalk(g)
    spec, s, days, outs = build("bounded")
    print(f"fixture: {len(days)} dates, {len(outs)} silver outputs in the marker")
    ev = {"date": days[-1], "mode": "daily", "batch_id": "b", "sink": spec, "budget_s": 0.001}
    first = g.handler_entry(dict(ev))
    print("first:", first.get("status"), str(first.get("detail"))[:160])
    v.check(first.get("status") == "PARTIAL" and not markers.has_marker("build-canonical-shape", days[-1], s),
            "the first budgeted invocation returns PARTIAL and writes no output marker")
    n, last = 1, first
    while last.get("status") == "PARTIAL" and n < 60:
        last = g.handler_entry(dict(ev))
        n += 1
    objs = g1_objects(s, days)
    per = sorted({len(v_) for v_ in objs.values()})
    print(f"invocations {n}, final {last.get('status')}, G1 objects per date {per}")
    v.check(last.get("status") == "OK" and n > 1, f"the batch completes across {n} invocations (more than one)")
    v.check(per == [1], "every date has exactly one G1 object")
    spec2, s2, days2, _ = build("control")
    ctl = g.handler_entry({"date": days2[-1], "mode": "daily", "batch_id": "b", "sink": spec2})
    per2 = sorted({len(x) for x in g1_objects(s2, days2).values()})
    print("control (no budget):", ctl.get("status"), "objects per date", per2)
    v.check(ctl.get("status") == "OK" and per2 == [1], "control: without budget_s the batch completes in one invocation")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
