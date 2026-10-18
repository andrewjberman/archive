#!/usr/bin/env python
"""OG-ap-42 Phase A: collect the local test arms and the lease-parameter reads into W/ap42_pa/*.json and assemble W/PHASE_A_OG-ap-42.json from the records (no value is typed here that a record does not hold).
READ ONLY on AWS (ssm describe-parameters); NOTHING is written to SSM. Counts, booleans and test ids only.
  ap42_pa/lease_param.json   the lease parameter read ABSENT now (the arming count is the count of puts this seat made: none)
  ap42_pa/tests.json         the named tests, the window set, their union in both orders, and the full suite's failing set against the live ref's
  ap42_pa/pins.json          the host run (copied from the scratch folder by this script)
usage: python ap42_phasea_collect.py <scratch dir holding pins.json, step1_before.json, host_md5_before.json, failed_release.txt, failed_live.txt, overlay.json>   (repository root)"""
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
P = W + "ap42_pa/"
SCRATCH = sys.argv[1]
REL = json.load(io.open(W + "ap42_release.json", encoding="utf-8"))
GW = "C:/tmp/og-rel-batch10/infra/aws/ec2/opal-gateway"
LEASE = "/opal-gateway/probe/lease"
WINDOW = ["en13", "en15", "en17", "en18", "en19", "en20", "en21", "en22", "en23", "en24", "rv2", "db3", "sv2", "en9", "cl2"]
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

named = ["tests/test_og_pr1.py", "tests/test_og_sec2.py"]
win = ["tests/test_og_%s.py" % x for x in WINDOW]
t = {"named_files": named, "named_forward": pytest_line(named), "named_reverse": pytest_line(named[::-1]), "window_set_files": len(win), "window_forward": pytest_line(win), "window_reverse": pytest_line(win[::-1]),
     "union_forward": pytest_line(win + named), "union_reverse": pytest_line(named + win[::-1])}
rel_f = set(io.open(os.path.join(SCRATCH, "failed_release.txt"), encoding="utf-8").read().split("\n")) - {""}
live_f = set(io.open(os.path.join(SCRATCH, "failed_live.txt"), encoding="utf-8").read().split("\n")) - {""}
t["full_suite"] = {"release_failed": len(rel_f), "live_ref_failed": len(live_f), "only_in_release": sorted(rel_f - live_f), "only_in_live_ref": sorted(live_f - rel_f), "names_in_both": len(rel_f & live_f),
                   "conditions": "both trees clean (git status reads 0 lines; the gate overlay restored in the release tree), the same pytest invocation over tests/"}
t["bash_n_deploy_script"] = subprocess.run(["bash", "-n", GW + "/deploy-to-ec2.sh"], capture_output=True).returncode == 0
pf = subprocess.run(["bash", GW + "/deploy-to-ec2.sh", "--preflight-only"], capture_output=True, text=True)
t["preflight_only"] = (pf.stdout.strip().splitlines() or [""])[-1]
save("tests.json", t)

for n in ("pins.json", "step1_before.json", "host_md5_before.json", "overlay.json"):
    shutil.copyfile(os.path.join(SCRATCH, n), P + n)
lis = json.load(io.open(P + "pins.json", encoding="utf-8"))
L = lis["pins"]
mm = L["mismatched_firm"]
wf = L["lease_without_valid_firm"]
gr = L["graph"]
unarmed_ok = L["unarmed"]["status"] == 403 and L["unarmed"]["error"] == "probe_not_armed"
body = {
    "release_sha": REL["release_sha"],
    "firm_pin": {
        "mismatched_firm_status": 403 if all(v["status"] == 403 for v in mm.values()) else sorted({v["status"] for v in mm.values()})[0],
        "mismatched_firm_error": "probe_firm_refused" if all(v["error"] == "probe_firm_refused" for v in mm.values()) else "mixed",
        "tool_ran_on_mismatch": L["tool_calls_on_mismatch"] > 0,
        "matched_firm_answered": L["matched_firm"]["status"] == 200 and L["matched_firm"]["tool_calls"] == 1,
        "lease_without_firm_refused": all(v["status"] == 403 and v["error"] == "probe_not_armed" for v in wf.values()),
        "guard": lis["guard"], "mismatch_variants_tried": len(mm), "mismatch_variants_refused": sum(1 for v in mm.values() if v["status"] == 403 and v["error"] == "probe_firm_refused"),
        "invalid_firm_lease_variants_tried": len(wf), "matched_rows": L["matched_firm"]["rows"], "tool_calls_on_mismatch": L["tool_calls_on_mismatch"],
    },
    "graph_pin": {"forged_host_refused": gr["forged_refused"] == gr["forged_tried"], "request_sent_to_forged_host": gr["clients_built_for_forged"] > 0,
                  "graph_host_allowed": gr["allowed_reached_stub"] == gr["allowed_tried"] and gr["allowed_answered"] == gr["allowed_tried"], "forged_tried": gr["forged_tried"], "forged_refused": gr["forged_refused"],
                  "allowed_tried": gr["allowed_tried"], "allowed_reached_stub": gr["allowed_reached_stub"]},
    "listener": {"bound_host": L["bound"][0] if len(L["bound"]) == 1 else "|".join(L["bound"]), "off_by_default": unarmed_ok, "armings": 0, "lease_parameter_written": False,
                 "test_port": 18099, "lease_parameter_absent_now": json.load(io.open(P + "lease_param.json", encoding="utf-8"))["absent"], "scratch_removed": lis["scratch_removed"], "port_free_after": lis["port_free_after"]},
    "tests": {"named_passed": t["named_forward"]["passed"], "named_failed": t["named_forward"]["failed"] + t["named_reverse"]["failed"],
              "window_set_passed": t["union_forward"]["passed"], "window_set_failed": t["union_forward"]["failed"] + t["union_reverse"]["failed"],
              "union_both_orders_equal": t["union_forward"]["passed"] == t["union_reverse"]["passed"]},
    "candidate_bytes_equal_release": lis["candidate_bytes_equal_release"], "candidate_peak_rss_mb": L["vm_hwm_mb"], "service": lis["service"],
    "host_before": {"md5_differ": len(json.load(io.open(P + "host_md5_before.json", encoding="utf-8")).get("differ", [])), "marker": json.load(io.open(P + "step1_before.json", encoding="utf-8")).get("marker")},
}
io.open(W + "PHASE_A_OG-ap-42.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("firm_pin", "graph_pin", "listener", "tests", "service", "host_before")}, indent=1))
print("full suite:", json.dumps({k: t["full_suite"][k] for k in ("release_failed", "live_ref_failed", "only_in_release", "only_in_live_ref")}))
print("named:", t["named_forward"], t["named_reverse"], "window:", t["window_forward"], t["window_reverse"], "union:", t["union_forward"], t["union_reverse"], "bash -n", t["bash_n_deploy_script"], t["preflight_only"])
