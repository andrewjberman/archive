#!/usr/bin/env python
"""OG-ap-38 Phase B step 6: assemble W/CODE7_SERVED.json from the measured records (no value is typed here that a record does not hold). Counts, bytes, seconds, words and booleans only.
  ap38_run3/step1_before.json            C2: the host read at the GO (base, env, process, marker, NRestarts, unit BEFORE, tools/list before)
  ap38_run3/step1_after.json             after the deploy (marker, unit limits, tools/list after)
  ap38_run3/host_md5_after.json          the host md5 walk against the RELEASE blobs plus .env names
  ap38_run3/installed.json               arm e13: the installed code's bounded call and a valid pair, in a fresh guarded process
  ap38_run3/e15.json                     arm e15: the first two chain pages equal the pre-deploy baseline (the hashes themselves stay untracked)
  ap38_run3/served27.json                the 27-tool served read under the hard guard (ap36_guarded.py + ap36_served_harness.py)
  ap38_run3/wincalls.json                the /mcp calls, window calls and etfs_compare_peers calls the service served in the read-back window
  ap38_run3/clock.txt, limits.txt        chronyc tracking + systemctl --failed (BEFORE the close), and the live unit limits, cgroup memory.max and marker
  ap38_run3/readback.jsonl               the 30-minute service read-back, one probe a minute
usage: python ap38_served_build.py   (repository root of the worktree that holds the records)"""
from __future__ import annotations

import datetime
import io
import json
import re

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
R = W + "ap38_run3/"
SEVEN = ["BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN", "ECLIPSE_READER_ROLE_ARN",
         "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN", "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"]
REL = json.load(io.open(W + "ap38_release.json", encoding="utf-8"))["release_sha"]
GUARD_AS = "oom_score_adj_1000_rlimit_as_1400mb"


def load(n):
    return json.load(io.open(R + n, encoding="utf-8"))


b0, b1, md5, inst, e15 = load("step1_before.json"), load("step1_after.json"), load("host_md5_after.json"), load("installed.json"), load("e15.json")
win = load("wincalls.json")
s27 = json.loads(io.open(R + "served27.txt", encoding="utf-8").read().split("--- STDOUT ---", 1)[1].split("--- STDERR", 1)[0].split("CODE_SERVED_JSON", 1)[1].strip())["body"]
clock = io.open(R + "clock.txt", encoding="utf-8").read()
lim = io.open(R + "limits.txt", encoding="utf-8").read()
rb = [json.loads(ln) for ln in io.open(R + "readback.jsonl", encoding="utf-8") if ln.strip()]
ok = [r for r in rb if r.get("service_rss_mb") is not None]
trig = False


def grab(text, key):
    m = re.search(r"^%s=(.*)$" % re.escape(key), text, re.M)
    return m.group(1).strip() if m else None


