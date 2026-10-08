"""RIV-tc-1 AC1 (CTO half C2 of round 27; ROUND_ANALYSIS.round22 ADDENDUM 6 item 2; CTO ruling R13): a top-up close is stored with
a currency, and the owed window ends on the page day. Grades the cell's items 1 to 5 on `enrichment_bloomberg._history_owed`, the
leg the daily run reaches only when `RIVALFUNDS_HISTORY_OWED` is "print" or "ask".

Interface read (from the cell):
  1. the leg calls `history_owed.owed(s, page_day)`, `page_day` the NEXT TRADING DAY after the report date (`lib.trading_calendar`),
     in `print` and in `ask`;
  2. `ask` only: the stored currency (`_stored_currencies`) where one exists; for the asked securities with none, ONE
     `_blp_reference_data` request, the single field `CRNCY`, BEFORE the history requests; `bbg_budget.check_points(units to ask +
     currency lookups)` before any request; the lookup recorded with `bbg_budget.record("history-owed", <securities asked>,
     batch_id)`; a top-up row carries the currency found, NULL only when the lookup returned none for it; a failed currency request
     sends no history request, lands nothing, and the line reads `carried <all>`;
  3. the `ask` line gains `currency lookups <n>`; the `print` line gains `currency lookups <n> (not sent)` (no request);
  4. `price_date` on every top-up row equals its partition date (round 27, unchanged);
  5. switch OFF: `tw-1.AC1.py` still ends `AC1 RESULT: PASS 0 failures`.

NO Bloomberg call, no network, no S3. As `tw-1.AC2.py`: `rivalfunds.history_owed` is a STUB module in `sys.modules` (it records the
`day` it is called with); the vendor seam `enrichment_bloomberg._blp_historical_data` / `_blp_reference_data` is bound to a
RECORDING stub; `integrations.bloomberg.mcp` is replaced by a module that raises; `boto3` and `requests.post` are refused; the
clock and `_run_date_et` are pinned; the budget ledger is a fresh temp dir per run (`RIVALFUNDS_BBG_BUDGET_DIR`);
`bbg_budget.check_points` and `bbg_budget.record` are wrapped to log; every sink is a recording `local:` sink; ONE ordered LOG holds
owed / check_points / record / hist / ref / put. `RIVALFUNDS_HISTORY_OWED` is set only inside a run and restored.
`RIVALFUNDS_CHECK_ROOT` (optional): a directory holding a `rivalfunds/` package to grade instead of the worktree's (a simulated
build); arm (g) then runs `tw-1.AC1.py` against the same package.

Fixture: report date 2026-10-02 (a Friday), run date pinned to 2026-10-07, so the page day (2026-10-05) is neither the report date,
nor the report date plus one calendar day, nor the run date. The daily run is passed one security (`D1 US Equity`). The stub owed
frame holds 13 units over five OTHER securities: `S3`, `S4`, `S5` on 2026-10-01, 2026-09-30 and 2026-09-29; `S1`, `S2` on 2026-09-30
and 2026-09-29. Each owed partition already holds one planted object (`ZZZ US Equity`, as_of_source "historical"); the one at
2026-10-01 (the newest owed date, so it is inside every reading of "the owed window") also holds the STORED currencies: S1 USD,
S2 EUR in the mixed fixture, all five in the all-stored fixture. The stub's `CRNCY` answer: S3 JPY, S4 GBp, S5 not answered.
  - (a) the window's end: in `print` and in `ask` every `history_owed.owed` call carries day 2026-10-05;
  - (b) `ask`, every asked security stored: no `CRNCY` reference request; all 13 units land, each row with its stored currency;
    `check_points` called once with 13; the history-owed records add up to the history points, one per history request;
  - (c) `ask`, S3 S4 S5 not stored: exactly ONE reference request with fields ["CRNCY"] for exactly those three, after the one
    `check_points(16)` and before the first history request; one history-owed record more than history requests, adding up to
    history points + 3; rows carry S1 USD, S2 EUR, S3 JPY, S4 GBp, S5 NULL;
  - (d) `ask`, the `CRNCY` request raises: no history request of the leg, no new object, a `HISTORY OWED:` line with `carried 13`,
    the run does not raise;
  - (e) the lines: the one `ask` line of (c) contains `currency lookups 3`; the one `print` line contains
    `currency lookups 3 (not sent)`, and the `print` run's requests and puts equal the switch-off run's, with no budget call;
  - (f) `price_date` (round 27): in (b) and (c) all 13 units land and every row's `price_date` and `date` equal its partition;
  - (g) switch OFF: `tw-1.AC1.py` run as a subprocess ends `AC1 RESULT: PASS 0 failures`;
  - (h) control: the switch-off run lands its one market object at the report date, reaches the client, calls no owed stub, leaves
    the owed partitions as planted; the planted stored currencies read back; the page day differs from the three decoys.
NOT graded (the cell leaves them open): where in the line the clause sits, the `ask` line's clause when the count is 0, how the
history requests are batched, the first/last dates passed to `_stored_currencies`, whether a FAILED lookup is recorded as spent,
the other fields of the line after a failed lookup, the result dict's keys.
FAIL at base (round 27 as built): (a) owed is called with 2026-10-02; (b) currency NULL; (c) no CRNCY request, check_points 13,
currency NULL; (d) the stub is never reached, 13 units land; (e) no `currency lookups` clause. (f), (g), (h) PASS."""
import contextlib
import datetime as dt
import hashlib
import io
import os
import pathlib
import re
import subprocess
import sys
import types

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

