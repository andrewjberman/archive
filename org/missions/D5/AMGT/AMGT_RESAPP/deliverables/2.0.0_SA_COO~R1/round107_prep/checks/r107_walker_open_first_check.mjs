// r107_walker_open_first_check.mjs -- AMGT_RESAPP round 107, AMGT-bn-2: the ui-walk walker can open a named disclosure first.
//
//   node r107_walker_open_first_check.mjs <repo-root>
//
// WHY: the walker expands at most 20 closed <details>, in page order. On a Security Analysis Model tab the 26 `Full figures`
// disclosures of the What Changed table come before `All figures`, so the All-figures grid is never opened (round 106's walk
// read change 2 as NOT EXERCISED). The cell adds `--open-first <summary text>` (repeatable) and a pure ordering helper
// `.claude/skills/ui-walk/open_first.mjs` exporting `orderSummaries(texts, openFirst)`.
//
// CONTRACT of orderSummaries(texts, openFirst) -> array of indices, a permutation of 0..texts.length-1:
//   - an index whose text, trimmed and lower-cased, equals an openFirst entry (trimmed, lower-cased) comes BEFORE every other index;
//   - matching indices are ordered by the position of their entry in openFirst, then by original index;
//   - every other index follows in original order; an empty or absent openFirst returns the identity order; an entry that matches
//     nothing changes nothing and does not throw.
// Prints `R107 WALKER OPEN-FIRST: YES (n of n)` or `NO (k of n arms ...)`; exit 0 only on YES. Reads files only.
import { pathToFileURL } from 'node:url'
import { readFileSync, existsSync } from 'node:fs'
import path from 'node:path'

const root = path.resolve(process.argv[2] || '.')
const arms = []
const arm = (name, ok, detail = '') => arms.push({ name, ok: !!ok, detail })
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b)
const isPerm = (xs, n) => Array.isArray(xs) && xs.length === n && same([...xs].sort((p, q) => p - q), Array.from({ length: n }, (_, i) => i))

const modPath = path.join(root, '.claude', 'skills', 'ui-walk', 'open_first.mjs')
const walkPath = path.join(root, '.claude', 'skills', 'ui-walk', 'walk.mjs')
let orderSummaries = null
try {
  if (existsSync(modPath)) orderSummaries = (await import(pathToFileURL(modPath).href)).orderSummaries
} catch (e) {
  arm('module loads', false, String(e && e.message).split('\n')[0])
}
arm('A1 module exports orderSummaries', typeof orderSummaries === 'function', existsSync(modPath) ? 'exists' : 'open_first.mjs not found')

if (typeof orderSummaries === 'function') {
  const call = (t, o) => { try { return orderSummaries(t, o) } catch (e) { return 'THROW ' + e.message } }
  arm('A2 empty openFirst is the identity', same(call(['a', 'b', 'c'], []), [0, 1, 2]) && same(call(['a', 'b'], undefined), [0, 1]))
  const model = [...Array(26).fill('Full figures'), 'All figures', 'About these figures']
  const r3 = call(model, ['All figures'])
  arm('A3 All figures (index 26 of 28) moves first, the rest keep order', isPerm(r3, 28) && r3[0] === 26 && same(r3.slice(1), [...Array(26).keys(), 27]))
  arm('A4 match is trimmed and case-insensitive', same(call(['x', ' ALL Figures '], ['all figures ']), [1, 0]))
  arm('A5 two entries keep the openFirst order', same(call(['a', 'b', 'c'], ['c', 'a']), [2, 0, 1]))
  arm('A6 an entry that matches nothing changes nothing and does not throw', same(call(['a', 'b'], ['zzz']), [0, 1]))
  arm('A7 every match of one entry comes first, in original order', same(call(['x', 'F', 'y', 'F'], ['f']), [1, 3, 0, 2]))
}

let walkText = ''
try { walkText = readFileSync(walkPath, 'utf8') } catch { /* arm below records it */ }
arm('A8 walk.mjs wires the flag, the helper and its log line',
  walkText.includes("'--open-first'") && walkText.includes('orderSummaries(') && walkText.includes('OPEN-FIRST'),
  walkText ? '' : 'walk.mjs not readable')

const pass = arms.filter((a) => a.ok).length
for (const a of arms) console.log(`${a.ok ? 'PASS' : 'FAIL'} ${a.name}${a.detail ? ' -- ' + a.detail : ''}`)
const yes = pass === arms.length
console.log(`R107 WALKER OPEN-FIRST: ${yes ? 'YES' : 'NO'} (${pass} of ${arms.length} arms)`)
process.exit(yes ? 0 : 1)
