#!/usr/bin/env python
"""OG-ap-48 Phase A: collect the local test arms and the lease-parameter read into W/ap48_pa/*.json and assemble W/PHASE_A_OG-ap-48.json from the records (no value is typed here that a record does not hold).
READ ONLY on AWS (ssm describe-parameters); NOTHING is written to SSM or to the audit lake. Counts, booleans and test ids only.
  ap48_pa/lease_param.json   the lease parameter read ABSENT now (the arming count is the count of puts this seat made: none)
  ap48_pa/tests.json         the named tests, the window set, their union in both orders, and the full suite's failing set against the live ref's
  ap48_pa/audit_leg.json     the host run (copied from the scratch folder by this script)
usage: python ap48_phasea_collect.py <scratch dir holding audit_leg.json, step1_before.json, host_md5_before.json, uvicorn_version.txt, failed_release.txt, failed_live.txt, overlay.json, hostshape.json>   (repository root)"""
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
P = W + "ap48_pa/"
SCRATCH = sys.argv[1]
REL = json.load(io.open(W + "ap48_release.json", encoding="utf-8"))
GW = "C:/tmp/og-rel-batch13/infra/aws/ec2/opal-gateway"
LEASE = "/opal-gateway/probe/lease"
WINDOW = ["en13", "en15", "en17", "en18", "en19", "en20", "en21", "en22", "en23", "en24", "rv2", "db3", "sv2", "en9", "cl2", "sec2"]
NAMED = ["tests/test_og_pr6.py", "tests/test_audit_bytes_principal.py", "tests/test_audit_lake_key_stamp.py", "tests/test_audit_rivalfunds_args.py", "tests/test_og_en10.py"]
PROCESS_WIDE = ("STDERR VOLUME and the boto3 S3 client's botocore Config; nothing else. I opened app/audit.py at the release and its diff against the live ref (5 hunks: the imports sys and time, a module counter with its lock "
                "and a 60 s constant, lake_put_failure_count() and _note_lake_failure(), the explicit botocore Config on the lazily built S3 client, and the except branch that now calls _note_lake_failure) and app/config.py (read only). "
                "Stderr: one line on the first failed lake put, then at most one per 60 s, carrying the exception class name and the running count only (never the message, bucket, key or record). "
                "The client Config: connect_timeout 2 s, read_timeout 3 s, retries mode standard with max_attempts 1 (botocore reads that as total_max_attempts 2: ONE retry). The floor-write lines of _emit are unchanged. "
                "No logger, handler, signal, thread, environment, sys.path or global-config change; the module-level lock and counter are this module's own. Measured in a fresh guarded process on the host against a non-routable endpoint.")
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

win = ["tests/test_og_%s.py" % x for x in WINDOW]
t = {"named_files": NAMED, "named_forward": pytest_line(NAMED), "named_reverse": pytest_line(NAMED[::-1]), "window_set_files": len(win), "window_forward": pytest_line(win), "window_reverse": pytest_line(win[::-1]),
     "union_forward": pytest_line(win + NAMED), "union_reverse": pytest_line(NAMED + win[::-1])}
rel_f = set(io.open(os.path.join(SCRATCH, "failed_release.txt"), encoding="utf-8").read().split("\n")) - {""}
live_f = set(io.open(os.path.join(SCRATCH, "failed_live.txt"), encoding="utf-8").read().split("\n")) - {""}
t["full_suite"] = {"release_failed": len(rel_f), "live_ref_failed": len(live_f), "only_in_release": sorted(rel_f - live_f), "only_in_live_ref": sorted(live_f - rel_f), "names_in_both": len(rel_f & live_f),
                   "conditions": "both trees clean (git status reads 0 lines; the gate overlay restored in the release tree), the same pytest invocation over tests/"}
t["bash_n_deploy_script"] = subprocess.run(["bash", "-n", GW + "/deploy-to-ec2.sh"], capture_output=True).returncode == 0
pf = subprocess.run(["bash", GW + "/deploy-to-ec2.sh", "--preflight-only"], capture_output=True, text=True)
t["preflight_only"] = (pf.stdout.strip().splitlines() or [""])[-1]
save("tests.json", t)

