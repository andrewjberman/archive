"""RIV-ks-1 AC1 (round 23; rows ETFS_RIVALS-Z-S65 and Z-S66; ROUND_ANALYSIS.round22 R1): a security named in an account's
text never opens a dialog that has no section for the panel's fund.

The fault, reproduced at CLOUD ce10d97077 by this fixture with the served markup: fund F traded a security under a raw key
(a CUSIP in the trade schedule) while its tables carry the security under the page's one key (`AAPL_US_Equity`); the two
keys carry page names that differ only in case ("APPLE INC", "Apple Inc"); F's account cites the raw key. Inside F's panel
`render._fund_keys` counts the traded raw key as one F "holds or traded", `_panel_page` / `_name_link` let the cited key
decide, and the name links to the raw key. `_sec_dialogs` builds sections from contribution and trend rows only, so that
dialog holds a name and nothing else. Served 2026-10-07: 4 buttons in GQGU's panel (META, ASML).

Interface (prescribed): on the rendered page every `data-sec` button inside a fund panel targets a dialog that carries a
section for that fund, or the mention is plain text; no dialog on the page has zero sections.

Fixture: tests/test_crorv_layout.py `_ctx` / `_hc`; funds IDVZ (home) and TXUE; contribution rows for AAPL_US_Equity and
MSFT_US_Equity in both funds; names {AAPL_US_Equity: "Apple Inc", MSFT_US_Equity: "Microsoft Corp", "037833100":
"APPLE INC"}; TXUE carries one trade under security_key "037833100"; one account in TXUE's panel.
  - (a) text "TXUE also opened Apple Inc for $1.0 million.", citing `TXUE|037833100` in trade_schedule:
    `render.fund_section_census(html)["missing"]` is 0 (base: 2);
  - (b) same page: no dialog has zero sections (base: a dialog for 037833100 with none);
  - (c) same page: the mention is a button targeting `rf-s-AAPL_US_Equity`, or plain text; never a button to the raw key;
  - (d) the same with the citation naming `TXUE|R30|037833100` in holding_contribution: 0 missing, no empty dialog;
  - (e) a key no table carries for ANY fund, traded and cited by TXUE, under a name of its own ("TXUE opened Zeta Corp.",
    names + {"999999999": "Zeta Corp"}): 0 missing, no empty dialog (plain text is the expected reading);
  - (f) control: without the trade the same text links to rf-s-AAPL_US_Equity and reads 0 missing; the page has both
    panels; test_r13fe1_alias_by_fund's rule still holds on its own fixture (a fund holding GOOG links to GOOG).
FAIL at base ce10d97077: (a), (b), (c), (d) FAIL; (e) per its print; (f) PASS."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[9]
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
from rivalfunds import render  # noqa: E402
from rivalfunds.tests import test_r13fe1_alias_by_fund as r13  # noqa: E402
from rivalfunds.tests.test_crorv_layout import _ctx, _hc  # noqa: E402

AAPL, MSFT, RAW = "AAPL_US_Equity", "MSFT_US_Equity", "037833100"
FUNDS = (("IDVZ", "home"), ("TXUE", "rival"))
NAMES = {AAPL: "Apple Inc", MSFT: "Microsoft Corp", RAW: "APPLE INC"}
fails = []


def check(label, ok, got=""):
    print(("PASS " if ok else "FAIL ") + label + ((" | " + str(got)[:300]) if got != "" else ""))
    if not ok:
        fails.append(label)


def page(text, cited, trade_key=RAW, names=None, trade_name="APPLE INC"):
    hc = []
    for fund, _r in FUNDS:
        for p in ("R30", "QTD", "YTD"):
            hc += _hc(fund, p, {AAPL: 0.02, MSFT: -0.01})
    acct = {"run_id": "r", "item_id": "a", "fund_id": "TXUE", "kind": "activity_30d", "observed": "[]", "inferred": "[]",
            "cited_rows": json.dumps(cited), "invalidation": None, "input_vintages": "{}", "web_reads": "[]",
            "grounding": "PASS", "grounding_reason": None, "input_manifest": "{}", "produced_at": "t", "text": text}
    ctx = _ctx({"holding_contribution": hc, "research_hypotheses": [acct]}, FUNDS)
    if trade_key:
        for g in ctx["groups"]:
            for f in g["funds"]:
                if f.get("fund") == "TXUE":
                    f["windows"] = list(f.get("windows") or []) + [{"trades": [
                        {"security_key": trade_key, "security_name": trade_name, "action": "entry", "est_notional": 1e6}]}]
    orig = render._collect_names
    render._collect_names = lambda cx: {**orig(cx), **(names or NAMES)}
    try:
        return render.render_page(ctx)
    finally:
        render._collect_names = orig


def ai(html):
    return html.split('data-ai-fund="TXUE"')[1].split('data-component="rankings"')[0]


def empty_dialogs(html):
    return [seg.split('"', 1)[0] for seg in html.split('data-sec-dialog="')[1:] if "<section" not in seg.split("<div id=rf-s-")[0]]


def buttons(html):
    return re.findall(r'<button class=rf-h data-sec="([^"]*)" popovertarget=(rf-s-[A-Za-z0-9_-]+)[^>]*>([^<]*)</button>', ai(html))


TEXT = "TXUE also opened Apple Inc for $1.0 million."
CITE_TS = [{"table": "trade_schedule", "key": f"TXUE|{RAW}", "revision": "x", "value": 1.0}]
CITE_HC = [{"table": "holding_contribution", "key": f"TXUE|R30|{RAW}", "revision": "x", "value": 1.0}]

h = page(TEXT, CITE_TS)
cen = render.fund_section_census(h)
check("(a) traded under a raw key and citing it: 0 buttons open a dialog without the fund's section", cen["missing"] == 0, cen)
check("(b) no dialog has zero sections", empty_dialogs(h) == [], empty_dialogs(h))
b = buttons(h)
words = re.sub(r"<[^>]+>", "", ai(h))
check("(c) the mention targets rf-s-AAPL_US_Equity or is plain text; never the raw key",
      all(k != RAW and t == "rf-s-AAPL_US_Equity" for k, t, _w in b) and ("Apple Inc" in words or "APPLE INC" in words), b)

h2 = page(TEXT, CITE_HC)
cen2 = render.fund_section_census(h2)
check("(d) the same with a holding_contribution citation of the raw key", cen2["missing"] == 0 and empty_dialogs(h2) == [],
      {"census": cen2, "empty": empty_dialogs(h2)})

h3 = page("TXUE opened Zeta Corp.", [{"table": "trade_schedule", "key": "TXUE|999999999", "revision": "x", "value": 1.0}],
          trade_key="999999999", names={**NAMES, "999999999": "Zeta Corp"}, trade_name="Zeta Corp")
cen3 = render.fund_section_census(h3)
check("(e) a traded, cited key no table carries: 0 missing and no empty dialog", cen3["missing"] == 0 and empty_dialogs(h3) == [],
      {"census": cen3, "empty": empty_dialogs(h3), "buttons": buttons(h3)})

h4 = page(TEXT, [], trade_key=None)
r13_html = r13._page([r13._acct("IDVZ", "IDVZ lost on Alphabet Inc."), r13._acct("TXUE", "TXUE trimmed Alphabet Inc-Cl C.")],
                     {"IDVZ": [r13.GOOGL, "AAPL_US_Equity"], "TXUE": [r13.GOOG, "AAPL_US_Equity"]})
ok_plain = "popovertarget=rf-s-AAPL_US_Equity>Apple Inc</button>" in ai(h4) and render.fund_section_census(h4)["missing"] == 0
ok_r13 = f'data-sec="{r13.GOOG}"' in r13._ai(r13_html, "TXUE") and render.fund_section_census(r13_html)["missing"] == 0
panels = sorted(set(re.findall(r'data-fund-panel="([^"]+)"', h4)))
check("(f) control: without the trade the name links to the tabled key; both panels; round 13's own-listing rule holds",
      ok_plain and ok_r13 and panels == ["IDVZ", "TXUE"], {"plain": ok_plain, "r13": ok_r13, "panels": panels})

print("AC1 RESULT: " + ("PASS 0 failures" if not fails else f"FAIL {len(fails)}: " + "; ".join(fails)))
sys.exit(0 if not fails else 1)
