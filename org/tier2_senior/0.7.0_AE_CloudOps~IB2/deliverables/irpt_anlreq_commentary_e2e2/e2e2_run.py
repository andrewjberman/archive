"""IRPT_ANLREQ TO-RUN-COMMENTARY-E2E-2 (the second run, with ONE synthetic named advisor; applier 0.7.0_AE_CloudOps~IB2): ONE fresh synthetic commentary run, steps A to D, in ONE process.

  python e2e_run.py --go          run once; stops at the FIRST red hop; always runs the deletes; writes state_e2e.json (closed codes, counts, keys' SHAPES)
  python e2e_run.py --selftest    the pure helpers on synthetic data (no AWS, no network)

The password is generated in memory and passed to the existing fwd1 mint on stdin; the access token lives in memory only. Nothing secret, no URL, no
signature and no non-synthetic address is written or printed. The API base is imported from the AQ2 sitting module (its constant), never typed here.
Every key is recorded in KEYS the moment it is created; the deletes use only recorded keys (artifact items found by a query on THIS run's REQ id only).
"""
from __future__ import annotations

import base64
import importlib.util
import io
import json
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
STATE_FILE = HERE / "state_e2e2.json"
REGION = "us-east-1"
EMAIL = "fwd1-commentary-e2e2-20261017@opal.invalid"
ADVISOR_DATE = "20261017"
ADVISOR = "irpt-w5-advisor-%s@opal.invalid" % ADVISOR_DATE
ADVISOR_TOOL = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~172/fwd1_advisor.py"
TENANT = "49financial"
HOLDINGS = "Ticker,Dollars,Acct Market Value\nSPY,100,26000000\nAGG,200,32000000\nTIMXX,50,5000000\nAPPL,50,5000000\nZQXWVK,50,5000000\n"
HOLDINGS_SHA = "30d44443701df5f92dfee4def4d1a1f139818ee416601b2577c66e30fb3b96a1"
POLL_STEP_S, POLL_BUDGET_S = 20, 1800
REQ_RE = re.compile(r"REQ-[0-9a-f]{24}")
TCK_RE = re.compile(r"^TCK-\d{8}-[0-9a-f]{8}$")


def utc(t=None):
    return datetime.fromtimestamp(t if t is not None else time.time(), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class Run:
    def __init__(self):
        self.st = {"started_utc": utc(), "hops": {}, "keys": [], "stopped_at": None, "stop_code": None, "journal": []}
        self.keys = self.st["keys"]
        self.token = None
        self.password = None
        self.base = None

    # ---- bookkeeping
    def say(self, msg):
        print("%s %s" % (utc(), msg), flush=True)

    def save(self):
        STATE_FILE.write_text(json.dumps(self.st, indent=1, sort_keys=True) + "\n", encoding="ascii")

    def record(self, kind, **key):
        self.keys.append(dict(kind=kind, **key))
        self.save()

    def hop(self, name, value):
        self.st["hops"][name] = value
        self.say("HOP %s %s" % (name, value))
        self.save()

    def stop(self, hop, code):
        self.st["stopped_at"], self.st["stop_code"] = hop, code
        self.say("STOP at %s code=%s" % (hop, code))
        self.save()

    # ---- http (closed output only)
    def call(self, method, path, body=None, authed=True):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "X-Contract-Version": "v1"}
        if authed and self.token:
            headers["Authorization"] = "Bearer " + self.token
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                status, raw = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            status, raw = e.code, e.read().decode("utf-8", "replace")
        try:
            obj = json.loads(raw)
        except ValueError:
            obj = None
        return status, obj, raw


def closed_code(obj, raw=""):
    """The closed reason words of an answer (UPPER_SNAKE only); never a body."""
    found = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and re.fullmatch(r"[A-Z][A-Z0-9_]{3,}", v) and k in ("public_reason_code", "code", "state", "reason", "error_code", "finding_code"):
                    found.append(v)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    out = []
    for c in found:
        if c not in out:
            out.append(c)
    return ",".join(out[:3]) if out else "NONE"


