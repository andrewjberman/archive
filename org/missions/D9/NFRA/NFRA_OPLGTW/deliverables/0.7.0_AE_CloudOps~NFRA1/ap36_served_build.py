#!/usr/bin/env python
"""OG-ap-36 Phase B step 6: assemble W/CODE6_SERVED.json from the measured records (no value is typed here that a record does not hold, but the two named facts of the
COO's ruling, msg 35543: the served read is graded 26 of 27 with per_tool_exception etfs_compare_peers and exception_row NFRA_OPLGTW-Z-S375).

  ap36_served27.json          the 27-tool served harness, awaiting the two async client tools, under the hard guard   <- ap36_guarded.py + ap36_served_harness.py
  ap36_arms.json              the paging arms through the installed code, a new process, sha256 fields removed       <- ap36_arms.py (the full record stays out of git)
  ap36_e11.json               the six-page equality against the live code's pages (rows, sha256, cursors, partition_rows, fence_excluded)
  ap36_host_md5_after.json    the host md5 walk against the RELEASE blobs plus .env names                            <- ap36_host_md5.py
  ap36_toolslist_before.json / ap36_toolslist_after.json   tools/list before (at the GO) and after the deploy       <- ap36_toolslist.py
  ap36_harvest_md5.json       the host md5 of app/harvest_research.py and the md5 of its 1753c741d9 blob (CT4)
  ap36_baseline.json          the probe just before the switch
  ap36_readback1.jsonl / ap36_readback2.jsonl   the two 30-minute service read-backs (the first spans the 17:21Z restart the seat caused)
  ap36_wincalls.json          the /mcp calls and window calls the service served from the deploy to the end of read-back 2          <- ap34_wincalls.py
Counts, seconds, percentages, dates and booleans only. usage: python ap36_served_build.py   (repository root of the worktree that holds the records)"""
from __future__ import annotations

import datetime
import io
import json
import os

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
SEVEN = ["BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN", "ECLIPSE_READER_ROLE_ARN",
         "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN", "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"]
RELEASE = json.load(io.open(W + "ap36_release.json", encoding="utf-8"))["release_sha"]


def load(n):
    return json.load(io.open(W + n, encoding="utf-8"))


def series(name):
    rows = [json.loads(ln) for ln in io.open(W + name, encoding="utf-8") if ln.strip()]
    tf = W + name + ".trigger"
    trig = io.open(tf, encoding="utf-8").read().splitlines() if os.path.exists(tf) else []
    ok = [r for r in rows if r.get("service_rss_mb") is not None]
    t0 = datetime.datetime.strptime(rows[0]["t"], "%Y-%m-%dT%H:%M:%SZ")
    t1 = datetime.datetime.strptime(rows[-1]["t"], "%Y-%m-%dT%H:%M:%SZ")
    return {"probes": len(rows), "interval_s": 60, "first_t": rows[0]["t"], "last_t": rows[-1]["t"], "minutes": int(round((t1 - t0).total_seconds() / 60.0)),
            "service_rss_mb_min": min(r["service_rss_mb"] for r in ok), "service_rss_mb_max": max(r["service_rss_mb"] for r in ok),
            "service_growth_over_pre_switch_baseline_max_mb": max(r["growth_vs_baseline_mb"] for r in ok),
            "host_pct_max": max(r["host_pct"] for r in rows), "health_not_200": sum(1 for r in rows if r.get("health") != 200),
            "service_pids_seen": len({r.get("pid") for r in rows}), "n_restarts_values": sorted({str(r.get("n_restarts")) for r in rows}),
            "triggers_fired": len(trig), "samples": [{k: r.get(k) for k in ("t", "service_rss_mb", "host_pct", "health", "growth_vs_baseline_mb", "pid")} for r in rows]}


s27, arms, md5 = load("ap36_served27.json"), load("ap36_arms.json"), load("ap36_host_md5_after.json")
tl_before, tl_after = load("ap36_toolslist_before.json"), load("ap36_toolslist_after.json")
hv, e11, base, wincalls = load("ap36_harvest_md5.json"), load("ap36_e11.json"), load("ap36_baseline.json"), load("ap36_wincalls.json")
b27 = s27.get("body", s27)
names = set(md5["env"]["reader_role_arn_keys"])
D = arms["detail"]
a = dict(arms["arms"])
a["e11_pages_equal_live_code_row_for_row"] = bool(e11["e11"])
a.pop("e7_catalog_on_host", None)
a["e7_catalog_on_host"] = bool(arms["arms"]["e7_catalog_on_host"])               # kept beside the nine; the nine are what the order names
chains = {}
for tool, c in D["chains"].items():
    chains[tool] = {k: c[k] for k in ("pages", "total_in_window_first_page", "partitions_read_total", "distinct_partition_dates_read", "partition_dates_repeated", "rows_total",
                                      "row_repeats_across_pages", "longest_page_wall_seconds", "chain_ended_with_null_cursor", "cursors_strictly_earlier",
                                      "rss_median_page_growth_mb", "within_page_non_increasing", "page_order_ok", "first_page")}
    chains[tool]["per_page"] = [{k: p.get(k) for k in ("n", "wall_seconds", "partitions_read", "window_partial", "rows", "next_cursor", "absent_reason", "rss_mb_after",
                                                         "host_mem_used_pct_after", "partition_rows", "fence_excluded")} for p in c["per_page"]]
    chains[tool]["final_next_cursor_null"] = bool(c["per_page"]) and c["per_page"][-1].get("next_cursor") is None
