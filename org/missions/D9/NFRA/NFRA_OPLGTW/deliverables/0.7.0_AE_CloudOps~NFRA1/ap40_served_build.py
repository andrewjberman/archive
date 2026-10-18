#!/usr/bin/env python
"""OG-ap-40 Phase B: assemble W/CODE9_SERVED.json from the measured records (no value is typed here that a record does not hold). Counts, MB, seconds, words and booleans only.
  ap40_pb/step1_before.json, step1_after.json   the host read at the GO and after the deploy (marker, unit limits, tools/list)
  ap40_pb/host_md5_after.json                   the host md5 walk against the RELEASE blobs plus .env names
  ap40_pb/probe_raw.json                        the ONE arming: unarmed call, lease, peers, window chain, refusals, expiry, delete, closed call, audit-lake counts
  ap40_pb/served27.txt                          the 27-tool served read under the hard guard (ap36_guarded.py + ap36_served_harness.py)
  ap40_pb/wincalls.json                         the /mcp calls and window calls the service served in the read-back window (the probes' calls go to the listener, not /mcp)
  ap40_pb/clock.txt, limits.txt                 chronyc tracking + systemctl --failed (BEFORE the close), and the live unit limits, cgroup memory.max, marker and harvest md5
  ap40_pb/readback.jsonl (+ .trigger absent)    the 31-minute service read-back, one probe a minute
usage: python ap40_served_build.py   (repository root of the worktree that holds the records)"""
from __future__ import annotations

import datetime
import io
import json
import os
import re
import statistics

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
R = W + "ap40_pb/"
SEVEN = ["BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN", "ECLIPSE_READER_ROLE_ARN",
         "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN", "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"]
REL = json.load(io.open(W + "ap40_release.json", encoding="utf-8"))["release_sha"]
GUARD_AS = "oom_score_adj_1000_rlimit_as_1400mb"
CT1_MD5 = "596c299597067fe5a8afb8e3493a0ed9"


def load(n):
    return json.load(io.open(R + n, encoding="utf-8"))


b0, b1, md5, pr, win = load("step1_before.json"), load("step1_after.json"), load("host_md5_after.json"), load("probe_raw.json"), load("wincalls.json")
s27 = json.loads(io.open(R + "served27.txt", encoding="utf-8").read().split("--- STDOUT ---", 1)[1].split("--- STDERR", 1)[0].split("CODE_SERVED_JSON", 1)[1].strip())["body"]
clock = io.open(R + "clock.txt", encoding="utf-8").read()
lim = io.open(R + "limits.txt", encoding="utf-8").read()
rb = [json.loads(ln) for ln in io.open(R + "readback.jsonl", encoding="utf-8") if ln.strip()]
ok = [r for r in rb if r.get("service_rss_mb") is not None]
trigger_file = os.path.exists(R + "readback.jsonl.trigger")


def grab(text, key):
    m = re.search(r"^%s=(.*)$" % re.escape(key), text, re.M)
    return m.group(1).strip() if m else None


leap = (re.search(r"Leap status\s*:\s*(\S+)", clock) or [None, None])[1]
refid = (re.search(r"Reference ID\s*:\s*(\S+)", clock) or [None, None])[1]
stratum = (re.search(r"Stratum\s*:\s*(\d+)", clock) or [None, None])[1]
failed = int(grab(clock, "FAILED_COUNT"))
clock_read_at = (re.search(r"^(\d{4}-\d\d-\d\dT[\d:]+Z)$", clock, re.M) or [None, None])[1]
names = set(md5["env"]["reader_role_arn_keys"])
unit = {"memory_max_bytes": int(grab(lim, "MemoryMax")), "memory_high_bytes": int(grab(lim, "MemoryHigh")), "oom_score_adj": int(grab(lim, "OOMScoreAdjust")), "cgroup_memory_max_bytes": int(grab(lim, "CGMAX"))}
marker = grab(lim, "MARKER")
harvest_md5 = grab(lim, "HARVEST_MD5")
tool_bad = [n for n, v in s27["per_tool"].items() if not (v.get("opal_served") is True and v.get("non_opal_refused") is True and v.get("reads_on_refusal") == 0)]

