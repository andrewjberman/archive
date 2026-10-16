#!/usr/bin/env python
"""OG-ap-23 Phase A step 2: take the batch into the release tree (bytes, no newline translation).
WHOLE from trunk_sha: the named modules, refs, lib, tests.  BY HUNK against the base: tools.py, destructive_ops.py,
data_entitlement.py (ADDITIVE hunks only -- trunk's OG-bd-3 logic hunks and cosmetic re-orders are NOT taken),
integration.py (live->trunk is exactly MX-c-22, so the trunk bytes ARE the hunk), the two pin tests, and the one
deploy-to-ec2.sh line.  Prints what it did, with counts."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

TREE = "C:/tmp/og-rel-code"
TRUNK = sys.argv[1]
LIVE = sys.argv[2]
G = "infra/aws/ec2/opal-gateway/"


def show(ref, path):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def put(path, data):
    full = os.path.join(TREE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as fh:
        fh.write(data)


def ls(ref, pre):
    return subprocess.run(["git", "ls-tree", "-r", "--name-only", ref, "--", pre],
                          capture_output=True).stdout.decode().split()


taken = []
whole = ["client_core", "client_role", "etfs_rivals", "etfs_rivals_flow", "etfs_silver", "portal_served",
         "portal_json_served", "admin_gateway_breakdown", "admin_people"]
whole += ["client_adapter_" + n for n in ("schwab", "bd49f", "orion", "eclipse", "bdcottonwood", "smartx", "commonwealth")]
paths = [G + "app/%s.py" % m for m in whole] + [G + "app/refs/partner_roster.json", "lib/opal_naming.py"]
cells = ("cl1", "cl2", "cl3", "cl4", "cl5", "cl6", "cl7", "cl8", "rv1", "rv2", "ch1", "gp1", "gf1", "sv1", "sv2")
for t in ls(TRUNK, G + "tests/"):
    b = t.rsplit("/", 1)[-1]
    if (b.startswith("test_og_") and b[8:-3] in cells) or b in (
            "test_admin_gateway_breakdown.py", "test_admin_people.py", "test_positioning_extension.py"):
        paths.append(t)
for p in paths:
    d = show(TRUNK, p)
    if d is None:
        print("ABSENT at trunk (named): " + p)
        continue
    put(p, d)
    taken.append(p)

# scopes.json: byte-equal copy of the registry at trunk_sha
sc = show(TRUNK, "infra/logic/registry/scopes.json")
put(G + "app/refs/scopes.json", sc)
taken.append(G + "app/refs/scopes.json")

# integration.py: live->trunk is exactly the MX-c-22 commit (checked by the caller), so trunk's bytes are the hunk
put(G + "app/integrations/portal_index/integration.py", show(TRUNK, G + "app/integrations/portal_index/integration.py"))
taken.append(G + "app/integrations/portal_index/integration.py")

# ---- the three additive files: start from the BASE bytes, add only what trunk adds ----
ADDED = ["etfs_get_peer_group_members", "etfs_get_rival_fund_holdings", "etfs_who_holds", "etfs_get_security_reference",
         "etfs_get_coverage", "etfs_get_fund_trades", "etfs_get_fund_flows", "etfs_compare_peers",
         "etfs_get_research_notes", "etfs_get_rival_page_status",
         "client_resolve_account", "client_get_holdings", "client_get_transactions", "client_get_allocation",
         "client_get_fees", "mdpf_get_model_composition", "etfs_get_new_securities",
         "etfs_get_fund_bloomberg_characteristics", "etfs_get_fund_snapshot",
         "portal_get_correlations", "portal_get_etf_returns", "portal_get_factor_tilts",
         "portal_get_model_portfolio_timeseries", "portal_get_peer_performance", "portal_get_trending",
         "portal_get_cma_assumptions"]

for fn in ("destructive_ops.py", "data_entitlement.py"):
    p = G + "app/" + fn
    base = show(LIVE, p).decode("utf-8")
    tr = show(TRUNK, p).decode("utf-8")
    # the block trunk adds = from the first added name's line through the last added name's line
    lines = tr.split("\n")
    first = next(i for i, ln in enumerate(lines) if '"etfs_get_peer_group_members"' in ln)
    last = next(i for i, ln in enumerate(lines) if '"portal_get_cma_assumptions"' in ln)
    block = "\n".join(lines[first:last + 1]) + "\n"
    assert block.count('"') // 2 >= len(ADDED)
    anchor = re.search(r'(?m)^[ \t]*"harvest_get_published_analysis",[^\n]*\n', base)
    assert anchor, fn
    out = base[:anchor.end()] + block + base[anchor.end():]
    put(p, out.encode("utf-8"))
    taken.append(p)

# tools.py
p = G + "app/tools.py"
base = show(LIVE, p).decode("utf-8")
tr = show(TRUNK, p).decode("utf-8")
imp_start = tr.index("from . import etfs_rivals as _rv1")
imp_end = tr.index("from .config import get_config")
imports = tr[imp_start:imp_end]
hv = re.search(r"(?m)^from \. import harvest_published as _hvpub[^\n]*\n", base)
assert hv
base = base[:hv.end()] + imports + base[hv.end():]
reg_start = tr.index("# NFRA_OPLGTW G5r rival funds (round 37, FWD-22): ten READ tools")
cma = tr.index("def portal_get_cma_assumptions()")
reg_end = tr.index("\n\n", tr.index("lambda t: _pj.portal_get_cma_assumptions()", cma)) + 1
registrations = tr[reg_start:reg_end]
hp = base.index("def harvest_get_published_analysis(")
hp_end = base.index("\n\n", base.index("_hvpub.harvest_get_published_analysis(security_key, sections))", hp)) + 1
base = base[:hp_end] + "\n\n" + registrations + base[hp_end:]
put(p, base.encode("utf-8"))
taken.append(p)

# the two pin tests: re-derived against the base, plus the added tools (86 -> 86+26, 95 -> 95+26)
K = len(ADDED)
for fn, old, new in (("test_data_entitlement_family.py", 86, 86 + K), ("test_entitlement_admin.py", 95, 95 + K)):
    p = G + "tests/" + fn
    b = show(LIVE, p).decode("utf-8")
    if fn == "test_data_entitlement_family.py":
        n = b.count("len(non_data) == %d " % old) + b.count("all %d non-data" % old) + b.count("denies none of the %d," % old)
        b = b.replace("len(non_data) == %d " % old, "len(non_data) == %d " % new)
        b = b.replace("all %d non-data" % old, "all %d non-data" % new)
        b = b.replace("denies none of the %d," % old, "denies none of the %d," % new)
    else:
        n = b.count("assert len(registered_tool_names) == %d" % old)
        b = b.replace("assert len(registered_tool_names) == %d" % old, "assert len(registered_tool_names) == %d" % new)
    print("  pin %s %d -> %d (%d spots)" % (fn, old, new, n))
    put(p, b.encode("utf-8"))
    taken.append(p)

# deploy-to-ec2.sh: ONE line, staging lib/opal_naming.py beside the calendar
p = G + "deploy-to-ec2.sh"
b = show(LIVE, p)
cal = b'cp "$WORKSPACE_ROOT/lib/trading_calendar.py" "$TMP/bundle/lib"\n'
assert b.count(cal) == 1
b = b.replace(cal, cal + b'cp "$WORKSPACE_ROOT/lib/opal_naming.py" "$TMP/bundle/lib"\n')
put(p, b)
taken.append(p)

print("taken %d paths" % len(taken))
json.dump(taken, open(sys.argv[3], "w"), indent=1)