def selftest():
    assert closed_code({"status": {"public_reason_code": "NOT_AUTHORIZED"}}) == "NOT_AUTHORIZED"
    assert closed_code({"data": {"state": "NORMALIZED"}}) == "NORMALIZED"
    assert closed_code({"x": "free text"}) == "NONE"
    assert REQ_RE.search("x REQ-" + "a" * 24 + " y") and not REQ_RE.search("REQ-short")
    assert TCK_RE.match("TCK-20261017-0123abcd") and not TCK_RE.match("TCK-1")
    import hashlib
    assert hashlib.sha256(HOLDINGS.encode("ascii")).hexdigest() == HOLDINGS_SHA
    print("SELFTEST OK: closed_code, the id shapes, the holdings bytes")
    return 0


def main_run():
    import boto3
    run = Run()
    ddb = boto3.client("dynamodb", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)
    sqs = boto3.client("sqs", region_name=REGION)
    ssm = boto3.client("ssm", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    aq2 = load_module("aq2_r28", "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/sitting_r28.py")
    run.base = aq2.BASE
    mint = load_module("fwd1_mint_e2e", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_mint.py")
    mint.EMAIL, mint.PK = EMAIL, "USER#" + EMAIL  # the existing mint's constants, pointed at this run's one synthetic address (no repo edit)
    ticket_table = ((lam.get_function_configuration(FunctionName="opal-ticket-api").get("Environment") or {}).get("Variables") or {}).get("TABLE_NAME")
    jobs_keys = [k["AttributeName"] for k in ddb.describe_table(TableName="irpt-jobs")["Table"]["KeySchema"]]
    tkeys = [k["AttributeName"] for k in ddb.describe_table(TableName=ticket_table)["Table"]["KeySchema"]]
    run.say("tables resolved: jobs key names %s, ticket table key names %s" % (jobs_keys, tkeys))

    def dlq_depth():
        out = {}
        for tag, name in (("dlq", "outlook-global-commentary-draft-commentary-ready-dlq"), ("main", "outlook-global-commentary-draft-commentary-ready-queue")):
            a = sqs.get_queue_attributes(QueueUrl=sqs.get_queue_url(QueueName=name)["QueueUrl"], AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible"])["Attributes"]
            out[tag] = int(a["ApproximateNumberOfMessages"]) + int(a["ApproximateNumberOfMessagesNotVisible"])
        return out

    run.st["dlq_before"] = dlq_depth()
    req_id = upload_id = input_id = ticket_id = None
    try:
        # ---- A mint
        run.password = secrets.token_urlsafe(32)
        so, sys.stdout = sys.stdout, io.StringIO()
        si, sys.stdin = sys.stdin, io.StringIO(json.dumps({"password": run.password}))
        try:
            rc = mint.cmd_mint()
        finally:
            out, sys.stdout, sys.stdin = sys.stdout.getvalue(), so, si
        run.record("users", table="opal-users-v2", PK="USER#" + EMAIL, SK="PROFILE")
        ok = rc == 0 and "MINT-OK READBACK-OK" in out
        run.hop("A", "mint ok" if ok else "mint REFUSED " + (out.strip().splitlines() or ["?"])[0][:60])
        if not ok:
            return run.stop("A", "MINT_REFUSED") or run
        # ---- A2 advisor mint (the tool's own pre-state refusal applies; remove runs later only if the mint did not refuse at the pre-state)
        adv = subprocess.run([sys.executable, str(ROOT / ADVISOR_TOOL), "mint", "--date", ADVISOR_DATE], capture_output=True, text=True, timeout=300)
        aout = adv.stdout or ""
        run.st["advisor_written"] = "ADVISOR-MINT-REFUSED prestate" not in aout
        if run.st["advisor_written"]:
            run.record("advisor_users", table="opal-users-v2", PK="USER#" + ADVISOR, SK="PROFILE")
            run.record("advisor_partner", table="opal-partner-49financial", email=ADVISOR)
        ok = adv.returncode == 0 and "ADVISOR-MINT-OK" in aout and "ADVISOR-READBACK-OK" in aout
        run.hop("A2", "advisor ok" if ok else "advisor REFUSED " + ((aout.strip().splitlines() or ["?"])[-1].split(" ", 1)[0][:60]))
        if not ok:
            return run.stop("A2", "ADVISOR_" + ("PRESTATE" if not run.st["advisor_written"] else "MINT")) or run
        # ---- L login
        s, obj, raw = run.call("POST", "/auth/login", {"email": EMAIL, "password": run.password}, authed=False)
        run.token = obj.get("accessToken") if isinstance(obj, dict) and obj.get("mfaRequired") is not True else None
        run.hop("L", "login ok" if run.token else "login REFUSED status=%s %s" % (s, closed_code(obj)))
        if not run.token:
            return run.stop("L", "LOGIN_%s" % s) or run
        # ---- U upload (ONE try)
        body = {"upload_token": "e2e-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S"), "filename": "holdings_e2e.csv",
                "file_base64": base64.b64encode(HOLDINGS.encode("ascii")).decode("ascii"), "file_type": "csv"}
        t_u = utc()
        s, obj, raw = run.call("POST", "/api/scoped/investor-reporting/analysis/inputs?selected_tenant=" + TENANT + "&advisor_email=" + ADVISOR, body)
        d = obj.get("data") if isinstance(obj, dict) and isinstance(obj.get("data"), dict) else (obj if isinstance(obj, dict) else {})
        state = d.get("state") if isinstance(d, dict) else None
        upload_id = d.get("upload_id") if isinstance(d, dict) else None
        input_id = d.get("input_id") if isinstance(d, dict) else None
        if upload_id:
            run.record("upload", tenant=TENANT, upload_id=upload_id, input_id=input_id)
        ok = s == 200 and state == "NORMALIZED" and bool(input_id)
        code = state if ok else (closed_code(obj) if closed_code(obj) != "NONE" else "STATUS_%s" % s)
        run.hop("U", "upload ok" if ok else "upload REFUSED %s at %s" % (code, t_u))
        if not ok:
            return run.stop("U", code) or run
        # ---- T ticket
        tb = {"ticket_type": "analysis_request", "title": "SYNTHETIC e2e commentary",
              "answers": {"advisor": "SYNTHETIC e2e advisor", "firm": TENANT, "household": "SYNTHETIC e2e household", "report_type": "Overview"},
              "attachment": {"upload_id": upload_id, "input_id": input_id}}
        s, obj, raw = run.call("POST", "/api/scoped/tickets", tb)
        tk = (obj.get("ticket") or {}) if isinstance(obj, dict) else {}
        ticket_id = tk.get("ticket_id") if isinstance(tk, dict) else None
        if ticket_id:
            run.record("ticket", table=ticket_table, **{tkeys[0]: ticket_id})
        ok = s in (200, 201) and bool(ticket_id and TCK_RE.match(ticket_id))
        run.hop("T", "ticket ok" if ok else "ticket REFUSED status=%s %s" % (s, closed_code(obj)))
        if not ok:
            return run.stop("T", "TICKET_%s" % s) or run
        # ---- S submit (re-login first: the token is short-lived)
        s, obj, raw = run.call("POST", "/auth/login", {"email": EMAIL, "password": run.password}, authed=False)
        run.token = obj.get("accessToken") if isinstance(obj, dict) else run.token
        rid = "e2e-commentary-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%MZ")
        sb = {"request_id": rid, "client_id": None, "account_ids": [], "snapshot_id": None, "variant": "overview", "comparison_keys": [],
              "report_title": "SYNTHETIC commentary e2e", "prepared_for": "Synthetic Test", "input_id": input_id, "ticket_id": ticket_id,
              "commentary_requested": True}
        t_s = time.time()
        s, obj, raw = run.call("POST", "/api/scoped/investor-reporting/analysis?selected_tenant=" + TENANT, sb)
        m = REQ_RE.search(raw or "")
        req_id = m.group(0) if m else None
        ok = s in (200, 201, 202) and bool(req_id) and not (isinstance(obj, dict) and obj.get("ok") is False)
        run.hop("S", ("submit ok " + (req_id or "") if ok else "submit REFUSED status=%s %s" % (s, closed_code(obj))))
        run.st["s_time_utc"] = utc(t_s)
        if req_id:
            run.record("request", table="irpt-requests", tenant=TENANT, request_revision="analysis#%s#1" % req_id)
            run.record("job", table="irpt-jobs", **{jobs_keys[0]: TENANT, jobs_keys[1]: req_id})
        if not ok:
            return run.stop("S", closed_code(obj) if closed_code(obj) != "NONE" else "STATUS_%s" % s) or run
        # ---- P poll (20 s step, 30 minutes total from S)
        green = {}
        sha = None
        last_journal = 0.0
        deadline = t_s + POLL_BUDGET_S
        while time.time() < deadline:
            job = ddb.get_item(TableName="irpt-jobs", Key={jobs_keys[0]: {"S": TENANT}, jobs_keys[1]: {"S": req_id}}, ConsistentRead=True).get("Item")
            if job and job.get("state", {}).get("S") == "READY":
                green.setdefault("P1", utc())
            item = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": "analysis#%s#1" % req_id}}, ConsistentRead=True).get("Item")
            ref = (item or {}).get("commentary_ref", {}).get("M")
            if ref and re.fullmatch(r"[0-9a-f]{64}", ref.get("sha256", {}).get("S", "")):
                sha = ref["sha256"]["S"]
                green.setdefault("P2", utc())
            arts = ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)", FilterExpression="contains(logical_id, :r)",
                             ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "ARTIFACT#"}, ":r": {"S": req_id}}, ConsistentRead=True)["Items"]
            lids = {a.get("logical_id", {}).get("S") for a in arts}
            if req_id in lids:
                green.setdefault("P3", utc())
            if sha and ("%s-commentary-%s" % (req_id, sha)) in lids:
                green.setdefault("P5", utc())
            if "P2" in green and time.time() - last_journal >= 60:
                last_journal = time.time()
                lines = journal_since(ssm, ec2_id(boto3), run.st["s_time_utc"], run)
                run.st["journal"] = lines
                if any("outcome=ATTACHED" in x or "outcome=ALREADY_ATTACHED" in x for x in lines):
                    green.setdefault("P4", utc())
                if any("retained_for_retry" in x for x in lines):
                    run.hop("P4", "retained_for_retry seen")
                    break
            run.st["green"] = green
            run.save()
            if all(k in green for k in ("P1", "P2", "P3", "P4", "P5")):
                break
            time.sleep(POLL_STEP_S)
        run.st["green"] = green
        first_red = next((k for k in ("P1", "P2", "P3", "P4", "P5") if k not in green), None)
        run.hop("POLL", "green=%s first_red=%s" % (sorted(green), first_red))
        if first_red:
            return run.stop(first_red, "RETAINED_FOR_RETRY" if any("retained_for_retry" in x for x in run.st["journal"]) else "NOT_READY_IN_BUDGET") or run
        # ---- R route read (re-login first)
        s, obj, raw = run.call("POST", "/auth/login", {"email": EMAIL, "password": run.password}, authed=False)
        run.token = obj.get("accessToken") if isinstance(obj, dict) else run.token
        s, obj, raw = run.call("GET", "/api/scoped/investor-reporting/analysis/requests/%s/commentary-pdf?selected_tenant=%s" % (req_id, TENANT))
        data = obj.get("data") if isinstance(obj, dict) and isinstance(obj.get("data"), dict) else (obj if isinstance(obj, dict) else {})
        url = ((data or {}).get("download_route") or {}).get("url") if isinstance(data, dict) else None
        if s == 200 and url:
            try:
                with urllib.request.urlopen(urllib.request.Request(url), timeout=120) as r:
                    blob = r.read()
                    ctype = r.headers.get("Content-Type", "?")
                run.st["route"] = {"pass": True, "size": len(blob), "type": ctype.split(";")[0], "pdf": blob[:4] == b"%PDF"}
            except Exception as e:  # noqa: BLE001 -- the type name only; the URL is never printed
                run.st["route"] = {"pass": False, "code": "PDF_FETCH_" + type(e).__name__}
        else:
            run.st["route"] = {"pass": False, "code": closed_code(obj) if closed_code(obj) != "NONE" else "STATUS_%s" % s}
        url = None
        run.hop("R", "route %s" % json.dumps(run.st["route"], sort_keys=True))
        if not run.st["route"].get("pass"):
            run.stop("R", run.st["route"].get("code", "ROUTE_REFUSED"))
        return run
    finally:
        run.token = None
        run.password = None
        try:
            run.st["dlq_after"] = dlq_depth()
        except Exception as e:  # noqa: BLE001
            run.st["dlq_after"] = {"error": type(e).__name__}
        try:
            delete_all(run, ddb, s3, mint, req_id, upload_id, input_id, ticket_id, ticket_table, tkeys, jobs_keys)
        except Exception as e:  # noqa: BLE001 -- the state is saved and the leftover reported, never hidden
            run.st["delete_error"] = type(e).__name__
            run.say("D ERROR %s" % type(e).__name__)
        run.st["finished_utc"] = utc()
        run.save()


