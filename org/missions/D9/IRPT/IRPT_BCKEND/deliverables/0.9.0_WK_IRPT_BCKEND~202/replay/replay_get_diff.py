"""IB-pr-391 replay: ArtifactRepository.get()/head()/put() for EXISTING callers (user principals) through one packaged repository.py.

  python -I -B replay_get_diff.py <module_dir> <out.json>

Loads <module_dir>/repository.py by path, drives the same scenario list over offline fakes and writes the normalized outcomes
(exception type + first message words, or OK + sha256). Run once per live zip and once for the built zip, then compare the JSON.
Synthetic bytes, zero network. ASCII only.
"""
import copy
import hashlib
import importlib.util
import io
import json
import sys
from pathlib import Path

module_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("irpt_repo_under_replay", module_dir / "repository.py")
repo = importlib.util.module_from_spec(spec)
sys.modules["irpt_repo_under_replay"] = repo
spec.loader.exec_module(repo)


class AwsError(Exception):
    def __init__(self, code):
        self.response = {"Error": {"Code": code}}


class Table:
    def __init__(self):
        self.rows = {}

    def get_item(self, Key, ConsistentRead):
        item = self.rows.get((Key["tenant"], Key["request_revision"]))
        if not item:
            return {}
        from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
        return {"Item": TypeDeserializer().deserialize(TypeSerializer().serialize(item))}

    def put_item(self, Item, ConditionExpression):
        key = (Item["tenant"], Item["request_revision"])
        if key in self.rows:
            raise AwsError("ConditionalCheckFailedException")
        self.rows[key] = copy.deepcopy(Item)


class S3:
    def __init__(self):
        self.objects, self.n = {}, 0

    def put_object(self, Bucket, Key, Body, ContentType, IfNoneMatch):
        if (Bucket, Key) in self.objects:
            raise AwsError("PreconditionFailed")
        self.n += 1
        self.objects[(Bucket, Key)] = (bytes(Body), "version-%d" % self.n)
        return {"VersionId": "version-%d" % self.n}

    def head_object(self, Bucket, Key):
        return {"VersionId": self.objects[Bucket, Key][1]}

    def get_object(self, Bucket, Key, VersionId):
        body, version = self.objects[Bucket, Key]
        assert VersionId == version
        return {"Body": io.BytesIO(body)}


def norm(fn):
    try:
        got = fn()
    except BaseException as exc:  # the outcome class IS the datum
        return "%s: %s" % (type(exc).__name__, " ".join(str(exc).split()[:6]))
    if isinstance(got, dict) and "data" in got:
        return "OK data_sha256=%s ref_family=%s" % (hashlib.sha256(got["data"]).hexdigest()[:16], got["ref"].get("family"))
    if isinstance(got, dict):
        return "OK keys=%s" % sorted(k for k in got if k not in ("version_id",))
    return "OK %r" % (got,)


def new_repo(table, s3):
    return repo.ArtifactRepository(
        repo.DynamoReportIndex(table),
        repo.S3ReportBlobs(s3, lambda firm, family, identity, sha: ("test-private", "/".join((firm, family, identity, sha)))),
        lambda principal, owner: principal["principal_id"] == owner["principal_id"] and principal["firm_id"] == owner["firm_id"],
        {"test-original-csv", "test-vendor-pdf"})


table, s3 = Table(), S3()
repo_ = new_repo(table, s3)
alice = {"firm_id": "test-firm", "principal_id": "alice"}
bob = {"firm_id": "test-firm", "principal_id": "bob"}
carol_other_firm = {"firm_id": "other-firm", "principal_id": "alice"}
impostor = {"firm_id": "test-firm", "principal_id": "svc-commentary"}
owner = {**alice, "account_ids": [], "prospect_input_id": "upload-1"}
DATA = b"Ticker,Dollars\nAAPL,100\n"
outcomes = {}
receipt = repo_.put(alice, owner, "test-original-csv", "upload-1", DATA, "text/csv")
outcomes["put_own_receipt_family"] = receipt.get("family")
aid = receipt["artifact_id"]
outcomes["put_retry_same_receipt"] = norm(lambda: repo_.put(alice, owner, "test-original-csv", "upload-1", DATA, "text/csv") == receipt)
outcomes["get_own"] = norm(lambda: repo_.get(alice, aid))
outcomes["get_own_explicit_firm"] = norm(lambda: repo_.get(alice, aid, data_firm="test-firm"))
outcomes["head_own"] = norm(lambda: repo_.head(alice, aid))
outcomes["get_other_principal_same_firm"] = norm(lambda: repo_.get(bob, aid))
outcomes["get_same_name_other_firm"] = norm(lambda: repo_.get(carol_other_firm, aid))
outcomes["get_own_wrong_data_firm"] = norm(lambda: repo_.get(alice, aid, data_firm="other-firm"))
outcomes["get_unknown_id"] = norm(lambda: repo_.get(alice, "ART-" + "0" * 64))
outcomes["get_malformed_id"] = norm(lambda: repo_.get(alice, "../x"))
outcomes["get_user_named_like_the_service_subject"] = norm(lambda: repo_.get(impostor, aid))
outcomes["put_unregistered_family"] = norm(lambda: repo_.put(alice, owner, "NOT-A-FAMILY", "x", DATA, "text/csv"))
outcomes["put_conflicting_bytes"] = norm(lambda: repo_.put(alice, owner, "test-original-csv", "upload-1", b"other", "text/csv"))
outcomes["put_for_another_owner"] = norm(lambda: repo_.put(bob, owner, "test-original-csv", "upload-2", DATA, "text/csv"))
outcomes["head_other_principal"] = norm(lambda: repo_.head(bob, aid))
outcomes["s3_objects_after"] = len(s3.objects)
outcomes["index_rows_after"] = len(table.rows)
out.write_text(json.dumps({"module": str(module_dir), "repository_sha256": hashlib.sha256(
    (module_dir / "repository.py").read_bytes()).hexdigest(), "outcomes": outcomes}, indent=1, sort_keys=True), encoding="ascii")
print("OK:", len(outcomes), "outcomes ->", out.name)
