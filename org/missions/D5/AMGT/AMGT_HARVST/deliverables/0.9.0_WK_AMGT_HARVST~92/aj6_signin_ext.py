"""HVST-aj-6 (stage 2 harness; BUILT in stage 1, NOT RUN): ONE unattended ft sign-in whose hCaptcha is solved by the NopeCHA
BROWSER EXTENSION (whitelist VEW-1; Andrew-direct 2026-10-02 ~16:47Z, open-calls option A).

Adapted from aj6_signin.py (the Ocilar attempt): the CRO harvester is imported as a module (never edited) and run through its
own `harvest()`. Three differences:
  1. The browser is launched PERSISTENT on the ft profile (`<runtime>/browser-profiles/ft`), headed, with the prepared NopeCHA
     extension loaded (lib/opal_data_harvest/nopecha_extension.py). Branded Chrome 154 ignores --load-extension and, given
     --disable-extensions-except, blocks the extension (both measured), so the harness drops Playwright's default
     `--disable-extensions` and loads the prepared directory through CDP Extensions.loadUnpacked, served under
     `--enable-unsafe-extension-debugging` (nopecha_extension.cdp_launch_args / load_unpacked). The CRO script calls `chromium.launch(...)` then `browser.new_context(...)`; a
     small shim answers both with `launch_persistent_context`, so its sign-in steps run unchanged.
  2. `solve_hcaptcha_if_present` is replaced by a WAITER: the extension solves the challenge in the page with the account
     key. This harness injects no token and calls no solver API; it only watches for the challenge frame to clear, then
     (if the login page is still showing) presses the page's own sign-in button once, as the Token path did after injection.
  3. NopeCHA's Python Token API is replaced by a stub that RAISES and COUNTS (`nopecha_token_api_calls` must read 0);
     Kimi and the vision fallback are stubbed the same way (`kimi_vision_calls` must read 0).
The NopeCHA key is read at runtime from Secrets by nopecha_extension.prepare() and written only into the prepared manifest under
the runtime cache. It is never printed, logged or recorded here.

DO NOT RUN while another job holds the ft profile (Chrome refuses a second owner of a profile). Stage 2 runs it once, on the
issuer's GO, at most 2 attempts in total.

  python aj6_signin_ext.py <runtime_root> <scratch_dir> <result_json> [--wait-seconds N]
"""
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
WAIT_S = int(sys.argv[sys.argv.index("--wait-seconds") + 1]) if "--wait-seconds" in sys.argv else 150
if "--wait-seconds" in sys.argv:
    args.remove(sys.argv[sys.argv.index("--wait-seconds") + 1])
runtime, scratch, result_path = Path(args[0]), Path(args[1]), Path(args[2])
scratch.mkdir(parents=True, exist_ok=True)
sys.argv = [sys.argv[0]]  # the CRO script reads sys.argv at import: headed, no --park

CRO = Path("org/tier1_exec/4.0.0_SA_CRO/scripts").resolve()
sys.path.insert(0, str(CRO))
import ft_harvest_session as ft  # noqa: E402
import requests  # noqa: E402

from lib.opal_data_harvest import nopecha_extension  # noqa: E402
from lib.opal_data_harvest.input_source import InputSourceMonitor  # noqa: E402
from lib.opal_data_harvest.tab_transport import LAUNCH_ARGS  # noqa: E402

EXT = {"kimi_vision_calls": 0, "nopecha_token_api_calls": 0, "blocked_http": []}
EVENTS = []
ERRORS = []
EXTENSION = {"prepared": False, "id": None, "service_workers": [], "version": nopecha_extension.EXTENSION_VERSION}
BARRED_HOSTS = ("moonshot", "kimi", "nopecha")  # python-side calls only: the extension calls NopeCHA from inside the browser
PROFILE = runtime / "browser-profiles" / "ft"
SIGNIN_SELECTORS = ("#sign-in-button", "button:has-text('Sign in')")


def event(name, **extra):
    EVENTS.append(dict({"event": name, "at": dt.datetime.now(dt.timezone.utc).isoformat()}, **extra))


def kimi_stub(*a, **k):
    EXT["kimi_vision_calls"] += 1
    raise RuntimeError("kimi_vision is BARRED")


