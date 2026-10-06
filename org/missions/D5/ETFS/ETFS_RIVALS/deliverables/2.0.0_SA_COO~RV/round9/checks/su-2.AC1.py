"""RIV-su-2 AC1 (CTO~Z msg 29624 term 4): security_universe is built INCREMENTALLY -- the prior universe plus that day's G1 --
never a 3-year rescan. Measured: round 8's `gold_security_universe.handler_entry` reads every canonical_shape report date from
(as-of minus 3 years) through the as-of (504 dates on S3) and ran the publish Lambda into its 900 s timeout at 1024/1024 MB.

Interface (prescribed): `handler_entry({"date": <page day>, "sink", "mode": "incremental"|"seed"})`. `seed` keeps today's full
build (bounded by its own budget/cursor if it needs one). `incremental` reads the newest prior universe object dated before the
as-of and the canonical_shape of the as-of date ONLY, and writes the merged list at date=<as-of>: a new security is added with
first_seen = last_seen = the as-of; a security seen again keeps its first_seen, advances last_seen, adds its fund and counts
the date once more. With no prior universe object, `incremental` builds as `seed` does.
Fixture (offline, local sink): canonical for 2026-09-28, 09-29, 09-30 (fund TXUE; AAA and BBB on the first two dates, AAA and a
new CCC on 09-30); `seed` for page day 2026-09-30 (as-of 09-29) writes the prior universe; then:
  - (a) `incremental` for page day 2026-10-01 (as-of 09-30): CCC added (first_seen 09-30), AAA keeps first_seen 09-28 and reads
    last_seen 09-30 with n_report_dates 3, BBB unchanged (last_seen 09-29, n_report_dates 2);
  - (b) that incremental run GETs exactly ONE canonical_shape object (counted at the sink);
  - (c) control: `seed` for page day 2026-10-01 in a fresh sink yields the same rows (security_key, first_seen, last_seen,
    funds, n_report_dates) as (a).
FAIL at base: (b) FAILS (the mode is ignored and every date is read: 3 GETs); (a) and (c) PASS (a rescan is correct, only
unbounded)."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DATES = ("2026-09-28", "2026-09-29", "2026-09-30")
BOOKS = {"2026-09-28": ("AAA", "BBB"), "2026-09-29": ("AAA", "BBB"), "2026-09-30": ("AAA", "CCC")}
REV = "20261001T000000Z-cccccccccccc"
COLS = ["security_key", "first_seen", "last_seen", "funds", "n_report_dates"]


def stage(s):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import homes

    for d in DATES:
        rows = [{"fund_id": "TXUE", "fund_ticker": "TXUE", "report_date": d, "is_cash_line": False, "position_type": "long",
                 "security_bloomberg": f"{k} US Equity", "security_name": f"{k} Corp", "security_id": f"{k}_US_Equity",
                 "raw_identifier": f"{k} US Equity", "quantity": 100.0, "market_value": 1000.0, "weight": 0.5,
                 "dataset_revision": REV} for k in BOOKS[d]]
        buf = io.BytesIO()
        pq.write_table(pa.Table.from_pandas(pd.DataFrame(rows), preserve_index=False), buf)
        s.put(homes.canonical_shape(d, f"holdings-{REV}.parquet"), buf.getvalue())


def rows_of(s, res):
    import pyarrow.parquet as pq
    uri = [u for u in (res.get("outputs") or []) if u.endswith(".parquet")][0]
    df = pq.read_table(io.BytesIO(s.get(uri))).to_pandas()
    for col in ("first_seen", "last_seen"):
        df[col] = df[col].astype(str).str[:10]
    return df[COLS].sort_values("security_key").reset_index(drop=True)


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import gold_security_universe as gsu
    from rivalfunds import sinks

    spec = f"local:{c.tmpdir('rv_su2_')}"
    s = sinks.get_sink(spec)
    stage(s)
    r0 = gsu.handler_entry({"date": "2026-09-30", "sink": spec, "mode": "seed"})
    print("seed 09-30:", r0.get("status"), r0.get("detail"))

    real_get_sink, gets = sinks.get_sink, []

    class Counting:
        def __init__(self, inner):
            self.inner = inner

        def get(self, key, *a, **k):
            if "/canonical_shape/" in str(key):
                gets.append(key)
            return self.inner.get(key, *a, **k)

        def __getattr__(self, name):
            return getattr(self.inner, name)

    sinks.get_sink = lambda sp: Counting(real_get_sink(sp))
    try:
        r1 = gsu.handler_entry({"date": "2026-10-01", "sink": spec, "mode": "incremental"})
    finally:
        sinks.get_sink = real_get_sink
    a = rows_of(s, r1)
    print("incremental 10-01:", r1.get("status"), "| canonical GETs:", len(gets))
    print(a.to_string(index=False))
    by = {r["security_key"]: r for r in a.to_dict("records")}
    aaa, bbb, ccc = (by.get(f"{k} US Equity", {}) for k in ("AAA", "BBB", "CCC"))
    v.check(ccc.get("first_seen") == "2026-09-30" and aaa.get("first_seen") == "2026-09-28" and aaa.get("last_seen") == "2026-09-30"
            and int(aaa.get("n_report_dates", 0)) == 3 and bbb.get("last_seen") == "2026-09-29" and int(bbb.get("n_report_dates", 0)) == 2,
            "(a) incremental merges the prior universe with the as-of date's G1")
    v.check(len(gets) == 1, "(b) the incremental run reads exactly ONE canonical_shape object")

    spec2 = f"local:{c.tmpdir('rv_su2_seed_')}"
    s2 = sinks.get_sink(spec2)
    stage(s2)
    b = rows_of(s2, gsu.handler_entry({"date": "2026-10-01", "sink": spec2, "mode": "seed"}))
    v.check(a.astype(str).equals(b.astype(str)), "(c) control: seed for the same day yields the same rows")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
