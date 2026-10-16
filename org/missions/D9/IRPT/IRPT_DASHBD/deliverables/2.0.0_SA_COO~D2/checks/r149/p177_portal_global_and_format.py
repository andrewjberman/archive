"""IRPT_DASHBD round 149, workstream PORTALGLOBAL (issuer 2.0.0_SA_COO~D2) -- DB-b-309, the Performance tab after Andrew's 5174 smoke, ON TOP OF the DB-b-307 branch (CTO ruling d22e05dd68 and msgs 9754, 9755, 9770;
write set and panel plan by the page owner 2.0.0_SA_COO~C2, R151_PERFORMANCE_TAB_WRITE_SET_AND_PANELS.md @9b04f830b2): (1) at Global every client-scoped read sends selected_tenant = the client's firm; (2) the firm-binding
banner is gone and a non-global login is offered only its own firm; (3) the template never renders silent; (4) Beginning value before Ending value and money printed as dollars with a symbol and grouping; (5) the
export's print window prints the SAME template document, carried by the export's own target and not by per-page-load memory. CLIENT-FACING; the cell lives in the PORTAL repo (<root>/portal, branch cand/dell2/...).

  DBP177-1-AC1  the diff: the agreed write set only, none of the protected files, the plumbing present (header selection, tab, view, headline order, formatter, print entry)
  DBP177-1-AC2  the behaviour: the money formatter, the worded template states (loading, unavailable) and the live/preview states, on a probe test
  DBP177-1-AC3  the proof: the cell's tests, every irpt-dashbd test, the typecheck and the production build pass, and the build carries neither the banner nor the fixture

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import re
import shutil
import sys
from pathlib import Path

P175 = None


def load_p175():
    global P175
    if P175 is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("p175_for_177", str(Path(__file__).resolve().parent / "p175_portal_template_mount.py"))
        P175 = importlib.util.module_from_spec(spec)
        sys.modules["p175_for_177"] = P175
        spec.loader.exec_module(P175)
    return P175


IR = "src/pages/InvestorReporting/"
HEADER_SEL = IR + "header/HeaderSelectionContext.ts"
INDEX = IR + "index.tsx"
TAB = IR + "tabs/reporting/ReportingTab.tsx"
VIEW = IR + "tabs/reporting/PerformanceTemplateView.tsx"
HEADLINE = IR + "tabs/reporting/PerformanceHeadline.tsx"
ACCOUNTS = IR + "tabs/reporting/AccountsTable.tsx"
CURRENCY = IR + "tabs/reporting/currency.ts"
PRINT = IR + "render/PrintEntry.tsx"
PREVIEW = IR + "export/Preview.tsx"
MANIFEST = IR + "render/manifest.ts"
STORE = IR + "tabs/reporting/templateState.ts"
ALLOWED = {HEADER_SEL, INDEX, TAB, VIEW, HEADLINE, ACCOUNTS, CURRENCY, PRINT, PREVIEW, MANIFEST, STORE}
PROTECTED = {IR + "dashboard/DashboardPerformance.tsx", IR + "dashboard/seriesContract.ts", IR + "dashboard/coverageWords.ts", IR + "dashboard/reportingRead.ts", IR + "export/submit.ts", IR + "export/ExportButton.tsx"}
TESTS = IR + "__tests__/irpt-dashbd/"
OLD_TESTS = IR + "__tests__/dsgn-irptv1/"
PROBE = TESTS + "_p177_probe.test.tsx"
BANNER_SENTENCE = "does not match this client"


def check_diff(root):
    p175 = load_p175()
    p = p175.portal(root)
    br, _ = p175.git(p, "rev-parse", "--abbrev-ref", "HEAD")
    p175.need(br.strip() == "cand/dell2/irpt-49f-performance-template-mount", "the portal branch must stay cand/dell2/irpt-49f-performance-template-mount (the cell is ONE branch for Andrew), it is %s" % br.strip())
    base = "1779d676064a2e8e7c4b8edda52c719c9c519199"
    out, rc = p175.git(p, "diff", "--name-only", base, "HEAD")
    p175.need(rc == 0, "the DB-b-307 head %s is not an ancestor of this branch" % base[:8])
    changed = {x for x in out.splitlines() if x.strip()}
    p175.need(changed, "nothing changed since the DB-b-307 head")
    extra = [f for f in changed if f not in ALLOWED and not f.startswith(TESTS) and not f.startswith(OLD_TESTS)]
    p175.need(not extra, "portal files outside the agreed write set changed: %s" % extra[:4])
    p175.need(not (changed & PROTECTED), "a protected file changed: %s" % sorted(changed & PROTECTED))
    t = lambda f: (p / f).read_text(encoding="utf-8")  # noqa: E731
    p175.need(re.search(r"selectedTenant\??\s*:\s*string", t(HEADER_SEL)) is not None, "HeaderSelection must carry an optional selectedTenant")
    p175.need("selectedTenant" in t(INDEX), "index.tsx must hand the client's own firm to the header selection (selectedTenant)")
    tab = t(TAB)
    p175.need("header?.selectedTenant" in tab or "header.selectedTenant" in tab, "ReportingTab.tsx must read the header's selectedTenant for the client-scoped reads")
    p175.need("firmBindingNotice" not in tab and "FIRM_BINDING_REASON" not in tab, "the firm-binding banner (firmBindingNotice, FIRM_BINDING_REASON) must be gone from ReportingTab.tsx")
    for f in changed:
        if f.startswith(IR) and not f.startswith(IR + "__tests__/") and (p / f).is_file():
            p175.need(BANNER_SENTENCE not in t(f), "the banner sentence is still in %s" % f.rsplit("/", 1)[-1])
    head = t(HEADLINE)
    i_b, i_e = head.find("beginning"), head.find("ending")
    spec = re.search(r"tileSpecs[^=]*=\s*\[(.*?)\n\s*\]", head, flags=re.S)
    p175.need(spec is not None and spec.group(1).find("beginning") != -1 and spec.group(1).find("beginning") < spec.group(1).find("ending"), "in tileSpecs the beginning tile must come before the ending tile (i_b=%d i_e=%d)" % (i_b, i_e))
    p175.need("formatUsd" in head and "formatUsd" in t(ACCOUNTS), "PerformanceHeadline.tsx and AccountsTable.tsx must print money through formatUsd")
    p175.need((p / CURRENCY).is_file() and re.search(r"export\s+function\s+formatUsd", t(CURRENCY)) is not None, "currency.ts must export formatUsd")
    pr = t(PRINT)
    p175.need("PerformanceReportDocument" in pr and "readTemplateState" not in pr, "the print entry must render PerformanceReportDocument from a state it resolves itself, not from readTemplateState (per-page-load memory)")
    p175.need("resolveTemplate" in pr or "readServedReport" in pr, "the print entry must resolve the template through resolveTemplate or readServedReport")
    view = t(VIEW)
    p175.need(re.search(r"kind:\s*'loading'", view) is not None and re.search(r"kind:\s*'unavailable'", view) is not None, "the view must declare the loading and unavailable states")
    return True


PROBE_TEXT = """import { describe, expect, test } from 'bun:test'
import { createElement } from 'react'
import { renderToStaticMarkup } from 'react-dom/server'
import { PerformanceTemplateBody, resolveTemplate } from '../../tabs/reporting/PerformanceTemplateView'
import { formatUsd } from '../../tabs/reporting/currency'
import { SYNTHETIC_REPORT_ALPHA } from '../../dashboard/report/fixtures/syntheticReport'

