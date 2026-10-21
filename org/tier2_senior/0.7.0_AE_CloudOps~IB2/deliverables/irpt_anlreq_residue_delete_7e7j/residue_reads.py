"""IRPT_ANLREQ TO-RUN-RESIDUE-DELETE-7E7J reads (applier 0.7.0_AE_CloudOps~IB2): READ ONLY. Nothing is deleted or written here.

  python residue_reads.py r0       R0: the 29 manifest versions PRESENT (head-object by VersionId, lock fields), the audit key's versions, the three roles absent, the bucket
                                   facts, the Deny, the control object, Andrew's retained objects, and the retention counts (a) and (b)
  python residue_reads.py after    the same Deny, control and Andrew reads again, the 29 versions ABSENT and the manifest keys' versions empty, the roles absent

Key names are printed for the control object and Andrew's retained objects only (the order asks for names); no object body and no row value is read.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer

HERE = Path(__file__).resolve().parent
REGION = "us-east-1"
BUCKET = "opal-data-irpt"
ROOT = HERE.parents[4]
MANIFEST = ROOT / Path("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/synthetic_residue_delete_list_supplement_runs7e_7j_20261021.json")
ROLES = ["irpt-residue-delete-0-role", "irpt-residue-delete-1-role", "irpt-residue-delete-2-role"]
ANDREW_TICKET = "TCK-20261020-b1d61f80"
DENY_SID = "DenyS3DeletesOnProductionData"
s3 = boto3.client("s3", region_name=REGION)
iam = boto3.client("iam", region_name=REGION)
ddb = boto3.client("dynamodb", region_name=REGION)
lines = []


def say(x):
    lines.append(x)
    print(x)


def manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["objects"]


def head(key, vid=None):
    kw = {"Bucket": BUCKET, "Key": key}
    if vid:
        kw["VersionId"] = vid
    try:
        r = s3.head_object(**kw)
        return "PRESENT", r
    except ClientError as e:
        return "ABSENT:%s" % e.response["Error"]["Code"], None


def versions_of(key):
    """One exact key: every version and delete marker (a single-key list)."""
    out = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=key):
        out += [("V", v["VersionId"]) for v in pg.get("Versions", []) if v["Key"] == key]
        out += [("M", m["VersionId"]) for m in pg.get("DeleteMarkers", []) if m["Key"] == key]
    return out


def deny_present():
    pols = [p for p in iam.get_paginator("list_policies").paginate(Scope="Local") for p in p["Policies"] if p["PolicyName"] == "cloudops-dell-agent-deploy-policy"]
    if len(pols) != 1:
        return "policy count %d" % len(pols)
    doc = iam.get_policy_version(PolicyArn=pols[0]["Arn"], VersionId=pols[0]["DefaultVersionId"])["PolicyVersion"]["Document"]
    st = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    return "present" if any(s.get("Sid") == DENY_SID and s.get("Effect") == "Deny" for s in st) else "ABSENT"


def roles_state():
    out = []
    for r in ROLES:
        try:
            iam.get_role(RoleName=r)
            out.append("%s EXISTS" % r)
        except iam.exceptions.NoSuchEntityException:
            out.append("%s NoSuchEntity" % r)
    return out


def andrew_objects():
    """The retained objects of Andrew's ticket, found by read-only reads of the request index rows that name the ticket (ids and blob pointers); none is a value."""
    des = TypeDeserializer()
    rows = []
    for pg in ddb.get_paginator("scan").paginate(TableName="irpt-requests"):
        for it in pg["Items"]:
            rows.append({k: des.deserialize(v) for k, v in it.items()})
    ids = set()
    for r in rows:
        s = json.dumps(r, default=str)
        if ANDREW_TICKET in s:
            ids.update(re.findall(r"(REQ-[0-9a-f]{24}|UP-[0-9a-f]{64}|portfolio_[0-9a-f]{64}|ART-[0-9a-f]{64})", s))
    # one more hop: rows that carry any of those ids name the artifacts and their blobs
    for _ in range(2):
        for r in rows:
            s = json.dumps(r, default=str)
            if any(i in s for i in list(ids)):
                ids.update(re.findall(r"(ART-[0-9a-f]{64})", s))
    blobs = set()
    for r in rows:
        s = json.dumps(r, default=str)
        if any(i in s for i in ids):
            b = r.get("blob") if isinstance(r.get("blob"), dict) else None
            if b and b.get("bucket") == BUCKET and b.get("key"):
                blobs.add(b["key"])
    return sorted(blobs), len(ids), len(rows)


def retention_counts(man):
    des = TypeDeserializer()
    fam, byart = 0, {}
    arts = sorted({re.search(r"ART-[0-9a-f]{64}", o["key"]).group(0) for o in man if o["tier"] == "state" and re.search(r"ART-[0-9a-f]{64}", o["key"])})
    for pg in ddb.get_paginator("scan").paginate(TableName="irpt-requests"):
        for it in pg["Items"]:
            r = {k: des.deserialize(v) for k, v in it.items()}
            if r.get("family") == "ANALYSIS_AUDIT":
                fam += 1
            lid = r.get("logical_id")
            if isinstance(lid, str):
                for a in arts:
                    if a in lid:
                        k = (r.get("family"), r.get("state"))
                        byart[k] = byart.get(k, 0) + 1
    return fam, byart, len(arts)


