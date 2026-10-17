"""TCKT_VNEXT TO-R20-RV2 (PART 4, FWD-11 re-shot) -- ONE read-only shot of the completed meeting ticket (0.7.0_AE_CloudOps~TV2).

Pair : R18_RUN_PAIR.md AMENDMENT 6 (COO blob 7e96f36b11, CTO half b427f42ef2); order AMENDMENT 1 (GO msg 10445). The 5174 server is the CTO's and
already serves the fixed sha (he moved it himself, msg 10454): this script never starts, stops, restarts or checks out anything.
One process holds the signing key and the token; the token is never printed, written or traced: it reaches the page only as the body of a stubbed
/auth/refresh response inside one in-memory context. The read: the board, the Completed tab (navigation only), the filer's own ticket. No ticket write,
no click on a control. One shot, clipped to the ticket's two board rows; the path and byte count are printed and nothing is described. The contrast of the
outcome line is measured from the saved PNG (WCAG relative luminance) and printed as a number.
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
from PIL import Image

REGION = "us-east-1"
ORIGIN = "http://localhost:5174"
HOSTPORT = "localhost:5174"
USERS, TICKETS = "opal-users-v2", "opal-tickets"
FILER = "tckt-r20-filer-20261017@opal.invalid"
NAME = "TCKT R20 synthetic filer"
FIRM = "cottonwood"
TICKET = "TCK-20261017-da2a1987"
FN = "opal-ticket-api"
EXPECT_SHA = "iRxJZYp6IXEtiXDRMT4R/EOwKvsqh5Id5NNgPcpy3RM="
DEV_SHA = "539b1ee70ba1b2a9b0c562a9169d9fcca1b7c18e"
FLOOR_SHA = "8ecad4a5fb"
SERVER_TREE = "C:/dev/smoke-template-5174"
LIFE = 300
KEY_SECRET = "opal/auth/jwt-private-key"

OUT = Path(__file__).resolve().parent
SHOT_DIR_REL = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_reshot/"
TRACE = OUT / "R20_RESHOT_TRACE.json"
RESULT = OUT / "R20_RESHOT_RESULT.json"

ddb = boto3.client("dynamodb", region_name=REGION)
state = {"written": False, "exp": None}
trace = {"claim": "measured", "executor": "0.7.0_AE_CloudOps~TV2", "server_reused": True, "events": [], "blocked_requests": [], "request_census": {}}


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


def git(*args):
    return subprocess.check_output(["git", "-C", SERVER_TREE] + list(args), text=True).strip()


def preflight():
    head = git("rev-parse", "HEAD")
    say("served checkout %s HEAD=%s" % (SERVER_TREE, head))
    if head != DEV_SHA:
        raise Stop("the served checkout HEAD is not the named sha")
    if git("status", "--short"):
        raise Stop("the served checkout has uncommitted changes")
    if subprocess.run(["git", "-C", SERVER_TREE, "merge-base", "--is-ancestor", FLOOR_SHA, "HEAD"]).returncode != 0:
        raise Stop("the served checkout does not carry the window-5 floor %s" % FLOOR_SHA)
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
    return head


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
    """WCAG ratio of the strongest text pixel against the crop's background (its most common colour)."""
    img = Image.open(png_path).convert("RGB")
    x, y, w, h = [int(round(v)) for v in crop]
    x, y = max(0, x), max(0, y)
    reg = img.crop((x, y, min(img.width, x + w), min(img.height, y + h)))
    px = list(reg.getdata())
    bg = Counter(px).most_common(1)[0][0]
    lb = lum(bg)
    ink = max(px, key=lambda p: abs(lum(p) - lb))
    li = lum(ink)
    ratio = (max(lb, li) + 0.05) / (min(lb, li) + 0.05)
    return round(ratio, 2), bg, ink, (x, y, w, h), len(px)


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
        name = "filer_completed__%s__%s__localhost-5174__dev-%s.png" % (FILER.split("@")[0], TICKET, DEV_SHA[:12])
        path = OUT / name
        pg.screenshot(path=str(path), clip=clip, full_page=True)
        size = path.stat().st_size
        say("SHOT filer_completed saved: %s (%d bytes)" % (SHOT_DIR_REL + name, size))
        crop = (bl["x"] + sx - clip["x"], bl["y"] + sy - clip["y"], bl["width"], bl["height"])
        ratio, bg, ink, box, npx = contrast(path, crop)
        say("CONTRAST of the outcome line, from the saved PNG: %.2f:1 (WCAG; strongest text pixel rgb%s against the row background rgb%s; crop %s, %d pixels)"
            % (ratio, ink, bg, box, npx))
        ctx.close()
        browser.close()
    return {"path": SHOT_DIR_REL + name, "bytes": size, "viewer": FILER, "origin": ORIGIN}, origin, {
        "ratio": ratio, "ink_rgb": list(ink), "bg_rgb": list(bg), "crop_px": list(box), "pixels": npx,
        "method": "WCAG 2.x relative luminance; ink = the pixel in the line's box farthest in luminance from the box's most common colour"}


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
    shot = origin = contrast_rec = head = None
    try:
        head = preflight()
        token = write_row_and_mint()
        shot, origin, contrast_rec = read_and_shoot(token)
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
                                 "row_absent_after": absent, "final_ticket": final, "contrast": contrast_rec, "engine_requests_seen": eng,
                                 "trace": trace}, indent=1) + "\n", encoding="utf-8")
    if stop is None and absent and shot:
        RESULT.write_text(json.dumps({
            "claim": "measured", "browser_origin": origin, "dev_sha": head, "filer": FILER, "mt_ticket": TICKET, "shots": {"filer_completed": shot},
            "row_deleted_at": deleted_at, "token_exp": iso(state["exp"]), "row_absent_after": True, "no_engine_call": not eng,
            "token_printed": False, "server_reused": True, "outcome_line_contrast": contrast_rec, "ticket_after": final,
            "blocked_requests_count": len(trace["blocked_requests"])}, indent=1) + "\n", encoding="utf-8")
        say("result written: %s" % RESULT.name)
        return 0
    say("trace written: %s" % TRACE.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
