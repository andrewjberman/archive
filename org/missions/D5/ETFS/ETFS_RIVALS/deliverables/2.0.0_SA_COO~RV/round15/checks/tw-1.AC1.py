"""RIV-tw-1 AC1 (FWD-24; C-OWED-IN-THE-LEG; CTO ruling R13; PRD v0.19): THE SWITCH IS OFF. With `RIVALFUNDS_HISTORY_OWED` unset,
empty or "0", a `daily` run of `enrichment_bloomberg.handler_entry` is byte-for-byte the run the module makes TODAY -- the same
sink calls, the same client requests, the same stdout, the same result dict -- and `rivalfunds.history_owed` is never imported.
The vehicle runs this module from the working tree every day at 11:00Z, so this is the arm that guards the job.

The baseline is the module AS IT IS AT BASE, read from git by pin (`git show 361b735308:data/etfs/scripts/rivalfunds/
enrichment_bloomberg.py`) and executed in this process as `rivalfunds.enrichment_bloomberg_base` beside the module under test:
it survives the build (the pin stays an ancestor), it is not a recorded snapshot (it is run, with the same fixture, the same
stubs, the same pinned clock), and at base the two runs are the same file. NO Bloomberg call: the vendor seam is the one
`tests/test_r12eb1_session_attempts.py` stubs (`_blp_historical_data` / `_blp_reference_data`), bound on BOTH modules to a
RECORDING stub; `integrations.bloomberg.mcp` is replaced by a module that records and raises; `boto3` and `requests.post` are
refused; `_run_date_et` is pinned to 2026-10-06 and the module's clock to 2026-10-06T11:00:05Z on both; the budget ledger is a
fresh temp dir per run (`RIVALFUNDS_BBG_BUDGET_DIR`); every sink is a recording wrapper of a `local:` sink.
Fixture: run date 2026-10-06, report date 2026-10-05, three securities in one G1 canonical_shape object (the vehicle passes no
`securities`, so the daily run reads them from G1 as it does live). Each run is `handler_entry({"mode": "daily", "date",
"batch_id", "sink"})` on a fresh sink, then `main(["--mode", "daily", "--date", ...])` on a second fresh sink.
A guard is planted BEFORE the module under test is first imported: a sentinel `rivalfunds.history_owed` in `sys.modules` that
records and raises on any attribute access, plus a recording `builtins.__import__` and `importlib.import_module`, so even a
top-level import by the module is seen.
  - (a) switch UNSET: the run's sink calls (list, get, exists, put -- put with a digest of its bytes), client requests (every
    historical and reference request, with its arguments), stdout lines, result dict (no `history_owed` key), budget-ledger
    lines, and `main`'s stdout and exit code are EQUAL to the base module's, run for run;
  - (b) the same with the variable set to the empty string;
  - (c) the same with the variable set to "0";
  - (d) across the three OFF runs `rivalfunds.history_owed` was never imported (no import request, no attribute access on the
    sentinel), and neither was it imported when the module under test was loaded;
  - (e) the module defines `HISTORY_OWED_CAP == 20000` (amended 2026-10-08 by RIV-tc-1 AMENDMENT 1, ruling R24; was 5000) and its source reads the environment variable named exactly
    `RIVALFUNDS_HISTORY_OWED`;
  - (f) control: the OFF daily run lands its market object (one `market-*.parquet` at the report date), the recording client
    was reached, and the base reference run did the same.
The module under test is NOT imported by name before the guard; nothing under `integrations/` is touched.
FAIL at base 361b735308: (e) FAILS (no `HISTORY_OWED_CAP`, the variable `RIVALFUNDS_HISTORY_OWED` is read nowhere: the module is
the base file); (a), (b), (c), (d), (f) PASS (the module under test IS the base module, so the OFF runs are the base run) and must
KEEP passing after the build."""
import builtins
import contextlib
import datetime as dt
import hashlib
import importlib
import io
import json
import os
import pathlib
import subprocess
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

BASE_PIN = "361b735308"
REL = "data/etfs/scripts/rivalfunds/enrichment_bloomberg.py"
ENV = "RIVALFUNDS_HISTORY_OWED"
OWED = "rivalfunds.history_owed"
DAY = "2026-10-05"                 # the report date the vehicle passes (the previous trading day)
RUN_DATE = dt.date(2026, 10, 6)
FIXED = dt.datetime(2026, 10, 6, 11, 0, 5, tzinfo=dt.timezone.utc)
SECS = ["AAA US Equity", "BBB US Equity", "CCC US Equity"]

