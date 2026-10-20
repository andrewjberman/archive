"""TCKT_VNEXT round 22 -- R22-dl-1: the fabric's synthetic S3 residue is DELETED by exact bucket, key and VersionId through a throwaway role, and the role is gone.

  python r22_residue_delete_check.py              the live check: the manifest, the result file, every manifest version ABSENT (a 404 only), no version or
                                                  delete marker left on any manifest key, the throwaway role ABSENT, the Deny still in the deploy policy, and a
                                                  non-manifest control object still PRESENT
  python r22_residue_delete_check.py --self-test  the manifest and result scans on a good and several bad documents (no AWS)

Prints RUN-OK (residuedelete) <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1).
"""
import json
import os
import subprocess
import sys

MANIFEST = "org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R22_DELETE/R22_DELETE_MANIFEST.json"
RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r22_delete/R22_DELETE_RESULT.json"
AWS = os.path.abspath(".tools/aws.cmd")
ROLE_PREFIX = "tckt-residue-delete-r22-"
CHUNK = 12
BUCKETS = {"opal-data-cottonwood", "opal-data-irpt"}
DEPLOY_POLICY = "arn:aws:iam::313476888478:policy/cloudops-dell-agent-deploy-policy"
KEYS = {"manifest_blob", "role_names", "role_created_at", "role_destroyed_at", "assume_duration_seconds", "plan_apply_summary", "plan_destroy_summary",
        "deleted", "role_absent_after", "deny_intact_after", "control_object", "no_other_identity"}


def manifest_problem(m):
    objs = m.get("objects") if isinstance(m, dict) else None
    if not isinstance(objs, list) or not objs:
        return "the manifest has no objects list"
    seen = set()
    for o in objs:
        if not isinstance(o, dict) or not all(isinstance(o.get(k), str) and o.get(k).strip() for k in ("bucket", "key", "version_id")):
            return "an entry lacks bucket, key or version_id"
        if o["bucket"] not in BUCKETS:
            return "bucket %s is not one of the two named buckets" % o["bucket"]
        if any(c in o["key"] for c in "*?[]") or o["key"].endswith("/"):
            return "key %r is a prefix or a pattern" % o["key"]
        if o["version_id"] in ("null", "*") or any(c in o["version_id"] for c in "*?"):
            return "version_id %r is not an exact VersionId" % o["version_id"]
        t = (o["bucket"], o["key"], o["version_id"])
        if t in seen:
            return "a duplicate entry"
        seen.add(t)
    return None


