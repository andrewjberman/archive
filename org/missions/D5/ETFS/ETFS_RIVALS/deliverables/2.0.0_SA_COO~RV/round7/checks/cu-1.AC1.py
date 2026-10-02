"""RIV-cu-1 AC1 (row ETFS_RIVALS-Z-W4-S9, its continuation half; issuer act I-1, evidence C:/tmp/r7i1/): the 09:00 ET
sweep continues every OPEN G1 cursor of an earlier marker date inside its lookback, so a batch that ended PARTIAL
completes on the next scheduled sweep. Source: I-1 fired batch `d5-gqgu-03` (its build-silver marker under
date=2026-10-01 lists 60 report dates, 2026-03-31..06-25) through the canonical-shape Lambda. Invocations 1 and 2 ended
PARTIAL (23/60, then 44/60) and left `state/build_canonical_shape/date=2026-10-01/d5-gqgu-03.cursor` with no `.json`
marker; only a third invoke fired by hand finished it (run1.json, run1.log). Nothing continues a cursor across
invocations: the canonical-shape rule fires only on a NEW silver marker (generated.auto.tfvars.json `rules`), and
`sweep.run_dag` walks only its own day. FAIL at base: `sweep.handler_entry` never reads a cursor of another day.

Interface (prescribed; the issuer copies it into the cell; write set sweep.py):
- An OPEN cursor is a `markers.cursor_uri("build-canonical-shape", D, B)` object whose marker `homes.marker_uri(...)`
  is absent. A cursor beside its marker is CLOSED: G1 leaves the cursor in place when it finishes. The sweep lists the
  stage's state prefix, `homes.address("rivalfunds", "etfs", "state", "build_canonical_shape", "date=")`.
- `sweep.CURSOR_LOOKBACK_DAYS = 10`: the window is the 10 NYSE trading days before the sweep's day
  (`lib.trading_calendar.prev_trading_day`), the day itself excluded (its own DAG already continues a cursor of its own
  day). For 2026-10-02 the window is 2026-09-18..2026-10-01.
- Each open cursor in the window is continued through `run_gold_chain({"date": D, "mode": "daily", "batch_id": B,
  "sink": <sink>}, <the sweep's runners>)`: G1 continues from its cursor, then G2 and the gated G5 for that batch, as
  the canonical-shape Lambda does for one marker event. Nothing else runs for D: no fetch, no silver, no publish. The
  G5 marker's own rule publishes; no rule watches build_canonical_shape markers, so G2 and G5 run here or never.
- Within the budget: a continuation starts only while the Lambda has more than MARGIN_MS left, and its G1 event
  carries `budget_s` <= (remaining ms - MARGIN_MS) / 1000 whenever that is under G1's own budget (600 s).
- Report: `result["detail"]["open_cursors"]`, a list with one dict per open cursor of an EARLIER day:
  {"date": D, "batch_id": B, "action": "continued" | "beyond_lookback" | "out_of_time", ...}; a continued entry also
  carries "status" (the chain's result status). Absent or [] when there is none.
- Order relative to the day's own DAG: free (not graded).

Fixture (offline, local sink; `_common.offline_guards()`; AI gate unset): every stage module's `handler_entry` and
`sweep._real_runners` are stubs that record (stage, date, batch_id, mode, budget_s, and for G1 the done-count of the
cursor it reads) and write the stage's marker at the builder's address, its outputs derived from the batch's input
marker. The sweep runs through `sweep.handler_entry` with the sweep schedule's own input (`_s24_sweep.schedule_payload`:
scheduled-time 2026-10-02T13:00:00Z, sink local) and a Lambda-like context of 900 s. Every fixture plants the complete
daily chain of 2026-10-01 and a pull-enrichment marker under 2026-10-02 (the G3 gate admits every batch).
  - (a) the I-1 state: own day 2026-10-02 complete; batch d5-gqgu-03's build-silver marker under 2026-10-01 listing the
    60 report dates, its cursor with 44 done, no G1 marker.
    (a1) G1 runs ONCE for (2026-10-01, d5-gqgu-03), mode daily, and reads the planted cursor (44 done);
    (a2) the G1 marker is written and the cursor is closed; a second sweep with the same payload runs nothing;
    (a3) the runner calls are exactly G1, G2 and G5 of that batch (no other stage, no other day);
    (a4) detail.open_cursors reports it: action continued, status OK.
  - (b) control, no open cursor: the I-1 END state (the cursor beside its G1, G2, G5 and G6 markers) and an own day
    with work (its fetch-holdings marker only). The runners called are exactly the day's DAG (build-silver, G1, G2, G5,
    publish-page of the day's batch); the result (status, ran, outputs, complete, stopped_at, waiting, unresolved,
    out_of_time) is today's and open_cursors is absent or []; the sink gains exactly the five day markers.
  - (c) the bound: open cursors under 2026-09-18 (10th trading day back), 2026-09-17 (11th) and 2026-06-01.
    (c1) the two beyond the window are left alone: no runner call, cursor bytes unchanged, no G1 marker;
    (c2) both are reported: action beyond_lookback;
    (c3) the one under 2026-09-18 is continued (G1 runs, its marker is written);
    (c4) sweep.CURSOR_LOOKBACK_DAYS == 10.
  - (d) within the budget: the (a) state with 600 s left at the start. G1 still runs for the batch, and its event
    carries 0 < budget_s <= 450 (600 s less MARGIN_MS).
Base: a1-a4, c2-c4 and d FAIL; b and c1 PASS (nothing reads another day's cursor, so nothing is touched)."""
import hashlib
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _s24_sweep as p  # noqa: E402

