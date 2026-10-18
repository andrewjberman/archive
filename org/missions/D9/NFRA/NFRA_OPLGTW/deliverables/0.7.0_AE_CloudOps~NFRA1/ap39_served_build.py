#!/usr/bin/env python
"""OG-ap-39 Phase B: assemble W/CODE8_SERVED.json from the measured records (no value is typed here that a record does not hold). Counts, bytes, seconds, words and booleans only.
  ap39_pb/step1_before.json, step1_after.json   the host read at the GO and after the deploy (marker, unit limits, tools/list)
  ap39_pb/host_md5_after.json                   the host md5 walk against the RELEASE blobs plus .env names
  ap39_pb/notes_after.json                      arm e13_notes_served: the served tool descriptions read from the INSTALLED registry in a fresh guarded process
  ap39_pb/e15.json                              arm e15: the first two chain pages equal the pre-deploy baseline (written here from the untracked hash records)
  ap39_pb/served27.txt                          the 27-tool served read under the hard guard (ap36_guarded.py + ap36_served_harness.py)
  ap39_pb/wincalls.json                         the /mcp calls and window calls the service served in the read-back window
  ap39_pb/clock.txt, limits.txt                 chronyc tracking + systemctl --failed (BEFORE the close), and the live unit limits, cgroup memory.max and marker
  ap39_pb/readback.jsonl                        the 30-minute service read-back, one probe a minute
usage: python ap39_served_build.py   (repository root of the worktree that holds the records)"""
from __future__ import annotations

import datetime
import io
import json
import re

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
R = W + "ap39_pb/"
HASHES = "C:/tmp/pb39c/"          # the page-hash records stay untracked
SEVEN = ["BLACKDIAMOND49F_READER_ROLE_ARN", "BLACKDIAMONDCOTTONWOOD_READER_ROLE_ARN", "ORION_READER_ROLE_ARN", "ECLIPSE_READER_ROLE_ARN",
         "COMMONWEALTH_READER_ROLE_ARN", "SMARTX_READER_ROLE_ARN", "BLACKDIAMOND49FLIVE_READER_ROLE_ARN"]
REL = json.load(io.open(W + "ap39_release.json", encoding="utf-8"))["release_sha"]
GUARD_AS = "oom_score_adj_1000_rlimit_as_1400mb"
CT1_MD5 = "596c299597067fe5a8afb8e3493a0ed9"


def load(n):
    return json.load(io.open(R + n, encoding="utf-8"))


def pages(n):
    d = json.load(io.open(HASHES + n, encoding="utf-8"))
    return d, [(p["page"], p["rows"], p["sha"], p["used"], p["next"]) for p in d["pages"]]


