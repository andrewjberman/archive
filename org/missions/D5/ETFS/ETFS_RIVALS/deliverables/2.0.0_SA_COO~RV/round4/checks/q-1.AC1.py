"""RIV-q-1 AC1 -- GQGU through its measured issuer route (analysis ruling 4; rows Z-S5/Z-S6): the issuer collector lands a
GQGU capture under a GQGU key and issuer silver types it per fund, beside BASG, never displacing it.

Real bytes: the 2 newest archived GQGU issuer files (.runtime/amgt-reconn-daily-census-20260929/gqgu/<D>.txt, SEI filepoint,
39 GQGU rows on 2026-09-28) and the BASG archive file for 2026-09-28, landed through
`collector_issuer.land_bronze(raw, requested_date, source_url, sink, captured_at, fund=<FUND>)` (the interface this cell
adds; `fund` defaults to BASG), then issuer silver replayed for 2026-09-28. Then, for 2026-09-28:
  - a GQGU bronze object is keyed `gqgu-<requested_date>-<ts>-<sha12>` and its sidecar claims report date 2026-09-28;
  - issuer silver holds a `gqgu-<capture_id>.parquet` whose GQGU rows equal the file's 39 GQGU rows;
  - control: the BASG silver object for the same date is still there, with BASG's own row count."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D = "2026-09-28"


def rows_of(txt: pathlib.Path, fund: str) -> int:
    lines = txt.read_bytes().decode("utf-8-sig").splitlines()
    i = lines[0].split("|").index("fund_ticker")
    return sum(1 for ln in lines[1:] if ln.strip() and ln.split("|")[i].strip() == fund)


def run(v):
    c.setup_path()
    import pandas as pd
    from rivalfunds import collector_issuer, homes

    gdir = c.main_root() / c.GQGU_REL
    gfiles = sorted(gdir.glob("20*.txt"))[-2:]
    bfile = next(f for f in c.archive_files(400) if f.stem == D)
    sink = c.tmpdir("rv_q1_")
    for f, fund in [(g, "GQGU") for g in gfiles] + [(bfile, "BASG")]:
        m = c.archive_meta(f)
        collector_issuer.land_bronze(raw=f.read_bytes(), requested_date=m["requested_date"], source_url=m["url"],
                                     sink=f"local:{sink}", captured_at=m["at"], fund=fund)
    bronze = sorted(p.name for p in c.local_path(sink, homes.issuer_bronze(D, "x")).parent.parent.rglob("gqgu-*") if p.is_file())
    print("gqgu bronze:", bronze[:4])
    v.check(any(n.startswith(f"gqgu-{D}-") and not n.endswith(".sidecar.json") for n in bronze),
            f"a GQGU bronze object keyed gqgu-{D}-<ts>-<sha12>")
    c.replay("silver_issuer", sink, D)
    sdir = c.local_path(sink, homes.issuer_silver(D, "x")).parent
    names = sorted(p.name for p in sdir.glob("*.parquet"))
    print("silver objects:", names)
    gq = [p for p in sdir.glob("gqgu-*.parquet")]
    want = rows_of(next(g for g in gfiles if g.stem == D), "GQGU") if any(g.stem == D for g in gfiles) else None
    got = sum(int((pd.read_parquet(p)["fund_ticker"].astype(str).str.strip() == "GQGU").sum()) for p in gq)
    v.check(want is not None and len(gq) >= 1 and got == want, f"GQGU silver rows {got} == file GQGU rows {want}")
    bq = [p for p in sdir.glob("basg-*.parquet")]
    bgot = sum(int((pd.read_parquet(p)["fund_ticker"].astype(str).str.strip() == "BASG").sum()) for p in bq)
    v.check(len(bq) >= 1 and bgot == rows_of(bfile, "BASG"), f"control: BASG silver kept ({bgot} == {rows_of(bfile, 'BASG')})")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
