/**
 * repairs38.cjs -- DSGN_AMGTV1 round 38, the REPAIR CELL check (issuer 2.0.0_SA_COO~D): WHAT CHANGED USES THE SHARED STATES, EVERY
 * CARD ENDS IN THE SHARED FOOTER, THE PAGE ENDS ON THE SHARED END LINE.
 *
 * Usage (from the directory whose portal/ is the checkout under test -- the repository root for a worker,
 *   `cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round38/checks/
 *   repairs/repairs38.cjs"`; C:/tmp/wk-dsgn-amgtv1-92 for the issuer). Fixtures resolve from this file's own location; the portal
 *   resolves from the cwd (cwd/portal).
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (round15/checks/_load.cjs) is honoured for every render here; the render child
 *   (_render38.cjs beside this file) and the KEEP children inherit the same environment. A worker never sets it.
 * Fixtures (all served captures, nothing captured this round): round37/fixtures {overlay,thesis,peers}.{MSFT,AMD}_US_Equity.json,
 *   chatter.30.json; round35/fixtures {thesis,versions,compare}.BA_US_Equity.json, timeline.{MSFT,AMD,BA}_US_Equity.json;
 *   round29/fixtures/leadprice/rankings.trending.price.live.json.
 * Why (the CTO's round-38 list, ledger/CTO_LIST_ROUND38.md @0a865d7e8f):
 *   1 FWD-19 "What changed renders the shared PanelLoading and PanelError; a 500 shows the designed error, never a skeleton". Live:
 *     round37/walk/read-20261005T054042Z/fwd19-BA-US-what-changed-error-panel.png (skeleton bars on a 500; 06-fwd19-panels-BA-US.json
 *     logs 20+ compare GETs on one pair, the panel never settling). At base components/model/WhatChangedPanel.tsx hand-rolls its
 *     loading (a [data-panel-state="loading"] div of three bg-lightGray bars, in DefaultPair and PairFace) and its error (a bold <p>),
 *     and DefaultPair answers a failed probe by mounting PairFace on the SAME pair: PairFace's new observer refetches the errored
 *     query, which goes back to pending, and DefaultPair -- observing the same query -- draws its skeleton again (the loop).
 *   2 FWD-11 "every card ends in the shared footer, reading as a time and a source, from served fields only; a card with no served
 *     time or source prints no footer line (FWD-27); the page ends with the shared 'End of Security Analysis. Data as of <served
 *     date>.' line". The reference pages: every /market and /philosophy card ends in src/ui/components/panels/PanelFooter.tsx
 *     ("<formatPanelTimestamp> | Source: ..."), and both pages end in src/ui/components/PageEnd.tsx (MarketPerformance.tsx:155,
 *     CapitalMarketAssumptions.tsx:149; Positioning/shared/PageEnd.tsx re-exports it). At base no Security Analysis file renders
 *     either one; LeadPanel.tsx hand-rolls its "<day> | Source: ..." caption.
 * THE CARD TABLE, the served fields and the region of each card: _cards38.cjs (CARDS, cardRegions); printed below as the CENSUS.
 * Renders (the child _render38.cjs; the REAL page sources through round15/checks/_load.cjs):
 *   changed  WhatChangedPanel over the BA /thesis + /versions, its compare read LOADING, ERROR, ERROR REMOUNTED (the walk's loop:
 *            first observer of a pair reads the settled error, a later observer of the same pair reads pending) and SERVED.
 *   page     the REAL SecurityAnalysis.tsx: Security mode, MSFT / AMD / BA x the five tabs (15 renders), and Universe mode, the
 *            Price and the Chatter face (2 renders).
 * Definitions:
 *   SKELETON (arm 1): markup a shared state never emits in this render (the loader stubs PanelLoading / PanelError to
 *     data-stub="<name>"): [data-panel-state], aria-busy="true", or a h-4 w-full rounded-[2px] bar.
 *   WANTS A FOOTER (arm 2): the card serves at least one time field AND one source field (_cards38.cjs CARDS).
 *   THE FOOTER IS RIGHT (arm 2): exactly one shared PanelFooter in the card (nested cards cut out), whose time (its `timestamp`
 *     when that parses, else `dataAsOf` -- PanelFooter's own order) is a served time of the card (same instant, or the same day for
 *     a bare day), whose printed text reads "<time> | Source: ...", whose `content` reads "Source: <words>" naming EVERY served source
 *     value of the card (the page's PUBLISHER_NAMES name, a significant token, or the value itself when it is not a code) and
 *     printing no served code raw and no machine token; nothing visible follows it inside the card; no other "<x> | Source:" line
 *     sits in the card; no SmartPanelFooter (it stamps the data manifest's time, never a served field of this page).
 *   NO FOOTER LINE (arm 2): a card that does not want a footer renders no PanelFooter, no SmartPanelFooter and no "<x> | Source:"
 *     line.
 *   THE END LINE (arm 3): exactly one shared PageEnd per page render, pageName "Security Analysis", printed "End of Security
 *     Analysis." plus " Data as of <words>." whose `dataAsOf` is a served date of the page (_cards38.cjs PAGE_TIMES); no visible
 *     text after it; no hand-rolled "End of Security Analysis". A date is REQUIRED where the page serves one in Security mode;
 *     in Universe mode a printed date must be served but none is required (blind spot below).
 * Arms:
 *   1  WHAT CHANGED USES THE SHARED STATES (FWD-19): LOADING renders PanelLoading and no SKELETON; ERROR and ERROR REMOUNTED render
 *      PanelError, no PanelLoading and no SKELETON; SERVED still renders the [data-what-changed-table] and neither state.
 *   2  EVERY CARD ENDS IN THE SHARED FOOTER (FWD-11, FWD-27): every located card of every render is graded (the header cards K/N/T
 *      on the Thesis render of each name); every expected card is located (K/N/T where the /overlay is served, the tab card in
 *      every render, W on BA Model, LEAD in Universe mode); at least one card wants a footer and at least one does not (else
 *      NOT_EXERCISED). The per-card table prints.
 *   3  THE PAGE ENDS ON THE SHARED END LINE: every one of the 17 page renders.
 *   4  KEEP: round37 repairs37.cjs; round36 repairs36.cjs; round35 changed35.cjs, cloud35.cjs, payload35.cjs; round34 labels34.cjs,
 *      repairs34.cjs, peername34.cjs; round29 timeline/chart.cjs exit 0 on the same tree.
 *   5  PLANTED: arm 1's grader flags a skeleton on error, a skeleton beside PanelError, a hand-rolled loading and an error with no
 *      PanelError, and accepts the shared states; arm 2's grader flags a footer with an invented date, an invented source, a raw
 *      code, a missing footer, a footer that is not last, a hand-rolled time|source line, a placeholder footer on a card that serves
 *      no source and a SmartPanelFooter, and accepts a good card and a footerless card that serves nothing; arm 3's grader flags a
 *      missing end line, two end lines, an end line that is not last, an invented date and a dateless end line on a dated page,
 *      and accepts the good end line.
 * Blind spots: the header cards are graded on one tab render per name (the header is the same element on every tab); the source
 *   words are graded for NAMING the served source, not for their prose; the time is graded as one of the card's served times, not
 *   the newest; the timeline serves no source field and What changed's sources are the /thesis figures' sources (the /compare
 *   serves only "pool"); Universe mode's end line needs no date (the shell holds no served read there: the Lead Panel owns its
 *   window); BA has no /overlay or /peers capture, so its header and Peers card read as serving nothing; the walk's retry window
 *   (react-query retry 2, ~3 s pending before the settled error) is not modelled -- the identity header has the same window and
 *   was graded DESIGNED; the PanelFooter is the dark band component -- its colour on a light card is FWD-12's read, not graded.
 * Prints INFO lines, the CENSUS, one line per arm and "WHAT CHANGED USES THE SHARED STATES, EVERY CARD ENDS IN THE SHARED FOOTER,
 * THE PAGE ENDS ON THE SHARED END LINE: <k> of 5 arms"; exit 0 only at 5 of 5. Static renders only; no network, no AWS, writes no
 * file.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const DROOT = path.join(__dirname, '..', '..', '..');
const PORTAL = path.join(process.cwd(), 'portal');
const SA = 'src/pages/SecurityAnalysis/';
const TITLE = 'WHAT CHANGED USES THE SHARED STATES, EVERY CARD ENDS IN THE SHARED FOOTER, THE PAGE ENDS ON THE SHARED END LINE';
const X = require(path.join(__dirname, '_cards38.cjs'));
const norm = X.norm;

if (!fs.existsSync(path.join(PORTAL, 'package.json'))) {
  console.log('LOADER ERROR: no portal/package.json under ' + process.cwd() + ' -- run from the directory whose portal/ is under test');
  process.exit(3);
}
const OVERRIDES = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) {
  const i = pair.indexOf('=');
  OVERRIDES[pair.slice(0, i)] = pair.slice(i + 1);
}
const readSource = (rel) => { try { return fs.readFileSync(OVERRIDES[rel] || path.join(PORTAL, rel), 'utf8'); } catch (e) { return null; } };

function child(mode) {
  const r = spawnSync(process.execPath, [path.join(__dirname, '_render38.cjs'), mode], { cwd: process.cwd(), env: process.env, encoding: 'utf8', timeout: 600000, maxBuffer: 512 * 1024 * 1024 });
  const lines = String(r.stdout || '').split('\n').filter((x) => x.startsWith('{'));
  if (!lines.length) return { error: `the ${mode} render child printed no result (rc=${r.status}; ${norm(String(r.stderr || r.stdout || '')).slice(0, 160)})` };
  try { return JSON.parse(lines[lines.length - 1]); } catch (e) { return { error: `the ${mode} render child printed unreadable JSON` }; }
}

// ==== arm 1 grader ================================================================================================================
const SKELETON = /data-panel-state="[^"]*"|aria-busy="true"|class="[^"]*\bh-4 w-full rounded-\[2px\][^"]*"/;
const STUB = (name) => new RegExp(`data-stub="${name}"`);
/** c = {name, html, stop}; kind from the name. */
function changedFaults(c) {
  if (c.stop) return [`${c.name}: ${c.stop}`];
  const html = c.html || '';
  const f = [];
  const sk = SKELETON.exec(html);
  const skel = sk ? `"${sk[0].slice(0, 60)}"` : null;
  if (/^LOADING/.test(c.name)) {
    if (!STUB('PanelLoading').test(html)) f.push(`${c.name}: renders no shared PanelLoading`);
    if (skel) f.push(`${c.name}: a hand-rolled skeleton (${skel}) rather than the shared PanelLoading`);
  } else if (/^ERROR/.test(c.name)) {
    if (!STUB('PanelError').test(html)) f.push(`${c.name}: renders no shared PanelError ("${norm(html.replace(/<[^>]*>/g, ' ')).slice(-90)}")`);
    if (STUB('PanelLoading').test(html)) f.push(`${c.name}: a 500 still shows a loading state (PanelLoading) beside or instead of the error`);
    if (skel) f.push(`${c.name}: a 500 shows a skeleton (${skel})`);
  } else {
    if (!/data-what-changed-table/.test(html)) f.push(`${c.name}: the What changed table no longer renders`);
    if (STUB('PanelError').test(html) || STUB('PanelLoading').test(html)) f.push(`${c.name}: a served compare renders a loading or error state`);
  }
  return f;
}

