/**
 * timeline.cjs -- DSGN_AMGTV1 round 6, AV-u-1: THE TIMELINE PANEL -- A FAILED CALL READS IN WORDS, A PARTIAL DAY SAYS WHICH
 * PUBLISHERS WERE SEARCHED AND WHAT WAS FOUND, AND THE LEGEND READS ON THE BAND (round-5 analysis s.4 item 1 with section 2a;
 * FWD-5, FWD-11).
 *
 * Usage (repo root): node <this file>
 * Renders components/TimelinePanel.tsx with @tanstack/react-query's useQuery and recharts replaced by stubs, on SERVED /timeline
 * payloads captured at the cut from the deployed scoped API (round6/fixtures/timeline.992_HK_Equity.json -- 1 PARTIAL day,
 * searched "wsj", 0 articles; timeline.ASML_NA_Equity.json -- 74 PARTIAL days, searched "sa", 0 articles; and the served
 * /timeline/day body for 992 HK 2026-09-23). One ISSUER VARIANT entry (an unmapped code "zz" with 3 articles) is built in
 * memory from a served entry to exercise the fallback and the "N found" branch; it is labelled as such below.
 * The producer's "covered" (publishers_covered_codes) means the publisher's listing SEARCH reached that day -- not that it
 * wrote about the name (CTO~Z round-5 analysis section 2a). The served payload carries the searched count and codes and the
 * day's articles_total; it carries NO count of publishers not reached, so the page may not state one.
 * Arms:
 *   1  a failed call reads in words: a thrown fetch ("API request failed: 500 Internal Server Error - ") and a served error body
 *      ({error:true, error_code:"UPSTREAM_TIMEOUT", ...}) each render the panel's designed ERROR state (data-timeline-panel=
 *      "ERROR", never "LOADING"), and its visible text carries no HTTP status number, no "API request failed" / "Internal
 *      Server Error" transport text and no error_code token; a loading query still renders LOADING (the control)
 *   2  a PARTIAL day says what was searched, in words: the day tooltip for every served PARTIAL day (wsj, sa) and the variant,
 *      and the exported DayDissection for the served 992 HK day, each read "Searched:" + the publisher's name in words
 *      ("The Wall Street Journal", "Seeking Alpha") + "nothing found" (0 articles) or "<N> found"; the unmapped code reads in
 *      words, never raw; no visible text says "covered", carries a raw publisher code (wsj / sa / zz), a served field name
 *      (mention_score) or a bracketed status ([PARTIAL]); and no invented "Not reached: <number>" (not served)
 *   3  the legend reads on the band and the chart keeps its colours: every colour the legend's words use clears 4.5:1 on BOTH
 *      band rungs the timeline sits on -- --layer-body (221 45% 18%) and --layer-tile (221 40% 24%), resolved from index.css's
 *      .dark-band / body blocks (base: warning 4.31:1 and danger 3.93:1 on the tile); PARTIAL_BASE / DENIED_BASE fills unchanged
 * Prints one line per arm and "TIMELINE PANEL IN WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');
const L = require('./_load.cjs');
const React = L.React;
const TL = 'src/pages/SecurityAnalysis/components/TimelinePanel.tsx';

// ---- stubs -----------------------------------------------------------------------------------------------------------
const seen = [];
function rc(name) {
  const C = (props) => {
    const p = props || {};
    seen.push({ name, props: p });
    return React.createElement('div', { 'data-rc': name }, p.children);
  };
  C.displayName = name;
  return C;
}
const rcCache = {};
L.stubSource('recharts', new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (typeof k !== 'string') return undefined;
    if (!rcCache[k]) rcCache[k] = rc(k);
    return rcCache[k];
  },
}));
const q = { range: null, day: null };
L.stubSource('@tanstack/react-query', {
  __esModule: true,
  useQuery: (opts) => {
    const kind = opts && opts.queryKey ? opts.queryKey[1] : 'range';
    const s = q[kind] || { isLoading: false, isError: false, data: undefined };
    return { isLoading: false, isError: false, error: null, data: undefined, refetch: () => {}, ...s };
  },
});

// the api client reads import.meta.env at load; the useQuery stub above never calls it
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);

let mod = null;
try {
  mod = L.source(TL);
} catch (e) {
  console.log('load failed: ' + String(e.message).split('\n')[0]);
}
const Panel = mod && mod.TimelinePanel;
const render = (C, props) => {
  seen.length = 0;
  try {
    return L.render(C, props);
  } catch (e) {
    console.log('render failed: ' + String(e.message).split('\n')[0]);
    return '';
  }
};

// ---- arm 1: a failed call reads in words ------------------------------------------------------------------------------
const TRANSPORT = /\b[1-5]\d\d\b|API request failed|Internal Server Error|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;
q.range = { isError: true, error: new Error('API request failed: 500 Internal Server Error - ') };
const thrown = render(Panel, { securityKey: '992_HK_Equity' });
q.range = { data: { error: true, error_code: 'UPSTREAM_TIMEOUT', message: 'upstream timed out after 8 s' } };
const body = render(Panel, { securityKey: '992_HK_Equity' });
q.range = { isLoading: true };
const loading = render(Panel, { securityKey: '992_HK_Equity' });
const state = (h) => ((/data-timeline-panel="([A-Z_]+)"/.exec(h) || [])[1] || 'none');
const hit = (h) => (L.textOf(h).match(TRANSPORT) || [null])[0];
const a1 = state(thrown) === 'ERROR' && state(body) === 'ERROR' && state(loading) === 'LOADING' && !hit(thrown) && !hit(body);
const a1d = `thrown -> ${state(thrown)} (machine text: ${JSON.stringify(hit(thrown))}); error body -> ${state(body)} (machine text: ${JSON.stringify(hit(body))}); loading -> ${state(loading)}`;

// ---- arm 2: a PARTIAL day says what was searched ----------------------------------------------------------------------
const hk = L.fixture('timeline.992_HK_Equity.json').payload;
const asml = L.fixture('timeline.ASML_NA_Equity.json').payload;
const hkDay = L.fixture('timelineDay.992_HK_Equity.2026-09-23.json').payload;
const hkPartial = hk.series.filter((d) => d.data_status === 'PARTIAL');
const asmlPartial = asml.series.filter((d) => d.data_status === 'PARTIAL');
// ISSUER VARIANT (not served): a served ASML PARTIAL entry with an unmapped code and 3 articles, to exercise the fallback
// and the "<N> found" branch. Every other input to this arm is a served payload.
const variant = { ...asmlPartial[0], publishers_covered_codes: ['zz'], publishers_covered: 1, articles_total: 3 };
const WORDS = { wsj: 'The Wall Street Journal', sa: 'Seeking Alpha' };
q.range = { data: hk };
render(Panel, { securityKey: '992_HK_Equity' });
const tip = seen.find((e) => e.name === 'Tooltip');
const Content = tip && tip.props.content && tip.props.content.type;
const tipText = (entry) => {
  if (!Content) return '';
  try {
    return L.textOf(L.render(Content, { active: true, payload: [{ payload: entry }] }));
  } catch (e) {
    return 'render failed: ' + String(e.message).split('\n')[0];
  }
};
const BAD = /covered|\bwsj\b|\bsa\b|\bzz\b|mention_score|\[(PARTIAL|DENIED|COMPLETE)\]|Not reached:\s*\d/i;
const cases = [];
for (const e of [hkPartial[0], asmlPartial[0], asmlPartial[asmlPartial.length - 1]]) {
  const code = (e.publishers_covered_codes || [])[0];
  const t = tipText(e);
  cases.push({ where: `tooltip ${e.date} (${code})`, t, ok: /Searched:/.test(t) && t.includes(WORDS[code]) && /nothing found/i.test(t) && !BAD.test(t) });
}
{
  const t = tipText(variant);
  cases.push({ where: 'tooltip variant (zz, 3 articles)', t, ok: /Searched:/.test(t) && /\b3 found\b/.test(t) && !BAD.test(t) });
}
const Dissection = mod && mod.DayDissection;
if (Dissection) {
  q.day = { data: hkDay };
  const t = L.textOf(render(Dissection, { securityKey: '992_HK_Equity', date: '2026-09-23' }));
  cases.push({ where: 'DayDissection 992 HK 2026-09-23', t, ok: /Searched:/.test(t) && t.includes(WORDS.wsj) && /nothing found/i.test(t) && !BAD.test(t) });
} else {
  cases.push({ where: 'DayDissection', t: 'not exported', ok: false });
}
const bad2 = cases.filter((c) => !c.ok);
const a2 = cases.length === 5 && bad2.length === 0;
const a2d = `${cases.length - bad2.length} of ${cases.length} readings in words` +
  (bad2.length ? `; first failing: ${bad2[0].where}: "${String(bad2[0].t).slice(0, 140)}"` : '');

// ---- arm 3: legend contrast on both band rungs; fills unchanged -------------------------------------------------------
const ov = (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]).find(([k]) => k === TL);
const src = fs.readFileSync(ov ? ov[1] : path.join(L.base, TL), 'utf8');
const consts = {};
for (const m of src.matchAll(/^const ([A-Z_]+) = '([^']*)'/gm)) consts[m[1]] = m[2];
const legend = L.innerOf(src.replace(/\{' -- '\}/g, ''), 'data-timeline-legend') || '';
const exprs = [...legend.matchAll(/color:\s*([^}]+?)\s*\}/g)].map((m) => m[1].trim()).map((e) => (/^'.*'$/.test(e) ? e.slice(1, -1) : consts[e] !== undefined ? consts[e] : e));
const css = fs.readFileSync(path.join(L.base, 'src/index.css'), 'utf8');
const bandBlock = (css.split('.dark-band {')[1] || '').split('}')[0];
const tok = (name) => {
  const m = new RegExp('--' + name + ':\\s*([0-9.]+)\\s+([0-9.]+)%\\s+([0-9.]+)%').exec(bandBlock);
  return m ? [Number(m[1]), Number(m[2]), Number(m[3])] : null;
};
function hsl2rgb([h, s, l]) {
  s /= 100; l /= 100;
  const k = (n) => (n + h / 30) % 12;
  const a = s * Math.min(l, 1 - l);
  const f = (n) => l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)));
  return [f(0) * 255, f(8) * 255, f(4) * 255];
}
const hex2rgb = (h) => [0, 2, 4].map((i) => parseInt(h.slice(1 + i, 3 + i), 16));
const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
const ratio = (a, b) => { const x = lum(a); const y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
const BAND_INK = hex2rgb('#E8ECF5'); // --palette-white, the band's own ink (portal/CLAUDE.md colour law)
const resolve = (e) => {
  if (e === 'currentColor' || e === 'hsl(var(--palette-white))') return BAND_INK;
  const m = /^hsl\(var\(--([a-z-]+)\)\)$/.exec(e);
  if (m && tok(m[1])) return hsl2rgb(tok(m[1]));
  if (/^#[0-9a-fA-F]{6}$/.test(e)) return hex2rgb(e);
  return null;
};
const RUNGS = { 'layer-body': hsl2rgb([221, 45, 18]), 'layer-tile': hsl2rgb([221, 40, 24]) };
const readings = exprs.map((e) => {
  const c = resolve(e);
  return { e, body: c ? ratio(c, RUNGS['layer-body']) : 0, tile: c ? ratio(c, RUNGS['layer-tile']) : 0 };
});
const fillsKept = consts.DENIED_BASE === 'hsl(var(--status-danger))' && consts.PARTIAL_BASE === 'hsl(var(--status-warning))';
const a3 = exprs.length >= 3 && readings.every((r) => r.body >= 4.5 && r.tile >= 4.5) && fillsKept;
const a3d = `${readings.map((r) => `${r.e} body ${r.body.toFixed(2)} tile ${r.tile.toFixed(2)}`).join('; ')}; fills kept ${fillsKept}`;

const arms = [
  ['a failed call reads in words (designed ERROR state, no transport text)', a1, a1d],
  ['a PARTIAL day says which publishers were searched and what was found', a2, a2d],
  ['the legend clears 4.5:1 on both band rungs; the chart fills unchanged', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`TIMELINE PANEL IN WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
