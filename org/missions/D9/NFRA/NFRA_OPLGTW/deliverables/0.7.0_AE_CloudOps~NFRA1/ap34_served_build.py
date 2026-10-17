#!/usr/bin/env python
"""OG-ap-34 Phase B step 6: assemble W/CODE5_SERVED.json from the measured records (no value is typed here that a record does not hold).

  ap34_served27.json          the 27-tool served harness                                 <- ap23_run_served.py (OG-ap-23's, unchanged)
  ap34_arms.json              the paging arms through the installed code, new process    <- ap34_arms.py
  ap34_host_md5_after.json    the host md5 walk against the RELEASE blobs plus .env names <- ap31_host_md5.py
  ap34b_toolslist.json / ap34_toolslist_after.json   tools/list before (at the GO) and after the deploy <- ap31_toolslist.py
  CHAIN_PRE.json              the CT1 pre-deploy plateau test (two full chains, one fresh process)
  ap34_readback.jsonl         the 30-minute service read-back, one probe a minute (+ .trigger if any)
  ap34_wincalls.json          the /mcp calls and window calls the service served in the read-back window
Counts, seconds, percentages, dates and booleans only. usage: python ap34_served_build.py   (repository root of the worktree that holds the records)"""
from __future__ import annotations

import datetime
import io
import json
import os
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
SEVEN = ["BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN", "ECLIPSE_READER_ROLE_ARN",
         "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN", "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"]
SHIM = os.path.join(".tools", "aws.cmd" if os.name == "nt" else "aws")


def load(n):
    return json.load(io.open(W + n, encoding="utf-8"))


s27, arms, md5 = load("ap34_served27.json"), load("ap34_arms.json"), load("ap34_host_md5_after.json")
tl_before, tl_after = load("ap34b_toolslist.json"), load("ap34_toolslist_after.json")
chain_pre, wincalls = load("CHAIN_PRE.json")["body"], load("ap34_wincalls.json")
b27 = s27.get("body", s27)
rb = [json.loads(ln) for ln in io.open(W + "ap34_readback.jsonl", encoding="utf-8") if ln.strip()]
trigger_file = W + "ap34_readback.jsonl.trigger"
triggers = io.open(trigger_file, encoding="utf-8").read().splitlines() if os.path.exists(trigger_file) else []
baseline = load("ap34_baseline.json")
ref = subprocess.run([SHIM, "s3api", "head-object", "--bucket", "opal-313476888478-lambda-artifacts", "--key", "ec2/opal-gateway/opal-gateway-latest.tar.gz",
                      "--query", 'Metadata."git-ref"', "--output", "text"], capture_output=True).stdout.decode().strip()