G1, G2, G5 = "build-canonical-shape", "build-coverage", "build-trade-schedule"
DAY = "2026-10-02"  # the sweep's own day (a Friday)
T1 = "2026-10-01"  # the I-1 batch's marker date
BATCH = "d5-gqgu-03"
FIRST, LAST, N_DATES, DONE = "2026-03-31", "2026-06-25", 60, 44
OLD = "2026-06-01"
LOOKBACK = 10
CALLS = []
_DATE_RE = re.compile(r"date=(\d{4}-\d{2}-\d{2})")


def _sha12(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def _dates(uris):
    return sorted({m.group(1) for m in (_DATE_RE.search(str(u)) for u in uris) if m})


def _prev(d, n):
    """The n NYSE trading days before d, newest first."""
    import datetime as dt

    from lib.trading_calendar import prev_trading_day

    out, cur = [], dt.date.fromisoformat(d)
    for _ in range(n):
        cur = prev_trading_day(cur)
        out.append(cur.isoformat())
    return out


def outs_of(stage, d, b, rds):
    """A stage's outputs for batch b of marker day d over report dates rds (builder addresses, the real key shapes)."""
    from rivalfunds import homes

    last = max(rds) if rds else d
    if stage == "build-silver":
        return [homes.issuer_silver(rd, "gqgu-20260929T204153Z-%s.parquet" % _sha12(rd)) for rd in rds]
    if stage == G1:
        return [homes.canonical_shape(rd, "holdings-20260930T151301Z-b02-%s.parquet" % _sha12(rd)) for rd in rds]
    if stage == G2:
        return [homes.address("rivalfunds", "etfs", "gold", "holdings_coverage", "date=" + last,
                              "holdings_coverage.parquet")]
    if stage == G5:
        return [homes.trade_schedule(last, "trade_schedule-%s.parquet" % b)]
    if stage == "publish-page":
        return [homes.page(d, "index.html")]
    return []


def stub(stage):
    def run(ev):
        from rivalfunds import markers

        d, b, spec = ev["date"], ev["batch_id"], ev["sink"]
        rec = {"stage": stage, "date": d, "batch_id": b, "mode": ev.get("mode"), "budget_s": ev.get("budget_s")}
        CALLS.append(rec)
        rds = []
        if stage == "build-silver":
            rds = [_prev(d, 1)[0]]
        elif stage in (G1, G2, G5):
            if stage == G1:
                cur = markers.read_cursor(G1, d, b, spec)
                rec["cursor_done"] = len(cur.get("done") or {}) if cur else None
            up = markers.get_marker("build-silver" if stage == G1 else G1, d, b, spec)
            if not up:
                return {"status": "SKIPPED", "batch_id": b, "outputs": [], "marker": None, "detail": "no input marker"}
            rds = _dates(up.get("outputs", []))
        outs = outs_of(stage, d, b, rds)
        uri = markers.write_marker(stage, d, b, spec, {"status": "OK", "outputs": outs})
        return {"status": "OK", "batch_id": b, "outputs": outs, "marker": uri, "detail": {}}
    return run


def install():
    c.setup_path()
    c.offline_guards()
    p.gate(False)
    from rivalfunds import (collector_issuer, gold_canonical_shape, gold_holdings_coverage, gold_peer_group_map,
                            gold_trade_schedule, publish_page, silver_bloomberg, silver_issuer, sweep)

    runners = {st: stub(st) for st in sweep.ALL_STAGES}
    mods = {"fetch-holdings": collector_issuer, "build-silver": silver_issuer,
            "build-bloomberg-silver": silver_bloomberg, G1: gold_canonical_shape, G2: gold_holdings_coverage,
            G5: gold_trade_schedule, "publish-page": publish_page, "build-peer-group-map": gold_peer_group_map}
    for st, m in mods.items():
        m.handler_entry = runners[st]
    sweep._real_runners = lambda: dict(runners)


def mark(spec, stage, d, b, rds):
    from rivalfunds import markers

    return markers.write_marker(stage, d, b, spec, {"status": "OK", "outputs": outs_of(stage, d, b, rds)})


def plant_chain(spec, d, b, upto=None):
    """A daily chain for day d, batch b over report date T-1: every stage, or the stages through `upto`."""
    rds = [_prev(d, 1)[0]]
    for st in ("build-peer-group-map", "fetch-holdings", "build-silver", G1, G2, G5, "publish-page"):
        mark(spec, st, d, "g0" if st == "build-peer-group-map" else b, rds)
        if st == upto:
            return


def plant_batch(spec, d, b, rds, done_n, closed=False):
    """A G1 batch as I-1 left it: the build-silver marker over rds, a cursor with done_n dates done (the real cursor
    body: {date: {output, pick, unread}}), and, when closed, the G1/G2/G5/G6 markers beside it."""
    from rivalfunds import markers

    mark(spec, "build-silver", d, b, rds)
    done = {rd: {"output": outs_of(G1, d, b, [rd])[0], "pick": {"GQGU": "issuer", "TXUE": "bloomberg"},
                 "unread": ["IDVZ", "PFOE"]} for rd in rds[:done_n]}
    markers.write_cursor(G1, d, b, spec, {"done": done})
    if closed:
        for st in (G1, G2, G5, "build-flow-reconciliation"):
            mark(spec, st, d, b, rds)


def fixture(own_work=False):
    from rivalfunds import sinks

    tmp = pathlib.Path(c.tmpdir("rv_cu1_"))
    spec = f"local:{tmp}"
    plant_chain(spec, DAY, "own", upto="fetch-holdings" if own_work else None)
    plant_chain(spec, T1, "d1001-exec")
    mark(spec, "pull-enrichment", DAY, "enr-" + DAY, [])
    return spec, sinks.get_sink(spec), tmp


def sweep_once(spec, total_ms=900_000):
    from rivalfunds import sweep

    CALLS.clear()
    r = sweep.handler_entry(p.schedule_payload(spec, day=DAY), p.Context(total_ms))
    return r, [dict(x) for x in CALLS]


def triples(calls):
    return [(x["stage"], x["date"], x["batch_id"]) for x in calls]


def entry(r, d, b):
    oc = (r.get("detail") or {}).get("open_cursors")
    return next((e for e in (oc if isinstance(oc, list) else []) if isinstance(e, dict) and e.get("date") == d
                 and e.get("batch_id") == b), None)


def is_open(s, d, b):
    from rivalfunds import homes, markers

    return s.exists(markers.cursor_uri(G1, d, b)) and not s.exists(homes.marker_uri(G1, d, b))


def rel(uri):
    from rivalfunds import sinks

    bucket, key = sinks.split_uri(uri)
    return f"{bucket}/{key}"


def limb_a(v):
    from lib.trading_calendar import trading_days_between
    from rivalfunds import homes

    rds = [x.isoformat() for x in trading_days_between(FIRST, LAST)]
    spec, s, tmp = fixture()
    plant_batch(spec, T1, BATCH, rds, DONE)
    print("(a) plant:", len(rds), "report dates", rds[0], "..", rds[-1], "| cursor open:", is_open(s, T1, BATCH),
          "| G1 marker:", s.exists(homes.marker_uri(G1, T1, BATCH)))
    r, calls = sweep_once(spec)
    d = r.get("detail") or {}
    print("(a) sweep:", r.get("status"), "| ran:", d.get("ran"), "| runner calls:", triples(calls),
          "| open_cursors:", d.get("open_cursors"))
    g1 = [x for x in calls if (x["stage"], x["date"], x["batch_id"]) == (G1, T1, BATCH)]
    print("(a) G1 calls for the batch:", g1)
    v.check(len(g1) == 1 and g1[0]["mode"] == "daily" and g1[0].get("cursor_done") == DONE,
            "(a1) the sweep runs G1 ONCE for (%s, %s), mode daily, and it reads the planted cursor (%d done)"
            % (T1, BATCH, DONE))
    marker1, open1 = s.exists(homes.marker_uri(G1, T1, BATCH)), is_open(s, T1, BATCH)
    exp = [(G1, T1, BATCH), (G2, T1, BATCH), (G5, T1, BATCH)]
    e = entry(r, T1, BATCH)
    r2, calls2 = sweep_once(spec)
    print("(a) after: G1 marker:", marker1, "| cursor open:", open1, "| second sweep calls:", triples(calls2),
          "| its entry:", entry(r2, T1, BATCH))
    v.check(marker1 and not open1 and calls2 == [] and (entry(r2, T1, BATCH) or {}).get("action") != "continued",
            "(a2) the G1 marker is written and the cursor is closed; a second sweep with the same payload runs nothing")
    v.check(triples(calls) == exp, "(a3) the runner calls are exactly G1, G2 and G5 of the batch: %s" % exp)
    v.check(bool(e) and e.get("action") == "continued" and e.get("status") == "OK",
            "(a4) detail.open_cursors reports the batch: action continued, status OK")


def limb_b(v):
    from lib.trading_calendar import trading_days_between
    from rivalfunds import homes

    rds = [x.isoformat() for x in trading_days_between(FIRST, LAST)]
    spec, s, tmp = fixture(own_work=True)
    plant_batch(spec, T1, BATCH, rds, DONE, closed=True)
    print("(b) plant: I-1 end state, cursor open:", is_open(s, T1, BATCH), "| own day: fetch-holdings marker only")
    before = p.snapshot(tmp)
    r, calls = sweep_once(spec)
    after = p.snapshot(tmp)
    d = r.get("detail") or {}
    day_stages = ("build-silver", G1, G2, G5, "publish-page")
    exp_calls = [(st, DAY, "own") for st in day_stages]
    t1 = [_prev(DAY, 1)[0]]
    exp_out = [u for st in day_stages for u in outs_of(st, DAY, "own", t1)]
    got ={"status": r.get("status"), "ran": d.get("ran"), "outputs": r.get("outputs"), "complete": d.get("complete"),
           "stopped_at": d.get("stopped_at"), "waiting": d.get("waiting"), "unresolved": d.get("unresolved"),
           "out_of_time": d.get("out_of_time")}
    exp = {"status": "OK", "ran": list(day_stages), "outputs": exp_out, "complete": True, "stopped_at": None,
           "waiting": [], "unresolved": {}, "out_of_time": False}
    new = sorted(set(after) - set(before))
    changed = sorted(k for k in before if after.get(k) != before[k])
    exp_new = sorted(rel(homes.marker_uri(st, DAY, "own")) for st in day_stages)
    print("(b) runner calls:", triples(calls))
    print("(b) result:", {k: v_ for k, v_ in got.items() if k != "outputs"}, "| outputs:", len(got["outputs"] or []),
          "| open_cursors:", d.get("open_cursors"))
    print("(b) sink: new", [k.rsplit("/", 3)[-3:] for k in new], "| changed:", changed)
    v.check(triples(calls) == exp_calls, "(b1) control: the runners called are exactly the day's DAG %s" % exp_calls)
    v.check(got == exp and d.get("open_cursors") in (None, []),
            "(b2) control: the result is today's (status OK, the same ran and outputs, complete) and no open cursor "
            "is reported")
    v.check(new == exp_new and changed == [],
            "(b3) control: the sink gains exactly the five day markers and no planted object changes")


def limb_c(v):
    from rivalfunds import homes, markers, sweep

    back = _prev(DAY, LOOKBACK + 1)
    d_in, d_out = back[LOOKBACK - 1], back[LOOKBACK]
    plants = [(d_in, "d5-edge-in"), (d_out, "d5-edge-out"), (OLD, "d5-old-01")]
    spec, s, tmp = fixture()
    for d, b in plants:
        plant_batch(spec, d, b, sorted(_prev(d, 6)), 3)
    cur0 = {(d, b): s.get(markers.cursor_uri(G1, d, b)) for d, b in plants}
    print("(c) window: %d trading days before %s = %s..%s | planted under %s" % (LOOKBACK, DAY, back[LOOKBACK - 1],
                                                                               back[0], [d for d, _ in plants]))
    r, calls = sweep_once(spec)
    print("(c) runner calls:", triples(calls), "| open_cursors:", (r.get("detail") or {}).get("open_cursors"))
    stale = plants[1:]
    untouched = all(not any((x["date"], x["batch_id"]) == (d, b) for x in calls)
                    and s.get(markers.cursor_uri(G1, d, b)) == cur0[(d, b)]
                    and not s.exists(homes.marker_uri(G1, d, b)) for d, b in stale)
    v.check(untouched, "(c1) the cursors under %s and %s (beyond the lookback) are left alone: no runner call, bytes "
                       "unchanged, no G1 marker" % (d_out, OLD))
    v.check(all((entry(r, d, b) or {}).get("action") == "beyond_lookback" for d, b in stale),
            "(c2) both are reported in detail.open_cursors: action beyond_lookback")
    v.check(any((x["stage"], x["date"], x["batch_id"]) == (G1, d_in, "d5-edge-in") for x in calls)
            and s.exists(homes.marker_uri(G1, d_in, "d5-edge-in")),
            "(c3) the cursor under %s (the 10th trading day back) is continued: G1 runs, its marker is written" % d_in)
    lb = getattr(sweep, "CURSOR_LOOKBACK_DAYS", None)
    print("(c) sweep.CURSOR_LOOKBACK_DAYS:", lb)
    v.check(lb == LOOKBACK, "(c4) sweep.CURSOR_LOOKBACK_DAYS == %d (the stated lookback)" % LOOKBACK)


def limb_d(v):
    from lib.trading_calendar import trading_days_between
    from rivalfunds import sweep

    rds = [x.isoformat() for x in trading_days_between(FIRST, LAST)]
    spec, s, tmp = fixture()
    plant_batch(spec, T1, BATCH, rds, DONE)
    r, calls = sweep_once(spec, total_ms=600_000)
    g1 = [x for x in calls if (x["stage"], x["date"], x["batch_id"]) == (G1, T1, BATCH)]
    cap = (600_000 - sweep.MARGIN_MS) / 1000.0
    print("(d) 600 s left at the start | G1 calls for the batch:", g1, "| cap:", cap)
    b0 = g1[0].get("budget_s") if g1 else None
    ok = isinstance(b0, (int, float)) and not isinstance(b0, bool) and 0 < b0 <= cap
    v.check(bool(g1) and ok, "(d) within the budget: G1 runs for the batch with 0 < budget_s <= %.0f" % cap)


def run(v):
    install()
    for name, fn in (("a", limb_a), ("b", limb_b), ("c", limb_c), ("d", limb_d)):
        try:
            fn(v)
        except Exception as e:  # a limb's exception is its own FAIL; the next limb still runs
            v.check(False, "(%s) exception: %s: %s" % (name, type(e).__name__, e))


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
