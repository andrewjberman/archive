// dd-3 (round 80): FWD-7 (first visit first) and FWD-1 (AMD). Derived from round 79 cc8_walk.mjs; GET only.
// dd-3 (round 80): FWD-7 (first visit first) and FWD-1 (AMD). Derived from round 79 cc8_walk.mjs; GET only.
// AX6_MODULE after sign-in. Third-party DOCUMENT requests are aborted (nothing leaves the device).
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const TABS = ['THESIS', 'EXEC MANAGEMENT', 'PEERS', 'MODEL', 'POSTURE']

export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, waitForLoaded, context } = ctx
  const dir = path.join(OUT, 'data')
  for (const d of ['fwd7', 'fwd18', 'fwd1', 'sections', 'api']) mkdirSync(path.join(dir, d), { recursive: true })
  mkdirSync(path.join(OUT, 'shots'), { recursive: true })
  const captures = []
  let n = 0
  const rec = (o) => { captures.push(o); writeFileSync(path.join(dir, 'captures.json'), JSON.stringify(captures, null, 1)) }
  const control = () => page.evaluate((T) => ({
    pathname: location.pathname,
    tab_labels: [...document.querySelectorAll('button,[role=tab],a')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && T.includes((e.textContent || '').trim().toUpperCase()) }).map((e) => (e.textContent || '').trim()),
    h1: ((document.querySelector('h1') || {}).textContent || '').trim(),
    dialogs_open: document.querySelectorAll('[role=dialog],dialog[open]').length,
  }), TABS).catch(() => ({ pathname: null, tab_labels: [] }))
  const capture = async (label, extra = {}, viewport = true) => {
    n += 1
    const file = `shots/${String(n).padStart(3, '0')}-${label.replace(/[^a-z0-9]+/gi, '-').slice(0, 60)}.png`
    await page.screenshot({ path: path.join(OUT, file), fullPage: !viewport }).catch((e) => log('shot failed', e.message.split('\n')[0]))
    const c = await control()
    rec({ label, file, viewport, at: new Date().toISOString(), ...c, ...extra })
    log('CAPTURE', label, file, JSON.stringify(c.pathname), (c.tab_labels || []).length, 'tab labels', c.dialogs_open, 'dialogs')
    return file
  }
  const save = (rel, obj) => writeFileSync(path.join(dir, rel), typeof obj === 'string' ? obj : JSON.stringify(obj, null, 1))
  const bodyText = () => page.evaluate(() => document.body.innerText || '')
  const openName = async (key, waitMs = 6000) => {
    await page.goto(opt.base + '/security-analysis/' + encodeURIComponent(key), { waitUntil: 'domcontentloaded', timeout: 30000 })
    await settle(page, 2500)
    await waitForLoaded(page)
    await page.waitForSelector('[data-top-band],[data-input-provenance],[data-top-band-description]', { timeout: 20000 }).catch(() => {})
    await page.waitForTimeout(waitMs)
  }
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
  const SKIP = /^(host|connection|content-length|accept-encoding|cookie|origin|referer|user-agent|sec-|:)/i
  const apiGet = async (url) => {
    const sent = Object.fromEntries(Object.entries(lastScoped || {}).filter(([k]) => !SKIP.test(k)))
    const r = await page.evaluate(async ({ url, headers }) => {
      try { const x = await fetch(url, { method: 'GET', headers, cache: 'no-store' }); const t = await x.text(); let j = null; try { j = JSON.parse(t) } catch {} return { status: x.status, bytes: t.length, json: j } } catch (e) { return { status: 'fetch failed: ' + String(e).slice(0, 80), bytes: null, json: null } }
    }, { url, headers: sent })
    return { ...r, header_names_sent: Object.keys(sent).sort() }
  }
  const thesisRead = async (key) => {
    const a = await apiGet('/api/scoped/amgt/security/' + encodeURIComponent(key) + '/thesis')
    const j = a.json || {}
    const out = {
      key, status: a.status, bytes: a.bytes, header_names_sent: a.header_names_sent,
      segment_table: j.segment_table === undefined ? 'KEY ABSENT' : j.segment_table,
      dossier_sections: j.dossier_sections === undefined ? 'KEY ABSENT' : j.dossier_sections,
      thesis_driver_chart: j.thesis_driver_chart === undefined ? 'KEY ABSENT' : j.thesis_driver_chart,
      thesis_driver: j.thesis_driver === undefined ? 'KEY ABSENT' : j.thesis_driver,
      segment_breakdown_reason: j.segment_breakdown ? j.segment_breakdown.reason : undefined,
      top_level_keys: Object.keys(j),
    }
    save(`api/thesis_${key}.json`, out)
    return { out, full: j }
  }

  // ======================= FWD-7: the first page opened after the landing =======================
  const read7 = () => page.evaluate(() => {
    const trs = [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')]
    return {
      headers: [...document.querySelectorAll('[data-slot="freshness-table"] thead th')].map((t) => (t.textContent || '').trim()),
      rows: trs.map((tr, i) => ({ i, name: (tr.children[0]?.textContent || '').trim(), stale: tr.getAttribute('data-stale'), cells: [...tr.children].slice(1).map((c) => (c.textContent || '').trim()),
        inputs: [...tr.querySelectorAll('td[data-input]')].map((td) => ({ input: td.getAttribute('data-input'), state: td.getAttribute('data-state'), text: (td.textContent || '').trim() })),
        stale_words: [...tr.querySelectorAll('[data-stale-input]')].map((l) => l.textContent) })),
      summary: (document.querySelector('[data-slot="freshness-summary"]') || {}).textContent || null,
      page_end: (document.body.innerText || '').split('\n').slice(-3).join(' | '),
    }
  })
  let apiFresh = null
  let ten = []
  for (const pass of ['first', 'second']) {
    try {
      setStep('fwd7 ' + pass)
      const landed = page.url().replace(/^https?:\/\/[^/]+/, '')
      const t0 = Date.now()
      await page.goto(opt.base + '/freshness', { waitUntil: 'domcontentloaded', timeout: 30000 })
      const dcl = Date.now() - t0
      const got = await page.locator('[data-slot="freshness-table"] tbody tr').first().waitFor({ timeout: 90000 }).then(() => true).catch(() => false)
      const firstRow = Date.now() - t0
      await settle(page, 1500)
      const r = await read7()
      save(`fwd7/dom_${pass}.json`, { pass, landed_before_visit: landed, table_appeared: got, domcontentloaded_ms: dcl, first_row_ms_from_navigation: firstRow, stale_rows: r.rows.filter((x) => x.stale === 'true').length, ...r })
      log('FWD7', pass, 'first row', firstRow, 'ms;', r.rows.length, 'rows;', r.rows.filter((x) => x.stale === 'true').length, 'stale')
      await capture(`fwd7-freshness-${pass}-top`, { first_row_ms_from_navigation: firstRow, rows: r.rows.length, stale_rows: r.rows.filter((x) => x.stale === 'true').length, summary: r.summary })
      if (pass === 'first') {
        const a = await apiGet('/api/scoped/amgt/freshness?view=page')
        apiFresh = a.json
        save('api/freshness_rows.json', { status: a.status, bytes: a.bytes, rows: (a.json.rows || []).map((x) => ({ name: x.name, security_key: x.security_key, covered: x.covered, seeking_alpha: x.seeking_alpha, stale: x.stale, stale_inputs: x.stale_inputs, keyed_date: x.keyed_date })) })
        const rows = (a.json.rows || []).filter((x) => x.covered)
        const byName = (rx) => rows.find((x) => rx.test(x.name) || rx.test(x.security_key || ''))
        const pick = []
        const add = (x) => { if (x && !pick.includes(x)) pick.push(x) }
        add(byName(/^Boeing|^BA_US_Equity/i)); add(byName(/Alibaba|BABA/i)); add(byName(/Costco|COST_US/i))
        const st = (s) => rows.filter((x) => x.seeking_alpha && x.seeking_alpha.state === s)
        const nr = st('no_record'); const ck = st('checked'); const rd = st('read')
        add(nr[0]); add(nr[Math.floor(nr.length / 2)]); add(nr[nr.length - 1])
        add(ck[0]); add(ck[ck.length - 1]); add(rd.find((x) => !pick.includes(x))); add(rows.find((x) => x.stale))
        for (const x of [...ck, ...rd, ...nr]) { if (pick.length >= 10) break; add(x) }
        ten = pick.slice(0, 10)
        // the ten as the PAGE draws them, beside the API client's state and sentence
        const lines = ten.map((x) => {
          const d = r.rows.find((y) => y.name === x.name)
          return { name: x.name, security_key: x.security_key, page_row_found: !!d, page_sa_cell: d ? (d.inputs.find((i) => /seeking/i.test(i.input)) || {}).text : null, page_sa_state_attr: d ? (d.inputs.find((i) => /seeking/i.test(i.input)) || {}).state : null,
            page_row_cells: d ? d.cells : null, page_stale_attr: d ? d.stale : null, page_stale_words: d ? d.stale_words : null,
            api_state: x.seeking_alpha && x.seeking_alpha.state, api_sentence: x.seeking_alpha && x.seeking_alpha.sentence, api_last_read: x.seeking_alpha && x.seeking_alpha.last_read, api_stale: x.stale }
        })
        const body = await bodyText()
        for (const l of lines) l.page_draws_api_sentence = l.api_sentence ? body.includes(l.api_sentence) : null
        save('fwd7/ten_rows.json', lines)
        log('FWD7 TEN', JSON.stringify(lines.map((l) => [l.name, l.page_sa_cell, l.api_state])))
        for (const l of lines) {
          const loc = page.locator('[data-slot="freshness-table"] tbody tr', { hasText: l.name }).first()
          if (await loc.count()) {
            await loc.evaluate((el) => el.scrollIntoView({ block: 'center' }))
            await page.waitForTimeout(250)
          }
          await capture('fwd7-row-' + l.name, { name: l.name, page_sa_cell: l.page_sa_cell, api_state: l.api_state })
        }
      }
    } catch (e) { log('FWD7 ERROR', pass, String(e.message).split('\n')[0]); rec({ label: 'fwd7-error-' + pass, error: String(e.message).split('\n')[0] }) }
  }

  // ======================= FWD-1 on AMD =======================
  try {
    setStep('AMD')
    await openName('AMD_US_Equity', 7000)
    const T = await thesisRead('AMD_US_Equity')
    const st = T.out.segment_table
    const seg = {
      status: st && st.status, row_count: st && Array.isArray(st.rows) ? st.rows.length : null,
      first_row_name: st && st.rows && st.rows[0] ? st.rows[0].segment : null, first_row_first_value: st && st.rows && st.rows[0] ? st.rows[0].values[0] : null,
      rows_all: st && st.rows ? st.rows.map((r) => [r.segment, r.level, r.values && r.values[0]]) : null,
      periods_0_label: st && st.periods && st.periods[0] ? st.periods[0].label : null, currency: st && st.currency, units: st && st.units, period_note: st && st.period_note, reason: st && st.reason,
    }
    save('fwd1/AMD_segment_table_api.json', seg)
    const top = await page.evaluate(() => ({ h1: ((document.querySelector('h1') || {}).textContent || '').trim(), company_line: ((document.querySelector('[data-top-band-description]') || {}).innerText || '').trim(), head_text: (document.body.innerText || '').slice(0, 1800) }))
    save('fwd1/AMD_top.json', top)
    await page.evaluate(() => window.scrollTo(0, 0))
    await capture('fwd1-AMD-top-of-page', { h1: top.h1 })
    const dom = await page.evaluate(() => {
      const sb = document.querySelector('[data-segment-breakdown]')
      return sb ? { state: sb.getAttribute('data-segment-state'), header: (sb.querySelector('h4') || {}).textContent || null, headings: [...sb.querySelectorAll('[data-segment-heading]')].map((h) => h.textContent), reasons: [...sb.querySelectorAll('[data-segment-reason]')].map((h) => h.textContent), rows: sb.querySelectorAll('[data-segment-row]').length, tables: sb.querySelectorAll('table').length, table_dump: [...sb.querySelectorAll('table')].map((t) => ({ head: [...t.querySelectorAll('thead th, tr:first-child th')].map((h) => (h.textContent || '').trim()), rows: [...t.querySelectorAll('tbody tr')].map((r) => [...r.children].map((c) => (c.textContent || '').trim())) })), attrs: [...sb.querySelectorAll('*')].flatMap((e) => [...e.attributes].filter((a) => a.name.startsWith('data-segment')).map((a) => a.name + '=' + String(a.value).slice(0, 40))).slice(0, 40), text: sb.innerText.slice(0, 3000) } : null
    })
    save('fwd1/AMD_segments_dom.json', dom || { absent: true })
    const sbLoc = page.locator('[data-segment-breakdown]').first()
    if (await sbLoc.count()) await sbLoc.scrollIntoViewIfNeeded().catch(() => {})
    await capture('fwd1-AMD-segment-place', { dom_segments: dom && { state: dom.state, rows: dom.rows, tables: dom.tables }, api_segment_table: { status: seg.status, rows: seg.row_count } })
    const about = page.locator('summary', { hasText: /About the company/i }).first()
    if (await about.count()) {
      await about.scrollIntoViewIfNeeded().catch(() => {})
      await about.click({ timeout: 4000 }).catch(() => {})
      await page.waitForTimeout(600)
      const at = await page.evaluate(() => { const d = [...document.querySelectorAll('details')].find((x) => /About the company/i.test((x.querySelector('summary') || {}).textContent || '')); return d ? { open: d.open, text: d.innerText.slice(0, 1500) } : null })
      save('fwd1/AMD_about.json', at)
      await capture('fwd1-AMD-about-open', { about_len: at && at.text.length })
    } else save('fwd1/AMD_about.json', { absent: true })
    if (await clickTab(/^model$/i)) {
      const mod = await page.evaluate(() => ({ text_head: (document.body.innerText || '').slice(0, 2500), tables: [...document.querySelectorAll('table')].map((t) => ({ head: [...t.querySelectorAll('thead th, tr:first-child th')].map((h) => (h.textContent || '').trim()).slice(0, 12), rows: t.querySelectorAll('tbody tr').length, first_rows: [...t.querySelectorAll('tbody tr')].slice(0, 4).map((r) => [...r.children].map((c) => (c.textContent || '').trim()).slice(0, 6)) })) }))
      save('fwd1/AMD_model_tab.json', mod)
      await page.evaluate(() => window.scrollTo(0, 0))
      await capture('fwd1-AMD-model-tab', { tables: mod.tables.map((t) => t.rows) })
    }
  } catch (e) { log('AMD ERROR', String(e.message).split('\n')[0]); rec({ label: 'name-error-AMD', error: String(e.message).split('\n')[0] }) }
  save('blocked_third_party.json', blocked)
  log('DD3 OUT', OUT)
}
