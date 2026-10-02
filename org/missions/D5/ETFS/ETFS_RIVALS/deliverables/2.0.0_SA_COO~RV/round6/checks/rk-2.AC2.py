"""RIV-rk-2 AC2 (CRO~RV CALL 13 C1 (b), PROVISIONAL): a fund x period holding a single security with |contribution| above
`contribution_single_holding_bound` (guardrails_config.json, value 0.25, status PROVISIONAL) is REFUSED as ONE row: axis
"refused", bucket "single_holding_above_bound", contribution = that holding's value. A holding at 0.24 passes.
Interface: `gold_holding_contribution.plausibility_guard(df, bounds=None) -> df`; the bound is read through
`guardrails.load_config()`."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    import pandas as pd

    from rivalfunds import gold_holding_contribution as g
    from rivalfunds import guardrails

    cfg = guardrails.load_config().get("contribution_single_holding_bound") or {}
    print("config entry:", cfg)
    v.check(float(cfg.get("value", -1)) == 0.25 and str(cfg.get("status")) == "PROVISIONAL",
            "guardrails_config carries contribution_single_holding_bound = 0.25, PROVISIONAL")
    df = pd.DataFrame(c.contribution_rows("BASG", "MTD", {"X": 0.31, "Y": 0.01})
                      + c.contribution_rows("PCLG", "MTD", {"Z": 0.24, "W": -0.02}))
    out = g.plausibility_guard(df)
    b = out[(out["fund_id"] == "BASG") & (out["period"] == "MTD")]
    print("BASG MTD:", b[["axis", "bucket", "contribution"]].values.tolist())
    v.check(len(b) == 1 and str(b.iloc[0]["axis"]) == "refused" and str(b.iloc[0]["bucket"]) == "single_holding_above_bound"
            and abs(float(b.iloc[0]["contribution"]) - 0.31) < 1e-9,
            "a 0.31 single holding refuses its fund x period, naming bound (b) and the holding's value")
    p = out[(out["fund_id"] == "PCLG") & (out["period"] == "MTD")]
    v.check(len(p) == 2 and set(p["axis"].astype(str)) == {"security"}, "control: a 0.24 holding passes")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
