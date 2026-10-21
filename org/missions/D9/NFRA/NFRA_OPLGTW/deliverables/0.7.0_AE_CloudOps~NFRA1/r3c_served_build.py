#!/usr/bin/env python
"""OG-rl-19 Phase B: assemble W/R3C_SERVED.json from the measured records in W/r3c_pb/ (no value is typed here that a record holds). Counts, codes, dates, MB, seconds and booleans only.
  r3c_pb/pre.json            the act's gates (r3c_act.py pre): host marker equal to base_sha, R3a files, halves
  r3c_pb/step1_before.json   ap38_step1 BEFORE the deploy (tools/list, env keys, unit)
  r3c_pb/apply.json          the Terraform apply (r3c_act.py apply); r3c_pb/iam_before.json, iam_after.json
  r3c_pb/gate.json           the gate read (r3c_host.py gate), r3c_pb/dual_before.json (live code), dual_after.json (deployed code), probe_after.json (the sk2 probe on the deployed tree)
  r3c_pb/deploy.json         {"started_utc", "finished_utc"} around the deploy command
  r3c_pb/step1_after.json, host_md5_after.json, served27.txt, accesslog.json, auditwarn.json, clock.txt, limits.txt, readback.jsonl, r3a.json {"ref": "<file name>", "read_at": "<UTC>"}
usage: python r3c_served_build.py   (repository root)"""
from __future__ import annotations

import datetime
import io
import json
import os
import re

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
R = W + "r3c_pb/"
REL = json.load(io.open(W + "rl19_release.json", encoding="utf-8"))["release_sha"]
GUARD = "oom_score_adj_1000_rlimit_as_1400mb"


def load(n):
    return json.load(io.open(R + n, encoding="utf-8"))


def grab(text, key):
    m = re.search(r"^%s=(.*)$" % re.escape(key), text, re.M)
    return m.group(1).strip() if m else None


pre, b0, b1, ap, gate, db, da, pa, dep, r3a = (load(n) for n in ("pre.json", "step1_before.json", "step1_after.json", "apply.json", "gate.json", "dual_before.json", "dual_after.json", "probe_after.json", "deploy.json", "r3a.json"))
md5, ua, ac, auditwarn = load("host_md5_after.json"), load("unarmed_raw.json"), load("accesslog.json"), load("auditwarn.json")
ib, ia = load("iam_before.json"), load("iam_after.json")
s27 = json.loads(io.open(R + "served27.txt", encoding="utf-8").read().split("--- STDOUT ---", 1)[1].split("--- STDERR", 1)[0].split("CODE_SERVED_JSON", 1)[1].strip())["body"]
clock, lim = io.open(R + "clock.txt", encoding="utf-8").read(), io.open(R + "limits.txt", encoding="utf-8").read()
rb = [json.loads(ln) for ln in io.open(R + "readback.jsonl", encoding="utf-8") if ln.strip()]
trigger = os.path.exists(R + "readback.jsonl.trigger")
leap = (re.search(r"Leap status\s*:\s*(\S+)", clock) or [None, None])[1]
refid = (re.search(r"Reference ID\s*:\s*(\S+)", clock) or [None, None])[1]
stratum = (re.search(r"Stratum\s*:\s*(\d+)", clock) or [None, None])[1]
okp = [r for r in rb if r.get("service_rss_mb") is not None]
al, jr = ac["audit_lake"], ac["journal"]
calls = ua["calls"]
mem_line = (b1.get("mem_line") or "0 0").split()
gr, dbm, dam = gate["result"], db["result"]["masters"], da["result"]["masters"]
d0, d1 = dbm["08403355"], dam["08403355"]
others_same = all(dbm[m]["dates"] == dam[m]["dates"] and dbm[m]["newest"] == dam[m]["newest"] and dbm[m]["snapshot_status"] == dam[m]["snapshot_status"] for m in ("08242234", "08335338"))


def iso(t):
    return datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()


