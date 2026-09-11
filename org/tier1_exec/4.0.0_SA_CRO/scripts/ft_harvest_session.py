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

import nopecha
import requests
from playwright.sync_api import sync_playwright

S = os.path.dirname(os.path.abspath(__file__))
A = sys.argv
HEADLESS = "--headless" in A
PARK = "--park" in A
MAX_HCAPTCHA_ROUNDS = int(A[A.index("--max-steps") + 1]) if "--max-steps" in A else 3
KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
KIMI_MODEL = os.environ.get("KIMI_MODEL", "kimi-k3")  # ported from sa_harvest_session.py 2026-09-11:
# measured ~8x faster than kimi-k2.6 on identical vision-grounding tasks, same accuracy.
KIMI_TIMEOUT_S = 20  # ported same day, same reason: was 90s here, no live run had ever exercised it
SESSION_SECRET_ID = "astn/ft/session"
IDENTITY_COOKIES = ("FTSession", "FTSession_s")
DROP_COOKIES = {"__cf_bm", "_cfuvid"}  # IP-bound to the harvest machine; fetch_ft.js drops these too
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

# --- network-level auth oracle, ported from sa_harvest_session.py 2026-09-11 (Andrew-direct
# 2026-09-10: "it is not done until there is some network change and a jwt served or something").
# A cookie-jar read after the fact cannot show the identity cookie was actually SERVED BY THE
# NETWORK during this run. Response.header_values() (not the duplicate-collapsing .headers dict --
# the exact bug found and fixed on the SA path) preserves every Set-Cookie header individually.
JWT_SHAPE_RE = re.compile(r"[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")
NETWORK_AUTH_EVENTS = []


def _record_network_auth_event(kind, url, name, length=None):
    NETWORK_AUTH_EVENTS.append({"ts": time.time(), "url": url[:120], "kind": kind, "name": name, "length": length})
    log(f"NETWORK AUTH EVENT: kind={kind} name={name!r} url={url[:80]!r}" + (f" len={length}" if length else ""))


def _on_response(resp):
    try:
        for sc in resp.header_values("set-cookie"):
            for name in IDENTITY_COOKIES:
                if re.match(rf"{re.escape(name)}=", sc.strip()):
                    _record_network_auth_event("set-cookie", resp.url, name)
        try:
            auth_hdr = resp.request.headers.get("authorization", "")
        except Exception:
            auth_hdr = ""
        if auth_hdr and JWT_SHAPE_RE.search(auth_hdr):
            _record_network_auth_event("authorization-header", resp.url, "authorization", len(auth_hdr))
    except Exception:
        pass  # best-effort observer; must never crash the harvest it is watching


def has_network_auth_evidence():
    return len(NETWORK_AUTH_EVENTS) > 0, list(NETWORK_AUTH_EVENTS)


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


def kimi_vision(png_bytes, prompt, max_tokens=4000, timeout=KIMI_TIMEOUT_S):
    """Same call shape as bd_49f_auto_login.js / harvest_ft_session.js kimiVision(). kimi-k2.6 is a
    reasoning model -- a low max_tokens returns EMPTY because hidden reasoning tokens eat the
    budget (measured on the Seeking Alpha harvester); 4000 is the FT harvester's own budget for
    the harder real-photo hCaptcha grid, carried over unchanged. `timeout` is overridable per call
    (measured live 2026-09-11: the blanket 20s ported from SA's simpler classify/locate calls timed
    out on this specific real-photo grid task -- a harder task than anything SA's harvester asks of
    a single call, so it gets its own longer budget at the call site, not a blanket bump)."""
    body = {
        "model": KIMI_MODEL, "temperature": 1, "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(png_bytes).decode()}},
            {"type": "text", "text": prompt},
        ]}],
    }
    kimi_key = _secret("astn/kimi/api-key").strip()
    r = requests.post(KIMI_URL, json=body, headers={"Authorization": "Bearer " + kimi_key, "Content-Type": "application/json"}, timeout=timeout)
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


def _extract_hcaptcha_sitekey(page):
    """hCaptcha's standard site integration renders its container with a `data-sitekey` attribute
    on the PARENT page's own DOM -- the canonical, documented place every integrator puts it, and
    far more reliable than parsing the challenge iframe's own asset-versioned URL for a query
    param that isn't guaranteed to be there in a simple regex-matchable form. Frame-URL parsing is
    kept only as a fallback."""
    try:
        el = page.locator("[data-sitekey]").first
        if el.count():
            sk = el.get_attribute("data-sitekey")
            if sk:
                return sk
    except Exception:
        pass
    for f in page.frames:
        if "hcaptcha.com" in f.url:
            m = re.search(r"[?&]sitekey=([0-9a-fA-F-]+)", f.url)
            if m:
                return m.group(1)
    return None


