"""RIV-b-1 AC2 -- Bloomberg silver types every row of every fund: after importing two real captures and replaying
build-bloomberg-silver, silver for the newest report date holds, per fund, exactly the capture's row count (all six IDVZ-group
funds), every capture column is kept, and a second replay adds no rows."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    files = c.idvz_captures(2)
    newest = files[-1]
    sink = c.tmpdir("rv_b1s_")
    c.import_bloomberg(sink, files)
    date = c.capture(newest)["requested_date"]
    r1 = c.replay("silver_bloomberg", sink, date)
    print("r1:", str(r1)[:300])
    root = c.local_path(sink, c.address("bloomberg", "etfs", "silver", "holdings", "date=")).parent
    df, n = c.read_parquets(root / f"date={date}")
    v.check(n >= 1, f"silver objects for report date {date}: {n}")
    fund_col = next((k for k in ("fund_ticker", "fund_id", "fund") if k in df.columns), None)
    v.check(fund_col is not None, f"a fund column exists ({list(df.columns)[:12]})")
    if fund_col:
        got = df.groupby(fund_col).size().to_dict()
        want = c.capture_rows_by_fund(newest)
        v.check(sorted(got) == sorted(want), f"funds {sorted(got)} == {sorted(want)}")
        v.check(all(got.get(k) == want[k] for k in want), f"rows per fund {got} == capture {want}")
    hdr = c.capture(newest)["rows"][0]
    lower = {str(col).lower() for col in df.columns}
    kept = [h for h in hdr if h != "id()" and (h.lower() in lower or h.lower().replace("_", "") in {x.replace("_", "") for x in lower})]
    v.check(len(kept) == len([h for h in hdr if h != "id()"]), f"every capture column kept ({len(kept)} of {len(hdr) - 1})")
    c.replay("silver_bloomberg", sink, date, batch_id="chk-2")
    df2, _ = c.read_parquets(root / f"date={date}")
    v.check(len(df2) == len(df), f"second replay adds no rows ({len(df)} -> {len(df2)})")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
