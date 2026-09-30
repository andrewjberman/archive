"""RIV-g-1 AC1 -- canonical_shape from real silver: five archived BASG days through c-1 and s-1, then the master
shape. BASG positions only, every one of them (cash and unidentified included), unique on the grain, the classification
and GICS fields present and separate, GICS absent with a status (round 1 has no GICS source), unmapped source fields kept."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

REQUIRED = ["fund_id", "fund_ticker", "report_date", "snapshot_id", "position_id", "security_id", "raw_identifier",
            "resolution_status", "quantity", "market_value", "weight", "position_type", "asset_class",
            "sub_asset_class", "sub_asset_class_status", "gics_sector", "gics_industry_group", "gics_industry",
            "gics_sub_industry", "gics_status", "extra_attributes", "source_channel", "bronze_uri", "sha256"]


def run(v):
    c.setup_path()
    files = c.archive_files(5)
    sink = c.tmpdir("rv_g1_")
    res = c.run_chain(sink, files, through="canonical")
    print("canonical:", str(res["canonical"])[:500])
    v.check(res["canonical"].get("status") == "OK", f"canonical status OK (got {res['canonical'].get('status')})")
    for f in files:
        d = c.archive_meta(f)["requested_date"]
        part = c.local_path(sink, c.address("rivalfunds", "etfs", "gold", "canonical_shape", f"date={d}"))
        df, n = c.read_parquets(part)
        v.check(n >= 1, f"{d}: canonical_shape partition at date={d}")
        if not n:
            continue
        missing = [k for k in REQUIRED if k not in df.columns]
        v.check(not missing, f"{d}: required columns present (missing {missing})")
        if missing:
            continue
        v.check(set(df["fund_ticker"]) == {"BASG"}, f"{d}: BASG only ({sorted(set(df['fund_ticker']))})")
        v.check(len(df) == c.basg_rows(f), f"{d}: every BASG position kept ({len(df)} == {c.basg_rows(f)})")
        v.check(not df.duplicated(["fund_id", "snapshot_id", "position_id"]).any(), f"{d}: unique on (fund_id, snapshot_id, position_id)")
        cash = df[df["position_type"].astype(str).str.lower() == "cash"]
        v.check(len(cash) >= 1 and set(cash["asset_class"]) <= {"Cash", "Fixed Income"}, f"{d}: cash rows visible with a vocabulary cash class ({len(cash)} row(s))")
        v.check(df["gics_sector"].isna().all() and (df["gics_status"] == "UNRESOLVED").all(), f"{d}: GICS null with status UNRESOLVED on every row")
        eq = df[df["asset_class"] == "Equity"]
        v.check(eq["sub_asset_class"].isna().all() and (eq["sub_asset_class_status"] == "UNRESOLVED").all(),
                f"{d}: equity sub_asset_class null with status UNRESOLVED ({len(eq)} equity rows)")
        v.check(set(df["resolution_status"]) <= {"RESOLVED", "UNRESOLVED"}, f"{d}: resolution_status in RESOLVED/UNRESOLVED")
        unres = df[df["resolution_status"] == "UNRESOLVED"]
        v.check(unres["security_id"].isna().all() and unres["raw_identifier"].notna().all(), f"{d}: an UNRESOLVED row carries no key and keeps its raw identifier")
        ea = df["extra_attributes"].dropna().map(lambda s: json.loads(s) if isinstance(s, str) else s)
        v.check(len(ea) == len(df) and any("security_number" in json.dumps(x) for x in ea), f"{d}: extra_attributes kept, carrying an unmapped source field (security_number)")
        print(f"{d}: rows {len(df)} resolved {int((df['resolution_status'] == 'RESOLVED').sum())} unresolved {len(unres)}")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
