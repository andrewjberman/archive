"""IRPT_YCDGEN F1, the seat-driven arm (CTO ruling d54e0b7515): ONE real Cottonwood Overview through the deployed portal route.

    python f1_svc_run.py <holdings.csv> <out.json>

Runs as svc-irpt-analysis@opalinvest.com, the call sequence the portal itself makes (ProspectComposer.tsx / prospect.ts /
ProspectJobStatus.tsx): POST /auth/login; POST .../analysis/inputs?selected_tenant=cottonwood, re-posting the SAME body every
3 s while RESOLVING; POST .../analysis (variant overview); GET .../status/{id} until it leaves LOADING; then the rendered
result read back: GET .../analysis/requests/{id}?include=comparisons,composition and GET .../analysis/{id}/sections.

The password is read by NAME from Secrets Manager into memory and never printed or written. The record keeps no client
figure: every number becomes "<num>", every free string becomes "<str:len>", and only CODE-like strings (A-Z, 0-9, _ . : -)
and ids are kept, so the record shows which sections were worked out and which say they cannot be, with their reason codes.
Ledger irpt-ycdgen-f1-svc-20261008 leg F1. ASCII only.
"""
import base64
import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

import boto3

API = "https://d2n2nzpeqf34ge.cloudfront.net"  # production's same-origin path: CloudFront routes /auth/* and /api/scoped/*
EMAIL = "svc-irpt-analysis@opalinvest.com"
SECRET = "irpt/svc-irpt-analysis/password"
TENANT = os.environ.get("F1_TENANT", "cottonwood")  # st28 seat arm: 49financial (CTO~DELL2 msg 2148); the default keeps st25/st26 runs
BASE = "/api/scoped/investor-reporting"
CODE = re.compile(r"^[A-Z0-9][A-Z0-9_.:-]{0,79}$")
IDLIKE = re.compile(r"^[A-Za-z0-9_-]{8,128}$")
log = []


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def stamp():
    return now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def scrub(v, key=""):
    if isinstance(v, dict):
        return {k: scrub(x, k) for k, x in v.items()}
    if isinstance(v, list):
        return [scrub(x, key) for x in v]
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, (int, float)):
        return "<num>"
    if isinstance(v, str):
        if "token" in key.lower() or "password" in key.lower() or "url" in key.lower():
            return "<redacted>"
        if CODE.match(v) or (IDLIKE.match(v) and ("id" in key.lower() or "ref" in key.lower() or "sha" in key.lower())):
            return v
        if re.match(r"^\d{4}-\d{2}-\d{2}", v) and len(v) <= 32:
            return v
        return "<str:%d>" % len(v)
    return "<%s>" % type(v).__name__


def call(method, path, body, headers, record_body=None):
    req = urllib.request.Request(API + path, data=None if body is None else json.dumps(body).encode(), method=method,
                                 headers=headers)
    started = stamp()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status, raw = r.status, r.read()
    except urllib.error.HTTPError as e:
        status, raw = e.code, e.read()
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except Exception:
        parsed = {"_non_json": raw.decode("utf-8", "replace")[:200]}
    log.append({"at": started, "method": method, "path": path, "status": status,
                "request_body": record_body if record_body is not None else scrub(body),
                "response": scrub(parsed)})
    return status, parsed


def say(*parts):
    print(now().strftime("%H:%M:%SZ"), *parts, flush=True)


