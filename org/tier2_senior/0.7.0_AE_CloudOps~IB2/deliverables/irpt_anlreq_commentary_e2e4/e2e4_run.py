"""IRPT_ANLREQ TO-RUN-COMMENTARY-E2E-4 (the fourth run: a FRESH upload token and distinct bytes, the identical request re-posted with the four-minute
backoff while RESOLVING, a two-key Multi-Comp, a route read and ONE sections read; applier 0.7.0_AE_CloudOps~IB2): steps R0 to D in ONE process.

  python e2e4_run.py --selftest   the pure helpers on synthetic data (no AWS, no network)
  python e2e4_run.py --go         R0 (read only; a red mints NOTHING), then A..D; stops at the FIRST red hop; deletes only after the LAST read

The password and the upload token are generated in memory; the access token lives in memory only. Nothing secret, no URL, no signature and no
non-synthetic address is written or printed. The API base is imported from the AQ2 sitting module (its constant), never typed here.
Every key is recorded in KEYS the moment it is created; the deletes use only recorded keys (artifact items found by a query on THIS run's REQ id only).
"""
from __future__ import annotations

import base64
import hashlib
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
STATE_FILE = HERE / "state_e2e4.json"
REGION = "us-east-1"
EMAIL = "fwd1-commentary-e2e4-20261019@opal.invalid"
LEFTOVER_NOTE = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e2/LEFTOVER.txt"
OLD_TOKEN_SHAS = {hashlib.sha256(b"e2e-20261017T204547").hexdigest()}  # the run-2 and run-3 token (recorded in the run-3 driver); an equal token is a STOP
OLD_HOLDINGS_SHAS = {"30d44443701df5f92dfee4def4d1a1f139818ee416601b2577c66e30fb3b96a1"}
ADVISOR_DATE = "20261018"
ADVISOR = "irpt-w5-advisor-%s@opal.invalid" % ADVISOR_DATE
MONDAY_ADVISOR = "irpt-w5-advisor-20261019@opal.invalid"
ADVISOR_TOOL = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~172/fwd1_advisor.py"
TENANT = "49financial"
HOLDINGS = "Ticker,Dollars,Acct Market Value\nSPY,101,26000000\nAGG,200,32000000\nTIMXX,50,5000000\nAPPL,50,5000000\nZQXWVK,50,5000000\n"
HOLDINGS_SHA = "8bfd3093b8ba004b234353359d93925f4e3dd197c9a05ccab826de5e63274215"
FN_WANT = {"irpt-ycharts-generate": "kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE=", "irpt-status": "274dl2bCd2VC3OcX4Uqc4AMbWep65B97F1+CVNoKfMc=",
           "outlook-global-commentary-draft-lambda": "I/6mirBTU5+JPCUUx6Xrmd1bn1vGAjvZTL75LhOm3HY="}
WANT_ROOT = "0485393f3a-r34l"
WAITS = [3, 3, 6, 6, 12, 12, 24, 24, 30, 30, 30, 30, 30]  # sums to 240 s (ADDENDUM 4)
POLL_STEP_S, POLL_BUDGET_S = 20, 1800
YC_QUIET_S = 390
REQ_RE = re.compile(r"REQ-[0-9a-f]{24}")
TCK_RE = re.compile(r"^TCK-\d{8}-[0-9a-f]{8}$")
HOST_R0 = HERE / "host_r0.sh"


