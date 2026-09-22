'use strict';
// IB-rtm-1 harness. NOT a replacement for or modification of CVO~B's R12 diagnostic
// (`IRPT_BCKEND_R12_CAPTURE_FAILURE_DIAGNOSTIC.cjs`, read-only, run UNCHANGED by
// battery_ib_rtm_1.py --arm classify). This harness builds arm (d)'s own two single-difference
// pairs, run and reported by battery_ib_rtm_1.py --arm classify alongside the CVO diagnostic.
//
// Same EventEmitter-based mock shape as the R11/R12 diagnostics (page.on/context.on exist,
// matching real Playwright and letting the session-lifetime observer install exactly as it
// does against the real page). No browser, network, credential, or real write; VM mocks only.
const fs = require('node:fs');
const vm = require('node:vm');
const { EventEmitter } = require('node:events');
const { execFileSync } = require('node:child_process');
const { createHash } = require('node:crypto');
const sourcePath = 'infra/aws/ec2/investor-reporting-export/capture-session.cjs';
// Optional argv[2]: a git blob sha -- lets battery_ib_rtm_1.py run this SAME pair as a
// NEGATIVE CONTROL against a pre-repair blob, proving the pairs actually discriminate rather
// than merely describing intent.
const bytes = process.argv[2] ? execFileSync('git', ['cat-file', 'blob', process.argv[2]]) : fs.readFileSync(sourcePath);
const origin = 'https://opalinvest.dev';
const check = origin + '/investor-reporting/print';
const foreign = 'https://example.invalid/post-rename-hop';

function baseMocks(out, diskOpts) {
  return {
    playwright: { chromium: { launch: async () => ({ newContext: async () => diskOpts.context, close: async () => {} }) } },
    path: require('node:path'),
    readline: { createInterface: () => ({ close() {}, question: (_q, cb) => {
      out.prompts++;
      if (out.prompts > 6) throw new Error('HARNESS STOP: runaway prompts');
      cb('');
    } }) },
  };
}

/**
 * Pair (i), arm (a): classification by TYPE, never by a message substring. Both cases model a
 * navigation error on the FIRST verification attempt. The GOOD case's error carries
 * `error.name === 'TimeoutError'` (Playwright's own error class) -- must retry once and recover.
 * The BAD twin's error carries the SAME general shape (a message that, like the GOOD case's,
 * would satisfy a naive /timeout/i.test() keyword search -- both messages literally contain the
 * substring "timeout") but is NOT a TimeoutError by name and does NOT match this tool's own
 * exact deadline-message format -- a certificate failure whose URL happens to carry
 * `?timeout=1` -- and must now terminally refuse. The discriminating property is error TYPE
 * (Playwright's own `.name`, or an exact match against this tool's own configured deadline
 * message), never a keyword search anywhere in the message text.
 */
async function runClassify(name, cfg) {
  const out = { name, writes: 0, success: false, exitCode: null, prompts: 0, verificationCalls: 0, output: '', errors: '' };
  const page = new EventEmitter();
  const context = new EventEmitter();
  let current = 'about:blank';
  const frame = { url: () => current, parentFrame: () => null };
  page.mainFrame = () => frame;
  page.url = () => current;
  function navigation(hops, status = 200) {
    let previous = null;
    let response;
    for (const url of hops) {
      const before = previous;
      const request = { url: () => url, redirectedFrom: () => before, isNavigationRequest: () => true, frame: () => frame };
      previous = request;
      response = { url: () => url, status: () => status, frame: () => frame, request: () => request };
      current = url;
      page.emit('request', request); context.emit('request', request);
      page.emit('response', response); context.emit('response', response);
    }
    page.emit('framenavigated', frame);
    return response;
  }
  let gotoCalls = 0;
  page.goto = async () => {
    if (++gotoCalls === 1) return navigation([origin]);
    out.verificationCalls++;
    if (out.verificationCalls === 1 && cfg.throwOnce) {
      const e = new Error(cfg.errorMessage);
      if (cfg.errorName) e.name = cfg.errorName;
      throw e;
    }
    return navigation([check], 200);
  };
  page.locator = (selector) => ({ count: async () => (String(selector).includes('data-print-state') ? 1 : 0) });
  context.newPage = async () => page;
  context.storageState = async () => ({ cookies: [], origins: [] });
  const mocks = Object.assign(baseMocks(out, { context }), {
    fs: { mkdirSync() {}, writeFileSync() { out.writes++; } },
  });
  await vm.runInNewContext(bytes.toString('utf8'), {
    require: (n) => { if (!(n in mocks)) throw new Error('Unexpected module: ' + n); return mocks[n]; },
    URL, console: { log() {} },
    process: { env: { IRPT_CAPTURE_PORTAL_ORIGIN: origin, IRPT_CAPTURE_INSTANCE_ID: 'i-0167fd745ad906a66' },
      stdin: {}, stdout: { write: (s) => { out.output += s; } },
      stderr: { write: (s) => { out.errors += s; } }, exit: (c) => { out.exitCode = c; } },
  }, { filename: sourcePath });
  out.success = out.output.includes('OK: session state captured');
  return out;
}

/**
 * Pair (ii), arm (b): truthful cleanup reporting. Both cases model a foreign-origin main-frame
 * navigation the instant after `fs.renameSync` completes (the same narrowest post-rename window
 * IB-rtl-1's own harness pair modeled), so the write DOES land and the latch DOES fire, then
 * `fs.unlinkSync` is called. The GOOD case's `unlinkSync` succeeds (file actually removed). The
 * BAD twin's `unlinkSync` is mocked to throw EPERM -- the file must REMAIN on disk, the printed
 * message must be the new truthful-failure text, and the exit code must be the distinct
 * CLEANUP_FAILURE_EXIT_CODE, never the generic refusal exit code the GOOD case still uses. The
 * discriminating property is whether the delete call itself succeeded, nothing else.
 */
