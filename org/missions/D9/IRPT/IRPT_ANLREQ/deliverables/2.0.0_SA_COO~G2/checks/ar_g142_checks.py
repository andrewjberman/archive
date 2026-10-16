"""IRPT_ANLREQ AR-g-142 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g142_checks.py build   the provider lease counts reserved calls per window, ONE count per host account: OperationLease(..., window_budget=(calls, window_s)) refuses the
                                     (calls+1)th reserve inside a window with OperationRefused OPERATION_WINDOW_BUDGET and retry_after = ceil(window_start + window_s - now); the count lives in
                                     the stored row (window_start, window_count), survives acquire and release, so a second lease object on the same store shares it; a window rolls over at exactly window_s; a refused
                                     reserve consumes nothing (no count, no spacing, no in-flight); an invalid budget is refused at construction (OPERATION_BUDGET_INVALID);
                                     ResidentSession takes window_budget and hands it to its lease
    python ar_g142_checks.py guard   nothing else moves: no budget = the lease of today (20 spaced calls pass, the stored row keeps exactly its eight keys); a row without the window fields
                                     reads under a budget (count starts at 1); an unknown extra key or a malformed window field is still OPERATION_STORE_INVALID; OPERATION_SPACING still
                                     comes before the budget and consumes no count
    python ar_g142_checks.py regress each existing lease, session, capture and runner test file on its own, then the scope check
    python ar_g142_checks.py scope   the branch changed only operation_lease.py, resident_session.py, their tests, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G142-OK / AR-G142-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import copy
import importlib.util
import inspect
import math
import subprocess
import sys
import threading

IR = "infra/aws/lambda/investor-reporting/"
LEASE = IR + "ycharts/session/operation_lease.py"
SESSION = IR + "ycharts/session/resident_session.py"
TESTS = IR + "ycharts/session/tests/"
OWN = (LEASE, SESSION, TESTS + "test_operation_lease.py", TESTS + "test_resident_session.py", TESTS + "test_resident_session_checker.py", TESTS + "test_window_budget.py",
       "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-142.lease-window-budget.md")
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~269/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~270/",
              "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/")
REGRESS_FILES = (TESTS + "test_operation_lease.py", TESTS + "test_resident_session.py", TESTS + "test_resident_session_checker.py", TESTS + "test_host_capture.py",
                 IR + "ycharts/research/tests/test_runner.py")
BASE_KEYS = {"version", "fence", "holder", "session_fence", "expires_at", "next_allowed_at", "observed_at", "in_flight_until"}


def load():
    spec = importlib.util.spec_from_file_location("operation_lease_g142", LEASE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # a dataclass needs its module registered
    spec.loader.exec_module(module)
    return module


class Store:
    def __init__(self):
        self.rows, self.lock = {}, threading.Lock()

    def read(self, key):
        with self.lock:
            return copy.deepcopy(self.rows.get(key))

    def compare_and_swap(self, key, expected_version, replacement):
        with self.lock:
            old = self.rows.get(key)
            if (old["version"] if old else None) != expected_version:
                return False
            self.rows[key] = copy.deepcopy(replacement)
            return True

    def only_row(self):
        assert len(self.rows) == 1
        return next(iter(self.rows.values()))


def make(mod, store, clock, budget=None):
    kwargs = {} if budget is None else {"window_budget": budget}
    return mod.OperationLease(store, provider="ycharts", account_id="enrolled-1", clock=lambda: clock[0], **kwargs)


def call(lease, token, clock):
    """One reserve + complete at the current clock."""
    deadline = clock[0] + 30
    lease.reserve(token, hard_deadline=deadline)
    lease.complete(token, hard_deadline=deadline)


def code_of(fn):
    try:
        fn()
    except Exception as exc:  # the test reads whatever a refusal is
        return getattr(exc, "code", None) or type(exc).__name__, getattr(exc, "retry_after", None)
    return None, None


def arms_build(mod):
    fails = []
    if "window_budget" not in inspect.signature(mod.OperationLease.__init__).parameters:
        return ["OperationLease takes no window_budget"]
    # b1: three calls pass, the fourth is refused with the wait to the window's end; the refusal consumes nothing.
    clock, store = [100.0], Store()
    lease = make(mod, store, clock, (3, 100.0))
    token = lease.acquire("holder-a", session_fence=1, ttl=900)
    for _ in range(3):
        call(lease, token, clock)
        clock[0] += 3
    before = copy.deepcopy(store.only_row())
    code, retry = code_of(lambda: lease.reserve(token, hard_deadline=clock[0] + 30))
    if code != "OPERATION_WINDOW_BUDGET" or retry != math.ceil(100.0 + 100.0 - clock[0]):
        fails.append("b1 the 4th call: code %r retry_after %r (want OPERATION_WINDOW_BUDGET and %d)" % (code, retry, math.ceil(200.0 - clock[0])))
    after = store.only_row()
    if after["window_count"] != 3 or after["window_start"] != 100.0 or after["in_flight_until"] != 0 or after["next_allowed_at"] != before["next_allowed_at"]:
        fails.append("b1 a refused reserve changed the row: count %r start %r in_flight %r next_allowed %r (was %r)" % (
            after.get("window_count"), after.get("window_start"), after["in_flight_until"], after["next_allowed_at"], before["next_allowed_at"]))
    if set(after) != BASE_KEYS | {"window_start", "window_count"}:
        fails.append("b1 the stored row keys are %r" % sorted(after))
    # b2: the window rolls over at exactly window_s, not before.
    clock[0] = 199.9
    code, _ = code_of(lambda: lease.reserve(token, hard_deadline=clock[0] + 30))
    if code != "OPERATION_WINDOW_BUDGET":
        fails.append("b2 at window_start + window_s - 0.1 the call was not refused (%r)" % (code,))
    clock[0] = 200.0
    try:
        call(lease, token, clock)
    except Exception as exc:
        fails.append("b2 at exactly window_start + window_s the call was refused (%r)" % (getattr(exc, "code", exc),))
        return fails
    row = store.only_row()
    if row["window_start"] != 200.0 or row["window_count"] != 1:
        fails.append("b2 at exactly window_start + window_s: start %r count %r (want 200.0 and 1)" % (row["window_start"], row["window_count"]))
    # b3: ONE count per account: a second lease object on the same store shares it.
    clock, store = [100.0], Store()
    first = make(mod, store, clock, (3, 100.0))
    t1 = first.acquire("holder-a", session_fence=1, ttl=900)
    for _ in range(2):
        call(first, t1, clock)
        clock[0] += 3
    first.release(t1)
    second = make(mod, store, clock, (3, 100.0))
    t2 = second.acquire("holder-b", session_fence=1, ttl=900)
    call(second, t2, clock)
    clock[0] += 3
    code, _ = code_of(lambda: second.reserve(t2, hard_deadline=clock[0] + 30))
    if code != "OPERATION_WINDOW_BUDGET":
        fails.append("b3 the 4th call across two lease objects was not refused (%r)" % (code,))
    # b4: an invalid budget is refused at construction.
    for bad in ((0, 10.0), (3, 0), (3, -1.0), (True, 10.0), ("3", 10.0), (3, float("nan")), (3,), [3, 10.0, 1], 5, (2.5, 10.0)):
        code, _ = code_of(lambda bad=bad: make(mod, Store(), [100.0], bad))
        if code != "OPERATION_BUDGET_INVALID":
            fails.append("b4 budget %r gives %r (want OPERATION_BUDGET_INVALID)" % (bad, code))
    # b5: ResidentSession takes window_budget and hands it to its lease.
    try:
        text = open(SESSION, encoding="utf-8").read()
        if "window_budget" not in text or "window_budget=window_budget" not in text.replace(" ", ""):
            fails.append("b5 resident_session.py does not pass window_budget to its OperationLease")
    except OSError as exc:
        fails.append("b5 cannot read resident_session.py: %s" % exc)
    return fails


def arms_guard(mod):
    fails = []
    # g1: no budget = today: 20 spaced calls pass and the row keeps exactly its eight keys.
    clock, store = [100.0], Store()
    lease = make(mod, store, clock)
    token = lease.acquire("holder-a", session_fence=1, ttl=900)
    try:
        for _ in range(20):
            call(lease, token, clock)
            clock[0] += 3
            if clock[0] > 100 + 800:
                lease.renew(token, ttl=900)
    except Exception as exc:
        fails.append("g1 no budget: a call was refused (%r)" % (getattr(exc, "code", exc),))
    if set(store.only_row()) != BASE_KEYS:
        fails.append("g1 no budget: the stored row keys are %r (want exactly the eight)" % sorted(store.only_row()))
    if "window_budget" not in inspect.signature(mod.OperationLease.__init__).parameters:
        return fails  # g2 to g4 need a budget to exist; the build arm holds the base to account for that
    # g2: a row without the window fields reads under a budget; the count starts at 1.
    row_before = copy.deepcopy(store.only_row())
    budgeted = make(mod, store, clock, (3, 100.0))
    lease.release(token)
    token2 = budgeted.acquire("holder-b", session_fence=1, ttl=900)
    clock[0] += 3
    try:
        call(budgeted, token2, clock)
    except Exception as exc:
        fails.append("g2 an old-schema row refused under a budget (%r)" % (getattr(exc, "code", exc),))
    else:
        row = store.only_row()
        if row.get("window_count") != 1 or row_before.get("window_count") is not None:
            fails.append("g2 count after the first budgeted call is %r (want 1)" % (row.get("window_count"),))
    # g3: an unknown extra key, or a malformed window field, is still OPERATION_STORE_INVALID.
    for label, patch in (("unknown key", {"surprise": 1}), ("negative count", {"window_start": 100.0, "window_count": -1}),
                         ("string count", {"window_start": 100.0, "window_count": "2"}), ("count without start", {"window_count": 1}),
                         ("bool count", {"window_start": 100.0, "window_count": True})):
        store.only_row().update(patch)
        code, _ = code_of(lambda: budgeted.assert_owned(token2))
        if code != "OPERATION_STORE_INVALID":
            fails.append("g3 %s: assert_owned gives %r (want OPERATION_STORE_INVALID)" % (label, code))
        for key in patch:
            store.only_row().pop(key, None)
    # g4: OPERATION_SPACING comes before the budget and consumes no count.
    clock, store = [100.0], Store()
    lease = make(mod, store, clock, (3, 100.0))
    token = lease.acquire("holder-a", session_fence=1, ttl=900)
    call(lease, token, clock)
    clock[0] += 1
    code, _ = code_of(lambda: lease.reserve(token, hard_deadline=clock[0] + 30))
    if code != "OPERATION_SPACING" or store.only_row()["window_count"] != 1:
        fails.append("g4 a call 1 s after the last: code %r count %r (want OPERATION_SPACING and 1)" % (code, store.only_row().get("window_count")))
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
        print("AR-G142-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G142-FAIL usage: build | guard | scope | regress")
        return 2
    mod = load()
    fails = arms_build(mod) if mode == "build" else arms_guard(mod)
    print("AR-G142-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
