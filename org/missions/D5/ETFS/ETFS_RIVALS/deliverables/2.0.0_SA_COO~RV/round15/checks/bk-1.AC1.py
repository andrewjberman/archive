"""RIV-bk-1 AC1 (PRD v0.18 FWD-22; rows ETFS_RIVALS-Z-S60 / Z-S61; changes 1 and 2 of the cell): a backfill-marked G4 row
(`as_of_source` exactly "backfill": a past date's close and nothing else) never moves the rankings and never stands in for
the day's market reference in the canonical shape.

Interface (prescribed, from the cell):
  - `gold_holding_contribution.drop_backfill(g4: DataFrame) -> DataFrame` returns the frame without the rows whose
    `as_of_source` == "backfill"; a frame with no such column is returned unchanged. `handler_entry`'s own G4 read loads
    `as_of_source` and drops those rows before anything else uses the frame, so a day's table is identical with and without
    backfill-marked rows in G4.
  - `gold_canonical_shape._g4_for(s, rd, cache)`: a partition whose rows are ALL backfill-marked is never picked (the pick
    falls back to the nearest earlier partition holding a non-backfill row), and a backfill-marked row is never used to
    fill GICS.
  Open details this check accepts both ways: (i) whether `handler_entry` calls `drop_backfill` or filters by other means
  (arm (b) reads only the written table); (ii) whether a backfill-marked row of a MIXED partition is left out of `_g4_for`'s
  `rows` or skipped inside `apply_g4` (arm (d) reads only what `apply_g4(rows, _g4_for(...))` resolves).

Fixture builders reused: `rivalfunds.tests.test_r7cg1_census_reads_rankings_gics` (`_put`, `_line`: the G1 line and the
parquet put of the one test that runs `gold_holding_contribution.handler_entry` on a `local:` sink) and the producer's own G4
row builder (`enrichment_bloomberg.market_rows` / `_market_table` / `_parquet_bytes` / `market_target_uri`, as bf-1.AC2
plants its object); the backfill partitions are built exactly as `_market_range` builds them (PX_LAST only,
`MARKET_SOURCE_HIST`, `BACKFILL_SOURCE`).
Rankings fixture, page day 2026-10-05 (as-of 2026-10-02), `universe.entries` pinned to one fund TXUE, two `local:` sinks that
differ ONLY by the planted partitions:
  G1  TXUE reports 2026-09-29, 09-30, 10-01, 10-02: XAA_US_Equity quantity 100 at market value 1000 / 1010 / 1020 / 1030
      (implied 10.0, 10.1, 10.2, 10.3: about +1% a day), YBB_US_Equity quantity 100 at 1000 throughout; weight 0.2 each.
  G4  normal: date=2026-09-29 (a legacy object with NO `as_of_source` column: XAA px_close 10.0) and date=2026-10-02
      (`as_of_source` "historical": XAA px_close 10.3, sector Information Technology; YBB total return 0.5 percent).
      So without a plant XAA's 09-30, 10-01 and 10-02 are each holding-implied (no day has a close at both ends).
  G4  planted in sink B only: date=2026-09-30 XAA px_close 11.0 and date=2026-10-01 XAA px_close 12.1, every row
      `as_of_source` "backfill". At the base they give XAA a close at both ends of all three days: +10.0%, +10.0%, -14.9%.
  - (a) `drop_backfill` exists; on a 4-row frame (backfill, historical, pull, null) it returns exactly the 3 non-backfill
    rows in order, and a frame with no `as_of_source` column comes back equal to itself;
  - (b) `handler_entry` over sink A and over sink B both return OK and the two written tables are equal on every column but
    `revision`, `produced_at`, `input_manifest` (the module's own `_content_sha` drops exactly those three; the two shas
    agree and so do the frames);
  - (c) `_g4_for` on a sink holding a normal partition 2026-09-29 (AAA US Equity, sector Information Technology) and an
    all-backfill partition 2026-10-01: for report date 2026-10-02 and for 2026-10-01 it returns the 2026-09-29 object, with
    AAA_US_Equity's sector in its rows;
  - (d) on the same sink a MIXED partition 2026-10-02 (BBB US Equity normal, sector Energy; CCC US Equity backfill-marked
    and carrying a sector, which no real backfill row does): for report date 2026-10-02 that partition is picked (it holds
    a non-backfill row) and `apply_g4` resolves BBB_US_Equity and NOT CCC_US_Equity;
  - (e) control: on sink A the table is non-empty and XAA's R30 row is priced `holding_implied` on 3 days; the two planted
    objects are in sink B, each row `as_of_source` "backfill" with a close; `_g4_for` for report date 2026-09-29 returns
    the 2026-09-29 object.
FAIL at base 0ed013f33d: (a), (b), (c), (d) FAIL (no drop_backfill; XAA reads g4_close with another contribution; the
all-backfill partition is picked; the backfill row fills GICS); (e) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

PAGE, ASOF = "2026-10-05", "2026-10-02"
ENTS = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"}]
XAA, YBB = "XAA_US_Equity", "YBB_US_Equity"
REPORTS = (("2026-09-29", 1000.0), ("2026-09-30", 1010.0), ("2026-10-01", 1020.0), ("2026-10-02", 1030.0))
PLANTS = (("2026-09-30", 11.0), ("2026-10-01", 12.1))
PROVENANCE = ("revision", "produced_at", "input_manifest")
IT = {"GICS_SECTOR_NAME": "Information Technology"}


def put_market(eb, s, date, data, tag, as_of_source, labels=None):
    """One G4 object at the producer's own address, built by the producer's own row builder. Returns its uri."""
    prov = {"revision": f"{date.replace('-', '')}T010000Z-{tag * 12}", "produced_at": f"{date}T01:00:00Z",
            "producer_version": eb.GOLD_VERSION, "input_manifest": "{}"}
    rows = eb.market_rows(data, date, eb.MARKET_SOURCE_HIST, prov, as_of_source, labels)
    uri = eb.market_target_uri(date, prov["revision"])
    s.put(uri, eb._parquet_bytes(eb._market_table(rows)), "application/octet-stream")
    return uri


def rankings_sink(name, planted):
    """The rankings fixture on a fresh `local:` sink; `planted` adds the two backfill partitions. Returns (spec, sink, uris)."""
    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import homes, sinks
    from rivalfunds.tests import test_r7cg1_census_reads_rankings_gics as t7

    spec = f"local:{c.tmpdir(f'rv_bk1_{name}_')}"
    s = sinks.get_sink(spec)
    for d, mv in REPORTS:
        t7._put(s, homes.canonical_shape(d, f"holdings-{t7.REV}.parquet"),
                [dict(t7._line("TXUE", XAA, date=d), market_value=mv), t7._line("TXUE", YBB, date=d)])
    # a legacy G4 object: no as_of_source column at all (its rows are never backfill)
    t7._put(s, eb.market_target_uri("2026-09-29", "20260929T010000Z-bbbbbbbbbbbb"),
            [{"security_id": XAA, "date": "2026-09-29", "px_close": 10.0, "gics_sector": None}])
    put_market(eb, s, ASOF, {"XAA US Equity": {"PX_LAST": 10.3, **IT}, "YBB US Equity": {"DAY_TO_DAY_TOT_RETURN_GROSS_DVDS": 0.5}},
               "c", "historical")
    uris = []
    if planted:
        for d, px in PLANTS:
            uris.append(put_market(eb, s, d, {"XAA US Equity": {"PX_LAST": px}}, "d", eb.BACKFILL_SOURCE))
    return spec, s, uris


def rankings(hc, pq, spec, s):
    """(result, table or None) of one handler_entry run; a raising stage is a failed arm, not a dead check."""
    try:
        r = hc.handler_entry({"date": PAGE, "sink": spec})
    except Exception as e:  # noqa: BLE001
        return {"status": f"RAISED {type(e).__name__}", "detail": str(e), "outputs": []}, None
    outs = r.get("outputs") or []
    return r, (pq.read_table(io.BytesIO(s.get(outs[0]))).to_pandas() if r.get("status") == "OK" and outs else None)


def xaa(df, period="R30"):
    if df is None:
        return {}
    x = df[(df.fund_id == "TXUE") & (df.axis == "security") & (df.bucket == XAA) & (df.period == period)]
    return x.iloc[0].to_dict() if len(x) == 1 else {}


def words(row):
    con = row.get("contribution")
    return (f"contribution {None if con is None else round(float(con), 6)} | price_source {row.get('price_source')} | "
            f"n_days_priced {row.get('n_days_priced')} | n_days_holding_implied {row.get('n_days_holding_implied')}")


def g4_pick(g1, s, rd):
    try:
        return g1._g4_for(s, rd, {})
    except Exception as e:  # noqa: BLE001 -- a raising pick is a failed arm
        print(f"  _g4_for({rd}) raised {type(e).__name__}: {e}")
        return None


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd
    import pyarrow.parquet as pq

    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import gold_canonical_shape as g1
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import sinks

    hc.universe.entries = lambda: list(ENTS)

    # ---- (a) drop_backfill ------------------------------------------------------------------------------------------
    frame = pd.DataFrame({"security_id": ["A", "B", "C", "D"], "px_close": [1.0, 2.0, 3.0, 4.0],
                          "as_of_source": [eb.BACKFILL_SOURCE, "historical", "pull", None]})
    bare = frame.drop(columns=["as_of_source"])
    fn = getattr(hc, "drop_backfill", None)
    kept, same = None, None
    if callable(fn):
        try:
            kept = list(fn(frame.copy())["security_id"])
            back = fn(bare.copy())
            same = list(back.columns) == list(bare.columns) and back.reset_index(drop=True).equals(bare)
        except Exception as e:  # noqa: BLE001
            print("drop_backfill raised:", type(e).__name__, e)
    print(f"drop_backfill: exists {callable(fn)} | kept of [A backfill, B historical, C pull, D null]: {kept} | a frame with no "
          f"as_of_source column unchanged: {same}")
    v.check(kept == ["B", "C", "D"] and same is True,
            "(a) drop_backfill removes exactly the backfill-marked rows and returns a frame without the column unchanged")

    # ---- (b) the rankings with and without the planted partitions ---------------------------------------------------
    spec_a, s_a, _ = rankings_sink("plain", planted=False)
    spec_b, s_b, planted = rankings_sink("planted", planted=True)
    r_a, t_a = rankings(hc, pq, spec_a, s_a)
    r_b, t_b = rankings(hc, pq, spec_b, s_b)
    sha = {k: (None if t is None else hc._content_sha(t)) for k, t in (("plain", t_a), ("planted", t_b))}
    body = {k: (None if t is None else t.drop(columns=list(PROVENANCE), errors="ignore").reset_index(drop=True))
            for k, t in (("plain", t_a), ("planted", t_b))}
    equal = body["plain"] is not None and body["planted"] is not None and body["plain"].equals(body["planted"])
    print(f"rankings without the plant: status {r_a.get('status')} | rows {None if t_a is None else len(t_a)} | sha {sha['plain']}")
    print(f"rankings with the plant:    status {r_b.get('status')} | rows {None if t_b is None else len(t_b)} | sha {sha['planted']}")
    for p in ("R30", "MTD"):
        print(f"  XAA {p} without: {words(xaa(t_a, p))}")
        print(f"  XAA {p} with:    {words(xaa(t_b, p))}")
    print(f"tables equal on every column but {PROVENANCE}: {equal}")
    v.check(r_a.get("status") == "OK" and r_b.get("status") == "OK" and equal and sha["plain"] == sha["planted"],
            "(b) the day's holding_contribution table is identical with and without backfill-marked G4 partitions")

    # ---- (c), (d) the canonical shape's G4 pick ---------------------------------------------------------------------
    s = sinks.get_sink(f"local:{c.tmpdir('rv_bk1_pick_')}")
    normal = put_market(eb, s, "2026-09-29", {"AAA US Equity": {"PX_LAST": 5.0, "CRNCY": "USD", **IT}}, "a", "historical")
    backfill = put_market(eb, s, "2026-10-01", {"AAA US Equity": {"PX_LAST": 6.0}}, "b", eb.BACKFILL_SOURCE)
    picks = {rd: g4_pick(g1, s, rd) for rd in ("2026-10-02", "2026-10-01", "2026-09-29")}
    for rd, g in picks.items():
        row = ((g or {}).get("rows") or {}).get("AAA_US_Equity") or {}
        print(f"_g4_for({rd}): date {(g or {}).get('date')} | object {str((g or {}).get('uri')).rsplit('/', 1)[-1]} | "
              f"AAA sector {row.get('gics_sector')!r} | AAA as_of_source {row.get('as_of_source')!r}")

    def is_normal(g):
        return bool(g) and g.get("date") == "2026-09-29" and g.get("uri") == normal and (
            (g.get("rows") or {}).get("AAA_US_Equity") or {}).get("gics_sector") == "Information Technology"

    v.check(is_normal(picks["2026-10-02"]) and is_normal(picks["2026-10-01"]),
            "(c) an all-backfill partition is never picked: the nearest earlier partition holding a non-backfill row is")

    mixed = put_market(eb, s, "2026-10-02", {"BBB US Equity": {"PX_LAST": 7.0, "GICS_SECTOR_NAME": "Energy"},
                                              "CCC US Equity": {"PX_LAST": 8.0, "GICS_SECTOR_NAME": "Utilities"}}, "e", "historical",
                       labels={"CCC US Equity": (pd.Timestamp("2026-10-02").date(), eb.BACKFILL_SOURCE, eb.MARKET_SOURCE_HIST)})
    g = g4_pick(g1, s, "2026-10-02")
    rows = [{"security_id": k, "is_cash_line": False, "asset_class": None} for k in ("BBB_US_Equity", "CCC_US_Equity")]
    try:
        n = g1.apply_g4(rows, g)
    except Exception as e:  # noqa: BLE001
        print("apply_g4 raised:", type(e).__name__, e)
        n = None
    got = {r["security_id"]: (r.get("gics_status"), r.get("gics_sector")) for r in rows}
    print(f"mixed partition 2026-10-02: picked date {(g or {}).get('date')} object {str((g or {}).get('uri')).rsplit('/', 1)[-1]} | "
          f"apply_g4 resolved {n} | {got}")
    v.check(bool(g) and g.get("uri") == mixed and n == 1 and got["BBB_US_Equity"] == ("RESOLVED", "Energy")
            and got["CCC_US_Equity"] == (None, None),
            "(d) a partition holding a non-backfill row is picked, and its backfill-marked row never fills GICS")

    # ---- (e) control ------------------------------------------------------------------------------------------------
    base = xaa(t_a)
    marks = {}
    for u in planted:
        df = pq.read_table(io.BytesIO(s_b.get(u))).to_pandas() if s_b.exists(u) else None
        marks[u.split("date=")[1][:10]] = None if df is None else (sorted(set(df["as_of_source"].astype(str))),
                                                                    int(df["px_close"].notna().sum()), len(df))
    back_ok = pq.read_table(io.BytesIO(s.get(backfill))).to_pandas()["as_of_source"].tolist() == [eb.BACKFILL_SOURCE]
    print(f"control: table rows {None if t_a is None else len(t_a)} | XAA R30 {words(base)} | planted objects "
          f"(as_of_source, closes, rows) {marks} | the pick fixture's 2026-10-01 object all backfill: {back_ok}")
    v.check(t_a is not None and len(t_a) > 0 and base.get("price_source") == "holding_implied"
            and base.get("n_days_holding_implied") == 3 and len(marks) == 2
            and all(m == ([eb.BACKFILL_SOURCE], 1, 1) for m in marks.values()) and back_ok and is_normal(picks["2026-09-29"]),
            "(e) control: without the plant XAA is holding-implied on its 3 days, the planted objects are in the sink and "
            "marked backfill, and _g4_for picks a normal partition of its own report date")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
