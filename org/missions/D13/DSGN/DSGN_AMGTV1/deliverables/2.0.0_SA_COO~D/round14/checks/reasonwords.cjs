/**
 * reasonwords.cjs -- DSGN_AMGTV1 round 14, AV-k-1: SERVED REASONS READ AS WORDS ON EVERY FACE (round-13 analysis ruling 1;
 * FWD-11; row Z-S7).
 *
 * Usage (repo root): node <this file>
 * Ruling 1: the producer's per-field dossier reasons carry machine tokens ("(IDVZ|PFOE|DIVZ)", "RECOMMENDATION line",
 * "class A missing or class B missing", "MANAGEMENT section"). The page turns a served reason into words by ONE mapping (the
 * ModelTab pattern: dropContractCodes / formulaInWords / caseAbsenceWords) on every face that prints a dossier reason -- the
 * header's fund line, Exec's management line, Posture's fund / last-stated-position line, Thesis's pillars line -- and keeps
 * the served reason WHOLE in a data-* attribute. A served reason carrying no token reads as served. Producer wording is not
 * re-opened.
 * Faces (the element carrying the dossier line): header [data-header-dossier-position], Exec [data-dossier-management],
 * Posture [data-dossier-position], Thesis [data-dossier-pillars]. Visible text = the element's inner text; the served reason must
 * equal (decoded, byte for byte) some data-* attribute value on that element's opening tag.
 * Token detector (visible text only): a parenthesised code list "(ABCD|EFGH)"; an ALL-CAPS word of 4+ letters; a SNAKE_CASE
 * caps token; "class A"/"class B"/"class-A"/"class-B".
 * Fixtures (round14/fixtures, SERVED): thesisBundle + overlay for BA_US_Equity (the Z-S7 families) and 6501_JP_Equity (a plain
 * reason, no token). PLANTED variants are in-memory copies of BA's bundle.
 * Arms:
 *   1  BA's four faces on the served fixture: no token in visible text, a sentence present, and each face's served reason(s)
 *      whole in a data attribute
 *   2  a PLANTED new token family (a copy of BA whose reasons carry "(ABCD|EFGH)", "(QRST|UVWX|YZAB)", SNAKE_CASE and bare
 *      ALL-CAPS section words never seen in the served data) is worded by the same mapping on all four faces (no token, every
 *      plain served word kept, reason whole in its attribute); and 6501's plain served reason reads verbatim on its four faces
 *   3  NEGATIVE control: (a) the detector flags each Z-S7 family when the served BA reasons are printed verbatim (the defect
 *      this cell exists for), and a truncated attribute fails the whole-reason test; (b) the mapping does not over-reach: a
 *      planted reason with only a date, a decimal and 3-letter acronyms ("EPS", "USD") reads verbatim on all four faces
 * Prints one line per arm and "SERVED REASONS READ AS WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 * No network, no AWS, writes no file.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');

const SA = 'src/pages/SecurityAnalysis/';
const BA = 'BA_US_Equity';
const J6501 = '6501_JP_Equity';
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');

const live = { [BA]: S.unwrap(L.fixture(`thesisBundle.${BA}.json`)), [J6501]: S.unwrap(L.fixture(`thesisBundle.${J6501}.json`)) };
const overlay = { [BA]: S.unwrap(L.fixture(`overlay.${BA}.json`)), [J6501]: S.unwrap(L.fixture(`overlay.${J6501}.json`)) };

// ---- the faces ----------------------------------------------------------------------------------------------------------------
const FACES = {
  header: { attr: 'data-header-dossier-position', reasons: (d) => [d.fund_of_record && d.fund_of_record.reason] },
  exec: { attr: 'data-dossier-management', reasons: (d) => [d.management && d.management.reason] },
  posture: { attr: 'data-dossier-position', reasons: (d) => [d.fund_of_record && d.fund_of_record.reason, d.last_stated_position && d.last_stated_position.reason] },
  thesis: { attr: 'data-dossier-pillars', reasons: (d) => [d.thesis_pillars_absent && d.thesis_pillars_absent.reason] },
};

function render(key, bundle) {
  const saved = S.bundles[key];
  S.bundles[key] = bundle;
  const r = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + e.message; } };
  const out = {
    header: r(() => { const m = L.source(SA + 'components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: overlay[key], onBack: () => {}, onRefresh: () => {} }); }),
    exec: r(() => L.render(L.source(SA + 'tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: key })),
    posture: r(() => L.render(L.source(SA + 'tabs/PostureTab.tsx').PostureTab, { securityKey: key })),
    thesis: r(() => L.render(L.source(SA + 'tabs/ThesisTab.tsx').ThesisTab, { securityKey: key })),
  };
  S.bundles[key] = saved;
  return out;
}

/** The face's dossier element: { line (visible text), attrs (decoded data-* values on its opening tag) } or null. */
function faceOf(html, face) {
  const attr = FACES[face].attr;
  const at = html.indexOf(attr + '="');
  if (at < 0) return null;
  const open = html.lastIndexOf('<', at);
  const tagEnd = html.indexOf('>', at);
  const tag = html.slice(open, tagEnd + 1);
  const attrs = [];
  const re = /\sdata-[a-z0-9-]+="([^"]*)"/g;
  let m;
  while ((m = re.exec(tag)) !== null) attrs.push(unesc(m[1]));
  return { line: L.textOf(L.innerOf(html, attr) || ''), attrs };
}

