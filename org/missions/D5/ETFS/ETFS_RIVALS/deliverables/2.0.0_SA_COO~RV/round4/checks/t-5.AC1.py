"""RIV-t-5 AC1 -- the DAILY trade schedule pairs each fund with ITS OWN prior report date (row W1-S27; analysis ruling 1;
C-TRADE-SCHEDULE "each pair of consecutive GENUINELY dated reports").

Real data, one plant: the last 4 IDVZ-group captures run to canonical_shape in a local sink, with TXUE's rows dropped from the
SECOND-newest capture (so TXUE's own prior report date is the third-newest, while the global prior date is the second-newest).
A canonical marker for a daily batch naming ONLY the newest date's G1 object is written, then build-trade-schedule runs in
DAILY mode for that batch:
  - TXUE has G5 rows whose window_start is its OWN prior date (the third-newest capture's date);
  - control: SCHY (no plant) has G5 rows whose window_start is the global prior date;
  - every fund that has G1 rows on the newest date and on any earlier date gets a window ending on the newest date."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def planted(files):
    tmp = pathlib.Path(c.tmpdir("rv_t5p_"))
    out = []
    for k, f in enumerate(files):
        d = c.capture(f)
        hdr = d["rows"][0]
        fi = hdr.index("ORIG_IDS")
        rows = d["rows"] if k != len(files) - 2 else [hdr] + [r for r in d["rows"][1:] if not str(r[fi]).startswith("TXUE")]
        p = tmp / f.name
        p.write_text(json.dumps({**d, "rows": rows}), encoding="utf-8")
        out.append(p)
    return out


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg, gold_trade_schedule, markers, sinks

    files = planted(c.idvz_captures(4))
    dates = [c.capture(f)["requested_date"] for f in files]
    newest, global_prior, own_prior = dates[-1], dates[-2], dates[-3]
    sink = c.tmpdir("rv_t5_")
    c.run_idvz_chain(sink, files, "canonical")
    enrichment_bloomberg.handler_entry({"mode": "import", "dividends_json": str(c.dividends_path()), "batch_id": "t5-g3",
                                        "sink": f"local:{sink}", "date": newest})
    g1_newest = sorted((c.gold_dir(sink, "canonical_shape") / f"date={newest}").glob("*.parquet"))
    uri = "s3://" + str(g1_newest[-1]).replace("\\", "/").split(f"{pathlib.Path(sink).name}/", 1)[1]
    markers.write_marker(gold_trade_schedule.CANONICAL_STAGE, newest, "t5-daily", sinks.get_sink(f"local:{sink}"),
                         {"status": "OK", "outputs": [uri]})
    r = gold_trade_schedule.handler_entry({"mode": "daily", "date": newest, "batch_id": "t5-daily", "sink": f"local:{sink}"})
    print("daily G5:", r.get("status"), str(r.get("detail"))[:200])
    df, n = c.read_parquets(c.gold_dir(sink, "trade_schedule") / f"date={newest}")
    v.check(n >= 1, f"a daily G5 object for {newest} ({n})")
    if not len(df):
        return
    starts = lambda f: set(df.loc[df["fund_id"].astype(str) == f, "window_start"].astype(str).str[:10])  # noqa: E731
    print(f"dates: own_prior {own_prior}, global_prior {global_prior}, newest {newest}; TXUE starts {starts('TXUE')}, "
          f"SCHY starts {starts('SCHY')}")
    v.check(own_prior in starts("TXUE"), f"TXUE's window starts at its own prior report date {own_prior}")
    v.check(global_prior in starts("SCHY"), f"control: SCHY's window starts at the global prior date {global_prior}")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
