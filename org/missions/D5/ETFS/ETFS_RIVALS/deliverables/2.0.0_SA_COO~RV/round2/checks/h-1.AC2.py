"""RIV-h-1 AC2 -- a PLANTED repeat: a real capture re-published under a LATER requested date (same rows, the older report
dates inside) reads status repeat on that later day with actual_report_date the older date, never new; and on a real
day the modal-date rule holds -- the fund's actual_report_date equals the MODE of its rows' REPORT_DATE."""
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    two = c.idvz_captures(3)
    base = c.capture(two[1])
    later = c.capture(two[2])["requested_date"]
    planted = pathlib.Path(c.tmpdir("rv_g22p_")) / f"{later}.json"
    planted.write_text(json.dumps({**base, "requested_date": later}), encoding="utf-8")
    sink = c.tmpdir("rv_g22_")
    c.run_idvz_chain(sink, [two[0], two[1], planted], "coverage")
    df, _ = c.read_parquets(c.gold_dir(sink, "holdings_coverage"))
    df["d"] = df["expected_date"].astype(str).str[:10]
    older = base["requested_date"]
    for fund in ("TXUE", "SCHY"):
        row = df[(df["fund_id"] == fund) & (df["d"] == later)]
        st = list(row["status"]) if len(row) else []
        ard = [str(x)[:10] for x in row["actual_report_date"]] if len(row) else []
        v.check("repeat" in st and "new" not in st, f"{fund} on {later}: {st} (repeat, never new)")
        v.check(older in ard, f"{fund} actual_report_date {ard} carries the older {older}")
    rows = base["rows"]
    hdr = rows[0]
    for fund in ("INEQ", "SCHY"):
        dates = [str(r[hdr.index("REPORT_DATE")])[:10] for r in rows[1:] if str(r[hdr.index("ORIG_IDS")]).split()[0] == fund]
        mode = collections.Counter(dates).most_common(1)[0][0]
        row = df[(df["fund_id"] == fund) & (df["d"] == older)]
        ard = [str(x)[:10] for x in row["actual_report_date"]] if len(row) else []
        v.check(mode in ard, f"{fund} on {older}: actual_report_date {ard} == modal {mode}")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
