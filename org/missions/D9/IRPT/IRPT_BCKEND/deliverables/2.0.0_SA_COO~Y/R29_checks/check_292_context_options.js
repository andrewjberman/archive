#!/usr/bin/env node
/* IB-yr-292 AC1 -- the browser-context options carry Playwright's recordHar ONLY behind YC_RECORD_HAR=1.
 *
 * Requires the library and calls its exported `contextOptions()` three times:
 *   (1) YC_RECORD_HAR unset          -> no recordHar key; userAgent and viewport present
 *   (2) YC_RECORD_HAR=1 + a path     -> recordHar.path === the path, recordHar.content === 'omit'
 *   (3) YC_RECORD_HAR=1, no path     -> throws (a recording with nowhere to go is a refusal, never a default)
 * PASS iff all three hold. Base run (CLOUD HEAD before the cut): FAIL -- contextOptions is not exported.
 * Issuer 2.0.0_SA_COO~Y, round 29. No browser is launched; no network. ASCII only.
 */
'use strict';
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..', '..', '..', '..', '..', '..', '..'); // R29_checks is eight levels below the repo root
const lib = require(path.join(ROOT, 'infra', 'aws', 'ec2', 'investor-reporting-ycharts', 'ycharts_session.js'));

function fail(msg) { process.stdout.write('FAIL: ' + msg + '\n'); process.exit(1); }

if (typeof lib.contextOptions !== 'function') fail('contextOptions is not exported (typeof ' + typeof lib.contextOptions + ')');

delete process.env.YC_RECORD_HAR; delete process.env.YC_RECORD_HAR_PATH;
const off = lib.contextOptions();
if (!off || typeof off.userAgent !== 'string' || !off.viewport) fail('default options lack userAgent/viewport: ' + JSON.stringify(off));
if ('recordHar' in off) fail('recordHar present with YC_RECORD_HAR unset');

process.env.YC_RECORD_HAR = '1'; process.env.YC_RECORD_HAR_PATH = '/tmp/w27-login.har';
const on = lib.contextOptions();
if (!on.recordHar || on.recordHar.path !== '/tmp/w27-login.har') fail('recordHar.path not honoured: ' + JSON.stringify(on.recordHar));
if (on.recordHar.content !== 'omit') fail('recordHar.content must be omit (no bodies): ' + JSON.stringify(on.recordHar));
if (on.userAgent !== off.userAgent) fail('userAgent changed under recording');

delete process.env.YC_RECORD_HAR_PATH;
let threw = false;
try { lib.contextOptions(); } catch (e) { threw = true; }
if (!threw) fail('YC_RECORD_HAR=1 with no YC_RECORD_HAR_PATH did not throw');

process.stdout.write('PASS: contextOptions -- off: no recordHar; on: path honoured, content omit; no path: refused\n');
