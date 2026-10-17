"""TCKT_VNEXT TO-R20-RV (PART 3, FWD-11) -- the filer's RENDERED read of one meeting ticket, six shots (0.7.0_AE_CloudOps~TV2).

Pair : R18_RUN_PAIR.md AMENDMENT 5 (COO blob 08c9ba4bb2, CTO half 098b12581d); order AMENDMENT 2 (GO msg 10369); the ten-step draft is the step list.
One process holds the signing key, the three tokens and the browser contexts. A token is never printed, written or put in a trace: it reaches a page
only as the body of a stubbed /auth/refresh response inside that one in-memory context. The dev server on localhost:5174 is the CTO's: this script
never starts, stops, restarts or edits it.

Phases (gate files in ./gates are written by the applier; the routing window is applied by the applier under safe-apply):
  A  preflight, ONE key read, mint filer + coordinator + bystander, filer browser open, page origin printed             -> STAGE1_READY
  B  on WINDOW_OPEN: the filer files ONE Meeting Request (shot 1), the coordinator confirms one time                    -> CONFIRMED
  C  on WINDOW_CLOSED: shots 2 to 4, claim + complete by the filer (shot 5), the meeting form unsubmitted (shot 6)      -> SHOTS_DONE
  D  wait past the LAST exp, delete the three rows, read each ABSENT.
Shots are clipped to the one ticket's two board rows (the ticket row and its outcome row), so no other ticket is captured. A screenshot is
saved, its path and byte count are printed, and it is not described. Browser rule: only the gated API calls run; every other API-shaped
request is aborted and logged by method and path.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
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
STAMP = "20261017"
FILER = "tckt-r20-filer-%s@opal.invalid" % STAMP
COORD = "tckt-r20-coord-%s@opal.invalid" % STAMP
VIEW = "tckt-r20-view-%s@opal.invalid" % STAMP
FIRM = "cottonwood"
FN = "opal-ticket-api"
EXPECT_SHA = "iRxJZYp6IXEtiXDRMT4R/EOwKvsqh5Id5NNgPcpy3RM="
DEV_SHA = "38d4f9473284a585bc217981213b9516e29d3a87"
SERVER_TREE = "C:/dev/smoke-template-5174"
JEANETTE = "jeanette@opalinvest.com"
LIFE = 1140
KEY_SECRET = "opal/auth/jwt-private-key"
TIME_1 = "2026-10-23 14:00 ET (R20 run 20261017)"
TIME_2 = "2026-10-24 10:30 ET (R20 run 20261017)"
WHO = "TCKT R20 synthetic coordinator (test)"
PURPOSE = "Synthetic live run of the Meeting Request, rendered read. No client data."
RESOLUTION = "[TEST] R20 rendered-read run close"
SENT_RE = re.compile(r"WE_[A-Z_]*SENT\b")
NAMES = {FILER: "TCKT R20 synthetic filer", COORD: "TCKT R20 synthetic coordinator", VIEW: "TCKT R20 synthetic bystander"}

OUT = Path(__file__).resolve().parent
GATES = OUT / "gates"
TRACE = OUT / "R20_RUN_TRACE.json"
RESULT = OUT / "R20_RUN_RESULT.json"
SHOT_DIR_REL = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_run/"

ddb = boto3.client("dynamodb", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)
state = {"written": [], "exp": []}
trace = {"claim": "measured", "executor": "0.7.0_AE_CloudOps~TV2", "server_reused": True, "events": [], "blocked_requests": [],
         "request_census": {}, "statuses": {}, "shots_taken": []}


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


def lam_cfg():
    return boto3.client("lambda", region_name=REGION).get_function_configuration(FunctionName=FN)


def preflight():
    head = subprocess.check_output(["git", "-C", SERVER_TREE, "rev-parse", "HEAD"], text=True).strip()
    say("served checkout %s HEAD=%s" % (SERVER_TREE, head))
    if head != DEV_SHA:
        raise Stop("the served checkout HEAD is not the handed-over sha")
    dirty = subprocess.check_output(["git", "-C", SERVER_TREE, "status", "--short"], text=True).strip()
    if dirty:
        raise Stop("the served checkout has uncommitted changes")
    cfg = lam_cfg()
    say("deployed %s CodeSha256=%s State=%s" % (FN, cfg["CodeSha256"], cfg.get("State")))
    if cfg["CodeSha256"] != EXPECT_SHA:
        raise Stop("deployed CodeSha256 differs from the R20 release")
    rb = routing_of(cfg)
    say("routing_before meeting_request=%s" % json.dumps(rb))
    if (rb or {}).get("primary") != [JEANETTE]:
        raise Stop("routing before the window is not jeanette alone")
    for who in (FILER, COORD, VIEW):
        if item_of(USERS, key_of(who)) is not None:
            raise Stop("an identity row is already PRESENT")
    say("all three identity keys ConsistentRead ABSENT")
    return rb


def write_rows_and_mint():
    """ONE key read; three rows written (cleanup flag set per row at the write); three tokens, in memory only."""
    pem = None
    tokens, iats = {}, {}
    for ident in (FILER, COORD, VIEW):
        item = {"PK": {"S": "USER#" + ident}, "SK": {"S": "PROFILE"}, "email": {"S": ident}, "firmId": {"S": "opal-capital"},
                "status": {"S": "active"}, "userType": {"S": "test-filer"}, "name": {"S": NAMES[ident]},
                "allowedFirmIds": {"L": [{"S": FIRM}]}}
        ddb.put_item(TableName=USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
        state["written"].append(ident)
        back = item_of(USERS, key_of(ident))
        if back is None or [x["S"] for x in back["allowedFirmIds"]["L"]] != [FIRM] or "scope_all_firms" in back:
            raise Stop("row not PRESENT with the one-firm list after the put")
        say("row written for %s; ConsistentRead PRESENT allowedFirmIds=[%s]" % (ident.split("@")[0], FIRM))
    pem = boto3.client("secretsmanager", region_name=REGION).get_secret_value(SecretId=KEY_SECRET)["SecretString"]
    for ident in (FILER, COORD, VIEW):
        iat = int(time.time())
        claims = {"sub": ident, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal",
                  "role": "user", "userType": "test-filer", "name": NAMES[ident], "iat": iat, "exp": iat + LIFE}
        tokens[ident] = pyjwt.encode(claims, pem, algorithm="RS256")
        iats[ident] = iat
        state["exp"].append(iat + LIFE)
        say("token minted for %s (memory only) iat=%s exp=%s life=%ds" % (ident.split("@")[0], iso(iat), iso(iat + LIFE), LIFE))
    del pem
    return tokens, iats


def norm_path(p, tids):
    for t in tids:
        p = p.replace(t, "<T>")
    return re.sub(r"TCK-[0-9]{8}-[0-9a-f]{8}", "<T>", p)


class Session:
    def __init__(self, browser, ident, token, tids):
        self.ident, self.tids, self.allowed, self.violations = ident, tids, set(), []
        user = {"email": ident, "name": NAMES[ident], "role": "user", "mustChangePassword": False, "firmId": "opal-capital",
                "userType": "test-filer", "advisorId": None, "firmRole": None, "advisorRole": None}
        auth_body = json.dumps({"accessToken": token, "user": user})
        self.ctx = browser.new_context(viewport={"width": 1440, "height": 1000})

        def on_route(route):
            req = route.request
            u = urlparse(req.url)
            rtype = req.resource_type
            k = "%s %s %s" % (req.method, u.netloc, norm_path(u.path, self.tids))
            trace["request_census"][k] = trace["request_census"].get(k, 0) + 1
            if u.netloc != HOSTPORT:
                if rtype in ("font", "stylesheet", "image", "media"):
                    return route.continue_()
                trace["blocked_requests"].append("%s %s %s" % (req.method, u.netloc, rtype))
                if rtype == "document":
                    self.violations.append(u.netloc)
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
                if (req.method, p) in self.allowed:
                    self.allowed.discard((req.method, p))
                    return route.continue_()
                trace["blocked_requests"].append("%s %s" % (req.method, norm_path(p, self.tids)))
                return route.abort()
            return route.continue_()

        self.ctx.route("**/*", on_route)
        self.page = self.ctx.new_page()
        self.dialogs = []

        def on_dialog(d):
            self.dialogs.append(d.type)
            d.accept(RESOLUTION)

        self.page.on("dialog", on_dialog)

        def on_response(r):
            p = urlparse(r.url).path
            if r.request.method == "POST" and p.startswith("/api/scoped/tickets"):
                trace["statuses"]["http POST %s as %s" % (norm_path(p, self.tids), self.ident.split("-")[2])] = r.status

        self.page.on("response", on_response)

    def open_board(self):
        pg = self.page
        pg.goto(ORIGIN + "/ticket-center", wait_until="domcontentloaded", timeout=60000)
        if urlparse(pg.url).path != "/ticket-center":
            raise Stop("the board did not open (landed on %s)" % urlparse(pg.url).path)
        origin = pg.evaluate("window.location.origin")
        say("PAGE ORIGIN (%s) window.location.origin = %s" % (self.ident.split("-")[2], origin))
        if origin != ORIGIN or self.violations:
            raise Stop("page origin %r (violations %s) is not exactly %s" % (origin, self.violations, ORIGIN))
        self.wait_board()
        return origin

    def wait_board(self):
        pg = self.page
        try:
            pg.get_by_role("button", name="Open", exact=True).first.wait_for(state="visible", timeout=60000)
            pg.locator("thead th", has_text="Ticket").first.wait_for(state="visible", timeout=60000)
        except Exception as e:  # noqa: BLE001
            raise Stop("the board did not finish signing in for %s: %s" % (self.ident.split("-")[2], type(e).__name__))

    def tab(self, label):
        pg = self.page
        for loc in (pg.get_by_role("tab", name=label, exact=True), pg.get_by_role("button", name=label, exact=True),
                    pg.get_by_text(label, exact=True)):
            if loc.count():
                loc.first.click()
                return
        raise Stop("board tab %r not found" % label)

    def rows(self, mt):
        """The ticket's row and its outcome row (the next table row), found by the ticket id."""
        row = self.page.locator("tbody tr").filter(has=self.page.locator("td", has_text=mt)).first
        row.wait_for(state="visible", timeout=60000)
        out = row.locator("xpath=following-sibling::tr[1]")
        out.locator('[data-slot="meeting-outcome-line"]').wait_for(state="visible", timeout=30000)
        return row, out

    def shot(self, role, mt, rows, results):
        """Save a PNG clipped to the union of the ticket's two rows; print path and bytes; describe nothing."""
        row, out = rows
        row.scroll_into_view_if_needed()
        b1, b2 = row.bounding_box(), out.bounding_box()
        sx, sy = self.page.evaluate("[window.scrollX, window.scrollY]")
        x0, y0 = min(b1["x"], b2["x"]), min(b1["y"], b2["y"])
        x1, y1 = max(b1["x"] + b1["width"], b2["x"] + b2["width"]), max(b1["y"] + b1["height"], b2["y"] + b2["height"])
        return self._save(role, mt, {"x": max(0, x0 + sx - 8), "y": max(0, y0 + sy - 8), "width": x1 - x0 + 16, "height": y1 - y0 + 16}, results)

    def _save(self, role, mt, clip, results):
        name = "%s__%s__%s__localhost-5174.png" % (role, self.ident.split("@")[0], mt or "no-ticket")
        path = OUT / name
        self.page.screenshot(path=str(path), clip=clip, full_page=True)
        size = path.stat().st_size
        rel = SHOT_DIR_REL + name
        say("SHOT %s saved: %s (%d bytes)" % (role, rel, size))
        results[role] = {"path": rel, "bytes": size, "viewer": self.ident, "origin": ORIGIN}
        trace["shots_taken"].append(role)
        return path


