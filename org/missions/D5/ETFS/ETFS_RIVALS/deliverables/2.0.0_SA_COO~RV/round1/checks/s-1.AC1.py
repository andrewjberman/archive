"""RIV-s-1 AC1 -- typed silver from real bronze: five archived BASG issuer days landed through RIV-c-1, replayed into
silver; one partition per REPORT date under the builder's issuer silver prefix, every source row and column kept."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

HEADER = ("date|fund_id|fund_name|fund_cusip|fund_ticker|security_group|security_type|security_number|security_cusip|"
          "security_sedol|security_isin|security_ticker|security_description|quantity|market_value|notional_value|"
          "percent_of_market_value|percent_of_net_assets").split("|")


def run(v):
    c.setup_path()
    files = c.archive_files(5)
    sink = c.tmpdir("rv_s1_")
    res = c.run_chain(sink, files, through="silver")
    print("silver:", str(res["silver"])[:500])
    v.check(res["silver"].get("status") == "OK", f"silver status OK (got {res['silver'].get('status')})")
    v.check(bool(res["silver"].get("marker")) and c.local_path(sink, res["silver"]["marker"]).exists(), "silver marker written")
    for f in files:
        d = c.archive_meta(f)["requested_date"]
        part = c.local_path(sink, c.address("issuer-site", "etfs", "silver", "holdings", f"date={d}"))
        df, n = c.read_parquets(part)
        v.check(n >= 1, f"{d}: a silver partition at date={d} ({n} part(s))")
        if n:
            missing = [h for h in HEADER if h not in df.columns]
            v.check(not missing, f"{d}: every source column kept (missing {missing})")
            v.check(len(df) == c.all_rows(f), f"{d}: every source row kept, all funds ({len(df)} == {c.all_rows(f)})")
            for col in ("bronze_uri", "sha256", "captured_at", "parser_version"):
                v.check(col in df.columns, f"{d}: lineage column {col}")
            if "quantity" in df.columns:
                v.check(str(df["quantity"].dtype).startswith("float"), f"{d}: quantity typed float ({df['quantity'].dtype})")
            if "security_cusip" in df.columns:
                v.check(df["security_cusip"].dropna().map(lambda x: isinstance(x, str)).all(), f"{d}: security_cusip typed string (leading zeros kept)")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
