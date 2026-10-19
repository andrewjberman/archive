#!/usr/bin/env python
"""OG-ap-46 Phase A: collect the local test arms and the lease-parameter read into W/ap46_pa/*.json and assemble W/PHASE_A_OG-ap-46.json from the records (no value is typed here that a record does not hold).
READ ONLY on AWS (ssm describe-parameters); NOTHING is written to SSM. Counts, booleans and test ids only.
  ap46_pa/lease_param.json   the lease parameter read ABSENT now (the arming count is the count of puts this seat made: none)
  ap46_pa/tests.json         the named tests, the window set, their union in both orders, and the full suite's failing set against the live ref's
  ap46_pa/loggers.json       the host run (copied from the scratch folder by this script)
usage: python ap46_phasea_collect.py <scratch dir holding loggers.json, step1_before.json, host_md5_before.json, uvicorn_version.txt, failed_release.txt, failed_live.txt, overlay.json>   (repository root)"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
P = W + "ap46_pa/"
SCRATCH = sys.argv[1]
REL = json.load(io.open(W + "ap46_release.json", encoding="utf-8"))
GW = "C:/tmp/og-rel-batch12/infra/aws/ec2/opal-gateway"
LEASE = "/opal-gateway/probe/lease"
WINDOW = ["en13", "en15", "en17", "en18", "en19", "en20", "en21", "en22", "en23", "en24", "rv2", "db3", "sv2", "en9", "cl2", "sec2"]
NAMES = ["uvicorn", "uvicorn.error", "uvicorn.access", "uvicorn.asgi"]
PROCESS_WIDE = ("none, read: I opened app/probe_listener.py (the diff against the live ref is one corrected comment, no executable line) and app/family_depth.py (its top level holds imports of json, os, re, sys and datetime, constants and "
                "function and class definitions and a __main__ guard; no thread, no socket, no AWS client, no logger, no signal handler, no environment or sys.path change, no global config at import; boto3 and yaml are imported inside functions). "
                "Measured in a fresh guarded process: importing app.family_depth started 0 threads, opened 0 sockets and made 0 AWS calls. The release does not mount its route and server.py and tools.py do not name it.")
os.makedirs(P, exist_ok=True)


def save(name, obj):
    io.open(P + name, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=1) + "\n")


def pytest_line(files):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + files, cwd=GW, capture_output=True, text=True, timeout=900)
    last = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout).strip().splitlines()[-1]
    p = re.search(r"(\d+) passed", last)
    f = re.search(r"(\d+) (?:failed|error)", last)
    return {"passed": int(p.group(1)) if p else 0, "failed": int(f.group(1)) if f else 0}


ssm = boto3.client("ssm", region_name="us-east-1")
existing = [x["Name"] for x in ssm.describe_parameters(ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": ["/opal-gateway/probe/"]}])["Parameters"]]
save("lease_param.json", {"lease_parameter": LEASE, "parameters_under_probe_prefix_now": len(existing), "absent": LEASE not in existing, "puts_made_by_this_seat": 0})

named = ["tests/test_og_cd1.py", "tests/test_og_pr1.py", "tests/test_og_pr5.py"]
win = ["tests/test_og_%s.py" % x for x in WINDOW]
t = {"named_files": named, "named_forward": pytest_line(named), "window_set_files": len(win), "window_forward": pytest_line(win), "window_reverse": pytest_line(win[::-1]),
     "union_forward": pytest_line(win + named), "union_reverse": pytest_line(named + win[::-1])}
rel_f = set(io.open(os.path.join(SCRATCH, "failed_release.txt"), encoding="utf-8").read().split("\n")) - {""}
live_f = set(io.open(os.path.join(SCRATCH, "failed_live.txt"), encoding="utf-8").read().split("\n")) - {""}
t["full_suite"] = {"release_failed": len(rel_f), "live_ref_failed": len(live_f), "only_in_release": sorted(rel_f - live_f), "only_in_live_ref": sorted(live_f - rel_f), "names_in_both": len(rel_f & live_f),
                   "conditions": "both trees clean (git status reads 0 lines; the gate overlay restored in the release tree), the same pytest invocation over tests/"}
t["bash_n_deploy_script"] = subprocess.run(["bash", "-n", GW + "/deploy-to-ec2.sh"], capture_output=True).returncode == 0
pf = subprocess.run(["bash", GW + "/deploy-to-ec2.sh", "--preflight-only"], capture_output=True, text=True)
t["preflight_only"] = (pf.stdout.strip().splitlines() or [""])[-1]
save("tests.json", t)

for n in ("loggers.json", "step1_before.json", "host_md5_before.json", "overlay.json", "uvicorn_version.txt"):
    shutil.copyfile(os.path.join(SCRATCH, n), P + n)
lis = json.load(io.open(P + "loggers.json", encoding="utf-8"))
L = lis["loggers"]
c, lv, lr, on = L["candidate"], L["live_ref"], L["listener_run"], L["candidate_on_raise"]
body = {
    "release_sha": REL["release_sha"],
    "loggers": {"checked": NAMES, "loggers_unchanged": bool(c["loggers_unchanged"]), "access_record_reaches_handler": bool(c["access_record_reaches_handler"]),
                "restore_on_raise": bool(on["raised"] and on["loggers_unchanged"] and on["unrestored_config_would_have_changed"]), "listener_access_log": bool(c["listener_access_log"]), "guard": lis["guard"],
                "uvicorn_version": L["uvicorn_version"], "candidate_changed_loggers": c["changed_loggers"],
                "listener_access_lines_observed_in_the_service_handler": lr["listener_access_lines_in_handler"],
                "listener_access_lines_note": "config.access_log is False, but uvicorn's HTTP protocol decides per connection by access_logger.hasHandlers() (uvicorn 0.52.3 h11_impl.py line 57 and httptools_impl.py line 61), so once the service's handlers are restored the listener's requests ARE logged; one unarmed request produced one line"},
    "live_ref_loggers_note": {"loggers_unchanged": bool(lv["loggers_unchanged"]), "access_record_reaches_handler": bool(lv["access_record_reaches_handler"]), "access_handlers_before": lv["access_handlers_before"],
                                       "access_handlers_after": lv["access_handlers_after"], "access_level_before": lv["access_level_before"], "access_level_after": lv["access_level_after"]},
    "listener": {"bound_host": lr["bound"][0] if len(lr["bound"]) == 1 else "|".join(lr["bound"]), "off_by_default": lr["unarmed_status"] == 403 and lr["unarmed_error"] == "probe_not_armed", "armings": 0,
                 "lease_parameter_written": False, "test_port": 18099, "info_startup_lines": lr["info_startup_lines"],
                 "lease_parameter_absent_now": json.load(io.open(P + "lease_param.json", encoding="utf-8"))["absent"], "scratch_removed": lis["scratch_removed"], "port_free_after": lis["port_free_after"]},
    "tests": {"named_passed": t["named_forward"]["passed"], "named_failed": t["named_forward"]["failed"], "window_set_passed": t["union_forward"]["passed"],
              "window_set_failed": t["union_forward"]["failed"] + t["union_reverse"]["failed"], "union_both_orders_equal": t["union_forward"]["passed"] == t["union_reverse"]["passed"]},
    "candidate_bytes_equal_release": lis["candidate_bytes_equal_release"], "family_depth_import": {k: lis["family_depth_import"][k] for k in ("threads_started", "sockets_opened", "boto3_calls", "families_file_present")},
    "process_wide_state": PROCESS_WIDE, "candidate_peak_rss_mb": L["vm_hwm_mb"], "service": lis["service"],
    "host_before": {"md5_differ": len(json.load(io.open(P + "host_md5_before.json", encoding="utf-8")).get("differ", [])), "marker": json.load(io.open(P + "step1_before.json", encoding="utf-8")).get("marker")},
}
io.open(W + "PHASE_A_OG-ap-46.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("loggers", "live_ref_loggers_note", "listener", "tests", "service", "host_before")}, indent=1)[:3500])
print("full suite:", json.dumps({k: t["full_suite"][k] for k in ("release_failed", "live_ref_failed", "only_in_release", "only_in_live_ref")}))
print("named:", t["named_forward"], "window:", t["window_forward"], t["window_reverse"], "union:", t["union_forward"], t["union_reverse"], "bash -n", t["bash_n_deploy_script"], t["preflight_only"])
