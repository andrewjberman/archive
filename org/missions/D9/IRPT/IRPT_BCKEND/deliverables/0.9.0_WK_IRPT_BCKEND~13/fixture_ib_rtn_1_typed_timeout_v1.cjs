'use strict';
// IB-rtn-1 arm (b): a VERSIONED, typed-timeout fixture -- FIXTURE_VERSION = 1, this file's own
// name distinct from every prior fixture/harness (harness_ib_rti_1.cjs, harness_ib_rtj_1.cjs,
// harness_ib_rtk_1.cjs, harness_ib_rtl_1.cjs, harness_ib_rtm_1.cjs). NOT a modification of any of
// those, and NEVER touches 3.0.0_SA_CVO~B's committed diagnostics.
//
// WHY THIS FILE EXISTS, DISTINCT FROM harness_ib_rtm_1.cjs's runClassify() and from
// 3.0.0_SA_CVO~B's R13 typed-pair companion: every case in both of those throws its error
// SYNCHRONOUSLY, immediately, inside the mocked page.goto() call -- `throw new Error(msg)` with
// `.name` assigned programmatically right before the throw. That is sufficient to test the
// CLASSIFICATION predicate (isRecognizedTimeout), but it is a "bare throw new Error() relabeled"
// in exactly the sense arm (b) says a fixture must NOT be: it proves nothing about whether the
// classification also holds when a timeout arises the way it actually does in production -- from
// a REAL, asynchronous deadline: the tool's own configured `timeout: GOTO_TIMEOUT_MS` option
// racing against a navigation that never settles, with Node's OWN `setTimeout` (a genuine
// async timer, not a synchronous throw) as the mechanism that eventually rejects the promise.
//
// This fixture's mocked page.goto() therefore returns a Promise that:
//   - on the configured verification attempt, races an unsettled "navigation" (a Promise that
//     would resolve only after `cfg.hangMs`, i.e. modeling a hung/never-answering page) against
//     a REAL `setTimeout(..., cfg.timeoutMs)` callback that fires asynchronously, after real
//     elapsed event-loop time (scaled down from the tool's real 60000ms for test speed -- the
//     MECHANISM under test is "does a real timer firing produce a recognized timeout", not "does
//     this fixture wait 60 real seconds"; the discriminating property does not depend on the
//     magnitude of the delay);
//   - when the timer fires, rejects with an error object built by `cfg.makeError()`, so the SAME
//     real-timer mechanism can produce either a genuinely-typed error (GOOD case) or an untyped
//     one carrying the identical message text (BAD control) -- isolating "was this recognized"
//     to error TYPE alone, never to whether a timer genuinely fired (it did, in both cases).
//
// TWO cases:
//   GOOD  -- the timer fires and rejects with `new TimeoutErrorClass(...)`, where
//            TimeoutErrorClass is the EXACT SAME class object exposed to the source under test as
//            `require('playwright').errors.TimeoutError` -- so `error instanceof
//            playwrightErrors.TimeoutError` is a GENUINE class-identity check, not name-matching
//            duck-typing. Expected: recognized as a timeout, retried, recovers on the clean
//            second attempt (writes=1, success=true).
//   BAD   -- the SAME real timer, same delay, same message text, rejects with a PLAIN `Error`
//            that never had `.name` set (defaults to 'Error') and is NOT an instance of
//            TimeoutErrorClass. Expected: NOT recognized as a timeout (this is a genuine
//            navigation error under the closed taxonomy) -- terminal refusal, never retried
//            (writes=0, success=false). Proves the classifier is TYPE-only, not "did a timer
//            fire" or "does the message look like a timeout".
//
// No browser, network, credential, or real filesystem write. Optional argv[2]: a git blob sha
// (negative control against a pre-repair blob), matching every prior fixture/harness's own
// convention; default reads the worktree source.
const fs = require('node:fs');
const vm = require('node:vm');
const { EventEmitter } = require('node:events');
const { execFileSync } = require('node:child_process');
const { createHash } = require('node:crypto');

const FIXTURE_VERSION = 1;
const sourcePath = 'infra/aws/ec2/investor-reporting-export/capture-session.cjs';
const bytes = process.argv[2] ? execFileSync('git', ['cat-file', 'blob', process.argv[2]]) : fs.readFileSync(sourcePath);
const origin = 'https://opalinvest.dev';
const check = origin + '/investor-reporting/print';

// The REAL class object handed to the source under test as `errors.TimeoutError`. A genuine
// `instanceof` check against THIS class is what `isRecognizedTimeout`'s path 1 must exercise.
class TimeoutErrorClass extends Error {
  constructor(message) {
    super(message);
    this.name = 'TimeoutError';
  }
}

// Scaled down from the tool's real GOTO_TIMEOUT_MS (60000) for test speed: the property under
// test is "does a REAL, asynchronous setTimeout firing get recognized", which does not depend on
// the magnitude of the delay -- 25ms of genuine event-loop time is exactly as real as 60000ms.
const FIXTURE_TIMEOUT_MS = 25;
const HANG_MS = FIXTURE_TIMEOUT_MS + 500; // the "hung navigation" never resolves before the timer

