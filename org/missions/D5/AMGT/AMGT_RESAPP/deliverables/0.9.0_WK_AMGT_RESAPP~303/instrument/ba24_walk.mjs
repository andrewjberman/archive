// ba-24 walk module (round 77): DEV-ONLY nav, FWD-7 closing visit, FWD-1, FWD-18 repairs, FWD-14, FWD-16, FWD-12, REFRESH, RESOLVE.
// GET only; the walker's network guard is unchanged. Loaded by walk_ay6.mjs through AX6_MODULE after sign-in.
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const TABS = ['THESIS', 'EXEC MANAGEMENT', 'PEERS', 'MODEL', 'POSTURE']
const NAMES = ['BA_US_Equity', 'AMD_US_Equity', 'ASML_NA_Equity']

export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, waitForLoaded, context } = ctx
  const dir = path.join(OUT, 'data')
  for (const d of ['fwd7', 'fwd18', 'fwd1', 'fwd16', 'fwd12', 'misc']) mkdirSync(path.join(dir, d), { recursive: true })
  mkdirSync(path.join(OUT, 'shots'), { recursive: true })
  const captures = []
  let n = 0
  const rec = (o) => { captures.push(o); writeFileSync(path.join(dir, 'captures.json'), JSON.stringify(captures, null, 1)) }
  const control = () => page.evaluate((T) => ({
    pathname: location.pathname,
    tab_labels: [...document.querySelectorAll('button,[role=tab],a')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && T.includes((e.textContent || '').trim().toUpperCase()) }).map((e) => (e.textContent || '').trim()),
    h1: ((document.querySelector('h1') || {}).textContent || '').trim(),
  }), TABS).catch(() => ({ pathname: null, tab_labels: [] }))
  // viewport=true takes the visible window only (a long table is clipped to what a reader sees); else the full page.
  const capture = async (label, extra = {}, viewport = false) => {
    n += 1
    const file = `shots/${String(n).padStart(3, '0')}-${label.replace(/[^a-z0-9]+/gi, '-').slice(0, 60)}.png`
    await page.screenshot({ path: path.join(OUT, file), fullPage: !viewport }).catch((e) => log('shot failed', e.message.split('\n')[0]))
    const c = await control()
    rec({ label, file, viewport, at: new Date().toISOString(), ...c, ...extra })
    log('CAPTURE', label, file, JSON.stringify(c.pathname), c.tab_labels.length, 'tab labels')
    return file
  }
  const save = (rel, obj) => writeFileSync(path.join(dir, rel), typeof obj === 'string' ? obj : JSON.stringify(obj, null, 1))
  const openName = async (key) => {
    await page.goto(opt.base + '/security-analysis/' + encodeURIComponent(key), { waitUntil: 'domcontentloaded', timeout: 30000 })
    await settle(page, 2500)
    return waitForLoaded(page)
  }
  // the headers the page sends on its scoped reads, held in-process for the RESOLVE read (names only are written)
  let lastScoped = null
  page.on('request', (req) => { const h = req.headers(); if (h.authorization && /\/api\/scoped\//.test(req.url())) lastScoped = h })
  const blocked = []
  await context.route((u) => !/^(localhost|127\.0\.0\.1)$/.test(u.hostname) && !/\.(cloudfront\.net|opalinvest\.com)$/.test(u.hostname), (route) => {
    const rq = route.request()
    if (rq.resourceType() === 'document') { blocked.push(rq.url()); return route.abort('blockedbyclient') }
    return route.fallback()
  })
  // every API answer the page receives while on a name page, to place the REFRESH press
  const apiLog = []
  page.on('response', (res) => { const u = res.url(); if (/\/api\//.test(u)) apiLog.push({ at: Date.now(), method: res.request().method(), status: res.status(), path: u.replace(/^https?:\/\/[^/]+/, '').replace(/\?.*/, '') }) })
  page.on('requestfailed', (req) => { if (/\/api\//.test(req.url())) apiLog.push({ at: Date.now(), method: req.method(), status: 'FAILED', failure: req.failure()?.errorText || null, path: req.url().replace(/^https?:\/\/[^/]+/, '').replace(/\?.*/, '') }) })

  // ---------- DEV-ONLY: the nav on the page sign-in landed on ----------
  try {
    setStep('dev-only nav')
    const landed = page.url()
    await settle(page, 1500)
    const nav = await page.evaluate(() => {
      const links = [...document.querySelectorAll('a[href]')].map((a) => ({ text: (a.textContent || '').trim(), href: a.getAttribute('href'), visible: (() => { const r = a.getBoundingClientRect(); return r.width > 0 && r.height > 0 })() }))
      return { links_total: links.length, freshness_entries: links.filter((l) => /freshness/i.test(l.text) || /\/freshness/.test(l.href || '')), nav_texts: links.filter((l) => l.visible).map((l) => l.text).filter(Boolean).slice(0, 40) }
    })
    save('misc/dev_only_nav.json', { landed_url: landed.replace(/^https?:\/\/[^/]+/, ''), ...nav })
    const fl = page.locator('a[href="/freshness"]').first()
    if (await fl.count()) await fl.scrollIntoViewIfNeeded().catch(() => {})
    await capture('devonly-nav-with-freshness-entry', { landed: landed.replace(/^https?:\/\/[^/]+/, ''), freshness_entries: nav.freshness_entries }, true)
    log('DEV-ONLY nav', JSON.stringify(nav.freshness_entries))
    const flink = page.locator('a[href="/freshness"]').first()
    if (await flink.count()) {
      await flink.hover({ timeout: 4000 }).catch(() => {})
      await page.waitForTimeout(900)
      const hv = await page.evaluate(() => { const a = document.querySelector('a[href="/freshness"]'); const r = a ? a.getBoundingClientRect() : null; const tip = [...document.querySelectorAll('[role=tooltip]')].map((t) => (t.innerText || '').trim()); return { link_rect_width: r ? Math.round(r.width) : null, tooltips: tip, link_text: a ? (a.innerText || a.textContent || '').trim() : null } })
      save('misc/dev_only_hover.json', hv)
      await capture('devonly-nav-freshness-entry-hovered', { hover: hv }, true)
    }
  } catch (e) { log('DEV-ONLY ERROR', String(e.message).split('\n')[0]); rec({ label: 'devonly-error', error: String(e.message).split('\n')[0] }) }

  // ---------- FWD-7 / FWD-14: /freshness first visit, then a second ----------
  const read = () => page.evaluate(() => {
    const trs = [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')]
    const headers = [...document.querySelectorAll('[data-slot="freshness-table"] thead th')].map((t) => (t.textContent || '').trim())
    const rows = trs.map((tr, i) => ({ i, name: (tr.children[0]?.textContent || '').trim(), cells: [...tr.children].slice(1).map((c) => (c.textContent || '').trim()), stale: tr.getAttribute('data-stale'),
      stale_input_words: [...tr.querySelectorAll('[data-stale-input]')].map((l) => l.textContent), states: Object.fromEntries([...tr.querySelectorAll('td[data-input]')].map((td) => [td.getAttribute('data-input'), td.getAttribute('data-state')])) }))
    const txt = (sel) => (document.querySelector(sel) || {}).textContent || null
    return { summary: txt('[data-slot="freshness-summary"]'), owner_line: txt('[data-slot="lists-owner"]'), out_of_date: txt('[data-slot="lists-out-of-date"]'), uncollected_note: txt('[data-slot="uncollected-note"]'), no_rule_note: txt('[data-slot="no-rule-note"]'),
      h1: (document.querySelector('h1') || {}).textContent || null, headers, rows, stale_rows: rows.filter((r) => r.stale === 'true').length,
      sort_buttons: [...document.querySelectorAll('[aria-label="Sort by"] button')].map((b) => ({ label: b.textContent, pressed: b.getAttribute('aria-pressed') })),
      page_end: (document.body.innerText || '').split('\n').slice(-6).join(' | '), body_head: (document.body.innerText || '').slice(0, 900) }
  })
  let firstRead = null
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
      const reqs = await page.evaluate(() => performance.getEntriesByType('resource').filter((e) => /freshness/.test(e.name)).map((e) => ({ name: e.name.replace(/\?.*/, ''), start_ms: Math.round(e.startTime), duration_ms: Math.round(e.duration), encoded: e.encodedBodySize, decoded: e.decodedBodySize })))
      const out = { pass, table_appeared: got, domcontentloaded_ms: tNav, first_row_ms_from_navigation: waited, freshness_requests: reqs, ...r }
      save(`fwd7/fwd7-${pass}.json`, out)
      log('FWD7', pass, 'first row at', waited, 'ms;', r.rows.length, 'rows;', r.stale_rows, 'stale;', JSON.stringify(r.headers))
      await capture(`fwd7-freshness-${pass}-top`, { table_appeared: got, first_row_ms_from_navigation: waited, rows: r.rows.length, stale_rows: r.stale_rows, summary: r.summary, owner_line: r.owner_line, out_of_date: r.out_of_date }, true)
      if (pass === 'first') {
        firstRead = r
        // FWD-14: the owner line and the out-of-date sentence, as drawn under the summary
        const ow = page.locator('[data-slot="lists-owner"]').first()
        await capture('fwd14-freshness-owner-line', { owner_line: r.owner_line, out_of_date: r.out_of_date, summary: r.summary }, true)
        // default sort = Stalest first: find a stale and a not-stale row FROM THE PAGE
        const staleIdx = r.rows.filter((x) => x.stale === 'true').map((x) => x.i)
        const freshIdx = r.rows.filter((x) => x.stale !== 'true').map((x) => x.i)
        save('fwd7/found_from_page.json', { default_sort: r.sort_buttons, stale_count: staleIdx.length, not_stale_count: freshIdx.length, first_stale: staleIdx.length ? r.rows[staleIdx[0]] : null, first_not_stale: freshIdx.length ? r.rows[freshIdx[0]] : null })
        // the two together: centre the boundary between the last stale row and the first not-stale row in the window
        const rowsLoc = page.locator('[data-slot="freshness-table"] tbody tr')
        if (staleIdx.length && freshIdx.length) {
          const boundary = Math.max(...staleIdx.filter((i) => i < Math.min(...freshIdx)).concat([0]))
          await rowsLoc.nth(Math.min(r.rows.length - 1, Math.min(...freshIdx))).evaluate((el) => el.scrollIntoView({ block: 'center' }))
          await page.waitForTimeout(400)
          await capture('fwd7-stale-beside-not-stale-default-sort', { sort: 'Stalest first (default)', stale_row: r.rows[Math.max(...staleIdx.filter((i) => i < Math.min(...freshIdx)).concat([staleIdx[0]]))], not_stale_row: r.rows[Math.min(...freshIdx)] }, true)
        } else {
          await capture('fwd7-no-mixed-rows-default-sort', { stale_count: staleIdx.length, not_stale_count: freshIdx.length, sort: 'Stalest first (default)' }, true)
        }
        // each sort; the page itself reorders
        const btns = page.locator('[aria-label="Sort by"] button')
        const nb = await btns.count()
        for (let i = 0; i < nb; i++) {
          const lab = ((await btns.nth(i).innerText()) || '').trim()
          await btns.nth(i).click({ timeout: 4000 }).catch(() => {})
          await page.waitForTimeout(600)
          await page.evaluate(() => window.scrollTo(0, 0))
          const s = await read()
          save(`fwd7/sort-${lab.replace(/\W+/g, '_')}.json`, { sort: lab, pressed: s.sort_buttons, first_ten: s.rows.slice(0, 10), stale_in_first_ten: s.rows.slice(0, 10).filter((x) => x.stale === 'true').length })
          await capture(`fwd7-sort-${lab}`, { sort: lab, first_five: s.rows.slice(0, 5) }, true)
        }
        // restore stalest-first so the five-row date-versus-flag capture is in a known order, then read 5 rows
        if (nb) { await btns.nth(0).click({ timeout: 4000 }).catch(() => {}); await page.waitForTimeout(500); await page.evaluate(() => window.scrollTo(0, 0)) }
        const agree = r.rows.map((x) => {
          const days = x.cells.slice(1, 1 + (r.headers.length - 3)).filter((c) => /^\d{4}-\d{2}-\d{2}$/.test(c)).sort()
          return { name: x.name, oldest_input_shown: x.cells[0], oldest_of_input_cells: days[0] || null, equal: (days[0] || null) === (/^\d{4}-/.test(x.cells[0]) ? x.cells[0] : null), stale: x.stale, stale_words: x.stale_input_words }
        })
        save('fwd7/date_vs_flag.json', { checked_rows: agree.length, equal_count: agree.filter((a) => a.equal).length, five: agree.slice(0, 5), mismatches: agree.filter((a) => !a.equal).slice(0, 15) })
        await capture('fwd7-date-vs-flag-five-rows', { five: agree.slice(0, 5), equal_count: agree.filter((a) => a.equal).length, of: agree.length }, true)
        // a never-collected column and its words
        const nc = r.rows.reduce((a, x) => { for (const [k, v] of Object.entries(x.states)) a[k] = { ...(a[k] || {}), [v]: ((a[k] || {})[v] || 0) + 1 }; return a }, {})
        save('fwd7/input_states.json', { by_input: nc, headers: r.headers, uncollected_note: r.uncollected_note })
      }
    } catch (e) { log('FWD7 ERROR', pass, String(e.message).split('\n')[0]); rec({ label: 'fwd7-error-' + pass, error: String(e.message).split('\n')[0] }) }
  }

  // ---------- name pages: FWD-16 top band, FWD-12 provenance, FWD-18 repairs, FWD-1 segments, REFRESH ----------
  for (const key of NAMES) {
    const short = key.split('_')[0]
    try {
      setStep('name ' + short)
      await openName(key)
      await page.waitForSelector('[data-top-band],[data-input-provenance],[data-top-band-description]', { timeout: 20000 }).catch(() => {})
      await page.waitForTimeout(2500)
      // FWD-16 top band + FWD-12 provenance, above any tab
      const top = await page.evaluate(() => {
        const t = (e) => (e ? (e.innerText || '').trim() : null)
        const tb = document.querySelector('[data-top-band]')
        const ip = document.querySelector('[data-input-provenance]')
        const desc = document.querySelector('[data-top-band-description]')
        return {
          company_line: t(desc),
          top_band: tb ? { text: t(tb), items: [...tb.querySelectorAll('[data-top-band-item]')].map((i) => t(i)), items_reason: t(tb.querySelector('[data-top-band-items-reason]')), social: t(tb.querySelector('[data-top-band-social]')), day_line: t([...tb.querySelectorAll('p')].find((p) => /In the news on/.test(p.textContent || ''))) } : null,
          provenance: ip ? { header: t(ip.querySelector('h4')), rows: [...ip.querySelectorAll('[data-provenance-row]')].map((li) => t(li)), controls: [...ip.querySelectorAll('button,a,[role=button]')].map((b) => t(b)) } : null,
        }
      })
      save(`fwd16/${short}_top.json`, top)
      log('FWD16', short, JSON.stringify({ company_line: !!top.company_line, band: !!top.top_band, prov_rows: top.provenance && top.provenance.rows.length }))
      await page.evaluate(() => window.scrollTo(0, 0))
      await capture(`fwd16-${short}-top-of-page`, { top }, true)
      if (top.top_band) {
        await page.locator('[data-top-band]').first().scrollIntoViewIfNeeded().catch(() => {})
        await capture(`fwd16-${short}-top-band-in-view`, { top_band: top.top_band }, true)
      }
      if (top.provenance) {
        await page.locator('[data-input-provenance]').first().scrollIntoViewIfNeeded().catch(() => {})
        await capture(`fwd12-${short}-input-provenance`, { provenance: top.provenance }, true)
      }
      // page-wide controls that read like a re-run / refresh
      const ctl = await page.evaluate(() => [...document.querySelectorAll('button,a,[role=button],summary')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && /re-?run|refresh|update now|reload|retry/i.test((e.textContent || '') + ' ' + (e.getAttribute('aria-label') || '')) }).map((e) => ({ tag: e.tagName, text: (e.textContent || '').trim().slice(0, 80), aria: e.getAttribute('aria-label') })))
      save(`fwd12/${short}_rerun_like_controls.json`, ctl)
      log('RERUN-LIKE CONTROLS', short, JSON.stringify(ctl))

      // FWD-18 / FWD-1 on the Thesis tab
      const dom = await page.evaluate(() => {
        const dc = document.querySelector('[data-driver-chart]')
        const sb = document.querySelector('[data-segment-breakdown]')
        return {
          driver_chart: dc ? { state: dc.getAttribute('data-driver-chart'), source: dc.getAttribute('data-driver-chart-source'), caption: (dc.querySelector('[data-driver-chart-caption]') || {}).textContent || null,
            passage_links: [...dc.querySelectorAll('[data-driver-chart-passage-link]')].map((b) => b.textContent), points_line: (dc.querySelector('[data-driver-chart-points]') || {}).textContent || null,
            y_ticks: [...dc.querySelectorAll('.recharts-yAxis .recharts-cartesian-axis-tick-value')].map((e) => e.textContent), y_axis_svg_text: [...dc.querySelectorAll('svg .recharts-yAxis text, svg .recharts-yAxis tspan')].map((e) => e.textContent), all_svg_text: [...dc.querySelectorAll('svg text')].map((e) => e.textContent), x_ticks: [...dc.querySelectorAll('.recharts-xAxis .recharts-cartesian-axis-tick-value')].map((e) => e.textContent),
            text: dc.innerText.slice(0, 1500) } : null,
          segments: sb ? { state: sb.getAttribute('data-segment-state'), header: (sb.querySelector('h4') || {}).textContent || null,
            headings: [...sb.querySelectorAll('[data-segment-heading]')].map((h) => h.textContent), reasons: [...sb.querySelectorAll('[data-segment-reason]')].map((h) => h.textContent),
            rows: [...sb.querySelectorAll('[data-segment-row]')].map((li) => ({ n: li.getAttribute('data-segment-row'), text: (li.querySelector('p') || {}).textContent || null })),
            text: sb.innerText.slice(0, 3000) } : null,
        }
      })
      save(`fwd18/${short}_dom.json`, dom)
      log('FWD18 DOM', short, JSON.stringify({ driver: dom.driver_chart && dom.driver_chart.state, links: dom.driver_chart && dom.driver_chart.passage_links.length, y_ticks: dom.driver_chart && dom.driver_chart.y_ticks, seg: dom.segments && dom.segments.state, seg_headings: dom.segments && dom.segments.headings.length }))
      const dcLoc = page.locator('[data-driver-chart]').first()
      if (await dcLoc.count()) await dcLoc.scrollIntoViewIfNeeded().catch(() => {})
      await capture(`fwd18-${short}-driver-chart`, { dom_driver: dom.driver_chart }, true)

      // press ONE point at a time and count renders of the passage on the page after each press
      const links = page.locator('[data-driver-chart-passage-link]')
      const nl = await links.count()
      const presses = []
      for (let i = 0; i < nl; i++) {
        const link = links.nth(i)
        const label = await link.innerText()
        await link.scrollIntoViewIfNeeded().catch(() => {})
        await link.click({ timeout: 5000 }).catch(() => {})
        await page.waitForTimeout(800)
        const st = await page.evaluate(() => {
          const bq = [...document.querySelectorAll('[data-driver-chart-passage-source]')]
          const cites = [...document.querySelectorAll('[data-driver-chart-passage-cite]')]
          const tbl = document.querySelector('[data-driver-chart-passage-table]')
          return { passage_blocks_on_page: bq.length, cites_on_page: cites.length, cite_texts: cites.map((c) => c.textContent),
            source_attr: bq[0] ? bq[0].getAttribute('data-driver-chart-passage-source') : null,
            text: bq[0] ? bq[0].innerText.slice(0, 1500) : null,
            table: tbl ? { column_labels: [...tbl.querySelectorAll('thead th, tr:first-child th')].map((h) => (h.textContent || '').trim()), rows: tbl.querySelectorAll('tbody tr').length, heading: (document.querySelector('[data-driver-chart-passage-table-heading]') || {}).textContent || null, note: (document.querySelector('[data-driver-chart-passage-table-note]') || {}).textContent || null, unaligned_rows: document.querySelectorAll('[data-driver-chart-passage-row-unaligned]').length } : null,
            table_reason: (document.querySelector('[data-driver-chart-passage-table-reason]') || {}).textContent || null,
            bq_text_occurrences_in_body: (() => { const b = bq[0]; if (!b) return 0; const s = (b.innerText || '').trim().slice(0, 40); return s ? (document.body.innerText.split(s).length - 1) : 0 })() }
        })
        presses.push({ link_label: label, ...st })
        if (i < 2 || st.table) await capture(`fwd18-${short}-passage-open-${i + 1}`, { press: { link_label: label, ...st } }, true)
        await link.click({ timeout: 5000 }).catch(() => {}) // close it again so the next press stands alone
        await page.waitForTimeout(300)
      }
      save(`fwd18/${short}_presses.json`, presses)
      log('FWD18 PRESSES', short, JSON.stringify(presses.map((p) => ({ l: p.link_label, blocks: p.passage_blocks_on_page, cites: p.cites_on_page, occ: p.bq_text_occurrences_in_body, table_cols: p.table && p.table.column_labels.length, tbl: !!p.table }))))

      // segments
      const sbLoc = page.locator('[data-segment-breakdown]').first()
      if (await sbLoc.count()) await sbLoc.scrollIntoViewIfNeeded().catch(() => {})
      await capture(`fwd1-${short}-segments`, { dom_segments: dom.segments && { state: dom.segments.state, headings: dom.segments.headings, rows: dom.segments.rows.length } }, true)
      const sum = page.locator('[data-segment-cite] summary').first()
      if (await sum.count()) { await sum.click({ timeout: 4000 }).catch(() => {}); await page.waitForTimeout(500); await capture(`fwd1-${short}-segment-source-open`, {}, true) }
      // business description
      const about = page.locator('summary', { hasText: /About the company/i }).first()
      if (await about.count()) {
        await about.scrollIntoViewIfNeeded().catch(() => {})
        await about.click({ timeout: 4000 }).catch(() => {})
        await page.waitForTimeout(600)
        const at = await page.evaluate(() => { const d = [...document.querySelectorAll('details')].find((x) => /About the company/i.test((x.querySelector('summary') || {}).textContent || '')); return d ? { open: d.open, text: d.innerText.slice(0, 1500) } : null })
        save(`fwd1/${short}_about.json`, at)
        await capture(`fwd1-${short}-about-open`, { about: at && { open: at.open, len: at.text.length } }, true)
      } else { save(`fwd1/${short}_about.json`, { absent: true }) }

      // REFRESH: on BA only, before leaving the page
      if (short === 'BA') {
        await page.evaluate(() => window.scrollTo(0, 0))
        const rfAll = await page.evaluate(() => [...document.querySelectorAll('button,[role=button],a')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && /refresh/i.test((e.textContent || '') + ' ' + (e.getAttribute('aria-label') || '') + ' ' + (e.getAttribute('title') || '')) }).map((e) => ({ tag: e.tagName, text: (e.textContent || '').trim().slice(0, 80), href: e.getAttribute('href'), aria: e.getAttribute('aria-label'), title: e.getAttribute('title'), disabled: e.disabled === true, in_nav: !!e.closest('nav,aside,[role=navigation]') })))
        const rf = rfAll.filter((x) => !x.in_nav)
        save('misc/refresh_control.json', { controls_found_all: rfAll, controls_found_outside_nav: rf })
        log('REFRESH controls', JSON.stringify(rfAll))
        if (rf.length === 0) {
          await capture('refresh-ba-no-control-on-page', { controls_found_outside_nav: 0, nav_entries_matching: rfAll }, true)
        } else {
          await capture('refresh-ba-before-press', { controls_found: rf }, true)
          const before = apiLog.length
          const tp = Date.now()
          await page.locator('button,[role=button],a').filter({ hasText: /refresh/i }).first().click({ timeout: 5000 }).catch((e) => log('refresh press failed', String(e.message).split('\n')[0]))
          await page.waitForTimeout(6000)
          const after = await page.evaluate(() => ({ alerts: [...document.querySelectorAll('[role=alert],[role=status],[data-sonner-toast],.toast,[aria-live]')].map((e) => (e.innerText || '').trim()).filter(Boolean).slice(0, 8), spinners: document.querySelectorAll('[class*=animate-spin],[role=progressbar],[aria-busy=true]').length }))
          save('misc/refresh_after.json', { after, api_during: apiLog.slice(before).map((a) => ({ ...a, ms_after_press: a.at - tp })) })
          await capture('refresh-ba-after-press-6s', { after, api_during: apiLog.slice(before).length }, true)
        }
      }

      // model tab: ledger (FWD-12), model numbers (FWD-1)
      const modelTab = page.getByRole('button', { name: /^model$/i }).first()
      const mt = (await modelTab.count()) ? modelTab : page.getByRole('tab', { name: /^model$/i }).first()
      if (await mt.count()) {
        await mt.scrollIntoViewIfNeeded().catch(() => {})
        await mt.click({ timeout: 4000 }).catch(() => {})
        await page.waitForTimeout(3500)
        const led = await page.evaluate(() => ({ ledger: [...document.querySelectorAll('[data-ledger-class]')].map((li) => ({ cls: li.getAttribute('data-ledger-class'), text: (li.innerText || '').trim() })), refreshing_details: (() => { const d = [...document.querySelectorAll('details')].find((x) => /Refreshing an input/i.test(x.textContent || '')); return d ? (d.innerText || '').trim() : null })(), text_head: document.body.innerText.slice(0, 1500) }))
        save(`fwd12/${short}_model_ledger.json`, led)
        const ld = page.locator('[data-ledger-class]').first()
        if (await ld.count()) await ld.scrollIntoViewIfNeeded().catch(() => {})
        await capture(`fwd12-${short}-model-tab-ledger`, { ledger: led.ledger, refreshing: led.refreshing_details }, true)
        await page.evaluate(() => window.scrollTo(0, 0))
        await capture(`fwd1-${short}-model-tab`, {}, true)
      }
    } catch (e) { log('NAME ERROR', short, String(e.message).split('\n')[0]); rec({ label: 'name-error-' + short, error: String(e.message).split('\n')[0] }) }
  }

  // ---------- RESOLVE THROUGH THE GATEWAY ----------
  try {
    setStep('resolve')
    if (!lastScoped) { await page.goto(opt.base + '/security-analysis/' + encodeURIComponent('BA_US_Equity'), { waitUntil: 'domcontentloaded' }); await page.waitForTimeout(4000) }
    const SKIP = /^(host|connection|content-length|accept-encoding|cookie|origin|referer|user-agent|sec-|:)/i
    const sent = Object.fromEntries(Object.entries(lastScoped || {}).filter(([k]) => !SKIP.test(k)))
    const get = (url, headers) => page.evaluate(async ({ url, headers }) => {
      try { const r = await fetch(url, { method: 'GET', headers, cache: 'no-store' }); const t = await r.text(); return { status: r.status, bytes: t.length, body: t.slice(0, 6000) } } catch (e) { return { status: 'fetch failed: ' + String(e).slice(0, 80), bytes: null, body: null } }
    }, { url, headers })
    const url = '/api/scoped/amgt/resolve?q=Lenovo'
    const withH = await get(url, sent)
    const ctrl = await get(url, {})
    const has992 = typeof withH.body === 'string' && /992_HK_Equity/.test(withH.body)
    const res = { path: url, status: withH.status, bytes: withH.bytes, header_names_sent: Object.keys(sent).sort(), lists_992_HK_Equity: has992, control_without_headers_status: ctrl.status, body_head: withH.body && withH.body.slice(0, 1500) }
    save('misc/resolve.json', res)
    log('RESOLVE', JSON.stringify({ status: res.status, has992, control: res.control_without_headers_status }))
    await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {})
    await settle(page, 1500)
    await capture('resolve-lenovo-readout-page-context', { resolve: { status: res.status, lists_992_HK_Equity: has992 } }, true)
  } catch (e) { log('RESOLVE ERROR', String(e.message).split('\n')[0]); rec({ label: 'resolve-error', error: String(e.message).split('\n')[0] }) }

  save('blocked_third_party.json', blocked)
  log('BA24 OUT', OUT)
}
