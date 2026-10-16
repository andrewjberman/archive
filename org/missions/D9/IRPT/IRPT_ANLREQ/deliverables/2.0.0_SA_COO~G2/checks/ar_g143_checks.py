"""IRPT_ANLREQ AR-g-143 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g143_checks.py build   the resolve hop treats a lease WINDOW-BUDGET refusal like a busy provider: a RETRY whose code ends ":OPERATION_WINDOW_BUDGET" (and carries requested_at) is
                                     re-sent for its retry_after (clamped to 1..900 s; the flat 60 s when it names none) BEFORE the received message is deleted, with no visibility change,
                                     and past RESOLVE_BUSY_DEADLINE_S from requested_at the upload ends through _end_busy_resolve with the journal line RESOLVE_PROVIDER_BUSY, all through the REAL poll_once
    python ar_g143_checks.py guard   nothing else moves: the OPERATION_BUSY class keeps its re-send; the WAF class keeps 150, 300, 450 s and every other RETRY code the flat 60 s at every
                                     receive; a code that only CONTAINS WINDOW_BUDGET, a missing or non-string code and a missing requested_at take the visibility path as before
    python ar_g143_checks.py regress each existing resident-worker test file on its own, then the scope check
    python ar_g143_checks.py scope   the branch changed only resident_worker.py, its test file, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G143-OK / AR-G143-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
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
OWN = (WORKER, TEST, "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-143.resolve-window-budget-requeue.md")
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~269/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~270/",
              "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/")
REGRESS_FILES = (TEST, IR + "ycharts/generate/tests/test_frozen_worker.py")
BUDGET = "PROVIDER_READ_UNAVAILABLE:OPERATION_WINDOW_BUDGET"
BUSY = "PROVIDER_READ_UNAVAILABLE:OPERATION_BUSY"
WAF = "PROVIDER_READ_UNAVAILABLE:WAF_CHALLENGE"


def load_worker():
    for sub in ("", "reports", "ycharts/generate", "ycharts/session", "ycharts/extract", "_scope", "_ids", "_keys", "_authz", "intake", "ops", "lib"):
        sys.path.insert(0, IR + sub if sub else IR)
    import resident_worker
    return resident_worker


class Queue:
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


def poll(rw, code, receives=1, retry_after=None, requested_at=1000.0, now=1001.0):
    """Run the REAL poll_once once for a resolve_upload message whose execute answers RETRY with `code`. Returns (queue, journal, busy-ended count)."""
    queue, busy_ended = Queue(receives), []
    detail = {"retry_after": retry_after, "requested_at": requested_at}
    if code is not None:
        detail["code"] = code
    assembly = SimpleNamespace(execute=lambda decoded, heartbeat: {"state": "RETRY", "detail": detail}, clock=lambda: now)
    saved_busy, saved_exh = rw._end_busy_resolve, rw._end_exhausted_resolve
    rw._end_busy_resolve = lambda asm, message: busy_ended.append(message)
    rw._end_exhausted_resolve = lambda asm, message: None
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            rw.poll_once(sqs=queue, queue_url="offline", assembly=assembly)
    finally:
        rw._end_busy_resolve, rw._end_exhausted_resolve = saved_busy, saved_exh
    return queue, out.getvalue(), busy_ended


def arms_build(rw):
    fails = []
    for retry_after, want in ((120, 120), (None, 60), (5000, 900), (0, 1)):
        queue, journal, ended = poll(rw, BUDGET, retry_after=retry_after)
        if queue.sent != [(queue.sent[0][0] if queue.sent else None, want)] or queue.deleted != ["rh-1"] or queue.visibility or ended:
            fails.append("b1 retry_after %r: sent %r deleted %r visibility %r busy-ended %d (want one re-send with DelaySeconds %d, the original deleted, no visibility call)" % (
                retry_after, queue.sent, queue.deleted, queue.visibility, len(ended), want))
    queue, journal, ended = poll(rw, BUDGET, retry_after=120, requested_at=1000.0, now=1000.0 + rw.RESOLVE_BUSY_DEADLINE_S)
    if len(ended) != 1 or queue.sent or "state=ATTENTION code=RESOLVE_PROVIDER_BUSY" not in journal:
        fails.append("b2 past the busy deadline: busy-ended %d sent %r journal %r (want the upload ended through _end_busy_resolve with RESOLVE_PROVIDER_BUSY)" % (len(ended), queue.sent, journal[-120:]))
    queue, journal, _ = poll(rw, BUDGET, retry_after=120)
    if "OPERATION_WINDOW_BUDGET" not in journal:
        fails.append("b3 the journal does not name the class: %r" % (journal[-160:],))
    return fails


def arms_guard(rw):
    fails = []
    queue, _, ended = poll(rw, BUSY, retry_after=120)
    if len(queue.sent) != 1 or queue.sent[0][1] != 120 or queue.deleted != ["rh-1"] or queue.visibility or ended:
        fails.append("g1 the BUSY class changed: sent %r deleted %r visibility %r" % (queue.sent, queue.deleted, queue.visibility))
    for receives, want in ((1, 150), (2, 300), (3, 450)):
        queue, _, _ = poll(rw, WAF, receives=receives)
        if queue.visibility != [want] or queue.sent:
            fails.append("g2 WAF at receive %d: visibility %r sent %r (want [%d])" % (receives, queue.visibility, queue.sent, want))
    for code in ("PROVIDER_READ_UNAVAILABLE:STATUS_503", "PROVIDER_READ_UNAVAILABLE:OPERATION_WINDOW_BUDGET_EXTRA", "OPERATION_WINDOW_BUDGET:PROVIDER_READ_UNAVAILABLE", None, 7):
        for receives in (1, 2, 3):
            queue, _, _ = poll(rw, code, receives=receives)
            if queue.visibility != [60] or queue.sent or queue.deleted:
                fails.append("g3 code %r receive %d: visibility %r sent %r deleted %r (want [60])" % (code, receives, queue.visibility, queue.sent, queue.deleted))
    queue, _, _ = poll(rw, BUDGET, retry_after=120, requested_at=None)
    if queue.sent or queue.visibility != [60]:
        fails.append("g4 a budget code with no requested_at: sent %r visibility %r (want the flat 60 s visibility path, as for BUSY)" % (queue.sent, queue.visibility))
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
        print("AR-G143-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G143-FAIL usage: build | guard | scope | regress")
        return 2
    rw = load_worker()
    fails = arms_build(rw) if mode == "build" else arms_guard(rw)
    print("AR-G143-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
