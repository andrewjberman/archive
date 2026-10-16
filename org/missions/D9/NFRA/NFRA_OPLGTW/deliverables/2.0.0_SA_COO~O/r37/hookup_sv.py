# -*- coding: utf-8 -*-
"""The issuer's hookup for the json-served tool family (OG-sv-1, OG-sv-2): seven READ tools of app/portal_json_served.py.
Usage: python hookup_sv.py <gateway-root>.
Adds seven tools (portal_get_correlations, portal_get_etf_returns, portal_get_factor_tilts, portal_get_model_portfolio_timeseries,
portal_get_peer_performance, portal_get_trending, portal_get_cma_assumptions). Pins: registry 114 -> 121, non-data 105 -> 112."""
import sys

GW = sys.argv[1].rstrip("/")
APP, TESTS = GW + "/app/", GW + "/tests/"
TOOLS = [
    ("portal_get_correlations", 'window: str = ""', "window", '{"window": (window or "")[:16]}',
     "The correlation matrices of the portal's correlation object: with no window, the tickers and the window names; with one window, its matrix."),
    ("portal_get_etf_returns", "", "", "{}", "The ETF benchmark returns by period from the portal's returns object, with its own date and lag."),
    ("portal_get_factor_tilts", "part: str", "part", '{"part": (part or "")[:48]}',
     "One part of the portal's factor-tilt objects (the parts the catalog row names), with its own date and lag."),
    ("portal_get_model_portfolio_timeseries", "", "", "{}", "The daily model and benchmark return series, newest rows first, with its own date and lag."),
    ("portal_get_peer_performance", "", "", "{}", "The monthly peer percentile ranks by model and period; stale only when its month-end is earlier than the latest completed month-end."),
    ("portal_get_trending", "", "", "{}", "The bullish and bearish news topics of one date from the portal's trending object, with its own date and lag."),
    ("portal_get_cma_assumptions", "", "", "{}", "The capital-markets assumptions: one row per asset class of the annual edition the object names."),
]
NAMES = [t[0] for t in TOOLS]
assert len(NAMES) == 7


def edit(path, old, new, count=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == count, "%s: %r found %d times" % (path, old[:60], s.count(old))
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


edit(APP + "tools.py", "from . import client_core as _cc, portal_served as _ps, etfs_silver as _es   # NFRA_OPLGTW G2 client tools + remainders (FWD-22)",
     "from . import client_core as _cc, portal_served as _ps, etfs_silver as _es   # NFRA_OPLGTW G2 client tools + remainders (FWD-22)"
     "\nfrom . import portal_json_served as _pj   # NFRA_OPLGTW json-served tool family (FWD-22, PRD v3.13)")
blk = ["# NFRA_OPLGTW json-served tool family (round 37, FWD-22, PRD v3.13): seven READ tools of the portal-v2 json objects, Opal principals only.",
       "# Every bucket and prefix comes from the tool's DATA_CATALOG row at call time; each states its own date and freshness."]
for name, sig, call, audit, doc in TOOLS:
    blk += ["@mcp.tool()", "def %s(%s) -> dict:" % (name, sig), '    """%s"""' % doc,
            '    return _run("%s", %s, lambda t: _pj.%s(%s))' % (name, audit, name, call), "", ""]
anchor = '    return _run("etfs_get_fund_snapshot", {"fund_ticker": (fund_ticker or "")[:8], "as_of": as_of}, lambda t: _es.etfs_get_fund_snapshot(fund_ticker, as_of))\n\n\n'
edit(APP + "tools.py", anchor, anchor + "\n".join(blk).rstrip("\n") + "\n\n\n")
for f, why in (("data_entitlement.py", "read class, legacy: Opal principals only"), ("destructive_ops.py", "READ-ONLY, Opal principals only")):
    s = open(APP + f, encoding="utf-8").read()
    tail = '    "etfs_get_fund_snapshot",'
    assert s.count(tail) == 1, f
    i = s.index(tail)
    j = s.index("\n", i)
    ins = "".join('\n    "%s",' % n for n in NAMES)
    ins = ins.replace('",', '",   # NFRA_OPLGTW json-served tool family (FWD-22), %s' % why, 1)
    open(APP + f, "w", encoding="utf-8", newline="").write(s[:j] + ins + s[j:])
edit(TESTS + "test_entitlement_admin.py", "    assert len(registered_tool_names) == 114", "    assert len(registered_tool_names) == 121")
s = open(TESTS + "test_entitlement_admin.py", encoding="utf-8").read()
a = "three etfs silver tools: 114."
assert s.count(a) == 1
open(TESTS + "test_entitlement_admin.py", "w", encoding="utf-8", newline="").write(s.replace(a, a[:-1] + ", + the seven json-served portal tools: 121."))
edit(TESTS + "test_data_entitlement_family.py", "assert len(non_data) == 105 and", "assert len(non_data) == 112 and")
s = open(TESTS + "test_data_entitlement_family.py", encoding="utf-8").read()
assert "# discovery: all 105 non-data tools" in s and "the profile denies none of the 105" in s
s = s.replace("# discovery: all 105 non-data tools", "# discovery: all 112 non-data tools").replace("the profile denies none of the 105", "the profile denies none of the 112")
open(TESTS + "test_data_entitlement_family.py", "w", encoding="utf-8", newline="").write(s)
print("hookup applied: %d tools" % len(NAMES))
