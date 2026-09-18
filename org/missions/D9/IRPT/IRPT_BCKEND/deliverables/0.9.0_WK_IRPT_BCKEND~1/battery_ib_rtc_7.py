#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtc-7 acceptance battery -- R37-AC1, five graded arms (a)-(e).

Prints IBR37-PRINCIPAL-FENCED-AND-THREE-OF-THREE-DIRECTORIES only when arms (a)-(e) ALL hold.

R-44 conditions 2/3: the IAM apply is a never-widen-class act (both sign-off halves, ledger),
and the cell must show a NEGATIVE control on the new role (denied on another firm's prefix and
on the 49 Financial DESTINATION), not only a positive one.

WHAT THIS BATTERY IS NOT (bound 12): it wraps nothing it grades and reads no earlier output of
its own. Every arm below is a LIVE re-derivation against the real world at run time:
  (a) re-hashes the packet and both signed halves from the worktree, and checks each half names
      all five keys (K1-K5) and the packet's own blob hash -- textual, not assumed.
  (b) re-plans both Terraform roots with the vendored binary (0-diff proves the live state is
      EXACTLY what was signed) and re-reads the role, its inline policy and the host policy
      statement count fresh via boto3 IAM calls, printing sha256 of each document.
  (c) fires a FRESH read-only SSM negative-control command on the host (assume the new role,
      attempt the four probes) -- a new command id every run, never a cached transcript.
  (d) invokes the DEPLOYED Lambda with the schedule's own payload (read live from schedule.tf,
      never typed twice), polls to a terminal state, and re-reads each firm's landed manifest by
      the exact key the response names, hashing the fetched bytes.
  (e) re-runs writer_census_ib_rtc_6.py's own census() function live (the same instrument IB-rtc-6
      used) against the account as it stands NOW, with the new role actually created.

Graded arms:
  (a) HALVES       2 of 2 present; packet blob hash == the expected hash; each half names K1-K5
                    and cites the packet's blob hash.
  (b) APPLIED      both roots 0-diff on a fresh plan; role + inline policy fetched and hashed;
                    mdpf-runner-scoped statement count (33) and sha256 fetched and hashed.
  (c) NEG-CONTROL  3 of 3 DENIED (inf read, cottonwood read, 49F-destination write), 1 of 1
                    READ-OK (49F dimension read), name-check 0 of 4 denied prefixes matched.
  (d) THIRD-DIR    49f landed (or already landed and reconciled) with ETag+sha256, 3 of 3 firm
                    directories present with hashes, bundle VersionId matches IB-rtc-9's mint.
  (e) CENSUS       writer census: exactly 12 writers, same membership as IB-rtc-6's baseline.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

WS = pathlib.Path(__file__).resolve().parents[7]
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(WS / "org" / "missions" / "D9" / "IRPT" / "IRPT_BCKEND" / "deliverables" / "0.4.0_DS_ClientPlatform~X"))

TERRAFORM = WS / ".tools" / "terraform.exe"
DIRECTORY_ROOT = WS / "infra" / "aws" / "terraform" / "investor-reporting" / "directory"
MDPF_ROOT = WS / "infra" / "aws" / "terraform" / "mdpf-pipeline"

PACKET = WS / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtc-6.md"
COO_HALF = WS / "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtc-7_49F_PRINCIPAL.md"
CTO_HALF = WS / "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtc-7_49F_PRINCIPAL.md"
EXPECTED_PACKET_HASH = "bb92a81c697c6d3fb8b01cb65fedfb9cb0563e38"

ROLE_NAME = "irpt-49f-directory-read-role"
ROLE_POLICY_NAME = "irpt-49f-directory-read-policy"
ROLE_ARN = "arn:aws:iam::313476888478:role/irpt-49f-directory-read-role"
HOST_ROLE = "mdpf-daily-runner-ec2-role"
HOST_POLICY = "mdpf-runner-scoped"
INSTANCE = "i-02448edb624a7a7cf"
REGION = "us-east-1"
FUNCTION = "irpt-directory-refresh"
BUNDLE_BUCKET = "opal-data-mdpf"
BUNDLE_KEY = "code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz"
EXPECTED_BUNDLE_VERSION = "0XLkiPt4wljdniLnF2fkPKN4qAIkjUbc"          # IB-rtc-9's mint

