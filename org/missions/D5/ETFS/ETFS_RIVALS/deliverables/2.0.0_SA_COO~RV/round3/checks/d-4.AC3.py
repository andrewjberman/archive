"""RIV-d-4 AC3 (live, READ-ONLY) -- the served canonical_shape at the act's newest report date carries resolved
identity at or above the MEASURED floor, and GICS from a served G4.

Reads d4_live.json `newest_report_date` and `identity_floor` (the value RIV-d-4 set in the publisher's identity_coverage
threshold, from RIV-i-1's measured fraction); then the newest G1 object at that date and the newest G4 object at or before it."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _live as L  # noqa: E402


def run(v):
    rec = L.record()
    rd, floor = rec.get("newest_report_date"), rec.get("identity_floor")
    key, g1 = L.latest_parquet(f"rivalfunds/etfs/gold/canonical_shape/date={rd}/")
    v.check(g1 is not None and isinstance(floor, (int, float)) and 0 < floor <= 1, f"G1 {key} and a numeric floor {floor!r}")
    if g1 is None:
        return
    nc = g1[~g1["is_cash_line"].astype(bool)]
    for f, g in nc.groupby(nc["fund_ticker"].astype(str).str.strip()):
        frac = float((g["resolution_status"] == "RESOLVED").mean())
        print(f"  {f}: {frac:.3f} resolved of {len(g)}")
        v.check(frac >= float(floor or 1), f"{f}: resolved {frac:.3f} >= floor {floor}")
    g4 = sorted(k for k in L.keys("rivalfunds/etfs/gold/security_market/") if k.endswith(".parquet")
                and k.split("date=")[1][:10] <= rd)
    v.check(len(g4) > 0, f"a served G4 object at or before {rd} ({len(g4)})")
    v.check(int((g1["gics_status"].astype(str) == "RESOLVED").sum()) > 0, "G1 carries RESOLVED GICS rows")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
