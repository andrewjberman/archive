"""RIV-pg-1 AC1 (FWD-18, FWD-19 behaviour; amendment A1) -- the page leads with the components, switches fund and period with no
script, and keeps the audit material one step away.

Offline: the test_p2 page fixture plus the A1 tables (`_a1_page.publish`), one publish for 2026-09-30.
  - the publish is OK, the page has no `<script`, and `render.validate` passes on it;
  - one `rf-fund` radio per universe fund, IDVZ `checked`; `rf-period` radios in the order MTD, QTD, YTD, MTD `checked`;
  - a ranking panel for every universe fund x {MTD, QTD, YTD};
  - control: the first ranking panel comes before `<details id="audit"`, which exists and is not `open`."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _a1_page as ap  # noqa: E402
import _common as c  # noqa: E402


def _inputs(html, name):
    tags = [t for t in re.findall(r"<input\b[^>]*>", html) if f'name="{name}"' in t]
    return [(re.search(r'id="([^"]+)"', t).group(1) if re.search(r'id="([^"]+)"', t) else None, " checked" in t or "checked>" in t
             or 'checked="' in t) for t in tags]


def run(v):
    c.setup_path()
    from rivalfunds import render, universe

    r, html = ap.publish()
    print("publish:", r.get("status"), "| bytes", len(html))
    funds = [e["fund_id"] for e in universe.entries()]
    ok, why = render.validate(html, html.count('<details class="trace"'))
    v.check(r.get("status") == "OK" and html and "<script" not in html.lower() and ok, f"published, script-free, validate passes ({why})")
    fr, pr = _inputs(html, "rf-fund"), _inputs(html, "rf-period")
    print("fund radios:", fr[:4], "...", len(fr), "| period radios:", pr)
    v.check(sorted(i for i, _ in fr) == sorted(f"rf-fund-{f}" for f in funds) and [i for i, on in fr if on] == ["rf-fund-IDVZ"]
            and [i for i, _ in pr] == ["rf-period-MTD", "rf-period-QTD", "rf-period-YTD"] and [i for i, on in pr if on] == ["rf-period-MTD"],
            "one fund radio per fund with IDVZ checked; periods MTD, QTD, YTD with MTD checked")
    panels = set(re.findall(r'data-rank-fund="([A-Z]+)"\s+data-rank-period="(MTD|QTD|YTD)"', html))
    print("ranking panels:", len(panels), "of", len(funds) * 3)
    v.check(panels == {(f, p) for f in funds for p in ("MTD", "QTD", "YTD")}, "a ranking panel for every fund x period")
    first, audit = html.find("data-rank-fund="), re.search(r"<details\b[^>]*\bid=\"audit\"[^>]*>", html)
    print("first panel at", first, "| audit tag:", audit and audit.group(0))
    v.check(first >= 0 and audit is not None and first < audit.start() and " open" not in audit.group(0),
            "control: the components lead, the audit block follows closed")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
