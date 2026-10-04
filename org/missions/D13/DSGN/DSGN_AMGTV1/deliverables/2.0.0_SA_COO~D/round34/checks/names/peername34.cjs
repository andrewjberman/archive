/**
 * peername34.cjs -- DSGN_AMGTV1 round 34, AV-zl-1 (issuer 2.0.0_SA_COO~D): THE PEERS TABLE NAMES ITS SUBJECT AS THE HEADER DOES
 * (PRD FWD-27 "one display name per security").
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-93): node <this file>
 * Why: the round-34 gap read on PROD dbd29c6320 (round34/walk/read-20261004T001928Z, reads 18-20) found ONE security under two
 *   names on one page: the header, Lead Panel and every other tab print the served overlay `display_name` ("The Boeing Co",
 *   "Valero Energy Corp", "Advanced Micro Devices Inc"); the Peers subject row prints the served `peers.subject.name` ("BOEING
 *   CO/THE (subject)", "VALERO ENERGY CORP (subject)", "Advanced Micro Devices, Inc. (subject)") -- cscTable.ts:151. Both are
 *   served; which one the page prints for its own subject is a presentation choice (C-PRESENTATION-ONLY: nothing is rewritten).
 * Inputs: round34/fixtures/{overlay,peers}.{BA,VLO}_US_Equity.json (captured on the deployed opal-amgt-scoped-api, read-only).
 * Render: round15/checks/_load.cjs, the REAL tabs/PeersTab.tsx (and cscTable.ts) with usePeerSet / useSecurityOverlay answering
 *   the captured payloads.
 * Arms:
 *   1  ONE NAME: for BA and VLO, the subject row ([data-csc-row="subject"]) names the security by the overlay's served
 *      `display_name`, and the served `peers.subject.name` (when it differs) prints nowhere on the tab.
 *   2  NOTHING INVENTED: with the overlay's `display_name` planted absent (null), the subject row prints the served
 *      `peers.subject.name` -- the page never makes a name up.
 *   3  KEEP: round29 tabs/peersmenu.cjs and round22 subjectrow.cjs still exit 0.
 *   4  PLANTED: the name predicate rejects the raw peer name in the subject row and a page printing both names, and accepts the
 *      good row.
 * Prints one line per arm and "ONE NAME FOR THE SUBJECT IN PEERS: <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const DROOT = path.join(__dirname, '..', '..', '..');
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const SA = 'src/pages/SecurityAnalysis/';
const FIX = path.join(__dirname, '..', '..', 'fixtures');
const load = (f) => { const d = JSON.parse(fs.readFileSync(path.join(FIX, f), 'utf8')); return d && d.payload ? d.payload : d; };
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
const textOf = (h) => decode(String(h).replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();

function render(peers, overlay, key) {
  L.hookState.impl = { usePeerSet: () => peers, useSecurityOverlay: () => overlay };
  const m = L.source(SA + 'tabs/PeersTab.tsx');
  return L.render(m.PeersTab, { securityKey: key });
}
/** The subject row's first cell text, or null. */
function subjectCell(html) {
  const row = /<tr[^>]*data-csc-row="subject"[^>]*>([\s\S]*?)<\/tr>/.exec(html);
  if (!row) return null;
  const td = /<td[^>]*>([\s\S]*?)<\/td>/.exec(row[1]);
  return td ? textOf(td[1]) : null;
}
/** The one-name predicate: the subject cell names `want`; `avoid` (when it differs) prints nowhere. */
function nameFaults(html, want, avoid) {
  const f = [];
  const cell = subjectCell(html);
  if (cell === null) return ['no [data-csc-row="subject"] row'];
  if (!cell.includes(want)) f.push(`the subject row reads "${cell}" (want "${want}")`);
  if (avoid && avoid !== want && textOf(html).includes(avoid)) f.push(`"${avoid}" prints on the tab`);
  return f;
}

const arms = [];
const names = [['BA', 'BA_US_Equity'], ['VLO', 'VLO_US_Equity']];
// Arm 1 -- one name.
{
  const f = [];
  const tally = [];
  for (const [n, key] of names) {
    try {
      const peers = load(`peers.${key}.json`);
      const overlay = load(`overlay.${key}.json`);
      const want = overlay.display_name;
      const avoid = peers.subject && peers.subject.name;
      const html = render(peers, overlay, key);
      f.push(...nameFaults(html, want, avoid).map((x) => `${n}: ${x}`));
      tally.push(`${n} "${subjectCell(html)}"`);
    } catch (e) { f.push(`${n}: RENDER ${first(e)}`); }
  }
  arms.push(['ONE NAME: the Peers subject row names the security by the header\'s served display_name; the raw peer name prints nowhere', f.length === 0,
    f.length ? f.join(' | ') : tally.join('; ')]);
}
// Arm 2 -- nothing invented.
{
  const f = [];
  try {
    const peers = load('peers.BA_US_Equity.json');
    const overlay = Object.assign(JSON.parse(JSON.stringify(load('overlay.BA_US_Equity.json'))), { display_name: null });
    const cell = subjectCell(render(peers, overlay, 'BA_US_Equity'));
    if (cell === null || !cell.includes(peers.subject.name)) f.push(`with no served display_name the subject row reads "${cell}" (want the served "${peers.subject.name}")`);
  } catch (e) { f.push('RENDER ' + first(e)); }
  arms.push(['NOTHING INVENTED: with no served display_name the subject row prints the served peer name', f.length === 0,
    f.length ? f.join(' | ') : 'falls back to the served peers.subject.name']);
}
// Arm 3 -- keep.
{
  const f = [];
  for (const rel of ['round29/checks/tabs/peersmenu.cjs', 'round22/checks/subjectrow.cjs']) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), encoding: 'utf8', timeout: 600000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) f.push(`${rel} rc=${r.status} ("${last.slice(0, 80)}")`);
  }
  arms.push(['KEEP: round29 peersmenu.cjs and round22 subjectrow.cjs exit 0', f.length === 0, f.length ? f.join(' | ') : '2 of 2 exit 0']);
}
// Arm 4 -- planted.
{
  const f = [];
  const row = (t) => `<table><tbody><tr data-csc-row="subject"><td>${t}</td><td>BA US</td></tr><tr data-csc-row="member"><td>Deere &amp; Company</td></tr></tbody></table>`;
  if (nameFaults(row('The Boeing Co (subject)'), 'The Boeing Co', 'BOEING CO/THE').length) f.push('good row rejected');
  if (nameFaults(row('BOEING CO/THE (subject)'), 'The Boeing Co', 'BOEING CO/THE').length === 0) f.push('the raw peer name accepted');
  if (nameFaults(row('The Boeing Co (subject)') + '<p>BOEING CO/THE</p>', 'The Boeing Co', 'BOEING CO/THE').length === 0) f.push('both names accepted');
  if (nameFaults('<table></table>', 'The Boeing Co', null).length === 0) f.push('a missing subject row accepted');
  arms.push(['PLANTED: the name predicate rejects the raw peer name, both names and a missing row; accepts the good row', f.length === 0,
    f.length ? f.join(' | ') : '3 rejected, 1 accepted']);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`ONE NAME FOR THE SUBJECT IN PEERS: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
