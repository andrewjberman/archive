/**
 * r65.cjs -- DSGN_AMGTV1 round 65 issuer CHECK (2.0.0_SA_COO~D1): THE SERVED DESCRIPTION DOES NOT REPEAT ITS HEADING.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round65/checks/r65.cjs"
 *
 * Why (ledger/ROUND_ANALYSIS.round64.md @3f30e42354 section 2 item 1; round-64 walk shot 008): ASML's served dossier description begins
 * "COMPANY DESCRIPTION:" directly under the heading "Company description", so the label reads twice.
 * Arms (exit 0 only on all four), rendered through the real module (components/ThesisCards.tsx ThesisCardDetail, investment_thesis):
 *   1 STRIPPED: a served description whose text begins with its own heading (any case) followed by a colon prints without that leading
 *     label and colon (and the space after it); the rest of the text is printed verbatim, once.
 *   2 LEFT WHOLE: a served description that only contains the heading words mid-text, or begins with a different label, is printed
 *     verbatim.
 *   3 HEADING KEPT: the served heading itself still prints once above the text.
 *   4 PLANTED.
 * Source read only; no network; writes nothing.
 */
'use strict';
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');

const REST = 'What started as a failing joint venture between ASM International and Philips became the sole supplier of EUV machines.';
const MID = 'ASML lists its Company description: in the annual report, and builds lithography machines.';
const OTHER = 'Overview: ASML builds lithography machines.';
const bundleWith = (text) => ({ drafted_sections: [
  { section_id: 'investment_thesis', label: 'Investment thesis', held_no_span_at_read: 0, sentences: [{ text: 'Thesis line.', generated: true, evidence: [], quoted_spans: [] }] }],
  dossier_sections: [{ field: 'company_description', heading: 'Company description', status: 'served', text, reason: null, citation: null }] });

const servedText = (html) => {
  const m = /<p\b[^>]*data-thesis-description="served"[^>]*>([\s\S]*?)<\/p>/.exec(html || '');
  return m ? m[1].replace(/<[^>]*>/g, '').replace(/&#x27;|&#39;/g, "'").replace(/&amp;/g, '&').trim() : null;
};
const headingCount = (html) => ((html || '').replace(/<[^>]*>/g, '\n').match(/^\s*Company description\s*$/gim) || []).length;

const G = {
  stripped: (draw) => {
    const f = [];
    for (const lead of ['COMPANY DESCRIPTION:', 'Company description: ', 'company description :  ']) {
      const t = servedText(draw(bundleWith(lead + REST)));
      if (t === null) { f.push('no data-thesis-description="served" paragraph'); break; }
      if (t !== REST) f.push(`"${lead.trim()}" + text printed as ${JSON.stringify(t.slice(0, 60))}... (wanted the text without the label)`);
    }
    return f;
  },
  whole: (draw) => {
    const f = [];
    for (const text of [MID, OTHER, REST]) {
      const t = servedText(draw(bundleWith(text)));
      if (t !== text) f.push(`${JSON.stringify(text.slice(0, 40))}... printed as ${JSON.stringify((t || '').slice(0, 60))}`);
    }
    return f;
  },
  heading: (draw) => (headingCount(draw(bundleWith('COMPANY DESCRIPTION:' + REST))) === 1 ? [] : ['the heading "Company description" does not print exactly once']),
};

const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
let draw = null; let lerr = null;
try {
  const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
  const C = L.source('src/pages/SecurityAnalysis/components/ThesisCards.tsx').ThesisCardDetail;
  if (typeof C !== 'function') throw new Error('ThesisCards.tsx exports no ThesisCardDetail');
  draw = (bundle) => { try { return L.render(C, { sectionId: 'investment_thesis', bundle }); } catch (e) { return ''; } };
} catch (e) { lerr = 'LOADER: ' + String(e.message).split('\n')[0]; }
push('STRIPPED', lerr ? [lerr] : G.stripped(draw));
push('LEFT WHOLE', lerr ? [lerr] : G.whole(draw));
push('HEADING KEPT', lerr ? [lerr] : G.heading(draw));
{
  const p = [];
  const fake = (mode) => (bundle) => {
    const d = bundle.dossier_sections[0];
    let t = d.text;
    if (mode === 'clean') t = t.replace(/^\s*company description\s*:\s*/i, '');
    if (mode === 'greedy') t = t.replace(/company description\s*:\s*/ig, '');
    return `<div><h4>Company description</h4><p data-thesis-description="served">${t}</p></div>`;
  };
  if (G.stripped(fake('clean')).length || G.whole(fake('clean')).length || G.heading(fake('clean')).length) p.push('the clean page refused');
  if (!G.stripped(fake('none')).length) p.push('the round-64 page (label repeated) admitted');
  if (!G.whole(fake('greedy')).length) p.push('a greedy strip of mid-text words admitted');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 65 REPEATED LABEL: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
