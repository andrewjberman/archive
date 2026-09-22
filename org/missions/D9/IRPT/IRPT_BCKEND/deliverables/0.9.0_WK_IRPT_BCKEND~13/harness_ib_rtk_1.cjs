'use strict';
// IB-rtk-1 harness. NOT a replacement for or modification of CVO~B's R10 lifecycle diagnostic
// (`IRPT_BCKEND_R10_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs`, read-only, run UNCHANGED by
// battery_ib_rtk_1.py's --arm lifecycle). This harness exists ONLY to build the SECOND
// single-difference pair arm (f) requires -- a same-origin TRANSIENT failure (HTTP 5xx) on the
// verification navigation followed by a clean retry, which the R10 diagnostic's six cases do
// not model (its case 4, "verification foreign first attempt then clean", is the retryable-hop
// counterexample; there is no built-in same-origin-transient-then-clean positive control to
// pair it against). Same EventEmitter-based mock shape as the R10 diagnostic (so `page.on`/
// `context.on` exist, matching real Playwright and letting the session-lifetime observer
// install exactly as it does against the real page) -- extended only to let each verification
// ATTEMPT carry its own hops/status via `cfg.verificationSequence[attemptIndex]`, so a per-
// attempt transient-then-clean sequence can be modeled without touching the R10 diagnostic
// file at all. No browser, network, credential, or real write; VM mocks only.
const fs = require('node:fs');
const vm = require('node:vm');
const { EventEmitter } = require('node:events');
const { createHash } = require('node:crypto');
const sourcePath = 'infra/aws/ec2/investor-reporting-export/capture-session.cjs';
const bytes = fs.readFileSync(sourcePath);
const origin = 'https://opalinvest.dev';
const check = origin + '/investor-reporting/print';
const foreign = 'https://example.invalid/hop';

async function run(name, cfg) {
  const out = { name, writes: 0, success: false, prompts: 0, gotoCalls: 0, verificationCalls: 0, output: '', errors: '' };
  const page = new EventEmitter();
  const context = new EventEmitter();
  let current = 'about:blank';
  const frame = { url: () => current, parentFrame: () => null };
  page.mainFrame = () => frame;
  page.url = () => current;
  function navigation(hops, status = 200) {
    let previous = null;
    let finalResponse;
    for (let i = 0; i < hops.length; i++) {
      const before = previous;
      const req = { url: () => hops[i], redirectedFrom: () => before, isNavigationRequest: () => true, frame: () => frame };
      previous = req;
      const resp = { status: () => (i === hops.length - 1 ? status : 302), url: () => hops[i], frame: () => frame, request: () => req };
      current = hops[i];
      page.emit('request', req); context.emit('request', req);
      page.emit('response', resp); context.emit('response', resp);
      finalResponse = resp;
    }
    page.emit('framenavigated', frame);
    return finalResponse;
  }
  page.goto = async () => {
    out.gotoCalls++;
    if (out.gotoCalls === 1) return navigation(cfg.initial || [origin]);
    const attemptIndex = out.verificationCalls; // 0-based, before increment
    out.verificationCalls++;
    const seq = (cfg.verificationSequence || [])[attemptIndex];
    const hops = seq ? seq.hops : [check];
    const status = seq ? (seq.status ?? 200) : 200;
    return navigation(hops, status);
  };
  page.locator = (selector) => ({ count: async () => (String(selector).includes('data-print-state') ? 1 : 0) });
  context.newPage = async () => page;
  context.storageState = async () => ({ cookies: [], origins: [] });
  const mocks = {
    playwright: { chromium: { launch: async () => ({ newContext: async () => context, close: async () => {} }) } },
    fs: { mkdirSync() {}, writeFileSync() { out.writes++; } },
    path: require('node:path'),
    readline: { createInterface: () => ({ close() {}, question: (_q, cb) => {
      out.prompts++;
      if (out.prompts > 6) throw new Error('HARNESS STOP: runaway prompts');
      if (out.prompts === 1 && cfg.interval) navigation(cfg.interval);
      cb('');
    } }) },
  };
  await vm.runInNewContext(bytes.toString('utf8'), {
    require: (name2) => { if (!(name2 in mocks)) throw new Error('Unexpected module: ' + name2); return mocks[name2]; },
    URL, console: { log() {} },
    process: { env: { IRPT_CAPTURE_PORTAL_ORIGIN: origin, IRPT_CAPTURE_INSTANCE_ID: 'i-0167fd745ad906a66' },
      stdin: {}, stdout: { write: (s) => { out.output += s; } },
      stderr: { write: (s) => { out.errors += s; } }, exit: (c) => { out.exitCode = c; } },
  }, { filename: sourcePath });
  out.success = out.output.includes('OK: session state captured');
  return out;
}

(async () => {
  // PAIR (ii), the "good" arm this harness exists to build: a SAME-ORIGIN TRANSIENT failure
  // (HTTP 500, one of the three named retryable causes) on the FIRST verification attempt,
  // then a clean second attempt -- must still succeed, since arm (e) preserves transient retry
  // and touches nothing about it.
  const transientThenClean = await run('same-origin transient (HTTP 500) then clean retry', {
    verificationSequence: [{ hops: [check], status: 500 }, { hops: [check], status: 200 }],
  });
  // The "bad" arm of the SAME pair: a foreign-origin hop on the FIRST verification attempt,
  // then a clean second attempt -- must now REFUSE (this is CVO~B's own R10 diagnostic case 4,
  // "verification foreign first attempt then clean", reproduced here with the identical shape
  // for a side-by-side single-difference pair; the only property that differs between this case
  // and transientThenClean above is WHETHER the first attempt's failure was a foreign-origin hop
  // or a same-origin transient one).
  const foreignThenClean = await run('foreign hop then clean retry', {
    verificationSequence: [{ hops: [check, foreign, check], status: 200 }, { hops: [check], status: 200 }],
  });
  const results = { transientThenClean, foreignThenClean };
  const pairOk = transientThenClean.writes === 1 && transientThenClean.success === true &&
    foreignThenClean.writes === 0 && foreignThenClean.success === false;
  process.stdout.write(JSON.stringify({ source: sourcePath, sourceSha256: createHash('sha256').update(bytes).digest('hex'),
    purpose: 'IB-rtk-1 arm (f) retry single-difference pair (ii): the ONE property that differs ' +
      'between these two cases is whether the first verification attempt\'s failure is a ' +
      'foreign-origin hop or a same-origin transient (HTTP 5xx); the retry outcome after a ' +
      'clean second attempt must differ accordingly.',
    discriminatingProperty: 'first-attempt failure cause: same-origin HTTP 500 (transient, retryable) vs foreign-origin hop (never retryable)',
    pairOk, results }, null, 2) + '\n');
  process.exitCode = pairOk ? 0 : 1;
})().catch((error) => { console.error(error); process.exitCode = 2; });