SEEN: list = []                    # every sign that history_owed was asked for: (kind, detail)


class Sentinel(types.ModuleType):
    """`rivalfunds.history_owed` as the OFF path must never find it: any attribute access (beyond the import machinery's own
    dunders) is recorded and raises."""

    def __getattribute__(self, name):
        if name.startswith("__") and name.endswith("__"):
            return super().__getattribute__(name)
        SEEN.append(("attribute", name))
        raise AssertionError(f"history_owed.{name} touched with the switch OFF")


def plant_guards():
    sys.modules[OWED] = Sentinel(OWED)
    real_import, real_import_module = builtins.__import__, importlib.import_module

    def _imp(name, globals=None, locals=None, fromlist=(), level=0):  # noqa: A002
        if name.endswith("history_owed") or "history_owed" in (fromlist or ()):
            SEEN.append(("import", f"{name!r} fromlist={tuple(fromlist or ())} level={level}"))
        return real_import(name, globals, locals, fromlist, level)

    def _imp_module(name, package=None):
        if str(name).endswith("history_owed"):
            SEEN.append(("import_module", str(name)))
        return real_import_module(name, package)

    builtins.__import__, importlib.import_module = _imp, _imp_module


class Client:
    """The recording stub of the vendor seam. A historical call answers every requested field for every trading day of its
    own window; a reference call answers nothing (the daily dividends pull then writes its status rows)."""

    def __init__(self, days):
        self.days, self.hist, self.ref, self.leaked = days, [], [], []

    @staticmethod
    def _iso(x):
        s = str(x)[:10]
        return s if "-" in s else f"{s[:4]}-{s[4:6]}-{s[6:8]}"

    def historical(self, securities, fields, start=None, end=None, *a, **k):
        lo, hi = self._iso(start), self._iso(end)
        self.hist.append((list(securities), list(fields), lo, hi, repr(sorted(k))))
        return {s: {d: {f: 100.0 + i + int(d[-2:]) / 100 for f in fields} for d in self.days if lo <= d <= hi}
                for i, s in enumerate(securities)}

    def reference(self, securities, fields, overrides=None, timeout_s=90.0, *a, **k):
        self.ref.append((list(securities), list(fields), repr(overrides)))
        return {}


class RecSink:
    """A `local:` sink that records every call. `put` records a digest of the bytes; `overwrites` lists a put onto a key that
    already held an object."""
    kind = "local"

    def __init__(self, root, log):
        from rivalfunds import sinks
        self.inner, self.log, self.overwrites = sinks.LocalSink(root), log, []

    def get(self, uri):
        self.log.append(("get", uri))
        return self.inner.get(uri)

    def exists(self, uri):
        self.log.append(("exists", uri))
        return self.inner.exists(uri)

    def list(self, prefix):
        self.log.append(("list", prefix))
        return self.inner.list(prefix)

    def put(self, uri, data, content_type=None):
        self.log.append(("put", uri, hashlib.sha256(data).hexdigest()[:16]))
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


def plant_g1(root):
    """One G1 canonical_shape object at the report date: three non-cash securities of one fund (what the vehicle's daily run
    reads when it is passed no `securities`). Written straight to the dir, so it is in no run's call trace."""
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import homes, sinks

    df = pd.DataFrame({"fund_id": ["AAA"] * 3, "fund_ticker": ["AAA"] * 3, "security_bloomberg": SECS,
                       "is_cash_line": [False] * 3, "position_type": ["equity"] * 3})
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(df, preserve_index=False), buf)
    sinks.LocalSink(root).put(homes.canonical_shape(DAY, "holdings-20261005T100000Z-aaaaaaaaaaaa.parquet"), buf.getvalue())


def base_module():
    """The module as it is at the pin, executed here as `rivalfunds.enrichment_bloomberg_base` (a sibling in the package, so
    its relative imports resolve). Returns (module, None) or (None, why)."""
    r = subprocess.run(["git", "-C", str(c.ROOT), "show", f"{BASE_PIN}:{REL}"], capture_output=True)
    if r.returncode != 0:
        return None, f"git show {BASE_PIN}:{REL} rc={r.returncode}: {r.stderr.decode('utf-8', 'replace').strip()[:200]}"
    name = "rivalfunds.enrichment_bloomberg_base"
    mod = types.ModuleType(name)
    mod.__package__, mod.__file__ = "rivalfunds", f"<{BASE_PIN}:{REL}>"
    sys.modules[name] = mod
    exec(compile(r.stdout.decode("utf-8"), mod.__file__, "exec"), mod.__dict__)
    return mod, None


