"""TCKT_VNEXT TO-R18-CLOSE PART 1b -- claim then complete the ONE synthetic meeting ticket (0.7.0_AE_CloudOps~TV2).

Pair : R18_RUN_PAIR.md AMENDMENT 4 (COO blob b83e173a01, CTO half ea18a44085, origin half cf7c856072); order TO-R18-CLOSE AMENDMENT 1 (GO msg 9815).
One process holds the signing key, the token and the browser context. The token is never printed, written or put in a trace: it reaches the page
only as the body of a stubbed /auth/refresh response inside that one in-memory context. The dev server on localhost:5174 is REUSED: this script
never starts, stops or restarts it.

Browser rule: the page may make exactly these API calls -- GET /api/scoped/tickets, GET /api/scoped/tickets/metrics, the directory resolve read,
POST claim and POST complete for the ONE ticket, each once, in that order. Every other API-shaped request is aborted and logged by method and path
only. ANY WE_*SENT token on the ticket is a STOP: nothing further is done to it.
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
IDENT = "tckt-r18-filer-20261016@opal.invalid"
NAME = "TCKT R18 synthetic filer"
FIRM = "cottonwood"
TICKET = "TCK-20261016-9d7654eb"
FN = "opal-ticket-api"
EXPECT_SHA = "JwdnACONAnxwqzhsVgqgU+nRoLdmS7MyLmzXmZuXsR4="
LIFE = 900  # seconds; the pair allows at most 20 minutes
KEY_SECRET = "opal/auth/jwt-private-key"
RESOLUTION = "[TEST] R18 part-1 close"
LEDGER = "org/critical_paths/change_management/20261016T2005Z_tckt-vnext-r18-close-20261016_deploy_completion.md"
SENT_RE = re.compile(r"WE_[A-Z_]*SENT\b")

OUT = Path(__file__).resolve().parent
TRACE = OUT / "R18_CLOSE_TRACE.json"
RESULT = OUT / "R18_CLOSE_RESULT.json"

ddb = boto3.client("dynamodb", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)
state = {"written": False, "exp": None}
trace = {"claim": "measured", "executor": "0.7.0_AE_CloudOps~TV2", "server_reused": True, "events": [], "blocked_requests": [],
         "request_census": {}, "statuses": {}}


class Stop(Exception):
    pass


def iso(t=None):
    return dt.datetime.fromtimestamp(time.time() if t is None else t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def say(msg):
    line = "%s %s" % (iso(), msg)
    print(line, flush=True)
    trace["events"].append(line)


def row_key():
    return {"PK": {"S": "USER#" + IDENT}, "SK": {"S": "PROFILE"}}


def item_of(table, key):
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def ticket_view():
    it = item_of(TICKETS, {"ticket_id": {"S": TICKET}})
    if it is None:
        raise Stop("ticket not found")
    return {"ticket_type": (it.get("ticket_type") or {}).get("S"), "status": (it.get("status") or {}).get("S"),
            "assignee": (it.get("assignee") or {}).get("S"),
            "firm": (((it.get("requester") or {}).get("M") or {}).get("firm") or {}).get("S")}


def preflight():
    cfg = boto3.client("lambda", region_name=REGION).get_function_configuration(FunctionName=FN)
    say("deployed %s CodeSha256=%s State=%s" % (FN, cfg["CodeSha256"], cfg.get("State")))
    if cfg["CodeSha256"] != EXPECT_SHA:
        raise Stop("deployed CodeSha256 differs from the released package")
    v = ticket_view()
    say("ticket %s before: type=%s status=%s assignee=%s firm=%s" % (TICKET, v["ticket_type"], v["status"], v["assignee"], v["firm"]))
    if (v["ticket_type"], v["status"], v["assignee"], v["firm"]) != ("meeting_request", "open", None, FIRM):
        raise Stop("the ticket is not an open, unassigned meeting_request for %s" % FIRM)
    if item_of(USERS, row_key()) is not None:
        raise Stop("the identity row is already PRESENT")
    say("identity key ConsistentRead ABSENT")
    return v


def write_row_and_mint():
    item = {"PK": {"S": "USER#" + IDENT}, "SK": {"S": "PROFILE"}, "email": {"S": IDENT}, "firmId": {"S": "opal-capital"},
            "status": {"S": "active"}, "userType": {"S": "test-filer"}, "name": {"S": NAME},
            "allowedFirmIds": {"L": [{"S": FIRM}]}}
    ddb.put_item(TableName=USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
    state["written"] = True
    back = item_of(USERS, row_key())
    if back is None or [x["S"] for x in back["allowedFirmIds"]["L"]] != [FIRM] or "scope_all_firms" in back:
        raise Stop("row not PRESENT with the one-firm list after the put")
    under = ddb.query(TableName=USERS, KeyConditionExpression="PK = :p", ConsistentRead=True,
                      ExpressionAttributeValues={":p": {"S": "USER#" + IDENT}}).get("Items", [])
    others = sum(1 for r in under if r["SK"]["S"] != "PROFILE")
    say("ROLE SET: role=user userType=%s firmId=%s allowedFirmIds=%s entitlement/other rows under the key: %s"
        % (back["userType"]["S"], back["firmId"]["S"], [x["S"] for x in back["allowedFirmIds"]["L"]], others))
    if others != 0:
        raise Stop("the identity has rows other than PROFILE")
    pem = boto3.client("secretsmanager", region_name=REGION).get_secret_value(SecretId=KEY_SECRET)["SecretString"]
    iat = int(time.time())
    claims = {"sub": IDENT, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal",
              "role": "user", "userType": "test-filer", "name": NAME, "iat": iat, "exp": iat + LIFE}
    token = pyjwt.encode(claims, pem, algorithm="RS256")
    del pem
    say("token minted (held in memory only) iat=%s exp=%s life=%ds" % (iso(iat), iso(iat + LIFE), LIFE))
    return token, iat, iat + LIFE


def we_tokens(since_ms, wait_s, need_client=False):
    """Every WE_* token the ticket service logged for this ticket since the click (read-only filter on the function's log group)."""
    names, end = set(), time.time() + wait_s
    while time.time() < end:
        tok = None
        while True:
            kw = {"logGroupName": "/aws/lambda/" + FN, "startTime": since_ms, "filterPattern": '"WE_" "%s"' % TICKET}
            if tok:
                kw["nextToken"] = tok
            r = logs.filter_log_events(**kw)
            for ev in r.get("events", []):
                names.update(re.findall(r"WE_[A-Z_]+", ev["message"]))
            tok = r.get("nextToken")
            if not tok:
                break
        if any(SENT_RE.search(n) for n in names):
            break
        if names and (not need_client or any(n.startswith("WE_CLIENT_") for n in names)):
            break
        time.sleep(3)
    return sorted(names)


def drive(token):
    allowed = set()
    user = {"email": IDENT, "name": NAME, "role": "user", "mustChangePassword": False, "firmId": "opal-capital",
            "userType": "test-filer", "advisorId": None, "firmRole": None, "advisorRole": None}
    auth_body = json.dumps({"accessToken": token, "user": user})
    violations = []

    def norm(p):
        return p.replace(TICKET, "<T>")

    def on_route(route):
        req = route.request
        u = urlparse(req.url)
        rtype = req.resource_type
        k = "%s %s %s" % (req.method, u.netloc, norm(u.path))
        trace["request_census"][k] = trace["request_census"].get(k, 0) + 1
        if u.netloc != HOSTPORT:
            if rtype in ("font", "stylesheet", "image", "media"):
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
                return route.continue_()
            if (req.method, p) in allowed:
                allowed.discard((req.method, p))
                return route.continue_()
            trace["blocked_requests"].append("%s %s" % (req.method, norm(p)))
            return route.abort()
        return route.continue_()

    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(channel="msedge", headless=True)
        except Exception:  # noqa: BLE001
            browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 1000})
        ctx.route("**/*", on_route)
        page = ctx.new_page()
        dialogs = []

        def on_dialog(d):
            dialogs.append({"type": d.type})
            d.accept(RESOLUTION)

        page.on("dialog", on_dialog)

        def on_response(r):
            p = urlparse(r.url).path
            if r.request.method == "POST" and p.startswith("/api/scoped/tickets/"):
                trace["statuses"]["http POST " + norm(p)] = r.status

        page.on("response", on_response)

        def row():
            return page.locator("tbody tr").filter(has=page.locator("td", has_text=TICKET)).first

        page.goto(ORIGIN + "/ticket-center", wait_until="domcontentloaded", timeout=60000)
        if urlparse(page.url).path != "/ticket-center":
            raise Stop("the board did not open (landed on %s)" % urlparse(page.url).path)
        origin = page.evaluate("window.location.origin")
        say("PAGE ORIGIN window.location.origin = %s" % origin)
        if origin != ORIGIN or violations:
            raise Stop("page origin %r (violations %s) is not exactly %s" % (origin, violations, ORIGIN))
        out["browser_origin"] = origin
        try:
            page.get_by_role("button", name="Open", exact=True).first.wait_for(state="visible", timeout=60000)
            page.locator("thead th", has_text="Ticket").first.wait_for(state="visible", timeout=60000)
        except Exception as e:  # noqa: BLE001
            raise Stop("the board did not finish signing in: %s" % type(e).__name__)
        say("board signed in")
        page.get_by_role("button", name="Open", exact=True).first.click()
        row().wait_for(state="visible", timeout=45000)
        say("the ticket is listed on the Open tab")
        # CLAIM
        allowed.add(("POST", "/api/scoped/tickets/%s/claim" % TICKET))
        t0 = int(time.time() * 1000) - 2000
        row().get_by_role("button", name="Claim", exact=True).click()
        page.get_by_text("Claimed %s." % TICKET).wait_for(state="visible", timeout=45000)
        v = ticket_view()
        say("CLAIM pressed; http=%s; ConsistentRead status=%s assignee=%s" % (trace["statuses"].get("http POST /api/scoped/tickets/<T>/claim"), v["status"], v["assignee"]))
        out["claim_status"], out["claim_assignee"] = v["status"], v["assignee"]
        claim_tokens = we_tokens(t0, 90, need_client=True)
        say("CLAIM log tokens: %s" % claim_tokens)
        out["claim_tokens"] = claim_tokens
        if any(SENT_RE.search(n) for n in claim_tokens):
            raise Stop("a SENT token after the claim: %s; nothing further is done to the ticket" % claim_tokens)
        if not any(n.startswith("WE_CLIENT_") for n in claim_tokens):
            raise Stop("no WE_CLIENT_* outcome line was readable after the claim; COMPLETE not pressed")
        if v["status"] != "in_progress" or v["assignee"] != IDENT:
            raise Stop("the claim did not land as in_progress under the identity")
        # COMPLETE
        for loc in (page.get_by_role("tab", name="In Progress", exact=True), page.get_by_role("button", name="In Progress", exact=True),
                    page.get_by_text("In Progress", exact=True)):
            if loc.count():
                loc.first.click()
                break
        else:
            raise Stop("the In Progress tab was not found")
        row().wait_for(state="visible", timeout=45000)
        allowed.add(("POST", "/api/scoped/tickets/%s/complete" % TICKET))
        t1 = int(time.time() * 1000) - 2000
        row().get_by_role("button", name="Complete", exact=True).click()
        page.get_by_text("Completed %s." % TICKET).wait_for(state="visible", timeout=45000)
        v2 = ticket_view()
        say("COMPLETE pressed; http=%s; dialog=%s; ConsistentRead status=%s" % (trace["statuses"].get("http POST /api/scoped/tickets/<T>/complete"), dialogs[-1:] or None, v2["status"]))
        out["complete_status"] = v2["status"]
        complete_tokens = we_tokens(t1, 25)
        say("COMPLETE log tokens: %s" % complete_tokens)
        out["complete_tokens"] = complete_tokens
        if any(SENT_RE.search(n) for n in complete_tokens):
            raise Stop("a SENT token after the complete: %s" % complete_tokens)
        if v2["status"] != "completed":
            raise Stop("the complete did not leave the ticket completed")
        ctx.close()
        browser.close()
    return out