function keepsPassing(rels) {
  const faults = [];
  for (const rel of rels) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), env: process.env, encoding: 'utf8', timeout: 1800000, maxBuffer: 64 * 1024 * 1024 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) faults.push(`KEEP: ${rel} rc=${r.status} ("${last.slice(0, 100)}")`);
  }
  return faults;
}

// ==== renders =====================================================================================================================
const CH = child('changed');
const PG = child('page');
const PUBS = (PG && PG.pubs) || X.DEFAULT_PUBLISHERS;

// ---- INFO: the base fault sites (not graded) ----
{
  const SITES = [
    [SA + 'components/model/WhatChangedPanel.tsx', /data-panel-state="loading"|could not be loaded just now|if \(probe\.isError \|\| servesAnyMove/],
    [SA + 'components/LeadPanel.tsx', /\{sourceFooterContent\(fields\)\}|Articles collected, from the harvest/],
    [SA + 'SecurityAnalysis.tsx', /<\/TabNavigation>|tabContentRef\}>/],
  ];
  const hits = [];
  for (const [rel, re] of SITES) String(readSource(rel) || '').split(/\r?\n/).forEach((l, i) => { if (re.test(l)) hits.push(`${rel.replace(SA, '')}:${i + 1} ${norm(l).slice(0, 80)}`); });
  // Every page source (the checkout's, plus any override path under the page), harnesses excluded.
  const pageFiles = [];
  const walk = (dir, rel) => { for (const e of fs.readdirSync(dir, { withFileTypes: true })) { if (e.name.startsWith('__')) continue; const r = rel + e.name; if (e.isDirectory()) walk(path.join(dir, e.name), r + '/'); else if (/\.tsx$/.test(e.name)) pageFiles.push(SA + r); } };
  try { walk(path.join(PORTAL, SA), ''); } catch (e) { /* no page */ }
  for (const k of Object.keys(OVERRIDES)) if (k.startsWith(SA) && /\.tsx$/.test(k) && !pageFiles.includes(k)) pageFiles.push(k);
  const uses = ['PanelFooter', 'PageEnd', 'PanelLoading', 'PanelError'].map((n) => {
    const files = pageFiles.filter((rel) => new RegExp(`<${n}\\b`).test(String(readSource(rel) || ''))).map((rel) => rel.replace(SA, ''));
    return `${n} in ${files.length ? files.join(', ') : 'no file'}`;
  });
  console.log(`INFO base fault-site census (not graded): ${hits.length} line(s)${hits.length ? ': ' + hits.join(' | ') : ''}`);
  console.log(`INFO shared-component use (JSX, not graded): ${uses.join('; ')}`);
}

