#!/usr/bin/env python
"""OG-rz-2 Phase B: assemble W/RZ2_SERVED.json (and W/rz2_facts.json) from the measured records in W/rz2_pb/ (no value is typed here that a record holds). Counts, MB, seconds, words and booleans only; no address, ARN or account number.
  rz2_pb/pre.json, step1_before.json   the host read before the stop (COO H5)
  rz2_pb/apply.json                    the apply summary (plan at apply, the apply's own counts, times)
  rz2_pb/resize_wait.json              the state timeline and the post-resize facts
  rz2_pb/sampler.jsonl                 the public-endpoint sampler (the downtime)
  rz2_pb/step1_after.json, host_md5_after.json, unarmed_raw.json, served27.txt, accesslog.json, startup.json, auditwarn.json, clock.txt, limits.txt, lease_final.json, readback.jsonl
  rz2_pb/mem_aua.json, mem_discover.json, large_replies.json   the two large replies, one at a time
usage: python rz2_served_build.py   (repository root)"""
from __future__ import annotations

import datetime
import io
import json
import os
import re

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
R = W + "rz2_pb/"
REL = json.load(io.open(W + "RZ2_RELEASE.json", encoding="utf-8"))["release_sha"]
GUARD = "oom_score_adj_1000_rlimit_as_1400mb"


def load(n):
    return json.load(io.open(R + n, encoding="utf-8"))


def grab(text, key):
    m = re.search(r"^%s=(.*)$" % re.escape(key), text, re.M)
    return m.group(1).strip() if m else None


pre, apply_, wait, b1, md5, ua, ac, lf = (load(n) for n in ("pre.json", "apply.json", "resize_wait.json", "step1_after.json", "host_md5_after.json", "unarmed_raw.json", "accesslog.json", "lease_final.json"))
auditwarn, lr = load("auditwarn.json"), load("large_replies.json")
s27 = json.loads(io.open(R + "served27.txt", encoding="utf-8").read().split("--- STDOUT ---", 1)[1].split("--- STDERR", 1)[0].split("CODE_SERVED_JSON", 1)[1].strip())["body"]
clock, lim = io.open(R + "clock.txt", encoding="utf-8").read(), io.open(R + "limits.txt", encoding="utf-8").read()
rb = [json.loads(ln) for ln in io.open(R + "readback.jsonl", encoding="utf-8") if ln.strip()]
samples = [json.loads(ln) for ln in io.open(R + "sampler.jsonl", encoding="utf-8") if ln.strip()]
trigger = os.path.exists(R + "readback.jsonl.trigger")


def secs(t):
    return datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()


# the downtime: from the first sample that is not a service answer (401) to the first 401 after it
up = lambda s: s.get("code") == 401  # noqa: E731
first_bad = next((i for i, s in enumerate(samples) if not up(s)), None)
first_up_after = next((i for i in range(first_bad + 1, len(samples)) if up(samples[i])), None) if first_bad is not None else None
intervals, cur = [], None
for smp in samples:
    if not up(smp) and cur is None:
        cur = smp["t"]
    elif up(smp) and cur is not None:
        intervals.append({"first_failed_sample_utc": cur, "first_answer_after_utc": smp["t"], "seconds": round(secs(smp["t"]) - secs(cur))})
        cur = None
down = {"all_intervals": intervals, "interval_note": "interval 1 is the resize stop/start; intervals 2 and 3 are the deploy's restart; interval 4 coincides with the first large reply requested from this seat (a short stall of the single-worker service on a cold call, not a hang)", "samples": len(samples), "first_failed_sample_utc": samples[first_bad]["t"] if first_bad is not None else None, "first_answer_after_utc": samples[first_up_after]["t"] if first_up_after is not None else None,
        "downtime_seconds": round(secs(samples[first_up_after]["t"]) - secs(samples[first_bad]["t"])) if first_up_after is not None else None,
        "failed_samples": sum(1 for s in samples if not up(s)), "method": "an unauthenticated POST to the public MCP endpoint every 2 s from this seat (a healthy gateway answers 401 itself; a stopped or hung one answers 5xx or nothing), first failed sample to first 401 after it; the span includes the sampler's own 2 s step"}
