"""RIV-r-1 AC1 -- the reachability measurement is RECORDED and it is the host's own answer.

Reads the worker's result file and re-reads the SAME SSM command invocation from AWS: the invocation succeeded, ran
on the recorded instance, and its stdout carries the HTTP status the file records. Reachable or not is the FINDING;
this criterion grades that the measurement was taken from AWS and recorded faithfully."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

RESULT = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~4/r1_reachability.json"


def run(v):
    import boto3

    root = c.setup_path()
    p = root / RESULT
    v.check(p.exists(), f"result file {RESULT}")
    if not p.exists():
        return
    r = json.loads(p.read_text(encoding="utf-8"))
    for k in ("measured_at_utc", "instance_id", "command_id", "url", "http_status", "bytes", "first_line", "root_http_status"):
        v.check(k in r, f"field {k} recorded")
    if "command_id" not in r or "instance_id" not in r:
        return
    inv = boto3.client("ssm", region_name="us-east-1").get_command_invocation(CommandId=r["command_id"], InstanceId=r["instance_id"])
    v.check(inv.get("Status") == "Success", f"SSM invocation Status Success ({inv.get('Status')})")
    out = inv.get("StandardOutputContent", "")
    v.check(str(r.get("http_status")) in out, f"the host's stdout carries the recorded HTTP status {r.get('http_status')}")
    v.check("brownadvisory.filepoint.live" in r.get("url", ""), "the probed URL is BASG's issuer file")
    print(json.dumps(r)[:600])


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
