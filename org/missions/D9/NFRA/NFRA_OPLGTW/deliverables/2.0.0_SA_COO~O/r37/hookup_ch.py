# -*- coding: utf-8 -*-
"""The issuer's batch hookup for the G2 client tools and the remainders (OG-cl-1..6, OG-gp-1, OG-gf-1).
Usage: python hookup_ch.py <gateway-root> <repo-root>.
Adds nine tools: the five client_* tools (app/client_core.py, seven adapters registered at import), mdpf_get_model_composition
(app/portal_served.py) and the three etfs silver tools (app/etfs_silver.py). Pins: registry 105 -> 114, non-data 96 -> 105.
Copies data/mdpf/config/partner_roster.json byte-equal to app/refs/ (the core's ROSTER_FILE)."""
import os
import shutil
import sys

GW = sys.argv[1].rstrip("/")
REPO = sys.argv[2].rstrip("/")
APP, TESTS = GW + "/app/", GW + "/tests/"
ADAPTERS = ["bd49f", "bdcottonwood", "eclipse", "orion", "schwab", "commonwealth", "smartx"]
# (module alias, tool name, signature, call args, audit args, doc)   -- an account ref is audited as its masked first 8 chars only
TOOLS = [
    ("_cc", "client_resolve_account", "firm: str, account_last4: str, platform: str = None, as_of: str = None",
     "firm, account_last4, platform, as_of",
     '{"firm": (firm or "")[:32], "platform": platform, "as_of": as_of}',
     "Resolve the last four digits of a client account to its candidate accounts at one firm, across the firm's custodial and reporting platforms; candidates carry a masked account_ref, never a full number."),
    ("_cc", "client_get_holdings", "firm: str, account: str, platform: str = None, as_of: str = None", "firm, account, platform, as_of",
     '{"firm": (firm or "")[:32], "account": (account or "")[:8], "platform": platform, "as_of": as_of}',
     "The positions and cash of one client account (an account_ref from client_resolve_account) on the newest partition at or before as_of."),
    ("_cc", "client_get_transactions", "firm: str, account: str, platform: str = None, from_date: str = None, to_date: str = None",
     "firm, account, platform, from_date, to_date",
     '{"firm": (firm or "")[:32], "account": (account or "")[:8], "platform": platform, "from_date": from_date, "to_date": to_date}',
     "The transactions of one client account over a window of at most 13 months."),
    ("_cc", "client_get_allocation", "firm: str, account: str, platform: str = None, as_of: str = None", "firm, account, platform, as_of",
     '{"firm": (firm or "")[:32], "account": (account or "")[:8], "platform": platform, "as_of": as_of}',
     "The allocation of one client account, with its model assignment where the platform serves one, and the partition lag in trading days."),
    ("_cc", "client_get_fees", "firm: str, account: str, platform: str = None, from_date: str = None, to_date: str = None",
     "firm, account, platform, from_date, to_date",
     '{"firm": (firm or "")[:32], "account": (account or "")[:8], "platform": platform, "from_date": from_date, "to_date": to_date}',
     "The fee rows of one client account over a window of at most 13 months, or the platform's refusal where it serves no fee source."),
    ("_ps", "mdpf_get_model_composition", "scope: str, model_key: str = \"\"", "scope, model_key",
     '{"scope": (scope or "")[:32], "model_key": (model_key or "")[:64]}',
     "The composition of one portfolio model (its sleeves and weights) for one scope, from the served portfolio tables."),
    ("_es", "etfs_get_new_securities", "as_of: str = None", "as_of", '{"as_of": as_of}',
     "The securities new to the ETF holdings on a report date, with the date each first appeared."),
    ("_es", "etfs_get_fund_bloomberg_characteristics", "fund_ticker: str, as_of: str = None", "fund_ticker, as_of",
     '{"fund_ticker": (fund_ticker or "")[:8], "as_of": as_of}',
     "The Bloomberg characteristics of one ETF (a fund-level reference record), with its own date."),
    ("_es", "etfs_get_fund_snapshot", "fund_ticker: str, as_of: str = None", "fund_ticker, as_of",
     '{"fund_ticker": (fund_ticker or "")[:8], "as_of": as_of}',
     "The point-in-time snapshot of one ETF from the silver tables, with its own date."),
]
NAMES = [t[1] for t in TOOLS]
assert len(NAMES) == 9


