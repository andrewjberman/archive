/**
 * AMGT_CORPUS round 40 -- the four page cells, one arm each. Issuer's file. Read-only: it writes nothing unless --snapshot.
 *
 * RUN:  node page_check.cjs <arm> [<portal root>] [--snapshot]      arm = ap2 | ap3 | ap4 | ap5
 *       (default portal root: <git toplevel>/portal)
 *
 * METHOD. The REAL component file is transpiled with the installed typescript and run in a vm. `react` and
 * `react-dom/server` are the installed ones; every other import is a stub (a component stub renders nothing, a helper stub
 * returns its first argument as text). The function under test is read out of the module scope by name and rendered to
 * static markup, or called. No browser, no HTTP.
 *
 * ap2  CRPS-ap-2  tabs/ThesisTab.tsx  ResearchTeamPillars   -> `ap2 build <b>/1 control <c>/1`
 *      build    a pillar whose citation carries a passage shows, inside its own <li data-dossier-pillar>, a
 *               <details data-pillar-open> holding an element with data-pillar-passage whose text is the passage, and an
 *               element with data-pillar-locator naming the locator; a pillar with no passage carries NO <details
 *               data-pillar-open> and one element with data-pillar-passage="NOT_SERVED".
 *      control  the section is still data-dossier-pillars="SERVED", both pillar leads and texts and the Terms line are
 *               still there, and a null dossier still renders data-dossier-pillars="NOT_CARRIED".
 * ap3  CRPS-ap-3  components/SecurityOverlay.tsx  DossierPositionLine, PostureHeaderLine -> `ap3 build <b>/1 control <c>/2`
 *      build    with both fields cited, the line carries data-header-dossier-cite="fund_of_record" and
 *               data-header-dossier-cite="last_stated_position", each holding the report's FILE NAME and its passage, and
 *               no s3:// key in visible text; a served field with no citation carries
 *               data-header-dossier-cite-absent="<field>".
 *      control  c1 the line is still data-header-dossier-position="SERVED" and still reads the fund and the position;
 *               c2 PostureHeaderLine's markup for a served machine verdict is byte-equal to ap3_base_snapshot.json.
 * ap4  CRPS-ap-4  components/HeaderBrief.tsx  FeedList      -> `ap4 build <b>/1 control <c>/1`
 *      build    given terms=["pricing power","vapour","buybacks"], the feed carries one <details data-feed-term="<term>"
 *               data-feed-term-count="<k>"> per term, k = the items whose title contains the term (case-insensitive),
 *               each holding exactly those items' data-feed-item keys; a term with no item reads count 0 and holds none.
 *      control  with no terms the markup is byte-equal to ap4_base_snapshot.json.
 * ap5  CRPS-ap-5  tabs/ModelTab.tsx  rowUnitWords           -> `ap5 build <b>/3 control <c>/3`
 *      build    "ZERO-DOMINATED: no magnitude: 10 of 10 fiscal years are zero" -> "zero in all 10 years";
 *               "... 7 of 10 ..." -> "zero in 7 of 10 years"; a ZERO-DOMINATED text with no counts -> the served text,
 *               lowercased (never blank).
 *      control  UNRESOLVED -> "unit not resolved"; PERCENT -> "%"; RATIO -> "multiple".
 */
const fs = require('fs')
const path = require('path')
const vm = require('vm')
const { execSync } = require('child_process')
const { createRequire } = require('module')

const HERE = __dirname
const top = execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim()
const args = process.argv.slice(2)
const snapshot = args.includes('--snapshot')
const positional = args.filter((a) => !a.startsWith('--'))
const arm = positional[0]
const portalRoot = path.resolve(positional[1] || path.join(top, 'portal'))

function installed(name) {
  const roots = [portalRoot]
  try {
    const common = execSync('git rev-parse --path-format=absolute --git-common-dir', { encoding: 'utf8', cwd: top }).trim()
    roots.push(path.join(path.dirname(common), 'portal'))
  } catch (e) { /* optional */ }
  for (const root of roots) {
    try { return createRequire(path.join(root, 'package.json'))(name) } catch (e) { /* next */ }
  }
  throw new Error(name + ' not resolvable from ' + roots.join(' or '))
}
const ts = installed('typescript')
const React = installed('react')
const { renderToStaticMarkup } = installed('react-dom/server')