ENV = "RIVALFUNDS_HISTORY_OWED"
ROOT_ENV = "RIVALFUNDS_CHECK_ROOT"
DAY = "2026-10-02"                                               # the report date (a Friday)
RUN_DATE = dt.date(2026, 10, 7)
FIXED = dt.datetime(2026, 10, 7, 11, 0, 5, tzinfo=dt.timezone.utc)
DAILY_SECS = ["D1 US Equity"]
SECS = [f"S{i} US Equity" for i in range(1, 6)]
OWED_DATES = ["2026-10-01", "2026-09-30", "2026-09-29"]          # newest first, as the frame is sorted
STORE_DATE = OWED_DATES[0]                                       # the partition whose planted object carries the stored currencies
LATE = SECS[2:]                                                  # S3 S4 S5: also owed on the newest date
STORED_MIXED = {SECS[0]: "USD", SECS[1]: "EUR"}
STORED_ALL = {SECS[0]: "USD", SECS[1]: "EUR", SECS[2]: "CHF", SECS[3]: "CAD", SECS[4]: "SEK"}
LOOKUP = {SECS[0]: "XXX", SECS[1]: "XXX", SECS[2]: "JPY", SECS[3]: "GBp"}   # S5 is not answered; S1/S2 must never be asked
EXPECT_MIXED = {SECS[0]: "USD", SECS[1]: "EUR", SECS[2]: "JPY", SECS[3]: "GBp", SECS[4]: None}
PLANTED_REV = "20260924T010000Z-plantedplant"
BATCH_ID = "chk-daily"
LOG: list = []                                                   # one ordered log: owed / check_points / record / hist / ref / put
FAILS: list = []


def sid(sec):
    return sec.replace(" ", "_")


def close_of(sec, day):
    """The stub vendor's close for one security on one day (a function of the pair, not of the request's shape)."""
    return 100.0 + 10 * int(sec[1]) + int(day[-2:]) / 100


def owed_units():
    return [(s, d) for d in OWED_DATES for s in SECS if d != STORE_DATE or s in LATE]


class OwedStub(types.ModuleType):
    """The stand-in for RIV-ho-1's module: `owed(s, day, window_days=365)` records `day`; `summary(df)` is the PRD's dict."""

    def __init__(self):
        super().__init__("rivalfunds.history_owed")
        self.calls = []

    def owed(self, s, day, window_days=365, *a, **k):
        import pandas as pd
        self.calls.append(str(day)[:10])
        LOG.append(("owed", str(day)[:10]))
        rows = [{"security_id": sid(s_), "security_bloomberg": s_, "date": d, "funds": "AAA,BBB"} for s_, d in owed_units()]
        return pd.DataFrame(rows, columns=["security_id", "security_bloomberg", "date", "funds"])

    def summary(self, df):
        if df is None or len(df) == 0:
            return {"securities": 0, "units": 0, "dates": 0, "newest": None, "oldest": None}
        return {"securities": int(df["security_id"].nunique()), "units": int(len(df)), "dates": int(df["date"].nunique()),
                "newest": max(df["date"]), "oldest": min(df["date"])}


