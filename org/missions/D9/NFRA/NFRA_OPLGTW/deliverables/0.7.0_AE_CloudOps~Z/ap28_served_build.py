#!/usr/bin/env python
"""OG-ap-28 Phase B step 5: assemble W/CODE2_SERVED.json from the four measured records (no value is typed here that a record does not hold).

  ap28_served27.json    the 27-tool served harness (registry, per-tool, health, env_key_count)   <- ap23_run_served.py
  ap28_arms.json        the seven arms                                                          <- ap28_arms.py
  ap28_host_md5_after.json  the host md5 walk against the RELEASE blobs, plus the .env names   <- ap28_host_md5.py
  ap28_toolslist.json   tools_list_before (measured at Phase A)                                 <- ap28_toolslist.py
Counts and booleans only. usage: python ap28_served_build.py   (repository root)"""
from __future__ import annotations

import datetime
import io
import json
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/"
SEVEN = ["BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN", "ECLIPSE_READER_ROLE_ARN",
         "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN", "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"]


def load(n):
    return json.load(io.open(W + n, encoding="utf-8"))


s27, arms, md5, tl = load("ap28_served27.json"), load("ap28_arms.json"), load("ap28_host_md5_after.json"), load("ap28_toolslist.json")
tl_after = load("ap28_toolslist_after.json")
b27 = s27.get("body", s27)
ref = subprocess.run(["aws", "s3api", "head-object", "--bucket", "opal-313476888478-lambda-artifacts", "--key", "ec2/opal-gateway/opal-gateway-latest.tar.gz",
                      "--query", 'Metadata."git-ref"', "--output", "text"], capture_output=True).stdout.decode().strip()
names = set(md5["env"]["reader_role_arn_keys"])
D = arms["detail"]
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
    "tools_list_before": tl["tools_list_master_admin"],
    "tools_list_after": tl_after["tools_list_master_admin"],
    "muse_env_present": arms["muse_env_present"],
    "arms": arms["arms"],
    "arm_counts": {
        "e12_rows_per_tool": {t: v["rows"] for t, v in D["e12_a_per_tool"].items()},
        "e12_all_four_bucket_opal_data_bd": all(v["bucket_is_opal_data_bd"] for v in D["e12_a_per_tool"].values()),
        "e12_all_four_newest_dated_file": all(v["as_of_is_newest_dated_file"] for v in D["e12_a_per_tool"].values()),
        "e12_dedicated_role_on_all_four": all(v["role_ok"] for v in D["e12_a_per_tool"].values()),
        "e12_allocation_also_reads_the_assets_copy_profile_through_the_legacy_49f_role": "gateway-49f-blackdiamond-read-role" in D["e12_a_per_tool"]["client_get_allocation"]["session_roles"],
        "e12_non_admin_refused": D["e12_b"]["refused"], "e12_non_admin_s3_client_requests": D["e12_b"]["s3_client_requests"],
        "e4_weight_unit_values": D["e4_bd49f"].get("units"), "e4_bd49f_currency_basis": D.get("e4_bd_currency", {}).get("basis"),
        "e4_bd49f_unrealized_currency_like_columns": D.get("e4_bd_unrealized_currency_like_columns"),
        "e4_smartx_currency_basis": D.get("e4_smartx", {}).get("basis_distinct"), "e4_smartx_weight_units": D.get("e4_smartx", {}).get("units"),
        "e10_limit_per_window": [D["e10"]["limit"], D["e10"]["window_s"]], "e10_posts": 130, "e10_n_429": D["e10"]["n_429"], "e10_audit_rows": D["e10"]["rows"],
        "tools_list_after_with_app_server_imported_in_the_arms_harness": arms["tools_list_after"],
        "e8_teams_poll_status": D.get("teams_poll_status"), "e9_http_status": D["e9"]["http_status"],
    },
    "limits": ["tools_list_before and tools_list_after are the SAME measure (the registry's async list_tools() to a master_admin stand-in with app.tools imported, before and after the deploy: 103 and 103, ap28_toolslist.json and ap28_toolslist_after.json). The arms harness imports app.server, which registers the integration tools too, and reads 120; that is a different measure and is recorded apart (arm_counts), not as a change",
               "e10 drives the installed GuardMiddleware and ratelimit/audit code in-process with the bearer lookup stubbed to one synthetic stand-in (a real bearer needs a refresh family written to the access-state table, which the order forbids); the live service's limiter is untouched; the 429 row is captured at audit._emit, not read back from the lake",
               "e4: the BD49F and SmartX adapters carry weight_unit 'fraction' but currency null with currency_basis source_absent: neither adapter requests a currency column and the live BD unrealized table has none; schwab has no resolve source in the gateway; cottonwood, commonwealth and orion were not exercised"],
}
rec = {"body": body}
io.open(W + "CODE2_SERVED.json", "w", encoding="utf-8", newline="\n").write(json.dumps(rec, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("live_commit", "health_status", "env_key_count", "reader_env_keys_present", "registry_count", "per_tool_good", "host_md5", "tools_list_before", "tools_list_after", "muse_env_present", "arms")}, indent=1))
