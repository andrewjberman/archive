"""Seeking Alpha session harvester -- the bd-49f Kimi authenticator pattern ported to SA.

  our own Google Chrome (headed, native IP -- Bright Data parked pending KYC)
    -> Kimi-VL classifies each screen (BOT_WALL / LOGIN / ANON / LOGGED_IN / MFA_OTP / MODAL / UNKNOWN)
    -> BOT_WALL: Kimi grid-localizes the 'Press & Hold' button, mouse.down + hold + mouse.up
    -> ANON: open the header 'Log in' modal (DOM-first, vision-locate fallback)
    -> LOGIN: fill email/password (DOM-first, vision-locate fallback), submit
    -> success oracle = the site's identity cookies PRESENT (user_id + session_id), never a vision verdict
    -> park the session bundle: storage_state -> scratch; --park writes Secrets Manager seeking-alpha/session

ROE (inherited unchanged from bd_49f_auto_login.js): observe-act-only; NEVER print a credential, OTP or
cookie VALUE; screenshots mask the password field; the only persisted artifact is the session bundle.
Env: SA_SECRETS_DIR (optional dev override). Deps: playwright, requests, boto3; Google Chrome installed.
Usage: python sa_harvest_session.py [--cred seeking-alpha|external-apis] [--headless] [--park] [--max-steps N]
"""

import base64
import io
import json
import os
import re
import sys
import time
import datetime
import requests
from playwright.sync_api import sync_playwright

try:
    from PIL import Image
except ImportError:
    Image = None

# Factored out to press_and_hold_lib.py 2026-09-11 so Bloomberg.com's harvester (a second site
# hitting the same PerimeterX-style widget) can reuse this proven mechanism without duplicating it
# or importing this module (which runs a full SA login as a side effect at import time).
from press_and_hold_lib import press_and_hold as _pahl_press_and_hold
from press_and_hold_lib import press_and_hold_adaptive as _pahl_press_and_hold_adaptive

S = os.path.dirname(os.path.abspath(__file__))
A = sys.argv
cred_src = A[A.index("--cred") + 1] if "--cred" in A else "seeking-alpha"
HEADLESS = "--headless" in A
PARK = "--park" in A
MAX_STEPS = int(A[A.index("--max-steps") + 1]) if "--max-steps" in A else 14
KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
KIMI_MODEL = os.environ.get("KIMI_MODEL", "kimi-k3")  # measured 2026-09-10 (google_oauth_handler.py):
# ~8x faster than kimi-k2.6 on identical vision-grounding tasks (10-12s vs 59-150+s), same accuracy.
# This file was still on k2.6 until now -- almost certainly why a live run hit a 60s ReadTimeout.
KIMI_TIMEOUT_S = 20  # Andrew-direct 2026-09-10: "we need to have 20s timeout" -- was 60s; two
# attempts (classify()/locate() both already retry once) now costs at most ~40s dead air, not 120s.
SESSION_SECRET_ID = "seeking-alpha/session"
IDENTITY_COOKIES = (
    "user_id",
)  # session_id is issued to ANON visitors too (measured run 1); user_id is the discriminator


# --- secrets: Secrets Manager by default; SA_SECRETS_DIR=<dir of secret_*.json files> for a dev box ---
def _secret(name):
    d = os.environ.get("SA_SECRETS_DIR")
    if d:
        return (
            open(
                os.path.join(d, "secret_" + name.replace("/", "_") + ".json"),
                encoding="utf-8",
            )
            .read()
            .strip()
        )
    import boto3

    return (
        boto3.client("secretsmanager", region_name="us-east-1")
        .get_secret_value(SecretId=name)["SecretString"]
        .strip()
    )


kimi_key = _secret("astn/kimi/api-key")
if cred_src == "seeking-alpha":
    c = json.loads(_secret("seeking-alpha/credentials"))
    EMAIL, PASSWORD = c["email"], c["password"]
else:
    c = json.loads(_secret("opal/external-apis"))
    EMAIL, PASSWORD = c["seeking_alpha_email"], c["seeking_alpha_password"]

run_ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def log(m):
    print(f"[sa-harvest {time.strftime('%H:%M:%S')}] {m}", flush=True)


