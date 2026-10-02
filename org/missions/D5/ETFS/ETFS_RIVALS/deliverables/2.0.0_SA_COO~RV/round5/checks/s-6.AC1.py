"""RIV-s-6 AC1 (row W3-S15; analysis ruling 4) -- the G4 producer never writes a current-value pull under a past partition date: a
past date uses a historical request, or the pull is refused/labelled.

Offline, with the Bloomberg hooks stubbed (no Bloomberg call): `enrichment_bloomberg._blp_reference_data` returns current values
for `X US Equity`; `enrichment_bloomberg._blp_historical_data` (the hook this cell adds) returns values dated 2025-06-30.
  - past date, historical hook raising: `handler_entry({"mode": "market", "date": "2025-06-30", ...})` writes NO G4 row under
    date=2025-06-30 whose `as_of` is 2025-06-30 (today it does, from the current-value pull);
  - past date, historical hook answering: a G4 object lands under date=2025-06-30, its rows `as_of` 2025-06-30 and
    `as_of_source` = historical;
  - control: today's ET date (the run date) with the reference stub still lands its G4 rows, `as_of_source` = pull."""
import datetime as dt
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAST = "2025-06-30"
SEC = "X US Equity"


def run(v):
    c.setup_path()
    import pyarrow.parquet as pq
    from rivalfunds import enrichment_bloomberg as e
    from rivalfunds import homes, sinks

    vals = {f: 1.0 for f in e.MARKET_FIELDS}
    e._blp_reference_data = lambda secs, fields, overrides=None, timeout_s=90.0: {s_: dict(vals) for s_ in secs}

    def g4(spec, date):
        s = sinks.get_sink(spec)
        pre = homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={date}") + "/"
        rows = []
        for u in s.list(pre):
            if u.endswith(".parquet"):
                rows += pq.read_table(io.BytesIO(s.get(u))).to_pylist()
        return rows

    def boom(*a, **k):
        raise RuntimeError("no historical data in this arm")
    e._blp_historical_data = boom
    spec = f"local:{c.tmpdir('rv_s6a_')}"
    r = e.handler_entry({"mode": "market", "date": PAST, "securities": [SEC], "batch_id": "a", "sink": spec})
    rows = g4(spec, PAST)
    bad = [x for x in rows if str(x.get("as_of"))[:10] == PAST]
    print(f"past, no historical: status {r.get('status')}, rows under {PAST}: {len(rows)}, claiming as_of {PAST}: {len(bad)}")
    v.check(not bad, f"no G4 row under date={PAST} claims as_of {PAST} from a current-value pull")

    e._blp_historical_data = lambda secs, fields, start, end, **k: {s_: {PAST: dict(vals)} for s_ in secs}
    spec = f"local:{c.tmpdir('rv_s6b_')}"
    r = e.handler_entry({"mode": "market", "date": PAST, "securities": [SEC], "batch_id": "b", "sink": spec})
    rows = g4(spec, PAST)
    good = [x for x in rows if str(x.get("as_of"))[:10] == PAST and x.get("as_of_source") == "historical"]
    print(f"past, historical: status {r.get('status')}, rows {len(rows)}, historical-sourced {len(good)}")
    v.check(len(good) >= 1, f"a historical request lands G4 rows under {PAST} with as_of_source historical")

    import zoneinfo
    today = dt.datetime.now(zoneinfo.ZoneInfo("America/New_York")).date().isoformat()  # the run date is an ET date
    spec = f"local:{c.tmpdir('rv_s6c_')}"
    r = e.handler_entry({"mode": "market", "date": today, "securities": [SEC], "batch_id": "c", "sink": spec})
    rows = g4(spec, today)
    print(f"control today {today}: status {r.get('status')}, rows {len(rows)}, as_of_source {sorted({str(x.get('as_of_source')) for x in rows})}")
    v.check(len(rows) >= 1 and all(x.get("as_of_source") == "pull" for x in rows),
            "control: today's pull still lands its rows, as_of_source pull")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
