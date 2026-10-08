"""RIV-tw-1 AC2 (FWD-24; C-OWED-GRAIN, C-OWED-IN-THE-LEG, C-OWED-BUDGET; CTO ruling R13; PRD v0.19): with the switch
`RIVALFUNDS_HISTORY_OWED` set to "print" the daily run prints ONE line and sends and writes nothing more; set to "ask" it asks
the owed closes inside the budget (`bbg_budget.check_points` BEFORE any history request, every request recorded as
"history-owed"), lands each date's top-up as ONE NEW object in that date's partition (named with a capture time, beside the object
already there, which stays byte-identical), every row carrying `price_date`, `as_of_source` "backfill"; a close whose own date is
not the partition's is not written and is counted; a name that already exists is never overwritten.

NO Bloomberg call and none of RIV-ho-1's code: `rivalfunds.history_owed` is a STUB module planted in `sys.modules` (its `owed(s,
day)` returns a fixed frame, its `summary(df)` is the PRD's dict) so this check does not depend on RIV-ho-1's build. The vendor seam
is the one `tests/test_r12eb1_session_attempts.py` stubs (`enrichment_bloomberg._blp_historical_data` / `_blp_reference_data`),
bound to a RECORDING stub that answers every requested field for every trading day of the request; `integrations.bloomberg.mcp` is
replaced by a module that records and raises; `boto3` and `requests.post` are refused; `_run_date_et` is pinned to 2026-10-06 and the
module's clock to 2026-10-06T11:00:05Z; the budget ledger is a fresh temp dir per arm (`RIVALFUNDS_BBG_BUDGET_DIR`); every sink is a
recording wrapper of a `local:` sink. `bbg_budget.check_points` and `bbg_budget.record` are wrapped to log, in one ordered log with
the client's requests and the sink's puts, and (arm d only) `check_points` is made to refuse.
Fixture: daily run for report date 2026-10-05 over four securities (`S1`..`S4 US Equity`). The stub owed frame holds 12 units: those
four securities on 2026-10-02, 2026-10-01 and 2026-09-30, sorted date descending then security_id. Each of those three partitions
already holds ONE object (`market-20260924T010000Z-plantedplant.parquet`, one row of `ZZZ US Equity`).
The free choices of the build are NOT graded: how the history request is batched (one request per date, per batch, per range), the
exact revision string, extra fields in the printed line (only the four named fields appear, in that order; `misdated <n>` may sit
anywhere), the shape of the `history_owed` result value, whether `landed` counts rows or objects.
  - (a) "print": the stdout holds exactly `HISTORY OWED: owed 12 units, 4 securities, 3 dates; asked 0 (request off); carried 12`;
    the client requests and the sink PUTS equal the same run with the switch off; `check_points` and `record` are never called;
    the result dict has a `history_owed` key;
  - (b) "ask" under the cap: `check_points(12)` is called BEFORE the first history request; the line reads `HISTORY OWED: owed 12;
    asked 12; landed <l>; carried 0`; each of the three partitions holds the planted object, byte for byte, plus ONE new
    `market-*.parquet` whose name carries a capture time (`revision.capture_time` not None), its 4 rows `price_date` == the
    partition date, `date` == the partition, `as_of_source` "backfill", `source` == `MARKET_SOURCE_HIST`, `px_close` the stub's
    close; the daily date's partition is what the switch-off run leaves; one `record("history-owed", n, batch_id)` per history
    request, whose rows add up to the points of the requests sent;
  - (c) the cap: `HISTORY_OWED_CAP` monkeypatched to 5: `check_points(5)`; `asked 5`, `carried 7`; the new rows are exactly the first
    5 units of the frame (the four on 2026-10-02 and S1 on 2026-10-01); 2026-09-30 holds only its planted object and no request
    window reaches it;
  - (d) `check_points` refuses: it was called with 12; no history request, no `record`, no new object; the refusal text is printed
    and a `HISTORY OWED:` line says `carried 12`;
  - (e) the vendor answers S3's 2026-09-30 close under the key 2026-09-29: that close is written nowhere (no object at 2026-09-29,
    S3 absent from 2026-09-30's new object), the line carries `misdated 1`, `asked 12`, and every other unit lands;
  - (f) never overwrite: the names the top-ups took in one run are pre-planted with other bytes in a fresh sink and the run is
    repeated: those bytes, the planted objects and the daily object are unchanged, no put lands on an existing key, the run does not
    raise;
  - (g) control: with the switch unset the daily run lands its one market object at 2026-10-05, the recording client was reached,
    the stub owed module is importable and was not called, and the three partitions hold only their planted object.
FAIL at base 361b735308: (a) no `HISTORY OWED:` line and no `history_owed` key (the switch is read nowhere); (b) no line, no
`check_points`, no new object; (c) the same (and the monkeypatched cap is read by no code); (d) no line, `check_points` never
called; (e) no line, nothing counted; (f) nothing landed in the first run, so there is no top-up name to collide with; (g) PASSES."""
import contextlib
import datetime as dt
import hashlib
import importlib
import io
import os
import pathlib
import re
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

