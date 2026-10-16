"""restore_san.py -- the ONE-KEY re-store of SAN_FP_Equity (mgmt_recent withheld) that goes with the AI-fill restore (AMGT_RESAPP AIFILL round 109).

  python restore_san.py pre                 read-only: the key's versions, current sha256, the prefix object count and the hold value -> pre_san.json
  python restore_san.py write --confirm     ONE put through lib.research.aifill.store.write_document, read back
  python restore_san.py rollback --confirm  copy-object of the pre-recorded current version onto the key

The body is restore/SAN_FP_Equity.json: the stored round-109 document with ONLY its mgmt_recent block replaced by the contract's NONE block
(reason text in the file) and every block re-stamped validation HELD. write refuses unless: the signed half's sha256 is the one set below and
the half file matches it; the file equals document_bytes(doc) plus one LF; the document passes the contract and the serve's rules; against the
object now stored only mgmt_recent differs (validation stamps aside); and the object's sha256 still equals the pre-record. A read-back
mismatch, an object count other than 95 or a changed hold is Branch 2: run rollback.
"""
import copy
import hashlib
import json
import os
import sys

import boto3

from lib.research.aifill import contract, store
from lib.research.api import scoped_amgt

HERE = os.path.dirname(os.path.abspath(__file__))
KEY = "SAN_FP_Equity"
FILE = os.path.join(HERE, "SAN_FP_Equity.json")
PRE = os.path.join(HERE, "pre_san.json")
LOG = os.path.join(HERE, "san_write_log.json")
COO_HALF = os.path.join(HERE, "..", "..", "..", "..", "ledger", "NEVER_WIDEN_ROUND109_AIFILL_HOLD_RESTORE_COO_HALF.md")
COO_HALF_SHA = "d4281bce35cb60614086030ac68ca1e88c6a21a29eaf896acc03e28053d40e05"  # the signed restore half's sha256, the one the CTO half binds
PREFIX = "amgt/harvest/gold/ai_fill/"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def hold_value():
    conf = boto3.client("lambda", region_name=store.REGION).get_function_configuration(FunctionName=os.environ["AIFILL_SERVED_FUNCTION"])
    return (conf.get("Environment", {}).get("Variables", {}) or {}).get("AMGT_AIFILL_ROOT")


def prefix_count(s3, bucket):
    count, token = 0, None
    while True:
        args = {"Bucket": bucket, "Prefix": PREFIX}
        if token:
            args["ContinuationToken"] = token
        reply = s3.list_objects_v2(**args)
        count += len(reply.get("Contents", []))
        if not reply.get("IsTruncated"):
            return count
        token = reply["NextContinuationToken"]


def stripped(doc):
    out = copy.deepcopy(doc)
    for block in out["blocks"].values():
        block.pop("validation", None)
    return out