def remove_row(exp):
    wait = (exp + 5 - time.time()) if exp else 0
    if wait > 0:
        say("waiting %ds for the token to pass exp %s before the row is removed" % (int(wait), iso(exp)))
        time.sleep(wait)
    ddb.delete_item(TableName=USERS, Key=row_key())
    deleted_at = iso()
    absent = item_of(USERS, row_key()) is None
    say("row deleted at %s; ConsistentRead ABSENT=%s" % (deleted_at, absent))
    return deleted_at, absent


def main():
    stop = None
    out = {}
    exp = iat = None
    try:
        preflight()
        token, iat, exp = write_row_and_mint()
        state["exp"] = exp
        out = drive(token)
        del token
    except Stop as e:
        stop = "STOP: %s" % e
        say(stop)
    except Exception as e:  # noqa: BLE001
        stop = "STOP (unexpected %s): %s" % (type(e).__name__, str(e)[:300])
        say(stop)
    finally:
        deleted_at = absent = None
        if state["written"]:
            deleted_at, absent = remove_row(state["exp"])
    final = ticket_view()
    eng = [k for k in trace["request_census"] if "/api/general/trades" in k]
    TRACE.write_text(json.dumps({"stop": stop, "iat": iso(iat) if iat else None, "exp": iso(exp) if exp else None, "row_deleted_at": deleted_at,
                                 "row_absent_after": absent, "final_ticket": final, "out": out, "engine_requests_seen": eng,
                                 "trace": trace}, indent=1) + "\n", encoding="utf-8")
    if stop is None and absent and out.get("complete_status") == "completed":
        RESULT.write_text(json.dumps({
            "claim": "measured", "ticket": TICKET, "claim_status": out["claim_status"], "claim_assignee": out["claim_assignee"],
            "complete_status": out["complete_status"], "log_tokens": {"claim": out["claim_tokens"], "complete": out["complete_tokens"]},
            "identity": IDENT, "row_deleted_at": deleted_at, "token_exp": iso(exp), "row_absent_after": True,
            "browser_origin": out["browser_origin"], "server_reused": True, "change_ledger": LEDGER,
            "no_engine_call": not eng, "token_printed": False, "blocked_requests_count": len(trace["blocked_requests"])}, indent=1) + "\n",
            encoding="utf-8")
        say("result written: %s" % RESULT.name)
        return 0
    say("trace written: %s" % TRACE.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
