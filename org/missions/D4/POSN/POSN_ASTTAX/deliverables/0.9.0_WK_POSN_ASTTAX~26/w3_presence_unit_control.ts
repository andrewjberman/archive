/**
 * POSN_ASTTAX.TO-W3-1 / W3-AC3 -- THE PRESENCE RULE, EXERCISED ON ITS EDGES.
 * RE-CUT 2026-09-15 ~05:2xZ (act 1, on this worker's row W26-S6).
 *
 * A UNIT CONTROL ON PURE FUNCTIONS, NOT A RENDER FIXTURE. It imports the REAL exported
 * helpers from the panel the page renders (never a copy of them, which would only test the
 * copy) and runs them over CONSTRUCTED column sets -- states today's served bytes do not
 * contain, which is the whole point: a class present ONLY in a benchmark column does not
 * exist in the 2026-09-11 models payload, so no screenshot can exercise it.
 *
 * TWO HELPERS, TWO LEVELS, BOTH EXERCISED:
 *   presentClassKeys(columns)       -- the rule over a column list  (cases b..f)
 *   presentClassKeysForView(spec)   -- WHICH COLUMNS A VIEW DRAWS   (cases a, a1, a2, a3)
 * The second is what the re-cut is about: the earlier build unioned the portfolio columns
 * into every view, so the Benchmark view listed a class no benchmark column held. Case a1
 * is that witness and FAILS against the superseded rule.
 *
 * THE LAST CASE IS A DELIBERATELY WRONG EXPECTATION and MUST print FAIL. Without it a
 * clean run proves only that the harness prints PASS. The exit code is 0 only when every
 * REAL case passes AND the deliberately wrong one failed.
 *
 * Run from portal/ (bun executes TS directly):
 *   bun ../org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~26/w3_presence_unit_control.ts
 */
import {
  presentClassKeys,
  presentClassKeysForView,
  type AssetClassKey,
  type ClassColumn,
  type ViewBasis,
} from '../../../../../../../portal/src/pages/Positioning/panels/PositioningSummary'

// The ASSET_CLASSES order the panel declares (PositioningSummary.tsx :79-92), written here
// as the EXPECTATION SIDE of case (c): if the helper ever returned first-seen order, or the
// declaration were reordered under it, this case fails rather than quietly re-ordering the page.
const DECLARED_ORDER: AssetClassKey[] = [
  'fixedIncome', 'equity', 'structured', 'commodities', 'alternatives',
]

const Z: Required<ClassColumn> = {
  fixedIncome: 0, equity: 0, structured: 0, commodities: 0, alternatives: 0,
}
const col = (patch: ClassColumn): ClassColumn => ({ ...Z, ...patch })

let realFailures = 0
let realCases = 0
let expectedFailureFired = false