async function runRealTimerCase(name, makeError) {
  const out = { name, fixtureVersion: FIXTURE_VERSION, timeoutMs: FIXTURE_TIMEOUT_MS,
    writes: 0, success: false, exitCode: null, prompts: 0, verificationCalls: 0,
    realTimerFired: false, elapsedMs: null, output: '', errors: '' };
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
  const start = Date.now();
  page.goto = (url, opts) => {
    if (++gotoCalls === 1) return Promise.resolve(navigation([origin]));
    out.verificationCalls++;
    if (out.verificationCalls === 1) {
      // A REAL race: a hung "navigation" that would eventually resolve after HANG_MS, against a
      // REAL Node setTimeout armed with THIS call's own configured `opts.timeout` (falling back
      // to FIXTURE_TIMEOUT_MS if the source did not pass one) -- genuinely asynchronous; nothing
      // here is a synchronous throw.
      const timeoutMs = (opts && typeof opts.timeout === 'number') ? Math.min(opts.timeout, FIXTURE_TIMEOUT_MS) : FIXTURE_TIMEOUT_MS;
      return new Promise((resolve, reject) => {
        const hangTimer = setTimeout(() => { resolve(navigation([check], 200)); }, HANG_MS);
        setTimeout(() => {
          out.realTimerFired = true;
          out.elapsedMs = Date.now() - start;
          clearTimeout(hangTimer);
          reject(makeError(timeoutMs));
        }, timeoutMs);
      });
    }
    return Promise.resolve(navigation([check], 200));
  };
  page.locator = (selector) => ({ count: async () => (String(selector).includes('data-print-state') ? 1 : 0) });
  context.newPage = async () => page;
  context.storageState = async () => ({ cookies: [], origins: [] });
  const mocks = {
    playwright: {
      chromium: { launch: async () => ({ newContext: async () => context, close: async () => {} }) },
      errors: { TimeoutError: TimeoutErrorClass },
    },
    path: require('node:path'),
    fs: { mkdirSync() {}, writeFileSync() { out.writes++; } },
    readline: { createInterface: () => ({ close() {}, question: (_q, cb) => {
      out.prompts++;
      if (out.prompts > 6) throw new Error('FIXTURE STOP: runaway prompts');
      cb('');
    } }) },
  };
  await vm.runInNewContext(bytes.toString('utf8'), {
    require: (n) => { if (!(n in mocks)) throw new Error('Unexpected module: ' + n); return mocks[n]; },
    URL, Buffer, console: { log() {} },
    process: { env: { IRPT_CAPTURE_PORTAL_ORIGIN: origin, IRPT_CAPTURE_INSTANCE_ID: 'i-0167fd745ad906a66' },
      stdin: {}, stdout: { write: (s) => { out.output += s; } },
      stderr: { write: (s) => { out.errors += s; } }, exit: (c) => { out.exitCode = c; } },
  }, { filename: sourcePath });
  out.success = out.output.includes('OK: session state captured');
  return out;
}

(async () => {
  const good = await runRealTimerCase(
    'GOOD: real setTimeout fires, rejects with a genuine instanceof-TimeoutErrorClass error -- must recover',
    (timeoutMs) => new TimeoutErrorClass(`Timeout ${timeoutMs}ms exceeded`));
  const bad = await runRealTimerCase(
    'BAD: SAME real setTimeout fires (same delay, same message text), rejects with a plain Error (no .name, not instanceof) -- must stay terminal',
    (timeoutMs) => new Error(`Timeout ${timeoutMs}ms exceeded`));

  const goodOk = good.realTimerFired === true && good.writes === 1 && good.success === true &&
    good.verificationCalls === 2 && good.exitCode === null;
  const badOk = bad.realTimerFired === true && bad.writes === 0 && bad.success === false &&
    bad.verificationCalls === 1 && bad.exitCode === 1 && bad.errors.includes('NAVIGATION_ERROR');
  const pairOk = goodOk && badOk;

  const result = {
    fixture: 'fixture_ib_rtn_1_typed_timeout_v1.cjs',
    fixtureVersion: FIXTURE_VERSION,
    source: process.argv[2] || sourcePath,
    sourceSha256: createHash('sha256').update(bytes).digest('hex'),
    purpose: 'arm (b): a genuine real-async-timer deadline, not a bare throw new Error() relabeled -- both cases use Node\'s own setTimeout to fire the rejection after real elapsed event-loop time; the ONLY difference between them is error TYPE (instanceof TimeoutErrorClass vs a plain Error), never whether a real timer fired (it did, in both).',
    discriminatingProperty: 'error TYPE (instanceof the exact class exposed as errors.TimeoutError) vs a plain Error carrying the identical message text, both produced by a REAL setTimeout firing',
    good, bad, goodOk, badOk, pairOk,
  };
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  process.exitCode = pairOk ? 0 : 1;
})().catch((error) => { console.error(error); process.exitCode = 2; });