class Client:
    """The recording stub of the vendor seam. A historical call answers every requested field for every trading day of its window
    (`CRNCY` as "USD"); a reference call for exactly ["CRNCY"] answers `LOOKUP` (or raises when `ref_fail`); any other answers {}."""

    def __init__(self, days, ref_fail=False):
        self.days, self.hist, self.ref, self.ref_fail = days, [], [], ref_fail

    @staticmethod
    def _iso(x):
        s = str(x)[:10]
        return s if "-" in s else f"{s[:4]}-{s[4:6]}-{s[6:8]}"

    def historical(self, securities, fields, start=None, end=None, *a, **k):
        lo, hi = self._iso(start), self._iso(end)
        self.hist.append((list(securities), list(fields), lo, hi))
        LOG.append(("hist", list(securities), list(fields), lo, hi))
        return {sec: {d: {f: ("USD" if f == "CRNCY" else close_of(sec, d)) for f in fields} for d in self.days if lo <= d <= hi}
                for sec in securities}

    def reference(self, securities, fields, overrides=None, timeout_s=90.0, *a, **k):
        self.ref.append((list(securities), list(fields)))
        LOG.append(("ref", list(securities), list(fields)))
        if list(fields) != ["CRNCY"]:
            return {}
        if self.ref_fail:
            raise RuntimeError("stub: the currency request failed")
        return {sec: {"CRNCY": LOOKUP[sec]} for sec in securities if sec in LOOKUP}


class RecSink:
    """A `local:` sink that records every put (uri, digest) in the ordered log."""
    kind = "local"

    def __init__(self, root):
        from rivalfunds import sinks
        self.inner = sinks.LocalSink(root)

    def get(self, uri):
        return self.inner.get(uri)

    def exists(self, uri):
        return self.inner.exists(uri)

    def list(self, prefix):
        return self.inner.list(prefix)

    def put(self, uri, data, content_type=None):
        LOG.append(("put", uri, hashlib.sha256(data).hexdigest()[:16]))
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


def plant(eb, root, stored):
    """One planted object per owed partition (ZZZ, "historical"); the STORE_DATE one also carries `stored` {security: currency}."""
    from rivalfunds import sinks
    s = sinks.LocalSink(root)
    out = {}
    for d in OWED_DATES:
        prov = {"revision": PLANTED_REV, "produced_at": "2026-09-24T01:00:00Z", "producer_version": "planted", "input_manifest": "{}"}
        data = {"ZZZ US Equity": {"PX_LAST": 1.0}}
        if d == STORE_DATE:
            data.update({sec: {"PX_LAST": 2.0, "CRNCY": ccy} for sec, ccy in stored.items()})
        uri = eb.market_target_uri(d, PLANTED_REV)
        raw = eb._parquet_bytes(eb._market_table(eb.market_rows(data, d, "planted", prov, "historical")))
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