def solve_hcaptcha_if_present(page):
    """NopeCHA Token API (Andrew-direct 2026-09-11: 'i thought you could just operate it via API
    solely' -- correct, and simpler/more verifiable than the browser-extension route, which never
    demonstrably activated -- confirmed empty ctx.service_workers/background_pages against a live
    challenge, and no visible solving behavior, despite the extension showing ENABLED in
    chrome://extensions). NopeCHA solves the challenge entirely on ITS OWN backend given just the
    sitekey and page URL -- no browser interaction needed there, no tile screenshots, no multi-
    object vision classification (the exact task MEASURED too slow for Kimi: a simple vision call
    returns in ~7s, but a multi-object grid-classification-shaped call timed out at 60s without
    completing). The returned token is injected the same way every third-party captcha-solving
    integration does it: set the `h-captcha-response` textarea's value, then let the page's own
    submit flow proceed. Returns True once the challenge frame is gone."""
    frame = next((f for f in page.frames if "hcaptcha.com" in f.url and re.search(r"challenge|frame", f.url)), None)
    if not frame:
        return False
    sitekey = _extract_hcaptcha_sitekey(page)
    if not sitekey:
        log("hCaptcha challenge detected but no sitekey could be extracted -- cannot use the Token API")
        return False
    log(f"hCaptcha challenge detected, sitekey found -- solving via NopeCHA Token API (url={page.url[:70]!r})")
    # BUG FOUND AND FIXED 2026-09-11 (traced after the balance check silently returned the Free
    # plan despite a real paid Starter key): the installed nopecha>=2.0 package's `nopecha.api_key
    # = ...` pattern shown in NopeCHA's OWN official example scripts is a DEAD ASSIGNMENT --
    # `nopecha/__init__.py` uses a module-level __getattr__ (PEP 562) that intercepts READS of
    # `Token`/`Balance`/`api_key` and lazily redirects to a deprecated `_v1_compat` shim, but
    # __getattr__ never fires on a WRITE, so `nopecha.api_key = x` just creates an orphaned
    # attribute on the wrong object. The shim actually reads its key ONCE at first access via
    # `os.getenv("NOPECHA_API_KEY", "")` -- every prior call in this investigation silently ran as
    # an unauthenticated, IP-rate-limited anonymous request, never touching the paid account at
    # all (verified: setting this env var instead returns the real Starter/2000-credit plan).
    os.environ["NOPECHA_API_KEY"] = _secret("nopecha/api-key").strip()
    try:
        raw = nopecha.Token.solve(type="hcaptcha", sitekey=sitekey, url=page.url)
    except Exception as e:
        log(f"NopeCHA token solve failed: {type(e).__name__} {str(e)[:150]}")
        return False
    # BUG FOUND AND FIXED 2026-09-11 (measured live: "token length=1" -- not a real hCaptcha token,
    # which are long strings): Token.solve() returns the RAW response dict {"data": "<token>"},
    # confirmed by reading the installed library's own source (_v1_compat.UrllibAPIClient
    # ._request_get returns job_request.body verbatim) -- not the bare token string the official
    # example script's `print(token)` line implies. len(raw)==1 was the dict's ONE KEY, not a
    # 1-character token; the previous run injected a stringified dict into the page instead of
    # the real token, which is exactly why it looked like it worked but wasn't.
    token = raw.get("data") if isinstance(raw, dict) else raw
    if not token or not isinstance(token, str):
        log(f"NopeCHA returned no usable token (raw response shape: {type(raw).__name__})")
        return False
    log(f"NopeCHA returned a token (length={len(token)}) -- injecting into the page")
    try:
        # MEASURED live 2026-09-11: injecting only the textarea value did not visibly progress the
        # form (no re-submit even attempted). Many hCaptcha integrations register a
        # `data-callback="fnName"` on the widget container and read completion via THAT callback
        # firing (internal JS state), not by polling the textarea's DOM value -- setting the value
        # alone can be invisible to such a site. This now reports concrete diagnostics (how many
        # textareas were actually found, whether a callback name exists, whether it was invoked)
        # instead of injecting blind and hoping.
        result = page.evaluate(
            """(tok) => {
                const areas = document.querySelectorAll(
                    'textarea[name="h-captcha-response"], textarea[name="g-recaptcha-response"]'
                );
                areas.forEach(el => { el.value = tok; el.dispatchEvent(new Event('change', {bubbles: true})); });
                const containers = document.querySelectorAll('[data-callback], .h-captcha, [data-sitekey]');
                let callbackName = null;
                containers.forEach(c => { if (c.dataset && c.dataset.callback) callbackName = c.dataset.callback; });
                let callbackInvoked = false;
                if (callbackName && typeof window[callbackName] === 'function') {
                    try { window[callbackName](tok); callbackInvoked = true; } catch (e) {}
                }
                return {textareas_found: areas.length, callback_name: callbackName, callback_invoked: callbackInvoked};
            }""",
            token,
        )
        log(f"token injection result: {result}")
    except Exception as e:
        log(f"token injection failed: {type(e).__name__} {str(e)[:100]}")
        return False
    time.sleep(0.5)
    sub = page.locator("#sign-in-button, button:has-text('Sign in')").first
    sub_count = sub.count()
    log(f"sign-in button present after injection: {sub_count > 0} (url={page.url[:80]!r})")
    if sub_count:
        try:
            sub.click(timeout=5000)
            log("re-submitted the sign-in form after token injection")
        except Exception as e:
            log(f"re-submit click failed: {type(e).__name__} {str(e)[:100]}")
    time.sleep(2.5)
    frame = next((f for f in page.frames if "hcaptcha" in f.url and "challenge" in f.url), None)
    return frame is None


