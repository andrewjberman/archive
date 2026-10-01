"""RIV-g-6 AC1 -- canonical_shape carries GICS from G4 and, for an equity row, sub_asset_class IS its GICS sector
(C-SHAPES v0.7; analysis ruling 5; row S1 reading (a)).

Real data: the 2 newest BASG issuer days and the PFOE-group captures for the same dates run to silver; G4 is imported from
the Positioning pull's REAL s3://opal-data-etfs/bbg/2026-09-28/characteristics.parquet (copied READ-ONLY) at date
2026-09-28 (enrichment_bloomberg 'import-market'); canonical_shape for 2026-09-28 then shows:
  - every non-cash row whose security_id is in G4: gics_sector, gics_industry_group and gics_industry_group_code equal to
    G4's, gics_status 'RESOLVED', gics_source naming the G4 revision -- and at least 40 such rows across BASG and the four
    Bloomberg-sourced PFOE rivals (measured at the cut: 13 + 5 + 15 + 14 + 19 = 66 ids overlap);
  - every equity row with gics_status RESOLVED: sub_asset_class == gics_sector, sub_asset_class_status 'RESOLVED';
  - no row's sub_asset_class equals a FINER GICS level (industry group, industry, sub-industry) unless it equals the sector;
  - control: a non-cash equity row whose key is NOT in G4 keeps gics_status and sub_asset_class_status 'UNRESOLVED'."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D0, D1 = "2026-09-25", "2026-09-28"
FUNDS = ("BASG", "WCMG", "TSEL", "ETFT", "PCLG")


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg

    sink = c.tmpdir("rv_g6a_")
    c.land(sink, c.archive_files(2))
    c.replay("silver_issuer", sink, D1)
    c.import_bloomberg(sink, [c.pfoe_capture(D0), c.pfoe_capture(D1)], batch_id="g6-imp")
    c.replay("silver_bloomberg", sink, D1)
    src = c.mirror_s3(sink, c.CHARACTERISTICS_FMT.format(d=D1))
    enrichment_bloomberg.handler_entry({"mode": "import-market", "characteristics": str(src), "date": D1,
                                        "batch_id": "g6-g4", "sink": f"local:{sink}"})
    g4, _ = c.read_parquets(c.gold_dir(sink, "security_market") / f"date={D1}")
    c.replay("gold_canonical_shape", sink, D1, batch_id="g6-g1")
    df, _ = c.read_parquets(c.gold_dir(sink, "canonical_shape") / f"date={D1}")
    latest = df[df["dataset_revision"] == df["dataset_revision"].max()]
    latest = latest[latest["fund_ticker"].astype(str).str.strip().isin(FUNDS) & ~latest["is_cash_line"].astype(bool)]
    if not len(g4):
        v.check(False, "G4 imported (0 rows)")
        return
    g4i = g4.set_index("security_id")
    inn = latest[latest["security_id"].astype(str).isin(set(g4i.index.astype(str)))]
    print(f"G1 non-cash rows {len(latest)}; with a key in G4: {len(inn)}")
    v.check(len(inn) >= 40, f"at least 40 G1 rows keyed into G4 ({len(inn)})")
    bad = [k for k, r in inn.iterrows()
           if not (str(r.get("gics_status")) == "RESOLVED"
                   and str(r.get("gics_sector")) == str(g4i.loc[r["security_id"], "gics_sector"])
                   and str(r.get("gics_industry_group")) == str(g4i.loc[r["security_id"], "gics_industry_group"])
                   and str(g4i.loc[r["security_id"], "revision"]) in str(r.get("gics_source")))]
    v.check(len(inn) > 0 and not bad, f"GICS fields equal G4's, RESOLVED, sourced to the G4 revision ({len(bad)} bad)")
    eq = latest[(latest["asset_class"].astype(str) == "Equity") & (latest["gics_status"].astype(str) == "RESOLVED")]
    agree = (eq["sub_asset_class"].astype(str) == eq["gics_sector"].astype(str)) & (eq["sub_asset_class_status"] == "RESOLVED")
    v.check(len(eq) > 0 and bool(agree.all()), f"equity sub_asset_class == gics_sector on all {len(eq)} resolved rows")
    finer = latest[(latest["sub_asset_class"].notna())
                   & (latest["sub_asset_class"].astype(str) != latest["gics_sector"].astype(str))
                   & (latest["sub_asset_class"].astype(str).isin(set(latest["gics_industry_group"].dropna().astype(str))
                                                                 | set(latest["gics_industry"].dropna().astype(str))
                                                                 | set(latest["gics_sub_industry"].dropna().astype(str))))]
    v.check(len(finer) == 0, f"no finer GICS level stands in a sub_asset_class ({len(finer)})")
    out = latest[(latest["asset_class"].astype(str) == "Equity")
                 & ~latest["security_id"].astype(str).isin(set(g4i.index.astype(str)))]
    v.check(len(out) > 0 and set(out["gics_status"].astype(str)) == {"UNRESOLVED"}
            and set(out["sub_asset_class_status"].astype(str)) == {"UNRESOLVED"},
            f"control: {len(out)} equity rows outside G4 stay UNRESOLVED")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