def arm(ctx, name, env_value, stored, ref_fail=False):
    """One isolated daily run on a fresh sink holding the planted objects. Returns the facts; never raises for a raising run."""
    eb, bb, homes, days = ctx["eb"], ctx["bb"], ctx["homes"], ctx["days"]
    root = c.tmpdir(f"rv_tc1_{name}_")
    planted = plant(eb, root, stored)
    LOG.clear()
    sink, client, stub = RecSink(root), Client(days, ref_fail), sys.modules["rivalfunds.history_owed"]
    stub.calls.clear()
    keep = {k: getattr(eb, k) for k in ("dt", "_blp_historical_data", "_blp_reference_data", "_run_date_et")}
    real_check, real_record = bb.check_points, bb.record

    def check_points(points, today=None):
        LOG.append(("check_points", int(points)))
        return real_check(points, today)

    def record(mode, rows, batch_id):
        LOG.append(("record", mode, int(rows), batch_id))
        return real_record(mode, rows, batch_id)

    eb.dt, eb._blp_historical_data, eb._blp_reference_data = clock_shim(), client.historical, client.reference
    eb._run_date_et = lambda: RUN_DATE
    bb.check_points, bb.record = check_points, record
    prev, prev_dir = os.environ.pop(ENV, None), os.environ.get(bb.ENV_DIR)
    if env_value is not None:
        os.environ[ENV] = env_value
    os.environ[bb.ENV_DIR] = c.tmpdir(f"rv_tc1_{name}_ledger_")
    buf, raised = io.StringIO(), None
    try:
        with contextlib.redirect_stdout(buf):
            res = eb.handler_entry({"mode": "daily", "date": DAY, "batch_id": BATCH_ID, "securities": list(DAILY_SECS), "sink": sink})
    except Exception as e:  # noqa: BLE001 -- a raising run is a failed arm, not a dead check
        res, raised = {"status": f"RAISED {type(e).__name__}", "detail": str(e)}, f"{type(e).__name__}: {e}"
    finally:
        for k, val in keep.items():
            setattr(eb, k, val)
        bb.check_points, bb.record = real_check, real_record
        os.environ.pop(ENV, None)
        if prev is not None:
            os.environ[ENV] = prev
        if prev_dir is None:
            os.environ.pop(bb.ENV_DIR, None)
        else:
            os.environ[bb.ENV_DIR] = prev_dir
    lines = [ln.strip() for ln in buf.getvalue().splitlines() if ln.strip()]
    log = list(LOG)
    return {"res": res if isinstance(res, dict) else {"status": repr(res)}, "raised": raised, "lines": lines,
            "hline": [ln for ln in lines if ln.startswith("HISTORY OWED:")], "log": log, "client": client, "planted": planted,
            "owed_calls": list(stub.calls), "parts": partitions(root, homes, OWED_DATES + [DAY]),
            "puts": [e for e in log if e[0] == "put"], "cps": [e[1] for e in log if e[0] == "check_points"],
            "recs": [e for e in log if e[0] == "record"],
            "reqs": [e for e in log if e[0] == "hist" and is_owed_request(eb, e)],
            "ccy_refs": [e for e in log if e[0] == "ref" and e[2] == ["CRNCY"]],
            "other_refs": [e for e in log if e[0] == "ref" and e[2] != ["CRNCY"]]}


def new_rows(r):
    """Every row of every object that is not the planted one, in the owed partitions: [(partition date, row dict)]."""
    import pyarrow.parquet as pq
    out = []
    for d in OWED_DATES:
        for u, raw in r["parts"][d].items():
            if u != r["planted"][d][0]:
                for row in pq.read_table(io.BytesIO(raw)).to_pandas().to_dict("records"):
                    out.append((d, row))
    return out


def new_object_count(r):
    return sum(1 for d in OWED_DATES for u in r["parts"][d] if u != r["planted"][d][0])


def nz(v):
    """A parquet cell as a plain value: None for a NULL / NaN, else the stripped string."""
    return None if v is None or (isinstance(v, float) and v != v) else str(v).strip()


def currencies(r):
    """{(security, partition date): currency or None} of the landed top-up rows."""
    return {(row.get("security_bloomberg"), d): nz(row.get("currency")) for d, row in new_rows(r)}


def price_date_problems(r):
    probs = []
    for d, row in new_rows(r):
        sec = row.get("security_bloomberg")
        if "price_date" not in row:
            probs.append(f"{d}: {sec} has no price_date column")
        elif nz(row["price_date"]) is None or nz(row["price_date"])[:10] != d:
            probs.append(f"{d}: {sec} price_date {row['price_date']!r}")
        if str(row.get("date"))[:10] != d:
            probs.append(f"{d}: {sec} date {row.get('date')!r}")
    return probs


def first_index(log, pred):
    return next((i for i, e in enumerate(log) if pred(e)), None)


