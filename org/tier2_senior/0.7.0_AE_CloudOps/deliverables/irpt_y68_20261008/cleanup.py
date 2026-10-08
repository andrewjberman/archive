"""Exact-key Y68 cleanup. Identity and key values never enter output artifacts."""

import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

import boto3
from botocore.exceptions import ClientError

OUT = pathlib.Path(__file__).resolve().parent
PIN = "84916b911a:org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~159/Y68-1_admit_keys.json"
KEYS = json.loads(subprocess.check_output(["git", "show", PIN]))
DDB = [k for k in KEYS["admit_keys"] if k["kind"] == "ddb"]
S3 = [k for k in KEYS["admit_keys"] if k["kind"] == "s3"]
assert len(DDB) == 7 and len(S3) == 2
assert all(k["table"] == "irpt-requests" and k["tenant"] == "49financial" for k in DDB)
assert all(k["bucket"] == "opal-data-irpt" for k in S3)
ddb = boto3.client("dynamodb", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")


def opaque(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:16]


def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2) + "\n")


def dkey(k):
    return {n: {"S": k[n]} for n in ("tenant", "request_revision")}


def readrow(k):
    row = ddb.get_item(
        TableName=k["table"],
        Key=dkey(k),
        ConsistentRead=True,
        ProjectionExpression="#b,#o,#a",
        ExpressionAttributeNames={
            "#b": "body_sha256",
            "#o": "owner",
            "#a": "acting_principal_id",
        },
    ).get("Item")
    # A projected empty map can still be an existing row; Item presence decides.
    return {
        "exists": row is not None,
        "hashes": {n: opaque(v) for n, v in (row or {}).items()},
    }


def versions(k):
    rows = []
    for page in s3.get_paginator("list_object_versions").paginate(
        Bucket=k["bucket"], Prefix=k["key"]
    ):
        for field in ("Versions", "DeleteMarkers"):
            rows.extend(
                {
                    "version_id": v["VersionId"],
                    "delete_marker": field == "DeleteMarkers",
                }
                for v in page.get(field, [])
                if v["Key"] == k["key"]
            )
    return rows


def head(k, version):
    try:
        s3.head_object(Bucket=k["bucket"], Key=k["key"], VersionId=version)
        return "EXISTS"
    except ClientError as exc:
        status = exc.response["ResponseMetadata"]["HTTPStatusCode"]
        if status in (404, 405):
            return "NOT_FOUND" if status == 404 else "DELETE_MARKER"
        raise RuntimeError("Head failed HTTP " + str(status)) from None


def preflight():
    rows = [{"key_ref": opaque(k), "kind": "ddb", "before": readrow(k)} for k in DDB]
    for k in S3:
        live = versions(k)
        assert set(KEYS["s3_versions"][k["key"]]) <= {v["version_id"] for v in live}, (
            "Pinned version absent: STOP"
        )
        for v in live:
            v["head_before"] = head(k, v["version_id"])
            v["additional_to_file"] = (
                v["version_id"] not in KEYS["s3_versions"][k["key"]]
            )
        rows.append({"key_ref": opaque(k), "kind": "s3", "versions": live})
    save("before.json", rows)
    print(
        json.dumps(
            {
                "ddb_keys": 7,
                "s3_keys": 2,
                "ddb_existing": sum(
                    r["before"]["exists"] for r in rows if r["kind"] == "ddb"
                ),
                "versions": sum(len(r["versions"]) for r in rows if r["kind"] == "s3"),
            }
        )
    )


def apply():
    assert not (OUT / "started.json").exists(), "Already started; never blindly repeat"
    save(
        "started.json",
        {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat()},
    )
    result = {"results": [], "s3_versions": [], "sweep_extra_count": None}
    for k in DDB:
        before = readrow(k)
        ddb.delete_item(TableName=k["table"], Key=dkey(k))
        after = readrow(k)
        assert not after["exists"], "DDB after read exists"
        result["results"].append(
            {
                "key_ref": opaque(k),
                "before": "EXISTS" if before["exists"] else "NOT_FOUND",
                "before_hashes": before["hashes"],
                "after_delete": "NOT_FOUND",
            }
        )
        save("Y68-1_laptop_cleanup_result.json", result)
    finish()


