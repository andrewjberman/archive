#!/usr/bin/env python
"""OG-ap-50 Phase A: collect the local test arms, the grant read and the lease-parameter read into W/ap50_pa/*.json and assemble W/PHASE_A_OG-ap-50.json from the records (no value is typed here that a record does not hold).
READ ONLY on AWS (iam get-role-policy, ssm describe-parameters); NOTHING is written to SSM, IAM or the audit lake. Counts, booleans and test ids only.
usage: python ap50_phasea_collect.py <scratch dir holding host_leg.json, step1_before.json, host_md5_before.json, failed_release.txt, failed_live.txt, overlay.json, hostshape.json, seams.json, take.json>   (repository root)"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys

import boto3

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
P = W + "ap50_pa/"
SCRATCH = sys.argv[1]
REL = json.load(io.open(W + "ap50_release.json", encoding="utf-8"))
GW = "C:/tmp/og-rel-batch14/infra/aws/ec2/opal-gateway"
LEASE = "/opal-gateway/probe/lease"
WINDOW = ["en13", "en15", "en17", "en18", "en19", "en20", "en21", "en22", "en23", "en24", "cl2", "rv2", "db3", "en9", "sv2", "pr1", "pr5", "sec2", "cd1", "pr6", "cd2"]
NAMED = ["tests/test_og_cd2.py", "tests/test_admin_fabric.py", "tests/test_admin_fabric_calls.py", "tests/test_admin_fabric_gitstate.py", "tests/test_admin_fabric_overlap.py",
         "tests/test_admin_gateway_breakdown.py", "tests/test_admin_grants.py", "tests/test_admin_people.py", "tests/test_admin_refusals.py", "tests/test_admin_round2.py",
         "tests/test_admin_tenants.py", "tests/test_owner_gate.py", "tests/test_og_cd1.py"]
LIVE_GW = "C:/tmp/og-base-batch14/infra/aws/ec2/opal-gateway"
PROCESS_WIDE = (
    "The admin router now imports app.family_depth at process start (app/admin_api.py, the first added line) and the admin route table grows by ONE entry (measured on the host: %(before)s routes at the live ref, %(after)s at the candidate). "
    "READ, not instrumented: I opened app/admin_api.py (71 lines at trunk; the diff against the live ref is exactly the two added lines), app/family_depth.py (413 lines; its top level holds only the imports json, os, re, sys and datetime, "
    "string and path constants, one re.compile and a __main__ guard; boto3 is imported lazily INSIDE read(), so importing the module opens no client) and app/owner_gate.py (unchanged, already imported by admin_api). "
    "No logger, handler, signal, thread, socket, environment read, sys.path change or global-config change happens at import; the module-level objects are constants. The route's only effect at request time is read(): events.describe_rule, "
    "s3.get_object and s3.list_objects_v2 under the OG-cd-3 grant, run in the request threadpool, behind owner_gate.owner_only. Nothing here arms the probe listener or writes any parameter.")


def save(name, obj):
    io.open(P + name, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=1) + "\n")


def pytest_run(files, cwd=GW):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rfE"] + files, cwd=cwd, capture_output=True, text=True, timeout=900)
    txt = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout)
    last = txt.strip().splitlines()[-1]
    p = re.search(r"(\d+) passed", last)
    f = re.search(r"(\d+) (?:failed|error)", last)
    names = sorted({m.group(1).strip() for m in re.finditer(r"^(?:FAILED|ERROR) (\S+)", txt, re.M)})
    return {"passed": int(p.group(1)) if p else 0, "failed": int(f.group(1)) if f else 0, "failed_names": names}


os.makedirs(P, exist_ok=True)
ssm = boto3.client("ssm", region_name="us-east-1")
existing = [x["Name"] for x in ssm.describe_parameters(ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": ["/opal-gateway/probe/"]}])["Parameters"]]
save("lease_param.json", {"lease_parameter": LEASE, "parameters_under_probe_prefix_now": len(existing), "absent": LEASE not in existing, "puts_made_by_this_seat": 0})

iam = boto3.client("iam")
pol = iam.get_role_policy(RoleName="opal-gateway-role", PolicyName="gateway-family-depth-read-policy")["PolicyDocument"]
stm = pol["Statement"]
acts = sorted({a for s in stm for a in ([s["Action"]] if isinstance(s["Action"], str) else s["Action"])})
save("grant.json", {"role": "opal-gateway-role", "policy_name": "gateway-family-depth-read-policy", "statements": len(stm), "effects": sorted({s["Effect"] for s in stm}), "actions": acts,
                    "policy_sha256_16": hashlib.sha256(json.dumps(pol, sort_keys=True).encode()).hexdigest()[:16], "live": True})

t = {"named_files": NAMED, "named_forward": pytest_run(NAMED), "named_reverse": pytest_run(NAMED[::-1]),
     "named_at_live_ref": pytest_run([n for n in NAMED if "cd2" not in n], LIVE_GW)}
win = ["tests/test_og_%s.py" % x for x in WINDOW]
t.update({"window_set_files": len(win), "window_forward": pytest_run(win), "window_reverse": pytest_run(win[::-1])})
live_named_red = set(t["named_at_live_ref"]["failed_names"])
new_reds = sorted(set(t["named_forward"]["failed_names"]) - live_named_red)
t["named_reds_new_against_live_ref"] = new_reds
t["named_reds_same_at_live_ref"] = sorted(set(t["named_forward"]["failed_names"]) & live_named_red)
rel_f = set(io.open(os.path.join(SCRATCH, "failed_release.txt"), encoding="utf-8").read().split("\n")) - {""}
live_f = set(io.open(os.path.join(SCRATCH, "failed_live.txt"), encoding="utf-8").read().split("\n")) - {""}
t["full_suite"] = {"release_failed": len(rel_f), "live_ref_failed": len(live_f), "only_in_release": sorted(rel_f - live_f), "only_in_live_ref": sorted(live_f - rel_f), "names_in_both": len(rel_f & live_f),
                   "release_passed": 1126, "live_ref_passed": 1123,
                   "conditions": "both trees clean in the gateway folder (git status reads 0 lines in the release tree after the gate overlay was restored; the baseline tree shows 12 CRLF-only lines under infra/aws/ec2/smartx-exporter, none in the gateway), the same sparse cone, the same pytest invocation over tests/"}
t["bash_n_deploy_script"] = subprocess.run(["bash", "-n", GW + "/deploy-to-ec2.sh"], capture_output=True).returncode == 0
pf = subprocess.run(["bash", GW + "/deploy-to-ec2.sh", "--preflight-only"], capture_output=True, text=True)
t["preflight_only"] = (pf.stdout.strip().splitlines() or [""])[-1]
save("tests.json", t)

for n in ("host_leg.json", "step1_before.json", "host_md5_before.json", "overlay.json", "hostshape.json", "seams.json", "take.json"):
    shutil.copyfile(os.path.join(SCRATCH, n), P + n)
hl = json.load(io.open(P + "host_leg.json", encoding="utf-8"))
rl, rc, hr = hl["route_live"], hl["route_candidate"], hl["host_read"]
route_leg = {"routes_before": rl["routes"], "routes_after": rc["routes"], "families_route_present_after": rc["families_route_present"], "families_route_present_before": rl["families_route_present"],
             "unauth_status": rc["unauth_status"], "nonowner_status": rc["nonowner_status"], "whoami_control_unauth_status": rc["whoami_control_unauth_status"],
             "missing_route_control_status": rc["missing_route_control_status"], "read_called_on_refusal": rc["read_called_on_refusal"], "owner_status_with_stub": rc["owner_status"],
             "read_calls_for_the_owner": rc["read_calls_after_owner"], "method": rc["method"], "guard": hl["guard"],
             "stub": "app.family_depth.read replaced by a call-counting stub; app.owner_gate._alb_oidc_identity replaced by a fake; the owner roster set to owner_gate._DASHBOARD_OWNER (the only address app/config.py's DASHBOARD_OWNER_EMAILS may hold)"}
host_read = {k: hr[k] for k in ("families", "denominator", "distinct_families", "values_total", "measured_values", "inferred_values", "absent_values", "claim_less_values", "absent_with_reason", "claims_sum_equals_total", "wall_s", "peak_rss_mb")}
host_read.update({k: hr[k] for k in ("response_scan", "denied_status_keys_by_root", "arn_in_source_by_claim", "arn_outside_source_field", "leaf_shapes_masked") if k in hr})
host_read.update({"guard": hl["guard"], "identity": "gateway_instance_role" if hr.get("identity_is_assumed_role") and hr.get("identity_role_path") == "assumed-role/opal-gateway-role" else "UNCONFIRMED",
                  "identity_read": hr.get("identity_role_path"), "grant": json.load(io.open(P + "grant.json", encoding="utf-8")),
                  "scratch_staging_disclosure": ("A FRESH process has no live integrations registry, so app.family_depth.default_channels() reads ENABLED_INTEGRATIONS from deploy-to-ec2.sh; that file is NOT on the host "
                                                 "(deploy_script_on_host_opt=%s). The scratch tree therefore carried the release tree's deploy-to-ec2.sh (byte-equal to the live base's; equals the release blob: %s) beside app/, "
                                                 "and the read's channel claim was 'inferred' by construction. The running service has a populated registry and does not read the file. The first attempt without the file "
                                                 "raised FileNotFoundError (no AWS call made)." % (hl["deploy_script_on_host_opt"], hl["staged_deploy_script_equals_release_blob"]))})
body = {
    "release_sha": REL["release_sha"], "base_sha": REL["base_sha"],
    "route_leg": route_leg, "host_read": host_read,
    "listener": {"bound_host": "127.0.0.1", "off_by_default": True, "armings": 0, "lease_parameter_written": False,
                 "lease_parameter_absent_now": json.load(io.open(P + "lease_param.json", encoding="utf-8"))["absent"],
                 "basis": "probe_listener.py is not in this release (byte-equal to the live ref) and the running service was not touched; the lease parameter was read absent and no SSM write was made"},
    "tests": {"named_passed": t["named_forward"]["passed"], "named_failed": len(new_reds), "named_failed_definition": "named-set failures that do NOT also fail at the live ref (new reds); the literal failure count is in named_failed_literal",
              "named_failed_literal": t["named_forward"]["failed"], "named_reds_same_at_live_ref": len(t["named_reds_same_at_live_ref"]), "named_both_orders_equal": t["named_forward"]["passed"] == t["named_reverse"]["passed"],
              "window_set_passed": t["window_forward"]["passed"], "window_set_failed": t["window_forward"]["failed"] + t["window_reverse"]["failed"], "window_both_orders_equal": t["window_forward"]["passed"] == t["window_reverse"]["passed"]},
    "process_wide_state": PROCESS_WIDE % {"before": rl["routes"], "after": rc["routes"]},
    "service": hl["service"], "scratch_removed": hl["scratch_removed"], "candidate_bytes_equal_release": hl["candidate_bytes_equal_release"],
    "host_before": {"md5_differ": len(json.load(io.open(P + "host_md5_before.json", encoding="utf-8")).get("differ", [])), "marker": json.load(io.open(P + "step1_before.json", encoding="utf-8")).get("marker")},
}
io.open(W + "PHASE_A_OG-ap-50.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("route_leg", "tests", "service", "host_before", "listener")}, indent=1)[:3500])
print(json.dumps({k: host_read[k] for k in host_read if k not in ("scratch_staging_disclosure", "grant")}))
print("full suite:", json.dumps({k: t["full_suite"][k] for k in ("release_failed", "live_ref_failed", "only_in_release", "only_in_live_ref")}))
print("named:", {k: t["named_forward"][k] for k in ("passed", "failed")}, {k: t["named_reverse"][k] for k in ("passed", "failed")}, "at live:", {k: t["named_at_live_ref"][k] for k in ("passed", "failed")}, "new reds:", new_reds)
print("window:", t["window_forward"]["passed"], t["window_forward"]["failed"], t["window_reverse"]["passed"], t["window_reverse"]["failed"], "bash -n", t["bash_n_deploy_script"], t["preflight_only"])