def result_problem(res, man, blob):
    missing = sorted(KEYS - set(res))
    if missing:
        return "missing key(s): %s" % missing
    if res["manifest_blob"] != blob:
        return "the result's manifest blob is not the manifest on disk"
    n_roles = -(-len(man["objects"]) // CHUNK)
    if res["role_names"] != [ROLE_PREFIX + str(i) for i in range(n_roles)]:
        return "the role names are not %s0 .. %s%d (one per chunk of %d)" % (ROLE_PREFIX, ROLE_PREFIX, n_roles - 1, CHUNK)
    if not isinstance(res["assume_duration_seconds"], int) or not (900 <= res["assume_duration_seconds"] <= 900):
        return "the assumed session must be exactly 900 seconds (15 minutes)"
    if not (str(res["role_destroyed_at"]) > str(res["role_created_at"])):
        return "the role was not destroyed after it was created"
    if res["role_absent_after"] is not True or res["deny_intact_after"] is not True or res["no_other_identity"] is not True:
        return "role_absent_after, deny_intact_after and no_other_identity must all be True"
    want = {(o["bucket"], o["key"], o["version_id"]) for o in man["objects"]}
    got = set()
    for d in res["deleted"]:
        if not isinstance(d, dict) or d.get("absent_after") is not True or not d.get("deleted_at"):
            return "a deleted entry lacks absent_after True or deleted_at"
        got.add((d.get("bucket"), d.get("key"), d.get("version_id")))
        if not (str(d["deleted_at"]) > str(res["role_created_at"]) and str(d["deleted_at"]) < str(res["role_destroyed_at"])):
            return "a delete happened outside the role's life"
    if got != want:
        return "the deleted set differs from the manifest: %d deleted, %d in the manifest, %d extra, %d missing" % (len(got), len(want), len(got - want), len(want - got))
    c = res["control_object"]
    if not isinstance(c, dict) or c.get("present_after") is not True or (c.get("bucket"), c.get("key")) in {(b, k) for b, k, _ in want}:
        return "the control object must be a NON-manifest object read PRESENT after"
    return None


def run(*args):
    return subprocess.run([AWS] + list(args) + ["--region", "us-east-1"], capture_output=True, text=True, timeout=120)


def absent_version(bucket, key, vid):
    p = run("s3api", "head-object", "--bucket", bucket, "--key", key, "--version-id", vid)
    if p.returncode == 0:
        return False
    if "404" in p.stderr or "Not Found" in p.stderr or "NoSuchVersion" in p.stderr:
        return True
    raise RuntimeError("head-object failed without a 404: %s" % p.stderr.strip()[-160:])


def live():
    try:
        man = json.load(open(MANIFEST, encoding="utf-8"))
        res = json.load(open(RES, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("RUN-BAD cannot read the manifest or the result file: %s" % e)
        return 1
    why = manifest_problem(man)
    if why:
        print("RUN-BAD manifest: %s" % why)
        return 1
    blob = subprocess.run(["git", "hash-object", MANIFEST], capture_output=True, text=True).stdout.strip()
    why = result_problem(res, man, blob)
    if why:
        print("RUN-BAD %s" % why)
        return 1
    try:
        for o in man["objects"]:
            if not absent_version(o["bucket"], o["key"], o["version_id"]):
                print("RUN-BAD a manifest version is still PRESENT: %s" % o["key"][-60:])
                return 1
            p = run("s3api", "list-object-versions", "--bucket", o["bucket"], "--prefix", o["key"], "--output", "json")
            if p.returncode != 0:
                raise RuntimeError("list-object-versions rc=%d" % p.returncode)
            j = json.loads(p.stdout or "{}")
            left = [v for v in (j.get("Versions") or []) + (j.get("DeleteMarkers") or []) if v.get("Key") == o["key"]]
            if left:
                print("RUN-BAD a manifest key still has a version or delete marker: %s" % o["key"][-60:])
                return 1
        for rn in res["role_names"]:
            p = run("iam", "get-role", "--role-name", rn)
            if p.returncode == 0 or "NoSuchEntity" not in p.stderr:
                print("RUN-BAD the throwaway role %s is not ABSENT (a NoSuchEntity answer is required)" % rn)
                return 1
        p = run("iam", "get-policy", "--policy-arn", DEPLOY_POLICY, "--query", "Policy.DefaultVersionId", "--output", "text")
        vid = p.stdout.strip()
        p = run("iam", "get-policy-version", "--policy-arn", DEPLOY_POLICY, "--version-id", vid, "--query", "PolicyVersion.Document", "--output", "json")
        doc = json.loads(p.stdout)
        sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
        deny = [s for s in sts if s.get("Sid") == "DenyS3DeletesOnProductionData" and s.get("Effect") == "Deny"]
        if not deny or "s3:DeleteObject*" not in (deny[0].get("Action") if isinstance(deny[0].get("Action"), list) else [deny[0].get("Action")]):
            print("RUN-BAD DenyS3DeletesOnProductionData is no longer in the deploy policy")
            return 1
        c = res["control_object"]
        p = run("s3api", "head-object", "--bucket", c["bucket"], "--key", c["key"])
        if p.returncode != 0:
            print("RUN-BAD the control object is not PRESENT: %s" % p.stderr.strip()[-120:])
            return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK (residuedelete) %d exact versions ABSENT with no marker left; the throwaway roles ABSENT; the Deny still in the deploy policy; the control object PRESENT" % len(man["objects"]))
    return 0


def good_manifest():
    return {"objects": [{"bucket": "opal-data-cottonwood", "key": "portal/cottonwood/a/x.csv", "version_id": "v1"},
                        {"bucket": "opal-data-irpt", "key": "irpt/f/state/ART-1/y.csv", "version_id": "v2"}]}


def good_result():
    return {"manifest_blob": "B", "role_names": [ROLE_PREFIX + "0"], "role_created_at": "2026-10-20T20:00:00Z", "role_destroyed_at": "2026-10-20T20:20:00Z", "assume_duration_seconds": 900,
            "plan_apply_summary": "3 to add, 0 to change, 0 to destroy", "plan_destroy_summary": "0 to add, 0 to change, 3 to destroy",
            "deleted": [{"bucket": "opal-data-cottonwood", "key": "portal/cottonwood/a/x.csv", "version_id": "v1", "deleted_at": "2026-10-20T20:05:00Z", "absent_after": True},
                        {"bucket": "opal-data-irpt", "key": "irpt/f/state/ART-1/y.csv", "version_id": "v2", "deleted_at": "2026-10-20T20:06:00Z", "absent_after": True}],
            "role_absent_after": True, "deny_intact_after": True, "no_other_identity": True,
            "control_object": {"bucket": "opal-data-irpt", "key": "irpt/f/state/other.csv", "present_after": True}}


def self_test():
    m = good_manifest()
    if manifest_problem(m) is not None:
        return "good manifest refused: %s" % manifest_problem(m)
    mm = {
        "wildcard key": lambda d: d["objects"][0].update(key="portal/cottonwood/*"),
        "prefix key": lambda d: d["objects"][0].update(key="portal/cottonwood/a/"),
        "latest version": lambda d: d["objects"][0].update(version_id="null"),
        "third bucket": lambda d: d["objects"][0].update(bucket="opal-data-bd"),
        "empty list": lambda d: d.update(objects=[]),
        "duplicate": lambda d: d["objects"].append(dict(d["objects"][0])),
        "missing version": lambda d: d["objects"][1].pop("version_id"),
    }
    for name, mut in mm.items():
        d = json.loads(json.dumps(m))
        mut(d)
        if manifest_problem(d) is None:
            return "manifest mutant not caught: %s" % name
    r = good_result()
    if result_problem(r, m, "B") is not None:
        return "good result refused: %s" % result_problem(r, m, "B")
    rm = {
        "other manifest": lambda d: d.update(manifest_blob="C"),
        "other role name": lambda d: d.update(role_names=["admin"]),
        "a role per chunk missing": lambda d: d.update(role_names=[]),
        "long session": lambda d: d.update(assume_duration_seconds=3600),
        "role kept": lambda d: d.update(role_absent_after=False),
        "role destroyed before created": lambda d: d.update(role_destroyed_at="2026-10-20T19:00:00Z"),
        "deny changed": lambda d: d.update(deny_intact_after=False),
        "another identity used": lambda d: d.update(no_other_identity=False),
        "a version not deleted": lambda d: d["deleted"].pop(),
        "an extra delete": lambda d: d["deleted"].append({"bucket": "opal-data-irpt", "key": "irpt/real.csv", "version_id": "v9", "deleted_at": "2026-10-20T20:07:00Z", "absent_after": True}),
        "delete outside the role's life": lambda d: d["deleted"][0].update(deleted_at="2026-10-20T21:00:00Z"),
        "not read absent": lambda d: d["deleted"][0].update(absent_after=False),
        "control is a manifest key": lambda d: d.update(control_object={"bucket": "opal-data-irpt", "key": "irpt/f/state/ART-1/y.csv", "present_after": True}),
        "control gone": lambda d: d["control_object"].update(present_after=False),
        "missing key": lambda d: d.pop("plan_destroy_summary"),
    }
    for name, mut in rm.items():
        d = json.loads(json.dumps(r))
        mut(d)
        if result_problem(d, m, "B") is None:
            return "result mutant not caught: %s" % name
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = self_test()
        print("R22-RESIDUEDELETE-SELFTEST-OK" if why is None else "R22-RESIDUEDELETE-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    return live()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