def ec2_id(boto3):
    ec2 = boto3.client("ec2", region_name=REGION)
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    return ids[0]


def journal_since(ssm, iid, since_utc, run):
    """The closed IRPT_RESIDENT_PACKAGE lines since the S time: (UTC to the second, outcome=CODE | retained_for_retry class= code=). The script file is saved."""
    script = (
        "set -u\nUNIT=irpt-analysis-resident.service\nSINCE='%s'\n"
        "journalctl -u \"$UNIT\" --since \"$SINCE\" --no-pager -o short-iso -q 2>/dev/null | grep -E 'IRPT_RESIDENT_PACKAGE (outcome=|retained_for_retry)' | awk '{ts=substr($1,1,19); l=$0; m=\"\"; if (match(l, /outcome=[A-Z_]+/)) m=substr(l,RSTART,RLENGTH); else if (match(l, /retained_for_retry class=[A-Za-z_]+ code=([A-Z][A-Z0-9_]*|-)/)) m=substr(l,RSTART,RLENGTH); if (m!=\"\") print \"RAW P4 \" ts \"Z \" m}'\n"
    ) % since_utc.replace("T", " ").replace("Z", "")
    (HERE / "host_p4.sh").write_text(script, encoding="ascii", newline="\n")
    cid = ssm.send_command(InstanceIds=[iid], DocumentName="AWS-RunShellScript", Comment="E2E P4 journal read-only", Parameters={"commands": [script], "executionTimeout": ["120"]}, TimeoutSeconds=300)["Command"]["CommandId"]
    for _ in range(60):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=iid)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            return [ln[4:] for ln in inv.get("StandardOutputContent", "").splitlines() if ln.startswith("RAW P4 ")]
    return []


