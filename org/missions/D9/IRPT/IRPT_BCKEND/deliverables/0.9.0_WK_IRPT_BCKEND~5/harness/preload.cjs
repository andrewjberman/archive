'use strict';
// Preload for battery_ib_rth_5.py's `node --require`. Monkeypatches child_process.execFileSync
// BEFORE render_export.cjs's own `const { execFileSync } = require('child_process')` runs --
// Node's module cache means both requires see the SAME object, so the destructure in
// render_export.cjs picks up this patched function. Fakes only the exact two AWS CLI shapes
// this script calls (s3api get-object / put-object); anything else throws loud rather than
// silently falling through to a real process spawn from inside a battery run.
const cp = require('child_process');
const fs = require('fs');

cp.execFileSync = function fakeExecFileSync(cmd, args) {
  if (cmd === 'aws' && Array.isArray(args) && args[0] === 's3api' && args[1] === 'get-object') {
    const destPath = args[args.length - 1];
    fs.writeFileSync(destPath, JSON.stringify({ versions: { renderer_version: 'fake-test' } }), 'utf8');
    return '';
  }
  if (cmd === 'aws' && Array.isArray(args) && args[0] === 's3api' && args[1] === 'put-object') {
    return '';
  }
  throw new Error(`BLOCKED: fake execFileSync received an unexpected command: ${cmd} ${JSON.stringify(args)}`);
};
