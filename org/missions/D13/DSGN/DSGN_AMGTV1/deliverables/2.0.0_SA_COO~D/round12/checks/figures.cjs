/**
 * figures.cjs -- DSGN_AMGTV1 round 12, AV-m-3: A PM NEVER PARSES A RAW FLOAT AND CAN STILL DISPUTE ANY HEADLINE FIGURE (FWD-13;
 * round-11 analysis ruling 3).
 *
 * Usage (repo root): node <this file>
 * FWD-13 (PRD v0.4 :139-148): "every figure on the four header cards carries its units and tabular numerals, its tooltip carries
 * the mnemonic and the full-precision value verbatim, and price, market cap, net debt, enterprise value, beta and short interest
 * each sit on one named card. ACCEPT: No 161867780096.00003 anywhere; every figure traceable to its field." Ruling 3: FWD-13 binds
 * EVERY rendered figure -- header cards, What-moved and rule lines; SHORT_INT_RATIO gets its line name from the served field names
 * (the served header figure's `basis.definition`), never a page-side dictionary guess.
 * The tooltip contract checked: a figure's element is accompanied by an element carrying `data-figure-tooltip="<MNEMONIC>"` and
 * the served value verbatim (String(value)) in `data-full-value` -- or, for a What-moved line, `data-full-from` and `data-full-to`
 * -- whose DataTooltip names the mnemonic and prints the full value (the page's StatTile pattern, `data-stat-tooltip`).
 * Fixtures (round12/fixtures, SERVED, captured at the cut): BA US /overlay, /thesis, /versions, /compare oldest -> newest (7
 * changed header figures incl. CUR_MKT_CAP 161867780096.00003 -> 155544819936.0 and SHORT_INT_RATIO 2.903939 -> 3.036011).
 * Arms:
 *   1  the header cards: every SERVED figure row of the four card windows (HeaderCardDetail) and every card face's lead figure is
 *      tabular and carries its tooltip (mnemonic + the served value verbatim); price, market cap, net debt, enterprise value, beta
 *      and short interest each sit on exactly one card
 *   2  what moved: each of the 7 changed lines shows its from and to with at most 4 fractional digits and no ungrouped integer of
 *      5+ digits, carries its tooltip (mnemonic, full from, full to, verbatim), and is named in words -- SHORT_INT_RATIO by its
 *      served definition, never "a line this page has no name for yet"; no raw mnemonic in visible text
 *   3  no raw float anywhere on the BA Model tab: its visible text holds 0 numbers with more than 4 fractional digits (the rule
 *      lines included), while the fiscal table still shows its served figures (control: BA 2016 EPS 7.92)
 * Prints one line per arm and "NO RAW FLOAT, EVERY FIGURE TRACEABLE: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const esc = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const overlay = S.unwrap(L.fixture('overlay.BA_US_Equity.json'));
const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
const versions = S.unwrap(L.fixture('versions.BA_US_Equity.json'));
const compare = S.unwrap(L.fixture('compare.BA_US_Equity.oldest-latest.json'));
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === 'BA_US_Equity' ? thesis : (S.bundles[k] || undefined)),
  useModelVersions: () => versions,
  useModelCompare: () => compare,
  useInputLedger: () => undefined,
});
const HC = (() => { try { return L.source('src/pages/SecurityAnalysis/components/HeaderCards.tsx'); } catch (e) { return null; } })();
const C = (() => { try { return L.source('src/pages/SecurityAnalysis/constants.ts'); } catch (e) { return {}; } })();
const MT = (() => { try { return L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); } catch (e) { return null; } })();
const safe = (f) => { try { return f(); } catch (e) { return 'RENDER FAILED ' + e.message; } };
const attrs = (tag) => Object.fromEntries([...tag.matchAll(/([a-zA-Z-]+)="([^"]*)"/g)].map((m) => [m[1], unesc(m[2])]));
const tooltipsIn = (html) => [...html.matchAll(/<[a-z]+[^>]*data-figure-tooltip="[^"]*"[^>]*>/g)].map((m) => attrs(m[0]));
const FRAC = /-?\d[\d,]*\.\d{5,}/g;
const UNGROUPED = /(?<![\d,.])\d{5,}(?![\d,])/g;
const served = Object.fromEntries((overlay.header_figures || []).map((f) => [f.mnemonic, f]));

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const cardOf = {};
let rows = 0;
for (const card of C.HEADER_CARD_DEFS || []) {
  const html = safe(() => L.render(HC.HeaderCardDetail, { cardKey: card.key, bundle: overlay }));
  for (const m of html.matchAll(/<li[^>]*data-card-figure-mnemonic="([^"]+)"[^>]*data-card-figure-state="SERVED"[^>]*>|<li[^>]*data-card-figure-state="SERVED"[^>]*data-card-figure-mnemonic="([^"]+)"[^>]*>/g)) {
    const mn = m[1] || m[2];
    rows += 1;
    (cardOf[mn] = cardOf[mn] || new Set()).add(card.key);
    const start = m.index;
    const end = html.indexOf('</li>', start);
    const li = html.slice(start, end);
    const tips = tooltipsIn(li).filter((t) => t['data-figure-tooltip'] === mn);
    if (!/tabular-nums/.test(li)) f1.push(`${card.key}/${mn}: the figure is not tabular`);
    if (tips.length === 0) f1.push(`${card.key}/${mn}: no tooltip carrying the mnemonic`);
    else if (served[mn] && tips[0]['data-full-value'] !== String(served[mn].value)) f1.push(`${card.key}/${mn}: tooltip value "${tips[0]['data-full-value']}", want "${String(served[mn].value)}"`);
  }
}
if (rows === 0) f1.push('no SERVED figure row rendered in any card window');
const face = safe(() => L.render(HC.HeaderCards, { bundle: overlay }));
const leads = [...face.matchAll(/data-header-card="([^"]+)"[\s\S]*?data-header-card-lead[\s\S]*?<\/button>/g)];
for (const m of leads) if (tooltipsIn(m[0]).length === 0) f1.push(`card face ${m[1]}: the lead figure carries no tooltip`);
for (const mn of ['PX_LAST', 'CUR_MKT_CAP', 'NET_DEBT', 'CURR_ENTP_VAL', 'EQY_BETA', 'SI_PERCENT_EQUITY_FLOAT']) {
  const n = cardOf[mn] ? cardOf[mn].size : 0;
  if (served[mn] && n !== 1) f1.push(`${mn} sits on ${n} cards, want exactly 1`);
}
const a1 = f1.length === 0;
const a1d = a1 ? `${rows} served card figures and ${leads.length} card faces, each tabular with a tooltip carrying its mnemonic and the served value verbatim; the six named figures on one card each` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const html = safe(() => L.render(MT.ModelTab, { securityKey: 'BA_US_Equity' }));
const csec = L.innerOf(html, 'data-model-compare') || '';
const lines = [...csec.matchAll(/<li[^>]*data-model-change="([^"]+)"[^>]*>([\s\S]*?)<\/li>/g)];
if (lines.length !== compare.compared.changed.length) f2.push(`${lines.length} changed lines rendered, want ${compare.compared.changed.length}`);
for (const c of compare.compared.changed) {
  const m = lines.find((x) => unesc(x[1]) === c.figure);
  if (!m) { f2.push(`${c.mnemonic}: no line`); continue; }
  const text = unesc(L.textOf(m[2]));
  const vis = text;
  const frac = vis.match(FRAC);
  const big = vis.match(UNGROUPED);
  if (frac) f2.push(`${c.mnemonic}: a raw float "${frac[0]}" in "${vis.slice(0, 90)}"`);
  if (big) f2.push(`${c.mnemonic}: an ungrouped figure "${big[0]}" in "${vis.slice(0, 90)}"`);
  const tips = tooltipsIn(m[0]).filter((t) => t['data-figure-tooltip'] === c.mnemonic);
  if (tips.length === 0) f2.push(`${c.mnemonic}: no tooltip carrying the mnemonic`);
  else if (tips[0]['data-full-from'] !== String(c.from) || tips[0]['data-full-to'] !== String(c.to)) f2.push(`${c.mnemonic}: tooltip from/to "${tips[0]['data-full-from']}"/"${tips[0]['data-full-to']}", want "${String(c.from)}"/"${String(c.to)}"`);
  if (/no name for yet/i.test(vis)) f2.push(`${c.mnemonic}: reads "${vis.slice(0, 60)}"`);
}
const sir = lines.find((x) => /SHORT_INT_RATIO/.test(unesc(x[1])));
const sirDef = served.SHORT_INT_RATIO && served.SHORT_INT_RATIO.basis && served.SHORT_INT_RATIO.basis.definition;
const sirName = sirDef ? String(sirDef).replace(/\.$/, '') : null;
if (sir && sirName && !new RegExp(esc(sirName.split(' (')[0]), 'i').test(unesc(L.textOf(sir[2])))) f2.push(`SHORT_INT_RATIO is not named by its served definition "${sirName}"`);
const mn = /\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/.exec(unesc(L.textOf(csec)));
if (mn) f2.push(`a raw mnemonic "${mn[0]}" in visible text`);
const a2 = f2.length === 0;
const a2d = a2 ? `${lines.length} changed lines: no raw float or ungrouped figure, each with a tooltip of its mnemonic and full from/to, each named (short interest ratio by its served definition)` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
const all = unesc(L.textOf(html));
const raw = all.match(FRAC) || [];
if (raw.length) f3.push(`${raw.length} number(s) with more than 4 fractional digits on the Model tab; first "${raw[0]}"`);
if (!/\b7\.92\b/.test(all)) f3.push('the control figure (BA 2016 EPS 7.92) is no longer shown');
const a3 = f3.length === 0;
const a3d = a3 ? `0 numbers with more than 4 fractional digits across the BA Model tab (${all.length} characters); the fiscal table still shows its served figures` : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['header cards: tabular, each with its mnemonic and full value; one card per named figure', a1, a1d],
  ['what moved: readable figures, each traceable to its field', a2, a2d],
  ['no raw float anywhere on the Model tab', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`NO RAW FLOAT, EVERY FIGURE TRACEABLE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
