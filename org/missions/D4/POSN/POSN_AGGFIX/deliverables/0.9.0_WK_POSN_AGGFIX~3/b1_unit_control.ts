/**
 * POSN_AGGFIX.TO-B1-1 (slot ~3) -- B1-AC4 UNIT CONTROL over the pure helpers in shared/bookSet.ts.
 *
 * Imports the RENDERED module (portal/src/pages/Positioning/shared/bookSet.ts at the worktree) and runs its
 * exported helpers over CONSTRUCTED inputs. capabilitiesFor is compared against the edf85ce503 copy of the same
 * file, passed as argv[2] by b1_unit_run.sh. The NEGATIVE CONTROL disables the remembered-choice check IN MEMORY
 * (a book list whose `includes` answers true for anything) and must report the client landing on 'AGG' --
 * proving that check, and nothing else, is what keeps a client off the aggregate.
 *
 * Usage (from portal/): bun <this> <absolute path of the base bookSet copy>
 */
import { pathToFileURL } from 'node:url'
import * as BS from '../../../../../../../portal/src/pages/Positioning/shared/bookSet.ts'

const basePath = process.argv[2]
if (!basePath) {
  console.log('usage: bun <this> <base bookSet copy>')
  process.exit(2)
}
const BASE = await import(pathToFileURL(basePath).href)

let pass = 0
let fail = 0
const J = (v: unknown) => JSON.stringify(v)
function check(id: string, what: string, input: unknown, expected: unknown, got: unknown) {
  const ok = J(expected) === J(got)
  if (ok) pass += 1
  else fail += 1
  console.log((ok ? 'PASS  ' : 'FAIL  ') + id.padEnd(4) + ' ' + what)
  console.log('      input    = ' + J(input))
  console.log('      expected = ' + J(expected))
  console.log('      got      = ' + J(got))
}

// ---- THE VIEWERS, AND THE PAGE PREDICATE READ AT THE BASE (B1-AC1) ------------------------------------------
// PAGE PREDICATE: firmId === 'opal-capital' OR userType === 'Dev' (AuthContext.tsx :736-738, :750-752;
// Positioning.tsx :267 @edf85ce503). The claim sets are the render harness's (b_five_books_dom.mjs VIEWERS).
const VIEWERS = {
  'opal-staff': { firmId: 'opal-capital', userType: null, advisorId: null, firmRole: null, advisorRole: null },
  advisor: { firmId: '49financial', userType: null, advisorId: 'b-harness-advisor', firmRole: 'user', advisorRole: 'architect' },
  client: { firmId: '49financial', userType: null, advisorId: null, firmRole: null, advisorRole: null },
} as const
const internalOf = (c: { firmId: string | null; userType: string | null }) =>
  c.firmId === 'opal-capital' || c.userType === 'Dev'

// ---- CONSTRUCTED PAYLOADS -----------------------------------------------------------------------------------
const holding = (ticker: string, weight: number, extra: Record<string, unknown> = {}) =>
  ({ ticker, name: ticker + ' fund', asset_class: 'Equity', sub_asset_class: 'Developed', weight, ...extra })
const CODES = ['UST', 'ST', 'INT', 'LT', 'ULT']
const shared = () => ({
  generated_at: '2026-09-15T00:00:00Z',
  data_as_of: '2026-09-14',
  portfolios: Object.fromEntries(CODES.map((c) => [c, { name: c }])),
  current_holdings: Object.fromEntries(CODES.map((c) => [c, { holdings: [holding('T' + c, 1)], aum: 100 }])),
}) as any
const AGG_BLOCK = {
  holdings: [holding('IEFA', 0.6, { model_breakdown: { INT: 0.1, LT: 0.2 } }), holding('VGSH', 0.4, { model_breakdown: { UST: 0.3 } })],
  total_aum: 500,
}
const payload = (status: string, holdings: unknown[]) => ({
  status, reason: status === 'OK' ? null : 'constructed: the weight read failed',
  generated_at: '2026-09-15T00:00:00Z', data_as_of: '2026-09-14',
  current_holdings: { AGG: { holdings, total_aum: 500 } },
  weights: { UST: 0.2, ST: 0.2, INT: 0.2, LT: 0.2, ULT: 0.2 },
  weights_source: { key: 'k', version_id: 'v', period: 'p' },
  members: { UST: 1, ST: 1, INT: 1, LT: 1, ULT: 1, blends: [] },
  left_out: [],
  reconciliation: { five_primary_sum: 5, members_sum: 5, file_total_model_aum: 5, gap: 0, gap_explanation_ref: 'r' },
}) as any
const OK = payload('OK', AGG_BLOCK.holdings)
const UNAVAILABLE_WITH_HOLDINGS = payload('UNAVAILABLE', AGG_BLOCK.holdings)
const OK_EMPTY = payload('OK', [])

