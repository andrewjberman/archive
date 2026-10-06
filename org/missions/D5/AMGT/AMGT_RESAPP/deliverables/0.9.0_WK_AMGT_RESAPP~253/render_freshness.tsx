// Renders the /freshness page's FreshnessView over the captured deployed body and prints its text.
// Run from portal/: bun run ../org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~253/render_freshness.tsx
import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
// react and react-dom are taken from THIS worktree's portal/node_modules, the copy the component itself resolves (two copies break hooks)
const portalRequire = createRequire(fileURLToPath(new URL('../../../../../../../portal/package.json', import.meta.url)))
const { createElement } = portalRequire('react')
const { renderToStaticMarkup } = portalRequire('react-dom/server')
const { FreshnessView } = await import('../../../../../../../portal/src/pages/Freshness/Freshness')

const dir = new URL('.', import.meta.url)
const body = JSON.parse(readFileSync(new URL('freshness_body.json', dir), 'utf-8'))
const today = String(body.generated_at).slice(0, 10)
const text = (html: string) => html.replace(/<\/(tr|p|li|div)>/g, '\n').replace(/<\/(td|th|button)>/g, ' | ').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/ \| \n/g, '\n')
const out: string[] = []
out.push(`captured body: ${body.rows.length} rows served, generated_at ${body.generated_at}; page day ${today}`)
for (const sort of ['stalest', 'freshest', 'name'] as const) {
  const html = renderToStaticMarkup(createElement(FreshnessView, { rows: body.rows, today, initialSort: sort }))
  const rows = [...html.matchAll(/<tr data-stale="(true|false)"[^>]*>(.*?)<\/tr>/g)]
  const stale = rows.filter((m) => m[1] === 'true').length
  out.push('', `=== sort: ${sort} ===`, `rows shown ${rows.length}; rows flagged stale ${stale}`)
  out.push(...text(html.slice(0, html.indexOf('<table'))).split('\n').filter(Boolean))
  out.push('first five rows:')
  rows.slice(0, 5).forEach((m, i) => out.push(`${i + 1}. ${text(m[0]).split('\n').filter(Boolean).join(' / ')}`))
  if (sort === 'stalest') {
    out.push('', '--- full page text (stalest first) ---')
    out.push(...text(html).split('\n').filter(Boolean))
  }
}
console.log(out.join('\n'))