# --- Kimi-VL: screenshot + prompt -> text. Same shape as bd_49f_auto_login.js kimiVision(). ---
def kimi_vision(png_bytes, prompt, max_tokens=1500, timeout=KIMI_TIMEOUT_S):
    body = {
        "model": KIMI_MODEL,
        "temperature": 1,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/png;base64,"
                            + base64.b64encode(png_bytes).decode()
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }
    r = requests.post(
        KIMI_URL,
        json=body,
        headers={
            "Authorization": "Bearer " + kimi_key,
            "Content-Type": "application/json",
        },
        timeout=timeout,
    )
    r.raise_for_status()
    j = r.json()
    return (j["choices"][0]["message"]["content"] or "").strip()


# --- lightweight perceptual-hash cache (Andrew-direct 2026-09-10: "somehow cache the previous
# runs") -- same technique already proven in google_oauth_handler.py's dynamic-nav loop: a cheap
# average-hash fingerprint of the screenshot recognizes "this is the same screen as last poll"
# (tolerant to cursor-blink/anti-aliasing noise an exact byte hash would miss) and skips a
# redundant Kimi round-trip entirely when nothing has visibly changed -- exactly the case of a
# still-loading or unmoving bot wall between polls, which is also where the process is most
# exposed to eating another timeout for no new information.
def _img_hash(png_bytes, hash_size=8):
    if Image is None:
        return None
    try:
        img = Image.open(io.BytesIO(png_bytes)).convert("L").resize((hash_size, hash_size))
        px = list(img.getdata())
        avg = sum(px) / len(px)
        return "".join("1" if p >= avg else "0" for p in px)
    except Exception:
        return None


def _hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


_CLASSIFY_CACHE = {}  # hash -> (state, src)
_LOCATE_CACHE = {}  # (hash, description) -> point-or-None


CLASSIFY = (
    "You are driving a Seeking Alpha (seekingalpha.com) browser session. Classify the CURRENT screen as EXACTLY ONE token:\n"
    "- BOT_WALL: an anti-bot interstitial -- 'Access to this page has been denied', 'Before we continue', a 'Press & Hold' button, or a captcha.\n"
    "- LOGIN: a sign-in form or modal with an email field and/or a password field visible.\n"
    "- MFA_OTP: a verification-code prompt with a code input box.\n"
    "- LOGGED_IN: Seeking Alpha site content whose header shows a signed-in user (avatar/initials, 'Portfolio', notifications bell) and NO 'Log in' button.\n"
    "- ANON: Seeking Alpha site content whose header shows a 'Log in' or 'Create free account' control (not signed in).\n"
    "- MODAL: a cookie/consent/subscription/newsletter overlay blocking the page (not a login form).\n"
    "- UNKNOWN: none of the above.\n"
    "Note: seeing the Press & Hold wall again right after it was just completed is NORMAL (the site "
    "sometimes asks twice) -- classify it as BOT_WALL again, not UNKNOWN.\n"
    "Reply with ONLY the one token."
)


def classify(page, screenshot_fn):
    shot = screenshot_fn()
    h = _img_hash(shot)
    if h is not None:
        ck = next((k for k in _CLASSIFY_CACHE if _hamming(k, h) <= 4), None)
        if ck is not None:
            state, src = _CLASSIFY_CACHE[ck]
            log(f"classify: cache hit (perceptual match) -> {state} -- no Kimi call")
            return state, src + "+cache"
    for attempt in range(2):
        try:
            raw = kimi_vision(shot, CLASSIFY)
            if raw:
                a = raw.upper()
                for s in (
                    "BOT_WALL",
                    "MFA_OTP",
                    "LOGIN",
                    "LOGGED_IN",
                    "ANON",
                    "MODAL",
                    "UNKNOWN",
                ):
                    if s in a:
                        if h is not None and s != "UNKNOWN":
                            _CLASSIFY_CACHE[h] = (s, "kimi")
                        return s, "kimi"
                log(f"classify: KIMI_UNPARSED {raw[:80]!r} (try {attempt + 1}/2)")
            else:
                log(f"classify: KIMI_EMPTY (try {attempt + 1}/2)")
        except Exception as e:
            log(
                f"classify: KIMI_ERROR {type(e).__name__} {str(e)[:100]} (try {attempt + 1}/2)"
            )
    dom = classify_by_dom(page)
    return (dom or "UNKNOWN"), "dom"


