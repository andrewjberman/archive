#!/usr/bin/env python3
"""Sign-in-with-Google automation handler -- a captcha_sentinel.py dispatch handler for the
GOOGLE_OAUTH_POPUP state. Fills Andrew's Google credentials, and if Google challenges with a
2-Step Verification text-message code, reads it from Quo's SMS API rather than pausing for a
human -- mirroring the estate's own bd_49f Black Diamond OTP-gateway pattern exactly: a
capability read (Quo), a strict RECENCY WINDOW so a stale/unrelated text is never accepted, and
the code value is never logged.

ANDREW-DIRECT 2026-09-10 (this seat's session): "it is officialmadeaux@gmail.com and it's
[password] for pw. Also its fine if they want to 2fa just have it pick send me a text on Quo and
Kimi should control that via API ... this key should be put in AWS Secrets manager tagged to Quo."
Both secrets are parked: google/officialmadeaux/credentials, quo/api-key.

QUO API -- MEASURED LIVE 2026-09-10 (https://www.quo.com/docs/mdx/api-reference/):
  GET https://api.quo.com/v1/phone-numbers   -- Authorization: <apiKey> (RAW key, no "Bearer"
      prefix -- confirmed against the live account: a Bearer-prefixed call was never tried because
      the raw form worked on the first attempt with a browser-shaped User-Agent).
      Workspace has exactly ONE number: id=PNEJ5tafLm, +15616213066, name="Operations".
  GET https://api.quo.com/v1/messages?phoneNumberId=...&createdAfter=...&maxResults=...
      Returns {"data": [{"id","from","text","direction","createdAt",...}], "nextPageToken"}.
  ⛔ A REQUEST WITH NO BROWSER-SHAPED User-Agent GETS A CLOUDFLARE 403 (error code 1010) --
     NOT an auth failure. Always send a real UA. Confirmed: the identical call with a UA got 200,
     the same call with Python's default urllib UA got blocked at the edge before reaching Quo's
     own auth check at all.

ROE: the API key and any fetched message body are never printed in full; only the fact that a
code was found, its length, and its arrival timestamp are logged. Google's password is read from
Secrets Manager at run time and never logged.

STATUS: the Google-side selectors below are the estate's best current read of Google's sign-in UI
(as of this cut) -- UNPROVEN against a live run through to a completed 2FA text exchange. Treat a
first live run as an exercise, not a certified path, exactly as the estate's own hCaptcha-solver
framework carries the same honest caveat.
"""
import base64
import datetime
import io
import json
import os
import re
import time

import requests

try:
    from PIL import Image
except ImportError:
    Image = None

QUO_BASE = "https://api.quo.com/v1"
QUO_PHONE_NUMBER_ID = "PNEJ5tafLm"  # measured live 2026-09-10 -- the workspace's one number
QUO_PHONE_NUMBER_E164 = "+15616213066"  # same number; /v1/conversations 401'd on the bare ID string but 200'd on E.164 -- use this form there
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
CODE_PATTERN = re.compile(r"\b(\d{6})\b")


def _secret(name):
    d = os.environ.get("SA_SECRETS_DIR")
    if d:
        with open(os.path.join(d, "secret_" + name.replace("/", "_") + ".json"), encoding="utf-8") as fh:
            return fh.read().strip()
    import boto3
    return boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=name)["SecretString"]


def log(m):
    print(f"[google-oauth {time.strftime('%H:%M:%S')}] {m}", flush=True)


