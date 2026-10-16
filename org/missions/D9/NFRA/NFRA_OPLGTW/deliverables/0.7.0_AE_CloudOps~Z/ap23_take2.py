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
whole.append("mdpf_classification")   # A2: the security-classification tool (OG-ac-2)
whole.append("data_entitlement")      # A7: WHOLE from trunk_sha (OG-bd-3's decide() branch and tier lines, OG-ad-1's client admission)
paths = [G + "app/%s.py" % m for m in whole] + ["lib/opal_naming.py"]   # A2: the roster and the registry copy are NOT committed
cells = ("cl1", "cl2", "cl3", "cl4", "cl5", "cl6", "cl7", "cl8", "rv1", "rv2", "ch1", "gp1", "gf1", "sv1", "sv2", "ac2", "ad1", "bd3")
for t in ls(TRUNK, G + "tests/"):
    b = t.rsplit("/", 1)[-1]
    if (b.startswith("test_og_") and b[8:-3] in cells) or b in (
            "test_admin_gateway_breakdown.py", "test_admin_people.py", "test_positioning_extension.py",
            # A7: data_entitlement.py is whole from trunk (OG-bd-3, and OG-ad-1 moving the client tools out of NATIVE_TOOLS into
            # CLIENT_TOOLS), so the four tests that pin that module's membership are taken whole as well: their follow-ups are trunk's own
            "test_entitlement_admin.py", "test_data_entitlement_family.py", "test_data_entitlement_guard.py", "test_og_bd2.py"):
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
# UNTRACKED, tests only (A2): the deploy script stages both at bundle time, so neither is committed
put(G + "app/refs/partner_roster.json", show(TRUNK, "data/mdpf/config/partner_roster.json"))

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
         "portal_get_cma_assumptions", "mdpf_get_security_classification"]

for fn in ("destructive_ops.py",):   # A7: data_entitlement.py is taken WHOLE (above), it carries OG-bd-3 and OG-ad-1
    p = G + "app/" + fn
    base = show(LIVE, p).decode("utf-8")
    tr = show(TRUNK, p).decode("utf-8")
    # the block trunk adds = from the first added name's line through the last added name's line
    lines = tr.split("\n")
    first = next(i for i, ln in enumerate(lines) if '"etfs_get_peer_group_members"' in ln)
    last = next(i for i, ln in enumerate(lines) if '"mdpf_get_security_classification"' in ln)
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
cma = tr.index("def mdpf_get_security_classification(")
reg_end = tr.index("\n\n", tr.index("_mc.mdpf_get_security_classification(ticker, as_of))", cma)) + 1
registrations = tr[reg_start:reg_end]
hp = base.index("def harvest_get_published_analysis(")
hp_end = base.index("\n\n", base.index("_hvpub.harvest_get_published_analysis(security_key, sections))", hp)) + 1
base = base[:hp_end] + "\n\n" + registrations + base[hp_end:]
put(p, base.encode("utf-8"))
taken.append(p)

# the two pin tests: re-derived against the base, plus the added tools (86 -> 86+26, 95 -> 95+26)
K = len(ADDED)
# non_data = registered tools outside DATA_GRANT_TOOLS: the 27 added, less the 5 client_* tools that PRD v3.14 puts in the data-grant family
for fn, old, new in ():   # A7: the two pin tests are now taken whole above (their pins are trunk's: 108 and 122)
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

