"""HVST-ac-2 (0.9.0_WK_AMGT_HARVST~85): the Seeking Alpha probe, OUTSIDE the Worker, under the signed never-widen pair.

COO half @0ee2667f36, CTO half @e5171bf838 (two conditions):
  (1) no sign-in is reachable: TokenFirstSessions gets a REFUSING signin and a REFUSING refresh (both counted);
      a missing stored sa token is Branch B ("no stored sa token"), recorded, nothing signed in;
  (2) at most 3 requests, counted in code: the inner HTTP session is wrapped so a 4th request raises BEFORE it is
      sent; the retry policy is set to ONE attempt per request (no 429/401 re-try, so a request is one send);
      `Publisher.seeking_alpha` is never called (it fetches one article per hit) -- the sa module's `check` and
      `news` are called DIRECTLY.

Request 1: the account read alone. Request 2: only on an authorized account read, ONE news page for Lenovo (LNVGY,
from the collector's RESOLVED universe). The second account pre-check the CTO half counts toward the 3-cap is not
made (the lead's order names two calls; the cap stays 3). NO S3 write, NO run record, NO upload.

`--dry` goes as far as the stored token, the security and the session build, and makes NO vendor request.
"""
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip())
COMMON = Path(subprocess.run(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True, check=True).stdout.strip())
MAIN_TREE = (COMMON if COMMON.is_absolute() else ROOT / COMMON).resolve().parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from lib.opal_data_harvest import publishers, transport  # noqa: E402
from lib.opal_data_harvest.__main__ import universe  # noqa: E402
from lib.opal_data_harvest.auth import SessionManager  # noqa: E402
from lib.opal_data_harvest.sessions import TokenFirstSessions  # noqa: E402

WK = ROOT / "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~85"
OUT = WK / "ac2_probe.json"
FLOOR = dt.date(2026, 1, 1)
CAP = 3
ONE_ATTEMPT = {"max_attempts": 1, "auth_confirm_retries": 0}
DRY = "--dry" in sys.argv

events = []
counters = {"sign_in_calls": 0, "refresh_calls": 0, "requests": 0, "request_paths": []}


def record(event):
    events.append(event)


class StopProbe(RuntimeError):
    pass


def refusing_signin(publisher, credentials):
    counters["sign_in_calls"] += 1
    raise StopProbe("sign-in refused by the probe (no sign-in path is allowed)")


class CappedInner:
    """Wraps the curl_cffi session: a request past the cap raises BEFORE it is sent."""

    def __init__(self, inner):
        self._inner = inner

    def get(self, url, **kwargs):
        if counters["requests"] >= CAP:
            raise StopProbe("request cap %d reached; the next request is refused before it is sent" % CAP)
        counters["requests"] += 1
        counters["request_paths"].append(publishers.urlparse(url).path)
        return self._inner.get(url, **kwargs)

    def __getattr__(self, name):
        return getattr(self._inner, name)


def classify(exc, session, before):
    """(status, class, body) of a stopped request. The bot_check classifier of lib/opal_data_harvest/bot_check.py is
    not in the pinned code (row Z-W85-S1), so the transport's own challenge markers and attempt class decide."""
    captured = session.captured[before:]
    last = captured[-1] if captured else None
    status = last["status"] if last else getattr(exc, "status", None)
    body = last["body"] if last else None
    name = type(exc).__name__
    text = (body or b"").decode("utf-8", "replace").lower()
    challenge = any(m in text for m in ("captcha-delivery.com", "blockscript", "px-captcha", "press &amp; hold"))
    if name == "StopProbe":
        klass = "stopped_before_send"
    elif name == "ReHarvestRequired" or challenge or name == "VerificationRequired":
        klass = "bot_check"
    elif status == 402 or name == "AccountUnavailable":
        klass = "account_402" if status == 402 else "account_unavailable"
    elif name == "Throttled" or status == 429:
        klass = "rate_limited"
    elif name == "AuthExpired" or status == 401:
        klass = "auth_expired_401" if status == 401 else "auth_expired"
    elif name == "NotAuthorized":
        klass = "unauthorized_account"
    elif name == "UpstreamUnavailable":
        klass = "upstream_%s" % status
    elif last is None:
        klass = "no_response:%s" % name
    else:
        klass = "other:%s" % name
    return status, klass, body


