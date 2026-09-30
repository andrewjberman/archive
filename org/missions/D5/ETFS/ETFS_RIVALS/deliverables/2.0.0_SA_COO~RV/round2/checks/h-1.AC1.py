"""RIV-h-1 AC1 -- holdings_coverage over REAL captures with a PLANTED gap: import the last 5 IDVZ-group captures EXCEPT the
middle one; G2 then reads, for each rival, status new on the 4 captured days and gap on the skipped trading day; every row
carries row_count, weight_sum, selected and selection_reason; keying is the modal report date (a lingering older-dated
0%-weight line never turns a fresh day into repeat)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    five = c.idvz_captures(5)
    skipped = c.capture(five[2])["requested_date"]
    files = five[:2] + five[3:]
    sink = c.tmpdir("rv_g21_")
    res = c.run_idvz_chain(sink, files, "coverage")
    print("coverage:", str(res.get("coverage"))[:300])
    df, n = c.read_parquets(c.gold_dir(sink, "holdings_coverage"))
    v.check(n >= 1 and len(df) > 0, f"G2 objects {n}, rows {len(df)}")
    for col in ["fund_id", "expected_date", "source", "actual_report_date", "status", "row_count", "weight_sum", "selected",
                "selection_reason"]:
        v.check(col in df.columns, f"column {col}")
    if not {"fund_id", "expected_date", "status"} <= set(df.columns):
        return
    df["d"] = df["expected_date"].astype(str).str[:10]
    captured = [c.capture(f)["requested_date"] for f in files]
    for fund in c.IDVZ_GROUP[1:]:
        sub = df[(df["fund_id"] == fund) & (df.get("selected", True) == True)]  # noqa: E712
        st = dict(zip(sub["d"], sub["status"]))
        v.check(all(st.get(d) == "new" for d in captured[1:]), f"{fund}: new on captured days {[st.get(d) for d in captured[1:]]}")
        v.check(st.get(skipped) == "gap", f"{fund}: gap on the skipped day {skipped} ({st.get(skipped)})")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
