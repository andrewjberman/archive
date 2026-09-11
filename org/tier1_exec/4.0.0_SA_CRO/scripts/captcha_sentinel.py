#!/usr/bin/env python3
"""Captcha Sentinel -- a shared, event-driven perceive-classify-dispatch engine for beating
adaptive anti-bot defenses during a login flow. Built for AMGT_RESAPP's FT and Seeking Alpha
harvesters (ft_harvest_session.py, sa_harvest_session.py) to import and register handlers into,
so both sites drive ONE detection/classification engine instead of duplicating ad hoc logic.

WHY THIS EXISTS (measured live, 2026-09-10): a script that only checks "what screen am I on" at
its own fixed steps (after clicking Sign in, after 8s, ...) is blind to anything that happens
between those checks, and blind to anything that opens in a SEPARATE WINDOW rather than the main
page -- both measured true today. Seeking Alpha's defense is ADAPTIVE, not a single static
challenge: the same account, hammered with enough attempts in a short window, escalated from a
press-and-hold wall to a forced Google OAuth popup outside the main frame entirely. No captcha
library "solves" an OAuth redirect -- that is a different problem, and the honest answer is to
recognize it and stop, not to keep guessing.

THE PIPELINE:
  1. DETECT  -- fast, cheap, layered:
       (a) an injected MutationObserver on every page (including future popups) that PUSHES the
           instant the DOM changes materially -- no polling delay for the common case;
       (b) native Playwright events: a new page/popup opening, a navigation, an interesting
           network response;
       (c) a 1s poll of a content-length fingerprint per open page as a SAFETY NET, catching
           anything (a) and (b) missed (e.g. a popup whose init script had no chance to attach
           before the challenge rendered).
  2. CAPTURE -- on ANY detected change, an OS-level FULL-SCREEN screenshot, immediately, always --
     never a single Playwright page.screenshot(), because the challenge can be a separate window
     the "current" page object never sees. Uses mss (fast); falls back to PIL.ImageGrab.
  3. CLASSIFY -- a background worker feeds every screenshot to Kimi vision continuously (Kimi is
     "online" from the start of the flow, not invoked only at fixed checkpoints), against a small
     CLOSED set of named states -- classification only, never asked to also solve the challenge in
     the same call (a harder, less reliable ask that is exactly where the old per-site scripts kept
     failing).
  4. DISPATCH -- the caller registers one handler per state. This module does not assume any
     particular solver is correct for a given site; it hands the recognized state to whatever the
     caller wired up (a loaded NopeCHA extension is often already handling press-and-hold/hCaptcha
     passively before dispatch even fires -- the oracle for "did it work" is always the caller's own
     success cookie check, never a vision or extension self-report). STATE_NO_AUTOMATED_HANDLER
     (e.g. GOOGLE_OAUTH_POPUP) has no built-in solver by design -- escalate to a human, never guess.

ROE (inherited unchanged from the estate's harvesters): observe-act-only; a credential, cookie or
session VALUE is never logged; screenshots taken here may show visible page content but are never
persisted with a form field's typed value exposed beyond what the page itself renders (a password
field's browser-native masking is the only protection assumed, matching bd_49f_auto_login.js's own
screenshot ROE -- callers masking password fields before triggering a sentinel-adjacent screenshot
is the caller's responsibility for its own known steps).

STATES (the closed set -- extend deliberately, never silently):
  ANON, LOGIN_FORM, PRESS_HOLD_WALL, HCAPTCHA_CHALLENGE, IMAGE_SELECT_CHALLENGE,
  GOOGLE_OAUTH_POPUP, LOGGED_IN, UNKNOWN

Usage (as a library -- see sa_harvest_session.py / ft_harvest_session.py for real registration):
    from captcha_sentinel import Sentinel, STATE_NO_AUTOMATED_HANDLER
    sentinel = Sentinel(kimi_key_getter=lambda: my_kimi_key)
    sentinel.on("PRESS_HOLD_WALL", my_press_and_hold_fallback)
    sentinel.on("HCAPTCHA_CHALLENGE", my_kimi_tile_fallback)
    sentinel.on(STATE_NO_AUTOMATED_HANDLER, my_human_escalation)  # GOOGLE_OAUTH_POPUP et al.
    sentinel.start(context)          # wires every current + future page in the context
    ... drive the login flow ...
    sentinel.stop()
"""
from __future__ import annotations

import base64
import io
import queue
import threading
import time

import requests

try:
    import mss
    _HAVE_MSS = True
except ImportError:
    _HAVE_MSS = False
    from PIL import ImageGrab

