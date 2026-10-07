"""RIV-bf-1 AC2 (FWD-22; F.5 card 2 answer; WORLD; ROUND15_CELLS_DRAFT.md revision 1.5; amended round 20, RIV-bk-1): a range
backfill that fits sends ONE historical request per batch of 50 securities per contiguous run of un-held trading days (ONE CRNCY
reference request first, for the securities with no stored currency), lands one `security_market` object per date labelled
`backfill`, never overwrites a date that already holds a market object, and records its points in the budget ledger.

Measured today (CLOUD 90e794e816): `{"mode": "market-range"}` returns FAILED "bad event: mode 'market-range' is not ..."; the
only past-date route is `market`, one date per run (`_market_pull`, one-day `_blp_historical_data` per batch).

Interface (prescribed, verbatim from the cell): event `{"mode": "market-range", "start", "end", "securities": [...], "batch_id",
"sink", "max_points": int, "dry_run": bool}`. [...] Otherwise ONE historical request per batch of 50 securities over `[start,
end]` for `px_close`'s field only; it writes one `gold/security_market/date=<D>` object per date that has rows (never overwriting
an existing object of that date: a date already holding a `market-*.parquet` is skipped and counted), each row `as_of_source =
"backfill"`; it records the points in the `bbg_budget` ledger with mode `market-range`.
NO Bloomberg call: the vendor seam is the one `tests/test_s4_security_market.py` and `tests/test_r12eb1_session_attempts.py` stub
(`enrichment_bloomberg._blp_historical_data` / `_blp_reference_data`), bound here to a RECORDING stub that answers every requested
field for every trading day of the request; `integrations.bloomberg.mcp` is replaced by a module that records and raises;
`_run_date_et` is pinned to 2026-10-06; the budget ledger is a fresh temp dir (`RIVALFUNDS_BBG_BUDGET_DIR`); the sink is `local:`.
Fixture: 60 securities (`S000 US Equity` .. `S059 US Equity`), start 2026-09-21 (Monday), end 2026-09-28 (Monday): 6 NYSE
trading days, 360 points, `max_points` 1000, `dry_run` false. The sink already holds ONE object for 2026-09-23
(`market-20260924T010000Z-plantedplant.parquet`, one row, `as_of_source` "historical").
  - (a) status OK; the stub records exactly 4 historical requests (round 20: the held 2026-09-23 splits the range into the runs
    2026-09-21..09-22 and 2026-09-24..09-28), of 50 and 10 securities in each run and each for `["PX_LAST"]` only; ONE reference
    request, for `["CRNCY"]` and the 60 securities (none holds a stored currency); nothing reaches the shared client;
  - (b) each of 2026-09-21, -22, -24, -25, -28 holds exactly ONE `market-*.parquet` of 60 rows, every row `as_of_source` ==
    "backfill", `date` == its partition and `px_close` set; the weekend 26 / 27 holds none;
  - (c) the skip: 2026-09-23 still holds exactly the planted object, byte for byte, and the result counts 1 skipped date;
  - (d) the ledger holds `market-range` lines whose rows sum to the points asked: 300 historical (the held date is not asked)
    plus 60 for the currency request;
  - (e) control: the existing mode `plan-market` over the same 60 securities returns OK with 2 batches and no vendor call.
FAIL at base: (a), (b), (c), (d) FAIL (the mode is refused as a bad event: no request, no object, no count, no ledger line);
(e) PASSES."""
import datetime as dt
import io
import json
import os
import pathlib
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

SECS = [f"S{i:03d} US Equity" for i in range(60)]
START, END = "2026-09-21", "2026-09-28"
RUN_DATE = dt.date(2026, 10, 6)
PLAN = 360
SKIP = "2026-09-23"   # the date the sink already holds a market object for


