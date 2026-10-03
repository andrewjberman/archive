"""RIV-rk-2 AC1 (CRO~RV CALL 13 C1 (a), as amended @6e3c94774a): a fund x period whose security-axis total is below -100% is
REFUSED. Its rows give way to ONE row (axis "refused", bucket "total_below_minus_100pct", contribution = the total), and every
other fund x period passes untouched.
Interface: `gold_holding_contribution.plausibility_guard(df, bounds=None) -> df`.

Fixture: ETFT YTD planted at -1.88 (grade 2's F1 figure), spread over 8 holdings of -0.235 so no single holding crosses (b);
TXUE YTD at +0.05.
Control (READ-ONLY S3): the served 2026-10-02 holding_contribution through the guard refuses nothing (measured 14:2xZ: lowest
total -4.9%, largest holding 3.6%)."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    import pandas as pd

    from rivalfunds import gold_holding_contribution as g

    planted = c.contribution_rows("ETFT", "YTD", {f"S{i}": -0.235 for i in range(1, 9)})
    keep = c.contribution_rows("TXUE", "YTD", {"C": 0.03, "D": 0.02})
    out = g.plausibility_guard(pd.DataFrame(planted + keep))
    e = out[(out["fund_id"] == "ETFT") & (out["period"] == "YTD")]
    print("ETFT YTD after the guard:", e[["axis", "bucket", "contribution"]].values.tolist())
    v.check(len(e) == 1 and str(e.iloc[0]["axis"]) == "refused" and str(e.iloc[0]["bucket"]) == "total_below_minus_100pct"
            and abs(float(e.iloc[0]["contribution"]) + 1.88) < 1e-9,
            "the planted -188% fund x period is ONE refused row naming bound (a) and carrying the total")
    t = out[(out["fund_id"] == "TXUE") & (out["period"] == "YTD")].sort_values("bucket")
    v.check(t[["axis", "bucket", "contribution"]].values.tolist() == [["security", "C", 0.03], ["security", "D", 0.02]],
            "control: TXUE YTD passes untouched")

    from rivalfunds import homes, revision, sinks
    s = sinks.get_sink("s3")
    us = [u for u in s.list(homes.address("rivalfunds", "etfs", "gold", "holding_contribution", "date=2026-10-02") + "/")
          if u.endswith(".parquet")]
    served = pd.read_parquet(io.BytesIO(s.get(revision.newest(us))))
    guarded = g.plausibility_guard(served)
    n_ref = int((guarded["axis"].astype(str) == "refused").sum())
    print("served 2026-10-02:", len(served), "rows ->", len(guarded), "| refused rows:", n_ref)
    v.check(n_ref == 0 and len(guarded) == len(served), "control: the served 2026-10-02 table refuses nothing")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
