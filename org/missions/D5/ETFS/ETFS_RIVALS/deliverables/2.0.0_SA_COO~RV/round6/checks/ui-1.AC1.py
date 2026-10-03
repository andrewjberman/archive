"""RIV-ui-1 AC1 (RFW-U01, design rule "say it once"): the page header states the current-funds count ONCE. The KPI tile
keeps "<n> of <m>"; the headline sentence names only the lagging funds and is absent when none lag.
INTERFACE: `render._shell(ctx, body)` renders the header (`<header>`). The lagging sentence is the element carrying
`data-headline`, present only when a fund lags; each lagging fund in it keeps `data-lagging="<FUND>"` (round-5 hook).

Pure, offline fixture: funds AAA (home), BBB, CCC (rivals) in one group.
  - all three current: "3 of 3" appears once in the header text and there is no `data-headline` element;
  - CCC lags: "2 of 3" appears once; there is one `data-headline` element, CCC is marked data-lagging="CCC" in the
    header, and the sentence names neither AAA nor BBB;
  - control: the KPI tile row (`rf-kpis`) is present in both headers."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402


def _header(render, funds):
    root = u.parse(render._shell(u.page_ctx(funds), ""))
    return next(iter(root.tags("header")), None)


def run(v):
    c.setup_path()
    from rivalfunds import render

    cur = [u.fund_view("AAA", role="home"), u.fund_view("BBB"), u.fund_view("CCC")]
    h = _header(render, cur)
    t = u.text(h) if h is not None else ""
    print("all current, header text:", t[:300])
    n = len(re.findall(r"\b3 of 3\b", t))
    v.check(n == 1, f"all current: '3 of 3' appears once in the header (found {n})")
    v.check(h is not None and not h.all("data-headline"), "all current: no lagging sentence (no data-headline element)")

    lag = [
        u.fund_view("AAA", role="home"),
        u.fund_view("BBB"),
        u.fund_view("CCC", status="not-updated", reason="content_repeat: the report repeats the prior day"),
    ]
    h2 = _header(render, lag)
    t2 = u.text(h2) if h2 is not None else ""
    print("CCC lags, header text:", t2[:300])
    n2 = len(re.findall(r"\b2 of 3\b", t2))
    v.check(n2 == 1, f"CCC lags: '2 of 3' appears once in the header (found {n2})")
    hl = h2.all("data-headline") if h2 is not None else []
    hl_text = " ".join(u.text(x) for x in hl)
    v.check(
        len(hl) == 1 and bool(h2.all("data-lagging", "CCC")) and "AAA" not in hl_text and "BBB" not in hl_text,
        "CCC lags: one data-headline element, CCC marked data-lagging, no current fund named in the sentence",
    )
    v.check(
        h is not None and h2 is not None and bool(h.cls("rf-kpis")) and bool(h2.cls("rf-kpis")),
        "control: the KPI tile row is present in both headers",
    )


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
