/**
 * r64b.cjs -- DSGN_AMGTV1 round 64 issuer CHECK (2.0.0_SA_COO~D1): THE WALKER CAN PRESS ON /security-analysis AND SHOW THE RESULT.
 *
 * Usage (from the repository root):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round64/checks/r64b.cjs"
 *
 * Why (ledger/ROUND_ANALYSIS.round63.md @f7d74e6665 section 2 items 2-3): the CVO graded the figure press and the ASML listing press
 * as never exercised (no press, no after-shot). .claude/skills/ui-walk/walk.mjs walkSecurityAnalysis has no press step: `--press`
 * applies to plain routes only.
 * Arms (exit 0 only on all four), read from .claude/skills/ui-walk/walk.mjs:
 *   1 FLAGS: it parses `--security-press <css>` and `--window-press <css>`, both repeatable, into opt.securityPresses and
 *     opt.windowPresses, and walkSecurityAnalysis uses both.
 *   2 GUARDED: each press path refuses a target whose text matches DO_NOT_CLICK (finding walker:press-refused) and records a missing
 *     target (finding walker:press-not-found); no press path bypasses the network guard (no new route handler, no fetch).
 *   3 RECORDED: the window press writes window-press.json beside findings.json, one record per press, carrying the pressed element's
 *     css, whether it was pressed, and the focused element after the press (document.activeElement: tag, id, data-thesis-passage).
 *   4 PLANTED.
 * Source read only; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const W = path.join(process.cwd(), '.claude', 'skills', 'ui-walk', 'walk.mjs');
let t = null;
try { t = fs.readFileSync(W, 'utf8'); } catch (e) { t = null; }

const fnBody = (src, name) => {
  const at = src.indexOf(`async function ${name}(`);
  if (at < 0) return '';
  const next = src.indexOf('\nasync function ', at + 10);
  const next2 = src.indexOf('\nfunction ', at + 10);
  const ends = [next, next2].filter((x) => x > 0);
  return src.slice(at, ends.length ? Math.min(...ends) : at + 8000);
};

const G = {
  flags: (src) => {
    if (src === null) return ['walk.mjs missing'];
    const f = [];
    if (!/'--security-press'/.test(src) || !/opt\.securityPresses/.test(src)) f.push('no --security-press flag into opt.securityPresses');
    if (!/'--window-press'/.test(src) || !/opt\.windowPresses/.test(src)) f.push('no --window-press flag into opt.windowPresses');
    const body = fnBody(src, 'walkSecurityAnalysis');
    const uses = (k) => body.includes(k) || new RegExp(`async function (\\w+)[\\s\\S]{0,4000}?${k.replace('.', '\\.')}`).test(src) && body.length > 0;
    if (!body) f.push('no walkSecurityAnalysis');
    else {
      if (!uses('opt.securityPresses')) f.push('walkSecurityAnalysis never uses opt.securityPresses');
      if (!uses('opt.windowPresses')) f.push('walkSecurityAnalysis never uses opt.windowPresses');
    }
    return f;
  },
  guarded: (src) => {
    if (src === null) return ['walk.mjs missing'];
    const f = [];
    // ISSUER FIX (drain of ~139): read the press CODE, never a comment. Comments are stripped, and each path is read from the function
    // that runs it (walkSecurityAnalysis for the security press, the function that iterates opt.windowPresses for the window press).
    const code = src.replace(/\/\*[\s\S]*?\*\//g, '').replace(/(^|[^:'"`\\])\/\/[^\n]*/g, '$1');
    const fnWith = (k) => {
      const re = /async function (\w+)\(/g; let m; const hits = [];
      while ((m = re.exec(code))) hits.push(m.index);
      for (let i = 0; i < hits.length; i += 1) {
        const body = code.slice(hits[i], i + 1 < hits.length ? hits[i + 1] : code.length);
        if (body.includes(k) && /for \(const \w+ of /.test(body.slice(body.indexOf(k) - 40, body.indexOf(k) + 40))) return body;
      }
      return '';
    };
    for (const k of ['opt.securityPresses', 'opt.windowPresses']) {
      const s = fnWith(k);
      if (!s) { f.push(`no function iterates ${k}`); continue; }
      if (!/DO_NOT_CLICK\.test/.test(s)) f.push(`the ${k} path does not test DO_NOT_CLICK`);
      if (!/walker:press-refused/.test(s)) f.push(`the ${k} path records no walker:press-refused`);
      if (!/walker:press-not-found/.test(s)) f.push(`the ${k} path records no walker:press-not-found`);
    }
    if ((src.match(/page\.route\(/g) || []).length > 2) f.push('a new page.route handler appeared');
    return f;
  },
  recorded: (src) => {
    if (src === null) return ['walk.mjs missing'];
    const f = [];
    if (!/window-press\.json/.test(src)) f.push('no window-press.json written');
    if (!/document\.activeElement/.test(src)) f.push('the focused element after the press is not read (document.activeElement)');
    if (!/data-thesis-passage/.test(src)) f.push('the record does not carry the focused element\'s data-thesis-passage');
    return f;
  },
};

const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
push('FLAGS', G.flags(t));
push('GUARDED', G.guarded(t));
push('RECORDED', G.recorded(t));
{
  const p = [];
  const base = "async function walkSecurityAnalysis(page, route) {\n  for (const sec of opt.securities) { await checks(page, sec) }\n}\nconst DO_NOT_CLICK = /export/\npage.route('**', g)\n";
  if (!G.flags(base).length || !G.recorded(base).length) p.push('the round-63 walker admitted');
  const clean = "else if (a === '--security-press') (opt.securityPresses = opt.securityPresses || []).push(x)\nelse if (a === '--window-press') (opt.windowPresses = opt.windowPresses || []).push(x)\npage.route('**', g)\n" +
    "async function walkSecurityAnalysis(page, route) {\n  for (const css of opt.securityPresses || []) { if (DO_NOT_CLICK.test(txt)) findings.push({ check: 'walker:press-refused' }); else if (!n) findings.push({ check: 'walker:press-not-found' }) }\n" +
    "  for (const css of opt.windowPresses || []) { if (DO_NOT_CLICK.test(txt)) findings.push({ check: 'walker:press-refused' }); else if (!n) findings.push({ check: 'walker:press-not-found' }); const a = await page.evaluate(() => { const e = document.activeElement; return { tag: e.tagName, id: e.id, passage: e.getAttribute('data-thesis-passage') } }) }\n" +
    "  fs.writeFileSync(path.join(out, 'window-press.json'), JSON.stringify(rec))\n}\n";
  if (G.flags(clean).length || G.guarded(clean).length || G.recorded(clean).length) p.push('the clean walker refused: ' + [...G.flags(clean), ...G.guarded(clean), ...G.recorded(clean)].join('; '));
  if (!G.guarded(clean.replace(/DO_NOT_CLICK\.test\(txt\)/g, 'false')).length) p.push('an unguarded press admitted');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 64 WALKER PRESS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
