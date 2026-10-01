"""RIV-q-1 AC2 (reopen, rows ETFS_RIVALS-Z-W4-S12 / Z-W4-S13) -- G2 holdings_coverage observes each issuer fund from its OWN
captures: a GQGU capture is GQGU's coverage evidence and never BASG's.

Today `gold_holdings_coverage._issuer_obs` stamps EVERY issuer-site sidecar `fund: BASG` and `_latest` keeps the latest capture
per (BASG, issuer, day). The vehicle fetches BASG then GQGU each morning, so GQGU's capture is the later one and BASG's coverage
row for that day would read GQGU's file (0 BASG rows); GQGU itself gets no coverage row (its calendar reads unavailable).

Real bytes, the morning order reproduced: the BASG archive file for 2026-09-28 landed at its own capture time, then the GQGU file
for the same day landed 5 seconds LATER; silver, G1 and G2 replayed for that day into a local sink. Then, for expected 2026-09-28:
  - BASG's coverage row reads a basg-* capture and carries BASG's own row count;
  - GQGU has its own coverage row from a gqgu-* capture with GQGU's row count;
  - control: no coverage row of either fund points at the other fund's capture."""
import datetime as dt
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
    from rivalfunds import collector_issuer

    bfile = next(f for f in c.archive_files(400) if f.stem == D)
    gfile = c.main_root() / c.GQGU_REL / f"{D}.txt"
    bm, gm = c.archive_meta(bfile), c.archive_meta(gfile)
    b_at = dt.datetime.fromisoformat(bm["at"].replace("Z", "+00:00"))
    if b_at.tzinfo is None:
        b_at = b_at.replace(tzinfo=dt.timezone.utc)
    g_at = (b_at + dt.timedelta(seconds=5)).isoformat()
    sink = c.tmpdir("rv_q1b_")
    collector_issuer.land_bronze(raw=bfile.read_bytes(), requested_date=bm["requested_date"], source_url=bm["url"],
                                 sink=f"local:{sink}", captured_at=bm["at"], fund="BASG")
    collector_issuer.land_bronze(raw=gfile.read_bytes(), requested_date=gm["requested_date"], source_url=gm["url"],
                                 sink=f"local:{sink}", captured_at=g_at, fund="GQGU")
    for stage in ("silver_issuer", "gold_canonical_shape", "gold_holdings_coverage"):
        c.replay(stage, sink, D, batch_id="q1b")
    df, _ = c.read_parquets(c.gold_dir(sink, "holdings_coverage"))
    if len(df):
        df = df[df["expected_date"].astype(str).str[:10] == D]
    print(f"coverage rows for {D}: {len(df)}")

    def row(fund):
        r = df[df["fund_id"].astype(str).str.strip() == fund] if len(df) else df
        r = r[r["source"].astype(str) == "issuer"] if len(r) else r
        return r

    nb, ng = rows_of(bfile, "BASG"), rows_of(gfile, "GQGU")
    b, g = row("BASG"), row("GQGU")
    for name, r in (("BASG", b), ("GQGU", g)):
        print(name, [(str(x.sidecar_uri).rsplit("/", 1)[-1][:40], x.row_count) for x in r.itertuples()] if len(r) else [])
    v.check(len(b) >= 1 and all("/basg-" in str(u) for u in b["sidecar_uri"]) and int(b["row_count"].max()) == nb,
            f"BASG's coverage row reads a basg-* capture with BASG's {nb} rows")
    v.check(len(g) >= 1 and all("/gqgu-" in str(u) for u in g["sidecar_uri"]) and int(g["row_count"].max()) == ng,
            f"GQGU has its own coverage row from a gqgu-* capture with GQGU's {ng} rows")
    cross = (len(b) and any("/gqgu-" in str(u) for u in b["sidecar_uri"])) or (len(g) and any("/basg-" in str(u) for u in g["sidecar_uri"]))
    v.check(not cross, "control: no coverage row points at the other fund's capture")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
