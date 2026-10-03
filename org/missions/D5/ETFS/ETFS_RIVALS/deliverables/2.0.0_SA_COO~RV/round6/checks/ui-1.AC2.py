"""RIV-ui-1 AC2 (RFW-U17, C-pattern status chip): the fund header reads "Latest report 30 Sep", with the source as its
own chip and current/late as a separate chip. No ISO date and no semicolon-joined status text on the header.
INTERFACE: `render._fund_panel(ctx, f)`; the header is the fragment before `data-component="rankings"`. The source chip
is the existing badge element (`data-source="<source>"`). The freshness chip is ONE element carrying
`data-freshness="current"` (fund updated) or `data-freshness="late"` (fund not updated, a report on file).

Pure, offline fixture (A1 tables absent; only the header is read):
  - IDVZ, home, updated, latest 2026-09-30 from home_producer: the header text matches "Latest report 30 Sep", carries
    no "2026-09-30" and no ";", and the header has one data-freshness="current" element;
  - TXUE, rival, NOT updated (a guardrail failure), latest 2026-09-25 from bloomberg: "Latest report 25 Sep", no
    "2026-09-25", no ";", one data-freshness="late" element;
  - control: each header keeps its source chip (data-source="home_producer" / "bloomberg")."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402


def _head(render, f):
    html = render._fund_panel(u.page_ctx([f]), f)
    frag = html.split('data-component="rankings"')[0]
    return u.parse(frag)


def run(v):
    c.setup_path()
    from rivalfunds import render

    cases = (
        (
            "IDVZ",
            u.fund_view(
                "IDVZ",
                role="home",
                latest_date="2026-09-30",
                latest_source="home_producer",
                fund_name="Opal International Dividend ETF",
            ),
            "30 Sep",
            "2026-09-30",
            "current",
            "home_producer",
        ),
        (
            "TXUE",
            u.fund_view(
                "TXUE",
                status="not-updated",
                latest_date="2026-09-25",
                latest_source="bloomberg",
                reason="content_repeat: the report repeats the prior day",
                fund_name="TXUE Test Fund",
            ),
            "25 Sep",
            "2026-09-25",
            "late",
            "bloomberg",
        ),
    )
    for fund, f, short, iso, fresh, src in cases:
        root = _head(render, f)
        t = u.text(root)
        print(f"{fund} header text:", t)
        v.check(
            bool(re.search(r"Latest report\s+" + short + r"\b", t)) and iso not in t and ";" not in t,
            f"{fund}: the header reads 'Latest report {short}', no ISO date, no semicolon",
        )
        chips = root.all("data-freshness")
        v.check(
            len(chips) == 1 and chips[0].attrs["data-freshness"] == fresh,
            f'{fund}: one separate freshness chip data-freshness="{fresh}" (found {[x.attrs for x in chips]})',
        )
        v.check(bool(root.all("data-source", src)), f'control: {fund} keeps its source chip data-source="{src}"')


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
