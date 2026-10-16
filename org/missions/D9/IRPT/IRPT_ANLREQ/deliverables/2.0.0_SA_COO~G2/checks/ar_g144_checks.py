"""IRPT_ANLREQ AR-g-144 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g144_checks.py build   the resident carries the third price tier and the host's call budget: the bindings accept the tier "ycharts" and an optional
                                     ycharts_window_budget {"calls": int >= 1, "window_s": number > 0} (anything else is ResidentInstallRefused RESIDENT_WINDOW_BUDGET_BINDING); a new module
                                     ycharts/research/price_transport_ycharts.py turns the resident's stored session into the (path, params) transport the existing price_adapter_ycharts reader calls
                                     (one session.acquire per call, the query encoded as the research runner encodes it, the facade closed even when the call raises, a non-200 reply or a body that is not
                                     JSON raises); _pricing_extras(bindings, clients, clock, session=None) builds the "ycharts" reader from it and REFUSES a "ycharts" tier with no session
                                     (PRICING_YCHARTS_SESSION_REQUIRED); build_resident_runtime hands the budget to the ResidentSession it builds and the session to _pricing_extras
    python ar_g144_checks.py guard   nothing else moves: a bindings file with the two old tiers and no budget loads as before; an unknown tier is still refused; a disabled pricing binding still gives
                                     no extras; _pricing_extras without a ycharts tier works with no session
    python ar_g144_checks.py regress each existing pricing, price-source, adapter and session test file on its own, then the scope check
    python ar_g144_checks.py scope   the branch changed only resident_installed.py, the new transport module, their tests, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G144-OK / AR-G144-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile

IR = "infra/aws/lambda/investor-reporting/"
INSTALLED = IR + "reports/resident_installed.py"
TRANSPORT = IR + "ycharts/research/price_transport_ycharts.py"
STAGE_BINDINGS = "C:/dev/irpt-release-r34m/x34/reports/resident_bindings.json"  # the r34g package's own bindings: the fixture for the validator arms
OWN = (INSTALLED, TRANSPORT, IR + "reports/tests/test_opal_pricing_binding.py", IR + "reports/tests/test_ycharts_price_tier.py",
       IR + "ycharts/research/tests/test_price_transport_ycharts.py",
       "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-144.ycharts-price-tier-and-host-budget-binding.md")
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~271/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~272/",
              "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/")
REGRESS_FILES = (IR + "reports/tests/test_opal_pricing_binding.py", IR + "reports/tests/test_resident_r32_source.py", IR + "ycharts/research/tests/test_price_source.py",
                 IR + "ycharts/research/tests/test_price_adapter_ycharts.py", IR + "ycharts/session/tests/test_resident_session.py")


def setup_paths():
    for sub in ("", "reports", "ycharts/generate", "ycharts/session", "ycharts/extract", "ycharts/research", "_scope", "_ids", "_keys", "_authz", "intake", "ops", "lib"):
        sys.path.insert(0, IR + sub if sub else IR)


class Facade:
    """What session.acquire() returns: records the path it is asked for and answers a scripted (info, body), or raises."""

    def __init__(self, owner, reply):
        self.owner, self.reply, self.closed = owner, reply, False

    def request(self, path, method="GET", payload=None, content_type=None):
        self.owner.paths.append(path)
        if isinstance(self.reply, Exception):
            raise self.reply
        return self.reply

    def close(self):
        self.closed = True


class Session:
    def __init__(self, reply):
        self.reply, self.paths, self.facades, self.acquire_kwargs = reply, [], [], []

    def acquire(self, **kwargs):
        self.acquire_kwargs.append(kwargs)
        facade = Facade(self, self.reply)
        self.facades.append(facade)
        return facade


SERVED = {"chart_data": [[{"raw_data": [[1790000000000, 100.0], [1790086400000, 101.0], [1790172800000, 102.5]]}]]}


def ok_reply(answer=None):
    body = json.dumps(SERVED if answer is None else answer).encode()
    return {"status": 200, "content_type": "application/json", "bytes": len(body)}, body


def code_of(fn):
    try:
        fn()
    except Exception as exc:  # a refusal is whatever the code raises
        return str(exc), type(exc).__name__
    return None, None


def arms_build():
    fails = []
    setup_paths()
    import resident_installed as ri
    if not os.path.isfile(STAGE_BINDINGS):
        return ["the fixture bindings are absent: %s" % STAGE_BINDINGS]
    base = json.load(open(STAGE_BINDINGS, encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="g144_")
    try:
        def load(**changes):
            doc = json.loads(json.dumps(base))
            for key, value in changes.items():
                if value is None:
                    doc.pop(key, None)
                else:
                    doc[key] = value
            path = os.path.join(tmp, "b.json")
            json.dump(doc, open(path, "w", encoding="utf-8"))
            return ri.load_bindings(path)

        # b1: the tier and the budget binding.
        try:
            load(opal_pricing={"enabled": True, "tiers": ["estate", "yfinance", "ycharts"]}, ycharts_window_budget={"calls": 6, "window_s": 390})
            load(opal_pricing={"enabled": True, "tiers": ["ycharts"]})
        except Exception as exc:
            fails.append("b1 a valid ycharts tier / budget binding was refused: %s" % exc)
        for label, bad in (("not a dict", [6, 390]), ("extra key", {"calls": 6, "window_s": 390, "x": 1}), ("calls 0", {"calls": 0, "window_s": 390}),
                           ("calls bool", {"calls": True, "window_s": 390}), ("calls str", {"calls": "6", "window_s": 390}), ("calls float", {"calls": 2.5, "window_s": 390}),
                           ("window 0", {"calls": 6, "window_s": 0}), ("window negative", {"calls": 6, "window_s": -1}), ("window nan", {"calls": 6, "window_s": float("nan")}),
                           ("window str", {"calls": 6, "window_s": "390"}), ("window bool", {"calls": 6, "window_s": True}), ("missing window", {"calls": 6})):
            code, _ = code_of(lambda bad=bad: load(ycharts_window_budget=bad))
            if code != "RESIDENT_WINDOW_BUDGET_BINDING":
                fails.append("b1 budget %s gives %r (want RESIDENT_WINDOW_BUDGET_BINDING)" % (label, code))
        # b2: the transport module.
        try:
            import price_transport_ycharts as pt
        except ImportError as exc:
            return fails + ["b2 ycharts/research/price_transport_ycharts.py is missing: %s" % exc]
        session = Session(ok_reply())
        answer = pt.make_transport(session)("/charts/fund_data.json", {"securities": "id:SPY,include:true,", "zoom": "max"})
        if answer != SERVED:
            fails.append("b2 the transport did not return the parsed answer: %r" % (answer,))
        if session.paths != ["/charts/fund_data.json?securities=id:SPY,include:true,&zoom=max"]:
            fails.append("b2 the request path is %r (want the query encoded as the research runner does: urlencode with safe=':,')" % (session.paths,))
        if len(session.facades) != 1 or not session.facades[0].closed:
            fails.append("b2 one acquire per call and the facade closed after it: %d facades, closed %r" % (len(session.facades), [f.closed for f in session.facades]))
        for label, reply in (("an exception", RuntimeError("boom")), ("status 202", ({"status": 202}, b"[]")), ("status 429", ({"status": 429}, b"{}")),
                             ("a body that is not JSON", ({"status": 200}, b"<html>challenge</html>"))):
            session = Session(reply)
            code, _ = code_of(lambda session=session: pt.make_transport(session)("/charts/fund_data.json", {"securities": "id:SPY,"}))
            if code is None:
                fails.append("b2 %s did not raise" % label)
            if not session.facades or not session.facades[0].closed:
                fails.append("b2 %s left the facade open" % label)
        # b3: _pricing_extras builds the ycharts reader from a session; refuses a ycharts tier with no session.
        binding_doc = load(opal_pricing={"enabled": True, "tiers": ["ycharts"]})
        session = Session(ok_reply())
        try:
            extras = ri._pricing_extras(binding_doc, {"s3": object()}, lambda: 1790259200.0, session=session)
            built = extras()
            reader = built["price_readers"].get("ycharts")
            rows = reader("SPY", "2026-09-01", "2026-12-31") if callable(reader) else None
            if not callable(reader) or not isinstance(rows, list) or not rows or len(session.facades) != 1:
                fails.append("b3 the ycharts reader: callable %r rows %r facades %d (want one call and a non-empty list)" % (callable(reader), rows, len(session.facades)))
        except Exception as exc:
            fails.append("b3 _pricing_extras with a session raised %s: %s" % (type(exc).__name__, exc))
        code, _ = code_of(lambda: ri._pricing_extras(binding_doc, {"s3": object()}, lambda: 1790259200.0))
        if code != "PRICING_YCHARTS_SESSION_REQUIRED":
            fails.append("b3 a ycharts tier with no session gives %r (want PRICING_YCHARTS_SESSION_REQUIRED)" % (code,))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # b4: build_resident_runtime hands the budget to ResidentSession and the session to _pricing_extras (read from the source tree).
    tree = ast.parse(open(INSTALLED, encoding="utf-8").read())
    runtime = next((n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "build_resident_runtime"), None)
    if runtime is None:
        return fails + ["b4 build_resident_runtime not found"]
    calls = [n for n in ast.walk(runtime) if isinstance(n, ast.Call)]
    session_calls = [c for c in calls if getattr(c.func, "id", None) == "ResidentSession"]
    extras_calls = [c for c in calls if getattr(c.func, "id", None) == "_pricing_extras"]
    if len(session_calls) != 1 or "window_budget" not in [k.arg for k in session_calls[0].keywords]:
        fails.append("b4 the ResidentSession built by build_resident_runtime gets no window_budget")
    if len(extras_calls) != 1 or "session" not in [k.arg for k in extras_calls[0].keywords]:
        fails.append("b4 _pricing_extras is called without session=")
    return fails


def arms_guard():
    fails = []
    setup_paths()
    import resident_installed as ri
    if not os.path.isfile(STAGE_BINDINGS):
        return ["the fixture bindings are absent: %s" % STAGE_BINDINGS]
    base = json.load(open(STAGE_BINDINGS, encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="g144_")
    try:
        def load(doc):
            path = os.path.join(tmp, "b.json")
            json.dump(doc, open(path, "w", encoding="utf-8"))
            return ri.load_bindings(path)

        try:
            load(json.loads(json.dumps(base)))
        except Exception as exc:
            fails.append("g1 the shipped r34g bindings no longer load: %s" % exc)
        bad = json.loads(json.dumps(base))
        bad["opal_pricing"] = {"enabled": True, "tiers": ["estate", "bogus"]}
        code, _ = code_of(lambda: load(bad))
        if code != "RESIDENT_PRICING_BINDINGS":
            fails.append("g2 an unknown tier gives %r (want RESIDENT_PRICING_BINDINGS)" % (code,))
        off = {"opal_pricing": {"enabled": False, "tiers": ["estate", "yfinance"]}}
        if ri._pricing_extras(off, {"s3": object()}, lambda: 1790259200.0) is not None:
            fails.append("g3 a disabled pricing binding gives extras")
        two = {"opal_pricing": {"enabled": True, "tiers": ["yfinance"]}}
        try:
            extras = ri._pricing_extras(two, {"s3": object()}, lambda: 1790259200.0)
            if not callable(extras):
                fails.append("g4 an enabled two-tier binding with no session gives no extras callable")
        except Exception as exc:
            fails.append("g4 _pricing_extras without a ycharts tier and without a session raised %s" % exc)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
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
        print("AR-G144-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G144-FAIL usage: build | guard | scope | regress")
        return 2
    fails = arms_build() if mode == "build" else arms_guard()
    print("AR-G144-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
