// r19 AR-y-202 supplementary: the deployed stored-row NEEDS_CORRECTION shape (uploads.py:411-415, _answer), built from the
// moved answer's own findings. NOT a door run: labelled as constructed. Runs the portal's own readers at PROD and DEV.
import { readFileSync, writeFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'

const S = 'C:/dev/wk-irpt-anlreq-57/.scratch/r19'
const COMMITS: Record<string, string> = { PROD: `${S}/prod`, DEV: `${S}/dev` }
const bodies: Record<string, { answer: any }> = JSON.parse(readFileSync(`${S}/run_hr/answer_bodies.json`, 'utf8'))
const SHEETS = ['total_row_sheet', 'two_value_account_sheet', 'repair_header_two_values', 'brokerage_two_account', 'header_repeated_csv']
const ANSWERS = { advisor: 'Adv', firm: 'FIRM-1', household: 'HH', report_type: 'Overview', comparison_model: '' }
const errText = (e: any) => `${e?.name ?? 'Error'}: ${String(e?.message ?? e).slice(0, 200)}`

const out: any[] = []
for (const commit of Object.keys(COMMITS)) {
  const root = COMMITS[commit]
  const env = await import(pathToFileURL(`${root}/src/pages/InvestorReporting/contracts/envelope.ts`).href)
  const tc = await import(pathToFileURL(`${root}/src/pages/TicketCenter/analysisRequest.ts`).href)
  const pr = await import(pathToFileURL(`${root}/src/pages/InvestorReporting/tabs/analysis/prospect.ts`).href)
  for (const sheet of SHEETS) {
    const moved = bodies[`${sheet}|moved`].answer
    const findings = moved.findings ?? []
    // uploads.py:411-415 _answer NEEDS_CORRECTION: upload_id, input_id None, state, reason (retained), findings, findings_total
    const body = { upload_id: moved.upload_id, input_id: null, state: 'NEEDS_CORRECTION', reason: 'TEMPLATE_FINDINGS',
      findings, findings_total: findings.length }
    const codes = [...new Set(findings.map((f: any) => f.code))]
    const base = { case: sheet, arm: 'AFTER', body_source: 'constructed from uploads.py:411-415 (_answer NEEDS_CORRECTION shape) carrying the moved answer findings; not a door run',
      commit, commit_sha: commit === 'PROD' ? '37aa1247ee4ba487e5610dc5b78d65ae28468a99' : '64980b4d3a1e11d8407b6a263ddcd5447dafaef2',
      codes, body_keys: Object.keys(body).sort() }
    let adapted: any = null
    let parseErr: string | null = null
    try {
      adapted = env.parseIrEnvelope('analysis-input-upload', { contract_version: env.IR_CONTRACT_VERSION,
        operation: 'analysis-input-upload', firm_id: 'FIRM-1', data: body, unprojected_grant: { count: 0, denominator: 0, kinds: {} } }).data
    } catch (e: any) { parseErr = errText(e) }
    out.push({ ...base, reader: 'contracts/envelope.ts parseIrEnvelope (analysis-input-upload)', outcome: parseErr ? 'THREW' : 'RETURNED', error: parseErr })
    const ir = { uploadAnalysisInput: async () => env.parseIrEnvelope('analysis-input-upload', { contract_version: env.IR_CONTRACT_VERSION,
      operation: 'analysis-input-upload', firm_id: 'FIRM-1', data: body, unprojected_grant: { count: 0, denominator: 0, kinds: {} } }).data }
    const tickets = { createTicket: async (x: any) => ({ ticket: { ticket_id: 'T-1', title: x.title, answers: x.answers, attachment: x.attachment } }),
      recordTicketReport: async () => ({}) }
    let ticketOut: any = null
    let ticketErr: string | null = null
    try {
      ticketOut = await tc.fileAnalysisRequest({ ir, tickets, wait: async () => {} },
        { title: 'T', answers: ANSWERS, upload: { upload_token: 'tok', file_type: 'csv', file_base64: 'eA==' } })
    } catch (e: any) { ticketErr = errText(e) }
    const shown: Record<string, string> = {}
    if (ticketOut && ticketOut.filed === false && Array.isArray(ticketOut.findings)) {
      findings.forEach((f: any, i: number) => { shown[f.code] = ticketOut.findings[i] ?? '(no line)' })
    }
    out.push({ ...base, reader: 'TicketCenter/analysisRequest.ts fileAnalysisRequest (via parseIrEnvelope)',
      outcome: ticketErr ? 'THREW' : 'RETURNED', error: ticketErr,
      ticket_result: ticketOut ? { filed: ticketOut.filed, state: ticketOut.state ?? 'FILED', message: ticketOut.message ?? null,
        findings: ticketOut.findings ?? null, details: ticketOut.details ?? null } : null, shown_per_code: shown })
    let proxyOut: any = null
    let proxyErr: string | null = parseErr
    if (adapted) { try { proxyOut = pr.proxyableFindings(adapted.findings) } catch (e: any) { proxyErr = errText(e) } }
    out.push({ ...base, reader: 'InvestorReporting/tabs/analysis/prospect.ts proxyableFindings',
      outcome: proxyErr ? 'THREW' : 'RETURNED', error: proxyErr, proxy_offers: proxyOut ? proxyOut.map((p: any) => p.code) : null })
  }
}
writeFileSync(`${S}/run_hr/readers_deployed_shape.json`, JSON.stringify(out, null, 1) + '\n', 'utf8')
for (const r of out) console.log(r.commit, r.case, r.reader.slice(0, 20), r.outcome, r.error ?? '', JSON.stringify(r.ticket_result?.message ?? ''), JSON.stringify(r.shown_per_code ?? {}))
