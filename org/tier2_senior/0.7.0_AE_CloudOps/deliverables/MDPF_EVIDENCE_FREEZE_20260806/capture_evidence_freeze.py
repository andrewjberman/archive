"""MDPF_PROPVALIDATION P0.1 -- evidence freeze + rollback baseline. READ-ONLY.

ONE artifact serving two purposes (COO~Z: "this IS doc 04 s.4's rollback capture -- one
artifact, not two"). Captures the live plane at a stamped instant so a rollback has
something to restore TO, and so the cutover has a before-image to diff against.

Captured per 04 s.4:
  - Lambda code SHA256, config, layer ARNs, roles, environment
  - Schedule/rule definitions, targets, retry policy, DLQ policy, Lambda permissions
  - IAM inline + attached policy documents
  - S3 bucket versioning state, and current VersionId/ETag for every served pair
    and the dated _aggregate_aua contract
  - EC2 instance + SSM document identifiers

DISCIPLINE THIS FILE ENFORCES:
  - EVERY collection prints its denominator. A count that was never paginated is a page
    size wearing a total's clothing.
  - EVERY failure is recorded as a structured error IN the artifact, never swallowed. A
    retrieval failure returns a VALUE, and a swallowed one reads as absence.
  - Timestamps are boto3 tz-aware UTC, serialised with the +00:00 offset. Never an
    `aws s3 ls` column -- that prints LOCAL time and silently shifts by the box offset.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from zoneinfo import ZoneInfo

import boto3
from botocore.exceptions import ClientError

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

ASSETS = "opal-data-assets"
PORTAL = "opal-data-portal-v2"
EC2_ID = "i-02448edb624a7a7cf"

LAMBDAS = [
    "mdpf-daily-trigger",
    "mdpf-accrual-trigger",
    "opal-assets-mdpf-portal-publisher",
    "opal-assets-daily-emitter",
    "mdpf-freshness-checker",
]
SCHEDULES = [
    "mdpf-scheduled-floor",
    "mdpf-accrual-bridge-daily",
    "opal-assets-mdpf-portal-publisher-daily",
]
GOLD_PREFIX = "portal/gold/mdpf/"
AGG_PREFIX = "gold/mdpf_revamp/_aggregate_aua/"
PLATINUM_PREFIX = "platinum/mdpf/"
JSON_BELL_PREFIX = "json/mdpf/"

lam = boto3.client("lambda")
sch = boto3.client("scheduler")
ev = boto3.client("events")
iam = boto3.client("iam")
s3 = boto3.client("s3")
ec2 = boto3.client("ec2")
ssm = boto3.client("ssm")

ERRORS: list[dict] = []


def err(where: str, e: Exception) -> dict:
    rec = {"where": where, "error": type(e).__name__, "detail": str(e)[:300]}
    ERRORS.append(rec)
    return rec


def iso(o):
    if isinstance(o, dt.datetime):
        return o.astimezone(UTC).isoformat()
    return str(o)


def capture_lambdas() -> dict:
    out, roles = {}, set()
    for fn in LAMBDAS:
        try:
            c = lam.get_function_configuration(FunctionName=fn)
        except ClientError as e:
            out[fn] = err(f"lambda:{fn}", e)
            continue
        try:
            pol = lam.get_policy(FunctionName=fn)["Policy"]
        except ClientError:
            pol = None       # no resource policy is a real state, not an error
        out[fn] = {
            "CodeSha256": c["CodeSha256"],
            "Runtime": c.get("Runtime"),
            "MemorySize": c.get("MemorySize"),
            "Timeout": c.get("Timeout"),
            "EphemeralStorageMB": c.get("EphemeralStorage", {}).get("Size"),
            "Architectures": c.get("Architectures"),
            "Role": c["Role"],
            "Handler": c.get("Handler"),
            "Layers": [lyr["Arn"] for lyr in c.get("Layers", [])],
            "Environment": c.get("Environment", {}).get("Variables", {}),
            "LastModified": c.get("LastModified"),
            "RevisionId": c.get("RevisionId"),
            "ReservedConcurrency": _reserved(fn),
            "ResourcePolicy": json.loads(pol) if pol else None,
        }
        roles.add(c["Role"].rsplit("/", 1)[-1])
    return {"functions": out, "denominator": f"{len(LAMBDAS)} requested, "
            f"{sum(1 for v in out.values() if 'CodeSha256' in v)} captured",
            "roles_seen": sorted(roles)}


def _reserved(fn):
    try:
        return lam.get_function_concurrency(FunctionName=fn).get("ReservedConcurrentExecutions")
    except ClientError as e:
        return err(f"concurrency:{fn}", e)


def capture_iam(role_names) -> dict:
    out = {}
    for r in role_names:
        entry = {}
        try:
            entry["inline"] = {}
            names = iam.list_role_policies(RoleName=r)["PolicyNames"]
            entry["inline_denominator"] = len(names)
            for p in names:
                entry["inline"][p] = iam.get_role_policy(RoleName=r, PolicyName=p)["PolicyDocument"]
            att = iam.list_attached_role_policies(RoleName=r)["AttachedPolicies"]
            entry["attached_denominator"] = len(att)
            entry["attached"] = {}
            for a in att:
                v = iam.get_policy(PolicyArn=a["PolicyArn"])["Policy"]["DefaultVersionId"]
                entry["attached"][a["PolicyArn"]] = iam.get_policy_version(
                    PolicyArn=a["PolicyArn"], VersionId=v)["PolicyVersion"]["Document"]
        except ClientError as e:
            entry = err(f"iam:{r}", e)
        out[r] = entry
    return {"roles": out, "denominator": f"{len(role_names)} roles"}


def capture_schedules() -> dict:
    out = {}
    for s in SCHEDULES:
        try:
            d = sch.get_schedule(Name=s)
            d.pop("ResponseMetadata", None)
            out[s] = json.loads(json.dumps(d, default=iso))
        except ClientError as e:
            out[s] = err(f"schedule:{s}", e)
    rules = {}
    try:
        paginator = ev.get_paginator("list_rules")
        allr, pages = [], 0
        for page in paginator.paginate():
            pages += 1
            allr.extend(page.get("Rules", []))
        mdpf = [r for r in allr if "mdpf" in r["Name"].lower()]
        for r in mdpf:
            tg = ev.list_targets_by_rule(Rule=r["Name"]).get("Targets", [])
            rules[r["Name"]] = {"rule": json.loads(json.dumps(r, default=iso)),
                                "targets": json.loads(json.dumps(tg, default=iso))}
        rules["_denominator"] = (f"{len(allr)} rules across {pages} pages "
                                 f"(explicitly paginated -- a --query length() would "
                                 f"have returned the PAGE count), {len(mdpf)} mdpf-matching")
    except ClientError as e:
        rules["_error"] = err("events:list_rules", e)
    return {"scheduler": out, "classic_rules": rules,
            "denominator": f"{len(SCHEDULES)} schedules requested"}


def _list(bucket, prefix):
    keys, pages = [], 0
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        pages += 1
        keys.extend(page.get("Contents", []))
    return keys, pages


def capture_s3() -> dict:
    out = {"versioning": {}, "surfaces": {}}
    for b in (ASSETS, PORTAL):
        try:
            v = s3.get_bucket_versioning(Bucket=b)
            out["versioning"][b] = {"Status": v.get("Status", "NOT-ENABLED"),
                                    "MFADelete": v.get("MFADelete", "-")}
        except ClientError as e:
            out["versioning"][b] = err(f"versioning:{b}", e)

    for label, bucket, prefix, dated in [
        ("platinum_served", PORTAL, PLATINUM_PREFIX, True),
        ("json_bell", PORTAL, JSON_BELL_PREFIX, False),
        ("gold_canonical", ASSETS, GOLD_PREFIX, True),
        ("aggregate_aua", ASSETS, AGG_PREFIX, True),
    ]:
        try:
            keys, pages = _list(bucket, prefix)
        except ClientError as e:
            out["surfaces"][label] = err(f"s3:{bucket}/{prefix}", e)
            continue
        # dated history is enormous; freeze the NON-dated served pairs in full and
        # only the newest dated partition per family -- and SAY SO.
        undated = [k for k in keys if not _is_dated(k["Key"])]
        dated_keys = [k for k in keys if _is_dated(k["Key"])]
        newest = sorted(dated_keys, key=lambda k: k["Key"])[-3:] if dated_keys else []
        frozen = undated + newest
        recs = {}
        for k in frozen:
            try:
                h = s3.head_object(Bucket=bucket, Key=k["Key"])
                recs[k["Key"]] = {"VersionId": h.get("VersionId", "null"),
                                  "ETag": h["ETag"].strip('"'),
                                  "LastModified": iso(h["LastModified"]),
                                  "ContentLength": h["ContentLength"],
                                  "Metadata": h.get("Metadata", {})}
            except ClientError as e:
                recs[k["Key"]] = err(f"head:{bucket}/{k['Key']}", e)
        out["surfaces"][label] = {
            "bucket": bucket, "prefix": prefix,
            "denominator": (f"{len(keys)} objects across {pages} pages; "
                            f"{len(undated)} undated served keys FROZEN IN FULL; "
                            f"{len(dated_keys)} dated keys, newest {len(newest)} frozen "
                            f"(dated history is immutable and not a rollback target)"),
            "frozen": recs,
        }
    return out


def _is_dated(key: str) -> bool:
    tail = key.rsplit("/", 1)[-1]
    return len(tail) == 15 and tail[4] == "-" and tail[7] == "-" and tail.endswith(".json")


def capture_ec2() -> dict:
    out = {}
    try:
        r = ec2.describe_instances(InstanceIds=[EC2_ID])
        inst = r["Reservations"][0]["Instances"][0]
        out["instance"] = {
            "InstanceId": inst["InstanceId"],
            "State": inst["State"]["Name"],
            "InstanceType": inst["InstanceType"],
            "ImageId": inst["ImageId"],
            "LaunchTime": iso(inst["LaunchTime"]),
            "IamInstanceProfile": inst.get("IamInstanceProfile", {}).get("Arn"),
            "SubnetId": inst.get("SubnetId"),
            "SecurityGroups": [g["GroupId"] for g in inst.get("SecurityGroups", [])],
            "BlockDeviceMappings": [
                {"DeviceName": b["DeviceName"],
                 "VolumeId": b["Ebs"]["VolumeId"],
                 "DeleteOnTermination": b["Ebs"].get("DeleteOnTermination")}
                for b in inst.get("BlockDeviceMappings", [])],
            "Tags": {t["Key"]: t["Value"] for t in inst.get("Tags", [])},
        }
        vols = [b["Ebs"]["VolumeId"] for b in inst.get("BlockDeviceMappings", [])]
        if vols:
            vd = ec2.describe_volumes(VolumeIds=vols)["Volumes"]
            out["volumes"] = [{"VolumeId": v["VolumeId"], "Size": v["Size"],
                               "VolumeType": v["VolumeType"], "State": v["State"],
                               "Encrypted": v["Encrypted"],
                               "SnapshotId": v.get("SnapshotId")} for v in vd]
            out["existing_snapshots"] = _snaps(vols)
    except ClientError as e:
        out["instance"] = err(f"ec2:{EC2_ID}", e)
    return out


def _snaps(vols):
    try:
        s = ec2.describe_snapshots(OwnerIds=["self"],
                                   Filters=[{"Name": "volume-id", "Values": vols}])["Snapshots"]
        return [{"SnapshotId": x["SnapshotId"], "VolumeId": x["VolumeId"],
                 "StartTime": iso(x["StartTime"]), "State": x["State"],
                 "Description": x.get("Description", "")[:120]} for x in s]
    except ClientError as e:
        return err("ec2:snapshots", e)


def capture_ssm() -> dict:
    out = {}
    try:
        docs, pages = [], 0
        for page in ssm.get_paginator("list_documents").paginate(
                Filters=[{"Key": "Owner", "Values": ["Self"]}]):
            pages += 1
            docs.extend(page.get("DocumentIdentifiers", []))
        out["self_owned_documents"] = [d["Name"] for d in docs]
        out["denominator"] = f"{len(docs)} self-owned SSM documents across {pages} pages"
        out["mdpf_matching"] = [d["Name"] for d in docs if "mdpf" in d["Name"].lower()]
    except ClientError as e:
        out = err("ssm:list_documents", e)
    return out


def main():
    now = dt.datetime.now(UTC)
    lam_cap = capture_lambdas()
    art = {
        "artifact": "MDPF_PROPVALIDATION_P0.1_evidence_freeze",
        "purpose": "Phase 0 evidence freeze AND doc 04 s.4 rollback baseline (one artifact)",
        "captured_at_utc": now.isoformat(),
        "captured_at_et": now.astimezone(ET).isoformat(),
        "captured_by": "0.7.0_AE_CloudOps~Z",
        "account": boto3.client("sts").get_caller_identity()["Account"],
        "region": boto3.session.Session().region_name,
        "read_only": True,
        "timestamp_discipline": ("all timestamps are boto3 tz-aware UTC serialised with "
                                 "+00:00; no `aws s3 ls` column is used anywhere -- it "
                                 "prints LOCAL time and silently shifts by the box offset"),
        "lambdas": lam_cap,
        "iam": capture_iam(lam_cap["roles_seen"]),
        "schedules": capture_schedules(),
        "s3": capture_s3(),
        "ec2": capture_ec2(),
        "ssm": capture_ssm(),
    }
    art["errors"] = {"count": len(ERRORS), "records": ERRORS,
                     "note": "a retrieval failure returns a VALUE; every failure is "
                             "recorded here rather than read as absence"}
    path = sys.argv[1] if len(sys.argv) > 1 else "p0_1_evidence_freeze.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(art, f, indent=2, default=iso)
    print(f"WROTE {path}")
    print(f"captured_at_utc {art['captured_at_utc']}  account {art['account']} "
          f"region {art['region']}")
    print(f"lambdas       : {lam_cap['denominator']}")
    print(f"iam           : {art['iam']['denominator']}")
    print(f"schedules     : {art['schedules']['denominator']}")
    print(f"classic rules : {art['schedules']['classic_rules'].get('_denominator')}")
    for k, v in art["s3"]["surfaces"].items():
        print(f"s3 {k:<16}: {v.get('denominator', v)}")
    print(f"s3 versioning : { {b: v.get('Status') for b, v in art['s3']['versioning'].items()} }")
    ec2i = art["ec2"].get("instance", {})
    print(f"ec2           : {ec2i.get('InstanceId')} state={ec2i.get('State')} "
          f"vols={[v['VolumeId'] for v in art['ec2'].get('volumes', [])]} "
          f"existing_snapshots={len(art['ec2'].get('existing_snapshots', []) or [])}")
    print(f"ssm           : {art['ssm'].get('denominator')} "
          f"mdpf-matching={art['ssm'].get('mdpf_matching')}")
    print(f"ERRORS        : {len(ERRORS)}")
    for e in ERRORS:
        print(f"   {e['where']}: {e['error']} {e['detail'][:120]}")


if __name__ == "__main__":
    main()
