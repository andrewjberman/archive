"""TCKT_VNEXT TO-R20-PROD2 (PART 6, FWD-11 journey ON PROD) -- 0.7.0_AE_CloudOps~TV2.

Pair : R18_RUN_PAIR.md AMENDMENTS 8 and 9 (COO blob 0b2978bfea, CTO half e7a33cf976); order AMENDMENT 1 (GO msg 10800, hold lifted msg 10833).
A synthetic filer FILES one Meeting Request on https://opalinvest.dev, a synthetic coordinator CONFIRMS it inside one routing window, the filer reads the
confirmed line. Then the ONE synthetic ticket (record saved first) and BOTH identity rows are deleted by key.
One process holds the signing key and both tokens; a token is never printed, written or traced: it reaches a page only as the body of a stubbed
/auth/refresh response inside one in-memory context. Gate files in ./gates are written by the applier; the routing window is applied by the applier
under safe-apply. The New Ticket type list is RECORDED whole (a Trade Request option is expected after the TO-DB-b-336 release and is not a STOP); no
Trade Request type is selected and no attachment route is called. A PROD head that moves after the start gate is a STOP. Shots are clipped to the one
ticket's two board rows (or the form); path and byte count are printed, nothing is described; the contrast of the confirmed line is measured from the
saved PNG (WCAG relative luminance) and printed as a number. The ticket delete is guarded: it names the printed id and refuses unless the stored item
was created by the synthetic filer and is a meeting_request, and never any protected ticket.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import boto3
import jwt as pyjwt
from botocore.exceptions import ClientError
from PIL import Image

REGION = "us-east-1"
ORIGIN = "https://opalinvest.dev"
HOSTPORT = "opalinvest.dev"
USERS, TICKETS = "opal-users-v2", "opal-tickets"
STAMP = "20261019"
FILER = "tckt-r20-pfiler-%s@opal.invalid" % STAMP
COORD = "tckt-r20-pcoord-%s@opal.invalid" % STAMP
NAMES = {FILER: "TCKT R20 PROD synthetic filer", COORD: "TCKT R20 PROD synthetic coordinator"}
FIRM = "cottonwood"
FN = "opal-ticket-api"
EXPECT_SHA = "iRxJZYp6IXEtiXDRMT4R/EOwKvsqh5Id5NNgPcpy3RM="
JEANETTE = "jeanette@opalinvest.com"
PROTECTED = {"TCK-20261017-da2a1987", "TCK-20261017-5af976ff"}
PORTAL = "C:/dev/ajb_workspace/portal"
START_HEAD = "8cd45f623bdfae12ac6e4cfcfc8e0d74325ed4c3"
LIFE = 1080  # 18 minutes; the pair allows at most 20. Each safe-apply costs ~70 s in the seat-gate check plus any halt-gate stop
KEY_SECRET = "opal/auth/jwt-private-key"
TIME_1 = "2026-10-26 14:00 ET (R20 PROD run 20261019)"
TIME_2 = "2026-10-27 10:30 ET (R20 PROD run 20261019)"
WHO = "TCKT R20 PROD synthetic coordinator (test)"
PURPOSE = "Synthetic live run of the Meeting Request on PROD. No client data."
SENT_RE = re.compile(r"WE_[A-Z_]*SENT\b")

OUT = Path(__file__).resolve().parent
GATES = OUT / "gates"
TRACE = OUT / "R20_PROD2_TRACE.json"
RESULT = OUT / "R20_PROD2_RESULT.json"
RECORD = OUT / "R20_PROD2_TICKET_ITEM.json"
SHOT_DIR_REL = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_prod2/"

ddb = boto3.client("dynamodb", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)
state = {"written": [], "exp": [], "mt": None}
trace = {"claim": "measured", "executor": "0.7.0_AE_CloudOps~TV2", "events": [], "blocked_requests": [], "request_census": {}, "statuses": {}}


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


def lam_cfg():
    return boto3.client("lambda", region_name=REGION).get_function_configuration(FunctionName=FN)


def routing_of(cfg):
    return json.loads(((cfg.get("Environment") or {}).get("Variables") or {}).get("ROUTING_MATRIX") or "{}").get("meeting_request")


def prod_head():
    out = subprocess.check_output(["git", "-C", PORTAL, "ls-remote", "origin", "refs/heads/PROD"], text=True).strip()
    return out.split()[0] if out else ""


def check_head(label):
    h = prod_head()
    if h != START_HEAD:
        raise Stop("origin/PROD moved after the start gate (%s): %s is not %s" % (label, h, START_HEAD))
    say("PROD head check (%s): %s unchanged" % (label, h[:12]))


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
    if code is None:
        raise Stop("the PROD site could not be read in 3 attempts (%s)" % last)
    say("GET %s/ -> %s" % (ORIGIN, code))
    if code != 200:
        raise Stop("the PROD site does not answer 200")
    cfg = lam_cfg()
    say("deployed %s CodeSha256=%s State=%s" % (FN, cfg["CodeSha256"], cfg.get("State")))
    if cfg["CodeSha256"] != EXPECT_SHA:
        raise Stop("deployed CodeSha256 differs from the R20 release")
    rb = routing_of(cfg)
    say("routing_before meeting_request=%s" % json.dumps(rb))
    if (rb or {}).get("primary") != [JEANETTE]:
        raise Stop("routing before the window is not jeanette alone")
    for t in sorted(PROTECTED):
        if item_of(TICKETS, {"ticket_id": {"S": t}}) is None:
            raise Stop("protected ticket %s is missing before the run" % t)
    for who in (FILER, COORD):
        if item_of(USERS, key_of(who)) is not None:
            raise Stop("an identity row is already PRESENT")
    say("both identity keys ConsistentRead ABSENT; the two protected tickets are present (read only)")
    return rb


def write_rows_and_mint():
    tokens = {}
    for ident in (FILER, COORD):
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
    for ident in (FILER, COORD):
        iat = int(time.time())
        claims = {"sub": ident, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal",
                  "role": "user", "userType": "test-filer", "name": NAMES[ident], "iat": iat, "exp": iat + LIFE}
        tokens[ident] = pyjwt.encode(claims, pem, algorithm="RS256")
        state["exp"].append(iat + LIFE)
        say("token minted for %s (memory only) iat=%s exp=%s life=%ds" % (ident.split("@")[0], iso(iat), iso(iat + LIFE), LIFE))
    del pem
    return tokens


def lum(rgb):
    def c(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def contrast(png_path, crop):
    img = Image.open(png_path).convert("RGB")
    x, y, w, h = [int(round(v)) for v in crop]
    x, y = max(0, x), max(0, y)
    reg = img.crop((x, y, min(img.width, x + w), min(img.height, y + h)))
    px = list(reg.get_flattened_data()) if hasattr(reg, "get_flattened_data") else list(reg.getdata())
    bg = Counter(px).most_common(1)[0][0]
    lb = lum(bg)
    ink = max(px, key=lambda p: abs(lum(p) - lb))
    return round((max(lb, lum(ink)) + 0.05) / (min(lb, lum(ink)) + 0.05), 2), bg, ink, (x, y, w, h), len(px)


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
        for loc in (pg.get_by_role("tab", name=label, exact=True), pg.get_by_role("button", name=label, exact=True), pg.get_by_text(label, exact=True)):
            if loc.count():
                loc.first.click()
                return
        raise Stop("board tab %r not found" % label)

    def rows(self, mt):
        row = self.page.locator("tbody tr").filter(has=self.page.locator("td", has_text=mt)).first
        row.wait_for(state="visible", timeout=60000)
        out = row.locator("xpath=following-sibling::tr[1]")
        out.locator('[data-slot="meeting-outcome-line"]').wait_for(state="visible", timeout=30000)
        return row, out

    def shot(self, role, mt, rows, results):
        row, out = rows
        row.scroll_into_view_if_needed()
        b1, b2 = row.bounding_box(), out.bounding_box()
        sx, sy = self.page.evaluate("[window.scrollX, window.scrollY]")
        x0, y0 = min(b1["x"], b2["x"]), min(b1["y"], b2["y"])
        x1, y1 = max(b1["x"] + b1["width"], b2["x"] + b2["width"]), max(b1["y"] + b1["height"], b2["y"] + b2["height"])
        clip = {"x": max(0, x0 + sx - 8), "y": max(0, y0 + sy - 8), "width": x1 - x0 + 16, "height": y1 - y0 + 16}
        name = "%s__%s__%s__opalinvest-dev.png" % (role, self.ident.split("@")[0], mt)
        path = OUT / name
        self.page.screenshot(path=str(path), clip=clip, full_page=True)
        size = path.stat().st_size
        say("SHOT %s saved: %s (%d bytes)" % (role, SHOT_DIR_REL + name, size))
        results[role] = {"path": SHOT_DIR_REL + name, "bytes": size, "viewer": self.ident, "origin": ORIGIN}
        return path, clip


def ticket_view(tid):
    it = item_of(TICKETS, {"ticket_id": {"S": tid}})
    if it is None:
        raise Stop("ticket not found")
    meeting = (it.get("meeting") or {}).get("M") or {}
    routing = (it.get("routing") or {}).get("M") or {}
    return {"ticket_type": (it.get("ticket_type") or {}).get("S"), "status": (it.get("status") or {}).get("S"),
            "primary": [x.get("S") for x in (routing.get("primary") or {}).get("L", [])], "created_by": (it.get("created_by") or {}).get("S"),
            "meeting": {k: (v.get("S") if "S" in v else None) for k, v in meeting.items() if k in ("status", "time", "by")}}


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


def phase_a(browser, tokens, ctx_out):
    fs = Session(browser, FILER, tokens[FILER], [])
    origin = fs.open_board()
    pg = fs.page
    pg.get_by_role("button", name="New Ticket").first.click()
    sel = pg.locator("select").filter(has=pg.locator("option", has_text="Meeting Request")).first
    sel.wait_for(state="visible", timeout=30000)
    options = [t.strip() for t in sel.locator("option").all_inner_texts()]
    say("New Ticket type options recorded (whole, before anything is chosen): %s" % options)
    ctx_out["type_options"] = options
    sel.select_option(label="Meeting Request")
    firm = pg.locator('select[aria-label="Firm"]')
    firm.wait_for(state="visible", timeout=30000)
    pg.locator('select[aria-label="Firm"] option[value="%s"]' % FIRM).wait_for(state="attached", timeout=60000)
    firm.select_option(value=FIRM)
    pg.get_by_label("Who", exact=True).fill(WHO)
    pg.get_by_label("Purpose", exact=True).fill(PURPOSE)
    pg.get_by_label("Proposed time 1", exact=True).fill(TIME_1)
    pg.get_by_label("Proposed time 2", exact=True).fill(TIME_2)
    say("filer: Meeting Request form filled on %s, NOT yet submitted (no write made)" % ORIGIN)
    return fs, origin


def phase_b(browser, fs, tokens, ctx_out):
    fp = fs.page
    submit = fp.locator('[data-slot="meeting-request-submit"]')
    submit.wait_for(state="visible", timeout=30000)
    if not submit.is_enabled():
        raise Stop("the submit is held: the form is incomplete")
    check_head("before the filing")
    fs.allowed.add(("POST", "/api/scoped/tickets"))
    since_ms = int(time.time() * 1000) - 2000
    submit.click()
    notice = fp.get_by_text(re.compile(r"Meeting request \S+ filed\.")).first
    try:
        notice.wait_for(state="visible", timeout=60000)
    except Exception as e:  # noqa: BLE001
        raise Stop("no filed notice after the submit (%s)" % type(e).__name__)
    mt = re.search(r"Meeting request (\S+) filed\.", notice.inner_text()).group(1)
    state["mt"] = mt
    fs.tids.append(mt)
    say("filer: MEETING TICKET FILED ON PROD %s" % mt)
    if mt in PROTECTED:
        raise Stop("the filed ticket id is a protected ticket")
    v = ticket_view(mt)
    say("ticket %s ConsistentRead: type=%s status=%s routing.primary=%s created_by=%s" % (mt, v["ticket_type"], v["status"], v["primary"], v["created_by"]))
    if v["ticket_type"] != "meeting_request" or v["status"] != "open" or v["primary"] != [COORD] or v["created_by"] != FILER:
        raise Stop("the filed ticket is not an open meeting_request created by the filer with the coordinator alone as routing.primary")
    create_tokens = we_tokens(mt, since_ms, 75)
    say("CREATE log tokens for %s: %s" % (mt, create_tokens))
    if any(SENT_RE.search(t) for t in create_tokens):
        raise Stop("a SENT token was logged on the CREATE: %s" % create_tokens)
    ctx_out["mt"], ctx_out["create_tokens"] = mt, create_tokens
    fs.tab("Open")
    rows = fs.rows(mt)
    if rows[1].get_by_text("Waiting for the coordinator").count() != 1 or rows[1].get_by_role("button", name=re.compile("^Confirm ")).count() != 0:
        raise Stop("shot 1 precondition: the filer's row must show the waiting words and no control")
    fs.shot("prod_filer_waiting", mt, rows, ctx_out["shots"])
    cs = Session(browser, COORD, tokens[COORD], [mt])
    cs.open_board()
    cs.tab("Open")
    crow = cs.rows(mt)
    btn = cs.page.get_by_role("button", name="Confirm " + TIME_1, exact=True)
    try:
        btn.wait_for(state="visible", timeout=60000)
    except Exception as e:  # noqa: BLE001
        raise Stop("the coordinator does not see the confirm control for the filed ticket: %s" % type(e).__name__)
    cs.shot("prod_coordinator_controls", mt, crow, ctx_out["shots"])  # BEFORE the click
    check_head("before the confirm")
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
    cs.ctx.close()
    ctx_out["confirm_tokens"] = confirm_tokens


def phase_c(fs, ctx_out):
    mt = ctx_out["mt"]
    check_head("before the final shot")
    fs.page.reload(wait_until="domcontentloaded", timeout=60000)
    fs.wait_board()
    fs.tab("Open")
    rows = fs.rows(mt)
    if rows[1].get_by_text(re.compile("^Confirmed for ")).count() != 1 or rows[1].get_by_role("button", name=re.compile("^Confirm ")).count() != 0:
        raise Stop("shot 3 precondition: the filer's row must show the confirmed words and no control")
    path, clip = fs.shot("prod_filer_confirmed", mt, rows, ctx_out["shots"])
    bl = rows[1].locator('[data-slot="meeting-outcome-line"]').bounding_box()
    sx, sy = fs.page.evaluate("[window.scrollX, window.scrollY]")
    ratio, bg, ink, box, npx = contrast(path, (bl["x"] + sx - clip["x"], bl["y"] + sy - clip["y"], bl["width"], bl["height"]))
    say("CONTRAST of the confirmed line, from the saved PNG: %.2f:1 (WCAG; strongest text pixel rgb%s against the row background rgb%s; crop %s, %d pixels)"
        % (ratio, ink, bg, box, npx))
    ctx_out["contrast"] = {"ratio": ratio, "ink_rgb": list(ink), "bg_rgb": list(bg), "crop_px": list(box), "pixels": npx,
                           "method": "WCAG 2.x relative luminance; ink = the pixel in the line's box farthest in luminance from the box's most common colour"}


def remove_all():
    last = max(state["exp"]) if state["exp"] else 0
    wait = last + 5 - time.time()
    if wait > 0:
        say("waiting %ds for the LAST token to pass exp %s before anything is removed" % (int(wait), iso(last)))
        time.sleep(wait)
    ticket_deleted_at, ticket_absent = None, None
    mt = state["mt"]
    if mt:
        item = item_of(TICKETS, {"ticket_id": {"S": mt}})
        if item is not None:
            RECORD.write_text(json.dumps(item, indent=1, default=str, sort_keys=True) + "\n", encoding="utf-8")
            say("ticket record saved whole to %s (%d bytes) BEFORE the delete" % (RECORD.name, RECORD.stat().st_size))
            say("DELETE BY KEY: opal-tickets ticket_id=%s (printed before the delete)" % mt)
            if mt in PROTECTED:
                say("REFUSED: protected ticket id")
            elif (item.get("created_by") or {}).get("S") != FILER or (item.get("ticket_type") or {}).get("S") != "meeting_request":
                say("REFUSED: the stored item is not a meeting_request created by the synthetic filer")
            else:
                try:
                    ddb.delete_item(TableName=TICKETS, Key={"ticket_id": {"S": mt}},
                                    ConditionExpression="created_by = :f AND ticket_type = :t",
                                    ExpressionAttributeValues={":f": {"S": FILER}, ":t": {"S": "meeting_request"}})
                except ClientError as e:
                    say("ticket delete failed: %s" % e.response["Error"]["Code"])
        ticket_deleted_at = iso()
        ticket_absent = item_of(TICKETS, {"ticket_id": {"S": mt}}) is None
        say("ticket %s deleted at %s; ConsistentRead ABSENT=%s" % (mt, ticket_deleted_at, ticket_absent))
    for who in state["written"]:
        try:
            ddb.delete_item(TableName=USERS, Key=key_of(who))
        except Exception as e:  # noqa: BLE001
            say("delete %s failed: %s" % (who.split("@")[0], type(e).__name__))
    deleted_at = iso()
    absent = all(item_of(USERS, key_of(who)) is None for who in (FILER, COORD))
    say("rows deleted at %s; ConsistentRead ABSENT (both)=%s" % (deleted_at, absent))
    return deleted_at, absent, ticket_deleted_at, ticket_absent


def main():
    GATES.mkdir(exist_ok=True)
    stop = None
    ctx_out = {"shots": {}}
    rb = during = after = origin = None
    pw = browser = None
    fire = (OUT / "fire_windows_answer.txt").read_text(encoding="utf-8")
    try:
        from playwright.sync_api import sync_playwright
        rb = preflight()
        tokens = write_rows_and_mint()
        pw = sync_playwright().start()
        try:
            browser = pw.chromium.launch(channel="msedge", headless=True)
        except Exception:  # noqa: BLE001
            browser = pw.chromium.launch(headless=True)
        fs, origin = phase_a(browser, tokens, ctx_out)
        say("MILESTONE STAGE1_READY first exp %s" % iso(min(state["exp"])))
        wait_flag("WINDOW_OPEN", min(state["exp"]) - 300, "applier applies the routing window and reads it back")
        during = routing_of(lam_cfg())
        say("routing_during (read by this process) meeting_request=%s" % json.dumps(during))
        if (during or {}).get("primary") != [COORD]:
            raise Stop("the live routing primary is not the synthetic coordinator alone")
        phase_b(browser, fs, tokens, ctx_out)
        say("MILESTONE CONFIRMED mt_ticket=%s" % ctx_out["mt"])
        wait_flag("WINDOW_CLOSED", min(state["exp"]) - 120, "applier closes the routing window")
        after = routing_of(lam_cfg())
        say("routing_after (read by this process) meeting_request=%s" % json.dumps(after))
        if (after or {}).get("primary") != [JEANETTE]:
            raise Stop("the live routing is not restored to jeanette alone")
        phase_c(fs, ctx_out)
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
            say("MILESTONE WINDOW-STILL-OPEN waiting for WINDOW_CLOSED before anything is removed")
            end = (max(state["exp"]) if state["exp"] else time.time()) + 600
            while time.time() < end and not flag("WINDOW_CLOSED"):
                time.sleep(2)
        deleted_at = absent = ticket_deleted_at = ticket_absent = None
        if state["written"]:
            deleted_at, absent, ticket_deleted_at, ticket_absent = remove_all()
    eng = [k for k in trace["request_census"] if "/api/general/trades" in k or "attachment-upload" in k]
    TRACE.write_text(json.dumps({"stop": stop, "exps": [iso(x) for x in state["exp"]], "row_deleted_at": deleted_at, "rows_absent_after": absent,
                                 "ticket_deleted_at": ticket_deleted_at, "ticket_absent_after": ticket_absent, "routing_before": rb,
                                 "routing_during": during, "routing_after": after, "start_head": START_HEAD,
                                 "ctx": ctx_out, "engine_or_attachment_requests_seen": eng, "trace": trace}, indent=1, default=str) + "\n", encoding="utf-8")
    if stop is None and absent and ticket_absent and len(ctx_out["shots"]) == 3 and ctx_out.get("contrast"):
        RESULT.write_text(json.dumps({
            "claim": "measured", "browser_origin": origin,
            "promote_proof": "git ls-remote origin refs/heads/PROD = %s at the start gate and unchanged at every stage check; 2a64d211 an ancestor; "
                             "TicketCenter.tsx at that head no longer filters trade_request and imports TradeFormOpen from ./TradeRequestParts; the promote's CI "
                             "run 39294118121 (Deploy to Production, PROD, push) completed success at 2026-10-19T17:26:22Z (gh run list); GET %s/ 200"
                             % (START_HEAD, ORIGIN),
            "filer": FILER, "coordinator_identity": COORD, "mt_ticket": ctx_out["mt"], "mt_confirmed_time": TIME_1,
            "routing_before": rb, "routing_during": during, "routing_after": after, "type_options": ctx_out["type_options"], "shots": ctx_out["shots"],
            "contrast_ratio": ctx_out["contrast"]["ratio"], "contrast_record": ctx_out["contrast"], "fire_windows_answer": fire,
            "row_deleted_at": deleted_at, "token_exp": iso(max(state["exp"])), "ticket_deleted_at": ticket_deleted_at, "ticket_absent_after": True,
            "rows_absent_after": True, "no_engine_call": not eng, "token_printed": False, "create_tokens": ctx_out["create_tokens"],
            "confirm_tokens": ctx_out["confirm_tokens"], "blocked_requests_count": len(trace["blocked_requests"])}, indent=1) + "\n", encoding="utf-8")
        say("result written: %s" % RESULT.name)
        return 0
    say("trace written: %s" % TRACE.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
