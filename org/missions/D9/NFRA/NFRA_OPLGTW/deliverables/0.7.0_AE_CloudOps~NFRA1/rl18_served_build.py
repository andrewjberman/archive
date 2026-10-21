#!/usr/bin/env python
"""OG-rl-18 Phase B: assemble W/CODE17_SERVED.json from the measured records in W/rl18_pb/ (no value is typed here that a record holds). Counts, MB, seconds, words and booleans only; no address, ARN or account number.
  rl18_pb/pre.json, step1_before.json   the host read before the deploy
  rl18_pb/step1_after.json, host_md5_after.json, unarmed_raw.json, served27.txt, accesslog.json, auditwarn.json, clock.txt, limits.txt, lease_final.json, readback.jsonl, masterwide.json, sampler.jsonl
usage: python rl18_served_build.py   (repository root)"""
from __future__ import annotations

import datetime
import io
import json
import os
import re

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
R = W + "rl18_pb/"
REL = json.load(io.open(W + "rl18_release.json", encoding="utf-8"))["release_sha"]
GUARD = "oom_score_adj_1000_rlimit_as_1400mb"


def load(n):
    return json.load(io.open(R + n, encoding="utf-8"))


def grab(text, key):
    m = re.search(r"^%s=(.*)$" % re.escape(key), text, re.M)
    return m.group(1).strip() if m else None


pre, b1, md5, ua, ac, lf, inf = (load(n) for n in ("pre.json", "step1_after.json", "host_md5_after.json", "unarmed_raw.json", "accesslog.json", "lease_final.json", "masterwide.json"))
auditwarn = load("auditwarn.json")
s27 = json.loads(io.open(R + "served27.txt", encoding="utf-8").read().split("--- STDOUT ---", 1)[1].split("--- STDERR", 1)[0].split("CODE_SERVED_JSON", 1)[1].strip())["body"]
clock, lim = io.open(R + "clock.txt", encoding="utf-8").read(), io.open(R + "limits.txt", encoding="utf-8").read()
rb = [json.loads(ln) for ln in io.open(R + "readback.jsonl", encoding="utf-8") if ln.strip()]
samples = [json.loads(ln) for ln in io.open(R + "sampler.jsonl", encoding="utf-8") if ln.strip()]
trigger = os.path.exists(R + "readback.jsonl.trigger")


def secs(t):
    return datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()


def up(s):
    return s.get("code") == 401


intervals, cur = [], None
for smp in samples:
    if not up(smp) and cur is None:
        cur = smp["t"]
    elif up(smp) and cur is not None:
        intervals.append({"first_failed_sample_utc": cur, "first_answer_after_utc": smp["t"], "seconds": round(secs(smp["t"]) - secs(cur))})
        cur = None
down = {"all_intervals": intervals, "samples": len(samples), "failed_samples": sum(1 for s in samples if not up(s)),
        "method": "an unauthenticated POST to the public MCP endpoint every 2 s from this seat (a healthy gateway answers 401 itself; a stopped or hung one answers 5xx or nothing), first failed sample to first 401 after it; each interval includes the sampler's own 2 s step"}
leap = (re.search(r"Leap status\s*:\s*(\S+)", clock) or [None, None])[1]
refid = (re.search(r"Reference ID\s*:\s*(\S+)", clock) or [None, None])[1]
stratum = (re.search(r"Stratum\s*:\s*(\d+)", clock) or [None, None])[1]
failed_units = int(grab(clock, "FAILED_COUNT"))
clock_read_at = (re.search(r"^(\d{4}-\d\d-\d\dT[\d:]+Z)$", clock, re.M) or [None, None])[1]