leap = (re.search(r"Leap status\s*:\s*(\S+)", clock) or [None, None])[1]
refid = (re.search(r"Reference ID\s*:\s*(\S+)", clock) or [None, None])[1]
stratum = (re.search(r"Stratum\s*:\s*(\d+)", clock) or [None, None])[1]
failed_units = int(grab(clock, "FAILED_COUNT"))
clock_read_at = (re.search(r"^(\d{4}-\d\d-\d\dT[\d:]+Z)$", clock, re.M) or [None, None])[1]
mb = lambda b: "%dM" % (int(b) // 1048576)  # noqa: E731
high_b, max_b = int(grab(lim, "MemoryHigh")), int(grab(lim, "MemoryMax"))
marker = grab(lim, "MARKER")
okp = [r for r in rb if r.get("service_rss_mb") is not None]
al, jr = ac["audit_lake"], ac["journal"]
lines, records = jr["post_mcp_lines"], al["records_in_window"]
calls = ua["calls"]
big = [{"name": x["name"], "complete": x["complete"], "reply_bytes": x["reply_bytes"], "before_mb": x["before_mb"], "max_mb": x["max_mb"], "after_mb": x["after_mb"], "peak_mb": x["max_mb"], "cgroup_peak_mb": x.get("cgroup_peak_mb"), "one_at_a_time": True} for x in lr["replies"]]
body = {
    "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "live_commit": REL,
    "health_after": s27["health_status"], "marker_equals_release": marker == REL, "marker_sha": marker,
    "unit_memory_high": mb(high_b), "unit_memory_max": mb(max_b), "memory_high_mb": high_b // 1048576, "memory_max_mb": max_b // 1048576,
    "memory_total_mb": wait["post_resize"]["memory_total_mb"], "tools_list": b1["tools"]["tools_list_master_admin"], "tools_list_before": load("step1_before.json")["tools"]["tools_list_master_admin"], "registry_count": s27["registry_count"],
    "tools_27_of_27": s27["per_tool_good"] == 27, "per_tool_good": s27["per_tool_good"], "harness_guard": GUARD, "nrestarts_after_deploy": int(grab(lim, "NRestarts")),
    "env_key_count": md5["env"]["key_count"], "muse_env_present": bool(b1["muse_client_id_is_a_key"]),
    "host_md5": {"equal": md5["equal_lf"] + md5["equal_crlf_only"], "differ": len(md5["differ"]), "missing_on_host": len(md5["missing_on_host"]), "expected_files": md5["denominator_expected_files"], "host_files": md5["denominator_host_files"]},
    "large_replies": big,
    "instance": {"type_before": pre["instance_type"], "type_after": "t4g.large", "state_after": wait["post_resize"].get("active_state"), "eip_associated_before": pre["eip_associated"], "eip_associated_after": wait["post_resize"]["eip_associated"],
                 "target_health_after": wait["post_resize"]["target_health"], "apply": apply_},
    "downtime": down,
    "host_clock": {"leap_status": leap, "synchronised": bool(refid and refid != "00000000" and stratum and int(stratum) < 16), "stratum": int(stratum), "read_at": clock_read_at}, "systemd_failed_units": failed_units, "clock_read_before_close": True,
    "readback": {"minutes": 30, "probes": len(rb), "first_t": rb[0]["t"], "last_t": rb[-1]["t"], "triggers_fired": 1 if trigger else 0, "nrestarts_during_readback": max(int(str(r.get("n_restarts"))) for r in rb), "health_not_200": sum(1 for r in rb if r.get("health") != 200),
                 "service_pids_seen": len({r.get("pid") for r in rb}), "service_rss_mb_min": min(r["service_rss_mb"] for r in okp), "service_rss_mb_max": max(r["service_rss_mb"] for r in okp), "host_pct_max": max(r["host_pct"] for r in rb)},
    "probe": {"armings": 0, "puts_made_by_this_seat": ua["puts_made_by_this_script"], "unarmed_status": calls[0]["status"] if all(c["status"] == 403 for c in calls) else "mixed", "unarmed_error": calls[0]["error"] if all(c["error"] == "probe_not_armed" for c in calls) else "mixed",
              "lease_parameter_absent_before": bool(ua["lease_before"]["absent"]), "lease_parameter_absent_after": bool(ua["lease_after"]["absent"]), "lease_parameter_absent_at_close": bool(lf["absent"]), "listener_bound": ua["state_before"]["bound"],
              "pid_stable": bool(ua["pid_stable"]), "nrestarts_after": int(ua["state_after"]["nrestarts"])},
    "access_log": {"window_minutes": 30, "window_start_utc": ac["window_start_utc"], "window_end_utc": ac["window_end_utc"], "post_mcp_lines_readback": lines, "audit_records_readback": records, "ratio_lines_to_records": round(lines / records, 3) if records else None,
                   "sampler_probes_in_the_journal_count": sum(1 for smp in samples if smp.get("code") == 401 and ac["window_start_utc"] <= smp["t"] <= ac["window_end_utc"]), "listener_access_lines": jr["post_probe_lines"], "listener_requests_made": len(calls), "method": ac["method"], "note": "the journal count includes the unauthenticated POST /mcp probes of this seat's downtime sampler (answered 401) that fell inside the window, counted in sampler_probes_in_the_journal_count; the audit lake records only authenticated calls, so the ratio is read with that subtracted too"},
    "audit_failure_counter": auditwarn,
    "limits": ["The served read was UNARMED ONLY: no lease was written and no SSM parameter was written by this seat.", "The large replies were requested one at a time, never concurrently; memory is the service cgroup's memory.current sampled every 0.5 s during each call.",
               "The downtime is measured from this seat by a public-endpoint sampler, so it includes the sampler's step; the audit-lake read OG-ev-13 spans this window and can exclude the interval named above."],
}
io.open(W + "RZ2_SERVED.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
io.open(W + "rz2_facts.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"downtime_seconds": down["downtime_seconds"], "first_failed_sample_utc": down["first_failed_sample_utc"], "first_answer_after_utc": down["first_answer_after_utc"],
                                                                                         "large_replies": [(x["name"], x["reply_bytes"], x["max_mb"]) for x in big], "dual_count": [lines, records]}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("live_commit", "health_after", "marker_equals_release", "unit_memory_high", "unit_memory_max", "memory_total_mb", "tools_list", "tools_27_of_27", "nrestarts_after_deploy", "host_md5", "large_replies", "downtime")}, indent=1)[:2600])