rb1, rb2 = series("ap36_readback1.jsonl"), series("ap36_readback2.jsonl")
body = {
    "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "live_commit": RELEASE,
    "health_status": b27.get("health_status"),
    "env_key_count": md5["env"]["key_count"],
    "reader_env_keys_present": sum(1 for k in SEVEN if k in names),
    "registry_count": b27.get("registry_count"),
    "per_tool_good": b27.get("per_tool_good"),
    "per_tool_exception": "etfs_compare_peers",
    "exception_row": "NFRA_OPLGTW-Z-S375",
    "host_md5": {"equal": md5["equal_lf"] + md5["equal_crlf_only"], "differ": len(md5["differ"]), "missing_on_host": len(md5["missing_on_host"]),
                 "expected_files": md5["denominator_expected_files"], "host_files": md5["denominator_host_files"]},
    "tools_list_before": tl_before["tools_list_master_admin"],
    "tools_list_after": tl_after["tools_list_master_admin"],
    "muse_env_present": bool(arms["muse_env_present"]) or bool(md5["env"]["muse_client_id_is_a_key"]),
    "marker_sha": D["marker_sha"],
    "harvest_research_md5": {"host": hv["host"], "expected": hv["expected"], "equal": hv["host"] == hv["expected"]},
    "memory_basis": arms["memory_basis"],
    "e12_basis": arms["e12_basis"],
    "readback": {"minutes": rb2["minutes"], "triggers_fired": rb2["triggers_fired"], "service_window_calls": wincalls["audit_lake"]["window_tool_calls_total"]},
    "arms": a,
    "arm_counts": {"chains": chains, "e8": D["e8"], "e9": D["e9"], "e12": D["e12"], "host_mem_used_pct": D["host_mem_used_pct"], "first_page_over_trigger_seconds": D["first_page_over_trigger_seconds"],
                   "e11_pages_compared": e11["pages"]},
    "service_read_back": {"baseline_just_before_switch": base, "readback_2_the_restarted_process": rb2, "readback_1_spans_the_1721Z_restart": rb1},
    "window_calls_served_by_the_service": {"journal_post_mcp_lines": wincalls["journal"]["post_mcp_lines"], "journal_post_mcp_status_200": wincalls["journal"]["post_mcp_status_200"],
                                           "audit_records_in_window": wincalls["audit_lake"]["records_in_window"],
                                           "client_get_transactions_calls": wincalls["audit_lake"]["window_tool_calls"]["client_get_transactions"],
                                           "client_get_fees_calls": wincalls["audit_lake"]["window_tool_calls"]["client_get_fees"],
                                           "window_calls_total": wincalls["audit_lake"]["window_tool_calls_total"],
                                           "window_start_utc": wincalls["window_start_utc"], "window_end_utc": wincalls["window_end_utc"]},
    "limits": ["memory_basis is fresh_process: the page chains ran through the INSTALLED release code in a NEW process on the host (an Opal master_admin stand-in built in-process, "
               "audit sink stubbed); no page ran in the service process, because /mcp takes only a bearer signed by the gateway key. The service's own long-lived heap over a full "
               "chain is therefore NOT measured (Z-S338 stays open until an organic window call).",
               "per_tool_good is 26 of 27 by the COO's ruling (msg 35543, CTO 35540): the one miss is etfs_compare_peers, which raises MemoryError under a 1400 MB guard; its module is byte-equal on "
               "both refs. Row NFRA_OPLGTW-Z-S375 is open and ARMED (disarm_owner 2.0.0_SA_COO~O).",
               "At 17:21Z an UNGUARDED first run of the 27-tool harness (this seat's act) ran the host out of memory: the kernel killed the gateway once (restart counter 1, back in 3 s) and "
               "eight system daemons, since restored. Read-back 1 (17:07 to 17:37Z) spans that restart (pids 1252977 then 1254532, n_restarts 0 then 1, health 200 at every sample); "
               "read-back 2 is a full 30 minutes on the restarted process.",
               "The harness was run twice (unguarded, then guarded twice); the arms ran twice (the first run's fees chain stopped on page 2 because the harness read an empty page's reason word as "
               "a refusal; fixed to follow next_cursor through an empty page), so the e12 refusal-word call was made twice on the test account.",
               "The host percent maximum in the read-backs includes the harness and the arms run by this seat in new processes during the windows."],
}
io.open(W + "CODE6_SERVED.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
print(json.dumps({k: body[k] for k in ("live_commit", "health_status", "env_key_count", "reader_env_keys_present", "registry_count", "per_tool_good", "per_tool_exception", "exception_row", "host_md5",
                                       "tools_list_before", "tools_list_after", "muse_env_present", "marker_sha", "harvest_research_md5", "readback", "memory_basis", "e12_basis", "arms")}, indent=1))
print(json.dumps({k: v for k, v in rb2.items() if k != "samples"}, indent=1))
print(json.dumps(body["window_calls_served_by_the_service"], indent=1))
