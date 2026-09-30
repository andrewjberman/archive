/**
 * bytes.cjs -- DSGN_AMGTV1 round 10, AV-o-3 AMENDMENT 1 (repair, issuer, after walk I): NO CONTROL BYTE IN THE PAGE'S SOURCE, AND THE
 * TWO LABELS IT BROKE READ RIGHT (issuer row DSGN_AMGTV1-Z-S5).
 *
 * Usage (repo root): node <this file>
 * Walk I (tmp/ui-walk/20260930T055658Z, shot 192) showed AZN's Model tab reading "Opal's opal's historical-multiple reference:
 * ...". The cause is a literal BACKSPACE byte (0x08) where a regex meant `\b`: `tabs/ModelTab.tsx` `/^Opal's<0x08>/i` (AV-o-3,
 * portal cb14d218) never matches, so a label already reading "Opal's ..." is prefixed again. The same byte sits in
 * `components/HeaderBrief.tsx` `descriptionSourceWords` (`/^bloomberg<0x08>/i`, `/^D-1<0x08>/`, since 2515f456, round 1), so no
 * served description source has ever read "Company description from Bloomberg" -- every header reads "Company description".
 * The class: a shell heredoc or a Python string turned `\b` into 0x08 on its way into the file; tsc and the harnesses pass it.
 * Arms:
 *   1  no control byte: 0 bytes below 0x20 other than tab / LF / CR in any .ts / .tsx / .cjs / .mjs / .js file under
 *      portal/src/pages/SecurityAnalysis (prints each hit: file, line, byte)
 *   2  the rule label reads once: AZN's Model tab (served /thesis, round10/fixtures) shows its rule base line starting with the
 *      served label "Opal's historical-multiple reference" exactly as served, and nowhere "Opal's opal's" (any case); an ISSUER
 *      VARIANT with the label "Historical-multiple reference" (no Opal's) reads "Opal's historical-multiple reference" -- one
 *      "Opal's", never two
 *   3  the description source reads in words: HeaderBrief `descriptionSourceWords("bloomberg CIE_DES_BULK")` is "Company
 *      description from Bloomberg", `("D-1 drafting/v1 sentence 1")` is "Company description from the drafted thesis", and
 *      `(null)` is "Company description"
 * Prints one line per arm and "NO CONTROL BYTES, LABELS READ RIGHT: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const dir = path.join(L.base, 'src/pages/SecurityAnalysis');
const hits = [];
let files = 0;
(function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) { walk(p); continue; }
    if (!/\.(ts|tsx|cjs|mjs|js)$/.test(e.name)) continue;
    files += 1;
    const b = fs.readFileSync(p);
    let line = 1;
    for (let i = 0; i < b.length; i += 1) {
      const c = b[i];
      if (c === 10) line += 1;
      else if (c < 32 && c !== 9 && c !== 13) hits.push(`${path.relative(L.base, p).replace(/\\/g, '/')}:${line} byte 0x${c.toString(16).padStart(2, '0')}`);
    }
  }
})(dir);
for (const h of hits) console.log(`CONTROL BYTE ${h}`);
const a1 = hits.length === 0 && files > 0;
const a1d = a1 ? `0 control bytes over ${files} source file(s)` : `${hits.length} control byte(s) over ${files} file(s); first: ${hits[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const renderModel = () => unesc(L.textOf((S.renderAll(['model-AZN'])[0] || {}).html || ''));
const t = renderModel();
const served = ((S.bundles.AZN_LN_Equity.model_cases || {}).base || {}).label;
if (!served || !t.includes(`${served}:`)) f2.push(`AZN: the served label "${served}" does not head its line`);
if (/Opal's\s+opal's/i.test(t)) f2.push(`AZN: "${(/Opal's\s+opal's[^:]*/i.exec(t) || [''])[0]}" -- Opal's twice`);
const orig = S.bundles.AZN_LN_Equity.model_cases.base.label;
S.bundles.AZN_LN_Equity.model_cases.base.label = 'Historical-multiple reference';
const tv = renderModel();
S.bundles.AZN_LN_Equity.model_cases.base.label = orig;
if (!tv.includes("Opal's historical-multiple reference:")) f2.push('variant: an unprefixed label is not read as "Opal\'s historical-multiple reference"');
if (/Opal's\s+opal's/i.test(tv)) f2.push('variant: Opal\'s twice');
const a2 = f2.length === 0;
const a2d = a2 ? `AZN's rule base reads "${served}: ..." once; the unprefixed variant reads "Opal's historical-multiple reference: ..."` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
let HB = null;
try { HB = L.source('src/pages/SecurityAnalysis/components/HeaderBrief.tsx'); } catch (e) { f3.push('HeaderBrief did not load: ' + String(e.message).split('\n')[0]); }
const dsw = HB && HB.descriptionSourceWords;
const cases = [
  ['bloomberg CIE_DES_BULK', 'Company description from Bloomberg'],
  ['D-1 drafting/v1 sentence 1', 'Company description from the drafted thesis'],
  [null, 'Company description'],
];
for (const [src, want] of cases) {
  const got = dsw ? dsw(src) : null;
  if (got !== want) f3.push(`descriptionSourceWords(${JSON.stringify(src)}) = ${JSON.stringify(got)} (want "${want}")`);
}
const a3 = f3.length === 0;
const a3d = a3 ? 'a Bloomberg source reads "Company description from Bloomberg"; a drafted one "... from the drafted thesis"; none "Company description"' : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['no control byte in the page source', a1, a1d],
  ["the rule label reads once (no \"Opal's opal's\")", a2, a2d],
  ['the description source reads in words', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`NO CONTROL BYTES, LABELS READ RIGHT: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