def ticket_view(tid):
    it = item_of(TICKETS, {"ticket_id": {"S": tid}})
    if it is None:
        raise Stop("ticket not found")
    meeting = (it.get("meeting") or {}).get("M") or {}
    routing = (it.get("routing") or {}).get("M") or {}
    return {"ticket_type": (it.get("ticket_type") or {}).get("S"), "status": (it.get("status") or {}).get("S"),
            "assignee": (it.get("assignee") or {}).get("S"),
            "primary": [x.get("S") for x in (routing.get("primary") or {}).get("L", [])],
            "created_by": (it.get("created_by") or {}).get("S"),
            "meeting": {k: (v.get("S") if "S" in v else None) for k, v in meeting.items() if k in ("status", "time", "by")}}


def we_tokens(tid, since_ms, wait_s, need_client=False):
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
        if any(SENT_RE.search(n) for n in names):
            break
        if names and (not need_client or any(n.startswith("WE_CLIENT_") for n in names)):
            break
        time.sleep(3)
    return sorted(names)


def firm_no_contact(since_ms):
    """WE_CLIENT_NO_CONTACT carries the firm and not the ticket id; read it by firm in the window since the claim."""
    n, tok = 0, None
    while True:
        kw = {"logGroupName": "/aws/lambda/" + FN, "startTime": since_ms, "filterPattern": '"WE_CLIENT_NO_CONTACT" "firm=%s"' % FIRM}
        if tok:
            kw["nextToken"] = tok
        r = logs.filter_log_events(**kw)
        n += len(r.get("events", []))
        tok = r.get("nextToken")
        if not tok:
            return n


