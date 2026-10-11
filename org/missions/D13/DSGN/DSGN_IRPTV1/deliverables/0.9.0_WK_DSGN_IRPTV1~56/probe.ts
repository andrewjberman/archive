// Reader census probe (cell IV-e-100). Usage: bun run probe.ts <prod|dev>
// Imports the portal's own parser and readers from an OUTSIDE export of the commit (git archive), feeds each one the producer's
// own served body (captured offline from the producer's tests at the release's pin) wrapped as a v1 envelope, and records
// PASS or the refusing member. Every route has a passing control and a refusing control.
import { readFileSync } from 'node:fs'

const E = 'C:/dev/_irpt_private_evidence_20261009/DSGN_IRPTV1/0.9.0_WK_DSGN_IRPTV1~56'
const side = process.argv[2]
if (side !== 'prod' && side !== 'dev') throw new Error('side')
const C = `${E}/${side}/src/pages/InvestorReporting/contracts`
const env = await import(`${C}/envelope.ts`)
const own = await import(`${C}/owned-requests.ts`)

const load = (tree: string, name: string) => JSON.parse(readFileSync(`${E}/bodies_${tree}/${name}.json`, 'utf8'))
const clone = <T,>(v: T): T => JSON.parse(JSON.stringify(v))
const FIRM = 'fir_' + 'a'.repeat(24)
const wrap = (operation: string, data: unknown) => ({
  contract_version: 'v1', operation, firm_id: FIRM, data, unprojected_grant: { count: 0, denominator: 1, kinds: {} },
})
// The producer's captured tenant slug is replaced by a synthetic one: no real identifier is kept in a record.
const scrub = (v: any) => JSON.parse(JSON.stringify(v).replace(new RegExp('49' + 'financial', 'g'), 'tenant-synthetic'))

type Case = { route: string; id: string; kind: 'PASS' | 'REFUSE'; body: unknown; note: string }
const cases: Case[] = []
const add = (route: string, id: string, kind: 'PASS' | 'REFUSE', data: unknown, note: string) =>
  cases.push({ route, id, kind, body: wrap(route, scrub(data)), note })

// ---- analysis-request-history
const h6 = load('r6', 'history_upload'), h5u = load('r5', 'history_upload'), h5s = load('r5', 'history_selected'), h5x = load('r5', 'history_unreadable')
add('analysis-request-history', 'CONTROL revision-6 page (two keys)', 'PASS', h6, 'what the rolled-back build serves')
add('analysis-request-history', 'release-5 page, UPLOAD rows', 'PASS', h5u, 'unreadable_rows + client_id + client_claim')
add('analysis-request-history', 'release-5 page, SELECTED rows', 'PASS', h5s, 'client_id a string')
add('analysis-request-history', 'release-5 page, one UNREADABLE row', 'PASS', h5x, 'client_id null, claim UNREADABLE, unreadable_rows 1')
{ const d = clone(h5u); delete d.unreadable_rows; add('analysis-request-history', 'release-5 rows, page member unreadable_rows removed', 'PASS', d, 'isolates the row members') }
{ const d = clone(h5u); d.items.forEach((r: any) => { delete r.client_id; delete r.client_claim }); add('analysis-request-history', 'release-5 page, row members removed', 'PASS', d, 'isolates the page member') }
{ const d = clone(h6); d.zz_extra = 1; add('analysis-request-history', 'NEGATIVE CONTROL page with an unknown key zz_extra', 'REFUSE', d, 'unknown page key') }
{ const d = clone(h5u); d.items[0].zz_extra = 1; add('analysis-request-history', 'NEGATIVE CONTROL row with an unknown key zz_extra', 'REFUSE', d, 'unknown row key') }

// ---- analysis-request-read (the single-request reader)
const r6 = load('r6', 'read_plain'), r5 = load('r5', 'read_plain'), r5o = load('r5', 'read_opted')
add('analysis-request-read', 'CONTROL revision-6 plain read', 'PASS', r6, 'rolled-back build')
add('analysis-request-read', 'release-5 plain read', 'PASS', r5, 'identity + accepted_at')
add('analysis-request-read', 'release-5 read include=comparisons,composition', 'PASS', r5o, 'what the page asks for')
{ const d = clone(r5); d.persist_inputs = { report_index: null }; add('analysis-request-read', 'NEGATIVE CONTROL include=persist_inputs member', 'REFUSE', d, 'the portal never asks for it; reader has none') }
{ const d = clone(r5); d.client_id = null; add('analysis-request-read', 'NEGATIVE CONTROL a history-only member client_id', 'REFUSE', d, 'single read is not widened') }

// ---- analysis-report (sections)
const s6y = load('r6', 'sections_ycharts'), s6o = load('r6', 'sections_opal'), s5y = load('r5', 'sections_ycharts'), s5o = load('r5', 'sections_opal')
add('analysis-report', 'CONTROL revision-6 YCHARTS sections', 'PASS', s6y, 'rolled-back build')
add('analysis-report', 'CONTROL revision-6 OPAL_ENGINE sections', 'PASS', s6o, 'rolled-back build')
add('analysis-report', 'release-5 YCHARTS sections (+retained_ref)', 'PASS', s5y, 'retained_ref added')
add('analysis-report', 'release-5 OPAL_ENGINE sections (+retained_ref)', 'PASS', s5o, 'retained_ref added; computation_validation')
{ const d = clone(s5y); delete d.extraction_validation; add('analysis-report', 'NEGATIVE CONTROL YCHARTS sections without extraction_validation', 'REFUSE', d, 'required member absent') }
{ const d = clone(s5o); delete d.computation_validation; add('analysis-report', 'NEGATIVE CONTROL OPAL sections without computation_validation', 'REFUSE', d, 'required member absent') }
{ const d = clone(s5y); delete d.request_ref; add('analysis-report', 'NEGATIVE CONTROL sections without request_ref', 'REFUSE', d, 'required member absent') }

