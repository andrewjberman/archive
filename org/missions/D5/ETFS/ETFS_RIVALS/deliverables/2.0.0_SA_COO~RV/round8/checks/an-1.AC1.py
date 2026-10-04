"""RIV-an-1 AC1 (the CVO's round-7 P2 "3 underscore keys on money-market lines" + RFW-U14's AI-text residue): the AI
account text reads each security under the page's ONE name. A whole stored security key reads as that name (a cash-like
line as reader words), the key kept in a title. The stored text is never rewritten (display only, as RFW-U09).
Source (measured on the served rv-publish-1002r7, rendered, visible only):
- `DGCXX_US_Equity` (TSEL, PCLG) and `IJGXX_US_Equity` (ETFT) are visible in the AI prose;
- 13 casing clashes in the AI accounts' opening lines and 26 in the full text (e.g. 'SPOTIFY TECHNOLOGY SA' / 'Spotify
  Technology SA');
- tables have 0 clashes (rd-1).
At the base, `render._rich` labels only the stored READING keys (fear_greed/..., keyword_sentiment/...).

Interface (prescribed): `render.render_page(ctx)`. Inside every AI card (`[data-ai-fund]`, dialog text included):
  - no whole security key of the form `<ID>_<CC>_Equity` in the text; a key the page names reads as `_NAMES[key]`;
    a cash-equivalent key (`gold_holding_contribution.cash_equivalent`) the page does not name reads in words containing
    the ticker and "money market" (e.g. "DGCXX money market fund");
  - a stored NAME that differs only in casing (or is the same security's G1 name) from the page's name for a key the
    account cites reads as the page's name;
  - each replaced key or name survives in a `title`;
  - the research_hypotheses row is unchanged.

Pure, offline (`_ui7.page_ctx`, one fund TXUE). Holdings:
- INTU_US_Equity 'INTUIT INC';
- MSFT_US_Equity 'MICROSOFT CORP';
- DGCXX_US_Equity, a money-market line with no name.
A1 names INTU 'Intuit Inc' and MSFT 'Microsoft Corp'. One activity_30d account cites
trade_schedule TXUE|DGCXX_US_Equity, TXUE|MSFT_US_Equity, holding_contribution TXUE|YTD|INTU_US_Equity and the
fear_greed index. Its text names each by key or stored name.
  - (a) no `_US_Equity` key in any AI card's prose (the `.rf-cite` citation list keeps the cited keys, by design);
  - (b) the AI card reads 'Intuit Inc' and 'Microsoft Corp', and no 'INTUIT INC' / 'MICROSOFT CORP' casing is left;
  - (c) DGCXX reads in words with 'DGCXX' and 'money market', and a title in the card carries 'DGCXX_US_Equity';
  - (e) no markup leaks into the card's text (a replacement inside an inserted tag would show '">' or 'title=');
  - (d) control: the reading key still reads as its label (title 'fear_greed/fear_greed_index'), and the stored account
        row is unchanged.
FAIL at base: (a), (b), (c); (d) and (e) PASS."""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

KEY = re.compile(r"\b[A-Z0-9]+_[A-Z]{2}_Equity\b")
TEXT = ("TXUE moved cash-like DGCXX_US_Equity around in small windows while it trimmed MICROSOFT CORP. "
        "INTU_US_Equity led the year, and INTUIT INC was the largest add as fear_greed/fear_greed_index sat at 28.")


def holdings():
    import pandas as pd

    base = {"position_type": "long", "asset_class": "Equity", "raw_identifier_kind": "ticker",
            "resolution_status": "RESOLVED", "weight": 0.05}
    return pd.DataFrame([
        dict(base, security_id="INTU_US_Equity", raw_identifier="INTU US Equity", security_name="INTUIT INC",
             quantity=100.0, market_value=50000.0),
        dict(base, security_id="MSFT_US_Equity", raw_identifier="MSFT US Equity", security_name="MICROSOFT CORP",
             quantity=50.0, market_value=20000.0),
        dict(base, security_id="DGCXX_US_Equity", raw_identifier="DGCXX US Equity", security_name=None,
             asset_class="Money Market", quantity=9000.0, market_value=9000.0)])


def ctx():
    f = u.fund_view("TXUE", latest_date="2026-10-01")
    f["policy"], f["holdings"] = "bloomberg_primary", holdings()
    names = {"INTU_US_Equity": "Intuit Inc", "MSFT_US_Equity": "Microsoft Corp"}
    hc = []
    for p in ("YTD", "QTD", "MTD"):
        for r in u.hc_rows("TXUE", p, {"INTU_US_Equity": 0.01, "MSFT_US_Equity": -0.004}, {"Information Technology": 0.006}):
            if r["axis"] == "security":
                r["security_name"] = names[r["bucket"]]
            hc.append(r)
    cited = [{"table": "trade_schedule", "key": "TXUE|DGCXX_US_Equity|2026-09-10", "revision": "r", "value": 9018.13},
             {"table": "trade_schedule", "key": "TXUE|MSFT_US_Equity|2026-09-14", "revision": "r", "value": -75306.1},
             {"table": "holding_contribution", "key": "TXUE|YTD|INTU_US_Equity", "revision": "r", "value": 0.0125},
             {"table": "market_context", "key": "fear_greed/fear_greed_index", "revision": "2026-10-01", "value": 28.0}]
    acct = u.account("TXUE", "activity_30d", TEXT, cited=cited, observed=["MICROSOFT CORP was trimmed."],
                     vintages={"fear_greed/fear_greed_index": "2026-10-01"})
    return acct, u.page_ctx([f], a1={"holding_contribution": hc, "buying_trend": u.bt_rows("TXUE"),
                                     "research_hypotheses": [acct], "input_census": []})


def run(v):
    c.setup_path()
    from rivalfunds import render

    acct, cx = ctx()
    before = json.dumps(acct, sort_keys=True)
    root = u.parse(render.render_page(cx))
    cards = root.all("data-ai-fund")
    cite = lambda n: "rf-cite" in (n.attrs.get("class") or "").split()  # noqa: E731 -- the audit citation list keeps keys
    t = " ".join(u.text(n, skip=cite) for n in cards)
    titles = " | ".join(n.attrs.get("title", "") for card in cards for n in card.all("title"))
    print("AI cards:", len(cards), "| text:", t[:700])
    print("titles in the cards:", titles[:400])
    v.check(len(cards) >= 1, "fixture: the page renders the TXUE AI card")
    keys = sorted(set(KEY.findall(t)))
    v.check(len(cards) >= 1 and not keys, f"(a) no whole security key in the AI card's text (found {keys})")
    v.check("Intuit Inc" in t and "Microsoft Corp" in t and "INTUIT INC" not in t and "MICROSOFT CORP" not in t,
            "(b) the AI card names INTU and MSFT as the page does ('Intuit Inc', 'Microsoft Corp'), no other casing")
    v.check(re.search(r"DGCXX[^.]{0,40}money market", t, re.I) is not None and "DGCXX_US_Equity" in titles,
            "(c) the money-market line reads in words ('DGCXX ... money market'), the key in a title")
    leaks = sorted(set(re.findall(r"<[a-z/][^ ]{0,12}|\"\s*>|title=", t)))
    v.check(not leaks, f"(e) no markup leaks into the AI card's text (found {leaks})")
    v.check("fear_greed/fear_greed_index" in titles and json.dumps(acct, sort_keys=True) == before,
            "(d) control: the reading key still reads as its label, and the stored account row is unchanged")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