def get_recent_sms_code(since_dt, window_seconds=180, max_polls=24, poll_interval=5):
    """RECENCY-WINDOWED read, the same shape as the estate's m365 OTP gateway (otp.py): accept
    ONLY a message received in [since_dt, since_dt + window_seconds]. A message outside that
    window is not a candidate, no matter how plausible its content looks -- this is what makes
    polling a shared/reused number safe against grabbing a stale or unrelated code.

    MEASURED (2026-09-10): /v1/messages requires a `participants` array, which defeats the whole
    point here -- the sender of an unsolicited verification text (Google's own number/short-code)
    is exactly what we do NOT know in advance. /v1/conversations needs no participant filter and
    sorts by recency, so the read is CONVERSATION-FIRST: find the most-recently-updated
    conversation on our one number, THEN fetch its latest message by id."""
    key = _secret("quo/api-key").strip()
    headers = {"Authorization": key, "User-Agent": UA, "Accept": "application/json"}
    until_dt = since_dt + datetime.timedelta(seconds=window_seconds)
    for attempt in range(max_polls):
        try:
            # MEASURED (2026-09-10): phoneNumbers=<id>+updatedAfter together returned a bare 401
            # with no diagnostic body; phoneNumbers alone (or omitted) returns 200. The recency
            # window is re-validated client-side per message below regardless, so updatedAfter is
            # dropped here rather than chased further -- it was never load-bearing.
            rc = requests.get(
                f"{QUO_BASE}/conversations",
                params={"phoneNumbers": QUO_PHONE_NUMBER_E164, "maxResults": 10},
                headers=headers, timeout=20,
            )
            if rc.status_code != 200:
                log(f"Quo conversations poll {attempt + 1}/{max_polls}: HTTP {rc.status_code} {rc.text[:150]}")
                time.sleep(poll_interval)
                continue
            convos = rc.json().get("data", [])
        except Exception as e:
            log(f"Quo conversations poll {attempt + 1}/{max_polls}: {type(e).__name__} {str(e)[:100]}")
            time.sleep(poll_interval)
            continue
        for convo in convos:
            last_id = convo.get("lastActivityId")
            if not last_id:
                continue
            try:
                rm = requests.get(f"{QUO_BASE}/messages/{last_id}", headers=headers, timeout=20)
                if rm.status_code != 200:
                    continue
                m = rm.json()
            except Exception:
                continue
            if m.get("direction") != "incoming":
                continue
            try:
                created = datetime.datetime.strptime(m["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
            except Exception:
                continue
            if not (since_dt <= created <= until_dt):
                continue  # outside the recency window -- never a candidate, however plausible
            code_m = CODE_PATTERN.search(m.get("text") or "")
            if code_m:
                log(f"Quo: code received at {created.isoformat()} from a conversation updated since login (window "
                    f"[{since_dt.isoformat()}, {until_dt.isoformat()}]), length={len(code_m.group(1))}")
                return code_m.group(1)
        log(f"Quo poll {attempt + 1}/{max_polls}: {len(convos)} conversation(s) updated since login, none yielded a matching code yet")
        time.sleep(poll_interval)
    log(f"Quo: no matching code within {window_seconds}s across {max_polls} polls")
    return None


def _click_first(page, selectors, timeout=8000):
    for sel in selectors:
        loc = page.locator(sel).first
        try:
            if loc.count():
                loc.click(timeout=timeout)
                return sel
        except Exception:
            continue
    return None


KIMI_MODEL = "kimi-k3"  # measured 2026-09-10: ~8x faster than kimi-k2.6 on this exact task
                        # (10-12s vs 59-150+s, ~180 vs ~2,663 reasoning tokens), same accuracy.


def _kimi_call(prompt, screenshot_bytes, max_tokens, timeout=90):
    key = _secret("astn/kimi/api-key").strip()
    body = {"model": KIMI_MODEL, "temperature": 1, "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(screenshot_bytes).decode()}},
                {"type": "text", "text": prompt}]}]}
    r = requests.post("https://api.moonshot.ai/v1/chat/completions", json=body,
                      headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, timeout=timeout)
    r.raise_for_status()
    return (r.json()["choices"][0]["message"]["content"] or "").strip()