KIMI_URL = "https://api.moonshot.ai/v1/chat/completions"
# MEASURED 2026-09-10: kimi-k2.6 spent up to 2,663 hidden reasoning tokens (59-150+s, sometimes
# timing out) on a task kimi-k3 solved in 10-12s using ~180 reasoning tokens -- same accuracy
# (both landed on the same pixel), ~8x faster. Switched estate-wide from this file forward;
# sa_harvest_session.py / ft_harvest_session.py / harvest_ft_session.js still call k2.6 and are a
# follow-up, not done in the same pass as this fix.
KIMI_MODEL = "kimi-k3"

# The closed state set. GOOGLE_OAUTH_POPUP and any future "we recognize this but have no business
# automating it" state route through STATE_NO_AUTOMATED_HANDLER's fallback rather than a captcha
# solver -- an OAuth login is an identity assertion, not a puzzle, and no captcha library applies.
STATES = (
    "ANON", "LOGIN_FORM", "PRESS_HOLD_WALL", "HCAPTCHA_CHALLENGE",
    "IMAGE_SELECT_CHALLENGE", "GOOGLE_OAUTH_POPUP", "LOGGED_IN", "UNKNOWN",
)
STATE_NO_AUTOMATED_HANDLER = "GOOGLE_OAUTH_POPUP"  # extend this tuple, not this module's logic, for new no-solver states
NO_SOLVER_STATES = {"GOOGLE_OAUTH_POPUP"}

CLASSIFY_PROMPT = (
    "You are watching a login flow for a signal-detection system, screenshotted the instant something "
    "changed on screen. This is a FULL SCREEN capture -- the relevant content may be in a popup window, "
    "not the main browser tab. Classify the CURRENT screen as EXACTLY ONE of these tokens:\n"
    "- ANON: an anonymous, logged-out page with no login form and no challenge visible.\n"
    "- LOGIN_FORM: an email/password sign-in form is visible and awaiting input.\n"
    "- PRESS_HOLD_WALL: an anti-bot interstitial with a 'Press & Hold' button, a human-verification "
    "prompt with a hold-to-confirm button, or a PerimeterX/HUMAN-style challenge.\n"
    "- HCAPTCHA_CHALLENGE: an hCaptcha image-tile grid challenge ('Please click each image containing...').\n"
    "- IMAGE_SELECT_CHALLENGE: any OTHER image-selection captcha (not hCaptcha's tile grid specifically).\n"
    "- GOOGLE_OAUTH_POPUP: a Google 'Sign in with Google' account-chooser or Google login page, in the "
    "main window or a separate popup.\n"
    "- LOGGED_IN: the destination site's own signed-in content (a dashboard, account page, or the "
    "original page now showing a signed-in header/avatar), no login form and no challenge.\n"
    "- UNKNOWN: none of the above confidently applies.\n"
    "Reply with ONLY the one token, nothing else."
)


def log(m):
    print(f"[sentinel {time.strftime('%H:%M:%S')}] {m}", flush=True)


def capture_full_screen() -> bytes:
    """OS-level full-screen capture -- ALWAYS the whole screen, never a single Playwright page.
    A popup/separate window is invisible to page.screenshot() but always on the physical screen."""
    if _HAVE_MSS:
        with mss.mss() as sct:
            mon = sct.monitors[0]  # index 0 = the union of all monitors (the true "full screen")
            shot = sct.grab(mon)
            return mss.tools.to_png(shot.rgb, shot.size)
    else:
        img = ImageGrab.grab(all_screens=True)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()


