"""IRPT_DASHBD round 150, workstream CHARTGAP (issuer 2.0.0_SA_COO~D2) -- DB-b-330, the CTO's defect (msg 10331 (a)): the Performance chart was BLANK for any
window holding a day with no return, because the curve waited on a MEASURED window (DashboardPerformance.tsx built the drawn values only when view.status was MEASURED).
The chart must draw every measured segment, with a visible break at each day that has no return and at each trading day the source did not report. The headline
figure keeps its rule (BREAK shows "Not measured"). PORTAL repo cell (<root>/portal), on a new branch cut from the pinned DEV head; CLIENT-FACING, so it reaches DEV only
through .tools/portal-merge-forward.sh on an approved row.

  DBP196-1-AC1  the diff and the source: only DashboardPerformance.tsx (at most 120 changed lines) and test files named dashboard-chart-breaks* changed since the pin, all committed;
                chartRows is exported, reads the served unreported list, no longer gates on MEASURED, keeps connectNulls false, maps the brush through the rows
  DBP196-1-AC2  the behaviour: the cell's own tests pass, and the issuer's probe (run from the checker, deleted after) passes against the worker's chartRows
  DBP196-1-AC3  the proof: every irpt-dashbd test and every dsgn-irptv1 test but the two that fail at the base (ExportBundle.ts drift), the typecheck and the production build pass (the p175 build scan: no preview banner, no fixture)

Usage: python <this file> <repo_root> <criterion_id>        prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <repo_root_of_reference_with_uncommitted_edit>
"""
import importlib.util
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P175 = None


def load_p175():
    global P175
    if P175 is None:
        spec = importlib.util.spec_from_file_location("p175_for_196", str(HERE.parent / "r149" / "p175_portal_template_mount.py"))
        P175 = importlib.util.module_from_spec(spec)
        sys.modules["p175_for_196"] = P175
        spec.loader.exec_module(P175)
    return P175


IR = "src/pages/InvestorReporting/"
BRANCH = "cand/dell2/irpt-performance-chart-breaks"
BASE = "38d4f9473284a585bc217981213b9516e29d3a87"
DASH = IR + "dashboard/DashboardPerformance.tsx"
TESTS = IR + "__tests__/irpt-dashbd/"
TEST_PREFIX = "dashboard-chart-breaks"
PROBE = TESTS + "_p196_probe.test.ts"
MAX_LINES = 120

