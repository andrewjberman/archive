'use strict';
// IB-rti-1 stub harness: runs a capture-session.cjs source in a fully stubbed VM (no browser, network,
// credential or real file write) and prints ONE JSON result line. Usage: node harness.cjs <source> <cfg-json>
// cfg: origin, instanceId, status, passwordCount, markerCount, firstUrl, finalUrl, hops[], portEnv,
//      checkRoute, storageState
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
      if (url === origin) {
        currentUrl = cfg.firstUrl || origin;
        return { status: () => 200, request: () => chain([origin]) };
      }
      currentUrl = cfg.finalUrl || url;
      const hops = cfg.hops || [url];
      return { status: () => cfg.status, request: () => chain(hops) };
    },
    url: () => currentUrl,
    locator: (sel) => ({ count: async () => (String(sel).includes('password') ? (cfg.passwordCount || 0) : (String(sel).includes('data-print-state') ? (cfg.markerCount || 0) : 0)) }),
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
