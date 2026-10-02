"""HVST-aj-6: ONE UNATTENDED ft sign-in whose hCaptcha is solved by the Ocilar API (whitelist VEW-4).

Authorization: Andrew-direct 2026-10-02 ~13:3xZ "LETS USE A NEW SOLVER"
(org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261002_133xZ_USE_OCILAR_HCAPTCHA_SOLVER.md); row VEW-4 in
org/ref/VENDOR_EGRESS_WHITELIST.yaml. NopeCHA (Token API and extension), Kimi and vision get ZERO calls.

Adapted from aj4_signin.py: the CRO harvester is imported as a module (not edited) and its
`solve_hcaptcha_if_present` is replaced by one that goes through lib/opal_data_harvest/ocilar_hcaptcha.py:
sitekey -> Ocilar solve -> inject -> submit; a token the page does not accept is retried ONCE (at most 2 Ocilar calls;
an Ocilar HTTP failure is NOT retried: it is recorded and the sign-in stops at that point).
The Ocilar key is read at runtime from Secrets and never printed, logged or written.

  python aj6_signin.py <runtime_root> <scratch_dir> <result_json>
"""
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")
runtime, scratch, result_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
scratch.mkdir(parents=True, exist_ok=True)
sys.argv = [sys.argv[0]]  # the CRO script reads sys.argv at import: headed, no --park

CRO = Path("org/tier1_exec/4.0.0_SA_CRO/scripts").resolve()
sys.path.insert(0, str(CRO))
import ft_harvest_session as ft  # noqa: E402
import requests  # noqa: E402

from lib.opal_data_harvest import ocilar_hcaptcha as oc  # noqa: E402
from lib.opal_data_harvest.input_source import InputSourceMonitor  # noqa: E402

EXT = {"kimi_vision_calls": 0, "nopecha_token_api_calls": 0, "blocked_http": []}
EVENTS = []
ERRORS = []
INJECTIONS = []
BARRED_HOSTS = ("moonshot", "kimi", "nopecha")


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
            raise RuntimeError("NopeCHA is not used in aj-6")


_real_post = requests.post


def guarded_post(url, *a, **k):
    if any(h in str(url) for h in BARRED_HOSTS):
        EXT["blocked_http"].append(str(url)[:60])
        raise RuntimeError("BARRED vendor call: " + str(url)[:60])
    return _real_post(url, *a, **k)


def challenge_frame(page):
    return next((f for f in page.frames if "hcaptcha.com" in f.url and re.search(r"challenge|frame", f.url)), None)


def solver(page):
    """Replaces ft.solve_hcaptcha_if_present. True once the challenge frame is gone."""
    if not challenge_frame(page):
        return False
    event("challenge_presented", url=page.url[:80])
    sitekey = oc.extract_sitekey(page)
    if not sitekey:
        ft.log("hCaptcha present but no sitekey could be extracted")
        ERRORS.append({"stage": "sitekey", "message": "no sitekey"})
        event("challenge_failed", reason="no_sitekey")
        return False
    try:
        key = oc.read_key()
    except oc.OcilarError as exc:
        ERRORS.append({"stage": "read_key", "status": exc.status, "message": str(exc)[:200]})
        event("challenge_failed", reason="read_key")
        return False
    for attempt in (1, 2):
        ft.log("hCaptcha: Ocilar solve attempt %d (sitekey found, url=%r)" % (attempt, page.url[:70]))
        try:
            token = oc.solve(sitekey, page.url, key)
        except oc.OcilarError as exc:
            ERRORS.append({"stage": "solve", "attempt": attempt, "status": exc.status, "message": str(exc)[:200]})
            ft.log("Ocilar solve failed: status=%s %s" % (exc.status, str(exc)[:150]))
            event("challenge_failed", reason="ocilar_error", status=exc.status)
            return False
        ft.log("Ocilar returned a token (length=%d); injecting" % len(token))
        try:
            INJECTIONS.append(oc.inject_and_submit(page, token, ("#sign-in-button", "button:has-text('Sign in')")))
        except Exception as exc:
            ERRORS.append({"stage": "inject", "attempt": attempt, "message": "%s: %s" % (type(exc).__name__, str(exc)[:150])})
            event("challenge_failed", reason="inject_error")
            return False
        time.sleep(2.5)
        if not challenge_frame(page):
            event("challenge_passed", attempt=attempt)
            return True
        ft.log("challenge frame still present after the token was injected (attempt %d)" % attempt)
    event("challenge_failed", reason="token_rejected_twice")
    return False


ft.kimi_vision = kimi_stub
ft.nopecha = _NopechaBarred
ft.solve_hcaptcha_if_present = solver
requests.post = guarded_post
ft.S = str(scratch)

started = dt.datetime.now(dt.timezone.utc)
ft.log("AJ6: one unattended headed sign-in; Ocilar solver (VEW-4); NopeCHA, Kimi, vision barred")
monitor_error = None
try:
    monitor = InputSourceMonitor()
    monitor.__enter__()
except Exception as exc:  # the instrument could not install: no zero-hardware claim may be made
    monitor, monitor_error = None, "%s: %s" % (type(exc).__name__, str(exc)[:150])
try:
    rc = ft.harvest()
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
                "auth_evidence": {"publisher": "ft", "source": "aj6_signin.py (imports ft_harvest_session)",
                                  "network_auth_corroborated": bool(net_ok), "network_auth_event_count": len(events),
                                  "cloud_park": False, "kimi_vision_calls": EXT["kimi_vision_calls"],
                                  "solver": "ocilar"},
                "network_auth_corroborated": bool(net_ok), "captured_at": finished.isoformat()}
    SessionVault(runtime).save("ft", envelope)
    saved = True
for f in bundle_files:
    f.unlink()  # the raw bundle carries cookie values: never kept

st = oc.stats()
passed = any(e["event"] == "challenge_passed" for e in EVENTS)
solved_by = "ocilar" if (st["calls"] and passed) else ("ocilar_failed" if st["calls"] else
                                                       "none_no_challenge_presented" if not EVENTS else "unsolved")
out = {"started_at": started.isoformat(), "finished_at": finished.isoformat(), "harvest_rc": rc,
       "challenge_events": EVENTS, "solved_by": solved_by, "whitelist": "VEW-4",
       "ocilar_calls": st["calls"], "ocilar_ok": st["ok"], "ocilar_latency_ms": st["latency_ms"],
       "ocilar_errors": st["errors"] + ERRORS, "injections": INJECTIONS,
       "nopecha_token_api_calls": EXT["nopecha_token_api_calls"], "kimi_vision_calls": EXT["kimi_vision_calls"],
       "blocked_http": EXT["blocked_http"], "hardware_input": hardware_input,
       "input_source": input_record, "input_source_error": monitor_error,
       "identity_cookie_names": [n for n in cookie_names if n in ft.IDENTITY_COOKIES],
       "bundle_cookie_count": len(cookie_names), "saved_to_vault": saved,
       "network_auth_events": len(ft.NETWORK_AUTH_EVENTS)}
result_path.write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out), flush=True)
sys.exit(0 if saved else 1)
