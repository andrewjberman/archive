/**
 * POSN_ASTTAX.TO-W3-1 / W3-AC3 -- THE PRESENCE RULE, EXERCISED ON ITS EDGES.
 *
 * A UNIT CONTROL ON A PURE FUNCTION, NOT A RENDER FIXTURE. It imports the REAL exported
 * helper from the panel the page renders (never a copy of it, which would only test the
 * copy) and runs it over CONSTRUCTED column sets -- states today's served bytes do not
 * contain, which is the whole point: a class present ONLY in a benchmark column does not
 * exist in the 2026-09-11 models payload, so no screenshot can exercise it.
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
  type AssetClassKey,
} from '../../../../../../../portal/src/pages/Positioning/panels/PositioningSummary'

type Column = Partial<Record<AssetClassKey, number>>

// The ASSET_CLASSES order the panel declares (PositioningSummary.tsx :79-92), written here
// as the EXPECTATION SIDE of case (c): if the helper ever returned first-seen order, or the
// declaration were reordered under it, this case fails rather than quietly re-ordering the page.
const DECLARED_ORDER: AssetClassKey[] = [
  'fixedIncome', 'equity', 'structured', 'commodities', 'alternatives',
]

const Z: Required<Column> = {
  fixedIncome: 0, equity: 0, structured: 0, commodities: 0, alternatives: 0,
}
const col = (patch: Column): Column => ({ ...Z, ...patch })

let realFailures = 0
let expectedFailureFired = false

const run = (
  id: string,
  label: string,
  columns: readonly Column[],
  expected: AssetClassKey[],
  deliberatelyWrong = false
) => {
  const got = presentClassKeys(columns)
  const ok = JSON.stringify(got) === JSON.stringify(expected)
  const verdict = ok ? 'PASS' : 'FAIL'
  if (deliberatelyWrong) {
    if (!ok) expectedFailureFired = true
  } else if (!ok) {
    realFailures += 1
  }
  console.log(`${verdict}  ${id}  ${label}`)
  console.log(`      input    = ${JSON.stringify(columns)}`)
  console.log(`      expected = ${JSON.stringify(expected)}`)
  console.log(`      got      = ${JSON.stringify(got)}`)
}

console.log('W3-AC3 PRESENCE UNIT CONTROL -- helper imported from')
console.log('  portal/src/pages/Positioning/panels/PositioningSummary.tsx (the rendered module)')
console.log(`  declared ASSET_CLASSES order = ${JSON.stringify(DECLARED_ORDER)}`)
console.log('')

// (a) A class NON-ZERO ONLY IN THE BENCHMARK COLUMN IS PRESENT. The portfolio columns hold
//     no Structured at all; the benchmark column does. A rule reading only the model books
//     would drop it, and the Benchmark view would draw a bar with no legend entry.
run('a', 'class non-zero ONLY in the benchmark column -> PRESENT',
  [col({ fixedIncome: 60, equity: 40 }), col({ fixedIncome: 55, equity: 40, structured: 5 })],
  ['fixedIncome', 'equity', 'structured'])

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
console.log(`REAL CASES: 6 (a,b,c,d,e,f) -- failures ${realFailures} of 6`)
console.log(`FALSIFIER  : case g printed ${expectedFailureFired ? 'FAIL as required' : 'PASS -- THE HARNESS CANNOT FAIL'}`)
const rc = realFailures === 0 && expectedFailureFired ? 0 : 1
console.log(`RESULT: ${rc === 0 ? 'OK' : 'BLOCKED'} (exit ${rc})`)
process.exit(rc)
