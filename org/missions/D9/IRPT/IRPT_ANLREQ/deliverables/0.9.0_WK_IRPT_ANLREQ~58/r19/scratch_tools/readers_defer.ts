// r19 AR-y-203: the _defer first answer (built by build_defer_bodies.py from the REAL moved or pinned intake functions)
// passed through the portal's own readers at the PROD and DEV commits. Reads only; writes the raw result file.
import { readFileSync, writeFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'

const S = 'C:/dev/wk-irpt-anlreq-58/.scratch/r19'
const COMMITS: Record<string, { root: string; sha: string }> = {
  PROD: { root: `${S}/portal_prod`, sha: '37aa1247ee4ba487e5610dc5b78d65ae28468a99' },
  DEV: { root: `${S}/portal_dev`, sha: '64980b4d3a1e11d8407b6a263ddcd5447dafaef2' },
}
const ANSWERS = { advisor: 'Adv', firm: 'FIRM-1', household: 'HH', report_type: 'Overview', comparison_model: '' }
const ARM_SOURCE: Record<string, string> = {
  AFTER: 'moved uploads.py and template_reader.py at 069b8f797e (archived intake folder)',
  BEFORE: 'pinned uploads.py at f09b802cdc and template_reader.py at 3f29017cfc (intake folder staged at the map pins)',
}

function errText(e: any): string {
  return `${e?.name ?? 'Error'}: ${String(e?.message ?? e).slice(0, 200)}`
}

const records: any[] = [
  ...JSON.parse(readFileSync(`${S}/bodies_AFTER.json`, 'utf8')),
  ...JSON.parse(readFileSync(`${S}/bodies_BEFORE.json`, 'utf8')),
].filter((r: any) => r.body)

const out: any[] = []
for (const commit of Object.keys(COMMITS)) {
  const { root, sha } = COMMITS[commit]
  const env = await import(pathToFileURL(`${root}/src/pages/InvestorReporting/contracts/envelope.ts`).href)
  const tc = await import(pathToFileURL(`${root}/src/pages/TicketCenter/analysisRequest.ts`).href)
  const pr = await import(pathToFileURL(`${root}/src/pages/InvestorReporting/tabs/analysis/prospect.ts`).href)
  for (const rec of records) {
    const body = rec.body
    const findings: any[] = body.findings ?? []
    const codes = [...new Set(findings.map((f: any) => f.code))]
    const base = {
      case: rec.case, arm: rec.arm, commit, commit_sha: sha,
      body_source: `_defer first answer built from ${ARM_SOURCE[rec.arm]} by the real _with_correction_words, MAX_STORED_FINDINGS and NEEDS_CORRECTION (build_defer_bodies.py); not a door run`,
      body_keys: Object.keys(body).sort(), reason: body.reason, state: body.state, findings_total: body.findings_total,
      codes, codes_location: ['findings'], reader_version: rec.reader_version,
    }
    const grant = { count: 0, denominator: 0, kinds: {} }
    const parse = () => env.parseIrEnvelope('analysis-input-upload', {
      contract_version: env.IR_CONTRACT_VERSION, operation: 'analysis-input-upload', firm_id: 'FIRM-1', data: body, unprojected_grant: grant })
    // reader 1: the typed client's parser
    let adapted: any = null
    let parseErr: string | null = null
    try { adapted = parse().data } catch (e: any) { parseErr = errText(e) }
    out.push({ ...base, reader: 'contracts/envelope.ts parseIrEnvelope (analysis-input-upload)',
      outcome: parseErr ? 'THREW' : 'RETURNED', error: parseErr, adapted_state: adapted?.state ?? null,
      adapted_reason: adapted?.reason ?? null, method: 'RUN' })
    // reader 2: the ticket path, fed through the same parser
    const ir = { uploadAnalysisInput: async () => parse().data }
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
      outcome: ticketErr ? 'THREW' : 'RETURNED', error: ticketErr, method: 'RUN',
      ticket_result: ticketOut ? { filed: ticketOut.filed, state: ticketOut.state ?? 'FILED', message: ticketOut.message ?? null,
        findings: ticketOut.findings ?? null, details: ticketOut.details ?? null } : null,
      shown_per_code: shown })
    // reader 3: the composer's proxy reader over the adapted findings
    let proxyOut: any = null
    let proxyErr: string | null = parseErr
    if (adapted) {
      try { proxyOut = pr.proxyableFindings(adapted.findings) } catch (e: any) { proxyErr = errText(e) }
    }
    out.push({ ...base, reader: 'InvestorReporting/tabs/analysis/prospect.ts proxyableFindings',
      outcome: proxyErr ? 'THREW' : 'RETURNED', error: proxyErr, method: 'RUN',
      proxy_offers: proxyOut ? proxyOut.map((p: any) => p.code) : null })
  }
}
writeFileSync(`${S}/readers_defer_raw.json`, JSON.stringify(out, null, 1) + '\n', 'utf8')
console.log('rows', out.length)
for (const r of out) {
  console.log(r.commit, r.arm, r.case, r.reader.slice(0, 24), r.outcome, r.error ?? '',
    JSON.stringify(r.ticket_result?.message ?? r.proxy_offers ?? r.adapted_state ?? ''))
}
