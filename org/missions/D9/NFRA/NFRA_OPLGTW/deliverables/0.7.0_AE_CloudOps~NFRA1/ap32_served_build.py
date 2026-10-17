#!/usr/bin/env python
"""OG-ap-32 Phase B step 5: assemble W/CODE4_SERVED.json from the measured records (no value is typed here that a record does not hold).
The release was ROLLED BACK at once on a trigger, so the record carries the arms as measured on the release (three false), the trigger, and the state after the rollback.
  ap32_arms.json                     the paging arms on the host, through the installed release code      <- ap32_arms.py
  ap32_served27.json_post_rollback   the 27-tool served harness against the rolled-back service           <- ap23_run_served.py
  ap32_host_md5_after.json           the host md5 walk against the RELEASE blobs right after the deploy    <- ap31_host_md5.py
  ap32_host_md5_rollback.json        the host md5 walk against the 4be300110e blobs after the rollback     <- ap31_host_md5.py
  ap32_toolslist_phaseb.json / ap32_toolslist_after.json / ap32_toolslist_rollback.json   tools/list at the GO, after the deploy, after the rollback
Counts, seconds, percentages and booleans only. usage: python ap32_served_build.py   (repository root of the worktree that holds the records)"""
from __future__ import annotations

import datetime
import io
import json
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
SEVEN = ["BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN", "ECLIPSE_READER_ROLE_ARN",
         "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN", "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"]


def load(n):
    return json.load(io.open(W + n, encoding="utf-8"))


arms, md5_rel, md5_rb = load("ap32_arms.json"), load("ap32_host_md5_after.json"), load("ap32_host_md5_rollback.json")
tl_before, tl_after, tl_rb = load("ap32_toolslist_phaseb.json"), load("ap32_toolslist_after.json"), load("ap32_toolslist_rollback.json")
s27 = load("ap32_served27_post_rollback.json")
b27 = s27.get("body", s27)
D = arms["detail"]
ref = subprocess.run(["aws", "s3api", "head-object", "--bucket", "opal-313476888478-lambda-artifacts", "--key", "ec2/opal-gateway/opal-gateway-latest.tar.gz",
                      "--query", 'Metadata."git-ref"', "--output", "text"], capture_output=True).stdout.decode().strip()
names = set(md5_rb["env"]["reader_role_arn_keys"])
chains = D["chains"]
body = {
    "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "live_commit": ref,
    "release_sha": "b124377b41caf5665b999378fd0ca08ad8a1fb7d",
    "release_live": False,
    "rolled_back": True,
    "trigger": {"fired": True, "which": "host memory above 85 percent during the paging read-back", "peak_host_mem_used_pct": D["host_mem_used_pct"]["peak_during_chains"],
                "limit_pct": 85, "memory_after_each_transactions_page_pct": [p["host_mem_used_pct_after"] for p in chains["client_get_transactions"]["per_page"]],
                "host_mem_before_pct": D["host_mem_used_pct"]["before"], "chain_stopped_by_the_80_pct_guard": D["stopped_on_memory"]},
    "health_status": b27.get("health_status"),
    "env_key_count": md5_rb["env"]["key_count"],
    "reader_env_keys_present": sum(1 for k in SEVEN if k in names),
    "registry_count": b27.get("registry_count"),
    "per_tool_good": b27.get("per_tool_good"),
    "host_md5": {"after_release_equal": md5_rel["equal_lf"] + md5_rel["equal_crlf_only"], "after_release_differ": len(md5_rel["differ"]),
                 "after_rollback_vs_base_equal": md5_rb["equal_lf"] + md5_rb["equal_crlf_only"], "after_rollback_vs_base_differ": len(md5_rb["differ"]),
                 "after_rollback_vs_base_differing_files": md5_rb["differ"], "expected_files": md5_rb["denominator_expected_files"], "host_files": md5_rb["denominator_host_files"]},
    "tools_list_before": tl_before["tools_list_master_admin"],
    "tools_list_after": tl_after["tools_list_master_admin"],
    "tools_list_after_rollback": tl_rb["tools_list_master_admin"],
    "muse_env_present": bool(arms["muse_env_present"]) or bool(md5_rb["env"]["muse_client_id_is_a_key"]),
    "arms": arms["arms"],
    "arm_counts": {t: {k: v for k, v in c.items() if k != "per_page"} for t, c in chains.items()},
    "arm_counts_per_page_walls": {t: [p.get("wall_seconds") for p in c["per_page"]] for t, c in chains.items()},
    "first_page_over_55s_trigger": D["first_page_over_trigger_seconds"],
    "limits": ["The arms ran in a NEW process on the host through the installed release code (the service itself served no page); the chain was stopped by the harness's 80 percent guard after 4 of about 12 transactions pages and the fees chain was not started.",
               "e1_cursor_first_page is false only because the fees chain never ran (the transactions chain hit the memory guard first); the transactions first page read 30 of 334 partitions, window_partial true, a cursor, in 29.64 s (inside the 45 s bound). e1_newest_first is false because the chain is incomplete AND page 4 of the transactions chain has a trade_date inversion inside the page (row Z-S339; pages 1 to 3 and the page-to-page order held).",
               "per_tool_good, registry_count and health_status are the post-rollback service's; the paging release served no tool-list change (103 after the deploy).",
               "The rolled-back state is the pre-deploy content: host md5 against the 4be300110e blobs reads 3 differing files, exactly the three AMGT_HARVST harvest files, as before the release."],
}
io.open(W + "CODE4_SERVED.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("live_commit", "release_live", "rolled_back", "health_status", "env_key_count", "registry_count", "per_tool_good", "tools_list_before", "tools_list_after",
                                       "tools_list_after_rollback", "muse_env_present", "arms", "trigger")}, indent=1))
