// bb-19 walk module (round 78): FWD-7, FWD-16 (one press), FWD-12, FWD-1 (AMD), COVERAGE (MSFT, BA), OFFICERS (BA, HD, BP/ LN).
// Derived from round 77's ba24_walk.mjs. GET only; the walker's network guard is unchanged. Loaded by walk_ay6.mjs through
// AX6_MODULE after sign-in. Third-party DOCUMENT requests are aborted in the browser context (nothing leaves the device).
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const TABS = ['THESIS', 'EXEC MANAGEMENT', 'PEERS', 'MODEL', 'POSTURE']

export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, waitForLoaded, context } = ctx
  const dir = path.join(OUT, 'data')
  for (const d of ['fwd7', 'fwd16', 'fwd12', 'fwd1', 'coverage', 'officers', 'api', 'misc']) mkdirSync(path.join(dir, d), { recursive: true })
  mkdirSync(path.join(OUT, 'shots'), { recursive: true })
  const captures = []
  let n = 0
  const rec = (o) => { captures.push(o); writeFileSync(path.join(dir, 'captures.json'), JSON.stringify(captures, null, 1)) }
  const control = () => page.evaluate((T) => ({
    pathname: location.pathname,
    tab_labels: [...document.querySelectorAll('button,[role=tab],a')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && T.includes((e.textContent || '').trim().toUpperCase()) }).map((e) => (e.textContent || '').trim()),
    h1: ((document.querySelector('h1') || {}).textContent || '').trim(),
  }), TABS).catch(() => ({ pathname: null, tab_labels: [] }))
  const capture = async (label, extra = {}, viewport = false, pg = page) => {
    n += 1
    const file = `shots/${String(n).padStart(3, '0')}-${label.replace(/[^a-z0-9]+/gi, '-').slice(0, 60)}.png`
    await pg.screenshot({ path: path.join(OUT, file), fullPage: !viewport }).catch((e) => log('shot failed', e.message.split('\n')[0]))
    const c = pg === page ? await control() : { pathname: 'popup' }
    rec({ label, file, viewport, at: new Date().toISOString(), ...c, ...extra })
    log('CAPTURE', label, file, JSON.stringify(c.pathname), (c.tab_labels || []).length, 'tab labels')
    return file
  }
  const save = (rel, obj) => writeFileSync(path.join(dir, rel), typeof obj === 'string' ? obj : JSON.stringify(obj, null, 1))
  const openName = async (key) => {
    await page.goto(opt.base + '/security-analysis/' + encodeURIComponent(key), { waitUntil: 'domcontentloaded', timeout: 30000 })
    await settle(page, 2500)
    await waitForLoaded(page)
    await page.waitForSelector('[data-top-band],[data-input-provenance],[data-top-band-description]', { timeout: 20000 }).catch(() => {})
    await page.waitForTimeout(2500)
  }
  const bodyText = () => page.evaluate(() => document.body.innerText || '')
  const clickTab = async (rx) => {
    const b = page.getByRole('button', { name: rx }).first()
    const t = (await b.count()) ? b : page.getByRole('tab', { name: rx }).first()
    if (!(await t.count())) return false
    await t.scrollIntoViewIfNeeded().catch(() => {})
    await t.click({ timeout: 4000 }).catch(() => {})
    await page.waitForTimeout(3500)
    return true
  }

  let lastScoped = null
  page.on('request', (req) => { const h = req.headers(); if (h.authorization && /\/api\/scoped\//.test(req.url())) lastScoped = h })
  const blocked = []
  await context.route((u) => !/^(localhost|127\.0\.0\.1)$/.test(u.hostname) && !/\.(cloudfront\.net|opalinvest\.com)$/.test(u.hostname), (route) => {
    const rq = route.request()
    if (rq.resourceType() === 'document') { blocked.push(rq.url()); return route.abort('blockedbyclient') }
    return route.fallback()
  })

  // the page's own API client: the overlay answer for one name (keys, research_coverage wherever it sits, provenance, band)
  const SKIP = /^(host|connection|content-length|accept-encoding|cookie|origin|referer|user-agent|sec-|:)/i
  const overlayRead = async (key, tag) => {
    const sent = Object.fromEntries(Object.entries(lastScoped || {}).filter(([k]) => !SKIP.test(k)))
    const url = '/api/scoped/amgt/security/' + encodeURIComponent(key) + '/overlay'
    const r = await page.evaluate(async ({ url, headers }) => {
      try { const x = await fetch(url, { method: 'GET', headers, cache: 'no-store' }); const t = await x.text(); let j = null; try { j = JSON.parse(t) } catch {} return { status: x.status, bytes: t.length, json: j } } catch (e) { return { status: 'fetch failed: ' + String(e).slice(0, 80), bytes: null, json: null } }
    }, { url, headers: sent })
    const j = r.json
    const found = []
    const walk = (o, p) => { if (o && typeof o === 'object') for (const [k, v] of Object.entries(o)) { if (/coverage/i.test(k)) found.push({ path: p + '/' + k, value: typeof v === 'object' ? JSON.stringify(v).slice(0, 600) : v }); walk(v, p + '/' + k) } }
    walk(j, '')
    const find = (o, k) => { if (o && typeof o === 'object') { if (k in o) return o[k]; for (const v of Object.values(o)) { const f = find(v, k); if (f !== undefined) return f } } return undefined }
    const tb = find(j, 'top_band')
    const ip = find(j, 'input_provenance')
    const out = {
      key, url, status: r.status, bytes: r.bytes, header_names_sent: Object.keys(sent).sort(),
      top_level_keys: j && typeof j === 'object' ? Object.keys(j) : null,
      data_keys: j && j.data && typeof j.data === 'object' ? Object.keys(j.data) : null,
      keys_matching_coverage: found,
      research_coverage_key_present: found.some((f) => /research_coverage$/.test(f.path)),
      top_band_keys: tb && typeof tb === 'object' ? Object.keys(tb) : null,
      top_band_day: tb ? tb.day : null,
      top_band_items: tb && Array.isArray(tb.items) ? tb.items.map((i) => ({ publisher: i.publisher, published_utc: i.published_utc, title: i.title, has_url: !!i.url, url_host: i.url ? (() => { try { return new URL(i.url).host } catch { return 'unparsed' } })() : null, other_keys: Object.keys(i) })) : null,
      top_band_items_reason: tb ? tb.items_reason : null,
      input_provenance: Array.isArray(ip) ? ip.map((e) => ({ input: e.input, source: e.source, last_run: e.last_run, outcome: e.outcome, reason: e.reason })) : ip === undefined ? 'ABSENT' : ip,
    }
    save(`api/overlay_${tag}.json`, out)
    log('API OVERLAY', tag, JSON.stringify({ status: out.status, research_coverage_key_present: out.research_coverage_key_present, prov: Array.isArray(out.input_provenance) && out.input_provenance.length }))
    return out
  }

  // ---------- FWD-7: /freshness first visit, then a second ----------
  const read = () => page.evaluate(() => {
    const trs = [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')]
    const headers = [...document.querySelectorAll('[data-slot="freshness-table"] thead th')].map((t) => (t.textContent || '').trim())
    const rows = trs.map((tr, i) => ({ i, name: (tr.children[0]?.textContent || '').trim(), cells: [...tr.children].slice(1).map((c) => (c.textContent || '').trim()), stale: tr.getAttribute('data-stale'),
      stale_input_words: [...tr.querySelectorAll('[data-stale-input]')].map((l) => l.textContent), states: Object.fromEntries([...tr.querySelectorAll('td[data-input]')].map((td) => [td.getAttribute('data-input'), td.getAttribute('data-state')])) }))
    const txt = (sel) => (document.querySelector(sel) || {}).textContent || null
    return { summary: txt('[data-slot="freshness-summary"]'), owner_line: txt('[data-slot="lists-owner"]'), out_of_date: txt('[data-slot="lists-out-of-date"]'), uncollected_note: txt('[data-slot="uncollected-note"]'),
      h1: (document.querySelector('h1') || {}).textContent || null, headers, rows, stale_rows: rows.filter((r) => r.stale === 'true').length,
      sort_buttons: [...document.querySelectorAll('[aria-label="Sort by"] button')].map((b) => ({ label: b.textContent, pressed: b.getAttribute('aria-pressed') })),
      page_end: (document.body.innerText || '').split('\n').slice(-6).join(' | '), body_head: (document.body.innerText || '').slice(0, 900) }
  })
  for (const pass of ['first', 'second']) {
    try {
      setStep('fwd7 ' + pass)
      const landed = page.url().replace(/^https?:\/\/[^/]+/, '')
      const t0 = Date.now()
      await page.goto(opt.base + '/freshness', { waitUntil: 'domcontentloaded', timeout: 30000 })
      const tNav = Date.now() - t0
      const got = await page.locator('[data-slot="freshness-table"] tbody tr').first().waitFor({ timeout: 90000 }).then(() => true).catch(() => false)
      const waited = Date.now() - t0
      await settle(page, 1500)
      const r = await read()
      const reqs = await page.evaluate(() => performance.getEntriesByType('resource').filter((e) => /freshness/.test(e.name)).map((e) => ({ name: e.name.replace(/\?.*/, ''), start_ms: Math.round(e.startTime), duration_ms: Math.round(e.duration), encoded: e.encodedBodySize, decoded: e.decodedBodySize })))
      // the Seeking Alpha column: index among headers (cells exclude the Company column)
      const saIdx = r.headers.findIndex((h) => /seeking alpha/i.test(h))
      const saCol = r.rows.map((x) => ({ name: x.name, cell: saIdx > 0 ? x.cells[saIdx - 1] : null, stale: x.stale, stale_words: x.stale_input_words, state: x.states['seeking_alpha'] || x.states['seeking-alpha'] || x.states }))
      const out = { pass, landed_before_visit: landed, table_appeared: got, domcontentloaded_ms: tNav, first_row_ms_from_navigation: waited, freshness_requests: reqs, seeking_alpha_header_index: saIdx, seeking_alpha_column_all_rows: saCol, ...r }
      save(`fwd7/fwd7-${pass}.json`, out)
      log('FWD7', pass, 'first row at', waited, 'ms;', r.rows.length, 'rows;', r.stale_rows, 'stale;', JSON.stringify(r.headers))
      await capture(`fwd7-freshness-${pass}-top`, { table_appeared: got, first_row_ms_from_navigation: waited, rows: r.rows.length, stale_rows: r.stale_rows, summary: r.summary, headers: r.headers, sa_first5: saCol.slice(0, 5) }, true)
      if (pass === 'first') {
        // stale and not-stale rows together, as found from the page
        const staleIdx = r.rows.filter((x) => x.stale === 'true').map((x) => x.i)
        const freshIdx = r.rows.filter((x) => x.stale !== 'true').map((x) => x.i)
        if (staleIdx.length && freshIdx.length) {
          const rowsLoc = page.locator('[data-slot="freshness-table"] tbody tr')
          await rowsLoc.nth(Math.min(r.rows.length - 1, Math.min(...freshIdx))).evaluate((el) => el.scrollIntoView({ block: 'center' }))
          await page.waitForTimeout(400)
        }
        await capture('fwd7-seeking-alpha-column-rows', { sa_first5: saCol.slice(0, 5), stale_count: staleIdx.length, not_stale_count: freshIdx.length, stale_rows: r.rows.filter((x) => x.stale === 'true').map((x) => ({ name: x.name, cells: x.cells, words: x.stale_input_words })) }, true)
      }
    } catch (e) { log('FWD7 ERROR', pass, String(e.message).split('\n')[0]); rec({ label: 'fwd7-error-' + pass, error: String(e.message).split('\n')[0] }) }
  }

  // ---------- BA: FWD-16 top band + ONE PRESS, FWD-12 places that state the inputs ----------
  try {
    setStep('name BA')
    await openName('BA_US_Equity')
    const top = await page.evaluate(() => {
      const t = (e) => (e ? (e.innerText || '').trim() : null)
      const tb = document.querySelector('[data-top-band]')
      const ip = document.querySelector('[data-input-provenance]')
      const desc = document.querySelector('[data-top-band-description]')
      return {
        company_line: t(desc),
        top_band: tb ? { text: t(tb), items: [...tb.querySelectorAll('[data-top-band-item]')].map((i) => ({ text: t(i), tag: i.tagName, href: i.getAttribute('href'), target: i.getAttribute('target') })), items_reason: t(tb.querySelector('[data-top-band-items-reason]')), social: t(tb.querySelector('[data-top-band-social]')), day_line: t([...tb.querySelectorAll('p')].find((p) => /In the news on/.test(p.textContent || ''))) } : null,
        provenance: ip ? { header: t(ip.querySelector('h4')), rows: [...ip.querySelectorAll('[data-provenance-row]')].map((li) => t(li)), controls: [...ip.querySelectorAll('button,a,[role=button]')].map((b) => t(b)) } : null,
      }
    })
    save('fwd16/BA_top.json', top)
    await overlayRead('BA_US_Equity', 'BA')
    await page.evaluate(() => window.scrollTo(0, 0))
    await capture('fwd16-BA-top-of-page', { top }, true)
    if (top.top_band) {
      await page.locator('[data-top-band]').first().scrollIntoViewIfNeeded().catch(() => {})
      await capture('fwd16-BA-top-band-before-press', { top_band: top.top_band }, true)
    }
    // ---- THE ONE PRESS ----
    const item = page.locator('[data-top-band-item]').first()
    if (await item.count()) {
      const pre = await item.evaluate((e) => ({ tag: e.tagName, text: (e.innerText || '').trim(), href: e.getAttribute('href'), target: e.getAttribute('target'), meta_line: [...e.querySelectorAll('span')].map((s) => (s.innerText || '').trim()) }))
      const urlBefore = page.url()
      const pagesBefore = context.pages().length
      const popupP = context.waitForEvent('page', { timeout: 6000 }).catch(() => null)
      await item.scrollIntoViewIfNeeded().catch(() => {})
      const tPress = Date.now()
      await item.click({ timeout: 6000 }).catch((e) => log('PRESS failed', String(e.message).split('\n')[0]))
      const popup = await popupP
      await page.waitForTimeout(2500)
      const post = await page.evaluate(() => ({ url: location.pathname, dialogs: document.querySelectorAll('[role=dialog],[role=alertdialog],dialog[open]').length, open_details: document.querySelectorAll('details[open]').length, body_len: (document.body.innerText || '').length }))
      let popupInfo = null
      if (popup) {
        await popup.waitForTimeout(1500).catch(() => {})
        popupInfo = { opened: true, url: popup.url(), title: await popup.title().catch(() => null) }
        await capture('fwd16-BA-the-opened-tab-after-press', { popup: popupInfo }, true, popup)
      }
      const pressRec = { pressed: pre, ms_after_press_read: Date.now() - tPress, page_url_before: urlBefore.replace(/^https?:\/\/[^/]+/, ''), page_url_after: page.url().replace(/^https?:\/\/[^/]+/, ''), pages_before: pagesBefore, pages_after: context.pages().length, new_tab: popupInfo, panel_dialogs_after: post.dialogs, details_open_after: post.open_details, blocked_third_party_document_requests: blocked.slice() }
      save('fwd16/BA_press.json', pressRec)
      log('FWD16 PRESS', JSON.stringify({ tag: pre.tag, href_host: (() => { try { return new URL(pre.href).host } catch { return pre.href } })(), new_tab: !!popup, popup_url: popupInfo && popupInfo.url, dialogs: post.dialogs }))
      await page.bringToFront().catch(() => {})
      await capture('fwd16-BA-main-page-after-press', { press: pressRec }, true)
      if (popup) await popup.close().catch(() => {})
    } else {
      save('fwd16/BA_press.json', { pressed: null, reason: 'no [data-top-band-item] on the page', items_reason: top.top_band && top.top_band.items_reason })
      await capture('fwd16-BA-no-news-item-to-press', {}, true)
    }

    // ---- FWD-12: every place the page states the inputs ----
    await page.evaluate(() => window.scrollTo(0, 0))
    const places = async (tab) => page.evaluate(() => {
      const t = (e) => (e.innerText || '').trim()
      const sections = [...document.querySelectorAll('[data-input-provenance],[data-ledger-class],details')].map((e) => ({ tag: e.tagName, attrs: [...e.attributes].filter((a) => a.name.startsWith('data-')).map((a) => a.name + '=' + a.value).slice(0, 4), head: t(e).slice(0, 160) }))
      const body = document.body.innerText || ''
      const lines = body.split('\n').map((s) => s.trim()).filter(Boolean)
      const hit = lines.filter((l) => /where (this page|each input)|data comes from|came from|inputs? (the|this)|thesis used|filings? (row|read|pulled)|last run|ran on|Refreshing an input|inputs have run|worked|source:?\s/i.test(l)).slice(0, 80)
      return { sections: sections.slice(0, 60), matching_lines: hit }
    })
    const thesisPlaces = await places('thesis')
    save('fwd12/BA_places_thesis_tab.json', thesisPlaces)
    save('fwd12/BA_thesis_tab_fulltext.txt', await bodyText())
    if (top.provenance) {
      await page.locator('[data-input-provenance]').first().scrollIntoViewIfNeeded().catch(() => {})
      await capture('fwd12-BA-input-provenance-block', { provenance: top.provenance }, true)
    } else {
      await capture('fwd12-BA-no-input-provenance-block', {}, true)
    }
    const tabNames = ['EXEC MANAGEMENT', 'PEERS', 'MODEL', 'POSTURE']
    for (const tn of tabNames) {
      const ok = await clickTab(new RegExp('^' + tn.replace(' ', '\\s+') + '$', 'i'))
      const short = tn.replace(/\s+/g, '_')
      if (ok) {
        save(`fwd12/BA_places_${short}.json`, await places(short))
        save(`fwd12/BA_${short}_fulltext.txt`, await bodyText())
        if (tn === 'MODEL') {
          const ld = page.locator('[data-ledger-class]').first()
          if (await ld.count()) await ld.scrollIntoViewIfNeeded().catch(() => {})
          const led = await page.evaluate(() => ({ ledger: [...document.querySelectorAll('[data-ledger-class]')].map((li) => ({ cls: li.getAttribute('data-ledger-class'), text: (li.innerText || '').trim() })) }))
          save('fwd12/BA_model_ledger.json', led)
          await capture('fwd12-BA-model-tab-ledger', { ledger: led.ledger }, true)
        }
      } else save(`fwd12/BA_places_${short}.json`, { tab_not_found: true })
    }
    // BA coverage: no such statement drawn (scan all five tabs' dumps afterwards; the page-wide regex here)
    await page.evaluate(() => window.scrollTo(0, 0))
  } catch (e) { log('BA ERROR', String(e.message).split('\n')[0]); rec({ label: 'name-error-BA', error: String(e.message).split('\n')[0] }) }

  const COVERAGE_RX = /not covered|outside (our |the )?coverage|coverage|not (in|on) (the|our) (covered|research)|isn'?t covered|no research|not tracked|no articles collected|nothing (has been )?(read|collected)|not collected|no (news|filing|analysis|thesis)/i
  const scanLines = (txt) => txt.split('\n').map((s) => s.trim()).filter(Boolean).filter((l) => COVERAGE_RX.test(l))

  // ---------- COVERAGE + OFFICERS + FWD-1 per name ----------
  const names = [
    { key: 'AMD_US_Equity', short: 'AMD', acts: ['fwd1'] },
    { key: 'MSFT_US_Equity', short: 'MSFT', acts: ['coverage'] },
    { key: 'BA_US_Equity', short: 'BA', acts: ['officers', 'coverage-ba'] },
    { key: 'HD_US_Equity', short: 'HD', acts: ['officers'] },
    { key: 'BP/_LN_Equity', short: 'BP', acts: ['officers'] },
  ]
  for (const nm of names) {
    const { key, short, acts } = nm
    try {
      setStep('name ' + short)
      await openName(key)
      await page.evaluate(() => window.scrollTo(0, 0))
      const h1 = await page.evaluate(() => ((document.querySelector('h1') || {}).textContent || '').trim())
      const top = await page.evaluate(() => {
        const t = (e) => (e ? (e.innerText || '').trim() : null)
        const tb = document.querySelector('[data-top-band]')
        const ip = document.querySelector('[data-input-provenance]')
        return { company_line: t(document.querySelector('[data-top-band-description]')), top_band: tb ? t(tb) : null, provenance: ip ? [...ip.querySelectorAll('[data-provenance-row]')].map((li) => t(li)) : null }
      })
      await overlayRead(key, short)
      const topText = await bodyText()
      save(`misc/${short}_thesis_tab_fulltext.txt`, topText)
      await capture(`name-${short}-top-of-page`, { h1, top }, true)

      if (acts.includes('fwd1')) {
        const dom = await page.evaluate(() => {
          const sb = document.querySelector('[data-segment-breakdown]')
          return sb ? { state: sb.getAttribute('data-segment-state'), header: (sb.querySelector('h4') || {}).textContent || null, headings: [...sb.querySelectorAll('[data-segment-heading]')].map((h) => h.textContent), reasons: [...sb.querySelectorAll('[data-segment-reason]')].map((h) => h.textContent), rows: sb.querySelectorAll('[data-segment-row]').length, text: sb.innerText.slice(0, 3000) } : null
        })
        save(`fwd1/${short}_segments_dom.json`, dom || { absent: true })
        const sbLoc = page.locator('[data-segment-breakdown]').first()
        if (await sbLoc.count()) await sbLoc.scrollIntoViewIfNeeded().catch(() => {})
        await capture(`fwd1-${short}-segment-breakdown`, { dom_segments: dom && { state: dom.state, header: dom.header, headings: dom.headings, rows: dom.rows } }, true)
        const about = page.locator('summary', { hasText: /About the company/i }).first()
        if (await about.count()) {
          await about.scrollIntoViewIfNeeded().catch(() => {})
          await about.click({ timeout: 4000 }).catch(() => {})
          await page.waitForTimeout(600)
          const at = await page.evaluate(() => { const d = [...document.querySelectorAll('details')].find((x) => /About the company/i.test((x.querySelector('summary') || {}).textContent || '')); return d ? { open: d.open, text: d.innerText.slice(0, 1500) } : null })
          save(`fwd1/${short}_about.json`, at)
          await capture(`fwd1-${short}-about-open`, { about: at && { open: at.open, len: at.text.length } }, true)
        } else save(`fwd1/${short}_about.json`, { absent: true })
        if (await clickTab(/^model$/i)) {
          const mod = await page.evaluate(() => ({ text_head: (document.body.innerText || '').slice(0, 2500), tables: [...document.querySelectorAll('table')].map((t) => ({ head: [...t.querySelectorAll('thead th, tr:first-child th')].map((h) => (h.textContent || '').trim()).slice(0, 12), rows: t.querySelectorAll('tbody tr').length })) }))
          save(`fwd1/${short}_model_tab.json`, mod)
          await page.evaluate(() => window.scrollTo(0, 0))
          await capture(`fwd1-${short}-model-tab`, { tables: mod.tables }, true)
        }
      }

      if (acts.includes('coverage') || acts.includes('coverage-ba')) {
        const dumps = { thesis: topText }
        for (const tn of TABS.slice(1)) {
          if (await clickTab(new RegExp('^' + tn.replace(' ', '\\s+') + '$', 'i'))) dumps[tn] = await bodyText()
        }
        const hits = Object.fromEntries(Object.entries(dumps).map(([k, v]) => [k, scanLines(v)]))
        save(`coverage/${short}_scan.json`, { key, regex: String(COVERAGE_RX), hits, chars_per_tab: Object.fromEntries(Object.entries(dumps).map(([k, v]) => [k, v.length])) })
        for (const [k, v] of Object.entries(dumps)) save(`coverage/${short}_${k.replace(/\s+/g, '_')}_fulltext.txt`, v)
        // the news timeline panel / overlay empty-month text on the default tab
        await clickTab(/^thesis$/i)
        await page.evaluate(() => window.scrollTo(0, 0))
        await capture(`coverage-${short}-thesis-tab-full-page`, { hit_counts: Object.fromEntries(Object.entries(hits).map(([k, v]) => [k, v.length])) }, false)
      }

      if (acts.includes('officers')) {
        const ok = await clickTab(/^exec\s+management$/i)
        const off = await page.evaluate(() => {
          const t = (e) => (e ? (e.innerText || '').trim() : null)
          const st = document.querySelector('[data-exec-status]')
          const rows = [...document.querySelectorAll('tr[data-exec-officer]')]
          return {
            status: st ? st.getAttribute('data-exec-status') : null,
            absent_because: st ? st.getAttribute('data-exec-absent-because') : null,
            caption: t(document.querySelector('[data-management-as-of]')),
            roster_source_note: t(document.querySelector('[data-exec-roster-source]')),
            empty_message: st && st.getAttribute('data-exec-status') !== 'SERVED' ? t(st) : null,
            row_count: rows.length,
            headers: [...document.querySelectorAll('tr[data-exec-officer]')].length ? [...(rows[0].closest('table')?.querySelectorAll('thead th') || [])].map((h) => (h.textContent || '').trim()) : null,
            first_three: rows.slice(0, 3).map((r) => ({ name: r.getAttribute('data-exec-officer'), cells: [...r.children].map((c) => (c.textContent || '').trim()) })),
            all_roles_in_order: rows.map((r) => ({ name: r.getAttribute('data-exec-officer'), role: (r.children[1]?.textContent || '').trim() })),
          }
        })
        save(`officers/${short}_exec_management.json`, { key, exec_tab_found: ok, ...off })
        log('OFFICERS', short, JSON.stringify({ status: off.status, rows: off.row_count, first: off.first_three.map((x) => x.name + ' / ' + (x.cells[1] || '')) }))
        await page.evaluate(() => window.scrollTo(0, 0))
        const tbl = page.locator('tr[data-exec-officer]').first()
        if (await tbl.count()) await tbl.scrollIntoViewIfNeeded().catch(() => {})
        await capture(`officers-${short}-exec-management`, { exec: { status: off.status, rows: off.row_count, first_three: off.first_three } }, true)
      }
    } catch (e) { log('NAME ERROR', short, String(e.message).split('\n')[0]); rec({ label: 'name-error-' + short, error: String(e.message).split('\n')[0] }) }
  }

  save('blocked_third_party.json', blocked)
  log('BB19 OUT', OUT)
}
