"""IRPT_DASHBD round 149, workstream PORTALPANELS (issuer 2.0.0_SA_COO~D2) -- DB-b-313, the Performance tab's holdings panels (CTO ruling msg 9866, write set of the page owner 2.0.0_SA_COO~C2,
R152_ALLOCATION_AND_MOVERS_PANELS_WRITE_SET.md @7e39422526), ON TOP OF the DB-b-309 branch head 75a71ae3: ONE new component PerformanceHoldingsPanels mounted once in ReportingTab, showing the allocation by asset class
(the existing ClassTotals over classTotalsView), the LARGEST POSITIONS (never called movers: the snapshot has no change field), and the worded states. CLIENT-FACING; the cell lives in the PORTAL repo (<root>/portal).

  DBP180-1-AC1  the diff: the agreed write set only, descent from 75a71ae3, the one mount, the new component's required words and imports, no "mover"
  DBP180-1-AC2  the behaviour: a probe renders the panels in the loading, failed, served and empty-node-free states
  DBP180-1-AC3  the proof: the cell's tests, every irpt-dashbd test, the typecheck and the production build pass, and the build carries neither the banner nor the fixture

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
        spec = importlib.util.spec_from_file_location("p175_for_180", str(Path(__file__).resolve().parent / "p175_portal_template_mount.py"))
        P175 = importlib.util.module_from_spec(spec)
        sys.modules["p175_for_180"] = P175
        spec.loader.exec_module(P175)
    return P175


IR = "src/pages/InvestorReporting/"
# AMENDMENT 1 (2026-10-16 ~23:3xZ, CTO ruling A, DB-b-316): the panels are folded into the smoke branch, so the branch is the template-mount branch and the base is its head 355b3bf8
BRANCH = "cand/dell2/irpt-49f-performance-template-mount"
BASE = "355b3bf85fd2e565ae121c5be6562668a9c94072"
TAB = IR + "tabs/reporting/ReportingTab.tsx"
PANELS = IR + "tabs/reporting/PerformanceHoldingsPanels.tsx"
TESTS = IR + "__tests__/irpt-dashbd/"
ALLOWED_EXACT = {TAB, PANELS, IR + "__tests__/fe-s-10/parity.test.ts"}  # AMENDMENT 2 (DB-b-316): the parity fixture
PROBE = TESTS + "_p180_probe.test.tsx"
WORDS = ["Largest positions", "Loading this client's holdings.", "This client's holdings could not be loaded.",
         "Allocation over time is not published for this client yet.", "Attribution is not published for this client yet.",
         "Sector breakdown is not published for this client yet."]
IMPORTS = ["classTotalsView", "ClassTotals", "securityRowsFrom", "foldSecurityRows"]


def check_diff(root):
    p175 = load_p175()
    p = p175.portal(root)
    br, _ = p175.git(p, "rev-parse", "--abbrev-ref", "HEAD")
    p175.need(br.strip() == BRANCH, "the portal branch must be %s (stacked on the DB-b-309 head), it is %s" % (BRANCH, br.strip()))
    _, rc = p175.git(p, "merge-base", "--is-ancestor", BASE, "HEAD")
    p175.need(rc == 0, "the DB-b-309 head %s is not an ancestor of this branch" % BASE[:8])
    out, rc = p175.git(p, "diff", "--name-only", BASE, "HEAD")
    p175.need(rc == 0, "cannot diff against %s" % BASE[:8])
    changed = {x for x in out.splitlines() if x.strip()}
    p175.need(changed, "nothing changed since the DB-b-309 head")
    extra = [f for f in changed if f not in ALLOWED_EXACT and not (f.startswith(TESTS) and f.rsplit("/", 1)[-1].startswith("performance-holdings-panels"))]
    p175.need(not extra, "portal files outside the agreed write set changed: %s" % extra[:4])
    p175.need(PANELS in changed and TAB in changed, "the new component and the one mount must both be in the diff")
    p175.need(any(f.startswith(TESTS + "performance-holdings-panels") for f in changed), "no test file named performance-holdings-panels* in the diff")
    stat, _ = p175.git(p, "diff", "--numstat", BASE, "HEAD", "--", TAB)
    nums = stat.split()
    p175.need(len(nums) >= 2 and nums[0].isdigit() and int(nums[0]) + int(nums[1]) <= 28, "ReportingTab.tsx may change only by the panels mount and the client-firm gate (at most 28 lines against 355b3bf8, the gate rewrite included): %s" % stat.strip())
    t = lambda f: (p / f).read_text(encoding="utf-8")  # noqa: E731
    tab, panels = t(TAB), t(PANELS)
    p175.need(tab.count("<PerformanceHoldingsPanels") == 1 and "PerformanceHoldingsPanels" in tab.split("export")[0] + tab, "ReportingTab.tsx must mount <PerformanceHoldingsPanels once")
    p175.need(re.search(r"<PerformanceHoldingsPanels[^>]*snapshot=\{header\?\.snapshot", tab) is not None, "the mount must pass snapshot={header?.snapshot ?? null}")
    for w in WORDS:
        p175.need(w in panels, "the component lacks the sentence: %s" % w)
    for name in IMPORTS:
        p175.need(re.search(r"\b%s\b" % name, panels) is not None, "the component must reuse %s" % name)
    p175.need("mover" not in panels.lower(), "the word 'mover' must not appear in the component (the snapshot has no change field)")
    p175.need("getHoldingsSnapshot" not in panels, "the component must not fetch a snapshot of its own")
    return True


PROBE_TEXT = """import { describe, expect, test } from 'bun:test'
import { createElement } from 'react'
import { renderToStaticMarkup } from 'react-dom/server'
import { PerformanceHoldingsPanels } from '../../tabs/reporting/PerformanceHoldingsPanels'

