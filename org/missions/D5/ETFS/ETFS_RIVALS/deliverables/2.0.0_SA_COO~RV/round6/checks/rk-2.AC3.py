"""RIV-rk-2 AC3: the page shows a refused fund x period IN PLACE of its ranking panel. `render._rank_panel` reads the refused row
and renders "Rankings refused" with the bound's name, marked `data-refused="<bucket>"`; it renders no ranking table for it.
A fund x period without a refused row renders its tables as before (control)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import render

    refused = {"fund_id": "ETFT", "role": "rival", "period": "YTD", "period_start": "2026-01-02", "period_end": "2026-10-01",
               "axis": "refused", "bucket": "total_below_minus_100pct", "security_name": None, "contribution": -1.88,
               "price_coverage": None, "n_days_priced": None, "n_days_period": None, "rank_best": None, "rank_worst": None,
               "n_ranked": None, "n_missing": None, "claim": "INFERRED", "revision": "fx"}
    ok_rows = c.contribution_rows("TXUE", "YTD", {"C": 0.03, "D": 0.02})
    ctx = {"day": "2026-10-02", "a1": {"holding_contribution": [refused] + ok_rows}}
    html = render._rank_panel(ctx, {"fund": "ETFT", "role": "rival"}, "YTD")
    print("ETFT YTD panel:", html[:300])
    v.check('data-refused="total_below_minus_100pct"' in html and "Rankings refused" in html and "<table" not in html,
            "a refused fund x period shows 'Rankings refused' with its bound, and no ranking table")
    ctrl = render._rank_panel(ctx, {"fund": "TXUE", "role": "rival"}, "YTD")
    v.check("data-refused" not in ctrl and "<table" in ctrl, "control: TXUE YTD renders its tables")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
