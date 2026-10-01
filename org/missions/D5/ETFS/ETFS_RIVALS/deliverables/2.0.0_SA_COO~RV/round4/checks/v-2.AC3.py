"""RIV-v-2 AC3 (reopen, row Z-S9) -- an issuer row names ITS OWN source channel: GQGU's G1 rows carry
source_channel 'issuer-site:gqgu' (today every issuer row is stamped the constant 'issuer-site:basg',
gold_canonical_shape.py SOURCE_CHANNEL). Same setup as AC2: real BASG bytes, a GQGU silver object planted at the adapter's name.
  - G1's GQGU rows all carry source_channel 'issuer-site:gqgu';
  - control: G1's BASG rows all carry source_channel 'issuer-site:basg' (unchanged)."""
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

    sink = c.tmpdir("rv_v2c_")
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
    c.replay("gold_canonical_shape", sink, rd, batch_id="v2c")
    df, _ = c.read_parquets(c.gold_dir(sink, "canonical_shape") / f"date={rd}")
    g1 = c.newest_rows(df.assign(_date=rd)) if len(df) else df
    ft = g1["fund_ticker"].astype(str).str.strip() if len(g1) else []
    nb, ng = int((ft == "BASG").sum()) if len(g1) else 0, int((ft == "GQGU").sum()) if len(g1) else 0
    print(f"G1 rows: BASG {nb}, GQGU {ng} (silver rows {n_basg})")
    gq = g1[ft == "GQGU"] if len(g1) else g1
    bs = g1[ft == "BASG"] if len(g1) else g1
    sg = sorted(set(gq["source_channel"].astype(str))) if len(gq) else []
    sb = sorted(set(bs["source_channel"].astype(str))) if len(bs) else []
    print(f"source_channel: GQGU {sg}, BASG {sb}")
    v.check(ng > 0 and sg == ["issuer-site:gqgu"], "G1's GQGU rows carry source_channel issuer-site:gqgu")
    v.check(nb > 0 and sb == ["issuer-site:basg"], "control: G1's BASG rows carry source_channel issuer-site:basg")

failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
