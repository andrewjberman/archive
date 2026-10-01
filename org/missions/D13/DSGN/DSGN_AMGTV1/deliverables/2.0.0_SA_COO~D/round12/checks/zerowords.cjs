/**
 * zerowords.cjs -- DSGN_AMGTV1 round 12, AV-m-5: THE POSTURE TAB READS AS SENTENCES WHEN THERE IS NO COMPARABLE AND NO CITATION
 * (FWD-11; round-11 analysis s.4 item 5).
 *
 * Usage (repo root): node <this file>
 * Round 11's walk K (IMB LN Posture, shot 249) read "a comparable the research team has not identified (comparable): no filing
 * evidence is carried for this name yet." -- a noun phrase used as a name, then "this name" for the comparable's side -- and the
 * footer "0 of the 0 citations can be shown on this page; 0 of 0 were checked against their filings". The CTO's item: "The
 * comparable line names the comparable, not 'this name'; the zero-citation footer" reads as words.
 * Fixtures (round12/fixtures, SERVED): IMB LN /thesis (captured at the round-12 cut: no comparable, 0 citations) and the round-11
 * /thesis of VLO US (a comparable and 20 citations -- the control).
 * Arms:
 *   1  the comparable's side when none is identified: IMB's filing-evidence section says the research team has not identified a
 *      comparable, in a sentence, and never "a comparable the research team has not identified (comparable)" or "for this name"
 *      on the comparable's line; the subject's line still names IMB LN
 *   2  the footer at zero: IMB's footer holds no "0 of the 0" / "0 of 0" and says in words that no citation is drafted yet; the
 *      footer keeps its data-posture-cites-resolved / data-posture-cites-total attributes
 *   3  nothing else moves (the control): VLO's footer still reads "<N> of the 20 citations can be shown on this page; 20 of 20 were
 *      checked against their filings" (N as the page resolves it -- 11 in this static render at the base), and VLO's evidence
 *      section still names its comparable
 * Prints one line per arm and "POSTURE READS AS SENTENCES AT ZERO: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const tabs = Object.fromEntries(S.renderAll(['posture-IMB', 'posture-VLO']).map((r) => [r.surface.replace('posture-', ''), r.html]));
function section(text) {
  const a = text.search(/filing evidence, each side/i);
  if (a < 0) return null;
  const b = text.indexOf('Reasons, each beside', a);
  return text.slice(a, b > a ? b : a + 1200);
}
const footerOf = (html) => {
  const m = /<p[^>]*data-posture-cites-total="[^"]*"[^>]*>([\s\S]*?)<\/p>/.exec(html) || /<p[^>]*data-posture-cites-resolved="[^"]*"[^>]*>([\s\S]*?)<\/p>/.exec(html);
  return m ? { tag: m[0], text: unesc(L.textOf(m[1])).trim() } : null;
};

const imbHtml = tabs.IMB || '';
const imbText = unesc(L.textOf(imbHtml));
const vloHtml = tabs.VLO || '';
const vloText = unesc(L.textOf(vloHtml));

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const sec = section(imbText);
if (!sec) f1.push('IMB has no filing-evidence section');
else {
  if (/has not identified \(comparable\)/i.test(sec)) f1.push('the comparable line still reads "... has not identified (comparable)"');
  const compLine = (/[^.]*comparable[^.]*\./i.exec(sec.replace(/^filing evidence, each side/i, '')) || [''])[0];
  if (/this name/i.test(compLine)) f1.push(`the comparable's line says "this name": "${compLine.trim().slice(0, 120)}"`);
  if (!/research team has not identified/i.test(sec)) f1.push('the section does not say the research team has not identified a comparable');
  if (!/IMB LN/.test(sec)) f1.push("the subject's line no longer names IMB LN");
}
const a1 = f1.length === 0;
const a1d = a1 ? `IMB's comparable side reads as a sentence: "${((/[^.]*comparable[^.]*\./i.exec((sec || '').replace(/^filing evidence, each side/i, '')) || [''])[0]).trim().slice(0, 110)}"` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const fi = footerOf(imbHtml);
if (!fi) f2.push("IMB's footer (data-posture-cites-*) is not rendered");
else {
  if (/\b0 of (the )?0\b/.test(fi.text)) f2.push(`IMB's footer reads "${fi.text.slice(0, 120)}"`);
  if (!/no citation|none (is|are) drafted|not drafted|no .*citations/i.test(fi.text)) f2.push(`IMB's footer does not say no citation is drafted: "${fi.text.slice(0, 120)}"`);
  if (!/data-posture-cites-resolved="0"/.test(fi.tag) || !/data-posture-cites-total="0"/.test(fi.tag)) f2.push("IMB's footer lost its data-posture-cites attributes");
}
const a2 = f2.length === 0;
const a2d = a2 ? `IMB's footer at zero: "${fi.text.slice(0, 110)}"` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
const fv = footerOf(vloHtml);
if (!fv || !/\b\d+ of the 20 citations can be shown on this page; 20 of 20 were checked against their filings/.test(fv.text)) f3.push(`VLO's footer moved: "${fv ? fv.text.slice(0, 120) : 'none'}"`);
const vsec = section(vloText);
if (!vsec || /research team has not identified/i.test(vsec)) f3.push("VLO's evidence section no longer names its comparable");
const a3 = f3.length === 0;
const a3d = a3 ? "VLO's footer and comparable are unchanged" : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['no comparable reads as a sentence, never "this name"', a1, a1d],
  ['the footer at zero reads in words', a2, a2d],
  ['nothing else moves (control)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`POSTURE READS AS SENTENCES AT ZERO: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
