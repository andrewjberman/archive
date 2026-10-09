/**
 * AMGT_CORPUS round 41 -- CRPS-aq-3 close read on SERVED data (issuer's file; read-only). Renders the REAL FeedList and
 * realPillarTerms from a portal tree (DEV 3af36f28) with each picked name's served thesis pillars and served feed, exactly as
 * NewsTab hands them over. The harness is page_check41.cjs's (transpile, vm, react real, other imports stubbed).
 *
 * RUN:  node aq3_close_render.cjs <served data json> <portal root>
 * The data json is {<security_key>: {pillars: [...], feed: {...}}}, read by the issuer through scoped_amgt.read_thesis_bundle
 * and read_security_overlay (the routes the page calls).
 * Prints per name: the real terms, each term block's count and the headlines it lists, or the absent sentence.
 */
const fs = require('fs')
const path = require('path')
const vm = require('vm')
const { createRequire } = require('module')

const [dataPath, portalRoot] = process.argv.slice(2)
const req = createRequire(path.join(path.resolve(portalRoot), 'package.json'))
const ts = req('typescript')
const React = req('react')
const { renderToStaticMarkup } = req('react-dom/server')
const stubFn = (...a) => {
  if (a.length === 1 && a[0] && typeof a[0] === 'object' && !Array.isArray(a[0])) return null
  const first = a.find((x) => x !== null && x !== undefined)
  return first === undefined ? '' : String(first)
}
const stubModule = new Proxy({}, { get: (_t, key) => (key === '__esModule' ? true : stubFn) })
const file = path.join(portalRoot, 'src', 'pages', 'SecurityAnalysis', 'components', 'HeaderBrief.tsx')
let out = ts.transpileModule(fs.readFileSync(file, 'utf8'), {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, jsx: ts.JsxEmit.React },
}).outputText
out += '\n;module.exports.__t = { FeedList: (typeof FeedList !== "undefined" ? FeedList : undefined) };\n'
const mod = { exports: {} }
const origError = console.error
console.error = () => {} // React key warnings are pre-existing noise
vm.runInNewContext(out, { module: mod, exports: mod.exports, require: (n) => (n === 'react' ? React : stubModule), console, React })
const FeedList = mod.exports.__t.FeedList
const realPillarTerms = mod.exports.realPillarTerms
const text = (h) => h.replace(/<[^>]+>/g, ' ').replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim()

const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'))
for (const [key, { pillars, feed }] of Object.entries(data)) {
  const terms = realPillarTerms(pillars)
  const html = renderToStaticMarkup(React.createElement(FeedList, { feed, terms: terms ?? undefined, topItems: null }))
  console.log(`== ${key}: pillars ${(pillars || []).length}, real terms ${JSON.stringify(terms)}, feed items ${((feed || {}).items || []).length}`)
  const blocks = [...html.matchAll(/<details[^>]*data-feed-term="([^"]*)"[^>]*data-feed-term-count="(\d+)"[^>]*>([\s\S]*?)<\/details>/g)]
  for (const [, term, count, inner] of blocks) {
    const heads = [...inner.matchAll(/data-feed-item[^>]*>([\s\S]*?)<\/a>/g)].map((m) => text(m[1]))
    console.log(`  term "${term}" count ${count}${heads.length ? ' -> ' + heads.join(' | ') : ''}`)
  }
  const absent = html.match(/data-feed-terms-absent[^>]*>([\s\S]*?)<\//)
  if (absent) console.log(`  absent: "${text(absent[1])}"`)
  const titleBlocks = (pillars || []).filter((p) => blocks.some((b) => b[1] === p.pillar)).length
  console.log(`  pillar-title filters shown: ${titleBlocks}`)
}
console.error = origError
