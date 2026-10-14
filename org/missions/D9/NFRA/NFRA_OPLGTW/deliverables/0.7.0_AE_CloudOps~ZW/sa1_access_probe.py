"""OG-sa-1 step 1 (0.7.0_AE_CloudOps~ZW): read Seeking Alpha ACCESS before anything is changed.

ONE vendor request, counted in code: the harvester's own sa `check()` (GET /api/v3/account/{user_id}/info) through the
runner pin's own TokenFirstSessions, with a REFUSING sign-in and a REFUSING refresh (both counted), a retry policy of one
attempt, and the inner HTTP session wrapped so a 2nd request raises BEFORE it is sent. No capture, no S3 write, no
Secrets Manager write. No token, cookie or credential is printed or written: the output holds the status, the class,
the token SOURCE (a path or a secret NAME) and its timestamps, never a value.

usage (run with cwd = the runner pin's worktree, so the code read is the code the runner runs):
  python sa1_access_probe.py --runtime-root <dir holding secrets/sa.dpapi> --out <json> [--dry]
--dry goes as far as the stored token and the session build and makes NO vendor request.
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())

from lib.opal_data_harvest import publishers  # noqa: E402
from lib.opal_data_harvest.auth import SessionManager  # noqa: E402
from lib.opal_data_harvest.sessions import TokenFirstSessions  # noqa: E402

CAP = 1
ONE_ATTEMPT = {"max_attempts": 1, "auth_confirm_retries": 0}
counters = {"sign_in_calls": 0, "refresh_calls": 0, "requests": 0, "request_paths": []}
events = []


class StopProbe(RuntimeError):
    pass


def record(event):
    events.append(event)


def refusing_signin(publisher, credentials):
    counters["sign_in_calls"] += 1
    raise StopProbe("sign-in refused by the probe")


class CappedInner:
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
    captured = session.captured[before:]
    last = captured[-1] if captured else None
    status = last["status"] if last else getattr(exc, "status", None)
    name = type(exc).__name__
    if name == "StopProbe":
        klass = "stopped_before_send"
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
    return status, klass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runtime-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    result = {"read_at": None, "dry": args.dry, "runtime_root": args.runtime_root, "token_source": None,
              "token_timestamps": None, "http_status": None, "class": None, "authorized": False}
    try:
        sessions = TokenFirstSessions(SessionManager(Path(args.runtime_root), record), record, signin=refusing_signin)

        def refusing_refresh(publisher):
            counters["refresh_calls"] += 1
            raise StopProbe("refresh refused by the probe")

        sessions.refresh = refusing_refresh
        envelope, source = sessions._stored_envelope("sa")
        result["token_source"] = source
        result["token_timestamps"] = dict(getattr(sessions, "_times", {}) or {})
        if envelope is None:
            result["class"] = "no_stored_sa_token"
            return result
        envelope = sessions.get("sa")
        publisher = publishers.Publisher("sa", envelope, record)
        publisher.backoff = dict(ONE_ATTEMPT)
        session = publisher.session
        session.inner = CappedInner(session.inner)
        module = publisher.module
        if args.dry:
            result["class"] = "dry_run_no_request"
            return result
        before = len(session.captured)
        result["read_at"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            module.check(session)
            result.update(http_status=session.captured[-1]["status"], authorized=True, **{"class": "ok"})
        except Exception as exc:  # noqa: BLE001 - every stop is classified and recorded
            status, klass = classify(exc, session, before)
            result.update(http_status=status, authorized=False, **{"class": klass})
            result["exception"] = type(exc).__name__
        return result
    finally:
        result["sign_in_calls"] = counters["sign_in_calls"]
        result["refresh_calls"] = counters["refresh_calls"]
        result["requests_made"] = counters["requests"]
        result["request_paths"] = counters["request_paths"]
        result["hosts"] = sorted({e["host"] for e in events if e.get("event") == "http" and e.get("host")})
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(result, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print(json.dumps(result, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
