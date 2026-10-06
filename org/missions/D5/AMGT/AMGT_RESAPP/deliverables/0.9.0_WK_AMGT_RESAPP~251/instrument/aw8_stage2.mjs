// stage 2: the aw-8 walk. GET only. Every capture records the route and the tab labels as the positive control.
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'

const TABS = ['Thesis', 'Exec Management', 'Peers', 'Model', 'Posture']
const sha = (t) => crypto.createHash('sha256').update(t).digest('hex').slice(0, 16)
const safe = (k) => encodeURIComponent(k).replace(/\*/g, '%2A')

export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, shot, waitForLoaded, clickLabel } = ctx
  const dir = path.join(OUT, 'data')
  for (const d of ['thesis', 'fwd1', 'print', 'fwd31', 'fwd18']) mkdirSync(path.join(dir, d), { recursive: true })
  const captures = []
  const rec = (o) => { captures.push(o); writeFileSync(path.join(dir, 'captures.json'), JSON.stringify(captures, null, 1)) }
  const get = (url) => page.evaluate(async (u) => {
    const t = localStorage.getItem('accessToken')
    const t0 = Date.now()
    try {
      const r = await fetch(u, { headers: t ? { Authorization: `Bearer ${t}` } : {} })
      return { status: r.status, ms: Date.now() - t0, body: await r.text() }
    } catch (e) { return { status: 'fetch failed ' + String(e).slice(0, 80), ms: Date.now() - t0, body: null } }
  }, url)
  // the positive control read from the page itself: the route and the tab labels
  const control = () => page.evaluate(() => ({
    pathname: location.pathname,
    tab_labels: [...document.querySelectorAll('button,[role=tab],a')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && ['THESIS','EXEC MANAGEMENT','PEERS','MODEL','POSTURE'].includes((e.textContent || '').trim().toUpperCase()) }).map((e) => (e.textContent || '').trim()),
    page_title_text: ((document.querySelector('h1') || {}).textContent || '').trim(),
  })).catch(() => ({ pathname: null, tab_labels: [] }))
  const capture = async (label, extra = {}) => {
    const file = await shot(page, label)
    const c = await control()
    rec({ label, file, at: new Date().toISOString(), ...c, ...extra })
    log('CAPTURE', label, file, JSON.stringify(c.pathname), c.tab_labels.length, 'tab labels')
    return file
  }
  const openName = async (key, tab) => {
    await page.goto(opt.base + '/security-analysis/' + encodeURIComponent(key), { waitUntil: 'domcontentloaded', timeout: 30000 })
    await settle(page, 2500)
    await waitForLoaded(page)
    if (tab) {
      const ok = await clickLabel(page, tab)
      await page.waitForTimeout(500)
      const w = await waitForLoaded(page)
      return { tab_clicked: ok, state: w.state, waited_ms: w.waited_ms }
    }
    return { state: 'loaded' }
  }

  // ---------- data: /freshness + every covered /thesis (the census and the 12 names are read from these) ----------
  setStep('stage2 data')
  await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await settle(page, 3000)
  const f = await get('/api/scoped/amgt/freshness')
  log('FRESHNESS', f.status, f.ms, 'ms', (f.body || '').length, 'bytes')
  writeFileSync(path.join(dir, 'freshness.json'), f.body || '')
  const rows = JSON.parse(f.body).rows
  const covered = rows.filter((r) => r.covered && r.security_key)
  const keys = covered.map((r) => r.security_key)
  const theses = {}
  let qi = 0
  const worker = async () => {
    while (qi < keys.length) {
      const k = keys[qi++]
      const r = await get(`/api/scoped/amgt/security/${encodeURIComponent(k)}/thesis`)
      writeFileSync(path.join(dir, 'thesis', safe(k) + '.json'), r.body || '')
      let j = null
      try { j = JSON.parse(r.body) } catch { /* not json */ }
      theses[k] = { status: r.status, ms: r.ms, ok: !!(j && j.management), body: j }
    }
  }
  await Promise.all([worker(), worker(), worker(), worker()])
  log('THESIS PULL', Object.keys(theses).length, 'keys;', Object.values(theses).filter((t) => t.ok).length, 'with a body')

  // ---------- FWD-18: click a driver-chart figure through to its passage (BA, ASML_NA) ----------
  for (const key of ['BA_US_Equity', 'ASML_NA_Equity']) {
    try {
      setStep('fwd18 ' + key)
      const st = await openName(key, 'Thesis')
      await page.waitForTimeout(1500)
      const served = theses[key]?.body?.thesis_driver_chart || null
      const links = page.locator('[data-driver-chart-passage-link]')
      const n = await links.count().catch(() => 0)
      const chart = await page.locator('[data-driver-chart]').first().getAttribute('data-driver-chart').catch(() => null)
      await capture(`fwd18-${key}-thesis-before-click`, { key, tab_state: st, chart_state: chart, passage_links: n, served_status: served?.status, served_points: (served?.points || []).length })
      const clicks = []
      for (let i = 0; i < n; i++) {
        const l = links.nth(i)
        const text = ((await l.innerText().catch(() => '')) || '').trim()
        const pid = await l.getAttribute('data-driver-chart-passage-link').catch(() => null)
        await l.scrollIntoViewIfNeeded().catch(() => {})
        const pressed = await l.click({ timeout: 5000 }).then(() => true).catch(() => false)
        await page.waitForTimeout(600)
        let expanded = await l.getAttribute('aria-expanded').catch(() => null)
        let reclicked = false
        if (expanded === 'false') { await l.click({ timeout: 5000 }).catch(() => {}); await page.waitForTimeout(600); expanded = await l.getAttribute('aria-expanded').catch(() => null); reclicked = true }
        const quote = await l.locator('xpath=following-sibling::blockquote').first().innerText().catch(() => null)
        const sp = (served?.points || []).find((p) => p.passage_id === pid) || null
        const norm = (t) => String(t || '').replace(/\s+/g, ' ').trim()
        const rec1 = { i, link_text: text, passage_id: pid, pressed, reclicked_because_shared_passage_toggled_shut: reclicked, aria_expanded: expanded, passage_text_shown: quote === null ? null : norm(quote).slice(0, 400),
          passage_shown_chars: quote === null ? 0 : norm(quote).length, says_not_shown: /not shown on this page/.test(quote || ''),
          served_passage_text_chars: sp ? norm(sp.passage_text).length : null, served_cite_location: sp?.passage_cite?.location || null,
          shown_equals_served: sp && quote !== null ? norm(quote) === norm(sp.passage_text) : null,
          shown_contains_served_start: sp && quote !== null ? norm(quote).includes(norm(sp.passage_text).slice(0, 40)) : null }
        clicks.push(rec1)
        await capture(`fwd18-${key}-point${i + 1}-opened`, { key, ...rec1 })
      }
      writeFileSync(path.join(dir, 'fwd18', safe(key) + '.json'), JSON.stringify({ key, chart, served_chart_status: served?.status, served_reason: served?.reason, served_points: (served?.points || []).map((p) => ({ period: p.period, value: p.value, passage_id: p.passage_id })), clicks }, null, 1))
    } catch (e) { log('FWD18 ERROR', key, String(e.message).split('\n')[0]); rec({ label: 'fwd18-error-' + key, error: String(e.message).split('\n')[0] }) }
  }

  // ---------- FWD-31: Exec Management, passage beside the roster; with / without the passage ----------
  const readExec = () => page.evaluate(() => {
    const q = (s) => document.querySelector(s)
    const pass = q('[data-dossier-management]')
    const officers = [...document.querySelectorAll('tr[data-exec-officer]')]
    const pb = pass ? pass.getBoundingClientRect() : null
    const ob = officers[0] ? officers[0].getBoundingClientRect() : null
    const panel = q('[data-tab-panel="exec_management"]')
    return {
      passage_state: pass ? pass.getAttribute('data-dossier-management') : null,
      passage_heading: pass ? ((pass.querySelector('h4') || {}).textContent || null) : null,
      passage_text_chars: pass ? (pass.textContent || '').length : null,
      passage_source_line: pass ? ([...pass.querySelectorAll('p')].map((p) => p.textContent).filter((t) => /^Source:/.test(t || ''))[0] || null) : null,
      passage_sentence_when_absent: pass && pass.tagName === 'P' ? pass.textContent : null,
      passage_report_key: pass ? pass.getAttribute('data-dossier-report-key') : null,
      passage_locator: pass ? pass.getAttribute('data-dossier-locator') : null,
      passage_box: pb ? [Math.round(pb.x), Math.round(pb.y), Math.round(pb.width), Math.round(pb.height)] : null,
      first_officer_box: ob ? [Math.round(ob.x), Math.round(ob.y), Math.round(ob.width), Math.round(ob.height)] : null,
      passage_above_roster: pb && ob ? pb.bottom <= ob.top + 1 : null,
      officer_rows: officers.length,
      roster_html: officers.map((o) => o.outerHTML),
      exec_status: (q('[data-exec-status]') || { getAttribute: () => null }).getAttribute('data-exec-status'),
      roster_source: (q('[data-exec-roster-source]') || { getAttribute: () => null }).getAttribute('data-exec-roster-source'),
      panel_text_chars: panel ? (panel.textContent || '').length : null,
    }
  })
  const fwd31 = {}
  const trySlot = async (key, tag) => {
    setStep(`fwd31 ${key} ${tag}`)
    const st = await openName(key, 'Exec Management')
    await page.waitForTimeout(1500)
    const d = await readExec()
    const html = d.roster_html
    const out = { ...d, roster_html: undefined, roster_rows_sha: html.map(sha), roster_all_sha: sha(html.join('\n')), tab_state: st }
    await capture(`fwd31-${key}-exec-${tag}`, { key, tag, ...out })
    return { ...out, _html: html }
  }
  const census = []
  for (const k of keys) {
    const t = theses[k]
    if (!t?.ok) continue
    const df = t.body.dossier_fields?.management
    const mg = t.body.management || {}
    if (df?.status === 'SERVED' && !(mg.officers || []).length) census.push(k)
  }
  const exerciseKeys = ['BABA_US_Equity', 'SAP_GY_Equity', 'BA_US_Equity']
  const censusPick = census.filter((k) => ((theses[k].body.dossier_fields.management.value || '').length) > 200)[0] || census[0]
  if (censusPick) exerciseKeys.push(censusPick)
  for (const key of exerciseKeys) {
    try {
      const withP = await trySlot(key, 'with-passage')
      fwd31[key] = { with: withP }
      if (['BABA_US_Equity', 'SAP_GY_Equity'].includes(key)) {
        // the without arm: the SAME live /thesis answer with dossier_fields.management removed, in this browser only (a local response edit, not a write)
        const re = new RegExp('/api/scoped/amgt/security/' + key + '/thesis')
        await page.route(re, async (route) => {
          const resp = await route.fetch()
          const j = await resp.json()
          if (j.dossier_fields) delete j.dossier_fields.management
          await route.fulfill({ response: resp, json: j })
        })
        const without = await trySlot(key, 'without-passage-local-control')
        await page.unroute(re)
        fwd31[key].without = without
        const a = withP._html, b = without._html
        fwd31[key].compare = { rows_with: a.length, rows_without: b.length, rows_equal: a.filter((x, i) => b[i] === x).length, all_equal: a.join('\n') === b.join('\n') }
        log('FWD31 BYTE ARM', key, JSON.stringify(fwd31[key].compare))
      }
    } catch (e) { log('FWD31 ERROR', key, String(e.message).split('\n')[0]); rec({ label: 'fwd31-error-' + key, error: String(e.message).split('\n')[0] }) }
  }
  writeFileSync(path.join(dir, 'fwd31', 'fwd31.json'), JSON.stringify({ census_pick: censusPick, census_n: census.length, results: Object.fromEntries(Object.entries(fwd31).map(([k, v]) => [k, { with: { ...v.with, _html: undefined }, without: v.without ? { ...v.without, _html: undefined } : null, compare: v.compare || null }])) }, null, 1))

  // ---------- FWD-1: the 12 names that serve segments, read on the page ----------
  const segNames = keys.filter((k) => (theses[k]?.body?.segment_breakdown?.rows || []).length > 0)
  log('FWD1 names serving segments:', segNames.length, segNames.join(','))
  const fwd1 = []
  for (const key of segNames) {
    try {
      setStep('fwd1 ' + key)
      const sb = theses[key].body.segment_breakdown
      const labels = [...new Set(sb.rows.map((r) => r.segment))]
      const texts = sb.rows.map((r) => r.text)
      await openName(key, null)
      const per = {}
      for (const tab of TABS) {
        const ok = await clickLabel(page, tab)
        await page.waitForTimeout(500)
        const w = await waitForLoaded(page)
        await page.waitForTimeout(800)
        const txt = await page.evaluate(() => document.body.innerText).catch(() => '')
        writeFileSync(path.join(dir, 'fwd1', `${safe(key)}.${tab.replace(/\s+/g, '_')}.txt`), txt)
        const low = txt.toLowerCase()
        per[tab] = {
          tab_clicked: ok, state: w.state, text_chars: txt.length,
          segment_labels_on_page: labels.filter((l) => low.includes(l.toLowerCase())).length,
          segment_sentences_on_page: texts.filter((t) => low.includes(t.toLowerCase().slice(0, 50))).length,
          word_segment_on_page: /segment/i.test(txt),
        }
        await capture(`fwd1-${key}-${tab.replace(/\s+/g, '-')}`, { key, tab, ...per[tab] })
      }
      fwd1.push({ key, served_segment_rows: sb.rows.length, served_labels: labels, served_source: sb.source, per })
    } catch (e) { log('FWD1 ERROR', key, String(e.message).split('\n')[0]); fwd1.push({ key, error: String(e.message).split('\n')[0] }) }
  }
  writeFileSync(path.join(dir, 'fwd1', 'fwd1.json'), JSON.stringify(fwd1, null, 1))

  // ---------- FWD-5: the Print action on three covered names; the page's own GET answer is kept ----------
  for (const key of ['BA_US_Equity', 'ASML_NA_Equity', 'BABA_US_Equity']) {
    try {
      setStep('fwd5 ' + key)
      await openName(key, null)
      const btn = page.getByRole('button', { name: 'Print', exact: true }).first()
      const respP = page.waitForResponse((r) => /\/security\/[^/]+\/print(\?|$)/.test(r.url()) && r.request().method() === 'GET', { timeout: 120000 })
      await btn.click({ timeout: 8000 })
      const resp = await respP
      const body = await resp.body()
      writeFileSync(path.join(dir, 'print', safe(key) + '.pdf'), body)
      await page.waitForTimeout(2000)
      await capture(`fwd5-${key}-print-modal`, { key, print_status: resp.status(), print_bytes: body.length, content_type: resp.headers()['content-type'] || null })
      await page.keyboard.press('Escape').catch(() => {})
      await page.waitForTimeout(400)
      const closeBtn = page.getByRole('button', { name: /close/i }).first()
      if (await page.locator('iframe[title="Security print pack"]').count().catch(() => 0)) await closeBtn.click({ timeout: 2000 }).catch(() => {})
    } catch (e) { log('FWD5 ERROR', key, String(e.message).split('\n')[0]); rec({ label: 'fwd5-error-' + key, error: String(e.message).split('\n')[0] }) }
  }

  // ---------- FWD-7: the /freshness page on the dev build ----------
  try {
    setStep('fwd7')
    await page.goto(opt.base + '/freshness', { waitUntil: 'domcontentloaded', timeout: 30000 })
    const t0 = Date.now()
    const got = await page.locator('[data-slot="freshness-table"] tbody tr').first().waitFor({ timeout: 90000 }).then(() => true).catch(() => false)
    const waited = Date.now() - t0
    await settle(page, 1500)
    const read = () => page.evaluate(() => {
      const trs = [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')]
      const lines = trs.map((tr) => ({ name: tr.children[0]?.textContent, last: tr.children[1]?.textContent, stale: tr.getAttribute('data-stale'), flags: [...tr.querySelectorAll('[data-stale-input]')].map((l) => l.textContent) }))
      return { summary: (document.querySelector('[data-slot="freshness-summary"]') || {}).textContent || null, rows: lines.length, stale_rows: lines.filter((l) => l.stale === 'true').length,
        first_five: lines.slice(0, 5), headers: [...document.querySelectorAll('[data-slot="freshness-table"] thead th')].map((t) => t.textContent),
        sort_buttons: [...document.querySelectorAll('[aria-label="Sort by"] button')].map((b) => ({ label: b.textContent, pressed: b.getAttribute('aria-pressed') })),
        all_stale: lines.filter((l) => l.stale === 'true').map((l) => ({ name: l.name, last: l.last, flags: l.flags })) }
    })
    const first = await read()
    await capture('fwd7-freshness-default', { table_appeared: got, waited_ms: waited, ...first, all_stale: undefined })
    writeFileSync(path.join(dir, 'fwd7.json'), JSON.stringify({ waited_ms: waited, first }, null, 1))
    const btns = page.locator('[aria-label="Sort by"] button')
    const nb = await btns.count()
    for (let i = 0; i < nb; i++) {
      const lab = ((await btns.nth(i).innerText()) || '').trim()
      await btns.nth(i).click({ timeout: 4000 }).catch(() => {})
      await page.waitForTimeout(600)
      const r = await read()
      await capture(`fwd7-freshness-sort-${lab}`, { sort: lab, summary: r.summary, first_five: r.first_five })
    }
  } catch (e) { log('FWD7 ERROR', String(e.message).split('\n')[0]); rec({ label: 'fwd7-error', error: String(e.message).split('\n')[0] }) }
  log('STAGE2 OUT', OUT)
}
