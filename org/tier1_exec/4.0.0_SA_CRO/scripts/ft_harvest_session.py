#!/usr/bin/env python3
"""Financial Times session harvester -- the standing reference for AMGT_RESAPP, mirroring
sa_harvest_session.py's shape and ROE exactly.

  our own Google Chrome (headed by default, real Chrome channel, anti-automation flag set)
    -> dismiss the Sourcepoint cookie-consent iframe (MEASURED: it transparently covers the
       whole login form; a normal click on 'Next' times out waiting for the iframe to stop
       intercepting it -- this is not a visual overlay, elementFromPoint on the button's own
       center resolves to the iframe)
    -> email -> Next -> password -> Sign in
    -> hCaptcha, IF it appears: Kimi-VL vision framework (grid tile-select) -- UNPROVEN against
       a live challenge, same honest caveat the estate's existing harvest_ft_session.js carries
    -> navigate to www.ft.com to let the session finish establishing
    -> success oracle = FTSession or FTSession_s cookie PRESENT, never a vision verdict
    -> park the session bundle: storage_state -> scratch; --park writes Secrets Manager
       astn/ft/session

TWO BUGS MEASURED LIVE 2026-09-10 AND FIXED HERE (both also fixed in the estate's own
tools/astn_wsjft/scripts/harvest_ft_session.js, a separate, smaller commit under ASTN_WSJFT):
  1. The Sourcepoint consent iframe (id^=sp_message_iframe) intercepts every click on the login
     form until dismissed. The original harvester never dismissed it -- every run hung on the
     'Next' click for the full 30s Playwright timeout. IT CAN RE-INJECT ITSELF after the DOM
     transitions to a later step (measured: it reappeared at the password step and intercepted
     'Sign in' too, same message_id, a fresh iframe) -- so dismissal here runs defensively before
     EVERY click, not once at page load.
  2. `chromium.launch(channel='chrome')` with no anti-automation flag leaves
     navigator.webdriver == true. Two side-by-side runs that added
     --disable-blink-features=AutomationControlled went through hCaptcha-free; two runs of the
     original (unpatched) launch config both got challenged. Fixed here by launching with the
     flag always set.

ROE (inherited unchanged from sa_harvest_session.py / bd_49f_auto_login.js): observe-act-only;
NEVER print a credential, OTP or cookie VALUE; screenshots (when taken) mask the password field;
the only persisted artifact is the session bundle.

Env: SA_SECRETS_DIR (optional dev override, same variable name as sa_harvest_session.py so one
override covers both harvesters in a dev session -- read secret_*.json files from that dir instead
of Secrets Manager). Deps: playwright, boto3; Google Chrome installed (channel='chrome').
Usage: python ft_harvest_session.py [--headless] [--park] [--max-steps N]
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
HEADLESS = "--headless" in A
PARK = "--park" in A
MAX_HCAPTCHA_ROUNDS = int(A[A.index("--max-steps") + 1]) if "--max-steps" in A else 3
KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
KIMI_MODEL = os.environ.get("KIMI_MODEL", "kimi-k2.6")
SESSION_SECRET_ID = "astn/ft/session"
IDENTITY_COOKIES = ("FTSession", "FTSession_s")
DROP_COOKIES = {"__cf_bm", "_cfuvid"}  # IP-bound to the harvest machine; fetch_ft.js drops these too
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"


def _secret(name):
    d = os.environ.get("SA_SECRETS_DIR")
    if d:
        with open(os.path.join(d, "secret_" + name.replace("/", "_") + ".json"), encoding="utf-8") as fh:
            return fh.read().strip()
    import boto3
    return boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=name)["SecretString"]


run_ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def log(m):
    print(f"[ft-harvest {time.strftime('%H:%M:%S')}] {m}", flush=True)


def kimi_vision(png_bytes, prompt, max_tokens=4000):
    """Same call shape as bd_49f_auto_login.js / harvest_ft_session.js kimiVision(). kimi-k2.6 is a
    reasoning model -- a low max_tokens returns EMPTY because hidden reasoning tokens eat the
    budget (measured on the Seeking Alpha harvester); 4000 is the FT harvester's own budget for
    the harder real-photo hCaptcha grid, carried over unchanged."""
    body = {
        "model": KIMI_MODEL, "temperature": 1, "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(png_bytes).decode()}},
            {"type": "text", "text": prompt},
        ]}],
    }
    kimi_key = _secret("astn/kimi/api-key").strip()
    r = requests.post(KIMI_URL, json=body, headers={"Authorization": "Bearer " + kimi_key, "Content-Type": "application/json"}, timeout=90)
    r.raise_for_status()
    return (r.json()["choices"][0]["message"]["content"] or "").strip()


def dismiss_consent(page):
    """FIX 1: the Sourcepoint consent iframe covers the whole form until dismissed."""
    try:
        fl = page.frame_locator('iframe[id^="sp_message_iframe"]')
        for sel in ("button:has-text('Accept')", "button:has-text('AGREE')", "button:has-text('I Accept')"):
            btn = fl.locator(sel).first
            if btn.count():
                btn.click(timeout=5000)
                log(f"consent banner dismissed via {sel!r}")
                return True
    except Exception as e:
        log(f"consent dismissal skipped/absent: {type(e).__name__}")
    return False


def has_identity(ctx):
    names = {c["name"] for c in ctx.cookies()}
    present = [n for n in IDENTITY_COOKIES if n in names]
    return bool(present), sorted(names), present


def solve_hcaptcha_if_present(page):
    """Framework, ported from harvest_ft_session.js -- UNPROVEN against a live tile-grid challenge
    (the estate's own honest status). Locates the challenge iframe, asks Kimi vision which tiles
    match the instruction, clicks them. Returns True once the challenge iframe is gone (solved OR
    it was never a visual challenge to begin with -- hCaptcha's invisible mode passes silently)."""
    frame = next((f for f in page.frames if "hcaptcha.com" in f.url and re.search(r"challenge|frame", f.url)), None)
    if not frame:
        return False
    log("hCaptcha challenge frame detected -> Kimi vision solve (framework; unproven vs a live grid)")
    for rnd in range(MAX_HCAPTCHA_ROUNDS):
        try:
            shot = page.screenshot()
        except Exception:
            break
        ask = ('This screenshot contains an hCaptcha image challenge with a grid of image tiles and an '
               'instruction line ("Please click each image containing a ..."). Read the instruction, then '
               'return ONLY a JSON list of the 1-based tile numbers (reading left-to-right, top-to-bottom) '
               'that match. Example: [1,4,6]')
        try:
            raw = kimi_vision(shot, ask)
            m = re.search(r"\[[^\]]*\]", raw)
            tiles = json.loads(m.group(0)) if m else []
        except Exception as e:
            log(f"kimi tile-select parse failed: {type(e).__name__} {str(e)[:80]}")
            tiles = []
        if not tiles:
            break
        cells = frame.locator(".task-image, .challenge-example, [class*='task']")
        n = cells.count()
        for t in tiles:
            if 1 <= t <= n:
                try:
                    cells.nth(t - 1).click(timeout=3000)
                except Exception:
                    pass
        verify = frame.locator(".button-submit, [class*='submit']").first
        if verify.count():
            try:
                verify.click(timeout=3000)
            except Exception:
                pass
            time.sleep(2.5)
        frame = next((f for f in page.frames if "hcaptcha" in f.url and "challenge" in f.url), None)
        if not frame:
            return True
    return False


def harvest():
    with sync_playwright() as p:
        creds = json.loads(_secret("astn/ft/credentials"))
        email, password = creds["username"], creds["password"]
        log(f"email={email} headless={HEADLESS} park={PARK} egress=native-IP kimi={KIMI_MODEL}")

        browser = p.chromium.launch(
            channel="chrome", headless=HEADLESS,
            # FIX 2: without this, navigator.webdriver stays true -- a strong bot signal that
            # measurably raised the hCaptcha challenge rate on every unpatched run.
            args=["--disable-blink-features=AutomationControlled", "--no-first-run"],
        )
        ctx = browser.new_context(viewport={"width": 1366, "height": 900}, user_agent=UA)
        ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        page = ctx.new_page()

        page.goto("https://accounts.ft.com/login", wait_until="domcontentloaded", timeout=60000)
        time.sleep(2.5)
        dismiss_consent(page)
        time.sleep(0.8)

        page.locator("#enter-email").fill(email)
        time.sleep(0.4)
        # MEASURED: the Sourcepoint consent widget can re-inject itself after the DOM
        # transitions to the next step (same message_id, a fresh iframe) -- dismiss defensively
        # before EVERY click, not just once at page load. A one-shot dismissal at the top was
        # what let the FIRST attempt at this script hang on the password step's own 'Sign in'
        # button, intercepted the identical way the 'Next' button was.
        dismiss_consent(page)
        page.locator("#enter-email-next").click(timeout=15000)
        log("email submitted")
        time.sleep(2.5)

        dismiss_consent(page)
        page.locator("#enter-password").fill(password)
        time.sleep(0.4)
        dismiss_consent(page)
        page.locator("#sign-in-button").click(timeout=15000)
        log("credentials submitted; waiting for challenge or redirect")
        time.sleep(3.5)

        solve_hcaptcha_if_present(page)
        time.sleep(1.5)

        # Let the session finish establishing (mirrors the estate's own harvester and the bd-49f
        # "let the dashboard land" lesson): navigating directly to www.ft.com also skips past any
        # passkey-setup interstitial FT shows post-login without needing to handle it explicitly.
        page.goto("https://www.ft.com", wait_until="domcontentloaded", timeout=60000)
        time.sleep(2.5)

        ok, names, present = has_identity(ctx)
        log(f"END identity={ok} (cookies present: {present}) total_cookies={len(names)}")

        rc = 1
        if ok:
            cookies = ctx.cookies()
            bundle = {c["name"]: c["value"] for c in cookies if c["name"] not in DROP_COOKIES}
            bundle_path = os.path.join(S, f"ft_session_{run_ts}.json") if not os.environ.get("SA_SECRETS_DIR") else os.path.join(os.environ["SA_SECRETS_DIR"], f"ft_session_{run_ts}.json")
            with open(bundle_path, "w", encoding="utf-8") as fh:
                json.dump(bundle, fh, indent=1)
            log(f"session bundle -> {bundle_path} ({len(bundle)} cookies)")
            rc = 0
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
                        resp = sm.put_secret_value(SecretId=SESSION_SECRET_ID, SecretString=json.dumps(bundle))
                    else:
                        resp = sm.create_secret(
                            Name=SESSION_SECRET_ID,
                            Description="FT authenticated session cookie bundle for ASTN_WSJFT / AMGT_RESAPP. Refreshed by ft_harvest_session.py.",
                            SecretString=json.dumps(bundle),
                        )
                    log(f"park -> {SESSION_SECRET_ID}: {'updated' if exists else 'CREATED'} VersionId={resp.get('VersionId')}")
                except Exception as e:
                    log(f"park FAILED {type(e).__name__}: {str(e)[:200]}")
                    rc = 1
        browser.close()
    return rc


if __name__ == "__main__":
    sys.exit(harvest())
