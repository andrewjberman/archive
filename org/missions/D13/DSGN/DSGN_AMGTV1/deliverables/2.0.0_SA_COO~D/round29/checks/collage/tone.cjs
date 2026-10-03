/**
 * tone.cjs -- DSGN_AMGTV1 round 29, AV-zg-4 CHATTER COLLAGE (issuer 2.0.0_SA_COO~D): EVERY BUBBLE IS FILLED BY ITS SERVED TONE
 * THROUGH THE ONE SHARED RAMP.
 *
 * Usage: cd C:/tmp/wk-dsgn-amgtv1-70 && node <this file>     (portal/ under the cwd is the checkout under test)
 * Grades PRD v0.10 FWD-21 (DSGN_AMGTV1_PRD.md ~291-315), the fill limb: "each bubble's fill is its served coverage tone on the
 *   Topic Cloud scale, through ONE shared sentiment-colour module, with a legend; a name whose served tone is null (no voters)
 *   is filled apart from the ramp's neutral centre and reads 'no clear tone' on hover (v0.10)"; "the size is labelled
 *   'collected', never 'market chatter'"; SAUX-18; decomposition v29 issuer rulings (c) (a field not yet served renders the
 *   designed empty state in words) and (d) (the ramp is TopicCloud's own getSentimentColor, extracted unchanged; TopicCloud's
 *   render byte-equal before and after).
 * Inputs (round29/fixtures/collage/, built by r29c.build.cjs; the BASE captures were taken on portal dcdc89b1):
 *   getSentimentColor.base.txt (the BASE function block -- the TRUTH for every colour graded here, never the candidate's module),
 *   TopicCloud.base.tsx.txt, topiccloud.keywords.json + topiccloud.base.html (the Topic Cloud render at BASE through _tc.cjs),
 *   r29c.chatter.toned.json (17 names collected in 2026-09: 14 with a planted `tone`, 1 with tone null, 2 with no tone field).
 * Arms:
 *   1  SHARED MODULE: portal/src/lib/sentimentColor.ts exports getSentimentColor whose text is the BASE block verbatim (an
 *      `export ` prefix allowed) and whose output equals BASE on 3,003 inputs (-1.5..+1.5 by 0.001, NaN, -Infinity); TopicCloud.tsx differs from BASE only by the one
 *      import line (the block, with or without its doc comment, removed; blank-line runs collapsed); ChatterBubbles.tsx imports
 *      getSentimentColor from the same module and defines no ramp of its own.
 *   2  CONTROL (passes at BASE by design): the Topic Cloud render is byte-equal to the BASE capture.
 *   3  FILL + LEGEND: each toned bubble's `fill` attribute is the BASE ramp's colour for its served tone; the null- and
 *      absent-tone bubbles share ONE fill that is no colour of the ramp and their hover says "no clear tone" (a toned hover
 *      never does); one [data-tone-legend] element carries the ramp's two ends and centre (#f5365c, #eab308, #2dce89), the
 *      no-tone fill and the words "no clear tone"; the face's text says "collected" and no markup says "market chatter".
 *   4  PLANTED: the arm-3 predicate rejects 5 known-bad faces, EACH FOR ITS OWN FAULT CLASS (a toned bubble in the old blue,
 *      a null tone on the neutral centre, a null tone without the words, a legend without the no-tone swatch, a face reading
 *      "market chatter"), and accepts a known-good one.
 * Prints one line per arm and "EVERY BUBBLE IS FILLED BY ITS SERVED TONE THROUGH THE ONE SHARED RAMP: <k> of 4 arms"; exit 0
 * only at 4 of 4. Reads only; writes no file. ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (see _load.cjs) is honoured for every
 * source read here.
 */
const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');

const CB = 'src/pages/SecurityAnalysis/components/ChatterBubbles.tsx';
const TC = 'src/components/market-performance/TopicCloud.tsx';
const LIB = 'src/lib/sentimentColor.ts';
const D = path.join(__dirname, '..', '..', '..');
const FX = path.join(D, 'round29', 'fixtures', 'collage');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const renderTopicCloud = require(path.join(__dirname, '_tc.cjs'));
const unwrap = (x) => (x && x.payload ? x.payload : x);
const fxText = (n) => fs.readFileSync(path.join(FX, n), 'utf8').replace(/\r\n/g, '\n');
const TONED = unwrap(JSON.parse(fxText('r29c.chatter.toned.json')));
const KEYWORDS = JSON.parse(fxText('topiccloud.keywords.json'));
const BASE_BLOCK = fxText('getSentimentColor.base.txt').replace(/\n+$/, '');
const BASE_TC = fxText('TopicCloud.base.tsx.txt');
const BASE_TC_HTML = fs.readFileSync(path.join(FX, 'topiccloud.base.html'), 'utf8');
const MONTH = '2026-09';
const ANCHORS = ['#f5365c', '#eab308', '#2dce89'];
const NO_TONE_WORDS = /no clear tone/i;

