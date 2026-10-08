// ---- the walk (round 51) ----
// walk51.mjs = round35/walk/closewalk35.mjs's head (options, lease, login, request guard, page helpers; unchanged, lines above
// its "the walk" marker) + this tail. Built by round51/walk/build_walk51.py. Reads, per name, on a local build of the round-51
// candidate against the live function:
//   r51-inputs <name>     SAUX-37: the block above the tabs draws one row per served /thesis input_provenance entry, in order; a
//                         landed filings row names its form and prints no raw ISO date; the Model tab draws no [data-input-ledger].
//   r51-coverage <name>   SAUX-39: the served research_coverage.sentence is drawn exactly once in one [data-research-coverage]
//                         element; a name with no served sentence draws none.
//   r51-officers <name>   SAUX-38: the Exec tab's [data-exec-officer] rows equal the served management.officers, name for name.
//   r51-phrases <name>    SAUX-40: the Thesis tab's [data-dossier-pillars] line does not say "research pack". The data lists every
//                         visible "research pack" / "research-team report" / "research team's report" line per tab and every
//                         served string in /thesis and /overlay that holds "research pack" (CTO msg 31695's two reads).
// Usage (repo root): node <this file> --no-officer "ROG SW" --names "BA US,AMD US,BP/ LN,MSFT US" [--base http://localhost:5174]
function R51_PROBE() {
  const clean = (s) => String(s || '').replace(/\s+/g, ' ').trim()
  const body = document.body.innerText || ''
  const lines = body.split('\n').map(clean).filter(Boolean)
  const pick = (re) => lines.filter((l) => re.test(l)).map((l) => l.slice(0, 260))
  const pillars = [...document.querySelectorAll('[data-dossier-pillars]')].map((e) => ({ state: e.getAttribute('data-dossier-pillars'), text: clean(e.innerText).slice(0, 300) }))
  const ledgerEls = [...document.querySelectorAll('[data-input-ledger]')]
  const tabPanel = document.querySelector('[data-tab-panel="model"]')
  return {
    provenance_rows: [...document.querySelectorAll('[data-provenance-row]')].map((e) => clean(e.innerText)),
    provenance_blocks: document.querySelectorAll('[data-input-provenance]').length,
    coverage: [...document.querySelectorAll('[data-research-coverage]')].map((e) => ({ status: e.getAttribute('data-research-coverage'), text: clean(e.innerText) })),
    officers: [...document.querySelectorAll('[data-exec-officer]')].map((e) => e.getAttribute('data-exec-officer')),
    input_ledgers: ledgerEls.length,
    research_pack_lines: pick(/research pack/i),
    research_team_report_lines: pick(/research-team report|research team's report/i),
    research_team_pack_lines: lines.filter((l) => /research team's (most recent )?packs?\b/i.test(l)),
    pillars,
    model_tab_tail: tabPanel ? clean(tabPanel.innerText).slice(-700) : null,
    model_tab_headings: tabPanel ? [...tabPanel.querySelectorAll('h3, h4, p.uppercase, p[class*="uppercase"]')].map((e) => clean(e.innerText)).filter(Boolean) : [],
  }
}
function stringsWith(obj, re, at = '', out = []) {
  if (typeof obj === 'string') { if (re.test(obj)) out.push({ at, value: obj.slice(0, 260) }) }
  else if (Array.isArray(obj)) obj.forEach((v, i) => stringsWith(v, re, `${at}[${i}]`, out))
  else if (obj && typeof obj === 'object') for (const [k, v] of Object.entries(obj)) stringsWith(v, re, at ? `${at}.${k}` : k, out)
  return out
}

const PLANNED = opt.names.flatMap((n) => [`r51-inputs ${n}`, `r51-coverage ${n}`, `r51-officers ${n}`, `r51-phrases ${n}`])
let holder = null; let armed = false; let browser; let fatal = null
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
    let ov = null; let openErr = null; let seg = null; const views = {}
    try {
      ov = await openName(page, name)
      seg = Object.keys(served.bySeg).find((k) => served.bySeg[k].overlay === ov) || null
      await waitFor(page, () => seg && served.bySeg[seg] && served.bySeg[seg].thesis, 30000).catch(() => {})
      await settle(page, 2000)
      await page.screenshot({ path: png(`r51-${slug(name)}-top.png`), fullPage: true })
      views.top = await page.evaluate(R51_PROBE)
      for (const t of TABS) {
        await closeDialogs(page)
        await clickTab(page, t.label)
        await waitTabReady(page, t.id)
        await page.screenshot({ path: png(`r51-${slug(name)}-${slug(t.label)}.png`), fullPage: true })
        views[t.id] = await page.evaluate(R51_PROBE)
      }
    } catch (e) { openErr = e }
    const thesis = seg && served.bySeg[seg] ? served.bySeg[seg].thesis : null
    const base = { name, security_key: seg, served_segments: seg ? Object.keys(served.bySeg[seg]) : [] }

    await read(`r51-inputs ${name}`, async () => {
      if (openErr) throw openErr
      if (!thesis) throw new Error('no /thesis response was captured for this name')
      const servedRows = Array.isArray(thesis.input_provenance) ? thesis.input_provenance : null
      if (!servedRows) throw new Error('the live /thesis carries no input_provenance list')
      const rows = views.top.provenance_rows
      const f = []
      if (views.top.provenance_blocks !== 1) f.push(`${views.top.provenance_blocks} provenance block(s) (1 wanted)`)
      if (rows.length !== servedRows.length) f.push(`${rows.length} row(s) drawn of ${servedRows.length} served`)
      servedRows.forEach((e, i) => { if (rows[i] && !rows[i].includes(e.source)) f.push(`row ${i + 1} does not carry the served source "${e.source}"`) })
      const at = servedRows.findIndex((e) => e.input === 'filings')
      if (at < 0) f.push('the live /thesis statement carries no filings row')
      else if (rows[at]) {
        const e = servedRows[at]
        if (e.outcome === 'landed' && e.form && !rows[at].includes(e.form)) f.push(`the filings row does not name the form ${e.form}`)
        if (/\d{4}-\d{2}-\d{2}/.test(rows[at])) f.push('the filings row prints a raw ISO date')
        if (e.outcome !== 'landed' && e.reason && !rows[at].includes(e.reason)) f.push('a not-landed filings row does not print its served reason')
      }
      const ledgers = Object.entries(views).filter(([, v]) => v.input_ledgers > 0).map(([k]) => k)
      if (ledgers.length) f.push(`[data-input-ledger] is drawn on: ${ledgers.join(', ')}`)
      return {
        verdict: f.length ? 'FAIL' : 'PASS',
        detail: f.length ? f.join(' | ') : `${rows.length} of ${servedRows.length} served rows drawn in order; filings row: "${rows[at]}"; 0 input ledgers on 6 views`,
        data: { ...base, served_input_provenance: servedRows, drawn_rows: rows, model_tab_headings: views.model.model_tab_headings, model_tab_tail: views.model.model_tab_tail },
      }
    })
    await read(`r51-coverage ${name}`, async () => {
      if (openErr) throw openErr
      const cov = (ov && ov.research_coverage) || null
      const drawn = views.top.coverage
      const f = []
      if (!cov) f.push('the live /overlay carries no research_coverage')
      else if (typeof cov.sentence === 'string' && cov.sentence) {
        if (drawn.length !== 1) f.push(`${drawn.length} coverage element(s) (1 wanted)`)
        else { if (drawn[0].text !== cov.sentence) f.push(`drawn "${drawn[0].text}" is not the served sentence`); if (drawn[0].status !== cov.status) f.push(`status ${drawn[0].status} is not the served ${cov.status}`) }
      } else if (drawn.length) f.push(`${drawn.length} coverage element(s) drawn where no sentence is served`)
      return {
        verdict: f.length ? 'FAIL' : 'PASS',
        detail: f.length ? f.join(' | ') : (cov.sentence ? `served ${cov.status}; the sentence is drawn once: "${drawn[0].text.slice(0, 70)}..."` : `served ${cov.status} with no sentence; nothing drawn`),
        data: { ...base, served_research_coverage: cov, drawn },
      }
    })
    await read(`r51-officers ${name}`, async () => {
      if (openErr) throw openErr
      if (!thesis) throw new Error('no /thesis response was captured for this name')
      const want = ((thesis.management && thesis.management.officers) || []).map((o) => o.name)
      const got = views.exec_management.officers
      const f = []
      if (got.length !== want.length) f.push(`drew ${got.length} of ${want.length} served officers`)
      const at = want.findIndex((n, i) => got[i] !== n)
      if (at !== -1) f.push(`row ${at + 1} is "${got[at]}", the served row ${at + 1} is "${want[at]}"`)
      return {
        verdict: f.length ? 'FAIL' : 'PASS',
        detail: f.length ? f.join(' | ') : (want.length ? `${got.length} of ${want.length} officers in the served order; first three: ${got.slice(0, 3).join(' / ')}` : 'the function serves 0 officers and 0 are drawn'),
        data: { ...base, served_order: want, drawn_order: got, roster_source: thesis.management ? thesis.management.roster_source : null },
      }
    })
    await read(`r51-phrases ${name}`, async () => {
      if (openErr) throw openErr
      const pillars = views.thesis.pillars
      const f = []
      for (const p of pillars) if (/research pack/i.test(p.text)) f.push(`the pillars line says "research pack": "${p.text}"`)
      const perView = Object.fromEntries(Object.entries(views).map(([k, v]) => [k, { research_pack: v.research_pack_lines, research_team_report: v.research_team_report_lines, research_team_pack: v.research_team_pack_lines }]))
      const servedPack = [...stringsWith(thesis, /research pack/i, 'thesis'), ...stringsWith(ov, /research pack/i, 'overlay')]
      const nPack = Object.values(perView).reduce((s, v) => s + v.research_pack.length, 0)
      const nTeam = Object.values(perView).reduce((s, v) => s + v.research_team_report.length, 0)
      return {
        verdict: f.length ? 'FAIL' : 'PASS',
        detail: f.length ? f.join(' | ') : `pillars line: "${pillars.map((p) => p.text).join(' // ').slice(0, 160)}"; visible lines over 6 views: ${nPack} with "research pack", ${nTeam} with the research team's phrase; ${servedPack.length} served string(s) hold "research pack"`,
        data: { ...base, pillars, visible_lines_per_view: perView, served_strings_with_research_pack: servedPack },
      }
    })
  }
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
fs.writeFileSync(path.join(OUT, 'walk51.json'), JSON.stringify({ base: opt.base, names: opt.names, fatal, reads }, null, 1))
console.log(`OUT ${OUT}`)
process.exit(n('ERROR') === 0 ? 0 : 1)