def main(argv):
    if argv[1] == "--read":
        return read_only(argv[2], argv[3])
    csv_path, out = argv[1], argv[2]
    data = open(csv_path, "rb").read()
    result = {"principal_role": "the Cottonwood-allowed service principal (svc)", "tenant": TENANT, "api": API,
              "file_sha256": hashlib.sha256(data).hexdigest(), "file_bytes": len(data), "started_at": stamp()}

    def dump(rc):
        result.update(ended_at=stamp(), rc=rc, calls=log)
        json.dump(result, open(out, "w", encoding="utf-8", newline="\n"), indent=1)
        return rc

    password = boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=SECRET)["SecretString"]
    s, login = call("POST", "/auth/login", {"email": EMAIL, "password": password}, {"Content-Type": "application/json"},
                    record_body={"email": "<svc>", "password": "<redacted>"})
    del password
    token = login.get("accessToken") if isinstance(login, dict) else None
    say("login", s, "token present", bool(token))
    if not token:
        return dump(1)
    h = {"Content-Type": "application/json", "Authorization": "Bearer " + token, "X-Contract-Version": "v1"}
    q = "?selected_tenant=" + TENANT
    # E5 (IRPT_BCKEND release 3): a filer whose allowedFirmIds lists the tenant names the firm advisor on the UPLOAD. The email is read
    # from the environment (F1_ADVISOR_EMAIL) and never written to the record; the analysis request stays owned by the submitter.
    advisor = os.environ.get("F1_ADVISOR_EMAIL", "").strip()
    uq = q + ("&advisor_email=" + urllib.parse.quote(advisor) if advisor else "")
    result.update(on_behalf_advisor_named=bool(advisor))
    upload = {"upload_token": "f1dell2-" + uuid.uuid4().hex, "filename": TENANT + "_prospect.csv",
              "file_base64": base64.b64encode(data).decode(), "file_type": "csv", "declared_currency": "USD"}
    shown = dict(upload, file_base64="<%d bytes, sha256 %s>" % (len(data), result["file_sha256"][:16]))
    up = None
    for attempt in range(41):
        s, resp = call("POST", BASE + "/analysis/inputs" + uq, upload, h, record_body=shown)
        log[-1]["path"] = log[-1]["path"].replace(urllib.parse.quote(advisor), "<advisor>") if advisor else log[-1]["path"]
        up = resp.get("data") if isinstance(resp, dict) else None
        state = up.get("state") if isinstance(up, dict) else None
        say("upload attempt", attempt, "HTTP", s, "state", state)
        if state != "RESOLVING":
            break
        time.sleep(3)
    result.update(upload_status=s, upload_state=state, upload_findings=scrub((up or {}).get("findings")))
    if state != "NORMALIZED" or not (up or {}).get("input_id"):
        say("upload did not normalize; no analysis posted")
        return dump(1)
    input_id = up["input_id"]
    request_id = "f1dell2-" + uuid.uuid4().hex[:24]
    body = {"request_id": request_id, "input_id": input_id, "client_id": None, "account_ids": [], "snapshot_id": None,
            "variant": "overview", "comparison_keys": [], "report_title": "F1 dell2 seat-driven Overview",
            "prepared_for": "Opal Capital"}
    s, resp = call("POST", BASE + "/analysis" + q, body, h)
    status = resp.get("status") if isinstance(resp, dict) else None
    result.update(input_id=input_id, request_id=request_id, submit_status=s, submit_state=(status or {}).get("state"),
                  submit_ok=resp.get("ok") if isinstance(resp, dict) else None, submitted_at=stamp())
    say("submit HTTP", s, "state", (status or {}).get("state"))
    if s != 200 and s != 202:
        return dump(1)
    server_id = ((resp.get("data") or {}).get("identity") or {}).get("request_id") if isinstance(resp, dict) else None
    say("server request id", server_id)
    result.update(server_request_id=server_id)
    return poll_and_read(h, q, server_id or request_id, result, dump)


def poll_and_read(h, q, request_id, result, dump):
    sh = dict(h, **{"X-IRPT-Status-Dates": "prospect-v1"})
    st = None
    deadline = time.time() + 1500
    while time.time() < deadline:
        s, resp = call("GET", BASE + "/status/" + request_id + q, None, sh)
        env = resp.get("status") if isinstance(resp, dict) else None
        st = (env or {}).get("state") or (resp.get("data") or {}).get("state") if isinstance(resp, dict) else None
        say("status HTTP", s, "state", st)
        if st not in ("LOADING", "QUEUED", "RUNNING", "PROCESSING", None):
            break
        time.sleep(10)
    result.update(final_state=st, final_at=stamp())
    s1, req = call("GET", BASE + "/analysis/requests/" + request_id + q + "&include=comparisons,composition", None, h)
    s2, sections = call("GET", BASE + "/analysis/" + request_id + "/sections" + q, None, h)
    result.update(request_read_status=s1, sections_read_status=s2, sections=scrub(sections))
    say("read back: request HTTP", s1, "sections HTTP", s2)
    return dump(0 if st == "READY" and s2 == 200 else 1)


def read_only(request_id, out):
    """Polls and reads back an ALREADY-SUBMITTED request by its server id; submits nothing."""
    result = {"principal_role": "the Cottonwood-allowed service principal (svc)", "tenant": TENANT, "api": API,
              "mode": "read-only", "server_request_id": request_id, "started_at": stamp()}

    def dump(rc):
        result.update(ended_at=stamp(), rc=rc, calls=log)
        json.dump(result, open(out, "w", encoding="utf-8", newline="\n"), indent=1)
        return rc

    password = boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=SECRET)["SecretString"]
    s, login = call("POST", "/auth/login", {"email": EMAIL, "password": password}, {"Content-Type": "application/json"},
                    record_body={"email": "<svc>", "password": "<redacted>"})
    del password
    token = login.get("accessToken") if isinstance(login, dict) else None
    say("login", s, "token present", bool(token))
    if not token:
        return dump(1)
    h = {"Content-Type": "application/json", "Authorization": "Bearer " + token, "X-Contract-Version": "v1"}
    q = "?selected_tenant=" + TENANT
    if request_id == "LATEST":
        # The filer's own history (GET .../analysis/requests); the newest accepted request is the one this seat submitted.
        s, hist = call("GET", BASE + "/analysis/requests" + q, None, h)
        found = []

        def walk(node):
            if isinstance(node, dict):
                ident = node.get("identity") if isinstance(node.get("identity"), dict) else {}
                rid = ident.get("request_id") or node.get("request_id")
                at = node.get("accepted_at") or node.get("created_at") or ident.get("accepted_at")
                if isinstance(rid, str) and rid.startswith("REQ-"):
                    found.append((str(at or ""), rid))
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(hist)
        say("history HTTP", s, "requests", len(set(r for _, r in found)))
        if not found:
            return dump(1)
        request_id = max(found)[1]
        result.update(server_request_id=request_id)
        say("latest request", request_id)
    return poll_and_read(h, q, request_id, result, dump)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