def r0():
    man = manifest()
    present, locks = 0, 0
    for o in man:
        st, r = head(o["key"], o["version_id"])
        if st == "PRESENT":
            present += 1
            if r.get("ObjectLockMode") or r.get("ObjectLockLegalHoldStatus") or r.get("ObjectLockRetainUntilDate"):
                locks += 1
    say("R0 manifest %d entries; head-object by VersionId: PRESENT=%d ABSENT=%d; entries with ObjectLockMode/LegalHold/retention: %d" % (len(man), present, len(man) - present, locks))
    audit_keys = sorted({o["key"] for o in man if o["family_dir"] == "analysis_audit"})
    for k in audit_keys:
        vs = versions_of(k)
        mine = sorted(o["version_id"] for o in man if o["key"] == k)
        say("R0 audit key (one exact key): %d version/marker rows: %s; the two named versions both present: %s; markers: %d" % (len(vs), [(t, v[:8]) for t, v in vs], sorted(v for t, v in vs if t == "V") == mine, sum(1 for t, _ in vs if t == "M")))
    say("R0 roles: %s" % roles_state())
    try:
        pol = json.loads(s3.get_bucket_policy(Bucket=BUCKET)["Policy"])
        say("R0 bucket policy statement ids: %s" % [s.get("Sid") for s in pol["Statement"]])
    except ClientError as e:
        say("R0 bucket policy read: %s" % e.response["Error"]["Code"])
    say("R0 versioning: %s" % s3.get_bucket_versioning(Bucket=BUCKET).get("Status"))
    try:
        s3.get_object_lock_configuration(Bucket=BUCKET)
        say("R0 object-lock configuration: PRESENT -> STOP")
    except ClientError as e:
        say("R0 object-lock configuration: %s" % e.response["Error"]["Code"])
    say("R0 Deny %s in cloudops-dell-agent-deploy-policy default version: %s" % (DENY_SID, deny_present()))
    ctl = "irpt/49financial/state/ycharts_opal_reports/ART-6bae814a58538a4e46cdfa76dbc95228b79ee0caf16fb8eb220de46694dbeda6/22a754c7965a4b2a679765de6ac468766f2a49459a9db1310b7133f8b59df17b.pdf"
    st, _ = head(ctl)
    if st != "PRESENT":
        # fall back to any existing current object under the state prefix that is not in the manifest
        mk = {o["key"] for o in man}
        for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="irpt/49financial/state/ycharts_opal_reports/", PaginationConfig={"MaxItems": 2000}):
            for c in pg.get("Contents", []):
                if c["Key"] not in mk:
                    ctl, st = c["Key"], "PRESENT"
                    break
            if st == "PRESENT":
                break
    say("R0 control object (not in the manifest) %s: %s" % (ctl, st))
    keys, nids, nrows = andrew_objects()
    stat = {k: head(k)[0] for k in keys}
    say("R0 Andrew's TCK-20261020-b1d61f80 retained objects found by read-only reads of the request index (%d rows scanned, %d ids): %d keys; PRESENT=%d" % (nrows, nids, len(keys), sum(1 for v in stat.values() if v == "PRESENT")))
    for k in keys:
        say("R0 andrew object %s %s" % (k, stat[k]))
    fam, byart, narts = retention_counts(man)
    say("R0 retention (a) rows with family ANALYSIS_AUDIT: %d" % fam)
    say("R0 retention (b) rows whose logical_id contains one of the %d manifest state ART ids, by (family, state): %s" % (narts, sorted(byart.items(), key=str)))
    (HERE / "r0_state.json").write_text(json.dumps({"control": ctl, "andrew": keys, "audit_keys": audit_keys}, indent=1) + "\n", encoding="ascii", newline="\n")


def after():
    man = manifest()
    st = json.loads((HERE / "r0_state.json").read_text(encoding="ascii"))
    absent = sum(1 for o in man if head(o["key"], o["version_id"])[0].startswith("ABSENT:404") or head(o["key"], o["version_id"])[0].startswith("ABSENT:NoSuchVersion"))
    say("AFTER manifest versions read ABSENT (404 only): %d of %d" % (absent, len(man)))
    empty = sum(1 for k in sorted({o["key"] for o in man}) if not versions_of(k))
    say("AFTER manifest keys whose versions and markers list EMPTY: %d of %d" % (empty, len({o["key"] for o in man})))
    for k in st["audit_keys"]:
        say("AFTER audit key versions: %s" % versions_of(k))
    say("AFTER roles: %s" % roles_state())
    say("AFTER Deny %s: %s" % (DENY_SID, deny_present()))
    say("AFTER control object %s: %s" % (st["control"], head(st["control"])[0]))
    a = {k: head(k)[0] for k in st["andrew"]}
    say("AFTER Andrew's retained objects: %d keys; PRESENT=%d" % (len(a), sum(1 for v in a.values() if v == "PRESENT")))


if __name__ == "__main__":
    {"r0": r0, "after": after}[sys.argv[1]]()
    (HERE / ("reads_%s.txt" % sys.argv[1])).write_text("\n".join(lines) + "\n", encoding="ascii", errors="replace", newline="\n")