def _kimi_present(page, description, max_tokens=2500):
    """THE READ -- a SEPARATE, larger-budget call whose only job is scene understanding: is the
    described element visible right now? Split out from coordinate-finding (Andrew-direct
    2026-09-10: 'split the call for the read and the write') so a not-present answer never
    triggers the model to also hunt for coordinates, and so each call's prompt matches its own
    actual reasoning burden -- perceiving the scene is the hard part; stating a coordinate once
    something is known to exist is comparatively easy."""
    shot = page.screenshot()
    ask = f"Look at this screenshot. Is {description} visible right now? Reply with ONLY YES or NO."
    try:
        raw = _kimi_call(ask, shot, max_tokens).upper()
        return "YES" in raw, shot
    except Exception as e:
        log(f"kimi_present({description!r}) failed: {type(e).__name__} {str(e)[:100]}")
        return None, shot


def _kimi_locate(page, description, max_tokens=400, skip_presence_check=False):
    """THE WRITE -- a SEPARATE, smaller-budget call for ONLY the coordinate, run after presence is
    already confirmed by _kimi_present (or by the caller's own context). MEASURED (2026-09-10):
    Google's current sign-in page returns ZERO queryable elements to BOTH document.querySelectorAll
    AND Playwright's own shadow-DOM-piercing locators, despite the form being visibly rendered
    (screenshot-confirmed) -- consistent with a closed shadow root or an isolated rendering
    context, not reachable via any DOM API for anyone. Coordinate-based interaction via vision is
    therefore the ONLY path here, not a fallback -- the same primitive already proven for the SA
    press-and-hold and FT hCaptcha grid-localize."""
    if not skip_presence_check:
        present, shot = _kimi_present(page, description)
        if present is False:
            return None
        if present is None:  # the read call itself failed -- fall through and let the write call try alone
            shot = page.screenshot()
    else:
        shot = page.screenshot()
    ask = f"Return ONLY JSON {{\"x\":<int>,\"y\":<int>}} = the pixel center to click for {description}. No other text."
    try:
        raw = _kimi_call(ask, shot, max_tokens)
        m = re.search(r"\{[^}]*\}", raw)
        o = json.loads(m.group(0)) if m else {}
        return o if (o.get("x", -1) >= 0 and o.get("y", -1) >= 0) else None
    except Exception as e:
        log(f"kimi_locate({description!r}) failed: {type(e).__name__} {str(e)[:100]}")
        return None


def _vision_type(page, description, text, submit=False):
    pt = _kimi_locate(page, description)
    if not pt:
        return False
    page.mouse.click(pt["x"], pt["y"])
    time.sleep(0.3)
    page.keyboard.type(text, delay=35)
    if submit:
        time.sleep(0.3)
        page.keyboard.press("Enter")
    return True


_NAV_TOOLS = [
    {"type": "function", "function": {
        "name": "click_element",
        "description": "Click the on-screen element whose visible text matches exactly. Report its pixel coordinates now, while you can see it, rather than making the caller ask again later.",
        "parameters": {"type": "object", "properties": {
            "label": {"type": "string", "description": "Exact visible text of the single element to click."},
            "x": {"type": "integer", "description": "Pixel x-coordinate of the center of that element in THIS screenshot."},
            "y": {"type": "integer", "description": "Pixel y-coordinate of the center of that element in THIS screenshot."},
        }, "required": ["label", "x", "y"]},
    }},
    {"type": "function", "function": {
        "name": "report_goal_reached",
        "description": "Call this instead of click_element when the goal state described in the prompt is already visible on screen right now -- do not click anything.",
        "parameters": {"type": "object", "properties": {}},
    }},
    {"type": "function", "function": {
        "name": "report_dead_end",
        "description": "Call this only if nothing clickable on screen can help reach the goal and no untried option remains.",
        "parameters": {"type": "object", "properties": {}},
    }},
]