PROBE_TEXT = """import { describe, expect, test } from 'bun:test'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { chartRows, performanceView, type WindowSelection } from '../../dashboard/DashboardPerformance'
import { readSeries, type SeriesDocument } from '../../dashboard/seriesContract'

const FIXTURES = fileURLToPath(new URL('./fixtures/', import.meta.url))
const WHOLE: WindowSelection = { kind: 'custom', start: '2026-07-10', end: '2026-08-14' }
const LATE: WindowSelection = { kind: 'custom', start: '2026-07-20', end: '2026-08-14' }

function served(name: string, nullDay?: string, extraUnreported?: string): SeriesDocument {
  const raw = JSON.parse(readFileSync(`${FIXTURES}${name}`, 'utf8')) as Record<string, any>
  if (nullDay !== undefined) {
    const i = (raw.date as string[]).indexOf(nullDay)
    raw.total_return_daily[i] = null
    raw.day_quality[i] = 'NOT_MEASURABLE'
  }
  if (extraUnreported !== undefined) raw.unreported_trading_days = [extraUnreported, ...raw.unreported_trading_days]
  const read = readSeries(raw)
  if (!read.ok) throw new Error(`${name} was refused: ${JSON.stringify(read.refusal)}`)
  return read.document
}

describe('p196 probe', () => {
  test('BREAK window still draws its measured days, null at the no-return day', () => {
    const series = served('series-unreported-days.json', '2026-07-29')
    const view = performanceView(series, LATE)
    expect(view.status).toBe('BREAK')
    const rows = chartRows(series, view)
    expect(rows.filter((r) => r.cumulative !== null).length).toBeGreaterThan(5)
    expect(rows.find((r) => r.date === '2026-07-29')?.cumulative).toBeNull()
    expect(rows.find((r) => r.date === '2026-08-03')?.cumulative).not.toBeNull()
  })
  test('the values are the linked path, day for day', () => {
    const series = served('series-unreported-days.json', '2026-07-29')
    const view = performanceView(series, LATE)
    const rows = chartRows(series, view)
    expect(view.path.length).toBeGreaterThan(5)
    for (const p of view.path) expect(rows.find((r) => r.date === p.date)?.cumulative).toBe(p.cumulative)
  })
  test('unreported days become valueless gap rows, in date order, inside the history only', () => {
    const series = served('series-unreported-days.json', undefined, '2026-07-01')
    const rows = chartRows(series, performanceView(series, WHOLE))
    expect(rows.filter((r) => r.gap).map((r) => r.date)).toEqual(['2026-07-14', '2026-07-15', '2026-08-05'])
    expect(rows.filter((r) => r.gap).every((r) => r.cumulative === null && !r.isolated)).toBe(true)
    expect(rows.length).toBe(series.date.length + 3)
    for (let i = 1; i < rows.length; i++) expect(rows[i].date > rows[i - 1].date).toBe(true)
  })
  test('no statement of unreported days adds no row', () => {
    const series = served('series-no-statement.json')
    expect(chartRows(series, performanceView(series, WHOLE)).length).toBe(series.date.length)
  })
  test('a MEASURED window has a value on every served day of it', () => {
    const series = served('series-unreported-empty.json')
    const view = performanceView(series, LATE)
    expect(view.status).toBe('MEASURED')
    const inWindow = chartRows(series, view).filter((r) => r.date >= LATE.start && r.date <= LATE.end)
    expect(inWindow.length).toBeGreaterThan(5)
    expect(inWindow.every((r) => r.cumulative !== null && !r.gap)).toBe(true)
  })
  test('a day outside the window has no value', () => {
    const series = served('series-unreported-days.json', '2026-07-29')
    const rows = chartRows(series, performanceView(series, LATE))
    const before = rows.filter((r) => r.date < LATE.start)
    expect(before.length).toBeGreaterThan(2)
    expect(before.every((r) => r.cumulative === null)).toBe(true)
  })
  test('isolated: a measured day between two breaks only', () => {
    const series = served('series-unreported-days.json', '2026-07-17')
    const rows = chartRows(series, performanceView(series, WHOLE))
    const byDate = new Map(rows.map((r) => [r.date, r]))
    expect(byDate.get('2026-07-16')?.isolated).toBe(true)
    expect(byDate.get('2026-07-20')?.isolated).toBe(false)
    expect(rows.filter((r) => r.isolated).every((r) => r.cumulative !== null)).toBe(true)
  })
})
"""


def need(cond, msg):
    load_p175().need(cond, msg)


def check_diff(root, branch=BRANCH, git_scope=True):
    p175 = load_p175()
    p = p175.portal(root)
    if git_scope:
        br, _ = p175.git(p, "rev-parse", "--abbrev-ref", "HEAD")
        need(br.strip() == branch, "the portal branch must be %s, it is %s" % (branch, br.strip()))
        _, rc = p175.git(p, "merge-base", "--is-ancestor", BASE, "HEAD")
        need(rc == 0, "the pinned DEV head %s is not an ancestor of this branch" % BASE[:8])
        out, rc = p175.git(p, "diff", "--name-only", BASE, "HEAD")
        need(rc == 0, "cannot diff against %s" % BASE[:8])
        changed = {x for x in out.splitlines() if x.strip()}
        need(changed, "nothing changed since the pinned DEV head")
        extra = [f for f in changed if f != DASH and not (f.startswith(TESTS) and f.rsplit("/", 1)[-1].startswith(TEST_PREFIX))]
        need(not extra, "portal files outside the agreed write set changed: %s" % extra[:4])
        need(DASH in changed and any(f.startswith(TESTS + TEST_PREFIX) for f in changed), "DashboardPerformance.tsx and a test file named %s* must both be committed" % TEST_PREFIX)
        stat, _ = p175.git(p, "diff", "--numstat", BASE, "HEAD", "--", DASH)
        nums = stat.split()
        need(len(nums) >= 2 and nums[0].isdigit() and int(nums[0]) + int(nums[1]) <= MAX_LINES, "DashboardPerformance.tsx may change by at most %d lines: %s" % (MAX_LINES, stat.strip()))
        dirty, _ = p175.git(p, "diff", "HEAD", "--name-only")
        need(not dirty.strip(), "uncommitted edits to tracked files: %s" % dirty.split()[:3])
    text = (p / DASH).read_bytes().decode("utf-8").replace("\r\n", "\n")
    need("export function chartRows(" in text, "chartRows is not exported")
    body = text.split("export function chartRows(", 1)[1].split("\nfunction ", 1)[0]
    need("unreported_trading_days" in body, "chartRows must read the served unreported_trading_days")
    need("MEASURED" not in body, "chartRows must not gate the drawn values on a MEASURED window")
    need("sort(" in body, "chartRows must put the rows in date order")
    need("view.path" in body, "chartRows must draw the window's linked path")
    need("view.status === 'MEASURED' ? view.path" not in text, "the chart still builds its curve only for a MEASURED window")
    need("connectNulls={false}" in text and "connectNulls={true}" not in text and re.search(r"connectNulls(?!=\{false\})", text) is None, "the area must keep connectNulls={false} (a break is a break)")
    need("series.date[range.startIndex]" not in text and "series.date[range.endIndex]" not in text, "the brush must be mapped through the chart rows, not the served dates")
    need("<IsolatedDot" in text or re.search(r"dot=\{", text) is not None, "an isolated measured day must be drawn (a dot)")
    need('data-slot="dashboard-chart-breaks"' in text, "the chart must carry its one-sentence break note (data-slot dashboard-chart-breaks)")
    need("connectNulls" in text and len(re.findall(r"<Area[\s>]", text)) == 1, "exactly one <Area> is expected")
    return True


