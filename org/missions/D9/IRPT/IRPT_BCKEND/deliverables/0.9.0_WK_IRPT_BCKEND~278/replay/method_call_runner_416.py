"""IB-pr-416 METHOD-call arm, dynamic half (TO AMENDMENT 2; CTO AMENDMENT 7 of the IRPT_ANLREQ release-1 half): ONE extracted Lambda zip, one
process, offline. Run as
    python -I method_call_runner_416.py <extracted_zip_dir> <label> <out_json> <function> <routes_json> [<layer_python_dir> ...]
It imports the zip's OWN modules from the zip directory (flat layout, as /var/task), builds the function's real Entry (irpt-status: the
owned-history boundary composed by status_installed.compose_ports/build_boundary over IN-MEMORY FAKE clients; the other two: entry.ENTRY),
and for EACH route of the function calls the real Entry.handle with a synthetic event for two principals: an Opal internal caller whose profile
row lists cottonwood, and a plain cottonwood firm user. boto3 is replaced by an in-memory fake (every read answers empty / not found; nothing
leaves the process, no AWS call, no client data). A sys.settrace hook watches every frame whose code lives in the zip directory and records
each TypeError raised there whose message is a call-arity or keyword error ("takes N positional arguments", "unexpected keyword argument",
"missing N required", "got multiple values"), even when the code under test catches it and answers a refusal, so the arm reads a split that
the boundary swallowed. Per route and principal: code, ok, escaped exception class, arity_errors (module:line and message with no values),
functions_entered (distinct code objects entered in the zip's modules: how deep the call went). ASCII only.
"""
import json
import os
import re
import sys

zip_dir, label, out_path, function, routes_path = sys.argv[1:6]
for _layer in reversed(sys.argv[6:]):
    sys.path.insert(0, _layer)
sys.path.insert(0, zip_dir)
os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(
    {"opal-capital": "b-opal", "cottonwood": "b-cot", "inflection": "b-inf", "49financial": "b-49f"})
os.environ.update({"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake", "AWS_DEFAULT_REGION": "us-east-1"})

import boto3  # noqa: E402
from botocore.exceptions import ClientError  # noqa: E402


class FakeTable:
    def __getattr__(self, name):
        def call(*a, **k):
            if name in ("query", "scan", "batch_get_item"):
                return {"Items": [], "Count": 0, "Responses": {}}
            return {}
        return call


class FakePaginator:
    def paginate(self, *a, **k):
        return iter([{"Contents": [], "Items": [], "CommonPrefixes": []}])


class FakeClient:
    def __init__(self, service):
        self.service = service
        self.meta = type("M", (), {"region_name": "us-east-1"})()

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
ARITY_HITS = []
ENTERED = set()
ROOT = os.path.abspath(zip_dir).replace("\\", "/").rstrip("/") + "/"


def _local(frame, event, arg):
    if event == "exception":
        exc_type, exc, _tb = arg
        if issubclass(exc_type, TypeError) and ARITY.search(str(exc)):
            ARITY_HITS.append({"where": "%s:%d" % (os.path.basename(frame.f_code.co_filename)[:-3], frame.f_lineno),
                               "message": str(exc)[:160]})
    return _local


def _tracer(frame, event, arg):
    fn = frame.f_code.co_filename.replace("\\", "/")
    if not fn.startswith(ROOT):
        return None
    if event == "call":
        ENTERED.add((fn, frame.f_code.co_name))
    return _local


def headers(email, firm, user_type="user"):
    import served
    return {"X-Contract-Version": served.CONTRACT_VERSION, "X-Firm-Id": firm, "x-origin-verify": "cloudfront",
            "x-user-email": email, "x-user-role": "user", "x-user-type": user_type}


import served  # noqa: E402  (the zip's own)

if function == "irpt-status":
    import status_installed  # noqa: E402  (the zip's own)
    from read_memo import ReadMemo  # noqa: E402
    clients = {"dynamodb": FakeClient("dynamodb"), "table": ReadMemo(table_factory=lambda: FakeTable()), "s3": FakeClient("s3")}
    boundary = status_installed.build_boundary(status_installed.compose_ports(clients=clients))
else:
    import entry as zip_entry  # noqa: E402  (the zip's own)
    boundary = zip_entry.ENTRY
    # the deps triple and render ports the way the call-site runner (live_call_runner_416.py) stubs them: no AWS read, so the handler reaches
    # enforcer_for -> the Enforcer build and the compute call instead of stopping at a loader's S3 read
    from ids import opaque_firm
    boundary.render_ports = lambda t: (lambda *a, **k: None, lambda *a, **k: None, lambda *a, **k: None)
    boundary.deps = lambda t: ((lambda x: {}), (lambda x: {}), (lambda x: ({}, "rev")))
    boundary.opaque_firm_for = opaque_firm

REQ = "REQ-" + "0" * 24
PARAMS = {"requestId": REQ, "jobId": REQ, "reportId": "report-0", "accountSetId": "set-0"}
routes = [r for r in json.load(open(routes_path, encoding="utf-8"))["routes"] if r["handler"] == function]
PRINCIPALS = (("internal_row_listed", lambda: headers("ops@opalinvest.com", "opal-capital"), {"allowedFirmIds": ["cottonwood"]}),
              ("firm_user_own", lambda: headers("adv@cottonwood.example", "cottonwood"), None))
out = {}
for r in routes:
    rk = r["route_key"]
    names = re.findall(r"\{(\w+)\}", rk)
    res = {}
    for pname, hmake, row in PRINCIPALS:
        del ARITY_HITS[:]
        ENTERED.clear()
        boundary.load_service_profile = (lambda email, _row=row: _row)
        event = {"headers": hmake(), "routeKey": rk, "pathParameters": {n: PARAMS.get(n, "x-0") for n in names},
                 "queryStringParameters": {"selected_tenant": "cottonwood"} if pname == "internal_row_listed" else {}}
        escaped, reply = None, None
        sys.settrace(_tracer)
        try:
            reply = boundary.handle(event)
        except BaseException as exc:  # noqa: BLE001 -- recorded, not hidden
            escaped = type(exc).__name__
        finally:
            sys.settrace(None)
        status = (reply or {}).get("status") or {} if isinstance(reply, dict) else {}
        res[pname] = {"ok": reply.get("ok") if isinstance(reply, dict) else None, "code": status.get("public_reason_code"),
                      "escaped": escaped, "arity_errors": list(ARITY_HITS), "arity_error_count": len(ARITY_HITS),
                      "functions_entered": len(ENTERED)}
    out[rk] = {"operation": r["operation"], "principals": res}
json.dump({"label": label, "function": function, "served_file": served.__file__, "routes": out}, open(out_path, "w", encoding="utf-8"),
          indent=1, sort_keys=True)
print("OK: %s %s routes=%d arity_errors=%d" % (label, function, len(out), sum(p["arity_error_count"] for v in out.values() for p in v["principals"].values())))
