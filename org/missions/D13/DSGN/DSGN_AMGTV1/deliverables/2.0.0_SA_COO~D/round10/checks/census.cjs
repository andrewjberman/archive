/**
 * census.cjs -- DSGN_AMGTV1 round 6: THE INVERTED NON-PROSE CENSUS (round-2 analysis, the CVO's decision 2), plus round 4's
 * status-word class and the ticker's own metacharacter (round-3 analysis decision 2 and item 3), plus round 5's passage-id
 * and preset-code classes and the lead chart's generations line (round-4 analysis s.4 items 1 and 3).
 *
 * An INSTRUMENT for the CVO's FWD-11 judgment, not a pass/fail criterion. It lists every VISIBLE token on a surface that is
 * NOT ordinary prose -- a word, a number, a money figure, a date or a ticker -- with its count, so each is judged; a zero means
 * nothing non-prose is visible, not "none of the shapes we already knew". Collapsed <details> content is excluded (behind an
 * affordance a PM opens on purpose); attributes are free.
 * Usage (repo root): node <this file> [surface ...]   (default: every surface below)
 * round 7 (round-6 analysis ruling 1): the census covers EVERY walked name -- header-<NAME> and posture-<NAME> for VLO, INTU,
 * SAP GY and 992 HK -- plus `planted`, a 992 HK /thesis ISSUER VARIANT whose posture reason carries planted machine tokens
 * (PLANTED_REASON_TOKEN, model_block_ZZ.json, AMGT-zz-9, F9/G-99); any of them visible is counted under [planted].
 * round 5: `chart` is the lead panel's rank-history chart (its generations line); `posture-sap` is SAP GY's Posture tab.
 * The passage-id class (P + 4 digits) and the preset-code class (every fit preset and membership book the fixtures' posture
 * objects serve: DIVZ, IDVZ, PFDE, PFOE today) are counted like the status words: they pass the word/ticker classes.
 * Ordinary prose (after trimming surrounding punctuation ( ) [ ] , . ; : " ' ! ?):
 *   word      letters, optionally joined by ' or - (Valero, research, can't, long-term, BETTER)
 *   number    123 / 1,234 / 12.5 / -4.7% / 16.0x / 117B / 3.25M / 5.93B
 *   money     USD / EUR / ... are words; $18.9 / 382.86 are numbers
 *   date      2026-09-25 / 2026E / FY2025 / Q3
 *   ticker    1-6 upper-case letters or digits (VLO, 992, HK, BP)
 *   form      10-K / 10-Q / 20-F / 8-K
 *   glue      pure punctuation (--, ->, |, x, &, /)
 * Everything else is printed.
 */