def utc(t=None):
    return datetime.fromtimestamp(t if t is not None else time.time(), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def in_forbidden_window(now=None):
    n = now or datetime.now(timezone.utc)
    if n.weekday() < 5 and (11, 30) <= (n.hour, n.minute) <= (14, 15):
        return "weekday band 11:30Z-14:15Z"
    if (n.year, n.month, n.day) == (2026, 10, 20) and (5, 45) <= (n.hour, n.minute) < (7, 0):
        return "gateway resize 05:45Z-07:00Z"
    return None


class Run:
    def __init__(self):
        self.st = {"started_utc": utc(), "hops": {}, "keys": [], "stopped_at": None, "stop_code": None, "journal": [], "r0": {}}
        self.keys = self.st["keys"]
        self.token = None
        self.password = None
        self.base = None

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


def sections_summary(obj):
    """ADDENDUM 5: closed counts and names only. The response may be enveloped under data; keys, counts and ids are returned, never a value."""
    top = sorted(obj.keys()) if isinstance(obj, dict) else []
    d = obj.get("data") if isinstance(obj, dict) and isinstance(obj.get("data"), dict) else obj
    inner = sorted(d.keys()) if isinstance(d, dict) and d is not obj else None
    secs = d.get("sections") if isinstance(d, dict) else None
    secs = secs if isinstance(secs, list) else []
    by = {}
    for s in secs:
        st = s.get("status") if isinstance(s, dict) else None
        by[st] = by.get(st, 0) + 1
    n_bo = sum(1 for s in secs if isinstance(s, dict) and s.get("method") == "BUILDER_ONLY" and s.get("status") != "VALUE")
    n_niv = sum(1 for s in secs if isinstance(s, dict) and s.get("status") == "NOT_AVAILABLE" and s.get("reason") == "NOT_IN_THIS_VERSION")
    disc = d.get("disclosures") if isinstance(d, dict) else None
    ids = [x.get("disclosure_id") for x in disc if isinstance(x, dict)] if isinstance(disc, list) else None
    return {"top_keys": top, "data_keys": inner, "n_sections": len(secs), "by_status": {str(k): v for k, v in sorted(by.items(), key=lambda kv: str(kv[0]))},
            "n_value": by.get("VALUE", 0), "n_not_available": by.get("NOT_AVAILABLE", 0), "n_builder_only_without_value": n_bo, "n_not_in_this_version": n_niv,
            "disclosure_ids": ids, "last_disclosure": (("NOT_SHOWN" if ids and ids[-1] == "NOT_SHOWN" else (ids[-1] if ids else "NONE")) if ids is not None else "NOT-IN-RESPONSE")}


def selftest():
    assert closed_code({"status": {"public_reason_code": "NOT_AUTHORIZED"}}) == "NOT_AUTHORIZED"
    assert closed_code({"x": "free text"}) == "NONE"
    assert REQ_RE.search("x REQ-" + "a" * 24 + " y") and not REQ_RE.search("REQ-short")
    assert TCK_RE.match("TCK-20261019-0123abcd") and not TCK_RE.match("TCK-1")
    assert hashlib.sha256(HOLDINGS.encode("ascii")).hexdigest() == HOLDINGS_SHA and HOLDINGS_SHA not in OLD_HOLDINGS_SHAS
    assert sum(WAITS) == 240
    s = sections_summary({"data": {"sections": [{"method": "BUILDER_ONLY", "status": "VALUE"}, {"method": "BUILDER_ONLY", "status": "NOT_AVAILABLE", "reason": "NOT_IN_THIS_VERSION"}, {"status": "VALUE"}],
                                   "disclosures": [{"disclosure_id": "A"}, {"disclosure_id": "NOT_SHOWN"}]}})
    assert s["n_sections"] == 3 and s["n_value"] == 2 and s["n_builder_only_without_value"] == 1 and s["n_not_in_this_version"] == 1 and s["last_disclosure"] == "NOT_SHOWN"
    assert sections_summary({"data": {"sections": []}})["last_disclosure"] == "NOT-IN-RESPONSE"
    assert in_forbidden_window(datetime(2026, 10, 20, 6, 0, tzinfo=timezone.utc)) and not in_forbidden_window(datetime(2026, 10, 19, 22, 0, tzinfo=timezone.utc))
    print("SELFTEST OK: closed_code, id shapes, holdings bytes, backoff sum, sections summary, windows")
    return 0


def ec2_id(boto3):
    ec2 = boto3.client("ec2", region_name=REGION)
    r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["irpt-ycharts-runner"]}, {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    if len(ids) != 1:
        raise RuntimeError("running irpt-ycharts-runner count %d" % len(ids))
    return ids[0]


def ssm_run(ssm, iid, script, comment, wait_polls=60):
    cid = ssm.send_command(InstanceIds=[iid], DocumentName="AWS-RunShellScript", Comment=comment[:100], Parameters={"commands": [script], "executionTimeout": ["180"]}, TimeoutSeconds=300)["Command"]["CommandId"]
    for _ in range(wait_polls):
        time.sleep(3)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=iid)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            return inv.get("StandardOutputContent", "")
    return ""