const arms = [];
// ---- arm 1 ----
{
  const f = [];
  if (CH.error) f.push(CH.error);
  const cases = CH.cases || [];
  if (!CH.error && cases.length !== 4) f.push(`${cases.length} of 4 What changed cases rendered`);
  for (const c of cases) f.push(...changedFaults(c));
  const read = cases.map((c) => `${c.name}: ${['PanelLoading', 'PanelError'].filter((n) => STUB(n).test(c.html || '')).join('+') || 'no shared state'}${SKELETON.test(c.html || '') ? ' + SKELETON' : ''}`);
  arms.push(['WHAT CHANGED USES THE SHARED STATES: loading renders PanelLoading, a failed compare renders PanelError and never a skeleton (settled and remounted), a served compare still draws its table', f.length === 0,
    (f.length ? `${f.length} fault(s): ${f.join(' | ')}` : `${cases.length} of ${cases.length} cases`) + ` [${read.join('; ')}]`]);
}
// ---- arm 2 (+ the census) ----
const CENSUS = [];
{
  const f = [];
  if (PG.error) f.push(PG.error);
  const renders = PG.renders || [];
  if (!PG.error && renders.length !== 17) f.push(`${renders.length} of 17 page renders`);
  let wantN = 0;
  let noN = 0;
  for (const r of renders) {
    if (r.stop) { f.push(`${r.label}: ${r.stop}`); continue; }
    const tree = X.parse(r.html);
    const regions = X.cardRegions(tree, r.mode);
    const ids = regions.map((g) => g.id);
    const expect = ['TAB'];
    if (r.mode === 'security' && r.served.includes('overlay')) expect.push('K', 'N', 'T');
    if (r.mode === 'universe') expect.push('LEAD');
    if (r.key === 'BA_US_Equity' && r.tab === 'model') expect.push('W');
    for (const id of expect) if (!ids.includes(id)) f.push(`${r.label}: card ${id} not located in the render (NOT_EXERCISED for it)`);
    for (const g of regions) {
      if (['K', 'N', 'T'].includes(g.id) && r.tab !== 'thesis') continue;
      const id = g.id === 'TAB' ? r.tab : g.id;
      const fields = r.fields[id];
      if (!fields) continue;
      const cardId = g.id === 'LEAD' ? (r.subject === 'PRICE' ? 'LEAD_PRICE' : 'LEAD_CHATTER') : id;
      const name = `${r.mode === 'universe' ? 'universe ' + r.subject : r.key.split('_')[0]} ${X.CARDS[cardId].name}`;
      const res = X.gradeCard(tree, g, regions, fields, PUBS, name);
      const wants = fields.times.length > 0 && fields.sources.length > 0;
      if (wants) wantN += 1; else noN += 1;
      f.push(...res.faults);
      const tf = Object.keys(fields.timesBy)[0];
      const newest = (vals) => vals.slice().sort((a, b) => { const ta = X.timeOf(a); const tb = X.timeOf(b); return (ta.ms !== null ? ta.ms : Date.parse(`${ta.day}T21:00:00Z`)) - (tb.ms !== null ? tb.ms : Date.parse(`${tb.day}T21:00:00Z`)); }).pop();
      const sf = Object.keys(fields.sourcesBy);
      CENSUS.push(`${name} -> time ${tf ? `${tf} (newest "${newest(fields.timesBy[tf])}")` : 'NONE SERVED'}; source ${sf.length ? sf.map((k) => `${k} ${fields.sourcesBy[k].map((v) => `"${v}"`).join('/')}`).join(', ') : 'NONE SERVED'}; wants footer ${wants ? 'YES' : 'no'}; renders footer ${res.footer ? `yes ("${res.printed[0].slice(0, 90)}")` : 'no'}; ${res.faults.length ? 'FAULT' : 'ok'}`);
    }
  }
  if (!PG.error && (!wantN || !noN)) f.push(`NOT_EXERCISED: ${wantN} card(s) want a footer, ${noN} do not -- both kinds are needed`);
  arms.push(['EVERY CARD ENDS IN THE SHARED FOOTER: a card serving a time and a source ends in one shared PanelFooter reading "<served time> | Source: <served source in words>"; a card serving neither prints no footer line', f.length === 0,
    (f.length ? `${f.length} fault(s): ${f.join(' | ')}` : `${CENSUS.length} of ${CENSUS.length} cards`) + ` [${wantN} want a footer, ${noN} do not]`]);
}
// ---- arm 3 ----
{
  const f = [];
  if (PG.error) f.push(PG.error);
  const renders = PG.renders || [];
  const shown = [];
  for (const r of renders) {
    if (r.stop) { f.push(`${r.label}: ${r.stop}`); continue; }
    const tree = X.parse(r.html);
    const res = X.gradePageEnd(tree, r.dates, r.label);
    // Universe mode: a printed date must be served, but none is required.
    if (r.mode === 'universe') res.faults = res.faults.filter((x) => !/prints no date though/.test(x));
    f.push(...res.faults);
    if (r.tab === 'thesis') shown.push(`${r.label}: "${(res.printed[0] || 'none').slice(0, 70)}"`);
  }
  arms.push(['THE PAGE ENDS ON THE SHARED END LINE: one shared PageEnd, last on the page, "End of Security Analysis. Data as of <served date in words>."', f.length === 0,
    (f.length ? `${f.length} fault(s): ${f.slice(0, 12).join(' | ')}${f.length > 12 ? ` | ... (${f.length - 12} more)` : ''}` : `${renders.length} of ${renders.length} renders`) + ` [${shown.join('; ')}]`]);
}
// ---- arm 4: KEEP ----
{
  const KEEP = ['round37/checks/repairs/repairs37.cjs', 'round36/checks/repairs/repairs36.cjs', 'round35/checks/changed/changed35.cjs', 'round35/checks/cloud/cloud35.cjs',
    'round35/checks/words/payload35.cjs', 'round34/checks/collage/labels34.cjs', 'round34/checks/repairs/repairs34.cjs',
    'round34/checks/names/peername34.cjs', 'round29/checks/timeline/chart.cjs'];
  const f = keepsPassing(KEEP);
  arms.push(['KEEP: round37 repairs37, round36 repairs36, round35 changed35/cloud35/payload35, round34 labels34/repairs34/peername34 and round29 timeline/chart.cjs exit 0 on the same tree', f.length === 0,
    f.length ? f.join(' | ') : `${KEEP.length} of ${KEEP.length} exit 0`]);
}
// ---- arm 5: PLANTED ----
{
  const f = [];
  let bad = 0; let rej = 0; let good = 0; let acc = 0;
  const R = (label, faults, why) => { bad += 1; if (faults.some((x) => why.test(x))) rej += 1; else f.push(`"${label}" not flagged for its reason (${faults.length ? faults[0] : 'accepted'})`); };
  const A = (label, faults) => { good += 1; if (!faults.length) acc += 1; else f.push(`"${label}" rejected: ${faults[0]}`); };
  // arm 1's grader
  const SK = '<div data-panel-state="loading" role="status" aria-busy="true"><div class="h-4 w-full rounded-[2px] bg-x"></div></div>';
  const cj = (name, body) => changedFaults({ name, html: `<section data-what-changed="">${body}</section>`, stop: null });
  R('a skeleton on error', cj('ERROR', SK), /a 500 shows a skeleton/);
  R('a skeleton beside the shared error', cj('ERROR', `<div data-stub="PanelError">x</div>${SK}`), /a 500 shows a skeleton/);
  R('a hand-rolled loading', cj('LOADING', SK), /renders no shared PanelLoading/);
  R('an error with no PanelError', cj('ERROR', '<p>What changed could not be loaded just now.</p>'), /renders no shared PanelError/);
  A('the shared error', cj('ERROR', '<div data-stub="PanelError"><span data-stub-text="message">What changed could not be loaded.</span></div>'));
  A('the shared loading', cj('LOADING', '<div data-stub="PanelLoading"><span data-stub-text="label">Loading what changed</span></div>'));
  // arm 2's grader
  const FIELDS = { times: ['2026-10-04T19:56:35Z'], sources: ['bloomberg-dapi', 'BBG'], timesBy: {}, sourcesBy: {} };
  const NONE = { times: ['2026-10-03'], sources: [], timesBy: {}, sourcesBy: {} };
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
  const footer = (props, shown) => `<div data-check-shared="PanelFooter" data-check-props="${esc(JSON.stringify(props))}"><div><span>${shown || 'October 4th, 2026, 3:56p ET'}</span><span>|</span><span>${props.content}</span></div></div>`;
  const GOOD = footer({ content: 'Source: Bloomberg.', timestamp: '2026-10-04T19:56:35Z' });
  const page = (card) => `<div><div data-stub="PageHeaderCleanBadge"></div><div data-stub="TabNavigation"></div><div><div data-stub="Panel"><div data-stub="PanelContent"><p>Fiscal figures</p></div>${card}</div></div></div>`;
  const gj = (card, fields) => { const t = X.parse(page(card)); const rs = X.cardRegions(t, 'security'); const g = rs.find((x) => x.id === 'TAB'); return g ? X.gradeCard(t, g, rs, fields || FIELDS, PUBS, 'planted').faults : ['no TAB region']; };
  A('a good card: "October 4th, 2026, 3:56p ET | Source: Bloomberg." last in the card', gj(GOOD));
  A('a card serving no source with no footer', gj('', NONE));
  R('a footer with an invented date', gj(footer({ content: 'Source: Bloomberg.', timestamp: '2026-10-05T12:00:00Z' }, 'October 5th, 2026, 8:00a ET')), /footer's time "2026-10-05T12:00:00Z" is not a served time/);
  R('a footer with an invented source', gj(footer({ content: 'Source: FactSet.', timestamp: '2026-10-04T19:56:35Z' })), /does not name the served source "bloomberg-dapi"/);
  R('a footer printing the served code raw', gj(footer({ content: 'Source: bloomberg-dapi, BBG.', timestamp: '2026-10-04T19:56:35Z' })), /prints the served code "bloomberg-dapi" raw/);
  R('a card with no footer', gj(''), /no shared footer, though the card serves a time/);
  R('a footer that is not last', gj(GOOD + '<p>Refreshing an input</p>'), /does not end in its footer -- "Refreshing an input"/);
  R('a hand-rolled time | source line', gj('<p>October 4th, 2026 | Source: Bloomberg</p>'), /hand-rolled time \| source line/);
  R('a placeholder footer on a card serving no source', gj(footer({ content: 'Source: not stated.', dataAsOf: '2026-10-03' }, 'October 3rd, 2026, 5:00p ET'), NONE), /prints a footer .* though the card serves no source/);
  R('a SmartPanelFooter', gj(`<div data-check-shared="SmartPanelFooter" data-check-props="{}"><div>x | Source: Bloomberg.</div></div>`), /SmartPanelFooter stamps the data manifest/);
  // arm 3's grader
  const END = (asOf, words) => `<div data-check-shared="PageEnd" data-check-props="${esc(JSON.stringify({ pageName: 'Security Analysis', dataAsOf: asOf }))}"><div data-page-end="">End of Security Analysis.${words ? ` Data as of ${words}.` : ''}</div></div>`;
  const pj = (body, dates) => X.gradePageEnd(X.parse(`<div><div data-stub="TabNavigation"></div><div><p>tab</p></div>${body}</div>`), dates || ['2026-10-02'], 'planted').faults;
  A('the good end line', pj(END('2026-10-02', 'October 2nd, 2026, 5:00p ET')));
  R('a missing end line', pj(''), /renders 0 times/);
  R('two end lines', pj(END('2026-10-02', 'October 2nd, 2026, 5:00p ET') + END('2026-10-02', 'October 2nd, 2026, 5:00p ET')), /renders 2 times/);
  R('an end line that is not last', pj(END('2026-10-02', 'October 2nd, 2026, 5:00p ET') + '<p>More</p>'), /is not at the end -- "More"/);
  R('an end line with an invented date', pj(END('2026-10-05', 'October 5th, 2026, 5:00p ET')), /date "2026-10-05" .* is not a served date/);
  R('a dateless end line on a dated page', pj(END(null, null)), /prints no date though the page serves one/);
  arms.push(['PLANTED: the three graders flag their planted faults (skeleton on error, skeleton beside the error, hand-rolled loading, error without PanelError; invented date, invented source, raw code, missing footer, footer not last, hand-rolled line, placeholder footer, SmartPanelFooter; missing, doubled, not-last, invented-date and dateless end line) and accept the good shapes', f.length === 0,
    f.length ? f.join(' | ') : `${rej} of ${bad} planted faults flagged for their reason; ${acc} of ${good} good shapes accepted`]);
}

console.log(`CENSUS (card -> served time field, served source field, footer), ${CENSUS.length} card read(s):`);
for (const line of CENSUS) console.log(`  ${line}`);
let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
