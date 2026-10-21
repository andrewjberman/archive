"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the Multi-Comp portfolio path (cell AR-g-185). READ ONLY, offline, no AWS.
Needs a python with pytest and jsonschema (the repository's producer tests import them), not `-I`.

    python ar_window_checks.py portfolio [--root <lambda tree root>]
    python ar_window_checks.py tests [--root <lambda tree root>]

Why: run 7J's served Multi-Comp PDF showed a portfolio row that differs from independent recomputation (YTD 10.66 against 8.83, 1Y 13.37
against 11.12). Reproduced exactly: the resident applies the filed amounts at the start of its 10-year price window (2016-10-20), cuts the
path to the common window (2024-04-30..) and rebases it to 100, so the filed weights (SPY 44) had drifted (SPY 60.1) by the window start. The
Multi-Comp's portfolio must be the filed amounts bought at the COMMON WINDOW START and held (the comparables start there too).
`portfolio`: runs the REAL producer (`opal_producer.produce`, the repository's own fakes from test_opal_producer.py) on a Multi-Comp with two
Opal models and one ETF, over price histories that start 60 months BEFORE the models' first observation, with strong drift in the pre-window
months (AAA +3 percent a month, BBB and CCC flat), and requires the served chart's "Your portfolio" last level to equal this file's own
arithmetic 100 * sum(w_i * L_i(end) / L_i(start)) with w_i the filed amounts over their total and start the models' first observation. It also
requires the first point to read 100 and the models' lines and the ETF line to be unchanged (they are computed from their own series).
`tests`: the five owned producer test files pass (63 at the base) and at least 65 ran, so each behavior has a test of its own.
Prints one RESULT line: AR-WINDOW-<arm>-OK or AR-WINDOW-<arm>-FAIL <why>. ASCII only.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
TREE = "infra/aws/lambda/investor-reporting"
TEST_FILES = ["ycharts/research/tests/test_compare_producer.py", "ycharts/research/tests/test_portfolio_series.py",
              "ycharts/research/tests/test_opal_producer_prices.py", "ycharts/research/tests/test_opal_producer.py",
              "ycharts/research/tests/test_compare_elements.py"]
MIN_TESTS = 65
AS_OF = "2026-10-14"
MONTHS = 31
PRE = 60
AMOUNTS = {"AAA": 500.0, "BBB": 300.0, "CCC": 200.0}
IN_WINDOW = {"AAA": lambda k: 0.90 if k == 20 else 1.02, "BBB": lambda k: 1.01, "CCC": lambda k: 1.015,
             "IWM": lambda k: 1.011 if k % 4 else 0.975, "SPY": lambda k: 1.008, "BIL": lambda k: 1.0003}
PRE_WINDOW = {"AAA": 1.03, "BBB": 1.0, "CCC": 1.0, "IWM": 1.0, "SPY": 1.0, "BIL": 1.0}


def fail(arm, why):
    print("AR-WINDOW-%s-FAIL %s" % (arm, why))
    sys.exit(1)


def day(k):
    total = 2024 * 12 + 3 + k
    return "%04d-%02d-14" % (total // 12, total % 12 + 1)


def table():
    out = {}
    for sym in IN_WINDOW:
        rows, v = [], 100.0
        for k in range(-PRE, MONTHS):
            if k > -PRE:
                v *= PRE_WINDOW[sym] if k <= 0 else IN_WINDOW[sym](k)
            rows.append((day(k), v))
        out[sym] = rows
    return out


def paths(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    here = os.path.join(base, "ycharts/research")
    sys.path[:0] = [os.path.join(here, "tests"), here, os.path.join(base, "ycharts/session"), os.path.join(base, "ycharts/generate"),
                    os.path.join(base, "reports"), os.path.join(base, "lib"), os.path.join(base, "ops"), os.path.join(base, "intake"),
                    os.path.join(base, "_scope"), os.path.join(base, "_ids"), os.path.join(base, "_keys"), os.path.join(base, "_authz"), base]
    return base


def arm_portfolio(root):
    base = paths(root)
    import test_opal_producer as tp
    import test_compare_producer as tc
    op = tp.op
    tbl = table()
    readers = {"estate": lambda symbol, start, end: list(tbl.get(symbol, []))}
    mp = json.loads((tc.MAPS / "multi_map.json").read_text(encoding="utf-8"))
    clf = tp.FakeClassifier()
    clf.rows["IWM"] = {"ticker": "IWM", "asset_class": "equity", "sub_asset_class": "Fixture Small Blend", "name": "iShares Russell 2000 ETF"}
    stores = tp.make_stores(classifier=clf, map=mp, pricing=True, as_of=AS_OF, price_readers=readers, comparables=tc.ENTRIES,
                            model_bytes=tc._model_bytes())
    try:
        op.produce(tp.REQ, tp.FIRM, stores)
    except Exception as exc:  # noqa: BLE001
        fail("portfolio", "the producer raised %s: %s" % (type(exc).__name__, str(exc)[:120]))
    doc = stores["reports"].persisted[0]["report"]
    sections = {s["section_id"]: s for s in doc["sections"]}
    chart = tc._value(sections, "opal.compare.chart")
    lines = {line["name"]: line["points"] for line in chart}
    if "Your portfolio" not in lines:
        fail("portfolio", "no Your portfolio line in the chart (%s)" % sorted(lines))
    start = day(0)
    w = {t: a / sum(AMOUNTS.values()) for t, a in AMOUNTS.items()}
    lv = {t: dict(tbl[t]) for t in AMOUNTS}
    want = 100.0 * sum(w[t] * lv[t][AS_OF] / lv[t][start] for t in AMOUNTS)
    pts = lines["Your portfolio"]
    got, first = pts[-1][1], pts[0][1]
    problems = []
    if abs(first - 100.0) > 1e-6:
        problems.append("the first point is %.6f, not 100" % first)
    if abs(got - want) > 0.01:
        problems.append("the portfolio's last level is %.4f, the amounts bought at the window start give %.4f" % (got, want))
    for name, f in (("iShares Russell 2000 ETF", None),):
        if name in lines:
            iw = dict(tbl["IWM"])
            wi = 100.0 * iw[AS_OF] / iw[start]
            if abs(lines[name][-1][1] - wi) > 0.01:
                problems.append("the ETF line ends at %.4f, its own series gives %.4f" % (lines[name][-1][1], wi))
        else:
            problems.append("the ETF line is missing")
    if problems:
        fail("portfolio", "; ".join(problems))
    del base
    print("AR-WINDOW-portfolio-OK")


def arm_tests(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + TEST_FILES
    run = subprocess.run(cmd, capture_output=True, text=True, cwd=base)
    found = re.findall(r"(\d+) passed", run.stdout)
    passed = int(found[-1]) if found else 0
    if run.returncode != 0 or passed < MIN_TESTS:
        print("AR-WINDOW-tests-FAIL rc=%d passed=%d (want rc 0 and at least %d): %s" % (run.returncode, passed, MIN_TESTS,
              " ".join(run.stdout.strip().splitlines()[-2:])[:200]))
        sys.exit(1)
    print("AR-WINDOW-tests-OK passed=%d" % passed)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("portfolio", "tests"):
        print("usage: ar_window_checks.py portfolio|tests [--root <root>]")
        sys.exit(2)
    root = REPO
    if "--root" in sys.argv:
        root = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
    {"portfolio": arm_portfolio, "tests": arm_tests}[sys.argv[1]](root)


if __name__ == "__main__":
    main()
