/**
 * IRPT_DASHBD DB-b-180 (worker 0.9.0_WK_IRPT_DASHBD~146) -- renders one filled report through the Performance tab
 * component and the export document component into local files. Nothing here is served, pushed or uploaded.
 *
 * Usage (run with bun; the harness finds the portal source from its own location, in this worktree):
 *   bun <absolute path to this file> <absolute path to the report JSON> [output folder]
 *
 * The output folder defaults to the PRIVATE folder C:/dev/_irpt_private_evidence_20261009/fwd21_sample (never a repo).
 * Writes FWD21_TAB_49F_SAMPLE.html, FWD21_EXPORT_49F_SAMPLE.html and FWD21_EXPORT_49F_SAMPLE.pdf (headless Edge),
 * and prints ONE JSON object of paths, byte counts, hashes and counts. It prints no figure, name or account id.
 *
 * The report JSON is handed to the components AS IS. The harness adds no adapter: if a component cannot read the
 * report, the error propagates and the harness exits 1 with the component's own message (the issuer decides).
 *
 * Edits made by the harness to its OWN output only: the logo file is inlined as a data URI (so the HTML does not
 * reach the portal's assets), the print stylesheet is inlined, and the tab page gets a 1000 px reading column.
 * The component sources are read, never edited.
 */

import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const DEFAULT_OUT = 'C:/dev/_irpt_private_evidence_20261009/fwd21_sample'
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
/** The neutral firm word for the page head: the sample carries no firm name, so none is printed. */
const FIRM_WORD = 'Sample Firm'
const ABSENT_RE = /Not available yet/g

// This file sits at <root>/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/<serial>/ ; seven levels up is the repo root.
const PORTAL = path.resolve(import.meta.dir, '../../../../../../../portal')
const SRC = path.join(PORTAL, 'src')
const REPORT_DIR = path.join(SRC, 'pages/InvestorReporting')

function sha256(bytes: Uint8Array): string {
  return createHash('sha256').update(bytes).digest('hex')
}

function count(text: string, re: RegExp): number {
  return (text.match(re) ?? []).length
}

