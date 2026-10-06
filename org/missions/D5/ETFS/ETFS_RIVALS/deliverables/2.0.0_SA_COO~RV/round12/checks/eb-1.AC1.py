"""RIV-eb-1 AC1 (round-10 analysis ADDENDUM 2 @b555e81836; MSTR~Z msg 30005): when Bloomberg is unreachable, the enrichment stops
within a small fixed number of session attempts and exits with the distinct "unreachable" code, so the vehicle reaches its later
stages. Measured 2026-10-06: with the DAPI precondition already FAILED, `rivalfunds.enrichment_bloomberg` kept issuing one
blp_client request per batch (each opens its own session; `no RESPONSE ... within 90s` per batch) until Task Scheduler's
30-minute ExecutionTimeLimit killed the vehicle at 11:30:01Z (0x41306); the names stage and the D12 leg never ran.

Interface (prescribed; ETFS_RIVALS code only -- integrations/bloomberg/ is under Andrew's no-modify order and is not touched):
  - an exception is UNREACHABLE when its class name is `BloombergError` (blp_client's session/connect-level error) -- the
    session-start, open-service and no-RESPONSE-timeout failures; a `BlpResponseError` or a per-security error is not;
  - `enrichment_bloomberg.SESSION_ATTEMPTS` (module int, 2 or 3): after that many CONSECUTIVE unreachable failures in one run, the
    run makes no further Bloomberg call (dividends, market, names), lands nothing, and returns status FAILED with
    `detail.unreachable` true and `detail.session_attempts` = the count; `exit_code` maps it to 1 (the existing contract);
  - eg-1's guard is unchanged; a reachable session enriches as today.
Fixture (offline, local sink, the module's `_blp_reference_data` / `_blp_historical_data` stubbed; blpapi never imported): G1 for
2026-10-01 with 300 non-cash securities (6 batches of DEFAULT_BATCH 50); the run date pinned to 2026-10-06 (a past partition).
  - (a) both stubs raise BloombergError("could not start blpapi session to 127.0.0.1:8194 ..."): `main(["--mode","daily",...])`
    returns 1, the stubs were called at most SESSION_ATTEMPTS times in total, the printed result reads detail.unreachable true;
  - (b) the same with BloombergError("no RESPONSE from Bloomberg within 90s"): exit 1, calls <= SESSION_ATTEMPTS;
  - (c) control: reachable stubs -> mode market lands a G4 revision (status OK) and main daily exits 0.
FAIL at base: (a) and (b) FAIL (18 calls: 6 dividend + 6 historical + 6 reference batches; no SESSION_ATTEMPTS); (c) PASSES."""
import contextlib
import io
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D = "2026-10-01"
REV = "20261001T000000Z-eeeeeeeeeeee"
N = 300


class BloombergError(RuntimeError):
    """Same class NAME as integrations.bloomberg.mcp.blp_client.BloombergError (that module imports blpapi at load)."""


def put_parquet(s, uri, rows):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
    s.put(uri, buf.getvalue())


def g1_rows():
    base = {"report_date": D, "is_cash_line": False, "position_type": "long", "asset_class": "Equity", "quantity": 100.0,
            "weight": 0.003, "security_sedol": None, "provider_security_type": None, "dataset_revision": REV,
            "gics_sector": "Industrials", "fund_id": "TXUE", "fund_ticker": "TXUE", "security_cusip": None, "security_isin": None,
            "market_value": 1000.0}
    return [dict(base, security_id=f"S{i:03d}_US_Equity", raw_identifier=f"S{i:03d} US Equity",
                 security_bloomberg=f"S{i:03d} US Equity", security_name=f"Sec {i:03d} Inc") for i in range(N)]


def fixture():
    from rivalfunds import homes, sinks
    spec = f"local:{c.tmpdir('rv_eb1_')}"
    s = sinks.get_sink(spec)
    put_parquet(s, homes.canonical_shape(D, f"holdings-{REV}.parquet"), g1_rows())
    return spec, s


def run_main(eb, spec, batch):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = eb.main(["--mode", "daily", "--date", D, "--sink", spec, "--batch-id", batch])
    try:
        res = json.loads(buf.getvalue().strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        res = {}
    return rc, res


def run(v):
    c.setup_path()
    c.offline_guards()
    import datetime as dt

    from rivalfunds import enrichment_bloomberg as eb

    eb._run_date_et = lambda: dt.date(2026, 10, 6)
    bound = getattr(eb, "SESSION_ATTEMPTS", None)
    print("SESSION_ATTEMPTS:", bound)

    for arm, msg in (("(a)", "could not start blpapi session to 127.0.0.1:8194 (is the Terminal running + logged in?)"),
                     ("(b)", "no RESPONSE from Bloomberg within 90s")):
        calls = []

        def down(*a, **k):
            calls.append(1)
            raise BloombergError(msg)

        eb._blp_reference_data = down
        eb._blp_historical_data = down
        spec, _ = fixture()
        rc, res = run_main(eb, spec, f"eb1{arm[1]}")
        det = res.get("detail") if isinstance(res.get("detail"), dict) else {}
        print(arm, "rc:", rc, "| calls:", len(calls), "| status:", res.get("status"), "| unreachable:", det.get("unreachable"))
        v.check(isinstance(bound, int) and 1 <= bound <= 3 and rc == 1 and len(calls) <= bound and det.get("unreachable") is True,
                f"{arm} Bloomberg unreachable ({msg[:30]}...): exit 1 within SESSION_ATTEMPTS calls, detail.unreachable true")

    def ref(secs, fields, overrides=None, timeout_s=90.0):
        return {x: {f: (242.0 if f == "PX_LAST" else "USD" if f == "CRNCY" else "Industrials" if f == "GICS_SECTOR_NAME"
                        else "Name" if f == "LONG_COMP_NAME" else None) for f in fields} for x in secs}

    eb._blp_reference_data = ref
    eb._blp_historical_data = lambda secs, fields, start, end, timeout_s=90.0: {}
    spec, _ = fixture()
    r = eb.handler_entry({"mode": "market", "date": D, "batch_id": "eb1c", "sink": spec})
    spec2, _ = fixture()
    rc, res = run_main(eb, spec2, "eb1c2")
    print("(c) market:", r.get("status"), "| daily rc:", rc, res.get("status"))
    v.check(r.get("status") == "OK" and rc == 0, "(c) control: a reachable session lands G4 (OK) and the daily run exits 0")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