ENV = "RIVALFUNDS_HISTORY_OWED"
DAY = "2026-10-05"
RUN_DATE = dt.date(2026, 10, 6)
FIXED = dt.datetime(2026, 10, 6, 11, 0, 5, tzinfo=dt.timezone.utc)
SECS = [f"S{i} US Equity" for i in range(1, 5)]
OWED_DATES = ["2026-10-02", "2026-10-01", "2026-09-30"]          # newest first, as the frame is sorted
MIS = "2026-09-29"                                               # the date a misdated close is keyed under (not an owed date)
PLANTED_REV = "20260924T010000Z-plantedplant"
LINE_A = "HISTORY OWED: owed 12 units, 4 securities, 3 dates; asked 0 (request off); carried 12"
REFUSAL = "stub refusal: 12 points > 3 points remaining of the 120000-point backfill budget"
LOG: list = []                                                   # one ordered log: owed / check_points / record / hist / ref / put


def sid(sec):
    return sec.replace(" ", "_")


def close_of(sec, day):
    """The stub vendor's close for one security on one day (a function of the pair, not of the request's shape)."""
    return 100.0 + 10 * int(sec[1]) + int(day[-2:]) / 100


def owed_rows():
    return [{"security_id": sid(s), "security_bloomberg": s, "date": d, "funds": "AAA,BBB"} for d in OWED_DATES for s in SECS]


class OwedStub(types.ModuleType):
    """The stand-in for RIV-ho-1's module: `owed(s, day, window_days=365)` and `summary(df)` as the cell names them."""

    def __init__(self):
        super().__init__("rivalfunds.history_owed")
        self.calls = []

    def owed(self, s, day, window_days=365, *a, **k):
        import pandas as pd
        self.calls.append(str(day))
        LOG.append(("owed", str(day)))
        return pd.DataFrame(owed_rows(), columns=["security_id", "security_bloomberg", "date", "funds"])

    def summary(self, df):
        if df is None or len(df) == 0:
            return {"securities": 0, "units": 0, "dates": 0, "newest": None, "oldest": None}
        return {"securities": int(df["security_id"].nunique()), "units": int(len(df)), "dates": int(df["date"].nunique()),
                "newest": max(df["date"]), "oldest": min(df["date"])}


class Client:
    """The recording stub of the vendor seam. `misdate` {(security, day): key} answers that close under another date key."""

    def __init__(self, days, misdate=None):
        self.days, self.hist, self.ref, self.misdate = days, [], [], misdate or {}

    @staticmethod
    def _iso(x):
        s = str(x)[:10]
        return s if "-" in s else f"{s[:4]}-{s[4:6]}-{s[6:8]}"

    def historical(self, securities, fields, start=None, end=None, *a, **k):
        lo, hi = self._iso(start), self._iso(end)
        self.hist.append((list(securities), list(fields), lo, hi))
        LOG.append(("hist", list(securities), list(fields), lo, hi))
        out = {}
        for sec in securities:
            rows = {}
            for d in self.days:
                if lo <= d <= hi:
                    rows[self.misdate.get((sec, d), d)] = {f: close_of(sec, d) for f in fields}
            out[sec] = rows
        return out

    def reference(self, securities, fields, overrides=None, timeout_s=90.0, *a, **k):
        self.ref.append((list(securities), list(fields)))
        LOG.append(("ref", list(securities), list(fields)))
        return {}