class _NopechaBarred:
    class Token:
        @staticmethod
        def solve(*a, **k):
            EXT["nopecha_token_api_calls"] += 1
            raise RuntimeError("the NopeCHA Token API is discontinued and not used in aj-6")


_real_post = requests.post


def guarded_post(url, *a, **k):
    if any(h in str(url) for h in BARRED_HOSTS):
        EXT["blocked_http"].append(str(url)[:60])
        raise RuntimeError("BARRED vendor call: " + str(url)[:60])
    return _real_post(url, *a, **k)


class _Browser:
    """Answers the CRO script's `browser.new_context(...)` / `browser.close()` with a persistent context."""

    def __init__(self, pw, launch_kwargs):
        self._pw, self._kw, self._ctx = pw, launch_kwargs, None

    def new_context(self, **ctx_kwargs):
        prepared = nopecha_extension.prepare(runtime)  # reads the key from Secrets; writes the prepared manifest
        ext_args = nopecha_extension.cdp_launch_args()  # branded Chrome 154: --load-extension is ignored, --disable-extensions-except blocks
        self._prepared = prepared
        EXTENSION["prepared"] = True
        PROFILE.mkdir(parents=True, exist_ok=True)
        base_args = list(LAUNCH_ARGS)
        for a in self._kw.get("args", []):
            if a not in base_args:
                base_args.append(a)
        self._ctx = self._pw.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE), channel="chrome", headless=False, args=base_args + ext_args,
            ignore_default_args=list(nopecha_extension.IGNORE_DEFAULT_ARGS), **ctx_kwargs)
        # Chrome 154 ignores --load-extension (measured); Extensions.loadUnpacked over the browser CDP session loads it.
        EXTENSION["id"] = nopecha_extension.load_unpacked(self._ctx, self._prepared)
        if EXTENSION["id"]:  # wake its service worker now (MV3 starts it lazily) so the record can show it running
            wake = self._ctx.new_page()
            try:
                wake.goto("chrome-extension://%s/manifest.json" % EXTENSION["id"], timeout=10000)
            except Exception as exc:
                ERRORS.append({"stage": "wake_extension", "message": "%s: %s" % (type(exc).__name__, str(exc)[:120])})
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline and not [w for w in self._ctx.service_workers if w.url.startswith("chrome-extension://")]:
                time.sleep(0.5)
            wake.close()
        EXTENSION["service_workers"] = sorted({w.url.split("/")[2][:4] + "..."
                                               for w in self._ctx.service_workers if w.url.startswith("chrome-extension://")})
        ft.log("extension id=%s service workers seen: %d" % (EXTENSION["id"], len(EXTENSION["service_workers"])))
        return self._ctx

    def close(self):
        if self._ctx is not None:
            self._ctx.close()


class _Chromium:
    def __init__(self, pw):
        self._pw = pw

    def launch(self, **kwargs):
        return _Browser(self._pw, kwargs)


class _Playwright:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self._cm = sync_playwright()

    def __enter__(self):
        self._pw = self._cm.__enter__()
        self.chromium = _Chromium(self._pw)
        return self

    def __exit__(self, *exc):
        return self._cm.__exit__(*exc)


def challenge_frame(page):
    return next((f for f in page.frames if "hcaptcha.com" in f.url and re.search(r"challenge|frame", f.url)), None)


def waiter(page):
    """Replaces ft.solve_hcaptcha_if_present. The extension solves; this only observes. True once the frame is gone."""
    if not challenge_frame(page):
        return False
    event("challenge_presented", url=page.url[:80])
    ft.log("hCaptcha presented; waiting up to %ds for the NopeCHA extension to solve it" % WAIT_S)
    deadline = time.monotonic() + WAIT_S
    while time.monotonic() < deadline:
        time.sleep(1.0)
        if not challenge_frame(page):
            event("challenge_passed", waited_s=round(WAIT_S - (deadline - time.monotonic()), 1))
            ft.log("challenge frame gone; the extension solved it")
            time.sleep(2.5)
            if "accounts.ft.com/login" in page.url:  # the page did not move on its own: its own button, once
                for sel in SIGNIN_SELECTORS:
                    btn = page.locator(sel).first
                    if btn.count():
                        try:
                            btn.click(timeout=5000)
                            event("signin_resubmitted", selector=sel)
                        except Exception as exc:
                            ERRORS.append({"stage": "resubmit", "message": "%s: %s" % (type(exc).__name__, str(exc)[:120])})
                        break
                time.sleep(3.0)
            return True
    event("challenge_failed", reason="not_solved_in_%ds" % WAIT_S)
    return False


