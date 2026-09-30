"""RIV-s-1 AC2 -- a replay is idempotent: replaying the same bronze twice adds no rows, and a bronze object whose
sidecar status is not OK is skipped and counted, never given a report date."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import silver_issuer
    from rivalfunds.collector_issuer import land_bronze

    files = c.archive_files(3)
    sink = c.tmpdir("rv_s1b_")
    c.land(sink, files)
    meta = c.archive_meta(files[-1])
    land_bronze(raw=files[-1].read_bytes(), requested_date="2099-01-02", source_url=meta["url"], sink=f"local:{sink}", captured_at=meta["at"])
    ev = {"mode": "replay", "batch_id": "chk", "sink": f"local:{sink}", "date": meta["requested_date"]}
    r1 = silver_issuer.handler_entry(dict(ev))
    silver_root = c.local_path(sink, c.address("issuer-site", "etfs", "silver", "holdings", "date=")).parent
    df1, n1 = c.read_parquets(silver_root)
    r2 = silver_issuer.handler_entry(dict(ev))
    df2, n2 = c.read_parquets(silver_root)
    print("r1:", str(r1)[:400])
    print("r2:", str(r2)[:400])
    expected = sum(c.all_rows(f) for f in files)
    v.check(len(df1) == expected, f"first replay: {len(df1)} rows == {expected} source rows (the DATE-MISMATCH object adds none)")
    v.check(len(df2) == len(df1), f"second replay adds no rows ({len(df2)} == {len(df1)})")
    v.check("2099-01-02" not in str(sorted(p.name for p in silver_root.glob("date=*"))), "no silver partition for the mismatched request date")
    skipped = (r1.get("detail") or {}).get("skipped_not_ok") if isinstance(r1.get("detail"), dict) else None
    v.check(skipped == 1, f"detail.skipped_not_ok == 1 (got {skipped})")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
