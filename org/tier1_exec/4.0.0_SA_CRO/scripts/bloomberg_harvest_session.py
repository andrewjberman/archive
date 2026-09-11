"""Bloomberg.com session harvester -- ported almost wholesale from sa_harvest_session.py
(Andrew-direct 2026-09-11: "i would recomend using the seeking alpha scraper almost wholesale
here"), same architecture, same ROE, same completion bar. The one structural difference: Bloomberg
signs in via GOOGLE OAUTH (a Google account, not a direct email/password form), so the LOGIN state
hands off to google_oauth_handler.py instead of filling fields itself.

  our own Google Chrome (headed, native IP)
    -> Kimi-VL classifies each screen (BOT_WALL / LOGIN / LOGGED_IN / ANON / MODAL / UNKNOWN)
    -> BOT_WALL: MEASURED LIVE 2026-09-11, the SAME PerimeterX Press & Hold widget as Seeking
       Alpha -- reuses the shared press_and_hold_lib.py mechanism (checkmark-in-center release,
       not a fixed duration) rather than reimplementing it
    -> LOGIN: click 'Sign In' -> click 'Continue with Google' -> hand off to
       google_oauth_handler.handle_google_oauth() with a Bloomberg-specific Google account
       (google/andrew-goldengate/credentials, distinct from officialmadeaux's)
    -> success oracle: Kimi vision says LOGGED_IN AND at least one cookie appeared that was not
       present at the start of the run. Bloomberg's real identity-cookie NAME is not yet known
       (this is the first live attempt) -- once a real success run reveals it, IDENTITY_COOKIES
       below should be hardcoded to it exactly like Seeking Alpha's `user_id`/FT's `FTSession_s`,
       and this cookie-delta fallback narrowed or removed.
    -> park the session bundle: storage_state -> scratch; --park writes Secrets Manager bloomberg/session

ROE (inherited unchanged): observe-act-only; NEVER print a credential, OTP or cookie VALUE;
screenshots mask the password field (moot here -- no password field is ever filled directly, Google
OAuth owns that); the only persisted artifact is the session bundle.
Env: SA_SECRETS_DIR (optional dev override). Deps: playwright, requests, boto3; Google Chrome installed.
Usage: python bloomberg_harvest_session.py [--headless] [--park] [--max-steps N]
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

from press_and_hold_lib import press_and_hold_adaptive as _pahl_press_and_hold_adaptive
from nopecha_hcaptcha_lib import hcaptcha_present, solve_hcaptcha_via_nopecha

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from google_oauth_handler import handle_google_oauth

S = os.path.dirname(os.path.abspath(__file__))
A = sys.argv
HEADLESS = "--headless" in A
PARK = "--park" in A
MAX_STEPS = int(A[A.index("--max-steps") + 1]) if "--max-steps" in A else 14
# Andrew-direct 2026-09-11: "i think i need to sign in and walk it for you, can i walk the console
# instead of network" -- the automated module-dispatch loop actively re-clicks things every few
# seconds, which fights with manual mouse input in the same window. --manual disables ALL
# automated clicking: the script only WATCHES (polls is_logged_in()) while a human drives the
# browser directly, then captures and parks the session the moment it resolves -- same success
# oracle, same bundle format, as the automated path.
MANUAL = "--manual" in A
MANUAL_TIMEOUT_S = int(A[A.index("--manual-timeout") + 1]) if "--manual-timeout" in A else 300
KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
KIMI_MODEL = os.environ.get("KIMI_MODEL", "kimi-k3")
KIMI_TIMEOUT_S = 20
SESSION_SECRET_ID = "bloomberg/session"
GOOGLE_CREDS_SECRET_ID = "google/andrew-goldengate/credentials"
SEARCH_URL = "https://www.bloomberg.com/search?query=rtx"


def _secret(name):
    d = os.environ.get("SA_SECRETS_DIR")
    if d:
        return (
            open(os.path.join(d, "secret_" + name.replace("/", "_") + ".json"), encoding="utf-8")
            .read().strip()
        )
    import boto3
    return boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=name)["SecretString"].strip()


kimi_key = _secret("astn/kimi/api-key")
run_ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def log(m):
    print(f"[bbg-harvest {time.strftime('%H:%M:%S')}] {m}", flush=True)


def kimi_vision(png_bytes, prompt, max_tokens=1500, timeout=KIMI_TIMEOUT_S):
    body = {
        "model": KIMI_MODEL, "temperature": 1, "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(png_bytes).decode()}},
            {"type": "text", "text": prompt},
        ]}],
    }
    r = requests.post(KIMI_URL, json=body, headers={"Authorization": "Bearer " + kimi_key, "Content-Type": "application/json"}, timeout=timeout)
    r.raise_for_status()
    return (r.json()["choices"][0]["message"]["content"] or "").strip()


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


_CLASSIFY_CACHE = {}
_LOCATE_CACHE = {}

CLASSIFY = (
    "You are driving a Bloomberg.com browser session. Classify the CURRENT screen as EXACTLY ONE token:\n"
    "- BOT_WALL: an anti-bot interstitial -- 'Are you a robot', 'unusual activity', a 'Press & Hold' button, or a captcha.\n"
    "- LOGIN: a sign-in control or a Google account chooser/sign-in page.\n"
    "- LOGGED_IN: Bloomberg site content whose header shows a signed-in account (avatar/initials/account menu) and NO 'Sign In' control.\n"
    "- ANON: Bloomberg site content whose header shows a 'Sign In' control (not signed in).\n"
    "- MODAL: a cookie/consent/subscription/newsletter overlay blocking the page (not a login form).\n"
    "- UNKNOWN: none of the above.\n"
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
                for s in ("BOT_WALL", "LOGIN", "LOGGED_IN", "ANON", "MODAL", "UNKNOWN"):
                    if s in a:
                        if h is not None and s != "UNKNOWN":
                            _CLASSIFY_CACHE[h] = (s, "kimi")
                        return s, "kimi"
                log(f"classify: KIMI_UNPARSED {raw[:80]!r} (try {attempt + 1}/2)")
            else:
                log(f"classify: KIMI_EMPTY (try {attempt + 1}/2)")
        except Exception as e:
            log(f"classify: KIMI_ERROR {type(e).__name__} {str(e)[:100]} (try {attempt + 1}/2)")
    dom = classify_by_dom(page)
    return (dom or "UNKNOWN"), "dom"


def classify_by_dom(page):
    try:
        t = (page.title() or "").lower()
        if "robot" in t or re.search(r"press\s*&?\s*hold", page.inner_text("body")[:500], re.I):
            return "BOT_WALL"
        if "accounts.google.com" in page.url:
            return "LOGIN"
        if page.locator("button:has-text('Sign In'), a:has-text('Sign In')").count() > 0:
            return "ANON"
    except Exception:
        log("dom-classify error")
    return None


def locate(page, screenshot_fn, description):
    vp = page.viewport_size or {"width": 1366, "height": 900}
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
            raw = kimi_vision(shot, ask, max_tokens=4000)
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
            log(f"locate: KIMI_ERROR {type(e).__name__} {str(e)[:80]} (try {attempt + 1}/2)")
    return None


def press_and_hold_adaptive(page, x, y, bbox, max_hold_s=8.0, poll_interval=0.15):
    _pahl_press_and_hold_adaptive(page, x, y, bbox, log, max_hold_s=max_hold_s, poll_interval=poll_interval)


def _locate_botwall(ctx, page):
    """Same cross-page search discipline as sa_harvest_session.py's _locate_botwall -- DOM-shape
    unknown for Bloomberg's widget (no confirmed id like SA's #px-captcha), so this goes text-first
    across every open page, vision second."""
    pages = [page] + [p for p in ctx.pages if p is not page]
    for p in pages:
        try:
            el = p.locator("text=/press\\s*&?\\s*hold/i").first
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


# --- network-level auth oracle, same mechanism as sa_harvest_session.py/ft_harvest_session.py.
# MEASURED LIVE 2026-09-11: a real successful login served these identity cookies (confirmed on
# login.bloomberg.com/user-info and post-login on www.bloomberg.com) -- "identity four"-equivalent,
# same shape as Seeking Alpha's own. Recording EVERY Set-Cookie (the first exploratory run's
# necessarily-broad approach) flooded stdout with ad-tech noise AND overflowed AWS Secrets
# Manager's size limit once combined with the cookie jar in the parked bundle -- narrowing to these
# known names fixes both at the source, not just via post-hoc filtering.
TRACKED_COOKIE_NAMES = ("_user-id", "_user-token", "_user-jwt", "_user-role", "_user-data",
                        "_breg-uid", "_breg-user", "_last-refresh", "session_id", "session_key",
                        "agent_id", "gatehouse_id")
JWT_SHAPE_RE = re.compile(r"[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")
NETWORK_AUTH_EVENTS = []


def _record_network_auth_event(kind, url, name, length=None):
    # MEASURED live 2026-09-11: unlike SA/FT (a short, known identity-cookie list), Bloomberg's real
    # cookie name is unknown, so this records EVERY Set-Cookie -- and Bloomberg's page loads dozens
    # of third-party ad-tech cookies per navigation, which flooded stdout (80KB+ in one run) with
    # pure noise. Recording stays complete (for the end-of-run corroboration check and the parked
    # bundle); per-event printing is silenced. A running count is logged periodically instead.
    NETWORK_AUTH_EVENTS.append({"ts": time.time(), "url": url[:120], "kind": kind, "name": name, "length": length})
    if len(NETWORK_AUTH_EVENTS) % 50 == 0:
        log(f"NETWORK AUTH EVENTS: {len(NETWORK_AUTH_EVENTS)} recorded so far (most recent: {name!r})")


def _on_response(resp):
    try:
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
    except Exception:
        pass


def has_network_auth_evidence():
    return len(NETWORK_AUTH_EVENTS) > 0, list(NETWORK_AUTH_EVENTS)


# --- MODULE DISPATCH (Andrew-direct 2026-09-11: "we should be able to make each of these items
# we've fought for a 'module' that kimi can call dynamically. E.g., if we get press and hold we
# call press and hold module, if we get hCaptcha its nopeCHA module, if theres a google option we
# run google oauth module, etc etc. Always persistent turn-based until page resolves. always
# screenshotting. order should not matter.") -- each module is a (name, detect, handle) tuple.
# detect(page, ctx) is a CHEAP, mostly-DOM check (no Kimi call) run fresh every turn; the FIRST
# module whose detect() fires this turn gets its handle() run. Because every module is re-checked
# every turn rather than switched on a single exclusive classify() token, which obstacle appears in
# which order does not matter -- a bot wall, an hCaptcha, and a Google sign-in can occur in any
# sequence and this loop reacts to whichever is actually on screen right now.

def detect_bot_wall(page, ctx):
    # BUG FOUND live 2026-09-11 (Andrew: "it got stuck on the press and hold when it came
    # surprisingly post the accept terms modal"): the old check truncated to the body's first 1000
    # characters of inner_text, so a widget appearing further down the DOM's text order than that
    # (easily the case on a content-heavy page) was invisible to this detector even though it was
    # clearly on screen -- a real false negative, not a hard case. A Playwright text locator
    # searches the WHOLE DOM regardless of text position, with no such truncation.
    try:
        if page.locator("text=/press\\s*&?\\s*hold/i").first.count() > 0:
            return True
    except Exception:
        pass
    # MEASURED live 2026-09-11: the same class of bug as the sign-in modal -- a PerimeterX-style
    # widget is commonly rendered inside its OWN iframe (isolating it from the host page's JS), so
    # a top-level-only text search can miss it entirely even when it's clearly on screen. Check
    # every frame's own text, not just the main document's.
    try:
        for f in page.frames:
            if f == page.main_frame:
                continue
            try:
                if re.search(r"press\s*&?\s*hold", f.locator("body").inner_text(timeout=2000), re.I):
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def handle_bot_wall(page, ctx):
    wall_page, bbox, pt = _locate_botwall(ctx, page)
    if wall_page is not page:
        log(f"Press & Hold widget found on a DIFFERENT page than the tracked one: {wall_page.url[:70]!r}")
    if bbox:
        cx, cy = bbox["x"] + bbox["width"] / 2, bbox["y"] + bbox["height"] / 2
        press_and_hold_adaptive(wall_page, cx, cy, bbox)
    elif pt:
        synth_bbox = {"x": pt["x"] - 60, "y": pt["y"] - 60, "width": 120, "height": 120}
        press_and_hold_adaptive(wall_page, pt["x"], pt["y"], synth_bbox)
    else:
        log("bot wall: no text match and no vision locate on any open page -> waiting 10s")
        time.sleep(10)
    time.sleep(6)


def detect_hcaptcha(page, ctx):
    return any(hcaptcha_present(p) for p in ctx.pages)


def handle_hcaptcha(page, ctx):
    target = next((p for p in ctx.pages if hcaptcha_present(p)), page)
    key = _secret("nopecha/api-key")
    solve_hcaptcha_via_nopecha(target, key, log, submit_selectors=("button:has-text('Sign In')", "button:has-text('Sign in')"))
    time.sleep(2)


def detect_google_oauth_page(page, ctx):
    return any("accounts.google.com" in p.url for p in ctx.pages)


def handle_google_oauth_module(page, ctx):
    gpage = next(p for p in ctx.pages if "accounts.google.com" in p.url)
    log("handing off to google_oauth_handler.handle_google_oauth")
    handled = handle_google_oauth(None, "GOOGLE_OAUTH_POPUP", b"", context=ctx, page_hint=gpage,
                                   creds_secret_id=GOOGLE_CREDS_SECRET_ID)
    log(f"google_oauth_handler returned: {handled}")
    time.sleep(3)


SIGNIN_IFRAME_SELECTOR = "#reg-ui-client__iframe"


def detect_signin_iframe(page, ctx):
    """Andrew-direct 2026-09-11 (pasted the real DOM after inspecting it himself, ending the
    guesswork): the ENTIRE 'choose a sign-in method' modal -- email field, 'Continue with
    Google/Apple/BBA' -- is NOT in the top-level page's DOM at all. It loads inside
    `<iframe id="reg-ui-client__iframe" src="https://www.bloomberg.com/account/iframe/login">`,
    a div appended at the very end of <body> (hence visually centered but last in DOM order, per
    Andrew: 'its a div at the very very bottom of the elements'). Every top-level page.locator()
    search this session has been silently querying the WRONG document -- exactly why only the
    vision fallback (a screenshot, which DOES capture iframe content visually) ever reliably found
    anything on this screen. This module pierces into that iframe's own document via
    page.frame_locator() instead of guessing from outside it.

    BUG FOUND live 2026-09-11: checking bare .count() (DOM presence) rather than visibility caused
    this to falsely fire when a NEW bot-wall modal appeared ON TOP of the sign-in iframe -- the
    iframe element was still present in the DOM, just hidden behind the newer overlay, and stole
    dispatch priority from the actually-correct bot_wall module. Requiring :visible fixes it."""
    try:
        return page.locator(f"{SIGNIN_IFRAME_SELECTOR}:visible").count() > 0
    except Exception:
        return False


def handle_signin_iframe(page, ctx):
    frame = page.frame_locator(SIGNIN_IFRAME_SELECTOR)
    try:
        gbtn = frame.locator("button:has-text('Google'), a:has-text('Google'), [aria-label*='Google' i]").first
        if gbtn.count() > 0:
            gbtn.click(timeout=8000)
            log("clicked 'Continue with Google' INSIDE the sign-in iframe")
            time.sleep(2.5)
            return
    except Exception as e:
        log(f"signin_iframe: locating Google button failed: {type(e).__name__} {str(e)[:100]}")
    log("signin_iframe present but no Google button found inside it yet -- waiting")
    time.sleep(2)


def detect_google_button(page, ctx):
    try:
        return page.locator(
            "button:has-text('Google'):visible, a:has-text('Google'):visible, [aria-label*='Google' i]:visible"
        ).count() > 0
    except Exception:
        return False


def handle_click_google_button(page, ctx):
    gbtn = page.locator("button:has-text('Google'), a:has-text('Google'), [aria-label*='Google' i]").first
    gbtn.click(timeout=10000)
    log("clicked 'Continue with Google'")
    time.sleep(2.5)


def detect_sign_in_needed(page, ctx):
    try:
        if page.locator("input[type='password']:visible").count() > 0:
            return False  # a direct login form is a different module's job -- none built for
            # Bloomberg (Google-only per Andrew-direct), left as a clean detect-miss rather than a
            # silent wrong-module trigger, matching the "order should not matter" contract: a
            # detector must only fire for the shape it actually handles.
        return page.locator("button:has-text('Sign In'):visible, a:has-text('Sign In'):visible").count() > 0
    except Exception:
        return False


def handle_click_sign_in(page, ctx):
    btn = page.locator("button:has-text('Sign In'), a:has-text('Sign In')").first
    if btn.count():
        btn.click(timeout=10000)
        log("clicked 'Sign In'")
    else:
        pt = locate(page, lambda: page.screenshot(timeout=15000), "the 'Sign In' control in the page header")
        if pt:
            page.mouse.click(pt["x"], pt["y"])
            log("clicked 'Sign In' via vision")
    time.sleep(2.5)


_BACKDROP_DETECT_JS = """() => {
    const vw = window.innerWidth, vh = window.innerHeight;
    const candidates = document.querySelectorAll('body *');
    for (const el of candidates) {
        const cs = getComputedStyle(el);
        if (cs.position !== 'fixed' && cs.position !== 'absolute') continue;
        if (parseFloat(cs.opacity || '1') < 0.05) continue;
        const r = el.getBoundingClientRect();
        if (r.width < vw * 0.6 || r.height < vh * 0.6) continue;
        const m = (cs.backgroundColor || '').match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)(?:,\\s*([\\d.]+))?\\)/);
        if (!m) continue;
        const a = m[4] === undefined ? 1 : parseFloat(m[4]);
        const brightness = (parseInt(m[1]) + parseInt(m[2]) + parseInt(m[3])) / 3;
        // a dark, semi-transparent, viewport-covering element = a modal backdrop dimming the page
        // behind a brighter centered box -- Andrew-direct 2026-09-11: "if there is a way to
        // deterministically identify a central modal popup (e.g. through a dimming of the rest of
        // the page but bright loosely in the center, then that is a hint." Content-agnostic on
        // purpose -- works regardless of what the modal's text actually says, unlike matching
        // specific button labels like 'Agree'/'Accept', which only covers the wording seen so far.
        if (a > 0.15 && a < 0.98 && brightness < 100) return true;
    }
    return false;
}"""


def dump_modal_html(page, tag):
    """Andrew asked (2026-09-11) whether he needed to use DevTools himself to inspect a confusing
    modal's structure -- he doesn't; Playwright can extract the exact DOM (tags/classes/ids/ARIA
    attributes) directly, which is more precise than eyeballing the Elements panel. Called every
    turn a modal-shaped backdrop is present, independent of which module ends up handling that
    turn, so ground truth is captured even on turns where a MORE specific module (google_button,
    etc.) fires instead of the generic dismiss handler."""
    try:
        html = page.evaluate("""() => {
            const vw = window.innerWidth, vh = window.innerHeight;
            const out = [];
            for (const el of document.querySelectorAll('body *')) {
                const cs = getComputedStyle(el);
                if (cs.position !== 'fixed' && cs.position !== 'absolute') continue;
                const r = el.getBoundingClientRect();
                if (r.width < vw * 0.3 || r.height < vh * 0.3) continue;
                out.push(el.outerHTML.slice(0, 4000));
            }
            return out.join('\\n\\n---NEXT CANDIDATE---\\n\\n');
        }""")
        path = os.path.join(S, f"bbg_modal_dom_{run_ts}_{tag}.html")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html or "(no large fixed/absolute element found)")
        log(f"modal DOM dumped -> {path}")
    except Exception as e:
        log(f"modal DOM dump failed: {type(e).__name__} {str(e)[:100]}")


def detect_overlay_modal(page, ctx):
    """Andrew-direct 2026-09-11 (live observation, twice): 'kimi did not realize that there was a
    layer of pop up modal on top of the base screen, and was trying to scroll the screen back and
    forth' -- a 'We've updated our terms' consent overlay sat on top of everything else, and
    nothing checked for it BEFORE trying to click things behind it, so a Sign-In-button detector
    kept firing on a button it could see in the DOM but that was actually covered, and repeated
    failed .click() calls (which auto-scroll their target into view) produced visible scrolling.
    THIS MODULE MUST BE CHECKED FIRST, before any other module's detect() -- a page-covering
    overlay always takes priority over whatever is behind it; this is a genuine exception to
    'order should not matter' (a covering layer is definitionally ordered above what it covers).

    PRIMARY signal is the structural dimmed-backdrop heuristic (content-agnostic, same "new page
    appeared" spirit as the cross-page popup detection -- a structural fact about the DOM, not a
    guess at wording); ARIA role and known dismiss-button text are kept as fallbacks for modals that
    skip the classic dark-backdrop pattern."""
    try:
        if page.evaluate(_BACKDROP_DETECT_JS):
            return True
        if page.locator("[role='dialog']:visible, [aria-modal='true']:visible").count() > 0:
            return True
        return page.locator(
            "button:has-text('Agree'), button:has-text('Accept'), button:has-text('I Agree'), "
            "button:has-text('Got it'), button:has-text('Continue'), button:has-text('I Accept')"
        ).count() > 0
    except Exception:
        return False


def handle_dismiss_modal(page, ctx):
    # MEASURED live 2026-09-11 (Andrew's screenshot): a bare "Continue" text match is dangerously
    # generic -- one real Bloomberg sign-in modal had FOUR buttons containing "Continue" (a disabled
    # bare email-continue, plus "Continue with Google/Apple/BBA"), and this dismiss fallback grabbing
    # whichever matched first (possibly the disabled one, or the wrong provider) is exactly what
    # produced repeated failed clicks and visible scrolling. Specific phrases go first; "Continue" is
    # last-resort AND excludes any button that also names a provider (those belong to a dedicated
    # module -- google_button, etc. -- checked before this one ever runs; this exclusion is
    # defense-in-depth in case this fallback is ever reached anyway).
    for sel in (
        "button:has-text('Agree')", "button:has-text('Accept')", "button:has-text('I Agree')",
        "button:has-text('Got it')", "button:has-text('I Accept')",
        "[aria-label='Close']", "button:has-text('Close')",
        "button:has-text('Continue'):not(:has-text('Google')):not(:has-text('Apple')):not(:has-text('Facebook')):not(:has-text('Microsoft'))",
    ):
        try:
            btn = page.locator(sel).first
            if btn.count() and btn.is_visible() and btn.is_enabled():
                btn.click(timeout=5000)
                log(f"dismissed overlay via {sel!r}")
                time.sleep(1.5)
                return
        except Exception:
            continue
    # the backdrop detector is content-agnostic, so its dismiss button's wording may not match any
    # of the known text patterns above -- vision fallback before giving up and just pressing Escape.
    pt = locate(page, lambda: page.screenshot(timeout=15000),
                "the button that accepts/agrees/continues/closes this popup overlay dialog")
    if pt:
        page.mouse.click(pt["x"], pt["y"])
        log("dismissed overlay via vision")
        time.sleep(1.5)
        return
    log("overlay detected but no dismiss button matched (DOM or vision) -- trying Escape")
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    time.sleep(1.5)


# Andrew-direct 2026-09-11 (live observation): "it found the sign in button, but then it brought up
# a modal to use google sign-in, and didnt realize the modal popped up" -- a dimmed-backdrop modal
# is not ALWAYS something to dismiss and get out of the way of; here the modal WAS the login
# chooser, and its content (a 'Continue with Google' button) is exactly what needs to be clicked
# INTO, not away from. So content-specific, ACTIONABLE modules go first -- a challenge or a
# recognized sign-in control, wherever it happens to render, including inside a modal-shaped
# overlay -- and the generic "dismiss this unknown overlay" fallback runs LAST, only once nothing
# more specific was found. This still is not a violation of "order should not matter": every
# module's detect() is still checked fresh every turn: the point is HOW they're prioritized, not a
# fixed assumed SEQUENCE of prior states.
MODULES = [
    ("bot_wall", detect_bot_wall, handle_bot_wall),
    ("hcaptcha_nopecha", detect_hcaptcha, handle_hcaptcha),
    ("google_oauth", detect_google_oauth_page, handle_google_oauth_module),
    ("signin_iframe", detect_signin_iframe, handle_signin_iframe),  # the real fix -- see docstring
    ("google_button", detect_google_button, handle_click_google_button),
    ("overlay_modal", detect_overlay_modal, handle_dismiss_modal),  # generic dismiss -- LAST resort
    ("sign_in_needed", detect_sign_in_needed, handle_click_sign_in),
]


def is_logged_in(page, ctx, baseline_cookie_names):
    """Terminal/resolved check -- vision LOGGED_IN AND at least one new cookie since the run
    started. Checked FIRST every turn, before any defeat module: 'is the page already resolved'
    takes priority over 'what obstacle is currently on screen'."""
    current_names = {c["name"] for c in ctx.cookies()}
    new_cookies = current_names - baseline_cookie_names
    if not new_cookies:
        return False, new_cookies
    state, _ = classify(page, lambda: page.screenshot(timeout=15000))
    return state == "LOGGED_IN", new_cookies


def _run_manual_mode(ctx, baseline_cookie_names):
    """Andrew-direct 2026-09-11: 'i think i need to sign in and walk it for you, can i walk the
    console instead of network'. Disables ALL automated clicking -- only watches (the shared cookie
    jar plus a vision-confirmed LOGGED_IN check) while a human drives the browser directly, which
    does not fight with manual mouse input the way the automated dispatch loop would. Screenshots
    every open page each poll ('will it be recording this whole thing') -- cookies/DOM state are
    context-wide and don't depend on which window has focus, so this doesn't need to track where
    the human is actually clicking. Returns (rc, page_or_None) -- page_or_None is the Bloomberg tab
    once LOGGED_IN is confirmed, or None if the wait timed out."""
    log(f"MANUAL MODE: drive the browser yourself now -- watching for up to {MANUAL_TIMEOUT_S}s, "
        f"no automated clicking will happen. Sign in however you like (Google or otherwise); "
        f"this just watches for a new identity cookie plus a vision-confirmed logged-in screen.")
    started = time.monotonic()
    manual_poll = 0
    while time.monotonic() - started < MANUAL_TIMEOUT_S:
        manual_poll += 1
        live_pages = [p for p in ctx.pages if not p.is_closed()]
        if not live_pages:
            log("no pages left open -- stopping manual wait")
            return 1, None
        for i, p in enumerate(live_pages):
            try:
                p.screenshot(path=os.path.join(S, f"bbg_manual_{run_ts}_poll{manual_poll}_page{i}.png"), timeout=8000)
            except Exception:
                pass
        try:
            current_names = {c["name"] for c in ctx.cookies()}
            new_cookies = current_names - baseline_cookie_names
            if new_cookies:
                log(f"new cookie(s) observed: {sorted(new_cookies)} -- confirming with vision")
                target = next((p for p in live_pages if "bloomberg.com" in p.url), live_pages[0])
                state, _ = classify(target, lambda: target.screenshot(timeout=15000))
                if state == "LOGGED_IN":
                    log(f"LOGGED_IN confirmed after {time.monotonic() - started:.0f}s of manual driving")
                    return 0, target
        except Exception as e:
            log(f"manual-mode poll error (non-fatal, continuing to watch): {type(e).__name__} {str(e)[:100]}")
        time.sleep(3)
    log(f"manual mode timed out after {MANUAL_TIMEOUT_S}s without detecting a logged-in state")
    return 1, None


with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="chrome", headless=HEADLESS,
        args=["--disable-blink-features=AutomationControlled", "--no-first-run"],
    )
    ctx = browser.new_context(viewport={"width": 1366, "height": 900}, locale="en-US", timezone_id="America/New_York")
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    page = ctx.new_page()
    ctx.on("page", lambda p: p.on("response", _on_response))
    page.on("response", _on_response)

    log(f"headless={HEADLESS} park={PARK} egress=native-IP kimi={KIMI_MODEL} google_creds={GOOGLE_CREDS_SECRET_ID}")
    page.goto(SEARCH_URL, timeout=90000, wait_until="domcontentloaded")
    time.sleep(4)
    baseline_cookie_names = {c["name"] for c in ctx.cookies()}
    log(f"baseline cookies at start: {len(baseline_cookie_names)}")

    rc = 1
    if MANUAL:
        rc, manual_page = _run_manual_mode(ctx, baseline_cookie_names)
        if manual_page is not None:
            page = manual_page

    # MANUAL mode never runs the automated dispatch loop at all (range(0) below) -- keeps the
    # existing loop body's indentation/logic completely untouched rather than re-nesting it.
    consecutive_no_match = 0
    known_pages = list(ctx.pages)
    for step in range(0 if MANUAL else MAX_STEPS):
        # BUG FOUND live 2026-09-11: a Google OAuth popup can CLOSE ITSELF once auth completes (a
        # normal, expected pattern -- it posts back to its opener and closes) -- and the tracked
        # `page` variable, still pointing at that now-dead Page object, crashed the whole harvest
        # on the very next screenshot with an unhandled TargetClosedError. What looked like an
        # external browser closure ("Andrew: however, when the final modal popped up for text
        # input and password it finished it") was actually the popup's own successful-completion
        # close -- so recover by switching to any still-open page BEFORE doing anything else.
        if page.is_closed():
            still_open = [p for p in ctx.pages if not p.is_closed()]
            if not still_open:
                log("the tracked page closed and no other page is open -- nothing left to drive, stopping")
                break
            page = still_open[0]
            log(f"tracked page closed (likely a completed OAuth popup closing itself) -- switching to still-open page: {page.url[:70]!r}")

        # Andrew-direct 2026-09-11: "always screenshotting" -- unconditional, every turn, before
        # anything else runs, regardless of which module (if any) ends up handling this turn.
        try:
            page.screenshot(path=os.path.join(S, f"bbg_harvest_{run_ts}_step{step}.png"), timeout=15000)
        except Exception:
            pass
        if detect_overlay_modal(page, ctx):
            dump_modal_html(page, f"step{step}")

        current_pages = [p for p in ctx.pages if not p.is_closed()]
        new_pages = [p for p in current_pages if p not in known_pages]
        if new_pages:
            page = new_pages[-1]
            log(f"NEW PAGE/POPUP detected ({len(current_pages)} open total) -- switching active page to it: {page.url[:70]!r}")
        known_pages = current_pages

        resolved, new_cookies = is_logged_in(page, ctx, baseline_cookie_names)
        log(f"step {step}: url={page.url[:70]!r} resolved={resolved} new_cookies={sorted(new_cookies)}")
        if resolved:
            net_ok, events = has_network_auth_evidence()
            if not net_ok:
                log("new cookie(s) present but no network auth event observed yet -- waiting 3s for one")
                time.sleep(3)
                net_ok, events = has_network_auth_evidence()
            if net_ok:
                log(f"LOGGED_IN with new cookie(s), corroborated by {len(events)} network auth event(s) -- settling 4s")
            else:
                log("LOGGED_IN with new cookie(s) but NO corroborating network auth event -- accepting the "
                    "weaker jar-delta oracle alone, flagged as such in the parked bundle")
            time.sleep(4)
            rc = 0
            break

        # "Persistent turn-based until page resolves ... order should not matter": every module's
        # detect() is checked fresh THIS turn, not switched on a single exclusive prior-state token.
        matched = None
        for name, detect, handle in MODULES:
            try:
                if detect(page, ctx):
                    matched = name
                    log(f"module matched: {name!r}")
                    handle(page, ctx)
                    break
            except Exception as e:
                log(f"module {name!r} error: {type(e).__name__} {str(e)[:100]}")
        if matched:
            consecutive_no_match = 0
            continue

        consecutive_no_match += 1
        if consecutive_no_match >= 3:
            log("3 consecutive turns with no module match and no resolution -> stopping")
            break
        state, src = classify(page, lambda: page.screenshot(timeout=15000))
        log(f"no module matched -- vision fallback classify: {state} ({src})")
        if state == "MODAL":
            pt = locate(page, lambda: page.screenshot(timeout=15000),
                        "the close (X) button or 'Accept' button of the overlay dialog")
            if pt:
                page.mouse.click(pt["x"], pt["y"])
            else:
                page.keyboard.press("Escape")
            time.sleep(2)
        else:
            time.sleep(4)

    current_names = {c["name"] for c in ctx.cookies()}
    new_cookies = sorted(current_names - baseline_cookie_names)
    net_ok, net_events = has_network_auth_evidence()
    log(f"END rc={rc} new_cookies={new_cookies} network_auth_corroborated={net_ok} "
        f"network_auth_event_count={len(net_events)} total_cookies={len(current_names)}")
    bundle_path = os.path.join(S, f"bloomberg_session_{run_ts}.json")
    storage_state = ctx.storage_state()
    if rc == 0:
        cookies = storage_state["cookies"]
        bundle = {
            "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
            "google_creds_secret_id": GOOGLE_CREDS_SECRET_ID,
            "user_agent": page.evaluate("navigator.userAgent"),
            "new_cookie_names_this_run": new_cookies,
            "cookie_names": sorted({c["name"] for c in cookies}),
            "all_cookies": cookies,
            "network_auth_corroborated": net_ok,
            "network_auth_events": [{k: v for k, v in e.items() if k != "ts"} for e in net_events],
        }
        json.dump(bundle, open(bundle_path, "w"), indent=1)
        log(f"session bundle -> {bundle_path} ({len(cookies)} cookies)")
        if PARK:
            import boto3
            # BUG FOUND live 2026-09-11: the full bundle (125 cookies incl. dozens of third-party
            # ad-tech ones, plus 308 network_auth_events) exceeded AWS Secrets Manager's size limit
            # and the park failed after a real, successful login -- the identity was captured but
            # never got parked. Fixed by parking a TRIMMED bundle: Bloomberg-domain cookies only
            # (every real identity cookie is Bloomberg-domain; third-party ones are never needed
            # for REST access anyway) and a small events sample + count instead of the full list.
            # The full, untrimmed bundle still exists locally at bundle_path for audit.
            bbg_cookies = [c for c in cookies if "bloomberg" in c.get("domain", "")]
            parked_bundle = dict(bundle)
            parked_bundle["cookie_names"] = sorted(c["name"] for c in bbg_cookies)
            parked_bundle["all_cookies"] = bbg_cookies
            parked_bundle["network_auth_event_count"] = len(net_events)
            parked_bundle["network_auth_events"] = parked_bundle["network_auth_events"][-10:]
            log(f"parking TRIMMED bundle: {len(bbg_cookies)} bloomberg-domain cookies of {len(cookies)} total, "
                f"{len(net_events)} network events summarized")
            sm = boto3.client("secretsmanager", region_name="us-east-1")
            try:
                sm.describe_secret(SecretId=SESSION_SECRET_ID)
                exists = True
            except sm.exceptions.ResourceNotFoundException:
                exists = False
            try:
                if exists:
                    resp = sm.put_secret_value(SecretId=SESSION_SECRET_ID, SecretString=json.dumps(parked_bundle))
                else:
                    resp = sm.create_secret(
                        Name=SESSION_SECRET_ID,
                        Description="Bloomberg.com parked session bundle (harvested by the Kimi authenticator pattern via Google OAuth). Consumers ride this; never log in inline.",
                        SecretString=json.dumps(parked_bundle),
                        Tags=[{"Key": "service", "Value": "bloomberg"}, {"Key": "kind", "Value": "site-session"}],
                    )
                log(f"park -> {SESSION_SECRET_ID}: {'updated' if exists else 'CREATED'} VersionId={resp.get('VersionId')}")
            except Exception as e:
                log(f"park FAILED {type(e).__name__}: {str(e)[:200]}")
                rc = 1
    browser.close()
sys.exit(rc)
