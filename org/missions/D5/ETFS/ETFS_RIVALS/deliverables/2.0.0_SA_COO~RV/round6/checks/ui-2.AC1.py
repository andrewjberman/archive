"""RIV-ui-2 AC1 (RFW-U03, portal/DESIGN.md C12 one designed EMPTY state per panel): a fund x period with 0 ranked
holdings renders ONE empty-state line carrying its reason and the count of holdings without a price, and no table shell.
Folds rk-2 AC3 (the refused display) as the panel's third state: ranked, empty and refused are mutually exclusive.
INTERFACE: `render._rank_panel(ctx, f, period)`. The empty state is ONE element carrying `data-empty-state`; the refused
state keeps `data-refused="<bucket>"` and the words "Rankings refused" (rk-2 AC3, unchanged).

Pure, offline fixture (day 2026-10-02):
  - IDVZ MTD: 3 security rows and 1 sector row, every contribution and rank null, n_ranked 0, n_missing 3 (the shape
    gold_holding_contribution writes for a period with no priced holding): exactly one `data-empty-state` element, no
    `<table`, and the empty-state text carries the count 3;
  - ETFT YTD: one refused row (total_below_minus_100pct): `data-refused`, "Rankings refused", no `<table`, no
    `data-empty-state`;
  - control: TXUE YTD with 2 ranked holdings renders its tables and no `data-empty-state`."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import render

    empty = u.hc_rows("IDVZ", "MTD", {"A1": 0.0, "A2": 0.0, "A3": 0.0}, {"Energy": 0.0}, priced=False, end="2026-10-02")
    refused = {
        "fund_id": "ETFT",
        "role": "rival",
        "period": "YTD",
        "period_start": "2026-01-02",
        "period_end": "2026-10-01",
        "axis": "refused",
        "bucket": "total_below_minus_100pct",
        "security_name": None,
        "contribution": -1.88,
        "price_coverage": None,
        "n_days_priced": None,
        "n_days_period": None,
        "rank_best": None,
        "rank_worst": None,
        "n_ranked": None,
        "n_missing": None,
        "claim": "INFERRED",
        "revision": "fx",
    }
    ranked = c.contribution_rows("TXUE", "YTD", {"C": 0.03, "D": -0.02})
    ctx = {"day": "2026-10-02", "a1": {"holding_contribution": empty + [refused] + ranked}}

    html = render._rank_panel(ctx, {"fund": "IDVZ", "role": "home"}, "MTD")
    root = u.parse(html)
    es = root.all("data-empty-state")
    print("IDVZ MTD text:", u.text(root)[:400])
    print("IDVZ MTD: data-empty-state elements", len(es), "| <table count", html.count("<table"))
    v.check(
        len(es) == 1 and "<table" not in html, "a 0-ranked fund x period renders ONE empty-state element and no table"
    )
    v.check(
        len(es) == 1 and bool(re.search(r"\b3\b", u.text(es[0]))),
        "the empty-state line carries the count of holdings without a price (3)",
    )

    try:
        ref = render._rank_panel(ctx, {"fund": "ETFT", "role": "rival"}, "YTD")
    except Exception as e:  # noqa: BLE001 -- a refused-only panel raises today; the control still runs
        ref = f"raised {type(e).__name__}: {e}"
    print("ETFT YTD panel:", ref[:240])
    v.check(
        'data-refused="total_below_minus_100pct"' in ref
        and "Rankings refused" in ref
        and "<table" not in ref
        and "data-empty-state" not in ref,
        "a refused fund x period shows its refused state: no table, no empty state",
    )

    ctrl = render._rank_panel(ctx, {"fund": "TXUE", "role": "rival"}, "YTD")
    v.check("<table" in ctrl and "data-empty-state" not in ctrl, "control: a ranked fund x period renders its tables")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
