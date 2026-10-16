#!/usr/bin/env python
"""OG-ap-31 Phase B step 5: assemble W/CODE3_SERVED.json from the measured records (no value is typed here that a record does not hold).

  ap31_served27.json          the 27-tool served harness (registry, per-tool, health, env_key_count)   <- ap23_run_served.py (OG-ap-23's, unchanged)
  ap31_arms.json              arms e1 to e4 on the host                                                <- ap31_arms.py
  ap31_e6_discover_buckets_host.txt   arm e6, the issuer's discover_buckets_host.sh output             <- 2.0.0_SA_COO~MI round18
  ap31_host_md5_after.json    the host md5 walk against the RELEASE blobs, plus the .env names          <- ap31_host_md5.py
  ap31_toolslist_phaseb.json / ap31_toolslist_after.json   tools_list before (at the GO) and after the deploy  <- ap31_toolslist.py
Counts and booleans only. usage: python ap31_served_build.py   (repository root of the worktree that holds the records)"""
from __future__ import annotations

import datetime
import io
import json
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
SEVEN = ["BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN", "ECLIPSE_READER_ROLE_ARN",
         "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN", "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"]


def load(n):
    return json.load(io.open(W + n, encoding="utf-8"))


s27, arms, md5 = load("ap31_served27.json"), load("ap31_arms.json"), load("ap31_host_md5_after.json")
tl_before, tl_after = load("ap31_toolslist_phaseb.json"), load("ap31_toolslist_after.json")
b27 = s27.get("body", s27)
e6txt = io.open(W + "ap31_e6_discover_buckets_host.txt", encoding="utf-8").read()
served = re.search(r"buckets served by plain words: (\d+) of (\d+)", e6txt)
echoed = re.search(r"buckets whose match echoes the bucket field: (\d+) of (\d+)", e6txt)
vf_lines = [ln for ln in e6txt.splitlines() if ln.startswith("BUCKET") and ("opal-data-assets" in ln.split()[1] or "opal-data-bd" in ln.split()[1])]
vf_ok = sum(1 for ln in vf_lines if "vendor_firm_echo=True" in ln)
e6 = bool(served and echoed and served.group(1) == served.group(2) and echoed.group(1) == echoed.group(2) and len(vf_lines) == 2 and vf_ok == 2
          and "RC=0" in e6txt and "health=200" in e6txt and "RESULT: PASS" in e6txt)
ref = subprocess.run(["aws", "s3api", "head-object", "--bucket", "opal-313476888478-lambda-artifacts", "--key", "ec2/opal-gateway/opal-gateway-latest.tar.gz",
                      "--query", 'Metadata."git-ref"', "--output", "text"], capture_output=True).stdout.decode().strip()
names = set(md5["env"]["reader_role_arn_keys"])
D = arms["detail"]
a = dict(arms["arms"])
a["e6_discover_echo"] = e6
body = {
    "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "live_commit": ref,
    "health_status": b27.get("health_status"),
    "env_key_count": md5["env"]["key_count"],
    "reader_env_keys_present": sum(1 for k in SEVEN if k in names),
    "registry_count": b27.get("registry_count"),
    "per_tool_good": b27.get("per_tool_good"),
    "host_md5": {"equal": md5["equal_lf"] + md5["equal_crlf_only"], "differ": len(md5["differ"]), "missing_on_host": len(md5["missing_on_host"]),
                 "expected_files": md5["denominator_expected_files"], "host_files": md5["denominator_host_files"]},
    "tools_list_before": tl_before["tools_list_master_admin"],
    "tools_list_after": tl_after["tools_list_master_admin"],
    "muse_env_present": bool(arms["muse_env_present"]) or bool(md5["env"]["muse_client_id_is_a_key"]),
    "arms": a,
    "arm_counts": {
        "e1": D["e1"], "e2": D["e2"],
        "e3": {k: {x: v[x] for x in ("string_figures", "float_exponents", "exponent_tokens_in_text", "weight_over_6", "money_over_2", "as_of_equals_partition_date")}
               for k, v in D["e3"].items()},
        "e4": D["e4"],
        "e6": {"buckets_served": served.group(0) if served else None, "buckets_echoing_bucket": echoed.group(0) if echoed else None,
               "assets_and_bd_vendor_firm_echoed": "%d of %d" % (vf_ok, len(vf_lines))},
        "no_identity_route_status": D["no_identity_route_status"],
    },
    "limits": ["e1 to e4 are read-only calls by an Opal master_admin stand-in built in-process from the host's roster key (a synthetic Opal-domain address), through the installed code on "
               "the host; one account that all four live 49F tables hold, resolved by the tool's own resolver. e4 uses a stand-in store that holds a deny record and writes nothing, and the "
               "LIVE access-state table for the non-admin address (a read).",
               "e6 is the issuer's discover_buckets_host.sh, unchanged, run once.",
               "tools_list_before is the master_admin stand-in's tools/list measured at the GO (ap31_toolslist_phaseb.json), tools_list_after the same measure after the deploy.",
               "/api/admin/gitstate answers 404 on this release (no such route registered), so it is not evidence for the existing-routes trigger; / , /gateway and /api/admin/people answer 401 to no identity."],
}
rec = {"body": body}
io.open(W + "CODE3_SERVED.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("live_commit", "health_status", "env_key_count", "reader_env_keys_present", "registry_count", "per_tool_good", "host_md5", "tools_list_before",
                                       "tools_list_after", "muse_env_present", "arms")}, indent=1))