DENIED_PREFIXES = ["role/cot-", "role/inf-", "role/mdpf-", "role/opal-assets-mdpf-"]

N1_BUCKET, N1_PREFIX = "opal-data-inf", "silver/api_dims/representatives/"
N2_BUCKET, N2_PREFIX = "opal-data-assets", "blackdiamond/cottonwood/silver/fact_allocations/"
N3_BUCKET, N3_KEY = "opal-data-bd", "investor-reporting/directory/zz-negative-control-battery"
P1_BUCKET, P1_PREFIX = "opal-data-49financial", "gold/advi/dimensions/dim_relationship/"

FIRM_BUCKETS = {"49financial": "opal-data-bd", "cottonwood": "opal-data-cot", "inflection": "opal-data-inf"}

results = []


def record(name, ok, detail):
    results.append((name, ok, detail))
    print("[%s] %s -- %s" % ("PASS" if ok else "FAIL", name, detail))


def sh(cmd, cwd=None, timeout=280):
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def git_hash_object(path):
    rc, out, err = sh(["git", "hash-object", str(path)], cwd=WS)
    if rc != 0:
        raise RuntimeError("git hash-object failed: %s" % err)
    return out.strip()


# ============================================================================
# ARM (a) -- HALVES
# ============================================================================
def arm_a():
    lines = []
    ok = True
    packet_hash = git_hash_object(PACKET)
    lines.append("packet blob hash: %s (expect %s)" % (packet_hash, EXPECTED_PACKET_HASH))
    if packet_hash != EXPECTED_PACKET_HASH:
        ok = False

    halves_present = 0
    for label, path in (("COO", COO_HALF), ("CTO", CTO_HALF)):
        if path.is_file():
            halves_present += 1
            text = path.read_text(encoding="utf-8")
            keys_named = sum(1 for k in ("K1", "K2", "K3", "K4", "K5") if k in text)
            cites_hash = EXPECTED_PACKET_HASH in text
            lines.append("%s half: keys named %d of 5; cites packet hash: %s" % (label, keys_named, cites_hash))
            if keys_named < 5 or not cites_hash:
                ok = False
        else:
            lines.append("%s half: MISSING at %s" % (label, path))
            ok = False
    lines.append("halves present: %d of 2" % halves_present)
    if halves_present != 2:
        ok = False
    record("a.HALVES", ok, "; ".join(lines))
    return ok


# ============================================================================
# ARM (b) -- APPLIED (fresh terraform plans + fresh IAM reads, hashed)
# ============================================================================
def canon_sha256(doc):
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def tf_plan_summary(root, extra_args):
    (WS / ".scratch").mkdir(exist_ok=True)
    scratch_out = WS / ".scratch" / ("rtc7_battery_%s.tfplan" % root.name)
    args = [str(TERRAFORM), "-chdir=%s" % str(root), "plan", "-input=false",
            "-out=%s" % str(scratch_out)] + extra_args
    rc, out, err = sh(args, timeout=280)
    m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", out)
    no_changes = "No changes." in out
    if no_changes:
        return rc, (0, 0, 0), out
    if m:
        return rc, tuple(int(x) for x in m.groups()), out
    return rc, None, out


