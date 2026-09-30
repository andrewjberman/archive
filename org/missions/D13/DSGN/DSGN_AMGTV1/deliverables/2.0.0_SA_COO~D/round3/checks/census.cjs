/**
 * census.cjs -- DSGN_AMGTV1 round 3: THE INVERTED NON-PROSE CENSUS (round-2 analysis, the CVO's decision 2).
 *
 * An INSTRUMENT for the CVO's FWD-11 judgment, not a pass/fail criterion. It lists every VISIBLE token on a surface that is
 * NOT ordinary prose -- a word, a number, a money figure, a date or a ticker -- with its count, so each is judged; a zero means
 * nothing non-prose is visible, not "none of the shapes we already knew". Collapsed <details> content is excluded (behind an
 * affordance a PM opens on purpose); attributes are free.
 * Usage (repo root): node <this file> [header|lead|thesis|model|posture|exec ...]   (default: all six)
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
const want = process.argv.slice(2).length ? process.argv.slice(2) : ['header', 'lead', 'thesis', 'model', 'posture', 'exec'];
const bundles = {};
for (const k of ['VLO_US_Equity', 'WMB_US_Equity', 'INTU_US_Equity', 'SAP_GY_Equity']) bundles[k] = L.fixture(`thesisBundle.${k}.json`);
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
  /^[A-Z0-9]{1,6}$/,
  /^\d{1,2}-[A-Z]$/,
  /^[-|>&/x*+=]+$/,
];
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
  const list = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  const n = list.reduce((a, [, c]) => a + c, 0);
  console.log(`${name}: ${n} non-prose token(s) of ${tokens} ${list.length ? JSON.stringify(list.slice(0, 40)) : ''}`);
  return n;
}
let total = 0;
const safe = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + String(e.message).split('\n')[0]; } };
for (const s of want) {
  let html = '';
  if (s === 'header') html = safe(() => { const m = L.source('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: L.fixture('overlay.VLO_US_Equity.json'), onBack: () => {}, onRefresh: () => {} }); });
  if (s === 'lead') html = safe(() => { const r = L.fixture('rankings.TRENDING_PRICE.json'); const lp = L.source('src/pages/SecurityAnalysis/components/LeadPanel.tsx'); const e = (x) => '<p>' + String(x || '').replace(/</g, '&lt;') + '</p>'; return e(lp.sourceFooterContent(r)) + e(lp.sourceDisclosureText(r)) + (typeof lp.ResolutionNote === 'function' ? L.render(lp.ResolutionNote, { resolution: r.resolution }) : ''); });
  if (s === 'thesis') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/ThesisTab.tsx').ThesisTab, { securityKey: 'VLO_US_Equity' }));
  if (s === 'model') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx').ModelTab, { securityKey: 'VLO_US_Equity' }));
  if (s === 'posture') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/PostureTab.tsx').PostureTab, { securityKey: 'VLO_US_Equity' }));
  if (s === 'exec') html = safe(() => L.render(L.source('src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: 'INTU_US_Equity' }));
  total += census(s, html);
}
console.log(`NON-PROSE CENSUS: ${total} token(s) over ${want.length} surface(s) (an instrument for judgment, not a verdict)`);
