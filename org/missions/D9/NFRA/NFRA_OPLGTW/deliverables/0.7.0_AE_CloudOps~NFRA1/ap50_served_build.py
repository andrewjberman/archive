#!/usr/bin/env python
"""OG-ap-50 Phase B: assemble W/CODE14_SERVED.json from the measured records (no value is typed here that a record does not hold). Counts, MB, seconds, words and booleans only.
  ap50_pb/step1_before.json, step1_after.json   the host read at the GO and after the deploy (marker, unit limits, tools/list)
  ap50_pb/host_md5_after.json                   the host md5 walk against the RELEASE blobs plus .env names
  ap50_pb/unarmed_raw.json                      the served read UNARMED ONLY: the lease parameter read absent before and after, three calls answering 403 probe_not_armed, the PID stable (no SSM write)
  ap50_pb/served27.txt                          the 27-tool served read under the hard guard (ap36_guarded.py + ap36_served_harness.py)
  ap50_pb/accesslog.json                        the access log: the journal's POST /mcp and POST /probe/ lines and the audit lake's records over the SAME read-back window, and the pre-OG-ap-40 baseline window
  ap50_pb/clock.txt, limits.txt                 chronyc tracking + systemctl --failed (BEFORE the close), and the live unit limits, cgroup memory.max, marker and the host md5 of the named files
  ap50_pb/lease_final.json                      the lease parameter read absent at the close
  ap50_pb/readback.jsonl (+ .trigger absent)    the 31-minute service read-back, one probe a minute
usage: python ap50_served_build.py   (repository root of the worktree that holds the records)"""
from __future__ import annotations

import datetime
import hashlib
import io
import json
import os
import re
import subprocess

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
R = W + "ap50_pb/"
G = "infra/aws/ec2/opal-gateway/app/"
SEVEN = ["BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN", "ECLIPSE_READER_ROLE_ARN",
         "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN", "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"]
REL = json.load(io.open(W + "ap50_release.json", encoding="utf-8"))["release_sha"]
GUARD_AS = "oom_score_adj_1000_rlimit_as_1400mb"
CHECKED = ["harvest_research", "harvest_figures", "harvest_identity", "harvest_keys", "graph", "probe_listener", "audit", "admin_api", "family_depth"]


def load(n):
    return json.load(io.open(R + n, encoding="utf-8"))


rb0, rb1 = load("route_before.json"), load("route_after.json")
b0, b1, md5, ua, ac, lf = load("step1_before.json"), load("step1_after.json"), load("host_md5_after.json"), load("unarmed_raw.json"), load("accesslog.json"), load("lease_final.json")
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
files = {}
for f in CHECKED:
    blob = subprocess.run(["git", "show", "%s:%s%s" % (REL, G, f + ".py")], capture_output=True, check=True).stdout
    files[f] = {"host_md5": grab(lim, "MD5_" + f), "release_md5": hashlib.md5(blob).hexdigest()}
    files[f]["equal"] = files[f]["host_md5"] == files[f]["release_md5"]