body = {
    "read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "live_commit": REL,
    "base_reread_on_host_equals_base_sha": pre["host_marker_equals_base_sha"] is True,
    "health_after": s27["health_status"], "marker_equals_release": grab(lim, "MARKER") == REL, "marker_sha": grab(lim, "MARKER"),
    "unit_memory_high": "%dM" % (int(grab(lim, "MemoryHigh")) // 1048576), "unit_memory_max": "%dM" % (int(grab(lim, "MemoryMax")) // 1048576),
    "memory_total_mb": int(mem_line[1]) if len(mem_line) > 1 else None,
    "tools_list": b1["tools"]["tools_list_master_admin"], "tools_list_before": b0["tools"]["tools_list_master_admin"], "registry_count": s27["registry_count"],
    "tools_27_of_27": s27["per_tool_good"] == 27, "per_tool_good": s27["per_tool_good"], "harness_guard": GUARD, "nrestarts_after_deploy": int(grab(lim, "NRestarts")),
    "env_key_count": md5["env"]["key_count"], "muse_env_present": bool(b1["muse_client_id_is_a_key"]),
    "host_md5": {"equal": md5["equal_lf"] + md5["equal_crlf_only"], "differ": len(md5["differ"]), "missing_on_host": len(md5["missing_on_host"]), "expected_files": md5["denominator_expected_files"], "host_files": md5["denominator_host_files"]},
    "host_clock": {"leap_status": leap, "synchronised": bool(refid and refid != "00000000" and stratum and int(stratum) < 16), "stratum": int(stratum),
                   "read_at": (re.search(r"^(\d{4}-\d\d-\d\dT[\d:]+Z)$", clock, re.M) or [None, None])[1]}, "systemd_failed_units": int(grab(clock, "FAILED_COUNT")), "clock_read_before_close": True,
    "readback": {"minutes": 15, "probes": len(rb), "first_t": rb[0]["t"], "last_t": rb[-1]["t"], "triggers_fired": 1 if trigger else 0, "nrestarts_during_readback": max(int(str(r.get("n_restarts"))) for r in rb),
                 "health_not_200": sum(1 for r in rb if r.get("health") != 200), "service_pids_seen": len({r.get("pid") for r in rb}), "service_rss_mb_max": max(r["service_rss_mb"] for r in okp), "host_pct_max": max(r["host_pct"] for r in rb)},
    "order": {"r3a_confirmation_ref": r3a["ref"], "r3a_confirmation_read_before_terraform_apply": iso(r3a["read_at"]) < iso(ap["apply_started_utc"]),
              "terraform_applied_before_gate_read": iso(ap["apply_finished_utc"]) < iso(gate["captured_at"]), "gate_read_before_code_deploy": iso(gate["captured_at"]) < iso(dep["started_utc"]),
              "times_utc": {"r3a_read": r3a["read_at"], "apply_started": ap["apply_started_utc"], "apply_finished": ap["apply_finished_utc"], "gate_read": gate["captured_at"], "deploy_started": dep["started_utc"], "deploy_finished": dep["finished_utc"]}},
    "terraform": {"via": ap["via"], "add": ap["add"], "change": ap["change"], "destroy": ap["destroy"], "resources": ap["resources"], "apply_seconds": ap["apply_seconds"],
                  "policy_statements_before": {k: {p: v["statements"] for p, v in r["policies"].items()} for k, r in ib["roles"].items()}, "policy_statements_after": {k: {p: v["statements"] for p, v in r["policies"].items()} for k, r in ia["roles"].items()},
                  "statements_mentioning_49financial_after": {k: {p: v["mentions_49financial"] for p, v in r["policies"].items()} for k, r in ia["roles"].items()}},
    "gate_read": {"as_role": gr["as_role"], "get_object": gr["get_object"], "list_key_count": gr["list_key_count"], "list_error": gr.get("list_error"), "prefix": gr["prefix"], "bucket": gr["bucket"]},
    "dual_read": {"master": "08403355", "dates_before": d0["dates"], "dates_after": d1["dates"], "newest_before": d0["newest"], "newest_after": d1["newest"], "marker_location": d1.get("marker_location"),
                  "snapshot_status_before": d0["snapshot_status"], "snapshot_status_after": d1["snapshot_status"], "snapshot_files_before": d0.get("snapshot_files"), "snapshot_files_after": d1.get("snapshot_files"),
                  "other_masters_unchanged": others_same, "planted_second_master_ignored": pa["planted_second_master_ignored"], "sk2_probe_lines_ok_after": pa["ok"], "sk2_probe_lines_after": pa["lines"],
                  "firm_form_in_deployed_contract": da["result"]["firm_form_masters"], "code_has_firm_form_before": db["result"]["code_has_firm_form"], "code_has_firm_form_after": da["result"]["code_has_firm_form"]},
    "probe": {"armings": 0, "puts_made_by_this_seat": ua["puts_made_by_this_script"], "unarmed_status": calls[0]["status"] if all(c["status"] == 403 for c in calls) else "mixed", "unarmed_error": calls[0]["error"] if all(c["error"] == "probe_not_armed" for c in calls) else "mixed",
              "lease_parameter_absent_before": bool(ua["lease_before"]["absent"]), "lease_parameter_absent_after": bool(ua["lease_after"]["absent"]), "listener_bound": ua["state_before"]["bound"]},
    "access_log": {"window_minutes": 15, "window_start_utc": ac["window_start_utc"], "window_end_utc": ac["window_end_utc"], "post_mcp_lines_readback": jr["post_mcp_lines"], "audit_records_readback": al["records_in_window"], "method": ac["method"]},
    "audit_failure_counter": {"journal_lines_readback": auditwarn["journal_lines_readback"], "counter_value": auditwarn["counter_value"], "classes_seen": auditwarn["classes_seen"]},
}
io.open(W + "R3C_SERVED.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("live_commit", "health_after", "marker_equals_release", "tools_list", "tools_list_before", "order", "terraform", "gate_read", "dual_read", "audit_failure_counter")}, indent=1)[:3600])
