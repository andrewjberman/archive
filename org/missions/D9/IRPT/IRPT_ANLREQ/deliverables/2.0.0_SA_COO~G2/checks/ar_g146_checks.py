"""IRPT_ANLREQ AR-g-146 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

AR-g-142 put the window count INTO the provider lease row (two extra keys). That makes a rollback to the r34g resident unsafe: r34g's lease code checks the row's exact key set and
would refuse the row. This cell moves the count into its OWN row beside the lease row, so the lease row stays exactly as r34g reads it.

    python ar_g146_checks.py build   OperationLease(window_budget=(calls, window_s)) keeps its count in a SEPARATE store row (key PROVIDER_OPERATION#<hash of provider, account and "window">,
                                     keys exactly version, window_start, window_count); the lease row keeps EXACTLY its eight keys with or without a budget; the (calls+1)th reserve inside a window
                                     is refused OPERATION_WINDOW_BUDGET with retry_after = ceil(window_start + window_s - now) and consumes nothing (no count, no spacing, no in-flight); a window rolls over
                                     at exactly window_s; a second lease object on the same store shares the count; an invalid budget is refused at construction; the count survives a new job without
                                     any carry-over code in acquire
    python ar_g146_checks.py guard   nothing else moves: no budget = one store row and the lease of today; a budgeted lease with no window row yet counts from 1; a malformed window row is
                                     OPERATION_STORE_INVALID and leaves the lease row alone; OPERATION_SPACING still comes before the budget and consumes no count; a window row that cannot be written
                                     (its swap keeps failing) does not stop a reserve that already succeeded
    python ar_g146_checks.py regress each existing lease, session, capture and runner test file on its own, then the scope check
    python ar_g146_checks.py scope   the branch changed only operation_lease.py, their tests, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G146-OK / AR-G146-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
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
OWN = (LEASE, TESTS + "test_operation_lease.py", TESTS + "test_window_budget.py",
       "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-146.window-count-own-row.md")
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~273/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~274/",
              "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/")
REGRESS_FILES = (TESTS + "test_operation_lease.py", TESTS + "test_window_budget.py", TESTS + "test_resident_session.py", TESTS + "test_resident_session_checker.py",
                 TESTS + "test_host_capture.py", IR + "ycharts/research/tests/test_runner.py")
BASE_KEYS = {"version", "fence", "holder", "session_fence", "expires_at", "next_allowed_at", "observed_at", "in_flight_until"}
WINDOW_KEYS = {"version", "window_start", "window_count"}


def load():
    spec = importlib.util.spec_from_file_location("operation_lease_g146", LEASE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # a dataclass needs its module registered
    spec.loader.exec_module(module)
    return module


class Store:
    def __init__(self, break_window_swap=False):
        self.rows, self.lock, self.break_window_swap = {}, threading.Lock(), break_window_swap

    def read(self, key):
        with self.lock:
            return copy.deepcopy(self.rows.get(key))

    def compare_and_swap(self, key, expected_version, replacement):
        with self.lock:
            old = self.rows.get(key)
            if self.break_window_swap and "window_count" in replacement:
                if self.break_window_swap == "raise":
                    raise RuntimeError("store down")
                return False
            if (old["version"] if old else None) != expected_version:
                return False
            self.rows[key] = copy.deepcopy(replacement)
            return True

    def lease_row(self):
        rows = [r for r in self.rows.values() if "holder" in r]
        assert len(rows) == 1
        return rows[0]

    def window_rows(self):
        return [r for r in self.rows.values() if "holder" not in r]


def make(mod, store, clock, budget=None):
    kwargs = {} if budget is None else {"window_budget": budget}
    return mod.OperationLease(store, provider="ycharts", account_id="enrolled-1", clock=lambda: clock[0], **kwargs)


def call(lease, token, clock):
    deadline = clock[0] + 30
    lease.reserve(token, hard_deadline=deadline)
    lease.complete(token, hard_deadline=deadline)


def code_of(fn):
    try:
        fn()
    except Exception as exc:  # a refusal is whatever the code raises
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
    main_before, window_before = copy.deepcopy(store.lease_row()), copy.deepcopy(store.window_rows())
    code, retry = code_of(lambda: lease.reserve(token, hard_deadline=clock[0] + 30))
    if code != "OPERATION_WINDOW_BUDGET" or retry != math.ceil(100.0 + 100.0 - clock[0]):
        fails.append("b1 the 4th call: code %r retry_after %r (want OPERATION_WINDOW_BUDGET and %d)" % (code, retry, math.ceil(200.0 - clock[0])))
    if store.lease_row() != main_before or store.window_rows() != window_before:
        fails.append("b1 a refused reserve changed a row: lease row before %r after %r; window rows before %r after %r" % (main_before, store.lease_row(), window_before, store.window_rows()))
    windows = store.window_rows()
    if len(windows) != 1 or set(windows[0]) != WINDOW_KEYS or windows[0]["window_count"] != 3 or windows[0]["window_start"] != 100.0:
        fails.append("b1 the window row is %r (want one row with keys %s, count 3, start 100.0)" % (windows, sorted(WINDOW_KEYS)))
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
    if not store.window_rows():
        return fails + ["b2 there is no window row after the rollover call (the count is not in its own row)"]
    row = store.window_rows()[0]
    if row["window_start"] != 200.0 or row["window_count"] != 1:
        fails.append("b2 at exactly window_start + window_s: start %r count %r (want 200.0 and 1)" % (row["window_start"], row["window_count"]))
    # b3: ONE count per account: a second lease object on the same store shares it, with no carry-over code in acquire.
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
    # b5: ResidentSession takes window_budget and hands it to its lease (kept from AR-g-142).
    try:
        text = open(SESSION, encoding="utf-8").read()
        if "window_budget" not in text or "window_budget=window_budget" not in text.replace(" ", ""):
            fails.append("b5 resident_session.py does not pass window_budget to its OperationLease")
    except OSError as exc:
        fails.append("b5 cannot read resident_session.py: %s" % exc)
    # b6: the lease row keeps EXACTLY its eight keys, budgeted or not, at every step.
    clock, store = [100.0], Store()
    lease = make(mod, store, clock, (3, 100.0))
    token = lease.acquire("holder-a", session_fence=1, ttl=900)
    seen = [set(store.lease_row())]
    call(lease, token, clock)
    seen.append(set(store.lease_row()))
    lease.release(token)
    seen.append(set(store.lease_row()))
    if any(keys != BASE_KEYS for keys in seen):
        fails.append("b6 the lease row's keys changed with a budget: %r (want exactly %s)" % ([sorted(k) for k in seen if k != BASE_KEYS][:1], sorted(BASE_KEYS)))
    fails += arms_window(mod, ([100.0], Store()))
    return fails


def arms_window(mod, lease_released_store):
    """b7 to b9: the window row beside the lease row (a budgeted lease over an old store, a malformed window row, an unwritable window row)."""
    fails = []
    clock, store = lease_released_store
    lease = make(mod, store, clock)
    token = lease.acquire("holder-a", session_fence=1, ttl=900)
    # b7: a budgeted lease over a store with no window row yet counts from 1.
    budgeted = make(mod, store, clock, (3, 100.0))
    lease.release(token)
    token2 = budgeted.acquire("holder-b", session_fence=1, ttl=900)
    clock[0] += 3
    try:
        call(budgeted, token2, clock)
    except Exception as exc:
        fails.append("b7 a budgeted lease over an old store refused (%r)" % (getattr(exc, "code", exc),))
    else:
        windows = store.window_rows()
        if len(windows) != 1 or windows[0].get("window_count") != 1:
            fails.append("b7 the count after the first budgeted call is %r (want one window row at 1)" % (windows,))
    # b8: a malformed window row is OPERATION_STORE_INVALID and leaves the lease row alone.
    for label, patch in (("unknown key", {"surprise": 1}), ("negative count", {"window_count": -1}), ("string count", {"window_count": "2"}),
                         ("bool count", {"window_count": True}), ("negative start", {"window_start": -1.0}), ("string start", {"window_start": "x"})):
        window = store.window_rows()[0]
        saved = copy.deepcopy(window)
        window.update(patch)
        main_before = copy.deepcopy(store.lease_row())
        clock[0] += 3
        code, _ = code_of(lambda: budgeted.reserve(token2, hard_deadline=clock[0] + 30))
        if code != "OPERATION_STORE_INVALID":
            fails.append("b8 %s: reserve gives %r (want OPERATION_STORE_INVALID)" % (label, code))
        if store.lease_row() != main_before:
            fails.append("b8 %s: the lease row changed" % label)
        window.clear()
        window.update(saved)
    window = store.window_rows()[0]
    saved = copy.deepcopy(window)
    del window["window_start"]
    clock[0] += 3
    code, _ = code_of(lambda: budgeted.reserve(token2, hard_deadline=clock[0] + 30))
    if code != "OPERATION_STORE_INVALID":
        fails.append("b8 missing window_start: reserve gives %r (want OPERATION_STORE_INVALID)" % (code,))
    window.clear()
    window.update(saved)
    # b9: a window row that cannot be written does not stop a reserve that already succeeded.
    for mode in (True, "raise"):
        clock, store = [100.0], Store(break_window_swap=mode)
        lease = make(mod, store, clock, (3, 100.0))
        token = lease.acquire("holder-a", session_fence=1, ttl=900)
        try:
            call(lease, token, clock)
        except Exception as exc:
            fails.append("b9 a window-row write that %s stopped the call (%r)" % ("raises" if mode == "raise" else "keeps failing its swap", getattr(exc, "code", exc)))
    return fails


def arms_guard(mod):
    fails = []
    # g1: no budget = today: 20 spaced calls pass, ONE store row, eight keys.
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
    if len(store.rows) != 1 or set(store.lease_row()) != BASE_KEYS:
        fails.append("g1 no budget: %d store rows, lease row keys %r (want one row, exactly the eight keys)" % (len(store.rows), sorted(store.lease_row())))
    if "window_budget" not in inspect.signature(mod.OperationLease.__init__).parameters:
        return fails
    # g2: OPERATION_SPACING comes before the budget and consumes no count (design-neutral: after the refused call, two more calls pass and the next is refused).
    clock, store = [100.0], Store()
    lease = make(mod, store, clock, (3, 100.0))
    token = lease.acquire("holder-a", session_fence=1, ttl=900)
    call(lease, token, clock)
    clock[0] += 1
    code, _ = code_of(lambda: lease.reserve(token, hard_deadline=clock[0] + 30))
    if code != "OPERATION_SPACING":
        fails.append("g2 a call 1 s after the last gives %r (want OPERATION_SPACING)" % (code,))
    outcomes = []
    for _ in range(3):
        clock[0] += 3
        outcomes.append(code_of(lambda: call(lease, token, clock))[0])
    if outcomes != [None, None, "OPERATION_WINDOW_BUDGET"]:
        fails.append("g2 after the spacing refusal the next three calls gave %r (want two passes then OPERATION_WINDOW_BUDGET: the refusal consumed no count)" % (outcomes,))
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
        print("AR-G146-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G146-FAIL usage: build | guard | scope | regress")
        return 2
    mod = load()
    try:
        fails = arms_build(mod) if mode == "build" else arms_guard(mod)
    except Exception as exc:  # a crash inside an arm is a failed check, named
        fails = ["the check crashed: %s: %s" % (type(exc).__name__, exc)]
    print("AR-G146-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