class Sentinel:
    def __init__(self, kimi_key_getter, poll_seconds=1.0, max_tokens=400, consecutive_unknown_cap=5):
        # 400 on kimi-k3 (measured: a comparable single-token-answer vision call used ~180
        # reasoning tokens end to end) -- this budget would have been dangerously tight on k2.6.
        self._kimi_key_getter = kimi_key_getter
        self.poll_seconds = poll_seconds
        self.max_tokens = max_tokens
        self.consecutive_unknown_cap = consecutive_unknown_cap
        self._handlers = {}
        self._events = queue.Queue()
        self._stop = threading.Event()
        self._threads = []
        self._context = None
        self._fingerprints = {}  # page -> last content-length fingerprint (the poll safety net)
        self._consecutive_unknown = 0
        self.last_state = None
        self.state_history = []  # [(ts, state, source)]
        self._lock = threading.Lock()

    def on(self, state, handler):
        """Register a handler(sentinel, state, screenshot_bytes) for one state. A state with no
        registered handler and no built-in solver just logs and does nothing further that tick --
        the caller's own success-cookie polling loop is what actually decides when to stop."""
        assert state in STATES, f"unknown state {state!r} -- extend the closed set deliberately"
        self._handlers[state] = handler

    def _kimi_vision(self, png_bytes, prompt, max_tokens):
        body = {
            "model": KIMI_MODEL, "temperature": 1, "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(png_bytes).decode()}},
                {"type": "text", "text": prompt},
            ]}],
        }
        key = self._kimi_key_getter()
        r = requests.post(KIMI_URL, json=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"}, timeout=90)
        r.raise_for_status()
        return (r.json()["choices"][0]["message"]["content"] or "").strip()

    def _classify(self, png_bytes):
        for attempt in range(2):
            try:
                raw = self._kimi_vision(png_bytes, CLASSIFY_PROMPT, self.max_tokens)
                up = raw.upper()
                for s in STATES:
                    if s in up:
                        return s
                log(f"classify: UNPARSED reply {raw[:60]!r} (try {attempt + 1}/2)")
            except Exception as e:
                log(f"classify: KIMI_ERROR {type(e).__name__} {str(e)[:100]} (try {attempt + 1}/2)")
        return "UNKNOWN"

    def _on_event(self, source):
        """Fires on ANY detected change: capture full-screen NOW, queue for classification."""
        try:
            png = capture_full_screen()
        except Exception as e:
            log(f"screenshot FAILED on event from {source!r}: {type(e).__name__} {str(e)[:100]}")
            return
        self._events.put((time.time(), source, png))

    def _classify_worker(self):
        while not self._stop.is_set():
            try:
                ts, source, png = self._events.get(timeout=0.5)
            except queue.Empty:
                continue
            state = self._classify(png)
            with self._lock:
                self.last_state = state
                self.state_history.append((ts, state, source))
                self._consecutive_unknown = self._consecutive_unknown + 1 if state == "UNKNOWN" else 0
            log(f"CLASSIFIED {state} (source={source}, queue_depth={self._events.qsize()})")
            if self._consecutive_unknown >= self.consecutive_unknown_cap:
                log(f"WARN: {self._consecutive_unknown} consecutive UNKNOWN -- vision may be degraded or the state is genuinely novel")
            handler = self._handlers.get(state)
            if state in NO_SOLVER_STATES and STATE_NO_AUTOMATED_HANDLER in self._handlers:
                handler = self._handlers[STATE_NO_AUTOMATED_HANDLER]
            if handler:
                try:
                    handler(self, state, png)
                except Exception as e:
                    log(f"handler for {state} raised {type(e).__name__}: {str(e)[:150]}")

    def _poll_worker(self):
        """SAFETY NET: a 1s fingerprint poll per open page, independent of the MutationObserver and
        Playwright events -- catches anything they miss (e.g. a popup whose init script never got
        the chance to attach before its content rendered)."""
        while not self._stop.is_set():
            time.sleep(self.poll_seconds)
            if self._context is None:
                continue
            for pg in list(self._context.pages):
                try:
                    fp = pg.evaluate("document.body ? document.body.innerHTML.length : 0")
                except Exception:
                    continue
                prev = self._fingerprints.get(pg)
                if prev != fp:
                    self._fingerprints[pg] = fp
                    if prev is not None:  # skip the very first read (nothing to compare against)
                        self._on_event(f"poll:{pg.url[:60]}")

    def _wire_page(self, pg):
        try:
            pg.add_init_script(
                """
                (() => {
                  if (window.__sentinelWired__) return; window.__sentinelWired__ = true;
                  const notify = () => { if (window.__sentinelNotify__) window.__sentinelNotify__(); };
                  const obs = new MutationObserver(() => notify());
                  const attach = () => { if (document.body) obs.observe(document.body, {childList:true, subtree:true, attributes:true}); };
                  if (document.body) attach(); else document.addEventListener('DOMContentLoaded', attach);
                })();
                """
            )
            pg.expose_function("__sentinelNotify__", lambda: self._on_event(f"mutation:{pg.url[:60]}"))
        except Exception as e:
            log(f"wiring page failed (non-fatal, the 1s poll still covers it): {type(e).__name__}")
        pg.on("framenavigated", lambda f: self._on_event(f"navigation:{f.url[:60]}") if f == pg.main_frame else None)

    def start(self, context):
        self._context = context
        for pg in context.pages:
            self._wire_page(pg)
        context.on("page", lambda pg: (log(f"NEW PAGE/POPUP: {pg.url!r}"), self._wire_page(pg), self._on_event(f"newpage:{pg.url[:60]}")))
        t1 = threading.Thread(target=self._classify_worker, daemon=True)
        t2 = threading.Thread(target=self._poll_worker, daemon=True)
        t1.start()
        t2.start()
        self._threads = [t1, t2]
        log(f"started: mss={_HAVE_MSS} poll_seconds={self.poll_seconds}")

    def stop(self):
        self._stop.set()
        for t in self._threads:
            t.join(timeout=3)
        log(f"stopped: {len(self.state_history)} classifications total")

    def wait_for(self, target_states, timeout_s=120):
        """Block until last_state is one of target_states, or timeout. Returns the state (or None
        on timeout). Does NOT itself decide success -- the caller's own cookie check is the oracle;
        this only tells the caller when the sentinel has SEEN something worth checking for."""
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            with self._lock:
                if self.last_state in target_states:
                    return self.last_state
            time.sleep(0.3)
        return None