def classify_by_dom(page):
    try:
        t = (page.title() or "").lower()
        if "denied" in t or page.locator("#px-captcha").count() > 0:
            return "BOT_WALL"
        if (
            page.locator("input[type='password']:visible").count() > 0
            or page.locator(
                "input[type='email']:visible, input[name='email']:visible"
            ).count()
            > 0
        ):
            return "LOGIN"
        names = {c["name"] for c in page.context.cookies()}
        if all(n in names for n in IDENTITY_COOKIES):
            return "LOGGED_IN"
        if page.get_by_role("button", name=re.compile(r"^log ?in$", re.I)).count() > 0:
            return "ANON"
    except Exception as e:
        log(f"dom-classify error {type(e).__name__}")
    return None


def locate(page, screenshot_fn, description):
    vp = page.viewport_size or {"width": 1366, "height": 860}
    ask = (
        f'The screenshot is {vp["width"]}x{vp["height"]}px. Return ONLY JSON {{"x":<int>,"y":<int>}} = the pixel center to click for: '
        f'"{description}". If absent, return {{"x":-1,"y":-1}}.'
    )
    shot = screenshot_fn()
    h = _img_hash(shot)
    if h is not None:
        ck = next((k for k in _LOCATE_CACHE if k[1] == description and _hamming(k[0], h) <= 4), None)
        if ck is not None:
            log(f"locate({description!r}): cache hit (perceptual match) -- no Kimi call")
            return _LOCATE_CACHE[ck]
    for attempt in range(2):
        try:
            raw = kimi_vision(
                shot, ask, max_tokens=4000
            )  # reasoning model: the FT harvester budgets 4000 for localize
            if not raw:
                log(f"locate: KIMI_EMPTY (try {attempt + 1}/2)")
                continue
            m = re.search(r"\{[^}]*\}", raw)
            if not m:
                log(f"locate: KIMI_UNPARSED {raw[:80]!r} (try {attempt + 1}/2)")
                continue
            o = json.loads(m.group(0))
            result = o if (o.get("x", -1) >= 0 and o.get("y", -1) >= 0) else None
            if h is not None:
                _LOCATE_CACHE[(h, description)] = result
            return result
        except Exception as e:
            log(
                f"locate: KIMI_ERROR {type(e).__name__} {str(e)[:80]} (try {attempt + 1}/2)"
            )
    return None


def press_and_hold(page, x, y, hold_s):
    _pahl_press_and_hold(page, x, y, hold_s, log)


def press_and_hold_adaptive(page, x, y, bbox, max_hold_s=8.0, poll_interval=0.15):
    _pahl_press_and_hold_adaptive(page, x, y, bbox, log, max_hold_s=max_hold_s, poll_interval=poll_interval)


def _locate_botwall(ctx, page):
    """Andrew-direct 2026-09-10: 'keep in mind that box may appear inside the browser, it may be a
    popup outside the main browser'. #px-captcha lookups and screenshots scoped to a single tracked
    `page` object would silently miss a Press & Hold widget rendered on a NEW page/popup (the same
    pattern already observed live with Google's OAuth escalation) -- so this searches EVERY open
    page in the context: DOM first (fast, exact, zero Kimi calls), vision second only if DOM finds
    the widget on none of them. Returns (page_it_is_on, bbox_or_None, point_or_None)."""
    pages = [page] + [p for p in ctx.pages if p is not page]
    for p in pages:
        try:
            el = p.locator("#px-captcha").first
            if el.count():
                b = el.bounding_box()
                if b:
                    return p, b, None
        except Exception:
            continue
    for p in pages:
        try:
            pt = locate(p, lambda p=p: p.screenshot(timeout=15000), "the 'Press & Hold' human-verification button")
        except Exception:
            pt = None
        if pt:
            return p, None, pt
    return page, None, None


def has_identity(ctx):
    names = {c["name"] for c in ctx.cookies()}
    return all(n in names for n in IDENTITY_COOKIES), sorted(names)


# --- network-level auth oracle (Andrew-direct 2026-09-10: "it is not done until there is some
# network change and a jwt served or something") -- a cookie-jar read after the fact (has_identity,
# above) is a SNAPSHOT; it cannot tell you the identity cookie was actually SERVED BY THE NETWORK
# during this run vs. set by some other path. This listens on every response as it happens and
# records the EVENT of an auth artifact being minted: a Set-Cookie for one of the site's known
# identity cookies (its "identity four": user_id, session_id, user_remember_token, user_cookie_key
# -- see sa_rest_fetch.py), or a JWT-shaped bearer token appearing in a request's Authorization
# header or an xhr/fetch JSON response body. Never records a VALUE, only which artifact arrived and
# where (kind/name/url/length) -- same ROE as every credential-adjacent log line in this estate.
TRACKED_COOKIE_NAMES = ("user_id", "session_id", "user_remember_token", "user_cookie_key")
JWT_SHAPE_RE = re.compile(r"[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")
NETWORK_AUTH_EVENTS = []


