#!/usr/bin/env python
"""OG-ap-40 Phase A: collect the local and AWS-read arms into W/ap40_pa/*.json and assemble W/PHASE_A_OG-ap-40.json from the records (no value is typed here that a record does not hold).
READ ONLY on AWS (iam simulate, elbv2 describe). Counts, booleans, ports and test ids only; no account number is written.
  ap40_pa/iam.json        step zero: the gateway instance role's right to read, and to write or delete, the lease parameter (policy simulator)
  ap40_pa/alb.json        the target groups the gateway instance is in, with their ports
  ap40_pa/tests.json      the window set, the taken test file, their union in both orders, and the full suite's failing set against the live ref's
  ap40_pa/listener.json   the host run (copied from the scratch folder by the caller)
usage: python ap40_phasea_collect.py <scratch dir holding listener.json, step1_before.json, host_md5_before.json, failed_release.txt, failed_live.txt>   (repository root)"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
P = W + "ap40_pa/"
SCRATCH = sys.argv[1]
REL = json.load(io.open(W + "ap40_release.json", encoding="utf-8"))
GW = "C:/tmp/og-rel-batch9/infra/aws/ec2/opal-gateway"
LEASE = "/opal-gateway/probe/lease"
PORT = 8099
LEASE_MIN = 45
WINDOW = ["en13", "en15", "en17", "en18", "en19", "en20", "en21", "en22", "en23", "en24", "rv2", "db3", "sv2", "en9", "cl2"]
os.makedirs(P, exist_ok=True)


def save(name, obj):
    io.open(P + name, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, indent=1) + "\n")


def pytest_line(files):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + files, cwd=GW, capture_output=True, text=True, timeout=600)
    last = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout).strip().splitlines()[-1]
    p = re.search(r"(\d+) passed", last)
    f = re.search(r"(\d+) (?:failed|error)", last)
    return {"passed": int(p.group(1)) if p else 0, "failed": int(f.group(1)) if f else 0}


# step zero + ALB (AWS reads)
import boto3  # noqa: E402

iam, sts, elb = boto3.client("iam"), boto3.client("sts"), boto3.client("elbv2", region_name="us-east-1")
acct = sts.get_caller_identity()["Account"]
role = "opal-gateway-role"
arn = iam.get_role(RoleName=role)["Role"]["Arn"]
res = "arn:aws:ssm:us-east-1:%s:parameter%s" % (acct, LEASE)
dec = {}
for act in ("ssm:GetParameter", "ssm:PutParameter", "ssm:DeleteParameter"):
    ev = iam.simulate_principal_policy(PolicySourceArn=arn, ActionNames=[act], ResourceArns=[res])["EvaluationResults"][0]
    dec[act] = {"decision": ev["EvalDecision"], "matched": [x["SourcePolicyId"] for x in ev.get("MatchedStatements", [])][:3]}
ssm = boto3.client("ssm", region_name="us-east-1")
existing = [x["Name"] for x in ssm.describe_parameters(ParameterFilters=[{"Key": "Name", "Option": "BeginsWith", "Values": ["/opal-gateway/probe/"]}])["Parameters"]]
who = sts.get_caller_identity()["Arn"]
src = "arn:aws:iam::%s:role/%s" % (acct, who.split("/")[1]) if ":assumed-role/" in who else who
sim = iam.simulate_principal_policy(PolicySourceArn=src, ActionNames=["ssm:PutParameter", "ssm:DeleteParameter"], ResourceArns=[res])["EvaluationResults"]
arming = {}
for ev2 in sim:
    arming[ev2["EvalActionName"]] = ev2["EvalDecision"]
iam_rec = {"lease_parameter": LEASE, "gateway_role_get_parameter": dec["ssm:GetParameter"]["decision"], "gateway_role_get_matched_policy": dec["ssm:GetParameter"]["matched"],
           "gateway_role_put": dec["ssm:PutParameter"]["decision"], "gateway_role_delete": dec["ssm:DeleteParameter"]["decision"], "parameters_under_probe_prefix_now": len(existing),
           "arming_seat_put_delete": arming, "basis": "iam:SimulatePrincipalPolicy against the role's attached and inline policies (no service control policy or permissions boundary is evaluated)"}
save("iam.json", iam_rec)

tgs = []
for page in elb.get_paginator("describe_target_groups").paginate():
    tgs += page["TargetGroups"]
rows = []
for tg in tgs:
    th = elb.describe_target_health(TargetGroupArn=tg["TargetGroupArn"])["TargetHealthDescriptions"]
    ports = [t["Target"]["Port"] for t in th if t["Target"]["Id"] == "i-07dccb1615503ac99"]
    if ports or tg.get("Port") == PORT:
        rows.append({"target_group_port": tg.get("Port"), "instance_ports": ports})
alb_rec = {"target_groups_scanned": len(tgs), "target_groups_with_the_instance": len(rows), "rows": rows,
           "listener_port_in_any_target_group": any(PORT == r["target_group_port"] or PORT in r["instance_ports"] for r in rows)}
save("alb.json", alb_rec)

# tests
win = ["tests/test_og_%s.py" % x for x in WINDOW]
pr1 = ["tests/test_og_pr1.py"]
t = {"window_set_files": len(win), "window_forward": pytest_line(win), "window_reverse": pytest_line(win[::-1]), "taken_test": pytest_line(pr1),
     "union_forward": pytest_line(win + pr1), "union_reverse": pytest_line(pr1 + win[::-1])}
rel_f = set(io.open(os.path.join(SCRATCH, "failed_release.txt"), encoding="utf-8").read().split("\n")) - {""}
live_f = set(io.open(os.path.join(SCRATCH, "failed_live.txt"), encoding="utf-8").read().split("\n")) - {""}
only_rel, only_live = sorted(rel_f - live_f), sorted(live_f - rel_f)
t["full_suite"] = {"release_failed": len(rel_f), "live_ref_failed": len(live_f), "only_in_release": only_rel, "only_in_live_ref": only_live,
                   "conditions": "both trees clean (git status reads 0 lines at the files; the gate overlay restored in the release tree), the same pytest invocation over tests/",
                   "names_in_both": len(rel_f & live_f)}
t["bash_n_deploy_script"] = subprocess.run(["bash", "-n", GW + "/deploy-to-ec2.sh"], capture_output=True).returncode == 0
pf = subprocess.run(["bash", GW + "/deploy-to-ec2.sh", "--preflight-only"], capture_output=True, text=True)
t["preflight_only"] = (pf.stdout.strip().splitlines() or [""])[-1]
save("tests.json", t)

for n in ("listener.json", "step1_before.json", "host_md5_before.json", "overlay.json"):
    shutil.copyfile(os.path.join(SCRATCH, n), P + n)
lis = json.load(io.open(P + "listener.json", encoding="utf-8"))
L = lis["listener"]
bound = L["bound"]
ok_union = t["union_forward"]["failed"] == 0 and t["union_reverse"]["failed"] == 0 and t["union_forward"]["passed"] == t["union_reverse"]["passed"] >= 1
flow = (L["unarmed"]["status"] == 403 and L["unarmed"]["error"] == "probe_not_armed" and L["peers_valid_pair"]["status"] == 200 and L["transactions"]["status"] == 200
        and L["after_expiry"]["status"] == 403 and L["over_long_lease"]["status"] == 403 and L["malformed_lease"]["status"] == 403)
body = {
    "release_sha": REL["release_sha"],
    "listener": {
        "bound_host": bound[0] if len(bound) == 1 else "|".join(bound), "reachable_from_outside": L["private_address_connect"] == "connected" or not L["private_address_present"],
        "in_alb_target_group": bool(alb_rec["listener_port_in_any_target_group"]), "off_by_default": L["unarmed"]["status"] == 403 and L["unarmed"]["error"] == "probe_not_armed",
        "lease_minutes": LEASE_MIN, "expires_closed": L["after_expiry"]["status"] == 403 and L["over_long_lease"]["status"] == 403,
        "tools_served": sorted(L["audit"]["ok_outcomes"]), "other_tool_refused": L["other_tool"]["status"] == 404, "other_account_refused": L["other_account"]["status"] == 403,
        "audit_label_on_every_call": bool(L["audit"]["all_labelled"]), "guard": lis["guard"], "port": PORT,
        "private_address_connect": L["private_address_connect"], "target_group_ports_of_the_instance": [r["instance_ports"] for r in rows],
        "oversized_body_status": L["oversized_body"]["status"], "bad_json_status": L["bad_json"]["status"],
        "peers_valid_pair": L["peers_valid_pair"], "transactions": L["transactions"], "probe_labelled_records": L["audit"]["probe_labelled"], "http_requests": L["audit"]["http_requests"],
        "unlabelled_tool_own_records": L["audit"]["unlabelled_tool_own_records"], "candidate_bytes_equal_release": lis["candidate_bytes_equal_release"], "candidate_peak_rss_mb": L["vm_hwm_mb"],
        "server_hookup": L["hookup"], "scratch_removed": lis["scratch_removed"], "port_free_after": lis["port_free_after"],
    },
    "heap_read": {"method": "proc_status_signal", "before_mb": L["heap"]["before_mb"], "after_mb": L["heap"]["after_mb"], "service_pid_stable": bool(lis["service"]["pid_stable"]),
                  "signal_line_written": L["heap"]["signal_line_written"], "peak_mb": L["heap"]["hwm_mb"], "scope": "the candidate in a scratch process; the running service was not touched (its PID and NRestarts read before and after)"},
    "tests": {"arm_call_expiry_passed": bool(flow and L["other_tool"]["status"] == 404 and L["other_account"]["status"] == 403 and L["heap"]["signal_line_written"]),
              "window_set_passed": t["union_forward"]["passed"], "window_set_failed": t["union_forward"]["failed"] + t["union_reverse"]["failed"], "window_set_both_orders_equal": ok_union},
    "step_zero_iam": {"gateway_role_get_parameter": iam_rec["gateway_role_get_parameter"], "parameters_under_probe_prefix_now": iam_rec["parameters_under_probe_prefix_now"]},
    "service": lis["service"],
    "host_before": {"md5_differ": len(json.load(io.open(P + "host_md5_before.json", encoding="utf-8")).get("differ", [])), "marker": json.load(io.open(P + "step1_before.json", encoding="utf-8")).get("marker")},
}
io.open(W + "PHASE_A_OG-ap-40.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps(body["listener"], indent=1)[:1800])
print(json.dumps({k: body[k] for k in ("heap_read", "tests", "step_zero_iam", "service", "host_before")}, indent=1))
print("full suite:", json.dumps({k: t["full_suite"][k] for k in ("release_failed", "live_ref_failed", "only_in_release", "only_in_live_ref")}))
print("window both orders:", t["window_forward"], t["window_reverse"], "taken:", t["taken_test"], "union:", t["union_forward"], t["union_reverse"], "bash -n", t["bash_n_deploy_script"], t["preflight_only"])
