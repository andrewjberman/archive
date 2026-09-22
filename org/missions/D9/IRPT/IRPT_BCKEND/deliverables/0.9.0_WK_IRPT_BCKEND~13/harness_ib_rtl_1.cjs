'use strict';
// IB-rtl-1 harness. NOT a replacement for or modification of CVO~B's R11 lifecycle diagnostic
// (`IRPT_BCKEND_R11_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs`, read-only, run UNCHANGED by
// battery_ib_rtl_1.py's --arm invariant). This harness exists ONLY to build the ONE additional
// single-difference case arm (e)(i) names but R11's own 11 cases do not model: a foreign
// navigation occurring IMMEDIATELY AFTER THE RENAME (R11's own case 1, "storage wait foreign
// hop then portal", already covers the OTHER timing variant arm (e)(i) names -- during the
// storageState() await -- and is used unmodified, extracted from the R11 run, for that half
// of the pair). To exercise the post-rename timing window at all, this harness supplies a
// COMPLETE `fs` mock (mkdirSync + writeFileSync + renameSync + unlinkSync, unlike every
// upstream diagnostic's minimal two-method stub) so the repaired source's real
// write-temp-then-rename path actually executes, with a hook fired the instant `renameSync`
// is called to inject a foreign-origin main-frame navigation at that exact point -- the
// narrowest possible window after the last await the invariant (arm (b)) must guard.
// Same EventEmitter-based mock shape as the R10/R11 diagnostics (`page.on`/`context.on`
// exist, matching real Playwright and letting the session-lifetime observer install exactly
// as it does against the real page). No browser, network, credential, or real write; VM
// mocks only; `renameSync`/`unlinkSync` here write to/delete from an in-memory Map, never a
// real path.
const fs = require('node:fs');
const vm = require('node:vm');
const { EventEmitter } = require('node:events');
const { execFileSync } = require('node:child_process');
const { createHash } = require('node:crypto');
const sourcePath = 'infra/aws/ec2/investor-reporting-export/capture-session.cjs';
// Optional argv[2]: a git blob sha -- lets battery_ib_rtl_1.py run this SAME pair as a
// NEGATIVE CONTROL against the pre-repair blob (row-C-S170-era bytes), proving the pair
// actually discriminates rather than merely describing intent.
const bytes = process.argv[2] ? execFileSync('git', ['cat-file', 'blob', process.argv[2]]) : fs.readFileSync(sourcePath);
const origin = 'https://opalinvest.dev';
const check = origin + '/investor-reporting/print';
const foreign = 'https://example.invalid/post-rename-hop';

async function run(name, cfg) {
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
      const request = { url: () => url, redirectedFrom: () => before,
        isNavigationRequest: () => true, frame: () => frame };
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
  // clean: marker present, no password, every attempt -- differentiate by selector text,
  // matching the shape every upstream diagnostic's own locator mock uses.
  page.locator = (selector) => ({ count: async () => (String(selector).includes('data-print-state') ? 1 : 0) });
  context.newPage = async () => page;
  context.storageState = async () => ({ cookies: [], origins: [] });
  // A tiny in-memory filesystem: enough to exercise mkdirSync/writeFileSync/renameSync/
  // unlinkSync exactly as the real `fs` module's sync API shape, so the repaired source's
  // temp-file-then-rename path runs for real inside this harness (unlike every upstream
  // diagnostic's two-method stub, which forces the repaired source's own `typeof
  // fs.renameSync === 'function'` guard to fall back to a direct write instead).
  const disk = new Map();
  const mocks = {
    playwright: { chromium: { launch: async () => ({ newContext: async () => context, close: async () => {} }) } },
    fs: {
      mkdirSync() {},
      writeFileSync(p, data) { disk.set(p, data); out.writes++; },
      renameSync(from, to) {
        out.renames++;
        disk.set(to, disk.get(from));
        disk.delete(from);
        if (cfg.hopOnRename) navigation([origin, foreign, origin]); // the narrowest window: right after the rename, before the post-rename latch recheck
      },
      unlinkSync(p) { out.unlinks++; disk.delete(p); out.deleted = true; },
    },
    path: require('node:path'),
    readline: { createInterface: () => ({ close() {}, question: (_q, cb) => {
      out.prompts++;
      if (out.prompts > 6) throw new Error('HARNESS STOP: runaway prompts');
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
  out.diskFinal = disk.has('/opt/investor-reporting-export/session/storageState.json');
  return out;
}

(async () => {
  // PAIR, the one this harness exists to build: a foreign-origin main-frame navigation
  // occurring the INSTANT after `fs.renameSync` completes -- the narrowest window the
  // invariant (arm (b)) must still guard, since it is the LAST point before the file is
  // observable at its final name. Must now REFUSE and the file must be deleted (not merely
  // absent -- `unlinks===1` proves the delete-on-relatch path executed, not that the write
  // never landed).
  const hopOnRename = await run('foreign hop the instant after rename', { hopOnRename: true });
  // The "good" arm of the SAME pair: identical harness, identical clean navigation sequence,
  // the ONLY difference being no hop is injected at the rename point.
  const cleanRename = await run('clean rename, no hop', { hopOnRename: false });
  const pairOk = cleanRename.writes === 1 && cleanRename.renames === 1 && cleanRename.success === true &&
    cleanRename.unlinks === 0 && cleanRename.diskFinal === true &&
    hopOnRename.writes === 1 && hopOnRename.renames === 1 && hopOnRename.success === false &&
    hopOnRename.unlinks === 1 && hopOnRename.deleted === true && hopOnRename.diskFinal === false &&
    hopOnRename.exitCode === 1;
  const results = { cleanRename, hopOnRename };
  process.stdout.write(JSON.stringify({ source: process.argv[2] || sourcePath, sourceSha256: createHash('sha256').update(bytes).digest('hex'),
    purpose: 'IB-rtl-1 arm (e)(i) single-difference pair, post-rename timing variant: the ONE ' +
      'property that differs between these two cases is whether a foreign-origin main-frame ' +
      'navigation lands the instant after fs.renameSync completes (the narrowest window arm (b) ' +
      'must guard, since it is the LAST point before the write is observable at its final name).',
    discriminatingProperty: 'a foreign-origin main-frame navigation landing immediately after the atomic rename, vs none',
    pairOk, results }, null, 2) + '\n');
  process.exitCode = pairOk ? 0 : 1;
})().catch((error) => { console.error(error); process.exitCode = 2; });
