/**
 * r53a.cjs -- DSGN_AMGTV1 round 53 issuer CHECK (2.0.0_SA_COO~D): THE SEEKING ALPHA COLUMN DRAWS THE THREE SERVED STATES APART.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round53/checks/r53a.cjs"
 *
 * Why: PRD v0.18 SAUX-41 (FWD-27): "The column draws the three served states apart, in the served words: read (with its date),
 * checked with nothing new (with its date), and no record. 'No record' is never drawn as stale." Today the column prints
 * 'Not collected' for every state that is not read. The served shape (AMGT_RESAPP round 79 cc-3, live since the cc-7 redeploy):
 * every covered row of GET /freshness?view=page carries `seeking_alpha: {state, sentence, last_read, newest_job_finished_at,
 * newest_job_status}`, state one of read | checked | no_record.
 *
 * Input: the LIVE body read by the issuer from the deployed function (round53/served/freshness_page.json, 95 covered rows:
 * read 13, checked 15, no_record 67; one read row is served stale).
 *
 * Arms (each prints its evidence; exit 0 only on all three):
 *   1 THREE SERVED STATES: every covered row's Seeking Alpha cell (td[data-input="seekingalpha"]) carries
 *     data-sa-state="<served state>" and prints the served sentence verbatim, once; the per-state counts equal the served
 *     counts; no Seeking Alpha cell prints "Not collected".
 *   2 NO RECORD IS NEVER STALE, THE RULE STAYS THE SERVER'S: no row whose state is not read has a stale Seeking Alpha cell or a
 *     data-stale-input="seekingalpha" flag; every served-stale read row keeps its flag (control); the note above the table
 *     does not call Seeking Alpha not collected; the same body with `seeking_alpha` removed draws the column exactly as the
 *     base page does (the old body still reads).
 *   3 PLANTED: the graders refuse "Not collected" on a checked row, a no-record cell flagged stale, a sentence drawn twice
 *     and a missing data-sa-state.
 * Renders the REAL FreshnessView through round15/checks/_load.cjs (the API module stubbed); no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const D = path.join(__dirname, '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const BODY = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'served', 'freshness_page.json'), 'utf8'));
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(String(html).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const times = (hay, needle) => String(hay).split(needle).length - 1;

L.stubSource('src/api/endpoints/amgt-lead-panel', { getCoverageFreshness: () => null });
L.stubSource('src/api/endpoints/amgt-lead-panel.ts', { getCoverageFreshness: () => null });

/** Table lines of a rendered view: [{name, cell: {attrs, text} | null, staleSa: bool}]. */
function lines(html) {
  const body = String(html).split('<tbody>')[1] || '';
  const out = [];
  for (const tr of body.split('<tr').slice(1)) {
    const tds = tr.split('<td').slice(1);
    const name = tds.length ? text('<td' + tds[0].split('</td>')[0]) : '';
    const sa = tds.find((td) => /^[^>]*data-input="seekingalpha"/.test(td));
    let cell = null;
    if (sa) {
      const attrs = sa.slice(0, sa.indexOf('>'));
      cell = { attrs, text: text(sa.slice(sa.indexOf('>') + 1).split('</td>')[0]) };
    }
    out.push({ name, cell, staleSa: /data-stale-input="seekingalpha"/.test(tr) });
  }
  return out;
}
const attr = (attrs, name) => { const m = new RegExp(name + '="([^"]*)"').exec(attrs || ''); return m ? m[1] : null; };

const covered = BODY.rows.filter((r) => r.covered === true);
const servedName = (r) => r.name || r.security_key || 'Unnamed company';

function stateFaults(html, rows) {
  const f = [];
  const drawn = lines(html);
  const byName = new Map(drawn.map((l) => [l.name, l]));
  const counts = {};
  const want = {};
  for (const r of rows) {
    const sa = r.seeking_alpha || {};
    want[sa.state] = (want[sa.state] || 0) + 1;
    const l = byName.get(servedName(r));
    if (!l || !l.cell) { f.push(`${servedName(r)}: no Seeking Alpha cell`); continue; }
    const st = attr(l.cell.attrs, 'data-sa-state');
    if (st !== sa.state) f.push(`${servedName(r)}: data-sa-state ${JSON.stringify(st)} (served ${sa.state})`);
    else counts[st] = (counts[st] || 0) + 1;
    if (times(l.cell.text, sa.sentence) !== 1) f.push(`${servedName(r)}: the served sentence is printed ${times(l.cell.text, sa.sentence)} time(s): "${l.cell.text.slice(0, 90)}"`);
    if (/not collected/i.test(l.cell.text)) f.push(`${servedName(r)}: the cell prints Not collected`);
  }
  for (const k of Object.keys(want)) if ((counts[k] || 0) !== want[k]) f.push(`state ${k}: ${counts[k] || 0} cell(s) carry it of ${want[k]} served`);
  return f;
}
function staleFaults(html, rows) {
  const f = [];
  const byName = new Map(lines(html).map((l) => [l.name, l]));
  for (const r of rows) {
    const sa = r.seeking_alpha || {};
    const l = byName.get(servedName(r));
    if (!l) continue;
    const servedStale = (r.stale_inputs || []).includes('seekingalpha');
    if (sa.state !== 'read') {
      if (l.cell && attr(l.cell.attrs, 'data-state') === 'stale') f.push(`${servedName(r)} (${sa.state}): the cell is drawn stale`);
      if (l.staleSa) f.push(`${servedName(r)} (${sa.state}): Seeking Alpha is flagged stale`);
    } else if (servedStale && !l.staleSa) f.push(`${servedName(r)}: the served stale flag on a read row is not drawn`);
  }
  return f;
}