def bind(mod, client):
    """Pin the clock, the run date and the vendor seam on one module; returns the restore function."""
    keep = {k: getattr(mod, k) for k in ("dt", "_blp_historical_data", "_blp_reference_data", "_run_date_et")}
    mod.dt, mod._blp_historical_data, mod._blp_reference_data = clock_shim(), client.historical, client.reference
    mod._run_date_et = lambda: RUN_DATE

    def restore():
        for k, v in keep.items():
            setattr(mod, k, v)

    return restore


def ledger(bb):
    f = bb._ledger_file(bb._utc_today())
    out = []
    if f.is_file():
        for ln in f.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                d = json.loads(ln)
                out.append((d.get("mode"), d.get("rows"), d.get("batch_id")))
    return out


def run_once(mod, tag, env_value, days):
    """One daily run of `mod` plus one `main` run. Returns the measured facts as plain data."""
    from rivalfunds import bbg_budget as bb
    from rivalfunds import homes, sinks

    root, root_main = c.tmpdir(f"rv_tw1_{tag}_"), c.tmpdir(f"rv_tw1_{tag}_main_")
    plant_g1(root)
    plant_g1(root_main)
    log = []
    sink = RecSink(root, log)
    client = Client(days)
    restore = bind(mod, client)
    prev = os.environ.pop(ENV, None)
    if env_value is not None:
        os.environ[ENV] = env_value
    os.environ[bb.ENV_DIR] = c.tmpdir(f"rv_tw1_{tag}_ledger_")
    buf, buf_main = io.StringIO(), io.StringIO()
    try:
        try:
            with contextlib.redirect_stdout(buf):
                res = mod.handler_entry({"mode": "daily", "date": DAY, "batch_id": "chk-daily", "sink": sink})
        except Exception as e:  # noqa: BLE001 -- a raising run is a failed arm, not a dead check
            res = {"status": f"RAISED {type(e).__name__}", "detail": str(e)}
        led = ledger(bb)
        client_main = Client(days)
        restore()
        restore = bind(mod, client_main)
        os.environ[bb.ENV_DIR] = c.tmpdir(f"rv_tw1_{tag}_ledger_main_")
        try:
            with contextlib.redirect_stdout(buf_main):
                rc = mod.main(["--mode", "daily", "--date", DAY, "--sink", f"local:{root_main}", "--batch-id", "chk-main"])
        except Exception as e:  # noqa: BLE001
            rc = f"RAISED {type(e).__name__}: {e}"
        led_main = ledger(bb)
    finally:
        restore()
        os.environ.pop(ENV, None)
        if prev is not None:
            os.environ[ENV] = prev
    market = [u for u in sinks.LocalSink(root).list(homes.address("rivalfunds", "etfs", "gold", "security_market",
                                                                    f"date={DAY}") + "/") if u.endswith(".parquet")]
    return {"trace": log, "overwrites": sink.overwrites, "hist": client.hist, "ref": client.ref, "stdout": buf.getvalue(),
            "result": json.dumps(res, sort_keys=True, default=str), "has_key": "history_owed" in res, "ledger": led,
            "main_stdout": buf_main.getvalue(), "main_rc": rc, "main_hist": client_main.hist, "main_ref": client_main.ref,
            "main_ledger": led_main, "market": [u.rsplit("/", 1)[-1] for u in market], "status": res.get("status")}


FACTS = ("trace", "hist", "ref", "stdout", "result", "ledger", "main_stdout", "main_rc", "main_hist", "main_ref", "main_ledger")


def first_diff(a, b):
    """The first fact on which two runs differ, in words ('' when none)."""
    for k in FACTS:
        if a[k] != b[k]:
            x, y = a[k], b[k]
            if isinstance(x, list) and isinstance(y, list):
                n = next((i for i in range(min(len(x), len(y))) if x[i] != y[i]), min(len(x), len(y)))
                return (f"{k}: lengths {len(x)} vs {len(y)}, first difference at #{n}: "
                        f"{x[n] if n < len(x) else '-'} vs {y[n] if n < len(y) else '-'}")
            return f"{k}: {str(x)[:160]!r} vs {str(y)[:160]!r}"
    return ""