console.log('B1-AC4 UNIT CONTROL -- helpers imported from portal/src/pages/Positioning/shared/bookSet.ts')
console.log('  exported helpers present: ' + J(['AGGREGATE_BOOK', 'hasOpalAggregate', 'mergeOpalAggregate',
  'resolveViewerBooks', 'rememberedBookFor', 'landingBook'].map((n) => n + '=' + typeof (BS as any)[n])))
console.log('  AGGREGATE_BOOK = ' + J(BS.AGGREGATE_BOOK) + '   PREFERRED_DEFAULT_BOOK = ' + J(BS.PREFERRED_DEFAULT_BOOK))
console.log('  viewers (claims -> page predicate): ' + J(Object.fromEntries(Object.entries(VIEWERS).map(([k, c]) => [k, internalOf(c)]))))
console.log('')

// ---- THE MERGE ----------------------------------------------------------------------------------------------
{
  const data = shared()
  const before = J(data)
  const got = BS.mergeOpalAggregate(data, OK) as any
  check('m1', 'status OK with holdings present: current_holdings.AGG is merged into the data, the five books untouched',
    { payload: 'status OK, AGG holdings 2' },
    { agg: AGG_BLOCK.holdings, five: J(data.current_holdings.UST) + J(data.current_holdings.ULT), inputUnmutated: true },
    { agg: got?.current_holdings?.AGG?.holdings, five: J(got?.current_holdings?.UST) + J(got?.current_holdings?.ULT), inputUnmutated: J(data) === before })
}
{
  const data = shared()
  const got = BS.mergeOpalAggregate(data, UNAVAILABLE_WITH_HOLDINGS) as any
  check('m2', 'status UNAVAILABLE merges nothing -- even with holdings in the payload (the status gate, not the emptiness)',
    { payload: 'status UNAVAILABLE, AGG holdings 2' },
    { hasAggKey: false, sameObject: true }, { hasAggKey: 'AGG' in (got?.current_holdings ?? {}), sameObject: got === data })
}
{
  const data = shared()
  const got = BS.mergeOpalAggregate(data, OK_EMPTY) as any
  check('m3', 'status OK with EMPTY holdings merges nothing',
    { payload: 'status OK, AGG holdings 0' },
    { hasAggKey: false, sameObject: true }, { hasAggKey: 'AGG' in (got?.current_holdings ?? {}), sameObject: got === data })
}
{
  const data = shared()
  const got = BS.mergeOpalAggregate(data, null) as any
  check('m4', 'no payload (query disabled for this viewer) merges nothing',
    { payload: null }, { sameObject: true }, { sameObject: got === data })
}

// ---- THE VIEWER-SCOPED BOOK SET -----------------------------------------------------------------------------
const merged = BS.mergeOpalAggregate(shared(), OK)
const plain = shared()
const codes = Object.keys(plain.portfolios)
const staffBooks = BS.resolveViewerBooks('models', codes, { internal: internalOf(VIEWERS['opal-staff']) }, merged)
check('b1', 'internal viewer, aggregate merged: Aggregate FIRST, then the five in declared order',
  { viewer: 'opal-staff', internal: true, merged: true }, ['AGG', ...CODES], staffBooks)
check('b2', 'internal viewer, nothing merged: no Aggregate',
  { viewer: 'opal-staff', internal: true, merged: false }, CODES,
  BS.resolveViewerBooks('models', codes, { internal: true }, plain))
check('b3', 'advisor, even with the aggregate present in the data: no Aggregate',
  { viewer: 'advisor', internal: internalOf(VIEWERS.advisor), merged: true }, CODES,
  BS.resolveViewerBooks('models', codes, { internal: internalOf(VIEWERS.advisor) }, merged))
check('b4', 'client, even with the aggregate present in the data: no Aggregate',
  { viewer: 'client', internal: internalOf(VIEWERS.client), merged: true }, CODES,
  BS.resolveViewerBooks('models', codes, { internal: internalOf(VIEWERS.client) }, merged))
