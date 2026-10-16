# -*- coding: utf-8 -*-
"""The issuer's hookup for the security-classification tool (OG-ac-2): one READ tool of app/mdpf_classification.py.
Usage: python hookup_ac.py <gateway-root>.
Adds mdpf_get_security_classification. Pins: registry 121 -> 122, non-data 112 -> 113."""
import sys

GW = sys.argv[1].rstrip("/")
APP, TESTS = GW + "/app/", GW + "/tests/"
NAME = "mdpf_get_security_classification"


def edit(path, old, new, count=1):
    s = open(path, encoding="utf-8").read()
    assert s.count(old) == count, "%s: %r found %d times" % (path, old[:60], s.count(old))
    open(path, "w", encoding="utf-8", newline="").write(s.replace(old, new))


imp = "from . import portal_json_served as _pj   # NFRA_OPLGTW json-served tool family (FWD-22, PRD v3.13)"
edit(APP + "tools.py", imp, imp + "\nfrom . import mdpf_classification as _mc   # NFRA_OPLGTW security-classification tool (FWD-22, named next increment)")
anchor = '    return _run("portal_get_cma_assumptions", {}, lambda t: _pj.portal_get_cma_assumptions())\n\n\n'
blk = ("# NFRA_OPLGTW security-classification tool (round 37, FWD-22): one READ tool of the DynamoDB etf-classifications table, Opal principals only.\n"
       "# One get_item by the hash key per call; the table read needs the gateway role's OG-ap-25 grant before it serves.\n"
       "@mcp.tool()\n"
       "def mdpf_get_security_classification(ticker: str = None, as_of: str = \"latest\") -> dict:\n"
       "    \"\"\"One security's classification (asset class, sub-asset class, who classified it, the model's confidence) by its ticker key, with the row's own date.\"\"\"\n"
       "    return _run(\"mdpf_get_security_classification\", {\"ticker\": (ticker or \"\")[:96], \"as_of\": as_of}, lambda t: _mc.mdpf_get_security_classification(ticker, as_of))\n\n\n")
edit(APP + "tools.py", anchor, anchor + blk)
for f, why in (("data_entitlement.py", "read class, legacy: Opal principals only"), ("destructive_ops.py", "READ-ONLY, Opal principals only")):
    s = open(APP + f, encoding="utf-8").read()
    tail = '    "portal_get_cma_assumptions",'
    assert s.count(tail) == 1, f
    i = s.index(tail)
    j = s.index("\n", i)
    ins = '\n    "%s",   # NFRA_OPLGTW security-classification tool (FWD-22), %s' % (NAME, why)
    open(APP + f, "w", encoding="utf-8", newline="").write(s[:j] + ins + s[j:])
edit(TESTS + "test_entitlement_admin.py", "    assert len(registered_tool_names) == 121", "    assert len(registered_tool_names) == 122")
s = open(TESTS + "test_entitlement_admin.py", encoding="utf-8").read()
a = "the seven json-served portal tools: 121."
assert s.count(a) == 1
open(TESTS + "test_entitlement_admin.py", "w", encoding="utf-8", newline="").write(s.replace(a, a[:-1] + ", + mdpf_get_security_classification: 122."))
edit(TESTS + "test_data_entitlement_family.py", "assert len(non_data) == 112 and", "assert len(non_data) == 113 and")
s = open(TESTS + "test_data_entitlement_family.py", encoding="utf-8").read()
assert "# discovery: all 112 non-data tools" in s and "the profile denies none of the 112" in s
s = s.replace("# discovery: all 112 non-data tools", "# discovery: all 113 non-data tools").replace("the profile denies none of the 112", "the profile denies none of the 113")
open(TESTS + "test_data_entitlement_family.py", "w", encoding="utf-8", newline="").write(s)
print("hookup applied: 1 tool")