def mb(b):
    return "%dM" % (int(b) // 1048576)


high_b, max_b = int(grab(lim, "MemoryHigh")), int(grab(lim, "MemoryMax"))
marker = grab(lim, "MARKER")
okp = [r for r in rb if r.get("service_rss_mb") is not None]
al, jr = ac["audit_lake"], ac["journal"]
lines, records = jr["post_mcp_lines"], al["records_in_window"]
calls = ua["calls"]
mem_line = (b1.get("mem_line") or "0 0").split()
body = {
    "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "live_commit": REL, "base_commit": pre["marker"],
    "health_after": s27["health_status"], "marker_equals_release": marker == REL, "marker_sha": marker,
    "unit_memory_high": mb(high_b), "unit_memory_max": mb(max_b), "memory_total_mb": int(mem_line[1]) if len(mem_line) > 1 else None,
    "tools_list": b1["tools"]["tools_list_master_admin"], "tools_list_before": load("step1_before.json")["tools"]["tools_list_master_admin"], "registry_count": s27["registry_count"],
    "tools_27_of_27": s27["per_tool_good"] == 27, "per_tool_good": s27["per_tool_good"], "harness_guard": GUARD, "nrestarts_after_deploy": int(grab(lim, "NRestarts")),
    "env_key_count": md5["env"]["key_count"], "muse_env_present": bool(b1["muse_client_id_is_a_key"]),
    "host_md5": {"equal": md5["equal_lf"] + md5["equal_crlf_only"], "differ": len(md5["differ"]), "missing_on_host": len(md5["missing_on_host"]), "expected_files": md5["denominator_expected_files"], "host_files": md5["denominator_host_files"]},
    "downtime": down,
    "host_clock": {"leap_status": leap, "synchronised": bool(refid and refid != "00000000" and stratum and int(stratum) < 16), "stratum": int(stratum), "read_at": clock_read_at}, "systemd_failed_units": failed_units, "clock_read_before_close": True,
    "readback": {"minutes": 30, "probes": len(rb), "first_t": rb[0]["t"], "last_t": rb[-1]["t"], "triggers_fired": 1 if trigger else 0, "nrestarts_during_readback": max(int(str(r.get("n_restarts"))) for r in rb), "health_not_200": sum(1 for r in rb if r.get("health") != 200),
                 "service_pids_seen": len({r.get("pid") for r in rb}), "service_rss_mb_min": min(r["service_rss_mb"] for r in okp), "service_rss_mb_max": max(r["service_rss_mb"] for r in okp), "rss_series_mb_each_probe": [[r["t"][11:19], r["service_rss_mb"]] for r in okp], "rss_at_restart_mb": okp[0]["service_rss_mb"], "host_pct_max": max(r["host_pct"] for r in rb)},
    "probe": {"armings": 0, "puts_made_by_this_seat": ua["puts_made_by_this_script"], "unarmed_status": calls[0]["status"] if all(c["status"] == 403 for c in calls) else "mixed", "unarmed_error": calls[0]["error"] if all(c["error"] == "probe_not_armed" for c in calls) else "mixed",
              "lease_parameter_absent_before": bool(ua["lease_before"]["absent"]), "lease_parameter_absent_after": bool(ua["lease_after"]["absent"]), "lease_parameter_absent_at_close": bool(lf["absent"]), "listener_bound": ua["state_before"]["bound"],
              "pid_stable": bool(ua["pid_stable"]), "nrestarts_after": int(ua["state_after"]["nrestarts"])},
    "access_log": {"window_minutes": 30, "window_start_utc": ac["window_start_utc"], "window_end_utc": ac["window_end_utc"], "post_mcp_lines_readback": lines, "audit_records_readback": records, "ratio_lines_to_records": round(lines / records, 3) if records else None,
                   "sampler_probes_in_the_journal_count": sum(1 for smp in samples if smp.get("code") == 401 and ac["window_start_utc"] <= smp["t"] <= ac["window_end_utc"]), "listener_access_lines": jr["post_probe_lines"], "listener_requests_made": len(calls),
                   "method": ac["method"], "note": "the journal count includes the unauthenticated POST /mcp probes of this seat's downtime sampler (answered 401) that fell inside the window, counted in sampler_probes_in_the_journal_count, and this seat's own proof calls; the audit lake records only authenticated calls"},
    "audit_failure_counter": {"journal_lines_readback": auditwarn["journal_lines_readback"], "counter_value": auditwarn["counter_value"], "classes_seen": auditwarn["classes_seen"], "method": auditwarn["method"]},
    "masterwide": {"sentinel_parse_in_deployed_tree": inf["sentinel_parse_in_deployed_tree"], "explicit_scope_unchanged": inf["explicit_scope_unchanged"], "sentinel_grants_in_store": inf["sentinel_grants_in_store"],
                   "explicit_scope_compared_with": inf.get("explicit_scope_compared_with"), "store_read_at": inf.get("store_read_at")},
    "limits": ["The served read was UNARMED ONLY: no lease was written and no SSM parameter was written by this seat.",
               "The downtime is measured from this seat by a public-endpoint sampler, so each interval includes the sampler's step."],
}
io.open(W + "CODE17_SERVED.json", "w", encoding="utf-8", newline="\n").write(json.dumps(body, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("live_commit", "health_after", "marker_equals_release", "unit_memory_high", "unit_memory_max", "memory_total_mb", "tools_list", "tools_list_before", "tools_27_of_27", "nrestarts_after_deploy",
                                       "host_md5", "downtime", "masterwide", "audit_failure_counter")}, indent=1)[:2800])
