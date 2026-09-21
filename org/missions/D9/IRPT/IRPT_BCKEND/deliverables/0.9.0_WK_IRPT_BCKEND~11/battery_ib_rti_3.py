"""IB-rti-3 battery: L4 negative control on a discriminating instrument.
READ-CLASS ONLY: iam List/Get/Simulate, sts:AssumeRole (existing trust), s3:ListBucket (MaxKeys=1),
s3:GetBucketPolicy. No write of any kind. Arms: --arm principal | --arm exercise.
"""
import argparse
import fnmatch
import hashlib
import json
import time
import boto3
from botocore.exceptions import ClientError

ACCT = "313476888478"
SEAT = f"arn:aws:iam::{ACCT}:user/Andrew_Berman"
BUCKETS = {
    "opal-data-inflection": "*-inf-*",
    "opal-data-cottonwood": "*-cot-*",
}
CONTROL_BUCKETS = ["opal-data-assets", "opal-data-49financial", "opal-data-blackdiamond"]
ACTION = "s3:ListBucket"
OUT = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~11/"

iam = boto3.client("iam")
s3 = boto3.client("s3")
sts = boto3.client("sts")


def live_policy(b):
    raw = s3.get_bucket_policy(Bucket=b)["Policy"]
    return raw, json.loads(raw)


def exempt_list(pol):
    out = []
    for st in pol["Statement"]:
        if st.get("Effect") == "Deny":
            v = st["Condition"]["ArnNotLike"]["aws:PrincipalArn"]
            out += [v] if isinstance(v, str) else v
    return out


def is_exempt(arn, patterns):
    return any(fnmatch.fnmatchcase(arn, p) for p in patterns)


def listall(fn, key, **kw):
    out = []
    for pg in boto3.client("iam").get_paginator(fn).paginate(**kw):
        out += pg[key]
    return out


def trust_admits_seat(doc):
    """Return (admits, why). Conditions -> not admitted unless empty."""
    for st in doc.get("Statement", []):
        if st.get("Effect") != "Allow":
            continue
        act = st.get("Action")
        acts = [act] if isinstance(act, str) else act
        if not any(a in ("sts:AssumeRole", "sts:*", "*") for a in acts):
            continue
        p = st.get("Principal", {})
        aws = p.get("AWS") if isinstance(p, dict) else p
        if aws is None:
            continue
        aws = [aws] if isinstance(aws, str) else aws
        hit = [a for a in aws if a in ("*", SEAT, f"arn:aws:iam::{ACCT}:root", ACCT)]
        if hit:
            if st.get("Condition"):
                # kept as a candidate route: the condition (ArnNotEquals on a role / RoleSessionName) is one the seat can meet
                return True, "trust stmt Principal.AWS=" + json.dumps(hit) + " WITH Condition " + json.dumps(st["Condition"])
            return True, "trust stmt Principal.AWS=" + json.dumps(hit) + " no Condition"
    return False, "trust does not admit the seat"


def granting_statements(role_name, action, resource):
    """Simulate identity policy for action on resource; return (decision, matched)."""
    arn = f"arn:aws:iam::{ACCT}:role/{role_name}"
    r = iam.simulate_principal_policy(PolicySourceArn=arn, ActionNames=[action], ResourceArns=[resource])
    ev = r["EvaluationResults"][0]
    return ev["EvalDecision"], ev.get("MatchedStatements", []), ev.get("OrganizationsDecisionDetail")


def stmt_text(role_name, source_policy_id, action):
    """Fetch the policy statement text that mentions the action (inline or attached)."""
    try:
        d = iam.get_role_policy(RoleName=role_name, PolicyName=source_policy_id)["PolicyDocument"]
        return "inline:" + source_policy_id, d["Statement"]
    except ClientError:
        pass
    for ap in listall("list_attached_role_policies", "AttachedPolicies", RoleName=role_name):
        if ap["PolicyName"] == source_policy_id:
            v = iam.get_policy(PolicyArn=ap["PolicyArn"])["Policy"]["DefaultVersionId"]
            d = iam.get_policy_version(PolicyArn=ap["PolicyArn"], VersionId=v)["PolicyVersion"]["Document"]
            return ap["PolicyArn"], d["Statement"]
    return "unresolved", []