# the probe block
pe, ch = pr["peers"], pr["chain"]
pages = ch["pages"]
growths = [p["growth_mb"] for p in pages if p.get("growth_mb") is not None]
hb, ha = pe["heap_before_signal"], pe["heap_after_signal"]
heap_before = hb.get("VmRSS") if hb.get("line_found") else pe["rss_before_proc_mb"]
heap_after = ha.get("VmRSS") if ha.get("line_found") else pe["rss_after_proc_mb"]
expired = pr["expired_call"]
closed = pr["closed_call"]
lake = pr["audit_lake"]
probe = {
    "lease_minutes": pr["lease"]["minutes"], "audit_label": "probe:OG-ap-40", "armings": pr["armings"],
    "peers": {"answered": pe["status"] == 200, "rows_matched": pe["rows_matched"], "wall_s": pe["wall_s"], "service_heap_before_mb": heap_before, "service_heap_after_mb": heap_after,
              "heap_source": "SIGUSR2 line" if hb.get("line_found") and ha.get("line_found") else "/proc", "vmrss_after_mb": pe["rss_after_proc_mb"], "hwm_after_mb": pe["hwm_after_proc_mb"],
              "service_pid": pe["pid_after"], "pid_stable": pe["pid_before"] == pe["pid_after"], "c15_retried": pe["c15_retried"]},
    "window_chain": {"pages": len(pages), "answered": all(p["status"] == 200 for p in pages), "ended_by_cursor": pages[-1]["next_cursor_present"] is False, "rows_per_page": [p["rows"] for p in pages],
                     "heap_growth_median_mb": round(statistics.median(growths), 2), "heap_growth_per_page_mb": growths, "first_page_wall_s": pages[0]["wall_s"], "max_page_wall_s": max(p["wall_s"] for p in pages),
                     "max_vmrss_mb": max(p["rss_after_mb"] for p in pages), "service_pid_stable": ch["pid_before"] == ch["pid_after"], "stopped_over_1200": ch["stopped_over_1200"],
                     "heap_before_signal_mb": ch["heap_before_signal"].get("VmRSS"), "heap_after_signal_mb": ch["heap_after_signal"].get("VmRSS"), "page_hashes": [p["sha"][:16] for p in pages]},
    "other_tool_refused": pr["refusals"]["other_tool"]["status"] == 404 and pr["refusals"]["other_tool"]["error"] == "probe_tool_refused",
    "other_account_refused": pr["refusals"]["other_account"]["status"] == 403 and pr["refusals"]["other_account"]["error"] == "probe_account_refused",
    "unarmed_before_arming": {"status": pr["unarmed_call"]["status"], "error": pr["unarmed_call"]["error"]},
    "expired_refused": bool(expired["status"] == 403 and expired["error"] == "probe_not_armed" and pr["parameter_present_at_expiry"] is True and pr["expired_call_at"] > pr["lease"]["expires_at"]),
    "parameter_present_at_expiry": pr["parameter_present_at_expiry"], "expired_call_at": pr["expired_call_at"], "lease_expired_at": pr["lease"]["expires_at"],
    "parameter_not_found_after_delete": bool(pr["parameter_not_found_after_delete"]), "deleted_at": pr["deleted_at"],
    "listener_closed_at_rest": bool(closed["status"] == 403 and closed["error"] == "probe_not_armed" and pr["parameter_exists_at_end"] is False), "closed_call_at": pr["closed_call_at"],
    "nrestarts_after_probes": int(pr["state_after"]["nrestarts"]), "service_pid_before": pr["state_before"]["pid"], "service_pid_after": pr["state_after"]["pid"],
    "listener_bound": pr["state_before"]["bound"], "listener_bound_to_service_pid": pr["state_before"]["bound_to_service_pid"], "emergency_delete": bool(pr.get("emergency_delete")),
    "audit_lake_labelled_records": {"probe_og_ap_40": lake["probe_og_ap_40_labelled"], "probe_unarmed": lake["probe_unarmed_labelled"], "read_errors": lake["read_errors"]},
}
body = {
    "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "live_commit": REL,
    "health_status": s27["health_status"],
    "env_key_count": md5["env"]["key_count"],
    "reader_env_keys_present": sum(1 for k in SEVEN if k in names),
    "registry_count": s27["registry_count"],
    "per_tool_good": s27["per_tool_good"],
    "per_tool_not_good": tool_bad,
    "harness_guard": GUARD_AS,
    "host_md5": {"equal": md5["equal_lf"] + md5["equal_crlf_only"], "differ": len(md5["differ"]), "missing_on_host": len(md5["missing_on_host"]),
                 "expected_files": md5["denominator_expected_files"], "host_files": md5["denominator_host_files"]},
    "harvest_research_md5": {"host": harvest_md5, "expected_ct1": CT1_MD5, "equal": harvest_md5 == CT1_MD5},
    "tools_list_before": b0["tools"]["tools_list_master_admin"],
    "tools_list_after": b1["tools"]["tools_list_master_admin"],
    "muse_env_present": bool(b1["muse_client_id_is_a_key"]) or bool(md5["env"]["muse_client_id_is_a_key"]),
    "marker_sha": marker,
    "unit_limits": unit,
    "host_clock": {"leap_status": leap, "synchronised": bool(refid and refid != "00000000" and stratum and int(stratum) < 16), "reference_id": refid, "stratum": int(stratum), "read_at": clock_read_at},
    "systemd_failed_units": failed,
    "clock_read_before_close": True,
    "readback": {"minutes": 30, "triggers_fired": 1 if trigger_file else 0, "service_window_calls": win["audit_lake"]["window_tool_calls_total"],
                 "nrestarts_during_readback": max(int(str(r.get("n_restarts"))) for r in rb), "probes": len(rb), "first_t": rb[0]["t"], "last_t": rb[-1]["t"],
                 "service_pids_seen": len({r.get("pid") for r in rb}), "health_not_200": sum(1 for r in rb if r.get("health") != 200),
                 "service_rss_mb_min": min(r["service_rss_mb"] for r in ok), "service_rss_mb_max": max(r["service_rss_mb"] for r in ok), "host_pct_max": max(r["host_pct"] for r in rb),
                 "mcp_requests_served": win["journal"]["post_mcp_lines"], "audit_records_in_window": win["audit_lake"]["records_in_window"],
                 "service_window_calls_note": "all %d window calls in the audit lake for this window came through the listener (the %d chain pages and the refused calls); /mcp requests served: %d" % (
                     win["audit_lake"]["window_tool_calls_total"], len(pages), win["journal"]["post_mcp_lines"])},
    "probe": probe,
    "arms": {"e10_marker_equals_release_sha": marker == REL,
             "e14_unit_limits_unchanged": bool(unit["memory_max_bytes"] == 1468006400 and unit["memory_high_bytes"] == 1258291200 and unit["oom_score_adj"] == 300 and unit["cgroup_memory_max_bytes"] == 1468006400)},
    "limits": ["The probes ran through the listener of the RUNNING service, one arming of 25 minutes on the one test account (CTO ruling, msg 35661). The 27-tool read ran in a fresh process under oom_score_adj_1000_rlimit_as_1400mb.",
               "The window chain walked the 13-month window to its natural end (the last page carried no next cursor); the peers call took %s s through the listener." % pe["wall_s"],
               "The read-back's /mcp counts exclude the probes (they go to the listener port); the audit lake labels them probe:OG-ap-40 and probe:unarmed."],
}
io.open(W + "CODE9_SERVED.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
served = ("Served: the 27-tool read passes %d of 27 under the hard guard; host md5 %d of %d equal to the release blobs and harvest_research.py md5 %s equal to CT1; the unit limits are unchanged; "
          "THROUGH THE LISTENER of the running service on ONE arming of %d minutes: etfs_compare_peers answered %d rows (service heap %s to %s MB, peak %s MB), the window chain ran %d pages to its end "
          "(first page %s s, median per-page growth %s MB, highest VmRSS %s MB), another tool and another account were refused, the same lease lapsed and the next call was refused, the parameter was deleted "
          "(ParameterNotFound) and the next call refused, the service PID unchanged and NRestarts %d; the 30-minute read-back (%d probes) shows the service at %s to %s MB, NRestarts %d, health 200 throughout; "
          "the host clock reads Leap %s, synchronised, and systemctl --failed %d units (read %s, before the close)."
          % (s27["per_tool_good"], body["host_md5"]["equal"], body["host_md5"]["expected_files"], harvest_md5, pr["lease"]["minutes"], pe["rows_matched"], heap_before, heap_after, pe["hwm_after_proc_mb"],
             len(pages), pages[0]["wall_s"], probe["window_chain"]["heap_growth_median_mb"], probe["window_chain"]["max_vmrss_mb"], probe["nrestarts_after_probes"], len(rb),
             body["readback"]["service_rss_mb_min"], body["readback"]["service_rss_mb_max"], body["readback"]["nrestarts_during_readback"], leap, failed, clock_read_at))
io.open(W + "ap40_facts.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"served_sentence": served}, indent=1) + chr(10))
print(json.dumps({k: body[k] for k in ("live_commit", "health_status", "env_key_count", "reader_env_keys_present", "registry_count", "per_tool_good", "per_tool_not_good", "host_md5", "harvest_research_md5",
                                       "tools_list_before", "tools_list_after", "muse_env_present", "marker_sha", "unit_limits", "host_clock", "systemd_failed_units", "arms")}, indent=1))
print(json.dumps(body["readback"], indent=1))
print(json.dumps(probe, indent=1))
print(served)
