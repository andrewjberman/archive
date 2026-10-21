"""TCKT_VNEXT TO-R23-F51 (cell R23-f5-1, FWD-5 ON DEV) -- a picker claims one of two open tickets FROM THE BOARD (0.7.0_AE_CloudOps~TV2).

Order: TCKT_VNEXT.TO-R23-F51 (GO msg 11773; CVO ADJUDICATION_v21 via CTO msg 11772). Two synthetic internal identities (filer, picker): the filer files ONE Service Request and
ONE Other ticket through the New Ticket form; the picker, in a SEPARATE browser context, reads the whole board, takes the full-page shot r23_board_full, records each of the two
rows' type label and age text as read, chooses one, presses Claim IN THE BOARD ROW (neither ticket is opened), takes r23_board_claimed. Both tickets are saved whole with
`aws dynamodb get-item --consistent-read` BEFORE any delete, then, after BOTH tokens' exp, both tickets and both identity rows are deleted by key and read ABSENT.
A token is never printed, written or put in a trace: it reaches a page only as the body of a stubbed /auth/refresh response in that one in-memory context. The dev server
on localhost:5174 is the CTO's: this script never starts, stops or edits it. Every API-shaped request other than the gated ones is aborted and logged by method and path.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import boto3
import jwt as pyjwt
from botocore.exceptions import ClientError

REGION = "us-east-1"
ORIGIN = "http://localhost:5174"
HOSTPORT = "localhost:5174"
USERS, TICKETS = "opal-users-v2", "opal-tickets"
STAMP = "20261021"
FILER = "tckt-r23-filer-%s@opal.invalid" % STAMP
PICKER = "tckt-r23-picker-%s@opal.invalid" % STAMP
NAMES = {FILER: "TCKT R23 synthetic filer", PICKER: "TCKT R23 synthetic picker"}
FIRM = "cottonwood"
KEY_SECRET = "opal/auth/jwt-private-key"
LIFE = 480
SERVER_TREE = "C:/dev/smoke-template-5174"
PORTAL = "C:/dev/ajb_workspace/portal"
PROTECTED = {"TCK-20261017-da2a1987", "TCK-20261017-5af976ff"}
TITLE = "synthetic FWD-5 arm"
DESC = "synthetic FWD-5 arm"
LABEL = {"service_request": "Service Request", "other": "Other"}
BASE = Path(__file__).resolve().parent
GATES = BASE / "gates"
TRACE = BASE / "R23_FWD5_TRACE.json"
RESULT = BASE / "R23_FWD5_RESULT.json"
RECORD = BASE / "R23_FWD5_TICKET_ITEMS.json"
SHOT_DIR_REL = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r23_fwd5_dev/"

ddb = boto3.client("dynamodb", region_name=REGION)
state = {"written": [], "exp": [], "tickets": {}, "engine": False, "opened": False}
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


def key_of(ident):
    return {"PK": {"S": "USER#" + ident}, "SK": {"S": "PROFILE"}}


def item_of(table, key):
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def cli_item(tid):
    """The exact `aws dynamodb get-item --consistent-read` output for one ticket (saved unchanged)."""
    p = subprocess.run([".tools/aws", "dynamodb", "get-item", "--table-name", TICKETS, "--key", json.dumps({"ticket_id": {"S": tid}}),
                        "--consistent-read", "--region", REGION, "--output", "json"], capture_output=True, text=True, timeout=120)
    if p.returncode != 0 or not p.stdout.strip():
        raise Stop("get-item for %s failed: rc=%d" % (tid, p.returncode))
    return json.loads(p.stdout)


def count_tickets(status):
    n, total = 0, 0
    kw = {"TableName": TICKETS, "ProjectionExpression": "ticket_id, #s", "ExpressionAttributeNames": {"#s": "status"}}
    for page in ddb.get_paginator("scan").paginate(**kw):
        for it in page.get("Items", []):
            total += 1
            if it.get("status", {}).get("S") == status:
                n += 1
    return n, total


def norm_path(p):
    return re.sub(r"TCK-[0-9]{8}-[0-9a-f]{8}", "<T>", p)


def preflight():
    now = dt.datetime.now(dt.timezone.utc)
    hm = now.hour * 60 + now.minute
    if now.weekday() < 5 and 11 * 60 + 30 <= hm < 14 * 60 + 15:
        raise Stop("weekday band 11:30Z to 14:15Z: no run")
    head = subprocess.check_output(["git", "-C", SERVER_TREE, "rev-parse", "HEAD"], text=True).strip()
    dirty = subprocess.check_output(["git", "-C", SERVER_TREE, "status", "--short"], text=True).strip()
    portal_head = subprocess.check_output(["git", "-C", PORTAL, "rev-parse", "HEAD"], text=True).strip()
    origin_dev = subprocess.check_output(["git", "-C", PORTAL, "rev-parse", "origin/DEV"], text=True).strip()
    behind = subprocess.check_output(["git", "-C", PORTAL, "diff", "--name-only", head, origin_dev, "--", "src/pages/TicketCenter"], text=True).split()
    state["served_head"], state["behind"] = head, len(behind)
    say("served checkout %s HEAD=%s dirty=%s; workspace portal checkout HEAD=%s; origin/DEV=%s; TicketCenter files behind origin/DEV: %d"
        % (SERVER_TREE, head, "yes" if dirty else "no", portal_head, origin_dev, len(behind)))
    if dirty:
        raise Stop("the served checkout has uncommitted changes")
    code = urllib.request.urlopen(ORIGIN + "/src/api/endpoints/tickets.ts", timeout=30).read().decode("utf-8", "replace")
    labels = re.findall(r"""(service_request|other|meeting_request|analysis_request|trade_request)\s*:\s*["']([^"']+)["']""", code)
    say("served type labels (TICKET_TYPE_LABELS as served): %s" % labels)
    got = dict(labels)
    if got.get("service_request") != "Service Request" or got.get("other") != "Other":
        raise Stop("the served type list does not carry Service Request and Other")
    for who in (FILER, PICKER):
        if item_of(USERS, key_of(who)) is not None:
            raise Stop("an identity row is already PRESENT")
    say("both identity keys ConsistentRead ABSENT")
    for t in sorted(PROTECTED):
        if item_of(TICKETS, {"ticket_id": {"S": t}}) is None:
            raise Stop("protected ticket %s is missing" % t)
    n_open, n_all = count_tickets("open")
    state["open_before"] = n_open
    say("protected tickets present (read only); open tickets already on the board table: %d of %d tickets (they will appear in the shot)" % (n_open, n_all))


def write_rows_and_mint():
    tokens = {}
    for ident in (FILER, PICKER):
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
    for ident in (FILER, PICKER):
        iat = int(time.time())
        claims = {"sub": ident, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal", "role": "user",
                  "userType": "test-filer", "name": NAMES[ident], "iat": iat, "exp": iat + LIFE}
        tokens[ident] = pyjwt.encode(claims, pem, algorithm="RS256")
        state["exp"].append(iat + LIFE)
        say("token minted for %s (memory only) iat=%s exp=%s life=%ds" % (ident.split("@")[0], iso(iat), iso(iat + LIFE), LIFE))
    del pem
    return tokens


class Session:
    def __init__(self, browser, ident, token):
        self.ident, self.allowed, self.violations = ident, set(), []
        user = {"email": ident, "name": NAMES[ident], "role": "user", "mustChangePassword": False, "firmId": "opal-capital",
                "userType": "test-filer", "advisorId": None, "firmRole": None, "advisorRole": None}
        auth_body = json.dumps({"accessToken": token, "user": user})
        self.ctx = browser.new_context(viewport={"width": 1440, "height": 1000})

        def on_route(route):
            req = route.request
            u = urlparse(req.url)
            k = "%s %s %s" % (req.method, u.netloc, norm_path(u.path))
            trace["request_census"][k] = trace["request_census"].get(k, 0) + 1
            if u.netloc != HOSTPORT:
                if req.resource_type in ("font", "stylesheet", "image", "media"):
                    return route.continue_()
                trace["blocked_requests"].append("%s %s %s" % (req.method, u.netloc, req.resource_type))
                if req.resource_type == "document":
                    self.violations.append(u.netloc)
                return route.abort()
            p = u.path
            if "/api/general/trades" in p:
                state["engine"] = True
                self.violations.append("ENGINE " + p)
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
                if (req.method, p) in self.allowed:
                    self.allowed.discard((req.method, p))
                    return route.continue_()
                trace["blocked_requests"].append("%s %s" % (req.method, norm_path(p)))
                return route.abort()
            return route.continue_()

        self.ctx.route("**/*", on_route)
        self.page = self.ctx.new_page()
        self.created = []

        def on_response(r):
            p = urlparse(r.url).path
            who = "filer" if self.ident == FILER else "picker"
            if r.request.method == "POST" and p.startswith("/api/scoped/tickets"):
                trace["statuses"]["POST %s as %s" % (norm_path(p), who)] = r.status
                if p == "/api/scoped/tickets" and r.status in (200, 201):
                    try:
                        body = r.json()
                    except Exception:  # noqa: BLE001
                        body = {}
                    tk = (body or {}).get("ticket") or {}
                    self.created.append((tk.get("ticket_id"), tk.get("ticket_type")))

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

    def file_one(self, kind):
        """Open New Ticket, choose the type, fill title and details, press Create Ticket; return (ticket_id, type) from the create response."""
        pg = self.page
        before = len(self.created)
        pg.get_by_role("button", name="New Ticket").first.click()
        sel = pg.locator("select").filter(has=pg.locator("option", has_text=LABEL[kind])).first
        sel.wait_for(state="visible", timeout=30000)
        sel.select_option(label=LABEL[kind])
        pg.get_by_placeholder("Title (what is being requested?)").fill(TITLE)
        pg.locator("textarea").first.fill(DESC)
        btn = pg.get_by_role("button", name="Create Ticket")
        if not btn.is_enabled():
            raise Stop("Create Ticket is held for %s" % kind)
        self.allowed.add(("POST", "/api/scoped/tickets"))
        btn.click()
        pg.get_by_text("Ticket created.").first.wait_for(state="visible", timeout=60000)
        if len(self.created) != before + 1 or not self.created[-1][0]:
            raise Stop("the create response carried no ticket id for %s" % kind)
        tid, ttype = self.created[-1]
        state["tickets"][tid] = ttype
        say("filer: %s ticket filed on DEV %s (type %s)" % (LABEL[kind], tid, ttype))
        if ttype != kind:
            raise Stop("the created ticket type %r is not %r" % (ttype, kind))
        return tid

    def row(self, tid):
        r = self.page.locator("tbody tr").filter(has=self.page.locator("td", has_text=tid)).first
        r.wait_for(state="visible", timeout=60000)
        return r

    def read_row(self, tid):
        r = self.row(tid)
        cells = r.locator("td")
        type_label = cells.nth(1).inner_text().strip()
        age = r.locator('[data-slot="ticket-age"]')
        age_text = age.first.inner_text().strip() if age.count() else ""
        created = cells.nth(4).inner_text().strip()
        return {"type_label": type_label, "age_text": age_text, "created_cell": created, "status_text": cells.nth(6).inner_text().strip(),
                "has_claim": r.get_by_role("button", name="Claim", exact=True).count() == 1}

    def shot_full(self, role, tid_tag, results):
        name = "%s__%s__%s__localhost-5174.png" % (role, self.ident.split("@")[0], tid_tag)
        path = BASE / name
        self.page.screenshot(path=str(path), full_page=True)
        size = path.stat().st_size
        rows = self.page.locator("tbody tr:visible").count()
        say("SHOT %s saved (FULL PAGE): %s (%d bytes, %d board rows visible)" % (role, SHOT_DIR_REL + name, size, rows))
        results[role] = {"path": SHOT_DIR_REL + name, "bytes": size, "origin": ORIGIN, "viewer": self.ident, "full_page": True, "rows_visible": rows}
        trace["shots_taken"].append(role)


def age_seconds(text):
    """Seconds from an age text like '(2m)', '(45s)', '(1.2h)'; None when unreadable."""
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*(s|m|h|d)", text or "")
    if not m:
        return None
    return float(m.group(1)) * {"s": 1, "m": 60, "h": 3600, "d": 86400}[m.group(2)]


def choose(board_read):
    ids = sorted(board_read)
    a, b = ids[0], ids[1]
    sa, sb = age_seconds(board_read[a]["age_text"]), age_seconds(board_read[b]["age_text"])
    la = board_read[a]["type_label"]
    if sa is not None and sb is not None and sa != sb:
        pick, other = (a, b) if sa > sb else (b, a)
        basis = ("Both rows read status open and unclaimed; %s (%s) shows the longer wait %s against %s (%s) at %s, so I took the one that has waited longest."
                 % (pick, board_read[pick]["type_label"], board_read[pick]["age_text"], other, board_read[other]["type_label"], board_read[other]["age_text"]))
        return pick, other, basis
    pick, other = (a, b) if la == "Service Request" else (b, a)
    basis = ("Both rows read status open and unclaimed with the same age text (%s and %s); I took the Service Request row (%s, type %s) over the %s row (%s), a client-service type before a general one."
             % (board_read[a]["age_text"] or "none", board_read[b]["age_text"] or "none", pick, board_read[pick]["type_label"],
                board_read[other]["type_label"], other))
    return pick, other, basis


def journey(browser, tokens, out):
    fs = Session(browser, FILER, tokens[FILER])
    out["origin"] = fs.open_board()
    out["filer_session"] = fs
    t_service = fs.file_one("service_request")
    fs.tab("Open")
    t_other = fs.file_one("other")
    for t in (t_service, t_other):
        if t in PROTECTED:
            raise Stop("a filed ticket id is protected")
        v = item_of(TICKETS, {"ticket_id": {"S": t}})
        if v is None or v["created_by"]["S"].lower() != FILER or v["status"]["S"] != "open":
            raise Stop("ticket %s is not an open ticket by the filer" % t)
    if len(state["tickets"]) != 2:
        raise Stop("not exactly two tickets filed")
    ps = Session(browser, PICKER, tokens[PICKER])
    ps.open_board()
    ps.tab("Open")
    board_read = {}
    for t in (t_service, t_other):
        board_read[t] = ps.read_row(t)
        say("board row %s read as picker: type=%r age=%r status=%r claim_control=%s" % (t, board_read[t]["type_label"], board_read[t]["age_text"],
                                                                                    board_read[t]["status_text"], board_read[t]["has_claim"]))
        if not board_read[t]["has_claim"]:
            raise Stop("the board row for %s carries no Claim control (FWD-5 failing)" % t)
        if not board_read[t]["type_label"] or not board_read[t]["age_text"]:
            raise Stop("the board row for %s shows no type or no age text (FWD-5 failing)" % t)
    shots = {}
    ps.shot_full("r23_board_full", "board", shots)
    pick, other, basis = choose(board_read)
    say("picker chooses %s over %s: %s" % (pick, other, basis))
    ps.allowed.add(("POST", "/api/scoped/tickets/%s/claim" % pick))
    ps.row(pick).get_by_role("button", name="Claim", exact=True).click()
    ps.page.get_by_text("Claimed %s." % pick).first.wait_for(state="visible", timeout=60000)
    say("picker claimed %s FROM THE BOARD (no ticket opened); claim status %s" % (pick, trace["statuses"].get("POST /api/scoped/tickets/<T>/claim as picker")))
    ps.shot_full("r23_board_claimed", "board", shots)
    out.update({"picker_session": ps, "pick": pick, "other": other, "basis": basis, "board_read": board_read, "shots": shots})


def wait_review(deadline):
    """After exp: the operator's shot review (step f) is a file: REVIEW_OK or REVIEW_STOP in ./gates."""
    say("MILESTONE waiting for the shot review file (gates/REVIEW_OK or gates/REVIEW_STOP)")
    while time.time() < deadline:
        if (GATES / "REVIEW_STOP").exists():
            return False
        if (GATES / "REVIEW_OK").exists():
            return True
        time.sleep(2)
    return False