def _record_network_auth_event(kind, url, name, length=None):
    NETWORK_AUTH_EVENTS.append(
        {"ts": time.time(), "url": url[:120], "kind": kind, "name": name, "length": length}
    )
    log(
        f"NETWORK AUTH EVENT: kind={kind} name={name!r} url={url[:80]!r}"
        + (f" len={length}" if length else "")
    )


def _on_response(resp):
    try:
        headers = resp.headers
        # BUG FIXED 2026-09-10 (found chasing a real live run that showed identity cookies present
        # with zero corroborating network events): resp.headers is a dict that COLLAPSES duplicate
        # headers, and Set-Cookie is exactly the header that legitimately repeats -- one response
        # commonly sets several cookies (PerimeterX/analytics ones alongside the identity ones) in
        # separate Set-Cookie headers. header_values() preserves every one of them individually;
        # .headers.get("set-cookie") could join or drop entries and silently miss the real one.
        try:
            set_cookie_values = resp.header_values("set-cookie")
        except Exception:
            set_cookie_values = []
        for sc in set_cookie_values:
            for name in TRACKED_COOKIE_NAMES:
                if re.match(rf"{re.escape(name)}=", sc.strip()):
                    _record_network_auth_event("set-cookie", resp.url, name)
        try:
            auth_hdr = resp.request.headers.get("authorization", "")
        except Exception:
            auth_hdr = ""
        if auth_hdr and JWT_SHAPE_RE.search(auth_hdr):
            _record_network_auth_event("authorization-header", resp.url, "authorization", len(auth_hdr))
        rtype = getattr(resp.request, "resource_type", "")
        ctype = headers.get("content-type", "")
        if rtype in ("xhr", "fetch") and "json" in ctype.lower():
            try:
                body = resp.text()
            except Exception:
                body = ""
            if body and len(body) < 20000:
                for field in ("token", "jwt", "access_token", "id_token", "auth_token"):
                    m = re.search(rf'"{field}"\s*:\s*"([^"]{{20,}})"', body, re.I)
                    if m and JWT_SHAPE_RE.search(m.group(1)):
                        _record_network_auth_event("json-body-field", resp.url, field, len(m.group(1)))
    except Exception:
        pass  # best-effort observer; must never crash the harvest it is watching


def has_network_auth_evidence():
    return len(NETWORK_AUTH_EVENTS) > 0, list(NETWORK_AUTH_EVENTS)