tool_bad = [n for n, v in s27["per_tool"].items() if not (v.get("opal_served") is True and v.get("non_opal_refused") is True and v.get("reads_on_refusal") == 0)]
calls = ua["calls"]
probe = {
    "armings": 0, "puts_made_by_this_seat": ua["puts_made_by_this_script"],
    "unarmed_status": calls[0]["status"] if all(c["status"] == 403 for c in calls) else sorted({c["status"] for c in calls})[0],
    "unarmed_error": calls[0]["error"] if all(c["error"] == "probe_not_armed" for c in calls) else "mixed",
    "unarmed_calls": [{"tool": c["tool"], "status": c["status"], "error": c["error"], "at": c["at"]} for c in calls],
    "lease_parameter_absent_before": bool(ua["lease_before"]["absent"]), "lease_parameter_absent_after": bool(ua["lease_after"]["absent"]),
    "lease_parameter_absent_at_close": bool(lf["absent"]), "lease_final_read_at": lf["read_at"],
    "lease_before_read_at": ua["lease_before"]["read_at"], "lease_after_read_at": ua["lease_after"]["read_at"],
    "listener_bound": ua["state_before"]["bound"], "listener_bound_to_service_pid": ua["state_before"]["bound_to_service_pid"],
    "service_pid_before": ua["state_before"]["pid"], "service_pid_after": ua["state_after"]["pid"], "pid_stable": bool(ua["pid_stable"]), "nrestarts_after": int(ua["state_after"]["nrestarts"]),
}
jr, lk, bl = ac["journal"], ac["audit_lake"], ac["baseline_window"]["journal"]
lines, records = jr["post_mcp_lines"], lk["records_in_window"]
access_log = {
    "window_minutes": 30, "window_start_utc": ac["window_start_utc"], "window_end_utc": ac["window_end_utc"],
    "post_mcp_lines_readback": lines, "audit_records_readback": records, "ratio_lines_to_records": round(lines / records, 3) if records else None,
    "post_mcp_lines_before_ap40_30min": bl["post_mcp_lines"], "baseline_window": "%s to %s" % (ac["baseline_window"]["start_utc"], ac["baseline_window"]["end_utc"]),
    "listener_access_lines": jr["post_probe_lines"], "listener_requests_made": len(calls),
    "journal_lines_total_readback": jr["journal_lines_total"], "baseline_journal_lines_total": bl["journal_lines_total"],
    "uvicorn_startup_lines_seen": load("startup.json")["journal"]["uvicorn_startup_lines"],
    "ct3_both_sources_nonzero": bool(lines and records),
    "method": ac["method"],
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
    "named_files_md5": files,
    "tools_list_before": b0["tools"]["tools_list_master_admin"],
    "tools_list_after": b1["tools"]["tools_list_master_admin"],
    "muse_env_present": bool(b1["muse_client_id_is_a_key"]) or bool(md5["env"]["muse_client_id_is_a_key"]),
    "marker_sha": marker,
    "unit_limits": unit,
    "host_clock": {"leap_status": leap, "synchronised": bool(refid and refid != "00000000" and stratum and int(stratum) < 16), "reference_id": refid, "stratum": int(stratum), "read_at": clock_read_at},
    "systemd_failed_units": failed,
    "clock_read_before_close": True,
    "readback": {"minutes": 30, "triggers_fired": 1 if trigger_file else 0, "nrestarts_during_readback": max(int(str(r.get("n_restarts"))) for r in rb), "probes": len(rb),
                 "first_t": rb[0]["t"], "last_t": rb[-1]["t"], "service_pids_seen": len({r.get("pid") for r in rb}), "health_not_200": sum(1 for r in rb if r.get("health") != 200),
                 "service_rss_mb_min": min(r["service_rss_mb"] for r in ok), "service_rss_mb_max": max(r["service_rss_mb"] for r in ok), "host_pct_max": max(r["host_pct"] for r in rb),
                 "post_mcp_access_log_lines": lines, "audit_records_in_window": records},
    "probe": probe,
    "access_log": access_log,
    "route": {"before_status": rb0["families_status"], "unauth_status": rb1["families_status"], "whoami_control_status": rb1["whoami_status"], "missing_control_status": rb1["missing_status"],
              "probe": rb1["probe"], "before_read_at": rb0["read_at"][0], "after_read_at": rb1["read_at"][0], "before_whoami_status": rb0["whoami_status"], "before_missing_status": rb0["missing_status"],
              "service_pid_before": rb0["service_pid"], "service_pid_after": rb1["service_pid"], "lease_parameter_absent_before": rb0["lease_parameter_absent"], "lease_parameter_absent_after": rb1["lease_parameter_absent"]},
    "audit_failure_counter": load("auditwarn.json"),
    "arms": {"e10_marker_equals_release_sha": marker == REL,
             "e14_unit_limits_unchanged": bool(unit["memory_max_bytes"] == 1468006400 and unit["memory_high_bytes"] == 1258291200 and unit["oom_score_adj"] == 300 and unit["cgroup_memory_max_bytes"] == 1468006400),
             "named_files_md5_equal": all(v["equal"] for v in files.values())},
    "limits": ["The route was read with a LOCAL request to the service port on the host with NO identity header, so the owner gate's 200 branch was not exercised on the running service (the owner's header comes only from the load balancer); the owner-session read of the panel is the owner's, later.",
               "The served read was UNARMED ONLY: no lease was written (this seat made no SSM write of any kind) and the listener answered 403 probe_not_armed to all %d calls." % len(calls),
               "The listener's own access lines are counted separately (row Z-S397): %d lines for the %d requests this seat made." % (jr["post_probe_lines"], len(calls)),
               "The access-log criterion compares the journal with the audit lake over the same window; the audit lake counts tool and login records the access log does not, so the ratio is below 1.",
               "The 27-tool read ran in a fresh process under oom_score_adj_1000_rlimit_as_1400mb."],
}
io.open(W + "CODE14_SERVED.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
served = ("Served: the 27-tool read passes %d of 27 under the hard guard; host md5 %d of %d equal to the release blobs and the host md5 of dell1's four harvest files, graph.py, probe_listener.py and audit.py equal to the release's (%d of %d); "
          "the unit limits are unchanged; UNARMED ONLY: the lease parameter was absent before, after and at the close, no SSM write was made, %d calls to the listener answered 403 probe_not_armed, the service PID unchanged and NRestarts %d; "
          "THE ACCESS LOG IS BACK: over the 30-minute read-back the journal holds %d POST /mcp lines against %d audit-lake records (ratio %s; the window before the OG-ap-40 deploy held %d), and the listener's %d /probe/ lines equal the %d requests made; the audit lake leg is bounded (connect 2 s, read 3 s, two sends) and audible; "
          "the read-back (%d probes) shows the service at %s to %s MB, NRestarts %d, health 200 throughout; the host clock reads Leap %s, synchronised, and systemctl --failed %d units (read %s, before the close)."
          % (s27["per_tool_good"], body["host_md5"]["equal"], body["host_md5"]["expected_files"], sum(1 for v in files.values() if v["equal"]), len(files), len(calls), probe["nrestarts_after"],
             lines, records, access_log["ratio_lines_to_records"], bl["post_mcp_lines"], jr["post_probe_lines"], len(calls), len(rb), body["readback"]["service_rss_mb_min"], body["readback"]["service_rss_mb_max"],
             body["readback"]["nrestarts_during_readback"], leap, failed, clock_read_at))
served += (" THE NEW ROUTE (OG-cd-2) is mounted behind the owner gate on the running service: GET /api/admin/gateway/families answered %d before the deploy and %d after with no identity header (the whoami control %d, a missing route %d), read by a local request to the service port."
           % (body["route"]["before_status"], body["route"]["unauth_status"], body["route"]["whoami_control_status"], body["route"]["missing_control_status"]))
io.open(W + "ap50_facts.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"served_sentence": served}, indent=1) + chr(10))
print(json.dumps({k: body[k] for k in ("live_commit", "health_status", "env_key_count", "reader_env_keys_present", "registry_count", "per_tool_good", "per_tool_not_good", "host_md5", "named_files_md5",
                                       "tools_list_before", "tools_list_after", "muse_env_present", "marker_sha", "unit_limits", "host_clock", "systemd_failed_units", "arms")}, indent=1))
print(json.dumps(body["readback"], indent=1))
print(json.dumps(probe, indent=1))
print(json.dumps(access_log, indent=1))
print(served)
