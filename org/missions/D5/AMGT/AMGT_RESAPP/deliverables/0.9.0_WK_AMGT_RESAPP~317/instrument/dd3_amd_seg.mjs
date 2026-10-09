// dd-3 (round 80), pass 2: the AMD page's own "Revenue by segment" table as the DOM draws it (pass 1's selector
// [data-segment-breakdown] read only the filing panel below it). GET only; sections of dd3_walk.mjs reused in shape.
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'
export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, waitForLoaded } = ctx
  const dir = path.join(OUT, 'data', 'fwd1'); mkdirSync(dir, { recursive: true }); mkdirSync(path.join(OUT, 'shots'), { recursive: true })
  let lastScoped = null
  page.on('request', (req) => { const h = req.headers(); if (h.authorization && /\/api\/scoped\//.test(req.url())) lastScoped = h })
  setStep('AMD seg')
  await page.goto(opt.base + '/security-analysis/' + encodeURIComponent('AMD_US_Equity'), { waitUntil: 'domcontentloaded', timeout: 30000 })
  await settle(page, 2500); await waitForLoaded(page)
  await page.waitForSelector('[data-top-band],[data-input-provenance],[data-top-band-description]', { timeout: 20000 }).catch(() => {})
  await page.waitForTimeout(7000)
  const SKIP = /^(host|connection|content-length|accept-encoding|cookie|origin|referer|user-agent|sec-|:)/i
  const sent = Object.fromEntries(Object.entries(lastScoped || {}).filter(([k]) => !SKIP.test(k)))
  const api = await page.evaluate(async ({ headers }) => { const x = await fetch('/api/scoped/amgt/security/AMD_US_Equity/thesis', { method: 'GET', headers, cache: 'no-store' }); const j = await x.json(); return { status: x.status, st: j.segment_table } }, { headers: sent })
  writeFileSync(path.join(dir, 'AMD_segment_table_full_api.json'), JSON.stringify(api, null, 1))
  const dom = await page.evaluate(() => {
    const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 }
    const out = []
    for (const t of document.querySelectorAll('table')) {
      let h = t.previousElementSibling; let cap = (t.querySelector('caption') || {}).textContent || null
      let up = t; for (let i = 0; i < 4 && !cap; i++) { up = up.parentElement; if (!up) break; const hh = up.querySelector('h1,h2,h3,h4,h5,h6'); if (hh) cap = hh.textContent }
      const txt = (t.parentElement ? t.parentElement.innerText : '') || ''
      if (!/segment/i.test((cap || '') + txt.slice(0, 200))) continue
      out.push({ caption: (cap || '').trim(), visible: vis(t), attrs: [...t.attributes].map((a) => a.name + '=' + a.value.slice(0, 40)), parent_attrs: t.parentElement ? [...t.parentElement.attributes].map((a) => a.name + '=' + a.value.slice(0, 40)) : [], head: [...t.querySelectorAll('thead th, tr:first-child th')].map((x) => x.textContent.trim()), rows: [...t.querySelectorAll('tbody tr')].map((r) => [...r.children].map((c) => c.textContent.trim())) })
    }
    return { tables: out, all_tables: document.querySelectorAll('table').length, notes: [...document.querySelectorAll('p')].map((p) => p.innerText.trim()).filter((s) => /Figures are in|A column is named|Source: Bloomberg product segments|do not add up/.test(s)) }
  })
  writeFileSync(path.join(dir, 'AMD_revenue_by_segment_dom.json'), JSON.stringify(dom, null, 1))
  const loc = page.locator('table', { hasText: /Data Center/ }).first()
  if (await loc.count()) await loc.evaluate((el) => el.scrollIntoView({ block: 'center' }))
  await page.waitForTimeout(500)
  const file = 'shots/017-fwd1-AMD-revenue-by-segment-table.png'
  await page.screenshot({ path: path.join(OUT, file), fullPage: false })
  log('SEG', JSON.stringify(dom.tables.map((t) => [t.caption, t.head, t.rows.length])), file)
}
