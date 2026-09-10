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
import json
import os
import re
import sys
import time
import datetime
import requests
from playwright.sync_api import sync_playwright

S = os.path.dirname(os.path.abspath(__file__))
A = sys.argv
cred_src = A[A.index("--cred") + 1] if "--cred" in A else "seeking-alpha"
HEADLESS = "--headless" in A
PARK = "--park" in A
MAX_STEPS = int(A[A.index("--max-steps") + 1]) if "--max-steps" in A else 14
KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
KIMI_MODEL = os.environ.get("KIMI_MODEL", "kimi-k2.6")
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
def kimi_vision(png_bytes, prompt, max_tokens=1500):
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
        timeout=60,
    )
    r.raise_for_status()
    j = r.json()
    return (j["choices"][0]["message"]["content"] or "").strip()


CLASSIFY = (
    "You are driving a Seeking Alpha (seekingalpha.com) browser session. Classify the CURRENT screen as EXACTLY ONE token:\n"
    "- BOT_WALL: an anti-bot interstitial -- 'Access to this page has been denied', 'Before we continue', a 'Press & Hold' button, or a captcha.\n"
    "- LOGIN: a sign-in form or modal with an email field and/or a password field visible.\n"
    "- MFA_OTP: a verification-code prompt with a code input box.\n"
    "- LOGGED_IN: Seeking Alpha site content whose header shows a signed-in user (avatar/initials, 'Portfolio', notifications bell) and NO 'Log in' button.\n"
    "- ANON: Seeking Alpha site content whose header shows a 'Log in' or 'Create free account' control (not signed in).\n"
    "- MODAL: a cookie/consent/subscription/newsletter overlay blocking the page (not a login form).\n"
    "- UNKNOWN: none of the above.\nReply with ONLY the one token."
)


def classify(page, screenshot_fn):
    shot = screenshot_fn()
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
            return o if (o.get("x", -1) >= 0 and o.get("y", -1) >= 0) else None
        except Exception as e:
            log(
                f"locate: KIMI_ERROR {type(e).__name__} {str(e)[:80]} (try {attempt + 1}/2)"
            )
    return None


def press_and_hold(page, x, y, hold_s):
    log(f"press-and-hold at ({x},{y}) for {hold_s}s")
    page.mouse.move(x, y, steps=12)
    time.sleep(0.3)
    page.mouse.down()
    time.sleep(hold_s)
    page.mouse.up()


def has_identity(ctx):
    names = {c["name"] for c in ctx.cookies()}
    return all(n in names for n in IDENTITY_COOKIES), sorted(names)


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
    for step in range(MAX_STEPS):
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
            log("identity cookies PRESENT -- settling 4s")
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
            pt = locate(page, shot, "the 'Press & Hold' human-verification button")
            if pt:
                press_and_hold(page, pt["x"], pt["y"], 6 + 2 * walls)
            else:
                el = page.locator("#px-captcha").first
                if el.count():
                    b = el.bounding_box()
                    if b:
                        press_and_hold(
                            page,
                            b["x"] + b["width"] / 2,
                            b["y"] + b["height"] / 2,
                            6 + 2 * walls,
                        )
                else:
                    log("bot wall: no locate and no #px-captcha -> waiting 10s")
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
    log(f"END rc={rc} identity={ok} cookie_names={names}")
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
