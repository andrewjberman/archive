"""RIV-nf-1 AC1 (row Z-S29; CTO~Z ruling (B) 2026-10-05 16:22Z): the trade schedule rebuilds ONLY the named funds and carries
every other fund's rows from the prior object unchanged. Measured: `gold_trade_schedule.run_stage` builds one G5 object (and
its G6) per report date from every fund's windows; the D12 Step B mirror dry run re-derived every fund's trades on 189 dates
(confidence 176 dates, action 99, ...), and `hold_funds` drops a fund from the new object instead of keeping its rows.

Interface (prescribed): the stage event key `rebuild_funds` (a list of tickers). With it, for each scope date the new G5 object
is the newest prior G5 object's rows for every fund NOT named (values unchanged) plus freshly inferred rows for the named funds;
G6 likewise from the newest prior G6 object. A date with no prior object builds every fund. Without the key nothing changes.
Fixture (offline, local sink): canonical D1 and D2 for SCHY and TXUE (revision 20260930T000000Z-aaaaaaaaaaaa; SCHY doubles S1 on
D2, so it has a trade); G5/G6 built for D2;
the prior G5's SCHY rows then carry est_price 999.0 (standing in for rows an older code wrote); a NEWER canonical revision of D2
(20261001T000000Z-bbbbbbbbbbbb) doubles TXUE's S3; the stage runs for D2 with that batch.
  - (a) with rebuild_funds ['TXUE']: the newest G5 at D2 holds SCHY's prior rows unchanged (est_price 999.0, same row count) and
    TXUE rows re-inferred from the new revision (they differ from the prior TXUE rows);
  - (b) with rebuild_funds ['TXUE']: the newest G6 at D2 holds SCHY's prior G6 row unchanged;
  - (c) control: without rebuild_funds, SCHY's rows are re-inferred (no est_price 999.0).
FAIL at base: (a) and (b) FAIL (the key is ignored, every fund is re-inferred); (c) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

REV_A, REV_B = "20260930T000000Z-aaaaaaaaaaaa", "20261001T000000Z-bbbbbbbbbbbb"
KEY = "S3 US Equity"


def build(rebuild):
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import gold_trade_schedule as g
    from rivalfunds import homes, markers, revision, sinks
    from rivalfunds.tests.test_g52_trade_schedule_v2 import BOOK, D1, D2, _canon, _doubled, _put_canonical

    spec = f"local:{c.tmpdir('rv_nf1_')}"
    s = sinks.get_sink(spec)
    for d in (D1, D2):
        schy = _doubled(BOOK, "S1 US Equity") if d == D2 else BOOK  # SCHY trades S1 on D2 in both revisions
        _put_canonical(s, d, _canon(d, schy, fund="SCHY") + _canon(d, BOOK, fund="TXUE"), rev=REV_A)
    markers.write_marker(g.CANONICAL_STAGE, D2, "b1", s, {"status": "OK", "outputs": [homes.canonical_shape(D2, f"holdings-{REV_A}.parquet")]})
    r1 = g.handler_entry({"date": D2, "mode": "daily", "batch_id": "b1", "sink": spec})
    g5_prior = [u for u in r1["outputs"] if u.endswith(".parquet")][0]
    t = pq.read_table(io.BytesIO(s.get(g5_prior)))
    df = t.to_pandas()
    df.loc[df["fund_id"].astype(str) == "SCHY", "est_price"] = 999.0
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(df, preserve_index=False, schema=t.schema), buf)
    s.put(g5_prior, buf.getvalue())
    g6_pre = homes.address("rivalfunds", "etfs", "gold", "flow_reconciliation", f"date={D2}") + "/"
    g6_prior = revision.newest([u for u in s.list(g6_pre) if u.endswith(".parquet")])
    prior_g6 = pq.read_table(io.BytesIO(s.get(g6_prior))).to_pandas()

    _put_canonical(s, D2, _canon(D2, _doubled(BOOK, "S1 US Equity"), fund="SCHY") + _canon(D2, _doubled(BOOK, KEY), fund="TXUE"),
                   rev=REV_B)
    markers.write_marker(g.CANONICAL_STAGE, D2, "b2", s, {"status": "OK", "outputs": [homes.canonical_shape(D2, f"holdings-{REV_B}.parquet")]})
    ev = {"date": D2, "mode": "daily", "batch_id": "b2", "sink": spec}
    if rebuild:
        ev["rebuild_funds"] = ["TXUE"]
    r2 = g.handler_entry(ev)
    g5_pre = homes.address("rivalfunds", "etfs", "gold", "trade_schedule", f"date={D2}") + "/"
    newest5 = revision.newest([u for u in s.list(g5_pre) if u.endswith(".parquet")])
    newest6 = revision.newest([u for u in s.list(g6_pre) if u.endswith(".parquet")])
    new5 = pq.read_table(io.BytesIO(s.get(newest5))).to_pandas()
    new6 = pq.read_table(io.BytesIO(s.get(newest6))).to_pandas()
    return {"r2": r2.get("status"), "prior5": df, "new5": new5, "prior6": prior_g6, "new6": new6,
            "new5_is_prior": newest5 == g5_prior, "pd": pd}


def run(v):
    c.setup_path()
    c.offline_guards()

    def fund(df, f):
        return df[df["fund_id"].astype(str) == f].reset_index(drop=True)

    a = build(rebuild=True)
    pd = a["pd"]
    sp, sn = fund(a["prior5"], "SCHY"), fund(a["new5"], "SCHY")
    tp, tn = fund(a["prior5"], "TXUE"), fund(a["new5"], "TXUE")
    print("with rebuild_funds: stage", a["r2"], "| new object differs from prior:", not a["new5_is_prior"],
          "| SCHY rows prior/new", len(sp), len(sn), "| SCHY est_price new", sorted(set(sn["est_price"].astype(str)))[:3],
          "| TXUE rows prior/new", len(tp), len(tn))
    cols = [x for x in sp.columns if x in sn.columns]
    schy_same = len(sp) == len(sn) and len(sp) > 0 and sp[cols].astype(str).equals(sn[cols].astype(str))
    txue_changed = not (len(tp) == len(tn) and tp[cols].astype(str).equals(tn[cols].astype(str)))
    v.check((not a["new5_is_prior"]) and schy_same and txue_changed,
            "(a) rebuild_funds ['TXUE']: SCHY's prior G5 rows carried unchanged (est_price 999.0), TXUE re-inferred")
    p6, n6 = fund(a["prior6"], "SCHY"), fund(a["new6"], "SCHY")
    c6 = [x for x in p6.columns if x in n6.columns and x not in ("produced_at",)]
    v.check(len(p6) > 0 and len(p6) == len(n6) and p6[c6].astype(str).equals(n6[c6].astype(str)),
            "(b) rebuild_funds ['TXUE']: SCHY's prior G6 row carried unchanged")

    b = build(rebuild=False)
    sb = fund(b["new5"], "SCHY")
    print("control without rebuild_funds: SCHY est_price", sorted(set(sb["est_price"].astype(str)))[:3])
    v.check(len(sb) > 0 and not (sb["est_price"] == 999.0).any(), "(c) control: without the key SCHY is re-inferred")
    _ = pd


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
