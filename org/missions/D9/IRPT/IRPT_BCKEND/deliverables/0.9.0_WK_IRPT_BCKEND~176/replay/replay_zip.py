"""IB-pr-368 offline differential replay, ONE zip per process (run with python -I).

Usage: python -I replay_zip.py <live|built> <unzipped_zip_dir> <repo_root> <snapshot.json> <out.json>

live  mode: reserves ONE retained ANALYSIS fixture (a source artifact, its promotion, then the published report) through THIS
            zip's own ReportRepository / RetentionPolicy code path with in-memory index and blob fakes and the HEAD registry
            policy row for irpt-x10-v1, writes the index/blob state to <snapshot.json>, then reads the report back with
            repository.get.
built mode: loads <snapshot.json> (the rows and bytes the LIVE code wrote) and reads the same report back through THIS zip's
            repository.get.
Both modes then run the NEGATIVE CONTROL: the report's retention row has its policy_sha256 altered; repository.get must refuse.
No network, no AWS, no credentials: the fakes are in this file. Synthetic ids only.
"""
import base64
import copy
import hashlib
import io
import json
import os
import sys

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from botocore.exceptions import ClientError
import jsonschema

POLICY_REVISION = "irpt-x10-v1"
NOW = 1_800_000_000


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


class Table:
    def __init__(self, rows=None):
        self.rows = rows if rows is not None else {}

    def get_item(self, Key, ConsistentRead):
        assert ConsistentRead is True
        row = copy.deepcopy(self.rows.get((Key["tenant"], Key["request_revision"])))
        return {"Item": TypeDeserializer().deserialize(TypeSerializer().serialize(row))} if row else {}

    def put_item(self, Item, ConditionExpression, **kwargs):
        key = (Item["tenant"], Item["request_revision"])
        previous = self.rows.get(key)
        if ConditionExpression == "attribute_not_exists(request_revision)":
            allowed = previous is None
        else:
            assert ConditionExpression == "#g = :g AND expires_at > :now AND #s = :reserved"
            args = kwargs["ExpressionAttributeValues"]
            allowed = (previous is not None and previous["generation"] == args[":g"]
                       and previous["expires_at"] > args[":now"] and previous["state"] == args[":reserved"])
        if not allowed:
            raise ClientError({"Error": {"Code": "ConditionalCheckFailedException"}}, "PutItem")
        self.rows[key] = copy.deepcopy(Item)
        return {}


class S3:
    def __init__(self, objects=None):
        self.objects = objects if objects is not None else {}
        self.put_count = len(self.objects)

    def put_object(self, Bucket, Key, Body, ContentType, IfNoneMatch):
        assert IfNoneMatch == "*"
        key = (Bucket, Key)
        if key in self.objects:
            raise ClientError({"Error": {"Code": "PreconditionFailed"}}, "PutObject")
        self.put_count += 1
        self.objects[key] = (bytes(Body), "version-%d" % self.put_count)
        return {"VersionId": self.objects[key][1]}

    def head_object(self, Bucket, Key):
        return {"VersionId": self.objects[Bucket, Key][1]}

    def get_object(self, Bucket, Key, VersionId):
        body, version = self.objects[Bucket, Key]
        assert VersionId == version
        return {"Body": io.BytesIO(body)}


def analysis_report():
    return {"request_ref": {"request_id": "REQ-replay-fixture", "request_revision": 1,
                            "attempt_id": "ATT-replay-fixture", "attempt_number": 1},
            "vendor_artifact": {"sha256": "a" * 64, "byte_length": 7, "retrieved_at": "2026-09-22T20:00:00Z"},
            "effective_inputs": {"read_back": "READ_BACK_VERIFIED", "holdings_fingerprint": "b" * 64, "settings": {}},
            "sections": [], "disclosures": [],
            "extraction_validation": {"status": "CERTIFIED", "checks_run": 1, "checks_failed": 0},
            "release": {"released_revision": "1"}}