def edit(path, old, new, count=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == count, "%s: %r found %d times" % (path, old[:60], s.count(old))
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


imp = "from . import etfs_rivals as _rv1, etfs_rivals_flow as _rv2   # NFRA_OPLGTW G5r rival funds (FWD-22)"
mods = ", ".join("client_adapter_%s as _ca_%s" % (a, a) for a in ADAPTERS)
new_imp = (imp + "\nfrom . import client_core as _cc, portal_served as _ps, etfs_silver as _es   # NFRA_OPLGTW G2 client tools + remainders (FWD-22)"
           "\nfrom . import " + mods)
# The register loop goes AFTER every import (ruff E402), just before the first new tool block.
LOOP = "for _adapter_mod in (" + ", ".join("_ca_%s" % a for a in ADAPTERS) + "):\n    _cc.register_adapter(_adapter_mod)"
edit(APP + "tools.py", imp, new_imp)
blk = ["# Register the seven client adapters once, after every import (E402).", LOOP, "",
       "# NFRA_OPLGTW G2 client tools and remainders (round 37, FWD-22): nine READ tools, Opal principals only.",
       "# Every key and bucket comes from the module's DATA_CATALOG row at call time; the client tools admit through the client surface before any read."]
for mod, name, sig, call, audit, doc in TOOLS:
    blk += ["@mcp.tool()", "def %s(%s) -> dict:" % (name, sig), '    """%s"""' % doc,
            '    return _run("%s", %s, lambda t: %s.%s(%s))' % (name, audit, mod, name, call), "", ""]
anchor = '    return _run("etfs_get_rival_page_status", {"page_day": page_day}, lambda t: _rv2.etfs_get_rival_page_status(page_day))\n\n\n'
edit(APP + "tools.py", anchor, anchor + "\n".join(blk).rstrip("\n") + "\n\n\n")
for f, why in (("data_entitlement.py", "read class, legacy: Opal principals only"), ("destructive_ops.py", "READ-ONLY, Opal principals only")):
    s = open(APP + f, encoding="utf-8").read()
    tail = '    "etfs_get_rival_page_status",'
    assert s.count(tail) == 1, f
    i = s.index(tail)
    j = s.index("\n", i)
    ins = "".join('\n    "%s",' % n for n in NAMES)
    ins = ins.replace('",', '",   # NFRA_OPLGTW G2 client tools + remainders (FWD-22), %s' % why, 1)
    open(APP + f, "w", encoding="utf-8", newline="").write(s[:j] + ins + s[j:])
edit(TESTS + "test_entitlement_admin.py", "    assert len(registered_tool_names) == 105", "    assert len(registered_tool_names) == 114")
s = open(TESTS + "test_entitlement_admin.py", encoding="utf-8").read()
a = "the ten rival-funds tools: 105."
assert s.count(a) == 1
open(TESTS + "test_entitlement_admin.py", "w", encoding="utf-8", newline="").write(s.replace(a, a[:-1] + ", + the five client tools, mdpf_get_model_composition and three etfs silver tools: 114."))
edit(TESTS + "test_data_entitlement_family.py", "assert len(non_data) == 96 and", "assert len(non_data) == 105 and")
s = open(TESTS + "test_data_entitlement_family.py", encoding="utf-8").read()
assert "# discovery: all 96 non-data tools" in s and "the profile denies none of the 96" in s
s = s.replace("# discovery: all 96 non-data tools", "# discovery: all 105 non-data tools").replace("the profile denies none of the 96", "the profile denies none of the 105")
open(TESTS + "test_data_entitlement_family.py", "w", encoding="utf-8", newline="").write(s)
os.makedirs(APP + "refs", exist_ok=True)
shutil.copyfile(REPO + "/data/mdpf/config/partner_roster.json", APP + "refs/partner_roster.json")
print("hookup applied: %d tools, %d adapters" % (len(NAMES), len(ADAPTERS)))