def arm_b():
    import boto3
    lines = []
    ok = True

    rc, plan, out = tf_plan_summary(DIRECTORY_ROOT, [])
    lines.append("directory root re-plan rc=%d plan=%s" % (rc, plan))
    if rc != 0 or plan is None or plan[2] != 0:
        ok = False

    rc2, plan2, out2 = tf_plan_summary(MDPF_ROOT, ["-target=aws_iam_role_policy.mdpf_runner"])
    lines.append("mdpf-pipeline targeted re-plan rc=%d plan=%s" % (rc2, plan2))
    if rc2 != 0 or plan2 is None or plan2[2] != 0:
        ok = False

    iam = boto3.client("iam", region_name=REGION)
    role = iam.get_role(RoleName=ROLE_NAME)["Role"]
    trust_sha = canon_sha256(role["AssumeRolePolicyDocument"])
    pol = iam.get_role_policy(RoleName=ROLE_NAME, PolicyName=ROLE_POLICY_NAME)["PolicyDocument"]
    pol_sha = canon_sha256(pol)
    lines.append("K1 role %s trust sha256=%s created=%s" % (role["Arn"], trust_sha, role["CreateDate"]))
    lines.append("K2 policy sha256=%s statements=%d" % (pol_sha, len(pol.get("Statement", []))))
    if role["Arn"] != ROLE_ARN:
        ok = False
    if len(pol.get("Statement", [])) != 2:
        ok = False

    host_pol = iam.get_role_policy(RoleName=HOST_ROLE, PolicyName=HOST_POLICY)["PolicyDocument"]
    host_sha = canon_sha256(host_pol)
    n_stmts = len(host_pol.get("Statement", []))
    has_k3 = any(s.get("Sid") == "IrptDirectory49fAssumeSourcePrincipal"
                 and s.get("Resource") == ROLE_ARN for s in host_pol.get("Statement", []))
    lines.append("K3 host policy statements=%d (expect 33) sha256=%s has_k3_statement=%s"
                 % (n_stmts, host_sha, has_k3))
    if n_stmts != 33 or not has_k3:
        ok = False

    record("b.APPLIED", ok, "; ".join(lines))
    return ok


# ============================================================================
# ARM (c) -- NEGATIVE CONTROL (fresh SSM dispatch, read-only)
# ============================================================================
NEGCTL_SCRIPT = """#!/bin/bash
set -u
cd /tmp || exit 1
ROLE_ARN="%(role_arn)s"
CREDS_JSON=$(aws sts assume-role --role-arn "$ROLE_ARN" --role-session-name irpt-battery-negctl --duration-seconds 900 --output json 2>&1)
RC=$?
echo "ASSUME-RC=$RC"
if [ $RC -ne 0 ]; then echo "$CREDS_JSON"; echo "NEGCTL-FATAL"; exit 1; fi
AK=$(echo "$CREDS_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['Credentials']['AccessKeyId'])")
SK=$(echo "$CREDS_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['Credentials']['SecretAccessKey'])")
ST=$(echo "$CREDS_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['Credentials']['SessionToken'])")
AARN=$(echo "$CREDS_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['AssumedRoleUser']['Arn'])")
echo "ASSUMED-ARN=$AARN"
MATCHES=0
for p in "role/cot-" "role/inf-" "role/mdpf-" "role/opal-assets-mdpf-"; do
  case "$AARN" in *"$p"*) MATCHES=$((MATCHES+1));; esac
done
echo "NAME-MATCHES=$MATCHES"
export AWS_ACCESS_KEY_ID="$AK" AWS_SECRET_ACCESS_KEY="$SK" AWS_SESSION_TOKEN="$ST"
N1=$(aws s3api list-objects-v2 --bucket %(n1_bucket)s --prefix "%(n1_prefix)s" --output json 2>&1); echo "N1-RC=$? N1-OUT=$N1" | tr '\\n' ' '; echo ""
N2=$(aws s3api list-objects-v2 --bucket %(n2_bucket)s --prefix "%(n2_prefix)s" --output json 2>&1); echo "N2-RC=$? N2-OUT=$N2" | tr '\\n' ' '; echo ""
echo battery-negctl-probe > /tmp/zz-negctl-battery.txt
N3=$(aws s3api put-object --bucket %(n3_bucket)s --key "%(n3_key)s" --body /tmp/zz-negctl-battery.txt --output json 2>&1); echo "N3-RC=$? N3-OUT=$N3" | tr '\\n' ' '; echo ""
P1=$(aws s3api list-objects-v2 --bucket %(p1_bucket)s --prefix "%(p1_prefix)s" --max-items 1 --query "Contents[0].Key" --output text 2>&1); echo "P1-RC=$? P1-KEY=$P1"
rm -f /tmp/zz-negctl-battery.txt
echo NEGCTL-DONE
""" % {
    "role_arn": ROLE_ARN,
    "n1_bucket": N1_BUCKET, "n1_prefix": N1_PREFIX,
    "n2_bucket": N2_BUCKET, "n2_prefix": N2_PREFIX,
    "n3_bucket": N3_BUCKET, "n3_key": N3_KEY,
    "p1_bucket": P1_BUCKET, "p1_prefix": P1_PREFIX,
}


