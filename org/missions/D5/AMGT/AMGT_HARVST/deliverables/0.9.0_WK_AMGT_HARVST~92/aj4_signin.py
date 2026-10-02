"""HVST-aj-4 step 2: ONE UNATTENDED ft sign-in through the CRO harvester imported as a module.

Authorization: Andrew-direct 2026-10-02 ~13:08Z "nopeCHA is permanently whitelisted for egress"
(org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261002_130xZ_VENDOR_EGRESS_WHITELIST_NOPECHA_PERMANENT.md).
NopeCHA ONLY. Kimi and the vision fallback stay BARRED.

Difference from ai2_signin_attempt3.py: the hCaptcha solver is the CRO script's own solve_hcaptcha_if_present (NopeCHA
Token API, key read through the script's _secret path), wrapped only to COUNT calls and record the outcome; no human wait.
  - kimi_vision is replaced with a stub that RAISES, and requests.post to moonshot raises too (kimi_vision_calls stays 0);
  - the script's `S` (raw cookie bundle dir) is pointed at a scratch dir; the bundle is saved into the collector's vault
    (the envelope attempt 3 wrote) and the raw file is deleted; no --park (no Secrets write); nothing secret is printed.

  python aj4_signin.py <runtime_root> <scratch_dir> <result_json>
"""
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, ".")
runtime, scratch, result_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
scratch.mkdir(parents=True, exist_ok=True)
sys.argv = [sys.argv[0]]  # the CRO script reads sys.argv at import: headed, no --park

CRO = Path("org/tier1_exec/4.0.0_SA_CRO/scripts").resolve()
sys.path.insert(0, str(CRO))
import ft_harvest_session as ft  # noqa: E402
import nopecha as real_nopecha  # noqa: E402
import requests  # noqa: E402

EXT = {"kimi_vision_calls": 0, "nopecha_calls": 0, "nopecha_errors": [], "blocked_http": []}
CH = {"challenge_seen": False, "solver_returned": None}


def kimi_stub(*a, **k):
    EXT["kimi_vision_calls"] += 1
    raise RuntimeError("kimi_vision is BARRED")


_real_post = requests.post


def guarded_post(url, *a, **k):
    if any(h in str(url) for h in ("moonshot", "kimi")):
        EXT["blocked_http"].append(str(url)[:60])
        raise RuntimeError("Kimi/vision call BARRED: " + str(url)[:60])
    return _real_post(url, *a, **k)


class _Token:
    @staticmethod
    def solve(*a, **k):
        EXT["nopecha_calls"] += 1
        try:
            return real_nopecha.Token.solve(*a, **k)
        except Exception as exc:  # the CRO script catches and logs; record the exact error here too
            EXT["nopecha_errors"].append("%s: %s" % (type(exc).__name__, str(exc)[:200]))
            raise


class _NopechaProxy:
    Token = _Token


_orig_solve = ft.solve_hcaptcha_if_present


def solver(page):
    CH["challenge_seen"] = CH["challenge_seen"] or any(
        "hcaptcha.com" in f.url for f in page.frames)
    result = _orig_solve(page)
    CH["solver_returned"] = bool(result)
    return result


ft.kimi_vision = kimi_stub
ft.nopecha = _NopechaProxy
ft.solve_hcaptcha_if_present = solver
requests.post = guarded_post
ft.S = str(scratch)

started = dt.datetime.now(dt.timezone.utc)
ft.log("AJ4: one unattended headed sign-in; NopeCHA enabled, Kimi/vision barred")
rc = ft.harvest()
finished = dt.datetime.now(dt.timezone.utc)

bundle_files = sorted(scratch.glob("ft_session_*.json"))
saved, cookie_names = False, []
if rc == 0 and bundle_files:
    bundle = json.loads(bundle_files[-1].read_text(encoding="utf-8"))
    cookie_names = sorted(bundle)
    net_ok, events = ft.has_network_auth_evidence()
    from lib.opal_data_harvest.storage import SessionVault  # noqa: E402
    envelope = {"publisher": "ft", "bundle": bundle,
                "auth_evidence": {"publisher": "ft", "source": "aj4_signin.py (imports ft_harvest_session)",
                                  "network_auth_corroborated": bool(net_ok), "network_auth_event_count": len(events),
                                  "cloud_park": False, "kimi_vision_calls": EXT["kimi_vision_calls"],
                                  "solver": "nopecha"},
                "network_auth_corroborated": bool(net_ok), "captured_at": finished.isoformat()}
    SessionVault(runtime).save("ft", envelope)
    saved = True
for f in bundle_files:
    f.unlink()  # the raw bundle carries cookie values: never kept

solved_by = ("nopecha" if EXT["nopecha_calls"] and CH["solver_returned"] else
             "nopecha_failed" if EXT["nopecha_calls"] else "none_no_challenge_solved" if not CH["challenge_seen"] else "unsolved")
out = {"started_at": started.isoformat(), "finished_at": finished.isoformat(), "harvest_rc": rc,
       "identity_cookie_names": [n for n in cookie_names if n in ft.IDENTITY_COOKIES],
       "bundle_cookie_count": len(cookie_names), "saved_to_vault": saved,
       "nopecha_calls": EXT["nopecha_calls"], "nopecha_errors": EXT["nopecha_errors"],
       "kimi_vision_calls": EXT["kimi_vision_calls"], "blocked_http": EXT["blocked_http"],
       "challenge_seen": CH["challenge_seen"], "solver_returned": CH["solver_returned"],
       "solved_by": solved_by, "hardware_input": "none",
       "network_auth_events": len(ft.NETWORK_AUTH_EVENTS)}
result_path.write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out), flush=True)
sys.exit(0 if saved else 1)
