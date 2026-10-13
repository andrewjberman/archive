"""TCKT_VNEXT R16-cw-2 -- one crawl sitting closes two cottonwood test tickets (0.7.0_AE_CloudOps~TV2).

Order  : TCKT_VNEXT.TO-RUN-R16-cw2 (steps 1 to 7 of R2_CW1_CRAWL_PAIR.md + COO AMENDMENT 1; CTO half @4fea908a37).
Process: ONE process holds the signing key, the token and the browser context. The token is never printed, written or put in a
         trace; it reaches the page only as the body of a mocked /auth/refresh response inside the one in-memory context.

Browser rule: the page may make exactly these requests to the API -- GET /api/scoped/tickets, GET /api/scoped/tickets/metrics, and
POST claim / complete for the ticket the script is about to press. Every other API-shaped request (fetch/xhr/ping) is aborted and
logged by method + path only. No page content, no other ticket's id or title is recorded: a row is read only for the target id.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import boto3
import jwt as pyjwt

REGION = "us-east-1"
HOST = "d2n2nzpeqf34ge.cloudfront.net"
BASE = "https://" + HOST
USERS, TICKETS = "opal-users-v2", "opal-tickets"
IDENT = "tckt-r2-crawler-20261013@opal.invalid"
NAME = "TCKT_VNEXT R2 one-ticket crawler"
FIRMS = ["cottonwood"]
T1, T2 = "TCK-20261009-a1052909", "TCK-20261012-13cd3a1d"
OTHER_FIRM_TICKET = "TCK-20261009-67ab7f27"  # a 49financial ticket: GET must be 404 (the pair's one-firm proof)
FN = "opal-ticket-api"
EXPECT_SHA = "4sDK8P5mtgodi1IkSfaFQZi1YgmJq6URLeypEcaULu8="
LIFE = 720  # seconds; the run is about 4 minutes, the pair says run + 5 minutes and never more than 20
MIN_LEFT_FOR_SECOND = 180
KEY_SECRET = "opal/auth/jwt-private-key"
RESOLUTION = "[TEST] R16-cw-2 crawl close"

OUT = Path(__file__).resolve().parent
RESULT = OUT / "R16_CRAWL_RESULT_20261013.json"
STOPFILE = OUT / "R16_CRAWL_STOP_20261013.json"
if STOPFILE.exists():
    STOPFILE = OUT / "R16_CRAWL_STOP_20261013_S2.json"

ddb = boto3.client("dynamodb", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)
trace = {"claim": "measured", "executor": "0.7.0_AE_CloudOps~TV2", "events": [], "blocked_requests": []}


class Stop(Exception):
    pass


def iso(t=None):
    if t is None:
        t = time.time()
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def say(msg):
    line = "%s %s" % (iso(), msg)
    print(line, flush=True)
    trace["events"].append(line)


def item_of(table, key):
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def ticket_state(tid):
    it = item_of(TICKETS, {"ticket_id": {"S": tid}})
    if it is None:
        raise Stop("ticket %s not found" % tid)
    asg = it.get("assignee") or {}
    return {"status": it["status"]["S"], "assignee": asg.get("S"), "created_by": (it.get("created_by") or {}).get("S"),
            "firm": ((it.get("requester") or {}).get("M", {}).get("firm") or {}).get("S"),
            "email_has_at": "@" in (((it.get("requester") or {}).get("M", {}).get("email") or {}).get("S") or ""),
            "events": len((it.get("events") or {}).get("L", []))}


def row_key():
    return {"PK": {"S": "USER#" + IDENT}, "SK": {"S": "PROFILE"}}


# ------------------------------------------------------------------ steps 1 to 3

def preconditions():
    cfg = boto3.client("lambda", region_name=REGION).get_function_configuration(FunctionName=FN)
    say("deployed %s CodeSha256=%s State=%s" % (FN, cfg["CodeSha256"], cfg.get("State")))
    if cfg["CodeSha256"] != EXPECT_SHA:
        raise Stop("deployed CodeSha256 differs from the one member-diffed against the tree")
    before = {}
    for tid in (T1, T2):
        s = ticket_state(tid)
        before[tid] = s
        say("%s prior status=%s assignee=%s created_by=%s firm=%s requester_email_has_at=%s"
            % (tid, s["status"], s["assignee"], s["created_by"], s["firm"], s["email_has_at"]))
        if (s["status"], s["assignee"], s["created_by"], s["firm"]) != ("open", None, "svc-commentary", "cottonwood"):
            raise Stop("%s is not open/unassigned/svc-commentary/cottonwood" % tid)
        if s["email_has_at"]:
            raise Stop("%s requester email is a deliverable-shaped address; the claim could mail a person" % tid)
    if item_of(USERS, row_key()) is not None:
        raise Stop("identity row already PRESENT")
    say("identity key ConsistentRead ABSENT")
    return cfg["CodeSha256"], before


def write_row_and_mint():
    item = {"PK": {"S": "USER#" + IDENT}, "SK": {"S": "PROFILE"}, "email": {"S": IDENT}, "firmId": {"S": "opal-capital"},
            "status": {"S": "active"}, "userType": {"S": "test-filer"}, "name": {"S": NAME},
            "allowedFirmIds": {"L": [{"S": f} for f in FIRMS]}}
    ddb.put_item(TableName=USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
    back = item_of(USERS, row_key())
    if back is None or [x["S"] for x in back["allowedFirmIds"]["L"]] != FIRMS:
        raise Stop("row not PRESENT with the expected list after the put")
    say("row written; ConsistentRead PRESENT allowedFirmIds=%s" % FIRMS)
    pem = boto3.client("secretsmanager", region_name=REGION).get_secret_value(SecretId=KEY_SECRET)["SecretString"]
    iat = int(time.time())
    claims = {"sub": IDENT, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal",
              "role": "user", "userType": "test-filer", "name": NAME, "iat": iat, "exp": iat + LIFE}
    token = pyjwt.encode(claims, pem, algorithm="RS256")
    del pem
    say("token minted (held in memory only) iat=%s exp=%s life=%ds" % (iso(iat), iso(iat + LIFE), LIFE))
    return token, iat, iat + LIFE


def api(token, method, path):
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("x-contract-version", "v1")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def one_firm_proof(token):
    st, body = api(token, "GET", "/api/scoped/tickets")
    firms, n = set(), 0
    if st == 200:
        lst = json.loads(body.decode("utf-8", "replace")).get("tickets") or []
        n = len(lst)
        firms = {(t.get("requester") or {}).get("firm") for t in lst if isinstance(t, dict)}
    say("one-firm proof: GET /api/scoped/tickets -> %s, %d ticket(s), distinct requester.firm=%s" % (st, n, sorted(map(str, firms))))
    if st != 200 or firms - {"cottonwood"}:
        raise Stop("list is not clamped to cottonwood")
    st2, _ = api(token, "GET", "/api/scoped/tickets/" + OTHER_FIRM_TICKET)
    say("one-firm proof: GET of one 49financial ticket id -> %s" % st2)
    if st2 != 404:
        raise Stop("a 49financial ticket is not 404 for the identity")
    say("one-firm proof: no data-refresh probe (CTO v2.2 AMENDMENT 1 @133952758b dropped it: that gate admits any Opal-internal "
        "caller, row TCKT_VNEXT-D2-S17); zero calls are proven from the log group in step 6")
    return {"list_status": st, "list_count": n, "list_firms": sorted(map(str, firms)), "foreign_ticket_status": st2,
            "data_refresh_probe": "not run (CTO ruling; zero-call read in step 6)"}


# ------------------------------------------------------------------ browser

def mail_token(tid, since_ms, wait_s=90):
    """The one WE_CLIENT_* outcome line the claim logged for this ticket (ticket-api log group)."""
    end = time.time() + wait_s
    while time.time() < end:
        names = set()
        tok = None
        while True:
            kw = {"logGroupName": "/aws/lambda/" + FN, "startTime": since_ms, "filterPattern": '"WE_CLIENT_" "%s"' % tid}
            if tok:
                kw["nextToken"] = tok
            r = logs.filter_log_events(**kw)
            for ev in r.get("events", []):
                w = ev["message"].split(" ", 1)[0]
                if w.startswith("WE_CLIENT_"):
                    names.add(w)
            tok = r.get("nextToken")
            if not tok:
                break
        outcome = names & {"WE_CLIENT_SENT", "WE_CLIENT_SEND_FAILED", "WE_CLIENT_NOT_SINGULAR"}
        if outcome:
            return sorted(outcome), sorted(names)
        time.sleep(3)
    return [], []


def mock_tickets():
    """Synthetic tickets shaped like the two targets (types only; every value is fake). --dry never touches AWS."""
    def mk(tid, with_draft):
        t = {"ticket_id": tid, "ticket_type": "analysis_request", "status": "open", "title": "[TEST] synthetic %s" % tid[-4:],
             "description": "synthetic", "requester": {"email": "svc-commentary", "name": "svc-commentary", "firm": "cottonwood"},
             "created_by": "svc-commentary", "created_at": "2026-10-09T12:00:00Z", "assignee": None, "source": "portal",
             "routing": {"primary": ["x"], "secondary": [], "visibility": []},
             "events": [{"ts": "2026-10-09T12:00:00Z", "actor": "svc-commentary", "action": "created"}],
             "answers": {"add_commentary": True, "advisor": "adv", "report_type": "Overview", "firm": "cottonwood"},
             "attachment": {"upload_id": "u", "input_id": "i"}, "client_updates": []}
        if with_draft:
            t["report_ref"] = {"request_id": "r"}
            t["draft_commentary"] = {"text": "synthetic draft", "generated_at": "2026-10-09T12:00:00Z", "status": "DRAFT", "model": "m"}
            t["client_updates"] = [{"ts": "2026-10-09T12:00:00Z", "text": "t", "author": "a"}]
        return t
    return {T1: mk(T1, True), T2: mk(T2, False)}


def crawl(token, exp, out, mock=None):
    from playwright.sync_api import sync_playwright

    def state_of(tid):
        if mock is None:
            return ticket_state(tid)
        return {"status": mock[tid]["status"], "assignee": mock[tid]["assignee"]}

    allowed_writes = set()
    user = {"email": IDENT, "name": NAME, "role": "user", "mustChangePassword": False, "firmId": "opal-capital",
            "userType": "test-filer", "advisorId": None, "firmRole": None, "advisorRole": None}
    auth_body = json.dumps({"accessToken": token, "user": user})
    writes = {}

    def on_route(route):
        req = route.request
        u = urlparse(req.url)
        rtype = req.resource_type
        if u.netloc != HOST:
            if rtype in ("font", "stylesheet", "image", "script", "media"):
                return route.continue_()
            trace["blocked_requests"].append("%s %s %s" % (req.method, u.netloc, rtype))
            return route.abort()
        p = u.path
        if p in ("/auth/refresh", "/auth/me"):
            return route.fulfill(status=200, content_type="application/json",
                                 body=auth_body if p == "/auth/refresh" else json.dumps({"user": user}))
        if rtype in ("fetch", "xhr", "ping", "eventsource", "websocket", "other") and (p.startswith("/api/") or p.startswith("/auth/")
                                                                                 or p.startswith("/v1/")):
            if req.method == "GET" and p in ("/api/scoped/tickets", "/api/scoped/tickets/metrics"):
                if mock is None:
                    return route.continue_()
                if p.endswith("/metrics"):
                    return route.fulfill(status=200, content_type="application/json",
                                         body=json.dumps({"by_assignee": {}, "by_type": {}, "sampled": 0}))
                want = (parse_qs(u.query).get("status") or [None])[0]
                lst = [t for t in mock.values() if want in (None, t["status"])]
                return route.fulfill(status=200, content_type="application/json", body=json.dumps({"tickets": lst, "count": len(lst)}))
            if req.method == "POST" and (req.method, p) in allowed_writes:
                allowed_writes.discard((req.method, p))
                writes[p] = "sent"
                if mock is None:
                    return route.continue_()
                tid, act = p.split("/")[-2], p.split("/")[-1]
                mock[tid]["status"] = "in_progress" if act == "claim" else "completed"
                mock[tid]["assignee"] = IDENT
                return route.fulfill(status=200, content_type="application/json", body=json.dumps({"ticket": mock[tid]}))
            trace["blocked_requests"].append("%s %s" % (req.method, p.replace(T1, "<T1>").replace(T2, "<T2>")))
            return route.abort()
        return route.continue_()

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(channel="msedge", headless=True)
        except Exception:  # noqa: BLE001 -- fall back to the bundled chromium
            browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 1000})
        ctx.route("**/*", on_route)
        page = ctx.new_page()
        dialogs = []

        def on_dialog(d):
            dialogs.append({"type": d.type, "message": d.message})
            d.accept(RESOLUTION)

        page.on("dialog", on_dialog)
        statuses = {}

        def on_response(r):
            p = urlparse(r.url).path
            if r.request.method == "POST" and p.startswith("/api/scoped/tickets/") and p.rsplit("/", 1)[-1] in ("claim", "complete"):
                statuses[p] = r.status

        page.on("response", on_response)

        def row_for(tid):
            return page.locator("tbody tr").filter(has=page.locator("td", has_text=tid)).first

        def diag():
            try:
                txt = page.locator("body").inner_text(timeout=3000)
            except Exception:  # noqa: BLE001
                txt = ""
            flags = [w for w in ("Something went wrong", "Tickets could not be loaded", "Sign in", "Loading") if w in txt]
            return "path=%s title=%r body_chars=%d flags=%s buttons=%d" % (urlparse(page.url).path, page.title(), len(txt), flags,
                                                                           page.get_by_role("button").count())

        def wait_board():
            t0 = time.time()
            try:
                page.get_by_role("button", name="Open", exact=True).first.wait_for(state="visible", timeout=60000)
                page.locator("thead th", has_text="Ticket").first.wait_for(state="visible", timeout=60000)
            except Exception as e:  # noqa: BLE001
                raise Stop("the board did not finish signing in: %s | %s" % (type(e).__name__, diag()))
            say("sign-in wait observed: Open tab + table header visible after %.1fs; %s" % (time.time() - t0, diag()))

        def click_tab(label):
            page.get_by_role("button", name=label, exact=True).first.wait_for(state="visible", timeout=45000)
            for loc in (page.get_by_role("tab", name=label, exact=True), page.get_by_role("button", name=label, exact=True),
                        page.get_by_text(label, exact=True)):
                if loc.count():
                    loc.first.click()
                    return
            raise Stop("board tab %r not found" % label)

        def wait_row(tid):
            row = row_for(tid)
            row.wait_for(state="visible", timeout=45000)
            return row

        def row_cells(tid):
            cells = row_for(tid).locator("td")
            return {"assignee": cells.nth(5).inner_text().strip(), "status": cells.nth(6).inner_text().strip()}

        page.goto(BASE + "/ticket-center", wait_until="domcontentloaded", timeout=60000)
        say("board opened; url path=%s" % urlparse(page.url).path)
        if urlparse(page.url).path != "/ticket-center":
            raise Stop("the board did not open (landed on %s)" % urlparse(page.url).path)
        wait_board()
        per = {}
        for idx, tid in enumerate((T1, T2)):
            if idx == 1 and exp - time.time() < MIN_LEFT_FOR_SECOND:
                raise Stop("token has under %d s left before the second claim" % MIN_LEFT_FOR_SECOND)
            if idx == 0:
                for chk in (T1, T2):
                    cs = state_of(chk)
                    if (cs["status"], cs["assignee"]) != ("open", None):
                        raise Stop("%s is not open/unassigned before the first CLAIM" % chk)
            click_tab("Open")
            row = wait_row(tid)
            prior = state_of(tid)
            say("%s before CLAIM: store status=%s assignee=%s | board row=%s" % (tid, prior["status"], prior["assignee"], row_cells(tid)))
            claim_path = "/api/scoped/tickets/%s/claim" % tid
            allowed_writes.add(("POST", claim_path))
            t0_ms = int(time.time() * 1000) - 2000
            row.get_by_role("button", name="Claim", exact=True).click()
            page.get_by_text("Claimed %s." % tid).wait_for(state="visible", timeout=45000)
            say("%s CLAIM pressed; http=%s" % (tid, statuses.get(claim_path)))
            mt, seen = (mail_token(tid, t0_ms) if mock is None else (['WE_CLIENT_SEND_FAILED'], ['WE_CLIENT_SEND_FAILED']))
            say("%s mail branch tokens=%s (all WE_CLIENT_* seen=%s)" % (tid, mt, seen))
            mid = state_of(tid)
            say("%s after CLAIM: status=%s assignee=%s" % (tid, mid["status"], mid["assignee"]))
            per[tid] = {"prior_status": prior["status"], "after_claim_status": mid["status"], "claim_http": statuses.get(claim_path),
                        "mail": mt}
            if not mt:
                raise Stop("%s: no WE_CLIENT_* outcome line was readable after the claim; COMPLETE not pressed" % tid)
            if "WE_CLIENT_SENT" in mt:
                per[tid]["stop"] = "WE_CLIENT_SENT"
                out["partial"] = per
                raise Stop("%s: WE_CLIENT_SENT after the claim; STOP before COMPLETE" % tid)
            if mid["status"] != "in_progress" or mid["assignee"] != IDENT:
                raise Stop("%s: the claim did not land as in_progress under the identity" % tid)
            click_tab("In Progress")
            row = wait_row(tid)
            comp_path = "/api/scoped/tickets/%s/complete" % tid
            allowed_writes.add(("POST", comp_path))
            row.get_by_role("button", name="Complete", exact=True).click()
            page.get_by_text("Completed %s." % tid).wait_for(state="visible", timeout=45000)
            say("%s COMPLETE pressed; http=%s; dialog=%s" % (tid, statuses.get(comp_path), dialogs[-1] if dialogs else None))
            after = state_of(tid)
            say("%s after COMPLETE: status=%s assignee=%s" % (tid, after["status"], after["assignee"]))
            per[tid].update({"later_status": after["status"], "complete_http": statuses.get(comp_path)})
            out["partial"] = per
            if after["status"] != "completed":
                raise Stop("%s: COMPLETE did not leave the ticket completed" % tid)
        # step 5: reload the board and read the two rows
        page.reload(wait_until="domcontentloaded", timeout=60000)
        wait_board()
        click_tab("Completed")
        board = {}
        for tid in (T1, T2):
            wait_row(tid)
            board[tid] = row_cells(tid)
            say("%s board row after reload: %s" % (tid, board[tid]))
        out["board_after_reload"] = board
        if mock is not None:
            say("DRY: mock end states %s" % {t: (mock[t]["status"], mock[t]["assignee"]) for t in (T1, T2)})
        out["per_ticket"] = per
        out["dialogs"] = dialogs
        out["writes_sent"] = sorted(writes)
        ctx.close()
        browser.close()


# ------------------------------------------------------------------ step 6 and 7

def streams_active(group, lo_s, hi_s):
    n = 0
    pag = logs.get_paginator("describe_log_streams")
    for page in pag.paginate(logGroupName=group, orderBy="LastEventTime", descending=True):
        for s in page.get("logStreams", []):
            last = s.get("lastEventTimestamp")
            first = s.get("firstEventTimestamp")
            if last is None:
                continue
            if last < lo_s * 1000:
                return n
            if first is not None and first <= hi_s * 1000:
                n += 1
    return n


def count_events(group, pattern, lo_s, hi_s):
    n, tok = 0, None
    while True:
        kw = {"logGroupName": group, "filterPattern": pattern, "startTime": lo_s * 1000, "endTime": hi_s * 1000}
        if tok:
            kw["nextToken"] = tok
        r = logs.filter_log_events(**kw)
        n += len(r.get("events", []))
        tok = r.get("nextToken")
        if not tok:
            return n


def zero_call_read(iat, exp):
    group = "/aws/lambda/opal-data-refresh-api"
    pat = '"%s"' % IDENT
    lo, hi = iat, int(time.time())
    streams = streams_active(group, lo, hi)
    window = "exact"
    if streams == 0:
        lo, window = iat - 6 * 3600, "widened to iat-6h (no stream had an event inside the exact window)"
        streams = streams_active(group, lo, hi)
    count = count_events(group, pat, lo, hi)
    # positive controls, same mechanics: (a) this group does emit caller-address lines (any recent admitted/refused line is found by the
    # same filter call); (b) the ticket log shows both claims landed in the window (the ticket log carries no actor address).
    ctl_a = count_events(group, '"Opal-internal"', int(time.time()) - 24 * 3600, int(time.time()))
    ctl_b = {t: count_events("/aws/lambda/" + FN, '"WE_CLIENT_" "%s"' % t, iat, hi) for t in (T1, T2)}
    say("zero-call read: %s streams_with_events=%d identity_matches=%d | control(a) caller-address lines in 24h=%d | control(b) %s"
        % (group, streams, count, ctl_a, ctl_b))
    return {"log_group": group, "window": window, "from": iso(lo), "to": iso(hi), "streams_searched": streams, "count": count,
            "streams_basis": "describe_log_streams: streams whose first/last event overlap the window",
            "control_caller_lines_24h": ctl_a, "control_ticket_log_claim_lines": ctl_b,
            "control_note": "the ticket log never carries the actor address, so the pair's control (find the identity in the ticket log) "
                            "cannot be run as written; the substitutes above prove the filter and group return events"}


def remove_row(exp):
    wait = exp + 5 - time.time()
    if wait > 0:
        say("waiting %ds for the token to pass exp %s before the row is removed" % (int(wait), iso(exp)))
        time.sleep(wait)
    ddb.delete_item(TableName=USERS, Key=row_key())
    deleted_at = iso()
    absent = item_of(USERS, row_key()) is None
    say("row deleted at %s; ConsistentRead ABSENT=%s" % (deleted_at, absent))
    return deleted_at, absent


def main():
    sha = before = None
    iat = exp = None
    row_written = False
    stop = None
    out = {}
    zc = None
    try:
        sha, before = preconditions()
        token, iat, exp = write_row_and_mint()
        row_written = True
        proof = one_firm_proof(token)
        crawl(token, exp, out)
        del token
        zc = zero_call_read(iat, exp)
    except Stop as e:
        stop = "STOP: %s" % e
        say(stop)
    except Exception as e:  # noqa: BLE001 -- anything else is a STOP too; the row is still removed after exp
        stop = "STOP (unexpected %s): %s" % (type(e).__name__, str(e)[:240])
        say(stop)
    finally:
        deleted_at = absent = None
        if row_written:
            deleted_at, absent = remove_row(exp)
    final = {t: ticket_state(t) for t in (T1, T2)}
    trace_doc = {"stop": stop, "row_written": row_written, "iat": iso(iat) if iat else None, "exp": iso(exp) if exp else None,
                 "row_deleted_at": deleted_at, "row_absent_after": absent, "final_states": final, "crawl": out, "zero_call_read": zc,
                 "trace": trace}
    if stop is None and zc and absent:
        result = {"tickets": [T1, T2], "identity": IDENT, "firm_list": FIRMS, "token_exp": iso(exp), "row_deleted_at": deleted_at,
                  "row_absent_after": bool(absent), "mail_branch": {t: out["per_ticket"][t]["mail"][0] for t in (T1, T2)},
                  "zero_call_read": zc, "token_printed": False, "claim": "measured",
                  "token_iat": iso(iat), "deployed_code_sha256": sha, "one_firm_proof": proof,
                  "prior_status": {t: {"status": before[t]["status"], "assignee": before[t]["assignee"]} for t in (T1, T2)},
                  "later_status": {t: {"status": final[t]["status"], "assignee": final[t]["assignee"]} for t in (T1, T2)},
                  "board_after_reload": out.get("board_after_reload"), "writes_sent": out.get("writes_sent"),
                  "dialogs": out.get("dialogs"), "per_ticket": out.get("per_ticket"),
                  "blocked_requests": trace["blocked_requests"]}
        RESULT.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        say("result written: %s" % RESULT.name)
        return 0
    STOPFILE.write_text(json.dumps(trace_doc, indent=1) + "\n", encoding="utf-8")
    say("STOP file written: %s" % STOPFILE.name)
    return 1


def dry():
    """No AWS, no ticket write: the same browser flow against a mocked ticket backend and a dummy token."""
    out = {}
    try:
        crawl("dummy.not.a.token", time.time() + LIFE, out, mock=mock_tickets())
    except Stop as e:
        say("DRY STOP: %s" % e)
        return 1
    say("DRY OK: blocked requests (method + path only): %d" % len(trace["blocked_requests"]))
    return 0


if __name__ == "__main__":
    sys.exit(dry() if "--dry" in sys.argv else main())
