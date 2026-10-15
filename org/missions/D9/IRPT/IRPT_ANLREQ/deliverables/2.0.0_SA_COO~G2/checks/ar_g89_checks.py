"""IRPT_ANLREQ AR-g-89 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g89_checks.py g89   a priced Opal page names no vendor and no time budget, carries the Opal credit, and still prints
                                  the figure; four named new tests exist and pass

Prints one RESULT line: AR-G89-OK / AR-G89-FAIL; rc 0 only on OK. ASCII only. It borrows the fakes and the hand-computed series of
ar_g86_checks.py (same folder).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ar_g86_checks as g86  # noqa: E402

T = g86.T
NEW_TESTS = {
    T + "test_opal_producer_page_wording.py": [
        "test_priced_page_names_no_vendor_and_no_time_budget",
        "test_priced_package_page_names_no_vendor",
        "test_priced_page_prints_the_figure_and_the_opal_credit",
        "test_unavailable_lines_use_the_opal_wording",
    ],
}


def cases(tp):
    out = {}
    lo = tp.lo
    stores, rec = g86.run(tp, pricing=True, price_readers=g86.readers_all(), as_of=g86.AS_OF)
    page = "\n".join(stores["html"])
    out["a priced page names no vendor and no time budget"] = (
        "YCharts" not in page and "time budget" not in page.lower() and "Data: YCharts" not in page)
    pages = page.count('<section class="page">')
    out["every page carries the Opal credit and no other"] = pages >= 1 and page.count(lo.OPAL_SOURCE_CREDIT) == pages
    want_ret, _ = g86.expected(["AAA", "BBB", "CCC"])
    shown = "{:,.4f}".format(want_ret).rstrip("0").rstrip(".")
    out["the priced figure is printed on the page"] = shown in page and rec["elements"] is not None
    out["an unavailable priced element uses the Opal wording"] = (
        "Not available: this element is not given for this portfolio. Reason: INPUT_MISSING:risk_free" in page)
    pk = tp.make_stores(map=g86.MINI, pricing=True, price_readers=g86.readers_all(), as_of=g86.AS_OF)
    tp.op.produce_package(tp.REQ, tp.FIRM, pk, {"text": "Draft commentary text."})
    ppage = "\n".join(pk["html"])
    out["a priced package page names no vendor, commentary page included"] = (
        "YCharts" not in ppage and "time budget" not in ppage.lower() and ppage.count(lo.OPAL_SOURCE_CREDIT) >= 2
        and "Commentary" in ppage)
    off = tp.make_stores(map=g86.MINI)
    tp.op.produce(tp.REQ, tp.FIRM, off)
    opage = "\n".join(off["html"])
    out["a page with pricing off is as it was: Opal credit, no vendor, the not-in-this-version line"] = (
        "YCharts" not in opage and opage.count(lo.OPAL_SOURCE_CREDIT) == opage.count('<section class="page">')
        and lo.NOT_IN_THIS_VERSION_LINE in opage)
    return out


def main(mode):
    if mode != "g89":
        print("usage: ar_g89_checks.py g89")
        return 2
    try:
        tp = g86.load()
    except Exception as exc:
        print("AR-G89-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
        return 1
    try:
        got = cases(tp)
    except Exception as exc:
        print("AR-G89-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:240]))
        return 1
    wrong = [k for k, ok in got.items() if not ok]
    missing = []
    for path, names in NEW_TESTS.items():
        rc, line, passed, text = g86.pytest_run([path], extra=("--collect-only",))
        have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", text))
        missing += [n for n in names if n not in have]
    rc, line, passed, text = g86.pytest_run(list(NEW_TESTS))
    need = sum(len(v) for v in NEW_TESTS.values())
    print("direct cases %d, wrong %s" % (len(got), wrong or "none"))
    print("named tests missing: %s" % (missing or "none"))
    print("new tests: %s" % line)
    if wrong or missing or rc != 0 or g86.bad_count(line) or passed < need:
        print("AR-G89-FAIL wrong=%s missing=%s rc=%d passed=%d (need >= %d)" % (wrong or "none", missing or "none", rc, passed, need))
        return 1
    print("AR-G89-OK direct=%d named=%d passed=%d" % (len(got), need, passed))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