async function runCleanup(name, cfg) {
  const out = { name, writes: 0, renames: 0, unlinks: 0, deleted: false, success: false,
    exitCode: null, prompts: 0, verificationCalls: 0, diskFinal: null, output: '', errors: '' };
  const page = new EventEmitter();
  const context = new EventEmitter();
  let current = 'about:blank';
  const frame = { url: () => current, parentFrame: () => null };
  page.mainFrame = () => frame;
  page.url = () => current;
  function navigation(hops, status = 200) {
    let previous = null;
    let response;
    for (const url of hops) {
      const before = previous;
      const request = { url: () => url, redirectedFrom: () => before, isNavigationRequest: () => true, frame: () => frame };
      previous = request;
      response = { url: () => url, status: () => status, frame: () => frame, request: () => request };
      current = url;
      page.emit('request', request); context.emit('request', request);
      page.emit('response', response); context.emit('response', response);
    }
    page.emit('framenavigated', frame);
    return response;
  }
  let gotoCalls = 0;
  page.goto = async () => {
    if (++gotoCalls === 1) return navigation([origin]);
    out.verificationCalls++;
    return navigation([check], 200);
  };
  page.locator = (selector) => ({ count: async () => (String(selector).includes('data-print-state') ? 1 : 0) });
  context.newPage = async () => page;
  context.storageState = async () => ({ cookies: [], origins: [] });
  const disk = new Map();
  const mocks = Object.assign(baseMocks(out, { context }), {
    fs: {
      mkdirSync() {},
      writeFileSync(p, data) { disk.set(p, data); out.writes++; },
      renameSync(from, to) {
        out.renames++;
        disk.set(to, disk.get(from));
        disk.delete(from);
        navigation([origin, foreign, origin]); // the narrowest window: instant after rename
      },
      unlinkSync(p) {
        out.unlinks++;
        if (cfg.unlinkFails) {
          const e = new Error('EPERM: simulated unlink failure');
          e.code = 'EPERM';
          throw e;
        }
        disk.delete(p);
        out.deleted = true;
      },
    },
  });
  await vm.runInNewContext(bytes.toString('utf8'), {
    require: (n) => { if (!(n in mocks)) throw new Error('Unexpected module: ' + n); return mocks[n]; },
    URL, console: { log() {} },
    process: { env: { IRPT_CAPTURE_PORTAL_ORIGIN: origin, IRPT_CAPTURE_INSTANCE_ID: 'i-0167fd745ad906a66' },
      stdin: {}, stdout: { write: (s) => { out.output += s; } },
      stderr: { write: (s) => { out.errors += s; } }, exit: (c) => { out.exitCode = c; } },
  }, { filename: sourcePath });
  out.success = out.output.includes('OK: session state captured');
  out.diskFinal = disk.has('/opt/investor-reporting-export/session/storageState.json');
  return out;
}

(async () => {
  const classifyGood = await runClassify(
    'typed timeout: genuine TimeoutError, retries once and recovers',
    { throwOnce: true, errorName: 'TimeoutError', errorMessage: 'Timeout 60000ms exceeded' });
  const classifyBad = await runClassify(
    'typed timeout TWIN: message also contains "timeout" (a cert failure on a URL carrying ?timeout=1), error.name=Error, never retried',
    { throwOnce: true, errorMessage: 'page.goto: net::ERR_CERT_AUTHORITY_INVALID at https://opalinvest.dev/investor-reporting/print?timeout=1' });
  const pairIOk = classifyGood.writes === 1 && classifyGood.success === true && classifyGood.verificationCalls === 2 && classifyGood.exitCode === null &&
    classifyBad.writes === 0 && classifyBad.success === false && classifyBad.verificationCalls === 1 && classifyBad.exitCode === 1;

  const cleanupGood = await runCleanup('post-rename hop, deletion succeeds', { unlinkFails: false });
  const cleanupBad = await runCleanup('SAME post-rename hop, deletion fails EPERM (truthful failure)', { unlinkFails: true });
  const pairIIOk = cleanupGood.writes === 1 && cleanupGood.renames === 1 && cleanupGood.unlinks === 1 &&
    cleanupGood.deleted === true && cleanupGood.diskFinal === false && cleanupGood.success === false && cleanupGood.exitCode === 1 &&
    cleanupBad.writes === 1 && cleanupBad.renames === 1 && cleanupBad.unlinks === 1 &&
    cleanupBad.deleted === false && cleanupBad.diskFinal === true && cleanupBad.success === false && cleanupBad.exitCode === 4 &&
    cleanupBad.errors.includes('could NOT be removed') && !cleanupBad.errors.includes('was deleted');

  const result = {
    source: process.argv[2] || sourcePath,
    sourceSha256: createHash('sha256').update(bytes).digest('hex'),
    pairI: {
      purpose: 'arm (d)(i): typed classification, never message substring',
      discriminatingProperty: 'error TYPE (Playwright errors.TimeoutError by name, or an exact match against this tool\'s own configured deadline message) vs an unrelated error whose message merely contains the word "timeout" as a substring',
      good: classifyGood, bad: classifyBad, pairIOk,
    },
    pairII: {
      purpose: 'arm (d)(ii): truthful cleanup reporting',
      discriminatingProperty: 'whether the unlinkSync delete call itself succeeded',
      good: cleanupGood, bad: cleanupBad, pairIIOk,
    },
    allOk: pairIOk && pairIIOk,
  };
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  process.exitCode = result.allOk ? 0 : 1;
})().catch((error) => { console.error(error); process.exitCode = 2; });