def journal_since(ssm, iid, since_utc):
    """The closed IRPT_RESIDENT_PACKAGE lines since the S time: (UTC to the second, outcome=CODE | retained_for_retry class= code=)."""
    script = (
        "set -u\nUNIT=irpt-analysis-resident.service\nSINCE='%s'\n"
        "journalctl -u \"$UNIT\" --since \"$SINCE\" --no-pager -o short-iso -q 2>/dev/null | grep -E 'IRPT_RESIDENT_PACKAGE (outcome=|retained_for_retry)' | awk '{ts=substr($1,1,19); l=$0; m=\"\"; if (match(l, /outcome=[A-Z_]+/)) m=substr(l,RSTART,RLENGTH); else if (match(l, /retained_for_retry class=[A-Za-z_]+ code=([A-Z][A-Z0-9_]*|-)/)) m=substr(l,RSTART,RLENGTH); if (m!=\"\") print \"RAW P4 \" ts \"Z \" m}'\n"
    ) % since_utc.replace("T", " ").replace("Z", "")
    (HERE / "host_p4.sh").write_text(script, encoding="ascii", newline="\n")
    out = ssm_run(ssm, iid, script, "E2E4 P4 journal read-only")
    return [ln[7:] for ln in out.splitlines() if ln.startswith("RAW P4 ")]


def resolve_count(ssm, iid, since_utc):
    """Journal window, total lines scanned, the count of lines containing RESOLVE and the count of 'IRPT_RESIDENT_RESOLVE state=' lines since the first post. Counts only."""
    since = since_utc.replace("T", " ").replace("Z", "")
    script = "\n".join([
        "set -u", "UNIT=irpt-analysis-resident.service", "J=$(mktemp)",
        "journalctl -u \"$UNIT\" --since '" + since + "' --no-pager -o short-iso -q > \"$J\" 2>/dev/null",
        "echo \"RAW RES first=$(head -1 \"$J\" | cut -d' ' -f1) last=$(tail -1 \"$J\" | cut -d' ' -f1) scanned=$(wc -l < \"$J\") resolve_lines=$(grep -c RESOLVE \"$J\" || true) state_lines=$(grep -c 'IRPT_RESIDENT_RESOLVE state=' \"$J\" || true)\"",
        "rm -f \"$J\""]) + "\n"
    (HERE / "host_resolve.sh").write_text(script, encoding="ascii", newline="\n")
    out = ssm_run(ssm, iid, script, "E2E4 RESOLVE count read-only")
    m = re.search(r"RAW RES first=(\S*) last=(\S*) scanned=(\d+) resolve_lines=(\d+) state_lines=(\d+)", out)
    return {"window": "%s..%s" % (m.group(1), m.group(2)), "scanned": int(m.group(3)), "resolve_lines": int(m.group(4)), "state_lines": int(m.group(5))} if m else {"error": "unparsed"}


def original_holdings_key(ddb, upload_id):
    it = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": "UPLOAD#" + upload_id}}, ConsistentRead=True).get("Item") or {}
    for aid in sorted(set(re.findall(r"ART-[0-9a-f]{16,}", json.dumps(it)))):
        a = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": TENANT}, "request_revision": {"S": "ARTIFACT#" + aid}}, ConsistentRead=True).get("Item") or {}
        k = ((a.get("blob") or {}).get("M") or {}).get("key", {}).get("S")
        if k and "/original_holdings/" in k:
            return k
    return None


