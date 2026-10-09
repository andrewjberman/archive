import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


ROOT = Path(__file__).resolve().parents[5]
PIN = "14ddee6c67"
KEYS_PATH = (
    "org/tier2_senior/0.7.0_AE_CloudOps~DELL2/"
    "deliverables/irpt_y75/Y75-1_admit_keys.json"
)
RESULT_PATH = ROOT / (
    "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
    "2.0.0_SA_COO~Y2/r75/Y75-1_laptop_cleanup_result.json"
)


def load_pinned_keys():
    raw = subprocess.check_output(["git", "show", f"{PIN}:{KEYS_PATH}"], cwd=ROOT)
    return json.loads(raw)


def ref(*parts):
    material = "|".join(parts).encode("utf-8")
    return hashlib.sha256(material).hexdigest()[:12]


def email_count(path):
    text = path.read_text(encoding="utf-8")
    return len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text))


def write_result(result):
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    count = email_count(RESULT_PATH)
    if count:
        RESULT_PATH.unlink(missing_ok=True)
        raise RuntimeError("written email-shaped count was nonzero")
    return count


def object_sha256(s3, bucket, key, version_id):
    response = s3.get_object(Bucket=bucket, Key=key, VersionId=version_id)
    body = response["Body"]
    digest = hashlib.sha256()
    try:
        while True:
            chunk = body.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    finally:
        body.close()
    return digest.hexdigest()


def exact_versions(s3, bucket, key):
    versions = []
    paginator = s3.get_paginator("list_object_versions")
    for page in paginator.paginate(Bucket=bucket, Prefix=key):
        for item in page.get("Versions", []):
            if item["Key"] == key:
                versions.append(("VERSION", item["VersionId"]))
        for item in page.get("DeleteMarkers", []):
            if item["Key"] == key:
                versions.append(("DELETE_MARKER", item["VersionId"]))
    return versions


def head_status(s3, bucket, key, version_id):
    try:
        s3.head_object(Bucket=bucket, Key=key, VersionId=version_id)
        return "EXISTS"
    except ClientError as exc:
        code = str(exc.response.get("Error", {}).get("Code", ""))
        status = exc.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if code in {"404", "NoSuchKey", "NoSuchVersion", "NotFound"} or status == 404:
            return "NOT_FOUND"
        raise


def query_sweep_extras(table, tenant, named_revisions, tokens):
    extras = []
    kwargs = {
        "KeyConditionExpression": Key("tenant").eq(tenant),
        "ProjectionExpression": "#rr",
        "ExpressionAttributeNames": {"#rr": "request_revision"},
        "ConsistentRead": True,
    }
    while True:
        page = table.query(**kwargs)
        for item in page.get("Items", []):
            revision = item.get("request_revision", "")
            if revision not in named_revisions and any(token in revision for token in tokens):
                extras.append(revision)
        if "LastEvaluatedKey" not in page:
            break
        kwargs["ExclusiveStartKey"] = page["LastEvaluatedKey"]
    return extras


def validate_shape(keys):
    ddb = [entry for entry in keys["admit_keys"] if entry.get("kind") == "ddb"]
    s3 = [entry for entry in keys["admit_keys"] if entry.get("kind") == "s3"]
    tables = sorted({entry["table"] for entry in ddb})
    buckets = sorted({entry["bucket"] for entry in s3})
    if len(ddb) != 7 or len(s3) != 2 or tables != ["irpt-requests"] or buckets != ["opal-data-irpt"]:
        raise RuntimeError("STOP: pinned key denominator is not 7 DDB / 2 S3 on the approved surfaces")
    return ddb, s3, tables[0], buckets[0]


