/**
 * r30r.build.cjs -- builds the round-30 AV-zh-2 REPAIRS fixtures (issuer 2.0.0_SA_COO~D). NOT a check.
 *
 * Usage: cd C:/tmp/wk-dsgn-amgtv1-82 && node <this file>     (portal/ under the cwd must be the BASE, portal e370eb7c)
 * Writes, beside this file (ASCII only: every non-ASCII character is written as a \uXXXX escape, the parsed value unchanged):
 *   overlay.BA_US_Equity.urlnull.PLANTED.json  the SERVED round14 BA overlay (round14/fixtures/overlay.BA_US_Equity.json) with its
 *     feed PLANTED: five items, newest first -- three with `url: null` (the shape COO~Z msg 28802 says the harvested gold serves
 *     after RESAPP's next redeploy, row Z-W212-S2) and two with a served url (the one served WSJ item, verbatim, and one planted).
 *     HEADER_FEED_VISIBLE_COUNT is 3, so items 1-3 (null, served, null) render open and items 4-5 (null, served) sit in the
 *     "Expand" <details>: both regions carry both kinds.
 *   chartColors.base.exports.json  the BASE portal/src/lib/chartColors.ts export census: per top-level export its kind and a
 *     sha256 of its value (JSON of the evaluated value; a function's whitespace-collapsed declaration text). chrome.cjs arm 1
 *     compares the candidate against it (the change is additive: every BASE export unchanged, exactly one new export).
 * No network, no AWS. Re-running it on the BASE rewrites the same bytes.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');

const OUT = __dirname;
const D = path.join(__dirname, '..', '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const ts = require('module').createRequire(path.join(L.base, 'package.json'))('typescript');

const ascii = (s) => s.replace(/[\u0080-\uffff]/g, (c) => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'));
const write = (name, obj) => { fs.writeFileSync(path.join(OUT, name), ascii(JSON.stringify(obj, null, 1)) + '\n'); console.log('OK: wrote ' + name); };

let commit = 'UNREAD';
try { commit = execFileSync('git', ['-C', L.base, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(); } catch (e) { commit = 'UNREAD (' + String(e.message).split('\n')[0] + ')'; }
if (!/^e370eb7c/.test(commit)) { console.log('ERROR: portal/ under the cwd is at ' + commit + ', not the BASE e370eb7c'); process.exit(2); }

// ---- 1. the planted url-null feed ---------------------------------------------------------------------------------------
const served = JSON.parse(fs.readFileSync(path.join(D, 'round14', 'fixtures', 'overlay.BA_US_Equity.json'), 'utf8'));
const ov = JSON.parse(JSON.stringify(served.payload || served));
const wsj = ov.feed.items[0];
const item = (k, pub, at, title, url) => ({
  publisher: pub, published_at: at, article_key: k, url, title, published_date: at.slice(0, 10), fetched_at: null,
  first_discovered_at: null, security_key: 'BA', key_form: 'BA', words: null, body_sha256: null, content_status: 'harvested_gold',
});
ov.feed.items = [
  item('harvest:BA:2026-09-29:planted-1', 'reuters', '2026-09-29T14:05:00Z', 'Boeing resumes 737 MAX deliveries to China (planted, no url served)', null),
  item('harvest:BA:2026-09-24:planted-2', 'reuters', '2026-09-24T11:40:00Z', 'Boeing names new head of its defense unit (planted, url served)', 'https://www.reuters.com/business/aerospace-defense/planted-boeing-defense-head-2026-09-24/'),
  item('harvest:BA:2026-09-18:planted-3', 'barrons', '2026-09-18T16:20:00Z', 'Boeing stock: what the strike vote means (planted, no url served)', null),
  item('harvest:BA:2026-09-10:planted-4', 'wsj', '2026-09-10T09:00:00Z', 'Boeing and its machinists return to the table (planted, no url served)', null),
  wsj,
];
ov.feed.item_count = ov.feed.items.length;
write('overlay.BA_US_Equity.urlnull.PLANTED.json', {
  _capture_note: 'PLANTED by r30r.build.cjs: round14/fixtures/overlay.BA_US_Equity.json (SERVED) with feed.items replaced by 5 items, newest first; items 1, 3 and 4 carry url null (COO~Z msg 28802, RESAPP row Z-W212-S2: harvested gold carries no url); item 5 is the served WSJ item verbatim; item 2 is planted with a url.',
  payload: ov,
});

// ---- 2. the BASE chartColors.ts export census ------------------------------------------------------------------------------
const CC = 'src/lib/chartColors.ts';
const text = fs.readFileSync(path.join(L.base, CC), 'utf8').replace(/\r\n/g, '\n'); // LF-normalised: a Windows checkout is CRLF
const sha = (s) => crypto.createHash('sha256').update(s).digest('hex');
function census(srcText, mod) {
  const sf = ts.createSourceFile('chartColors.ts', srcText, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS);
  const out = {};
  const exported = (n) => (n.modifiers || []).some((m) => m.kind === ts.SyntaxKind.ExportKeyword);
  const collapse = (s) => s.replace(/\s+/g, ' ').trim();
  for (const st of sf.statements) {
    if (!exported(st)) continue;
    if (ts.isFunctionDeclaration(st) && st.name) out[st.name.text] = { kind: 'function', sha256: sha(collapse(st.getText(sf))) };
    else if (ts.isVariableStatement(st)) {
      for (const d of st.declarationList.declarations) {
        const name = d.name.getText(sf);
        const v = mod[name];
        out[name] = typeof v === 'function' ? { kind: 'function', sha256: sha(collapse(d.getText(sf))) } : { kind: 'value', sha256: sha(JSON.stringify(v)) };
      }
    }
  }
  return out;
}
const exportsBase = census(text, L.source(CC));
write('chartColors.base.exports.json', {
  _capture_note: 'BASE census of portal/src/lib/chartColors.ts by r30r.build.cjs (top-level exports: kind + sha256 of the JSON value, or of a function declaration with whitespace collapsed). Type-only exports are not tokens and are not listed. source_sha256 is of the LF-normalised text.',
  portal_commit: commit,
  source_sha256: sha(text),
  export_count: Object.keys(exportsBase).length,
  exports: exportsBase,
});
