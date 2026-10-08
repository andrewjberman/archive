// cc-8 pass 1 (round 79): reconnaissance + the raw API-client reads. GET only; the walker's network guard is unchanged.
// Loaded by walk_ay6.mjs through AX6_MODULE after sign-in. Saves raw served answers and the clickable inventory so the
// final pass presses by what the page really draws. Third-party DOCUMENT requests are aborted (nothing leaves the device).
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const NAMES = ['ASML_NA_Equity', 'BA_US_Equity', 'AMD_US_Equity', 'NU_US_Equity']

export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, waitForLoaded, context } = ctx
  const dir = path.join(OUT, 'data')
  for (const d of ['api', 'dom', 'fwd7']) mkdirSync(path.join(dir, d), { recursive: true })
  mkdirSync(path.join(OUT, 'shots'), { recursive: true })
  const save = (rel, obj) => writeFileSync(path.join(dir, rel), typeof obj === 'string' ? obj : JSON.stringify(obj, null, 1))
  let n = 0
  const shot = async (label, viewport = true) => {
    n += 1
    const file = `shots/${String(n).padStart(3, '0')}-${label.replace(/[^a-z0-9]+/gi, '-').slice(0, 60)}.png`
    await page.screenshot({ path: path.join(OUT, file), fullPage: !viewport }).catch((e) => log('shot failed', e.message.split('\n')[0]))
    log('CAPTURE', file)
  }
  let lastScoped = null
  page.on('request', (req) => { const h = req.headers(); if (h.authorization && /\/api\/scoped\//.test(req.url())) lastScoped = h })
  const blocked = []
  await context.route((u) => !/^(localhost|127\.0\.0\.1)$/.test(u.hostname) && !/\.(cloudfront\.net|opalinvest\.com)$/.test(u.hostname), (route) => {
    const rq = route.request()
    if (rq.resourceType() === 'document') { blocked.push(rq.url()); return route.abort('blockedbyclient') }
    return route.fallback()
  })
  const SKIP = /^(host|connection|content-length|accept-encoding|cookie|origin|referer|user-agent|sec-|:)/i
  const apiGet = async (url) => {
    const sent = Object.fromEntries(Object.entries(lastScoped || {}).filter(([k]) => !SKIP.test(k)))
    return page.evaluate(async ({ url, headers }) => {
      try { const x = await fetch(url, { method: 'GET', headers, cache: 'no-store' }); const t = await x.text(); let j = null; try { j = JSON.parse(t) } catch {} return { status: x.status, bytes: t.length, json: j, text: j ? null : t.slice(0, 300) } } catch (e) { return { status: 'fetch failed: ' + String(e).slice(0, 80), bytes: null, json: null } }
    }, { url, headers: sent })
  }

  // ---- FWD-7: first and second visit, DOM table + raw API ----
  for (const pass of ['first', 'second']) {
    setStep('fwd7 ' + pass)
    const t0 = Date.now()
    await page.goto(opt.base + '/freshness', { waitUntil: 'domcontentloaded', timeout: 30000 })
    const dcl = Date.now() - t0
    const got = await page.locator('[data-slot="freshness-table"] tbody tr').first().waitFor({ timeout: 90000 }).then(() => true).catch(() => false)
    const first_row_ms = Date.now() - t0
    await settle(page, 1500)
    const r = await page.evaluate(() => {
      const trs = [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')]
      return {
        headers: [...document.querySelectorAll('[data-slot="freshness-table"] thead th')].map((t) => (t.textContent || '').trim()),
        rows: trs.map((tr, i) => ({ i, name: (tr.children[0]?.textContent || '').trim(), stale: tr.getAttribute('data-stale'), cells: [...tr.children].slice(1).map((c) => (c.textContent || '').trim()),
          sa: (() => { const td = tr.querySelector('td[data-input="seekingalpha"],td[data-input="seeking_alpha"],td[data-input*="seeking"]'); return td ? { input: td.getAttribute('data-input'), state: td.getAttribute('data-state'), text: (td.textContent || '').trim() } : null })(),
          inputs: [...tr.querySelectorAll('td[data-input]')].map((td) => ({ input: td.getAttribute('data-input'), state: td.getAttribute('data-state'), text: (td.textContent || '').trim() })),
          stale_words: [...tr.querySelectorAll('[data-stale-input]')].map((l) => l.textContent) })),
        summary: (document.querySelector('[data-slot="freshness-summary"]') || {}).textContent || null,
        notes: ['lists-owner', 'lists-out-of-date', 'uncollected-note', 'no-rule-note'].map((s) => [s, (document.querySelector(`[data-slot="${s}"]`) || {}).textContent || null]),
        page_end: (document.body.innerText || '').split('\n').slice(-6).join(' | '),
      }
    })
    save(`fwd7/dom_${pass}.json`, { pass, table_appeared: got, domcontentloaded_ms: dcl, first_row_ms_from_navigation: first_row_ms, stale_rows: r.rows.filter((x) => x.stale === 'true').length, ...r })
    log('FWD7', pass, 'first row', first_row_ms, 'ms;', r.rows.length, 'rows;', r.rows.filter((x) => x.stale === 'true').length, 'stale;', JSON.stringify(r.headers))
    if (pass === 'first') {
      const a = await apiGet('/api/scoped/amgt/freshness?view=page')
      save('api/freshness_raw.json', a)
      log('API freshness', a.status, a.bytes)
    }
    await shot('fwd7-freshness-' + pass + '-top', true)
  }

  // ---- the four names: raw thesis answer + DOM inventory ----
  for (const key of NAMES) {
    try {
      setStep('name ' + key)
      await page.goto(opt.base + '/security-analysis/' + encodeURIComponent(key), { waitUntil: 'domcontentloaded', timeout: 30000 })
      await settle(page, 2500)
      await waitForLoaded(page)
      await page.waitForTimeout(6000)
      const a = await apiGet('/api/scoped/amgt/security/' + encodeURIComponent(key) + '/thesis')
      save(`api/thesis_${key}.json`, a)
      log('API thesis', key, a.status, a.bytes, a.json ? Object.keys(a.json).join(',').slice(0, 300) : a.text)
      const inv = await page.evaluate(() => {
        const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 }
        const attrs = (e) => [...e.attributes].filter((a) => a.name.startsWith('data-') || a.name.startsWith('aria-')).map((a) => a.name + '=' + String(a.value).slice(0, 60)).slice(0, 6)
        return {
          h1: ((document.querySelector('h1') || {}).textContent || '').trim(),
          buttons: [...document.querySelectorAll('button,a,[role=button],summary')].filter(vis).map((e) => ({ tag: e.tagName, text: (e.textContent || '').trim().slice(0, 120), attrs: attrs(e) })),
          data_hooks: [...new Set([...document.querySelectorAll('*')].flatMap((e) => [...e.attributes].filter((a) => a.name.startsWith('data-')).map((a) => a.name)))].sort(),
          svg_charts: document.querySelectorAll('svg.recharts-surface').length,
          driver_chart: [...document.querySelectorAll('[data-driver-chart]')].map((e) => ({ state: e.getAttribute('data-driver-chart'), text: (e.innerText || '').trim().slice(0, 500) })),
          segment: [...document.querySelectorAll('[data-segment-breakdown]')].map((e) => ({ state: e.getAttribute('data-segment-state'), text: (e.innerText || '').trim().slice(0, 1500) })),
          body: document.body.innerText || '',
        }
      })
      save(`dom/${key}_thesis_tab.json`, inv)
      await shot('name-' + key + '-thesis-tab-full', false)
    } catch (e) { log('NAME ERROR', key, String(e.message).split('\n')[0]) }
  }
  save('blocked_third_party.json', blocked)
  log('CC8 RECON OUT', OUT)
}
