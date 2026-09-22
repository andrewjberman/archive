'use strict';
// IB-rtj-1 stub harness: runs a capture-session.cjs source in a fully stubbed VM (no browser,
// network, credential or real file write) and prints ONE JSON result line. Unlike
// IB-rti-1's harness_ib_rti_1.cjs (which hardcodes a single-hop chain([origin]) for the
// INITIAL navigation and so cannot exercise a redirect WITHIN that navigation), this harness
// takes the initial navigation's own hop chain as a config input -- required to build the
// single-difference regression pair for row C-S153 (arm (d) of IRPT_BCKEND.TO-IB-rtj-1).
// Usage: node harness_ib_rtj_1.cjs <source> <cfg-json>
// cfg: origin, instanceId, initialHops[] (default [origin]), verificationHops[] (default
//      [checkUrl]), status (verification nav status, default 200), passwordCount, markerCount,
//      portEnv, checkRoute, storageState
const fs = require('node:fs');
const vm = require('node:vm');
const sourcePath = process.argv[2];
const cfg = JSON.parse(process.argv[3] || '{}');
const source = fs.readFileSync(sourcePath, 'utf8');
(async () => {
  const calls = { navigations: [], storageStateCalls: 0, fileWrites: [], prompts: 0, output: '', errors: '', exitCode: null, launched: 0 };
  let currentUrl = 'about:blank';
  const origin = cfg.origin;
  const checkUrl = new URL(cfg.checkRoute || '/investor-reporting/print', origin).toString();
  const chain = (urls) => {
    let prev = null;
    let last = null;
    for (const u of urls) { const before = prev; last = { url: () => u, redirectedFrom: () => before }; prev = last; }
    return last;
  };
  const page = {
    goto: async (url) => {
      calls.navigations.push(url);
      const isInitial = calls.navigations.length === 1;
      const hops = isInitial ? (cfg.initialHops || [origin]) : (cfg.verificationHops || [checkUrl]);
      currentUrl = hops[hops.length - 1];
      return { status: () => (isInitial ? 200 : (cfg.status ?? 200)), request: () => chain(hops) };
    },
    url: () => currentUrl,
    locator: (sel) => ({ count: async () => (String(sel).includes('password') ? (cfg.passwordCount || 0) : (String(sel).includes('data-print-state') ? (cfg.markerCount ?? 1) : 0)) }),
  };
  const context = { newPage: async () => page, storageState: async () => { calls.storageStateCalls++; return cfg.storageState || { cookies: [], origins: [] }; } };
  const mocks = {
    playwright: { chromium: { launch: async () => { calls.launched++; return { newContext: async () => context, close: async () => {} }; } } },
    fs: { mkdirSync: () => {}, writeFileSync: (p, data) => { calls.fileWrites.push({ path: p, data: String(data) }); } },
    path: require('node:path'),
    readline: { createInterface: () => ({ close: () => {}, question: (_q, cb) => {
      calls.prompts++;
      if (calls.prompts > 20) throw new Error('HARNESS STOP: runaway prompts');
      cb('');
    } }) },
  };
  const env = { IRPT_CAPTURE_PORTAL_ORIGIN: origin };
  if (cfg.instanceId !== undefined) env.IRPT_CAPTURE_INSTANCE_ID = cfg.instanceId;
  if (cfg.portEnv) env.IRPT_CAPTURE_DEBUG_PORT = cfg.portEnv;
  if (cfg.checkRoute) env.IRPT_CAPTURE_CHECK_ROUTE = cfg.checkRoute;
  const sandbox = {
    require: (name) => { if (!(name in mocks)) throw new Error(`Unexpected module ${name}`); return mocks[name]; },
    URL, console: { log() {} },
    process: { env, stdin: {}, stdout: { write: (t) => { calls.output += t; } }, stderr: { write: (t) => { calls.errors += t; } }, exit: (c) => { if (calls.exitCode === null) calls.exitCode = c; } },
  };
  await vm.runInNewContext(source, sandbox, { filename: sourcePath });
  process.stdout.write(JSON.stringify(calls) + '\n');
})().catch((e) => { console.error(e); process.exitCode = 2; });