def grade(letter, title, fn):
    """Run one arm: `fn()` returns (ok, evidence). A raising arm FAILS; it never stops the script."""
    try:
        ok, evidence = fn()
    except Exception as e:  # noqa: BLE001 -- an arm fails cleanly
        ok, evidence = False, f"the arm raised {type(e).__name__}: {e}"
    print(f"  ({letter}) evidence: {evidence}")
    print(f"{'OK' if ok else 'FAIL'} ({letter}) {title}")
    if not ok:
        FAILS.append(letter)


def run_tw1_ac1():
    """`tw-1.AC1.py` in its own process, from the worktree root, against the same package this check grades."""
    path = str(HERE / "tw-1.AC1.py")
    env = {k: v for k, v in os.environ.items() if k not in (ENV, "RIVALFUNDS_BBG_BUDGET_DIR")}
    env["RIVALFUNDS_BBG_BUDGET_DIR"] = c.tmpdir("rv_tc1_tw1_ledger_")
    alt = os.environ.get(ROOT_ENV)
    if alt:   # the package is resolved before the check's own path setup; the check file itself is run unchanged
        boot = ("import runpy, sys; sys.path.insert(0, sys.argv[1]); import rivalfunds; sys.argv = [sys.argv[2]]; "
                "runpy.run_path(sys.argv[0], run_name='__main__')")
        cmd = [sys.executable, "-c", boot, alt, path]
    else:
        cmd = [sys.executable, path]
    p = subprocess.run(cmd, cwd=str(c.ROOT), env=env, capture_output=True, timeout=900)
    out = [ln.strip() for ln in p.stdout.decode("utf-8", "replace").splitlines() if ln.strip()]
    return p.returncode, (out[-1] if out else ""), p.stderr.decode("utf-8", "replace").strip()[-300:]


def build_context():
    c.setup_path()
    alt = os.environ.get(ROOT_ENV)
    if alt:
        sys.path.insert(0, alt)
    c.offline_guards()
    fake = types.ModuleType("integrations.bloomberg.mcp")

    def _leak(*a, **k):
        raise PermissionError("offline check: blp_client is refused (no Bloomberg call)")

    fake.blp_client = types.SimpleNamespace(reference_data=_leak, historical_data=_leak)
    sys.modules["integrations.bloomberg.mcp"] = fake
    stub = OwedStub()
    sys.modules["rivalfunds.history_owed"] = stub

    from lib import trading_calendar as tc
    import rivalfunds
    from rivalfunds import bbg_budget as bb
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes

    rivalfunds.history_owed = stub
    days = [d.isoformat() for d in tc.trading_days_between("2026-09-01", "2026-10-07")]
    after = [d for d in days if d > DAY]
    return {"eb": eb, "bb": bb, "homes": homes, "days": days, "stub": stub, "page_day": after[0] if after else None, "runs": {}}


def main():
    ctx = None
    try:
        ctx = build_context()
    except Exception as e:  # noqa: BLE001 -- an import error is a FAIL of every arm, not a crash
        import traceback
        traceback.print_exc()
        print(f"setup failed: {type(e).__name__}: {e}")
    letters = "abcdefgh"
    if ctx is None:
        FAILS.extend(letters)
        for x in letters:
            print(f"FAIL ({x}) not run: the setup failed")
    else:
        body(ctx)
    print("AC1 RESULT: PASS 0 failures" if not FAILS else f"AC1 RESULT: FAIL {len(FAILS)} failure(s): {', '.join(FAILS)}")
    return 0 if not FAILS else 1


