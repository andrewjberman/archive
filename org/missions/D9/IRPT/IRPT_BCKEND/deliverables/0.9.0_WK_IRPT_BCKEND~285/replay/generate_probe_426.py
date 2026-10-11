"""IB-pr-426 replay, direct probes of ONE extracted irpt-ycharts-generate tree (flat, as /var/task). Run as
    python -I probe426.py <extracted_zip_dir> <label> <out_json>
Offline: boto3 is replaced by an in-memory fake BEFORE any packaged module is imported, every socket connect is refused, and nothing
is read from or written to AWS. Probes (each recorded as a result or the exception class, never a value from client data):
  composition   generate_installed.compose_ports/describe over fake clients: ingestion_revision, destination_revision, the declared routes
  naming        opal_naming.reporting_policy / reporting_destination / lookup over the PACKAGED registry, every policy revision
  routes        every route of the Entry (analysis POST custody + prospect bodies, upload POST, catalogue GET) for three principals, with
                a TypeError call-arity trace over every frame of the packaged modules
  svc_operation the svc-custody-statement subject on direct-invoke events naming each operation (served.py's allow-list)
  loader        loaders.load_directory with a latest.json pointer that names no key
  seam          ids.projection_for_firm over a custodian-key seam mapping an account to None-like strings
  publication   publication.foreign_firm_names / printed_firm_names (the opal_naming lookup call site)
ASCII only.
"""
import hashlib
import io
import json
import os
import re
import socket
import sys

zip_dir, label, out_path = sys.argv[1:4]
sys.dont_write_bytecode = True
sys.path.insert(0, zip_dir)
os.environ.update({
    "AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake", "AWS_DEFAULT_REGION": "us-east-1",
    "IRPT_DIRECTORY_BUCKET_MAP": json.dumps({"opal-capital": "b-opal", "cottonwood": "b-cot", "inflection": "b-inf", "49financial": "b-49f"}),
    "IRPT_GENERATION_QUEUE_URL": "https://sqs.us-east-1.amazonaws.com/000000000000/irpt-generation-fake",
    "IRPT_REQUESTS_TABLE": "irpt-requests", "IRPT_JOBS_TABLE": "irpt-jobs"})
for k in ("AWS_PROFILE", "AWS_SESSION_TOKEN"):
    os.environ.pop(k, None)

ATTEMPTS = []


def _refuse(self, *a, **k):
    ATTEMPTS.append(1)
    raise OSError("OFFLINE-GUARD")


socket.socket.connect = _refuse
_real_gai = socket.getaddrinfo
socket.getaddrinfo = lambda host, *a, **k: _real_gai(host, *a, **k) if host in (None, "localhost", "127.0.0.1", "::1", "") else (_ for _ in ()).throw(OSError("OFFLINE-GUARD"))
socket.socket.connect_ex = _refuse

import boto3  # noqa: E402
from botocore.exceptions import ClientError  # noqa: E402


class FakeTable:
    def __getattr__(self, name):
        def call(*a, **k):
            return {"Items": [], "Count": 0, "Responses": {}} if name in ("query", "scan", "batch_get_item") else {}
        return call


class _Svc:
    service_name = "dynamodb"


class _Meta:
    service_model = _Svc()
    region_name = "us-east-1"


class FakePaginator:
    def paginate(self, *a, **k):
        return iter([{"Contents": [], "Items": [], "CommonPrefixes": []}])


class FakeClient:
    meta = _Meta()

    def __init__(self, service):
        self.service = service

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)

        def call(*a, **k):
            if self.service == "s3" and name in ("get_object", "head_object"):
                raise ClientError({"Error": {"Code": "NoSuchKey", "Message": "absent"}}, name)
            if name == "get_paginator":
                return FakePaginator()
            if name in ("query", "scan"):
                return {"Items": [], "Count": 0}
            if name == "list_objects_v2":
                return {"KeyCount": 0, "Contents": []}
            return {}
        return call


class FakeResource:
    def Table(self, name):  # noqa: N802 -- boto3's own spelling
        return FakeTable()


class FakeSession:
    def client(self, service, *a, **k):
        return FakeClient(service)

    def resource(self, service, *a, **k):
        return FakeResource()


boto3.client = lambda service, *a, **k: FakeClient(service)
boto3.resource = lambda service, *a, **k: FakeResource()
boto3.session.Session = FakeSession
boto3.Session = FakeSession

ARITY = re.compile(r"positional argument|unexpected keyword argument|required positional|required keyword|multiple values for argument")
HITS, ENTERED = [], set()
ROOT = os.path.abspath(zip_dir).replace("\\", "/").rstrip("/") + "/"


def _local(frame, event, arg):
    if event == "exception":
        exc_type, exc, _tb = arg
        if issubclass(exc_type, TypeError) and ARITY.search(str(exc)):
            HITS.append("%s:%s" % (os.path.basename(frame.f_code.co_filename)[:-3], frame.f_code.co_name))
    return _local


