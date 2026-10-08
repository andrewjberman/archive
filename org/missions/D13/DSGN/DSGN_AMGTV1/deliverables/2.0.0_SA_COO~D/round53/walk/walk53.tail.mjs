// ---- the walk (round 53) ----
// walk53.mjs = round35/walk/closewalk35.mjs's head (options, lease, login, request guard, page helpers; unchanged, lines above
// its "the walk" marker) + this tail. Built by round53/walk/build_walk53.py. The ONE REAL RUN of round 53: a local build of the
// round-53 candidate against the live function. Reads:
//   r53-segment <name>    SAUX-43: on the Thesis tab, ONE [data-segment-table]; a served table draws one head cell per served
//                         period label in order and one body row per served row in order, with its source line; a served reason
//                         draws that reason once and no table.
//   r53-sections <name>   SAUX-42: on the Thesis tab, ONE [data-dossier-sections] with the five served fields in order, each
//                         carrying its served state; a served section prints its text and holds one closed opener; an absent
//                         one prints its served reason.
//   r53-freshness         SAUX-41: on /freshness, every Seeking Alpha cell carries the served state and prints the served
//                         sentence; no cell prints "Not collected"; no checked or no-record row is flagged stale.
// Usage (repo root): node <this file> --names "AMD US,ASML NA,NU US" [--base http://localhost:5174]
function R53_PROBE() {
  const clean = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  const seg = [...document.querySelectorAll('[data-segment-table]')].map((e) => ({
    state: e.getAttribute('data-segment-table'),
    head: [...e.querySelectorAll('table[data-segment-table-revenue] thead th')].map((th) => clean(th.innerText)),
    rows: [...e.querySelectorAll('table[data-segment-table-revenue] tbody tr')].map((tr) => clean((tr.querySelector('td') || {}).innerText)),
    operating_rows: e.querySelectorAll('table[data-segment-table-operating] tbody tr').length,
    source: clean((e.querySelector('[data-segment-table-source]') || {}).innerText),
    text: clean(e.innerText).slice(0, 2000),
  }))
  const ds = [...document.querySelectorAll('[data-dossier-sections]')].map((e) => ({
    sections: [...e.querySelectorAll('[data-dossier-section]')].map((s) => ({
      field: s.getAttribute('data-dossier-section'),
      state: s.getAttribute('data-dossier-section-state'),
      openers: s.querySelectorAll('details[data-dossier-section-open]').length,
      open_now: s.querySelectorAll('details[data-dossier-section-open][open]').length,
      text: clean(s.innerText).slice(0, 4000),
    })),
  }))
  return { seg, ds }
}
function FRESH_PROBE() {
  const clean = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  return [...document.querySelectorAll('[data-slot="freshness-table"] tbody tr')].map((tr) => {
    const td = tr.querySelector('td[data-input="seekingalpha"]')
    return {
      name: clean((tr.querySelector('td') || {}).innerText),
      sa_state: td ? td.getAttribute('data-sa-state') : null,
      data_state: td ? td.getAttribute('data-state') : null,
      text: td ? clean(td.innerText) : null,
      sa_flagged: !!tr.querySelector('[data-stale-input="seekingalpha"]'),
    }
  })
}
const norm = (s) => String(s || '').replace(/\s+/g, ' ').trim()

