"""RIV-s-4 AC1 -- G4 `security_market` lands GICS from REAL Bloomberg responses (C-GOLD-MODEL G4; analysis ruling 5).

Real data: the Positioning pull's s3://opal-data-etfs/bbg/2026-09-29/characteristics.parquet (Bloomberg BDP responses:
security, NAME, GICS_SECTOR_NAME, GICS_INDUSTRY_GROUP_NAME, GICS_INDUSTRY_GROUP) is copied READ-ONLY to a local file and
imported with enrichment_bloomberg mode 'import-market' at date 2026-09-29. Then G4 at
address('rivalfunds','etfs','gold','security_market','date=2026-09-29') holds:
  - one row per distinct input security (the denominator is printed);
  - security_id in the crosswalk key grammar (spaces -> underscores, e.g. 'AAPL US Equity' -> 'AAPL_US_Equity') and the
    raw form kept in security_bloomberg;
  - gics_sector and gics_industry_group populated on exactly the rows whose input carries them, with gics_industry_group_code
    the 4-digit code;
  - the C-GOLD-MODEL columns revision, produced_at, producer_version, input_manifest, and claim = 'MEASURED' on every row."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D = "2026-09-29"


def run(v):
    c.setup_path()
    import pandas as pd
    from rivalfunds import enrichment_bloomberg

    sink = c.tmpdir("rv_s4a_")
    src = c.mirror_s3(sink, c.CHARACTERISTICS_FMT.format(d=D))
    inp = pd.read_parquet(src)
    n_in = inp["security"].astype(str).nunique()
    n_gics = int(inp.groupby("security")["GICS_SECTOR_NAME"].first().notna().sum())
    print(f"input: {n_in} distinct securities, {n_gics} with GICS_SECTOR_NAME")
    r = enrichment_bloomberg.handler_entry({"mode": "import-market", "characteristics": str(src), "date": D,
                                            "batch_id": "s4-imp", "sink": f"local:{sink}"})
    print("import-market:", str(r)[:300])
    df, n = c.read_parquets(c.gold_dir(sink, "security_market") / f"date={D}")
    v.check(n >= 1 and len(df) == n_in, f"G4 rows {len(df)} == distinct input securities {n_in}")
    if not len(df):
        return
    v.check(all(str(a) == str(b).replace(" ", "_") for a, b in zip(df["security_id"], df["security_bloomberg"])),
            "security_id is the key grammar of security_bloomberg on every row")
    v.check(int(df["gics_sector"].notna().sum()) == n_gics, f"gics_sector populated on {int(df['gics_sector'].notna().sum())} of {n_gics}")
    codes = df["gics_industry_group_code"].dropna().astype(str)
    v.check(len(codes) > 0 and all(len(x.split(".")[0]) == 4 for x in codes), "gics_industry_group_code is the 4-digit code")
    need = {"revision", "produced_at", "producer_version", "input_manifest", "claim"}
    v.check(need <= set(df.columns) and set(df["claim"].astype(str)) == {"MEASURED"},
            f"C-GOLD-MODEL columns present, claim MEASURED ({sorted(need - set(df.columns))})")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
