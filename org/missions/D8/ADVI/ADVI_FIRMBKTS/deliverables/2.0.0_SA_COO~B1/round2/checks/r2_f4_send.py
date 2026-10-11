"""ADVI_FIRMBKTS round 2: the ONE SSM command of cell FB-e-4 (F4's negative arm), issuer 2.0.0_SA_COO~B1.

What it does, in full: on ONE named SSM-managed runner it assumes `irpt-cot-ycharts-research-role` (a `*-cot-*` role
that the runner's own instance role is trusted to assume), prints that session's STS caller ARN, makes ONE read-only
ListObjectsV2 (MaxKeys 1) on opal-data-inflection and ONE on opal-data-cottonwood, and prints each result or error
text. It prints no credential, writes nothing to AWS and deletes nothing. The instance, the role and the buckets are
constants here: the file takes no argument that changes them. Evidence goes to --out (JSON) for r2_f4.py --arms negative.

  python r2_f4_send.py --print            print the command and parameters, send nothing
  python r2_f4_send.py --out FILE         send, wait up to --wait seconds, write the evidence record
  python r2_f4_send.py --collect ID --out FILE
                                          fetch a command already sent (no second send)
Never edit this file. Plain ASCII.
"""
import argparse
import json
import sys
import time

INSTANCE = "i-0167fd745ad906a66"   # irpt-ycharts-runner
ROLE = "arn:aws:iam::313476888478:role/irpt-cot-ycharts-research-role"
REGION = "us-east-1"
COMMANDS = [
    "set -u",
    "PY=$(command -v python3 || command -v python)",
    "J=$(aws sts assume-role --role-arn " + ROLE + " --role-session-name fb-r2-4-negarm --duration-seconds 900 --output json 2>&1)"
    " || { echo \"ASSUME-FAILED: $(echo \"$J\" | head -c 400)\"; exit 0; }",
    "case \"$J\" in *AccessKeyId*) ;; *) echo \"ASSUME-FAILED: $(echo \"$J\" | head -c 400)\"; exit 0;; esac",
    "export AWS_ACCESS_KEY_ID=$(echo \"$J\" | $PY -c 'import sys,json;print(json.load(sys.stdin)[\"Credentials\"][\"AccessKeyId\"])')",
    "export AWS_SECRET_ACCESS_KEY=$(echo \"$J\" | $PY -c 'import sys,json;print(json.load(sys.stdin)[\"Credentials\"][\"SecretAccessKey\"])')",
    "export AWS_SESSION_TOKEN=$(echo \"$J\" | $PY -c 'import sys,json;print(json.load(sys.stdin)[\"Credentials\"][\"SessionToken\"])')",
    "echo \"CALLER: $(aws sts get-caller-identity --query Arn --output text 2>&1 | head -c 300)\"",
    "echo \"INF: $(aws s3api list-objects-v2 --bucket opal-data-inflection --max-keys 1 --query KeyCount --output text 2>&1 | tr '\\n' ' ' | head -c 600)\"",
    "echo \"COT: $(aws s3api list-objects-v2 --bucket opal-data-cottonwood --max-keys 1 --query KeyCount --output text 2>&1 | tr '\\n' ' ' | head -c 600)\"",
    "unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN J",
]


def _fetch(ssm, cid, wait):
    t0 = time.time()
    inv = {}
    while True:
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception as e:  # noqa: BLE001 -- not registered yet
            inv = {"Status": "Pending", "note": str(e)[:120]}
        if inv.get("Status") not in ("Pending", "InProgress", "Delayed"):
            break
        if time.time() - t0 > wait:
            break
        time.sleep(3)
    keep = ("Status", "StatusDetails", "ResponseCode", "StandardOutputContent", "StandardErrorContent")
    out = {k: inv.get(k) for k in keep}
    out["InstanceId"] = INSTANCE
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", dest="show", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--wait", type=int, default=90)
    ap.add_argument("--collect")
    a = ap.parse_args()
    if a.show:
        print(json.dumps({"InstanceIds": [INSTANCE], "DocumentName": "AWS-RunShellScript",
                          "Parameters": {"commands": COMMANDS, "executionTimeout": ["120"]}}, indent=1))
        return 0
    if not a.out:
        ap.error("--out FILE is required")
    import boto3
    ssm = boto3.client("ssm", region_name=REGION)
    if a.collect:
        cid = a.collect
    else:
        r = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                             Comment="ADVI_FIRMBKTS FB-e-4 negative arm: one assume-role, two read-only lists",
                             Parameters={"commands": COMMANDS, "executionTimeout": ["120"]}, TimeoutSeconds=120)
        cid = r["Command"]["CommandId"]
        print("SENT command_id=%s instance=%s" % (cid, INSTANCE))
    rec = {"command_id": cid, "instance": INSTANCE, "role": ROLE, "invocation": _fetch(ssm, cid, a.wait)}
    with open(a.out, "w", encoding="ascii", newline="\n") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=True)
    print("EVIDENCE %s status=%s" % (a.out, rec["invocation"].get("Status")))
    print(rec["invocation"].get("StandardOutputContent") or "(no output yet)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
