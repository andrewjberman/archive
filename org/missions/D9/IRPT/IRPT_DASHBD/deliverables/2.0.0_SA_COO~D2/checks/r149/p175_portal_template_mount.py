"""IRPT_DASHBD round 149, workstream PORTALMOUNT (issuer 2.0.0_SA_COO~D2) -- DB-b-307, the Performance tab's TEMPLATE VIEW and its PDF export (CTO msg 9662 for Andrew): the 21 files of the render candidate
(cand/dell2/irpt-49f-report-render-disclosure-placeholder @42a1539b, PerformanceReport and PerformanceReportDocument) are cherry-picked onto current DEV and MOUNTED: PerformanceTemplateView in the Performance tab, the
PerformanceReportDocument behind the export button; the served filled_report.json comes from the route, and ONLY under the Vite dev server a synthetic fixture with a visible SYNTHETIC PREVIEW banner stands in when
the route has nothing. CLIENT-FACING (the approval row waits for Andrew). The cell lives in the PORTAL repo (<root>/portal, branch cand/dell2/...).

  DBP175-1-AC1  the diff: the 21 candidate files byte-identical to the candidate, the agreed write set only, the three forbidden files untouched, the mounts present
  DBP175-1-AC2  the behaviour: the view's pure core (resolveTemplate, PerformanceTemplateBody) on served, preview and none states; the DEV gate is a dynamic import; the route is the served route
  DBP175-1-AC3  the proof: every irpt-dashbd portal test passes, the typecheck passes, and the PRODUCTION build contains neither the banner nor the fixture

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

CAND = "42a1539b183adf19efd4ded2ead8642f48ddb3d0"
IR = "src/pages/InvestorReporting/"
VIEW = IR + "tabs/reporting/PerformanceTemplateView.tsx"
STORE = IR + "tabs/reporting/templateState.ts"
TAB = IR + "tabs/reporting/ReportingTab.tsx"
EDITS = {IR + "tabs/reporting/ReportingTab.tsx", IR + "export/Preview.tsx", IR + "render/PrintEntry.tsx", IR + "render/manifest.ts", IR + "export/ExportButton.tsx"}
FORBIDDEN = {IR + "dashboard/DashboardPerformance.tsx", IR + "dashboard/seriesContract.ts", IR + "dashboard/coverageWords.ts"}
TESTS = IR + "__tests__/irpt-dashbd/"
PROBE = TESTS + "_p175_probe.test.tsx"
FIXTURE_SRC = IR + "dashboard/report/fixtures/syntheticReport.ts"
BANNER = "SYNTHETIC PREVIEW"
FIXTURE_MARK = re.compile(r"pvs\.ytd\.beginning_value[\"']?\s*:\s*241732")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def run(cmd, cwd, timeout=900):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


def portal(root):
    p = Path(root).resolve() / "portal"  # absolute: git -C <p> with cwd=<p> must not resolve portal/portal (worker row W246-S1)
    need((p / "package.json").is_file(), "no portal checkout at %s" % p)
    return p


def git(p, *a):
    r = run(["git", "-C", str(p)] + list(a), p)
    return r.stdout, r.returncode


def base_of(p):
    out, rc = git(p, "merge-base", "HEAD", "origin/DEV")
    need(rc == 0 and out.strip(), "no merge-base with origin/DEV")
    return out.strip()


def candidate_files(p):
    mb, rc = git(p, "merge-base", CAND, "origin/DEV")
    need(rc == 0, "the candidate commit is not in this portal repo")
    out, _ = git(p, "diff", "--name-only", mb.strip(), CAND)
    names = [x for x in out.splitlines() if x.strip()]
    need(len(names) == 21, "the candidate should add 21 files, read %d" % len(names))
    return names


def check_diff(root):
    p = portal(root)
    br, _ = git(p, "rev-parse", "--abbrev-ref", "HEAD")
    need(br.strip().startswith("cand/dell2/"), "the portal branch must be named cand/dell2/<slug>, it is %s" % br.strip())
    base = base_of(p)
    out, _ = git(p, "diff", "--name-only", base, "HEAD")
    changed = {x for x in out.splitlines() if x.strip()}
    cand = candidate_files(p)
    allowed = set(cand) | EDITS | {VIEW, STORE}
    extra = [f for f in changed if f not in allowed and not f.startswith(TESTS)]
    need(not extra, "portal files outside the agreed write set changed: %s" % extra[:4])
    need(not (changed & FORBIDDEN), "a forbidden file changed: %s" % sorted(changed & FORBIDDEN))
    need(VIEW in changed and STORE in changed, "the new view %s or the shared state module %s is missing" % (VIEW, STORE))
    for f in cand:
        a, rc = git(p, "show", "%s:%s" % (CAND, f))
        b, rc2 = git(p, "show", "HEAD:%s" % f)
        need(rc == 0 and rc2 == 0 and a == b, "candidate file %s differs from the candidate" % f)
    tab = (p / TAB).read_text(encoding="utf-8")
    need(len(re.findall(r"import\s+\{[^}]*PerformanceTemplateView[^}]*\}\s+from", tab)) == 1 and len(re.findall(r"<PerformanceTemplateView\b", tab)) == 1, "ReportingTab.tsx must import PerformanceTemplateView once and mount it once")
    d, _ = git(p, "diff", "--numstat", base, "HEAD", "--", TAB)
    add, rem = (int(x) for x in d.split()[:2])
    need(add <= 14 and rem <= 2, "ReportingTab.tsx: one import and one mount only (added %d, removed %d)" % (add, rem))
    for f in (IR + "render/manifest.ts",):
        need("PerformanceReportDocument" in (p / f).read_text(encoding="utf-8"), "%s must reference PerformanceReportDocument" % f.rsplit("/", 1)[-1])
    need(any("PerformanceReportDocument" in (p / f).read_text(encoding="utf-8") for f in (IR + "export/Preview.tsx", IR + "render/PrintEntry.tsx")), "Preview.tsx or PrintEntry.tsx must reference PerformanceReportDocument")
    need(any("templateState" in (p / f).read_text(encoding="utf-8") for f in (IR + "export/Preview.tsx", IR + "render/PrintEntry.tsx")), "the export (Preview.tsx or PrintEntry.tsx) must read the tab's template state from templateState")
    vtext = (p / VIEW).read_text(encoding="utf-8")
    need("templateState" in vtext, "the view must publish its state through templateState")
    need(re.search(r"publishTemplateState\(\s*null\s*\)", vtext) is not None, "the view must clear the published state (publishTemplateState(null)) in an effect cleanup, so the export never reads a stale tab (the page owner's condition 1)")
    return True


PROBE_TEXT = """import { describe, expect, test } from 'bun:test'
import { createElement } from 'react'
import { renderToStaticMarkup } from 'react-dom/server'
import { PerformanceTemplateBody, SYNTHETIC_PREVIEW_BANNER, resolveTemplate } from '../../tabs/reporting/PerformanceTemplateView'
import { SYNTHETIC_REPORT_ALPHA } from '../../dashboard/report/fixtures/syntheticReport'
import { publishTemplateState, readTemplateState } from '../../tabs/reporting/templateState'

