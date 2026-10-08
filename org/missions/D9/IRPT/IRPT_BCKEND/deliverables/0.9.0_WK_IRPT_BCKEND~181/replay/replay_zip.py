"""IB-pr-373 (E10 recut) offline differential replay (release-order regression arm), ONE zip per process (run with python -I).

Usage: python -I replay_zip.py <live|built> <unzipped_zip_dir> <snapshot.json> <out.json>

Modeled on IB-pr-370's replay_zip.py (itself IB-pr-368's). Every module and registry accessor is THE ZIP'S OWN (repository, retention, composition,
submit_installed, lib/opal_naming.reporting_policy / reporting_destination reading the zip's own packaged registry); no repo file is read.

live  mode: reserves ONE retained ANALYSIS and ONE retained PERFORMANCE fixture under irpt-x10-v1 (a source artifact, its promotion, then
            the published report) through THIS zip's code path with in-memory index and blob fakes; writes the index/blob state to
            <snapshot.json>; reads each report back with repository.get.
built mode: loads <snapshot.json> (the rows and bytes the LIVE code wrote) and reads the same reports back through THIS zip's
            repository.get. Then the CUSTODY arms (built only): the zip's OWN custody_persist.custody_report_persist (the guarded
            operation) against the registry row AS PACKAGED (irpt-custody-x10-v1 ACTIVE): persist for a retained custody submission
            with the owner and accounts server-derived + read back by reference, other-firm refusal, caller-supplied owner/principal/
            account keys, a request not yet accepted, an unregistered registry, the composition removed (negative control), a
            non-Opal principal, and the zip's entry.py (route; the IB-pr-372 marked event is not handled). No simulated registry row.
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
    """IB-pr-373: the zip's OWN custody_persist.custody_report_persist (the guarded operation) against the registry row AS PACKAGED."""
    import custody_persist
    import retained_export
    import submit_installed
    res = {}
    row = opal_naming.reporting_policy(CUSTODY_REVISION)
    res["registry_row_as_packaged"] = {"state": row["state"], "enforcement_ref": row["enforcement_ref"], "firms": row["firms"],
                                       "families": sorted(row["families"]), "policy_sha256": row["policy_sha256"]}
    res["modules"] = {m.__name__: os.path.relpath(m.__file__, zipdir).replace("\\", "/")
                      for m in (custody_persist, retained_export, submit_installed)}

    def try_(fn):
        try:
            return {"ok": True, "result": fn()}
        except Exception as exc:
            return {"ok": False, "exc": "%s: %s" % (type(exc).__name__, exc)}

    def fingerprint(row_):
        return hashlib.sha256(canon(row_)).hexdigest()

    accounts = ["acc-a", "acc-b"]
    creator = {"firm_id": "49financial", "principal_id": "opal.creator@opal.example", "home_firm_id": "opal-capital",
               "principal_class": "OPAL_GLOBAL", "advisor_id": None}
    creator["ownership_fingerprint"] = fingerprint(creator)
    persister = {"firm_id": "49financial", "principal_id": "opal.persister@opal.example", "home_firm_id": "opal-capital",
                 "principal_class": "OPAL_GLOBAL", "advisor_id": None}
    persister["ownership_fingerprint"] = fingerprint(persister)
    custody_owner = {"schema_version": "custody-owner-v1", "firm_id": "49financial", "principal_id": creator["principal_id"],
                     "home_firm_id": "opal-capital", "principal_class": "OPAL_GLOBAL", "advisor_id": None,
                     "account_ids": sorted(accounts), "account_set_id": "sel_" + "e9" * 32, "snapshot_id": "snap-1",
                     "directory_revision": "dir-1", "entitlement_revision": "ent-1"}
    custody_owner["ownership_fingerprint"] = fingerprint(custody_owner)
    composition_doc = {"schema_version": "irpt-analysis-composition.v1", "browser": {"snapshot_id": "snap-1", "account_ids": accounts},
                       "resolved": {"owner": custody_owner, "document": {"source": {"lane": "CUSTODY", "snapshot_id": "snap-1"}},
                                    "input_ref": {"input_id": "in-1"}},
                       "recipe_version": "v1", "settings": {"k": 1}}
    custody_doc = {"as_of_date": "2026-09-30", "title": "Performance client statement", "sections": [], "synthetic": True}

    def world(policy_fn=None, promote=True):
        table, s3 = Table(), S3()
        pol = policy_fn or opal_naming.reporting_policy
        stores = composition.build_retained_repositories(table, s3, retained_export.authorizer(creator, accounts), validate,
                                                         reporting_policy=pol, reporting_destination=opal_naming.reporting_destination,
                                                         clock=lambda: NOW)
        ref = stores.artifacts.put(creator, custody_owner, "REQUEST_COMPOSITION", "REQ-replay-custody",
                                   canon(composition_doc), "application/json")
        if promote:
            stores.retention.promote(creator, ref["retention_ref"])

        def reports(auth):  # exactly submit_installed.compose's `reports` closure
            return submit_installed.retained_reports(table, s3, auth, submit_installed._validate, pol,
                                                     opal_naming.reporting_destination, clock=lambda: NOW)

        def artifacts(auth):  # exactly submit_installed.compose's `artifacts` closure
            return submit_installed.retained_artifacts(table, s3, auth, submit_installed._validate, pol,
                                                       opal_naming.reporting_destination, clock=lambda: NOW)
        return table, s3, ref, reports, artifacts

    class Req:
        headers = {}

    class Ctx:
        def __init__(self, tenant="49financial"):
            self.tenant = tenant

    def persist(ref, reports, artifacts, who=None, permitted=None, **over):
        who = who or persister
        body = {"retained_request": {"artifact_id": ref["artifact_id"]}, "document": copy.deepcopy(custody_doc),
                "provenance": {"recipe_version": "v1"}}
        body.update(over)
        original = submit_installed.compose
        submit_installed.compose = lambda request, ctx: {"reports": reports, "artifacts": artifacts, "principal": lambda: dict(who)}
        try:
            return custody_persist.custody_report_persist(Req(), {"permitted_account_set": permitted or accounts},
                                                          {"body": json.dumps(body)}, Ctx(who["firm_id"]))
        finally:
            submit_installed.compose = original

    def custody_blobs(s3):
        return len([k for k in s3.objects if "CUSTODY_REPORT" in k[1]])

    # ARM C1 -- the packaged row (ACTIVE): persist a report for the retained request, owner and accounts server-derived; read it back.
    table, s3, req, reports, artifacts = world()
    out = try_(lambda: persist(req, reports, artifacts))
    c1 = {"persist": {"ok": out["ok"], "exc": out.get("exc")}}
    if out["ok"]:
        r = out["result"]
        c1["ref"] = {"report_id": r["report_id"], "revision": r["revision"], "report_kind": r["report_kind"]}
        rows = [v for k, v in table.rows.items() if k[1].startswith("RETENTION#") and v.get("family") == "CUSTODY_REPORT"]
        c1["custody_retention_row_policy_revision"] = [x["ref"]["policy_revision"] for x in rows]
        report_row = [v for k, v in table.rows.items() if k[1].startswith("REPORT#%s#" % r["report_id"])][0]
        c1["stored_owner_equals_retained_request_owner"] = (
            report_row["owner"]["principal_id"] == creator["principal_id"] != persister["principal_id"]
            and report_row["owner"]["account_ids"] == sorted(accounts)
            and report_row["owner"]["account_set_id"] == custody_owner["account_set_id"])
        c1["depends_on_the_retained_requests_retention_ref"] = [x["dependencies"] for x in rows] == [[req["retention_ref"]]]
        auth = retained_export.authorizer(persister, accounts)
        body = {"authorized_report_revisions": [{"report_id": r["report_id"], "revision": r["revision"]}]}
        got = try_(lambda: retained_export.resolve(body, reports=reports(auth), principal=persister, tenant="49financial",
                                                   authorize=auth))
        c1["opal_read_by_ref"] = {"ok": got["ok"], "exc": got.get("exc"),
                                  "report_kind": got["result"]["kind"] if got["ok"] else None,
                                  "document_equal": got["ok"] and got["result"]["report"] == custody_doc}
        other = {"firm_id": "inflection", "principal_id": "other-advisor"}
        oauth = retained_export.authorizer(other, accounts)
        o = try_(lambda: retained_export.resolve(body, reports=reports(oauth), principal=other, tenant="inflection",
                                                 authorize=oauth))
        c1["other_firm_read_by_ref"] = {"ok": o["ok"], "exc": o.get("exc"), "body_returned": o["ok"]}
    res["packaged_active_round_trip"] = c1

    # ARM C2 -- a caller-supplied owner / principal / account key is refused by name; nothing custody is written.
    table, s3, req, reports, artifacts = world()
    c2 = {}
    for field, value in (("owner", {"firm_id": "49financial", "principal_id": "x"}), ("principal", {"firm_id": "49financial"}),
                         ("account_ids", ["acc-z"]), ("account_set_id", "sel_" + "00" * 32)):
        c2[field] = try_(lambda: persist(req, reports, artifacts, **{field: value}))
        c2[field]["custody_blobs"] = custody_blobs(s3)
    res["caller_supplied_principal_owner_or_accounts"] = c2

    # ARM C3 -- the retained request not yet accepted (accepted-only family): refused by name, nothing written.
    table, s3, req, reports, artifacts = world(promote=False)
    c3 = try_(lambda: persist(req, reports, artifacts))
    c3["custody_blobs"] = custody_blobs(s3)
    res["request_not_accepted"] = c3

    # ARM C4 -- an UNREGISTERED registry (the custody row absent): the probe omits the revision and the persist is refused.
    def without_custody(revision):
        if revision == CUSTODY_REVISION:
            raise ValueError("unknown reporting policy revision")
        return opal_naming.reporting_policy(revision)

    table, s3, req, reports, artifacts = world(without_custody)
    c4 = try_(lambda: persist(req, reports, artifacts))
    c4["custody_blobs"] = custody_blobs(s3)
    res["unregistered_registry"] = c4

    # ARM C5 -- NEGATIVE CONTROL: the composition removed (a repository built without the custody revision).
    table, s3, req, _reports, artifacts = world()

    def plain(auth):
        return composition.build_retained_repositories(table, s3, auth, validate, reporting_policy=opal_naming.reporting_policy,
                                                       reporting_destination=opal_naming.reporting_destination,
                                                       clock=lambda: NOW).reports
    c5 = try_(lambda: persist(req, plain, artifacts))
    c5["custody_blobs"] = custody_blobs(s3)
    res["negative_control_without_composition"] = c5

    # ARM C6 -- a non-Opal (firm advisor) principal is refused before anything is read.
    table, s3, req, reports, artifacts = world()
    advisor = {"firm_id": "49financial", "principal_id": "advisor", "principal_class": "FIRM_ADVISOR", "advisor_id": "ADV-1",
               "home_firm_id": "49financial"}
    c6 = try_(lambda: persist(req, reports, artifacts, who=advisor))
    c6["custody_blobs"] = custody_blobs(s3)
    res["non_opal_principal"] = c6

    # ARM C7 -- the deployed entry (the zip's own entry.py, flat layout): the route is the guarded Entry's, and the marked event
    #           of IB-pr-372 reaches the Entry like any event (refused, nothing written); entry.py carries no such path.
    table, s3, req, reports, artifacts = world()
    try:
        import entry
        marked = try_(lambda: entry.lambda_handler({"irpt_custody_persist": {"tenant": "49financial", "principal": dict(persister),
                                                                             "permitted_account_set": accounts,
                                                                             "owner": dict(custody_owner)}}, None))
        src = open(os.path.join(zipdir, "entry.py"), encoding="utf-8").read()
        answered = marked["result"] if marked["ok"] else {}
        res["entry_dispatch"] = {"route": entry.ROUTES.get("POST /api/scoped/investor-reporting/custody-report"),
                                 "operations": sorted(entry.ENTRY.operations),
                                 "marked_event": {"raised": marked.get("exc"), "answered_ok_flag": answered.get("ok"),
                                                  "reason": (answered.get("status") or {}).get("public_reason_code"),
                                                  "has_data": "data" in answered, "custody_blobs": custody_blobs(s3)},
                                 "entry_py_mentions_irpt_custody_persist": "irpt_custody_persist" in src,
                                 "has_run_custody_persist": hasattr(entry, "run_custody_persist")}
    except Exception as exc:  # an import failure at cold start is the finding
        res["entry_dispatch"] = {"ok": False, "exc": "%s: %s" % (type(exc).__name__, exc)}
    return res


if __name__ == "__main__":
    main()