async function main(): Promise<void> {
  const sampleArg = process.argv[2] ?? ''
  const outDir = process.argv[3] ?? DEFAULT_OUT
  if (!path.isAbsolute(sampleArg)) {
    console.error('ERROR: pass the absolute path of the report JSON as the first argument')
    process.exit(2)
  }
  const sampleBytes = readFileSync(sampleArg)
  const report = JSON.parse(sampleBytes.toString('utf8'))
  mkdirSync(outDir, { recursive: true })

  // React is loaded from the portal's install (the component files resolve it there too).
  const req = createRequire(path.join(PORTAL, 'package.json'))
  const reactNs: any = await import(pathToFileURL(req.resolve('react')).href)
  const serverNs: any = await import(pathToFileURL(req.resolve('react-dom/server')).href)
  const React: any = reactNs.createElement ? reactNs : reactNs.default
  const renderToStaticMarkup: (el: unknown) => string = serverNs.renderToStaticMarkup ?? serverNs.default.renderToStaticMarkup

  const tabNs: any = await import(pathToFileURL(path.join(REPORT_DIR, 'dashboard/report/PerformanceReport.tsx')).href)
  const docNs: any = await import(pathToFileURL(path.join(REPORT_DIR, 'render/performance/report/PerformanceReportDocument.tsx')).href)
  const brand: any = await import(pathToFileURL(path.join(REPORT_DIR, 'render/brand.ts')).href)

  // The two renders. A component error is NOT caught: it is the measurement.
  const tabMarkup: string = renderToStaticMarkup(React.createElement(tabNs.PerformanceReport, { report, firmWord: FIRM_WORD }))
  const exportMarkup: string = renderToStaticMarkup(React.createElement(docNs.PerformanceReportDocument, { report, firmWord: FIRM_WORD }))

  const logoPath = fileURLToPath(brand.LOGO_URL)
  const logoData = 'data:image/svg+xml;base64,' + readFileSync(logoPath).toString('base64')
  const inlineLogo = (m: string): string => m.split(brand.LOGO_URL).join(logoData)
  const printCss = readFileSync(path.join(REPORT_DIR, 'render/print.css'), 'utf8')

  const tabHtml = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>Performance Report sample (local)</title><style>'
    + 'body{margin:0;padding:16px;background:#ffffff;font-family:Arial,sans-serif;color:#222222}'
    + '.tab-column{max-width:1000px;margin:0 auto}</style></head><body><div class="tab-column">'
    + inlineLogo(tabMarkup) + '</div></body></html>\n'

  const exportHtml = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>Performance Report sample (local, print)</title><style>'
    + printCss + '\nhtml,body{-webkit-print-color-adjust:exact;print-color-adjust:exact;margin:0;background:#ffffff}</style></head><body>'
    + inlineLogo(exportMarkup) + '</body></html>\n'

  const tabPath = path.join(outDir, 'FWD21_TAB_49F_SAMPLE.html')
  const exportHtmlPath = path.join(outDir, 'FWD21_EXPORT_49F_SAMPLE.html')
  const pdfPath = path.join(outDir, 'FWD21_EXPORT_49F_SAMPLE.pdf')
  writeFileSync(tabPath, tabHtml, 'utf8')
  writeFileSync(exportHtmlPath, exportHtml, 'utf8')

  // The PDF is the export HTML printed by headless Edge, run at its own path (no shell; argument vector only).
  const proc = Bun.spawn([EDGE, '--headless', '--disable-gpu', '--no-pdf-header-footer', '--print-to-pdf=' + pdfPath,
    pathToFileURL(exportHtmlPath).href], { stdout: 'ignore', stderr: 'ignore' })
  const edgeRc = await proc.exited

  const pdfBytes = readFileSync(pdfPath)
  const pdfPages = count(pdfBytes.toString('latin1'), /\/Type\s*\/Page[^s]/g)

  const ids = (html: string) => new Set([...html.matchAll(/data-member="([^"]+)"/g)].map((m) => m[1]))
  // A table cell or dd carries its words directly; a chart (figure) carries them in the one p it holds when absent.
  const absentCells = (html: string) => [
    ...[...html.matchAll(/<(?:td|dd)\b[^>]*data-absent="true"[^>]*>([^<]*)</g)].map((m) => m[1] ?? ''),
    ...[...html.matchAll(/<figure\b[^>]*data-absent="true"[^>]*>([\s\S]*?)<\/figure>/g)].map((m) => /<p[^>]*>([^<]*)</.exec(m[1] ?? '')?.[1] ?? ''),
  ]
  const tabAbsent = absentCells(tabMarkup)
  const exportAbsent = absentCells(exportMarkup)
  const sampleAbsent = Object.values(report.values ?? {}).filter((v: any) => v && typeof v === 'object' && 'absent' in v).length
  const info = (bytes: Buffer, p: string) => ({ path: p, bytes: bytes.length, sha256: sha256(bytes) })

  const out = {
    sample_sha256: sha256(sampleBytes),
    harness_sha256: sha256(readFileSync(import.meta.path)),
    outputs: {
      tab_html: info(Buffer.from(tabHtml, 'utf8'), tabPath),
      export_html: info(Buffer.from(exportHtml, 'utf8'), exportHtmlPath),
      export_pdf: info(pdfBytes, pdfPath),
    },
    edge_rc: edgeRc,
    export_pdf_pages: pdfPages,
    tab_member_ids: ids(tabMarkup).size,
    export_member_ids: ids(exportMarkup).size,
    tab_not_available_words: count(tabMarkup, ABSENT_RE),
    export_not_available_words: count(exportMarkup, ABSENT_RE),
    tab_absent_cells_without_words: tabAbsent.filter((t) => !t.startsWith('Not available yet') && t !== '-').length,
    export_absent_cells_without_words: exportAbsent.filter((t) => !t.startsWith('Not available yet') && t !== '-').length,
    fee_basis_label_tab: count(tabHtml, /before advisory fees/gi),
    fee_basis_label_export: count(exportHtml, /before advisory fees/gi),
    external_refs: count(tabHtml + exportHtml, /(src|href)="https?:|url\(https?:/g),
    absent_top_level_in_sample: sampleAbsent,
  }
  console.log(JSON.stringify(out, null, 2))
  if (edgeRc !== 0 || pdfBytes.subarray(0, 5).toString('latin1') !== '%PDF-') {
    console.error('ERROR: headless Edge did not write a PDF (rc ' + edgeRc + ')')
    process.exit(1)
  }
}

main().catch((e) => {
  // The component's own message, with no sample value in it (the error text names keys and members, not figures).
  console.error('HARNESS-ERROR: ' + (e instanceof Error ? e.name + ': ' + e.message : String(e)))
  process.exit(1)
})
