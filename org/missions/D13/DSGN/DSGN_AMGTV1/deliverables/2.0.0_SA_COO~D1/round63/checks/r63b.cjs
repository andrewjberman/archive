/**
 * r63b.cjs -- DSGN_AMGTV1 round 63 issuer CHECK (2.0.0_SA_COO~D1): THE THESIS WINDOW SAYS NOTHING FALSE ABOUT THE DESCRIPTION, AND A
 * FIGURE OPENS ITS PASSAGE.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D1/round63/checks/r63b.cjs"
 *
 * Why (ledger/ROUND_ANALYSIS.round62.md @4b7ce964a2 section 2 items 1-3; AMGT_RESAPP round-83 walk, WALK_ROUND83.md): the served
 * description verdict tests ONLY the section's first sentence (lib/research/api/scoped_amgt.py company_description_verdict). On ASML it
 * reads FAILED while the section serves 1,535 characters of business text, and components/ThesisCards.tsx:368-384 then prints "No
 * company description is on file yet." above that text and heads it with the fixed "Filed detail (does not describe the business)".
 * A figure in a sentence (a served quoted_spans entry, e.g. "2.9") is not pressable; the passage it rests on is printed under the
 * sentence.
 * Arms (exit 0 only on all five):
 *   1 NO FALSE ABSENCE: the branch that prints the description's sentences draws no "No company description is on file yet.".
 *   2 NO FIXED CAPTION: ThesisCards.tsx carries no "does not describe the business" string; the description is headed by its served
 *     label (description.label).
 *   3 SPANS PLACED: components/thesisSpans.ts (pure, no page imports) exports splitOnSpans(text, spans). It returns pieces
 *     [{ text, span }] whose texts join back to the sentence exactly, with each served span that occurs in the text (first occurrence,
 *     in order, no overlap) as its own piece marked span: true; a span not in the text is skipped (loaded through the real module).
 *   4 A FIGURE OPENS ITS PASSAGE (AMENDED at the round-63 close walk, tmp/ui-walk/20261009T112329Z shot 008: the served
 *     quoted_spans are phrases, not figures, so a per-span button left "EUR 2.9 billion" unpressable, and each inline-block button
 *     broke its sentence onto a new line): ThesisCards.tsx draws the WHOLE sentence text inside ONE <button> marked
 *     data-sentence-press, laid out inline (class `inline`, never `inline-block` or `block`), pointing at the sentence's passage
 *     through aria-controls and moving the reader there (scrollIntoView or focus). The served spans stay inside it as
 *     <span data-figure-span> (underlined), never as buttons.
 *   5 PLANTED.
 * Source read only; no network; writes nothing.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const DD = path.join(__dirname, '..', '..', '..', '2.0.0_SA_COO~D');
const SA = path.join(process.cwd(), 'portal', 'src', 'pages', 'SecurityAnalysis');
const read = (rel) => { try { return fs.readFileSync(path.join(SA, rel), 'utf8'); } catch (e) { return null; } };

const descriptionBranch = (t) => {
  const at = t.indexOf('hasDescription && description &&');
  if (at < 0) return '';
  const end = t.indexOf('{primaryHas', at);
  return t.slice(at, end < 0 ? at + 3000 : end);
};

const G = {
  absence: (t) => {
    if (t === null) return ['ThesisCards.tsx missing'];
    const b = descriptionBranch(t);
    if (!b) return ['no description branch (hasDescription && description &&)'];
    return /No company description is on file/.test(b) ? ['the branch that prints the description still says "No company description is on file yet."'] : [];
  },
  caption: (t) => {
    if (t === null) return ['ThesisCards.tsx missing'];
    const f = [];
    if (/does not describe the business/i.test(t)) f.push('the fixed "does not describe the business" caption is still in ThesisCards.tsx');
    if (!/heading=\{\s*description\.label\s*\}/.test(descriptionBranch(t))) f.push('the description is not headed by its served label (heading={description.label})');
    return f;
  },
  spans: (fn) => {
    if (typeof fn !== 'function') return ['components/thesisSpans.ts exports no splitOnSpans'];
    const f = [];
    const cases = [
      ['In Logic, net sales increased by EUR 2.9 billion, primarily driven by AI demand.', ['2.9', 'AI demand'], ['In Logic, net sales increased by EUR ', '[2.9]', ' billion, primarily driven by ', '[AI demand]', '.']],
      ['Revenue rose 5% to 10.1 billion.', ['5%', 'missing', '10.1'], ['Revenue rose ', '[5%]', ' to ', '[10.1]', ' billion.']],
      ['Plain text.', [], ['Plain text.']],
      ['Plain text.', undefined, ['Plain text.']],
      ['abcabc', ['bc', 'abc'], ['a', '[bc]', '[abc]']],
    ];
    for (const [text, spans, want] of cases) {
      let out;
      try { out = fn(text, spans); } catch (e) { f.push(`splitOnSpans threw on ${JSON.stringify(text)}: ${e.message}`); continue; }
      if (!Array.isArray(out)) { f.push('splitOnSpans returned no array'); continue; }
      const joined = out.map((p) => (p ? p.text : '')).join('');
      const got = out.map((p) => (p && p.span ? `[${p.text}]` : p && p.text)).filter((x) => x !== '');
      if (joined !== text) f.push(`pieces of ${JSON.stringify(text)} join to ${JSON.stringify(joined)}`);
      if (JSON.stringify(got) !== JSON.stringify(want)) f.push(`${JSON.stringify(text)} with ${JSON.stringify(spans)} -> ${JSON.stringify(got)} (wanted ${JSON.stringify(want)})`);
    }
    return f;
  },
  press: (t) => {
    if (t === null) return ['ThesisCards.tsx missing'];
    const f = [];
    if (!/splitOnSpans\s*\(/.test(t)) f.push('ThesisCards.tsx does not use splitOnSpans');
    const open = /<button\b(?:[^>]|=>)*?data-sentence-press(?:[^>]|=>)*>/.exec(t);
    if (!open) f.push('no sentence-wide <button data-sentence-press>');
    else {
      if (!/aria-controls=/.test(open[0])) f.push('the sentence button names no passage (aria-controls)');
      const cls = /className=(?:"([^"]*)"|\{`([^`]*)`\}|\{'([^']*)'\})/.exec(open[0]);
      const c = cls ? (cls[1] || cls[2] || cls[3] || '') : '';
      if (!/(^|\s)inline(\s|$)/.test(c) || /(^|\s)(inline-block|block|flex|inline-flex)(\s|$)/.test(c)) f.push(`the sentence button is not laid out inline (class "${c}")`);
      if (!/scrollIntoView|\.focus\(/.test(t)) f.push('pressing the sentence does not move to its passage (scrollIntoView / focus)');
    }
    if (/<button\b(?:[^>]|=>)*?data-figure-span/.test(t)) f.push('a served span is still its own <button> (it must be a <span data-figure-span> inside the sentence button)');
    if (!/<span\b(?:[^>]|=>)*?data-figure-span/.test(t)) f.push('no <span data-figure-span> for the served spans');
    return f;
  },
};

const t = read('components/ThesisCards.tsx');
const arms = [];
const push = (name, f) => arms.push([name, f.length === 0, f.length ? f.join(' | ') : 'holds']);
push('NO FALSE ABSENCE', G.absence(t));
push('NO FIXED CAPTION', G.caption(t));
{
  let fn = null; let e2 = null;
  try {
    const L = require(path.join(DD, 'round15', 'checks', '_load.cjs'));
    fn = L.source('src/pages/SecurityAnalysis/components/thesisSpans.ts').splitOnSpans;
  } catch (e) { e2 = 'LOADER: ' + String(e.message).split('\n')[0]; }
  push('SPANS PLACED', e2 ? [e2] : G.spans(fn));
}
push('A FIGURE OPENS ITS PASSAGE', G.press(t));
{
  const p = [];
  const r62 = "{hasDescription && description && (\n<div>{description.description_verdict_state !== 'PASSED' && (<p>No company description is on file yet.</p>)}\n<Block heading={description.description_verdict_state === 'PASSED' ? description.label : 'Filed detail (does not describe the business)'} />\n</div>)}\n{primaryHas && primary && (";
  if (!G.absence(r62).length || !G.caption(r62).length) p.push('the round-62 form admitted');
  const clean = "{hasDescription && description && (\n<div><Block heading={description.label} /></div>)}\n{primaryHas && primary && (\n<button type=\"button\" data-sentence-press=\"\" aria-controls={passageId} className=\"inline text-left underline-offset-2\" onClick={() => document.getElementById(passageId)?.scrollIntoView()}>{splitOnSpans(sentence.text, sentence.quoted_spans).map((piece) => piece.span ? (<span data-figure-span=\"\" className=\"underline\">{piece.text}</span>) : piece.text)}</button>";
  const r63first = clean.replace(/<button type="button" data-sentence-press=""[^>]*>/, '<p>').replace('</button>', '</p>').replace('<span data-figure-span="" className="underline">{piece.text}</span>', '<button type="button" data-figure-span="" aria-controls={passageId} onClick={() => go()}>{piece.text}</button>');
  if (!G.press(r63first).length) p.push('the first round-63 build (per-span buttons) admitted');
  if (!G.press(clean.replace('className="inline text-left', 'className="inline-block text-left')).length) p.push('an inline-block sentence button admitted');
  if (G.absence(clean).length || G.caption(clean).length || G.press(clean).length) p.push('the clean form refused: ' + [...G.absence(clean), ...G.caption(clean), ...G.press(clean)].join('; '));
  const okSplit = (text, spans) => {
    const out = []; let at = 0;
    for (const s of spans || []) { if (!s) continue; const i = text.indexOf(s, at); if (i < 0) continue; if (i > at) out.push({ text: text.slice(at, i), span: false }); out.push({ text: s, span: true }); at = i + s.length; }
    if (at < text.length) out.push({ text: text.slice(at), span: false });
    return out;
  };
  if (G.spans(okSplit).length) p.push('the clean split refused: ' + G.spans(okSplit).join('; '));
  if (!G.spans((text) => [{ text, span: false }]).length) p.push('a split that marks no span admitted');
  if (!G.spans((text, spans) => (spans || []).map((s) => ({ text: s, span: true }))).length) p.push('a split that drops the text admitted');
  push('PLANTED', p);
}
let pass = 0;
for (const [name, ok, ev] of arms) { if (ok) pass += 1; console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); }
console.log(`ROUND 63 THESIS WINDOW: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
