"""IB-pr-370 offline differential replay (release-order regression arm), ONE zip per process (run with python -I).

Usage: python -I replay_zip.py <live|built> <unzipped_zip_dir> <snapshot.json> <out.json>

Modeled on IB-pr-368's replay_zip.py. Every module and registry accessor is THE ZIP'S OWN (repository, retention, composition,
submit_installed, lib/opal_naming.reporting_policy / reporting_destination reading the zip's own packaged registry); no repo file is read.

live  mode: reserves ONE retained ANALYSIS and ONE retained PERFORMANCE fixture under irpt-x10-v1 (a source artifact, its promotion, then
            the published report) through THIS zip's code path with in-memory index and blob fakes; writes the index/blob state to
            <snapshot.json>; reads each report back with repository.get.
built mode: loads <snapshot.json> (the rows and bytes the LIVE code wrote) and reads the same reports back through THIS zip's
            repository.get. Then the CUSTODY arms (built only): custody under the registry row as packaged (PENDING_ENFORCEMENT),
            then a SYNTHETIC in-memory ACTIVE copy of that row (a simulation of the later flip, never a release).
Both modes run the NEGATIVE CONTROL: a retention row's policy_sha256 altered; repository.get must refuse.
No network, no AWS, no credentials. Synthetic ids only.
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
CUSTODY_REVISION = "irpt-custody-x10-v1"
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
    mode, zipdir, snap_path, out_path = sys.argv[1:5]
    zipdir = os.path.abspath(zipdir)
    sys.path.insert(0, zipdir)
    sys.path.insert(0, os.path.join(zipdir, "lib"))
    import repository  # noqa: E402  (the zip's own modules)
    import retention   # noqa: E402
    import composition  # noqa: E402
    import opal_naming  # noqa: E402
    mods = (repository, retention, composition, opal_naming)
    for mod in mods:
        assert os.path.dirname(os.path.abspath(mod.__file__)) in (zipdir, os.path.join(zipdir, "lib")), (mod.__file__, zipdir)
    assert os.path.abspath(opal_naming.REPO) == zipdir, (opal_naming.REPO, zipdir)  # the registry read is the zip's own

    policy_row = opal_naming.reporting_policy(POLICY_REVISION)
    schema = json.load(open(os.path.join(zipdir, "irpt_contracts", "AnalysisReport.schema.json"), encoding="utf-8"))

    owner = {"firm_id": "49financial", "principal_id": "advisor", "account_ids": ["acc-a"]}
    principal = {"firm_id": "49financial", "principal_id": "advisor"}

    def authorize(p, o):
        return p["principal_id"] == o["principal_id"]

    def validate(kind, value):
        if kind == "ANALYSIS":
            jsonschema.Draft202012Validator(schema).validate(value)
        return True  # PERFORMANCE / CUSTODY_REPORT: the document schemas are not under test here

    def stack(table, s3, policy_fn=None, extra=(), destination_fn=None):
        kw = {"additional_policy_revisions": extra} if extra else {}  # the live composition has no such keyword
        return composition.build_retained_repositories(
            table, s3, authorize, validate,
            reporting_policy=policy_fn or opal_naming.reporting_policy,
            reporting_destination=destination_fn or opal_naming.reporting_destination,
            clock=lambda: NOW, **kw)

    out = {"mode": mode, "zip_dir_name": os.path.basename(zipdir), "policy_revision": POLICY_REVISION,
           "policy_sha256": policy_row["policy_sha256"], "policy_state": policy_row["state"],
           "module_files": sorted(os.path.relpath(m.__file__, zipdir).replace("\\", "/") for m in mods),
           "kinds": list(repository.KINDS)}

    def fixtures(stores):
        source = stores.artifacts.put(principal, owner, "ORIGINAL_CSV", "replay-source", b"symbol,value\nTEST,100\n", "text/csv")
        stores.retention.promote(principal, source["retention_ref"])
        refs = {}
        for kind, request_id in (("ANALYSIS", "REQ-replay-fixture"), ("PERFORMANCE", "REQ-replay-performance")):
            value = analysis_report() if kind == "ANALYSIS" else {"request_ref": {"request_id": request_id}, "series": [1, 2, 3]}
            req = value["request_ref"]
            refs[kind] = stores.reports.persist(principal, owner, kind, req, value, {"fixture": "replay-reserved-by-live-code"},
                                                retention_dependencies=[source["retention_ref"]])
        return source, refs

    if mode == "live":
        table, s3 = Table(), S3()
        source, refs = fixtures(stack(table, s3))
        snap = {"refs": {k: {"report_id": v["report_id"], "revision": v["revision"], "report_kind": v["report_kind"]}
                         for k, v in refs.items()},
                "rows": [[list(k), v] for k, v in table.rows.items()],
                "objects": [[list(k), base64.b64encode(v[0]).decode("ascii"), v[1]] for k, v in s3.objects.items()]}
        json.dump(snap, open(snap_path, "w", encoding="utf-8"), sort_keys=True)
        out["reserved"] = True
    else:
        snap = json.load(open(snap_path, encoding="utf-8"))
        out["reserved"] = False

    table = Table({tuple(k): v for k, v in snap["rows"]})
    s3 = S3({tuple(k): (base64.b64decode(b), ver) for k, b, ver in snap["objects"]})
    out["fixture"] = {"families": sorted(snap["refs"]), "index_rows": len(table.rows), "blobs": len(s3.objects),
                      "refs": snap["refs"]}

    out["get"] = {}
    for kind, ref in sorted(snap["refs"].items()):
        res = {"ok": False, "raised": None, "refused": False, "result_sha256": None}
        try:
            got = stack(table, s3).reports.get(principal, ref["report_id"], ref["revision"])
            res["result_sha256"] = hashlib.sha256(canon(got)).hexdigest()
            res["ok"] = got["ref"]["report_id"] == ref["report_id"] and got["ref"]["revision"] == ref["revision"]
        except repository.ReportRefused as exc:
            res["refused"] = True
            res["raised"] = "%s: %s" % (type(exc).__name__, exc)
        except Exception as exc:  # TypeError and anything else
            res["raised"] = "%s: %s" % (type(exc).__name__, exc)
        out["get"][kind] = res

    # NEGATIVE CONTROL: alter the policy_sha256 stored on a report's retention row, one family at a time.
    out["negative_control"] = {}
    for kind, ref in sorted(snap["refs"].items()):
        altered = {k: copy.deepcopy(v) for k, v in table.rows.items()}
        targets = [k for k, v in altered.items() if k[1].startswith("RETENTION#") and v.get("family") == kind]
        assert len(targets) == 1, targets
        original = altered[targets[0]]["policy_sha256"]
        altered[targets[0]]["policy_sha256"] = ("0" if original[0] != "0" else "1") + original[1:]
        neg = {"refused": False, "exc": None, "altered_rows": 1}
        try:
            stack(Table(altered), s3).reports.get(principal, ref["report_id"], ref["revision"])
        except repository.ReportRefused as exc:
            neg["refused"] = True
            neg["exc"] = "%s: %s" % (type(exc).__name__, exc)
        except Exception as exc:
            neg["exc"] = "NOT-A-REFUSAL %s: %s" % (type(exc).__name__, exc)
        out["negative_control"][kind] = neg

    if mode == "built":
        out["custody"] = custody_arms(composition, repository, retention, opal_naming, stack, fixtures, principal, owner, authorize,
                                      validate, zipdir)

    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


def custody_arms(composition, repository, retention, opal_naming, stack, fixtures, principal, owner, authorize, validate, zipdir):
    res = {"registry_row_as_packaged": None}
    row = opal_naming.reporting_policy(CUSTODY_REVISION)
    res["registry_row_as_packaged"] = {"state": row["state"], "enforcement_ref": row["enforcement_ref"], "firms": row["firms"],
                                       "families": sorted(row["families"]), "policy_sha256": row["policy_sha256"]}
    res["composition_custody_constant"] = composition.CUSTODY_POLICY_REVISION

    def try_(fn):
        try:
            v = fn()
            return {"ok": True, "result": v}
        except Exception as exc:
            return {"ok": False, "exc": "%s: %s" % (type(exc).__name__, exc)}

    custody_request = {"request_id": "REQ-custody-fixture"}
    custody_doc = {"as_of_date": "2026-09-30", "request_ref": custody_request, "synthetic": True}

    # ARM C1 -- the registry as packaged (PENDING_ENFORCEMENT): the repository composes, retention refuses.
    table, s3 = Table(), S3()
    stores = stack(table, s3, extra=(CUSTODY_REVISION,))
    source = stores.artifacts.put(principal, owner, "ORIGINAL_CSV", "custody-source", b"symbol,value\nTEST,100\n", "text/csv")
    stores.retention.promote(principal, source["retention_ref"])
    res["pending_persist"] = try_(lambda: stores.reports.persist(
        principal, owner, "CUSTODY_REPORT", custody_request, custody_doc, {"fixture": "custody"},
        retention_dependencies=[source["retention_ref"]]))
    res["pending_persist"]["rows_after"] = len(table.rows)
    res["pending_persist"]["blobs_after"] = len(s3.objects)
    # the submit path's own composition (submit_installed.retained_reports) requests the custody revision when the registry carries it
    import submit_installed
    t2, s2 = Table(), S3()
    reports = submit_installed.retained_reports(t2, s2, authorize, validate, opal_naming.reporting_policy,
                                                opal_naming.reporting_destination, clock=lambda: NOW)
    res["submit_installed_revisions"] = dict(reports.revisions)

    # ARM C2 -- SIMULATION ONLY: an in-memory ACTIVE copy of the packaged row (the later flip), digest recomputed as opal_naming does.
    def active_policy(revision):
        base = opal_naming.reporting_policy(revision)
        if revision != CUSTODY_REVISION:
            return base
        r = {k: v for k, v in base.items() if k != "policy_sha256"}
        r.update(state="ACTIVE", enforcement_ref="e" * 40)
        sha = hashlib.sha256(json.dumps(r, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()
        return {**r, "policy_sha256": sha}

    def destination(firm, family, identity, sha, *, policy_revision):
        # the writer destination is refused while the row is PENDING; on the simulated ACTIVE row it is the family's address
        policy = active_policy(policy_revision)
        return opal_naming._reporting_destination(policy, firm, family, identity, sha)

    table, s3 = Table(), S3()
    stores = stack(table, s3, policy_fn=active_policy, extra=(CUSTODY_REVISION,), destination_fn=destination)
    source, refs = fixtures(stores)
    sim = {"x10_reports_retained": sorted(refs)}
    custody = try_(lambda: stores.reports.persist(principal, owner, "CUSTODY_REPORT", custody_request, custody_doc,
                                                  {"fixture": "custody"}, retention_dependencies=[source["retention_ref"]]))
    if custody["ok"]:
        ref = custody["result"]
        custody["result"] = {"report_id": ref["report_id"], "revision": ref["revision"], "report_kind": ref["report_kind"]}
        got = try_(lambda: stores.reports.get(principal, ref["report_id"], ref["revision"]))
        sim["opal_style_read_by_ref"] = {"ok": got["ok"], "exc": got.get("exc"),
                                         "report_kind": got["result"]["ref"]["report_kind"] if got["ok"] else None,
                                         "document_equal": got["ok"] and got["result"]["report"] == custody_doc}
        other = {"firm_id": "inflection", "principal_id": "other-advisor"}
        sim["other_firm_read_by_ref"] = try_(lambda: stores.reports.get(other, ref["report_id"], ref["revision"]))
        sim["other_firm_read_by_ref"]["body_returned"] = sim["other_firm_read_by_ref"]["ok"]
        rows = [v for k, v in table.rows.items() if k[1].startswith("RETENTION#") and v.get("family") == "CUSTODY_REPORT"]
        sim["custody_retention_row_policy_revision"] = [r["ref"]["policy_revision"] for r in rows]
        fam = {}
        for k, v in table.rows.items():
            if k[1].startswith("RETENTION#") and "family" in v:
                fam.setdefault(v["family"], v["ref"]["policy_revision"])
        sim["retention_revision_by_family"] = fam
        x10 = {k: v for k, v in refs.items()}
        sim["x10_reads_after"] = {k: try_(lambda r=r: bool(stores.reports.get(principal, r["report_id"], r["revision"])))["ok"]
                                  for k, r in x10.items()}
    sim["custody_persist"] = custody
    res["simulated_active"] = sim
    return res


if __name__ == "__main__":
    main()