const arms = [];
let FV;
const loadFaults = [];
try { FV = L.source('src/pages/Freshness/Freshness.tsx').FreshnessView; } catch (e) { loadFaults.push('LOADER: Freshness.tsx ' + String(e.message).split('\n')[0]); }
const render = (rows) => L.render(FV, { rows, lists: BODY.lists, initialSort: 'name' });
let live = null;
if (FV) { try { live = render(BODY.rows); } catch (e) { loadFaults.push('RENDER FAILED ' + String(e.message).split('\n')[0]); } }
{
  const f = live ? stateFaults(live, covered) : loadFaults.slice();
  const tally = {};
  for (const r of covered) tally[r.seeking_alpha.state] = (tally[r.seeking_alpha.state] || 0) + 1;
  arms.push(['THREE SERVED STATES, IN THE SERVED WORDS', f.length === 0,
    f.length ? `${f.length} fault(s): ` + f.slice(0, 6).join(' | ') : `${covered.length} of ${covered.length} cells carry their served state and sentence once (${JSON.stringify(tally)}); none prints Not collected`]);
}
{
  const f = live ? staleFaults(live, covered) : loadFaults.slice();
  const servedStale = covered.filter((r) => (r.stale_inputs || []).includes('seekingalpha')).length;
  if (live) {
    const note = /data-slot="uncollected-note"[^>]*>([^<]*)</.exec(live);
    if (note && /Seeking Alpha/.test(note[1])) f.push(`the note above the table says: "${note[1]}"`);
    // the old body (no seeking_alpha) still reads as the base page draws it
    const old = BODY.rows.map((r) => { const c = { ...r }; delete c.seeking_alpha; return c; });
    try {
      const oldLines = lines(render(old));
      const byName = new Map(oldLines.map((l) => [l.name, l]));
      let bad = 0;
      for (const r of covered) {
        const l = byName.get(servedName(r));
        const st = r.inputs && r.inputs.seekingalpha ? r.inputs.seekingalpha.state : null;
        const wantText = st === 'not_collected' ? 'Not collected' : (r.inputs.seekingalpha.day || 'Never');
        if (!l || !l.cell || l.cell.text !== wantText) bad += 1;
      }
      if (bad) f.push(`${bad} cell(s) of the old body (no seeking_alpha) are not drawn as the base page draws them`);
    } catch (e) { f.push('old body RENDER FAILED ' + String(e.message).split('\n')[0]); }
  }
  arms.push(['NO RECORD IS NEVER STALE; THE RULE STAYS THE SERVER\'S', f.length === 0,
    f.length ? `${f.length} fault(s): ` + f.slice(0, 6).join(' | ') : `no checked or no-record row is drawn stale; ${servedStale} served-stale read row(s) keep the flag; the note does not call Seeking Alpha uncollected; the old body draws as before`]);
}
{
  const f = [];
  const one = (name, st, words, extra) => `<tbody><tr data-stale="false"><td>${name}</td><td data-input="seekingalpha" data-state="${extra || 'collected'}"${st === null ? '' : ` data-sa-state="${st}"`}>${words}</td></tr>`;
  const rRead = { name: 'A', covered: true, seeking_alpha: { state: 'read', sentence: 'Seeking Alpha last read 2026-09-22.' }, stale_inputs: [] };
  const rChk = { name: 'B', covered: true, seeking_alpha: { state: 'checked', sentence: 'Seeking Alpha was checked on 2026-10-05 and no article is held for this company.' }, stale_inputs: [] };
  const rNo = { name: 'C', covered: true, seeking_alpha: { state: 'no_record', sentence: 'No Seeking Alpha collection record is held for this company yet.' }, stale_inputs: [] };
  const rows3 = [rRead, rChk, rNo];
  const clean = one('A', 'read', rRead.seeking_alpha.sentence) + one('B', 'checked', rChk.seeking_alpha.sentence).replace('<tbody>', '') + one('C', 'no_record', rNo.seeking_alpha.sentence).replace('<tbody>', '');
  if (stateFaults(clean, rows3).length) f.push('the clean form refused: ' + stateFaults(clean, rows3)[0]);
  if (staleFaults(clean, rows3).length) f.push('the clean form refused on stale: ' + staleFaults(clean, rows3)[0]);
  if (!stateFaults(clean.replace(rChk.seeking_alpha.sentence, 'Not collected'), rows3).length) f.push('Not collected on a checked row accepted');
  if (!staleFaults(clean.replace('data-state="collected" data-sa-state="no_record"', 'data-state="stale" data-sa-state="no_record"'), rows3).length) f.push('a no-record cell drawn stale accepted');
  if (!stateFaults(clean.replace(rRead.seeking_alpha.sentence, rRead.seeking_alpha.sentence + ' ' + rRead.seeking_alpha.sentence), rows3).length) f.push('a sentence drawn twice accepted');
  if (!stateFaults(clean.replace(' data-sa-state="checked"', ''), rows3).length) f.push('a missing data-sa-state accepted');
  arms.push(['PLANTED', f.length === 0, f.length ? f.join(' | ') : '4 of 4 faults refused; the clean form admitted']);
}

const TITLE = 'THE SEEKING ALPHA COLUMN DRAWS THE THREE SERVED STATES APART';
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length && arms.length === 3 ? 0 : 1);
