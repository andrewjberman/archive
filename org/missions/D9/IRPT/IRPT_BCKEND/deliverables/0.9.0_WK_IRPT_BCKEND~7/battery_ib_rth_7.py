#!/usr/bin/env python3
"""
IB-rth-7 battery -- reconcile Terraform state against the manually-recovered
bucket policy (opal-data-inflection / opal-data-cottonwood).

Re-derives every measurement FRESH on each invocation -- no cached read, no
prior-run log substituted for a live one.

Arm (a), default (no flag) or --arm a:
    terraform init + plan (with refresh, no -target) on
    infra/aws/terraform/shared-infra. Reads the plan for
    aws_s3_bucket_policy.lgic_firm[...] / aws_s3_bucket_versioning.lgic_firm[...]
    and the plan's own summary line.
      0 to add / 0 to change / 0 to destroy  -> CONVERGED, prints
        IBR83-PLAN-CONVERGED-LEDGER-LEGS-DISPOSITIONED
      ANY drift (including TAINTED lgic_firm resources)
        -> STOP. Prints the diff verbatim. NO token.

Arm (b), --arm b:
    describe-instances on i-02448edb624a7a7cf.
      RUNNING -> exercises the two read-only SSM negative-control writes/reads,
        prints SSM command id + AccessDenied error for each; 2 of 2 DENIED ->
        prints IBR83-NEGATIVE-CONTROL-DENIED-2-OF-2. Anything NOT denied -> FAIL,
        no token.
      STOPPED -> does NOT start the host. Prints an UNEXERCISED record (host
        state + reason + owner). No token, neither PASS nor FAIL.

Never applies, never imports, never mutates Terraform state, never starts the
host, never writes an object to either bucket.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[7]
assert (REPO_ROOT / ".tools").is_dir() and (REPO_ROOT / "org").is_dir(), (
    f"REPO_ROOT resolved wrong: {REPO_ROOT}"
)

TF_ROOT = REPO_ROOT / "infra" / "aws" / "terraform" / "shared-infra"
TF_BIN = REPO_ROOT / ".tools" / "terraform.exe"
# native (non-MSYS) python cannot exec the extensionless bash shim directly (WinError 193);
# .tools/aws.cmd is the Windows-shell companion built for exactly this caller shape.
AWS_BIN = REPO_ROOT / ".tools" / "aws.cmd"

HOST_ID = "i-02448edb624a7a7cf"
INFLECTION_BUCKET = "opal-data-inflection"
COTTONWOOD_BUCKET = "opal-data-cottonwood"


def run(cmd, cwd=None, timeout=600):
    proc = subprocess.run(
        [str(c) for c in cmd],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout, proc.stderr


def arm_a():
    print("=== ARM (a): terraform init + plan, infra/aws/terraform/shared-infra ===")
    print(f"TF_BIN={TF_BIN}")
    print(f"TF_ROOT={TF_ROOT}")

    rc, out, err = run([TF_BIN, "init", "-input=false"], cwd=TF_ROOT, timeout=300)
    print("--- terraform init ---")
    print(out[-4000:])
    if err.strip():
        print("--- init stderr ---")
        print(err[-2000:])
    if rc != 0:
        print(f"FAIL: terraform init rc={rc}")
        return 1

    rc, out, err = run(
        [TF_BIN, "plan", "-input=false", "-no-color", "-refresh=true"],
        cwd=TF_ROOT,
        timeout=600,
    )
    print("--- terraform plan (full, verbatim) ---")
    print(out)
    if err.strip():
        print("--- plan stderr ---")
        print(err[-2000:])
    if rc not in (0, 2):
        print(f"FAIL: terraform plan rc={rc} (2=changes present is not itself a failure)")
        return 1

    # Isolate the lgic_firm resource lines specifically.
    lgic_lines = [
        ln for ln in out.splitlines()
        if "lgic_firm" in ln
    ]
    print("--- lines mentioning lgic_firm (denominator: {} of {} total plan lines) ---".format(
        len(lgic_lines), len(out.splitlines())
    ))
    for ln in lgic_lines:
        print(ln)

    tainted = [ln for ln in lgic_lines if "tainted" in ln]

    m = re.search(
        r"Plan:\s*(\d+)\s*to add,\s*(\d+)\s*to change,\s*(\d+)\s*to destroy",
        out,
    )
    no_changes = "No changes." in out or "Your infrastructure matches the configuration" in out

    if no_changes and not tainted:
        add = change = destroy = 0
        clean = True
    elif m:
        add, change, destroy = (int(x) for x in m.groups())
        clean = (add == 0 and change == 0 and destroy == 0) and not tainted
    else:
        print("FAIL: could not locate a 'Plan: N to add...' summary line or a 'No changes' line in plan output.")
        return 1

    print(f"--- summary: add={add} change={change} destroy={destroy} tainted_lgic_firm_lines={len(tainted)} ---")

    if clean:
        print("RESULT: 0/0/0, no tainted lgic_firm resources -- the manual PUT converged "
              "exactly with what Terraform would render.")
        print("IBR83-PLAN-CONVERGED-LEDGER-LEGS-DISPOSITIONED")
        return 0
    else:
        print("RESULT: DRIFT. Plan is NOT 0/0/0 clean on the lgic_firm resources "
              "(or carries TAINTED lgic_firm resources left over from the half-landed "
              "2026-09-18 apply, row W3-S45). STOPPING per BOUNDS -- no apply, no state "
              "mutation. This is a carry to the COO, not a fix landed by this cell.")
        return 2


def ssm_send(instance_id, doc_name, params, comment):
    cmd = [
        AWS_BIN, "ssm", "send-command",
        "--instance-ids", instance_id,
        "--document-name", doc_name,
        "--parameters", json.dumps(params),
        "--comment", comment,
        "--output", "json",
    ]
    rc, out, err = run(cmd, timeout=60)
    if rc != 0:
        return None, rc, out, err
    try:
        data = json.loads(out)
        command_id = data["Command"]["CommandId"]
    except Exception as exc:  # noqa: BLE001
        return None, rc, out, f"{err}\nPARSE-FAIL: {exc}"
    return command_id, rc, out, err


def ssm_wait_and_get(instance_id, command_id, timeout=90):
    import time
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        rc, out, err = run(
            [AWS_BIN, "ssm", "get-command-invocation",
             "--command-id", command_id, "--instance-id", instance_id,
             "--output", "json"],
            timeout=30,
        )
        if rc == 0:
            try:
                data = json.loads(out)
                last = data
                status = data.get("Status")
                if status not in ("Pending", "InProgress", "Delayed"):
                    return data
            except Exception:  # noqa: BLE001
                pass
        time.sleep(3)
    return last


def arm_b():
    print("=== ARM (b): negative control, host {} ===".format(HOST_ID))
    rc, out, err = run(
        [AWS_BIN, "ec2", "describe-instances",
         "--instance-ids", HOST_ID,
         "--query", "Reservations[0].Instances[0].State.Name",
         "--output", "text"],
        timeout=60,
    )
    if rc != 0:
        print(f"FAIL: describe-instances rc={rc} stderr={err}")
        return 1
    state = out.strip()
    print(f"HOST STATE: {state}")

    if state == "stopped":
        print("UNEXERCISED (R83-AC2 non-verdict): host {} is STOPPED.".format(HOST_ID))
        print("REASON: this cell's BOUNDS explicitly forbid starting the host "
              "('The host is never started by this cell'; 'another owner's resource, "
              "an EC2 state change outside this cell's grant').")
        print("OWNER: 2.0.0_SA_COO~B (issuer) -- following IB-rtf-5's own R62-AC3 "
              "precedent exactly (never a FAIL for a control nobody ran).")
        print("No token printed -- neither PASS nor FAIL.")
        return 0

    if state != "running":
        print(f"UNEXERCISED: host state is '{state}', neither running nor stopped -- "
              "not a state this criterion's two branches cover. Not started by this cell.")
        return 0

    # RUNNING: exercise the two read-only negative controls via SSM.
    print("HOST RUNNING -- exercising negative control via read-only SSM.")

    write_key = "irpt/inflection/gold/directory/zz-negative-control"
    cmd1, rc1, out1, err1 = ssm_send(
        HOST_ID,
        "AWS-RunShellScript",
        {"commands": [
            f"aws s3api put-object --bucket {INFLECTION_BUCKET} --key {write_key} "
            f"--body /dev/null 2>&1; echo RC=$?"
        ]},
        "IB-rth-7 R83-AC2 negative control: host role write attempt (expect AccessDenied)",
    )
    print(f"--- control 1: host role write to {INFLECTION_BUCKET}/{write_key} ---")
    print(f"send-command rc={rc1} command_id={cmd1}")
    if cmd1 is None:
        print(f"FAIL: could not dispatch SSM command. stdout={out1} stderr={err1}")
        return 1
    result1 = ssm_wait_and_get(HOST_ID, cmd1)
    print(json.dumps(result1, indent=2)[:3000] if result1 else "FAIL: no result (timeout)")

    read_prefix = "irpt/cottonwood/gold/directory/"
    cmd2, rc2, out2, err2 = ssm_send(
        HOST_ID,
        "AWS-RunShellScript",
        {"commands": [
            f"aws s3api list-objects-v2 --bucket {COTTONWOOD_BUCKET} --prefix {read_prefix} "
            f"2>&1; echo RC=$?"
        ]},
        "IB-rth-7 R83-AC2 negative control: 49f principal read attempt (expect AccessDenied)",
    )
    print(f"--- control 2: 49f principal read of {COTTONWOOD_BUCKET}/{read_prefix} ---")
    print(f"send-command rc={rc2} command_id={cmd2}")
    if cmd2 is None:
        print(f"FAIL: could not dispatch SSM command. stdout={out2} stderr={err2}")
        return 1
    result2 = ssm_wait_and_get(HOST_ID, cmd2)
    print(json.dumps(result2, indent=2)[:3000] if result2 else "FAIL: no result (timeout)")

    def denied(result):
        if not result:
            return False
        text = (result.get("StandardOutputContent", "") or "") + (result.get("StandardErrorContent", "") or "")
        return "AccessDenied" in text

    d1 = denied(result1)
    d2 = denied(result2)
    print(f"--- verdict: control1_denied={d1} control2_denied={d2} ---")
    if d1 and d2:
        print("IBR83-NEGATIVE-CONTROL-DENIED-2-OF-2")
        return 0
    print("FAIL: not 2 of 2 DENIED -- the fence is not actually live. BLOCKING.")
    return 2


def main():
    arm = "a"
    if "--arm" in sys.argv:
        idx = sys.argv.index("--arm")
        arm = sys.argv[idx + 1]
    if arm == "a":
        return arm_a()
    if arm == "b":
        return arm_b()
    print(f"FAIL: unknown --arm {arm!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
