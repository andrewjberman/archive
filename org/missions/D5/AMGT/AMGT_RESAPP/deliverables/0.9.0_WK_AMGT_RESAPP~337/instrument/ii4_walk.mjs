// ii-4 (round 84): FWD-18 on NU_US_Equity only. Derived from round 79 cc8_walk.mjs. GET only; walker guard unchanged.
// Extends round 78's bb19_walk.mjs. GET only; the walker's network guard is unchanged. Loaded by walk_ay6.mjs through
// AX6_MODULE after sign-in. Third-party DOCUMENT requests are aborted (nothing leaves the device).
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'

const TABS = ['THESIS', 'EXEC MANAGEMENT', 'PEERS', 'MODEL', 'POSTURE']

export async function run(ctx) {
  const { page, opt, OUT, log, settle, setStep, waitForLoaded, context } = ctx
  const dir = path.join(OUT, 'data')
  for (const d of ['fwd18', 'api']) mkdirSync(path.join(dir, d), { recursive: true })
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

  // ======================= FWD-18 on NU =======================
  try {
    setStep('NU')
    await openName('NU_US_Equity', 7000)
    const T = await thesisRead('NU_US_Equity')
    save('api/thesis_NU_US_Equity_full.json', T.full)
    // the company description as the page draws it (top band line, then the About disclosure)
    const top = await page.evaluate(() => ({ h1: ((document.querySelector('h1') || {}).textContent || '').trim(), company_line: ((document.querySelector('[data-top-band-description]') || {}).innerText || '').trim(), head_text: (document.body.innerText || '').slice(0, 2200) }))
    save('fwd18/NU_top.json', top)
    await page.evaluate(() => window.scrollTo(0, 0))
    await capture('fwd18-NU-top-of-page', { h1: top.h1 })
    const about = page.locator('summary', { hasText: /About the company/i }).first()
    if (await about.count()) {
      await about.scrollIntoViewIfNeeded().catch(() => {})
      await about.click({ timeout: 4000 }).catch(() => {})
      await page.waitForTimeout(700)
      const at = await page.evaluate(() => { const d = [...document.querySelectorAll('details')].find((x) => /About the company/i.test((x.querySelector('summary') || {}).textContent || '')); return d ? { open: d.open, text: d.innerText.slice(0, 2500) } : null })
      save('fwd18/NU_about.json', at)
      await capture('fwd18-NU-about-open', { about_len: at && at.text.length })
      await about.click({ timeout: 4000 }).catch(() => {})
    } else save('fwd18/NU_about.json', { absent: true })
    // where a driver chart would be
    const chartPlace = await page.evaluate(() => {
      const c = document.querySelector('[data-driver-chart]')
      return c ? { state: c.getAttribute('data-driver-chart'), text: (c.innerText || '').trim(), has_svg: !!c.querySelector('svg'), buttons: c.querySelectorAll('button').length } : null
    })
    save('fwd18/NU_chart_place.json', chartPlace)
    await page.locator('[data-driver-chart]').first().scrollIntoViewIfNeeded().catch(() => {})
    await page.waitForTimeout(500)
    await capture('fwd18-NU-driver-chart-place', { chart_place: chartPlace })
    // the segment panel beside it
    const seg = await page.evaluate(() => { const sb = document.querySelector('[data-segment-breakdown]'); return sb ? { state: sb.getAttribute('data-segment-state'), text: sb.innerText.slice(0, 2500), rows: sb.querySelectorAll('[data-segment-row]').length } : null })
    save('fwd18/NU_segments_dom.json', seg || { absent: true })

    const panelInv = async () => page.evaluate(() => {
      const root = document.querySelector('[data-tab-panel="thesis"]') || document.body
      const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 }
      return [...root.querySelectorAll('button,a,summary,[role=button],[tabindex="0"],[data-figure],[data-citation],[onclick]')].filter(vis).map((e) => ({ tag: e.tagName, text: (e.textContent || '').trim().slice(0, 140), attrs: [...e.attributes].filter((a) => a.name.startsWith('data-') || a.name.startsWith('aria-') || a.name === 'role').map((a) => a.name + '=' + String(a.value).slice(0, 50)).slice(0, 6) }))
    })
    save('fwd18/NU_thesis_panel_pressables.json', await panelInv())
    await page.evaluate(() => window.scrollTo(0, 0))
    await capture('fwd18-NU-thesis-panel', {})
    const cardWindows = {}
    let pressedOne = false
    for (const cid of ['investment_thesis', 'risks', 'recommendation']) {
      const card = page.locator(`[data-thesis-card="${cid}"]`).first()
      if (!(await card.count())) { cardWindows[cid] = { card: false }; continue }
      await card.scrollIntoViewIfNeeded().catch(() => {})
      await card.click({ timeout: 4000 }).catch(() => {})
      await page.waitForTimeout(1500)
      const w = await page.evaluate(() => {
        const dlg = document.querySelector('[role=dialog],dialog[open]')
        if (!dlg) return { dialog: false }
        const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 }
        return { dialog: true, text: (dlg.innerText || '').trim().slice(0, 9000),
          pressables: [...dlg.querySelectorAll('button,a,summary,[role=button],[tabindex="0"]')].filter(vis).map((e) => ({ tag: e.tagName, text: (e.textContent || '').trim().slice(0, 140), attrs: [...e.attributes].filter((a) => a.name.startsWith('data-') || a.name.startsWith('aria-')).map((a) => a.name + '=' + String(a.value).slice(0, 50)).slice(0, 5) })),
          passages: [...dlg.querySelectorAll('[data-thesis-passage]')].map((e) => ({ id: e.getAttribute('data-thesis-passage'), text: (e.innerText || '').trim().slice(0, 300) })) }
      })
      cardWindows[cid] = w
      await capture('fwd18-NU-card-' + cid + '-window', { card: cid, dialog: w.dialog, passages: (w.passages || []).length })
      if (w.dialog && !pressedOne) {
        // ONE figure press: a pressable element whose text carries a figure, else the first figure in a sentence of the window
        const snap = () => page.evaluate(() => { const dlg = document.querySelector('[role=dialog],dialog[open]'); return { url: location.pathname, dialogs: document.querySelectorAll('[role=dialog],dialog[open]').length, dialog_len: dlg ? (dlg.innerText || '').length : 0, passages: dlg ? dlg.querySelectorAll('[data-thesis-passage]').length : 0, popovers: document.querySelectorAll('[role=tooltip],[role=menu],[data-radix-popper-content-wrapper]').length, open_details: document.querySelectorAll('details[open]').length, expanded_true: document.querySelectorAll('[aria-expanded="true"]').length } })
        const target = await page.evaluate(() => {
          const dlg = document.querySelector('[role=dialog],dialog[open]')
          const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 }
          const FIGRX = /\d[\d,]*\.\d+|\d{1,3}(,\d{3})+|\d+(\.\d+)?%/
          const pres = [...dlg.querySelectorAll('button,a,[role=button],[tabindex="0"],[data-figure],[data-citation]')].filter(vis).find((e) => FIGRX.test(e.textContent || '') && !/close/i.test(e.textContent || ''))
          if (pres) { const r = pres.getBoundingClientRect(); return { kind: 'pressable', tag: pres.tagName, text: (pres.textContent || '').trim().slice(0, 140), cursor: getComputedStyle(pres).cursor, x: r.x + r.width / 2, y: r.y + r.height / 2 } }
          const ps = [...dlg.querySelectorAll('p')].filter((p) => !p.closest('[data-thesis-passage]') && FIGRX.test(p.textContent || ''))
          for (const p of ps) {
            const walker = document.createTreeWalker(p, NodeFilter.SHOW_TEXT); let node
            while ((node = walker.nextNode())) {
              const m = node.textContent.match(FIGRX)
              if (m) { const r = document.createRange(); r.setStart(node, m.index); r.setEnd(node, m.index + m[0].length); const b = r.getBoundingClientRect(); const h = node.parentElement
                return { kind: 'text-figure', figure: m[0], host_tag: h.tagName, host_is_interactive: !!h.closest('button,a,[role=button],summary,[tabindex]'), cursor: getComputedStyle(h).cursor, sentence: (p.textContent || '').trim().slice(0, 300), x: b.x + b.width / 2, y: b.y + b.height / 2 } }
            }
          }
          return null
        })
        if (target) {
          pressedOne = true
          const pagesBefore = context.pages().length
          const snapBefore = await snap()
          await capture('fwd18-NU-figure-before-press', { card: cid, target, snap: snapBefore })
          await page.mouse.click(target.x, target.y)
          await page.waitForTimeout(2500)
          const snapAfter = await snap()
          const dlgAfter = await page.evaluate(() => { const d = document.querySelector('[role=dialog],dialog[open]'); return d ? (d.innerText || '').slice(0, 3500) : null })
          save('fwd18/NU_figure_press.json', { card: cid, target, before: snapBefore, after: snapAfter, pages_before: pagesBefore, pages_after: context.pages().length, dialog_text_after: dlgAfter, dialog_text_before: w.text.slice(0, 3500) })
          log('NU FIGURE PRESS', JSON.stringify({ target, snapBefore, snapAfter }))
          await capture('fwd18-NU-figure-after-press', { card: cid, target, snap: snapAfter })
        } else { save('fwd18/NU_figure_press_' + cid + '.json', { card: cid, no_figure_found_in_window: true }); log('NU no figure in', cid) }
      }
      await page.keyboard.press('Escape').catch(() => {})
      await page.waitForTimeout(800)
    }
    save('fwd18/NU_card_windows.json', cardWindows)
    log('NU WINDOWS', JSON.stringify(Object.fromEntries(Object.entries(cardWindows).map(([k, v]) => [k, v.dialog ? { pressables: (v.pressables || []).length, passages: (v.passages || []).length } : v]))))
  } catch (e) { log('NU ERROR', String(e.message).split('\n')[0]); rec({ label: 'name-error-NU', error: String(e.message).split('\n')[0] }) }
  save('blocked_third_party.json', blocked)
  log('II4 OUT', OUT)
}
