#!/usr/bin/env python
"""OG-ap-28 Phase A step 2: take the round-38 batch into the release tree (bytes, no newline translation).

usage: python ap28_take.py <trunk_sha> <live_ref> <mcportal_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch2)

  WHOLE from trunk_sha: the 18 app/ref files the attribution run (ap28_attr.json) found fully attributable to the named orders (0 unattributable hunks), including
  app/refs/DATA_CATALOG.yaml (A1: MI's one emitted file), and every named test file that exists at trunk.
  NOT taken: app/tools.py, app/destructive_ops.py, the yearinreview files, the other unnamed differing files (the seam run found them satisfied by the base).
  BY HUNK against the LIVE script: deploy-to-ec2.sh gets ONE seventh reader key (BLACKDIAMOND49FLIVE_READER_ROLE_ARN), nothing else.
  The manifest: ONLY services.opal-gateway.mcportal_commit changes, by a one-value text replacement (no re-serialisation)."""
from __future__ import annotations

import json
import os
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch2"
TRUNK, LIVE, MCP, OUT = sys.argv[1:5]
G = "infra/aws/ec2/opal-gateway/"
APP = ["client_core", "client_role", "client_adapter_bd49f", "client_adapter_bdcottonwood", "client_adapter_commonwealth", "client_adapter_orion",
       "client_adapter_schwab", "client_adapter_smartx", "news_typed", "harvest_press", "data_entitlement", "server", "config", "query_v0", "ratelimit", "audit"]
TESTS = ["test_og_en4", "test_og_cl1", "test_og_cl2", "test_og_cl3", "test_og_cl4", "test_og_cl5", "test_og_cl6", "test_og_cl7", "test_og_cl8", "test_og_cl9",
         "test_og_en5", "test_og_nw1", "test_og_nw2", "test_og_nw3", "test_og_gt8", "test_og_en6", "test_og_hv1", "test_og_gt4", "test_og_gt5",
         "test_og_en8", "test_data_entitlement_family", "test_data_entitlement_guard", "test_entitlement_admin", "test_og_bd3", "test_og_ad1",
         "test_query_v0_tool", "test_og_en9", "test_graphql_catalog_gate", "test_portal_index_integration", "test_og_cat1",
         "test_og_en10", "test_ratelimit", "test_rate_limit", "test_server_guard", "test_og_en12", "test_client_role", "test_og_ch1",
         "test_og_gp1", "test_og_gf1", "test_og_ts1"]


def show(ref, path):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def put(path, data):
    full = os.path.join(TREE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as fh:
        fh.write(data)


taken, absent = [], []
paths = [G + "app/%s.py" % m for m in APP] + [G + "app/graphql_plumbing/catalog_gate.py", G + "app/refs/DATA_CATALOG.yaml"] + [G + "tests/%s.py" % t for t in TESTS]
for p in paths:
    d = show(TRUNK, p)
    if d is None:
        absent.append(p)
        continue
    put(p, d)
    taken.append(p)
print("taken whole from trunk: %d; named paths absent at trunk: %d" % (len(taken), len(absent)))
for a in absent:
    print("  ABSENT at trunk (named by an order, not a file): " + a.replace(G, ""))

# deploy-to-ec2.sh: the LIVE script plus the one seventh reader key
p = G + "deploy-to-ec2.sh"
b = show(LIVE, p)
anchor = b'READER_ARN_SMARTX="$(_vr_arn gateway-smartx-read-role)"\n'
assert b.count(anchor) == 1
b = b.replace(anchor, anchor + b'READER_ARN_BD49FLIVE="$(_vr_arn gateway-49f-blackdiamond-live-read-role)"\n')
fmt = b'SMARTX_READER_ROLE_ARN=%s\\n'          # a LITERAL backslash-n inside the printf format
assert b.count(fmt) == 1
b = b.replace(fmt, fmt + b'BLACKDIAMOND49FLIVE_READER_ROLE_ARN=%s\\n')
arg = b'"${READER_ARN_SMARTX}"'
assert b.count(arg) == 1
b = b.replace(arg, arg + b' "${READER_ARN_BD49FLIVE}"')
put(p, b)
taken.append(p)

# the manifest: one value, text replacement
mp = "infra/aws/ec2/EC2_MANIFEST.json"
m = show(LIVE, mp)
old = json.loads(m.decode("utf-8"))["services"]["opal-gateway"]["mcportal_commit"].encode("utf-8")
assert m.count(b'"mcportal_commit": "' + old + b'"') >= 1
sect = m.index(b'"opal-gateway"')
i = m.index(b'"mcportal_commit": "' + old + b'"', sect)
m2 = m[:i] + b'"mcportal_commit": "' + MCP.encode("utf-8") + b'"' + m[i + len(b'"mcportal_commit": "' + old + b'"'):]
put(mp, m2)
taken.append(mp)
print("manifest mcportal_commit %s -> %s" % (old.decode()[:10], MCP[:10]))
json.dump({"taken": taken, "absent_named": absent}, open(OUT, "w"), indent=1)
print("taken %d paths in all" % len(taken))