/** A stub for any import but react: called with one props object it is a component and renders nothing; called any other
 * way it is a helper and returns its first non-null argument as text. */
const stubFn = (...a) => {
  if (a.length === 1 && a[0] && typeof a[0] === 'object' && !Array.isArray(a[0])) return null
  const first = a.find((x) => x !== null && x !== undefined)
  return first === undefined ? '' : String(first)
}
const stubModule = new Proxy({}, { get: (_t, key) => (key === '__esModule' ? true : key === 'default' ? stubFn : stubFn) })

function load(rel, names, consts) {
  const file = path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', rel)
  const src = fs.readFileSync(file, 'utf8')
  let out = ts.transpileModule(src, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, jsx: ts.JsxEmit.React },
  }).outputText
  out += '\n;module.exports.__t = {' + names.map((n) => `${n}: (typeof ${n} !== 'undefined' ? ${n} : undefined)`).join(', ') + '};\n'
  const mod = { exports: {} }
  const req = (name) => {
    if (name === 'react') return React
    if (consts && name.endsWith('/constants')) return consts
    return stubModule
  }
  vm.runInNewContext(out, { module: mod, exports: mod.exports, require: req, console, React })
  for (const n of names) if (typeof mod.exports.__t[n] !== 'function') throw new Error(`${rel}: ${n} is not a function in module scope`)
  return mod.exports.__t
}
const render = (fn, props) => renderToStaticMarkup(React.createElement(fn, props))
const text = (html) => html.replace(/<[^>]+>/g, ' ').replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim()
function snap(name, value) {
  const p = path.join(HERE, name)
  if (snapshot) { fs.writeFileSync(p, JSON.stringify(value, null, 1) + '\n'); console.log('SNAPSHOT written ' + name + ' from ' + portalRoot); return true }
  return JSON.stringify(JSON.parse(fs.readFileSync(p, 'utf8'))) === JSON.stringify(value)
}

function ap2() {
  const { ResearchTeamPillars } = load('tabs/ThesisTab.tsx', ['ResearchTeamPillars'])
  const PASSAGE = 'Pricing power in combustibles funds the transition to next-generation products.'
  const dossier = {
    thesis_pillars: [
      { pillar: 'Pricing power', text: 'The group raises prices ahead of volume declines.', terms: ['pricing power', 'combustibles'],
        citation: { report_key: 's3://bucket/research/IMB/IMB Initiation 2026.docx', locator: 14, passage: PASSAGE } },
      { pillar: 'Capital returns', text: 'Buybacks continue at the current pace.', terms: ['buybacks'],
        citation: { report_key: 's3://bucket/research/IMB/IMB Update 2026 09.docx', locator: 3 } },
    ],
  }
  const html = render(ResearchTeamPillars, { dossier })
  const items = html.split(/<li /).slice(1).map((s) => '<li ' + s.split('</li>')[0])
  const one = items.find((s) => /data-dossier-pillar="1"/.test(s)) || ''
  const two = items.find((s) => /data-dossier-pillar="2"/.test(s)) || ''
  const open = /<details[^>]*data-pillar-open/.test(one)
  const passage = /data-pillar-passage(="[^"]*")?[^>]*>/.test(one) && text(one).includes(PASSAGE)
  const locator = /data-pillar-locator/.test(one) && /14/.test(text(one.split(/data-pillar-locator/)[1] || ''))
  const twoClosed = !/<details[^>]*data-pillar-open/.test(two) && /data-pillar-passage="NOT_SERVED"/.test(two)
  const build = open && passage && locator && twoClosed ? 1 : 0
  const t = text(html)
  const control =
    /data-dossier-pillars="SERVED"/.test(html) && t.includes('Pricing power') && t.includes('The group raises prices ahead of volume declines.') &&
    t.includes('Capital returns') && t.includes('Buybacks continue at the current pace.') && /Terms: [^<]*combustibles/.test(t) &&
    /data-dossier-pillars="NOT_CARRIED"/.test(render(ResearchTeamPillars, { dossier: null })) ? 1 : 0
  console.log(`pillar 1: open ${open} passage ${passage} locator ${locator}; pillar 2: no opener and NOT_SERVED ${twoClosed}`)
  console.log(`ap2 build ${build}/1 control ${control}/1`)
}

