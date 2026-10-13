// r19 AR-y-202: the portal's own reader functions, run at the PROD and DEV commits (archives under .scratch/r19/prod, .scratch/r19/dev).
// Inputs: the door answer bodies the offline harness returned (run_hr/answer_bodies.json). Writes raw results only.
import { readFileSync, writeFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'

const S = 'C:/dev/wk-irpt-anlreq-57/.scratch/r19'
const COMMITS: Record<string, { root: string; sha: string }> = {
  PROD: { root: `${S}/prod`, sha: '37aa1247ee4ba487e5610dc5b78d65ae28468a99' },
  DEV: { root: `${S}/dev`, sha: '64980b4d3a1e11d8407b6a263ddcd5447dafaef2' },
}
const bodies: Record<string, { res: { ok: boolean; answer?: any; refused?: string; error?: string }; answer: any }> =
  JSON.parse(readFileSync(`${S}/run_hr/answer_bodies.json`, 'utf8'))
const SHEETS = ['two_sheet_workbook', 'total_row_sheet', 'two_value_account_sheet', 'one_account_sheet',
  'repair_header_two_values', 'repair_header_one_value', 'attribute_header_one_account', 'brokerage_two_account',
  'header_repeated_csv']
const ANSWERS = { advisor: 'Adv', firm: 'FIRM-1', household: 'HH', report_type: 'Overview', comparison_model: '' }

function errText(e: any): string {
  return `${e?.name ?? 'Error'}: ${String(e?.message ?? e).slice(0, 200)}`
}

function codesOf(body: any): { codes: string[]; where: string[] } {
  const codes: string[] = []
  const where: string[] = []
  for (const f of body?.findings ?? []) { codes.push(f.code); where.push('findings') }
  for (const f of body?.portfolio?.findings ?? []) { codes.push(f.code); where.push('portfolio.findings') }
  return { codes, where }
}

const out: any[] = []
for (const commit of Object.keys(COMMITS)) {
  const { root, sha } = COMMITS[commit]
  const env = await import(pathToFileURL(`${root}/src/pages/InvestorReporting/contracts/envelope.ts`).href)
  const tc = await import(pathToFileURL(`${root}/src/pages/TicketCenter/analysisRequest.ts`).href)
  const pr = await import(pathToFileURL(`${root}/src/pages/InvestorReporting/tabs/analysis/prospect.ts`).href)
  for (const sheet of SHEETS) {
    for (const arm of ['BEFORE', 'AFTER']) {
      const key = `${sheet}|${arm === 'BEFORE' ? 'pinned' : 'moved'}`
      const entry = bodies[key]
      const body = entry?.answer
      const { codes, where } = codesOf(body)
      const base = { case: sheet, arm, commit, commit_sha: sha, answer_state: body?.state ?? null,
        codes: [...new Set(codes)], codes_location: [...new Set(where)], body_keys: body ? Object.keys(body).sort() : [] }
      // reader 1: the typed client's parser (envelope.ts parseIrEnvelope -> IR_DATA_ADAPTER['analysis-input-upload'] = adaptAnalysisUpload)
      let adapted: any = null
      let parseErr: string | null = null
      try {
        const parsed = env.parseIrEnvelope('analysis-input-upload', {
          contract_version: env.IR_CONTRACT_VERSION, operation: 'analysis-input-upload', firm_id: 'FIRM-1', data: body, unprojected_grant: { count: 0, denominator: 0, kinds: {} } })
        adapted = parsed.data
      } catch (e: any) { parseErr = errText(e) }
      out.push({ ...base, reader: 'contracts/envelope.ts parseIrEnvelope (analysis-input-upload)',
        outcome: parseErr ? 'THREW' : 'RETURNED', error: parseErr,
        adapted_state: adapted?.state ?? null })
      // reader 2: the ticket path (TicketCenter/analysisRequest.ts fileAnalysisRequest) fed through the same parser
      const ir = { uploadAnalysisInput: async () => env.parseIrEnvelope('analysis-input-upload', {
        contract_version: env.IR_CONTRACT_VERSION, operation: 'analysis-input-upload', firm_id: 'FIRM-1', data: body, unprojected_grant: { count: 0, denominator: 0, kinds: {} } }).data }
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
        const findings: any[] = body?.findings ?? []
        findings.forEach((f, i) => { shown[f.code] = ticketOut.findings[i] ?? '(no line)' })
      }
      out.push({ ...base, reader: 'TicketCenter/analysisRequest.ts fileAnalysisRequest (via parseIrEnvelope)',
        outcome: ticketErr ? 'THREW' : 'RETURNED', error: ticketErr,
        ticket_result: ticketOut ? { filed: ticketOut.filed, state: ticketOut.state ?? 'FILED', message: ticketOut.message ?? null,
          findings: ticketOut.findings ?? null, details: ticketOut.details ?? null } : null,
        shown_per_code: shown })
      // reader 3: the Investor Reporting composer's proxy reader (prospect.ts proxyableFindings) over the adapted findings
      let proxyOut: any = null
      let proxyErr: string | null = parseErr
      if (adapted) {
        try { proxyOut = pr.proxyableFindings(adapted.findings) } catch (e: any) { proxyErr = errText(e) }
      }
      out.push({ ...base, reader: 'InvestorReporting/tabs/analysis/prospect.ts proxyableFindings',
        outcome: proxyErr ? 'THREW' : 'RETURNED', error: proxyErr,
        proxy_offers: proxyOut ? proxyOut.map((p: any) => p.code) : null })
    }
  }
}
writeFileSync(`${S}/run_hr/readers_raw.json`, JSON.stringify(out, null, 1) + '\n', 'utf8')
console.log('rows', out.length)
for (const r of out) console.log(r.commit, r.case, r.arm, r.reader.slice(0, 22), r.outcome, r.error ?? '', JSON.stringify(r.ticket_result?.message ?? r.proxy_offers ?? ''))
