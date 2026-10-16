"""IRPT_ANLREQ AR-g-129 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g129_checks.py build   the resolve hop backs off a WAF challenge: resident_worker._resolve_retry_visibility(code, receives) answers 150, 300 and 450 s for a RETRY code
                                     ending ":WAF_CHALLENGE" at receive 1, 2 and 3; RESOLVE_WAF_BACKOFF_S is (150, 300, 450), sums to 900 and stays under upload_resolution.REDRIVE_SECONDS
                                     and RESOLVE_MAX_RECEIVES stays under the queue's maxReceiveCount of 5; and the REAL poll_once sets VisibilityTimeout from it, prints visibility=<s>
                                     in the RETRY journal line, and ends the row at receive 4
    python ar_g129_checks.py guard   nothing else moves: every other RETRY code keeps the flat RESOLVE_RETRY_VISIBILITY_S (60) at every receive through the real poll_once; a code that only
                                     CONTAINS WAF_CHALLENGE, a missing or non-string code, and the BUSY class (own re-send path, no visibility call) are unchanged
    python ar_g129_checks.py regress each existing test file on its own, then the scope check
    python ar_g129_checks.py scope   the branch changed only resident_worker.py, its test file, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G129-OK / AR-G129-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import contextlib
import io
import json
import subprocess
import sys
from types import SimpleNamespace

IR = "infra/aws/lambda/investor-reporting/"
WORKER = IR + "ycharts/generate/resident_worker.py"
TEST = IR + "ycharts/generate/tests/test_resolve_upload.py"
ORDER = "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-129.resolve-waf-backoff.md"
OWN = (WORKER, TEST, ORDER)
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~262/",
              "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/task_orders/")
REGRESS_FILES = (TEST, IR + "ycharts/generate/tests/test_frozen_worker.py")
WAF = "PROVIDER_READ_UNAVAILABLE:WAF_CHALLENGE"


def load_worker():
    for sub in ("", "reports", "ycharts/generate", "ycharts/session", "ycharts/extract", "_scope", "_ids", "_keys", "_authz", "intake", "ops", "lib"):
        sys.path.insert(0, IR + sub if sub else IR)
    import resident_worker
    return resident_worker


class Queue:
    """A queue double that records what poll_once does with the one received message."""

    def __init__(self, receives):
        self.receives, self.visibility, self.deleted, self.sent = receives, [], [], []

    def receive_message(self, **kw):
        body = json.dumps({"kind": "resolve_upload", "tenant": "t", "upload_id": "u", "revision": "1"})
        return {"Messages": [{"Body": body, "ReceiptHandle": "rh-1", "Attributes": {"ApproximateReceiveCount": str(self.receives)}}]}

    def change_message_visibility(self, **kw):
        self.visibility.append(kw["VisibilityTimeout"])

    def delete_message(self, **kw):
        self.deleted.append(kw["ReceiptHandle"])

    def send_message(self, **kw):
        self.sent.append((kw["MessageBody"], kw["DelaySeconds"]))


def poll(rw, code, receives):
    """Run the REAL poll_once once for a resolve_upload message whose execute answers RETRY with `code`. Returns (queue, journal text, ended rows)."""
    queue, ended = Queue(receives), []
    detail = {"retry_after": None, "requested_at": 1000.0}
    if code is not None:
        detail["code"] = code
    assembly = SimpleNamespace(execute=lambda decoded, heartbeat: {"state": "RETRY", "detail": detail}, clock=lambda: 1001.0)
    saved = rw._end_exhausted_resolve
    rw._end_exhausted_resolve = lambda asm, message: ended.append(message)
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            rw.poll_once(sqs=queue, queue_url="offline", assembly=assembly)
    finally:
        rw._end_exhausted_resolve = saved
    return queue, out.getvalue(), ended


def arms_build(rw):
    fails = []
    if not hasattr(rw, "_resolve_retry_visibility") or not hasattr(rw, "RESOLVE_WAF_BACKOFF_S"):
        return ["resident_worker has no _resolve_retry_visibility / RESOLVE_WAF_BACKOFF_S"]
    if tuple(rw.RESOLVE_WAF_BACKOFF_S) != (150, 300, 450):
        fails.append("RESOLVE_WAF_BACKOFF_S is %r, want (150, 300, 450)" % (rw.RESOLVE_WAF_BACKOFF_S,))
    from upload_resolution import REDRIVE_SECONDS
    if sum(rw.RESOLVE_WAF_BACKOFF_S) != 900 or sum(rw.RESOLVE_WAF_BACKOFF_S) > REDRIVE_SECONDS:
        fails.append("the back-off sums to %r (want 900, at most REDRIVE_SECONDS %r)" % (sum(rw.RESOLVE_WAF_BACKOFF_S), REDRIVE_SECONDS))
    if not rw.RESOLVE_MAX_RECEIVES < 5:
        fails.append("RESOLVE_MAX_RECEIVES %r is not below the queue's maxReceiveCount 5" % rw.RESOLVE_MAX_RECEIVES)
    for receives, want in ((1, 150), (2, 300), (3, 450)):
        got = rw._resolve_retry_visibility(WAF, receives)
        if got != want:
            fails.append("_resolve_retry_visibility(WAF, %d) is %r, want %d" % (receives, got, want))
        queue, journal, _ = poll(rw, WAF, receives)
        if queue.visibility != [want] or queue.deleted:
            fails.append("poll_once at receive %d: visibility calls %r deleted %r (want [%d] and none)" % (receives, queue.visibility, queue.deleted, want))
        if "IRPT_RESIDENT_RESOLVE state=RETRY code=%s visibility=%d" % (WAF, want) not in journal:
            fails.append("the journal at receive %d does not read '... code=%s visibility=%d': %r" % (receives, WAF, want, journal[-160:]))
    queue, journal, ended = poll(rw, WAF, 4)
    if len(ended) != 1 or queue.deleted != ["rh-1"] or "state=ATTENTION code=RESOLVE_RETRY_EXHAUSTED" not in journal:
        fails.append("receive 4 did not end the row (ended %r, deleted %r, journal %r)" % (len(ended), queue.deleted, journal[-120:]))
    return fails


def arms_guard(rw):
    fails = []
    flat = rw.RESOLVE_RETRY_VISIBILITY_S
    if flat != 60:
        fails.append("RESOLVE_RETRY_VISIBILITY_S is %r, want 60" % flat)
    others = ["PROVIDER_READ_UNAVAILABLE:STATUS_503", "PROVIDER_READ_UNAVAILABLE:BODY", "PROVIDER_READ_UNAVAILABLE:WAF_CAPTCHA", "LOOKUP_TIMEOUT",
              "PROVIDER_READ_UNAVAILABLE:WAF_CHALLENGE_EXTRA", "WAF_CHALLENGE:PROVIDER_READ_UNAVAILABLE", None, 7, ""]
    for code in others:
        for receives in (1, 2, 3):
            if hasattr(rw, "_resolve_retry_visibility") and rw._resolve_retry_visibility(code, receives) != flat:
                fails.append("_resolve_retry_visibility(%r, %d) is %r, want %d" % (code, receives, rw._resolve_retry_visibility(code, receives), flat))
    for code in ("PROVIDER_READ_UNAVAILABLE:STATUS_503", "PROVIDER_READ_UNAVAILABLE:WAF_CAPTCHA", "PROVIDER_READ_UNAVAILABLE:WAF_CHALLENGE_EXTRA", None):
        for receives in (1, 2, 3):
            queue, journal, _ = poll(rw, code, receives)
            if queue.visibility != [flat] or queue.deleted or queue.sent:
                fails.append("poll_once code %r receive %d: visibility %r deleted %r sent %r (want [%d])" % (code, receives, queue.visibility, queue.deleted, queue.sent, flat))
    busy_queue, journal, _ = poll(rw, "PROVIDER_READ_UNAVAILABLE:OPERATION_BUSY", 1)
    if busy_queue.visibility or len(busy_queue.sent) != 1 or busy_queue.deleted != ["rh-1"]:
        fails.append("the BUSY class changed: visibility %r sent %r deleted %r (want a re-send, no visibility call)" % (busy_queue.visibility, busy_queue.sent, busy_queue.deleted))
    return fails


def scope():
    rc = subprocess.run(["git", "merge-base", "HEAD", "box/dell2"], capture_output=True)
    base = rc.stdout.decode().strip()
    if rc.returncode != 0 or not base:
        return ["no merge-base with box/dell2"]
    diff = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], capture_output=True)
    if diff.returncode != 0:
        return ["git diff rc=%d" % diff.returncode]
    names = [n for n in diff.stdout.decode().splitlines() if n.strip()]
    stray = [n for n in names if n not in OWN and not n.startswith(OWN_PREFIX + ISSUER)]
    return ["outside the cell's write set: %s" % ", ".join(stray)] if stray else []


def regress():
    fails = []
    for path in REGRESS_FILES:
        out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", path], capture_output=True, text=True)
        if out.returncode != 0:
            fails.append("%s: rc=%d %s" % (path.rsplit("/", 1)[-1], out.returncode, (out.stdout or out.stderr).strip().splitlines()[-1:] or ""))
    return fails + scope()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode in ("scope", "regress"):
        fails = scope() if mode == "scope" else regress()
        print("AR-G129-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G129-FAIL usage: build | guard | scope | regress")
        return 2
    rw = load_worker()
    fails = arms_build(rw) if mode == "build" else arms_guard(rw)
    print("AR-G129-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
