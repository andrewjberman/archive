# -*- coding: utf-8 -*-
"""The issuer's hookup for the published-analysis tool (OG-gt-5): harvest_get_published_analysis.
Usage: python hookup_gt5.py <gateway-root>. Pins: registry 88 -> 89, non-data 79 -> 80."""
import sys

GW = sys.argv[1].rstrip("/")
APP, TESTS = GW + "/app/", GW + "/tests/"
NAME = "harvest_get_published_analysis"


def edit(path, old, new, count=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == count, "%s: %r found %d times" % (path, old[:60], s.count(old))
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


imp = "from . import portal_models as _ptm, portal_macro as _ptc, news_typed as _nws   # NFRA_OPLGTW G3 + G6 (FWD-22)"
edit(APP + "tools.py", imp, imp + "\nfrom . import harvest_published as _hvpub   # NFRA_OPLGTW OG-gt-5 (FWD-22)")
anchor = '    return _run("news_for_security", {"security_key": security_key, "ticker": ticker}, lambda t: _nws.news_for_security(security_key, ticker, window_days))\n\n\n'
blk = ('# NFRA_OPLGTW OG-gt-5 (round 37, FWD-22): one READ tool that invokes the published-analysis Lambda (the function name is read from the .env key\n'
       '# AMGT_SCOPED_API_FUNCTION at call time); Opal principals only, admitted by app/harvest_typed.admit_typed BEFORE any invoke.\n'
       '@mcp.tool()\n'
       'def harvest_get_published_analysis(security_key: str, sections: str = "overlay") -> dict:\n'
       '    """The published body of one security section (overlay, thesis, peers, ledger, versions or timeline), projected to 50 KB, with as_of, source_keys, a denominator and absent_reason."""\n'
       '    return _run("harvest_get_published_analysis", {"security_key": security_key, "sections": sections}, lambda t: _hvpub.harvest_get_published_analysis(security_key, sections))\n\n\n')
edit(APP + "tools.py", anchor, anchor + blk)
edit(APP + "data_entitlement.py", '    "news_for_security",\n})\nINTEGRATION_TOOLS',
     '    "news_for_security",\n    "%s",   # NFRA_OPLGTW OG-gt-5 (FWD-22), read class, legacy: Opal principals only\n})\nINTEGRATION_TOOLS' % NAME)
edit(APP + "destructive_ops.py", '    "news_for_security",\n})\n\n# The 5 mutating tools',
     '    "news_for_security",\n    "%s",   # NFRA_OPLGTW OG-gt-5 (FWD-22): READ-ONLY, invokes the published-analysis Lambda, Opal principals only\n})\n\n# The 5 mutating tools' % NAME)
edit(TESTS + "test_entitlement_admin.py", "    assert len(registered_tool_names) == 88", "    assert len(registered_tool_names) == 89")
s = open(TESTS + "test_entitlement_admin.py", encoding="utf-8").read()
a = "five G6 news tools (FWD-22): 88."
assert s.count(a) == 1, "comment anchor"
open(TESTS + "test_entitlement_admin.py", "w", encoding="utf-8", newline="").write(s.replace(a, "five G6 news tools (FWD-22): 88, + OG-gt-5's harvest_get_published_analysis: 89."))
edit(TESTS + "test_data_entitlement_family.py", "assert len(non_data) == 79 and", "assert len(non_data) == 80 and")
s = open(TESTS + "test_data_entitlement_family.py", encoding="utf-8").read()
assert "# discovery: all 79 non-data tools" in s and "the profile denies none of the 79" in s
s = s.replace("# discovery: all 79 non-data tools", "# discovery: all 80 non-data tools").replace("the profile denies none of the 79", "the profile denies none of the 80")
open(TESTS + "test_data_entitlement_family.py", "w", encoding="utf-8", newline="").write(s)
print("hookup applied: 1 tool")