def keep_body(label, body, inner):
    """Keep a refused body locally, capped and redacted by the transport's own keeper; its path, or None."""
    if not body:
        return None
    kept, _truncated = transport.keep_rejected_body(body, transport._secret_values(inner, {}))
    path = WK / ("ac2_%s_refusal_body.bin" % label)
    path.write_bytes(kept)
    return path.name


def hit_date(hit):
    return publishers._hit_date(hit) or publishers._hit_date(hit.get("attributes") if isinstance(hit, dict) else None)


def main():
    result = {"security": None, "token_source": None, "account": {"seq": None, "status": None, "class": None,
              "authorized": False, "body_kept": None}, "listing": None, "sign_in_calls": 0, "refresh_calls": 0,
              "hosts": []}
    config = json.loads(Path(publishers.__file__).with_name("config.json").read_text(encoding="utf-8"))
    try:
        rows = [r for r in universe(config) if "lenovo" in (r.get("company") or "").lower()]
        if len(rows) != 1 or not rows[0].get("sa_symbol"):
            raise StopProbe("the resolved universe holds %d Lenovo row(s)" % len(rows))
        security = rows[0]
        result["security"] = {"company": security["company"], "key": security["key"], "sa_symbol": security["sa_symbol"],
                              "identity_status": security.get("identity_status")}
        runtime = MAIN_TREE / config["runtime_root"]  # the saved-session file lives in the shared tree's runtime root
        sessions = TokenFirstSessions(SessionManager(runtime, record), record, signin=refusing_signin)

        def refusing_refresh(publisher):
            counters["refresh_calls"] += 1
            raise StopProbe("refresh refused by the probe (no refresh path is allowed)")

        sessions.refresh = refusing_refresh
        envelope, source = sessions._stored_envelope("sa")
        result["token_source"] = source
        if envelope is None:
            result["account"]["class"] = "no stored sa token"
            return result
        envelope = sessions.get("sa")  # the stored one; a miss would hit the refusing refresh
        publisher = publishers.Publisher("sa", envelope, record)
        publisher.backoff = dict(ONE_ATTEMPT)
        session = publisher.session  # builds the paced session (reads the proxy secret; no vendor request)
        session.inner = CappedInner(session.inner)
        module = publisher.module
        if DRY:
            result["account"]["class"] = "dry_run_no_request"
            return result

        before = len(session.captured)
        result["account"]["seq"] = 1
        try:
            module.check(session)
            result["account"].update(status=session.captured[-1]["status"], authorized=True, **{"class": "ok"})
        except Exception as exc:  # noqa: BLE001 - every stop is classified and recorded
            status, klass, body = classify(exc, session, before)
            result["account"].update(status=status, authorized=False, **{"class": klass},
                                     body_kept=keep_body("account", body, session.inner._inner))
            result["account"]["exception"] = type(exc).__name__
            return result

        before = len(session.captured)
        lst = {"seq": 2, "status": None, "class": None, "hits": None, "dated": None, "pre_floor": None}
        result["listing"] = lst
        try:
            payload = module.news(session, security["sa_symbol"], limit=config.get("candidate_limit", 20))
            hits = payload.get("data", []) if isinstance(payload, dict) else []
            dates = [hit_date(h) for h in hits]
            lst.update(status=session.captured[-1]["status"], hits=len(hits), dated=sum(1 for d in dates if d),
                       pre_floor=sum(1 for d in dates if d and d < FLOOR), **{"class": "ok"})
            lst["newest"] = max((d.isoformat() for d in dates if d), default=None)
            lst["oldest"] = min((d.isoformat() for d in dates if d), default=None)
        except Exception as exc:  # noqa: BLE001
            status, klass, body = classify(exc, session, before)
            lst.update(status=status, **{"class": klass}, body_kept=keep_body("listing", body, session.inner._inner))
            lst["exception"] = type(exc).__name__
        return result
    finally:
        result["sign_in_calls"], result["refresh_calls"] = counters["sign_in_calls"], counters["refresh_calls"]
        result["hosts"] = sorted({e["host"] for e in events if e.get("event") == "http" and e.get("host")})
        result["requests_made"] = counters["requests"]
        result["request_paths"] = counters["request_paths"]
        result["dry"] = DRY
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with open(WK / "ac2_probe_dry.json" if DRY else OUT, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(result, fh, indent=1, sort_keys=True)
        print(json.dumps(result, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
