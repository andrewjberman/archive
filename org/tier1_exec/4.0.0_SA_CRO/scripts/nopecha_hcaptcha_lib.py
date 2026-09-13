"""Shared hCaptcha-defeat module via the NopeCHA Token API -- factored out of ft_harvest_session.py
2026-09-11 (Andrew-direct: "we should be able to make each of these items we've fought for a
'module' that kimi can call dynamically ... if we get hCaptcha its nopeCHA module") so a second
site (Bloomberg.com) can reuse the proven, real-bug-fixed mechanism without duplicating it or
importing ft_harvest_session.py itself (unsafe: it runs a full FT login as a module-level side
effect at import time).

Three real bugs were found and fixed getting this to work (full history in
FT_AUTOMATED_AUTH_MECHANISM_20260911.md); all three fixes live here, not just documented:
  1. `nopecha.api_key = ...` (the official example's own pattern) is a DEAD ASSIGNMENT against the
     installed nopecha>=2.0 package -- module __getattr__ never fires on writes. The real key path
     is the NOPECHA_API_KEY environment variable, read once at first lazy access.
  2. Token.solve() returns the raw {"data": "<token>"} dict, not a bare string.
  3. Some sites (FT: 'onSocialSubmit') read completion via a registered `data-callback`, not the
     `h-captcha-response` textarea's value alone -- both are attempted.

ROE: never logs a token/credential value, only presence/length/shape.
"""
import os
import re
import time

import nopecha


def extract_hcaptcha_sitekey(page):
    """hCaptcha's standard site integration renders its container with a `data-sitekey` attribute
    on the PARENT page's own DOM -- far more reliable than parsing the challenge iframe's own
    asset-versioned URL for a query param that isn't guaranteed to be there in regex-matchable
    form. Frame-URL parsing is kept only as a fallback."""
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


def hcaptcha_present(page):
    return any("hcaptcha.com" in f.url and re.search(r"challenge|frame", f.url) for f in page.frames)


def solve_hcaptcha_via_nopecha(page, api_key_secret_value, log, submit_selectors=("button:has-text('Sign in')",)):
    """Solves whatever hCaptcha challenge is present on `page` via NopeCHA's Token API and injects
    the result. Returns True once the challenge frame is confirmed gone; False on any failure
    (no sitekey found, API error, no usable token, injection error) -- never fabricates success."""
    if not hcaptcha_present(page):
        return False
    sitekey = extract_hcaptcha_sitekey(page)
    if not sitekey:
        log("hCaptcha challenge detected but no sitekey could be extracted -- cannot use the Token API")
        return False
    log(f"hCaptcha challenge detected, sitekey found -- solving via NopeCHA Token API (url={page.url[:70]!r})")
    os.environ["NOPECHA_API_KEY"] = api_key_secret_value.strip()
    try:
        raw = nopecha.Token.solve(type="hcaptcha", sitekey=sitekey, url=page.url)
    except Exception as e:
        log(f"NopeCHA token solve failed: {type(e).__name__} {str(e)[:150]}")
        return False
    token = raw.get("data") if isinstance(raw, dict) else raw
    if not token or not isinstance(token, str):
        log(f"NopeCHA returned no usable token (raw response shape: {type(raw).__name__})")
        return False
    log(f"NopeCHA returned a token (length={len(token)}) -- injecting into the page")
    try:
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
    for sel in submit_selectors:
        sub = page.locator(sel).first
        if sub.count():
            try:
                sub.click(timeout=5000)
                log(f"re-submitted via {sel!r} after token injection")
            except Exception as e:
                log(f"re-submit click failed: {type(e).__name__} {str(e)[:100]}")
            break
    time.sleep(2.5)
    return not hcaptcha_present(page)