const OV = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) { const i = pair.indexOf('='); OV[pair.slice(0, i)] = pair.slice(i + 1); }
const srcText = (rel) => { const f = OV[rel] || path.join(L.base, rel); return fs.existsSync(f) ? fs.readFileSync(f, 'utf8').replace(/\r\n/g, '\n') : null; };
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const collapse = (s) => s.replace(/\n[ \t]*\n(?:[ \t]*\n)+/g, '\n\n').trim();

// The TRUTH: the BASE function block, transpiled here (never the candidate's module).
const ts = createRequire(path.join(L.base, 'package.json'))('typescript');
const baseRamp = (() => {
  const js = ts.transpileModule(BASE_BLOCK + '\nmodule.exports = getSentimentColor;\n', { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 } }).outputText;
  const mod = { exports: {} }; new Function('module', 'exports', js)(mod, mod.exports); return mod.exports;
})();
const GRID = [];
for (let i = -1500; i <= 1500; i++) GRID.push(i / 1000);
GRID.push(NaN, -Infinity);
const RAMP_IMAGE = new Set();
for (let i = -5000; i <= 5000; i++) RAMP_IMAGE.add(baseRamp(i / 10000));

const IMPORT_RE = /^import\s*\{[^}]*\bgetSentimentColor\b[^}]*\}\s*from\s*['"](?:@\/lib\/sentimentColor|(?:\.\.\/)+lib\/sentimentColor)['"];?[ \t]*$/gm;

/** Arm-3/4 predicate over a face model: {bubbles:[{key, tone, fill, hover}], legendHtml, legendText, faceText, html}. */
function fillFaults(m) {
  const f = [];
  const noTone = m.bubbles.filter((b) => typeof b.tone !== 'number' || !Number.isFinite(b.tone));
  const toned = m.bubbles.filter((b) => !noTone.includes(b));
  let wrong = 0; let ex = '';
  for (const b of toned) {
    const want = baseRamp(b.tone);
    if (String(b.fill || '').toLowerCase() !== want) { wrong += 1; if (!ex) ex = `${b.key} tone ${b.tone}: fill "${b.fill}" (want ${want})`; }
    if (NO_TONE_WORDS.test(b.hover)) { wrong += 1; if (!ex) ex = `${b.key} tone ${b.tone}: hover says "no clear tone"`; }
  }
  if (wrong) f.push(`TONED FILL: ${wrong} fault(s), e.g. ${ex}`);
  const fills = [...new Set(noTone.map((b) => String(b.fill || '').toLowerCase()))];
  if (noTone.length) {
    if (fills.length !== 1) f.push(`NO-TONE FILL: ${fills.length} different fills on ${noTone.length} no-tone bubbles (${fills.join(', ')})`);
    for (const x of fills) if (!x || RAMP_IMAGE.has(x)) f.push(`NO-TONE FILL "${x}" is ${x ? 'a colour of the ramp' : 'absent'} (must sit apart from it)`);
    const mute = noTone.filter((b) => !NO_TONE_WORDS.test(b.hover));
    if (mute.length) f.push(`NO-TONE HOVER: ${mute.length} bubble(s) without "no clear tone", e.g. ${mute[0].key}`);
  }
  if (m.legendHtml === null) f.push('NO LEGEND: no [data-tone-legend] element');
  else {
    const lh = m.legendHtml.toLowerCase();
    const lack = ANCHORS.filter((a) => !lh.includes(a));
    if (lack.length) f.push(`LEGEND lacks the ramp colour(s) ${lack.join(', ')}`);
    if (fills.length === 1 && fills[0] && !lh.includes(fills[0])) f.push(`LEGEND lacks the no-tone swatch ${fills[0]}`);
    if (!NO_TONE_WORDS.test(m.legendText)) f.push('LEGEND does not say "no clear tone"');
  }
  if (!/collected/i.test(m.faceText)) f.push('SIZE WORDS: the face never says "collected"');
  if (/market chatter/i.test(decode(m.html))) f.push('SIZE WORDS: the face says "market chatter"');
  return f;
}
function faceModel(html, data) {
  const bubbles = [];
  for (const r of data.rows) {
    const e = r.by_month[MONTH];
    if (!e || !(e.collected > 0)) continue;
    const at = html.indexOf(`data-bubble="${r.security_key}"`);
    if (at < 0) { bubbles.push({ key: r.security_key, tone: r.tone, fill: null, hover: '' }); continue; }
    const open = html.lastIndexOf('<', at);
    const head = html.slice(open, html.indexOf('>', at) + 1);
    const fill = (/\sfill="([^"]*)"/.exec(head) || [])[1] || null;
    const tag = /^<([a-zA-Z0-9]+)/.exec(head)[1];
    const end = html.indexOf(`</${tag}>`, at);
    const st = /<title>([\s\S]*?)<\/title>/.exec(html.slice(at, end < 0 ? at + 4000 : end));
    bubbles.push({ key: r.security_key, tone: r.tone, fill, hover: st ? decode(st[1]) : '' });
  }
  const legendHtml = L.innerOf(html, 'data-tone-legend');
  return { bubbles, legendHtml, legendText: legendHtml === null ? '' : L.textOf(legendHtml), faceText: L.textOf(html), html };
}