describe('p177 probe', () => {
  test('dollars with a symbol and grouping', () => {
    expect(formatUsd(92186.84, 'USD')).toBe('$92,186.84')
    expect(formatUsd(99698.29, 'USD')).toBe('$99,698.29')
    expect(formatUsd(1234567, 'USD')).toBe('$1,234,567.00')
    expect(formatUsd(-1234.5, 'USD')).toBe('-$1,234.50')
  })
  test('another currency prints its code and grouping, never a guessed symbol', () => {
    expect(formatUsd(1234.5, 'EUR')).toBe('EUR 1,234.50')
  })
  test('a served report is live, a fixture is a preview, a reason is unavailable, nothing yet is loading', () => {
    expect(resolveTemplate(SYNTHETIC_REPORT_ALPHA, null, null).kind).toBe('live')
    expect(resolveTemplate(null, SYNTHETIC_REPORT_ALPHA, null).kind).toBe('preview')
    expect(resolveTemplate(null, null, 'REFUSED').kind).toBe('unavailable')
    expect(resolveTemplate(null, null, null).kind).toBe('loading')
  })
  test('no state renders an empty node', () => {
    const html = (s: ReturnType<typeof resolveTemplate>) => renderToStaticMarkup(createElement(PerformanceTemplateBody, { state: s, firmId: '49financial' }))
    const loading = html(resolveTemplate(null, null, null))
    expect(loading.length).toBeGreaterThan(20)
    expect(loading).toContain('Loading the performance report for this client.')
    for (const reason of ['REFUSED', 'NOT_COVERED', 'NOT_READY', 'UNREADABLE'] as const) {
      const h = html(resolveTemplate(null, null, reason))
      expect(h.replace(/<[^>]*>/g, '').trim().length).toBeGreaterThan(20)
      expect(h).not.toContain('SYNTHETIC PREVIEW')
    }
    const live = html(resolveTemplate(SYNTHETIC_REPORT_ALPHA, null, null))
    expect(live).toContain('data-section="cover"')
    expect(live).not.toContain('SYNTHETIC PREVIEW')
    const prev = html(resolveTemplate(null, SYNTHETIC_REPORT_ALPHA, null))
    expect(prev.split('SYNTHETIC PREVIEW').length - 1).toBe(1)
  })
})
"""


def check_behaviour(root):
    p175 = load_p175()
    p = p175.portal(root)
    target = p / PROBE
    target.write_text(PROBE_TEXT, encoding="utf-8")
    try:
        bun = shutil.which("bun")
        p175.need(bun is not None, "bun is not on the PATH")
        r = p175.run([bun, "test", PROBE], p, 600)
        p175.need(r.returncode == 0, "the probe failed: %s" % (r.stdout + r.stderr)[-800:].replace("\n", " | "))
    finally:
        if target.exists():
            target.unlink()
    return True


def check_proof(root):
    p175 = load_p175()
    p = p175.portal(root)
    names = ("performance-tab-global-and-firm", "performance-template-states", "performance-headline-order-and-money", "performance-print-fresh-window")
    have = {n: any(f.name.startswith(n) for f in (p / TESTS).glob("*")) for n in names}
    p175.need(all(have.values()), "the cell's four test files are missing: %s" % [n for n, ok in have.items() if not ok])
    for f in (p / OLD_TESTS).glob("*"):
        if f.is_file():
            txt = f.read_text(encoding="utf-8", errors="replace")
            p175.need("firmBindingWords" not in txt and "FIRM_BINDING_REASON" not in txt, "%s still tests the removed banner" % f.name)
    return p175.check_proof(root)


CHECKS = {"DBP177-1-AC1": check_diff, "DBP177-1-AC2": check_behaviour, "DBP177-1-AC3": check_proof}

if __name__ == "__main__":
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DBP177-1-AC1": "OK: only the agreed write set changed and none of the protected files; the header selection carries the client's firm and the tab reads it; the firm banner is gone; Beginning comes before Ending; money goes through formatUsd; the print entry resolves its own template state",
               "DBP177-1-AC2": "OK: formatUsd prints $92,186.84 style dollars with grouping and a code for other currencies; the template resolves live, preview, unavailable and loading, and no state renders an empty node",
               "DBP177-1-AC3": "OK: the four test files exist and the removed banner is untested; every irpt-dashbd test passes, the typecheck passes and the production build carries neither the banner nor the fixture"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
