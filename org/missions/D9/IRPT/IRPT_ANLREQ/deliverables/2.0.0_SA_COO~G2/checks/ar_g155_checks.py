"""IRPT_ANLREQ AR-g-155 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g155_checks.py build   the YCharts price adapter asks YCharts in the estate client's own form, by CALLING the estate builder unchanged: a new module
                                     ycharts/research/price_form_ycharts.py subclasses ycharts_client.YChartsClient with __init__ skipped and _request returning the URL it is handed,
                                     calls the client's own fund_data(symbol, calc), and returns the URL's path and query (the client's BASE stripped); calc is "price" for every symbol
                                     except a "^" index ("level"); the symbol is stripped and upper-cased, a blank one raises ValueError. For SPY the path is BYTE-EQUAL to the request IB2's
                                     200 read made (PRICE_FORM_READ.txt, 41 parameters, urllib.parse.urlencode defaults, 760 characters). Building the path reads no secret and makes no network call.
                                     The adapter sends transport(path, {}) once per symbol. Two new test files exist (the form and a pin on the estate client's fund_data and _request
                                     signatures, because the subclass leans on a private method); the two existing tests that asserted the old forms assert the new one.
    python ar_g155_checks.py guard   nothing else moves: one transport call per symbol, the 2.0 s spacing sleep before every call but the first, a blank symbol gives [] with no call,
                                     a transport error propagates, a malformed or empty answer gives [], the window filter and the base-100 chaining give the same rows as before
    python ar_g155_checks.py regress each existing and new test file on its own, then the scope check
    python ar_g155_checks.py scope   the branch changed only the module, the adapter, three test files and two moved tests, the order and the worker's folder (against the merge-base with box/dell2)

Prints one RESULT line: AR-G155-OK / AR-G155-FAIL (or -REGRESS- / -SCOPE-); rc 0 only on OK. ASCII only.
"""
import os
import subprocess
import sys

IR = "infra/aws/lambda/investor-reporting/"
RES = IR + "ycharts/research/"
ADAPTER = RES + "price_adapter_ycharts.py"
FORM = RES + "price_form_ycharts.py"
NEW_TESTS = (RES + "tests/test_price_form_ycharts.py", RES + "tests/test_ycharts_client_pin.py")
MOVED_TESTS = (RES + "tests/test_price_adapter_ycharts.py", IR + "reports/tests/test_ycharts_price_tier.py")
OWN = (ADAPTER, FORM) + NEW_TESTS + MOVED_TESTS + ("org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-155.ycharts-price-estate-form.md",)
OWN_PREFIX = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~277/", "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~IB2/")
REGRESS_FILES = (RES + "tests/test_price_adapter_ycharts.py", RES + "tests/test_price_transport_ycharts.py", RES + "tests/test_price_source.py",
                 IR + "reports/tests/test_ycharts_price_tier.py", IR + "reports/tests/test_opal_pricing_binding.py")
ESTATE_DIR = "infra/aws/lambda/ycharts-market-data-pull"
# the request IB2's 200 read made for SPY (PRICE_FORM_READ.txt @52f06c5aa9, ycharts_price_probe3.sh @e04a2bcf14): fund_data(), calc price, urlencode defaults
EXPECT_SPY = "/charts/fund_data.json?aiSummaries=&calcs=id%3Aprice%2Cinclude%3Atrue%2C%2C&chartId=&chartType=interactive&correlations=&customGrowthAmount=&dataInLegend=value&dateSelection=range&displayDateRange=false&endDate=&format=real&legendOnChart=false&lineAnnotations=&nameInLegend=name_and_ticker&note=&partner=basic_2000&performanceDisclosure=false&quoteLegend=false&recessions=false&scaleType=linear&securities=id%3ASPY%2Cinclude%3Atrue%2C%2C&securityGroup=&securitylistName=&securitylistSecurityId=&source=false&splitType=single&startDate=&title=&units=false&useCustomColors=false&useEstimates=false&zoom=max&hideValueFlags=false&redesign=true&chartAnnotations=&axisExtremes=&sortColumn=&sortDirection=&le_o=quote_page_fund_data&maxPoints=100000&chartCreator=false"
FUND_SIG = "(self, yc_symbol: 'str', calc: 'str' = 'level', max_points: 'int' = 100000) -> 'dict'"
REQUEST_SIG = "(self, url: 'str', body: 'bytes | None' = None) -> 'dict'"


def setup_paths():
    for entry in (RES, IR + "lib", ESTATE_DIR):
        sys.path.insert(0, entry)