const arms = [];
// Arm 1 -- SHARED MODULE.
{
  const f = [];
  const lib = srcText(LIB);
  if (lib === null) f.push('NO MODULE: portal/src/lib/sentimentColor.ts does not exist');
  else {
    if (!lib.replace(/export\s+function\s+getSentimentColor\(/, 'function getSentimentColor(').includes(BASE_BLOCK)) f.push('NOT VERBATIM: the module does not carry the BASE getSentimentColor block unchanged');
    try {
      const mod = L.source(LIB);
      if (typeof mod.getSentimentColor !== 'function') f.push('NOT EXPORTED: getSentimentColor is not a named export');
      else {
        const diff = GRID.filter((s) => mod.getSentimentColor(s) !== baseRamp(s));
        if (diff.length) f.push(`OUTPUT: ${diff.length} of ${GRID.length} inputs differ from BASE, e.g. ${diff[0]}`);
      }
    } catch (e) { f.push('LOAD: ' + String(e.message).split('\n')[0]); }
  }
  const tc = srcText(TC) || '';
  if (/function\s+getSentimentColor\b|getSentimentColor\s*=/.test(tc)) f.push('TOPICCLOUD still defines getSentimentColor');
  const imps = tc.match(IMPORT_RE) || [];
  if (imps.length !== 1) f.push(`TOPICCLOUD: ${imps.length} import line(s) of getSentimentColor from lib/sentimentColor (want 1)`);
  else {
    const s = BASE_TC.indexOf('function getSentimentColor(');
    const e = s + BASE_BLOCK.length;
    const doc = BASE_TC.lastIndexOf('/**', s);
    const want = [BASE_TC.slice(0, s) + BASE_TC.slice(e), BASE_TC.slice(0, doc) + BASE_TC.slice(e)].map(collapse);
    if (!want.includes(collapse(tc.replace(IMPORT_RE, '')))) f.push('TOPICCLOUD changed beyond the import swap');
  }
  const cb = srcText(CB) || '';
  if (!(cb.match(IMPORT_RE) || []).length) f.push('CHATTER does not import getSentimentColor from lib/sentimentColor');
  if (/function\s+getSentimentColor\b|getSentimentColor\s*=|r:\s*245,\s*g:\s*54/.test(cb)) f.push('CHATTER defines a ramp of its own');
  arms.push(['SHARED MODULE: lib/sentimentColor.ts carries the BASE getSentimentColor unchanged; TopicCloud and the chatter import it', f.length === 0,
    f.length === 0 ? `verbatim; ${GRID.length} of ${GRID.length} outputs equal BASE; TopicCloud = BASE + 1 import line` : f.slice(0, 5).join(' | ')]);
}
// Arm 2 -- CONTROL: the Topic Cloud render.
{
  const f = [];
  try {
    const html = renderTopicCloud(L, KEYWORDS);
    if (html !== BASE_TC_HTML) {
      let i = 0; while (i < html.length && html[i] === BASE_TC_HTML[i]) i++;
      f.push(`RENDER DIFFERS from BASE at char ${i}: "${html.slice(Math.max(0, i - 20), i + 40)}"`);
    }
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['CONTROL: the Topic Cloud render is byte-equal to its BASE capture', f.length === 0,
    f.length === 0 ? `${BASE_TC_HTML.length} chars equal (${KEYWORDS.length} planted keywords)` : f.join(' | ')]);
}
// Arm 3 -- FILL + LEGEND.
{
  let f = [];
  let n = '';
  try {
    const m = L.source(CB);
    const html = L.render(m.ChatterBubbles, { data: TONED, month: MONTH, onMonthChange: () => {}, onSelectSecurity: () => {} });
    const model = faceModel(html, TONED);
    const absent = model.bubbles.filter((b) => b.fill === null && !html.includes(`data-bubble="${b.key}"`));
    if (absent.length) f.push(`MISSING ${absent.length} bubble(s)`);
    f = f.concat(fillFaults(model));
    const nt = model.bubbles.filter((b) => typeof b.tone !== 'number').length;
    n = `${model.bubbles.length - nt} toned on the ramp, ${nt} no-tone apart, legend + "collected"`;
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['FILL + LEGEND: each bubble is its served tone on the BASE ramp; a null or absent tone sits apart and says "no clear tone"; a legend; "collected"', f.length === 0,
    f.length === 0 ? n : f.slice(0, 5).join(' | ')]);
}
// Arm 4 -- PLANTED.
{
  const f = [];
  const legend = (noFill) => `<div data-tone-legend=""><span style="background-color:#f5365c"></span><span style="background-color:#eab308"></span><span style="background-color:#2dce89"></span>${noFill ? `<span style="background-color:${noFill}"></span>` : ''}<span>coverage tone, negative to positive; no clear tone</span></div>`;
  const GREY = '#7d8590';
  const good = {
    bubbles: [
      { key: 'A', tone: 0.3, fill: baseRamp(0.3), hover: 'Alpha; 9 articles collected' },
      { key: 'B', tone: -0.1, fill: baseRamp(-0.1), hover: 'Beta; 4 articles collected' },
      { key: 'C', tone: null, fill: GREY, hover: 'Gamma; 2 articles collected; no clear tone' },
      { key: 'E', tone: undefined, fill: GREY, hover: 'Epsilon; 1 article collected; no clear tone' },
    ],
    legendHtml: legend(GREY), legendText: L.textOf(legend(GREY)), faceText: 'Bubble area is the number of articles collected', html: '<div>articles collected</div>',
  };
  const mut = (fn) => { const s = JSON.parse(JSON.stringify(good)); s.bubbles[3].tone = undefined; fn(s); return s; };
  const g = fillFaults(good);
  if (g.length) f.push(`the good face is rejected: ${g[0]}`);
  // Each mutant must be rejected FOR ITS OWN REASON (the fault class named beside it), not merely rejected.
  const M5 = [
    ['a toned bubble in the old blue', /^TONED FILL/, mut((s) => { s.bubbles[0].fill = '#3b82f6'; })],
    ['a null tone on the neutral centre', /^NO-TONE FILL ".*" is a colour of the ramp/, mut((s) => { s.bubbles[2].fill = '#eab308'; s.bubbles[3].fill = '#eab308'; s.legendHtml = legend('#eab308'); })],
    ['a null tone without the words', /^NO-TONE HOVER/, mut((s) => { s.bubbles[2].hover = 'Gamma; 2 articles collected'; })],
    ['a legend without the no-tone swatch', /^LEGEND lacks the no-tone swatch/, mut((s) => { s.legendHtml = legend(null); })],
    ['a face reading "market chatter"', /says "market chatter"/, mut((s) => { s.html = '<p>Bubble area is market chatter</p>'; })],
  ];
  let caught = 0;
  for (const [n, why, s] of M5) { const x = fillFaults(s); if (x.some((y) => why.test(y))) caught += 1; else f.push(`mutant "${n}" not rejected for its reason (${x.length ? x[0] : 'accepted'})`); }
  arms.push(['PLANTED: the fill predicate rejects 5 known-bad faces, each for its own reason, and accepts a known-good one', f.length === 0,
    f.length === 0 ? `${caught} of 5 rejected for their reason; the good one accepted` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`EVERY BUBBLE IS FILLED BY ITS SERVED TONE THROUGH THE ONE SHARED RAMP: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
