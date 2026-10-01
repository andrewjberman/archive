"""RIV-r-3 AC1 -- issuer silver supersedes WITHOUT deleting (row Z-S4, the W5-S24 remedy on the issuer side).

Real bytes: the newest archived BASG issuer file is landed once at its own captured_at, replayed into silver, then landed
AGAIN (same bytes, captured 1 hour later) and replayed. The second replay must:
  - return status OK WITH a marker (a re-capture of a landed report date never leaves the batch markerless);
  - KEEP both silver objects for that report date (a local unlink always succeeds, so retention is asserted directly);
  - record the earlier object in detail.dropped_captures with retained = True;
and canonical_shape (G1) for that date must read the LATER capture's revision.
Control: the first replay wrote exactly one object."""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import collector_issuer, silver_issuer, homes

    sink = c.tmpdir("rv_r3a1_")
    f = c.archive_files(1)[0]
    meta = c.archive_meta(f)
    rd = meta["requested_date"]
    collector_issuer.land_bronze(raw=f.read_bytes(), requested_date=rd, source_url=meta["url"], sink=f"local:{sink}",
                                 captured_at=meta["at"])
    r1 = silver_issuer.handler_entry({"mode": "replay", "batch_id": "r3-a", "sink": f"local:{sink}", "date": rd})
    sdir = c.local_path(sink, homes.issuer_silver(rd, "x")).parent
    first = sorted(p.name for p in sdir.glob("*.parquet"))
    v.check(r1.get("status") == "OK" and len(first) == 1, f"control: first replay OK with one object ({r1.get('status')}, {first})")

    later = (dt.datetime.fromisoformat(meta["at"]) + dt.timedelta(hours=1)).isoformat()
    collector_issuer.land_bronze(raw=f.read_bytes(), requested_date=rd, source_url=meta["url"], sink=f"local:{sink}",
                                 captured_at=later)
    r2 = silver_issuer.handler_entry({"mode": "replay", "batch_id": "r3-b", "sink": f"local:{sink}", "date": rd})
    after = sorted(p.name for p in sdir.glob("*.parquet"))
    print("second replay:", r2.get("status"), "marker:", r2.get("marker"), "objects:", after)
    v.check(r2.get("status") == "OK" and bool(r2.get("marker")), "re-capture: status OK with a marker")
    v.check(len(after) == 2 and first[0] in after, f"both silver objects kept ({len(after)})")
    dropped = (r2.get("detail") or {}).get("dropped_captures") or []
    v.check(any(d.get("retained") is True and first[0].endswith(f"{d.get('capture_id')}.parquet") for d in dropped),
            f"the earlier object is recorded retained ({dropped})")

    g1 = c.replay("gold_canonical_shape", sink, rd, batch_id="r3-g1")
    print("canonical:", g1.get("status"))
    df, _n = c.read_parquets(c.gold_dir(sink, "canonical_shape") / ("date=" + rd))
    newest = max(after)[len("basg-"):-len(".parquet")]
    revs = set(df["dataset_revision"].astype(str)) if len(df) else set()
    v.check(newest in revs, f"G1 reads the later capture {newest} (revisions {sorted(revs)[:3]})")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
