"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the comparison chart's series colours (cell AR-g-195, CTO ADJ v31 note on run 7M).
READ ONLY, offline, no AWS. Needs a python with pytest and jsonschema (the repository's producer tests import them), not `-I`.

    python ar_palette_checks.py palette [--root <lambda tree root>]
    python ar_palette_checks.py tests [--root <lambda tree root>]

Why: run 7M's chart drew Opal Long-Term in #0A1733 and the typed ETF in #000000, a contrast of 1.18:1, and the palette of four colours repeats from
the fifth line on (a Multi-Comp can carry six lines). `palette` runs the layout's own `_lines_svg` and `_legend_html` on six named lines and on the
real producer's Multi-Comp (portfolio, two models, one ETF), reads the stroke colour of every polyline and the swatch colour of every legend item,
and requires, with this file's own colour arithmetic: (1) all colours of a chart distinct; (2) each colour at least 3.0:1 against the white page
(WCAG relative luminance); (3) every pair at least 30 apart in CIE76 Delta E (L*a*b*, D65), the measure of how distinct two colours look; (4) the
legend swatch i equals the stroke i. `tests`: the new test file passes with at least 3 tests.
Prints one RESULT line: AR-PALETTE-<arm>-OK or AR-PALETTE-<arm>-FAIL <why>. ASCII only.
"""
import itertools
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
TREE = "infra/aws/lambda/investor-reporting"
TEST_FILE = "ycharts/research/tests/test_layout_chart_palette.py"
MIN_TESTS = 3
MIN_CONTRAST = 3.0
MIN_DELTA_E = 30.0


def fail(arm, why):
    print("AR-PALETTE-%s-FAIL %s" % (arm, why))
    sys.exit(1)


def paths(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    here = os.path.join(base, "ycharts/research")
    sys.path[:0] = [os.path.join(here, "tests"), here, os.path.join(base, "ycharts/session"), os.path.join(base, "ycharts/generate"),
                    os.path.join(base, "ycharts/extract"), os.path.join(base, "reports"), os.path.join(base, "lib"), os.path.join(base, "ops"),
                    os.path.join(base, "intake"), os.path.join(base, "_scope"), os.path.join(base, "_ids"), os.path.join(base, "_keys"),
                    os.path.join(base, "_authz"), base]
    return base


def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def luminance(h):
    r, g, b = [lin(c) for c in rgb(h)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def lab(h):
    r, g, b = [lin(c) for c in rgb(h)]
    x, y, z = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, 0.2126 * r + 0.7152 * g + 0.0722 * b, (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1.0 / 3.0) if t > 0.008856 else 7.787 * t + 16.0 / 116.0
    return 116.0 * f(y) - 16.0, 500.0 * (f(x) - f(y)), 200.0 * (f(y) - f(z))


def delta_e(a, b):
    return math.dist(lab(a), lab(b))


def judge(tag, strokes, swatches):
    """-> list of problems for one chart."""
    problems = []
    if len(set(c.upper() for c in strokes)) != len(strokes):
        problems.append("%s: colours repeat: %s" % (tag, strokes))
    for c in strokes:
        if contrast(c, "#FFFFFF") < MIN_CONTRAST:
            problems.append("%s: %s is %.2f:1 against white (min %.1f)" % (tag, c, contrast(c, "#FFFFFF"), MIN_CONTRAST))
    for a, b in itertools.combinations(strokes, 2):
        if delta_e(a, b) < MIN_DELTA_E:
            problems.append("%s: %s and %s are %.1f apart in Delta E (min %.0f)" % (tag, a, b, delta_e(a, b), MIN_DELTA_E))
    if [s.upper() for s in swatches] != [c.upper() for c in strokes]:
        problems.append("%s: the legend swatches %s are not the strokes %s" % (tag, swatches, strokes))
    return problems


def chart_colours(html):
    strokes = re.findall(r'<polyline[^>]*stroke="(#[0-9A-Fa-f]{6})"', html)
    swatches = re.findall(r'width:14px;height:3px;background:(#[0-9A-Fa-f]{6})', html)
    return strokes, swatches


def arm_palette(root):
    paths(root)
    import layout_overview as lo
    import test_opal_producer as tp
    import test_compare_producer as tc
    problems = []
    brand = lo.load_brand()
    colors = lo._palette(brand["spec"])
    names = ["Your portfolio", "Opal Short-Term", "Opal Long-Term", "Vanguard Real Estate ETF", "Opal Intermediate-Term", "Opal Ultra Long-Term"]
    lines = [{"name": n, "points": [[1000 * k, 100.0 + i * 3 + k] for k in range(5)]} for i, n in enumerate(names)]
    html = lo._lines_svg(lines, colors) + lo._legend_html(lines, colors)
    strokes, swatches = chart_colours(html)
    if len(strokes) != 6:
        problems.append("six lines drew %d polylines" % len(strokes))
    problems += judge("six lines", strokes, swatches)
    clf = tp.FakeClassifier()
    clf.rows["IWM"] = {"ticker": "IWM", "asset_class": "equity", "sub_asset_class": "Fixture Small Blend", "name": "iShares Russell 2000 ETF"}
    mp = json.loads((tc.MAPS / "multi_map.json").read_text(encoding="utf-8"))
    stores = tp.make_stores(classifier=clf, map=mp, pricing=True, as_of=tc.AS_OF, price_readers=tc._readers(), comparables=tc.ENTRIES,
                            model_bytes=tc._model_bytes())
    try:
        tp.op.produce(tp.REQ, tp.FIRM, stores)
    except Exception as exc:  # noqa: BLE001
        fail("palette", "the producer raised %s: %s" % (type(exc).__name__, str(exc)[:120]))
    strokes, swatches = chart_colours("".join(stores["html"]))
    if len(strokes) != 4:
        problems.append("the producer's Multi-Comp drew %d polylines, want 4" % len(strokes))
    problems += judge("producer Multi-Comp", strokes, swatches)
    if problems:
        fail("palette", "; ".join(problems)[:900])
    print("AR-PALETTE-palette-OK")


def arm_tests(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", TEST_FILE]
    run = subprocess.run(cmd, capture_output=True, text=True, cwd=base)
    found = re.findall(r"(\d+) passed", run.stdout)
    passed = int(found[-1]) if found else 0
    if run.returncode != 0 or passed < MIN_TESTS:
        print("AR-PALETTE-tests-FAIL rc=%d passed=%d (want rc 0 and at least %d): %s" % (run.returncode, passed, MIN_TESTS,
              " ".join(run.stdout.strip().splitlines()[-2:])[:200]))
        sys.exit(1)
    print("AR-PALETTE-tests-OK passed=%d" % passed)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("palette", "tests"):
        print("usage: ar_palette_checks.py palette|tests [--root <root>]")
        sys.exit(2)
    root = REPO
    if "--root" in sys.argv:
        root = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
    {"palette": arm_palette, "tests": arm_tests}[sys.argv[1]](root)


if __name__ == "__main__":
    main()
