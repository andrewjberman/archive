"""TCKT_VNEXT TO-R18-RUN PART 1 (FWD-11, the Meeting Request) -- 0.7.0_AE_CloudOps~TV2.

Pair : R18_RUN_PAIR.md AMENDMENT 2 (blob 000c3467f5; CTO half 5e89bca0c2, origin half cf7c856072); order AMENDMENTS 5 and 6.
One process holds the signing key, both tokens and the browser contexts. A token is never printed, written or put in a trace: it reaches a page
only as the body of a stubbed /auth/refresh response inside that one in-memory context. The dev server on localhost:5174 is REUSED (AMENDMENT 6):
this script never starts, stops or restarts it.

Phases (gate files in ./gates are written by the applier between phases; the routing window is applied by the applier under safe-apply):
  A  preflight, mint the filer, open the filer browser on localhost:5174, print the page origin, open the Meeting Request form  -> STAGE1_READY
  B  on GO_WINDOW: mint the coordinator                                                                                         -> COORD_MINTED
  C  on WINDOW_OPEN: the filer files ONE Meeting Request; the coordinator confirms ONE proposed time in a second context          -> CONFIRMED
  D  on WINDOW_CLOSED (or at the later exp): wait past BOTH exp, delete both rows, read each ABSENT.
Browser rule: the page may make exactly these API calls -- GET /api/scoped/tickets, GET /api/scoped/tickets/metrics, the directory resolve read,
the filer's one POST /api/scoped/tickets, the coordinator's one POST /api/scoped/tickets/{ticket}/meeting. Every other API-shaped request is aborted
and logged by method and path only. No page content and no other ticket's id or title is recorded.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import boto3
import jwt as pyjwt

REGION = "us-east-1"
ORIGIN = "http://localhost:5174"
HOSTPORT = "localhost:5174"
USERS, TICKETS = "opal-users-v2", "opal-tickets"
FILER = "tckt-r18-filer-20261016@opal.invalid"
COORD = "tckt-r18-coord-20261016@opal.invalid"
FIRM = "cottonwood"
FN = "opal-ticket-api"
EXPECT_SHA = "JwdnACONAnxwqzhsVgqgU+nRoLdmS7MyLmzXmZuXsR4="
JEANETTE = "jeanette@opalinvest.com"
LIFE = 1140  # seconds (19 minutes); the pair allows at most 20 minutes
KEY_SECRET = "opal/auth/jwt-private-key"
TIME_1 = "2026-10-21 14:00 ET (R18 run 20261016)"
TIME_2 = "2026-10-22 10:30 ET (R18 run 20261016)"
WHO = "TCKT R18 synthetic coordinator (test)"
PURPOSE = "Synthetic live run of the Meeting Request. No client data."
SENT_RE = re.compile(r"WE_[A-Z_]*SENT\b")

OUT = Path(__file__).resolve().parent
GATES = OUT / "gates"
TRACE = OUT / "R18_RUN_PART1_TRACE.json"
RESULT = OUT / "R18_RUN_PART1_RESULT.json"

ddb = boto3.client("dynamodb", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)
trace = {"claim": "measured", "executor": "0.7.0_AE_CloudOps~TV2", "server_reused": True, "events": [], "blocked_requests": [],
         "request_census": {}, "external_static_hosts": {}, "statuses": {}}


class Stop(Exception):
    pass


def iso(t=None):
    return dt.datetime.fromtimestamp(time.time() if t is None else t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def say(msg):
    line = "%s %s" % (iso(), msg)
    print(line, flush=True)
    trace["events"].append(line)


def flag(name):
    return (GATES / name).exists()


def wait_flag(name, deadline, label):
    say("MILESTONE waiting for gate %s (%s)" % (name, label))
    while time.time() < deadline:
        if flag("ABORT"):
            raise Stop("ABORT gate written by the applier")
        if flag(name):
            say("gate %s seen" % name)
            return
        time.sleep(1)
    raise Stop("gate %s not written before %s" % (name, iso(deadline)))


def key_of(ident):
    return {"PK": {"S": "USER#" + ident}, "SK": {"S": "PROFILE"}}


def item_of(table, key):
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def routing_of(cfg):
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    return json.loads(env.get("ROUTING_MATRIX") or "{}").get("meeting_request")


def preflight():
    cfg = boto3.client("lambda", region_name=REGION).get_function_configuration(FunctionName=FN)
    say("deployed %s CodeSha256=%s State=%s" % (FN, cfg["CodeSha256"], cfg.get("State")))
    if cfg["CodeSha256"] != EXPECT_SHA:
        raise Stop("deployed CodeSha256 differs from the released package")
    rb = routing_of(cfg)
    say("routing_before meeting_request=%s" % json.dumps(rb))
    if (rb or {}).get("primary") != [JEANETTE]:
        raise Stop("routing before the window is not jeanette alone")
    for who in (FILER, COORD):
        if item_of(USERS, key_of(who)) is not None:
            raise Stop("an identity row is already PRESENT")
    say("both identity keys ConsistentRead ABSENT")
    return rb


def write_row_and_mint(ident, name):
    item = {"PK": {"S": "USER#" + ident}, "SK": {"S": "PROFILE"}, "email": {"S": ident}, "firmId": {"S": "opal-capital"},
            "status": {"S": "active"}, "userType": {"S": "test-filer"}, "name": {"S": name},
            "allowedFirmIds": {"L": [{"S": FIRM}]}}
    ddb.put_item(TableName=USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
    back = item_of(USERS, key_of(ident))
    if back is None or [x["S"] for x in back["allowedFirmIds"]["L"]] != [FIRM] or "scope_all_firms" in back:
        raise Stop("row not PRESENT with the one-firm list after the put")
    say("row written for %s; ConsistentRead PRESENT allowedFirmIds=[%s]" % (ident.split("@")[0], FIRM))
    pem = boto3.client("secretsmanager", region_name=REGION).get_secret_value(SecretId=KEY_SECRET)["SecretString"]
    iat = int(time.time())
    claims = {"sub": ident, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal",
              "role": "user", "userType": "test-filer", "name": name, "iat": iat, "exp": iat + LIFE}
    token = pyjwt.encode(claims, pem, algorithm="RS256")
    del pem
    say("token minted for %s (held in memory only) iat=%s exp=%s life=%ds" % (ident.split("@")[0], iso(iat), iso(iat + LIFE), LIFE))
    return token, iat, iat + LIFE


def norm_path(p, tids):
    for t in tids:
        p = p.replace(t, "<T>")
    return re.sub(r"TCK-[0-9]{8}-[0-9a-f]{8}", "<T>", p)


def open_session(browser, ident, name, token, allowed, tids):
    """One browser context signed in as `ident` via a stubbed /auth/refresh. `allowed` is a mutable set of (method, path) writes."""
    user = {"email": ident, "name": name, "role": "user", "mustChangePassword": False, "firmId": "opal-capital",
            "userType": "test-filer", "advisorId": None, "firmRole": None, "advisorRole": None}
    auth_body = json.dumps({"accessToken": token, "user": user})
    ctx = browser.new_context(viewport={"width": 1440, "height": 1000})
    violations = []

    def census(req):
        u = urlparse(req.url)
        k = "%s %s %s" % (req.method, u.netloc, norm_path(u.path, tids))
        trace["request_census"][k] = trace["request_census"].get(k, 0) + 1

    def on_route(route):
        req = route.request
        u = urlparse(req.url)
        rtype = req.resource_type
        census(req)
        if u.netloc != HOSTPORT:
            if rtype in ("font", "stylesheet", "image", "media"):
                trace["external_static_hosts"][u.netloc] = trace["external_static_hosts"].get(u.netloc, 0) + 1
                return route.continue_()
            trace["blocked_requests"].append("%s %s %s" % (req.method, u.netloc, rtype))
            if rtype == "document":
                violations.append(u.netloc)
            return route.abort()
        p = u.path
        if p == "/auth/refresh":
            return route.fulfill(status=200, content_type="application/json", body=auth_body)
        if p == "/auth/me":
            return route.fulfill(status=200, content_type="application/json", body=json.dumps({"user": user}))
        if p.startswith(("/api/", "/auth/", "/v1/")):
            if req.method == "GET" and p in ("/api/scoped/tickets", "/api/scoped/tickets/metrics"):
                return route.continue_()
            if req.method == "POST" and p == "/api/scoped/investor-reporting/directory/resolve":
                return route.continue_()  # the firm list read the form needs; a read
            if (req.method, p) in allowed:
                allowed.discard((req.method, p))
                trace["statuses"]["sent " + req.method + " " + norm_path(p, tids)] = "sent"
                return route.continue_()
            trace["blocked_requests"].append("%s %s" % (req.method, norm_path(p, tids)))
            return route.abort()
        return route.continue_()

    ctx.route("**/*", on_route)
    page = ctx.new_page()

    def on_response(r):
        p = urlparse(r.url).path
        if r.request.method == "POST" and p.startswith("/api/scoped/tickets"):
            trace["statuses"]["http POST " + norm_path(p, tids)] = r.status

    page.on("response", on_response)
    return ctx, page, violations


def wait_board(page):
    t0 = time.time()
    try:
        page.get_by_role("button", name="Open", exact=True).first.wait_for(state="visible", timeout=60000)
        page.locator("thead th", has_text="Ticket").first.wait_for(state="visible", timeout=60000)
    except Exception as e:  # noqa: BLE001
        txt = ""
        try:
            txt = page.locator("body").inner_text(timeout=3000)
        except Exception:  # noqa: BLE001
            pass
        flags = [w for w in ("Something went wrong", "Tickets could not be loaded", "Sign in", "Loading") if w in txt]
        raise Stop("the board did not finish signing in: %s flags=%s path=%s" % (type(e).__name__, flags, urlparse(page.url).path))
    say("board signed in after %.1fs" % (time.time() - t0))


def check_origin(page, violations, label):
    origin = page.evaluate("window.location.origin")
    say("PAGE ORIGIN (%s) window.location.origin = %s" % (label, origin))
    if origin != ORIGIN or violations:
        raise Stop("page origin %r (violations %s) is not exactly %s" % (origin, violations, ORIGIN))
    return origin


def ticket_view(tid):
    it = item_of(TICKETS, {"ticket_id": {"S": tid}})
    if it is None:
        raise Stop("ticket not found")
    meeting = (it.get("meeting") or {}).get("M") or {}
    routing = (it.get("routing") or {}).get("M") or {}
    return {"ticket_type": (it.get("ticket_type") or {}).get("S"), "status": (it.get("status") or {}).get("S"),
            "primary": [x.get("S") for x in (routing.get("primary") or {}).get("L", [])],
            "created_by": (it.get("created_by") or {}).get("S"),
            "meeting": {k: (v.get("S") if "S" in v else None) for k, v in meeting.items() if k in ("status", "time", "by")}}


def we_tokens(tid, since_ms, wait_s=75):
    """Every WE_* token the ticket service logged for this ticket since the click (read-only filter on the function's log group)."""
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


def phase_a(browser, filer_token, f_exp):
    allowed = set()
    ctx, page, violations = open_session(browser, FILER, "TCKT R18 synthetic filer", filer_token, allowed, [])
    page.goto(ORIGIN + "/ticket-center", wait_until="domcontentloaded", timeout=60000)
    if urlparse(page.url).path != "/ticket-center":
        raise Stop("the board did not open (landed on %s)" % urlparse(page.url).path)
    origin = check_origin(page, violations, "filer")
    wait_board(page)
    page.get_by_role("button", name="New Ticket").first.click()
    sel = page.locator("select").filter(has=page.locator("option", has_text="Meeting Request")).first
    sel.wait_for(state="visible", timeout=30000)
    sel.select_option(label="Meeting Request")
    firm = page.locator('select[aria-label="Firm"]')
    firm.wait_for(state="visible", timeout=30000)
    try:
        page.locator('select[aria-label="Firm"] option[value="%s"]' % FIRM).wait_for(state="attached", timeout=60000)
    except Exception as e:  # noqa: BLE001
        raise Stop("the firm list did not offer %s: %s" % (FIRM, type(e).__name__))
    firm.select_option(value=FIRM)
    say("filer: Meeting Request form open, firm %s chosen from the served list (no write made)" % FIRM)
    return ctx, page, allowed, violations, origin


def phase_c(browser, filer_page, filer_allowed, filer_violations, coord_token):
    # the filer fills and submits ONE ticket
    filer_page.get_by_label("Who", exact=True).fill(WHO)
    filer_page.get_by_label("Purpose", exact=True).fill(PURPOSE)
    filer_page.get_by_label("Proposed time 1", exact=True).fill(TIME_1)
    filer_page.get_by_label("Proposed time 2", exact=True).fill(TIME_2)
    submit = filer_page.locator('[data-slot="meeting-request-submit"]')
    submit.wait_for(state="visible", timeout=30000)
    if not submit.is_enabled():
        raise Stop("the submit is held: the form is incomplete")
    filer_allowed.add(("POST", "/api/scoped/tickets"))
    since_ms = int(time.time() * 1000) - 2000
    submit.click()
    notice = filer_page.get_by_text(re.compile(r"Meeting request \S+ filed\.")).first
    try:
        notice.wait_for(state="visible", timeout=60000)
    except Exception as e:  # noqa: BLE001
        raise Stop("no filed notice after the submit (%s); post statuses %s" % (type(e).__name__, trace["statuses"]))
    m = re.search(r"Meeting request (\S+) filed\.", notice.inner_text())
    mt = m.group(1)
    say("filer: MEETING TICKET FILED %s" % mt)
    v = ticket_view(mt)
    say("ticket %s read by ConsistentRead: type=%s status=%s routing.primary=%s created_by=%s" % (mt, v["ticket_type"], v["status"], v["primary"], v["created_by"]))
    if v["ticket_type"] != "meeting_request" or v["status"] != "open":
        raise Stop("the filed ticket is not an open meeting_request")
    if v["primary"] != [COORD]:
        raise Stop("the stored routing.primary is not the synthetic coordinator alone")
    tokens_create = we_tokens(mt, since_ms)
    say("CREATE log tokens for %s: %s" % (mt, tokens_create))
    if any(SENT_RE.search(t) for t in tokens_create):
        raise Stop("a SENT token was logged on the CREATE: %s" % tokens_create)
    # the coordinator confirms ONE of the two times in a second context
    c_allowed = set()
    cctx, cpage, cviol = open_session(browser, COORD, "TCKT R18 synthetic coordinator", coord_token, c_allowed, [mt])
    cpage.goto(ORIGIN + "/ticket-center", wait_until="domcontentloaded", timeout=60000)
    check_origin(cpage, cviol, "coordinator")
    wait_board(cpage)
    btn = cpage.get_by_role("button", name="Confirm " + TIME_1, exact=True)
    try:
        btn.wait_for(state="visible", timeout=60000)
    except Exception as e:  # noqa: BLE001
        raise Stop("the coordinator does not see the confirm control for the filed ticket: %s" % type(e).__name__)
    c_allowed.add(("POST", "/api/scoped/tickets/%s/meeting" % mt))
    since_ms = int(time.time() * 1000) - 2000
    with cpage.expect_response(lambda r: r.request.method == "POST" and r.url.endswith("/%s/meeting" % mt), timeout=60000) as ri:
        btn.click()
    say("coordinator: CONFIRM pressed for the first proposed time; http=%s" % ri.value.status)
    after = ticket_view(mt)
    say("ticket %s after the confirm: status=%s meeting=%s" % (mt, after["status"], after["meeting"]))
    if (after["meeting"].get("status"), after["meeting"].get("time"), after["meeting"].get("by"), after["status"]) != ("confirmed", TIME_1, COORD, "open"):
        raise Stop("the stored meeting outcome is not confirmed by the coordinator at the clicked time with the ticket still open")
    tokens_confirm = we_tokens(mt, since_ms, wait_s=20)
    say("CONFIRM log tokens for %s: %s" % (mt, tokens_confirm))
    if any(SENT_RE.search(t) for t in tokens_confirm):
        raise Stop("a SENT token was logged on the confirm: %s" % tokens_confirm)
    cctx.close()
    return {"mt_ticket": mt, "mt_confirmed_time": TIME_1, "ticket_after": after, "create_tokens": tokens_create, "confirm_tokens": tokens_confirm,
            "coordinator_http": ri.value.status, "violations": violations_of(filer_violations, cviol)}


def violations_of(a, b):
    return sorted(set(a) | set(b))


def remove_rows(exps):
    wait = max(exps) + 5 - time.time()
    if wait > 0:
        say("waiting %ds for BOTH tokens to pass exp (later exp %s) before the rows are removed" % (int(wait), iso(max(exps))))
        time.sleep(wait)
    for who in (FILER, COORD):
        try:
            ddb.delete_item(TableName=USERS, Key=key_of(who))
        except Exception as e:  # noqa: BLE001
            say("delete %s failed: %s" % (who.split("@")[0], type(e).__name__))
    deleted_at = iso()
    absent = all(item_of(USERS, key_of(who)) is None for who in (FILER, COORD))
    say("rows deleted at %s; ConsistentRead ABSENT (both)=%s" % (deleted_at, absent))
    return deleted_at, absent


def main():
    GATES.mkdir(exist_ok=True)
    stop = None
    exps, written = [], []
    out = {}
    rb = None
    pw = browser = None
    try:
        from playwright.sync_api import sync_playwright

        rb = preflight()
        filer_token, f_iat, f_exp = write_row_and_mint(FILER, "TCKT R18 synthetic filer")
        written.append(FILER)
        exps.append(f_exp)
        pw = sync_playwright().start()
        try:
            browser = pw.chromium.launch(channel="msedge", headless=True)
        except Exception:  # noqa: BLE001
            browser = pw.chromium.launch(headless=True)
        fctx, fpage, fallowed, fviol, origin = phase_a(browser, filer_token, f_exp)
        out["browser_origin"] = origin
        say("MILESTONE STAGE1_READY filer token exp %s" % iso(f_exp))
        wait_flag("GO_WINDOW", f_exp - 420, "applier checks the plan is ONE attribute change")
        coord_token, c_iat, c_exp = write_row_and_mint(COORD, "TCKT R18 synthetic coordinator")
        written.append(COORD)
        exps.append(c_exp)
        say("MILESTONE COORD_MINTED coordinator token exp %s" % iso(c_exp))
        wait_flag("WINDOW_OPEN", f_exp - 240, "applier applies the window and reads ROUTING_MATRIX back")
        cfg = boto3.client("lambda", region_name=REGION).get_function_configuration(FunctionName=FN)
        during = routing_of(cfg)
        say("routing_during (read by this process) meeting_request=%s" % json.dumps(during))
        if (during or {}).get("primary") != [COORD]:
            raise Stop("the live routing primary is not the synthetic coordinator alone")
        out.update(phase_c(browser, fpage, fallowed, fviol, coord_token))
        out["routing_during_seen"] = during
        say("MILESTONE CONFIRMED mt_ticket=%s" % out["mt_ticket"])
        fctx.close()
    except Stop as e:
        stop = "STOP: %s" % e
        say(stop)
        say("MILESTONE STOPPED the applier must close the window FIRST if it is open")
    except Exception as e:  # noqa: BLE001
        stop = "STOP (unexpected %s): %s" % (type(e).__name__, str(e)[:300])
        say(stop)
        say("MILESTONE STOPPED the applier must close the window FIRST if it is open")
    finally:
        try:
            if browser is not None:
                browser.close()
            if pw is not None:
                pw.stop()
        except Exception:  # noqa: BLE001
            pass
        if flag("WINDOW_OPEN") and not flag("WINDOW_CLOSED"):
            say("MILESTONE WINDOW-STILL-OPEN waiting for WINDOW_CLOSED before the rows are removed")
            end = (max(exps) if exps else time.time()) + 600
            while time.time() < end and not flag("WINDOW_CLOSED"):
                time.sleep(2)
        deleted_at, absent = (None, None)
        if written:
            deleted_at, absent = remove_rows(exps)
    eng = [k for k in trace["request_census"] if "/api/general/trades" in k]
    doc = {"stop": stop, "iat_exp": [iso(x) for x in exps], "row_deleted_at": deleted_at, "row_absent_after": absent, "routing_before": rb,
           "out": out, "engine_requests_seen": eng, "trace": trace}
    TRACE.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    if stop is None and absent and out.get("mt_ticket"):
        RESULT.write_text(json.dumps({
            "claim": "measured", "identity": FILER, "mt_filer": FILER, "coordinator_identity": COORD, "firm": FIRM, "mt_ticket": out["mt_ticket"],
            "mt_confirmed_time": out["mt_confirmed_time"], "browser_origin": out["browser_origin"], "token_exp": iso(max(exps)),
            "row_deleted_at": deleted_at, "row_absent_after": True, "no_engine_call": not eng, "token_printed": False, "server_reused": True,
            "create_tokens": out["create_tokens"], "confirm_tokens": out["confirm_tokens"], "routing_before": rb,
            "routing_during": out["routing_during_seen"], "blocked_requests_count": len(trace["blocked_requests"])}, indent=1) + "\n", encoding="utf-8")
        say("result written: %s" % RESULT.name)
        return 0
    say("trace written: %s" % TRACE.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