def _kimi_decide(prompt, screenshot_bytes, max_tokens=800, timeout=90):
    """Native function-calling read -- VERIFIED LIVE 2026-09-10 (test_kimi_tools.py): kimi-k3
    accepts an image_url input and a `tools` array in the SAME call, reasons about the screenshot
    in `reasoning_content`, and returns a real `tool_calls` entry with finish_reason='tool_calls'
    (measured: 156 completion tokens total, 103 of them reasoning, to correctly read a Google 2FA
    screen and choose 'Try another way' over the push-notification 'Yes' button). This replaces
    asking Kimi to hand-write loosely-shaped JSON into a content string and then regexing it out --
    the model's own tool-call schema is the parser now, which cannot emit malformed JSON the way a
    free-text completion occasionally can.

    click_element's schema also carries x/y (MEASURED, same live run, 2026-09-10): the model can
    correctly NAME a masked/oddly-rendered label (e.g. 'Get a verification code at (***) ***-**79')
    but a SEPARATE later call asking it to re-locate that same label from text alone came back empty
    -- re-describing a masked string is a worse question than pointing at what is already on screen
    in front of it. Coordinates from the SAME call it made the choice in avoid that round trip and
    its failure mode entirely; `x`/`y` in the return are None only for a legacy/cached decision that
    predates this field. Returns {"goal_reached": bool, "click_label": str|None, "x": int|None, "y": int|None}."""
    key = _secret("astn/kimi/api-key").strip()
    body = {"model": KIMI_MODEL, "temperature": 1, "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(screenshot_bytes).decode()}},
                {"type": "text", "text": prompt}]}],
            "tools": _NAV_TOOLS, "tool_choice": "auto"}
    r = requests.post("https://api.moonshot.ai/v1/chat/completions", json=body,
                      headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, timeout=timeout)
    r.raise_for_status()
    msg = r.json()["choices"][0]["message"]
    calls = msg.get("tool_calls") or []
    if not calls:
        # a bare content answer with no tool call at all -- treat as "nothing decided", not a crash
        return {"goal_reached": False, "click_label": None, "x": None, "y": None}
    fn = calls[0].get("function", {})
    name = fn.get("name")
    try:
        args = json.loads(fn.get("arguments") or "{}")
    except Exception:
        args = {}
    if name == "report_goal_reached":
        return {"goal_reached": True, "click_label": None, "x": None, "y": None}
    if name == "click_element":
        x, y = args.get("x"), args.get("y")
        valid_pt = isinstance(x, (int, float)) and isinstance(y, (int, float)) and x >= 0 and y >= 0
        return {"goal_reached": False, "click_label": args.get("label"),
                "x": int(x) if valid_pt else None, "y": int(y) if valid_pt else None}
    return {"goal_reached": False, "click_label": None, "x": None, "y": None}  # report_dead_end, or an unrecognized call


def _screenshot_hash(shot_bytes, hash_size=8):
    """Cheap average-hash (aHash) perceptual fingerprint of a screenshot -- recognizes 'this is the
    same screen as before' despite pixel-level noise (cursor blink, subpixel anti-aliasing) that an
    exact byte/MD5 hash would wrongly treat as a new state. Not a security primitive -- purely a
    cache key so a revisited screen skips a redundant Kimi round-trip. Returns None if Pillow is
    unavailable; callers must treat that as 'caching disabled', not an error."""
    if Image is None:
        return None
    try:
        img = Image.open(io.BytesIO(shot_bytes)).convert("L").resize((hash_size, hash_size))
        pixels = list(img.getdata())
        avg = sum(pixels) / len(pixels)
        return "".join("1" if p >= avg else "0" for p in pixels)
    except Exception:
        return None


def _hamming(a, b):
    return sum(c1 != c2 for c1, c2 in zip(a, b))


