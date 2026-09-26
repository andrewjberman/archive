"""OA-g-3 shared reader: scan gateway-access-state-table's POLICY records and parse each ACTIVE principal_profile and
the grant it names with the repo's OWN parser (app/data_entitlement.py at the workspace HEAD). Prints counts only --
never a tid, an oid or an email. Usage: python g3_scan.py AC1|AC2 <workspace-root>."""
import json
import os
import subprocess
import sys

from boto3.dynamodb.types import TypeDeserializer

ac, root = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(root, "infra", "aws", "ec2", "opal-gateway"))
from app import data_entitlement as de  # noqa: E402

aws = os.path.join(root, ".tools", "aws")
res = subprocess.run(["bash", aws, "dynamodb", "scan", "--table-name", "gateway-access-state-table", "--output", "json"],
                     capture_output=True, timeout=120)
try:
    raw = json.loads(res.stdout.decode("utf-8"))["Items"]
except Exception:
    print("SCAN-FAILED rc=%s" % res.returncode)
    print("NOT-OK")
    raise SystemExit(0)
ds = TypeDeserializer()
items = [{k: ds.deserialize(v) for k, v in it.items()} for it in raw]
policy = [i for i in items if str(i.get("pk", "")).startswith("POLICY#")]
by = {(i["pk"], i["sk"]): i for i in policy}
active = [i for i in policy if i.get("sk") == de.PROFILE and i.get("status") == "active"]
portal_only, ops = 0, []
for p in active:
    try:
        prof = de.parse_profile(p, p["tid"], p["oid"])
        gk = de.grant_key(p["tid"], p["oid"], prof.grant_revision)
        g = by.get((gk.pk, gk.sk)) if hasattr(gk, "pk") else by.get(tuple(gk))
        grant = de.parse_grant(g, p["tid"], p["oid"], prof.grant_revision)
    except Exception as exc:
        print("unparseable active profile: %s" % type(exc).__name__)
        continue
    sc = grant.scope
    if not sc.masters and getattr(sc, "portal_channels", None):
        portal_only += 1
        ops.append(sorted(sc.operations))
print("items=%d policy=%d active_profiles=%d portal_only_active=%d operations=%s"
      % (len(items), len(policy), len(active), portal_only, ops))
if ac == "AC1":
    print("OK" if portal_only == 1 else "NOT-OK")
else:
    print("OK" if portal_only == 1 and ops == [["query"]] else "NOT-OK")
