// stage 4: FWD-1, the "About the company" disclosure opened on the 12 names that serve segments (a <details>; page state only)
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs'
import path from 'node:path'
export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, shot, waitForLoaded } = ctx
  const dir = path.join(OUT, 'data'); mkdirSync(dir, { recursive: true })
  const keys = process.env.AW8_KEYS.split(',')
  const res = []
  for (const key of keys) {
    setStep('about ' + key)
    const body = await (async () => { await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded' }); await settle(page, 1500)
      return page.evaluate(async (u) => { const t = localStorage.getItem('accessToken'); const r = await fetch(u, { headers: { Authorization: `Bearer ${t}` } }); return r.text() }, `/api/scoped/amgt/security/${encodeURIComponent(key)}/thesis`) })()
    const sb = JSON.parse(body).segment_breakdown
    await page.goto(opt.base + '/security-analysis/' + encodeURIComponent(key), { waitUntil: 'domcontentloaded', timeout: 30000 })
    await settle(page, 2500); await waitForLoaded(page)
    const sum = page.locator('summary', { hasText: /about the company/i }).first()
    const found = await sum.count().catch(() => 0)
    let opened = false
    if (found) opened = await sum.click({ timeout: 5000 }).then(() => true).catch(() => false)
    await page.waitForTimeout(1500)
    const info = await page.evaluate(() => {
      const d = [...document.querySelectorAll('details')].find((x) => /about the company/i.test((x.querySelector('summary') || {}).textContent || ''))
      return { open: d ? d.open : null, text: d ? d.innerText : '', pathname: location.pathname,
        tabs: [...document.querySelectorAll('button')].filter((e) => ['THESIS','EXEC MANAGEMENT','PEERS','MODEL','POSTURE'].includes((e.textContent || '').trim().toUpperCase())).map((e) => e.textContent.trim()) }
    })
    const low = info.text.toLowerCase()
    const labels = [...new Set(sb.rows.map((r) => r.segment))]
    const file = await shot(page, `fwd1-${key}-about-the-company-open`)
    const r = { key, summary_found: found, pressed: opened, details_open: info.open, about_chars: info.text.length, served_segment_rows: sb.rows.length,
      labels_in_about: labels.filter((l) => low.includes(l.toLowerCase())).length, sentences_in_about: sb.rows.filter((x) => low.includes(x.text.toLowerCase().slice(0, 50))).length,
      word_segment_in_about: /segment/i.test(info.text), pathname: info.pathname, tab_labels: info.tabs, file, about_excerpt: info.text.slice(0, 300) }
    res.push(r); log('ABOUT', key, JSON.stringify({ ...r, about_excerpt: undefined }))
    writeFileSync(path.join(dir, 'fwd1_about.json'), JSON.stringify(res, null, 1))
  }
}