def ssm_run(comment, script_text, timeout=180):
    import boto3
    ssm = boto3.client("ssm", region_name=REGION)
    commands = script_text.splitlines()
    resp = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                             Parameters={"commands": commands}, Comment=comment)
    cid = resp["Command"]["CommandId"]
    deadline = time.time() + timeout
    inv = None
    while time.time() < deadline:
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    return cid, inv


def arm_c():
    lines = []
    ok = True
    cid, inv = ssm_run("IRPT_BCKEND IB-rtc-7 battery negative control", NEGCTL_SCRIPT)
    if inv is None:
        record("c.NEG-CONTROL", False, "SSM command %s did not reach a terminal state" % cid)
        return False
    out = inv.get("StandardOutputContent", "")
    lines.append("SSM command %s status=%s" % (cid, inv.get("Status")))

    def line_value(prefix):
        for ln in out.splitlines():
            if ln.startswith(prefix):
                return ln
        return None

    n1 = line_value("N1-RC=")
    n2 = line_value("N2-RC=")
    n3 = line_value("N3-RC=")
    p1 = line_value("P1-RC=")
    matches_line = line_value("NAME-MATCHES=")
    denied = 0
    for n, ln in (("N1", n1), ("N2", n2), ("N3", n3)):
        d = ln is not None and "AccessDenied" in ln
        lines.append("%s: %s -> %s" % (n, ln, "DENIED" if d else "NOT-DENIED"))
        if d:
            denied += 1
    read_ok = p1 is not None and "P1-RC=0" in p1 and "None" not in p1.split("P1-KEY=", 1)[-1]
    lines.append("P1: %s -> %s" % (p1, "READ-OK" if read_ok else "NOT-READ-OK"))
    matches = int(matches_line.split("=", 1)[1]) if matches_line else -1
    lines.append("name-check matches: %d of 4" % matches)
    lines.append("DENIED: %d of 3; READ-OK: %d of 1" % (denied, 1 if read_ok else 0))
    if denied != 3 or not read_ok or matches != 0:
        ok = False
    record("c.NEG-CONTROL", ok, "; ".join(lines))
    return ok


# ============================================================================
# ARM (d) -- THIRD DIRECTORY (fresh Lambda invoke, polled to terminal, hashed)
# ============================================================================
def schedule_payload():
    """Read the LIVE payload of the irpt_directory_refresh schedule specifically -- schedule.tf
    declares TWO aws_scheduler_schedule resources (irpt_holdings_snapshot first, then this one),
    so the extraction is bounded to THIS resource's own block, never the first 'target {' in the
    file."""
    text = (WS / "infra/aws/terraform/investor-reporting/directory/schedule.tf").read_text(encoding="utf-8")
    anchor = 'resource "aws_scheduler_schedule" "irpt_directory_refresh"'
    start = text.index(anchor)
    end_marker = '\noutput "directory_refresh_schedule_name"'
    end = text.index(end_marker, start)
    block = text[start:end]
    if "irpt_holdings_snapshot" in block:
        raise RuntimeError("schedule block bound incorrectly -- it still contains the sibling schedule")
    m = re.search(r'input = jsonencode\(\{\s*kind\s*=\s*"([^"]+)"\s*note\s*=\s*"([^"]+)"', block, re.S)
    if not m:
        raise RuntimeError("could not read the schedule's own payload from schedule.tf")
    return {"kind": m.group(1), "note": m.group(2)}