def run(v):
    c.setup_path()
    c.offline_guards()
    plant_guards()                                     # BEFORE the module under test is first imported
    fake = types.ModuleType("integrations.bloomberg.mcp")

    def _leak(*a, **k):
        raise PermissionError("offline check: blp_client is refused (no Bloomberg call)")

    fake.blp_client = types.SimpleNamespace(reference_data=_leak, historical_data=_leak)
    sys.modules["integrations.bloomberg.mcp"] = fake

    from lib import trading_calendar as tc
    from rivalfunds import enrichment_bloomberg as eb

    days = [d.isoformat() for d in tc.trading_days_between("2026-09-01", "2026-10-06")]
    print(f"module under test: {eb.__file__}")
    loaded_clean = not SEEN
    print(f"history_owed requests while loading the module under test: {len(SEEN)} {SEEN}")
    base, why = base_module()
    print(f"baseline: {BASE_PIN}:{REL} executed as rivalfunds.enrichment_bloomberg_base"
          if base is not None else f"baseline UNAVAILABLE: {why}")
    ref = run_once(base, "base", None, days) if base is not None else None
    if ref is not None:
        print(f"base run: status {ref['status']} | sink calls {len(ref['trace'])} | puts {sum(1 for t in ref['trace'] if t[0] == 'put')}"
              f" | historical requests {len(ref['hist'])} | reference requests {len(ref['ref'])} | stdout {len(ref['stdout'])} bytes"
              f" | main rc {ref['main_rc']} | main stdout {len(ref['main_stdout'])} bytes | market objects {ref['market']}")

    off = {}
    for arm, label, value in (("a", "UNSET", None), ("b", "EMPTY", ""), ("c", "0", "0")):
        r = run_once(eb, f"off_{arm}", value, days)
        off[arm] = r
        d = first_diff(r, ref) if ref is not None else "no baseline"
        print(f"switch {label}: status {r['status']} | sink calls {len(r['trace'])} | historical {len(r['hist'])} | reference "
              f"{len(r['ref'])} | stdout {len(r['stdout'])} bytes | history_owed key in result: {r['has_key']} | main rc "
              f"{r['main_rc']} | vs base: {'IDENTICAL' if not d else d}")
        v.check(ref is not None and not d and not r["has_key"] and not r["overwrites"] and r["status"] == ref["status"],
                f"({arm}) switch {label}: sink calls, client requests, stdout, result dict, ledger and main() are the base run's; "
                "no history_owed key")

    print(f"history_owed requests across the three OFF runs: {len(SEEN)} {SEEN}")
    v.check(loaded_clean and not SEEN,
            "(d) with the switch OFF, rivalfunds.history_owed is never imported (not at module load, not in the daily run)")

    src = pathlib.Path(eb.__file__).read_text(encoding="utf-8")
    cap = getattr(eb, "HISTORY_OWED_CAP", None)
    print(f"HISTORY_OWED_CAP = {cap!r} | source names {ENV!r}: {ENV in src} | source names HISTORY_OWED_CAP: {'HISTORY_OWED_CAP' in src}")
    v.check(cap == 20000 and isinstance(cap, int) and ENV in src,
            f"(e) the module defines HISTORY_OWED_CAP == 20000 and reads the variable {ENV}")

    ctl = off["a"]
    print(f"control: OFF daily run status {ctl['status']} | market objects at {DAY}: {ctl['market']} | client requests "
          f"{len(ctl['hist']) + len(ctl['ref'])} | base market objects {None if ref is None else ref['market']}")
    v.check(ref is not None and len(ctl["market"]) == 1 and ctl["market"][0].startswith("market-")
            and len(ctl["hist"]) + len(ctl["ref"]) > 0 and len(ref["market"]) == 1,
            "(f) control: the OFF daily run lands its one market object and reached the recording client (as the base run does)")


def main():
    v = c.Verdict("AC1")
    try:
        run(v)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 -- an import error at base is the expected FAIL of a build check
        v.check(False, f"exception: {type(e).__name__}: {e}")
    labels = ", ".join(m.split(" ")[0] if m.startswith("(") else "exception" for m in v.fails)
    print("AC1 RESULT: PASS 0 failures" if not v.fails else f"AC1 RESULT: FAIL {len(v.fails)}: {labels}")
    return 0 if not v.fails else 1


if __name__ == "__main__":
    sys.exit(main())