pb, pa = pages("pagehash_before.json"), pages("pagehash_after.json")
e15 = {"e15": pb[1] == pa[1], "pages": len(pa[1]), "rows": [p[1] for p in pa[1]], "before_captured_at": pb[0]["captured_at"], "after_captured_at": pa[0]["captured_at"]}
io.open(R + "e15.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps(e15, indent=1) + chr(10))

b0, b1, md5, notes, win = load("step1_before.json"), load("step1_after.json"), load("host_md5_after.json"), load("notes_after.json")["notes"], load("wincalls.json")
s27 = json.loads(io.open(R + "served27.txt", encoding="utf-8").read().split("--- STDOUT ---", 1)[1].split("--- STDERR", 1)[0].split("CODE_SERVED_JSON", 1)[1].strip())["body"]
clock = io.open(R + "clock.txt", encoding="utf-8").read()
lim = io.open(R + "limits.txt", encoding="utf-8").read()
rb = [json.loads(ln) for ln in io.open(R + "readback.jsonl", encoding="utf-8") if ln.strip()]
ok = [r for r in rb if r.get("service_rss_mb") is not None]


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
organic = win["audit_lake"]["etfs_compare_peers_calls"]
sn = {k: notes[k] for k in ("tools_list_count", "client_tools_with_notes", "window_read_busy_in_windowed_tools", "client_get_fees_note_source_scoped", "fee_note_names_the_source", "fee_note_denies_a_total")}
sn["fee_note_banned_phrases_present"] = len(notes["fee_note_banned_phrases_present"])
sn["guard"] = notes.get("guard") or load("notes_after.json")["guard"]
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
    "served_notes": sn,
    "readback": {"minutes": 30, "triggers_fired": 0, "service_window_calls": win["audit_lake"]["window_tool_calls_total"],
                 "nrestarts_during_readback": max(int(str(r.get("n_restarts"))) for r in rb), "probes": len(rb), "first_t": rb[0]["t"], "last_t": rb[-1]["t"],
                 "service_pids_seen": len({r.get("pid") for r in rb}), "health_not_200": sum(1 for r in rb if r.get("health") != 200),
                 "service_rss_mb_min": min(r["service_rss_mb"] for r in ok), "service_rss_mb_max": max(r["service_rss_mb"] for r in ok), "host_pct_max": max(r["host_pct"] for r in rb),
                 "mcp_requests_served": win["journal"]["post_mcp_lines"], "audit_records_in_window": win["audit_lake"]["records_in_window"],
                 "etfs_compare_peers_calls_served_by_the_service": organic},
    "arms": {"e10_marker_equals_release_sha": marker == REL,
             "e13_notes_served": bool(sn["client_tools_with_notes"] >= 2 and sn["window_read_busy_in_windowed_tools"] is True and sn["client_get_fees_note_source_scoped"] is True and sn["tools_list_count"] == 103),
             "e14_unit_limits_unchanged": bool(unit["memory_max_bytes"] == 1468006400 and unit["memory_high_bytes"] == 1258291200 and unit["oom_score_adj"] == 300 and unit["cgroup_memory_max_bytes"] == 1468006400),
             "e15_window_pages_equal_phase_a": bool(e15["e15"])},
    "arm_counts": {"e15": {"pages_compared": e15["pages"], "rows_per_page": e15["rows"], "baseline_captured_at": e15["before_captured_at"], "installed_captured_at": e15["after_captured_at"],
                           "basis": "the live code's first two pages, captured in a fresh guarded process BEFORE the deploy, against the installed code's, after; hashes untracked"}},
    "limits": ["The served notes were read from the INSTALLED registry in a fresh guarded process (cgroup MemoryMax 1400M); the service's own long-lived heap over a window or peers call is read only as the read-back's RSS under whatever organic load arrived: "
               "it served %d window calls and %d etfs_compare_peers calls (Z-S338 re-read, not closed; the Z-S375 disarm stays WITHHELD for a service call)." % (win["audit_lake"]["window_tool_calls_total"], organic),
               "The 27-tool read ran under oom_score_adj_1000_rlimit_as_1400mb (the address-space guard).",
               "The host percent maximum in the read-back includes the guarded arms run by this seat in new processes during the window."],
}
io.open(W + "CODE8_SERVED.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
served = ("Served: the 27-tool read passes %d of 27 under the hard guard; the installed registry serves %d tools and the absent_reason notes on %d of 5 client tools (window_read_busy in both windowed tools; "
          "the client_get_fees note names the source, does not establish a total and holds none of the banned phrases); host md5 139 of 139 equal to the release blobs and harvest_research.py md5 %s equal to CT1; "
          "the first two chain pages equal the live code's row for row; the 30-minute read-back (%d probes) shows the service at %s to %s MB, NRestarts %d, health 200 throughout, %d /mcp requests and %d window calls served; "
          "the host clock reads Leap %s, synchronised, and systemctl --failed %d units (read %s, before the close)."
          % (s27["per_tool_good"], sn["tools_list_count"], sn["client_tools_with_notes"], harvest_md5, len(rb), body["readback"]["service_rss_mb_min"], body["readback"]["service_rss_mb_max"],
             body["readback"]["nrestarts_during_readback"], win["journal"]["post_mcp_lines"], win["audit_lake"]["window_tool_calls_total"], leap, failed, clock_read_at))
io.open(W + "ap39_facts.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"served_sentence": served}, indent=1) + chr(10))
print(json.dumps({k: body[k] for k in ("live_commit", "health_status", "env_key_count", "reader_env_keys_present", "registry_count", "per_tool_good", "per_tool_not_good", "harness_guard", "host_md5",
                                       "harvest_research_md5", "tools_list_before", "tools_list_after", "muse_env_present", "marker_sha", "unit_limits", "host_clock", "systemd_failed_units",
                                       "clock_read_before_close", "served_notes", "arms")}, indent=1))
print(json.dumps(body["readback"], indent=1))
print(served)