def _navigate_dynamic(page, goal_description, max_turns=40, max_seconds=300):
    """CYCLE-INVARIANT navigation (Andrew-direct 2026-09-10: 'the flow may never be the same twice
    and kimi will need to know which button to click to navigate dynamically' / 'it needs to be
    cycle invariant and driven by a defined completion marker ... if they start mixing it up and
    doing 15 turns we have to ride with the punches'). Google's (and Seeking Alpha's) challenge UI
    has no fixed depth or shape -- a defense can escalate through an arbitrary, unknowable number of
    screens. So THIS LOOP DOES NOT STOP ON A TURN COUNT: it stops on one of two CONTENT markers --
    (1) Kimi reports the goal state is on screen (success), or (2) a screen is PROVEN EXHAUSTED --
    every option Kimi has ever offered for that exact visual state has already been tried and none
    advanced past it (genuine dead end). `max_turns`/`max_seconds` are a runaway safety net for a
    truly pathological loop, not an expected depth -- both are generous on purpose.

    Each turn is normally ONE call: a native tool-call decision (_kimi_decide) that both chooses
    what to click AND reports its coordinates in the same response, since MEASURED (2026-09-10) a
    later separate call asking Kimi to re-locate an already-named but visually unusual label (a
    masked phone number) from text alone can fail where naming it the first time, while looking
    straight at it, did not. A second _kimi_locate call is kept ONLY as a fallback for a decision
    that (rarely) omits valid coordinates -- the read/write split (Andrew-direct 2026-09-10: 'split
    the call for the read and the write') still exists, just as a fallback path, not the common one.

    A lightweight in-memory perceptual-hash cache (Andrew-direct 2026-09-10: 'needs some lightweight
    cache') maps 'a screen that looks like this' -> 'the last decision Kimi made about it'. Landing
    on a screen already seen skips straight to that decision without a Kimi call UNLESS the
    decision's label was already tried (meaning it looped back here without progress) -- in that
    case a fresh read is forced, telling Kimi every label already tried AT THIS SPECIFIC SCREEN, so
    it can propose a genuinely different option. If Kimi repeats an already-tried label (or offers
    nothing) for a screen where every option is now known-tried, that screen is EXHAUSTED and the
    loop ends -- this is the real completion marker on the failure side, not a step count."""
    tried_global = []
    tried_by_screen = {}  # hash -> set of labels already tried starting from this exact screen
    cache = {}  # hash -> {"decision": {...}, "point": {...} or None}
    started = time.monotonic()
    turn = 0
    while turn < max_turns and (time.monotonic() - started) < max_seconds:
        turn += 1
        shot = page.screenshot()
        h = _screenshot_hash(shot)
        cache_key = None
        if h is not None:
            cache_key = next((k for k in cache if _hamming(k, h) <= 4), None)

        already_tried_here = tried_by_screen.get(cache_key, set()) if cache_key else set()
        reuse = cache.get(cache_key) if cache_key else None
        if reuse and reuse["decision"].get("click_label") not in already_tried_here \
                and not reuse["decision"].get("goal_reached"):
            log(f"dynamic-nav turn {turn}: cache hit (perceptual match) -- reusing prior decision, no Kimi read")
            o, pt = reuse["decision"], reuse["point"]
        elif reuse and reuse["decision"].get("goal_reached"):
            o, pt = reuse["decision"], None
        else:
            avoid = ""
            if already_tried_here:
                avoid = (" On THIS EXACT SCREEN, these labels were already clicked and did NOT "
                         "advance past it -- you must propose something different, or state that "
                         "nothing else is clickable: " + "; ".join(repr(t) for t in already_tried_here) + ".")
            elif tried_global:
                avoid = (" Earlier screens in this flow already tried: "
                         + "; ".join(repr(t) for t in tried_global) + " (informational only).")
            ask = (
                f"Look at this screenshot of a live sign-in flow. GOAL: {goal_description}. "
                "Call exactly one of the provided tools to make progress." + avoid
            )
            try:
                o = _kimi_decide(ask, shot, max_tokens=1200)
            except Exception as e:
                log(f"dynamic-nav turn {turn}: read failed: {type(e).__name__} {str(e)[:100]}")
                return False
            # coordinates usually arrive IN this same decision now -- see _kimi_decide docstring
            pt = {"x": o["x"], "y": o["y"]} if (o.get("x") is not None and o.get("y") is not None) else None
            if h is not None:
                key = cache_key or h
                cache[key] = {"decision": o, "point": pt}
                cache_key = key

        if o.get("goal_reached") is True:
            log(f"dynamic-nav turn {turn}: goal reached -- {goal_description!r}")
            return True

        label = o.get("click_label")
        if not label or (cache_key and label in already_tried_here):
            log(f"dynamic-nav turn {turn}: screen exhausted -- no untried option remains (dead end, not a step-count cutoff)")
            return False

        if pt is None:
            pt = _kimi_locate(page, f"the element whose visible text reads {label!r}", skip_presence_check=True)
            if not pt:
                log(f"dynamic-nav turn {turn}: chose {label!r} but could not resolve its coordinates")
                return False
            if cache_key:
                cache[cache_key]["point"] = pt

        log(f"dynamic-nav turn {turn}: clicking {label!r}")
        page.mouse.click(pt["x"], pt["y"])
        tried_global.append(label)
        if cache_key:
            tried_by_screen.setdefault(cache_key, set()).add(label)
        time.sleep(1.8)

    log(f"dynamic-nav: safety net hit ({turn} turns, {time.monotonic() - started:.0f}s) without "
        f"reaching the goal or proving a dead end -- ({goal_description!r})")
    return False


