"""RIV-rd-1 AC1 (RFW-D12 render half; RFW-U16 trend half, chart:unknown-label): on the buying-trend card a line built
from ONE window reads "Single trade" -- not "Bet, 1 trade" -- and the no-sector bucket leaves the sector tables for ONE
footnote stating its share, as the rankings' `data-unclassified-share` footnote already does.
Source: the RFW register graded against the served page rv-publish-1002r6 (CLOUD eb6e9f04ff, the package at the base).
  - D12: `render._pattern` (render.py:965-975) prints '<Reading>, <n> trade(s)', so every one-window line reads
    "Bet, 1 trade" (58 on the served 10-02 page; every IDVZ line is 1 window);
  - U16: `_trend_card` (render.py:1027-1028) passes the sector rows to `_trend_table` unfiltered, so the Unclassified
    row (rank NULL since RIV-sx-1) prints as an unranked row "No GICS sector in the source" (8 on the served page).
INTERFACE: `render._trend_card(ctx, f)`.
  - a line whose `n_windows` is 1 reads "Single trade" in its "How" cell; neither the cell text nor its hover names
    BET or TILT. A line of 2+ windows keeps '<Reading>, <n> trades'.
  - the card's sector tables carry no Unclassified row; the card carries ONE element `data-unclassified-share=
    "<fraction>"` (outside every table row): |Unclassified gross| / sum of |sector gross| (`_traded_of`, the measure
    `_sectors_hidden` already applies to this card), its text stating the share as a percentage.

Pure, offline fixture (TXUE, buying_trend in the A1 contract, sx-1's served shape):
  security: Intuit Inc into, 5 windows, tilt, rank 1; Apple Inc into, 3 windows, bet, rank 2; Arthur J Gallagher away,
            1 window, bet, rank 1;
  sector:   Energy into, gross 31m, 4 windows, tilt, rank 1; Industrials away, gross 2.1m, 1 window, bet, rank 1;
            Unclassified into, gross 9m, 2 windows, rank NULL. Share 9 / 42.1 = 21.4% (< 50%, so the tables render).
  - D12: Arthur J Gallagher and Industrials read "Single trade", with no BET/TILT in the cell or its hover;
  - U16: no row of the card's tables names "No GICS sector" or "Unclassified";
  - U16: exactly one `data-unclassified-share` element outside the table rows, value 0.214 (+/- 0.005), text "21%"
    or "21.4%";
  - control: Intuit Inc reads "Tilt, 5 trades", Apple Inc "Bet, 3 trades", Energy "Tilt, 4 trades", and Energy and
    Industrials still rank 1 in their tables.
FAIL at base: the D12 limb and both U16 limbs; the control PASSes."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

LINES = (  # (axis, bucket, name, lean, net, gross, n_windows, reading, rank)
    ("security", "INTU_US_Equity", "Intuit Inc", "into", 22973442.0, 50000000.0, 5, "tilt", 1),
    ("security", "AAPL_US_Equity", "Apple Inc", "into", 5000000.0, 6000000.0, 3, "bet", 2),
    ("security", "AJG_US_Equity", "Arthur J Gallagher", "away", -1340000.0, 1500000.0, 1, "bet", 1),
    ("sector", "Energy", None, "into", 30000000.0, 31000000.0, 4, "tilt", 1),
    ("sector", "Industrials", None, "away", -2000000.0, 2100000.0, 1, "bet", 1),
    ("sector", "Unclassified", None, "into", 6000000.0, 9000000.0, 2, "tilt", None),
)
SHARE = 9.0 / 42.1
WORDS = re.compile(r"(?i)\b(?:bet|tilt)\b")


def rows():
    return [{"fund_id": "TXUE", "role": "rival", "window_start": "2026-01-02", "window_end": "2026-10-01",
             "n_trading_days": 189, "axis": a, "bucket": b, "security_name": nm, "net_notional_base": net,
             "gross_notional_base": g, "n_windows": nw, "lean": lean, "rank": rk, "reading": rd,
             "trend_mark": "0 + + 0 0 0 0 0 0 0", "n_refused_windows": 0, "claim": "INFERRED", "revision": "fx"}
            for a, b, nm, lean, net, g, nw, rd, rk in LINES]


def table_rows(root):
    """[(table title, rank text, line text, How cell node)] for every data row of the card's trend tables."""
    out = []
    for div in root.tags("div"):
        h = [x for x in div.children if isinstance(x, u.Node) and x.tag == "h4"]
        if not h:
            continue
        for tr in div.tags("tr"):
            tds = [x for x in tr.children if isinstance(x, u.Node) and x.tag == "td"]
            if len(tds) >= 4:
                out.append((u.text(h[0]), u.text(tds[0]), u.text(tds[1]), tds[-1]))
    return out


def run(v):
    c.setup_path()
    from rivalfunds import render

    html = render._trend_card({"day": "2026-10-02", "a1": {"buying_trend": rows()}}, {"fund": "TXUE", "role": "rival"})
    root = u.parse(html)
    got = table_rows(root)
    for title, rk, line, how in got:
        tips = [n.attrs.get("title", "")[:60] for n in how.all("title")]
        print(f"  {title!r:28} | {rk:>2} | {line:30} | {u.text(how)!r} | hover={tips}")
    how = {line: cell for _, _, line, cell in got}

    def single(name):
        cell = how.get(name)
        if cell is None:
            return False
        hover = " ".join(n.attrs.get("title", "") for n in cell.all("title"))
        return u.text(cell).lower() == "single trade" and not WORDS.search(u.text(cell)) and not WORDS.search(hover)

    v.check(single("Arthur J Gallagher") and single("Industrials"),
            "D12: a one-window line (Arthur J Gallagher, Industrials) reads 'Single trade', no BET/TILT in text or "
            "hover")
    unc = [(t, line) for t, _, line, _ in got if re.search(r"Unclassified|No GICS", line)]
    v.check(not unc, f"U16: no trend table row names the no-sector bucket (found {unc})")
    fn = root.all("data-unclassified-share")
    val = fn[0].attrs.get("data-unclassified-share") if len(fn) == 1 else None
    try:
        share = float(val)
    except (TypeError, ValueError):
        share = None
    ftxt = u.text(fn[0]) if len(fn) == 1 else ""
    in_row = len(fn) == 1 and u.inside(fn[0], lambda x: x.tag == "tr")
    print(f"footnotes: {len(fn)} value={val} in_row={in_row} text={ftxt!r}")
    v.check(share is not None and abs(share - SHARE) <= 0.005 and not in_row
            and bool(re.search(r"\b21(\.4)?%", ftxt)),
            f"U16: one footnote outside the tables states the no-sector share ({SHARE:.3f}, '21%' or '21.4%')")
    ranks = {(t, line): rk for t, rk, line, _ in got}
    ctl = (u.text(how.get("Intuit Inc", u.Node("x", []))) == "Tilt, 5 trades"
           and u.text(how.get("Apple Inc", u.Node("x", []))) == "Bet, 3 trades"
           and u.text(how.get("Energy", u.Node("x", []))) == "Tilt, 4 trades"
           and ranks.get(("Sectors leaned into", "Energy")) == "1"
           and ranks.get(("Sectors leaned away from", "Industrials")) == "1")
    v.check(ctl, "control: multi-window lines keep '<Reading>, <n> trades'; Energy and Industrials rank 1")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