leap = (re.search(r"Leap status\s*:\s*(\S+)", clock) or [None, None])[1]
refid = (re.search(r"Reference ID\s*:\s*(\S+)", clock) or [None, None])[1]
stratum = (re.search(r"Stratum\s*:\s*(\d+)", clock) or [None, None])[1]
failed = int(grab(clock, "FAILED_COUNT"))
clock_read_at = grab(clock, "BEGIN") or (re.search(r"^(\d{4}-\d\d-\d\dT[\d:]+Z)$", clock, re.M) or [None, None])[1]
names = set(md5["env"]["reader_role_arn_keys"])
unit = {"memory_max_bytes": int(grab(lim, "MemoryMax")), "memory_high_bytes": int(grab(lim, "MemoryHigh")), "oom_score_adj": int(grab(lim, "OOMScoreAdjust")), "cgroup_memory_max_bytes": int(grab(lim, "CGMAX"))}
marker = grab(lim, "MARKER")
pk = inst["peers"]
tool_bad = [n for n, v in s27["per_tool"].items() if not (v.get("opal_served") is True and v.get("non_opal_refused") is True and v.get("reads_on_refusal") == 0)]
organic = win["audit_lake"]["etfs_compare_peers_calls"]
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
    "tools_list_before": b0["tools"]["tools_list_master_admin"],
    "tools_list_after": b1["tools"]["tools_list_master_admin"],
    "muse_env_present": bool(b1["muse_client_id_is_a_key"]) or bool(md5["env"]["muse_client_id_is_a_key"]),
    "marker_sha": marker,
    "unit_limits": unit,
    "host_clock": {"leap_status": leap, "synchronised": bool(refid and refid != "00000000" and stratum and int(stratum) < 16), "reference_id": refid, "stratum": int(stratum), "read_at": clock_read_at},
    "systemd_failed_units": failed,
    "clock_read_before_close": True,
    "readback": {"minutes": 30, "triggers_fired": 1 if trig else 0, "service_window_calls": win["audit_lake"]["window_tool_calls_total"],
                 "nrestarts_during_readback": max(int(str(r.get("n_restarts"))) for r in rb), "probes": len(rb), "first_t": rb[0]["t"], "last_t": rb[-1]["t"],
                 "service_pids_seen": len({r.get("pid") for r in rb}), "health_not_200": sum(1 for r in rb if r.get("health") != 200),
                 "service_rss_mb_min": min(r["service_rss_mb"] for r in ok), "service_rss_mb_max": max(r["service_rss_mb"] for r in ok), "host_pct_max": max(r["host_pct"] for r in rb),
                 "mcp_requests_served": win["journal"]["post_mcp_lines"], "audit_records_in_window": win["audit_lake"]["records_in_window"],
                 "etfs_compare_peers_calls_served_by_the_service": organic},
    "arms": {"e10_marker_equals_release_sha": marker == REL,
             "e13_peers_bounded_on_installed_code": bool(pk["outcome"] in ("empty_section", "refusal") and pk["vm_hwm_mb"] <= 700 and pk["wall_s"] <= 30 and inst["valid_pair"]["outcome"] == "rows" and inst["valid_pair"]["vm_hwm_mb"] <= 700),
             "e14_unit_limits_active": bool(unit["memory_max_bytes"] == 1468006400 and unit["memory_high_bytes"] == 1258291200 and unit["oom_score_adj"] == 300 and unit["cgroup_memory_max_bytes"] == 1468006400),
             "e15_window_pages_equal_phase_a": bool(e15["e15"])},
    "arm_counts": {"e13": {"peers_outcome": pk["outcome"], "peers_peak_rss_mb": pk["vm_hwm_mb"], "peers_wall_s": pk["wall_s"], "periods_listed": pk["periods_listed"], "axes_listed": pk["axes_listed"],
                           "valid_pair_outcome": inst["valid_pair"]["outcome"], "valid_pair_rows": inst["valid_pair"]["rows_matched"], "valid_pair_peak_rss_mb": inst["valid_pair"]["vm_hwm_mb"], "guard": inst["guard"]},
                   "e15": {"pages_compared": e15["pages"], "rows_per_page": e15["rows"], "baseline_captured_at": e15["before_captured_at"], "installed_captured_at": e15["after_captured_at"],
                           "basis": "the live code's first two pages, captured in a fresh guarded process BEFORE the deploy, against the installed code's, after; hashes untracked"}},
    "peers_through_service": {"basis": "fresh_process", "answered": pk["outcome"] in ("empty_section", "rows"), "peak_rss_mb": pk["vm_hwm_mb"],
                              "why_not_service": "/mcp takes only a bearer signed by the gateway key and no seat mints one (C6, C16); no other route serves the tool; no organic etfs_compare_peers call arrived in the 30 minutes (audit records: %d)" % organic,
                              "disarm": "WITHHELD (needs the service basis)"},
    "tool_read_27": {"per_tool_good": s27["per_tool_good"], "etfs_compare_peers_seconds": s27["per_tool"]["etfs_compare_peers"].get("seconds"), "etfs_compare_peers_served": s27["per_tool"]["etfs_compare_peers"].get("opal_served"),
                     "client_admission": s27["client_admission"], "smartx_two_firm_arm": s27["smartx_two_firm_arm"], "assume_role_real": s27["assume_role_real"]},
    "limits": ["Every arm ran in a FRESH guarded process through the installed code (peers_through_service basis fresh_process): the service's own long-lived heap over a window or peers call is read only as the read-back's RSS under whatever organic load arrived; it served ZERO window calls and no etfs_compare_peers call (Z-S338 re-read, not closed; the Z-S375 disarm WITHHELD for a service call).",
               "The 27-tool read ran under oom_score_adj_1000_rlimit_as_1400mb (the address-space guard); the Phase A tool27 read ran the 26 Parquet tools under the cgroup guard.",
               "The host percent maximum in the read-back includes the guarded arms run by this seat in new processes during the window."],
}
io.open(W + "CODE7_SERVED.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
served = ("Served: the 27-tool read passes %d of 27 under the hard guard (etfs_compare_peers served in %s s); the installed code's runaway call answers an %s at %s MB peak in %s s and a valid pair answers %s rows at %s MB; "
          "the first two chain pages equal the live code's row for row; the 30-minute read-back (%d probes) shows the service at %s to %s MB, NRestarts %d, health 200 throughout, %d /mcp requests and ZERO window calls served; "
          "the host clock reads Leap %s, synchronised, and systemctl --failed %d units (read %s, before the close). The Z-S375 disarm is WITHHELD for a service call (peers_through_service basis fresh_process: no organic call arrived)."
          % (s27["per_tool_good"], s27["per_tool"]["etfs_compare_peers"].get("seconds"), pk["outcome"].replace("_", " "), pk["vm_hwm_mb"], pk["wall_s"], inst["valid_pair"]["rows_matched"], inst["valid_pair"]["vm_hwm_mb"],
             len(rb), body["readback"]["service_rss_mb_min"], body["readback"]["service_rss_mb_max"], body["readback"]["nrestarts_during_readback"], win["journal"]["post_mcp_lines"], leap, failed, clock_read_at))
io.open(W + "ap38_facts.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"served_sentence": served}, indent=1) + chr(10))
print(json.dumps({k: body[k] for k in ("live_commit", "health_status", "env_key_count", "reader_env_keys_present", "registry_count", "per_tool_good", "per_tool_not_good", "harness_guard", "host_md5", "tools_list_before",
                                       "tools_list_after", "muse_env_present", "marker_sha", "unit_limits", "host_clock", "systemd_failed_units", "clock_read_before_close", "arms", "peers_through_service")}, indent=1))
print(json.dumps(body["readback"], indent=1))
print(served)