const grade = (
  id: string,
  label: string,
  inputNote: string,
  got: AssetClassKey[],
  expected: AssetClassKey[],
  deliberatelyWrong = false
) => {
  const ok = JSON.stringify(got) === JSON.stringify(expected)
  if (deliberatelyWrong) {
    if (!ok) expectedFailureFired = true
  } else {
    realCases += 1
    if (!ok) realFailures += 1
  }
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${id}  ${label}`)
  console.log(`      input    = ${inputNote}`)
  console.log(`      expected = ${JSON.stringify(expected)}`)
  console.log(`      got      = ${JSON.stringify(got)}`)
}

const run = (
  id: string,
  label: string,
  columns: readonly ClassColumn[],
  expected: AssetClassKey[],
  deliberatelyWrong = false
) => grade(id, label, JSON.stringify(columns), presentClassKeys(columns), expected, deliberatelyWrong)

// A VIEW CASE: the portfolio / benchmark / relative column sets are constructed, and the
// helper is asked what the NAMED VIEW draws. `bookColumns` is the thunk the panel passes.
const runView = (
  id: string,
  label: string,
  view: { dataMode: ViewBasis; showCustom?: boolean; blendValid?: boolean },
  byBasis: Record<ViewBasis, readonly ClassColumn[]>,
  custom: Record<ViewBasis, ClassColumn>,
  expected: AssetClassKey[]
) => {
  const drawn: ViewBasis[] = [view.dataMode]
  if (view.showCustom) drawn.push('portfolio')
  const got = presentClassKeysForView({
    dataMode: view.dataMode,
    showCustom: !!view.showCustom,
    blendValid: !!view.blendValid,
    bookColumns: (basis) => byBasis[basis],
    customColumn: (basis) => custom[basis],
  })
  grade(id, label,
    `view=${view.dataMode}${view.showCustom ? ' +custom' : ''}` +
    `${view.showCustom ? ' blendValid=' + !!view.blendValid : ''}` +
    `  DRAWN BASES=${JSON.stringify([...new Set(drawn)])}` +
    `  columns=${JSON.stringify(byBasis)}`,
    got, expected)
}

console.log('W3-AC3 PRESENCE UNIT CONTROL -- helpers imported from')
console.log('  portal/src/pages/Positioning/panels/PositioningSummary.tsx (the rendered module)')
console.log(`  declared ASSET_CLASSES order = ${JSON.stringify(DECLARED_ORDER)}`)
console.log('')

// ---- THE VIEW RULE (the re-cut) ------------------------------------------------------
// One constructed payload used by cases a / a1 / a2 / a3, so the three views are asked
// about THE SAME BOOKS and only the VIEW differs -- which is the whole claim.
//   portfolio: Structured 5 (held by a portfolio, by NO benchmark)
//   benchmark: Commodities 5 (held by a benchmark, by NO portfolio)
const BOOKS: Record<ViewBasis, readonly ClassColumn[]> = {
  portfolio: [col({ fixedIncome: 55, equity: 40, structured: 5 })],
  benchmark: [col({ fixedIncome: 55, equity: 40, commodities: 5 })],
  relative:  [col({ fixedIncome: 0, equity: 0, structured: 5, commodities: -5 })],
}
const CUSTOM: Record<ViewBasis, ClassColumn> = {
  portfolio: col({ fixedIncome: 55, equity: 40, structured: 5 }),
  benchmark: col({ fixedIncome: 55, equity: 40, commodities: 5 }),
  relative:  col({ fixedIncome: 0, equity: 0, structured: 5, commodities: -5 }),
}

// (a) BENCHMARK VIEW: A CLASS NON-ZERO ONLY IN THE BENCHMARK COLUMNS IS PRESENT.
//     Commodities is held by no portfolio at all; the Benchmark view draws it, so the
//     legend and the rows must carry it. A rule reading only the model books would drop it
//     and the view would draw a bar with no legend entry.
runView('a', 'BENCHMARK view: a class non-zero ONLY in the benchmark columns -> PRESENT',
  { dataMode: 'benchmark' }, BOOKS, CUSTOM,
  ['fixedIncome', 'equity', 'commodities'])

// (a1) THE W26-S6 WITNESS -- BENCHMARK VIEW: A CLASS NON-ZERO ONLY IN THE PORTFOLIO
//      COLUMNS IS ABSENT. ITS OWN CONSTRUCTION, not a second reading of case (a)'s call:
//      here NO column outside the portfolios holds Structured at all, so the expectation
//      itself differs (a returns 3 keys, a1 returns 2) and the two cases cannot both be
//      satisfied by one behaviour. The shape is the SERVED one -- LT holds structured 1.5
//      and its benchmark holds 0 -- so this is the render's own defect in miniature: under
//      the superseded union rule the Benchmark view drew a Structured row of five zeros,
//      i.e. exactly the "showing all the floats" Andrew asked to stop (~00:4xZ / ~02:1xZ).
//      THIS CASE FAILS AGAINST THE SUPERSEDED RULE, which is what makes it evidence.
const BOOKS_PORTFOLIO_ONLY: Record<ViewBasis, readonly ClassColumn[]> = {
  portfolio: [col({ fixedIncome: 12.7, equity: 85.8, structured: 1.5 })],
  benchmark: [col({ fixedIncome: 15, equity: 85 })],
  relative:  [col({ fixedIncome: -2.3, equity: 0.8, structured: 1.5 })],
}
runView('a1', 'BENCHMARK view: a class non-zero ONLY in the portfolio columns -> ABSENT',
  { dataMode: 'benchmark' }, BOOKS_PORTFOLIO_ONLY, CUSTOM,
  ['fixedIncome', 'equity'])

// (a2) RELATIVE VIEW: A NON-ZERO DELTA IS PRESENT, whichever side holds it. Structured
//      (+5, portfolio side) and Commodities (-5, benchmark side) are both drawn; Fixed
//      Income and Equity net to zero and are not drawn at all (renderBarInner skips
//      `v === 0`), so they are absent.
runView('a2', 'RELATIVE view: a class with a non-zero delta on EITHER side -> PRESENT',
  { dataMode: 'relative' }, BOOKS, CUSTOM,
  ['structured', 'commodities'])

// (a3) CUSTOM VIEW draws BOTH bases (opaque = benchmark, translucent ghost = portfolio),
//      so the union is CORRECT there and only there; the Custom column joins on a valid
//      blend. Beyond the four asked, because it is the one view whose union is not a bug.
runView('a3', 'CUSTOM view (valid blend): benchmark bars + portfolio ghosts -> the UNION',
  { dataMode: 'benchmark', showCustom: true, blendValid: true }, BOOKS, CUSTOM,
  ['fixedIncome', 'equity', 'structured', 'commodities'])

// (a4) PORTFOLIO VIEW: only the portfolio columns are drawn, so the benchmark-only class
//      is absent -- the mirror of a1, and the case that proves a1 is about the VIEW rather
//      than about Structured.
runView('a4', 'PORTFOLIO view: a class non-zero ONLY in the benchmark columns -> ABSENT',
  { dataMode: 'portfolio' }, BOOKS, CUSTOM,
  ['fixedIncome', 'equity', 'structured'])

// ---- THE RULE ITSELF (unchanged by the re-cut) ---------------------------------------
console.log('')

// (b) A CLASS ZERO IN EVERY COLUMN IS ABSENT -- the rule Andrew ruled (~02:1xZ). Commodities
//     and Alternatives are zero in both columns here and appear in neither the legend nor
//     the rows.
run('b', 'class zero in EVERY column -> ABSENT',
  [col({ fixedIncome: 30, equity: 70 }), col({ fixedIncome: 40, equity: 60 })],
  ['fixedIncome', 'equity'])

// (c) THE RESULT PRESERVES ASSET_CLASSES ORDER, NOT THE COLUMNS' ORDER. The columns are fed
//     LAST-CLASS-FIRST on purpose: a first-seen implementation returns
//     ['alternatives','commodities','structured','equity','fixedIncome'] and fails here.
run('c', 'order is ASSET_CLASSES order, though the columns arrive reversed',
  [col({ alternatives: 3 }), col({ commodities: 4 }), col({ structured: 5 }),
   col({ equity: 6 }), col({ fixedIncome: 7 })],
  DECLARED_ORDER)

// (d) A NON-FINITE VALUE COUNTS AS ZERO. NaN / Infinity / -Infinity, and the Custom column's
//     '--' placeholder (typed through as unknown, because that is exactly how it would arrive
//     at runtime from an invalid blend) -- none of them is presence.
run('d', 'non-finite values (NaN, +Inf, -Inf, the Custom "--" string) count as ZERO',
  [col({ fixedIncome: NaN, equity: Infinity, structured: -Infinity,
         commodities: ('--' as unknown) as number, alternatives: 0 }),
   col({ equity: 12 })],
  ['equity'])

// (e) AN EMPTY COLUMN LIST RETURNS AN EMPTY SET -- the shape the caller must handle (the
//     panel falls back to the full declaration and renders its existing no-data state
//     rather than an empty section).
run('e', 'no columns at all -> empty set', [], [])

// (f) BEYOND THE FOUR ASKED, because the Relative view draws NEGATIVE numbers: a class
//     present only as a negative delta is still drawn, so it is still present.
run('f', 'a negative value is non-zero, so the class is PRESENT',
  [col({ fixedIncome: -2.5, equity: 2.5 })],
  ['fixedIncome', 'equity'])

// THE CONTROL THAT THE HARNESS CAN FAIL: a deliberately wrong expectation. If this prints
// PASS, every PASS above is worthless.
run('g', 'DELIBERATELY WRONG EXPECTATION -- this line MUST read FAIL',
  [col({ equity: 50 })],
  ['fixedIncome', 'equity'], true)

console.log('')
console.log(`REAL CASES: ${realCases} (a,a1,a2,a3,a4,b,c,d,e,f) -- failures ${realFailures} of ${realCases}`)
console.log(`FALSIFIER  : case g printed ${expectedFailureFired ? 'FAIL as required' : 'PASS -- THE HARNESS CANNOT FAIL'}`)
const rc = realFailures === 0 && expectedFailureFired ? 0 : 1
console.log(`RESULT: ${rc === 0 ? 'OK' : 'BLOCKED'} (exit ${rc})`)
process.exit(rc)
