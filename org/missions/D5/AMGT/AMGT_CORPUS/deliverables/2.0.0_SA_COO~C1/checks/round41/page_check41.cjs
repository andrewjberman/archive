/**
 * AMGT_CORPUS round 41 -- CRPS-aq-3 (analysis item 3a): the news feed's term filter reads each pillar's MATCHED terms
 * (terms[1:]) and never the pillar title (terms[0], the RULED label kept by continuation.py), and a name whose pillars carry no
 * real term says so in words. Issuer's file. Read-only unless --snapshot. The harness (transpile the REAL component with the
 * installed typescript, run it in a vm with react real and every other import stubbed) is round 40's page_check.cjs.
 *
 * RUN:  node page_check41.cjs aq3 [<portal root>] [--snapshot]      (default portal root: <git toplevel>/portal)
 *
 * aq3  components/HeaderBrief.tsx  realPillarTerms, FeedList; tabs/NewsTab.tsx   -> `aq3 build <b>/3 control <c>/1`
 *   build b1  realPillarTerms is EXPORTED from HeaderBrief.tsx and, given IMB's served shape -- pillars
 *             [{pillar:"Clean balance sheet for a Tobacco company", terms:["Clean balance sheet for a Tobacco company","net debt",
 *             "EBITDA"]}, {pillar:"Cash-return machine", terms:["Cash-return machine"]}, {pillar:"Pricing power reliably outruns
 *             volume decline", terms:["Pricing power reliably outruns volume decline","price"]}] -- returns exactly
 *             ["net debt","EBITDA","price"]; given pillars whose only terms are their titles it returns []; given no pillars
 *             (null/undefined/[]) it returns null.
 *         b2  FeedList with terms ["net debt"] over two headlines -- "Imperial Brands trims net debt again" and "Clean balance
 *             sheet for a Tobacco company, says analyst" -- carries one <details data-feed-term="net debt"
 *             data-feed-term-count="1"> and NO data-feed-term for the pillar title; FeedList with terms [] (pillars present, no
 *             real term) carries an element data-feed-terms-absent whose text says the team's pillars carry no term to filter
 *             the news, and no data-feed-term.
 *         b3  tabs/NewsTab.tsx feeds HeaderBrief through realPillarTerms (its source calls `realPillarTerms(`) and no longer
 *             flattens `p.terms` directly.
 *   control   FeedList with terms undefined (no dossier) renders byte-equal to aq3_base_snapshot.json taken at the base.
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

const stubFn = (...a) => {
  if (a.length === 1 && a[0] && typeof a[0] === 'object' && !Array.isArray(a[0])) return null
  const first = a.find((x) => x !== null && x !== undefined)
  return first === undefined ? '' : String(first)
}
const stubModule = new Proxy({}, { get: (_t, key) => (key === '__esModule' ? true : stubFn) })

function load(rel, names) {
  const file = path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', rel)
  const src = fs.readFileSync(file, 'utf8')
  let out = ts.transpileModule(src, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, jsx: ts.JsxEmit.React },
  }).outputText
  out += '\n;module.exports.__t = {' + names.map((n) => `${n}: (typeof ${n} !== 'undefined' ? ${n} : undefined)`).join(', ') + '};\n'
  const mod = { exports: {} }
  vm.runInNewContext(out, { module: mod, exports: mod.exports, require: (n) => (n === 'react' ? React : stubModule), console, React })
  return { scope: mod.exports.__t, exported: mod.exports }
}
const render = (fn, props) => renderToStaticMarkup(React.createElement(fn, props))
const text = (html) => html.replace(/<[^>]+>/g, ' ').replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim()

const FEED = {
  items: [
    { id: 'n1', title: 'Imperial Brands trims net debt again', url: 'https://example.test/n1', published_at: '2026-10-08T12:00:00Z' },
    { id: 'n2', title: 'Clean balance sheet for a Tobacco company, says analyst', url: 'https://example.test/n2', published_at: '2026-10-07T12:00:00Z' },
  ],
}

function aq3() {
  const { scope, exported } = load('components/HeaderBrief.tsx', ['FeedList', 'realPillarTerms'])
  const FeedList = scope.FeedList
  if (typeof FeedList !== 'function') throw new Error('HeaderBrief.tsx: FeedList is not a function in module scope')
  const base = render(FeedList, { feed: FEED, terms: undefined, topItems: null })
  if (snapshot) {
    fs.writeFileSync(path.join(HERE, 'aq3_base_snapshot.json'), JSON.stringify(base, null, 1) + '\n')
    console.log('SNAPSHOT written aq3_base_snapshot.json from ' + portalRoot)
    return 0
  }
  const real = exported.realPillarTerms
  let b1 = 0
  if (typeof real === 'function') {
    const imb = [
      { pillar: 'Clean balance sheet for a Tobacco company', terms: ['Clean balance sheet for a Tobacco company', 'net debt', 'EBITDA'] },
      { pillar: 'Cash-return machine', terms: ['Cash-return machine'] },
      { pillar: 'Pricing power reliably outruns volume decline', terms: ['Pricing power reliably outruns volume decline', 'price'] },
    ]
    const asml = [{ pillar: 'Monopoly in EUV', terms: ['Monopoly in EUV'] }, { pillar: 'Secular growth', terms: ['Secular growth'] }]
    const ok1 = JSON.stringify(real(imb)) === JSON.stringify(['net debt', 'EBITDA', 'price'])
    const ok2 = JSON.stringify(real(asml)) === '[]'
    const ok3 = real(null) === null && real(undefined) === null && real([]) === null
    b1 = ok1 && ok2 && ok3 ? 1 : 0
    console.log(`aq3 b1 imb ${ok1} title-only ${ok2} no-pillars ${ok3}`)
  } else {
    console.log('aq3 b1 realPillarTerms is not exported from HeaderBrief.tsx')
  }
  const withTerm = render(FeedList, { feed: FEED, terms: ['net debt'], topItems: null })
  const oneTerm = /data-feed-term="net debt"[^>]*data-feed-term-count="1"|data-feed-term-count="1"[^>]*data-feed-term="net debt"/.test(withTerm)
  const noTitle = !/data-feed-term="Clean balance sheet/.test(withTerm)
  const none = render(FeedList, { feed: FEED, terms: [], topItems: null })
  const absentEl = /data-feed-terms-absent/.test(none) && !/data-feed-term=/.test(none)
  const absentWords = /no (thesis )?term/i.test(text(none))
  const b2 = oneTerm && noTitle && absentEl && absentWords ? 1 : 0
  console.log(`aq3 b2 term-count ${oneTerm} no-title ${noTitle} absent-element ${absentEl} absent-words ${absentWords}`)
  const news = fs.readFileSync(path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', 'tabs', 'NewsTab.tsx'), 'utf8')
  const b3 = /realPillarTerms\(/.test(news) && !/flatMap\(\s*\(p\)\s*=>\s*p\.terms/.test(news) ? 1 : 0
  console.log(`aq3 b3 NewsTab uses realPillarTerms ${b3 === 1}`)
  const control = JSON.stringify(JSON.parse(fs.readFileSync(path.join(HERE, 'aq3_base_snapshot.json'), 'utf8'))) === JSON.stringify(base) ? 1 : 0
  console.log(`aq3 build ${b1 + b2 + b3}/3 control ${control}/1`)
  return b1 + b2 + b3 === 3 && control === 1 ? 0 : 1
}

if (arm !== 'aq3') { console.log('usage: node page_check41.cjs aq3 [<portal root>] [--snapshot]'); process.exit(2) }
process.exit(aq3())
