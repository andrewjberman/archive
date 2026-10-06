// ax-6 walk module: FWD-4 (feed link out, BA), FWD-5 (Print on BA, AMD, ASML_NA), FWD-7 (/freshness first paint).
// GET only; the walker's network guard is unchanged. Third-party hosts are aborted at the browser so no external page loads.
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const TABS = ['THESIS', 'EXEC MANAGEMENT', 'PEERS', 'MODEL', 'POSTURE']
const safe = (k) => encodeURIComponent(k).replace(/\*/g, '%2A')

export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, shot, waitForLoaded, context } = ctx
  const dir = path.join(OUT, 'data')
  for (const d of ['print', 'fwd4', 'fwd7']) mkdirSync(path.join(dir, d), { recursive: true })
  const captures = []
  const rec = (o) => { captures.push(o); writeFileSync(path.join(dir, 'captures.json'), JSON.stringify(captures, null, 1)) }
  const get = (url) => page.evaluate(async (u) => {
    const t = localStorage.getItem('accessToken'); const t0 = Date.now()
    try { const r = await fetch(u, { headers: t ? { Authorization: `Bearer ${t}` } : {} }); return { status: r.status, ms: Date.now() - t0, body: await r.text() } }
    catch (e) { return { status: 'fetch failed ' + String(e).slice(0, 80), ms: Date.now() - t0, body: null } }
  }, url)
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
  // no third-party page ever loads: every non-localhost request is aborted in the browser context
  const blocked = []
  await context.route((u) => !/^(localhost|127\.0\.0\.1)$/.test(u.hostname) && !/\.(cloudfront\.net|opalinvest\.com)$/.test(u.hostname), (route) => {
    const rq = route.request()
    if (rq.resourceType() === 'document') { blocked.push(rq.url()); return route.abort('blockedbyclient') }
    return route.fallback()
  })

  // ---------- keys from the live freshness answer ----------
  setStep('ax6 keys')
  await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await settle(page, 3000)
  const f = await get('/api/scoped/amgt/freshness')
  log('FRESHNESS', f.status, f.ms, 'ms', (f.body || '').length, 'bytes')
  writeFileSync(path.join(dir, 'freshness.json'), f.body || '')
  const frows = JSON.parse(f.body).rows
  const covered = frows.filter((r) => r.covered && r.security_key)
  const pick = (re) => covered.filter((r) => re.test(r.security_key)).map((r) => r.security_key)
  const keyOf = { BA: pick(/^BA_US_Equity$/)[0], AMD: pick(/^AMD_US_Equity$/)[0], ASML: pick(/^ASML_NA_Equity$/)[0] }
  log('KEYS', JSON.stringify(keyOf), 'covered', covered.length, 'of', frows.length)
  writeFileSync(path.join(dir, 'keys.json'), JSON.stringify({ keyOf, covered: covered.length, rows: frows.length, amd_like: pick(/AMD/i) }, null, 1))

  // ---------- FWD-4: BA's feed, one item's link followed out to its target URL ----------
  try {
    setStep('fwd4 BA')
    const key = keyOf.BA || 'BA_US_Equity'
    const ov = await get(`/api/scoped/amgt/security/${encodeURIComponent(key)}/overlay`)
    let feed = null
    try { feed = JSON.parse(ov.body).feed } catch { /* not json */ }
    const items = feed?.items || []
    const served = { status: ov.status, ms: ov.ms, coverage_status: feed?.coverage_status, items: items.length, with_url: items.filter((i) => typeof i.url === 'string' && i.url.trim() !== '').length }
    log('FWD4 SERVED', JSON.stringify(served))
    await openName(key)
    await page.waitForTimeout(1500)
    const dom = await page.evaluate(() => {
      const li = [...document.querySelectorAll('[data-feed-item]')]
      return { feed_state: (document.querySelector('[data-header-feed]') || { getAttribute: () => null }).getAttribute('data-header-feed'),
        items_in_markup: li.length, items_with_anchor: li.filter((x) => x.querySelector('a[href]')).length,
        first: li[0] ? { key: li[0].getAttribute('data-feed-item'), text: li[0].innerText.slice(0, 200), href: (li[0].querySelector('a') || {}).href || null, target: (li[0].querySelector('a') || {}).target || null } : null }
    })
    await capture('fwd4-BA-feed', { key, served, dom })
    let followed = null
    const a = page.locator('[data-feed-item] a[href]').first()
    if (await a.count()) {
      const href = await a.getAttribute('href')
      await a.scrollIntoViewIfNeeded().catch(() => {})
      const popP = context.waitForEvent('page', { timeout: 8000 }).catch(() => null)
      const urlBefore = page.url()
      await a.click({ timeout: 5000 }).catch(() => {})
      const pop = await popP
      let popUrl = null
      if (pop) { popUrl = pop.url(); await pop.waitForTimeout(500).catch(() => {}); popUrl = pop.url() !== 'about:blank' ? pop.url() : popUrl; await pop.close().catch(() => {}) }
      followed = { anchor_href: href, popup_opened: !!pop, popup_url_at_open: popUrl, same_tab_url_unchanged: page.url() === urlBefore, third_party_document_requests_aborted: blocked.slice() }
      log('FWD4 FOLLOWED', JSON.stringify(followed))
    }
    writeFileSync(path.join(dir, 'fwd4', 'fwd4.json'), JSON.stringify({ key, served, dom, followed, titles_first_5: items.slice(0, 5).map((i) => ({ title: i.title, publisher: i.publisher, published_at: i.published_at, has_url: !!i.url })) }, null, 1))
  } catch (e) { log('FWD4 ERROR', String(e.message).split('\n')[0]); rec({ label: 'fwd4-error', error: String(e.message).split('\n')[0] }) }

  // ---------- FWD-5: the Print action on BA, AMD, ASML_NA ----------
  const printed = []
  for (const [nm, key] of Object.entries({ BA: keyOf.BA, AMD: keyOf.AMD, ASML_NA: keyOf.ASML })) {
    if (!key) { printed.push({ name: nm, error: 'no covered key for ' + nm }); log('FWD5 NO KEY', nm); continue }
    try {
      setStep('fwd5 ' + key)
      await openName(key)
      const btn = page.getByRole('button', { name: 'Print', exact: true }).first()
      const respP = page.waitForResponse((r) => /\/security\/[^/]+\/print(\?|$)/.test(r.url()) && r.request().method() === 'GET', { timeout: 120000 })
      const t0 = Date.now()
      await btn.click({ timeout: 8000 })
      const resp = await respP
      const body = await resp.body()
      const ms = Date.now() - t0
      writeFileSync(path.join(dir, 'print', safe(key) + '.pdf'), body)
      await page.waitForTimeout(2000)
      await capture(`fwd5-${key}-print-modal`, { key, print_status: resp.status(), print_bytes: body.length, print_ms: ms, content_type: resp.headers()['content-type'] || null })
      printed.push({ name: nm, key, status: resp.status(), bytes: body.length, ms, content_type: resp.headers()['content-type'] || null })
      await page.keyboard.press('Escape').catch(() => {})
      await page.waitForTimeout(400)
      if (await page.locator('iframe[title="Security print pack"]').count().catch(() => 0)) await page.getByRole('button', { name: /close/i }).first().click({ timeout: 2000 }).catch(() => {})
    } catch (e) { log('FWD5 ERROR', key, String(e.message).split('\n')[0]); printed.push({ name: nm, key, error: String(e.message).split('\n')[0] }) }
  }
  writeFileSync(path.join(dir, 'print', 'print.json'), JSON.stringify(printed, null, 1))

  // ---------- FWD-7: /freshness, time to the first row from the navigation ----------
  const read = () => page.evaluate(() => {
    const trs = [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')]
    const lines = trs.map((tr) => ({ name: tr.children[0]?.textContent, last: tr.children[1]?.textContent, stale: tr.getAttribute('data-stale'), flags: [...tr.querySelectorAll('[data-stale-input]')].map((l) => l.textContent) }))
    return { summary: (document.querySelector('[data-slot="freshness-summary"]') || {}).textContent || null, rows: lines.length, stale_rows: lines.filter((l) => l.stale === 'true').length,
      first_five: lines.slice(0, 5), headers: [...document.querySelectorAll('[data-slot="freshness-table"] thead th')].map((t) => t.textContent),
      sort_buttons: [...document.querySelectorAll('[aria-label="Sort by"] button')].map((b) => ({ label: b.textContent, pressed: b.getAttribute('aria-pressed') })),
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
  log('AX6 OUT', OUT)
}
