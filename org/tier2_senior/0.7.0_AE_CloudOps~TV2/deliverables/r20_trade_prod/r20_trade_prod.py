"""TCKT_VNEXT TO-R20-PROD3 (cell R20-rv-6, the Trade Request journey ON PROD) -- 0.7.0_AE_CloudOps~TV2.

Order: TCKT_VNEXT.TO-R20-PROD3 (GO msg 10941, the CTO's msg 10936). One synthetic internal filer files ONE Trade Request with ONE synthetic .csv through
the form's own three calls (the upload door, the PUT to the presigned URL, the ticket), opens the ticket's attachment through the page's Open control, and
the SHA-256 of the bytes read back is printed beside the SHA-256 uploaded. After the token's last exp the ticket item (saved whole first), the filer row and
the ONE uploaded object are deleted by exact printed key and read ABSENT (a 404 only).
One process holds the signing key and the one token; the token is never printed, written or traced: it reaches the page only as the body of a stubbed
/auth/refresh response inside one in-memory context. A presigned URL is never printed or traced (path without query only). The engine submit
(/api/general/trades/submit) is never allowed: any such request is aborted and the run STOPs. A PROD head that moves after the start gate is a STOP.
Environment: R20T_HEAD = the origin/PROD head read at the start gate (required); R20T_SHA = the deployed CodeSha256 read at the gate (optional).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import boto3
import jwt as pyjwt
from botocore.exceptions import ClientError

REGION = "us-east-1"
ORIGIN = "https://opalinvest.dev"
HOSTPORT = "opalinvest.dev"
USERS, TICKETS = "opal-users-v2", "opal-tickets"
STAMP = "20261019"
FILER = "tckt-r20-trade-filer-%s@opal.invalid" % STAMP
NAME = "TCKT R20 PROD synthetic trade filer"
FIRM = "cottonwood"
BUCKET = "opal-data-%s" % FIRM
PREFIX = "portal/%s/state/ticket_attachments/trade-form/" % FIRM
FN = "opal-ticket-api"
PROTECTED = {"TCK-20261017-da2a1987", "TCK-20261017-5af976ff", "TCK-20261019-c50b4967"}
PORTAL = "C:/dev/ajb_workspace/portal"
START_HEAD = os.environ["R20T_HEAD"]
LIFE = 300  # 5 minutes; the pair allows at most 20; the journey takes about 1
KEY_SECRET = "opal/auth/jwt-private-key"
FILENAME = "tckt-r20-trade-synthetic.csv"
CONTENT_TYPE = "text/csv"
CONTENT = b"symbol,qty,px\r\nSYN1,100,12.34\r\n"
SENT_RE = re.compile(r"WE_[A-Z_]*SENT\b")

OUT = Path(__file__).resolve().parent
TRACE = OUT / "R20_TRADE_TRACE.json"
RESULT = OUT / "R20_TRADE_RESULT.json"
RECORD = OUT / "R20_TRADE_TICKET_ITEM.json"
SHOT_DIR_REL = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_trade_prod/"

ddb = boto3.client("dynamodb", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)
state = {"written": False, "exp": None, "ticket": None, "key": None, "put_status": None, "readback_sha": None, "prefix_before": None}
trace = {"claim": "measured", "executor": "0.7.0_AE_CloudOps~TV2", "events": [], "blocked_requests": [], "request_census": {}, "statuses": {}}


class Stop(Exception):
    pass


def iso(t=None):
    return dt.datetime.fromtimestamp(time.time() if t is None else t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def say(msg):
    msg = re.sub(r"(https://[^\s?]+)\?\S+", r"\g<1>?<redacted>", str(msg))
    line = "%s %s" % (iso(), msg)
    print(line, flush=True)
    trace["events"].append(line)


def key_of(ident):
    return {"PK": {"S": "USER#" + ident}, "SK": {"S": "PROFILE"}}


def item_of(table, key):
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def prod_head():
    out = subprocess.check_output(["git", "-C", PORTAL, "ls-remote", "origin", "refs/heads/PROD"], text=True).strip()
    return out.split()[0] if out else ""


def check_head(label):
    h = prod_head()
    if h != START_HEAD:
        raise Stop("origin/PROD moved after the start gate (%s): %s is not %s" % (label, h, START_HEAD))
    say("PROD head check (%s): %s unchanged" % (label, h[:12]))


def prefix_count():
    n, tok = 0, None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": PREFIX}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        n += len(r.get("Contents", []))
        tok = r.get("NextContinuationToken")
        if not tok:
            return n


def object_state(key):
    """'present' | 'absent' (a 404 only); anything else raises, a 403 is never absence."""
    try:
        s3.head_object(Bucket=BUCKET, Key=key)
        return "present"
    except ClientError as e:
        code = str(e.response.get("Error", {}).get("Code"))
        status = e.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if code in ("404", "NoSuchKey", "NotFound") and status == 404:
            return "absent"
        raise


def preflight():
    check_head("start")
    import urllib.request
    code, last = None, None
    for attempt in range(1, 4):
        try:
            code = urllib.request.urlopen(ORIGIN + "/", timeout=30).status
            break
        except Exception as e:  # noqa: BLE001 -- a read; a transient reset is retried, never a write
            last = type(e).__name__
            say("GET %s/ attempt %d failed: %s" % (ORIGIN, attempt, last))
            time.sleep(3)
    if code != 200:
        raise Stop("the PROD site does not answer 200 (%s %s)" % (code, last))
    say("GET %s/ -> %s" % (ORIGIN, code))
    cfg = boto3.client("lambda", region_name=REGION).get_function_configuration(FunctionName=FN)
    say("deployed %s CodeSha256=%s State=%s" % (FN, cfg["CodeSha256"], cfg.get("State")))
    if os.environ.get("R20T_SHA") and cfg["CodeSha256"] != os.environ["R20T_SHA"]:
        raise Stop("deployed CodeSha256 differs from the start gate's")
    for t in sorted(PROTECTED - {"TCK-20261019-c50b4967"}):
        if item_of(TICKETS, {"ticket_id": {"S": t}}) is None:
            raise Stop("protected ticket %s is missing before the run" % t)
    if item_of(USERS, key_of(FILER)) is not None:
        raise Stop("the filer row is already PRESENT")
    state["prefix_before"] = prefix_count()
    say("filer key ConsistentRead ABSENT; protected tickets present (read only); %s%s holds %d object(s) before the run (read, never emptied)"
        % (BUCKET + "/", PREFIX, state["prefix_before"]))


def write_row_and_mint():
    item = {"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}, "email": {"S": FILER}, "firmId": {"S": "opal-capital"}, "status": {"S": "active"},
            "userType": {"S": "test-filer"}, "name": {"S": NAME}, "allowedFirmIds": {"L": [{"S": FIRM}]}}
    ddb.put_item(TableName=USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
    state["written"] = True
    back = item_of(USERS, key_of(FILER))
    if back is None or [x["S"] for x in back["allowedFirmIds"]["L"]] != [FIRM] or "scope_all_firms" in back:
        raise Stop("row not PRESENT with the one-firm list after the put")
    say("row written for %s; ConsistentRead PRESENT allowedFirmIds=[%s]" % (FILER.split("@")[0], FIRM))
    pem = boto3.client("secretsmanager", region_name=REGION).get_secret_value(SecretId=KEY_SECRET)["SecretString"]
    iat = int(time.time())
    claims = {"sub": FILER, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal", "role": "user",
              "userType": "test-filer", "name": NAME, "iat": iat, "exp": iat + LIFE}
    token = pyjwt.encode(claims, pem, algorithm="RS256")
    state["exp"] = iat + LIFE
    del pem
    say("token minted for %s (memory only) iat=%s exp=%s life=%ds" % (FILER.split("@")[0], iso(iat), iso(iat + LIFE), LIFE))
    return token


def norm_path(p):
    p = re.sub(r"TCK-[0-9]{8}-[0-9a-f]{8}", "<T>", p)
    return p


def s3_ok(u):
    """True for the one firm bucket under the trade-form prefix (virtual-hosted or path style), never any other S3 address."""
    host = u.netloc.lower()
    if not host.endswith("amazonaws.com"):
        return False
    if host.startswith(BUCKET + "."):
        return u.path.lstrip("/").startswith(PREFIX)
    if host.startswith("s3") and u.path.lstrip("/").startswith(BUCKET + "/" + PREFIX):
        return True
    return False


class Session:
    def __init__(self, browser, token):
        self.allowed, self.violations, self.open_wanted = set(), [], False
        self.s3_put_seen, self.s3_get_seen = 0, 0
        user = {"email": FILER, "name": NAME, "role": "user", "mustChangePassword": False, "firmId": "opal-capital", "userType": "test-filer",
                "advisorId": None, "firmRole": None, "advisorRole": None}
        auth_body = json.dumps({"accessToken": token, "user": user})
        self.ctx = browser.new_context(viewport={"width": 1440, "height": 1000})

        def on_route(route):
            req = route.request
            u = urlparse(req.url)
            rtype = req.resource_type
            k = "%s %s %s" % (req.method, u.netloc.split(".")[0] if u.netloc != HOSTPORT else u.netloc, norm_path(u.path))
            trace["request_census"][k] = trace["request_census"].get(k, 0) + 1
            if u.netloc != HOSTPORT:
                if s3_ok(u):
                    if req.method == "OPTIONS":
                        return route.continue_()
                    if req.method == "PUT" and self.s3_put_seen == 0:
                        self.s3_put_seen += 1
                        return route.continue_()
                    if req.method == "GET" and self.open_wanted and self.s3_get_seen == 0:
                        self.s3_get_seen += 1
                        return route.continue_()
                if rtype in ("font", "stylesheet", "image", "media"):
                    return route.continue_()
                trace["blocked_requests"].append("%s %s %s" % (req.method, u.netloc.split(".")[0], rtype))
                if rtype == "document" and not s3_ok(u):
                    self.violations.append(u.netloc)
                return route.abort()
            p = u.path
            if "/api/general/trades" in p:
                self.violations.append("ENGINE " + p)
                state["engine"] = True
                trace["blocked_requests"].append("%s %s" % (req.method, p))
                return route.abort()
            if p == "/auth/refresh":
                return route.fulfill(status=200, content_type="application/json", body=auth_body)
            if p == "/auth/me":
                return route.fulfill(status=200, content_type="application/json", body=json.dumps({"user": user}))
            if p.startswith(("/api/", "/auth/", "/v1/")):
                if req.method == "GET" and p in ("/api/scoped/tickets", "/api/scoped/tickets/metrics"):
                    return route.continue_()
                if req.method == "POST" and p == "/api/scoped/investor-reporting/directory/resolve":
                    return route.continue_()
                if (req.method, p) in self.allowed or (req.method == "GET" and self.open_wanted and p.endswith("/attachment") and ("GET", "ATTACH") in self.allowed):
                    if (req.method, p) in self.allowed:
                        self.allowed.discard((req.method, p))
                    else:
                        self.allowed.discard(("GET", "ATTACH"))
                    return route.continue_()
                trace["blocked_requests"].append("%s %s" % (req.method, norm_path(p)))
                return route.abort()
            return route.continue_()

        self.ctx.route("**/*", on_route)
        self.page = self.ctx.new_page()

        def on_response(r):
            u = urlparse(r.url)
            m = r.request.method
            if u.netloc == HOSTPORT and m == "POST" and u.path in ("/api/scoped/tickets/attachment-upload", "/api/scoped/tickets"):
                trace["statuses"]["POST %s" % u.path] = r.status
                try:
                    body = r.json()
                except Exception:  # noqa: BLE001
                    body = {}
                if u.path.endswith("attachment-upload") and r.status == 200:
                    att = (body or {}).get("attachment") or {}
                    state["key"] = att.get("key")
                    say("upload door answered %s: object key %s" % (r.status, state["key"]))
                if u.path == "/api/scoped/tickets" and r.status in (200, 201):
                    state["ticket"] = ((body or {}).get("ticket") or {}).get("ticket_id")
            elif u.netloc == HOSTPORT and m == "GET" and u.path.endswith("/attachment") and fs_open_wanted():
                trace["statuses"]["GET open route"] = r.status
                if r.status == 200:
                    try:
                        state["open_url"] = (r.json() or {}).get("url")
                    except Exception:  # noqa: BLE001
                        state["open_url"] = None
            elif s3_ok(u) and m == "PUT":
                trace["statuses"]["PUT s3 trade-form object"] = r.status
                state["put_status"] = r.status

        def fs_open_wanted():
            return self.open_wanted

        self.page.on("response", on_response)

    def tab(self, label):
        pg = self.page
        for loc in (pg.get_by_role("tab", name=label, exact=True), pg.get_by_role("button", name=label, exact=True), pg.get_by_text(label, exact=True)):
            if loc.count():
                loc.first.click()
                return
        raise Stop("board tab %r not found" % label)

    def wait_board(self):
        pg = self.page
        try:
            pg.get_by_role("button", name="Open", exact=True).first.wait_for(state="visible", timeout=60000)
            pg.locator("thead th", has_text="Ticket").first.wait_for(state="visible", timeout=60000)
        except Exception as e:  # noqa: BLE001
            raise Stop("the board did not finish signing in: %s" % type(e).__name__)

    def shot(self, role, locator, results):
        locator.scroll_into_view_if_needed()
        b = locator.bounding_box()
        sx, sy = self.page.evaluate("[window.scrollX, window.scrollY]")
        clip = {"x": max(0, b["x"] + sx - 8), "y": max(0, b["y"] + sy - 8), "width": b["width"] + 16, "height": b["height"] + 16}
        name = "%s__%s__%s__opalinvest-dev.png" % (role, FILER.split("@")[0], state["ticket"] or "no-ticket")
        path = OUT / name
        self.page.screenshot(path=str(path), clip=clip, full_page=True)
        size = path.stat().st_size
        say("SHOT %s saved: %s (%d bytes)" % (role, SHOT_DIR_REL + name, size))
        results[role] = {"path": SHOT_DIR_REL + name, "bytes": size, "viewer": FILER, "origin": ORIGIN}


def ticket_view(tid):
    it = item_of(TICKETS, {"ticket_id": {"S": tid}})
    if it is None:
        raise Stop("ticket not found")
    att = ((it.get("attachment") or {}).get("M")) or {}
    return {"ticket_type": (it.get("ticket_type") or {}).get("S"), "status": (it.get("status") or {}).get("S"),
            "created_by": (it.get("created_by") or {}).get("S"),
            "att_key": (att.get("key") or {}).get("S"), "att_filename": (att.get("filename") or {}).get("S"),
            "att_type": (att.get("content_type") or {}).get("S"), "att_size": (att.get("size") or {}).get("N")}


def we_tokens(tid, since_ms, wait_s):
    names, end = set(), time.time() + wait_s
    while time.time() < end:
        tok = None
        while True:
            kw = {"logGroupName": "/aws/lambda/" + FN, "startTime": since_ms, "filterPattern": '"WE_" "%s"' % tid}
            if tok:
                kw["nextToken"] = tok
            r = logs.filter_log_events(**kw)
            for ev in r.get("events", []):
                names.update(re.findall(r"WE_[A-Z_]+", ev["message"]))
            tok = r.get("nextToken")
            if not tok:
                break
        if names:
            break
        time.sleep(3)
    return sorted(names)


def journey(browser, token, ctx_out):
    fs = Session(browser, token)
    pg = fs.page
    pg.goto(ORIGIN + "/ticket-center", wait_until="domcontentloaded", timeout=60000)
    if urlparse(pg.url).path != "/ticket-center":
        raise Stop("the board did not open (landed on %s)" % urlparse(pg.url).path)
    origin = pg.evaluate("window.location.origin")
    say("PAGE ORIGIN window.location.origin = %s" % origin)
    if origin != ORIGIN or fs.violations:
        raise Stop("page origin %r (violations %s) is not exactly %s" % (origin, fs.violations, ORIGIN))
    ctx_out["origin"] = origin
    fs.wait_board()
    pg.get_by_role("button", name="New Ticket").first.click()
    sel = pg.locator("select").filter(has=pg.locator("option", has_text="Meeting Request")).first
    sel.wait_for(state="visible", timeout=30000)
    options = [t.strip() for t in sel.locator("option").all_inner_texts()]
    say("New Ticket type options recorded (whole, before anything is chosen): %s" % options)
    ctx_out["type_options"] = options
    if not any("trade request" in o.lower() for o in options):
        raise Stop("Trade Request is not listed")
    sel.select_option(label=next(o for o in options if "trade request" in o.lower()))
    firm = pg.locator('select[aria-label="Firm"]')
    firm.wait_for(state="visible", timeout=30000)
    pg.locator('select[aria-label="Firm"] option[value="%s"]' % FIRM).wait_for(state="attached", timeout=60000)
    firm.select_option(value=FIRM)
    pg.locator('input[type="file"][aria-label="Trade request form"]').set_input_files(
        {"name": FILENAME, "mimeType": CONTENT_TYPE, "buffer": CONTENT})
    form = pg.locator('[data-slot="trade-request-form"]')
    pg.locator('[data-slot="trade-file-name"]').wait_for(state="visible", timeout=30000)
    submit = pg.locator('[data-slot="trade-request-submit"]')
    submit.wait_for(state="visible", timeout=30000)
    if not submit.is_enabled():
        raise Stop("the submit is held: the form is incomplete")
    fs.shot("prod_trade_form_filled", form, ctx_out["shots"])  # BEFORE the press
    check_head("before the submit")
    fs.allowed.add(("POST", "/api/scoped/tickets/attachment-upload"))
    fs.allowed.add(("POST", "/api/scoped/tickets"))
    since_ms = int(time.time() * 1000) - 2000
    submit.click()
    notice = pg.get_by_text(re.compile(r"Trade request \S+ filed\.")).first
    try:
        notice.wait_for(state="visible", timeout=90000)
    except Exception as e:  # noqa: BLE001
        err = pg.locator('[data-slot="trade-request-error"]')
        raise Stop("no filed notice after the submit (%s); form error: %s; statuses %s"
                   % (type(e).__name__, err.inner_text() if err.count() else "none", trace["statuses"]))
    tid = re.search(r"Trade request (\S+) filed\.", notice.inner_text()).group(1)
    state["ticket"] = tid
    say("filer: TRADE REQUEST FILED ON PROD %s" % tid)
    say("three HTTP statuses: upload door %s, PUT %s, ticket %s" % (trace["statuses"].get("POST /api/scoped/tickets/attachment-upload"),
                                                                    state["put_status"], trace["statuses"].get("POST /api/scoped/tickets")))
    if state.get("engine"):
        raise Stop("a request to the engine submit was seen (and aborted)")
    if tid in PROTECTED:
        raise Stop("the filed ticket id is a protected ticket")
    v = ticket_view(tid)
    say("ticket %s ConsistentRead: type=%s status=%s created_by=%s attachment key=%s filename=%s type=%s size=%s"
        % (tid, v["ticket_type"], v["status"], v["created_by"], v["att_key"], v["att_filename"], v["att_type"], v["att_size"]))
    if v["ticket_type"] != "trade_request" or v["created_by"] != FILER or not v["att_key"] or v["att_key"] != state["key"]:
        raise Stop("the filed ticket is not a trade_request by the filer carrying the upload door's key")
    if not v["att_key"].startswith(PREFIX) or v["att_key"].endswith("/"):
        raise Stop("the object key is outside the firm's trade-form prefix")
    if object_state(v["att_key"]) != "present":
        raise Stop("the object is not PRESENT after the PUT")
    say("object s3://%s/%s PRESENT (head-object 200)" % (BUCKET, v["att_key"]))
    create_tokens = we_tokens(tid, since_ms, 60)
    say("CREATE log tokens for %s: %s" % (tid, create_tokens))
    if any(SENT_RE.search(t) for t in create_tokens):
        raise Stop("a SENT token was logged on the CREATE: %s" % create_tokens)
    ctx_out["create_tokens"] = create_tokens
    pg.reload(wait_until="domcontentloaded", timeout=60000)
    fs.wait_board()
    fs.tab("Open")
    row = pg.locator("tbody tr").filter(has=pg.locator("td", has_text=tid)).first
    row.wait_for(state="visible", timeout=60000)
    openbtn = row.locator('[data-slot="trade-open-form"]')
    openbtn.wait_for(state="visible", timeout=30000)
    fs.shot("prod_trade_filed", row, ctx_out["shots"])
    check_head("before the open")
    fs.open_wanted = True
    fs.allowed.add(("GET", "ATTACH"))
    openbtn.click()
    end = time.time() + 40
    while time.time() < end and not state.get("open_url"):
        time.sleep(0.5)
    if not state.get("open_url"):
        refused = row.locator('[data-slot="trade-open-refused"]')
        raise Stop("the open route returned no url (status %s); refused text: %s"
                   % (trace["statuses"].get("GET open route"), refused.inner_text() if refused.count() else "none"))
    import urllib.request
    url = state.pop("open_url")
    up = urlparse(url)
    if not s3_ok(up):
        raise Stop("the open route's url is not the firm bucket's trade-form object")
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            body, status = resp.read(), resp.status
    except Exception as e:  # noqa: BLE001 -- the url is never printed
        raise Stop("the presigned read failed: %s" % type(e).__name__)
    del url
    state["readback_sha"] = hashlib.sha256(body).hexdigest()
    state["readback_len"], state["readback_status"], state["readback_path"] = len(body), status, up.path.lstrip("/")
    sha_up = hashlib.sha256(CONTENT).hexdigest()
    say("SHA-256 uploaded : %s (%d bytes)" % (sha_up, len(CONTENT)))
    say("SHA-256 readback : %s (%d bytes, http %s, object path %s)" % (state["readback_sha"], state["readback_len"], state["readback_status"], state["readback_path"]))
    ctx_out["sha_up"] = sha_up
    ctx_out["ticket_view"] = v
    if state.get("engine"):
        raise Stop("a request to the engine submit was seen (and aborted)")
    if state["readback_sha"] != sha_up or state["readback_path"] != v["att_key"]:
        raise Stop("the bytes read back are not the bytes uploaded, or came from another key")


def remove_all():
    if state["exp"] is None:
        return None, None, None, None, None
    wait = state["exp"] + 5 - time.time()
    if wait > 0:
        say("waiting %ds for the token to pass exp %s before anything is removed" % (int(wait), iso(state["exp"])))
        time.sleep(wait)
    tid, key = state["ticket"], state["key"]
    ticket_deleted_at = ticket_absent = None
    if tid:
        item = item_of(TICKETS, {"ticket_id": {"S": tid}})
        if item is not None:
            RECORD.write_text(json.dumps(item, indent=1, default=str, sort_keys=True) + "\n", encoding="utf-8")
            say("ticket record saved whole to %s (%d bytes) BEFORE the delete" % (RECORD.name, RECORD.stat().st_size))
            say("DELETE BY KEY: opal-tickets ticket_id=%s (printed before the delete)" % tid)
            if tid in PROTECTED:
                say("REFUSED: protected ticket id")
            else:
                try:
                    ddb.delete_item(TableName=TICKETS, Key={"ticket_id": {"S": tid}}, ConditionExpression="created_by = :f AND ticket_type = :t",
                                    ExpressionAttributeValues={":f": {"S": FILER}, ":t": {"S": "trade_request"}})
                except ClientError as e:
                    say("ticket delete failed: %s" % e.response["Error"]["Code"])
        ticket_deleted_at = iso()
        ticket_absent = item_of(TICKETS, {"ticket_id": {"S": tid}}) is None
        say("ticket %s deleted at %s; ConsistentRead ABSENT=%s" % (tid, ticket_deleted_at, ticket_absent))
    object_deleted_at = object_absent = None
    if key and key.startswith(PREFIX) and not key.endswith("/"):
        try:
            present = object_state(key)
        except Exception as e:  # noqa: BLE001
            present = "unknown"
            say("object head failed without a 404 (%s): the object is NOT read absent" % type(e).__name__)
        if present == "present":
            ver = s3.get_bucket_versioning(Bucket=BUCKET).get("Status")
            say("DELETE BY KEY: s3://%s/%s (printed before the delete); bucket versioning=%s" % (BUCKET, key, ver))
            r = s3.delete_object(Bucket=BUCKET, Key=key)
            say("delete-object answered: DeleteMarker=%s VersionId=%s" % (r.get("DeleteMarker"), r.get("VersionId")))
        object_deleted_at = iso()
        try:
            object_absent = object_state(key) == "absent"
        except Exception:  # noqa: BLE001
            object_absent = False
        say("object deleted at %s; head-object 404 ABSENT=%s" % (object_deleted_at, object_absent))
    elif key:
        say("REFUSED: the object key %r is not under the trade-form prefix" % key)
    else:
        object_absent = True  # no key was ever returned: no object was created by this run
    try:
        ddb.delete_item(TableName=USERS, Key=key_of(FILER))
    except Exception as e:  # noqa: BLE001
        say("delete filer row failed: %s" % type(e).__name__)
    row_deleted_at = iso()
    row_absent = item_of(USERS, key_of(FILER)) is None
    say("filer row deleted at %s; ConsistentRead ABSENT=%s" % (row_deleted_at, row_absent))
    return row_deleted_at, row_absent, ticket_deleted_at, ticket_absent, (object_deleted_at, object_absent)


def main():
    stop = None
    ctx_out = {"shots": {}}
    pw = browser = None
    try:
        from playwright.sync_api import sync_playwright
        preflight()
        token = write_row_and_mint()
        pw = sync_playwright().start()
        try:
            browser = pw.chromium.launch(channel="msedge", headless=True)
        except Exception:  # noqa: BLE001
            browser = pw.chromium.launch(headless=True)
        journey(browser, token, ctx_out)
        say("MILESTONE JOURNEY_DONE ticket=%s" % state["ticket"])
    except Stop as e:
        stop = "STOP: %s" % e
        say(stop)
    except Exception as e:  # noqa: BLE001
        stop = "STOP (unexpected %s): %s" % (type(e).__name__, re.sub(r"\?\S+", "?<redacted>", str(e))[:300])
        say(stop)
    finally:
        try:
            if browser is not None:
                browser.close()
            if pw is not None:
                pw.stop()
        except Exception:  # noqa: BLE001
            pass
        row_deleted_at = row_absent = ticket_deleted_at = ticket_absent = obj = None
        if state["written"]:
            row_deleted_at, row_absent, ticket_deleted_at, ticket_absent, obj = remove_all()
    object_deleted_at, object_absent = obj if obj else (None, None)
    eng = [k for k in trace["request_census"] if "/api/general/trades" in k]
    TRACE.write_text(json.dumps({"stop": stop, "exp": iso(state["exp"]) if state["exp"] else None, "row_deleted_at": row_deleted_at,
                                 "row_absent_after": row_absent, "ticket_deleted_at": ticket_deleted_at, "ticket_absent_after": ticket_absent,
                                 "object_deleted_at": object_deleted_at, "object_absent_after": object_absent, "start_head": START_HEAD,
                                 "prefix_count_before": state["prefix_before"], "ctx": ctx_out, "engine_requests_seen": eng, "trace": trace},
                                indent=1, default=str) + "\n", encoding="utf-8")
    if stop is None and row_absent and ticket_absent and object_absent and len(ctx_out["shots"]) == 2:
        v = ctx_out["ticket_view"]
        RESULT.write_text(json.dumps({
            "claim": "measured", "browser_origin": ctx_out["origin"],
            "promote_proof": (OUT / "promote_proof.txt").read_text(encoding="utf-8").strip(),
            "filer": FILER, "firm": FIRM, "ticket": state["ticket"], "filename": FILENAME, "content_type": CONTENT_TYPE, "size": len(CONTENT),
            "sha256_uploaded": ctx_out["sha_up"], "sha256_readback": state["readback_sha"], "s3_bucket": BUCKET, "s3_key": state["key"],
            "type_options": ctx_out["type_options"], "shots": ctx_out["shots"],
            "fire_windows_answer": (OUT / "fire_windows_answer.txt").read_text(encoding="utf-8"),
            "token_exp": iso(state["exp"]), "row_deleted_at": row_deleted_at, "ticket_deleted_at": ticket_deleted_at,
            "object_deleted_at": object_deleted_at, "ticket_absent_after": True, "object_absent_after": True, "row_absent_after": True,
            "no_engine_call": not eng and not state.get("engine"), "token_printed": False,
            "http_statuses": {"upload_door": trace["statuses"].get("POST /api/scoped/tickets/attachment-upload"), "put": state["put_status"],
                              "ticket": trace["statuses"].get("POST /api/scoped/tickets")},
            "prefix_count_before": state["prefix_before"], "create_tokens": ctx_out["create_tokens"],
            "blocked_requests_count": len(trace["blocked_requests"]), "stored_attachment": v}, indent=1) + "\n", encoding="utf-8")
        say("result written: %s" % RESULT.name)
        return 0
    say("trace written: %s" % TRACE.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
