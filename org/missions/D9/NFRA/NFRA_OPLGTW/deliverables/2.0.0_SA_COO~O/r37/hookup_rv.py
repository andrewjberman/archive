# -*- coding: utf-8 -*-
"""The issuer's batch hookup: the ten rival-funds tools (OG-rv-1: app/etfs_rivals.py, OG-rv-2: app/etfs_rivals_flow.py).
Usage: python hookup_rv.py <gateway-root>. Pins: registry 95 -> 105, non-data 86 -> 96."""
import sys

GW = sys.argv[1].rstrip("/")
APP, TESTS = GW + "/app/", GW + "/tests/"
# (module alias, tool name, signature, call args, audit args, doc)
TOOLS = [
    ("_rv1", "etfs_get_peer_group", "home_ticker: str", "home_ticker", '{"home_ticker": (home_ticker or "")[:8]}',
     "The peer group of one Opal home fund (IDVZ or PFOE): its rivals, from the rival-funds peer map; DIVZ and PFDE have none."),
    ("_rv1", "etfs_get_rival_fund_holdings", "fund_ticker: str, as_of: str = None", "fund_ticker, as_of",
     '{"fund_ticker": (fund_ticker or "")[:8], "as_of": as_of}',
     "What one fund of a rival-funds peer group holds on a report date, with identifiers and weights (fractions); the fund's own report date and lag are stated."),
    ("_rv1", "etfs_who_holds", "security: str, peer_group: str = None, as_of: str = None", "security, peer_group, as_of",
     '{"security": (security or "")[:64], "peer_group": peer_group, "as_of": as_of}',
     "Which rival-funds-group funds hold one security (ticker, Bloomberg id, CUSIP or ISIN) on a date, with weights."),
    ("_rv1", "etfs_get_security_reference", "security: str", "security", '{"security": (security or "")[:64]}',
     "The reference record of one security held by the rival funds: market data, corporate actions and names, each with its own date."),
    ("_rv1", "etfs_get_coverage", "fund_ticker: str = None", "fund_ticker", '{"fund_ticker": fund_ticker}',
     "The latest report date per rival-funds fund, read from the holdings themselves, with its lag in trading days and the reasons for a fund that is behind."),
    ("_rv2", "etfs_get_fund_trades", "fund_ticker: str = None, peer_group: str = None, from_date: str = None, to_date: str = None, action: str = None",
     "fund_ticker, peer_group, from_date, to_date, action",
     '{"fund_ticker": fund_ticker, "peer_group": peer_group, "from_date": from_date, "to_date": to_date, "action": action}',
     "The INFERRED trades of one rival-funds fund or of every fund of one peer group over a window, with the row's claim passed through."),
    ("_rv2", "etfs_get_fund_flows", "fund_ticker: str, from_date: str = None, to_date: str = None", "fund_ticker, from_date, to_date",
     '{"fund_ticker": (fund_ticker or "")[:8], "from_date": from_date, "to_date": to_date}',
     "The flow reconciliation of one rival-funds fund over a window (INFERRED)."),
    ("_rv2", "etfs_compare_peers", "home_ticker: str, period: str, axis: str", "home_ticker, period, axis",
     '{"home_ticker": (home_ticker or "")[:8], "period": period, "axis": axis}',
     "A home fund against its rival-funds peer group: buying trend and holding contribution for a period and an axis."),
    ("_rv2", "etfs_get_research_notes", "fund_ticker: str", "fund_ticker", '{"fund_ticker": (fund_ticker or "")[:8]}',
     "The AI-generated research notes of one rival-funds fund, each labelled with its model version and grounding."),
    ("_rv2", "etfs_get_rival_page_status", "page_day: str = None", "page_day", '{"page_day": page_day}',
     "What the PUBLISHED rival-funds page says (status, checks, per-fund latest report as published), beside the value in the holdings."),
]
NAMES = [t[1] for t in TOOLS]
assert len(NAMES) == 10


def edit(path, old, new, count=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == count, "%s: %r found %d times" % (path, old[:60], s.count(old))
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


imp = "from . import etfs_ownership as _eto, etfs_funds as _etf, portal_mdpf as _mdc   # NFRA_OPLGTW G5 wave A + G3 category views (FWD-22)"
edit(APP + "tools.py", imp, imp + "\nfrom . import etfs_rivals as _rv1, etfs_rivals_flow as _rv2   # NFRA_OPLGTW G5r rival funds (FWD-22)")
blk = ["# NFRA_OPLGTW G5r rival funds (round 37, FWD-22): ten READ tools over the rival-funds gold tables and the platinum page, Opal principals only.",
       "# Every key and bucket comes from the module's DATA_CATALOG table row at call time; each admits through app/typed_scope.admit_scope BEFORE any read."]
for mod, name, sig, call, audit, doc in TOOLS:
    blk += ["@mcp.tool()", "def %s(%s) -> dict:" % (name, sig), '    """%s"""' % doc,
            '    return _run("%s", %s, lambda t: %s.%s(%s))' % (name, audit, mod, name, call), "", ""]
anchor = '    return _run("mdpf_get_category_views", {"scope": (scope or "")[:32]}, lambda t: _mdc.mdpf_get_category_views(scope))\n\n\n'
edit(APP + "tools.py", anchor, anchor + "\n".join(blk).rstrip("\n") + "\n\n\n")
for f, why in (("data_entitlement.py", "read class, legacy: Opal principals only"), ("destructive_ops.py", "READ-ONLY, Opal principals only")):
    s = open(APP + f, encoding="utf-8").read()
    tail = '    "mdpf_get_category_views",'
    assert s.count(tail) == 1, f
    i = s.index(tail)
    j = s.index("\n", i)
    ins = "".join('\n    "%s",' % n for n in NAMES)
    ins = ins.replace('",', '",   # NFRA_OPLGTW G5r rival funds (FWD-22), %s' % why, 1)
    open(APP + f, "w", encoding="utf-8", newline="").write(s[:j] + ins + s[j:])
edit(TESTS + "test_entitlement_admin.py", "    assert len(registered_tool_names) == 95", "    assert len(registered_tool_names) == 105")
s = open(TESTS + "test_entitlement_admin.py", encoding="utf-8").read()
a = "the five G5 wave A etfs tools and mdpf_get_category_views: 95."
assert s.count(a) == 1
open(TESTS + "test_entitlement_admin.py", "w", encoding="utf-8", newline="").write(s.replace(a, a[:-1] + ", + the ten rival-funds tools: 105."))
edit(TESTS + "test_data_entitlement_family.py", "assert len(non_data) == 86 and", "assert len(non_data) == 96 and")
s = open(TESTS + "test_data_entitlement_family.py", encoding="utf-8").read()
assert "# discovery: all 86 non-data tools" in s and "the profile denies none of the 86" in s
s = s.replace("# discovery: all 86 non-data tools", "# discovery: all 96 non-data tools").replace("the profile denies none of the 86", "the profile denies none of the 96")
open(TESTS + "test_data_entitlement_family.py", "w", encoding="utf-8", newline="").write(s)
print("hookup applied: %d tools" % len(NAMES))
