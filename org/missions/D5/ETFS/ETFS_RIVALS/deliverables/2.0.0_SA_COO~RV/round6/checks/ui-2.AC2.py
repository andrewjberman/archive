"""RIV-ui-2 AC2 (RFW-U16 render half, chart:unknown-label): the no-sector bucket is never a ranked row on the page, and
it shows as ONE footnote under the sector tables carrying its share of the period's contribution. The producer half
(sx-1) writes the Unclassified sector row with NULL ranks and re-ranks the real sectors; the render must also hold on
a table written before sx-1 (Unclassified ranked).
INTERFACE: `render._rank_panel(ctx, f, period)`. The footnote is ONE element carrying
`data-unclassified-share="<fraction>"`: |Unclassified| / sum of |sector contribution| (the measure `_sectors_hidden`
already uses), and its text states that share as a percentage.

Pure, offline fixture: GQGU YTD, 2 ranked holdings and 4 sector rows: Energy +0.0200, Unclassified +0.0100, Industrials
+0.0080, Financials -0.0050. Unclassified holds 0.0100 / 0.0430 = 23.3% of the absolute sector contribution, under the
50% "Sectors not shown" rule, so the sector tables render. Two shapes:
  OLD = today's served shape (Unclassified rank_best 2 of 4); NEW = sx-1's prescribed shape (Unclassified rank NULL,
  Energy 1, Industrials 2; worst: Financials 1).
  - OLD: no table row of the panel names "Unclassified" or "No GICS sector";
  - OLD and NEW: exactly one `data-unclassified-share` element, value 0.233 (+/- 0.005), its text carrying "23%" (or
    "23.3%");
  - control (NEW): "Strongest sectors" reads Energy 1, Industrials 2, Financials shows under "Weakest sectors", and no
    row names the no-sector bucket."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402

SECTORS = {"Energy": 0.02, "Unclassified": 0.01, "Industrials": 0.008, "Financials": -0.005}


def _block(root, title):
    """The rows of the ranking table under the <h4> titled `title`: [(rank text, name text)]."""
    for div in root.tags("div"):
        h = [x for x in div.children if isinstance(x, u.Node) and x.tag == "h4"]
        if h and u.text(h[0]) == title:
            out = []
            for tr in div.tags("tr"):
                tds = [x for x in tr.children if isinstance(x, u.Node) and x.tag == "td"]
                if len(tds) >= 2:
                    out.append((u.text(tds[0]), u.text(tds[1])))
            return out
    return None


def _new_shape(rows):
    """sx-1's prescribed producer output: Unclassified keeps its contribution with NULL ranks; the real sectors rank
    among themselves and the sector n_ranked excludes it."""
    out = [dict(r) for r in rows]
    real = [r for r in out if r["axis"] == "sector" and r["bucket"] != "Unclassified"]
    for key, sgn in (("rank_best", -1), ("rank_worst", 1)):
        for i, r in enumerate(sorted(real, key=lambda r: sgn * r["contribution"])):
            r[key] = i + 1
    for r in out:
        if r["axis"] == "sector":
            r["n_ranked"] = len(real)
            if r["bucket"] == "Unclassified":
                r["rank_best"] = r["rank_worst"] = None
    return out


def _panel(render, rows):
    html = render._rank_panel(
        {"day": "2026-10-02", "a1": {"holding_contribution": rows}}, {"fund": "GQGU", "role": "rival"}, "YTD"
    )
    return u.parse(html)


def _unclassified_rows(root):
    return [
        u.text(td) for tr in root.tags("tr") for td in tr.tags("td") if re.search(r"Unclassified|No GICS", u.text(td))
    ]


def _footnote_ok(root):
    fn = root.all("data-unclassified-share")
    val = fn[0].attrs.get("data-unclassified-share") if len(fn) == 1 else None
    try:
        share = float(val)
    except (TypeError, ValueError):
        share = None
    ftxt = u.text(fn[0]) if len(fn) == 1 else ""
    print("  footnote:", len(fn), val, "|", ftxt)
    return share is not None and abs(share - 0.2326) <= 0.005 and bool(re.search(r"\b23(\.\d)?%", ftxt))


def run(v):
    c.setup_path()
    from rivalfunds import render

    old = u.hc_rows("GQGU", "YTD", {"G1": 0.015, "G2": -0.006}, SECTORS, end="2026-10-02")
    ro = _panel(render, old)
    print("OLD strongest:", _block(ro, "Strongest sectors"), "| weakest:", _block(ro, "Weakest sectors"))
    bad = _unclassified_rows(ro)
    v.check(not bad, f"OLD shape: no ranked row names the no-sector bucket (found {bad})")
    rn = _panel(render, _new_shape(old))
    print("NEW strongest:", _block(rn, "Strongest sectors"), "| weakest:", _block(rn, "Weakest sectors"))
    print("OLD:")
    ok_old = _footnote_ok(ro)
    print("NEW:")
    ok_new = _footnote_ok(rn)
    v.check(ok_old and ok_new, "one footnote under the sector tables states the no-sector share (0.233, '23%')")
    weak = _block(rn, "Weakest sectors") or []
    v.check(
        _block(rn, "Strongest sectors") == [("1", "Energy"), ("2", "Industrials")]
        and any(n == "Financials" for _, n in weak)
        and not _unclassified_rows(rn),
        "control (NEW shape): the real sectors rank 1, 2; Financials is weakest; no Unclassified row",
    )


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
