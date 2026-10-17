"""TCKT_VNEXT TO-R20-PROD (PART 5, FWD-11 PROD leg) -- ONE read-only render of the REAL completed meeting ticket on https://opalinvest.dev (0.7.0_AE_CloudOps~TV2).

Pair : R18_RUN_PAIR.md AMENDMENT 7 (COO blob 3acf507198, CTO half bda0290f7f); order AMENDMENT 1 (GO msg 10486).
One process holds the signing key and the token; the token is never printed, written or traced: it reaches the page only as the body of a stubbed
/auth/refresh response inside one in-memory context (the real token path of the earlier runs). The read: the board, the Completed tab (navigation only),
the filer's own ticket; then New Ticket, the select's option list RECORDED, Meeting Request chosen and NOT submitted. A Trade Request option STOPS the leg
(Andrew's hold). No ticket write, no click on a control. Shots are clipped to the ticket's two rows and to the form; the path and byte count are printed and
nothing is described; the outcome line's contrast is measured from the saved PNG (WCAG relative luminance) and printed as a number.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import boto3
import jwt as pyjwt
from PIL import Image

REGION = "us-east-1"
ORIGIN = "https://opalinvest.dev"
HOSTPORT = "opalinvest.dev"
USERS, TICKETS = "opal-users-v2", "opal-tickets"
FILER = "tckt-r20-filer-20261017@opal.invalid"
NAME = "TCKT R20 synthetic filer"
FIRM = "cottonwood"
TICKET = "TCK-20261017-da2a1987"
FN = "opal-ticket-api"
EXPECT_SHA = "iRxJZYp6IXEtiXDRMT4R/EOwKvsqh5Id5NNgPcpy3RM="
PORTAL = "C:/dev/ajb_workspace/portal"
PROMOTE_TIP = "15bc21b304d4b0a150a9cdd0c1b75251f0b8c2a8"
PROMOTE_MARK = "2a64d211"
LIFE = 300
KEY_SECRET = "opal/auth/jwt-private-key"

OUT = Path(__file__).resolve().parent
SHOT_DIR_REL = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_prod/"
TRACE = OUT / "R20_PROD_TRACE.json"
RESULT = OUT / "R20_PROD_RESULT.json"

ddb = boto3.client("dynamodb", region_name=REGION)
state = {"written": False, "exp": None}
trace = {"claim": "measured", "executor": "0.7.0_AE_CloudOps~TV2", "events": [], "blocked_requests": [], "request_census": {}}


class Stop(Exception):
    pass


def iso(t=None):
    return dt.datetime.fromtimestamp(time.time() if t is None else t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def say(msg):
    line = "%s %s" % (iso(), msg)
    print(line, flush=True)
    trace["events"].append(line)


def row_key():
    return {"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}}


def item_of(table, key):
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def pgit(*args):
    return subprocess.check_output(["git", "-C", PORTAL] + list(args), text=True).strip()


def preflight():
    tip = pgit("rev-parse", "origin/PROD")
    anc = subprocess.run(["git", "-C", PORTAL, "merge-base", "--is-ancestor", PROMOTE_MARK, "origin/PROD"]).returncode == 0
    say("git rev-parse origin/PROD = %s ; %s is an ancestor of origin/PROD: %s" % (tip, PROMOTE_MARK, "in" if anc else "NOT IN"))
    if not anc:
        raise Stop("origin/PROD does not carry %s" % PROMOTE_MARK)
    code = urllib.request.urlopen(ORIGIN + "/", timeout=30).status
    say("GET %s/ -> %s" % (ORIGIN, code))
    if code != 200:
        raise Stop("the PROD site does not answer 200")
    cfg = boto3.client("lambda", region_name=REGION).get_function_configuration(FunctionName=FN)
    if cfg["CodeSha256"] != EXPECT_SHA:
        raise Stop("deployed CodeSha256 differs from the R20 release")
    it = item_of(TICKETS, {"ticket_id": {"S": TICKET}})
    m = (it.get("meeting") or {}).get("M") or {}
    say("ticket %s before: status=%s meeting.status=%s" % (TICKET, it["status"]["S"], (m.get("status") or {}).get("S")))
    if it["status"]["S"] != "completed" or (m.get("status") or {}).get("S") != "confirmed":
        raise Stop("the ticket is not completed with a confirmed outcome")
    if item_of(USERS, row_key()) is not None:
        raise Stop("the filer row is already PRESENT")
    say("filer key ConsistentRead ABSENT")
    return ("git rev-parse origin/PROD = %s; git merge-base --is-ancestor %s origin/PROD reads in; origin/PROD tip commit is the merge of "
            "cand/dell2/tckt-outcome-line-contrast-prodfix; GET %s/ answers 200; CI run 39021252990 success and portal-v2.1.234 are DT's report (msg 10482), "
            "not re-read by this seat" % (tip, PROMOTE_MARK, ORIGIN))


def write_row_and_mint():
    item = {"PK": {"S": "USER#" + FILER}, "SK": {"S": "PROFILE"}, "email": {"S": FILER}, "firmId": {"S": "opal-capital"},
            "status": {"S": "active"}, "userType": {"S": "test-filer"}, "name": {"S": NAME}, "allowedFirmIds": {"L": [{"S": FIRM}]}}
    ddb.put_item(TableName=USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
    state["written"] = True
    back = item_of(USERS, row_key())
    if back is None or [x["S"] for x in back["allowedFirmIds"]["L"]] != [FIRM] or "scope_all_firms" in back:
        raise Stop("row not PRESENT with the one-firm list after the put")
    say("row written; ConsistentRead PRESENT allowedFirmIds=[%s]" % FIRM)
    pem = boto3.client("secretsmanager", region_name=REGION).get_secret_value(SecretId=KEY_SECRET)["SecretString"]
    iat = int(time.time())
    claims = {"sub": FILER, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal",
              "role": "user", "userType": "test-filer", "name": NAME, "iat": iat, "exp": iat + LIFE}
    token = pyjwt.encode(claims, pem, algorithm="RS256")
    del pem
    state["exp"] = iat + LIFE
    say("token minted (memory only) iat=%s exp=%s life=%ds" % (iso(iat), iso(iat + LIFE), LIFE))
    return token


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
    li = lum(ink)
    return round((max(lb, li) + 0.05) / (min(lb, li) + 0.05), 2), bg, ink, (x, y, w, h), len(px)


def read_and_shoot(token):
    from playwright.sync_api import sync_playwright
    user = {"email": FILER, "name": NAME, "role": "user", "mustChangePassword": False, "firmId": "opal-capital",
            "userType": "test-filer", "advisorId": None, "firmRole": None, "advisorRole": None}
    auth_body = json.dumps({"accessToken": token, "user": user})
    violations = []

    def norm(p):
        return re.sub(r"TCK-[0-9]{8}-[0-9a-f]{8}", "<T>", p)

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
            trace["blocked_requests"].append("%s %s" % (req.method, norm(p)))
            return route.abort()
        return route.continue_()

    shots, options, contrast_rec = {}, [], None
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(channel="msedge", headless=True)
        except Exception:  # noqa: BLE001
            browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 1000})
        ctx.route("**/*", on_route)
        pg = ctx.new_page()
        pg.goto(ORIGIN + "/ticket-center", wait_until="domcontentloaded", timeout=60000)
        if urlparse(pg.url).path != "/ticket-center":
            raise Stop("the board did not open (landed on %s)" % urlparse(pg.url).path)
        origin = pg.evaluate("window.location.origin")
        say("PAGE ORIGIN window.location.origin = %s" % origin)
        if origin != ORIGIN or violations:
            raise Stop("page origin %r (violations %s) is not exactly %s" % (origin, violations, ORIGIN))
        try:
            pg.get_by_role("button", name="Open", exact=True).first.wait_for(state="visible", timeout=60000)
            pg.locator("thead th", has_text="Ticket").first.wait_for(state="visible", timeout=60000)
        except Exception as e:  # noqa: BLE001
            raise Stop("the board did not finish signing in: %s" % type(e).__name__)
        for loc in (pg.get_by_role("tab", name="Completed", exact=True), pg.get_by_role("button", name="Completed", exact=True),
                    pg.get_by_text("Completed", exact=True)):
            if loc.count():
                loc.first.click()
                break
        else:
            raise Stop("the Completed tab was not found")
        row = pg.locator("tbody tr").filter(has=pg.locator("td", has_text=TICKET)).first
        row.wait_for(state="visible", timeout=60000)
        out = row.locator("xpath=following-sibling::tr[1]")
        line = out.locator('[data-slot="meeting-outcome-line"]')
        line.wait_for(state="visible", timeout=30000)
        row.scroll_into_view_if_needed()
        b1, b2, bl = row.bounding_box(), out.bounding_box(), line.bounding_box()
        sx, sy = pg.evaluate("[window.scrollX, window.scrollY]")
        x0, y0 = min(b1["x"], b2["x"]), min(b1["y"], b2["y"])
        x1, y1 = max(b1["x"] + b1["width"], b2["x"] + b2["width"]), max(b1["y"] + b1["height"], b2["y"] + b2["height"])
        clip = {"x": max(0, x0 + sx - 8), "y": max(0, y0 + sy - 8), "width": x1 - x0 + 16, "height": y1 - y0 + 16}
        name = "prod_filer_completed__%s__%s__opalinvest-dev.png" % (FILER.split("@")[0], TICKET)
        path = OUT / name
        pg.screenshot(path=str(path), clip=clip, full_page=True)
        size = path.stat().st_size
        say("SHOT prod_filer_completed saved: %s (%d bytes)" % (SHOT_DIR_REL + name, size))
        shots["prod_filer_completed"] = {"path": SHOT_DIR_REL + name, "bytes": size, "viewer": FILER, "origin": ORIGIN}
        crop = (bl["x"] + sx - clip["x"], bl["y"] + sy - clip["y"], bl["width"], bl["height"])
        ratio, bg, ink, box, npx = contrast(path, crop)
        say("CONTRAST of the outcome line, from the saved PNG: %.2f:1 (WCAG; strongest text pixel rgb%s against the row background rgb%s; crop %s, %d pixels)"
            % (ratio, ink, bg, box, npx))
        contrast_rec = {"ratio": ratio, "ink_rgb": list(ink), "bg_rgb": list(bg), "crop_px": list(box), "pixels": npx,
                        "method": "WCAG 2.x relative luminance; ink = the pixel in the line's box farthest in luminance from the box's most common colour"}
        # the New Ticket type list, RECORDED before anything is chosen
        pg.get_by_role("button", name="New Ticket").first.click()
        sel = pg.locator("select").filter(has=pg.locator("option", has_text="Meeting Request")).first
        sel.wait_for(state="visible", timeout=30000)
        options = [t.strip() for t in sel.locator("option").all_inner_texts()]
        say("New Ticket type options recorded: %s" % options)
        if any("trade request" in o.lower().replace("_", " ") for o in options):
            raise Stop("a Trade Request option is listed on PROD: a breach of Andrew's hold; nothing further is done")
        sel.select_option(label="Meeting Request")
        form = pg.locator('[data-slot="meeting-request-form"]')
        form.wait_for(state="visible", timeout=30000)
        pg.locator('select[aria-label="Firm"] option[value="%s"]' % FIRM).wait_for(state="attached", timeout=60000)
        form.scroll_into_view_if_needed()
        fb = form.bounding_box()
        heading = pg.get_by_text("New Ticket", exact=True).first
        hb = heading.bounding_box() if heading.count() else None
        sx, sy = pg.evaluate("[window.scrollX, window.scrollY]")
        fx0 = min(fb["x"], hb["x"]) if hb else fb["x"]
        fy0 = min(fb["y"], hb["y"]) if hb else fb["y"]
        fx1 = max(fb["x"] + fb["width"], (hb["x"] + hb["width"]) if hb else 0)
        fy1 = fb["y"] + fb["height"]
        clip2 = {"x": max(0, fx0 + sx - 12), "y": max(0, fy0 + sy - 12), "width": fx1 - fx0 + 24, "height": fy1 - fy0 + 24}
        name2 = "prod_meeting_form__%s__no-ticket__opalinvest-dev.png" % FILER.split("@")[0]
        path2 = OUT / name2
        pg.screenshot(path=str(path2), clip=clip2, full_page=True)
        size2 = path2.stat().st_size
        say("SHOT prod_meeting_form saved: %s (%d bytes); the form was NOT submitted" % (SHOT_DIR_REL + name2, size2))
        shots["prod_meeting_form"] = {"path": SHOT_DIR_REL + name2, "bytes": size2, "viewer": FILER, "origin": ORIGIN}
        ctx.close()
        browser.close()
    return shots, origin, options, contrast_rec


def remove_row():
    wait = (state["exp"] + 5 - time.time()) if state["exp"] else 0
    if wait > 0:
        say("waiting %ds for the token to pass exp %s before the row is removed" % (int(wait), iso(state["exp"])))
        time.sleep(wait)
    ddb.delete_item(TableName=USERS, Key=row_key())
    deleted_at = iso()
    absent = item_of(USERS, row_key()) is None
    say("row deleted at %s; ConsistentRead ABSENT=%s" % (deleted_at, absent))
    return deleted_at, absent


def main():
    stop = None
    shots = origin = contrast_rec = proof = None
    options = []
    try:
        proof = preflight()
        token = write_row_and_mint()
        shots, origin, options, contrast_rec = read_and_shoot(token)
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
            deleted_at, absent = remove_row()
    eng = [k for k in trace["request_census"] if "/api/general/trades" in k]
    it = item_of(TICKETS, {"ticket_id": {"S": TICKET}})
    final = {"status": it["status"]["S"], "meeting_status": (((it.get("meeting") or {}).get("M") or {}).get("status") or {}).get("S")}
    TRACE.write_text(json.dumps({"stop": stop, "exp": iso(state["exp"]) if state["exp"] else None, "row_deleted_at": deleted_at,
                                 "row_absent_after": absent, "final_ticket": final, "type_options": options, "contrast": contrast_rec,
                                 "engine_requests_seen": eng, "trace": trace}, indent=1) + "\n", encoding="utf-8")
    if stop is None and absent and shots and len(shots) == 2:
        RESULT.write_text(json.dumps({
            "claim": "measured", "browser_origin": origin, "promote_proof": proof, "filer": FILER, "mt_ticket": TICKET, "type_options": options,
            "shots": shots, "row_deleted_at": deleted_at, "token_exp": iso(state["exp"]), "row_absent_after": True, "no_engine_call": not eng,
            "token_printed": False, "outcome_line_contrast": contrast_rec, "ticket_after": final,
            "blocked_requests_count": len(trace["blocked_requests"])}, indent=1) + "\n", encoding="utf-8")
        say("result written: %s" % RESULT.name)
        return 0
    say("trace written: %s" % TRACE.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
