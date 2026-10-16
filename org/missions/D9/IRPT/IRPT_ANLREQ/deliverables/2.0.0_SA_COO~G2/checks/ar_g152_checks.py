"""IRPT_ANLREQ AR-g-152 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g152_checks.py build   the YCharts price adapter sends the form the CRO's captured working series call uses (overview_map.json, call benchmark_level_series): path /charts/fund_data.json and params
                                     securities="id:<SYMBOL>,include:true,," (DOUBLE trailing comma), calcs="id:level,include:true,,", zoom="max", maxPoints="100000", partner="basic_2000", in that key order; the symbol is
                                     stripped and upper-cased; the encoded request path (urlencode, safe=":,") equals the recipe string; the existing offline tests of the adapter and of the resident's price tier
                                     assert that same form (they moved with the code)
    python ar_g152_checks.py guard   nothing else moves: one transport call per symbol, the spacing sleep before every call but the first, a blank symbol gives [] with no call, a transport error propagates,
                                     a malformed or empty answer gives [], the window filter and the base-100 chaining of the served levels give the same rows as before
    python ar_g152_checks.py regress each existing adapter, transport, price-source and tier test file on its own, then the scope check
    python ar_g152_checks.py scope   the branch changed only the adapter, its two tests, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G152-OK / AR-G152-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import ast
import subprocess
import sys
import urllib.parse

IR = "infra/aws/lambda/investor-reporting/"
ADAPTER = IR + "ycharts/research/price_adapter_ycharts.py"
OWN = (ADAPTER, IR + "ycharts/research/tests/test_price_adapter_ycharts.py", IR + "reports/tests/test_ycharts_price_tier.py",
       "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-152.ycharts-price-recipe-form.md")
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~276/", "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~IB2/")
REGRESS_FILES = (IR + "ycharts/research/tests/test_price_adapter_ycharts.py", IR + "ycharts/research/tests/test_price_transport_ycharts.py",
                 IR + "ycharts/research/tests/test_price_source.py", IR + "reports/tests/test_ycharts_price_tier.py", IR + "reports/tests/test_opal_pricing_binding.py")
RECIPE_KEYS = ["securities", "calcs", "zoom", "maxPoints", "partner"]


def recipe(symbol):
    return {"securities": "id:" + symbol + ",include:true,,", "calcs": "id:level,include:true,,", "zoom": "max", "maxPoints": "100000", "partner": "basic_2000"}


def setup_paths():
    for sub in ("ycharts/research", "lib"):
        sys.path.insert(0, IR + sub)


def answer(points):
    return {"chart_data": [[{"raw_data": [[ms, level] for ms, level in points]}]]}


# 2024-01-02 .. 2024-01-05 UTC midnights, levels 100, 101, 102.01, 103.0301 (1% a day)
DAY = 86400000
T0 = 1704153600000
POINTS = [(T0 + i * DAY, 100.0 * (1.01 ** i)) for i in range(4)]


def run_reader(symbol, reply, start="2024-01-01", end="2024-12-31", sleeps=None):
    import price_adapter_ycharts as pa
    calls = []

    def transport(path, params):
        calls.append((path, dict(params)))
        if isinstance(reply, Exception):
            raise reply
        return reply
    pauses = [] if sleeps is None else sleeps
    reader = pa.make_reader(transport, sleep=pauses.append)
    return calls, reader(symbol, start, end), reader


def arms_build():
    setup_paths()
    fails = []
    calls, rows, _ = run_reader(" spy ", answer(POINTS))
    want = [("/charts/fund_data.json", recipe("SPY"))]
    if calls != want:
        fails.append("the call is not the recipe form: %r" % (calls,))
    if calls and list(calls[0][1]) != RECIPE_KEYS:
        fails.append("the param keys are not in the recipe order: %r" % (list(calls[0][1]),))
    if calls:
        got = calls[0][0] + "?" + urllib.parse.urlencode(calls[0][1], safe=":,")
        wanted = "/charts/fund_data.json?securities=id:SPY,include:true,,&calcs=id:level,include:true,,&zoom=max&maxPoints=100000&partner=basic_2000"
        if got != wanted:
            fails.append("the encoded request is %r" % (got,))
    if len(rows) != 4:
        fails.append("the reader no longer returns the four served rows: %r" % (rows,))
    for rel in ("ycharts/research/tests/test_price_adapter_ycharts.py", "reports/tests/test_ycharts_price_tier.py"):
        text = open(IR + rel, encoding="utf-8").read()
        if "id:SPY,include:true,&zoom=max" in text or ('"id:QQQ,include:true,"' in text):
            fails.append("%s still asserts the old form" % rel)
        if "calcs" not in text:
            fails.append("%s does not assert the recipe form (no calcs)" % rel)
    return fails


def arms_guard():
    setup_paths()
    fails = []
    calls, rows, reader = run_reader("SPY", answer(POINTS))
    expect = [("2024-01-02", 100.0), ("2024-01-03", 101.0), ("2024-01-04", 102.01), ("2024-01-05", 103.0301)]
    if len(rows) != 4 or any(r[0] != e[0] or abs(r[1] - e[1]) > 1e-6 for r, e in zip(rows, expect)):
        fails.append("the base-100 rows moved: %r" % (rows,))
    pauses = []
    calls, rows, reader = run_reader("SPY", answer(POINTS), sleeps=pauses)
    if len(calls) != 1 or pauses:
        fails.append("the first symbol should make one call and sleep nothing: %d calls, sleeps %r" % (len(calls), pauses))
    reader("QQQ", "2024-01-01", "2024-12-31")
    if pauses != [2.0] or len(calls) != 2:
        fails.append("the second symbol should sleep once (2.0 s) and make one more call: sleeps %r, %d calls" % (pauses, len(calls)))
    calls, rows, _ = run_reader("  ", answer(POINTS))
    if calls or rows != []:
        fails.append("a blank symbol made a call or returned rows")
    try:
        run_reader("SPY", RuntimeError("PRICE_HTTP_400"))
        fails.append("a transport error was swallowed")
    except RuntimeError as exc:
        if str(exc) != "PRICE_HTTP_400":
            fails.append("the transport error changed: %r" % (exc,))
    for bad in ({}, {"chart_data": []}, answer([]), None):
        calls, rows, _ = run_reader("SPY", bad)
        if rows != []:
            fails.append("a malformed or empty answer %r gave rows" % (bad,))
    calls, rows, _ = run_reader("SPY", answer(POINTS), start="2024-01-03", end="2024-01-04")
    if [r[0] for r in rows] != ["2024-01-03", "2024-01-04"] or abs(rows[0][1] - 100.0) > 1e-9:
        fails.append("the window filter or the re-seeding at 100 moved: %r" % (rows,))
    tree = ast.parse(open(ADAPTER, encoding="utf-8").read())
    if not any(isinstance(n, ast.FunctionDef) and n.name == "make_reader" for n in ast.walk(tree)):
        fails.append("make_reader is gone")
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
        print("AR-G152-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G152-FAIL usage: build | guard | scope | regress")
        return 2
    fails = arms_build() if mode == "build" else arms_guard()
    print("AR-G152-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