ft.kimi_vision = kimi_stub
ft.nopecha = _NopechaBarred
ft.solve_hcaptcha_if_present = waiter
ft.sync_playwright = _Playwright
requests.post = guarded_post
ft.S = str(scratch)

started = dt.datetime.now(dt.timezone.utc)
ft.log("AJ6-EXT: one unattended headed sign-in on the ft profile; NopeCHA browser extension (VEW-1); Token API, Kimi, vision barred")
monitor_error = None
try:
    monitor = InputSourceMonitor()
    monitor.__enter__()
except Exception as exc:  # the instrument could not install: no zero-hardware claim may be made
    monitor, monitor_error = None, "%s: %s" % (type(exc).__name__, str(exc)[:150])
rc, harvest_error = 1, None
try:
    rc = ft.harvest()
except Exception as exc:  # a launch failure (profile locked, extension refused) is a RESULT, recorded without a key
    harvest_error = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    ft.log("harvest raised " + harvest_error)
finally:
    if monitor is not None:
        monitor.__exit__(None, None, None)
finished = dt.datetime.now(dt.timezone.utc)

input_record = monitor.record() if monitor is not None else None
if input_record is None:
    hardware_input = "unavailable"
elif input_record["hardware_input_events"] == 0:
    hardware_input = "none"
else:
    hardware_input = "detected:%d" % input_record["hardware_input_events"]

bundle_files = sorted(scratch.glob("ft_session_*.json"))
saved, cookie_names = False, []
if rc == 0 and bundle_files:
    bundle = json.loads(bundle_files[-1].read_text(encoding="utf-8"))
    cookie_names = sorted(bundle)
    net_ok, events = ft.has_network_auth_evidence()
    from lib.opal_data_harvest.storage import SessionVault  # noqa: E402
    envelope = {"publisher": "ft", "bundle": bundle,
                "auth_evidence": {"publisher": "ft", "source": "aj6_signin_ext.py (imports ft_harvest_session)",
                                  "network_auth_corroborated": bool(net_ok), "network_auth_event_count": len(events),
                                  "cloud_park": False, "kimi_vision_calls": EXT["kimi_vision_calls"],
                                  "solver": "nopecha_extension"},
                "network_auth_corroborated": bool(net_ok), "captured_at": finished.isoformat()}
    SessionVault(runtime).save("ft", envelope)
    saved = True
for f in bundle_files:
    f.unlink()  # the raw bundle carries cookie values: never kept

passed = any(e["event"] == "challenge_passed" for e in EVENTS)
presented = any(e["event"] == "challenge_presented" for e in EVENTS)
solved_by = ("nopecha_extension" if (presented and passed) else
             "nopecha_extension_failed" if presented else
             "none_no_challenge_presented")
out = {"started_at": started.isoformat(), "finished_at": finished.isoformat(), "harvest_rc": rc, "harvest_error": harvest_error,
       "challenge_events": EVENTS, "solved_by": solved_by, "whitelist": nopecha_extension.WHITELIST,
       "extension": dict(EXTENSION, source_url=nopecha_extension.EXTENSION_ZIP_URL, sha256=nopecha_extension.EXTENSION_ZIP_SHA256),
       "errors": ERRORS, "nopecha_token_api_calls": EXT["nopecha_token_api_calls"],
       "kimi_vision_calls": EXT["kimi_vision_calls"], "blocked_http": EXT["blocked_http"], "hardware_input": hardware_input,
       "input_source": input_record, "input_source_error": monitor_error,
       "identity_cookie_names": [n for n in cookie_names if n in ft.IDENTITY_COOKIES],
       "bundle_cookie_count": len(cookie_names), "saved_to_vault": saved,
       "network_auth_events": len(ft.NETWORK_AUTH_EVENTS)}
result_path.write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out), flush=True)
sys.exit(0 if saved else 1)
