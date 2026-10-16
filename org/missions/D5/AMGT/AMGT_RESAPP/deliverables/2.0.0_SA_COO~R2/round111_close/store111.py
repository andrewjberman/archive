"""store111.py -- the AI fill store write of ROUND 111, ONLY the documents that changed (live95/changed.json), under its own never-widen pair (AMGT_RESAPP AIFILL), in three modes.
(A copy of round110_close/store110.py pointed at round111_close/live95 and limited to the names in changed.json; the pair it binds is
ledger/NEVER_WIDEN_ROUND111_AIFILL_37_KEY_STORE_WRITE_{COO,CTO}_HALF.md.)

  python store111.py pre                 read-only: pre-record of every key's versions and current sha256, the prefix
                                        object count and the hold value -> store_write/pre_versions.json
  python store111.py write --confirm     the 95 writes through lib.research.aifill.store.write_document, each read back
  python store111.py rollback --confirm  copy-object of each written key's pre-recorded prior VersionId onto the key

The set is the 95 files in live95/stamped (pinned by live95/stamped_sha256.json). The address of each document comes
from the document's own security_key through store.address_for, never from a file name. write refuses unless the
pre-record exists for all 95 keys, the COO half's sha256 equals the one the CTO half signed, the manifest matches the
stamped files, and every stamped file equals document_bytes(doc) plus one trailing newline (the form store.write_document
stores). A read-back mismatch, an object count other than 95 or a changed hold stops the run (Branch 2).
"""
import hashlib
import json
import os
import sys

import boto3

from lib.research.aifill import store

HERE = os.path.dirname(os.path.abspath(__file__))
STAMPED = os.path.join(HERE, "live95", "stamped")
MANIFEST = os.path.join(HERE, "live95", "stamped_sha256_changed.json")
CHANGED = os.path.join(HERE, "live95", "changed.json")
OUT = os.path.join(HERE, "store_write")
PRE = os.path.join(OUT, "pre_versions.json")
LOG = os.path.join(OUT, "write_log.jsonl")
COO_HALF = os.path.join(HERE, "..", "..", "..", "ledger", "NEVER_WIDEN_ROUND111_AIFILL_37_KEY_STORE_WRITE_COO_HALF.md")
COO_HALF_SHA = "8b1e8562bcf4479f3bd3b5a703e55665e1006c3a328761ad34494cc852ff48d5"  # the signed half's sha256, the one the CTO half binds
PREFIX = "amgt/harvest/gold/ai_fill/"
with open(CHANGED, "r", encoding="utf-8") as _handle:
    CHANGED_FILES = sorted(v["file"] for v in json.load(_handle).values())
EXPECTED_N = len(CHANGED_FILES)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_set():
    docs = {}
    for name in CHANGED_FILES:
        with open(os.path.join(STAMPED, name), "rb") as handle:
            raw = handle.read()
        doc = json.loads(raw.decode("utf-8"))
        docs[doc["security_key"]] = (name, raw, doc)
    if len(docs) != EXPECTED_N:
        raise SystemExit("BLOCKED: %d stamped documents, expected %d" % (len(docs), EXPECTED_N))
    return docs


def hold_value():
    function = os.environ["AIFILL_SERVED_FUNCTION"]
    conf = boto3.client("lambda", region_name=store.REGION).get_function_configuration(FunctionName=function)
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


def split_of(key):
    return store._split(store.address_for(key))


