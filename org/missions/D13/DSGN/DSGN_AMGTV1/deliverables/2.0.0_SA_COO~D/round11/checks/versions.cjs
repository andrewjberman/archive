/**
 * versions.cjs -- DSGN_AMGTV1 round 11, AV-n-5: THE MODEL TAB SHOWS THE MODEL'S LANDED VERSIONS AND WHAT MOVED BETWEEN TWO OF
 * THEM, NAMING THE EARLIER VERSION (round-10 analysis s.2 cell 5, routed from AMGT_RESAPP round-51 ruling 1; RESAPP FWD-6).
 *
 * Usage (repo root): node <this file>
 * RESAPP FWD-6 (AMGT_RESAPP_PRD.md:469-474): "An analyst returns to a company researched before and can say what moved, naming the
 * earlier version that shows it." The deployed scoped API serves `GET /security/{key}/versions` (versions[{stamp, object_key}],
 * newest LAST; denominators.versions; latest; read) and `GET /security/{key}/compare?from=&to=` (compared{from_stamp, to_stamp,
 * added[], removed[], changed[{figure, mnemonic, fiscal_year, scope, from, to}]}, denominators{added, removed, changed, unchanged,
 * figures_from, figures_to}, reason, read); the portal has no caller. The contract (AV-n-5's face): hooks `useModelVersions(key)`
 * and `useModelCompare(key, from, to)` in hooks/useLeadPanelApi.ts; the Model tab renders a versions section on
 * `[data-model-versions]`, one `[data-model-version="<stamp>"]` per landed version, and a compare on `[data-model-compare]`.
 * Fixtures (round11/fixtures, SERVED, captured at the cut): BA US /thesis, /versions (13 stamps) and /compare?from=<oldest>&to=
 * <newest> (212 added, 0 removed, 7 changed, 172 unchanged). ISSUER VARIANTS (labelled, in memory): a compare with `compared: null`
 * and its served-shape reason; a versions read with status READ_FAILED.
 * Arms:
 *   1  the versions listed: 13 `[data-model-version]` elements carrying the served stamps, newest first; each version's date in the
 *      long form in visible text; no raw stamp ("20260929T024521Z") in visible text
 *   2  what moved, naming the earlier version: by default the page asks `useModelCompare(key, <oldest stamp>, <newest stamp>)`; the
 *      compare shows the served counts (212 added, 0 removed, 7 changed, 172 unchanged) and names the earlier version's date in the
 *      long form ("September 10th, 2026"); each of the 7 changed figures shows its served from and to values and a line name in
 *      words -- no raw mnemonic token (`CURR_ENTP_VAL`) in visible text
 *   3  a compare or versions read that cannot answer says why, in words: the `compared: null` variant shows its served reason; the
 *      READ_FAILED versions variant shows a designed sentence and no "READ_FAILED" token
 * Prints one line per arm and "VERSIONS AND WHAT MOVED: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const DU = (() => { try { return L.source('src/lib/dateUtils.ts'); } catch (e) { return {}; } })();
const longDate = (d) => String(DU.formatPanelTimestamp(null, d) || '').replace(/,\s*\d{1,2}:\d{2}[ap]\s*ET$/i, '');
const stampDay = (s) => `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`;

const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
const versions = S.unwrap(L.fixture('versions.BA_US_Equity.json'));
const compare = S.unwrap(L.fixture('compare.BA_US_Equity.oldest-latest.json'));
const stamps = versions.versions.map((v) => v.stamp);
const oldest = stamps[0];
const newest = stamps[stamps.length - 1];
const calls = [];
let V = versions;
let C = compare;
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === 'BA_US_Equity' ? thesis : (S.bundles[k] || undefined)),
  useModelVersions: () => V,
  useModelCompare: (k, from, to) => { calls.push([k, from, to]); return C; },
  useInputLedger: () => S.unwrap(L.fixture('ledger.BA_US_Equity.json')),
});
const MT = (() => { try { return L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); } catch (e) { return null; } })();
const render = () => { try { return MT ? L.render(MT.ModelTab, { securityKey: 'BA_US_Equity' }) : ''; } catch (e) { return 'RENDER FAILED ' + e.message; } };

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const html = render();
const vsec = L.innerOf(html, 'data-model-versions') || '';
const shown = [...vsec.matchAll(/data-model-version="([^"]+)"/g)].map((m) => m[1]);
if (JSON.stringify(shown) !== JSON.stringify([...stamps].reverse())) f1.push(`versions shown ${JSON.stringify(shown.slice(0, 4))}... (${shown.length}), want ${stamps.length} newest first`);
const vt = unesc(L.textOf(vsec));
for (const s of stamps) if (!vt.includes(longDate(stampDay(s)))) { f1.push(`version ${s}: its date "${longDate(stampDay(s))}" is not shown`); break; }
if (/\b\d{8}T\d{6}Z\b/.test(unesc(L.textOf(html)))) f1.push('a raw stamp in visible text');
const a1 = f1.length === 0;
const a1d = a1 ? `${stamps.length} landed versions listed newest first, each dated in the long form; no raw stamp visible` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
if (!calls.some(([k, from, to]) => k === 'BA_US_Equity' && from === oldest && to === newest)) f2.push(`useModelCompare calls ${JSON.stringify(calls.slice(0, 3))}, want (BA_US_Equity, ${oldest}, ${newest})`);
const csec = unesc(L.textOf(L.innerOf(html, 'data-model-compare') || ''));
const d = compare.denominators;
for (const [n, w] of [[d.added, 'added'], [d.removed, 'removed'], [d.changed, 'changed'], [d.unchanged, 'unchanged']]) {
  if (!new RegExp(`\\b${n}\\b[^.;]{0,30}${w}|${w}[^.;]{0,30}\\b${n}\\b`, 'i').test(csec)) f2.push(`the compare does not show ${n} ${w}`);
}
if (!csec.includes(longDate(stampDay(oldest)))) f2.push(`the earlier version's date "${longDate(stampDay(oldest))}" is not named`);
for (const c of compare.compared.changed) {
  const fromS = String(c.from); const toS = String(c.to);
  const num = (x) => csec.replace(/,/g, '').includes(String(Math.round(Number(x))).replace('-', '')) || csec.includes(String(x));
  if (!num(fromS) || !num(toS)) f2.push(`changed ${c.mnemonic}: its served from/to values are not shown`);
}
const mn = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/.exec(unesc(L.textOf(html)));
if (mn) f2.push(`a raw mnemonic "${mn[0]}" in visible text`);
const a2 = f2.length === 0;
const a2d = a2 ? `compared ${oldest} -> ${newest} by default; 212 added / 0 removed / 7 changed / 172 unchanged shown; the earlier version named; each change's values and line name in words` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
C = clone(compare); C.compared = null; C.reason = 'a comparison needs two landed stamps; BA_US_Equity has 1';
const h3 = unesc(L.textOf(render()));
if (!/a comparison needs two landed/i.test(h3)) f3.push('the compared-null reason is not shown');
C = compare;
V = clone(versions); V.versions = []; V.read = Object.assign({}, V.read, { status: 'READ_FAILED', read_completed: false, reason: 'the versions list did not complete' });
const h4 = unesc(L.textOf(render()));
if (/READ_FAILED/.test(h4)) f3.push('a raw READ_FAILED token in visible text');
if (!/versions?/i.test(unesc(L.textOf(L.innerOf(render(), 'data-model-versions') || '')))) f3.push('the READ_FAILED versions variant renders no designed sentence');
V = versions;
const a3 = f3.length === 0;
const a3d = a3 ? 'the compared-null variant shows its reason; the READ_FAILED variant a designed sentence with no status token' : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['the landed versions are listed, dated in words', a1, a1d],
  ['what moved, naming the earlier version', a2, a2d],
  ['a read that cannot answer says why', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`VERSIONS AND WHAT MOVED: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