def answer(points):
    return {"chart_data": [[{"raw_data": [[ms, level] for ms, level in points]}]]}


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
    fails = []
    if not os.path.isfile(FORM):
        return ["%s does not exist" % FORM]
    setup_paths()
    import inspect
    import ycharts_client as yc
    if str(inspect.signature(yc.YChartsClient.fund_data)) != FUND_SIG or str(inspect.signature(yc.YChartsClient._request)) != REQUEST_SIG:
        fails.append("the estate client's fund_data or _request signature is not the pinned one: %s / %s" % (inspect.signature(yc.YChartsClient.fund_data), inspect.signature(yc.YChartsClient._request)))
    import price_form_ycharts as pf
    got = pf.request_path(" spy ")
    if got != EXPECT_SPY:
        fails.append("request_path(' spy ') is not byte-equal to IB2's 200 request: %r" % (got[:120],))
    lvl = pf.request_path("^spxtr")
    if "calcs=id%3Alevel%2Cinclude%3Atrue%2C%2C" not in lvl or "securities=id%3A%5ESPXTR%2Cinclude%3Atrue%2C%2C" not in lvl:
        fails.append("a ^ index does not get calc level: %r" % (lvl[:160],))
    if "calcs=id%3Aprice%2Cinclude%3Atrue%2C%2C" not in pf.request_path("AAPL") or "securities=id%3AAAPL%2C" not in pf.request_path("AAPL"):
        fails.append("a plain symbol does not get calc price")
    try:
        pf.request_path("  ")
        fails.append("a blank symbol did not raise")
    except ValueError:
        pass
    # no secret read, no network call
    import urllib.request

    class Boom(Exception):
        pass

    def no_open(*a, **k):
        raise Boom("urlopen called")
    real = urllib.request.urlopen
    fake_boto = type(sys)("boto3")

    def no_client(*a, **k):
        raise Boom("boto3.client called")
    fake_boto.client = no_client
    saved = sys.modules.get("boto3")
    urllib.request.urlopen = no_open
    sys.modules["boto3"] = fake_boto
    try:
        if pf.request_path("SPY") != EXPECT_SPY:
            fails.append("request_path changed between calls")
    except Boom as exc:
        fails.append("building the path reached the network or a secret: %s" % exc)
    finally:
        urllib.request.urlopen = real
        if saved is None:
            sys.modules.pop("boto3", None)
        else:
            sys.modules["boto3"] = saved
    calls, rows, _ = run_reader("spy", answer(POINTS))
    if calls != [(EXPECT_SPY, {})]:
        fails.append("the adapter's call is not (the SPY path, {}): %r" % (calls,))
    if len(rows) != 4:
        fails.append("the reader no longer returns the four served rows: %r" % (rows,))
    for rel in NEW_TESTS:
        if not os.path.isfile(rel):
            fails.append("%s does not exist" % rel)
    if os.path.isfile(NEW_TESTS[1]):
        text = open(NEW_TESTS[1], encoding="utf-8").read()
        if "inspect.signature" not in text or "fund_data" not in text or "_request" not in text:
            fails.append("%s does not pin the fund_data and _request signatures with inspect.signature" % NEW_TESTS[1])
    if os.path.isfile(NEW_TESTS[0]):
        text = open(NEW_TESTS[0], encoding="utf-8").read()
        if "aiSummaries=" not in text or "chartCreator=false" not in text:
            fails.append("%s does not hold the byte-equal SPY path" % NEW_TESTS[0])
    for rel in MOVED_TESTS:
        text = open(rel, encoding="utf-8").read()
        if "id:SPY,include:true,&zoom=max" in text or '"id:QQQ,include:true,"' in text:
            fails.append("%s still asserts an old form" % rel)
        if "quote_page_fund_data" not in text and "price_form_ycharts" not in text:
            fails.append("%s does not assert the new form" % rel)
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
    for path in REGRESS_FILES + tuple(p for p in NEW_TESTS if os.path.isfile(p)):
        out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", path], capture_output=True, text=True)
        if out.returncode != 0:
            fails.append("%s: rc=%d %s" % (path.rsplit("/", 1)[-1], out.returncode, (out.stdout or out.stderr).strip().splitlines()[-1:] or ""))
    return fails + scope()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode in ("scope", "regress"):
        fails = scope() if mode == "scope" else regress()
        print("AR-G155-%s-%s %s" % (mode.upper(), "FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    if mode not in ("build", "guard"):
        print("AR-G155-FAIL usage: build | guard | scope | regress")
        return 2
    fails = arms_build() if mode == "build" else arms_guard()
    print("AR-G155-%s %s: %s" % ("FAIL" if fails else "OK", mode, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