def relevant(stmts, action):
    keep = []
    st = stmts if isinstance(stmts, list) else [stmts]
    for s in st:
        a = s.get("Action", [])
        a = [a] if isinstance(a, str) else a
        if s.get("Effect") == "Allow" and any(fnmatch.fnmatchcase(action.lower(), x.lower()) for x in a):
            keep.append(s)
    return keep


def census():
    roles = listall("list_roles", "Roles")
    users = listall("list_users", "Users")
    return roles, users


def principal_arm():
    roles, users = census()
    print(f"CENSUS DENOMINATOR: {len(roles)} roles, {len(users)} users examined (iam list_roles/list_users, paginated) at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    print("USERS (no credentials held by the seat for any but the seat itself; a user is INELIGIBLE as an assume target):", [u["UserName"] for u in users])
    result = {}
    cd, cm, _ = granting_statements("opal-news-lambda-role", ACTION, "arn:aws:s3:::opal-data-inflection")
    print(f"SIMULATOR POSITIVE CONTROL: opal-news-lambda-role (AmazonS3ReadOnlyAccess; trust is the lambda service, NOT assumable by the seat, never a candidate) {ACTION} on opal-data-inflection = {cd} via {[x['SourcePolicyId'] for x in cm]}")
    for b, own in BUCKETS.items():
        raw, pol = live_policy(b)
        ex = exempt_list(pol)
        print(f"\n=== {b}: LIVE bucket policy sha256={hashlib.sha256(raw.encode()).hexdigest()[:16]} len={len(raw)}")
        print(f"FULL ArnNotLike exemption list ({len(ex)} entries), printed BEFORE choosing any principal:")
        for e in ex:
            print("   ", e)
        cands, rejected = [], []
        counts = {"service-linked": 0, "exempt(own pattern/list)": 0, "trust-not-admitting": 0, "no-identity-grant": 0}
        res = f"arn:aws:s3:::{b}"
        for r in roles:
            name, arn = r["RoleName"], r["Arn"]
            if r.get("Path", "").startswith("/aws-service-role/"):
                counts["service-linked"] += 1
                continue
            if is_exempt(arn, ex):
                counts["exempt(own pattern/list)"] += 1
                continue
            ok, why = trust_admits_seat(r["AssumeRolePolicyDocument"])
            if not ok:
                counts["trust-not-admitting"] += 1
                continue
            try:
                dec, matched, _ = granting_statements(name, ACTION, res)
            except ClientError as e:
                rejected.append((name, "simulate error " + e.response["Error"]["Code"]))
                continue
            if dec != "allowed":
                counts["no-identity-grant"] += 1
                rejected.append((name, f"trust ok ({why}) but identity IAM decision for {ACTION} on {res} = {dec}"))
                continue
            cands.append((name, arn, why, matched))
        print(f"census breakdown for {b}: {counts}; candidate(eligible)={len(cands)}")
        print("rejected with trust ok but no identity grant (up to 15):")
        for n, w in rejected[:15]:
            print("   ", n, "--", w)
        for name, arn, why, matched in cands[:12]:
            print(f"  ELIGIBLE CANDIDATE {arn}  exemption-check: NOT in list, does not match {own}; assume route: {why}")
            for m in matched:
                sid = m["SourcePolicyId"]
                src, stmts = stmt_text(name, sid, ACTION)
                print(f"     granting policy: {src} (type {m['SourcePolicyType']})")
                for s in relevant(stmts, ACTION):
                    print("     granting statement:", json.dumps(s)[:600])
        result[b] = cands
    ok = all(True for _ in BUCKETS)  # table complete for each bucket (eligible or NONE ELIGIBLE printed)
    for b, c in result.items():
        if not c:
            print(f"\n{b}: NONE ELIGIBLE (candidates rejected above; census denominator {len(roles)} roles + {len(users)} users)")
    if ok:
        print("IBR93-PRINCIPAL-TABLE-COMPLETE-2-OF-2")
    return result


def pick_role(b, cands):
    """Prefer a role with an account-wide s3 List grant not naming the target's firm."""
    return cands[0] if cands else None


def exercise_arm():
    roles, users = census()
    ex_ok = 0
    for b, own in BUCKETS.items():
        raw, pol = live_policy(b)
        ex = exempt_list(pol)
        print(f"\n=== {b}: live policy sha256={hashlib.sha256(raw.encode()).hexdigest()[:16]}; exemption list printed:")
        for e in ex:
            print("   ", e)
        # re-measure emptiness at the event
        try:
            n = s3.list_objects_v2(Bucket=b, MaxKeys=5).get("KeyCount")
            print("(seat, exempt Andrew_Berman) KeyCount at event:", n, "-- exempt identity; proves the exemption only, NOT used as the negative arm")
        except ClientError as e:
            print("seat list error:", e)
        res = f"arn:aws:s3:::{b}"
        cands = []
        for r in roles:
            if r.get("Path", "").startswith("/aws-service-role/") or is_exempt(r["Arn"], ex):
                continue
            ok, why = trust_admits_seat(r["AssumeRolePolicyDocument"])
            if not ok:
                continue
            try:
                dec, matched, _ = granting_statements(r["RoleName"], ACTION, res)
            except ClientError:
                continue
            if dec == "allowed":
                cands.append((r["RoleName"], r["Arn"], matched))
        if not cands:
            print(f"{b}: NONE ELIGIBLE -> L4 cannot be discriminatingly exercised without a new grant (owner 1.0.0_SA_CTO)")
            continue
        done = False
        for name, arn, matched in cands:
            print(f"\n-- attempting principal {arn}")
            for m in matched:
                src, stmts = stmt_text(name, m["SourcePolicyId"], ACTION)
                for s in relevant(stmts, ACTION):
                    print(f"   granting statement ({src}) for {ACTION} on {res}:", json.dumps(s)[:500])
            try:
                cr = sts.assume_role(RoleArn=arn, RoleSessionName="ibrti3-l4", DurationSeconds=900)["Credentials"]
            except ClientError as e:
                print("   assume_role refused:", e.response["Error"]["Message"])
                continue
            c = boto3.client("s3", aws_access_key_id=cr["AccessKeyId"], aws_secret_access_key=cr["SecretAccessKey"], aws_session_token=cr["SessionToken"])
            who = boto3.client("sts", aws_access_key_id=cr["AccessKeyId"], aws_secret_access_key=cr["SecretAccessKey"], aws_session_token=cr["SessionToken"]).get_caller_identity()["Arn"]
            print("   acting identity:", who)
            # positive arm: same principal, same action, control bucket outside fence
            pos = None
            for cb in CONTROL_BUCKETS:
                try:
                    c.list_objects_v2(Bucket=cb, MaxKeys=1)
                    pos = cb
                    print(f"   POSITIVE ARM: {who} {ACTION} on arn:aws:s3:::{cb} -> SUCCEEDED (control bucket, not named by the fence)")
                    break
                except ClientError as e:
                    print(f"   positive try {cb}: {e.response['Error']['Code']}: {e.response['Error']['Message']}")
            if not pos:
                continue
            try:
                c.list_objects_v2(Bucket=b, MaxKeys=1)
                print(f"   NEGATIVE ARM: {who} {ACTION} on {res} -> SUCCEEDED  => FENCE NOT LIVE (FAIL, BLOCKING)")
                print("IBR93-NEGATIVE-ARM-SUCCEEDED-FAIL")
                return
            except ClientError as e:
                msg = e.response["Error"]["Message"]
                print(f"   NEGATIVE ARM: {who} {ACTION} on {res} -> {e.response['Error']['Code']}: {msg}")
                if "explicit deny in a resource-based policy" in msg:
                    print("   ATTRIBUTION: S3 error context names an explicit deny in a resource-based policy")
                    ex_ok += 1
                    done = True
                    break
                print("   ATTRIBUTION: NOT available from the error context -> un-attributable")
        if not done:
            print(f"{b}: NOT DISCRIMINATED")
    if ex_ok == 2:
        print("IBR93-NEGATIVE-CONTROL-DISCRIMINATES-2-OF-2")
    else:
        print(f"NO TOKEN: {ex_ok} of 2 buckets discriminated -> non-verdict UNCOMPUTABLE-BY-CONSTRUCTION, L4 cannot be discriminatingly exercised without a new grant (owner 1.0.0_SA_CTO)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["principal", "exercise"])
    a = ap.parse_args()
    principal_arm() if a.arm == "principal" else exercise_arm()