def finish():
    saved = json.loads((OUT / "before.json").read_text())
    result = json.loads((OUT / "Y68-1_laptop_cleanup_result.json").read_text())
    assert len(result["results"]) == 7 and not result["s3_versions"], (
        "Unexpected checkpoint"
    )
    assert all(not readrow(k)["exists"] for k in DDB), "DDB key reappeared"
    query = dict(
        TableName="irpt-requests",
        KeyConditionExpression="#t=:t",
        ExpressionAttributeNames={
            "#t": "tenant",
            "#r": "request_revision",
            "#u": "upload_id",
            "#i": "input_id",
        },
        ExpressionAttributeValues={
            ":t": {"S": "49financial"},
        },
        ProjectionExpression="#t,#r,#u,#i",
        ConsistentRead=True,
    )
    found = []
    for page in ddb.get_paginator("query").paginate(**query):
        for row in page.get("Items", []):
            rev = row.get("request_revision", {}).get("S", "")
            if (
                KEYS["upload_id"] in rev
                or KEYS["input_id"] in rev
                or row.get("upload_id", {}).get("S") == KEYS["upload_id"]
                or row.get("input_id", {}).get("S") == KEYS["input_id"]
            ):
                found.append({n: row[n] for n in ("tenant", "request_revision")})
    known = {json.dumps(dkey(k), sort_keys=True) for k in DDB}
    result["sweep_extra_count"] = sum(
        json.dumps(k, sort_keys=True) not in known for k in found
    )
    for k in S3:
        current = versions(k)
        saved_versions = next(r["versions"] for r in saved if r["key_ref"] == opaque(k))
        assert {v["version_id"] for v in saved_versions} <= {
            v["version_id"] for v in current
        }, "Saved version moved: STOP"
        for v in current:
            before = head(k, v["version_id"])
            s3.delete_object(
                Bucket=k["bucket"], Key=k["key"], VersionId=v["version_id"]
            )
            after = head(k, v["version_id"])
            assert after == "NOT_FOUND", "Version still exists"
            result["s3_versions"].append(
                {
                    "key_ref": opaque(k),
                    "version_id": v["version_id"],
                    "before": before,
                    "after_delete": after,
                    "additional_to_file": v["version_id"]
                    not in KEYS["s3_versions"][k["key"]],
                }
            )
            save("Y68-1_laptop_cleanup_result.json", result)
        assert not versions(k), "Exact-key versions remain"
        result["results"].append(
            {
                "key_ref": opaque(k),
                "before": "EXISTS" if current else "NOT_FOUND",
                "after_delete": "NOT_FOUND",
            }
        )
    result["verified_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result["versions_left"] = 0
    save("Y68-1_laptop_cleanup_result.json", result)
    print(
        json.dumps(
            {
                "results": len(result["results"]),
                "ddb_not_found": 7,
                "s3_keys_empty": 2,
                "deleted_versions": len(result["s3_versions"]),
                "sweep_extra_count": result["sweep_extra_count"],
                "versions_left": 0,
                "utc": result["verified_utc"],
            }
        )
    )


if __name__ == "__main__":
    try:
        {"before": preflight, "apply": apply, "finish": finish}[sys.argv[1]]()
    except Exception as exc:
        print(
            "STOP: "
            + type(exc).__name__
            + (
                " "
                + exc.operation_name
                + " "
                + exc.response.get("Error", {}).get("Code", "")
                if isinstance(exc, ClientError)
                else ""
            )
            + "; raw exception suppressed to protect identity fields"
        )
        raise SystemExit(1) from None