def pre():
    s3 = boto3.client("s3", region_name=store.REGION)
    bucket, key = store._split(store.address_for(KEY))
    versions, token = [], {}
    while True:
        reply = s3.list_object_versions(Bucket=bucket, Prefix=key, **token)
        versions += [v for v in reply.get("Versions", []) if v["Key"] == key]
        if not reply.get("IsTruncated"):
            break
        token = {"KeyMarker": reply["NextKeyMarker"], "VersionIdMarker": reply["NextVersionIdMarker"]}
    current = [v for v in versions if v["IsLatest"]]
    if len(current) != 1:
        raise SystemExit("BLOCKED: %d latest versions" % len(current))
    body = s3.get_object(Bucket=bucket, Key=key, VersionId=current[0]["VersionId"])["Body"].read()
    record = {"bucket": bucket, "key": key, "current_version_id": current[0]["VersionId"], "current_sha256": sha(body),
              "current_bytes": len(body), "version_count": len(versions), "prefix_object_count": prefix_count(s3, bucket),
              "hold_AMGT_AIFILL_ROOT": hold_value()}
    with open(PRE, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(record, handle, indent=1, sort_keys=True)
        handle.write("\n")
    print("PRE-RECORD: %s version=%s sha256=%s versions=%d prefix_object_count=%d hold=%s" % (
        KEY, record["current_version_id"], record["current_sha256"][:16], record["version_count"], record["prefix_object_count"], record["hold_AMGT_AIFILL_ROOT"]))


def write():
    if COO_HALF_SHA is None:
        raise SystemExit("BLOCKED: COO_HALF_SHA is not set (the half is not signed and bound yet)")
    with open(COO_HALF, "rb") as handle:
        if sha(handle.read()) != COO_HALF_SHA:
            raise SystemExit("BLOCKED: the restore half's sha256 is not the one bound")
    with open(PRE, "r", encoding="utf-8") as handle:
        pre_record = json.load(handle)
    with open(FILE, "rb") as handle:
        raw = handle.read()
    doc = json.loads(raw.decode("utf-8"))
    if doc.get("security_key") != KEY or raw != store.document_bytes(doc) + b"\n":
        raise SystemExit("BLOCKED: the file is not the document for %s in the stored byte form" % KEY)
    if contract.validate_document(doc):
        raise SystemExit("BLOCKED: the document fails the contract")
    ok, why = scoped_amgt._validate_ai_fill_document(doc, KEY)
    if not ok:
        raise SystemExit("BLOCKED: the serve's rules refuse the document: %s" % why)
    s3 = boto3.client("s3", region_name=store.REGION)
    bucket, key = pre_record["bucket"], pre_record["key"]
    now = s3.get_object(Bucket=bucket, Key=key)
    stored_body = now["Body"].read()
    if sha(stored_body) != pre_record["current_sha256"]:
        raise SystemExit("BLOCKED: the stored object changed since the pre-record")
    stored = json.loads(stored_body.decode("utf-8"))
    a, b = stripped(stored), stripped(doc)
    differing = sorted(k for k in a["blocks"] if a["blocks"][k] != b["blocks"][k])
    if differing != ["mgmt_recent"] or any(a[k] != b[k] for k in a if k != "blocks"):
        raise SystemExit("BLOCKED: the document differs from the stored one in %s, not only mgmt_recent" % differing)
    receipt = store.write_document(doc, client=s3)
    reply = s3.get_object(Bucket=receipt["bucket"], Key=receipt["key"])
    body = reply["Body"].read()
    row = {"key": KEY, "put_sha256": receipt["sha256"], "readback_sha256": sha(body), "expect_sha256": sha(store.document_bytes(doc)),
           "new_version_id": reply.get("VersionId"), "prior_version_id": pre_record["current_version_id"]}
    row["ok"] = bool(row["put_sha256"] == row["readback_sha256"] == row["expect_sha256"] and row["new_version_id"] != row["prior_version_id"])
    count, hold = prefix_count(s3, bucket), hold_value()
    row["prefix_object_count"], row["hold_unchanged"] = count, hold == pre_record["hold_AMGT_AIFILL_ROOT"]
    with open(LOG, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(row, handle, indent=1, sort_keys=True)
        handle.write("\n")
    print("WRITE: ok=%s prefix_object_count=%d hold_unchanged=%s new_version=%s" % (row["ok"], count, row["hold_unchanged"], row["new_version_id"]))
    if not (row["ok"] and count == pre_record["prefix_object_count"] and row["hold_unchanged"]):
        print("BRANCH 2: run rollback")
        raise SystemExit(2)


def rollback():
    with open(PRE, "r", encoding="utf-8") as handle:
        pre_record = json.load(handle)
    s3 = boto3.client("s3", region_name=store.REGION)
    bucket, key = pre_record["bucket"], pre_record["key"]
    s3.copy_object(Bucket=bucket, Key=key, CopySource={"Bucket": bucket, "Key": key, "VersionId": pre_record["current_version_id"]},
                   ContentType=store.CONTENT_TYPE, MetadataDirective="REPLACE")
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    print("ROLLBACK: restored_sha_equal=%s" % (sha(body) == pre_record["current_sha256"]))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "pre":
        pre()
    elif mode in ("write", "rollback") and "--confirm" in sys.argv:
        {"write": write, "rollback": rollback}[mode]()
    else:
        raise SystemExit("usage: restore_san.py pre | write --confirm | rollback --confirm")