names = set(md5["env"]["reader_role_arn_keys"])
D = arms["detail"]
a = dict(arms["arms"])
ok = [r for r in rb if r.get("service_rss_mb") is not None]
chains = {}
for tool, c in D["chains"].items():
    chains[tool] = {k: c[k] for k in ("pages", "total_in_window_first_page", "partitions_read_total", "distinct_partition_dates_read", "partition_dates_repeated", "rows_total",
                                      "row_repeats_across_pages", "longest_page_wall_seconds", "chain_ended_with_null_cursor", "cursors_strictly_earlier",
                                      "rss_median_page_growth_mb", "within_page_non_increasing", "page_order_ok", "first_page")}
    chains[tool]["per_page"] = [{k: p.get(k) for k in ("n", "wall_seconds", "partitions_read", "window_partial", "rows", "next_cursor", "partitions_read_dates", "rss_mb_after",
                                                         "host_mem_used_pct_after")} for p in c["per_page"]]
    chains[tool]["final_next_cursor_null"] = bool(c["per_page"]) and c["per_page"][-1].get("next_cursor") is None
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
    "memory_basis": "fresh_process",
    "arms": a,
    "arm_counts": {"chains": chains, "e8": D["e8"], "host_mem_used_pct": D["host_mem_used_pct"], "first_page_over_trigger_seconds": D["first_page_over_trigger_seconds"]},
    "pre_deploy_plateau_test": {k: chain_pre[k] for k in ("verdict", "two_chains_in_one_process", "chain1_net_growth_from_start_mb", "chain2_net_growth_from_chain1_end_mb",
                                                           "chain2_net_growth_limit_mb", "chain_process_peak_growth_from_start_mb", "host_pct_peak", "longest_page_wall_s",
                                                           "ended_with_null_cursor_both")},
    "service_read_back": {"baseline_just_before_switch": {"t": baseline["t"], "service_rss_mb": baseline["service_rss_mb"], "host_pct": baseline["host_pct"]},
                          "probes": len(rb), "interval_s": 60, "first_t": rb[0]["t"], "last_t": rb[-1]["t"],
                          "service_rss_mb_min": min(r["service_rss_mb"] for r in ok), "service_rss_mb_max": max(r["service_rss_mb"] for r in ok),
                          "service_growth_over_pre_switch_baseline_max_mb": max(r["growth_vs_baseline_mb"] for r in ok),
                          "service_growth_over_first_post_switch_sample_max_mb": round(max(r["service_rss_mb"] for r in ok) - ok[0]["service_rss_mb"], 1),
                          "host_pct_max": max(r["host_pct"] for r in rb), "health_not_200": sum(1 for r in rb if r.get("health") != 200),
                          "service_pids_seen": len({r.get("pid") for r in rb}), "n_restarts_values": sorted({str(r.get("n_restarts")) for r in rb}),
                          "triggers_fired": len(triggers), "samples": [{k: r.get(k) for k in ("t", "service_rss_mb", "host_pct", "health", "growth_vs_baseline_mb")} for r in rb]},
    "window_calls_served_by_the_service": {"journal_post_mcp_lines": wincalls["journal"]["post_mcp_lines"], "journal_post_mcp_status_200": wincalls["journal"]["post_mcp_status_200"],
                                           "audit_records_in_window": wincalls["audit_lake"]["records_in_window"],
                                           "client_get_transactions_calls": wincalls["audit_lake"]["window_tool_calls"]["client_get_transactions"],
                                           "client_get_fees_calls": wincalls["audit_lake"]["window_tool_calls"]["client_get_fees"],
                                           "window_calls_total": wincalls["audit_lake"]["window_tool_calls_total"],
                                           "window_start_utc": wincalls["window_start_utc"], "window_end_utc": wincalls["window_end_utc"]},
    "limits": ["memory_basis is fresh_process: the page chains ran through the INSTALLED release code in a NEW process on the host (an Opal master_admin stand-in built in-process, "
               "audit sink stubbed); no page ran in the service process, because /mcp takes only a bearer signed by the gateway key and minting one as a roster principal is refused as "
               "impersonation (CTO Amendment 1). The service's own long-lived heap over a full chain is therefore NOT measured.",
               "The service served ZERO window calls (client_get_transactions or client_get_fees) in the 30-minute read-back; the read-back shows the service under whatever other load arrived "
               "(journal_post_mcp_lines /mcp requests, none a window read), inside the bounds.",
               "The host percent maximum in the read-back includes the 27-tool harness and the arms chains run by this seat in new processes during the window.",
               "The service restarted at the deploy, so its first post-switch RSS (a fresh process) is below the pre-switch baseline; growth is stated against both."],
}
io.open(W + "CODE5_SERVED.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
print(json.dumps({k: body[k] for k in ("live_commit", "health_status", "env_key_count", "reader_env_keys_present", "registry_count", "per_tool_good", "host_md5", "tools_list_before",
                                       "tools_list_after", "muse_env_present", "memory_basis", "arms")}, indent=1))
print(json.dumps(body["service_read_back"] | {"samples": "..."}, indent=1))
print(json.dumps(body["window_calls_served_by_the_service"], indent=1))
