"""HVST-ac-1 AC2: replay the two kept batch-1 refused bodies (READ-ONLY) through the bot_check classifier.

Reads `<runtime>/rejected_bodies/*.body` and the matching `<runtime>/runs/<job>.json` (status, url, content type
are the recorded facts of the refusal; the CLASS and SIGNATURE are DERIVED here by the rule, never typed from
the file name). Each body is then served as that refusal through the REAL PacedSession and the REAL Worker
(stub client, scratch root under the system temp dir) to show the record shape the new code writes.

No cookie or token text is printed: only class, signature, sizes and hashes. Sockets are replaced by counting
stubs that raise; the last line prints how many calls were made. The runtime root is opened read-only.
"""

import hashlib
import json
import os
import socket
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[8]
sys.path.insert(0, str(ROOT))
RUNTIME = Path(os.environ.get("HARVEST_RUNTIME_ROOT", "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"))

NETWORK_CALLS = []


def _refuse(*args, **kwargs):
    NETWORK_CALLS.append(args)
    raise OSError("network blocked in ac1 replay")


socket.socket.connect = _refuse
socket.create_connection = _refuse
socket.getaddrinfo = _refuse

from lib.opal_data_harvest import bot_check  # noqa: E402
from lib.opal_data_harvest.transport import PacedSession, RequestRejected  # noqa: E402
from lib.opal_data_harvest.worker import Worker  # noqa: E402

KEPT = (("20260930T163418Z-wsj-241953e39e", "wsj"), ("20260930T164017Z-ft-feffdb1b13", "ft"))
UNKEPT = ("bbg", "barrons")


class _Resp:
    def __init__(self, status, url, body, content_type):
        self.status_code, self.url, self.content = status, url, body
        self.headers = {"Content-Type": content_type}

    @property
    def text(self):
        return self.content.decode("utf-8", "replace")


class _Inner:
    def __init__(self, response):
        self.response, self.headers, self.cookies, self.calls = response, {}, None, 0

    def get(self, url, **kwargs):
        self.calls += 1
        return self.response

    def close(self):
        pass


class _Sessions:
    def __init__(self):
        self.log = []

    def get(self, publisher):
        self.log.append("get")
        return {"generation": 0}

    def refresh(self, publisher):
        self.log.append("refresh")
        raise AssertionError("a sign-in/refresh was reached")

    def persist_http_cookies(self, publisher, envelope, session):
        return envelope

    def repair_verification(self, publisher, envelope, target_url=None):
        self.log.append("repair")
        raise AssertionError("a repair was reached")


def main():
    print("runtime root (read-only):", RUNTIME)
    derived = []
    for stem, publisher in KEPT:
        body_path = RUNTIME / "rejected_bodies" / (stem + ".body")
        run = json.loads((RUNTIME / "runs" / (stem + ".json")).read_text(encoding="utf-8"))
        info = run["rejected_response"]
        with open(body_path, "rb") as handle:
            body = handle.read()
        klass, signature = bot_check.classify_body(body)
        print("\n== kept body: publisher=%s status=%s url=%s" % (publisher, info["status"], info["url"]))
        print("   bytes_kept=%d bytes_received=%s truncated=%s sha256_kept=%s" %
              (len(body), info["bytes_received"], info["truncated"], hashlib.sha256(body).hexdigest()))
        print("   recorded at batch 1: job status=%s, attempt class=%s" %
              (run["status"], [a["class"] for a in run["request_attempts"] if a["request_kind"] == "listing"]))
        print("   DERIVED by the rule: class=%s signature=%s" % (klass, signature))
        assert klass == "bot_check" and signature, (publisher, klass, signature)
        derived.append((publisher, klass, signature))

        # serve the kept body as that refusal through the REAL PacedSession and the REAL Worker (scratch root)
        response = _Resp(info["status"], info["url"], body, info["content_type"])
        inner = _Inner(response)
        waits = []
        session_probe = PacedSession(_Inner(response), publisher, lambda event: None, minimum=0, jitter=0, sleep=waits.append)
        try:
            session_probe.get(info["url"])
        except RequestRejected as exc:
            print("   PacedSession raised %s attempt_class=%s signature=%s status=%s (body kept: %d bytes)" %
                  (type(exc).__name__, exc.attempt_class, exc.signature, exc.status, len(exc.body or b"")))
        print("   attempt row written:", json.dumps(session_probe.attempts[0], sort_keys=True))

        class Client:
            def __init__(self, pub, envelope, record, minimum, jitter):
                self.session = PacedSession(inner, pub, record, minimum=0, jitter=0, sleep=lambda s: None)
                self.request_attempts = lambda: list(self.session.attempts)

            def articles(self, security, **kwargs):
                self.session.get(info["url"])
                yield

            def close(self):
                pass

        with tempfile.TemporaryDirectory() as scratch:
            sessions = _Sessions()
            worker = Worker(Path(scratch), {"minimum_request_seconds": 0, "jitter_seconds": 0}, Client, sessions)
            try:
                (result,) = worker.run([{"key": "BA", "ticker": "BA", "company": "Boeing", "aliases": ["Boeing"]}],
                                       [publisher], max_jobs=1)
            finally:
                worker.close()
            (record_path,) = (Path(scratch) / "run_records").glob("*.json")
            record = json.loads(record_path.read_text(encoding="utf-8"))
            job = record["jobs"][0]
            print("   job result: status=%s attempt_class=%s signature=%s sessions=%s auth_refreshes=%s signed_in=%s" %
                  (result["status"], result.get("attempt_class"), result.get("signature"), sessions.log,
                   result["auth_refreshes"], result["signed_in"]))
            print("   run record job entry:", json.dumps({k: job[k] for k in
                  ("publisher", "status", "attempt_class", "signature", "signed_in", "request_attempts")}, sort_keys=True))
            print("   run record request_attempts row:", json.dumps(
                {k: v for k, v in record["request_attempts"][0].items() if k not in ("job_id", "security_key")}, sort_keys=True))
            kept = result["rejected_response"]
            print("   rejected_response written:", json.dumps({k: kept[k] for k in
                  ("status", "url", "content_type", "bytes_received", "bytes_kept", "truncated", "attempt_class", "signature")},
                  sort_keys=True))
            assert result["status"] == "bot_check" and sessions.log == ["get"] and result["signed_in"] is False
            assert (RUNTIME / "rejected_bodies" / (stem + ".body")).read_bytes() == body, "runtime body changed"

    print()
    for publisher in UNKEPT:
        print("%s: no body kept at batch 1 -- unclassifiable until the next refusal (change 3 keeps it)" % publisher)
    print("\nDERIVED SUMMARY:", json.dumps(derived))
    print("NETWORK CALLS MADE: %d" % len(NETWORK_CALLS))


if __name__ == "__main__":
    main()