class Vendor:
    """The recording stub of the vendor seam: every call is recorded; a historical call answers each requested field for each
    trading day inside its own [start, end]."""

    def __init__(self, days):
        self.days, self.hist, self.ref, self.leaked = days, [], [], []

    @staticmethod
    def _iso(x):
        s = str(x)[:10]
        return s if "-" in s else f"{s[:4]}-{s[4:6]}-{s[6:8]}"

    def historical(self, securities, fields, start=None, end=None, *a, **k):
        lo, hi = self._iso(start), self._iso(end)
        self.hist.append((list(securities), list(fields), lo, hi))
        return {s: {d: {f: 100.0 + i + int(d[-2:]) / 100 for f in fields} for d in self.days if lo <= d <= hi}
                for i, s in enumerate(securities)}

    def reference(self, securities, fields, *a, **k):
        self.ref.append((list(securities), list(fields)))
        return {}

    @property
    def calls(self):
        return len(self.hist) + len(self.ref) + len(self.leaked)


def bind(eb, days):
    """Bind the recording stub at the tests' seam and make the shared client itself unreachable."""
    vd = Vendor(days)
    eb._blp_historical_data = vd.historical
    eb._blp_reference_data = vd.reference
    eb._run_date_et = lambda: RUN_DATE

    def _leak(*a, **k):
        vd.leaked.append(a)
        raise PermissionError("offline check: blp_client is refused (no Bloomberg call)")

    fake = types.ModuleType("integrations.bloomberg.mcp")
    fake.blp_client = types.SimpleNamespace(reference_data=_leak, historical_data=_leak)
    sys.modules["integrations.bloomberg.mcp"] = fake
    return vd


def find(obj, pred, path=""):
    """Every (path, value) in a nested result whose KEY satisfies pred."""
    out = []
    if isinstance(obj, dict):
        for k, val in obj.items():
            if pred(str(k)):
                out.append((f"{path}{k}", val))
            out += find(val, pred, f"{path}{k}.")
    elif isinstance(obj, (list, tuple)):
        for i, val in enumerate(obj):
            out += find(val, pred, f"{path}{i}.")
    return out


def market_objects(s, homes):
    """{date: [object uris]} of gold/security_market over every calendar day of the range."""
    out, d = {}, dt.date.fromisoformat(START)
    while d <= dt.date.fromisoformat(END):
        us = [u for u in s.list(homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d.isoformat()}") + "/")
              if u.endswith(".parquet")]
        if us:
            out[d.isoformat()] = us
        d += dt.timedelta(days=1)
    return out


def ledger_lines(bb):
    f = bb._ledger_file(bb._utc_today())
    return [json.loads(ln) for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()] if f.is_file() else []


