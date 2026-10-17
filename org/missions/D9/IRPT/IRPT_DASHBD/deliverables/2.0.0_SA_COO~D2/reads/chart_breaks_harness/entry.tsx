import { createRoot } from 'react-dom/client'
import { DashboardPerformance } from '../src/pages/InvestorReporting/dashboard/DashboardPerformance'
import { readSeries } from '../src/pages/InvestorReporting/dashboard/seriesContract'
import fixture from '../src/pages/InvestorReporting/__tests__/irpt-dashbd/fixtures/series-unreported-days.json'

const raw = JSON.parse(JSON.stringify(fixture)) as Record<string, any>
for (const day of ['2026-07-17', '2026-07-29']) {
  const i = raw.date.indexOf(day)
  raw.total_return_daily[i] = null
  raw.day_quality[i] = 'NOT_MEASURABLE'
}
const read = readSeries(raw)
const mode = new URLSearchParams(location.search).get('mode')
const sel = mode === 'late' ? { kind: 'custom' as const, start: '2026-07-20', end: '2026-08-14' } : { kind: 'custom' as const, start: '2026-07-10', end: '2026-08-14' }
createRoot(document.getElementById('root')!).render(
  <div style={{ width: 900, padding: 16, fontFamily: 'sans-serif', fontSize: 14 }}>
    <DashboardPerformance read={read} initialSelection={sel} />
  </div>,
)
