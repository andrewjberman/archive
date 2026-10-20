#!/usr/bin/env python
"""OG-rl-17 Phase A: assemble W/PHASE_A_OG-rl-17.json from the records (no value is typed here that a record holds). READ ONLY on AWS (ssm describe-parameters); NOTHING is written to SSM, IAM or the audit lake.
usage: python rl17_phasea.py <scratch tests.json>   (repository root; W/rl17_pa/host_leg.json and step1_before.json already written)"""
from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
P = W + "rl17_pa/"
REL = json.load(io.open(W + "rl17_release.json", encoding="utf-8"))
TREE = "C:/tmp/og-rel-batch16/infra/aws/ec2/opal-gateway"
LEASE = "/opal-gateway/probe/lease"
shutil.copyfile(sys.argv[1], P + "tests.json")
t = json.load(io.open(P + "tests.json", encoding="utf-8"))
hl = json.load(io.open(P + "host_leg.json", encoding="utf-8"))
s1 = json.load(io.open(P + "step1_before.json", encoding="utf-8"))
ssm = boto3.client("ssm", region_name="us-east-1")
existing = [x["Name"] for x in ssm.describe_parameters(ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": ["/opal-gateway/probe/"]}])["Parameters"]]
lease = {"lease_parameter": LEASE, "parameters_under_probe_prefix_now": len(existing), "absent": LEASE not in existing, "puts_made_by_this_seat": 0}
io.open(P + "lease_param.json", "w", encoding="utf-8", newline="\n").write(json.dumps(lease, indent=1) + "\n")
bash_n = subprocess.run(["bash", "-n", TREE + "/deploy-to-ec2.sh"], capture_output=True).returncode == 0
pf = subprocess.run(["bash", TREE + "/deploy-to-ec2.sh", "--preflight-only"], capture_output=True, text=True)
preflight = (pf.stdout.strip().splitlines() or [""])[-1]
imp, gb, fe, ct = hl["imports"], hl["guard_burst"], hl["fences"], hl["contract"]

PROCESS_WIDE = (
    "The service imports one new module, app/inflight_guard.py, whose module-level instance `guard` is a process-wide object (constants MAX_INFLIGHT %d and QUEUE_WAIT_S 20.0; the asyncio primitives are created lazily inside the running loop, "
    "so import creates no semaphore, task or loop), and app/tools.py's _PolicyGuardedMCP.call_tool, the dispatch chokepoint of EVERY tool, now runs the tool body inside `async with inflight_guard.guard.slot(name)` after the entitlement denial "
    "(a denied call takes no slot): a fifth concurrent call waits up to 20 s and is then returned as an enveloped gateway_busy refusal, audited as denied/gateway_busy. app/harvest_typed.py's project() (used by every typed tool and the client core) "
    "now measures size as json.dumps(indent=2). READ, not instrumented: I opened app/inflight_guard.py whole (76 lines: imports asyncio, contextlib and typing, two constants, the Busy exception, the InflightGuard class and `guard = InflightGuard()`), "
    "the OG-mg-3 hunks of app/tools.py (the added import and the try/except around call_tool; no other module-level statement) and the OG-sz-1 hunks of app/harvest_typed.py (the _size measure and project()). "
    "No logger, handler, signal, thread, socket, environment read, sys.path change or global-config change happens at import. tools/list does NOT change: the candidate registry counted %d tools on the host against %d at the live ref (no tool is added). "
    "Nothing arms the probe listener or writes any parameter." % (4, imp["registry_count_in_candidate"], s1["tools"]["tools_list_master_admin"]))
n_red = len(t["named_new_reds_against_live_ref"])
body = {
    "release_sha": REL["release_sha"], "base_sha": REL["base_sha"], "trunk_sha": REL["trunk_sha"],
    "tests": {"named_passed": t["named_forward"]["passed"], "named_failed": n_red, "named_failed_definition": "named-set failures that do NOT also fail at the live ref (new reds); the literal failure count is in named_failed_literal and the same-at-live-ref reds are counted beside it",
              "named_failed_literal": t["named_forward"]["failed"], "named_reds_same_at_live_ref": len(t["named_reds_same_at_live_ref"]), "named_both_orders_equal": t["named_forward"]["passed"] == t["named_reverse"]["passed"] and t["named_forward"]["failed"] == t["named_reverse"]["failed"],
              "named_files": t["named_files"], "named_files_new_in_release": t["named_files_new_in_release"],
              "window_set_passed": t["window_forward"]["passed"], "window_set_failed": t["window_forward"]["failed"] + t["window_reverse"]["failed"], "window_both_orders_equal": t["window_forward"]["passed"] == t["window_reverse"]["passed"],
              "window_files": t["window_files"], "window_set_definition": "the existing test_og_* files outside the named set that are GREEN at the live ref; the files red at the live ref are listed in the tests record and compared per test id in the full suite",
              "suite_difference_named": True, "full_suite": {"release_failed": t["full_suite"]["release_failed"], "live_ref_failed": t["full_suite"]["live_ref_failed"], "only_in_release": t["full_suite"]["only_in_release"],
                                                            "only_in_live_ref": t["full_suite"]["only_in_live_ref"], "only_in_release_explained": t["full_suite"]["only_in_release_explained"]},
              "standards_copy_overlay": t["standards_copy_overlay"], "standards_copy_restored_to_live_ref_bytes": t["standards_copy_restored_to_live_ref_bytes"]},
    "bash_n_deploy_script": bash_n, "preflight_only": preflight,
    "host_shaped_import_check": {"modules": imp["modules"], "imported": imp["imported"], "failed": imp["failed"], "registry_count_in_candidate": imp["registry_count_in_candidate"], "guard": hl["guard"]},
    "guard_burst": {"limit": gb["limit"], "ran": gb["ran"], "refused": gb["refused"], "code": gb["code"], "raised": gb["raised"], "max_concurrent_bodies": gb["max_concurrent_bodies"], "audit_rows_denied_gateway_busy": gb["audit_rows_denied_gateway_busy"],
                    "single_call_after_burst_runs": gb["single_call_after_burst_runs"], "snapshot": gb["snapshot"], "guard": hl["guard"]},
    "fences": {"orion": fe["fences"]["orion"], "eclipse": fe["fences"]["eclipse"], "commonwealth": fe["fences"]["commonwealth"], "controls_unserved_pairs": fe["controls"], "guard": hl["guard"]},
    "contract": {"copies_equal": ct["copies_equal"], "target_memory_mib": ct["target_memory_mib"]},
    "listener": {"bound_host": "127.0.0.1", "off_by_default": True, "armings": 0, "lease_parameter_written": False, "lease_parameter_absent_now": lease["absent"],
                 "basis": "probe_listener.py is not in this release (byte-equal to the live ref) and the running service was not touched; the lease parameter was read absent and no SSM write was made"},
    "process_wide_state": PROCESS_WIDE,
    "service": hl["service"], "scratch_removed": hl["scratch_removed"], "candidate_bytes_equal_release": hl["candidate_bytes_equal_release"],
    "host_before": {"marker": s1["marker"].split("=", 1)[-1], "marker_state": s1["marker"].split("=", 1)[0], "tools_list": s1["tools"]["tools_list_master_admin"], "env_key_count": s1["env_key_count"], "unit_memory_high": "%dM" % (int(s1["unit"]["MemoryHigh"]) // 1048576), "unit_memory_max": "%dM" % (int(s1["unit"]["MemoryMax"]) // 1048576)},
}
io.open(W + "PHASE_A_OG-rl-17.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("tests", "guard_burst", "fences", "contract", "listener", "host_shaped_import_check", "bash_n_deploy_script", "preflight_only")}, indent=1)[:3800])