def execute(keys):
    ddb_entries, s3_entries, table_name, bucket_name = validate_shape(keys)
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(table_name)
    s3 = boto3.client("s3", region_name="us-east-1")

    upload_entry = next(
        entry for entry in ddb_entries if entry["request_revision"].startswith("UPLOAD#")
    )
    upload_item = table.get_item(
        Key={
            "tenant": upload_entry["tenant"],
            "request_revision": upload_entry["request_revision"],
        },
        ConsistentRead=True,
    ).get("Item")

    original = next(entry for entry in s3_entries if "/original_holdings/" in entry["key"])
    pinned_versions = keys["s3_versions"].get(original["key"], [])
    body_match = False
    if len(pinned_versions) == 1:
        body_match = (
            object_sha256(s3, original["bucket"], original["key"], pinned_versions[0])
            == keys["body_sha256"]
        )

    readback = {
        "body_sha256_match": body_match,
        "owner_is_advisor": bool(upload_item) and upload_item.get("owner") == keys["advisor"],
        "acting_principal_is_filer": bool(upload_item)
        and upload_item.get("acting_principal_id") == keys["test_filer_email"],
    }
    if not all(readback.values()):
        write_result({"admit_readback": readback, "results": [], "sweep_extra": 0})
        raise SystemExit(2)

    results = []
    named_revisions = {entry["request_revision"] for entry in ddb_entries}
    for entry in ddb_entries:
        key = {"tenant": entry["tenant"], "request_revision": entry["request_revision"]}
        before = "EXISTS" if table.get_item(Key=key, ConsistentRead=True).get("Item") else "NOT_FOUND"
        table.delete_item(Key=key)
        after = "EXISTS" if table.get_item(Key=key, ConsistentRead=True).get("Item") else "NOT_FOUND"
        results.append(
            {
                "key_ref": ref(entry["table"], entry["tenant"], entry["request_revision"]),
                "before": before,
                "after_delete": after,
            }
        )
        if after != "NOT_FOUND":
            raise RuntimeError("a named DDB key remained after delete")

    tokens = {keys["upload_id"], keys["input_id"]}
    for revision in named_revisions:
        tokens.update(re.findall(r"(?:ART|RET)-[0-9a-f]+", revision))
    sweep_extras = query_sweep_extras(
        table, keys["admit_tenant"], named_revisions, sorted(tokens)
    )

    for entry in s3_entries:
        key_versions = exact_versions(s3, entry["bucket"], entry["key"])
        for version_kind, version_id in key_versions:
            before = (
                head_status(s3, entry["bucket"], entry["key"], version_id)
                if version_kind == "VERSION"
                else "DELETE_MARKER"
            )
            s3.delete_object(
                Bucket=entry["bucket"], Key=entry["key"], VersionId=version_id
            )
            after = head_status(s3, entry["bucket"], entry["key"], version_id)
            results.append(
                {
                    "key_ref": f"{ref(entry['bucket'], entry['key'])}@{version_id}",
                    "before": before,
                    "after_delete": after,
                }
            )
            if after != "NOT_FOUND":
                raise RuntimeError("a named S3 version remained after delete")
        if exact_versions(s3, entry["bucket"], entry["key"]):
            raise RuntimeError("an exact approved S3 key still has versions or delete markers")

    result = {
        "admit_readback": readback,
        "results": results,
        "sweep_extra": len(sweep_extras),
    }
    count = write_result(result)
    print(
        json.dumps(
            {
                "ddb_named": len(ddb_entries),
                "s3_named": len(s3_entries),
                "table": table_name,
                "bucket": bucket_name,
                "admit_readback": readback,
                "result_rows": len(results),
                "sweep_extra": len(sweep_extras),
                "email_shaped_count_written": count,
            },
            sort_keys=True,
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    if args.execute == args.preflight:
        parser.error("choose exactly one of --preflight or --execute")

    keys = load_pinned_keys()
    ddb, s3, table, bucket = validate_shape(keys)
    if args.preflight:
        print(json.dumps({"ddb_named": len(ddb), "s3_named": len(s3), "table": table, "bucket": bucket}, sort_keys=True))
        return
    execute(keys)


if __name__ == "__main__":
    main()