check('b5', 'internal viewer in ETFs mode with an aggregate in the data: no Aggregate (a rollup of the MODEL books only)',
  { viewer: 'opal-staff', mode: 'etfs', merged: true }, BS.resolveBooks('etfs', ['DIVZ']),
  BS.resolveViewerBooks('etfs', ['DIVZ'], { internal: true }, merged))
check('b6', 'the five-book resolution itself is unchanged: resolveBooks(models) equals the base module\'s',
  { mode: 'models', codes }, BASE.resolveBooks('models', codes), BS.resolveBooks('models', codes))

// ---- THE REMEMBERED CHOICE ----------------------------------------------------------------------------------
const clientBooks = BS.resolveViewerBooks('models', codes, { internal: internalOf(VIEWERS.client) }, merged)
check('r1', "client with a remembered 'AGG': falls back to the ordinary default",
  { remembered: 'AGG', books: clientBooks }, BS.PREFERRED_DEFAULT_BOOK, BS.landingBook('AGG', clientBooks))
check('r2', "internal viewer with the aggregate merged and a remembered 'AGG': honoured",
  { remembered: 'AGG', books: staffBooks }, 'AGG', BS.landingBook('AGG', staffBooks))
check('r3', "internal viewer, aggregate NOT merged, remembered 'AGG': falls back to the ordinary default",
  { remembered: 'AGG', books: CODES }, BS.PREFERRED_DEFAULT_BOOK,
  BS.landingBook('AGG', BS.resolveViewerBooks('models', codes, { internal: true }, plain)))
check('r4', "client with a remembered 'ST': honoured (a real book in the client's own set)",
  { remembered: 'ST', books: clientBooks }, 'ST', BS.landingBook('ST', clientBooks))
check('r5', 'client with nothing remembered: the ordinary default',
  { remembered: null, books: clientBooks }, BS.PREFERRED_DEFAULT_BOOK, BS.landingBook(null, clientBooks))
check('r6', "rememberedBookFor keeps a code only when the viewer's own set holds it",
  { client: ['AGG', 'LT'], staff: ['AGG'] }, [null, 'LT', 'AGG'],
  [BS.rememberedBookFor('AGG', clientBooks), BS.rememberedBookFor('LT', clientBooks), BS.rememberedBookFor('AGG', staffBooks)])

// ---- capabilitiesFor, IDENTICAL TO edf85ce503 FOR EVERY MODE ------------------------------------------------
const modes = BASE.POSITIONING_MODES as string[]
const baseCaps = Object.fromEntries(modes.map((m) => [m, BASE.capabilitiesFor(m)]))
const nowCaps = Object.fromEntries(modes.map((m) => [m, BS.capabilitiesFor(m as any)]))
check('c1', 'capabilitiesFor(mode) output identical to the edf85ce503 version for every mode (' + modes.length + ' of ' + modes.length + ')',
  { modes }, baseCaps, nowCaps)
check('c2', 'no capability key names an aggregate, in any mode',
  { keys: Object.keys(nowCaps.models ?? {}) }, 0,
  Object.values(nowCaps).flatMap((c) => Object.keys(c as object)).filter((k) => /agg/i.test(k)).length)

// ---- NEGATIVE CONTROL: THE REMEMBERED-CHOICE CHECK DISABLED IN MEMORY ---------------------------------------
// A copy of the client's book list whose `includes` answers true for every code: the membership test inside
// rememberedBookFor can no longer refuse anything. Nothing in the module is edited.
const leaky = Object.assign([...clientBooks], { includes: () => true }) as unknown as string[]
const landed = BS.landingBook('AGG', leaky)
const fired = landed === 'AGG'
console.log('')
console.log('NEGATIVE CONTROL (the check disabled in memory: the client book list\'s includes() always true)')
console.log('      client book list = ' + J([...clientBooks]) + '  remembered = "AGG"')
console.log('      client lands on  = ' + J(landed) + '   ' + (fired
  ? "CONTROL FIRED: with the check disabled the client lands on 'AGG'"
  : 'CONTROL DID NOT FIRE -- the check is not what keeps the client off the aggregate'))

console.log('')
console.log('REAL CASES ' + (pass + fail) + '   PASS ' + pass + '   FAIL ' + fail + '   NEGATIVE CONTROL ' + (fired ? 'FIRED' : 'NOT FIRED'))
process.exit(fail === 0 && fired ? 0 : 1)