def phase_a(browser, tokens):
    s = Session(browser, FILER, tokens[FILER], [])
    origin = s.open_board()
    return s, origin


def phase_b(browser, fs, tokens, ctx_out):
    fp = fs.page
    fp.get_by_role("button", name="New Ticket").first.click()
    sel = fp.locator("select").filter(has=fp.locator("option", has_text="Meeting Request")).first
    sel.wait_for(state="visible", timeout=30000)
    sel.select_option(label="Meeting Request")
    firm = fp.locator('select[aria-label="Firm"]')
    firm.wait_for(state="visible", timeout=30000)
    fp.locator('select[aria-label="Firm"] option[value="%s"]' % FIRM).wait_for(state="attached", timeout=60000)
    firm.select_option(value=FIRM)
    fp.get_by_label("Who", exact=True).fill(WHO)
    fp.get_by_label("Purpose", exact=True).fill(PURPOSE)
    fp.get_by_label("Proposed time 1", exact=True).fill(TIME_1)
    fp.get_by_label("Proposed time 2", exact=True).fill(TIME_2)
    submit = fp.locator('[data-slot="meeting-request-submit"]')
    submit.wait_for(state="visible", timeout=30000)
    if not submit.is_enabled():
        raise Stop("the submit is held: the form is incomplete")
    fs.allowed.add(("POST", "/api/scoped/tickets"))
    since_ms = int(time.time() * 1000) - 2000
    submit.click()
    notice = fp.get_by_text(re.compile(r"Meeting request \S+ filed\.")).first
    try:
        notice.wait_for(state="visible", timeout=60000)
    except Exception as e:  # noqa: BLE001
        raise Stop("no filed notice after the submit (%s)" % type(e).__name__)
    mt = re.search(r"Meeting request (\S+) filed\.", notice.inner_text()).group(1)
    fs.tids.append(mt)
    say("filer: MEETING TICKET FILED %s" % mt)
    v = ticket_view(mt)
    say("ticket %s ConsistentRead: type=%s status=%s routing.primary=%s created_by=%s" % (mt, v["ticket_type"], v["status"], v["primary"], v["created_by"]))
    if v["ticket_type"] != "meeting_request" or v["status"] != "open" or v["primary"] != [COORD]:
        raise Stop("the filed ticket is not an open meeting_request with the coordinator alone as routing.primary")
    create_tokens = we_tokens(mt, since_ms, 75)
    say("CREATE log tokens for %s: %s" % (mt, create_tokens))
    if any(SENT_RE.search(t) for t in create_tokens):
        raise Stop("a SENT token was logged on the CREATE: %s" % create_tokens)
    ctx_out["mt"], ctx_out["create_tokens"] = mt, create_tokens
    # shot 1: the filer's own ticket, waiting words, no control
    fs.tab("Open")
    rows = fs.rows(mt)
    if rows[1].get_by_text("Waiting for the coordinator").count() != 1 or rows[1].get_by_role("button", name=re.compile("^Confirm ")).count() != 0:
        raise Stop("shot 1 precondition: the filer's row must show the waiting words and no control")
    fs.shot("filer_waiting", mt, rows, ctx_out["shots"])
    # the coordinator confirms ONE proposed time in a second context
    cs = Session(browser, COORD, tokens[COORD], [mt])
    cs.open_board()
    cs.tab("Open")
    btn = cs.page.get_by_role("button", name="Confirm " + TIME_1, exact=True)
    try:
        btn.wait_for(state="visible", timeout=60000)
    except Exception as e:  # noqa: BLE001
        raise Stop("the coordinator does not see the confirm control: %s" % type(e).__name__)
    cs.allowed.add(("POST", "/api/scoped/tickets/%s/meeting" % mt))
    since_c = int(time.time() * 1000) - 2000
    with cs.page.expect_response(lambda r: r.request.method == "POST" and r.url.endswith("/%s/meeting" % mt), timeout=60000) as ri:
        btn.click()
    say("coordinator: CONFIRM pressed for the first proposed time; http=%s" % ri.value.status)
    after = ticket_view(mt)
    say("ticket %s after the confirm: status=%s meeting=%s" % (mt, after["status"], after["meeting"]))
    if (after["meeting"].get("status"), after["meeting"].get("time"), after["meeting"].get("by"), after["status"]) != ("confirmed", TIME_1, COORD, "open"):
        raise Stop("the stored outcome is not confirmed by the coordinator at the clicked time with the ticket open")
    confirm_tokens = we_tokens(mt, since_c, 15)
    say("CONFIRM log tokens: %s" % confirm_tokens)
    if any(SENT_RE.search(t) for t in confirm_tokens):
        raise Stop("a SENT token was logged on the confirm: %s" % confirm_tokens)
    ctx_out["confirm_tokens"], ctx_out["cs"] = confirm_tokens, cs