def pre():
    docs = load_set()
    s3 = boto3.client("s3", region_name=store.REGION)
    record = {"keys": {}}
    bucket = None
    for key in sorted(docs):
        bucket, objkey = split_of(key)
        versions = []
        token = {}
        while True:
            reply = s3.list_object_versions(Bucket=bucket, Prefix=objkey, **token)
            versions += [v for v in reply.get("Versions", []) if v["Key"] == objkey]
            if not reply.get("IsTruncated"):
                break
            token = {"KeyMarker": reply["NextKeyMarker"], "VersionIdMarker": reply["NextVersionIdMarker"]}
        current = [v for v in versions if v["IsLatest"]]
        if len(current) != 1:
            raise SystemExit("BLOCKED: %s has %d latest versions" % (key, len(current)))
        body = s3.get_object(Bucket=bucket, Key=objkey, VersionId=current[0]["VersionId"])["Body"].read()
        record["keys"][key] = {
            "bucket": bucket, "key": objkey, "current_version_id": current[0]["VersionId"],
            "current_last_modified": current[0]["LastModified"].isoformat(), "current_sha256": sha(body),
            "current_bytes": len(body), "version_count": len(versions),
            "all_version_ids": [v["VersionId"] for v in versions],
        }
    record["prefix_object_count"] = prefix_count(s3, bucket)
    record["hold_AMGT_AIFILL_ROOT"] = hold_value()
    record["bucket"] = bucket
    os.makedirs(OUT, exist_ok=True)
    with open(PRE, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(record, handle, indent=1, sort_keys=True)
        handle.write("\n")
    print("PRE-RECORD: keys=%d prefix_object_count=%d hold=%s versioned_keys_with_prior=%d"
          % (len(record["keys"]), record["prefix_object_count"], record["hold_AMGT_AIFILL_ROOT"],
             sum(1 for v in record["keys"].values() if v["version_count"] > 1)))


def preflight(docs):
    if COO_HALF_SHA is None:
        raise SystemExit("BLOCKED: COO_HALF_SHA is not set (the half is not signed and bound yet)")
    with open(COO_HALF, "rb") as handle:
        if sha(handle.read()) != COO_HALF_SHA:
            raise SystemExit("BLOCKED: the COO half's sha256 is not the one the CTO half signed")
    with open(MANIFEST, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    with open(PRE, "r", encoding="utf-8") as handle:
        pre_record = json.load(handle)
    if set(pre_record["keys"]) != set(docs):
        raise SystemExit("BLOCKED: the pre-record does not cover exactly the 95 keys")
    for key, (name, raw, doc) in docs.items():
        if manifest.get(name) != sha(raw):
            raise SystemExit("BLOCKED: %s differs from the pinned manifest" % name)
        if raw != store.document_bytes(doc) + b"\n":
            raise SystemExit("BLOCKED: %s is not document_bytes(doc) plus one newline" % name)
    return pre_record


def write():
    docs = load_set()
    pre_record = preflight(docs)
    s3 = boto3.client("s3", region_name=store.REGION)
    bucket = pre_record["bucket"]
    written = []
    os.makedirs(OUT, exist_ok=True)
    for key in sorted(docs):
        name, raw, doc = docs[key]
        expect = store.document_bytes(doc)
        receipt = store.write_document(doc, client=s3)
        reply = s3.get_object(Bucket=receipt["bucket"], Key=receipt["key"])
        body = reply["Body"].read()
        row = {"key": key, "uri": receipt["uri"], "put_sha256": receipt["sha256"], "readback_sha256": sha(body),
               "expect_sha256": sha(expect), "file_sha256": sha(raw), "new_version_id": reply.get("VersionId"),
               "prior_version_id": pre_record["keys"][key]["current_version_id"]}
        row["ok"] = bool(row["readback_sha256"] == row["expect_sha256"] == row["put_sha256"]
                         and row["new_version_id"] != row["prior_version_id"])
        with open(LOG, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
        written.append(key)
        if not row["ok"]:
            print("BRANCH 2: %s read-back mismatch; written so far %d; run rollback" % (key, len(written)))
            raise SystemExit(2)
    count = prefix_count(s3, bucket)
    hold = hold_value()
    print("WRITE DONE: keys=%d prefix_object_count=%d (pre %d) hold_unchanged=%s"
          % (len(written), count, pre_record["prefix_object_count"], hold == pre_record["hold_AMGT_AIFILL_ROOT"]))
    if count != pre_record["prefix_object_count"] or hold != pre_record["hold_AMGT_AIFILL_ROOT"]:
        print("BRANCH 2: object count or hold changed; run rollback")
        raise SystemExit(2)


def rollback():
    with open(PRE, "r", encoding="utf-8") as handle:
        pre_record = json.load(handle)
    s3 = boto3.client("s3", region_name=store.REGION)
    done = []
    with open(LOG, "r", encoding="utf-8") as handle:  # log-open-ok: single-writer ASCII log written by this script's write mode
        keys = [json.loads(line)["key"] for line in handle if line.strip()]
    for key in sorted(set(keys)):
        entry = pre_record["keys"][key]
        s3.copy_object(Bucket=entry["bucket"], Key=entry["key"],
                       CopySource={"Bucket": entry["bucket"], "Key": entry["key"], "VersionId": entry["current_version_id"]},
                       ContentType=store.CONTENT_TYPE, MetadataDirective="REPLACE")
        body = s3.get_object(Bucket=entry["bucket"], Key=entry["key"])["Body"].read()
        done.append((key, sha(body) == entry["current_sha256"]))
    print("ROLLBACK: keys=%d restored_sha_equal=%d" % (len(done), sum(1 for _, ok in done if ok)))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "pre":
        pre()
    elif mode in ("write", "rollback") and "--confirm" in sys.argv:
        {"write": write, "rollback": rollback}[mode]()
    else:
        raise SystemExit("usage: store95.py pre | write --confirm | rollback --confirm")
