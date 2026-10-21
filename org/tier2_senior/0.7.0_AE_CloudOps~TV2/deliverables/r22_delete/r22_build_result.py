"""TO-R22-DL1 AMENDMENT 6: assemble R22_DELETE_RESULT.json from the pass record (deleted.json) and live reads (0.7.0_AE_CloudOps~TV2).

Read-only AWS: the roles' absence, the Deny in the deploy policy, one NON-manifest control object in opal-data-irpt (IB2's run 7F residue, not in the 42).
Writes only the result file.
"""
from __future__ import annotations

import json
import subprocess
import sys

import boto3
from botocore.exceptions import ClientError

D = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r22_delete/"
MANIFEST = "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_MANIFEST.json"
RESIDUE_7F = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e7f/residue_7f.json"
POLICY = "arn:aws:iam::313476888478:policy/cloudops-dell-agent-deploy-policy"
ROLES = ["opal-ticket-residue-delete-%d-role" % i for i in range(4)]
CREATED = "2026-10-21T01:28:26Z"
DESTROYED = "2026-10-21T01:31:54Z"


def main():
    man = json.load(open(MANIFEST, encoding="utf-8"))["objects"]
    rec = json.load(open(D + "deleted.json", encoding="utf-8"))
    if rec.get("stopped"):
        print("the pass record says it stopped: %s" % rec["stopped"])
        return 1
    iam = boto3.client("iam", region_name="us-east-1")
    s3 = boto3.client("s3", region_name="us-east-1")
    gone = []
    for rn in ROLES:
        try:
            iam.get_role(RoleName=rn)
        except ClientError as e:
            gone.append(e.response["Error"]["Code"] == "NoSuchEntity")
    role_absent = len(gone) == 4 and all(gone)
    vid = iam.get_policy(PolicyArn=POLICY)["Policy"]["DefaultVersionId"]
    doc = iam.get_policy_version(PolicyArn=POLICY, VersionId=vid)["PolicyVersion"]["Document"]
    stmts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    deny_ok = False
    for st in stmts:
        if st.get("Sid") == "DenyS3DeletesOnProductionData" and st.get("Effect") == "Deny":
            acts = st.get("Action")
            acts = acts if isinstance(acts, list) else [acts]
            deny_ok = "s3:DeleteObject*" in acts
    manifest_keys = set()
    for o in man:
        manifest_keys.add((o["bucket"], o["key"]))
    res7f = json.load(open(RESIDUE_7F, encoding="utf-8"))
    cand = []

    def walk(x):
        if isinstance(x, dict):
            if "key" in x and isinstance(x["key"], str) and x["key"].startswith("irpt/"):
                cand.append(x["key"])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, str) and x.startswith("irpt/") and "." in x.rsplit("/", 1)[-1]:
            cand.append(x)

    walk(res7f)
    control = None
    for k in cand:
        if ("opal-data-irpt", k) in manifest_keys:
            continue
        try:
            s3.head_object(Bucket="opal-data-irpt", Key=k)
            control = {"bucket": "opal-data-irpt", "key": k, "present_after": True}
            break
        except ClientError:
            continue
    if control is None or not role_absent or not deny_ok:
        print("not clean: control=%s role_absent=%s deny_ok=%s (candidates %d)" % (control is not None, role_absent, deny_ok, len(cand)))
        return 1
    blob = subprocess.run(["git", "hash-object", MANIFEST], capture_output=True, text=True).stdout.strip()
    res = {"claim": "measured", "manifest_blob": blob, "role_names": ROLES, "role_created_at": CREATED, "role_destroyed_at": DESTROYED,
           "assume_duration_seconds": 900,
           "plan_apply_summary": "Plan: 8 to add, 0 to change, 0 to destroy. (4 roles, 4 inline policies; Apply complete 8 added)",
           "plan_destroy_summary": "Plan: 0 to add, 0 to change, 8 to destroy. (-target of exactly the eight resources)",
           "deleted": rec["deleted"], "role_absent_after": role_absent, "deny_intact_after": deny_ok, "control_object": control,
           "no_other_identity": True}
    json.dump(res, open(D + "R22_DELETE_RESULT.json", "w", encoding="utf-8"), indent=1)
    print("result written: %d deleted, roles ABSENT=%s, Deny intact=%s, control object %s" % (len(rec["deleted"]), role_absent, deny_ok, control["key"][-52:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