def run_tests(p, files, label, timeout=900):
    p175 = load_p175()
    bun = shutil.which("bun")
    need(bun is not None, "bun is not on the PATH")
    r = p175.run([bun, "test"] + files, p, timeout)
    out = (r.stdout + r.stderr)
    need(r.returncode == 0, "%s failed: %s" % (label, out[-700:].replace("\n", " | ")))
    need(re.search(r"\b[1-9]\d* pass", re.sub(r"\x1b\[[0-9;]*m", "", out)) is not None, "%s printed no pass count" % label)


def check_behaviour(root):
    p175 = load_p175()
    p = p175.portal(root)
    own = sorted(f for f in (p / TESTS).glob(TEST_PREFIX + "*") if f.is_file())
    need(own, "no test file named %s* under %s" % (TEST_PREFIX, TESTS))
    low = " ".join(f.read_text(encoding="utf-8") for f in own).lower()
    for word in ("break", "unreported", "isolated"):
        need(word in low, "the cell's test file does not speak of %s" % word)
    run_tests(p, [str(f.relative_to(p)).replace("\\", "/") for f in own], "the cell's tests")
    probe = p / PROBE
    probe.write_text(PROBE_TEXT, encoding="utf-8")
    try:
        run_tests(p, [PROBE], "the issuer's probe", 600)
    finally:
        if probe.exists():
            probe.unlink()
    return True


BASE_FAILS = 2  # iv-e-26.wire-regen and iv-e-98.generators-drift fail at the pinned DEV head on ExportBundle.ts drift (measured by the issuer, row W258-S1)
BASE_FAIL_TEXT = "byte-identical to the committed files: ExportBundle"


def dsgn_tests_except_base_failures(p):
    p175 = load_p175()
    bun = shutil.which("bun")
    need(bun is not None, "bun is not on the PATH")
    r = p175.run([bun, "test", IR + "__tests__/dsgn-irptv1"], p, 1500)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    # nested bun runs print their own summaries: the run's own is the LAST pair
    m = re.findall(r"^[ ]*(\d+) pass[ ]*$", out, re.M)
    f = re.findall(r"^[ ]*(\d+) fail[ ]*$", out, re.M)
    need(m and f and int(m[-1]) > 300, "the dsgn-irptv1 run printed no pass and fail summary")
    fails = int(f[-1])
    if fails == 0:
        return True
    need(fails == BASE_FAILS and out.count(BASE_FAIL_TEXT) >= BASE_FAILS and out.count("error: expect(received)") == BASE_FAILS,
         "the dsgn-irptv1 tests: %d fail, only the %d base failures (ExportBundle.ts drift) are allowed: %s" % (fails, BASE_FAILS, out[-500:].replace("\n", " | ")))
    return True


def check_proof(root):
    p175 = load_p175()
    p = p175.portal(root)
    need(any(f.name.startswith(TEST_PREFIX) for f in (p / TESTS).glob("*")), "the cell's test file %s* is missing" % TEST_PREFIX)
    dsgn_tests_except_base_failures(p)
    return p175.check_proof(root)