const TOKENS = [
  ['code list', /\(\s*[A-Z][A-Z0-9_]*(?:\s*\|\s*[A-Z][A-Z0-9_]*)+\s*\)|[A-Z]{2,}\|[A-Z]{2,}/],
  ['ALL-CAPS word', /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b|\b[A-Z]{4,}\b/],
  ['report class', /\bclass[- ]?[AB]\b/],
];
const tokensIn = (text) => TOKENS.filter(([, re]) => re.test(text)).map(([n]) => n);
const isSentence = (line) => /[.]$/.test(line) && line.split(/\s+/).filter((w) => /[a-z]{2,}/.test(w)).length >= 5;
const plainWords = (reason) => String(reason).split(/[\s(),;:|]+/).filter((w) => /^[a-z][a-z'-]*$/.test(w) && !/^tokens?$/.test(w));

/** Grade one face: the token families seen, sentence, reasons whole, and (optionally) plain served words kept / verbatim. */
function grade(key, bundle, opts) {
  const faults = [];
  const html = render(key, bundle);
  const d = bundle.dossier_fields;
  for (const face of Object.keys(FACES)) {
    const f = faceOf(html[face], face);
    if (!f) { faults.push(`${face}: the dossier line was not rendered`); continue; }
    const seen = tokensIn(f.line);
    if (seen.length) faults.push(`${face}: ${seen.join(' + ')} in "${f.line.slice(0, 110)}"`);
    if (!isSentence(f.line)) faults.push(`${face}: no sentence ("${f.line.slice(0, 80)}")`);
    for (const reason of FACES[face].reasons(d).filter(Boolean)) {
      if (!f.attrs.includes(reason)) faults.push(`${face}: served reason "${reason.slice(0, 60)}" not whole in a data attribute`);
      if (opts.words) {
        const lost = plainWords(reason).filter((w) => !new RegExp(`(^|[^a-z])${w.replace(/[-']/g, '.')}([^a-z]|$)`, 'i').test(f.line));
        if (lost.length) faults.push(`${face}: plain served words dropped (${lost.join(', ')}) from "${f.line.slice(0, 100)}"`);
      }
      if (opts.verbatim && !f.line.toLowerCase().includes(reason.toLowerCase())) faults.push(`${face}: "${reason}" not read as served ("${f.line.slice(0, 100)}")`);
    }
  }
  return faults;
}

// ---- arm 1 --------------------------------------------------------------------------------------------------------------------
const f1 = grade(BA, live[BA], {});
const a1 = f1.length === 0;
const a1d = a1 ? "BA's header, Exec, Posture and Thesis: 4 of 4 faces token-free sentences, 5 of 5 served reasons whole in a data attribute" : `${f1.length} faults over 4 faces; first: ${f1[0]}${f1[1] ? ' | ' + f1[1] : ''}`;

// ---- arm 2 --------------------------------------------------------------------------------------------------------------------
const planted = clone(live[BA]);
const pd = planted.dossier_fields;
pd.fund_of_record.reason = "no report's OUTLOOK_SUMMARY line names a desk token (ABCD|EFGH)";
pd.last_stated_position.reason = 'no report carries a non-empty VALUATION line';
pd.management.reason = 'no GOVERNANCE_NOTES section in the picked reports';
pd.thesis_pillars_absent.reason = 'no report carries a PILLARS block naming a theme (QRST|UVWX|YZAB)';
const f2p = grade(BA, planted, { words: true });
const f26 = grade(J6501, live[J6501], { verbatim: true });
const f2 = [...f2p.map((x) => 'planted ' + x), ...f26.map((x) => '6501 ' + x)];
const a2 = f2.length === 0;
const a2d = a2 ? 'planted families (2 code lists, 2 SNAKE_CASE, 2 ALL-CAPS words) worded on 4 of 4 faces, plain words kept, reasons whole; 6501 reads its served reason on 4 of 4 faces' : `${f2.length} faults (planted ${f2p.length}, 6501 ${f26.length}); first: ${f2[0]}${f2[1] ? ' | ' + f2[1] : ''}`;

// ---- arm 3 (negative control) ---------------------------------------------------------------------------------------------
const f3 = [];
const d = live[BA].dossier_fields;
const served = [d.fund_of_record.reason, d.last_stated_position.reason, d.management.reason, d.thesis_pillars_absent.reason];
const flagged = new Set();
for (const r of served) for (const n of tokensIn(r)) flagged.add(n);
if (flagged.size !== TOKENS.length) f3.push(`the detector flags ${flagged.size} of ${TOKENS.length} families on BA's served reasons printed verbatim`);
const verbatimLine = `<p data-dossier-management="ABSENT" data-dossier-reason="${d.management.reason.slice(0, 20)}">No: ${d.management.reason}.</p>`;
const vf = faceOf(verbatimLine, 'exec');
if (!vf || vf.attrs.includes(d.management.reason)) f3.push('a truncated data attribute passed the whole-reason test');
if (!vf || tokensIn(vf.line).length === 0) f3.push('a face printing the served management reason verbatim passed the token test');
const plain = clone(live[BA]);
const q = 'no report dated 2026-05-01 states EPS of 1.25 USD for this name';
for (const k of ['fund_of_record', 'last_stated_position', 'management', 'thesis_pillars_absent']) plain.dossier_fields[k].reason = q;
const f3o = grade(BA, plain, { verbatim: true });
for (const x of f3o) f3.push('over-reach ' + x);
const a3 = f3.length === 0;
const a3d = a3 ? `detector flags ${flagged.size} of ${TOKENS.length} Z-S7 families verbatim and refuses a truncated attribute; a token-free reason with a date, a decimal and EPS/USD reads verbatim on 4 of 4 faces` : `${f3.length} faults; first: ${f3[0]}${f3[1] ? ' | ' + f3[1] : ''}`;

const arms = [
  ["BA's Z-S7 families read as sentences on header, Exec, Posture and Thesis, reasons whole", a1, a1d],
  ["a planted new token family is worded by the same mapping; 6501's plain reason reads as served", a2, a2d],
  ['NEGATIVE control: the detector catches the verbatim families; the mapping does not over-reach', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`SERVED REASONS READ AS WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