def body(ctx):
    eb, page_day = ctx["eb"], ctx["page_day"]
    units = set(owed_units())
    n_units = len(units)
    print(f"module under test: {eb.__file__}")
    print(f"fixture: report date {DAY}, run date {RUN_DATE}, page day {page_day}; stub owed frame {n_units} units over {OWED_DATES}; "
          f"stored currencies planted at {STORE_DATE}")
    spec = {"off": (None, STORED_MIXED, False), "print": ("print", STORED_MIXED, False), "all": ("ask", STORED_ALL, False),
            "mixed": ("ask", STORED_MIXED, False), "fail": ("ask", STORED_MIXED, True)}

    def run_of(name):
        """The named run, made once. A run that cannot be made raises here, inside the arm that asked for it."""
        if name not in ctx["runs"]:
            env_value, stored, ref_fail = spec[name]
            ctx["runs"][name] = arm(ctx, name, env_value, stored, ref_fail)
        return ctx["runs"][name]

    def arm_a():
        p, m = run_of("print"), run_of("mixed")
        ok = bool(page_day) and all(r["owed_calls"] and set(r["owed_calls"]) == {page_day} for r in (p, m))
        return ok, f"owed() day in print {p['owed_calls']}, in ask {m['owed_calls']}; the page day is {page_day}"

    def arm_b():
        r, off = run_of("all"), run_of("off")
        got = currencies(r)
        want = {(s, d): STORED_ALL[s] for s, d in units}
        recs = [e for e in r["recs"] if e[1] == "history-owed"]
        pts = sum(points_of(ctx["days"], e) for e in r["reqs"])
        ok = (not r["raised"] and not r["ccy_refs"] and r["other_refs"] == off["other_refs"] and got == want and r["cps"] == [n_units]
              and bool(r["reqs"]) and len(recs) == len(r["reqs"]) and sum(e[2] for e in recs) == pts == n_units)
        wrong = {k: v for k, v in got.items() if want.get(k) != v}
        return ok, (f"CRNCY reference requests {len(r['ccy_refs'])} | check_points calls {r['cps']} (units {n_units}) | landed rows "
                    f"{len(got)} of {n_units}, rows whose currency is not the stored one: {len(wrong)} {sorted(wrong.items())[:3]} | "
                    f"history requests {len(r['reqs'])}, history-owed records {[e[2] for e in recs]} | line {r['hline']} | raised "
                    f"{r['raised']}")

    def arm_c():
        r, off = run_of("mixed"), run_of("off")
        log = r["log"]
        i_cp = first_index(log, lambda e: e[0] == "check_points")
        i_ref = first_index(log, lambda e: e[0] == "ref" and e[2] == ["CRNCY"])
        i_hist = first_index(log, lambda e: e[0] == "hist" and is_owed_request(eb, e))
        asked_secs = [sorted(e[1]) for e in r["ccy_refs"]]
        got = currencies(r)
        want = {(s, d): EXPECT_MIXED[s] for s, d in units}
        recs = [e for e in r["recs"] if e[1] == "history-owed"]
        pts = sum(points_of(ctx["days"], e) for e in r["reqs"])
        order_ok = None not in (i_cp, i_ref, i_hist) and i_cp < i_ref < i_hist
        ok = (not r["raised"] and asked_secs == [sorted(LATE)] and r["other_refs"] == off["other_refs"] and order_ok
              and r["cps"] == [n_units + len(LATE)] and len(recs) == len(r["reqs"]) + 1
              and sum(e[2] for e in recs) == pts + len(LATE) and pts == n_units and all(e[3] for e in recs) and got == want)
        wrong = {k: v for k, v in got.items() if want.get(k) != v}
        return ok, (f"CRNCY reference requests {asked_secs} (want one, for {sorted(LATE)}) | log positions: check_points {i_cp}, "
                    f"CRNCY request {i_ref}, first history request {i_hist} | check_points calls {r['cps']} (want "
                    f"[{n_units + len(LATE)}]) | history requests {len(r['reqs'])} ({pts} points), history-owed records "
                    f"{[e[2] for e in recs]} | landed rows {len(got)} of {n_units}, wrong currency: {len(wrong)} "
                    f"{sorted(wrong.items(), key=str)[:4]} | raised {r['raised']}")

    def arm_d():
        r = run_of("fail")
        carried = any(re.search(rf"\bcarried {n_units}\b", ln) for ln in r["hline"])
        ok = (not r["raised"] and len(r["ccy_refs"]) == 1 and not r["reqs"] and new_object_count(r) == 0 and carried)
        return ok, (f"CRNCY reference requests {len(r['ccy_refs'])} (the stub raises) | history requests of the leg {len(r['reqs'])} | "
                    f"new objects {new_object_count(r)} | HISTORY OWED lines {r['hline']} | carried {n_units} on one: {carried} | "
                    f"raised {r['raised']}")

    def arm_e():
        m, p, off = run_of("mixed"), run_of("print"), run_of("off")
        n = len(LATE)
        ask_ok = len(m["hline"]) == 1 and re.search(rf"\bcurrency lookups {n}\b", m["hline"][0]) is not None
        print_ok = len(p["hline"]) == 1 and f"currency lookups {n} (not sent)" in p["hline"][0]
        same_req = p["client"].hist == off["client"].hist and p["client"].ref == off["client"].ref
        same_puts = p["puts"] == off["puts"]
        budget = p["cps"] + p["recs"]
        ok = ask_ok and print_ok and same_req and same_puts and not budget and not p["raised"] and new_object_count(p) == 0
        return ok, (f"ask line {m['hline']} | print line {p['hline']} | print requests equal the switch-off run: {same_req} "
                    f"({len(p['client'].hist)} historical, {len(p['client'].ref)} reference) | puts equal: {same_puts} "
                    f"({len(p['puts'])} vs {len(off['puts'])}) | budget calls in print: {budget} | raised {p['raised']}")

    def arm_f():
        notes, ok = [], True
        for name in ("all", "mixed"):
            r = run_of(name)
            landed = {(row.get("security_bloomberg"), d) for d, row in new_rows(r)}
            probs = price_date_problems(r)
            ok = ok and landed == units and not probs and new_object_count(r) == len(OWED_DATES)
            notes.append(f"{name}: {len(landed)} of {n_units} units in {new_object_count(r)} new objects, problems {probs[:3]}")
        return ok, " | ".join(notes)

    def arm_g():
        rc, last, err = run_tw1_ac1()
        return rc == 0 and last == "AC1 RESULT: PASS 0 failures", f"tw-1.AC1.py rc {rc}, last line {last!r}" + (
            f", stderr tail {err!r}" if rc != 0 else "")

    def arm_h():
        off = run_of("off")
        import pyarrow.parquet as pq
        uri, raw = off["planted"][STORE_DATE]
        df = pq.read_table(io.BytesIO(raw)).to_pandas()
        read_back = {s: nz(v) for s, v in zip(df["security_bloomberg"], df["currency"]) if s in STORED_MIXED}
        decoys = {DAY, (dt.date.fromisoformat(DAY) + dt.timedelta(days=1)).isoformat(), RUN_DATE.isoformat()}
        as_planted = all(set(off["parts"][d]) == {off["planted"][d][0]} for d in OWED_DATES)
        ok = (off["res"].get("status") == "OK" and len(off["parts"][DAY]) == 1 and len(off["client"].hist) + len(off["client"].ref) > 0
              and not off["owed_calls"] and not off["hline"] and as_planted and read_back == STORED_MIXED
              and bool(page_day) and page_day not in decoys and not off["cps"] and not off["raised"])
        return ok, (f"switch-off status {off['res'].get('status')} | market objects at {DAY}: {len(off['parts'][DAY])} | client requests "
                    f"{len(off['client'].hist) + len(off['client'].ref)} | owed() calls {off['owed_calls']} | owed partitions as planted: "
                    f"{as_planted} | planted stored currencies read back {read_back} | page day {page_day} vs decoys {sorted(decoys)}")

    grade("a", "the window's end: owed() is called with the next trading day after the report date, in print and in ask", arm_a)
    grade("b", "ask, every asked security stored: no currency request, every row carries its stored currency, check_points(units)",
          arm_b)
    grade("c", "ask, three securities not stored: ONE CRNCY request for exactly those, after check_points(units + lookups) and "
               "before any history request, recorded as history-owed; rows carry the stored or looked-up currency, NULL when none",
          arm_c)
    grade("d", "ask, the currency request fails: no history request, no new object, a line with carried <all>", arm_d)
    grade("e", "the lines: ask has 'currency lookups <n>'; print has 'currency lookups <n> (not sent)', sends, writes and records "
               "nothing", arm_e)
    grade("f", "price_date is on every top-up row and equals its partition date; every unit lands (round 27)", arm_f)
    grade("g", "switch OFF: tw-1.AC1.py ends 'AC1 RESULT: PASS 0 failures'", arm_g)
    grade("h", "control: the switch-off run lands its market object, calls no owed stub, the fixture reads back", arm_h)


if __name__ == "__main__":
    sys.exit(main())