def delete_all(run, ddb, s3, mint, req_id, upload_id, input_id, ticket_id, ticket_table, tkeys, jobs_keys):
    """Delete exactly the recorded keys (plus the artifact items found by a query on THIS run's REQ id and the upload's own ids), each conditional, each read back ABSENT."""
    run.say("D: deleting recorded keys")
    recorded, absent = 0, 0
    plan = []  # (label, table, key, blobs)
    # discovery by recorded ids only
    if upload_id:
        plan.append(("upload", "irpt-requests", {"tenant": {"S": TENANT}, "request_revision": {"S": "UPLOAD#" + upload_id}}))
        norm = ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)",
                         ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "NORMALIZATION#" + upload_id + "#"}}, ConsistentRead=True)["Items"]
        for it in norm:
            plan.append(("normalization", "irpt-requests", {"tenant": it["tenant"], "request_revision": it["request_revision"]}))
    if input_id:
        plan.append(("input", "irpt-requests", {"tenant": {"S": TENANT}, "request_revision": {"S": "INPUT#" + input_id}}))
    if req_id:
        plan.append(("request", "irpt-requests", {"tenant": {"S": TENANT}, "request_revision": {"S": "analysis#%s#1" % req_id}}))
        plan.append(("job", "irpt-jobs", {jobs_keys[0]: {"S": TENANT}, jobs_keys[1]: {"S": req_id}}))
    if ticket_id:
        plan.append(("ticket", ticket_table, {tkeys[0]: {"S": ticket_id}}))
    # artifact items: by artifact ids read from the recorded upload/input rows, and by a query on this REQ id only
    art_ids = set()
    for label, tbl, key in list(plan):
        if label in ("upload", "input", "normalization"):
            it = ddb.get_item(TableName=tbl, Key=key, ConsistentRead=True).get("Item") or {}
            blob = json.dumps(it)
            art_ids.update(re.findall(r"ART-[0-9a-f]{16,}", blob))
    items = []
    if req_id:
        items += ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)", FilterExpression="contains(logical_id, :r)",
                           ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "ARTIFACT#"}, ":r": {"S": req_id}}, ConsistentRead=True)["Items"]
    for aid in sorted(art_ids):
        it = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": "ARTIFACT#" + aid}}, ConsistentRead=True).get("Item")
        if it and all(it["request_revision"]["S"] != x["request_revision"]["S"] for x in items):
            items.append(it)
    blobs = []
    for it in items:
        plan.append(("artifact", "irpt-requests", {"tenant": it["tenant"], "request_revision": it["request_revision"]}))
        b = (it.get("blob") or {}).get("M") or {}
        if b.get("bucket", {}).get("S") and b.get("key", {}).get("S"):
            blobs.append((b["bucket"]["S"], b["key"]["S"]))
    run.st["delete_plan"] = {"rows": len(plan), "blob_keys": len(blobs)}
    # delete rows (conditional on the recorded key), blobs with every version
    for label, tbl, key in plan:
        recorded += 1
        try:
            ddb.delete_item(TableName=tbl, Key=key, ConditionExpression=" AND ".join("attribute_exists(#k%d)" % i for i in range(len(key))),
                            ExpressionAttributeNames={"#k%d" % i: n for i, n in enumerate(key)})
        except Exception as e:  # noqa: BLE001
            run.say("D %s not deleted: %s" % (label, type(e).__name__))
        gone = ddb.get_item(TableName=tbl, Key=key, ConsistentRead=True).get("Item") is None
        absent += 1 if gone else 0
    for bucket, key in blobs:
        recorded += 1
        try:
            vs = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == key]
            for v in vs:
                s3.delete_object(Bucket=bucket, Key=key, VersionId=v["VersionId"])
        except Exception as e:  # noqa: BLE001
            run.say("D blob not deleted: %s" % type(e).__name__)
        left = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == key]
        absent += 1 if not left else 0
    # the users row through the existing mint's remove (ConsistentRead and the email index, polled)
    recorded += 1
    so, sys.stdout = sys.stdout, io.StringIO()
    try:
        mint.cmd_remove()
    finally:
        out, sys.stdout = sys.stdout.getvalue(), so
    absent += 1 if ("ABSENT GSI" in out and "ABSENT CONSISTENT" in out) else 0
    if run.st.get("advisor_written"):
        recorded += 2
        rem = subprocess.run([sys.executable, str(ROOT / ADVISOR_TOOL), "remove", "--date", ADVISOR_DATE], capture_output=True, text=True, timeout=600)
        rout = rem.stdout or ""
        absent += 1 if ("ABSENT GSI" in rout and "ABSENT CONSISTENT" in rout) else 0
        absent += 1 if "ABSENT PARTNER" in rout else 0
    run.st["deleted"] = {"absent": absent, "recorded": recorded}
    run.say("D deleted %d of %d recorded keys ABSENT" % (absent, recorded))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--go" in sys.argv:
        r = main_run()
        sys.exit(0 if r and not r.st.get("stopped_at") else 1)
    print("USAGE e2e_run.py --selftest | --go")
    sys.exit(2)
