"""RIV-ui-1 AC3 (RFW-U15, console clean): no SVG shape on the page carries a negative width or height. A bar drawn from a
signed value clamps at zero: a negative weight (an overdrawn cash line, a short) draws no bar, never a negative one.
INTERFACE: `render._svg_bars(before, after, wmax)` (the weight bars of the trade log and the holdings list) and
`render._holdings_section(ctx)`; the whole published page is swept for `<rect>` width/height attributes.

Offline:
  - `_svg_bars(-0.005, -0.004, 0.09)`: every <rect> width >= 0 (today -5.0 and -4.0);
  - the holdings list of a fund whose cash line weighs -0.0005 against a 9% top holding (the walker's -0.5): every
    <rect> width >= 0;
  - control: `_svg_bars(0.045, 0.09, 0.09)` still draws widths 45.0 and 90.0;
  - control: the round-5 page fixture plus a TXUE ranking and trend (`_ui.publish_with`) publishes, and no <rect> on it
    has a negative width or height (this sweep also covers any new chart the round adds)."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402


def _dims(html):
    out = []
    for tag in re.findall(r"<rect\b[^>]*>", html, re.I):
        for k, val in re.findall(r'\b(width|height)="([^"]*)"', tag, re.I):
            try:
                out.append((k, float(val)))
            except ValueError:
                out.append((k, float("nan")))
    return out


def _negative(html):
    return [(k, x) for k, x in _dims(html) if not x >= 0]


def run(v):
    c.setup_path()
    import pandas as pd

    from rivalfunds import render

    neg = render._svg_bars(-0.005, -0.004, 0.09)
    print("negative weights:", neg)
    v.check(not _negative(neg), f"_svg_bars clamps a negative weight at zero (negative dims: {_negative(neg)})")

    rows = [
        {
            "security_name": "Cash",
            "raw_identifier": "USD Curncy",
            "raw_identifier_kind": None,
            "position_type": "cash",
            "asset_class": "Cash",
            "quantity": -500.0,
            "market_value": -500.0,
            "weight": -0.0005,
            "resolution_status": "UNRESOLVED",
        },
        {
            "security_name": "Top Holding",
            "raw_identifier": "TOP1",
            "raw_identifier_kind": "cusip",
            "position_type": "long",
            "asset_class": "Equity",
            "quantity": 900.0,
            "market_value": 90000.0,
            "weight": 0.09,
            "resolution_status": "RESOLVED",
        },
    ]
    f = dict(u.fund_view("TXUE"), holdings=pd.DataFrame(rows))
    hold = render._holdings_section(u.page_ctx([f]))
    print("holdings rect dims:", _dims(hold))
    v.check(
        bool(_dims(hold)) and not _negative(hold),
        f"the holdings list draws no negative bar for a -0.05% cash line (negative dims: {_negative(hold)})",
    )

    pos = render._svg_bars(0.045, 0.09, 0.09)
    widths = [x for k, x in _dims(pos) if k.lower() == "width"]
    v.check(widths == [45.0, 90.0], f"control: positive weights still scale to the page maximum ({widths})")

    hc = u.hc_rows("TXUE", "MTD", {"S1": 0.012, "S2": -0.004}, {"Energy": 0.008, "Industrials": -0.002})
    bt = [
        {
            "fund_id": "TXUE",
            "role": "rival",
            "window_start": "2026-01-02",
            "window_end": u.PAGE_DAY,
            "n_trading_days": 188,
            "axis": "security",
            "bucket": "S1",
            "security_name": "Name S1",
            "net_notional_base": -2500000.0,
            "gross_notional_base": 2500000.0,
            "n_windows": 3,
            "lean": "away",
            "rank": 1,
            "reading": "tilt",
            "trend_mark": ". . 0 - - 0 + 0 0",
            "n_refused_windows": 0,
            "claim": "INFERRED",
            "revision": "fx",
        }
    ]
    r, html = u.publish_with({"holding_contribution": hc, "buying_trend": bt})
    print("publish:", r.get("status"), "| bytes", len(html), "| rect dims swept:", len(_dims(html)))
    v.check(
        r.get("status") == "OK" and bool(html) and not _negative(html),
        f"control: the published fixture page carries no negative SVG width or height ({_negative(html)[:6]})",
    )


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