def main():
    mode, zipdir, root, snap_path, out_path = sys.argv[1:6]
    zipdir = os.path.abspath(zipdir)
    sys.path.insert(0, zipdir)
    import repository  # noqa: E402  (the zip's own module)
    import retention   # noqa: E402
    import composition  # noqa: E402
    for mod in (repository, retention, composition):
        assert os.path.dirname(os.path.abspath(mod.__file__)) == zipdir, (mod.__file__, zipdir)

    registry = json.load(open(os.path.join(root, "infra/logic/registry/reporting_policies.json"), encoding="utf-8"))
    rows = [p for p in registry["policies"] if p["policy_revision"] == POLICY_REVISION]
    assert len(rows) == 1
    row = rows[0]
    # the same digest the served accessor (opal_naming.reporting_policy) computes
    row_sha = hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()
    policy = {**row, "policy_sha256": row_sha}
    schema = json.load(open(os.path.join(root, "docs/contracts/investor-reporting/v1/AnalysisReport.schema.json"), encoding="utf-8"))

    owner = {"firm_id": "49financial", "principal_id": "advisor", "account_ids": ["acc-a"]}
    principal = {"firm_id": "49financial", "principal_id": "advisor"}

    def authorize(p, o):
        return p["principal_id"] == o["principal_id"]

    def validate(kind, value):
        assert kind == "ANALYSIS"
        jsonschema.Draft202012Validator(schema).validate(value)

    def destination(firm, family, identity, sha, *, policy_revision):
        return "offline-private", "/".join((firm, family, identity, sha))

    def stack(table, s3):
        return composition.build_retained_repositories(
            table, s3, authorize, validate,
            reporting_policy=lambda revision: copy.deepcopy(policy),
            reporting_destination=destination, clock=lambda: NOW)

    out = {"mode": mode, "zip_dir_name": os.path.basename(zipdir), "policy_sha256": row_sha,
           "module_files": sorted(os.path.basename(m.__file__) for m in (repository, retention, composition))}

    if mode == "live":
        table, s3 = Table(), S3()
        stores = stack(table, s3)
        source = stores.artifacts.put(principal, owner, "ORIGINAL_CSV", "replay-source",
                                      b"symbol,value\nTEST,100\n", "text/csv")
        stores.retention.promote(principal, source["retention_ref"])
        value = analysis_report()
        ref = stores.reports.persist(principal, owner, "ANALYSIS", value["request_ref"], value,
                                     {"fixture": "replay-reserved-by-live-code"},
                                     retention_dependencies=[source["retention_ref"]])
        snap = {"report_id": ref["report_id"], "revision": ref["revision"], "report_kind": ref["report_kind"],
                "rows": [[list(k), v] for k, v in table.rows.items()],
                "objects": [[list(k), base64.b64encode(v[0]).decode("ascii"), v[1]] for k, v in s3.objects.items()]}
        json.dump(snap, open(snap_path, "w", encoding="utf-8"), sort_keys=True)
        out["reserved"] = True
    else:
        snap = json.load(open(snap_path, encoding="utf-8"))
        out["reserved"] = False

    table = Table({tuple(k): v for k, v in snap["rows"]})
    s3 = S3({tuple(k): (base64.b64decode(b), ver) for k, b, ver in snap["objects"]})
    out["fixture"] = {"family": snap["report_kind"], "report_id": snap["report_id"], "revision": snap["revision"],
                      "index_rows": len(table.rows), "blobs": len(s3.objects)}

    res = {"ok": False, "raised": None, "refused": False, "result_sha256": None}
    try:
        got = stack(table, s3).reports.get(principal, snap["report_id"], snap["revision"])
        res["result_sha256"] = hashlib.sha256(canon(got)).hexdigest()
        res["ok"] = got["ref"]["report_id"] == snap["report_id"] and got["ref"]["revision"] == snap["revision"]
    except repository.ReportRefused as exc:
        res["refused"] = True
        res["raised"] = "%s: %s" % (type(exc).__name__, exc)
    except Exception as exc:  # TypeError and anything else
        res["raised"] = "%s: %s" % (type(exc).__name__, exc)
    out["get"] = res

    # NEGATIVE CONTROL: alter the policy_sha256 stored on the report's retention row.
    altered = {k: copy.deepcopy(v) for k, v in table.rows.items()}
    targets = [k for k, v in altered.items() if k[1].startswith("RETENTION#") and v.get("family") == "ANALYSIS"]
    assert len(targets) == 1, targets
    original = altered[targets[0]]["policy_sha256"]
    altered[targets[0]]["policy_sha256"] = ("0" if original[0] != "0" else "1") + original[1:]
    neg = {"refused": False, "exc": None, "altered_rows": 1}
    try:
        stack(Table(altered), s3).reports.get(principal, snap["report_id"], snap["revision"])
    except repository.ReportRefused as exc:
        neg["refused"] = True
        neg["exc"] = "%s: %s" % (type(exc).__name__, exc)
    except Exception as exc:
        neg["exc"] = "NOT-A-REFUSAL %s: %s" % (type(exc).__name__, exc)
    out["negative_control"] = neg

    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