def remove_all():
    if not state["exp"]:
        return None
    wait = max(state["exp"]) + 5 - time.time()
    if wait > 0:
        say("waiting %ds for BOTH tokens to pass exp %s before anything is removed" % (int(wait), iso(max(state["exp"]))))
        time.sleep(wait)
    known = sorted(state["tickets"])
    # safety net: any ticket created_by the filer that this run did not record (a lost response); the denominator is printed
    found = set(known)
    scanned = 0
    for page in ddb.get_paginator("scan").paginate(TableName=TICKETS, ProjectionExpression="ticket_id, created_by"):
        for it in page.get("Items", []):
            scanned += 1
            if it.get("created_by", {}).get("S", "").lower() == FILER:
                found.add(it["ticket_id"]["S"])
    say("removal census: %d tickets scanned; created_by the filer: %s (recorded by the run: %s)" % (scanned, sorted(found), known))
    tickets_deleted_at = None
    for tid in sorted(found):
        if tid in PROTECTED:
            say("REFUSED: protected ticket id %s" % tid)
            continue
        say("DELETE BY KEY: opal-tickets ticket_id=%s (printed before the delete)" % tid)
        try:
            ddb.delete_item(TableName=TICKETS, Key={"ticket_id": {"S": tid}}, ConditionExpression="created_by = :f",
                            ExpressionAttributeValues={":f": {"S": FILER}})
        except ClientError as e:
            say("ticket delete failed: %s" % e.response["Error"]["Code"])
    tickets_deleted_at = iso()
    t_absent = all(item_of(TICKETS, {"ticket_id": {"S": t}}) is None for t in sorted(found))
    say("tickets deleted at %s; ConsistentRead ABSENT=%s" % (tickets_deleted_at, t_absent))
    for ident in state["written"]:
        try:
            ddb.delete_item(TableName=USERS, Key=key_of(ident))
        except Exception as e:  # noqa: BLE001
            say("delete row failed: %s" % type(e).__name__)
    rows_deleted_at = iso()
    r_absent = all(item_of(USERS, key_of(i)) is None for i in state["written"])
    say("identity rows deleted at %s; ConsistentRead ABSENT=%s" % (rows_deleted_at, r_absent))
    return {"tickets_deleted_at": tickets_deleted_at, "tickets_absent_after": t_absent, "rows_deleted_at": rows_deleted_at, "rows_absent_after": r_absent}