class RecSink:
    """A `local:` sink that records every put (uri, digest) in the ordered log; `overwrites` lists a put onto an existing key."""
    kind = "local"

    def __init__(self, root):
        from rivalfunds import sinks
        self.inner, self.overwrites, self.touched = sinks.LocalSink(root), [], []

    def get(self, uri):
        self.touched.append(uri)
        return self.inner.get(uri)

    def exists(self, uri):
        self.touched.append(uri)
        return self.inner.exists(uri)

    def list(self, prefix):
        got = self.inner.list(prefix)
        self.touched.extend(got)
        return got

    def put(self, uri, data, content_type=None):
        LOG.append(("put", uri, hashlib.sha256(data).hexdigest()[:16]))
        if self.inner.exists(uri):
            self.overwrites.append(uri)
        return self.inner.put(uri, data, content_type)


def clock_shim():
    class _Fixed(dt.datetime):
        @classmethod
        def now(cls, tz=None):
            return FIXED.astimezone(tz) if tz else FIXED.replace(tzinfo=None)

    return types.SimpleNamespace(date=dt.date, timedelta=dt.timedelta, timezone=dt.timezone, time=dt.time,
                                 MINYEAR=dt.MINYEAR, MAXYEAR=dt.MAXYEAR, datetime=_Fixed)


def part_prefix(homes, d):
    return homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d}") + "/"


def plant(eb, root):
    """The one planted object in each owed partition; returns {date: (uri, bytes)}."""
    from rivalfunds import sinks
    s = sinks.LocalSink(root)
    out = {}
    for d in OWED_DATES:
        prov = {"revision": PLANTED_REV, "produced_at": "2026-09-24T01:00:00Z", "producer_version": "planted", "input_manifest": "{}"}
        uri = eb.market_target_uri(d, PLANTED_REV)
        raw = eb._parquet_bytes(eb._market_table(eb.market_rows({"ZZZ US Equity": {"PX_LAST": 1.0}}, d, "planted", prov, "historical")))
        s.put(uri, raw, "application/octet-stream")
        out[d] = (uri, raw)
    return out


def partitions(root, homes, dates):
    """{date: {uri: bytes}} of every `market-*.parquet` in the partitions."""
    from rivalfunds import sinks
    s = sinks.LocalSink(root)
    return {d: {u: s.get(u) for u in s.list(part_prefix(homes, d)) if u.endswith(".parquet")
                and u.rsplit("/", 1)[-1].startswith("market-")} for d in dates}


def is_owed_request(eb, ev):
    """A history request of the leg: any historical request other than the daily pull's own (all historical fields, report date)."""
    _k, _secs, fields, lo, hi = ev
    return not (lo == hi == DAY and fields == list(eb.MARKET_HIST_FIELDS))


def points_of(days, ev):
    _k, secs, _f, lo, hi = ev
    return len(secs) * sum(1 for d in days if lo <= d <= hi)