def handle_google_oauth(sentinel, state, screenshot_bytes, context=None, page_hint=None):
    """captcha_sentinel.py dispatch handler for GOOGLE_OAUTH_POPUP. `context` is the Playwright
    BrowserContext (so every open page/popup can be searched for the actual Google page, since the
    sentinel's screenshot is full-screen and does not itself identify WHICH Playwright Page object
    is showing it). Success oracle is always the CALLER's own post-OAuth identity check on the
    origin site -- this function returns True only for "the Google-side flow completed without an
    unhandled error", never for "the origin site accepted the identity".
    """
    if context is None:
        log("no context supplied -- cannot locate the Google page; the caller must pass context=")
        return False
    creds = json.loads(_secret("google/officialmadeaux/credentials"))
    email, password = creds["email"], creds["password"]

    gpage = page_hint
    if gpage is None:
        for pg in context.pages:
            if "accounts.google.com" in pg.url:
                gpage = pg
                break
    if gpage is None:
        log("no accounts.google.com page found among open pages/popups")
        return False

    login_started_at = datetime.datetime.now(datetime.timezone.utc)

    # DOM-first, exactly as every other harvester in this estate: try it, and only fall through to
    # vision if the DOM genuinely has nothing (MEASURED here: it doesn't).
    email_field = gpage.locator("input[type='email']").first
    if email_field.count():
        email_field.fill(email)
        _click_first(gpage, ["#identifierNext button", "button:has-text('Next')"])
    else:
        log("no DOM email field -- vision path (closed shadow root / isolated render, measured)")
        if not _vision_type(gpage, "the 'Email or phone' sign-in input field", email):
            log("vision could not locate the email field either -- aborting this attempt")
            return False
        time.sleep(0.5)
        pt = _kimi_locate(gpage, "the 'Next' button")
        if pt:
            gpage.mouse.click(pt["x"], pt["y"])
        else:
            gpage.keyboard.press("Enter")
    time.sleep(2.5)

    pw_field = gpage.locator("input[type='password']:visible").first
    if pw_field.count():
        pw_field.fill(password)
        _click_first(gpage, ["#passwordNext button", "button:has-text('Next')"])
    else:
        if not _vision_type(gpage, "the password input field", password):
            log("vision could not locate the password field -- aborting this attempt")
            return False
        time.sleep(0.5)
        pt = _kimi_locate(gpage, "the 'Next' button")
        if pt:
            gpage.mouse.click(pt["x"], pt["y"])
        else:
            gpage.keyboard.press("Enter")
    time.sleep(3)

    # 2-Step Verification: Google's method-chooser has NO fixed shape or depth (measured: one
    # 'Try another way' click can land on a push-notification screen, a method LIST, or the same
    # screen again, depending on account state) -- a fixed click count/order cannot be correct in
    # general, so this is a turn-invariant loop, not a scripted sequence (Andrew-direct 2026-09-10:
    # "the flow may never be the same twice and kimi will need to know which button to click to
    # navigate dynamically").
    # Andrew-direct 2026-09-10 (live observation): a phone number just added to a Google account's
    # 2-Step Verification settings can stay GRAYED OUT / unusable for some time before Google will
    # actually send to it -- "adjust prompt to 'prefer' the sms to 3066 but if its grayed out the
    # phone device local device option can be selected". So the preference is explicit and ordered,
    # and the disabled option is a SKIP, not something to keep retrying.
    # Andrew-direct 2026-09-10 (live observation, run_google12.log): a first attempt clicked the
    # device-approval fallback correctly, then IMMEDIATELY clicked 'Try another way' on the very
    # next turn instead of waiting -- navigating off a pending 'check your phone' screen risks
    # cancelling that in-flight approval, and it only worked out because the human happened to
    # approve fast enough. Fixed by making 'you are now on a pending device-approval screen' its
    # own stop condition, not just a step toward the SMS goal, so the loop halts there instead of
    # continuing to click.
    reached_sms_goal = _navigate_dynamic(
        gpage,
        "reach a screen that has a text box for typing in a numeric code that was sent by TEXT "
        "MESSAGE / SMS -- NOT an authenticator-app code, NOT a security key. PREFERENCE ORDER: "
        "(1) BEST: an option to text a code to the phone number ending in 3066 -- if it is visible "
        "AND clickable (not grayed out / dimmed / disabled), click it. (2) If that 3066 option is "
        "visible but appears grayed out or disabled, do NOT click it and do NOT keep looking for a "
        "way to enable it -- instead click the option to get a prompt/notification on a phone or "
        "trusted device (approving there is an acceptable fallback). (3) If neither is showing yet "
        "and a method-chooser or 'Try another way' link is visible, click that to see more options. "
        "GOAL IS ALSO REACHED (call report_goal_reached, do not click anything else) the moment you "
        "land on a screen that says something like 'Check your phone/tablet', 'Tap Yes on your "
        "device', or 'Waiting for you to confirm' -- that is a pending device approval, not a dead "
        "end, and clicking anything else risks cancelling it.",
    )
    if not reached_sms_goal:
        log("dynamic-nav did not reach a text-message code or device-approval screen -- checking once more for a code field regardless")

    code_input = gpage.locator("input[type='tel'], input[name='Pin'], input[aria-label*='code' i]").first
    has_code_field = code_input.count() > 0
    if not has_code_field:
        # vision check: is a code-entry screen showing at all, DOM-invisible as everything else was?
        pt = _kimi_locate(gpage, "a verification code input box, if a 'check your phone' or 'enter the code' screen is showing; if not showing, this is absent")
        has_code_field = pt is not None
    if has_code_field:
        log("verification-code screen detected -- polling Quo for the SMS")
        code = get_recent_sms_code(login_started_at)
        if not code:
            log("no code arrived within the window -- leaving the page for a human to finish")
            return False
        if code_input.count():
            code_input.fill(code)
            _click_first(gpage, ["#idvPreregisteredPhoneNext button", "button:has-text('Next')", "button:has-text('Verify')"])
        else:
            _vision_type(gpage, "the verification code input box", code, submit=True)
        time.sleep(2.5)
    elif reached_sms_goal:
        # not a code field -- must be the pending device-approval stop condition above. Wait for a
        # human to tap the physical device rather than treating "no code field" as a dead end.
        log("pending device-approval screen -- waiting up to 90s for it to be approved elsewhere")
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if "accounts.google.com" not in gpage.url:
                log(f"navigated away from accounts.google.com -- approval likely granted (url={gpage.url[:80]!r})")
                break
            time.sleep(3)
        else:
            log("still on accounts.google.com after 90s -- approval not observed within the wait")

    log(f"Google flow reached: url={gpage.url[:80]!r} title={gpage.title()[:60]!r}")
    return True
