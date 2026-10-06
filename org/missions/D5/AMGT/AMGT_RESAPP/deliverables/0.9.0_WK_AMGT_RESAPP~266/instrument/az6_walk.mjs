// az-6 walk module: FWD-7 (/freshness first visit, first thing after sign-in), FWD-5 (Print button on BA, AMD, ASML_NA),
// FWD-18 + FWD-1 (BA thesis tab: driver chart passage, segment breakdown). GET only; the walker's network guard is unchanged.
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const TABS = ['THESIS', 'EXEC MANAGEMENT', 'PEERS', 'MODEL', 'POSTURE']

export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, shot, waitForLoaded, context } = ctx
  const dir = path.join(OUT, 'data')
  for (const d of ['print', 'fwd7', 'fwd18']) mkdirSync(path.join(dir, d), { recursive: true })
  const captures = []
  const rec = (o) => { captures.push(o); writeFileSync(path.join(dir, 'captures.json'), JSON.stringify(captures, null, 1)) }
  const control = () => page.evaluate((T) => ({
    pathname: location.pathname,
    tab_labels: [...document.querySelectorAll('button,[role=tab],a')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && T.includes((e.textContent || '').trim().toUpperCase()) }).map((e) => (e.textContent || '').trim()),
    h1: ((document.querySelector('h1') || {}).textContent || '').trim(),
  }), TABS).catch(() => ({ pathname: null, tab_labels: [] }))
  const capture = async (label, extra = {}) => {
    const file = await shot(page, label)
    const c = await control()
    rec({ label, file, at: new Date().toISOString(), ...c, ...extra })
    log('CAPTURE', label, file, JSON.stringify(c.pathname), c.tab_labels.length, 'tab labels')
    return file
  }
  const openName = async (key) => {
    await page.goto(opt.base + '/security-analysis/' + encodeURIComponent(key), { waitUntil: 'domcontentloaded', timeout: 30000 })
    await settle(page, 2500)
    return waitForLoaded(page)
  }
  const blocked = []
  await context.route((u) => !/^(localhost|127\.0\.0\.1)$/.test(u.hostname) && !/\.(cloudfront\.net|opalinvest\.com)$/.test(u.hostname), (route) => {
    const rq = route.request()
    if (rq.resourceType() === 'document') { blocked.push(rq.url()); return route.abort('blockedbyclient') }
    return route.fallback()
  })

  // ---------- FWD-7: /freshness FIRST visit, before any other page of this context reads freshness ----------
  const read = () => page.evaluate(() => {
    const trs = [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')]
    const lines = trs.map((tr) => ({ name: tr.children[0]?.textContent, last: tr.children[1]?.textContent, stale: tr.getAttribute('data-stale'), flags: [...tr.querySelectorAll('[data-stale-input]')].map((l) => l.textContent) }))
    return { summary: (document.querySelector('[data-slot="freshness-summary"]') || {}).textContent || null, rows: lines.length, stale_rows: lines.filter((l) => l.stale === 'true').length,
      first_five: lines.slice(0, 5), headers: [...document.querySelectorAll('[data-slot="freshness-table"] thead th')].map((t) => t.textContent),
      sort_buttons: [...document.querySelectorAll('[aria-label="Sort by"] button')].map((b) => ({ label: b.textContent, pressed: b.getAttribute('aria-pressed') })),
      body_text_head: (document.body.innerText || '').slice(0, 700),
      all: lines }
  })
  for (const pass of ['first', 'second']) {
    try {
      setStep('fwd7 ' + pass)
      const t0 = Date.now()
      await page.goto(opt.base + '/freshness', { waitUntil: 'domcontentloaded', timeout: 30000 })
      const tNav = Date.now() - t0
      const got = await page.locator('[data-slot="freshness-table"] tbody tr').first().waitFor({ timeout: 90000 }).then(() => true).catch(() => false)
      const waited = Date.now() - t0
      await settle(page, 1500)
      const r = await read()
      const reqs = await page.evaluate(() => performance.getEntriesByType('resource').filter((e) => /freshness/.test(e.name)).map((e) => ({ name: e.name.replace(/\?.*/, ''), start_ms: Math.round(e.startTime), duration_ms: Math.round(e.duration), transfer: e.transferSize, encoded: e.encodedBodySize, decoded: e.decodedBodySize })))
      const out = { pass, table_appeared: got, domcontentloaded_ms: tNav, first_row_ms_from_navigation: waited, freshness_requests: reqs, ...r }
      writeFileSync(path.join(dir, 'fwd7', `fwd7-${pass}.json`), JSON.stringify(out, null, 1))
      log('FWD7', pass, 'first row at', waited, 'ms;', r.rows, 'rows;', r.stale_rows, 'stale;', JSON.stringify(reqs))
      await capture(`fwd7-freshness-${pass}`, { table_appeared: got, first_row_ms_from_navigation: waited, rows: r.rows, stale_rows: r.stale_rows, summary: r.summary, first_five: r.first_five })
      if (pass === 'first') {
        const btns = page.locator('[aria-label="Sort by"] button')
        const nb = await btns.count()
        for (let i = 0; i < nb; i++) {
          const lab = ((await btns.nth(i).innerText()) || '').trim()
          await btns.nth(i).click({ timeout: 4000 }).catch(() => {})
          await page.waitForTimeout(600)
          const s = await read()
          await capture(`fwd7-freshness-sort-${lab}`, { sort: lab, summary: s.summary, first_five: s.first_five })
        }
      }
    } catch (e) { log('FWD7 ERROR', pass, String(e.message).split('\n')[0]); rec({ label: 'fwd7-error-' + pass, error: String(e.message).split('\n')[0] }) }
  }

  // ---------- FWD-18 + FWD-1: BA, AMD, ASML_NA on the Thesis tab ----------
  for (const key of ['BA_US_Equity', 'AMD_US_Equity', 'ASML_NA_Equity']) {
    const short = key.split('_')[0]
    try {
      setStep('fwd18 ' + short)
      await openName(key)
      await page.waitForTimeout(2500)
      const dom = await page.evaluate(() => {
        const dc = document.querySelector('[data-driver-chart]')
        const sb = document.querySelector('[data-segment-breakdown]')
        return {
          driver_chart: dc ? { state: dc.getAttribute('data-driver-chart'), source: dc.getAttribute('data-driver-chart-source'), caption: (dc.querySelector('[data-driver-chart-caption]') || {}).textContent || null,
            passage_links: [...dc.querySelectorAll('[data-driver-chart-passage-link]')].map((b) => b.textContent), points_line: (dc.querySelector('[data-driver-chart-points]') || {}).textContent || null,
            text: dc.innerText.slice(0, 1500) } : null,
          segments: sb ? { state: sb.getAttribute('data-segment-state'), header: (sb.querySelector('h4') || {}).textContent || null,
            headings_h4: [...sb.querySelectorAll('h4,h5,h3')].map((h) => h.textContent),
            rows: [...sb.querySelectorAll('[data-segment-row]')].map((li) => ({ n: li.getAttribute('data-segment-row'), heading: (li.querySelector('span') || {}).textContent || null, text: (li.querySelectorAll('p')[1] || {}).textContent || null })),
            source_line: [...sb.querySelectorAll('p')].map((p) => p.textContent).slice(-1)[0] || null, text: sb.innerText.slice(0, 2500) } : null,
          about_present: !!([...document.querySelectorAll('summary')].find((s) => /About the company/i.test(s.textContent || ''))),
        }
      })
      writeFileSync(path.join(dir, 'fwd18', short + '_dom.json'), JSON.stringify(dom, null, 1))
      log('FWD18 DOM', short, JSON.stringify({ driver: dom.driver_chart && dom.driver_chart.state, links: dom.driver_chart && dom.driver_chart.passage_links.length, seg: dom.segments && dom.segments.state, seg_rows: dom.segments && dom.segments.rows.length }))
      const dcLoc = page.locator('[data-driver-chart]').first()
      if (await dcLoc.count()) await dcLoc.scrollIntoViewIfNeeded().catch(() => {})
      await capture(`fwd18-${short}-driver-chart`, { dom_driver: dom.driver_chart })
      const link = page.locator('[data-driver-chart-passage-link]').first()
      let clicked = null
      if (await link.count()) {
        const label = await link.innerText()
        await link.scrollIntoViewIfNeeded().catch(() => {})
        await link.click({ timeout: 5000 }).catch(() => {})
        await page.waitForTimeout(800)
        clicked = await page.evaluate(() => {
          const bq = document.querySelector('[data-driver-chart-passage-source]')
          return bq ? { source_attr: bq.getAttribute('data-driver-chart-passage-source'), text: bq.innerText.slice(0, 2000), html_head: bq.innerHTML.slice(0, 1500), tables: bq.querySelectorAll('table').length, cite: (bq.querySelector('[data-driver-chart-passage-cite]') || {}).textContent || null } : null
        })
        clicked = { link_label: label, ...clicked }
        await capture(`fwd18-${short}-passage-open`, { clicked })
      }
      writeFileSync(path.join(dir, 'fwd18', short + '_click.json'), JSON.stringify(clicked, null, 1))
      log('FWD18 CLICK', short, JSON.stringify(clicked).slice(0, 500))
      const sbLoc = page.locator('[data-segment-breakdown]').first()
      if (await sbLoc.count()) await sbLoc.scrollIntoViewIfNeeded().catch(() => {})
      await capture(`fwd1-${short}-segments`, { dom_segments: dom.segments && { state: dom.segments.state, rows: dom.segments.rows.length } })
      const sum = page.locator('[data-segment-cite] summary').first()
      if (await sum.count()) {
        await sum.click({ timeout: 4000 }).catch(() => {})
        await page.waitForTimeout(500)
        await capture(`fwd1-${short}-segment-source-open`, {})
      }
      // business description leg: About the company
      const about = page.locator('summary', { hasText: /About the company/i }).first()
      if (await about.count()) {
        await about.scrollIntoViewIfNeeded().catch(() => {})
        await about.click({ timeout: 4000 }).catch(() => {})
        await page.waitForTimeout(600)
        const at = await page.evaluate(() => { const d = [...document.querySelectorAll('details')].find((x) => /About the company/i.test((x.querySelector('summary') || {}).textContent || '')); return d ? { open: d.open, text: d.innerText.slice(0, 1500) } : null })
        writeFileSync(path.join(dir, 'fwd18', short + '_about.json'), JSON.stringify(at, null, 1))
        await capture(`fwd1-${short}-about-open`, { about: at && { open: at.open, len: at.text.length } })
      }
      // model numbers leg: the Model tab
      const modelTab = page.getByRole('button', { name: /^model$/i }).first()
      const mt = (await modelTab.count()) ? modelTab : page.getByRole('tab', { name: /^model$/i }).first()
      if (await mt.count()) {
        await mt.scrollIntoViewIfNeeded().catch(() => {})
        await mt.click({ timeout: 4000 }).catch(() => {})
        await page.waitForTimeout(3500)
        const mtext = await page.evaluate(() => document.body.innerText.slice(0, 3500))
        writeFileSync(path.join(dir, 'fwd18', short + '_model_text.txt'), mtext)
        await capture(`fwd1-${short}-model-tab`, {})
      }
    } catch (e) { log('FWD18 ERROR', short, String(e.message).split('\n')[0]); rec({ label: 'fwd18-error-' + short, error: String(e.message).split('\n')[0] }) }
  }
  writeFileSync(path.join(dir, 'blocked_third_party.json'), JSON.stringify(blocked, null, 1))
  log('AZ6 OUT', OUT)
}