def _tracer(frame, event, arg):
    fn = frame.f_code.co_filename.replace("\\", "/")
    if not fn.startswith(ROOT):
        return None
    if event == "call":
        ENTERED.add((fn, frame.f_code.co_name))
    return _local


def short(exc):
    return type(exc).__name__ + (":" + str(exc).split(":", 1)[0][:60] if isinstance(exc, (ValueError, KeyError)) else "")


out = {"label": label}
import served  # noqa: E402
import generate_installed as gi  # noqa: E402


class _D(FakeClient):
    pass


clients = {"dynamodb": _D("dynamodb"), "table": FakeTable(), "s3": FakeClient("s3"), "sqs": FakeClient("sqs")}

# ---- composition
ports = gi.compose_ports(clients=clients, clock=lambda: 1000.0)
schemas = gi.schema_directory()
out["composition"] = {
    "ingestion_revision": ports["ingestion_revision"], "destination_revision": ports["destination_revision"],
    "declared_routes": sorted(gi.declared_routes()), "composed_ports": sorted(k for k, v in ports.items() if v is not None),
    "absent_producers": sorted(k for k, v in ports.items() if v is None),
    "schema_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()[:16] for p in sorted(schemas.glob("*.schema.json"))}}

# ---- naming (the packaged registry, as the function reads it)
import opal_naming as on  # noqa: E402
nm = {"policies": {}, "destinations": {}, "lookups": {}}
reg = on.load_registry()
nm["registry_files_loaded"] = sorted(k for k, v in reg.items() if v is not None)
for p in reg["reporting_policies"]["policies"]:
    rev = p["policy_revision"]
    try:
        pol = on.reporting_policy(rev)
        nm["policies"][rev] = {"state": pol["state"], "firms": list(pol["firms"]), "families": sorted(pol["families"]), "policy_sha256": pol["policy_sha256"]}
    except Exception as exc:  # noqa: BLE001
        nm["policies"][rev] = {"error": short(exc)}
    for firm in ("cottonwood", "49financial", "inflection"):
        for fam in sorted(p["families"]):
            try:
                nm["destinations"]["%s|%s|%s" % (rev, firm, fam)] = list(on.reporting_destination(
                    firm, fam, "ART-" + "a" * 64, "b" * 64, policy_revision=rev))
            except Exception as exc:  # noqa: BLE001
                nm["destinations"]["%s|%s|%s" % (rev, firm, fam)] = "ERR:" + short(exc)
for key in ("cottonwood", "49financial", "inflection", "opal-capital", "4698"):
    try:
        row = on.lookup(key)
        nm["lookups"][key] = {"key": row.get("key"), "long": row.get("long"), "class": row.get("class"), "bucket": row.get("bucket")}
    except Exception as exc:  # noqa: BLE001
        nm["lookups"][key] = "ERR:" + short(exc)
out["naming"] = nm

# ---- routes
boundary = gi.build_boundary(ports)
from ids import opaque_firm  # noqa: E402
boundary.render_ports = lambda t: (lambda *a, **k: None, lambda *a, **k: None, lambda *a, **k: None)
boundary.deps = lambda t: ((lambda x: {}), (lambda x: {}), (lambda x: ({}, "rev")))
boundary.opaque_firm_for = opaque_firm


def headers(email, firm, user_type="user"):
    return {"X-Contract-Version": served.CONTRACT_VERSION, "X-Firm-Id": firm, "x-origin-verify": "cloudfront",
            "x-user-email": email, "x-user-role": "user", "x-user-type": user_type}


CUSTODY = {"request_id": "areq-0001", "client_id": "C-one", "account_ids": ["A-one"], "snapshot_id": "SNAP-one", "variant": "overview",
           "comparison_keys": [], "report_title": None, "prepared_for": "Synthetic recipient"}
PROSPECT = {"request_id": "areq-0002", "input_id": "portfolio_" + "a" * 64, "variant": "overview", "comparison_keys": [],
            "report_title": None, "prepared_for": "Synthetic recipient"}
UPLOAD = {"filename": "synthetic.csv", "csv": "ticker,shares\nAAA,1\n"}
BODIES = {"POST /api/scoped/investor-reporting/analysis": [("custody_body", CUSTODY), ("prospect_body", PROSPECT)],
          "POST /api/scoped/investor-reporting/analysis/inputs": [("upload_body", UPLOAD)],
          "GET /api/scoped/investor-reporting/analysis/comparisons": [("no_body", None)]}
PRINCIPALS = (("internal_row_listed", lambda: headers("ops@opalinvest.com", "opal-capital"), {"allowedFirmIds": ["cottonwood"]}),
              ("firm_user_own", lambda: headers("adv@cottonwood.example", "cottonwood"), None),
              ("svc_custody_statement", lambda: headers("svc-custody-statement", "cottonwood", "service"), None))


def handle(event, row):
    del HITS[:]
    ENTERED.clear()
    boundary.load_service_profile = lambda email, _row=row: _row
    escaped, reply = None, None
    sys.settrace(_tracer)
    try:
        reply = boundary.handle(event)
    except BaseException as exc:  # noqa: BLE001 -- recorded, not hidden
        escaped = type(exc).__name__
    finally:
        sys.settrace(None)
    status = (reply or {}).get("status") or {} if isinstance(reply, dict) else {}
    return {"ok": reply.get("ok") if isinstance(reply, dict) else None, "code": status.get("public_reason_code"), "escaped": escaped,
            "arity_errors": sorted(set(HITS)), "arity_error_count": len(HITS), "functions_entered": len(ENTERED)}


routes = {}
for rk, bodies in BODIES.items():
    for bname, body in bodies:
        for pname, hmake, row in PRINCIPALS:
            event = {"headers": hmake(), "routeKey": rk, "pathParameters": {}, "isBase64Encoded": False,
                     "queryStringParameters": {"selected_tenant": "cottonwood"} if pname == "internal_row_listed" else {}}
            if body is not None:
                event["body"] = json.dumps(body)
            routes["%s | %s | %s" % (rk, bname, pname)] = handle(event, row)
out["routes"] = routes

# ---- svc_operation (direct-invoke events naming the operation)
svc = {}
for op in ("custody-report-persist", "analysis-requests", "submit-export", "analysis-request-read", "analysis-input-upload",
           "comparison-catalogue", "not-an-operation"):
    event = {"headers": headers("svc-custody-statement", "cottonwood", "service"), "operation": op, "body": json.dumps(CUSTODY),
             "queryStringParameters": {}}
    svc[op] = handle(event, None)
out["svc_operation"] = svc

# ---- loader pointer
import loaders  # noqa: E402


class PointerS3:
    def __init__(self, doc):
        self.doc = doc

    def get_object(self, **kw):
        return {"Body": io.BytesIO(json.dumps(self.doc).encode("utf-8")), "ContentLength": len(json.dumps(self.doc))}

    def __getattr__(self, n):
        raise AttributeError(n)


ld = {}
for name, doc in (("pointer_no_key", {}), ("pointer_empty_key", {"key": ""}), ("pointer_not_object", [1])):
    try:
        loaders.load_directory("cottonwood", s3=PointerS3(doc))
        ld[name] = "returned"
    except BaseException as exc:  # noqa: BLE001
        ld[name] = type(exc).__name__
out["loader"] = ld

# ---- seam projection
import ids  # noqa: E402
seam = {}
try:
    for mapped in ("None", "none", "NaN", "null", " ", "ACCT-0001"):
        for_firm = getattr(ids, "projection_for_firm")
        seam[repr(mapped)] = "present"
except Exception as exc:  # noqa: BLE001
    seam["error"] = short(exc)
out["seam_api"] = sorted(n for n in dir(ids) if "proj" in n.lower() or "seam" in n.lower())

# ---- publication (opal_naming.lookup call site, 1 argument)
import publication  # noqa: E402
pb = {}
try:
    pb["printed_firm_names"] = sorted(publication.printed_firm_names())
except Exception as exc:  # noqa: BLE001
    pb["printed_firm_names"] = "ERR:" + short(exc)
for firm in ("cottonwood", "49financial", "not-a-firm"):
    try:
        pb["foreign_firm_names(%s)" % firm] = publication.foreign_firm_names(b"%PDF-1.4 synthetic", firm)
    except BaseException as exc:  # noqa: BLE001
        pb["foreign_firm_names(%s)" % firm] = "ERR:" + short(exc)
out["publication"] = pb


# ---- addresses (holdings_publication.HoldingsPublication.location -> opal_naming.address: reads NAMING_SCHEMA.json, scopes, systems, tiers)
from holdings_publication import HoldingsPublication  # noqa: E402
ad = {}
for firm in ("49financial", "cottonwood", "inflection", "not-a-firm"):
    for qa in (False, True):
        try:
            hp = HoldingsPublication(FakeClient("s3"), firm, qa=qa)
            ad["%s|qa=%s" % (firm, qa)] = list(hp.location("platinum", "current", "manifest.json"))
        except BaseException as exc:  # noqa: BLE001
            ad["%s|qa=%s" % (firm, qa)] = "ERR:" + short(exc)
out["addresses"] = ad

# ---- schemas (every packaged contract is a valid Draft 2020-12 schema; digest per file is in composition)
import jsonschema  # noqa: E402
sv = {}
for p in sorted(gi.schema_directory().glob("*.schema.json")):
    try:
        jsonschema.Draft202012Validator.check_schema(json.loads(p.read_text(encoding="utf-8")))
        sv[p.name] = "valid"
    except Exception as exc:  # noqa: BLE001
        sv[p.name] = "ERR:" + short(exc)
out["schemas_valid"] = sv

out["network_connect_attempts"] = len(ATTEMPTS)
json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
print("OK: %s probes=%d routes=%d connect_attempts=%d" % (label, len([k for k in out if k not in ("label",)]), len(routes), len(ATTEMPTS)))