CHECKS = {"DBP196-1-AC1": check_diff, "DBP196-1-AC2": check_behaviour, "DBP196-1-AC3": check_proof}

# ---- selftest: the reference edit passes; every single-fault mutant of it fails AC1 or AC2 -------------------------------------------------------------
MUTANTS = [
    ("gate-on-measured-again", "const byDate = new Map(view.path.map((point) => [point.date, point.cumulative]))",
     "const byDate = new Map(view.status === 'MEASURED' ? view.path.map((point) => [point.date, point.cumulative]) : [])"),
    ("no-gap-rows", "if (!served.has(day) && day > first && day < last)", "if (false && !served.has(day) && day > first && day < last)"),
    ("gap-outside-history", "if (!served.has(day) && day > first && day < last)", "if (!served.has(day))"),
    ("no-sort", "  rows.sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0))\n", ""),
    ("gap-has-value", "rows.push({ date: day, cumulative: null, quality: '', gap: true })", "rows.push({ date: day, cumulative: 0, quality: '', gap: true })"),
    ("outside-window-zero", "cumulative: byDate.get(date) ?? null, quality", "cumulative: byDate.get(date) ?? 0, quality"),
    ("isolated-never", "isolated: row.cumulative !== null &&", "isolated: false && row.cumulative !== null &&"),
    ("isolated-on-null", "isolated: row.cumulative !== null &&", "isolated: row.cumulative === null &&"),
    ("isolated-needs-only-left", "&& (i === rows.length - 1 || rows[i + 1].cumulative === null),", ","),
    ("connect-nulls", "connectNulls={false}", "connectNulls"),
    ("brush-old-start", "const startRow = typeof range.startIndex === 'number' ? rows.slice(range.startIndex).find((row) => !row.gap) : undefined",
     "const startRow = typeof range.startIndex === 'number' ? { date: series.date[range.startIndex] } : undefined"),
    ("measured-gate-in-jsx", "const rows = chartRows(series, view)", "const rows = chartRows(series, view)\n  const _unused = view.status === 'MEASURED' ? view.path : []"),
    ("no-break-note", 'data-slot="dashboard-chart-breaks"', 'data-slot="dashboard-chart-note"'),
    ("no-dot", "dot={<IsolatedDot />}", ""),
    ("served-only-rows", "for (const day of series.unreported_trading_days ?? []) {", "for (const day of [] as string[]) {"),
]


def selftest(ref):
    p175 = load_p175()
    p = p175.portal(ref)
    f = p / DASH
    original = f.read_bytes()
    results = []
    try:
        check_diff(ref, git_scope=False)
        check_behaviour(ref)
        print("reference: AC1 and AC2 PASS")
        n = 0
        for name, old, new in MUTANTS:
            text = original.decode("utf-8").replace("\r\n", "\n")
            if old == new:
                continue
            if text.count(old) != 1:
                print("MUTANT %s: anchor matched %d times" % (name, text.count(old)))
                results.append((name, "ANCHOR"))
                continue
            f.write_bytes(text.replace(old, new).replace("\n", "\r\n").encode("utf-8"))
            try:
                check_diff(ref, git_scope=False)
                check_behaviour(ref)
                results.append((name, "SURVIVED"))
            except Exception as ex:
                results.append((name, "killed"))
                print("MUTANT %s killed: %s" % (name, str(ex)[:110]))
            n += 1
    finally:
        f.write_bytes(original)
        pr = p / PROBE
        if pr.exists():
            pr.unlink()
    bad = [r for r in results if r[1] != "killed"]
    print("selftest: %d mutants, %d not killed %s" % (len(results), len(bad), bad))
    return not bad


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        ok = selftest(sys.argv[2])
        print("SELFTEST " + ("PASS" if ok else "FAIL"))
        sys.exit(0 if ok else 1)
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DBP196-1-AC1": "OK: only DashboardPerformance.tsx (within the line cap) and the cell's test file changed since the pinned DEV head, committed; chartRows is exported, draws the window's path for every status, inserts the unreported days, keeps the area's nulls as breaks and maps the brush through the rows",
               "DBP196-1-AC2": "OK: the cell's tests and the issuer's probe pass against the worker's chartRows (a BREAK window draws its measured days, unreported days are valueless rows in date order, isolated days are marked)",
               "DBP196-1-AC3": "OK: every irpt-dashbd and dsgn-irptv1 test passes, the typecheck passes and the production build carries neither the SYNTHETIC PREVIEW banner nor the fixture"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