def arm(eb, bb, homes, days, name, env_value, cap=None, refusal=None, misdate=None, preload=None):
    """One isolated daily run on a fresh sink holding the planted objects (and `preload` {uri: bytes}, put on top). Returns the facts."""
    from rivalfunds import sinks
    root = c.tmpdir(f"rv_tw2_{name}_")
    planted = plant(eb, root)
    for uri, raw in (preload or {}).items():
        sinks.LocalSink(root).put(uri, raw, "application/octet-stream")
    LOG.clear()
    sink, client, stub = RecSink(root), Client(days, misdate), sys.modules["rivalfunds.history_owed"]
    stub.calls.clear()
    keep = {k: getattr(eb, k) for k in ("dt", "_blp_historical_data", "_blp_reference_data", "_run_date_et")}
    had_cap, old_cap = hasattr(eb, "HISTORY_OWED_CAP"), getattr(eb, "HISTORY_OWED_CAP", None)
    real_check, real_record = bb.check_points, bb.record

    def check_points(points, today=None):
        LOG.append(("check_points", int(points)))
        return refusal if refusal is not None else real_check(points, today)

    def record(mode, rows, batch_id):
        LOG.append(("record", mode, int(rows), batch_id))
        return real_record(mode, rows, batch_id)

    eb.dt, eb._blp_historical_data, eb._blp_reference_data = clock_shim(), client.historical, client.reference
    eb._run_date_et = lambda: RUN_DATE
    bb.check_points, bb.record = check_points, record
    if cap is not None:
        eb.HISTORY_OWED_CAP = cap
    prev = os.environ.pop(ENV, None)
    if env_value is not None:
        os.environ[ENV] = env_value
    os.environ[bb.ENV_DIR] = c.tmpdir(f"rv_tw2_{name}_ledger_")
    buf, raised = io.StringIO(), None
    try:
        with contextlib.redirect_stdout(buf):
            res = eb.handler_entry({"mode": "daily", "date": DAY, "batch_id": "chk-daily", "securities": list(SECS), "sink": sink})
    except Exception as e:  # noqa: BLE001 -- a raising run is a failed arm, not a dead check
        res, raised = {"status": f"RAISED {type(e).__name__}", "detail": str(e)}, f"{type(e).__name__}: {e}"
    finally:
        eb.dt, eb._blp_historical_data, eb._blp_reference_data, eb._run_date_et = (keep[k] for k in (
            "dt", "_blp_historical_data", "_blp_reference_data", "_run_date_et"))
        bb.check_points, bb.record = real_check, real_record
        if cap is not None:
            if had_cap:
                eb.HISTORY_OWED_CAP = old_cap
            else:
                del eb.HISTORY_OWED_CAP
        os.environ.pop(ENV, None)
        if prev is not None:
            os.environ[ENV] = prev
    lines = [ln.strip() for ln in buf.getvalue().splitlines() if ln.strip()]
    return {"root": root, "res": res, "raised": raised, "stdout": buf.getvalue(), "lines": lines,
            "hline": [ln for ln in lines if ln.startswith("HISTORY OWED:")], "log": list(LOG), "client": client, "sink": sink,
            "planted": planted, "owed_calls": list(stub.calls),
            "parts": partitions(root, homes, OWED_DATES + [MIS, DAY]), "puts": [e for e in LOG if e[0] == "put"]}


def fields_in_order(line):
    """{field: (value, position)} for the four named fields; ok only if they appear in the order owed, asked, landed, carried."""
    found = {}
    for k in ("owed", "asked", "landed", "carried"):
        m = re.search(rf"\b{k} (\d+)", line)
        if m:
            found[k] = (int(m.group(1)), m.start())
    ordered = len(found) == 4 and [found[k][1] for k in ("owed", "asked", "landed", "carried")] == sorted(
        found[k][1] for k in ("owed", "asked", "landed", "carried"))
    return found, ordered


def misdated_in(line):
    m = re.search(r"\bmisdated (\d+)", line)
    return int(m.group(1)) if m else 0


def new_objects(r, date):
    """The objects in the partition that are not the planted one: {uri: DataFrame}."""
    import pyarrow.parquet as pq
    planted_uri = r["planted"].get(date, (None,))[0]
    return {u: pq.read_table(io.BytesIO(raw)).to_pandas() for u, raw in r["parts"][date].items() if u != planted_uri}


def landed_units(r, dates=OWED_DATES):
    """{(security_bloomberg, date)} of every row in every new object, with a note per object: (units, problems)."""
    from rivalfunds import revision
    units, problems, names = set(), [], 0
    for d in dates:
        news = new_objects(r, d)
        if len(news) > 1:
            problems.append(f"{d}: {len(news)} new objects")
        for u, df in news.items():
            names += 1
            if revision.capture_time(u.rsplit("/", 1)[-1]) is None:
                problems.append(f"{d}: name {u.rsplit('/', 1)[-1]} carries no capture time")
            if not u.rsplit("/", 1)[-1].startswith("market-"):
                problems.append(f"{d}: name {u.rsplit('/', 1)[-1]} is not market-*")
            if "price_date" not in df.columns:
                problems.append(f"{d}: no price_date column")
                continue
            for row in df.to_dict("records"):
                sec = row["security_bloomberg"]
                units.add((sec, d))
                pd_ = None if row["price_date"] is None else str(row["price_date"])[:10]
                if pd_ != d:
                    problems.append(f"{d}: {sec} price_date {pd_}")
                if str(row["date"])[:10] != d:
                    problems.append(f"{d}: {sec} date {row['date']}")
                if row["as_of_source"] != "backfill":
                    problems.append(f"{d}: {sec} as_of_source {row['as_of_source']!r}")
                if row["px_close"] is None or abs(float(row["px_close"]) - close_of(sec, d)) > 1e-9:
                    problems.append(f"{d}: {sec} px_close {row['px_close']} != stub {close_of(sec, d)}")
            if len(df) != len(set(df["security_bloomberg"])):
                problems.append(f"{d}: duplicate securities in one object")
    return units, problems, names


