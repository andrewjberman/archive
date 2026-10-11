"""ADVI_FIRMBKTS round 2 check for cell FB-e-4 (F4: whom the two firm buckets' fence admits and refuses),
issuer 2.0.0_SA_COO~B1.

--arms positive            LIVE, read-only, as the caller's own identity (3 arms): the caller performs named s3 acts
                           on opal-data-inflection and opal-data-cottonwood and succeeds; versioning, blocked public
                           access and default encryption read from each live bucket; the fence's admit list read.
--arms negative --evidence FILE
                           grades the worker's saved SSM command record (4 arms): a `*-cot-*` role's own GET of
                           opal-data-inflection was REFUSED by the resource-based deny, and the same role's read of
                           opal-data-cottonwood was not refused by it (the difference control).
--root points at another tree. Never edit this file. Plain ASCII; the last line carries the arm count.
"""
import argparse
import fnmatch
import json
import re
import sys

INF, COT = "opal-data-inflection", "opal-data-cottonwood"
DENY_PHRASE = "explicit deny in a resource-based policy"
ROLE_GLOB = "arn:aws:sts::313476888478:assumed-role/*-cot-*/*"
RUNNER_INSTANCES = {"i-0167fd745ad906a66"}   # irpt-ycharts-runner: running and SSM-online at the cut


def positive():
    import boto3
    from botocore.exceptions import ClientError
    s3 = boto3.client("s3")
    who = boto3.client("sts").get_caller_identity()["Arn"]
    print("  caller: %s" % who)
    res = []
    ok1 = True
    for b in (INF, COT):
        try:
            n = s3.list_objects_v2(Bucket=b, MaxKeys=1).get("KeyCount", -1)
            s3.get_bucket_versioning(Bucket=b)
            print("  %s: ListBucket KeyCount=%s, GetBucketVersioning OK" % (b, n))
        except ClientError as e:
            print("  %s: REFUSED %s" % (b, e.response["Error"]["Code"]))
            ok1 = False
    res.append(("P1 the caller (an identity this estate holds, ARN printed above) performs ListBucket and "
                "GetBucketVersioning on each of the two buckets and succeeds", ok1 and "cloudops" in who))
    ok2 = True
    for b in (INF, COT):
        try:
            v = s3.get_bucket_versioning(Bucket=b).get("Status")
            pab = s3.get_public_access_block(Bucket=b)["PublicAccessBlockConfiguration"]
            enc = s3.get_bucket_encryption(Bucket=b)["ServerSideEncryptionConfiguration"]["Rules"][0][
                "ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"]
            good = v == "Enabled" and all(pab.get(k) is True for k in (
                "BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets")) and enc
            print("  %s: versioning=%s public-access-block=%s encryption=%s" % (b, v, all(pab.values()), enc))
            ok2 = ok2 and good
        except ClientError as e:
            print("  %s: posture read REFUSED %s" % (b, e.response["Error"]["Code"]))
            ok2 = False
    res.append(("P2 each bucket's versioning is Enabled, all four public-access blocks are on and default "
                "encryption is set, read from the live bucket", ok2))
    ok3 = True
    for b, glob in ((INF, "role/*-inf-*"), (COT, "role/*-cot-*")):
        try:
            pol = json.loads(s3.get_bucket_policy(Bucket=b)["Policy"])
            stm = [s for s in pol["Statement"] if s.get("Sid") == "DenyForeignFirmPrincipals"][0]
            adm = stm["Condition"]["ArnNotLike"]["aws:PrincipalArn"]
            adm = adm if isinstance(adm, list) else [adm]
            has_own = any(a.endswith(glob) for a in adm)
            other = "role/*-cot-*" if b == INF else "role/*-inf-*"
            lacks_other = not any(a.endswith(other) for a in adm)
            names_caller = any(fnmatch.fnmatch(who.replace(":user/", ":user/"), a) for a in adm)
            print("  %s: admit list %d patterns; own firm glob %s present=%s; other firm glob absent=%s; "
                  "caller named=%s  (POLICY TEXT, not an exercised refusal)"
                  % (b, len(adm), glob, has_own, lacks_other, names_caller))
            ok3 = ok3 and has_own and lacks_other and names_caller
        except Exception as e:  # noqa: BLE001
            print("  %s: policy read failed (%s)" % (b, type(e).__name__))
            ok3 = False
    res.append(("P3 each bucket's admit list names its own firm glob, lacks the other firm's, and names the "
                "caller (which explains P1)", ok3))
    return res, 3


def negative(path):
    with open(path, encoding="utf-8") as fh:
        rec = json.load(fh)
    inv = rec.get("invocation") or {}
    out = str(inv.get("StandardOutputContent", ""))
    res = []
    res.append(("N1 the command ran on a named SSM-managed runner and reports Status Success",
                inv.get("Status") == "Success" and inv.get("InstanceId") in RUNNER_INSTANCES
                and bool(rec.get("command_id"))))
    caller = re.search(r"^CALLER: (\S+)", out, re.M)
    res.append(("N2 the principal that made the calls is an assumed `*-cot-*` role (its STS ARN is printed)",
                bool(caller) and fnmatch.fnmatch(caller.group(1), ROLE_GLOB)))
    inf = re.search(r"^INF: (.*)$", out, re.M)
    res.append(("N3 the role's read of opal-data-inflection was REFUSED, and the refusal's text names an "
                "explicit deny in a resource-based policy", bool(inf) and DENY_PHRASE in inf.group(1)))
    cot = re.search(r"^COT: (.*)$", out, re.M)
    res.append(("N4 the same role's read of opal-data-cottonwood was NOT refused by that deny (the difference "
                "control: the fence refuses the other firm's role and not its own)",
                bool(cot) and DENY_PHRASE not in cot.group(1)))
    print("  caller=%s" % (caller.group(1) if caller else None))
    print("  INF: %s" % (inf.group(1)[:200] if inf else None))
    print("  COT: %s" % (cot.group(1)[:200] if cot else None))
    return res, 4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("positive", "negative"), required=True)
    ap.add_argument("--evidence")
    ap.add_argument("--root")
    a = ap.parse_args()
    try:
        if a.arms == "positive":
            res, total = positive()
        else:
            if not a.evidence:
                raise FileNotFoundError("--evidence FILE is required for the negative arms")
            res, total = negative(a.evidence)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable evidence (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res, total = [("the evidence this arm grades is present", False)], (3 if a.arms == "positive" else 4)
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 2 F4 %s: %d of %d arms" % (a.arms.upper(), n, total))
    sys.exit(0 if n == total else 1)


if __name__ == "__main__":
    main()