def r0_reads(run, boto3, ddb, sqs, ssm, lam):
    """R0 (a)-(g), read only. Returns True only when every read is green; a red mints NOTHING."""
    red = []
    r0 = run.st["r0"]
    # (a) clock
    why = in_forbidden_window()
    r0["clock"] = {"utc": utc(), "weekday": datetime.now(timezone.utc).strftime("%A"), "forbidden": why}
    run.say("R0a clock %s %s forbidden_window=%s" % (r0["clock"]["utc"], r0["clock"]["weekday"], why))
    if why:
        red.append("a:" + why)
    # (b) function hashes and the running resident root
    r0["fn"] = {}
    for fn, want in FN_WANT.items():
        got = lam.get_function(FunctionName=fn)["Configuration"]["CodeSha256"]
        r0["fn"][fn] = {"equal": got == want, "got": got if got != want else "(equal)"}
        run.say("R0b %s CodeSha256 equals the order's value: %s%s" % (fn, got == want, "" if got == want else " got " + got))
        if got != want:
            red.append("b:" + fn)
    iid = ec2_id(boto3)
    out = ssm_run(ssm, iid, HOST_R0.read_text(encoding="ascii"), "E2E4 R0 host reads")
    m = re.search(r"RAW R0 resident_root=(\S+) active=(\S+)", out)
    root, active = (m.group(1), m.group(2)) if m else (None, None)
    r0["resident"] = {"root": root, "active": active}
    run.say("R0b resident root %s active=%s (want %s)" % (root, active, WANT_ROOT))
    if root != WANT_ROOT or active != "active":
        red.append("b:resident_root")
    yc = []
    for ln in out.splitlines():
        mm = re.match(r"RAW R0 ycharts_token (\S+) count=(\d+) last=(\S+)", ln)
        if mm:
            yc.append((mm.group(3), mm.group(1), int(mm.group(2))))
    r0["ycharts_tokens"] = [{"token": tk, "count": c, "last": ts} for ts, tk, c in sorted(yc)]
    last_yc = max((ts for ts, _, _ in yc), default=None)
    r0["ycharts_last_utc"] = last_yc
    run.say("R0f last ycharts-mentioning journal line UTC %s (tokens %d)" % (last_yc, len(yc)))
    # (c) API base: the config source name only
    r0["api_source"] = "portal-vite.config.ts-proxy-auth-target"
    vite = (ROOT / "portal/vite.config.ts").read_text(encoding="utf-8")
    host = run.base.split("//", 1)[1]
    r0["api_base_in_vite_proxy"] = host in vite
    run.say("R0c API base is the portal's vite.config.ts proxy target (the API the PROD portal calls): %s; X-Api-Key required: no (runs 1-3 logged in and posted with only the bearer and the contract header)" % r0["api_base_in_vite_proxy"])
    if not r0["api_base_in_vite_proxy"]:
        red.append("c:api_base")
    # (d) TICKET_DL_MAP and notification behaviour
    env = (lam.get_function_configuration(FunctionName="opal-ticket-api").get("Environment") or {}).get("Variables") or {}
    dl = env.get("TICKET_DL_MAP", "")
    r0["ticket_dl_map_empty"] = (dl.strip() in ("", "{}"))
    src = (ROOT / "infra/aws/lambda/ticket_center/lambda_function.py").read_text(encoding="utf-8", errors="replace")
    teams = bool(re.search(r"teams|webhook|slack", src, re.I))
    r0["ticket_service"] = {"teams_or_channel_reference": teams, "email_via_ses_only": "send_raw_email" in src, "dl_refuses_on_empty_map": "refusing to send" in src}
    run.say("R0d TICKET_DL_MAP reads {}: %s; Teams/channel poster in the ticket service source: %s; ticket-created email goes through SES to the DL map only (empty map refuses to send)" % (r0["ticket_dl_map_empty"], teams))
    if not r0["ticket_dl_map_empty"] or teams:
        red.append("d:notify")
    # (e) the three synthetic identities absent
    r0["absent"] = {}
    for label, email in (("user", EMAIL), ("advisor_20261018", ADVISOR), ("advisor_20261019_untouched", MONDAY_ADVISOR)):
        row = ddb.get_item(TableName="opal-users-v2", Key={"PK": {"S": "USER#" + email}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
        gsi = ddb.query(TableName="opal-users-v2", IndexName="email-index", KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": email}}, Select="COUNT")["Count"]
        r0["absent"][label] = {"row_absent": row is None, "email_index_count": gsi}
        run.say("R0e %s: users row absent=%s email-index count=%d" % (label, row is None, gsi))
        if row is not None or gsi != 0:
            red.append("e:" + label)
    # (g) dead letter depth BEFORE
    run.st["dlq_before"] = dlq_depth(sqs)
    run.say("R0g commentary-ready queue depths before %s" % run.st["dlq_before"])
    # (h) token and bytes (the token itself is never written)
    run.token_secret = secrets.token_urlsafe(24)
    th = hashlib.sha256(run.token_secret.encode("ascii")).hexdigest()
    hh = hashlib.sha256(HOLDINGS.encode("ascii")).hexdigest()
    r0["token"] = {"first6": run.token_secret[:6], "sha256": th, "length": len(run.token_secret)}
    r0["holdings_sha256"] = hh
    run.say("R0h token first6 %s sha256 %s length %d; holdings sha256 %s (order %s)" % (r0["token"]["first6"], th, len(run.token_secret), hh, HOLDINGS_SHA))
    if hh != HOLDINGS_SHA or hh in OLD_HOLDINGS_SHAS or th in OLD_TOKEN_SHAS:
        red.append("h:token_or_bytes_equal_to_an_earlier_run")
    run.st["r0"]["red"] = red
    run.save()
    return not red


def dlq_depth(sqs):
    out = {}
    for tag, name in (("dlq", "outlook-global-commentary-draft-commentary-ready-dlq"), ("main", "outlook-global-commentary-draft-commentary-ready-queue")):
        a = sqs.get_queue_attributes(QueueUrl=sqs.get_queue_url(QueueName=name)["QueueUrl"], AttributeNames=["ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible"])["Attributes"]
        out[tag] = int(a["ApproximateNumberOfMessages"]) + int(a["ApproximateNumberOfMessagesNotVisible"])
    return out


def main_run():
    import boto3
    run = Run()
    run.token_secret = None
    ddb = boto3.client("dynamodb", region_name=REGION)
    s3 = boto3.client("s3", region_name=REGION)
    sqs = boto3.client("sqs", region_name=REGION)
    ssm = boto3.client("ssm", region_name=REGION)
    lam = boto3.client("lambda", region_name=REGION)
    aq2 = load_module("aq2_r28", "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/sitting_r28.py")
    run.base = aq2.BASE
    mint = load_module("fwd1_mint_e2e", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_mint.py")
    mint.EMAIL, mint.PK = EMAIL, "USER#" + EMAIL
    ticket_table = ((lam.get_function_configuration(FunctionName="opal-ticket-api").get("Environment") or {}).get("Variables") or {}).get("TABLE_NAME")
    jobs_keys = [k["AttributeName"] for k in ddb.describe_table(TableName="irpt-jobs")["Table"]["KeySchema"]]
    tkeys = [k["AttributeName"] for k in ddb.describe_table(TableName=ticket_table)["Table"]["KeySchema"]]
    req_id = upload_id = input_id = ticket_id = None
    run.st["last_read_utc"] = None
    try:
        # ---- R0 (a red mints NOTHING)
        if not r0_reads(run, boto3, ddb, sqs, ssm, lam):
            run.hop("R0", "RED %s" % run.st["r0"]["red"])
            return run.stop("R0", "R0_RED") or run
        run.hop("R0", "portal-vite.config.ts-proxy-auth-target notify=none xapikey=no")
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
        # ---- A2 advisor mint
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
        # ---- the comparison catalogue (names only) and the two keys
        s, cobj, craw = run.call("GET", "/api/scoped/investor-reporting/analysis/comparisons?selected_tenant=" + TENANT)
        entries = ((cobj.get("data") or {}).get("entries") if isinstance(cobj, dict) and isinstance(cobj.get("data"), dict) else None) or []
        keys2 = [e.get("key") for e in entries if isinstance(e, dict) and isinstance(e.get("key"), str)][:2]
        run.st["catalogue"] = {"status": s, "n_entries": len(entries), "keys_used": keys2}
        run.say("catalogue status=%s entries=%d keys used %s" % (s, len(entries), keys2))
        if s != 200 or len(keys2) != 2:
            return run.stop("U", "CATALOGUE_%s" % s) or run
        # ---- U upload, re-posted while RESOLVING with the ADDENDUM 4 backoff
        body = {"upload_token": run.token_secret, "filename": "holdings_e2e4.csv", "file_base64": base64.b64encode(HOLDINGS.encode("ascii")).decode("ascii"), "file_type": "csv"}
        t_first, posts, state, t_ans = time.time(), 0, None, None
        t_u = utc(t_first)
        run.st["first_post_utc"] = t_u
        while True:
            posts += 1
            s, obj, raw = run.call("POST", "/api/scoped/investor-reporting/analysis/inputs?selected_tenant=" + TENANT + "&advisor_email=" + ADVISOR, body)
            t_ans = time.time()
            d = obj.get("data") if isinstance(obj, dict) and isinstance(obj.get("data"), dict) else (obj if isinstance(obj, dict) else {})
            state = d.get("state") if isinstance(d, dict) else None
            upload_id = (d.get("upload_id") or upload_id) if isinstance(d, dict) else upload_id
            input_id = d.get("input_id") if isinstance(d, dict) else None
            run.say("U post %d answered status=%s state=%s" % (posts, s, state))
            run.st["last_post_utc"] = utc(t_ans)
            if s == 200 and state == "RESOLVING" and posts <= len(WAITS):
                time.sleep(WAITS[posts - 1])
                continue
            break
        run.token_secret = None  # not needed again; never written
        elapsed = int(round(t_ans - t_first))
        run.st["upload_posts"], run.st["upload_elapsed_s"] = posts, elapsed
        if upload_id:
            run.record("upload", tenant=TENANT, upload_id=upload_id, input_id=input_id)
            art_key = original_holdings_key(ddb, upload_id)
            run.st["art_key_recorded"] = bool(art_key)
            run.st["art_key_for_delete"] = art_key
            left = re.search(r"key \(bucket omitted\): (\S+)", (ROOT / LEFTOVER_NOTE).read_text(encoding="ascii"))
            run.st["same_art_key"] = bool(art_key and left and art_key == left.group(1))
        ok = s == 200 and state == "NORMALIZED" and bool(input_id)
        if ok:
            run.st["u_line"] = "ok tries=%d elapsed=%ds" % (posts, elapsed)
            run.hop("U", "upload ok tries=%d elapsed=%ds first_post=%s" % (posts, elapsed, t_u))
        else:
            code = state if (s == 200 and state) else (closed_code(obj) if closed_code(obj) != "NONE" else "STATUS_%s" % s)
            if code == "RESOLVING":
                rl = resolve_count(ssm, ec2_id(boto3), run.st["first_post_utc"])
                nrows = []
                if upload_id:
                    for it in ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)",
                                        ExpressionAttributeValues={":t": {"S": TENANT}, ":p": {"S": "NORMALIZATION#" + upload_id + "#"}}, ConsistentRead=True)["Items"]:
                        da = (it.get("dispatched_at") or {}).get("S") or (it.get("dispatched_at") or {}).get("N")
                        nrows.append({"state": (it.get("state") or {}).get("S"), "dispatched_at_age_s": None})
                        try:
                            if da:
                                t0 = datetime.fromisoformat(da.replace("Z", "+00:00")).timestamp() if not da.replace(".", "").isdigit() else float(da)
                                nrows[-1]["dispatched_at_age_s"] = int(time.time() - t0)
                        except Exception:  # noqa: BLE001
                            nrows[-1]["dispatched_at_age_s"] = "unparsed"
                run.st["resolve"], run.st["normalization_rows"] = rl, nrows
                run.st["u_line"] = "STOP RESOLVING tries=%d elapsed=%ds resolve_lines=%s" % (posts, elapsed, rl.get("resolve_lines"))
            else:
                run.st["u_line"] = "REFUSED %s" % code
            run.hop("U", "upload " + run.st["u_line"] + " first_post=" + t_u)
            return run.stop("U", code) or run
        # ---- T ticket
        tb = {"ticket_type": "analysis_request", "title": "SYNTHETIC e2e commentary",
              "answers": {"advisor": "SYNTHETIC e2e advisor", "firm": TENANT, "household": "SYNTHETIC e2e household", "report_type": "Multi-Comp", "comparison_model": ",".join(keys2)},
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
        # ---- S submit: at least 390 s after the R0(f) YCharts time
        lyc = run.st["r0"].get("ycharts_last_utc")
        if lyc:
            due = datetime.fromisoformat(lyc.replace("Z", "+00:00")).timestamp() + YC_QUIET_S
            while time.time() < due:
                time.sleep(min(20, max(1, due - time.time())))
        s, obj, raw = run.call("POST", "/auth/login", {"email": EMAIL, "password": run.password}, authed=False)
        run.token = obj.get("accessToken") if isinstance(obj, dict) else run.token
        rid = "e2e-commentary-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%MZ")
        sb = {"request_id": rid, "client_id": None, "account_ids": [], "snapshot_id": None, "variant": "multicomp", "comparison_keys": keys2,
              "report_title": "SYNTHETIC commentary e2e", "prepared_for": "Synthetic Test", "input_id": input_id, "ticket_id": ticket_id, "commentary_requested": True}
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
        # ---- P poll (20 s step, 30 minutes from S)
        green, sha, last_journal = {}, None, 0.0
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
                lines = journal_since(ssm, ec2_id(boto3), run.st["s_time_utc"])
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
        # ---- R route read
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
            except Exception as e:  # noqa: BLE001
                run.st["route"] = {"pass": False, "code": "PDF_FETCH_" + type(e).__name__}
        else:
            run.st["route"] = {"pass": False, "code": closed_code(obj) if closed_code(obj) != "NONE" else "STATUS_%s" % s}
        url = None
        run.st["last_read_utc"] = utc()
        run.hop("R", "route %s" % json.dumps(run.st["route"], sort_keys=True))
        if not run.st["route"].get("pass"):
            run.stop("R", run.st["route"].get("code", "ROUTE_REFUSED"))
        return run
    finally:
        try:
            # ---- R2 sections read (ONE try; after R or after a stop at R; only when a REQ exists and the run got that far)
            if req_id and run.st["hops"].get("S", "").startswith("submit ok") and run.st["stopped_at"] in (None, "R"):
                s, obj, raw = run.call("POST", "/auth/login", {"email": EMAIL, "password": run.password}, authed=False) if run.password else (0, None, "")
                run.token = obj.get("accessToken") if isinstance(obj, dict) else run.token
                s, obj, raw = run.call("GET", "/api/scoped/investor-reporting/analysis/%s/sections?selected_tenant=%s" % (req_id, TENANT))
                if s == 200 and isinstance(obj, (dict, list)):
                    run.st["r2"] = dict(sections_summary(obj if isinstance(obj, dict) else {"sections": obj}), status=s)
                else:
                    run.st["r2"] = {"refused": closed_code(obj) if closed_code(obj) != "NONE" else "STATUS_%s" % s, "status": s}
                run.st["last_read_utc"] = utc()
                run.say("R2 %s" % json.dumps(run.st["r2"], sort_keys=True))
        except Exception as e:  # noqa: BLE001
            run.st["r2"] = {"refused": "EXC_" + type(e).__name__}
            run.st["last_read_utc"] = utc()
        run.token = None
        run.password = None
        try:
            run.st["dlq_after"] = dlq_depth(sqs)
        except Exception as e:  # noqa: BLE001
            run.st["dlq_after"] = {"error": type(e).__name__}
        run.st["last_read_utc"] = utc()
        try:
            # ADDENDUM 4: the resident's resolve of this run's upload observed (a state line), or 5 minutes since the last post
            if run.st.get("last_post_utc"):
                lp = datetime.fromisoformat(run.st["last_post_utc"].replace("Z", "+00:00")).timestamp()
                while time.time() < lp + 300:
                    rl = resolve_count(ssm, ec2_id(boto3), run.st["first_post_utc"])
                    if rl.get("state_lines", 0) > 0:
                        run.st["resolve_observed"] = rl
                        break
                    time.sleep(30)
        except Exception as e:  # noqa: BLE001
            run.st["resolve_wait_error"] = type(e).__name__
        try:
            if any(k.get("kind") == "users" for k in run.keys):
                run.st["first_delete_utc"] = utc()
                delete_all(run, ddb, s3, mint, req_id, upload_id, input_id, ticket_id, ticket_table, tkeys, jobs_keys)
            else:
                run.say("D: nothing was minted by this run; nothing is deleted")
                run.st["deleted"] = {"absent": 0, "recorded": 0}
        except Exception as e:  # noqa: BLE001
            run.st["delete_error"] = type(e).__name__
            run.say("D ERROR %s" % type(e).__name__)
        run.st["finished_utc"] = utc()
        run.save()


def delete_all(run, ddb, s3, mint, req_id, upload_id, input_id, ticket_id, ticket_table, tkeys, jobs_keys):
    """Delete exactly the recorded keys (plus the artifact items found by a query on THIS run's REQ id and the upload's own ids), each conditional, each read back ABSENT."""
    run.say("D: deleting recorded keys (first delete %s after last read %s)" % (run.st["first_delete_utc"], run.st["last_read_utc"]))
    recorded, absent = 0, 0
    plan = []
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
    art_ids = set()
    for label, tbl, key in list(plan):
        if label in ("upload", "input", "normalization"):
            it = ddb.get_item(TableName=tbl, Key=key, ConsistentRead=True).get("Item") or {}
            art_ids.update(re.findall(r"ART-[0-9a-f]{16,}", json.dumps(it)))
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
    for label, tbl, key in plan:
        recorded += 1
        try:
            ddb.delete_item(TableName=tbl, Key=key, ConditionExpression=" AND ".join("attribute_exists(#k%d)" % i for i in range(len(key))), ExpressionAttributeNames={"#k%d" % i: n for i, n in enumerate(key)})
        except Exception as e:  # noqa: BLE001
            run.say("D %s not deleted: %s" % (label, type(e).__name__))
        absent += 1 if ddb.get_item(TableName=tbl, Key=key, ConsistentRead=True).get("Item") is None else 0
    for bucket, key in blobs:
        recorded += 1
        try:
            vs = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == key]
            for v in vs:
                s3.delete_object(Bucket=bucket, Key=key, VersionId=v["VersionId"])
        except Exception as e:  # noqa: BLE001
            run.say("D blob not deleted: %s" % type(e).__name__)
            run.st.setdefault("leftover_blob_keys", []).append(key)
        left = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == key]
        absent += 1 if not left else 0
    # the original-holdings blob: the key is recorded; the delete is refused for this principal (AR-y-402 W5 NONE FOUND): tried once, reported if it stays
    ahk = run.st.get("art_key_for_delete")
    if ahk:
        recorded += 1
        bucket = blobs[0][0] if blobs else None
        if bucket is None:
            run.st.setdefault("leftover_blob_keys", []).append(ahk)
        else:
            vs = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=ahk) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == ahk]
            code = None
            try:
                for v in vs:
                    s3.delete_object(Bucket=bucket, Key=ahk, VersionId=v["VersionId"])
            except Exception as e:  # noqa: BLE001
                code = getattr(e, "response", {}).get("Error", {}).get("Code") or type(e).__name__
            left = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=ahk) for v in (pg.get("Versions", []) + pg.get("DeleteMarkers", [])) if v["Key"] == ahk]
            if left:
                run.st.setdefault("leftover_blob_keys", []).append(ahk)
                run.st["leftover_delete_code"] = code or "STILL_PRESENT"
                recorded += 0
            else:
                absent += 1
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
    print("USAGE e2e4_run.py --selftest | --go")
    sys.exit(2)