const served = {
  nodes: [],
  classTotals: [
    { assetClass: 'equity', amount: 600, currency: 'USD', weight: 0.6 },
    { assetClass: 'cash', amount: 400, currency: 'USD', weight: 0.4 },
  ],
  classTotalsRemainder: null,
  classTotalsTarget: null,
} as never

const render = (snapshot: unknown, failed: boolean) =>
  renderToStaticMarkup(createElement(PerformanceHoldingsPanels as never, { snapshot, failed } as never))

const text = (html: string) => html.replace(/<[^>]*>/g, ' ').replace(/&#x27;/g, "'").replace(/\\s+/g, ' ').trim()

describe('p180 probe', () => {
  test('loading and failed are worded, never an empty node', () => {
    expect(text(render(null, false))).toContain("Loading this client's holdings.")
    expect(text(render(null, true))).toContain("This client's holdings could not be loaded.")
  })
  test('a snapshot without a nodes array never throws: the worded state shows (page owner msg 10063)', () => {
    for (const odd of [{}, { nodes: null }, { classTotals: [] }] as never[]) {
      const t = text(render(odd, false))
      expect(t.length).toBeGreaterThan(20)
      expect(t).toContain("This client's holdings could not be loaded.")
    }
  })
  test('a served snapshot shows the allocation by asset class and Largest positions', () => {
    const t = text(render(served, false))
    expect(t).toContain('Held positions by asset class')
    expect(t).toContain('Largest positions')
    expect(t.toLowerCase()).not.toContain('mover')
  })
  test('the two absent panels say so in one sentence each', () => {
    const t = text(render(served, false))
    expect(t).toContain('Allocation over time is not published for this client yet.')
    expect(t).toContain('Attribution is not published for this client yet.')
    expect(t).toContain('Sector breakdown is not published for this client yet.')
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
    have = any(f.name.startswith("performance-holdings-panels") for f in (p / TESTS).glob("*"))
    p175.need(have, "the cell's test file performance-holdings-panels* is missing")
    return p175.check_proof(root)


CHECKS = {"DBP180-1-AC1": check_diff, "DBP180-1-AC2": check_behaviour, "DBP180-1-AC3": check_proof}

if __name__ == "__main__":
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DBP180-1-AC1": "OK: only the agreed write set changed, descent from the DB-b-309 head, the one mount passing the header's snapshot, the required sentences and reuse, and no mover word",
               "DBP180-1-AC2": "OK: the panels render the loading and failed sentences, the allocation by asset class and Largest positions for a served snapshot, and the two worded absent lines",
               "DBP180-1-AC3": "OK: the cell's test file exists; every irpt-dashbd test passes, the typecheck passes and the production build carries neither the banner nor the fixture"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
