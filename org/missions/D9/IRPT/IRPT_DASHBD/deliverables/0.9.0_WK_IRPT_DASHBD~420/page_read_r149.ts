// IRPT_DASHBD round 149, TO DB-c-29, worker 0.9.0_WK_IRPT_DASHBD~420 -- the labelled TEST READ (not a serve, not a production run).
//
// Adapted from the round-148 page harness (page_read_r148.ts, worker 0.9.0_WK_IRPT_DASHBD~419) to the 49 Financial documents.
//
// The page's own reader (readSeries) and view (performanceView) over the downloaded series documents. Read only; counts only.
// Run from the portal worktree so the portal's path aliases resolve:
//   cd <worktree>/portal && bun run <this file> <temporary_folder_outside_every_repository>
// Prints ONE JSON line of counts. It prints no key, no account identifier, no series value and no sentence text.

import { readdirSync, readFileSync } from 'node:fs'
import { join } from 'node:path'
import { gunzipSync } from 'node:zlib'
import { performanceView, type WindowSelection } from '../../../../../../../portal/src/pages/InvestorReporting/dashboard/DashboardPerformance'
import { readSeries } from '../../../../../../../portal/src/pages/InvestorReporting/dashboard/seriesContract'

const SENTENCE_MARK = 'not reported by the source'
const LEADING_COUNT = /^(\d+) trading days? not reported/
const RETURNS_FROM = /^Returns from /
const EXCLUDED_NOTE = 'no measurable return'
const DAY_QUALITY_NOTE = /^\d+ days?: /

const dir = process.argv[2]
if (!dir) {
  console.log(JSON.stringify({ error: 'no folder argument' }))
  process.exit(2)
}

const counts = {
  docs_read: 0,
  page_parse_failed: 0,
  read_ok: 0,
  read_refused: 0,
  performance_view_threw: 0,
  accounts_printing_unreported_sentence: 0,
  sentences_total: 0,
  sentence_n_mismatch: 0,
  income_coerced_to_zero: 0,
  accounts_printing_returns_from: 0,
  accounts_printing_excluded_days_note: 0,
  accounts_printing_day_quality_note: 0,
}

const files = readdirSync(dir).filter((name) => name.endsWith('.series.json.gz')).sort()

for (const name of files) {
  counts.docs_read += 1
  const text = gunzipSync(readFileSync(join(dir, name))).toString('utf8')
  let raw: any
  let rawCopy: any
  try {
    raw = JSON.parse(text)
    rawCopy = JSON.parse(text)
  } catch {
    counts.page_parse_failed += 1
    continue
  }

  const read = readSeries(raw)
  if (!read.ok) {
    counts.read_refused += 1
    continue
  }
  counts.read_ok += 1
  const doc = read.document as any

  // A null on the raw document must not come back as a 0 from the page's reader.
  const rawIncome: unknown[] = Array.isArray(rawCopy.income) ? rawCopy.income : []
  const docIncome: unknown[] = Array.isArray(doc.income) ? doc.income : []
  if (rawIncome.some((value, i) => value === null && docIncome[i] === 0)) counts.income_coerced_to_zero += 1

  // The window the page is asked for: the whole history, from the first data day to the as-of day.
  const selection: WindowSelection = { kind: 'custom', start: doc.first_data_date, end: doc.as_of }
  let allNotes: string[]
  try {
    allNotes = performanceView(read.document, selection).notes
  } catch {
    counts.performance_view_threw += 1
    continue
  }

  const notes = allNotes.filter((note) => note.includes(SENTENCE_MARK))
  if (notes.length > 0) counts.accounts_printing_unreported_sentence += 1
  counts.sentences_total += notes.length

  if (allNotes.some((note) => RETURNS_FROM.test(note))) counts.accounts_printing_returns_from += 1
  if (allNotes.some((note) => note.includes(EXCLUDED_NOTE))) counts.accounts_printing_excluded_days_note += 1
  if (allNotes.some((note) => DAY_QUALITY_NOTE.test(note))) counts.accounts_printing_day_quality_note += 1

  const listed: unknown[] = doc.unreported_trading_days ?? []
  const listedLength = listed.length
  let mismatch = false
  if (listedLength === 0) {
    // An empty or missing list must print no sentence.
    if (notes.length > 0) mismatch = true
  } else {
    // A non-empty list must print one, and each printed count must equal the list's length.
    if (notes.length === 0) mismatch = true
    for (const note of notes) {
      const match = LEADING_COUNT.exec(note)
      if (!match || Number(match[1]) !== listedLength) mismatch = true
    }
  }
  if (mismatch) counts.sentence_n_mismatch += 1
}

console.log(JSON.stringify(counts))