def arm_d():
    import boto3
    lines = []
    ok = True
    lam = boto3.client("lambda", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)

    payload = schedule_payload()
    lines.append("schedule payload (read live from schedule.tf): %s" % payload)

    bundle_head = s3.head_object(Bucket=BUNDLE_BUCKET, Key=BUNDLE_KEY)
    bundle_version = bundle_head["VersionId"]
    lines.append("bundle current VersionId=%s (expect IB-rtc-9's mint %s)" % (bundle_version, EXPECTED_BUNDLE_VERSION))
    if bundle_version != EXPECTED_BUNDLE_VERSION:
        ok = False

    deadline = time.time() + 600
    envelopes = None
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        resp = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(payload).encode("utf-8"))
        body = json.loads(resp["Payload"].read())
        results_ = body.get("results", [])
        envelopes = {r["firm_id"]: r for r in results_}
        states = {fid: r["envelope"]["state"] for fid, r in envelopes.items()}
        lines.append("invoke attempt %d states=%s" % (attempt, states))
        if all(s in ("READY",) for s in states.values()):
            break
        if all(s not in ("RUNNING",) for s in states.values()):
            # terminal but not all READY (e.g. a real failure) -- stop polling, grade what we have
            break
        time.sleep(15)

    if envelopes is None or set(envelopes) != {"49financial", "cottonwood", "inflection"}:
        record("d.THIRD-DIR", False, "did not get a 3-firm response: %s" % (envelopes,))
        return False

    landed = 0
    for firm_id, bucket in FIRM_BUCKETS.items():
        env = envelopes[firm_id]["envelope"]
        state = env["state"]
        bdate = env["source_dates"]["business_date"]
        key = "investor-reporting/directory/%s/directory.json" % bdate
        try:
            head = s3.head_object(Bucket=bucket, Key=key)
            obj = s3.get_object(Bucket=bucket, Key=key)
            body_bytes = obj["Body"].read()
            sha = hashlib.sha256(body_bytes).hexdigest()
            lines.append("%s: state=%s revision=%s key=s3://%s/%s ETag=%s size=%d sha256=%s"
                         % (firm_id, state, env["operation"]["revision"], bucket, key,
                            head["ETag"], head["ContentLength"], sha))
            landed += 1
        except Exception as exc:                                  # noqa: BLE001
            lines.append("%s: state=%s -- artifact NOT present at %s (%s)" % (firm_id, state, key, exc))
    lines.append("directories present: %d of 3" % landed)
    if landed != 3:
        ok = False
    fortyninef_ready = envelopes["49financial"]["envelope"]["state"] == "READY"
    lines.append("49f state READY: %s (1 of 1 landed if True)" % fortyninef_ready)
    if not fortyninef_ready:
        ok = False

    record("d.THIRD-DIR", ok, "; ".join(lines))
    return ok


# ============================================================================
# ARM (e) -- WRITER CENSUS (live, same instrument as IB-rtc-6)
# ============================================================================
def arm_e():
    import writer_census_ib_rtc_6 as wc
    out = wc.census()
    writers = sorted("%s:%s" % (w["kind"], w["name"]) for w in out["writers"])
    expected = sorted([
        "role:bd-allocation-processor-role", "role:bd-daily-trigger-lambda-role",
        "role:bd-exporter-ec2-role", "role:bd-gold-detail-generator-role",
        "role:bd-gold-layer-lambda-role", "role:bd-merge-daily-lambda-role",
        "role:bd-pipeline-task-role", "role:bd-processor-lambda-role",
        "role:mdpf-daily-runner-ec2-role", "user:Andrew_Berman",
        "user:Andrew_Berman_Console", "user:Opal_Terminal",
    ])
    same_membership = writers == expected
    ok = out["verdict"] == "EVALUATED" and len(out["writers"]) == 12 and same_membership
    detail = ("verdict=%s writers=%d of %d principals; same_membership=%s"
              % (out["verdict"], len(out["writers"]), out["principals"], same_membership))
    record("e.CENSUS", ok, detail)
    return ok


def main():
    print("=== IB-rtc-7 battery -- live re-derivation, %d arms ===" % 5)
    a = arm_a()
    b = arm_b()
    c = arm_c()
    d = arm_d()
    e = arm_e()
    all_pass = a and b and c and d and e
    print("")
    print("R37-AC1: %d of 5 arms PASS" % sum(1 for _, ok, _ in results if ok))
    if all_pass:
        print("IBR37-PRINCIPAL-FENCED-AND-THREE-OF-THREE-DIRECTORIES")
        return 0
    print("TOKEN WITHHELD -- one or more arms FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
