#!/usr/bin/env python3
"""Round 144, workstream B-49F (issuer 2.0.0_SA_COO~D2), cell DB-b-277: the 49 Financial disclosure slot renders a VISIBLE placeholder.

Andrew, verbatim (ANDREW_DIRECT 2026-10-15 ~21:3xZ, row 90ef, via the CTO msg 8686): "We will deal with this later, should just be placeholder for now."
The CTO's act: render the `disclosure_text` slot as a VISIBLE placeholder ("Disclosure page pending"): never empty, never invented text.
The 49 Financial template file Andrew named (a252) holds no disclosure page (only the pointer line "This report is incomplete without the accompanying disclosure page"), so there is no firm
text to print; the renderer may not author disclosure language. The 49 Financial default performance report document (render/performance/report) therefore gains a LAST sheet, the disclosure
page, whose slot reads the visible placeholder while no text is supplied; the custody ClientReportDocument's unfilled disclosure slot reads it too.

Run as:  python -I <this file> <root> <CRITERION_ID>      (root = the worktree root; the portal is root/portal)

  DB144-1-AC1  the new test file exists, holds the required cases and passes under two runtime zones (bun test)
  DB144-1-AC2  the neighbours' existing tests pass (bun test)
  DB144-1-AC3  the placeholder is ONE shared constant used by both render paths, the report document ends with a disclosure sheet, the pointer line is unchanged, no other
               disclosure language was authored, the filled branch is unchanged, and the worker's record is complete and bound to a portal commit

Prints `<ID> PASS` or `<ID> FAIL` with the reason. Stdlib only; every subprocess is bounded.
       python -I <this file> --selftest        the pure clauses on synthetic arms
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RECORD = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~224/RD_DISCLOSURE_PLACEHOLDER_R144.json"
IR = "src/pages/InvestorReporting/"
NEW_TEST = IR + "__tests__/irpt-dashbd/disclosure-placeholder.test.tsx"
CLIENT_DOC = IR + "render/clientreport/ClientReportDocument.tsx"
PERF_DOC = IR + "render/performance/report/PerformanceReportDocument.tsx"
DOC_SHEETS = IR + "render/performance/report/documentSheets.ts"
NEIGHBOUR_DIRS = (IR + "__tests__/irpt-dashbd/", IR + "__tests__/clientreport/")
NEIGHBOUR_FILES = (IR + "__tests__/ir-66-print-kind/print-kind.test.ts", IR + "__tests__/ir-72-custody-print/custody-print.test.tsx")
POINTER = "This report is incomplete without the accompanying disclosure page."
WORDS = "Disclosure page pending"
VERDICT = "VERDICT: DISCLOSURE-PLACEHOLDER-OK"
REQUIRED_TOKENS = (WORDS, VERDICT, "data-disclosure-placeholder", "unfilled", "filled", "data-slot-state", "disclosures", "INCOMPLETE_WITHOUT_DISCLOSURE", "Page ")
TEST_RX = re.compile(r"(^|/)(__tests__|__harness__|__fixtures__|__mocks__)/|\.(test|spec)\.[cm]?[jt]sx?$|\.harness\.cjs$")
LONG_DIGITS = re.compile(r"\d{8,}")
BASE_COMMIT = "c81d54ff"  # the head of the 49 Financial report render lineage (wk-IRPT_DASHBD-180-portal), not merged to DEV


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def read(p):
    return Path(p).read_bytes().decode("utf-8")


def bun():
    b = shutil.which("bun")
    need(b, "bun is not on PATH")
    return b


def bun_test(portal, files, tz):
    env = dict(os.environ)
    env["TZ"] = tz
    r = subprocess.run([bun(), "test"] + files, cwd=str(portal), env=env, capture_output=True, timeout=300)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


# ------------------------------------------------------------------------------------------------ the pure clauses
def check_test_source(src):
    for tok in REQUIRED_TOKENS:
        need(tok in src, "the test file must hold %r (a required case or the verdict line)" % tok)
    need(len(re.findall(r"\b(it|test)\(", src)) >= 7, "the test file must hold at least seven cases")
    return True


def product_literals(portal):
    """Every non-test product file under portal/src that holds the placeholder words as a string literal, as (relative path, line)."""
    hits = []
    for p in (portal / "src").rglob("*"):
        if p.suffix not in (".ts", ".tsx") or TEST_RX.search(p.as_posix()):
            continue
        for n, line in enumerate(read(p).splitlines(), 1):
            s = line.strip()
            if WORDS in line and not s.startswith(("*", "//", "/*")):
                hits.append((p.relative_to(portal).as_posix(), n))
    return hits


def check_constant(hits, client_src, perf_src):
    need(len(hits) == 1, "the words %r must appear as ONE string literal in the product source (a shared constant), found %d: %s" % (WORDS, len(hits), hits[:3]))
    path, _n = hits[0]
    need(path.startswith("src/pages/InvestorReporting/"), "the constant must live under src/pages/InvestorReporting/, found %s" % path)
    name = Path(path).stem
    for label, src in (("ClientReportDocument.tsx", client_src), ("Disclosures.tsx", perf_src)):
        need(re.search(r"import\s*\{[^}]*\}\s*from\s*['\"][^'\"]*%s['\"]" % re.escape(name), src) or path.endswith(label), "%s must import the shared constant from %s" % (label, path))
    return True


def check_client_branches(src):
    """The unfilled slot prints the placeholder; the filled slot still prints each paragraph; the slot state words are unchanged."""
    need("data-slot-state={disclosures.length === 0 ? 'unfilled' : 'filled'}" in src, "ClientReportDocument must keep data-slot-state 'unfilled' | 'filled' on the disclosure slot")
    need("data-disclosure-placeholder" in src, "ClientReportDocument must mark the placeholder with data-disclosure-placeholder")
    need(src.count("data-disclosure-placeholder") >= 2, "both ClientReportDocument status pages (covered and not-covered) must print the placeholder")
    need("disclosures.map((text, index) =>" in src and "{text}" in src, "the filled branch must still print each disclosure paragraph verbatim")
    return True


def check_report_sheet(doc_src, sheets_src):
    """The report document ends with a disclosure sheet whose slot prints the placeholder when no text is supplied; the pointer line is unchanged."""
    need('data-slot="disclosure"' in doc_src and "data-slot-state" in doc_src and "data-disclosure-placeholder" in doc_src, "PerformanceReportDocument must hold a disclosure slot with data-slot, data-slot-state and data-disclosure-placeholder")
    need('"disclosures"' in doc_src or "'disclosures'" in doc_src or '"disclosures"' in sheets_src or "'disclosures'" in sheets_src, "the report document must name its disclosure sheet 'disclosures'")
    need("disclosures?:" in doc_src and "readonly string[]" in doc_src, "PerformanceReportDocument must take the firm's disclosure text as an optional prop (readonly string[]), never authored here")
    need(("INCOMPLETE_WITHOUT_DISCLOSURE = '%s'" % POINTER) in sheets_src or ('INCOMPLETE_WITHOUT_DISCLOSURE = "%s"' % POINTER) in sheets_src, "the pointer line constant INCOMPLETE_WITHOUT_DISCLOSURE must stay exactly %r" % POINTER)
    need(doc_src.count("{INCOMPLETE_WITHOUT_DISCLOSURE}") >= 1, "the pointer line must still print on the sheets")
    return True


def check_no_authored_language(src_texts):
    """The renderer may not author disclosure language: no new sentence of compliance wording beside the placeholder."""
    bad = [w for w in ("past performance", "not a guarantee", "advisory fee", "form adv", "hypothetical") if any(w in t.lower() for t in src_texts)]
    need(not bad, "authored disclosure language found in the render files: %s" % bad)
    return True


def check_record(r, commit_ok):
    need(isinstance(r, dict), "the record must be an object")
    exp = {"claim", "portal", "constant", "branches", "tests", "pushed", "deployed", "words"}
    need(set(r) == exp, "record keys differ: %s" % sorted(set(r) ^ exp))
    need(r["claim"] == "measured", "claim must be measured")
    pt = r["portal"]
    need(isinstance(pt, dict) and set(pt) == {"branch", "commit", "files_changed"} and pt["branch"] == "wk-IRPT_DASHBD-224-portal" and re.fullmatch(r"[0-9a-f]{7,40}", str(pt["commit"])),
         "portal: the branch wk-IRPT_DASHBD-224-portal and a commit")
    need(isinstance(pt["files_changed"], list) and pt["files_changed"] and all(str(x).startswith("src/") for x in pt["files_changed"]), "files_changed must list portal files under src/")
    need(commit_ok(pt["commit"]), "the portal commit does not exist or does not descend from the report render base %s" % BASE_COMMIT)
    c = r["constant"]
    need(isinstance(c, dict) and set(c) == {"file", "name", "value"} and c["value"] == WORDS and str(c["file"]).startswith("src/") and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", str(c["name"])), "constant: file, name and the exact words")
    b = r["branches"]
    need(b == {"client_unfilled": "placeholder", "client_filled": "verbatim paragraphs", "report_sheet": "last sheet, placeholder when no text is supplied", "pointer_line": "unchanged"}, "branches record")
    t = r["tests"]
    need(isinstance(t, dict) and t.get("mutant_failed") is True and t.get("lint_errors") == 0 and t.get("typecheck_errors") == 0 and (t.get("suite_after") or {}).get("new_failing_ids") == [],
         "tests: mutant_failed true, lint 0, typecheck 0, no new failing test")
    need(r["pushed"] is False and r["deployed"] is False, "pushed and deployed must be false (the issuer pushes the candidate)")
    need(isinstance(r["words"], str) and 80 <= len(r["words"]) <= 1800 and not LONG_DIGITS.findall(r["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


# ------------------------------------------------------------------------------------------------ the criteria
def check_ac1(root):
    portal = root / "portal"
    f = portal / NEW_TEST
    need(f.is_file(), "the new test file %s does not exist" % NEW_TEST)
    check_test_source(read(f))
    for tz in ("UTC", "America/Los_Angeles"):
        rc, out = bun_test(portal, [NEW_TEST], tz)
        need(rc == 0 and VERDICT in out, "bun test %s under TZ=%s: rc=%d, verdict line %s" % (NEW_TEST, tz, rc, "present" if VERDICT in out else "absent"))
    print("OK: the new test holds the required cases and passes under TZ=UTC and TZ=America/Los_Angeles")


def neighbours(portal):
    out = []
    for d in NEIGHBOUR_DIRS:
        out += sorted(p.relative_to(portal).as_posix() for p in (portal / d).glob("*.test.ts*") if p.relative_to(portal).as_posix() != NEW_TEST)
    return out + list(NEIGHBOUR_FILES)


def check_ac2(root):
    portal = root / "portal"
    nb = neighbours(portal)
    need(len(nb) >= 12, "the neighbour set must hold at least 12 test files (the irpt-dashbd and clientreport tests), found %d" % len(nb))
    for n in nb + [NEW_TEST]:
        need((portal / n).is_file(), "test file %s is missing" % n)
    rc, out = bun_test(portal, nb + [NEW_TEST], "UTC")
    need(rc == 0, "bun test of the %d neighbour test files and the new one failed (rc=%d): %s" % (len(nb), rc, out.strip().splitlines()[-1] if out.strip() else ""))
    print("OK: %d neighbour test files and the new test file pass together" % len(nb))


def check_ac3(root):
    portal = root / "portal"
    client, perf, sheets = read(portal / CLIENT_DOC), read(portal / PERF_DOC), read(portal / DOC_SHEETS)
    hits = product_literals(portal)
    check_constant(hits, client, perf)
    check_client_branches(client)
    check_report_sheet(perf, sheets)
    check_no_authored_language([client, perf, sheets, read(portal / hits[0][0])])
    r = json.loads(read(root / RECORD))

    def commit_ok(c):
        g = subprocess.run(["git", "-C", str(portal), "cat-file", "-t", c], capture_output=True, text=True, timeout=60)
        a = subprocess.run(["git", "-C", str(portal), "merge-base", "--is-ancestor", BASE_COMMIT, c], capture_output=True, timeout=60)
        return g.returncode == 0 and g.stdout.strip() == "commit" and a.returncode == 0
    check_record(r, commit_ok)
    need(r["constant"]["file"] == hits[0][0], "the record's constant file differs from the product source")
    print("OK: the words %r are one shared constant in %s used by both render paths; the unfilled slot and the report document's last sheet print the placeholder; the filled branch and the pointer line are unchanged; no authored language; the record is bound to a portal commit" % (WORDS, hits[0][0]))


CHECKS = {"DB144-1-AC1": check_ac1, "DB144-1-AC2": check_ac2, "DB144-1-AC3": check_ac3}


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    good_test = "\n".join(["it('a', () => {})"] * 7) + "\n" + " ".join(REQUIRED_TOKENS)
    assert check_test_source(good_test)
    for tok in REQUIRED_TOKENS:
        red(lambda tok=tok: check_test_source(good_test.replace(tok, "x")), "test lacks %s" % tok)
    red(lambda: check_test_source(" ".join(REQUIRED_TOKENS)), "too few cases")
    assert check_constant([("src/pages/InvestorReporting/render/disclosurePlaceholder.ts", 3)], "import { P } from '../disclosurePlaceholder'", "import { P } from '../disclosurePlaceholder'")
    red(lambda: check_constant([], "", ""), "no constant")
    red(lambda: check_constant([("src/a.ts", 1), ("src/b.ts", 2)], "", ""), "two literals")
    red(lambda: check_constant([("src/lib/x.ts", 1)], "", ""), "wrong place")
    red(lambda: check_constant([("src/pages/InvestorReporting/render/d.ts", 3)], "no import", "import { P } from '../d'"), "client lacks the import")
    client = ("data-slot-state={disclosures.length === 0 ? 'unfilled' : 'filled'}\n<p data-disclosure-placeholder>{X}</p>\n<p data-disclosure-placeholder>{X}</p>\n"
              "{disclosures.map((text, index) => (<p key={index}>{text}</p>))}")
    assert check_client_branches(client)
    red(lambda: check_client_branches(client.replace("'unfilled'", "'empty'")), "slot state changed")
    red(lambda: check_client_branches(client.replace("data-disclosure-placeholder", "x", 1)), "one page lacks the placeholder")
    red(lambda: check_client_branches(client.replace("disclosures.map((text, index) =>", "[].map(() =>")), "filled branch removed")
    doc = '<div data-slot="disclosure" data-slot-state="unfilled"><p data-disclosure-placeholder>{X}</p></div> disclosures?: readonly string[] | null {INCOMPLETE_WITHOUT_DISCLOSURE} "disclosures"'
    sheets = "export const INCOMPLETE_WITHOUT_DISCLOSURE = 'This report is incomplete without the accompanying disclosure page.'"
    assert check_report_sheet(doc, sheets)
    red(lambda: check_report_sheet(doc.replace('data-disclosure-placeholder', 'x'), sheets), 'no placeholder in the report sheet')
    red(lambda: check_report_sheet(doc.replace('data-slot-state', 'x'), sheets), 'no slot state')
    red(lambda: check_report_sheet(doc.replace('disclosures?:', 'x?:'), sheets), 'no optional prop')
    red(lambda: check_report_sheet(doc.replace('"disclosures"', 'x'), sheets), 'sheet not named')
    red(lambda: check_report_sheet(doc.replace('{INCOMPLETE_WITHOUT_DISCLOSURE}', ''), sheets), 'pointer line removed')
    red(lambda: check_report_sheet(doc, sheets.replace('accompanying', 'x')), 'pointer constant changed')
    assert check_no_authored_language(["Disclosure page pending"])
    red(lambda: check_no_authored_language(["Past performance is no guarantee"]), "authored language")
    rec = {"claim": "measured", "portal": {"branch": "wk-IRPT_DASHBD-224-portal", "commit": "abcdef1", "files_changed": ["src/a.ts"]}, "constant": {"file": "src/a.ts", "name": "X", "value": WORDS},
           "branches": {"client_unfilled": "placeholder", "client_filled": "verbatim paragraphs", "report_sheet": "last sheet, placeholder when no text is supplied", "pointer_line": "unchanged"},
           "tests": {"mutant_failed": True, "lint_errors": 0, "typecheck_errors": 0, "suite_after": {"new_failing_ids": []}}, "pushed": False, "deployed": False, "words": "w" * 100}
    assert check_record(rec, lambda c: True)
    import copy
    arms = (("claim", lambda r: r.update(claim="inferred")), ("branch", lambda r: r["portal"].update(branch="x")), ("commit", lambda r: r["portal"].update(commit="zz")), ("files", lambda r: r["portal"].update(files_changed=[])),
            ("value", lambda r: r["constant"].update(value="x")), ("branches", lambda r: r["branches"].update(pointer_line="changed")), ("mutant", lambda r: r["tests"].update(mutant_failed=False)),
            ("lint", lambda r: r["tests"].update(lint_errors=1)), ("new failing", lambda r: r["tests"]["suite_after"].update(new_failing_ids=["x"])), ("pushed", lambda r: r.update(pushed=True)),
            ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in arms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_record(r2, lambda c: True), label)
    red(lambda: check_record(rec, lambda c: False), "commit not descending from PROD")
    print("selftest: test source (%d red arms), constant (4), client (3), report sheet (6), language (1) and record (%d red arms + 1) clauses behave" % (len(REQUIRED_TOKENS) + 1, len(arms)))
    print("selftest PASS")


def main(argv):
    if argv[1:2] == ["--selftest"]:
        selftest()
        return 0
    if len(argv) != 3 or argv[2] not in CHECKS:
        print("usage: p144_placeholder.py <root> <%s>" % "|".join(CHECKS))
        return 2
    cid = argv[2]
    try:
        CHECKS[cid](Path(argv[1]).resolve())
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % cid)
        return 1
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as e:
        print("FAIL: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