def landed_fact(s, pq, uris, day):
    """(words, ok) for one landed date: exactly one market-*.parquet, 60 rows, all `backfill`, all of this date, all priced."""
    names = [u.rsplit("/", 1)[-1] for u in uris]
    if len(uris) != 1 or not names[0].startswith("market-"):
        return f"{len(uris)} objects {names}", False
    df = pq.read_table(io.BytesIO(s.get(uris[0]))).to_pandas()
    srcs, parts = sorted(set(df["as_of_source"].astype(str))), sorted({str(x)[:10] for x in df["date"]})
    priced = int(df["px_close"].notna().sum())
    ok = (len(df) == len(SECS) and srcs == ["backfill"] and parts == [day] and priced == len(SECS)
          and sorted(df["security_bloomberg"]) == sorted(SECS))
    return f"{len(df)} rows, as_of_source {srcs}, date {parts}, px_close set {priced}", ok


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from lib import trading_calendar as tc
    from rivalfunds import bbg_budget as bb
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes, sinks

    days = [d.isoformat() for d in tc.trading_days_between(START, END)]
    fixture_ok = len(SECS) * len(days) == PLAN and SKIP in days
    os.environ[bb.ENV_DIR] = str(c.tmpdir("rv_bf1_fit_ledger_"))
    spec = f"local:{c.tmpdir('rv_bf1_fit_sink_')}"
    s = sinks.get_sink(spec)
    prov = {"revision": "20260924T010000Z-plantedplant", "produced_at": "2026-09-24T01:00:00Z", "producer_version": "planted",
            "input_manifest": "{}"}
    planted_uri = eb.market_target_uri(SKIP, prov["revision"])
    planted = eb._parquet_bytes(eb._market_table(eb.market_rows({"S000 US Equity": {"PX_LAST": 1.0}}, SKIP, "planted", prov,
                                                                "historical")))
    s.put(planted_uri, planted, "application/octet-stream")
    print(f"fixture: {len(SECS)} securities x {len(days)} trading days {days} = {len(SECS) * len(days)} points | planted "
          f"date={SKIP}/{planted_uri.rsplit('/', 1)[-1]} ({len(planted)} bytes)")

    vd = bind(eb, days)
    try:
        res = eb.handler_entry({"mode": "market-range", "start": START, "end": END, "securities": list(SECS), "batch_id": "bf1-fit",
                                "sink": spec, "max_points": 1000, "dry_run": False})
    except Exception as e:  # noqa: BLE001 -- a raising mode is a failed arm, not a dead check
        res = {"status": f"RAISED {type(e).__name__}", "detail": str(e)}
    print(f"result: status {res.get('status')} | detail {str(res.get('detail'))[:300]}")

    shapes = sorted(((len(secs), fields, lo, hi) for secs, fields, lo, hi in vd.hist), reverse=True)
    asked = sorted(x for secs, _f, _lo, _hi in vd.hist for x in secs)
    runs = (("2026-09-24", "2026-09-28"), ("2026-09-21", "2026-09-22"))   # the un-held runs, newest first (the shapes sort reverse)
    want = [(n, ["PX_LAST"], lo, hi) for n in (50, 10) for lo, hi in runs]
    print(f"historical requests: {len(vd.hist)} {shapes} | reference requests: {len(vd.ref)} {[(len(x), f) for x, f in vd.ref]} | "
          f"reached blp_client: {len(vd.leaked)}")
    v.check(fixture_ok and res.get("status") == "OK" and shapes == want and asked == sorted(SECS * 2)
            and [(sorted(x), f) for x, f in vd.ref] == [(sorted(SECS), ["CRNCY"])] and not vd.leaked,
            "(a) ONE historical request per batch of 50 securities per run of un-held days, PX_LAST only, and ONE CRNCY reference request")

    objs = market_objects(s, homes)
    good = []
    for d in (x for x in days if x != SKIP):
        words, ok = landed_fact(s, pq, objs.get(d, []), d)
        good.append(ok)
        print(f"  date={d}: {words}")
    stray = sorted(d for d in objs if d not in days)
    print(f"partitions holding an object: {sorted(objs)} | outside the trading days: {stray}")
    v.check(fixture_ok and len(good) == 5 and all(good) and not stray,
            "(b) one market-*.parquet per landed date, 60 rows each, every row as_of_source 'backfill'; none on the weekend")

    at_skip = objs.get(SKIP, [])
    same = at_skip == [planted_uri] and s.get(planted_uri) == planted
    skipped = find(res, lambda k: "skip" in k.lower())
    counted = any(val == 1 or (isinstance(val, (list, tuple, dict)) and len(val) == 1) for _, val in skipped)
    print(f"date={SKIP}: objects {[u.rsplit('/', 1)[-1] for u in at_skip]} | planted bytes unchanged: {same} | skip keys in the "
          f"result: {skipped}")
    v.check(res.get("status") == "OK" and same and counted,
            "(c) a date already holding a market-*.parquet is skipped (the object untouched) and counted (1)")

    lines = [ln for ln in ledger_lines(bb) if ln.get("mode") == "market-range"]
    total = sum(int(ln.get("rows", 0)) for ln in lines)
    print(f"ledger market-range lines: {lines} | rows {total} | spent(today) {bb.spent()}")
    v.check(bool(lines) and total == (PLAN - len(SECS)) + len(SECS) and bb.spent() == total,
            "(d) the points are recorded in the bbg_budget ledger with mode 'market-range'")

    vd2 = bind(eb, days)
    p = eb.handler_entry({"mode": "plan-market", "date": END, "sink": f"local:{c.tmpdir('rv_bf1_ctl_sink_')}",
                          "securities": list(SECS)})
    print(f"plan-market: status {p['status']} | securities {len(p.get('securities') or [])} | batches "
          f"{[len(x) for x in p.get('batches') or []]} | vendor calls {vd2.calls}")
    v.check(p["status"] == "OK" and p.get("securities") == sorted(SECS) and [len(x) for x in p.get("batches") or []] == [50, 10]
            and vd2.calls == 0, "(e) control: plan-market still plans the 60 securities in 2 batches with no vendor call")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
