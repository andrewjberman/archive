'use strict';
// FAKE playwright module for IB-rth-5's wiring proof (battery_ib_rth_5.py). Resolved ONLY
// through a NODE_PATH the battery sets for its own child `node` invocations -- never installed,
// never present in the deployed artifact tree, never touches a real network or real browser.
//
// It records every call it receives (chromium.launch, browser.newContext, browser.newPage) to
// IB_RTH5_CALL_LOG so the Python battery can assert on the EXACT arguments render_export.cjs
// passed -- proof of WIRING, not just a matching log line.
//
// It ALWAYS reports a sign-in screen (`input[type=password]` count 1) regardless of what
// storageState was handed to newContext, because this fake session was never real -- a script
// that claimed success against this stub would be a defect in the CHECK, exactly what the task
// order's acceptance bar warns against.
const fs = require('fs');

function logCall(entry) {
  const logPath = process.env.IB_RTH5_CALL_LOG;
  if (!logPath) return;
  let existing = [];
  if (fs.existsSync(logPath)) {
    try { existing = JSON.parse(fs.readFileSync(logPath, 'utf8')); } catch (e) { existing = []; }
  }
  existing.push(entry);
  fs.writeFileSync(logPath, JSON.stringify(existing, null, 2));
}

function makeFakePage() {
  return {
    on() {},
    async goto(url, opts) {
      logCall({ call: 'page.goto', url, opts });
      return { status: () => 200 };
    },
    locator(sel) {
      return {
        async count() {
          if (sel.indexOf('does not support') >= 0) return 0;
          if (sel.indexOf('password') >= 0) return 1; // ALWAYS looks signed-out
          return 0;
        },
      };
    },
    async innerText() { return ''; },
    async pdf() { return Buffer.from('fake-pdf-bytes-never-reached'); },
  };
}

function makeFakeContext(contextOptions) {
  logCall({ call: 'browser.newContext', contextOptions: contextOptions || null });
  return {
    async newPage() {
      logCall({ call: 'context.newPage' });
      return makeFakePage();
    },
  };
}

const chromium = {
  async launch(opts) {
    logCall({ call: 'chromium.launch', opts: opts || null });
    return {
      async newContext(contextOptions) { return makeFakeContext(contextOptions); },
      async newPage() {
        // The PRE-cell-IB-rth-5 shape, kept only so a deliberately-unwired copy of
        // render_export.cjs (the negative control) still runs to completion under this stub.
        logCall({ call: 'browser.newPage (legacy direct path -- unwired)' });
        return makeFakePage();
      },
      async close() { logCall({ call: 'browser.close' }); },
    };
  },
};

module.exports = { chromium };