function ap3() {
  const { DossierPositionLine, PostureHeaderLine } = load('components/SecurityOverlay.tsx', ['DossierPositionLine', 'PostureHeaderLine'])
  const FUND_PASSAGE = 'We hold the shares in the Global Opportunities Fund.'
  const POS_PASSAGE = 'The position stands at 3.1% of the fund after the September add.'
  const cited = {
    fund_of_record: { status: 'SERVED', value: 'Global Opportunities Fund',
      citation: { report_key: 's3://bucket/research/BA/BA Update 2026 09.docx', locator: 2, passage: FUND_PASSAGE } },
    last_stated_position: { status: 'SERVED', value: { text: 'Overweight, 3.1% of the fund' },
      citation: { report_key: 's3://bucket/research/BA/BA Update 2026 09.docx', locator: 5, passage: POS_PASSAGE } },
  }
  const uncited = {
    fund_of_record: { status: 'SERVED', value: 'Global Opportunities Fund' },
    last_stated_position: { status: 'SERVED', value: { text: 'Overweight, 3.1% of the fund' } },
  }
  const html = render(DossierPositionLine, { dossier: cited })
  const part = (field) => (html.split(new RegExp(`data-header-dossier-cite="${field}"`))[1] || '').split(/data-header-dossier-cite="/)[0]
  const fund = text('<x ' + part('fund_of_record')).includes(FUND_PASSAGE) && text('<x ' + part('fund_of_record')).includes('BA Update 2026 09.docx')
  const pos = text('<x ' + part('last_stated_position')).includes(POS_PASSAGE)
  const noKey = !text(html).includes('s3://')
  const bare = render(DossierPositionLine, { dossier: uncited })
  const absent = /data-header-dossier-cite-absent="fund_of_record"/.test(bare) && /data-header-dossier-cite-absent="last_stated_position"/.test(bare)
  const build = fund && pos && noKey && absent ? 1 : 0
  const c1 = /data-header-dossier-position="SERVED"/.test(html) && text(html).includes('Global Opportunities Fund') &&
    text(html).includes('Overweight, 3.1% of the fund') ? 1 : 0
  const posture = { status: 'SERVED', verdict: 'better', as_of: '2026-10-06T13:00:00Z', comparable: 'RTX_US_Equity', comparable_name: 'RTX' }
  const c2 = snap('ap3_base_snapshot.json', { posture_line: render(PostureHeaderLine, { posture, subjectIdentity: null, readAt: null }) }) ? 1 : 0
  console.log(`fund cited ${fund}; position cited ${pos}; no s3 key in text ${noKey}; uncited fields marked ${absent}`)
  console.log(`ap3 build ${build}/1 control ${c1 + c2}/2`)
}

function ap4() {
  const { FeedList } = load('components/HeaderBrief.tsx', ['FeedList'], { HEADER_FEED_VISIBLE_COUNT: 3, __esModule: true })
  const item = (k, title) => ({ publisher: 'Reuters', published_at: '2026-10-0' + k + 'T10:00:00Z', article_key: 'a' + k, url: 'https://example.com/' + k, title })
  const feed = {
    coverage_status: 'COVERED',
    window: { start_date: '2026-09-07', end_date: '2026-10-07' },
    items: [
      item(1, 'Imperial leans on Pricing Power as volumes fall'),
      item(2, 'Vapour sales double in Europe'),
      item(3, 'Regulator reviews flavour rules'),
      item(4, 'Analysts question pricing power in the United States'),
    ],
  }
  const html = render(FeedList, { feed, terms: ['pricing power', 'vapour', 'buybacks'] })
  const block = (term) => {
    const m = html.split(new RegExp(`<details[^>]*data-feed-term="${term}"`))[1]
    if (m === undefined) return null
    const body = m.split('</details>')[0]
    const count = (body.match(/data-feed-term-count="(\d+)"/) || ('>' + m).match(/data-feed-term-count="(\d+)"/) || [])[1]
    const head = (html.match(new RegExp(`<details[^>]*data-feed-term="${term}"[^>]*>`)) || [''])[0]
    const headCount = (head.match(/data-feed-term-count="(\d+)"/) || [])[1]
    return { count: headCount !== undefined ? headCount : count, keys: (body.match(/data-feed-item="([^"]+)"/g) || []).map((s) => s.slice(16, -1)).sort().join(',') }
  }
  const pp = block('pricing power'), vp = block('vapour'), bb = block('buybacks')
  const build = pp && vp && bb && pp.count === '2' && pp.keys === 'a1,a4' && vp.count === '1' && vp.keys === 'a2' && bb.count === '0' && bb.keys === '' ? 1 : 0
  const control = snap('ap4_base_snapshot.json', { feed: render(FeedList, { feed }) }) ? 1 : 0
  console.log(`pricing power ${JSON.stringify(pp)}; vapour ${JSON.stringify(vp)}; buybacks ${JSON.stringify(bb)}`)
  console.log(`ap4 build ${build}/1 control ${control}/1`)
}

function ap5() {
  const { rowUnitWords } = load('tabs/ModelTab.tsx', ['rowUnitWords'])
  const words = (unit) => { try { return rowUnitWords({ cells: [{ unit }], currency: null }).words } catch (e) { return 'THREW ' + e.message } }
  const got = {
    all: words('ZERO-DOMINATED: no magnitude: 10 of 10 fiscal years are zero'),
    some: words('ZERO-DOMINATED: no magnitude: 7 of 10 fiscal years are zero'),
    odd: words('ZERO-DOMINATED: magnitude not stated'),
    unresolved: words('UNRESOLVED: no unit served'),
    percent: words('PERCENT'),
    ratio: words('RATIO'),
  }
  const build = (got.all === 'zero in all 10 years' ? 1 : 0) + (got.some === 'zero in 7 of 10 years' ? 1 : 0) +
    (got.odd === 'zero-dominated: magnitude not stated' ? 1 : 0)
  const control = (got.unresolved === 'unit not resolved' ? 1 : 0) + (got.percent === '%' ? 1 : 0) + (got.ratio === 'multiple' ? 1 : 0)
  console.log(JSON.stringify(got))
  console.log(`ap5 build ${build}/3 control ${control}/3`)
}

/**
 * rev  CRPS-ap-4 AMENDMENT 1 -- the five amendments of the CTO's review of candidate 636ce634
 *      (ledger/CTO_REVIEW_PORTAL_636ce634_ROUND40.md)            -> `rev build <b>/5 control <c>/3`
 *      build    r1 the term filter matches WHOLE WORDS: the term "AI" reads count 1 on four headlines of which one says
 *                  "AI demand", one "raises", one "said" and one "Air Liquide" (a substring match reads 4);
 *               r2 the pillar opener and the header cite word the same docx locator the same way ("Paragraph <n>") and
 *                  neither shows the word "locator";
 *               r3 on the header dossier line each served passage sits inside a <details> that is closed at rest;
 *               r4 the header dossier line's text has no ". --" join;
 *               r5 ThesisTab.tsx reads `const PILLARS_HEADING = "` (the lost space is back).
 *      control  the ap2, ap3 and ap4 arms of this file still read as they did (run them beside this arm); here: c1 a term
 *               matching a whole word in two headlines still reads 2 with exactly those items; c2 the no-terms feed is
 *               still byte-equal to ap4_base_snapshot.json; c3 the machine's posture line is still byte-equal to
 *               ap3_base_snapshot.json.
 */
function rev() {
  const { FeedList } = load('components/HeaderBrief.tsx', ['FeedList'], { HEADER_FEED_VISIBLE_COUNT: 3, __esModule: true })
  const item = (k, title) => ({ publisher: 'Reuters', published_at: '2026-10-0' + k + 'T10:00:00Z', article_key: 'a' + k, url: 'https://example.com/' + k, title })
  const feed = { coverage_status: 'COVERED', window: { start_date: '2026-09-07', end_date: '2026-10-07' },
    items: [item(1, 'AI demand lifts chip orders'), item(2, 'Company raises guidance on pricing power'), item(3, 'Analysts said margins held'),
      item(4, 'Air Liquide wins contract as pricing power holds')] }
  const html = render(FeedList, { feed, terms: ['AI', 'pricing power'] })
  const termBlock = (term) => {
    const head = (html.match(new RegExp(`<details[^>]*data-feed-term="${term}"[^>]*>`)) || [''])[0]
    const body = (html.split(new RegExp(`<details[^>]*data-feed-term="${term}"`))[1] || '').split('</details>')[0]
    return { count: (head.match(/data-feed-term-count="(\d+)"/) || [])[1], keys: (body.match(/data-feed-item="([^"]+)"/g) || []).map((s) => s.slice(16, -1)).sort().join(',') }
  }
  const ai = termBlock('AI'), pp = termBlock('pricing power')
  const r1 = ai.count === '1' && ai.keys === 'a1' ? 1 : 0
  const c1 = pp.count === '2' && pp.keys === 'a2,a4' ? 1 : 0
  const c2 = snap('ap4_base_snapshot.json', (() => {
    const base = { coverage_status: 'COVERED', window: { start_date: '2026-09-07', end_date: '2026-10-07' },
      items: [item(1, 'Imperial leans on Pricing Power as volumes fall'), item(2, 'Vapour sales double in Europe'),
        item(3, 'Regulator reviews flavour rules'), item(4, 'Analysts question pricing power in the United States')] }
    return { feed: render(FeedList, { feed: base }) }
  })()) ? 1 : 0

  const { ResearchTeamPillars } = load('tabs/ThesisTab.tsx', ['ResearchTeamPillars'])
  const pillars = render(ResearchTeamPillars, { dossier: { thesis_pillars: [{ pillar: 'Pricing power', text: 'The group raises prices.',
    terms: ['pricing power'], citation: { report_key: 's3://bucket/research/IMB/IMB Initiation 2026.docx', locator: 14, passage: 'Pricing power funds the transition.' } }] } })
  const { DossierPositionLine, PostureHeaderLine } = load('components/SecurityOverlay.tsx', ['DossierPositionLine', 'PostureHeaderLine'])
  const FUND_PASSAGE = 'We hold the shares in the Global Opportunities Fund.'
  const POS_PASSAGE = 'The position stands at 3.1% of the fund after the September add.'
  const line = render(DossierPositionLine, { dossier: {
    fund_of_record: { status: 'SERVED', value: 'Global Opportunities Fund',
      citation: { report_key: 's3://bucket/research/BA/BA Update 2026 09.docx', locator: 2, passage: FUND_PASSAGE } },
    last_stated_position: { status: 'SERVED', value: { text: 'Overweight, 3.1% of the fund' },
      citation: { report_key: 's3://bucket/research/BA/BA Update 2026 09.docx', locator: 5, passage: POS_PASSAGE } } } })
  const r2 = /Paragraph 14/.test(text(pillars)) && /Paragraph 2\b/.test(text(line)) && /Paragraph 5\b/.test(text(line)) &&
    !/locator/i.test(text(pillars)) && !/locator/i.test(text(line)) ? 1 : 0
  const insideClosedDetails = (passage) => {
    const at = line.indexOf(passage)
    if (at < 0) return false
    const before = line.slice(0, at)
    const open = before.lastIndexOf('<details'), close = before.lastIndexOf('</details>')
    if (open < 0 || close > open) return false
    return !/\sopen(=|\s|>)/.test(before.slice(open, before.indexOf('>', open) + 1))
  }
  const r3 = insideClosedDetails(FUND_PASSAGE) && insideClosedDetails(POS_PASSAGE) ? 1 : 0
  const r4 = !/\.\s*--/.test(text(line)) ? 1 : 0
  const src = fs.readFileSync(path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', 'tabs', 'ThesisTab.tsx'), 'utf8')
  const r5 = /const PILLARS_HEADING = "/.test(src) ? 1 : 0
  const posture = { status: 'SERVED', verdict: 'better', as_of: '2026-10-06T13:00:00Z', comparable: 'RTX_US_Equity', comparable_name: 'RTX' }
  const c3 = snap('ap3_base_snapshot.json', { posture_line: render(PostureHeaderLine, { posture, subjectIdentity: null, readAt: null }) }) ? 1 : 0
  console.log(`r1 whole-word ${JSON.stringify(ai)}; r2 one locator wording ${r2}; r3 passages behind closed details ${r3}; r4 no ". --" ${r4}; r5 space ${r5}`)
  console.log(`rev build ${r1 + r2 + r3 + r4 + r5}/5 control ${c1 + c2 + c3}/3`)
}

const ARMS = { ap2, ap3, ap4, ap5, rev }
if (!ARMS[arm]) { console.log('usage: node page_check.cjs <ap2|ap3|ap4|ap5> [<portal root>] [--snapshot]'); process.exit(2) }
ARMS[arm]()
