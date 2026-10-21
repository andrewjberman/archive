"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the report's presentation fixes (cell AR-g-186). READ ONLY, offline, no AWS.
Needs a python with pytest and jsonschema (the repository's producer tests import them), not `-I`.

    python ar_gapnote_checks.py gaps [--root <lambda tree root>]
    python ar_gapnote_checks.py placeholder [--root <lambda tree root>]
    python ar_gapnote_checks.py tests [--root <lambda tree root>]

Why: the read of run 7J's Multi-Comp PDF (FWD10_READ_RUN7J_20261021.md) found (1) the line "Not available: no row of this section has a value."
printed under the periodic-returns, risk and allocation tables of a section whose rows all carry values, while the only real gaps (the 3Y, 5Y and
10Y cells) read a bare n/a with no words; (2) the heading "Comparison: asset allocation" stranded at the bottom of a page with its table on the
next; and the 7f Overview sample prints the raw template placeholder `{portfolio_name}` in element labels (page 3: "Periodic Return - Total:
{portfolio_name}").
`gaps`: the REAL producer on a Multi-Comp (the repository's fakes; two Opal models and one ETF over a 31-month common window), its served HTML:
  (a) the text "no row of this section has a value" appears nowhere (every row of this fixture has values);
  (b) the periodic-returns element carries the line "Not available: 3Y, 5Y and 10Y returns, because the common window is shorter than those
      periods." exactly once (3Y, 5Y and 10Y are the periods longer than the window; 1M to 1Y have values);
  (c) each of the five comparison elements is rendered with class "el cmp", and the page style holds a rule `.cmp` with `break-inside: avoid`
      and `page-break-inside: avoid`, so a heading is never left apart from its table or chart.
`placeholder`: the REAL producer on an Overview (the repository's fakes, the real overview map): the served HTML contains no `{portfolio_name}`,
  the label that read "Periodic Return - Total: {portfolio_name}" reads "Periodic Return - Total: Your portfolio", and the same replacement
  holds for every element label.
`tests`: the four owned layout test files pass (77 at the base) and at least 80 ran.
Prints one RESULT line: AR-GAPNOTE-<arm>-OK or AR-GAPNOTE-<arm>-FAIL <why>. ASCII only.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
TREE = "infra/aws/lambda/investor-reporting"
TEST_FILES = ["ycharts/research/tests/test_layout_overview.py", "ycharts/research/tests/test_compare_elements.py",
              "ycharts/research/tests/test_opal_producer_page_wording.py", "ycharts/research/tests/test_compare_producer.py"]
MIN_TESTS = 80
EMPTY = "no row of this section has a value"
LINE = "Not available: 3Y, 5Y and 10Y returns, because the common window is shorter than those periods."


def fail(arm, why):
    print("AR-GAPNOTE-%s-FAIL %s" % (arm, why))
    sys.exit(1)


def paths(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    here = os.path.join(base, "ycharts/research")
    sys.path[:0] = [os.path.join(here, "tests"), here, os.path.join(base, "ycharts/session"), os.path.join(base, "ycharts/generate"),
                    os.path.join(base, "reports"), os.path.join(base, "lib"), os.path.join(base, "ops"), os.path.join(base, "intake"),
                    os.path.join(base, "_scope"), os.path.join(base, "_ids"), os.path.join(base, "_keys"), os.path.join(base, "_authz"), base]


def served_html(multicomp):
    import test_opal_producer as tp
    import test_compare_producer as tc
    op = tp.op
    if multicomp:
        stores = tc._stores()
    else:
        stores = tc._stores(map_name="overview_map.json", comparables=None, pricing=True)
    try:
        op.produce(tp.REQ, tp.FIRM, stores)
    except Exception as exc:  # noqa: BLE001
        fail("gaps" if multicomp else "placeholder", "the producer raised %s: %s" % (type(exc).__name__, str(exc)[:120]))
    return "".join(stores["html"])


def arm_gaps(root):
    paths(root)
    html = served_html(True)
    problems = []
    if EMPTY in html:
        problems.append("the false sentence '%s' is still printed %d time(s)" % (EMPTY, html.count(EMPTY)))
    if html.count(LINE) != 1:
        problems.append("the line about 3Y, 5Y and 10Y appears %d times (want 1)" % html.count(LINE))
    ids = re.findall(r'<div class="([^"]*)" data-id="opal\.compare\.[a-z]+"', html)
    if len(ids) != 5 or any(c.split() != ["el", "cmp"] for c in ids):
        problems.append("the five comparison elements carry classes %s (want five of 'el cmp')" % ids)
    rule = re.search(r"\.cmp\s*\{([^}]*)\}", html)
    if not rule or not re.search(r"break-inside:\s*avoid", rule.group(1)) or not re.search(r"page-break-inside:\s*avoid", rule.group(1)):
        problems.append("the page style has no .cmp rule with break-inside: avoid and page-break-inside: avoid")
    if problems:
        fail("gaps", "; ".join(problems))
    print("AR-GAPNOTE-gaps-OK")


def arm_placeholder(root):
    paths(root)
    html = served_html(False)
    problems = []
    if "{portfolio_name}" in html:
        problems.append("the raw placeholder {portfolio_name} is printed %d time(s)" % html.count("{portfolio_name}"))
    if "Periodic Return - Total: Your portfolio" not in html:
        problems.append("the label 'Periodic Return - Total: Your portfolio' is not printed")
    if problems:
        fail("placeholder", "; ".join(problems))
    print("AR-GAPNOTE-placeholder-OK")


def arm_tests(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + TEST_FILES
    run = subprocess.run(cmd, capture_output=True, text=True, cwd=base)
    found = re.findall(r"(\d+) passed", run.stdout)
    passed = int(found[-1]) if found else 0
    if run.returncode != 0 or passed < MIN_TESTS:
        print("AR-GAPNOTE-tests-FAIL rc=%d passed=%d (want rc 0 and at least %d): %s" % (run.returncode, passed, MIN_TESTS,
              " ".join(run.stdout.strip().splitlines()[-2:])[:200]))
        sys.exit(1)
    print("AR-GAPNOTE-tests-OK passed=%d" % passed)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("gaps", "placeholder", "tests"):
        print("usage: ar_gapnote_checks.py gaps|placeholder|tests [--root <root>]")
        sys.exit(2)
    root = REPO
    if "--root" in sys.argv:
        root = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
    {"gaps": arm_gaps, "placeholder": arm_placeholder, "tests": arm_tests}[sys.argv[1]](root)


if __name__ == "__main__":
    main()
