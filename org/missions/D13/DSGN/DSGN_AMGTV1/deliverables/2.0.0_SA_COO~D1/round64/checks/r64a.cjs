/**
 * r64a.cjs -- DSGN_AMGTV1 round 64 issuer CHECK (2.0.0_SA_COO~D1): THE THESIS WINDOW PRINTS THE SERVED DESCRIPTION UNDER ITS HEADING,
 * AND NO FILED FINANCIAL DETAIL WEARS THE DESCRIPTION LABEL.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round64/checks/r64a.cjs"
 *
 * Why (ledger/ROUND_ANALYSIS.round63.md @f7d74e6665 section 2 item 1; CVO ADJUDICATION_v37 @5ac5f33a6b, AV-zzo-1 NOT MET): /thesis serves
 * the description as `dossier_sections` entry `company_description` (status served, 1,535 characters on ASML). The window instead
 * heads the DRAFTED `company_description` section, whose sentences are machine-drafted Item 5 financial lines, with the served label
 * "Company description", so filed financial detail is labelled as the description and the description itself is never printed.
 * Arms (exit 0 only on all four), rendered through the real module (components/ThesisCards.tsx ThesisCardDetail, investment_thesis):
 *   1 THE SERVED DESCRIPTION: with a served dossier description, the window prints its text verbatim, once, on an element marked
 *     data-thesis-description="served", under the dossier entry's served heading.
 *   2 NO FALSE LABEL: the drafted company_description sentences are not headed by the description heading (the heading text and the
 *     drafted financial sentence are not adjacent); they are headed "From the filing".
 *   3 THE EMPTY STATE: with no served dossier description (absent, or no text), the window prints data-thesis-description="absent"
 *     with the served reason when one is served, prints no description text, and still labels the drafted sentences "From the filing".
 *   4 PLANTED: the graders refuse the round-63 markup and admit the clean markup.
 * Source read only; no network; writes nothing.
 */
'use strict';
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');

const DESC = 'ASML Holding N.V. develops, produces, and markets semiconductor manufacturing equipment.';
const FIN = 'In Logic, net sales increased by EUR 2.9 billion, primarily driven by foundry growth.';
const THESIS = 'ASML holds a monopoly in EUV lithography.';
const ev = (id, passage) => ({ id, passage, source: { accession: null, location: null } });
const drafted = [
  { section_id: 'company_description', label: 'Company description', held_no_span_at_read: 0, description_verdict_state: 'FAILED',
    description_verdict_reason: 'no served D-1 company_description sentence passing the describes-the-business test',
    sentences: [{ text: FIN, generated: true, evidence: [ev('e1', 'Total net sales growth ... PARAGRAPH 31')], quoted_spans: ['primarily driven by foundry growth'] }] },
  { section_id: 'investment_thesis', label: 'Investment thesis', held_no_span_at_read: 0,
    sentences: [{ text: THESIS, generated: true, evidence: [ev('e2', 'EUV passage')], quoted_spans: [] }] },
];
const served = { drafted_sections: drafted, dossier_sections: [
  { field: 'company_description', heading: 'Company description', status: 'served', text: DESC, reason: null, citation: null },
  { field: 'why_we_own', heading: 'Why we own it', status: 'absent', text: null, reason: 'not in the pack', citation: null }] };
const absent = { drafted_sections: drafted, dossier_sections: [
  { field: 'company_description', heading: 'Company description', status: 'absent', text: null, reason: 'The research pack has no description for this company.', citation: null }] };

const plain = (html) => html.replace(/<\/?(?:span|button|strong|em|a|mark|b|i)\b[^>]*>/g, '').replace(/<[^>]*>/g, ' ').replace(/&#x27;|&#39;/g, "'").replace(/&amp;/g, '&').replace(/\s+/g, ' ');
const count = (s, w) => s.split(w).length - 1;

const G = {
  served: (html) => {
    const f = [];
    const t = plain(html);
    if (!/data-thesis-description="served"/.test(html)) f.push('no element marked data-thesis-description="served"');
    if (count(t, DESC) !== 1) f.push(`the served description text appears ${count(t, DESC)} times (wanted 1)`);
    const at = t.indexOf(DESC);
    const head = t.lastIndexOf('Company description', at);
    if (at >= 0 && (head < 0 || at - head > 40)) f.push('the served description is not directly under its served heading');
    return f;
  },
  label: (html) => {
    const f = [];
    const t = plain(html);
    const fin = t.indexOf(FIN);
    if (fin < 0) return ['the drafted financial sentence is not drawn'];
    const before = t.slice(Math.max(0, fin - 60), fin);
    if (/Company description\s*$/i.test(before.replace(/MACHINE\s*$/i, '').trim())) f.push('the drafted financial sentence still sits directly under "Company description"');
    if (!/From the filing/.test(t.slice(0, fin))) f.push('the drafted company_description sentences are not headed "From the filing"');
    return f;
  },
  empty: (html) => {
    const f = [];
    const t = plain(html);
    if (!/data-thesis-description="absent"/.test(html)) f.push('no element marked data-thesis-description="absent"');
    if (!t.includes('The research pack has no description for this company.')) f.push('the served reason is not printed');
    if (t.includes(DESC)) f.push('description text printed with no served description');
    return f.concat(G.label(html));
  },
};

const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
let L = null; let Comp = null; let lerr = null;
try {
  L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
  Comp = L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx').ThesisCardDetail;
} catch (e) { lerr = 'LOADER: ' + String(e.message).split('\n')[0]; }
const draw = (bundle) => { try { return L.render(Comp, { sectionId: 'investment_thesis', bundle }); } catch (e) { return 'RENDER-THREW ' + e.message; } };
if (lerr || typeof Comp !== 'function') {
  const why = lerr || 'ThesisCards.tsx exports no ThesisCardDetail';
  push('THE SERVED DESCRIPTION', [why]); push('NO FALSE LABEL', [why]); push('THE EMPTY STATE', [why]);
} else {
  const hs = draw(served); const ha = draw(absent);
  push('THE SERVED DESCRIPTION', /^RENDER-THREW/.test(hs) ? [hs] : G.served(hs));
  push('NO FALSE LABEL', /^RENDER-THREW/.test(hs) ? [hs] : G.label(hs));
  push('THE EMPTY STATE', /^RENDER-THREW/.test(ha) ? [ha] : G.empty(ha));
}
{
  const p = [];
  const r63 = `<div data-thesis-window="investment_thesis"><h4>Company description</h4><p>MACHINE ${FIN}</p><blockquote>P31</blockquote><p>${THESIS}</p></div>`;
  if (!G.served(r63).length || !G.label(r63).length) p.push('the round-63 markup admitted');
  const clean = `<div><h4>Company description</h4><p data-thesis-description="served">${DESC}</p><h4>From the filing</h4><p>MACHINE ${FIN}</p><p>${THESIS}</p></div>`;
  if (G.served(clean).length || G.label(clean).length) p.push('the clean markup refused: ' + [...G.served(clean), ...G.label(clean)].join('; '));
  const cleanAbsent = `<div><p data-thesis-description="absent">The research pack has no description for this company.</p><h4>From the filing</h4><p>${FIN}</p></div>`;
  if (G.empty(cleanAbsent).length) p.push('the clean empty state refused: ' + G.empty(cleanAbsent).join('; '));
  if (!G.empty(clean).length) p.push('a served description admitted as the empty state');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev2] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev2}`); }
console.log(`ROUND 64 THESIS DESCRIPTION: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
