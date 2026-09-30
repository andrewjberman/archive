#!/usr/bin/env node
/* IB-yr-292 AC3 -- CONTROL: the session library's own offline suite still passes every arm.
 *
 * Runs `node --require ./tests/netguard.js tests/run_offline_suite.js` from the library directory in a
 * child process (the suite refuses to start without that preload, row IRPT_BCKEND-S121), parses the
 * RESULT block and prints summary. PASS iff summary.all_pass === true and no suite_error.
 * Base run (CLOUD HEAD before the cut): PASS -- the bound the cell must not move.
 * Issuer 2.0.0_SA_COO~Y, round 29. Loopback replay only; no vendor call. ASCII only.
 */
'use strict';
const path = require('path');
const { spawnSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..', '..', '..', '..', '..', '..', '..', '..'); // R29_checks is eight levels below the repo root
const LIB = path.join(ROOT, 'infra', 'aws', 'ec2', 'investor-reporting-ycharts');

const run = spawnSync(process.execPath, ['--require', './tests/netguard.js', 'tests/run_offline_suite.js'],
  { cwd: LIB, encoding: 'utf8', timeout: 100000 });
const out = run.stdout || '';
if (out.indexOf('RESULT-BEGIN') < 0 || out.indexOf('RESULT-END') < 0) {
  process.stdout.write('FAIL: no RESULT block (rc=' + run.status + ')\n' + (run.stderr || '').slice(-600) + '\n');
  process.exit(1);
}
const body = out.split('RESULT-BEGIN\n')[1].split('\nRESULT-END')[0];
const result = JSON.parse(body);
const summary = result.summary || {};
process.stdout.write('arms: ' + Object.keys(result.arms || {}).join(',') + ' | summary: ' + JSON.stringify(summary) + '\n');
if (result.suite_error || summary.all_pass !== true) {
  process.stdout.write('FAIL: suite not all_pass' + (result.suite_error ? ' -- ' + String(result.suite_error).slice(0, 300) : '') + '\n');
  process.exit(1);
}
process.stdout.write('PASS: offline suite all_pass with the netguard preload\n');
