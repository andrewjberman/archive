"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the CTO's second FWD-10/FWD-9 rulings (msg 11980). READ ONLY, offline, no AWS.
Needs a python with pytest, jsonschema and pypdf-free tests (the repository's producer tests), not `-I`.

    python ar_enrich2_checks.py excl [--root <lambda tree root>]
    python ar_enrich2_checks.py p21 [--root <lambda tree root>]
    python ar_enrich2_checks.py tests191 [--root <lambda tree root>]
    python ar_enrich2_checks.py tests192 [--root <lambda tree root>]

`excl` (cell AR-g-191): a kept row left out of the figures is named on the page. The REAL producer runs an Overview (the real overview map, a
ten-year synthetic price history) and a Multi-Comp (the real multi map, two models) over a request with two UNRESOLVED holdings: ZQXWVK (the
classifier holds nothing for it, so the swap pass leaves it out: reason code NO_CLASS) and QQQ (replaced by DDD from the pool). The page must carry
exactly ONE line `Left out of all figures: ZQXWVK, no asset class is held for it.` inside the section of the page that holds the first
`Top 10 Holdings` element, naming no replaced row and no amount; a run with no left-out row prints no such line.
`p21` (cell AR-g-192): the six Risk Info tables of the Overview (Alpha, Beta, Sharpe, Sortino, Max Drawdown, Monthly VaR; map elements p7.e02,
p7.e03, p7.e05, p7.e06, p7.e07, p7.e08) name BOTH `columns` and a `statistic`; the producer takes the statistic path and a scalar reaches a table
element, which prints "The kept answer is not a readable table." (measured on run 7L: six times). Each must print a table with one row per
column, labelled `<Statistic> <period>` (Alpha 1Y, Alpha 3Y, ...), the cells a number or `n/a`; the phrase must not occur.
`tests191` / `tests192`: the owned test files pass and at least the baseline plus the new tests ran.
Prints one RESULT line: AR-ENRICH2-<arm>-OK or AR-ENRICH2-<arm>-FAIL <why>. ASCII only.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
TREE = "infra/aws/lambda/investor-reporting"
MAPS = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps"
TESTS = {"tests191": (["ycharts/research/tests/test_layout_excluded_line.py"], 4),
         "tests192": (["ycharts/research/tests/test_layout_own_series_columns.py", "ycharts/research/tests/test_layout_overview.py"], 60)}
MONTHS = 130
FACT = {"AAA": lambda k: 0.90 if k % 40 == 20 else 1.012, "BBB": lambda k: 1.006 if k % 3 else 0.995, "CCC": lambda k: 1.009,
        "DDD": lambda k: 1.007, "SPY": lambda k: 1.008 if k % 5 else 0.985, "BIL": lambda k: 1.0003}
EXCL_PREFIX = "Left out of all figures:"
EXCL_LINE = "Left out of all figures: ZQXWVK, no asset class is held for it."
RISK = (("p7.e02", "Alpha", ("1Y", "3Y", "5Y", "10Y", "15Y")), ("p7.e03", "Beta", ("1Y", "3Y", "5Y", "10Y", "15Y")),
        ("p7.e05", "Sharpe", ("1Y", "3Y", "5Y", "10Y", "15Y")), ("p7.e06", "Sortino", ("1Y", "3Y", "5Y", "10Y", "15Y")),
        ("p7.e07", "Max drawdown", ("1Y", "3Y", "5Y", "10Y", "15Y")), ("p7.e08", "Var monthly", ("1Y", "3Y", "5Y", "10Y", "15Y")))


def fail(arm, why):
    print("AR-ENRICH2-%s-FAIL %s" % (arm, why))
    sys.exit(1)


def paths(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    here = os.path.join(base, "ycharts/research")
    sys.path[:0] = [os.path.join(here, "tests"), here, os.path.join(base, "ycharts/session"), os.path.join(base, "ycharts/generate"),
                    os.path.join(base, "ycharts/extract"), os.path.join(base, "reports"), os.path.join(base, "lib"), os.path.join(base, "ops"),
                    os.path.join(base, "intake"), os.path.join(base, "_scope"), os.path.join(base, "_ids"), os.path.join(base, "_keys"),
                    os.path.join(base, "_authz"), base]
    return base


def day(k):
    total = 2016 * 12 + 9 + k
    return "%04d-%02d-14" % (total // 12, total % 12 + 1)


def price_tables():
    out = {}
    for sym, f in FACT.items():
        rows, v = [], 100.0
        for k in range(MONTHS):
            if k:
                v *= f(k)
            rows.append((day(k), v))
        out[sym] = rows
    return out


def load_map(root, name):
    for base in (root, REPO):
        p = os.path.join(base, MAPS, name)
        if os.path.isfile(p):
            return json.load(open(p, encoding="utf-8"))
    fail("map", "map %s not found under %s or %s" % (name, root, REPO))


def overview_html(root, swap_rows, mapname="overview_map.json", comparables=None, model_bytes=None):
    """Runs the REAL producer; -> the HTML. swap_rows: the (ticker, amount) UNRESOLVED rows appended to the frozen input."""
    import test_opal_producer as tp
    import test_opal_producer_swap as ts
    tmp = tempfile.mkdtemp()
    tbl = price_tables()
    world = ts._world(swap_rows)
    stores = ts._stores(world, __import__("pathlib").Path(tmp))
    stores.update(map=load_map(root, mapname), pricing=True, as_of=day(MONTHS - 1),
                  price_readers={"estate": lambda symbol, start, end: list(tbl.get(symbol, []))})
    if comparables is not None:
        stores.update(comparables=comparables, model_bytes=model_bytes)
    tp.op.produce(tp.REQ, tp.FIRM, stores)
    return "".join(stores["html"])


def page_of(html, needle):
    """The <section class="page"> chunk that holds `needle`, or None."""
    for chunk in re.split(r'(?=<section class="page")', html):
        if needle in chunk:
            return chunk
    return None


def arm_excl(root):
    paths(root)
    problems = []
    cases = [("overview", dict(swap_rows=[("ZQXWVK", "125"), ("QQQ", "250")])),
             ("multicomp", None)]
    import test_compare_producer as tc
    for tag, kw in cases:
        try:
            if tag == "overview":
                html = overview_html(root, **kw)
            else:
                html = overview_html(root, [("ZQXWVK", "125"), ("QQQ", "250")], mapname="multi_map.json", comparables=tc.ENTRIES[:2],
                                     model_bytes=tc._model_bytes())
        except Exception as exc:  # noqa: BLE001
            problems.append("%s: the producer raised %s: %s" % (tag, type(exc).__name__, str(exc)[:120]))
            continue
        n = html.count(EXCL_PREFIX)
        if n != 1:
            problems.append("%s: the left-out line occurs %d times (want 1)" % (tag, n))
            continue
        if EXCL_LINE not in html:
            problems.append("%s: the line is not exactly %r" % (tag, EXCL_LINE))
        holder = page_of(html, "Top 10 Holdings")
        if holder is None or EXCL_PREFIX not in holder:
            problems.append("%s: the line is not on the page that holds the Top 10 Holdings element" % tag)
        line = html[html.find(EXCL_PREFIX): html.find(EXCL_PREFIX) + 160].split("<")[0]
        if "QQQ" in line or "125" in line or "250" in line:
            problems.append("%s: the line names a replaced row or an amount: %r" % (tag, line))
    try:
        clean = overview_html(root, [("QQQ", "250")])
        if EXCL_PREFIX in clean:
            problems.append("a run with no left-out row prints the line")
    except Exception as exc:  # noqa: BLE001
        problems.append("clean run raised %s: %s" % (type(exc).__name__, str(exc)[:120]))
    if problems:
        fail("excl", "; ".join(problems))
    print("AR-ENRICH2-excl-OK")


def arm_p21(root):
    paths(root)
    import test_opal_producer as tp
    tbl = price_tables()
    stores = tp.make_stores(classifier=tp.FakeClassifier(), map=load_map(root, "overview_map.json"), pricing=True, as_of=day(MONTHS - 1),
                            price_readers={"estate": lambda symbol, start, end: list(tbl.get(symbol, []))})
    try:
        tp.op.produce(tp.REQ, tp.FIRM, stores)
    except Exception as exc:  # noqa: BLE001
        fail("p21", "the producer raised %s: %s" % (type(exc).__name__, str(exc)[:120]))
    html = "".join(stores["html"])
    problems = []
    n = html.count("not a readable table")
    if n:
        problems.append("the phrase 'not a readable table' occurs %d times" % n)
    for eid, stat, periods in RISK:
        m = re.search(r'<div class="el" data-id="%s">(.*?)</div>' % re.escape(eid), html, re.S)
        if m is None:
            problems.append("%s: element missing" % eid)
            continue
        body = m.group(1)
        rows = re.findall(r"<tr><td>([^<]*)</td><td>([^<]*)</td></tr>", body)
        labels = [r[0] for r in rows]
        want = ["%s %s" % (stat, p) for p in periods]
        if [x.lower() for x in labels] != [x.lower() for x in want]:
            problems.append("%s: rows %r, want %r" % (eid, labels, want))
            continue
        bad = [c for _, c in rows if c != "n/a" and not re.fullmatch(r"-?[0-9]+(\.[0-9]+)?", c)]
        if bad:
            problems.append("%s: cells that are neither a number nor n/a: %r" % (eid, bad))
        if all(c == "n/a" for _, c in rows):
            problems.append("%s: every cell is n/a on a ten-year history" % eid)
    if problems:
        fail("p21", "; ".join(problems))
    print("AR-ENRICH2-p21-OK")


def arm_tests(arm, root):
    files, minimum = TESTS[arm]
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + files
    run = subprocess.run(cmd, capture_output=True, text=True, cwd=base)
    found = re.findall(r"(\d+) passed", run.stdout)
    passed = int(found[-1]) if found else 0
    if run.returncode != 0 or passed < minimum or (not files):
        print("AR-ENRICH2-%s-FAIL rc=%d passed=%d (want rc 0 and at least %d): %s" % (arm, run.returncode, passed, minimum,
              " ".join(run.stdout.strip().splitlines()[-2:])[:200]))
        sys.exit(1)
    print("AR-ENRICH2-%s-OK passed=%d" % (arm, passed))


def main():
    arms = ("excl", "p21", "tests191", "tests192")
    if len(sys.argv) < 2 or sys.argv[1] not in arms:
        print("usage: ar_enrich2_checks.py %s [--root <root>]" % "|".join(arms))
        sys.exit(2)
    root = REPO
    if "--root" in sys.argv:
        root = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
    arm = sys.argv[1]
    if arm.startswith("tests"):
        arm_tests(arm, root)
    else:
        {"excl": arm_excl, "p21": arm_p21}[arm](root)


if __name__ == "__main__":
    main()
