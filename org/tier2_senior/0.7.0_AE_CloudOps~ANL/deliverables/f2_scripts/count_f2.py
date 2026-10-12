"""count_f2.py -- READ-ONLY count for crossbox CALL XB-20261012T024226Z-0dce (IRPT_ANLREQ arm F2).

Reads: one consistent Scan of the requests table for analysis# items; GetItem of INPUT#, UPLOAD# and ARTIFACT# rows; GetObject of
a composition document (by the version its ARTIFACT# row records), only for a request whose owner address is on a reserved domain.
It makes no write call. Output: ONE JSON object of counts. No request id, address, name, input/upload id or file name is printed.
"""
import hashlib
import json
import re
import sys
import datetime
from collections import Counter

import boto3

TABLE, REGION = "irpt-requests", "us-east-1"
RESERVED_SUFFIX = (".invalid", ".test", ".example")
RESERVED_EXACT = ("example.com", "example.org", "example.net")
OWNER_ADDRESS_MEMBER, OWNER_CLASS_MEMBER = "principal_id", "principal_class"
CODE_TEXT = re.compile(r"[A-Za-z0-9_.:-]{1,48}\Z")

ddb = boto3.client("dynamodb", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)


def code_of(exc):
    code = getattr(exc, "response", {}).get("Error", {}).get("Code") if isinstance(getattr(exc, "response", None), dict) else None
    return re.sub(r"[^A-Za-z0-9_.:-]", "_", str(code or type(exc).__name__))[:48]


def plain(value):
    if isinstance(value, dict) and len(value) == 1:
        (kind, inner), = value.items()
        if kind == "S":
            return inner
        if kind == "N":
            number = float(inner)
            return int(number) if number == int(number) else number
        if kind == "BOOL":
            return bool(inner)
        if kind == "NULL":
            return None
        if kind == "M":
            return {k: plain(v) for k, v in inner.items()}
        if kind == "L":
            return [plain(v) for v in inner]
    return value


def get_row(tenant, revision):
    got = ddb.get_item(TableName=TABLE, ConsistentRead=True, Key={"tenant": {"S": tenant}, "request_revision": {"S": revision}})
    return {k: plain(v) for k, v in got["Item"].items()} if got.get("Item") else None


def is_reserved(address):
    domain = address.rsplit("@", 1)[1].strip().lower()
    return domain in RESERVED_EXACT or domain.endswith(RESERVED_SUFFIX)


def composition_input_ids(tenant, artifact_id):
    """The input ids a request's composition names (kept in memory only). Raises (code,) on any unreadable step."""
    row = get_row(tenant, "ARTIFACT#" + str(artifact_id))
    if row is None:
        raise LookupError("ARTIFACT_ROW_MISSING")
    where, ref = row.get("blob"), row.get("ref")
    if not isinstance(where, dict) or not isinstance(ref, dict) or not where.get("version_id") or where["version_id"] == "null":
        raise LookupError("ARTIFACT_ROW_SHAPE")
    body = s3.get_object(Bucket=where["bucket"], Key=where["key"], VersionId=where["version_id"])["Body"]
    try:
        data = body.read()
    finally:
        body.close()
    if hashlib.sha256(data).hexdigest() != ref.get("sha256"):
        raise LookupError("DIGEST_MISMATCH")
    doc = json.loads(data)
    ids = {(doc.get("browser") or {}).get("input_id"), (((doc.get("resolved") or {}).get("input_ref")) or {}).get("input_id")}
    return {i for i in ids if isinstance(i, str) and i}


def original_retained(tenant, input_id):
    """True when the input's upload names an original artifact whose ARTIFACT# row exists; else a not_resolved reason."""
    inp = get_row(tenant, "INPUT#" + input_id)
    if inp is None:
        return "INPUT_ROW_MISSING"
    upload = get_row(tenant, "UPLOAD#" + str(inp.get("upload_id")))
    if upload is None:
        return "UPLOAD_ROW_MISSING"
    ref = upload.get("artifact_ref")
    art = ref.get("artifact_id") if isinstance(ref, dict) else None
    if not art:
        return "UPLOAD_NO_ORIGINAL_REF"
    return True if get_row(tenant, "ARTIFACT#" + str(art)) is not None else "ORIGINAL_ARTIFACT_ROW_MISSING"


def main():
    unreadable, tenants, not_resolved = Counter(), {}, Counter()
    scanned = accepted = 0
    start = None
    while True:
        args = {"TableName": TABLE, "ConsistentRead": True, "FilterExpression": "begins_with(#r, :p)",
                "ExpressionAttributeNames": {"#r": "request_revision", "#t": "tenant", "#c": "record"},
                "ExpressionAttributeValues": {":p": {"S": "analysis#"}}, "ProjectionExpression": "#t, #r, #c"}
        if start:
            args["ExclusiveStartKey"] = start
        try:
            page = ddb.scan(**args)
        except Exception as exc:
            print("SCAN_FAILED " + code_of(exc), file=sys.stderr)
            return 3
        scanned += page.get("ScannedCount", 0)
        for item in page.get("Items", []):
            tenant = item["tenant"]["S"]
            t = tenants.setdefault(tenant, {"reserved_domain": 0, "not_reserved": 0, "no_address_member": 0,
                                            "by_owner_class": Counter(), "with_retained_original": 0, "not_resolved": 0})
            accepted += 1
            try:
                rec = json.loads(item["record"]["S"])
                owner = rec["owner"]
                address = owner.get(OWNER_ADDRESS_MEMBER)
            except Exception:
                unreadable["RECORD_SHAPE"] += 1
                continue
            if not isinstance(address, str) or "@" not in address:
                t["no_address_member"] += 1
                continue
            if not is_reserved(address):
                t["not_reserved"] += 1
                continue
            t["reserved_domain"] += 1
            cls = owner.get(OWNER_CLASS_MEMBER)
            t["by_owner_class"][cls if isinstance(cls, str) and CODE_TEXT.match(cls) else "no class member"] += 1
            try:
                ids = composition_input_ids(tenant, (rec.get("composition_ref") or {}).get("artifact_id"))
                verdicts = {original_retained(tenant, i) for i in ids}
            except LookupError as exc:
                verdicts, why = set(), str(exc)
            except Exception as exc:
                verdicts, why = set(), code_of(exc)
            else:
                why = "NO_INPUT_ID_IN_COMPOSITION"
            if True in verdicts:
                t["with_retained_original"] += 1
            else:
                t["not_resolved"] += 1
                not_resolved[sorted(v for v in verdicts if v is not True)[0] if verdicts else why] += 1
        start = page.get("LastEvaluatedKey")
        if not start:
            break
    out = {"read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "items_scanned": scanned,
           "accepted_read": accepted, "tenants_seen": len(tenants), "unreadable": dict(unreadable),
           "by_tenant": {k: {m: (dict(sorted(v.items())) if isinstance(v, Counter) else v) for m, v in t.items()}
                         for k, t in sorted(tenants.items())},
           "not_resolved_by_reason": dict(sorted(not_resolved.items()))}
    line = json.dumps(out, sort_keys=True)
    if "@" in line:
        print("REFUSED: output carries an at-sign", file=sys.stderr)
        return 4
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
