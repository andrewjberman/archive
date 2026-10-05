/**
 * AMGT_CORPUS round 38, CRPS-an-4 -- the /ui-walk walker closes the timeline day it opened before it presses the tabs.
 * Issuer's file. Static: a real walk needs the shared walker account (MSTR~Z slot); that run is the issuer's an-6.
 *
 * RUN (repo root): node an4_check.cjs
 *   b1  in `.claude/skills/ui-walk/walk.mjs`, the body of `async function walkTimeline(page, sec)` presses Escape (or clicks the
 *       opened dialog's close control) AFTER its last day-state wait and BEFORE it returns. On 2026-10-05 the TSM walk
 *       (tmp/ui-walk/20261005T135401Z) left the "October 3rd, 2026" day dialog open over every tab shot.
 *   c1  `node --check` parses walk.mjs (the file stays loadable).
 * Prints one line per arm, then `an4 build <p>/1 control <q>/1`.
 */
const fs = require('fs')
const path = require('path')
const { execSync, spawnSync } = require('child_process')

const top = execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim()
const file = path.join(top, '.claude', 'skills', 'ui-walk', 'walk.mjs')
const src = fs.readFileSync(file, 'utf8')

// the function body: from its signature to the next top-level `async function` / `function` / EOF
const start = src.indexOf('async function walkTimeline(page, sec)')
let b1 = false
let note = 'walkTimeline not found'
if (start >= 0) {
  const rest = src.slice(start + 10)
  const nextFn = rest.search(/\n(async )?function [A-Za-z_]+\(/)
  const body = nextFn >= 0 ? rest.slice(0, nextFn) : rest
  const lastWait = Math.max(body.lastIndexOf('waitForDayState('), 0)
  const after = body.slice(lastWait)
  const closes = /keyboard\.press\(\s*['"]Escape['"]\s*\)|\[aria-label="?[Cc]lose|getByRole\(\s*['"]button['"]\s*,\s*\{\s*name:\s*\/close/.test(after)
  b1 = closes
  note = `walkTimeline body ${body.length} chars; a close after the last day wait: ${closes}`
}
console.log(`ARM b1 ${b1 ? 'PASS' : 'FAIL'} ${note}`)
const chk = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' })
const c1 = chk.status === 0
console.log(`ARM c1 ${c1 ? 'PASS' : 'FAIL'} node --check rc ${chk.status} ${String(chk.stderr || '').split('\n')[0]}`)
console.log(`an4 build ${b1 ? 1 : 0}/1 control ${c1 ? 1 : 0}/1`)
