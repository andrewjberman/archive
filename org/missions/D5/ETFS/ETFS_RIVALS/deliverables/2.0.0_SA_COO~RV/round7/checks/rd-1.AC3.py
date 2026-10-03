"""RIV-rd-1 AC3 (RFW-U13 holdings half, DESIGN.md C14; RFW-U14, one name per security): the latest-holdings table and
the fund's report line read in plain words -- the system code in a title tooltip, the trade log's rule -- and a holding
reads the SAME name in the holdings table as on the face.
Source: the RFW register graded against the served page rv-publish-1002r6 (CLOUD eb6e9f04ff, the package at the base).
  - U13: `_holdings_section` prints "UNRESOLVED" as the Identity value (render.py:436; 94 on the served page) and the
    identifier type as a parenthesis "(cusip)" (`_ident`, render.py:79-80); `render_fund` prints "source policy
    bloomberg_primary" (render.py:399). The trade log already keeps codes in tooltips (`_coded`, `_trade_key`).
  - U14: the holdings-table name (render.py:438) does not read through the face's per-security name map, so a holding
    named 'INTUIT INC' in G1 reads 'INTUIT INC' there and 'Intuit Inc' in the rankings and the trend (45 case-only
    clashes in the register's grading, BASG 29 and GQGU 14 among them). At the base `_NAMES` stays empty under
    `render_page`: the second
    `def _render_page` (render.py:1457) rebinds the name the filling wrapper (render.py:1446) was meant to own.
INTERFACE: `render.render_page(ctx)` (the publish entry). Holdings table: no UNRESOLVED / RESOLVED code and no
identifier-type parenthesis in its text; each survives in a `title` (e.g. "Key resolution: UNRESOLVED", "Identifier
type: cusip"). Fund block (`article[data-fund]`): the source policy in words, the code in a `title`. Names: the
holdings row of a security shows exactly the name the rankings and the trend show for that key.

Pure, offline fixture (`_ui7.page_ctx`, one fund TXUE, policy bloomberg_primary, report 2026-10-01). Holdings:
INTU_US_Equity RESOLVED 'INTUIT INC' (cusip 461202103); G0593M107 UNRESOLVED 'AstraZeneca PLC' (cusip, no key); a cash
line. A1: holding_contribution YTD/QTD/MTD and buying_trend name INTU_US_Equity 'Intuit Inc'.
  - U13: the holdings section's text carries no 'UNRESOLVED' / 'RESOLVED' and no '(cusip)'; the TXUE block's text
    carries no 'bloomberg_primary';
  - U13: the codes survive as tooltips: titles in the holdings section carry 'UNRESOLVED' and 'cusip'; a title in the
    TXUE block carries 'bloomberg_primary';
  - U14: the holdings row of INTU_US_Equity reads 'Intuit Inc', and every case-insensitive 'intuit inc' on the page
    reads 'Intuit Inc' (one casing);
  - control: AstraZeneca PLC (no A1 row) keeps its own name with its identifier G0593M107; the cash line reads 'cash /
    currency'; the rankings show 'Intuit Inc'.
FAIL at base: both U13 limbs and the U14 limb; the control PASSes."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

# the codes in capitals ('resolved' in lower case is a plain word); an identifier type in parentheses in any case
CODES = re.compile(r"\bUNRESOLVED\b|\bRESOLVED\b|\((?i:cusip|isin|sedol|figi|ticker|security_id)\)")


def holdings():
    import pandas as pd

    base = {"position_type": "long", "asset_class": "Equity", "raw_identifier_kind": "cusip"}
    return pd.DataFrame([
        dict(base, security_id="INTU_US_Equity", raw_identifier="461202103", resolution_status="RESOLVED",
             security_name="INTUIT INC", quantity=100.0, market_value=50000.0, weight=0.05),
        dict(base, security_id=None, raw_identifier="G0593M107", resolution_status="UNRESOLVED",
             security_name="AstraZeneca PLC", quantity=10.0, market_value=3000.0, weight=0.03),
        dict(base, security_id=None, raw_identifier="USD Curncy", raw_identifier_kind=None,
             resolution_status="UNRESOLVED", security_name="Cash", position_type="cash", asset_class="Cash",
             quantity=5.0, market_value=5.0, weight=0.01)])


def ctx():
    f = u.fund_view("TXUE", latest_date="2026-10-01")
    f["policy"], f["holdings"] = "bloomberg_primary", holdings()
    hc = []
    for p in ("YTD", "QTD", "MTD"):
        sec = {"INTU_US_Equity": 0.01, "MSFT_US_Equity": -0.004}
        for r in u.hc_rows("TXUE", p, sec, {"Information Technology": 0.006}):
            if r["axis"] == "security":
                r["security_name"] = {"INTU_US_Equity": "Intuit Inc", "MSFT_US_Equity": "Microsoft Corp"}[r["bucket"]]
            hc.append(r)
    bt = u.bt_rows("TXUE")
    for r in bt:
        if r["bucket"] == "S1":
            r["bucket"], r["security_name"] = "INTU_US_Equity", "Intuit Inc"
    return u.page_ctx([f], a1={"holding_contribution": hc, "buying_trend": bt, "research_hypotheses": [],
                               "input_census": []})


def holding_rows(section):
    """{first cell text: [cell texts]} for each data row of the holdings tables."""
    out = {}
    for tr in section.tags("tr"):
        tds = [x for x in tr.children if isinstance(x, u.Node) and x.tag == "td"]
        if tds:
            out[u.text(tds[0])] = [u.text(x) for x in tds]
    return out


def run(v):
    c.setup_path()
    from rivalfunds import render

    root = u.parse(render.render_page(ctx()))
    sec = root.all("id", "holdings")
    art = [n for n in root.all("data-fund", "TXUE") if n.tag == "article"]
    if not sec or not art:
        v.check(False, f"the page carries the holdings section ({len(sec)}) and the TXUE block ({len(art)})")
        return
    hs, ab = sec[0], art[0]
    rows = holding_rows(hs)
    for k, cells in rows.items():
        print("  holdings row:", cells)
    print("report line:", u.text(ab)[:160])
    found = CODES.findall(u.text(hs)) + (["bloomberg_primary"] if "bloomberg_primary" in u.text(ab) else [])
    v.check(not found, f"U13: no system code in the holdings text or the fund's report line (found {found})")
    htitles = " ".join(n.attrs.get("title", "") for n in hs.all("title"))
    atitles = " ".join(n.attrs.get("title", "") for n in ab.all("title"))
    v.check("UNRESOLVED" in htitles and "cusip" in htitles and "bloomberg_primary" in atitles,
            "U13: the codes survive as tooltips (UNRESOLVED and cusip in the holdings, bloomberg_primary in the block)")
    intu = [k for k, cells in rows.items() if len(cells) > 1 and cells[1].startswith("461202103")]
    names = sorted(set(re.findall(r"(?i)intuit inc", u.text(root))))
    print("INTU holdings name:", intu, "| casings on the page:", names)
    v.check(intu == ["Intuit Inc"] and names == ["Intuit Inc"],
            "U14: the holdings row reads 'Intuit Inc', the face's name, and the page carries one casing")
    az = rows.get("AstraZeneca PLC", [])
    cash = rows.get("Cash", [])
    rk = [n for n in root.all("data-rank-fund", "TXUE") if "Intuit Inc" in u.text(n)]
    v.check(len(az) > 1 and az[1].startswith("G0593M107") and bool(cash) and "cash / currency" in cash[-1]
            and bool(rk),
            "control: AstraZeneca PLC keeps its name and identifier, the cash line reads 'cash / currency', the "
            "rankings show 'Intuit Inc'")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