def harvest():
    with sync_playwright() as p:
        creds = json.loads(_secret("astn/ft/credentials"))
        email, password = creds["username"], creds["password"]
        log(f"email={email} headless={HEADLESS} park={PARK} egress=native-IP kimi={KIMI_MODEL}")

        # Andrew-direct 2026-09-11: hCaptcha is solved via the NopeCHA TOKEN API (see
        # solve_hcaptcha_if_present) -- "i thought you could just operate it via API solely",
        # correct, and simpler than the browser-extension route tried first, which never
        # demonstrably activated (confirmed empty ctx.service_workers/background_pages against a
        # live challenge). No extension load needed, so this is the plain non-persistent launch.
        browser = p.chromium.launch(
            channel="chrome", headless=HEADLESS,
            # FIX 2: without this, navigator.webdriver stays true -- a strong bot signal that
            # measurably raised the hCaptcha challenge rate on every unpatched run.
            args=["--disable-blink-features=AutomationControlled", "--no-first-run"],
        )
        ctx = browser.new_context(viewport={"width": 1366, "height": 900}, user_agent=UA)
        ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        # attach the network-auth listener to every page that ever opens, not just the first --
        # a popup is exactly where an auth artifact (or the next challenge) might actually appear,
        # same reasoning as sa_harvest_session.py.
        ctx.on("page", lambda p: p.on("response", _on_response))
        page = ctx.new_page()
        page.on("response", _on_response)

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
        # "let the dashboard land" lesson). MEASURED LIVE 2026-09-11: FT can independently
        # auto-redirect to a passkey-setup interstitial (accounts.ft.com/passkeys/set-up) right
        # after a real successful login -- that redirect raced this explicit navigation and threw
        # an uncaught Playwright "interrupted by another navigation" error that crashed the whole
        # harvest, even though the identity cookie had ALREADY been served by then. Tolerating the
        # race (the login is done either way) rather than letting it kill the run.
        try:
            page.goto("https://www.ft.com", wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            log(f"navigation to www.ft.com raced with FT's own redirect ({type(e).__name__}) -- "
                f"continuing from wherever the page actually is now: {page.url[:80]!r}")
        time.sleep(2.5)

        ok, names, present = has_identity(ctx)
        net_ok, net_events = has_network_auth_evidence()
        if ok and not net_ok:
            log("identity cookies present but no network auth event observed yet -- waiting 3s for one")
            time.sleep(3)
            net_ok, net_events = has_network_auth_evidence()
        log(f"END identity={ok} (cookies present: {present}) total_cookies={len(names)} "
            f"network_auth_corroborated={net_ok} network_auth_event_count={len(net_events)}")
        if ok and not net_ok:
            log("accepting the cookie-jar oracle alone -- WEAKER than network-corroborated, flagged in the bundle")

        rc = 1
        if ok:
            cookies = ctx.cookies()
            # NOTE: unlike sa_harvest_session.py's structured bundle, THIS bundle is a flat
            # cookie name->value dict served directly as astn/ft/session and consumed as a literal
            # HTTP Cookie jar (by ft_rest_fetch.py, fetch_ft.js, and other ASTN_WSJFT consumers) --
            # injecting non-cookie metadata keys here would get sent to FT's servers as bogus
            # cookies. Network-auth provenance for this run stays in the log line above only; it
            # does not travel with this specific secret's shape.
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
