# -*- coding: utf-8 -*-
"""The issuer's hookup for the 8 G3 portal tools (OG-pt-1, OG-pt-2) and the 5 G6 news tools (OG-nw-1).
Usage: python hookup_g3g6.py <gateway-root>. Pins: registry 75 -> 88, non-data 66 -> 79."""
import sys

GW = sys.argv[1].rstrip("/")
APP, TESTS = GW + "/app/", GW + "/tests/"

# (module alias, tool name, signature, call args, audit args, doc)
TOOLS = [
    ("_ptm", "portal_get_model_positioning", "", "", "{}",
     "The five Opal model portfolios (allocation, holdings, deltas vs benchmark) and the aggregate book, from the portal bucket."),
    ("_ptm", "portal_get_model_attribution", "", "", "{}",
     "QTD, YTD, 1Y and since-inception attribution totals per model, with the allocation summary by period."),
    ("_ptm", "portal_get_market_returns", "ticker: str = None", "ticker", '{"ticker": (ticker or "")[:32]}',
     "No ticker: index and sector period returns. With a ticker: that ticker's price history."),
    ("_ptm", "portal_get_market_regime", "include_history: bool = False", "include_history", '{"include_history": bool(include_history)}',
     "The current market regime, its signals and the regime path; with include_history, the full regime history."),
    ("_ptc", "portal_get_macro", "slug: str = None", "slug", '{"slug": (slug or "")[:64]}',
     "The macro indicators, volatility and yield curve (no slug), or one indicator's series (slug)."),
    ("_ptc", "portal_get_valuation", "index: str = None", "index", '{"index": (index or "")[:64]}',
     "Valuation multiples and risk premium (no index), or one index's block of each (index)."),
    ("_ptc", "portal_get_security_scan", "universe: str, factor: str = None, top: int = 20", "universe, factor, top",
     '{"universe": (universe or "")[:64], "factor": (factor or "")[:64]}',
     "The top and bottom names of one universe by one factor's percentile (top is clamped to 100)."),
    ("_ptc", "portal_get_pipeline_freshness", "", "", "{}",
     "Each pipeline source's own data_as_of and run, with its trading-day lag behind T-1."),
    ("_nws", "news_search_articles",
     "date_from: str = None, date_to: str = None, text: str = None, source: str = None, sentiment_label: str = None, limit: int = 25",
     "date_from, date_to, text, source, sentiment_label, limit", '{"date_from": date_from, "date_to": date_to, "source": source}',
     "News articles from the news store over a date range (14-day cap per call), newest first, filtered by text, source and sentiment label."),
    ("_nws", "news_trending_topics", "date: str = None, side: str = \"all\", days: int = 1, match: str = None",
     "date, side, days, match", '{"date": date, "side": side, "days": days}',
     "Trending news topics for a day (or the last days), by side, with an optional name match."),
    ("_nws", "news_keyword_intelligence", "keyword: str = None, date: str = None", "keyword, date",
     '{"keyword": (keyword or "")[:64], "date": date}', "Keyword intelligence from the news store: one keyword on a date, or the day's top keywords."),
    ("_nws", "news_market_mood", "", "", "{}", "The market mood from the news store: the newest portal singleton, with its freshness in trading days."),
    ("_nws", "news_for_security", "security_key: str = None, ticker: str = None, window_days: int = 14", "security_key, ticker, window_days",
     '{"security_key": security_key, "ticker": ticker}', "News for one security by security_key or ticker over a window of days (14-day cap)."),
]
NAMES = [t[1] for t in TOOLS]
assert len(NAMES) == 13


def edit(path, old, new, count=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == count, "%s: %r found %d times" % (path, old[:60], s.count(old))
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


# 1. tools.py: the import after the G1 import, and the thirteen registrations after harvest_get_peers_and_scores
g1_imp = "from . import harvest_identity as _hvi, harvest_press as _hvp, harvest_figures as _hvf, harvest_research as _hvr   # NFRA_OPLGTW G1-TYPED (FWD-22)"
edit(APP + "tools.py", g1_imp, g1_imp + "\nfrom . import portal_models as _ptm, portal_macro as _ptc, news_typed as _nws   # NFRA_OPLGTW G3 + G6 (FWD-22)")
blk = ["# NFRA_OPLGTW G3 + G6 (round 37, FWD-22): eight typed portal READ tools (json-tiered and the portal singletons) and five news READ tools",
       "# (the news DynamoDB tables and two portal singletons), Opal principals only. Each admits through app/typed_scope.admit_scope BEFORE any read."]
for mod, name, sig, call, audit, doc in TOOLS:
    blk += ["@mcp.tool()", "def %s(%s) -> dict:" % (name, sig), '    """%s"""' % doc,
            '    return _run("%s", %s, lambda t: %s.%s(%s))' % (name, audit, mod, name, call), "", ""]
anchor = '    return _run("harvest_get_peers_and_scores", {"security_key": security_key}, lambda t: _hvr.harvest_get_peers_and_scores(security_key))\n\n\n'
edit(APP + "tools.py", anchor, anchor + "\n".join(blk).rstrip("\n") + "\n\n\n")
# 2. the two name lists
tail = '    "harvest_get_peers_and_scores",\n})\n'
edit(APP + "data_entitlement.py", tail + "INTEGRATION_TOOLS",
     '    "harvest_get_peers_and_scores",\n'
     + "".join('    "%s",\n' % n for n in NAMES).replace('",\n', '",   # NFRA_OPLGTW G3 + G6 (FWD-22), read class, legacy: Opal principals only\n', 1)
     + "})\nINTEGRATION_TOOLS")
edit(APP + "destructive_ops.py", tail + "\n# The 5 mutating tools",
     '    "harvest_get_peers_and_scores",\n'
     + "".join('    "%s",\n' % n for n in NAMES).replace('",\n', '",   # NFRA_OPLGTW G3 + G6 (FWD-22): READ-ONLY typed reads, Opal principals only\n', 1)
     + "})\n\n# The 5 mutating tools")
# 3. the pinned counts
edit(TESTS + "test_entitlement_admin.py", "    assert len(registered_tool_names) == 75", "    assert len(registered_tool_names) == 88")
edit(TESTS + "test_entitlement_admin.py", "+ the ten G1 typed harvest tools (G1-TYPED, FWD-22): 75.",
     "+ the ten G1 typed harvest tools (G1-TYPED, FWD-22): 75, + the eight G3 portal tools and five G6 news tools (FWD-22): 88.")
edit(TESTS + "test_data_entitlement_family.py", "assert len(non_data) == 66 and", "assert len(non_data) == 79 and")
s = open(TESTS + "test_data_entitlement_family.py", encoding="utf-8").read()
assert "# discovery: all 66 non-data tools" in s and "the profile denies none of the 66" in s
s = s.replace("# discovery: all 66 non-data tools", "# discovery: all 79 non-data tools").replace("the profile denies none of the 66", "the profile denies none of the 79")
open(TESTS + "test_data_entitlement_family.py", "w", encoding="utf-8", newline="").write(s)
print("hookup applied: %d tools" % len(NAMES))
