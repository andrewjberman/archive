"""HVST-ai-2 attempt 3: ONE headed ft sign-in through the CRO harvester imported as a module, with BOTH external vendor
calls barred (Andrew-direct 02:2xZ: Kimi vision and NopeCHA are not authorised; a human solves any hCaptcha in the visible
window). The CRO script is not edited.

  - kimi_vision is replaced with a stub that RAISES (and requests.post to api.moonshot.ai / nopecha.com raises too, so a
    call by any other name is also stopped);
  - solve_hcaptcha_if_present is replaced with a wait of up to 900 s for a human to clear the challenge in the window;
  - the script's `S` (where it writes the raw cookie bundle) is pointed at a scratch dir; the bundle is saved into the
    collector's vault (the same envelope auth.SessionManager._refresh writes) and the raw file is then deleted;
  - no --park (no Secrets write); credentials are read by the script's own _secret path and never printed.

  python aj4_signin_hand.py <runtime_root> <scratch_dir> <result_json>
"""
import datetime as dt
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, ".")
runtime, scratch, result_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
scratch.mkdir(parents=True, exist_ok=True)
sys.argv = [sys.argv[0]]  # the CRO script reads sys.argv at import: no --headless (headed), no --park

CRO = Path("org/tier1_exec/4.0.0_SA_CRO/scripts").resolve()
sys.path.insert(0, str(CRO))
import ft_harvest_session as ft  # noqa: E402
import requests  # noqa: E402

EXTERNAL = {"kimi_vision_calls": 0, "nopecha_solver_calls": 0, "blocked_http": []}
HUMAN = {"challenge_seen": False, "solved_by_hand": None, "waited_s": 0}


def kimi_stub(*a, **k):
    EXTERNAL["kimi_vision_calls"] += 1
    raise RuntimeError("kimi_vision is BARRED (no vendor word from Andrew)")


_real_post = requests.post


def guarded_post(url, *a, **k):
    if any(h in str(url) for h in ("moonshot", "kimi", "nopecha", "ocilar", "oscilar")):
        EXTERNAL["blocked_http"].append(str(url)[:60])
        raise RuntimeError("external vendor call BARRED: " + str(url)[:60])
    return _real_post(url, *a, **k)


def _challenge_frames(page):
    return [f for f in page.frames if "hcaptcha.com" in f.url and "frame=challenge" in f.url]


def human_solver(page):
    """Replaces solve_hcaptcha_if_present: waits up to 15 min for a human; True once the challenge is gone."""
    frames = [f for f in page.frames if "hcaptcha.com" in f.url and ("frame=challenge" in f.url or "frame=checkbox" in f.url)]
    visible = False
    for _ in range(4):  # the challenge can mount a moment after the submit
        if _challenge_frames(page) or frames:
            visible = True
            break
        time.sleep(1.5)
        frames = [f for f in page.frames if "hcaptcha.com" in f.url and "frame=checkbox" in f.url]
    if not visible:
        ft.log("no hCaptcha frame present after the sign-in submit")
        return False
    HUMAN["challenge_seen"] = True
    ft.log("hCaptcha PRESENT -- waiting up to 900 s for a HUMAN to solve it in the visible window (no solver is called)")
    t0 = time.time()
    while time.time() - t0 < 900:
        names = {c["name"] for c in page.context.cookies()}
        if any(n in names for n in ft.IDENTITY_COOKIES):
            HUMAN.update(solved_by_hand=True, waited_s=round(time.time() - t0))
            ft.log("identity cookie appeared -- challenge solved by hand")
            return True
        if not _challenge_frames(page) and "accounts.ft.com/login" not in page.url:
            HUMAN.update(solved_by_hand=True, waited_s=round(time.time() - t0))
            ft.log("challenge cleared and the page moved on -- challenge solved by hand")
            return True
        time.sleep(2)
    HUMAN.update(solved_by_hand=False, waited_s=900)
    ft.log("15 minutes elapsed with the challenge unsolved")
    return False


ft.kimi_vision = kimi_stub
ft.solve_hcaptcha_if_present = human_solver  # nopecha is only reachable through the original solver, now replaced
requests.post = guarded_post
ft.S = str(scratch)  # the raw bundle goes to scratch, never into the CRO scripts dir

started = dt.datetime.now(dt.timezone.utc)
ft.log("AJ4: one headed sign-in, Andrew solves by hand; all vendor solvers barred")
rc = ft.harvest()
finished = dt.datetime.now(dt.timezone.utc)

bundle_files = sorted(scratch.glob("ft_session_*.json"))
saved = False
cookie_names = []
if rc == 0 and bundle_files:
    bundle = json.loads(bundle_files[-1].read_text(encoding="utf-8"))
    cookie_names = sorted(bundle)
    net_ok, events = ft.has_network_auth_evidence()
    from lib.opal_data_harvest.storage import SessionVault  # noqa: E402
    envelope = {"publisher": "ft", "bundle": bundle,
                "auth_evidence": {"publisher": "ft", "source": "aj4_signin_hand.py (imports ft_harvest_session)",
                                  "network_auth_corroborated": bool(net_ok), "network_auth_event_count": len(events),
                                  "cloud_park": False, "kimi_vision_calls": EXTERNAL["kimi_vision_calls"],
                                  "solver": "andrew_hand"},
                "network_auth_corroborated": bool(net_ok), "captured_at": finished.isoformat()}
    SessionVault(runtime).save("ft", envelope)
    saved = True
for f in bundle_files:
    f.unlink()  # the raw bundle carries cookie values: never kept

out = {"started_at": started.isoformat(), "finished_at": finished.isoformat(), "harvest_rc": rc,
       "identity_cookie_names": [n for n in cookie_names if n in ft.IDENTITY_COOKIES],
       "bundle_cookie_count": len(cookie_names), "saved_to_vault": saved,
       "solved_by": "andrew_hand" if HUMAN["solved_by_hand"] else ("no_challenge_seen" if not HUMAN["challenge_seen"] else "unsolved"),
       "challenge_seen": HUMAN["challenge_seen"], "human_waited_s": HUMAN["waited_s"],
       "nopecha_calls": EXTERNAL["nopecha_solver_calls"], "kimi_vision_calls": EXTERNAL["kimi_vision_calls"],
       "ocilar_calls": 0, "vision_calls": 0, "blocked_http": EXTERNAL["blocked_http"],
       "hardware_input_note": "Andrew's hand on the hCaptcha is expected and is human-hand, not limb-2 evidence",
       "network_auth_events": len(ft.NETWORK_AUTH_EVENTS)}
result_path.write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out), flush=True)
sys.exit(0 if saved else 1)