def main():
    GATES.mkdir(exist_ok=True)
    stop, out, pw, browser, removed, review = None, {}, None, None, None, False
    try:
        from playwright.sync_api import sync_playwright
        preflight()
        tokens = write_rows_and_mint()
        pw = sync_playwright().start()
        try:
            browser = pw.chromium.launch(channel="msedge", headless=True)
        except Exception:  # noqa: BLE001
            browser = pw.chromium.launch(headless=True)
        journey(browser, tokens, out)
        if state["engine"]:
            raise Stop("a request to the engine submit was seen (and aborted)")
        rec = {"chosen": cli_item(out["pick"]), "other": cli_item(out["other"])}
        RECORD.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
        say("both tickets saved whole (get-item --consistent-read, unchanged) to %s (%d bytes)" % (RECORD.name, RECORD.stat().st_size))
        say("MILESTONE JOURNEY_DONE chosen=%s other=%s" % (out["pick"], out["other"]))
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
        if state["written"]:
            removed = remove_all()
            if stop is None:
                review = wait_review(time.time() + 900)
    TRACE.write_text(json.dumps({"stop": stop, "exp": [iso(x) for x in state["exp"]], "removed": removed, "served_head": state.get("served_head"),
                                 "open_before": state.get("open_before"), "trace": trace}, indent=1, default=str) + "\n", encoding="utf-8")
    if stop is None and removed and removed["tickets_absent_after"] and removed["rows_absent_after"] and review:
        res = {"claim": "measured", "browser_origin": out["origin"], "filer": FILER, "picker": PICKER, "chosen_ticket": out["pick"], "other_ticket": out["other"],
               "board_read": {t: {"type_label": v["type_label"], "age_text": v["age_text"]} for t, v in out["board_read"].items()},
               "chosen_basis": out["basis"], "claim_via": "board", "opened_before_claim": False, "shots": out["shots"], "token_exp": iso(max(state["exp"])),
               "rows_deleted_at": removed["rows_deleted_at"], "tickets_deleted_at": removed["tickets_deleted_at"], "tickets_absent_after": True,
               "rows_absent_after": True, "no_engine_call": not state["engine"], "token_printed": False, "shot_data_reviewed": True,
               "served_head": state["served_head"], "behind_origin_dev_files": state["behind"], "open_tickets_before": state["open_before"],
               "board_rows_extra": "board_read.created_cell and status_text are in the trace events"}
        RESULT.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
        say("result written: %s" % RESULT.name)
        return 0
    say("trace written: %s (stop=%s review_ok=%s)" % (TRACE.name, stop, review))
    return 1


if __name__ == "__main__":
    sys.exit(main())
