"""RIV-ui-2 AC3 (RFW-U02 default half, DESIGN.md C14): the page opens on the SHORTEST period that ranks at least one
holding for the opening fund, not on a fixed Month to date. When no period ranks, Month to date stays the default.
INTERFACE: the global period radios stay `rf-period-MTD|QTD|YTD` (round-5 pg-1); exactly one is `checked`, and it is the
opening fund's default: the first of MTD, QTD, YTD whose security rows carry n_ranked >= 1, else MTD.

Offline: `_ui.publish_with` (the round-5 page fixture; the opening fund is the home fund IDVZ), two publishes of
2026-09-30:
  - IDVZ MTD has 3 holdings and none priced (n_ranked 0), QTD and YTD rank 2: the checked period radio is rf-period-QTD;
  - control: IDVZ MTD ranks 2 as well: the checked period radio is rf-period-MTD.
Left to the judgment grade: the empty period's switch shows its state (greyed, with a tooltip)."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402


def _checked_periods(html):
    tags = [t for t in re.findall(r"<input\b[^>]*>", html) if 'name="rf-period"' in t]
    return [re.search(r'id="([^"]+)"', t).group(1) for t in tags if re.search(r"\schecked(\s|>|=|/)", t)]


def _opening(html):
    tags = [
        t for t in re.findall(r"<input\b[^>]*>", html) if 'name="rf-fund"' in t and re.search(r"\schecked(\s|>|=|/)", t)
    ]
    return [re.search(r'id="([^"]+)"', t).group(1) for t in tags]


def run(v):
    c.setup_path()
    held = {"A1": 0.012, "A2": -0.004, "A3": 0.001}
    ranked = {"A1": 0.012, "A2": -0.004}
    hc = (
        u.hc_rows("IDVZ", "MTD", held, priced=False)
        + u.hc_rows("IDVZ", "QTD", ranked)
        + u.hc_rows("IDVZ", "YTD", ranked)
    )
    r, html = u.publish_with({"holding_contribution": hc})
    print(
        "publish:",
        r.get("status"),
        "| opening fund radio:",
        _opening(html),
        "| checked period:",
        _checked_periods(html),
    )
    v.check(
        r.get("status") == "OK" and _opening(html) == ["rf-fund-IDVZ"] and _checked_periods(html) == ["rf-period-QTD"],
        "IDVZ opens; its MTD ranks nothing, so the page opens on Quarter to date",
    )

    hc2 = u.hc_rows("IDVZ", "MTD", ranked) + u.hc_rows("IDVZ", "QTD", ranked) + u.hc_rows("IDVZ", "YTD", ranked)
    r2, html2 = u.publish_with({"holding_contribution": hc2})
    print("control publish:", r2.get("status"), "| checked period:", _checked_periods(html2))
    v.check(
        r2.get("status") == "OK" and _checked_periods(html2) == ["rf-period-MTD"],
        "control: when MTD ranks a holding, the page opens on Month to date",
    )


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