with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="chrome",
        headless=HEADLESS,
        args=["--disable-blink-features=AutomationControlled", "--no-first-run"],
    )
    ctx = browser.new_context(
        viewport={"width": 1366, "height": 860},
        locale="en-US",
        timezone_id="America/New_York",
    )
    ctx.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
    )
    page = ctx.new_page()
    # attach the network-auth listener to EVERY page that ever opens, not just this first one --
    # a popup is exactly where an auth artifact might actually get served (see BOT_WALL below).
    ctx.on("page", lambda p: p.on("response", _on_response))
    page.on("response", _on_response)
    def shot():
        return page.screenshot(
            mask=[page.locator("input[type='password']")], timeout=15000
        )
    log(
        f"cred={cred_src} email={EMAIL} headless={HEADLESS} park={PARK} egress=native-IP kimi={KIMI_MODEL}"
    )
    page.goto(
        "https://seekingalpha.com/symbol/RTX",
        timeout=90000,
        wait_until="domcontentloaded",
    )
    time.sleep(4)

    rc = 1
    walls = 0
    logins = 0
    modal_opens = 0
    consecutive_unknown = 0
    known_pages = list(ctx.pages)
    for step in range(MAX_STEPS):
        # Andrew-direct 2026-09-10: "if there is an additional popup that is an obvious clue that
        # the new appearing window is the one to use ... that is going to be the next challenge
        # regardless whether its a press and hold, a gmail sign in, etc" -- a NEW page appearing is
        # itself the deterministic signal for where to act next, independent of what the challenge
        # turns out to be. Checked every step (not just inside BOT_WALL), general to any state.
        # `page` is reassigned here rather than renamed everywhere below: every branch in this loop
        # (and shot(), a closure over this same name) already reads the bare `page` variable, so
        # rebinding it once at the top of the iteration is sufficient -- Python resolves free
        # variables at call time, not definition time, in this flat (non-nested-function) scope.
        current_pages = list(ctx.pages)
        new_pages = [p for p in current_pages if p not in known_pages]
        if new_pages:
            page = new_pages[-1]
            log(f"NEW PAGE/POPUP detected ({len(current_pages)} open total) -- switching active page to it: {page.url[:70]!r}")
        known_pages = current_pages
        state, src = classify(page, shot)
        ok, names = has_identity(ctx)
        log(f"step {step}: state={state} ({src}) url={page.url[:70]} identity={ok}")
        try:
            page.screenshot(
                path=os.path.join(S, f"harvest_{run_ts}_step{step}_{state}.png"),
                mask=[page.locator("input[type='password']")],
                timeout=15000,
            )
        except Exception:
            pass
        if ok:
            net_ok, events = has_network_auth_evidence()
            if not net_ok:
                # Andrew-direct 2026-09-10: "not done until there is some network change and a
                # jwt served or something" -- a cookie-jar snapshot alone is not that evidence.
                # Give the network one more beat (a Set-Cookie on a trailing redirect can lag the
                # jar read by a few hundred ms) before accepting jar-alone.
                log("identity cookies PRESENT but no network auth event observed yet -- waiting 3s for one")
                time.sleep(3)
                net_ok, events = has_network_auth_evidence()
            if net_ok:
                log(f"identity cookies PRESENT, corroborated by {len(events)} network auth event(s) -- settling 4s")
            else:
                log("identity cookies PRESENT with NO corroborating network auth event after the extra wait "
                    "-- accepting the cookie-jar oracle alone, but this is the WEAKER of the two and is "
                    "flagged as such in the parked bundle")
            time.sleep(4)
            rc = 0
            break
        if state == "LOGGED_IN" and not ok:
            log(
                "vision says LOGGED_IN but identity cookies absent -- not accepting (oracle is the cookie)"
            )
            time.sleep(3)
            continue
        if state == "BOT_WALL":
            walls += 1
            if walls > 4:
                log("bot wall persists after 4 attempts -> giving up")
                break
            # Andrew-direct 2026-09-10: "that box may appear inside the browser, it may be a popup
            # outside the main browser" / "so you can't key off one fixed point" -- re-discover the
            # widget FRESH on every occurrence, searching every open page, never assuming it stays
            # on the page (or at the point) it was found at last time.
            if len(ctx.pages) > 1:
                log(f"{len(ctx.pages)} pages open during BOT_WALL -- searching all of them for the widget")
            wall_page, bbox, pt = _locate_botwall(ctx, page)
            if wall_page is not page:
                log(f"Press & Hold widget found on a DIFFERENT page than the tracked one: {wall_page.url[:70]!r}")
            if bbox:
                cx, cy = bbox["x"] + bbox["width"] / 2, bbox["y"] + bbox["height"] / 2
                press_and_hold_adaptive(wall_page, cx, cy, bbox)
            elif pt:
                # no exact element box from vision -- synthesize a generous one around the point
                synth_bbox = {"x": pt["x"] - 60, "y": pt["y"] - 60, "width": 120, "height": 120}
                press_and_hold_adaptive(wall_page, pt["x"], pt["y"], synth_bbox)
            else:
                log("bot wall: no #px-captcha and no vision locate on any open page -> waiting 10s")
                time.sleep(10)
            time.sleep(6)
            continue
        if state == "ANON":
            modal_opens += 1
            if modal_opens > 3:
                log("login modal would not open after 3 tries")
                break
            btn = page.locator(
                "[data-test-id='header-button-sign-in']"
            ).first  # measured: BUTTON 'LOG IN' at (1236,21)
            if not btn.count():
                btn = page.locator(
                    "button:has-text('Log in'), button:has-text('LOG IN')"
                ).first
            if btn.count():
                btn.click(timeout=10000)
                log("clicked header sign-in button")
            else:
                pt = locate(
                    page, shot, "the 'LOG IN' button in the page header (top right)"
                )
                if pt:
                    page.mouse.click(pt["x"], pt["y"])
                    log("clicked header sign-in via vision")
            time.sleep(4)
            continue
        if state == "LOGIN":
            logins += 1
            if logins > 3:
                log(
                    "login submitted 3 times without identity cookie -> giving up (wrong password or MFA)"
                )
                break
            pw = page.locator("input[type='password']:visible").first
            if pw.count():
                em = pw.locator(
                    "xpath=preceding::input[1]"
                )  # the modal's Email box is the nearest preceding input; the page banner's #email sits behind the modal
                em.click()
                em.fill("")
                em.type(EMAIL, delay=35)
                time.sleep(0.6)
                pw.click()
                pw.fill("")
                pw.type(PASSWORD, delay=35)
                time.sleep(0.6)
                sub = page.get_by_role(
                    "button", name=re.compile(r"^sign in$", re.I)
                ).first
                if sub.count():
                    sub.click(timeout=8000)
                    log("clicked 'Sign in'")
                else:
                    pw.press("Enter")
                    log("pressed Enter in password field")
            else:
                pt = locate(
                    page, shot, "the Email input field of the 'Member Sign In' form"
                )
                if pt:
                    page.mouse.click(pt["x"], pt["y"])
                    page.keyboard.type(EMAIL, delay=35)
                pt = locate(
                    page, shot, "the Password input field of the 'Member Sign In' form"
                )
                if pt:
                    page.mouse.click(pt["x"], pt["y"])
                    page.keyboard.type(PASSWORD, delay=35)
                    page.keyboard.press("Enter")
                else:
                    log("LOGIN: no password field found (DOM or vision)")
            log("login submitted; waiting 8s")
            time.sleep(8)
            try:  # ROE-safe: surface the form's ERROR text only (never a field value)
                errs = page.locator(
                    "form:has(input[type='password']) [role='alert'], form:has(input[type='password']) [class*='error' i], [data-test-id*='error' i]"
                ).all_inner_texts()
                errs = [e.strip() for e in errs if e.strip()]
                if errs:
                    log(f"form error text: {errs[:3]}")
            except Exception:
                pass
            continue
        if state == "MFA_OTP":
            log(
                "MFA/OTP screen -- no OTP adapter wired for SA yet (bd-49f uses the m365 gateway); stopping"
            )
            break
        if state == "MODAL":
            pt = locate(
                page,
                shot,
                "the close (X) button or 'Accept' button of the overlay dialog",
            )
            if pt:
                page.mouse.click(pt["x"], pt["y"])
            else:
                page.keyboard.press("Escape")
            time.sleep(2)
            continue
        consecutive_unknown += 1
        if consecutive_unknown >= 3:
            log("3 consecutive UNKNOWN -> vision may be down; stopping")
            break
        time.sleep(4)

    ok, names = has_identity(ctx)
    net_ok, net_events = has_network_auth_evidence()
    log(f"END rc={rc} identity={ok} network_auth_corroborated={net_ok} "
        f"network_auth_event_count={len(net_events)} cookie_names={names}")
    bundle_path = os.path.join(S, f"sa_session_{run_ts}.json")
    state = ctx.storage_state()
    if ok:
        cookies = state["cookies"]
        bundle = {
            "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
            "email": EMAIL,
            "user_agent": page.evaluate("navigator.userAgent"),
            "cookie_names": sorted({c["name"] for c in cookies}),
            "all_cookies": cookies,
            "network_auth_corroborated": net_ok,
            "network_auth_events": [
                {k: v for k, v in e.items() if k != "ts"} for e in net_events
            ],
        }
        json.dump(bundle, open(bundle_path, "w"), indent=1)
        log(f"session bundle -> {bundle_path} ({len(cookies)} cookies)")
        if PARK:
            import boto3

            sm = boto3.client("secretsmanager", region_name="us-east-1")
            try:
                sm.describe_secret(SecretId=SESSION_SECRET_ID)
                exists = True
            except sm.exceptions.ResourceNotFoundException:
                exists = False
            try:
                if exists:
                    resp = sm.put_secret_value(
                        SecretId=SESSION_SECRET_ID, SecretString=json.dumps(bundle)
                    )
                else:
                    resp = sm.create_secret(
                        Name=SESSION_SECRET_ID,
                        Description="Seeking Alpha parked session bundle (harvested by the Kimi authenticator pattern). Consumers ride this; never log in inline.",
                        SecretString=json.dumps(bundle),
                        Tags=[
                            {"Key": "service", "Value": "seeking-alpha"},
                            {"Key": "kind", "Value": "site-session"},
                        ],
                    )
                log(
                    f"park -> {SESSION_SECRET_ID}: {'updated' if exists else 'CREATED'} VersionId={resp.get('VersionId')}"
                )
            except Exception as e:
                log(f"park FAILED {type(e).__name__}: {str(e)[:200]}")
                rc = 1
    browser.close()
sys.exit(rc)
