/**
 * r59.cjs -- DSGN_AMGTV1 round 59 issuer CHECK (2.0.0_SA_COO~D1): the walk findings SAW-01..23, one arm group per cell.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round59/checks/r59.cjs" <A|B|C|D|E|F>
 *
 * Why: Andrew-direct ~05:0xZ-05:1xZ (record @1725deb826); register docs/briefs/dsgn-amgtv1-security-analysis-walk-findings-20261009.json;
 * ruled in ledger/ROUND_ANALYSIS.round58.md @23fec8836a (R1-R5). Each arm reads the SOURCE of the cell's owned files for the structural
 * fact the ruling names (a literal gone, a mount moved, a fold present). The behaviour is graded at the round's close by a signed-in walk
 * read against the register; this check is the cell's mechanical floor, not its acceptance.
 * Every cell group ends with a PLANTED arm proving its graders refuse the base form and admit the clean form. Exit 0 only on all arms.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const SA = path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis');
const read = (rel) => { try { return fs.readFileSync(path.join(SA, rel), 'utf8'); } catch (e) { return null; } };
const count = (s, needle) => (s ? s.split(needle).length - 1 : 0);
const TABS = ['tabs/ThesisTab.tsx', 'tabs/ExecManagementTab.tsx', 'tabs/PeersTab.tsx', 'tabs/ModelTab.tsx', 'tabs/PostureTab.tsx'];

// ---- graders (pure over source text) ----
const G = {
  spineLegendGone: (t) => (t === null ? ['TimelinePanel.tsx missing'] : ['partly searched', 'not searched'].filter((w) => t.includes(w)).map((w) => `"${w}" still in TimelinePanel`)),
  earningsLineGone: (t) => (t && t.includes('Earnings dates are not on file') ? ['"Earnings dates are not on file" still printed'] : []),
  topDays: (t) => (t && /data-timeline-top-day/.test(t) && /(breakout_ratio|z_score)/.test(t.replace(/^\s*(breakout_ratio|z_score)\??:.*$/gm, '')) ? [] : ['no data-timeline-top-day marked from served breakout_ratio / z_score']),
  eventLabels: (t) => (t && /data-timeline-event-label/.test(t) && /lead_headline/.test(t) ? [] : ['no data-timeline-event-label carrying the served lead_headline']),
  cloudTop: (t) => { const m = t && /\.slice\(\s*0\s*,\s*(\d+)\s*\)/.exec(t); return m && Number(m[1]) <= 12 ? [] : ['the word cloud does not show only its top terms (slice(0, N<=12))']; },
  oneNewsSurface: (hb, tb) => {
    const f = [];
    if (!hb || !/data-news-surface/.test(hb)) f.push('HeaderBrief draws no data-news-surface');
    if (!hb || !/mentions/.test(hb)) f.push('the news surface does not order by the served mentions');
    if (!hb || !/(new Set|\.has\()/.test(hb)) f.push('the news surface does not de-duplicate headlines');
    if (tb && /In the news on/.test(tb)) f.push('TopBand still draws "In the news on <day>"');
    return f;
  },
  structure: (sa, so, news, tabs) => {
    const f = [];
    if (!news) f.push('no tabs/NewsTab.tsx');
    else if (!/<TimelinePanel/.test(news) || !/<HeaderBrief/.test(news)) f.push('NewsTab does not mount TimelinePanel and HeaderBrief');
    if (so && (/<TimelinePanel/.test(so) || /<HeaderBrief/.test(so))) f.push('the identity header still mounts the spine or the feed');
    if (so && /<CompanyLine/.test(so)) f.push('the description is still printed twice (CompanyLine mounted)');
    if (so && /Readings of /.test(so)) f.push('the chatter strip still prints "Readings of ..."');
    if (so && /machine's view for a person/.test(so)) f.push('the overlay still carries the machine-view subtitle');
    if (sa && /<TopBand/.test(sa)) f.push('SecurityAnalysis still mounts the standalone TopBand card');
    if (sa) { const ip = sa.indexOf('<InputProvenance'); const tn = sa.indexOf('<TabNavigation'); if (ip !== -1 && tn !== -1 && ip < tn) f.push('the data-sources panel still sits above the tabs'); }
    tabs.forEach(([n, t]) => { if (t && /<IdentityLine/.test(t)) f.push(`${n} still mounts IdentityLine`); });
    return f;
  },
  thesisPosture: (th, ds, po, st) => {
    const f = [];
    if (!ds || !/data-absence-fold/.test(ds)) f.push('DossierSections does not fold its served reasons under one line (data-absence-fold)');
    if (ds && !/What is not on file/.test(ds)) f.push('the dossier fold line is not "What is not on file"');
    if (!po || !/data-absence-fold/.test(po)) f.push('PostureTab does not fold its absences (data-absence-fold)');
    if (th && /machine's view for a person/.test(th)) f.push('ThesisTab still carries the machine-view subtitle');
    if (po && /machine's view for a person/.test(po)) f.push('PostureTab still carries the machine-view subtitle');
    if (!st || !/<details/.test(st)) f.push('SegmentTable does not fold its notes');
    return f;
  },
  execPeers: (ex, pe) => {
    const f = [];
    if (ex && /per Bloomberg, not the filing/.test(ex)) f.push('Exec still prints "per Bloomberg, not the filing" per row');
    if (ex && /This table is the Bloomberg fallback/.test(ex)) f.push('Exec still prints "This table is the Bloomberg fallback"');
    if (!ex || !/data-absence-fold/.test(ex)) f.push('Exec does not fold its absences (data-absence-fold)');
    if (pe && /Not averaged:/.test(pe)) f.push('Peers still prints "Not averaged: ..."');
    if (!pe || !/data-absence-fold/.test(pe)) f.push('Peers does not fold its absences (data-absence-fold)');
    return f;
  },
  modelTilesPrint: (mt, hc, stt, pr) => {
    const f = [];
    if (!mt || !/data-model-summary/.test(mt)) f.push('ModelTab opens on no curated summary (data-model-summary)');
    if (!mt || !/data-model-full-grid/.test(mt)) f.push('ModelTab does not fold the full grid (data-model-full-grid)');
    if (mt && count(mt, 'The research team has no') > 1) f.push('"The research team has no ..." is still composed more than once');
    if (!hc || !/data-tile-absent/.test(hc)) f.push('HeaderCards draws no quiet absent tile (data-tile-absent)');
    if (stt && /Not shown: Bloomberg does not confirm this figure/.test(stt)) f.push('a tile body still reads "Not shown: Bloomberg does not confirm ..."');
    if (pr && /Print preview -- \{securityKey\}/.test(pr)) f.push('the print preview title still uses the raw security key');
    return f;
  },
};

function arms(cell) {
  const out = [];
  const push = (name, f) => out.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
  if (cell === 'A') {
    const tp = read('components/TimelinePanel.tsx'); const wc = read('components/TimelineWordCloud.tsx');
    push('NO COLLECTION LEGEND, NO EARNINGS DISCLAIMER', [...G.spineLegendGone(tp), ...G.earningsLineGone(tp)]);
    push('TOP DAYS AND LABELLED EVENTS', [...G.topDays(tp), ...G.eventLabels(tp)]);
    push('THE WORD CLOUD SHOWS ITS TOP TERMS', G.cloudTop(wc));
    const p = [];
    if (!G.spineLegendGone('x partly searched').length) p.push('legend fault admitted');
    if (G.spineLegendGone('clean').length) p.push('clean legend refused');
    if (!G.topDays('articles_total').length) p.push('no top days admitted');
    if (G.topDays('d.breakout_ratio > 2 && <g data-timeline-top-day />').length) p.push('clean top days refused');
    if (!G.cloudTop('terms.map').length || G.cloudTop('terms.slice(0, 10)').length) p.push('word-cloud grader wrong');
    push('PLANTED', p);
  } else if (cell === 'B') {
    const hb = read('components/HeaderBrief.tsx'); const tb = read('components/TopBand.tsx');
    push('ONE NEWS SURFACE, EACH HEADLINE ONCE, BY MENTIONS', G.oneNewsSurface(hb, tb));
    const p = [];
    if (!G.oneNewsSurface('<ul>', 'In the news on').length) p.push('base form admitted');
    if (G.oneNewsSurface('<section data-news-surface> new Set() item.mentions', 'export function CompanyLine').length) p.push('clean form refused');
    push('PLANTED', p);
  } else if (cell === 'C') {
    const sa = read('SecurityAnalysis.tsx'); const so = read('components/SecurityOverlay.tsx'); const nt = read('tabs/NewsTab.tsx');
    push('TABS IN THE FIRST SCREEN, IDENTITY ONCE, PLUMBING OUT OF THE FACE', G.structure(sa, so, nt, TABS.map((t) => [t, read(t)])));
    const p = [];
    if (!G.structure('<TopBand /><InputProvenance /><TabNavigation />', '<HeaderBrief /><CompanyLine />', null, [['t', '<IdentityLine />']]).length) p.push('base form admitted');
    if (G.structure('<TabNavigation /><details><InputProvenance /></details>', '<HeaderCards />', '<TimelinePanel /><HeaderBrief />', [['t', '<ThesisCards />']]).length) p.push('clean form refused');
    push('PLANTED', p);
  } else if (cell === 'D') {
    push('EACH ABSENCE ONCE ON THESIS AND POSTURE', G.thesisPosture(read('tabs/ThesisTab.tsx'), read('components/DossierSections.tsx'), read('tabs/PostureTab.tsx'), read('components/SegmentTable.tsx')));
    const p = [];
    if (!G.thesisPosture("a machine's view for a person", '{s.reason}', 'No call', '<p>').length) p.push('base form admitted');
    if (G.thesisPosture('<ThesisCards />', '<details data-absence-fold><summary>What is not on file</summary>', '<details data-absence-fold>', '<details>').length) p.push('clean form refused');
    push('PLANTED', p);
  } else if (cell === 'E') {
    push('EACH ABSENCE ONCE ON EXEC AND PEERS', G.execPeers(read('tabs/ExecManagementTab.tsx'), read('tabs/PeersTab.tsx')));
    const p = [];
    if (!G.execPeers('per Bloomberg, not the filing', 'Not averaged: currency').length) p.push('base form admitted');
    if (G.execPeers('<details data-absence-fold>', '<details data-absence-fold>').length) p.push('clean form refused');
    push('PLANTED', p);
  } else if (cell === 'F') {
    push('MODEL SUMMARY FIRST, QUIET TILES, NAMED PRINT TITLE', G.modelTilesPrint(read('tabs/ModelTab.tsx'), read('components/HeaderCards.tsx'), read('components/StatTile.tsx'), read('components/PrintExportAction.tsx')));
    const p = [];
    if (!G.modelTilesPrint('<table>', '<div>', 'Not shown: Bloomberg does not confirm this figure', 'Print preview -- {securityKey}').length) p.push('base form admitted');
    if (G.modelTilesPrint('<section data-model-summary /><details data-model-full-grid>', '<span data-tile-absent>', 'formatStatValue', 'Print preview -- {title}').length) p.push('clean form refused');
    push('PLANTED', p);
  } else {
    console.log('usage: r59.cjs <A|B|C|D|E|F>'); process.exit(2);
  }
  return out;
}

const cell = (process.argv[2] || '').toUpperCase();
const res = arms(cell);
let pass = 0;
for (const [name, ok, ev] of res) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 59 CELL ${cell}: ${pass} of ${res.length} arms`);
process.exit(pass === res.length ? 0 : 1);
