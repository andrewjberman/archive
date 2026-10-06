"""RIV-eg-1 AC1 (row Z-S25; round-9 analysis item 1, ruling 1): the G4 enrichment never lands an all-empty or all-error revision.
Measured 2026-10-05: the 08:32 ET vehicle's enrichment ran against a no-data Terminal and landed
`gold/security_market/date=2026-10-02/market-20261005T123318Z-c86a8d9e27fa.parquet` -- 601 rows, px_close / gics_sector /
security_name all null -- as the NEWEST revision (status OK, 601 security_errors), shadowing the good 10-04 revision for every
reader until a one-key restore at 12:46Z.

Interface (prescribed): `enrichment_bloomberg` mode `market` refuses to land a revision in which EVERY security is an error or
carries none of px_close, gics_sector and security_name: nothing is written, the prior revision stays the newest, and the result
reads status "REFUSED" with `detail.reason` naming the count ("all-empty: 0 of N securities carry ..."). A revision with at least
one usable security lands as today.
Fixture (offline, local sink; `_blp_reference_data` and `_blp_historical_data` stubbed; date 2026-10-02 is past, the
historical stub answers nothing so every security goes to the reference stub): securities AAA, BBB, CCC US Equity; a prior good
G4 revision already at date=2026-10-02:
  - (a) every security answers {"__error__": ...} -> status REFUSED, no new object, the prior revision is still the newest;
  - (b) every security answers with every field None (the 10-05 shape) -> status REFUSED, no new object;
  - (c) control: AAA answers px_close 10.0 and a sector, BBB and CCC error -> the revision lands (status OK, one new object).
FAIL at base: (a) and (b) FAIL (an all-error revision lands as OK); (c) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DATE = "2026-10-02"
SECS = ["AAA US Equity", "BBB US Equity", "CCC US Equity"]
PRIOR = "market-20261004T110545Z-aaaaaaaaaaaa.parquet"


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes, revision, sinks

    prefix = homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={DATE}") + "/"

    def arm(answer):
        spec = f"local:{c.tmpdir('rv_eg1_')}"
        s = sinks.get_sink(spec)
        buf = io.BytesIO()
        pq.write_table(pa.Table.from_pandas(pd.DataFrame([{"security_id": "AAA_US_Equity", "date": DATE, "px_close": 9.0,
                                                            "gics_sector": "Energy", "security_name": "Aaa Corp"}]),
                                            preserve_index=False), buf)
        s.put(prefix + PRIOR, buf.getvalue())
        eb._blp_historical_data = lambda secs, fields, start, end, timeout_s=90.0: {}
        eb._blp_reference_data = lambda secs, fields, overrides=None, timeout_s=90.0: {x: answer(x, fields) for x in secs}
        r = eb.handler_entry({"mode": "market", "date": DATE, "batch_id": "eg1", "sink": spec, "securities": SECS})
        objs = [u for u in s.list(prefix) if u.endswith(".parquet")]
        return r, objs, revision.newest(objs)

    ra, oa, na = arm(lambda x, f: {"__error__": "Daily Capacity, request is blocked"})
    print("(a)", ra.get("status"), str(ra.get("detail"))[:140], "| objects", len(oa), "| newest", na.rsplit("/", 1)[-1])
    v.check(ra.get("status") == "REFUSED" and len(oa) == 1 and na.endswith(PRIOR),
            "(a) an all-error revision is refused; the prior revision stays the newest")
    rb, ob, nb = arm(lambda x, f: {k: None for k in f})
    print("(b)", rb.get("status"), str(rb.get("detail"))[:140], "| objects", len(ob))
    v.check(rb.get("status") == "REFUSED" and len(ob) == 1 and nb.endswith(PRIOR),
            "(b) an all-empty revision (every field None) is refused")
    rc, oc, _ = arm(lambda x, f: ({k: (10.0 if k == "PX_LAST" else "Energy" if k == "GICS_SECTOR_NAME" else None) for k in f}
                                  if x.startswith("AAA") else {"__error__": "no data"}))
    print("(c)", rc.get("status"), "| objects", len(oc))
    v.check(rc.get("status") == "OK" and len(oc) == 2, "(c) control: a revision with one usable security lands")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