def phase_c(browser, fs, cs, tokens, ctx_out):
    mt, shots = ctx_out["mt"], ctx_out["shots"]
    # shot 2: the filer reloads and reads its own ticket: the confirmed words
    fs.page.reload(wait_until="domcontentloaded", timeout=60000)
    fs.wait_board()
    fs.tab("Open")
    rows = fs.rows(mt)
    if rows[1].get_by_text(re.compile("^Confirmed for ")).count() != 1 or rows[1].get_by_role("button", name=re.compile("^Confirm ")).count() != 0:
        raise Stop("shot 2 precondition: the filer's row must show the confirmed words and no control")
    fs.shot("filer_confirmed", mt, rows, shots)
    # shot 3: the coordinator's view of the same ticket: the controls present
    cs.page.reload(wait_until="domcontentloaded", timeout=60000)
    cs.wait_board()
    cs.tab("Open")
    crow = cs.rows(mt)
    if crow[1].get_by_role("button", name=re.compile("^Confirm ")).count() < 1:
        raise Stop("shot 3 precondition: the coordinator's row must show the controls")
    cs.shot("coordinator_controls", mt, crow, shots)
    cs.ctx.close()
    # shot 4: the bystander (outside routing.primary): the outcome line and NO control
    vs = Session(browser, VIEW, tokens[VIEW], [mt])
    vs.open_board()
    vs.tab("Open")
    vrow = vs.rows(mt)
    if vrow[1].get_by_role("button").count() != 0 or vrow[1].get_by_text(re.compile("^Confirmed for ")).count() != 1:
        raise Stop("shot 4 precondition: the bystander must see the confirmed words and no control")
    vs.shot("bystander_no_control", mt, vrow, shots)
    vs.ctx.close()
    # claim then complete by the filer (two transitions on this synthetic ticket)
    fs.tab("Open")
    row, _ = fs.rows(mt)
    fs.allowed.add(("POST", "/api/scoped/tickets/%s/claim" % mt))
    t0 = int(time.time() * 1000) - 2000
    row.get_by_role("button", name="Claim", exact=True).click()
    fs.page.get_by_text("Claimed %s." % mt).wait_for(state="visible", timeout=45000)
    v = ticket_view(mt)
    say("CLAIM pressed; ConsistentRead status=%s assignee=%s" % (v["status"], v["assignee"]))
    claim_tokens = we_tokens(mt, t0, 90, need_client=True)
    nc = firm_no_contact(t0)
    say("CLAIM log tokens (ticket id on the line): %s ; WE_CLIENT_NO_CONTACT firm=%s lines since the click: %d" % (claim_tokens, FIRM, nc))
    if any(SENT_RE.search(t) for t in claim_tokens):
        raise Stop("a SENT token after the claim: %s; nothing further is done to the ticket" % claim_tokens)
    if v["status"] != "in_progress" or v["assignee"] != FILER:
        raise Stop("the claim did not land as in_progress under the filer")
    fs.tab("In Progress")
    row, _ = fs.rows(mt)
    fs.allowed.add(("POST", "/api/scoped/tickets/%s/complete" % mt))
    t1 = int(time.time() * 1000) - 2000
    row.get_by_role("button", name="Complete", exact=True).click()
    fs.page.get_by_text("Completed %s." % mt).wait_for(state="visible", timeout=45000)
    v2 = ticket_view(mt)
    say("COMPLETE pressed; ConsistentRead status=%s" % v2["status"])
    complete_tokens = we_tokens(mt, t1, 20)
    say("COMPLETE log tokens: %s" % complete_tokens)
    if any(SENT_RE.search(t) for t in complete_tokens) or v2["status"] != "completed":
        raise Stop("the complete did not leave the ticket completed, or a SENT token was logged")
    ctx_out.update({"claim_tokens": claim_tokens, "claim_no_contact_lines": nc, "complete_tokens": complete_tokens})
    # shot 5: the filer's own completed ticket: the confirmed words STILL shown, no control
    fs.page.reload(wait_until="domcontentloaded", timeout=60000)
    fs.wait_board()
    fs.tab("Completed")
    drow = fs.rows(mt)
    if drow[1].get_by_text(re.compile("^Confirmed for ")).count() != 1 or drow[1].get_by_role("button", name=re.compile("^Confirm ")).count() != 0:
        say("shot 5 precondition NOT met: the completed ticket does not show the confirmed words with no control (FWD-11 stays NOT REALIZED if so)")
    fs.shot("filer_completed", mt, drow, shots)
    # shot 6: the meeting form, opened and NOT submitted
    fs.page.get_by_role("button", name="New Ticket").first.click()
    sel = fs.page.locator("select").filter(has=fs.page.locator("option", has_text="Meeting Request")).first
    sel.wait_for(state="visible", timeout=30000)
    sel.select_option(label="Meeting Request")
    form = fs.page.locator('[data-slot="meeting-request-form"]')
    form.wait_for(state="visible", timeout=30000)
    fs.page.locator('select[aria-label="Firm"] option[value="%s"]' % FIRM).wait_for(state="attached", timeout=60000)
    form.scroll_into_view_if_needed()
    fb = form.bounding_box()
    heading = fs.page.get_by_text("New Ticket", exact=True).first
    hb = heading.bounding_box() if heading.count() else None
    sx, sy = fs.page.evaluate("[window.scrollX, window.scrollY]")
    x0 = min(fb["x"], hb["x"]) if hb else fb["x"]
    y0 = min(fb["y"], hb["y"]) if hb else fb["y"]
    x1 = max(fb["x"] + fb["width"], (hb["x"] + hb["width"]) if hb else 0)
    y1 = fb["y"] + fb["height"]
    fs._save("meeting_form", None, {"x": max(0, x0 + sx - 12), "y": max(0, y0 + sy - 12), "width": x1 - x0 + 24, "height": y1 - y0 + 24}, shots)
    say("meeting form shot taken; the form was NOT submitted")


