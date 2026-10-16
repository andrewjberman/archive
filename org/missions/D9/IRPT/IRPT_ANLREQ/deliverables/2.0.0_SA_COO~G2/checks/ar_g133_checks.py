"""IRPT_ANLREQ AR-g-133 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g133_checks.py build   the door asks yfinance FIRST: SecurityResolver.check with a checker sends every uncached symbol to the checker in ONE batch,
                                     a symbol the checker KEPT never reaches the provider (price_source yfinance, provider_receipt None, the same KEPT row as before),
                                     only the rest go to the provider in one call, a provider FOUND beats a NOT_KEPT, a provider NOT_FOUND after a NOT_KEPT stays
                                     NOT_FOUND with NO second checker call, a CHECK_FAILED / NOT_CHECKED symbol the provider does not find reads UNAVAILABLE with its
                                     reason as before, and verified_suggestions shows a candidate the checker KEPT as well as one the provider FOUND
    python ar_g133_checks.py guard   nothing else moves: no checker = the resolver of today (one provider call with every pending symbol, identity port asked for
                                     a NOT_FOUND), a cached FOUND and a cached KEPT are served with no call at all, a provider outage leaves a non-kept symbol
                                     UNAVAILABLE and never NOT_FOUND, a checker that raises sends everything to the provider
    python ar_g133_checks.py regress each existing resolver test file on its own, then the scope check
    python ar_g133_checks.py scope   the branch changed only security_resolution.py, its tests, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G133-OK / AR-G133-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import copy
import importlib.util
import subprocess
import sys

IR = "infra/aws/lambda/investor-reporting/"
MODULE = IR + "intake/security_resolution.py"
TESTS = IR + "intake/tests/"
OWN = (MODULE, TESTS + "test_security_resolution.py", TESTS + "test_kept_holding.py", TESTS + "test_registry_known.py", TESTS + "test_door_yfinance_first.py",
       "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-133.door-asks-yfinance-first.md")
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~265/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~266/",
              "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/task_orders/")
REGRESS_FILES = (TESTS + "test_security_resolution.py", TESTS + "test_kept_holding.py", TESTS + "test_registry_known.py", TESTS + "test_yfinance_check.py",
                 IR + "ycharts/session/tests/test_resolution_broker.py")
ACCOUNT, REVISION = "fixture-account", "lookup-v1"


def load():
    spec = importlib.util.spec_from_file_location("security_resolution_g133", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def provider_row(symbol):
    return {"id": symbol, "security_id": symbol, "securitylist_security_id": "C12", "security_name": "fixture",
            "detailed_security_type": "stock", "features_needed": []}


class Provider:
    """The provider port: records each call, answers FOUND for the symbols in `found`, or raises when `boom`."""

    def __init__(self, found=(), boom=False):
        self.found, self.boom, self.calls = set(found), boom, []

    def __call__(self, symbols):
        self.calls.append(list(symbols))
        if self.boom:
            raise RuntimeError("provider outage")
        return {"http_status": 200, "complete": True, "final_url_path": "/securities/securities_info", "account_id": ACCOUNT,
                "source_revision": REVISION, "requested": list(symbols), "observed_at": "2026-10-16T15:00:00Z",
                "json": [provider_row(s) for s in symbols if s in self.found]}


class Checker:
    """The checker port: records each call and answers from `plan` {symbol: entry}; `boom` makes it raise."""

    def __init__(self, plan=None, boom=False):
        self.plan, self.boom, self.calls = plan or {}, boom, []

    def check(self, symbols):
        self.calls.append(list(symbols))
        if self.boom:
            raise RuntimeError("yahoo outage")
        return {s: copy.deepcopy(self.plan.get(s, {"state": "NOT_KEPT"})) for s in symbols}


class Cache:
    def __init__(self):
        self.rows = {}

    def get(self, key):
        return copy.deepcopy(self.rows.get(key))

    def put(self, key, value):
        self.rows[key] = copy.deepcopy(value)


KEPT = {"state": "KEPT", "rows": 5, "last_close": 10.5}


def resolver(mod, provider, checker, cache=None):
    return mod.SecurityResolver(provider_check=provider, identity=lambda symbol, kind: None, cache=cache, clock=lambda: 1000.0,
                                account_id=ACCOUNT, source_revision=REVISION, checker=checker)


def by_symbol(out):
    return {row["symbol"]: row for row in out["results"]}


def arms_build(mod):
    fails = []
    # b1: a mixed batch. ONE checker call with every symbol, the provider asked only about the one not kept.
    provider, checker = Provider(), Checker({"AAA": KEPT, "CCC": KEPT})
    out = resolver(mod, provider, checker).check(["AAA", "BBB", "CCC"])
    rows = by_symbol(out)
    if checker.calls != [["AAA", "BBB", "CCC"]]:
        fails.append("b1 the checker was called %r (want one call with all three)" % (checker.calls,))
    if provider.calls != [["BBB"]]:
        fails.append("b1 the provider was called %r (want one call with only BBB)" % (provider.calls,))
    for symbol in ("AAA", "CCC"):
        row = rows.get(symbol, {})
        if (row.get("state"), row.get("reason"), row.get("price_source"), row.get("provider_receipt")) != ("KEPT", "YFINANCE_HISTORY", "yfinance", None):
            fails.append("b1 %s is not the KEPT row: %r" % (symbol, {k: row.get(k) for k in ("state", "reason", "price_source", "provider_receipt")}))
        if row.get("checker") != {"rows": 5, "last_close": 10.5}:
            fails.append("b1 %s carries checker %r" % (symbol, row.get("checker")))
    if rows.get("BBB", {}).get("state") != "NOT_FOUND":
        fails.append("b1 BBB reads %r (want NOT_FOUND)" % (rows.get("BBB", {}).get("state"),))
    if out.get("provider_requested_count") != 1 or out.get("counts", {}).get("KEPT") != 2:
        fails.append("b1 counts: provider_requested_count %r KEPT %r (want 1 and 2)" % (out.get("provider_requested_count"), out.get("counts", {}).get("KEPT")))
    # b2: every symbol kept -> the provider is never called.
    provider, checker = Provider(), Checker({"AAA": KEPT, "BBB": KEPT})
    out = resolver(mod, provider, checker).check(["AAA", "BBB"])
    if provider.calls or out.get("provider_requested_count") != 0 or any(r["state"] != "KEPT" for r in out["results"]):
        fails.append("b2 all kept: provider calls %r, requested %r, states %r" % (provider.calls, out.get("provider_requested_count"), [r["state"] for r in out["results"]]))
    # b3: a provider FOUND beats a NOT_KEPT, and the checker is not asked a second time.
    provider, checker = Provider(found=["BBB"]), Checker({"AAA": KEPT})
    out = resolver(mod, provider, checker).check(["AAA", "BBB"])
    rows = by_symbol(out)
    if rows.get("BBB", {}).get("state") != "FOUND" or len(checker.calls) != 1:
        fails.append("b3 BBB %r after %d checker call(s) (want FOUND after exactly 1)" % (rows.get("BBB", {}).get("state"), len(checker.calls)))
    # b4: the checker raises -> every symbol goes to the provider; what it does not find reads UNAVAILABLE / YFINANCE_CHECK_FAILED / EXCEPTION as before.
    provider, checker = Provider(found=["AAA"]), Checker(boom=True)
    out = resolver(mod, provider, checker).check(["AAA", "BBB"])
    rows = by_symbol(out)
    if provider.calls != [["AAA", "BBB"]] or rows.get("AAA", {}).get("state") != "FOUND":
        fails.append("b4 raised checker: provider calls %r AAA %r (want one call with both, FOUND)" % (provider.calls, rows.get("AAA", {}).get("state")))
    if (rows.get("BBB", {}).get("state"), rows.get("BBB", {}).get("reason"), rows.get("BBB", {}).get("check_failed")) != ("UNAVAILABLE", "YFINANCE_CHECK_FAILED", "EXCEPTION"):
        fails.append("b4 raised checker: BBB reads %r" % ({k: rows.get("BBB", {}).get(k) for k in ("state", "reason", "check_failed")},))
    # b5: CHECK_FAILED and NOT_CHECKED symbols the provider does not find keep their reason words.
    provider = Provider()
    checker = Checker({"AAA": {"state": "CHECK_FAILED", "reason": "PUSHBACK"}, "BBB": {"state": "NOT_CHECKED"}})
    out = resolver(mod, provider, checker).check(["AAA", "BBB"])
    rows = by_symbol(out)
    if provider.calls != [["AAA", "BBB"]] or len(checker.calls) != 1:
        fails.append("b5 provider calls %r, checker calls %d (want one each, both symbols to the provider)" % (provider.calls, len(checker.calls)))
    if (rows.get("AAA", {}).get("state"), rows.get("AAA", {}).get("reason"), rows.get("AAA", {}).get("check_failed")) != ("UNAVAILABLE", "YFINANCE_CHECK_FAILED", "PUSHBACK"):
        fails.append("b5 AAA reads %r" % ({k: rows.get("AAA", {}).get(k) for k in ("state", "reason", "check_failed")},))
    if (rows.get("BBB", {}).get("state"), rows.get("BBB", {}).get("reason"), rows.get("BBB", {}).get("not_checked")) != ("UNAVAILABLE", "YFINANCE_NOT_CHECKED", "UPLOAD_LIMIT"):
        fails.append("b5 BBB reads %r" % ({k: rows.get("BBB", {}).get(k) for k in ("state", "reason", "not_checked")},))
    # b6: a suggestion the checker KEPT is displayed, like one the provider FOUND.
    provider, checker = Provider(found=["BBB"]), Checker({"AAA": KEPT})
    shown = mod.verified_suggestions([{"symbol": "AAA"}, {"symbol": "BBB"}, {"symbol": "CCC"}], resolver(mod, provider, checker))
    if [s["suggestion"]["symbol"] for s in shown] != ["AAA", "BBB"]:
        fails.append("b6 verified_suggestions shows %r (want AAA kept and BBB found, not CCC)" % ([s["suggestion"]["symbol"] for s in shown],))
    # b7: a provider outage does not touch what the checker kept (it is KEPT without the provider).
    provider, checker = Provider(boom=True), Checker({"AAA": KEPT})
    rows = by_symbol(resolver(mod, provider, checker).check(["AAA", "BBB"]))
    if rows["AAA"]["state"] != "KEPT":
        fails.append("b7 outage: AAA reads %r (want KEPT)" % (rows["AAA"]["state"],))
    return fails


def arms_guard(mod):
    fails = []
    # g1: no checker = the resolver of today.
    provider = Provider(found=["AAA"])
    out = resolver(mod, provider, None).check(["AAA", "BBB"])
    rows = by_symbol(out)
    if provider.calls != [["AAA", "BBB"]] or rows["AAA"]["state"] != "FOUND" or rows["BBB"]["state"] != "NOT_FOUND" or "reference" not in rows["BBB"]:
        fails.append("g1 no checker: provider calls %r states %r" % (provider.calls, {s: r["state"] for s, r in rows.items()}))
    # g2: a cached FOUND and a cached KEPT are served with no call at all, with the checker present.
    cache = Cache()
    resolver(mod, Provider(found=["AAA"]), None, cache).check(["AAA"])
    provider, checker = Provider(), Checker({"BBB": KEPT})
    first = resolver(mod, provider, checker, cache).check(["AAA", "BBB"])
    again_provider, again_checker = Provider(), Checker()
    again = by_symbol(resolver(mod, again_provider, again_checker, cache).check(["AAA", "BBB"]))
    if again_provider.calls or again_checker.calls or again["AAA"]["state"] != "FOUND" or again["BBB"]["state"] != "KEPT" or not again["AAA"]["cache_hit"] or not again["BBB"]["cache_hit"]:
        fails.append("g2 cached answers: provider calls %r checker calls %r states %r" % (again_provider.calls, again_checker.calls, {s: r["state"] for s, r in again.items()}))
    if by_symbol(first)["AAA"]["state"] != "FOUND" or checker.calls != [["BBB"]]:
        fails.append("g2 first pass: AAA %r, checker calls %r (want FOUND from cache, the checker asked only about BBB)" % (by_symbol(first)["AAA"]["state"], checker.calls))
    # g3: a provider outage leaves a symbol the checker did not keep UNAVAILABLE, never NOT_FOUND.
    provider, checker = Provider(boom=True), Checker({"AAA": KEPT})
    rows = by_symbol(resolver(mod, provider, checker).check(["AAA", "BBB"]))
    if rows["BBB"]["state"] != "UNAVAILABLE":
        fails.append("g3 outage: BBB reads %r (want UNAVAILABLE)" % (rows["BBB"]["state"],))
    # g4: the same symbol twice is one checker entry and one result per position.
    provider, checker = Provider(), Checker({"AAA": KEPT})
    out = resolver(mod, provider, checker).check(["AAA", "AAA"])
    if checker.calls != [["AAA"]] or out["requested_count"] != 2 or out["distinct_count"] != 1 or [r["state"] for r in out["results"]] != ["KEPT", "KEPT"]:
        fails.append("g4 duplicate symbol: checker calls %r, requested %r, distinct %r" % (checker.calls, out["requested_count"], out["distinct_count"]))
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
        print("AR-G133-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G133-FAIL usage: build | guard | scope | regress")
        return 2
    mod = load()
    fails = arms_build(mod) if mode == "build" else arms_guard(mod)
    print("AR-G133-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