const L = require('./_load.cjs');
const NAMES = { VLO: 'VLO_US_Equity', INTU: 'INTU_US_Equity', SAP: 'SAP_GY_Equity', HK: '992_HK_Equity' };
const ALL = ['lead', 'chart', 'thesis', 'model', 'exec', ...Object.keys(NAMES).flatMap((n) => ['header-' + n, 'posture-' + n]), 'planted'];
const want = process.argv.slice(2).length ? process.argv.slice(2) : ALL;
const bundles = {};
for (const k of ['VLO_US_Equity', 'WMB_US_Equity', 'INTU_US_Equity', 'SAP_GY_Equity', '992_HK_Equity']) bundles[k] = L.fixture(`thesisBundle.${k}.json`);
// ISSUER VARIANT (not served): 992 HK with a planted machine posture reason -- a correct page shows none of it
const PLANTED = 'no landed model_block_ZZ.json (AMGT-zz-9 record, F9/G-99) PLANTED_REASON_TOKEN';
bundles.PLANTED_992 = JSON.parse(JSON.stringify(bundles['992_HK_Equity']));
bundles.PLANTED_992.posture = Object.assign({}, bundles.PLANTED_992.posture, { reason: PLANTED });
const peers = {};
for (const k of ['VLO_US_Equity', 'WMB_US_Equity', 'INTU_US_Equity']) peers[k] = L.fixture(`peerSet.${k}.json`);
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: (k) => peers[k], useManagement: (k) => (bundles[k] || {}).management };
L.stubSource('src/pages/SecurityAnalysis/components/TimelinePanel.tsx', { TimelinePanel: () => null });
const strip = (html) => html.replace(/<details(?![^>]*\sopen)[^>]*>[\s\S]*?<\/details>/g, '');
const PROSE = [
  /^[A-Za-z]+(?:['’-][A-Za-z]+)*$/,
  /^[A-Za-z]+\(s\)?$/,
  /^[+-]?\$?\d[\d,]*(?:\.\d+)?(?:%|x|[KMBT])?$/,
  /^\d{4}-\d{2}-\d{2}$/, /^\d{4}E$/, /^FY\d{4}$/, /^Q[1-4]$/,
  // round 4 (decision 2): a Bloomberg ticker in its own exchange form keeps its "/" or "*" ("BP/ LN", "WALMEX* MM").
  /^[A-Z0-9]{1,8}[/*]?$/,
  /^\d{1,2}-[A-Z]$/,
  /^[-|>&/x*+=]+$/,
];
const STATUS_WORDS = /\b(REFUSED|ABSENT|SERVED|NOT_SERVED|UNRESOLVED|RESOLVED|PRESENT|COMPLETE|PENDING|EMPTY)\b|\bnot read\b/g;
// round 5: passage ids and preset / book codes -- the preset set is read from the fixtures' posture objects, never typed here.
// These two classes read the FULL visible text, collapsed <details> INCLUDED: the Posture cites they live in sit in a drawer
// the CVO opens on the walk, so a census blind to the drawer would read zero over the very lines round 5 rewrites.
const PASSAGE_IDS = /\bP\d{4}\b/g;
const presetCodes = new Set();
for (const bd of Object.values(bundles)) {
  const p = (bd && bd.posture) || {};
  for (const side of Object.values(p.fit || {})) for (const k of Object.keys((side && side.presets) || {})) presetCodes.add(k);
  for (const mem of [p.membership, p.comparable_membership]) {
    for (const k of [...((mem && mem.books) || []), ...Object.keys((mem && mem.holdings_source) || {})]) presetCodes.add(k);
  }
}
const PRESET_CODES = presetCodes.size ? new RegExp('\\b(' + [...presetCodes].join('|') + ')\\b', 'g') : /$^/g;
const PLANTED_TOKENS = /PLANTED_REASON_TOKEN|model_block_ZZ\.json|AMGT-zz-9|F9\/G-99/g;
const MACHINE_PHRASES = /the object|comparable selection|rung|log cap|cite\(s\)|bundles this page reads|on this name's peer set|validated \d+ of \d+ against its packs|covered|mention_score/gi;
function census(name, html) {
  const text = L.textOf(strip(html));
  const counts = {};
  let tokens = 0;
  for (const raw of text.split(/\s+/)) {
    const t = raw.replace(/^[(\["'“]+|[)\]"',.;:!?”]+$/g, '');
    if (!t) continue;
    tokens += 1;
    if (PROSE.some((re) => re.test(t))) continue;
    counts[t] = (counts[t] || 0) + 1;
  }
  // round 4 (round-3 analysis item 3): a STATUS-WORD class, which the word class above admits as prose because it is
  // letters -- an upper-case status label (REFUSED, ABSENT, SERVED ...) or the "not read" placeholder on the face.
  const status = text.match(STATUS_WORDS) || [];
  for (const w of status) counts['[status] ' + w] = (counts['[status] ' + w] || 0) + 1;
  const full = L.textOf(html);
  for (const w of full.match(PASSAGE_IDS) || []) counts['[passage] ' + w] = (counts['[passage] ' + w] || 0) + 1;
  for (const w of full.match(PRESET_CODES) || []) counts['[preset] ' + w] = (counts['[preset] ' + w] || 0) + 1;
  // round 6 (round-5 analysis ruling 5): the MACHINE-PHRASE class -- words that pass every class above but read as the
  // producer's internals, not a PM's: "the object", "comparable selection", "rung", "log cap", "cite(s)", "bundles this page
  // reads", "on this name's peer set", "validated N of N against its packs", a publisher "covered" a day (the producer's
  // search-reach word), and a served field name shown with its underscore (mention_score).
  for (const w of full.match(MACHINE_PHRASES) || []) counts['[phrase] ' + w.toLowerCase()] = (counts['[phrase] ' + w.toLowerCase()] || 0) + 1;
  for (const w of full.match(PLANTED_TOKENS) || []) counts['[planted] ' + w] = (counts['[planted] ' + w] || 0) + 1;
  const list = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  const n = list.reduce((a, [, c]) => a + c, 0);
  console.log(`${name}: ${n} non-prose token(s) of ${tokens} (status words ${status.length}) ${list.length ? JSON.stringify(list.slice(0, 40)) : ''}`);
  return n;
}
let total = 0;
const safe = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } };
for (const s of want) {
  let html = '';
  if (s === 'header') html = safe(() => { const m = L.source('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: L.fixture('overlay.VLO_US_Equity.json'), onBack: () => {}, onRefresh: () => {} }); });
  if (s === 'lead') html = safe(() => { const r = L.fixture('rankings.TRENDING_PRICE.json'); const lp = L.source('src/pages/SecurityAnalysis/components/LeadPanel.tsx'); const e = (x) => '<p>' + String(x || '').replace(/</g, '&lt;') + '</p>'; return e(lp.sourceFooterContent(r)) + e(lp.sourceDisclosureText(r)) + (typeof lp.ResolutionNote === 'function' ? L.render(lp.ResolutionNote, { resolution: r.resolution }) : ''); });
  if (s === 'chart') html = safe(() => {
    const React = L.React;
    L.stubSource('recharts', new Proxy({}, { get: (_t, k) => (k === '__esModule' ? true : typeof k === 'string' ? (p) => React.createElement('div', null, (p || {}).children) : undefined) }));
    return L.render(L.source('src/pages/SecurityAnalysis/components/RankedChart.tsx').RankedChart, { data: L.fixture('rankSeries.TRENDING_PRICE.12.json'), isLoading: false });
  });
  const nm = /^(header|posture)-(VLO|INTU|SAP|HK)$/.exec(s);
  if (nm && nm[1] === 'posture') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx').PostureTab, { securityKey: NAMES[nm[2]] }));
  if (nm && nm[1] === 'header') html = safe(() => { const m = L.source('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx'); let o; try { o = L.fixture(`overlay.${NAMES[nm[2]]}.json`); } catch (e) { o = Object.assign({}, bundles[NAMES[nm[2]]]); } return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: o, onBack: () => {}, onRefresh: () => {} }); });
  if (s === 'planted') html = safe(() => { const ov = JSON.parse(JSON.stringify(L.fixture('overlay.992_HK_Equity.json'))); ov.posture = Object.assign({}, ov.posture, { reason: PLANTED }); const m = L.source('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx'); return L.render(L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx').PostureTab, { securityKey: 'PLANTED_992' }) + L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: ov, onBack: () => {}, onRefresh: () => {} }); });
  if (s === 'posture-sap') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx').PostureTab, { securityKey: 'SAP_GY_Equity' }));
  if (s === 'thesis') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/ThesisTab.tsx').ThesisTab, { securityKey: 'VLO_US_Equity' }));
  if (s === 'model') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx').ModelTab, { securityKey: 'VLO_US_Equity' }));
  if (s === 'posture') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx').PostureTab, { securityKey: 'VLO_US_Equity' }));
  if (s === 'exec') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: 'INTU_US_Equity' }));
  total += census(s, html);
}
console.log(`NON-PROSE CENSUS: ${total} token(s) over ${want.length} surface(s) (an instrument for judgment, not a verdict)`);