// ---- status-job (OPAL_ENGINE section dates)
const j5 = load('r5', 'status_job_opal').body
add('status-job', 'release-5 OPAL_ENGINE status answer (dates by branch)', 'PASS', j5, 'PER_SECTION with a null as_of_date row')
{ const d = clone(j5); d.source_dates.zz_extra = 1; add('status-job', 'NEGATIVE CONTROL unknown source_dates key', 'REFUSE', d, 'unknown key') }
{ const d = clone(j5); d.source_dates.section_dates[0].zz_extra = 1; add('status-job', 'NEGATIVE CONTROL unknown section_dates row key', 'REFUSE', d, 'unknown key') }
{ const d = clone(j5); d.zz_extra = 1; add('status-job', 'NEGATIVE CONTROL unknown status key', 'REFUSE', d, 'unknown key') }
{ const d = clone(j5); d.source_dates.date_basis = 'UNDATED_INPUT'; add('status-job', 'NEGATIVE CONTROL UNDATED_INPUT beside dated rows', 'REFUSE', d, 'reader equality rule') }

// ---- status-summary (unchanged by release 5: the contract fixture stands in)
const ss = JSON.parse(readFileSync(`${E}/r5/infra/aws/lambda/investor-reporting/_contracts/fixtures/PublicStatusEnvelope.valid.json`, 'utf8'))
const ssd = ss.instance ?? ss
add('status-summary', 'contract fixture PublicStatusEnvelope.valid (release 5 does not change this route)', 'PASS', ssd, 'unchanged route')
{ const d = clone(ssd); d.zz_extra = 1; add('status-summary', 'NEGATIVE CONTROL unknown status key', 'REFUSE', d, 'unknown key') }

// ---- analysis-request-pdf / analysis-request-original (unchanged by release 5)
const pdf = JSON.parse(readFileSync(`${E}/r5/infra/aws/lambda/investor-reporting/_contracts/fixtures/AnalysisRequestPdf.valid.json`, 'utf8'))
const pdfd = pdf.instance ?? pdf
for (const op of ['analysis-request-pdf', 'analysis-request-original']) {
  add(op, 'contract fixture AnalysisRequestPdf.valid (release 5 does not change this route)', 'PASS', pdfd, 'unchanged route')
  { const d = clone(pdfd); delete d.download_route; add(op, 'NEGATIVE CONTROL download_route absent', 'REFUSE', d, 'required member absent') }
}

const out: any[] = []
for (const c of cases) {
  let res: any
  try {
    const p = env.parseIrEnvelope(c.route, c.body)
    res = { result: 'PASS', refused: p.refused }
  } catch (e: any) {
    res = { result: 'REFUSES', field: e.field ?? null, message: String(e.message).slice(0, 120) }
  }
  const ok = (c.kind === 'PASS') === (res.result === 'PASS')
  out.push({ side, route: c.route, case: c.id, expected: c.kind, ...res, as_expected: ok, note: c.note })
}
// the inner history / single-request readers, called directly, to NAME the refusing member inside `data`
const inner: any[] = []
const tryInner = (label: string, fn: () => unknown) => {
  try { fn(); inner.push({ side, label, result: 'PASS' }) } catch (e: any) { inner.push({ side, label, result: 'REFUSES', message: String(e.message) }) }
}
tryInner('readOwnedHistory(release-5 page)', () => own.readOwnedHistory(scrub(h5u)))
{ const d = scrub(h5u); delete d.unreadable_rows; tryInner('readOwnedHistory(release-5 page minus unreadable_rows)', () => own.readOwnedHistory(d)) }
{ const d = scrub(h5u); d.items.forEach((r: any) => { delete r.client_claim }); delete d.unreadable_rows; tryInner('readOwnedHistory(minus unreadable_rows, minus client_claim)', () => own.readOwnedHistory(d)) }
{ const d = scrub(h5u); d.items.forEach((r: any) => { delete r.client_id }); delete d.unreadable_rows; tryInner('readOwnedHistory(minus unreadable_rows, minus client_id)', () => own.readOwnedHistory(d)) }
tryInner('readOwnedRequest(release-5 plain read)', () => own.readOwnedRequest(scrub(r5)))
tryInner('readOwnedRequest(a history row as the single read)', () => own.readOwnedRequest(scrub(h5u).items[0]))
// 'analysis-request-original' / 'pdf' operations: is there an adapter at this commit?
const adapters = Object.keys(env.IR_DATA_ADAPTER)
console.log(JSON.stringify({ side, adapter_has_pdf: adapters.includes('analysis-request-pdf'), adapter_has_original: adapters.includes('analysis-request-original'), cases: out, inner }, null, 1))