# deploy-to-ec2.sh: the staging hunk only (A2): opal_naming, the roster and the registry copy ship from their repo sources
p = G + "deploy-to-ec2.sh"
b = show(LIVE, p)
cal = b'cp "$WORKSPACE_ROOT/lib/trading_calendar.py" "$TMP/bundle/lib"\n'
assert b.count(cal) == 1
stage = (
    b'# NFRA_OPLGTW OG-ap-23 (A2): lib/opal_naming.py, the partner roster and the registry copy ship from their repo sources, never as committed data copies.\n'
    b'for _stage_src in lib/opal_naming.py data/mdpf/config/partner_roster.json infra/logic/registry/scopes.json; do\n'
    b'    if [ ! -f "$WORKSPACE_ROOT/$_stage_src" ]; then\n'
    b'        echo "ERROR: REFUSED (no upload): ${_stage_src} is missing from the repo at ${WORKSPACE_ROOT} -- the artifact would ship without it." >&2\n'
    b'        exit 1\n'
    b'    fi\n'
    b'done\n'
    b'mkdir -p "$TMP/bundle/app/refs"\n'
    b'cp "$WORKSPACE_ROOT/lib/opal_naming.py" "$TMP/bundle/lib"\n'
    b'cp "$WORKSPACE_ROOT/data/mdpf/config/partner_roster.json" "$TMP/bundle/app/refs/partner_roster.json"\n'
    b'cp "$WORKSPACE_ROOT/infra/logic/registry/scopes.json" "$TMP/bundle/app/refs/scopes.json"\n'
    b'\n'
    b'# NFRA_OPLGTW OG-ap-23 (A3, Phase A gap 1): the six vendor reader role ARNs the client tools assume (app/client_role.py role_env_name).\n'
    b'# A role ARN is not a secret. Each one is READ from IAM, never typed, and a role that does not resolve REFUSES the deploy before any upload.\n'
    b'_vr_account="$(aws sts get-caller-identity --query Account --output text | tr -d \'\\r\')" \\\n'
    b'    || { echo "ERROR: REFUSED (no upload): the AWS account could not be resolved for the vendor reader roles." >&2; exit 1; }\n'
    b'_vr_arn() {\n'
    b'    _a="$(aws iam get-role --role-name "$1" --query Role.Arn --output text 2>/dev/null | tr -d \'\\r\')" || _a=""\n'
    b'    if [ "$_a" != "arn:aws:iam::${_vr_account}:role/$1" ]; then\n'
    b'        echo "ERROR: REFUSED (no upload): vendor reader role $1 did not resolve to its expected ARN in the account." >&2; return 1\n'
    b'    fi\n'
    b'    printf \'%s\' "$_a"\n'
    b'}\n'
    b'READER_ARN_BD49F="$(_vr_arn gateway-49f-blackdiamond-read-role)"\n'
    b'READER_ARN_BDCOTTONWOOD="$(_vr_arn gateway-cot-blackdiamond-read-role)"\n'
    b'READER_ARN_ORION="$(_vr_arn gateway-inf-orion-read-role)"\n'
    b'READER_ARN_ECLIPSE="$(_vr_arn gateway-inf-eclipse-read-role)"\n'
    b'READER_ARN_COMMONWEALTH="$(_vr_arn gateway-cot-commonwealth-read-role)"\n'
    b'READER_ARN_SMARTX="$(_vr_arn gateway-smartx-read-role)"\n')
b = b.replace(cal, cal + stage)
# the six keys in the .env the script rebuilds: six %s placed BEFORE the two ADVI roots (the ab1/ab2 tests pin the market-update
# argument second-to-last and the fee-statement argument last), with the six arguments in the same place in the argument list
fmt_head = b'ADVI_MARKET_UPDATE_S3_ROOT=%s\\n'   # the deploy script's printf carries a LITERAL backslash-n, not a newline
assert b.count(fmt_head) == 1
b = b.replace(fmt_head, b'BLACKDIAMOND49F_READER_ROLE_ARN=%s\\nBLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN=%s\\nORION_READER_ROLE_ARN=%s\\n'
              b'ECLIPSE_READER_ROLE_ARN=%s\\nCOMMONWEALTH_READER_ROLE_ARN=%s\\nSMARTX_READER_ROLE_ARN=%s\\n' + fmt_head)
arg_head = b'"${ADVI_MARKET_UPDATE_S3_ROOT}" "${ADVI_FEE_STATEMENT_S3_ROOT}" | sudo -u ec2-user tee'
assert b.count(arg_head) == 1
b = b.replace(arg_head, b'"${READER_ARN_BD49F}" "${READER_ARN_BDCOTTONWOOD}" "${READER_ARN_ORION}" "${READER_ARN_ECLIPSE}" '
              b'"${READER_ARN_COMMONWEALTH}" "${READER_ARN_SMARTX}" ' + arg_head)
# the tar line (the CTO's refusal, msg 34788): the staged app/refs copies ship FROM THE BUNDLE and the same two names are excluded from
# the $SRC side. GNU tar --exclude is cumulative from where it appears, so the bundle group goes FIRST and the two excludes sit between
# the groups; the existing excludes stay ahead of both groups and so still apply to both (tested: one entry per name, bundle content).
tar_old = (b'tar -czf "$TMP/$ART" -C "$SRC" \\\n'
           b"    --exclude='.env' --exclude='audit.jsonl' --exclude='*.log' --exclude='__pycache__' \\\n"
           b"    --exclude='.token_cache' --exclude='infra' --exclude='dev_smoke.py' --exclude='make_diagram.py' \\\n"
           b'    app deploy requirements.txt identity_tool_allowlist.txt \\\n'
           b'    -C "$TMP/bundle" "$DASHBOARD_BUNDLE_DIR" lib\n')
assert b.count(tar_old) == 1
tar_new = (b'tar -czf "$TMP/$ART" -C "$TMP/bundle" \\\n'
           b"    --exclude='.env' --exclude='audit.jsonl' --exclude='*.log' --exclude='__pycache__' \\\n"
           b"    --exclude='.token_cache' --exclude='infra' --exclude='dev_smoke.py' --exclude='make_diagram.py' \\\n"
           b'    "$DASHBOARD_BUNDLE_DIR" lib app/refs/partner_roster.json app/refs/scopes.json \\\n'
           b"    --exclude='app/refs/partner_roster.json' --exclude='app/refs/scopes.json' \\\n"
           b'    -C "$SRC" app deploy requirements.txt identity_tool_allowlist.txt\n')
b = b.replace(tar_old, tar_new)
put(p, b)
taken.append(p)

print("taken %d paths" % len(taken))
json.dump(taken, open(sys.argv[3], "w"), indent=1)