describe('p175 probe', () => {
  test('the shared state: what the view publishes is what the export reads', () => {
    publishTemplateState(null)
    expect(readTemplateState()).toBeNull()
    const s = resolveTemplate(SYNTHETIC_REPORT_ALPHA, null)
    publishTemplateState(s)
    expect(readTemplateState()).toEqual(s)
    publishTemplateState(null)
    expect(readTemplateState()).toBeNull()
  })
  test('the banner words', () => {
    expect(SYNTHETIC_PREVIEW_BANNER).toBe('SYNTHETIC PREVIEW')
  })
  test('a served report is live whatever the fixture', () => {
    expect(resolveTemplate(SYNTHETIC_REPORT_ALPHA, null).kind).toBe('live')
    expect(resolveTemplate(SYNTHETIC_REPORT_ALPHA, SYNTHETIC_REPORT_ALPHA).kind).toBe('live')
  })
  test('nothing served and a fixture is a preview', () => {
    expect(resolveTemplate(null, SYNTHETIC_REPORT_ALPHA).kind).toBe('preview')
  })
  test('nothing served and no fixture is none', () => {
    expect(resolveTemplate(null, null).kind).toBe('none')
  })
  test('the markup: live has no banner, preview has it once, none renders nothing', () => {
    const live = renderToStaticMarkup(createElement(PerformanceTemplateBody, { state: resolveTemplate(SYNTHETIC_REPORT_ALPHA, null), firmId: '49financial' }))
    const prev = renderToStaticMarkup(createElement(PerformanceTemplateBody, { state: resolveTemplate(null, SYNTHETIC_REPORT_ALPHA), firmId: '49financial' }))
    const none = renderToStaticMarkup(createElement(PerformanceTemplateBody, { state: resolveTemplate(null, null), firmId: '49financial' }))
    expect(live).toContain('data-section="cover"')
    expect(live).not.toContain('SYNTHETIC PREVIEW')
    expect(prev).toContain('data-section="cover"')
    expect(prev.split('SYNTHETIC PREVIEW').length - 1).toBe(1)
    expect(none).toBe('')
  })
})
"""


def check_behaviour(root):
    p = portal(root)
    view = (p / VIEW).read_text(encoding="utf-8")
    need("import.meta.env.DEV" in view, "the view must gate the fixture on import.meta.env.DEV")
    need(re.search(r"import\(\s*['\"][^'\"]*fixtures/syntheticReport['\"]\s*\)", view) is not None, "the fixture must be loaded by a dynamic import(...) of fixtures/syntheticReport")
    need(re.search(r"^\s*import\s[^\n]*fixtures/syntheticReport", view, flags=re.M) is None, "the view must NOT import the fixture statically")
    need(re.search(r"reporting/client/.{0,60}/report", view) is not None, "the view must read the served route .../reporting/client/<id>/report")
    need(view.count(BANNER) >= 1, "the banner words %s are missing from the view" % BANNER)
    target = p / PROBE
    target.write_text(PROBE_TEXT, encoding="utf-8")
    try:
        bun = shutil.which("bun")
        need(bun is not None, "bun is not on the PATH")
        r = run([bun, "test", PROBE], p, 600)
        need(r.returncode == 0, "the probe failed: %s" % (r.stdout + r.stderr)[-700:].replace("\n", " | "))
    finally:
        if target.exists():
            target.unlink()
    return True


def scan_dist(dist):
    hits = []
    for f in Path(dist).rglob("*"):
        if f.is_file() and f.suffix in (".js", ".css", ".html", ".map"):
            t = f.read_text(encoding="utf-8", errors="replace")
            if BANNER in t:
                hits.append((f.name, "banner"))
            if FIXTURE_MARK.search(t):
                hits.append((f.name, "fixture"))
    return hits


def check_proof(root):
    p = portal(root)
    bun = shutil.which("bun")
    need(bun is not None, "bun is not on the PATH")
    r = run([bun, "test", TESTS], p, 1500)
    need(r.returncode == 0, "the irpt-dashbd tests failed: %s" % (r.stdout + r.stderr)[-500:].replace("\n", " | "))
    r = run([bun, "run", "typecheck"], p, 1500)
    need(r.returncode == 0, "the typecheck failed: %s" % (r.stdout + r.stderr)[-500:].replace("\n", " | "))
    dist = p / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    r = run([bun, "run", "build"], p, 1800)
    need(r.returncode == 0, "the production build failed: %s" % (r.stdout + r.stderr)[-500:].replace("\n", " | "))
    need(dist.is_dir() and any(dist.rglob("*.js")), "the build produced no dist")
    ctl = dist / "_p175_control.js"
    ctl.write_text("var x='" + BANNER + "';var y={'pvs.ytd.beginning_value':241732}", encoding="utf-8")
    try:
        need({h[1] for h in scan_dist(dist)} == {"banner", "fixture"}, "the scan's positive control did not see the banner and the fixture marker")
    finally:
        ctl.unlink()
    hits = scan_dist(dist)
    need(not hits, "the production build carries the preview: %s" % hits[:3])
    return True


CHECKS = {"DBP175-1-AC1": check_diff, "DBP175-1-AC2": check_behaviour, "DBP175-1-AC3": check_proof}

if __name__ == "__main__":
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DBP175-1-AC1": "OK: the 21 candidate files equal the candidate; only the agreed write set changed; the three forbidden files are untouched; the tab mounts the view once and the export references the document",
               "DBP175-1-AC2": "OK: the view's pure core resolves served, preview and none states, the banner shows only in the preview, the fixture is a dev-gated dynamic import and the route is the served one",
               "DBP175-1-AC3": "OK: every irpt-dashbd portal test passes, the typecheck passes, and the production build carries neither the SYNTHETIC PREVIEW banner nor the fixture (the scan's positive control sees both)"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
