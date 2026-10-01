"""RIV-v-2 AC2 -- the contract is PER FUND: with two issuer funds on one report date, G1 reads each fund's own newest issuer
capture (today G1 takes ONE issuer object per date across all funds: `max(issuer_uris, key=_revision)`).

Real BASG bytes: the newest archived BASG issuer day lands and replays into silver. A SECOND issuer fund's silver object for the
same report date is planted at the name the GQGU adapter will write -- `gqgu-<capture_id>.parquet`, capture time one hour
LATER -- holding BASG's rows re-labelled fund_ticker 'GQGU' (the interface RIV-q-1 implements; its own check covers the
real GQGU bytes). canonical_shape is replayed for that date. Then:
  - G1 holds BASG rows (BASG is not displaced by a later-named other fund's object);
  - G1 holds GQGU rows with source_used 'issuer';
  - control: BASG's G1 rows equal its BASG silver rows in count."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    import pyarrow as pa
    import pyarrow.parquet as pq
    from rivalfunds import homes

    sink = c.tmpdir("rv_v2b_")
    f = c.archive_files(1)[0]
    c.land(sink, [f])
    rd = c.archive_meta(f)["requested_date"]
    c.replay("silver_issuer", sink, rd)
    sdir = c.local_path(sink, homes.issuer_silver(rd, "x")).parent
    basg = sorted(sdir.glob("basg-*.parquet"))[-1]
    cid = basg.name[len("basg-"):-len(".parquet")]
    ts, sha = cid.split("-", 1)
    later = ts[:9] + f"{(int(ts[9:11]) + 1) % 24:02d}" + ts[11:]
    t = pq.read_table(io.BytesIO(basg.read_bytes()))  # by bytes: a path under date=... adds a hive partition column
    import pyarrow.compute as pc

    t = t.filter(pc.equal(pc.utf8_trim_whitespace(t["fund_ticker"]), "BASG"))  # the file carries every SEI fund
    n_basg = t.num_rows
    t = t.set_column(t.schema.get_field_index("fund_ticker"), "fund_ticker", pa.array(["GQGU"] * n_basg))
    buf = io.BytesIO()
    pq.write_table(t, buf)
    (sdir / f"gqgu-{later}-{sha}.parquet").write_bytes(buf.getvalue())
    print(f"date {rd}: basg object {basg.name}, planted gqgu-{later}-{sha}.parquet")
    c.replay("gold_canonical_shape", sink, rd, batch_id="v2b")
    df, _ = c.read_parquets(c.gold_dir(sink, "canonical_shape") / f"date={rd}")
    g1 = c.newest_rows(df.assign(_date=rd)) if len(df) else df
    ft = g1["fund_ticker"].astype(str).str.strip() if len(g1) else []
    nb, ng = int((ft == "BASG").sum()) if len(g1) else 0, int((ft == "GQGU").sum()) if len(g1) else 0
    print(f"G1 rows: BASG {nb}, GQGU {ng} (silver rows {n_basg})")
    v.check(nb > 0, "G1 holds BASG rows")
    gq = g1[ft == "GQGU"] if len(g1) else g1
    v.check(ng > 0 and set(gq["source_used"].astype(str)) == {"issuer"}, "G1 holds GQGU rows, source_used issuer")
    v.check(nb == n_basg, f"control: BASG G1 rows {nb} == BASG silver rows {n_basg}")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
