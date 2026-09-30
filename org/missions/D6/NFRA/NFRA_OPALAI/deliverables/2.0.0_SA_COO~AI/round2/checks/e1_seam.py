"""OA-e-1 AC2 reader. Usage: python e1_seam.py <worktree-root>. Prints counts only, then OK or NOT-OK."""
import json
import os
import subprocess
import sys
import time

root = sys.argv[1]
aws = os.path.join(root, ".tools", "aws")
inst = "i-07dccb1615503ac99"


def run(args, t=40):
    r = subprocess.run(["bash", aws] + args, capture_output=True, timeout=t)
    return r.returncode, r.stdout.decode("utf-8", "replace").strip()


rc, cid = run(["ssm", "send-command", "--instance-ids", inst, "--document-name", "AWS-RunShellScript",
               "--parameters", 'commands=["grep -h ^TENANT_ID= /opt/opal-gateway/.env | head -1 | cut -d= -f2-"]',
               "--query", "Command.CommandId", "--output", "text"])
tenant, st = "", ""
for _ in range(10):
    time.sleep(3)
    rc2, st = run(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", inst,
                   "--query", "Status", "--output", "text"], 20)
    if st in ("Success", "Failed"):
        break
if st == "Success":
    _, tenant = run(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", inst,
                     "--query", "StandardOutputContent", "--output", "text"], 20)
    tenant = tenant.strip().strip('"').strip("'")
print("host TENANT_ID read=%s (ssm status %s)" % ("yes" if tenant else "no", st or "NONE"))
if not tenant:
    print("NOT-OK")
    raise SystemExit(0)

os.environ["TENANT_ID"] = tenant
os.environ.pop("MOCK_GRAPH", None)
sys.path.insert(0, os.path.join(root, "infra", "aws", "ec2", "opal-gateway"))
from boto3.dynamodb.types import TypeDeserializer  # noqa: E402
from app import data_entitlement as de  # noqa: E402
from app import asker_scope  # noqa: E402
from app.graphql_plumbing import catalog_gate  # noqa: E402

fn = getattr(asker_scope, "resolve_asker_class", None)
if fn is None:
    print("asker_scope.resolve_asker_class absent")
    print("NOT-OK")
    raise SystemExit(0)
rc, raw = run(["dynamodb", "scan", "--table-name", "gateway-access-state-table", "--output", "json"], 120)
try:
    items = json.loads(raw)["Items"]
except Exception:
    print("SCAN-FAILED rc=%s" % rc)
    print("NOT-OK")
    raise SystemExit(0)
ds = TypeDeserializer()
items = [{k: ds.deserialize(v) for k, v in it.items()} for it in items]
active = [i for i in items if str(i.get("pk", "")).startswith("POLICY#") and i.get("sk") == de.PROFILE
          and i.get("status") == "active"]
internal = sum(1 for p in active if fn(p["tid"]) == (catalog_gate.OPAL_INTERNAL, ""))
foreign = fn("00000000-0000-0000-0000-00000000abcd")
print("active profiles=%d resolved opal-internal=%d; foreign tenant -> %s" % (len(active), internal, foreign))
print("OK" if active and internal == len(active) and foreign is None else "NOT-OK")