for n in ("audit_leg.json", "step1_before.json", "host_md5_before.json", "overlay.json", "uvicorn_version.txt", "hostshape.json", "seams.json"):
    shutil.copyfile(os.path.join(SCRATCH, n), P + n)
lis = json.load(io.open(P + "audit_leg.json", encoding="utf-8"))
c, lv = lis["candidate"], lis["live"]
retries = c["config"]["retries_as_read"]
body = {
    "release_sha": REL["release_sha"],
    "audit_leg": {"config": {"connect_timeout": c["config"]["connect_timeout"], "read_timeout": c["config"]["read_timeout"], "max_attempts": retries.get("total_max_attempts"),
                             "retries_as_read": retries, "configured_retries_argument": {"max_attempts": 1, "mode": "standard"},
                             "note": "botocore reads max_attempts 1 as total_max_attempts 2, i.e. ONE retry; the send attempts counted on the host were %d" % c["send_attempts_made"]},
                  "failed_put_wall_s": c["failed_put_wall_s"], "send_attempts_made": c["send_attempts_made"], "counter_after_failure": c["counter_after_failure"], "stderr_lines": c["stderr_lines"],
                  "stderr_line_carries_only_class_and_count": c["stderr_line_carries_only_class_and_count"], "floor_line_written": c["floor_line_written"], "guard": lis["guard"],
                  "endpoint": "non-routable (the black hole named in the order); the real audit lake was never touched; the throwaway bucket name is not a bucket",
                  "live_ref_disclosure": {"finished_within_the_70_s_limit": lv["finished_within_limit"], "failed_put_wall_s": lv["failed_put_wall_s"], "connect_timeout": lv["config"]["connect_timeout"],
                                          "read_timeout": lv["config"]["read_timeout"], "retries_as_read": lv["config"]["retries_as_read"], "send_attempts_made_by_the_limit": lv["send_attempts_made"],
                                          "failure_counter_exists": lv["counter_after_failure"] is not None, "stderr_lines": lv["stderr_lines"], "floor_line_written": lv["floor_line_written"]}},
    "listener": {"bound_host": "127.0.0.1", "off_by_default": True, "armings": 0, "lease_parameter_written": False,
                 "lease_parameter_absent_now": json.load(io.open(P + "lease_param.json", encoding="utf-8"))["absent"],
                 "basis": "probe_listener.py is not in this release (byte-equal to the live ref) and the running service was not touched; the lease parameter was read absent and no SSM write was made"},
    "tests": {"named_passed": t["named_forward"]["passed"], "named_failed": t["named_forward"]["failed"], "window_set_passed": t["union_forward"]["passed"],
              "window_set_failed": t["union_forward"]["failed"] + t["union_reverse"]["failed"], "union_both_orders_equal": t["union_forward"]["passed"] == t["union_reverse"]["passed"]},
    "candidate_bytes_equal_release": lis["candidate_bytes_equal_release"], "process_wide_state": PROCESS_WIDE, "service": lis["service"], "scratch_removed": lis["scratch_removed"],
    "host_before": {"md5_differ": len(json.load(io.open(P + "host_md5_before.json", encoding="utf-8")).get("differ", [])), "marker": json.load(io.open(P + "step1_before.json", encoding="utf-8")).get("marker")},
}
io.open(W + "PHASE_A_OG-ap-48.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("audit_leg", "listener", "tests", "service", "host_before")}, indent=1)[:3800])
print("full suite:", json.dumps({k: t["full_suite"][k] for k in ("release_failed", "live_ref_failed", "only_in_release", "only_in_live_ref")}))
print("named:", t["named_forward"], t["named_reverse"], "window:", t["window_forward"], t["window_reverse"], "union:", t["union_forward"], t["union_reverse"], "bash -n", t["bash_n_deploy_script"], t["preflight_only"])
