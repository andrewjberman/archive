# -*- coding: utf-8 -*-
"""The issuer's batch hookup: the five G5 wave A etfs tools (OG-et-1, OG-et-2) and mdpf_get_category_views (OG-pt-5).
Usage: python hookup_g5cv.py <gateway-root>. Pins: registry 89 -> 95, non-data 80 -> 86."""
import sys

GW = sys.argv[1].rstrip("/")
APP, TESTS = GW + "/app/", GW + "/tests/"
# (module alias, tool name, signature, call args, audit args, doc)
TOOLS = [
    ("_eto", "etfs_get_partner_ownership", "firm: str = None, as_of: str = None, etf_ticker: str = None", "firm, as_of, etf_ticker",
     '{"firm": (firm or "")[:32], "as_of": as_of, "etf_ticker": etf_ticker}',
     "How much of each Opal ETF ONE partner firm holds (firm required: 49financial, cottonwood or inflection), the newest file or the as_of date, optionally one ETF."),
    ("_eto", "etfs_get_ownership_rollup", "", "", "{}",
     "The ownership dashboard's own cross-partner totals with their as-of dates; it sums nothing."),
    ("_eto", "etfs_get_monthly_report", "month: str = None", "month", '{"month": month}',
     "Did the monthly ownership report go out and was it complete: coverage read from each partner's own csv."),
    ("_etf", "etfs_get_fund_nav_history", "fund_ticker: str, start: str = None, end: str = None", "fund_ticker, start, end",
     '{"fund_ticker": (fund_ticker or "")[:8], "start": start, "end": end}',
     "NAV, market price, shares outstanding and net assets for ONE Opal fund (DIVZ, IDVZ, PFDE or PFOE) over a date range."),
    ("_etf", "etfs_get_fund_holdings", "fund_ticker: str, as_of: str = None", "fund_ticker, as_of",
     '{"fund_ticker": (fund_ticker or "")[:8], "as_of": as_of}',
     "What one Opal fund holds on a date, with weights in percentage points."),
    ("_mdc", "mdpf_get_category_views", "scope: str", "scope", '{"scope": (scope or "")[:32]}',
     "Firm AUA by category (Models, SMA, Client, Alternatives, Insurance) for ONE scope: global, 49financial, cottonwood or inflection; global is its own object, never a sum."),
]
NAMES = [t[1] for t in TOOLS]
assert len(NAMES) == 6


def edit(path, old, new, count=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == count, "%s: %r found %d times" % (path, old[:60], s.count(old))
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


imp = "from . import harvest_published as _hvpub   # NFRA_OPLGTW OG-gt-5 (FWD-22)"
edit(APP + "tools.py", imp, imp + "\nfrom . import etfs_ownership as _eto, etfs_funds as _etf, portal_mdpf as _mdc   # NFRA_OPLGTW G5 wave A + G3 category views (FWD-22)")
blk = ["# NFRA_OPLGTW G5 wave A + G3 category views (round 37, FWD-22): five ETF READ tools and one firm-scoped portal READ tool, Opal principals only.",
       "# Every key and bucket comes from the module's DATA_CATALOG table row at call time; each admits through app/typed_scope.admit_scope BEFORE any read."]
for mod, name, sig, call, audit, doc in TOOLS:
    blk += ["@mcp.tool()", "def %s(%s) -> dict:" % (name, sig), '    """%s"""' % doc,
            '    return _run("%s", %s, lambda t: %s.%s(%s))' % (name, audit, mod, name, call), "", ""]
anchor = '    return _run("harvest_get_published_analysis", {"security_key": security_key, "sections": sections}, lambda t: _hvpub.harvest_get_published_analysis(security_key, sections))\n\n\n'
edit(APP + "tools.py", anchor, anchor + "\n".join(blk).rstrip("\n") + "\n\n\n")
tail = '    "harvest_get_published_analysis",'
s = open(APP + "data_entitlement.py", encoding="utf-8").read()
i = s.index(tail)
j = s.index("\n", i)
ins = "".join('\n    "%s",' % n for n in NAMES)
ins = ins.replace('",', '",   # NFRA_OPLGTW G5 wave A + G3 category views (FWD-22), read class, legacy: Opal principals only', 1)
open(APP + "data_entitlement.py", "w", encoding="utf-8", newline="").write(s[:j] + ins + s[j:])
s = open(APP + "destructive_ops.py", encoding="utf-8").read()
i = s.index(tail)
j = s.index("\n", i)
ins = "".join('\n    "%s",' % n for n in NAMES)
ins = ins.replace('",', '",   # NFRA_OPLGTW G5 wave A + G3 category views (FWD-22): READ-ONLY, Opal principals only', 1)
open(APP + "destructive_ops.py", "w", encoding="utf-8", newline="").write(s[:j] + ins + s[j:])
edit(TESTS + "test_entitlement_admin.py", "    assert len(registered_tool_names) == 89", "    assert len(registered_tool_names) == 95")
s = open(TESTS + "test_entitlement_admin.py", encoding="utf-8").read()
a = "+ OG-gt-5's harvest_get_published_analysis: 89."
assert s.count(a) == 1
open(TESTS + "test_entitlement_admin.py", "w", encoding="utf-8", newline="").write(s.replace(a, a[:-1] + ", + the five G5 wave A etfs tools and mdpf_get_category_views: 95."))
edit(TESTS + "test_data_entitlement_family.py", "assert len(non_data) == 80 and", "assert len(non_data) == 86 and")
s = open(TESTS + "test_data_entitlement_family.py", encoding="utf-8").read()
assert "# discovery: all 80 non-data tools" in s and "the profile denies none of the 80" in s
s = s.replace("# discovery: all 80 non-data tools", "# discovery: all 86 non-data tools").replace("the profile denies none of the 80", "the profile denies none of the 86")
open(TESTS + "test_data_entitlement_family.py", "w", encoding="utf-8", newline="").write(s)
print("hookup applied: %d tools" % len(NAMES))