def planted_intact(r):
    return all(r["parts"][d].get(r["planted"][d][0]) == r["planted"][d][1] for d in OWED_DATES)


def run(v):
    c.setup_path()
    c.offline_guards()
    fake = types.ModuleType("integrations.bloomberg.mcp")

    def _leak(*a, **k):
        raise PermissionError("offline check: blp_client is refused (no Bloomberg call)")

    fake.blp_client = types.SimpleNamespace(reference_data=_leak, historical_data=_leak)
    sys.modules["integrations.bloomberg.mcp"] = fake
    stub = OwedStub()
    sys.modules["rivalfunds.history_owed"] = stub

    from lib import trading_calendar as tc
    from rivalfunds import bbg_budget as bb
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes

    import rivalfunds
    rivalfunds.history_owed = stub
    days = [d.isoformat() for d in tc.trading_days_between("2026-09-01", "2026-10-06")]
    all_units = {(s, d) for d in OWED_DATES for s in SECS}
    first5 = {(s, "2026-10-02") for s in SECS} | {("S1 US Equity", "2026-10-01")}
    print(f"fixture: report date {DAY}, run date {RUN_DATE}; stub owed frame {len(all_units)} units over {OWED_DATES}; each owed "
          f"partition already holds {PLANTED_REV}")

    off = arm(eb, bb, homes, days, "off", None)
    print(f"switch off: status {off['res'].get('status')} | HISTORY OWED lines {off['hline']} | puts {len(off['puts'])} | history requests "
          f"{len(off['client'].hist)}, reference {len(off['client'].ref)} | owed() calls {off['owed_calls']}")

    # ---- (a) print --------------------------------------------------------------------------------------------------
    a = arm(eb, bb, homes, days, "print", "print")
    same_req = a["client"].hist == off["client"].hist and a["client"].ref == off["client"].ref
    same_puts = a["puts"] == off["puts"]
    budget_calls = [e for e in a["log"] if e[0] in ("check_points", "record")]
    print(f"print: lines {a['hline']} | requests equal the switch-off run: {same_req} | puts equal: {same_puts} ({len(a['puts'])} vs "
          f"{len(off['puts'])}) | check_points/record calls: {budget_calls} | owed() calls {a['owed_calls']} | history_owed key: "
          f"{'history_owed' in a['res']}")
    v.check(a["hline"] == [LINE_A] and same_req and same_puts and not budget_calls and "history_owed" in a["res"]
            and not a["raised"], "(a) 'print': exactly one HISTORY OWED line, no extra request or put, no budget call, history_owed key")

    # ---- (b) ask under the cap --------------------------------------------------------------------------------------
    b = arm(eb, bb, homes, days, "ask", "ask")
    reqs = [e for e in b["log"] if e[0] == "hist" and is_owed_request(eb, e)]
    cp = [i for i, e in enumerate(b["log"]) if e[0] == "check_points"]
    first_req = next((i for i, e in enumerate(b["log"]) if e[0] == "hist" and is_owed_request(eb, e)), None)
    recs = [e for e in b["log"] if e[0] == "record" and e[1] == "history-owed"]
    units_b, problems_b, nobj_b = landed_units(b)
    f_b, ordered_b = fields_in_order(b["hline"][0]) if len(b["hline"]) == 1 else ({}, False)
    land_ok = f_b.get("landed", (None,))[0] in (len(units_b), nobj_b) if f_b else False
    daily_same = {u for u in b["parts"][DAY]} == {u for u in off["parts"][DAY]}
    extra_puts = [e[1] for e in b["puts"] if e not in off["puts"]]
    stray = [u for u in extra_puts if "security_market" in u and not any(f"date={d}/" in u for d in OWED_DATES)]
    print(f"ask: lines {b['hline']} | check_points calls {[e[1] for e in b['log'] if e[0] == 'check_points']} at log positions {cp}, "
          f"first history request at {first_req} | history requests {len(reqs)} ({[(len(e[1]), e[3], e[4]) for e in reqs]}) | "
          f"records {[e[2:] for e in recs]} vs request points {[points_of(days, e) for e in reqs]}")
    print(f"  landed units {len(units_b)} of 12 in {nobj_b} new objects | problems {problems_b} | planted intact: {planted_intact(b)} | "
          f"daily partition as the switch-off run leaves it: {daily_same} | puts beyond the switch-off run: {len(extra_puts)} "
          f"| stray puts {stray} | raised {b['raised']}")
    v.check(len(b["hline"]) == 1 and ordered_b and (f_b.get("owed", (0,))[0], f_b.get("asked", (0,))[0], f_b.get("carried", (9,))[0])
            == (12, 12, 0) and land_ok and misdated_in(b["hline"][0]) == 0 and cp and [e[1] for e in b["log"] if e[0] == "check_points"] == [12]
            and reqs and first_req is not None and cp[0] < first_req and len(recs) == len(reqs)
            and sum(e[2] for e in recs) == sum(points_of(days, e) for e in reqs) and all(e[3] for e in recs)
            and units_b == all_units and not problems_b and nobj_b == 3 and planted_intact(b) and daily_same and len(extra_puts) == 3
            and not stray and not b["parts"][MIS] and not b["raised"],
            "(b) 'ask': check_points(12) before any history request, one history-owed record per request, ONE new object per date "
            "with price_date/backfill rows, base objects untouched, line owed 12; asked 12; landed; carried 0")

    # ---- (c) the cap ------------------------------------------------------------------------------------------------
    cc = arm(eb, bb, homes, days, "cap", "ask", cap=5)
    reqs_c = [e for e in cc["log"] if e[0] == "hist" and is_owed_request(eb, e)]
    cps_c = [e[1] for e in cc["log"] if e[0] == "check_points"]
    units_c, problems_c, nobj_c = landed_units(cc)
    f_c, ordered_c = fields_in_order(cc["hline"][0]) if len(cc["hline"]) == 1 else ({}, False)
    reach = [e for e in reqs_c if e[3] <= "2026-09-30" <= e[4]]
    new_930 = new_objects(cc, "2026-09-30")
    print(f"cap 5: lines {cc['hline']} | check_points calls {cps_c} | history requests {[(len(e[1]), e[3], e[4]) for e in reqs_c]} | "
          f"landed units {sorted(units_c)} | problems {problems_c} | requests reaching 2026-09-30: {len(reach)} | new objects at "
          f"2026-09-30: {len(new_930)} | planted intact: {planted_intact(cc)}")
    v.check(len(cc["hline"]) == 1 and ordered_c and (f_c.get("owed", (0,))[0], f_c.get("asked", (0,))[0], f_c.get("carried", (0,))[0])
            == (12, 5, 7) and cps_c == [5] and reqs_c and units_c == first5 and not problems_c and not reach and not new_930
            and planted_intact(cc) and not cc["raised"],
            "(c) cap 5: check_points(5), asked 5, carried 7; exactly the first 5 units of the frame land; 2026-09-30 untouched")

    # ---- (d) a refusal from check_points ----------------------------------------------------------------------------
    d = arm(eb, bb, homes, days, "refused", "ask", refusal=REFUSAL)
    reqs_d = [e for e in d["log"] if e[0] == "hist" and is_owed_request(eb, e)]
    cps_d = [e[1] for e in d["log"] if e[0] == "check_points"]
    recs_d = [e for e in d["log"] if e[0] == "record"]
    units_d, problems_d, nobj_d = landed_units(d)
    carried12 = any("carried 12" in ln for ln in d["hline"])
    print(f"refused: lines {d['hline']} | other stdout {[ln for ln in d['lines'] if not ln.startswith('HISTORY OWED:')]} | check_points "
          f"calls {cps_d} | history requests {len(reqs_d)} | records {recs_d} | new objects {nobj_d} | refusal text printed: "
          f"{REFUSAL in d['stdout']} | carried 12 on a HISTORY OWED line: {carried12}")
    v.check(cps_d == [12] and not reqs_d and not recs_d and nobj_d == 0 and not units_d and REFUSAL in d["stdout"] and carried12
            and planted_intact(d) and not d["raised"],
            "(d) a check_points refusal: asked with 12, nothing requested, recorded or landed; refusal printed with carried 12")

    # ---- (e) a misdated close ---------------------------------------------------------------------------------------
    e = arm(eb, bb, homes, days, "misdated", "ask", misdate={("S3 US Equity", "2026-09-30"): "2026-09-29"})
    units_e, problems_e, nobj_e = landed_units(e, OWED_DATES + [MIS])
    f_e, ordered_e = fields_in_order(e["hline"][0]) if len(e["hline"]) == 1 else ({}, False)
    mis = misdated_in(e["hline"][0]) if len(e["hline"]) == 1 else None
    stray_929 = e["parts"][MIS]
    print(f"misdated: lines {e['hline']} | misdated {mis} | landed units {len(units_e)} of 12 (S3 on 2026-09-30 landed: "
          f"{('S3 US Equity', '2026-09-30') in units_e}) | objects at 2026-09-29: {list(stray_929)} | problems {problems_e}")
    v.check(len(e["hline"]) == 1 and ordered_e and mis == 1 and f_e.get("asked", (0,))[0] == 12 and units_e == all_units - {("S3 US Equity", "2026-09-30")}
            and not stray_929 and not problems_e and planted_intact(e) and not e["raised"],
            "(e) a returned close dated other than its partition is not written, is counted 'misdated 1', and every other unit lands")

    # ---- (f) never overwrite ----------------------------------------------------------------------------------------
    names = [u for dd in OWED_DATES for u in new_objects(b, dd)]
    sentinel = {u: b"SENTINEL-NOT-A-PARQUET-" + hashlib.sha256(u.encode()).digest() for u in names}
    f = arm(eb, bb, homes, days, "collide", "ask", preload=sentinel)
    after = {u: f["parts"][next(dd for dd in OWED_DATES if f"date={dd}/" in u)].get(u) for u in sentinel}
    touched = sorted({u for u in f["sink"].touched if u in sentinel})
    if not names:
        print("never overwrite: the ask run landed NO top-up object, so there is no name to collide with (the collision is not exercised)")
    print(f"never overwrite: top-up names learned from the ask run {[u.rsplit('/', 1)[-1] for u in names]} | pre-planted with other bytes "
          f"| sentinel bytes unchanged: {all(after[u] == sentinel[u] for u in sentinel)} | puts onto an existing key: "
          f"{f['sink'].overwrites} | sentinel names the run looked at: {len(touched)} | daily object unchanged: "
          f"{set(f['parts'][DAY]) == set(off['parts'][DAY])} | raised {f['raised']} | line {f['hline']}")
    v.check(len(names) == 3 and all(after[u] == sentinel[u] for u in sentinel) and not f["sink"].overwrites
            and planted_intact(f) and set(f["parts"][DAY]) == set(off["parts"][DAY]) and not f["raised"],
            "(f) a name that already exists is never overwritten, a planted object and the daily object stay as they were")

    # ---- (g) control ------------------------------------------------------------------------------------------------
    importable = importlib.import_module("rivalfunds.history_owed") is stub
    print(f"control: switch-off status {off['res'].get('status')} | market objects at {DAY}: {[u.rsplit('/', 1)[-1] for u in off['parts'][DAY]]} "
          f"| client requests {len(off['client'].hist) + len(off['client'].ref)} | stub owed module importable: {importable}, "
          f"owed() calls {off['owed_calls']} | owed partitions hold only the planted object: "
          f"{all(set(off['parts'][dd]) == {off['planted'][dd][0]} for dd in OWED_DATES)}")
    v.check(len(off["parts"][DAY]) == 1 and len(off["client"].hist) + len(off["client"].ref) > 0 and importable
            and not off["owed_calls"] and not off["hline"] and all(set(off["parts"][dd]) == {off["planted"][dd][0]} for dd in OWED_DATES),
            "(g) control: the switch-off daily run lands its one market object, reaches the client, calls no owed stub and leaves the "
            "owed partitions as planted")


def main():
    v = c.Verdict("AC2")
    try:
        run(v)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 -- an import error at base is the expected FAIL of a build check
        import traceback
        traceback.print_exc()
        v.check(False, f"exception: {type(e).__name__}: {e}")
    labels = ", ".join(m.split(" ")[0] if m.startswith("(") else "exception" for m in v.fails)
    print("AC2 RESULT: PASS 0 failures" if not v.fails else f"AC2 RESULT: FAIL {len(v.fails)}: {labels}")
    return 0 if not v.fails else 1


if __name__ == "__main__":
    sys.exit(main())