def remove_rows():
    last = max(state["exp"]) if state["exp"] else 0
    wait = last + 5 - time.time()
    if wait > 0:
        say("waiting %ds for the LAST token to pass exp %s before the rows are removed" % (int(wait), iso(last)))
        time.sleep(wait)
    for who in state["written"]:
        try:
            ddb.delete_item(TableName=USERS, Key=key_of(who))
        except Exception as e:  # noqa: BLE001
            say("delete %s failed: %s" % (who.split("@")[0], type(e).__name__))
    deleted_at = iso()
    absent = all(item_of(USERS, key_of(who)) is None for who in (FILER, COORD, VIEW))
    say("rows deleted at %s; ConsistentRead ABSENT (all three)=%s" % (deleted_at, absent))
    return deleted_at, absent


def main():
    GATES.mkdir(exist_ok=True)
    stop = None
    ctx_out = {"shots": {}}
    rb = during = after = origin = None
    pw = browser = None
    try:
        from playwright.sync_api import sync_playwright
        rb = preflight()
        tokens, _ = write_rows_and_mint()
        pw = sync_playwright().start()
        try:
            browser = pw.chromium.launch(channel="msedge", headless=True)
        except Exception:  # noqa: BLE001
            browser = pw.chromium.launch(headless=True)
        fs, origin = phase_a(browser, tokens)
        say("MILESTONE STAGE1_READY first exp %s" % iso(min(state["exp"])))
        wait_flag("WINDOW_OPEN", min(state["exp"]) - 600, "applier applies the routing window and reads it back")
        during = routing_of(lam_cfg())
        say("routing_during (read by this process) meeting_request=%s" % json.dumps(during))
        if (during or {}).get("primary") != [COORD]:
            raise Stop("the live routing primary is not the synthetic coordinator alone")
        phase_b(browser, fs, tokens, ctx_out)
        say("MILESTONE CONFIRMED mt_ticket=%s" % ctx_out["mt"])
        wait_flag("WINDOW_CLOSED", min(state["exp"]) - 300, "applier closes the routing window")
        after = routing_of(lam_cfg())
        say("routing_after (read by this process) meeting_request=%s" % json.dumps(after))
        if (after or {}).get("primary") != [JEANETTE]:
            raise Stop("the live routing is not restored to jeanette alone")
        phase_c(browser, fs, ctx_out.pop("cs"), tokens, ctx_out)
        say("MILESTONE SHOTS_DONE %d shots" % len(ctx_out["shots"]))
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
            end = (max(state["exp"]) if state["exp"] else time.time()) + 600
            while time.time() < end and not flag("WINDOW_CLOSED"):
                time.sleep(2)
        deleted_at, absent = (None, None)
        if state["written"]:
            deleted_at, absent = remove_rows()
    eng = [k for k in trace["request_census"] if "/api/general/trades" in k]
    mt = ctx_out.get("mt")
    final = ticket_view(mt) if mt else None
    TRACE.write_text(json.dumps({"stop": stop, "exps": [iso(x) for x in state["exp"]], "row_deleted_at": deleted_at, "row_absent_after": absent,
                                 "routing_before": rb, "routing_during": during, "routing_after": after, "final_ticket": final,
                                 "ctx": {k: v for k, v in ctx_out.items() if k != "cs"}, "engine_requests_seen": eng, "trace": trace},
                                indent=1) + "\n", encoding="utf-8")
    if stop is None and absent and len(ctx_out["shots"]) == 6 and final and final["status"] == "completed":
        RESULT.write_text(json.dumps({
            "claim": "measured", "browser_origin": origin, "dev_sha": DEV_SHA, "filer": FILER, "coordinator_identity": COORD, "bystander": VIEW,
            "mt_ticket": mt, "mt_confirmed_time": TIME_1, "completed_by": FILER, "routing_before": rb, "routing_during": during,
            "routing_after": after, "shots": ctx_out["shots"], "row_deleted_at": deleted_at, "token_exp": iso(max(state["exp"])),
            "rows_absent_after": True, "no_engine_call": not eng, "token_printed": False, "server_reused": True, "firm": FIRM,
            "create_tokens": ctx_out["create_tokens"], "confirm_tokens": ctx_out["confirm_tokens"], "claim_tokens": ctx_out["claim_tokens"],
            "claim_no_contact_lines": ctx_out["claim_no_contact_lines"], "complete_tokens": ctx_out["complete_tokens"],
            "blocked_requests_count": len(trace["blocked_requests"])}, indent=1) + "\n", encoding="utf-8")
        say("result written: %s" % RESULT.name)
        return 0
    say("trace written: %s" % TRACE.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
