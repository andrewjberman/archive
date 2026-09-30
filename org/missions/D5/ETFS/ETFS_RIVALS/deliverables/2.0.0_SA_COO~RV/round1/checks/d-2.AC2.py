"""RIV-d-2 AC2 -- the DEPLOYED gateway bytes are the merged bytes (CLAUDE.md 22a: diff deployed bytes against the
build input, never by filename). One read-only SSM command on the gateway instance hashes the deployed
rivalfunds_view.py and server.py; each must equal the sha256 of the same file at this tree's HEAD."""
import hashlib
import json
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

RECORD = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~5/d2_live.json"
FILES = ["app/rivalfunds_view.py", "app/server.py"]


def run(v):
    import boto3

    root = c.setup_path()
    rec = json.loads((root / RECORD).read_text(encoding="utf-8"))
    iid, base = rec["gateway_instance_id"], rec.get("gateway_app_root", "/opt/opal-gateway")
    want = {}
    for f in FILES:
        b = subprocess.run(["git", "show", f"HEAD:infra/aws/ec2/opal-gateway/{f}"], capture_output=True, check=True).stdout
        want[f] = hashlib.sha256(b).hexdigest()
    ssm = boto3.client("ssm", region_name="us-east-1")
    cmd = "sha256sum " + " ".join(f"{base}/{f}" for f in FILES)
    cid = ssm.send_command(InstanceIds=[iid], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]})["Command"]["CommandId"]
    out, status = "", "Pending"
    for _ in range(40):
        time.sleep(2)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=iid)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        status, out = inv["Status"], inv.get("StandardOutputContent", "")
        if status not in ("Pending", "InProgress", "Delayed"):
            break
    v.check(status == "Success", f"SSM sha256sum Status {status} (command {cid})")
    got = {ln.split()[1][len(base) + 1:]: ln.split()[0] for ln in out.splitlines() if len(ln.split()) == 2}
    for f in FILES:
        v.check(got.get(f) == want[f], f"deployed {f} sha256 {got.get(f)} == HEAD {want[f]}")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