const PLANNED = [...opt.names.flatMap((n) => [`r53-segment ${n}`, `r53-sections ${n}`]), 'r53-freshness']
let holder = null; let armed = false; let browser; let fatal = null
let freshBody = null
try {
  let armOut
  try { armOut = py('arm') } catch (e) {
    const so = e && e.stdout ? String(e.stdout) : ''
    holder = (so.match(/^HOLDER (\S+)/m) || [])[1] || null; armed = !!holder
    throw new Error(`arm failed: ${firstLine((e && e.stderr && String(e.stderr).trim()) || e)}`)
  }
  log(armOut.trim().split('\n').slice(-2).join(' | '))
  holder = (armOut.match(/^HOLDER (\S+)/m) || [])[1] || null; armed = true; armedAt = Date.now()
  const password = py('secret', { UI_WALK_CHILD: '1' })
  try { browser = await chromium.launch({ channel: 'msedge', headless: true }) } catch { browser = await chromium.launch({ headless: true }) }
  const page = await (await browser.newContext({ viewport: { width: 1440, height: 900 } })).newPage()
  page.setDefaultTimeout(30000)
  await page.route('**/*', (route) => {
    const req = route.request(); const m = req.method(); const p = new URL(req.url()).pathname
    if (m === 'GET' || m === 'HEAD' || m === 'OPTIONS' || ADMITTED_POST.some((re) => re.test(p))) return route.continue()
    if (/\/analytics\/ingest$/.test(p)) return route.fulfill({ status: 204, body: '' })
    return route.abort('blockedbyclient')
  })
  page.on('request', (r) => { if (/\/api\/scoped\//.test(r.url())) inflight.add(r) })
  page.on('requestfinished', (r) => inflight.delete(r))
  page.on('requestfailed', (r) => inflight.delete(r))
  page.on('response', async (resp) => {
    let u
    try { u = new URL(resp.url()) } catch { return }
    const p = u.pathname
    if (!/\/api\/scoped\/amgt\//.test(p) || resp.status() !== 200) return
    const body = await resp.json().catch(() => null); if (!body) return
    const data = unwrap(body)
    if (/\/freshness$/.test(p) && u.searchParams.get('view') === 'page') { freshBody = data; return }
    const k = p.match(/\/security\/([^/]+)\/([a-z-]+)$/)
    if (k) { const seg = decodeURIComponent(k[1]); (served.bySeg[seg] = served.bySeg[seg] || {})[k[2]] = data }
  })
  await page.goto(opt.base + '/login', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await page.fill('#email', EMAIL); await page.fill('#password', password.trim()); await page.click('button[type=submit]')
  await page.waitForURL((u) => !/\/login/.test(u.pathname), { timeout: 30000 }).catch(() => {})
  if (/\/login/.test(new URL(page.url()).pathname)) throw new Error('login did not complete')
  log('LOGGED IN')
  await page.goto(opt.base + '/security-analysis', { waitUntil: 'domcontentloaded', timeout: 30000 }); await settle(page, 3000)

  for (const name of opt.names) {
    let ov = null; let openErr = null; let seg = null; let view = null
    try {
      ov = await openName(page, name)
      seg = Object.keys(served.bySeg).find((k) => served.bySeg[k].overlay === ov) || null
      await waitFor(page, () => seg && served.bySeg[seg] && served.bySeg[seg].thesis, 30000).catch(() => {})
      await closeDialogs(page)
      await clickTab(page, 'Thesis')
      await waitTabReady(page, 'thesis')
      await settle(page, 2000)
      await page.screenshot({ path: png(`r53-${slug(name)}-thesis.png`), fullPage: true })
      view = await page.evaluate(R53_PROBE)
    } catch (e) { openErr = e }
    const thesis = seg && served.bySeg[seg] ? served.bySeg[seg].thesis : null
    const base = { name, security_key: seg }

    await read(`r53-segment ${name}`, async () => {
      if (openErr) throw openErr
      if (!thesis) throw new Error('no /thesis response was captured for this name')
      const st = thesis.segment_table
      if (!st) throw new Error('the live /thesis carries no segment_table')
      const f = []
      if (view.seg.length !== 1) f.push(`${view.seg.length} [data-segment-table] element(s) (1 wanted)`)
      const d = view.seg[0] || {}
      if (st.status === 'served') {
        const want = ['Segment', ...st.periods.map((p) => p.label)]
        if (JSON.stringify(d.head) !== JSON.stringify(want)) f.push(`head ${JSON.stringify(d.head)} (served ${JSON.stringify(want)})`)
        if (JSON.stringify(d.rows) !== JSON.stringify(st.rows.map((r) => norm(r.segment)))) f.push(`rows ${JSON.stringify(d.rows)} (served ${JSON.stringify(st.rows.map((r) => r.segment))})`)
        if ((st.operating_income_rows || []).length !== d.operating_rows) f.push(`${d.operating_rows} operating row(s) of ${(st.operating_income_rows || []).length}`)
        if (!d.source || !d.source.includes(st.source.label)) f.push(`source line "${d.source}"`)
      } else if (d.state !== 'none' || !norm(d.text).includes(norm(st.reason))) f.push(`a served reason is not drawn: state ${d.state}, text "${(d.text || '').slice(0, 120)}"`)
      return {
        verdict: f.length ? 'FAIL' : 'PASS',
        detail: f.length ? f.join(' | ') : (st.status === 'served' ? `${d.rows.length} rows x ${d.head.length - 1} columns as served, ${d.operating_rows} operating rows; "${d.source}"` : `the served reason is drawn: "${norm(st.reason)}"`),
        data: { ...base, served_status: st.status, drawn: d },
      }
    })
    await read(`r53-sections ${name}`, async () => {
      if (openErr) throw openErr
      if (!thesis) throw new Error('no /thesis response was captured for this name')
      const ds = thesis.dossier_sections
      if (!Array.isArray(ds)) throw new Error('the live /thesis carries no dossier_sections')
      const f = []
      if (view.ds.length !== 1) f.push(`${view.ds.length} [data-dossier-sections] element(s) (1 wanted)`)
      const got = (view.ds[0] || { sections: [] }).sections
      if (JSON.stringify(got.map((s) => s.field)) !== JSON.stringify(ds.map((e) => e.field))) f.push(`fields ${JSON.stringify(got.map((s) => s.field))}`)
      ds.forEach((e, i) => {
        const s = got[i]; if (!s) return
        if (s.state !== e.status) f.push(`${e.field}: state ${s.state} (served ${e.status})`)
        if (e.status === 'served') {
          if (s.openers !== 1 || s.open_now !== 0) f.push(`${e.field}: ${s.openers} opener(s), ${s.open_now} open`)
          if (!s.text.includes(norm(e.text).slice(0, 200))) f.push(`${e.field}: the served text is not on screen`)
        } else if (!s.text.includes(norm(e.reason))) f.push(`${e.field}: the served reason is not on screen`)
      })
      return {
        verdict: f.length ? 'FAIL' : 'PASS',
        detail: f.length ? f.join(' | ') : `5 of 5 in order (${ds.map((e) => `${e.field}:${e.status}`).join(', ')})`,
        data: { ...base, drawn: got.map((s) => ({ ...s, text: s.text.slice(0, 400) })) },
      }
    })
  }

  await page.goto(opt.base + '/freshness', { waitUntil: 'domcontentloaded', timeout: 30000 })
  await waitFor(page, () => !!freshBody, 60000).catch(() => {})
  await page.waitForSelector('[data-slot="freshness-table"] tbody tr', { timeout: 60000 }).catch(() => {})
  await settle(page, 2000)
  await page.screenshot({ path: png('r53-freshness.png'), fullPage: true })
  const cells = await page.evaluate(FRESH_PROBE)
  await read('r53-freshness', async () => {
    if (!freshBody) throw new Error('no /freshness?view=page response was captured')
    const rows = (freshBody.rows || []).filter((r) => r.covered === true)
    const byName = new Map(cells.map((c) => [c.name, c]))
    const f = []; const tally = {}
    for (const r of rows) {
      const sa = r.seeking_alpha || {}
      const c = byName.get(r.name || r.security_key || 'Unnamed company')
      if (!c) { f.push(`${r.name}: no row drawn`); continue }
      tally[c.sa_state] = (tally[c.sa_state] || 0) + 1
      if (c.sa_state !== sa.state) f.push(`${r.name}: data-sa-state ${c.sa_state} (served ${sa.state})`)
      if (c.text !== norm(sa.sentence)) f.push(`${r.name}: "${c.text}"`)
      if (sa.state !== 'read' && (c.sa_flagged || c.data_state === 'stale')) f.push(`${r.name}: ${sa.state} drawn stale`)
    }
    const nc = cells.filter((c) => /not collected/i.test(c.text || '')).length
    if (nc) f.push(`${nc} cell(s) print Not collected`)
    const examples = ['read', 'checked', 'no_record'].map((s) => { const r = rows.find((x) => (x.seeking_alpha || {}).state === s); return r ? `${r.name}: "${norm(r.seeking_alpha.sentence)}"` : `${s}: none served` })
    return {
      verdict: f.length ? 'FAIL' : 'PASS',
      detail: f.length ? `${f.length} fault(s): ` + f.slice(0, 5).join(' | ') : `${rows.length} of ${rows.length} rows carry the served state and sentence ${JSON.stringify(tally)}; 0 Not collected; e.g. ${examples.join(' // ')}`,
      data: { snapshot: freshBody.snapshot || null, drawn: cells, tally },
    }
  })
} catch (e) {
  fatal = firstLine(e)
  log(`FATAL: ${fatal}`)
} finally {
  if (browser) await browser.close().catch(() => {})
  if (armed) { try { log(py('disarm', {}, holder).trim().split('\n').slice(-3).join(' | ')) } catch (e) { log(`DISARM FAILED -- run: python .claude/skills/ui-walk/ui_walker_account.py disarm ${holder} :: ${firstLine(e)}`) } }
}
for (const id of PLANNED) if (!reads.some((r) => r.id === id)) record(id, 'ERROR', `cause: not reached${fatal ? ` (${fatal})` : ''}`, {})

console.log('')
for (const r of reads) console.log(`${r.verdict} ${r.id} :: ${r.evidence} :: ${r.detail}`)
const n = (v) => reads.filter((r) => r.verdict === v).length
console.log(`READS: ${reads.length} (PASS ${n('PASS')}, FAIL ${n('FAIL')}, ERROR ${n('ERROR')})${fatal ? `; FATAL ${fatal}` : ''}`)
fs.writeFileSync(path.join(OUT, 'walk53.json'), JSON.stringify({ base: opt.base, names: opt.names, fatal, reads }, null, 1))
console.log(`OUT ${OUT}`)
process.exit(n('ERROR') === 0 ? 0 : 1)
