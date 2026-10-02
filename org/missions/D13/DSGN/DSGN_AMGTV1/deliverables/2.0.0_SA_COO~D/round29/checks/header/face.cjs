/**
 * face.cjs -- DSGN_AMGTV1 round 29, AV-zg-2 OVERLAY HEADER (issuer 2.0.0_SA_COO~D): THE HEADER IS ONE LIGHT FACE, AT REST IN THE BOOK ORDER.
 *
 * Usage: cd <dir whose portal/ is the checkout under test> && node <this file>
 *   (e.g. cd C:/tmp/wk-dsgn-amgtv1-70). Static renders only; no network, no AWS, writes no file.
 * Grades (PRD v0.10 @175e4081b1):
 *   FWD-12 (header half): the identity header is a white hairline panel with navy ink (the /philosophy GraphicCard face); no white
 *     panel, strip or card inside a dark container (lightOnDark == 0); the header holds no dark band (CTO fold ruling 1: "FWD-12's
 *     identity header leaves the band"); the header region follows the /book L0 order.
 *   SAUX-02: no white card on a dark container. SAUX-05: no filled #5F3BE3 primary on a dark container; Refresh stays.
 *   SAUX-15: at rest the overlay shows the identity, the key figures, then recent news (HeaderBrief, its own card ABOVE the timeline),
 *     then the timeline (TimelinePanel); posture, the dossier line and the chatter/breakout readings open from a details control,
 *     never stacked at rest; the posture line and "identity as of ..." do not repeat.
 *   FWD-24 header limbs (CONTROL, must keep passing): the "Breakout (price)" cell reads the breakout row with places moved, and the
 *     readings show the latest served day.
 * Render: round15/checks/_load.cjs (the real page sources), with these issuer stubs so the ground law is visible in static markup:
 *   the REAL Panel (panels/Panel.tsx), the REAL buttonClass (Controls.tsx), the REAL GraphicCard and the REAL DataTooltip replace the
 *   loader's empty proxies; HeaderBrief and TimelinePanel (AV-zg-1's files) are MARKERS (`data-check-stub="HeaderBrief"` renders the
 *   `postureLine` prop it is handed, at rest; `data-check-stub="TimelinePanel"`), so this check grades only SecurityOverlay's own
 *   composition; GraphicPanel (the card's navy top) stays the loader stub `data-stub="GraphicPanel"` and is read as a navy card face.
 * Ground census (visible elements outside any [role=tooltip]; class tokens without a variant prefix):
 *   DARK own ground  dark-band | bg-[hsl(var(--bg-band|bg-header|palette-navy|palette-indigo))] | bg-[hsl(224_58%_20%)] | bg-black |
 *                    bg-{zinc,slate,gray,neutral}-{800,900} | data-stub="GraphicPanel"
 *   LIGHT own ground bg-white[/N] | bg-[hsl(var(--bg-surface|palette-white|bg-page|card|background))] | bg-card | bg-background
 *   band        a DARK own-ground element that is not a GraphicPanel, not a button and not inside another dark element
 *   lightOnDark a LIGHT own-ground element whose nearest grounded ancestor is DARK
 *   lightInk    an element carrying text-white[/N] | text-[hsl(var(--palette-white|palette-mediumGray))] with visible text, whose
 *               effective ground (own, else nearest ancestor, else the light page canvas) is LIGHT
 *   primaryOnDark an element filled bg-[hsl(var(--semantic-action-primary|primary))] | bg-[#5F3BE3] | bg-primary whose nearest
 *               grounded ancestor is DARK
 * AT REST = not inside a closed native <details> (its <summary> excepted), not inside [role=tooltip], not inside class `hidden`.
 * Inputs: round15/fixtures/r15c.overlay.{BA_US,VLO_US,6501_JP}_Equity.json (BA with the served display_name "The Boeing Company", as
 *   round20 namecard.cjs); round14/fixtures/thesisBundle.{BA_US,VLO_US}_Equity.json and round15/fixtures/
 *   r15c.thesisBundle.6501_JP_Equity.live.json (the dossier line); a monthly chatter payload built here (round19 chattercell.cjs shape).
 * Arms:
 *   1  LIGHT FACE (FWD-12, SAUX-02, SAUX-05): in the loaded, loading, error and no-data states: 0 bands, lightOnDark 0, lightInk 0,
 *      primaryOnDark 0; loaded: the [data-identity-card] sits on a white ground (not the bare canvas) and a Refresh control
 *      ([data-header-action="refresh"] or [data-primary-action="refresh"]) still renders.
 *   2  AT REST, IN ORDER (SAUX-15, FWD-12 L0): at rest, in document order: [data-identity-card] < the ONE [data-key-figures] < the
 *      HeaderBrief marker < the TimelinePanel marker (each exactly once, each at rest); [data-header-posture] (exactly 1),
 *      [data-header-reading], the "Breakout (price)" label and [data-axis-footnote] are in the markup but NOT at rest;
 *      [data-header-dossier-position] is not at rest; no other text is stacked at rest (visible at-rest text outside the identity
 *      card / name, the key figures, the two markers, buttons and <summary> is empty); "identity as of" appears at most once over
 *      the header plus IdentityLine's own render of the same identity.
 *   3  CONTROL FWD-24 (passes at base by design; must keep passing): BA and VLO: the "Breakout (price)" cell prints the served
 *      #rank, pct_jump_pct at its printed precision (never Trending's value, never x100) and places moved in words; the cell plus
 *      [data-axis-footnote] show the served as_of_date in words and no other day; the header says no "today" and no absence word
 *      (not served / unsupported / ABSENT / REFUSED). 6501 (breakout truly absent): the cell prints no number and carries the
 *      served absent_reason's words.
 *   4  PLANTED: the arm 1-3 predicates reject a white card on a band, a primary on a band, white ink on white, a posture line at
 *      rest, the timeline above the news, an open <details>, a stray line at rest, a breakout x100 and a dropped places-moved;
 *      they accept a correct synthetic face.
 * Prints one line per arm and "THE HEADER IS ONE LIGHT FACE, AT REST IN THE BOOK ORDER: <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const DROOT = path.join(__dirname, '..', '..', '..');
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const h = L.React.createElement;
const readFix = (p) => { const x = JSON.parse(fs.readFileSync(path.join(DROOT, p), 'utf8')); return x && x.payload && (x._capture_note || x._capture) ? x.payload : x; };

// ---- the HTML tree --------------------------------------------------------------------------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&amp;/g, '&');
function parse(html) {
  const root = { tag: '#root', attrs: {}, children: [], parent: null, start: -1 };
  let cur = root;
  const re = /<!--[\s\S]*?-->|<(\/?)([a-zA-Z][a-zA-Z0-9-]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>|([^<]+)/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[0].startsWith('<!--')) continue;
    if (m[5] !== undefined) { cur.children.push({ text: decode(m[5]), parent: cur }); continue; }
    const tag = m[2].toLowerCase();
    if (m[1]) { let n = cur; while (n && n.tag !== tag) n = n.parent; if (n && n.parent) cur = n.parent; continue; }
    const attrs = {};
    const ar = /([^\s=]+)(?:="([^"]*)")?/g;
    let a;
    while ((a = ar.exec(m[3])) !== null) attrs[a[1]] = a[2] === undefined ? '' : decode(a[2]);
    const node = { tag, attrs, children: [], parent: cur, start: m.index };
    cur.children.push(node);
    if (!m[4] && !VOID.has(tag)) cur = node;
  }
  return root;
}
function elements(node, out = []) { for (const c of node.children || []) if (c.tag) { out.push(c); elements(c, out); } return out; }
function textNodes(node, out = []) { for (const c of node.children || []) { if (c.tag) textNodes(c, out); else out.push(c); } return out; }
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
const textOf = (node) => norm(textNodes(node).map((t) => t.text).join(' '));
const ownText = (node) => norm((node.children || []).filter((c) => !c.tag).map((c) => c.text).join(' '));
const ancestors = (n) => { const out = []; for (let p = n.parent; p; p = p.parent) out.push(p); return out; };
const has = (n, attr, val) => n.attrs && Object.prototype.hasOwnProperty.call(n.attrs, attr) && (val === undefined || n.attrs[attr] === val);
const tokens = (n) => String((n.attrs && n.attrs.class) || '').split(/\s+/).filter((t) => t && !t.includes(':'));
const isTooltip = (n) => n.attrs && n.attrs.role === 'tooltip';
const inTooltip = (n) => [n, ...ancestors(n)].some((x) => x.attrs && isTooltip(x));

const DARK_TOK = [/^dark-band$/, /^bg-\[hsl\(var\(--(bg-band|bg-header|palette-navy|palette-indigo)\)\)\]$/, /^bg-\[hsl\(224_58%_20%\)\]$/, /^bg-black$/, /^bg-(zinc|slate|gray|neutral)-(800|900)$/];
const LIGHT_TOK = [/^bg-white(\/\d+)?$/, /^bg-\[hsl\(var\(--(bg-surface|palette-white|bg-page|card|background)\)\)\]$/, /^bg-card$/, /^bg-background$/];
const INK_TOK = [/^text-white(\/\d+)?$/, /^text-\[hsl\(var\(--(palette-white|palette-mediumGray)\)\)\]$/];
const PRIMARY_TOK = [/^bg-\[hsl\(var\(--(semantic-action-primary|primary)\)\)\]$/, /^bg-\[#5F3BE3\]$/i, /^bg-primary$/];
const anyTok = (n, set) => tokens(n).some((t) => set.some((re) => re.test(t)));
function ownGround(n) {
  if (!n.attrs) return null;
  if (n.attrs['data-stub'] === 'GraphicPanel') return 'dark';
  if (anyTok(n, DARK_TOK)) return 'dark';
  if (anyTok(n, LIGHT_TOK)) return 'light';
  return null;
}
function nearestAncestorGround(n) { for (const p of ancestors(n)) { const g = ownGround(p); if (g) return g; } return 'canvas'; }
const effGround = (n) => ownGround(n) || nearestAncestorGround(n);

/** Arm 1's predicate over one rendered header. */
function lightCensus(html) {
  const els = elements(parse(html)).filter((n) => !inTooltip(n));
  const c = { bands: 0, lightOnDark: 0, lightInk: 0, primaryOnDark: 0, first: [] };
  const note = (k, n) => { c[k] += 1; if (c.first.length < 4) c.first.push(`${k}: <${n.tag} ${String(n.attrs.class || n.attrs['data-stub'] || '').slice(0, 60)}> "${textOf(n).slice(0, 40)}"`); };
  for (const n of els) {
    const g = ownGround(n);
    if (g === 'dark' && n.attrs['data-stub'] !== 'GraphicPanel' && n.tag !== 'button' && !ancestors(n).some((p) => ownGround(p) === 'dark')) note('bands', n);
    if (g === 'light' && nearestAncestorGround(n) === 'dark') note('lightOnDark', n);
    if (anyTok(n, INK_TOK) && textOf(n) && (g || nearestAncestorGround(n)) !== 'dark') note('lightInk', n);
    if (anyTok(n, PRIMARY_TOK) && nearestAncestorGround(n) === 'dark') note('primaryOnDark', n);
  }
  return c;
}

/** AT REST: not in a closed <details> (its <summary> excepted), not in a tooltip, not in class `hidden` / [hidden]. */
function atRest(n) {
  const chain = [n, ...ancestors(n)];
  for (let i = 0; i < chain.length; i += 1) {
    const x = chain[i];
    if (!x.attrs) continue;
    if (isTooltip(x)) return false;
    if (has(x, 'hidden') || tokens(x).includes('hidden')) return false;
    if (x.tag === 'details' && !has(x, 'open')) { const below = chain[i - 1]; if (!(below && below.tag === 'summary')) return false; }
  }
  return true;
}

/** Arm 2's predicate. `idLineText` = IdentityLine's own visible text for the same identity. */
function restFaults(html, idLineText) {
  const f = [];
  const root = parse(html);
  const els = elements(root);
  const pick = (pred) => els.filter(pred);
  const one = (name, list) => { if (list.length !== 1) { f.push(`ORDER: ${list.length} ${name} (want exactly 1)`); return null; } if (!atRest(list[0])) { f.push(`ORDER: ${name} is not at rest`); return null; } return list[0]; };
  const idn = one('[data-identity-card]', pick((n) => has(n, 'data-identity-card')));
  const kf = one('[data-key-figures]', pick((n) => has(n, 'data-key-figures')));
  const news = one('HeaderBrief (recent news) marker', pick((n) => n.attrs['data-check-stub'] === 'HeaderBrief'));
  const tl = one('TimelinePanel marker', pick((n) => n.attrs['data-check-stub'] === 'TimelinePanel'));
  const seq = [['identity', idn], ['key figures', kf], ['recent news', news], ['timeline', tl]].filter(([, n]) => n);
  for (let i = 1; i < seq.length; i += 1) if (seq[i][1].start < seq[i - 1][1].start) f.push(`ORDER: ${seq[i][0]} renders above ${seq[i - 1][0]}`);
  const posture = pick((n) => has(n, 'data-header-posture'));
  if (posture.length !== 1) f.push(`POSTURE: ${posture.length} posture line(s) in the header markup (want exactly 1, behind the details control)`);
  const breakoutLabel = pick((n) => ownText(n) === 'Breakout (price)');
  const reading = pick((n) => has(n, 'data-header-reading'));
  const foot = pick((n) => has(n, 'data-axis-footnote'));
  for (const [name, list, need] of [['the posture line', posture, true], ['the dossier line', pick((n) => has(n, 'data-header-dossier-position')), false],
    ['a chatter reading [data-header-reading]', reading, true], ['the "Breakout (price)" label', breakoutLabel, true], ['the axis footnote', foot, true]]) {
    if (need && list.length === 0) f.push(`REACH: ${name} is not in the markup (it opens from the details control, never vanishes)`);
    const rest = list.filter(atRest);
    if (rest.length) f.push(`AT REST: ${name} is stacked at rest ("${textOf(rest[0]).slice(0, 70)}")`);
  }
  const EXCL = (n) => has(n, 'data-identity-card') || has(n, 'data-identity-name') || has(n, 'data-key-figures') || has(n, 'data-check-stub') || n.tag === 'button' || n.tag === 'summary';
  const residue = norm(textNodes(root).filter((t) => {
    let p = t.parent;
    if (!atRest(p)) return false;
    for (; p && p.tag !== '#root'; p = p.parent) if (EXCL(p)) return false;
    return true;
  }).map((t) => t.text).join(' '));
  if (residue.replace(/[\s.,;:|()-]+/g, '')) f.push(`STACKED: text at rest outside the identity, key figures, news and timeline: "${residue.slice(0, 90)}"`);
  const vis = textOf(root);
  const asOf = (vis.match(/identity as of/gi) || []).length + (String(idLineText || '').match(/identity as of/gi) || []).length;
  if (asOf > 1) f.push(`REPEAT: "identity as of" prints ${asOf} times (header ${(vis.match(/identity as of/gi) || []).length}, IdentityLine ${(String(idLineText || '').match(/identity as of/gi) || []).length}); want at most 1`);
  return f;
}

// ---- FWD-24 control predicate (round15 headerread.cjs, narrowed to the breakout cell and the served day) --------------------------
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const LONG_DATE = new RegExp(`\\b(${MONTHS.join('|')}) (\\d{1,2})(?:st|nd|rd|th)?,? (\\d{4})\\b`, 'g');
const longDays = (s) => { const out = []; let m; LONG_DATE.lastIndex = 0; while ((m = LONG_DATE.exec(s)) !== null) out.push(`${m[3]}-${String(MONTHS.indexOf(m[1]) + 1).padStart(2, '0')}-${m[2].padStart(2, '0')}`); return out; };
const dayWords = (iso) => { const [y, mo, d] = iso.split('-').map(Number); return new RegExp(`\\b${MONTHS[mo - 1]} ${d}(?:st|nd|rd|th)?,? ${y}\\b`); };
const percents = (s) => { const out = []; const re = /([-+]?\d+(?:\.(\d+))?)\s*%/g; let m; while ((m = re.exec(s)) !== null) out.push({ v: Number(m[1]), tol: 0.5 * Math.pow(10, -((m[2] || '').length)) + 1e-9, raw: m[0] }); return out; };
const near = (p, v) => Math.abs(Math.abs(p.v) - Math.abs(v)) <= p.tol && (p.v === 0 || v === 0 || Math.sign(p.v) === Math.sign(v) || !/[-+]/.test(p.raw));
const STOP = new Set(['this', 'that', 'with', 'from', 'have', 'there', 'their', 'which', 'were', 'been', 'into', 'than', 'then', 'each', 'among']);
const reasonWords = (r) => Array.from(new Set(String(r || '').toLowerCase().split(/[^a-z]+/).filter((w) => w.length >= 4 && !STOP.has(w))));
const axisRead = (ov, mv, sb) => (ov.axis_reads || []).find((e) => e.movement === mv && e.subject === sb);
function breakoutFaults(name, html, ov) {
  const f = [];
  const root = parse(html);
  const els = elements(root);
  const label = els.find((n) => ownText(n) === 'Breakout (price)');
  if (!label) return [`${name}: no element whose own text is "Breakout (price)"`];
  const cell = textOf(label.parent).replace('Breakout (price)', '').trim();
  const foot = els.filter((n) => has(n, 'data-axis-footnote')).map(textOf).join(' ');
  const bp = axisRead(ov, 'BREAKOUT', 'PRICE');
  const tp = axisRead(ov, 'TRENDING', 'PRICE');
  const row = (bp && bp.row) || ov.breakout_price || null;
  if (row) {
    if (!cell.includes(`#${row.rank}`)) f.push(`${name}: the breakout cell does not print the served rank #${row.rank}: "${cell.slice(0, 80)}"`);
    const v = row.pct_jump_pct;
    const ps = percents(cell);
    const decoy = tp && tp.row ? tp.row.return_30d_pct : null;
    if (!ps.length) f.push(`${name}: the breakout cell prints no percent (served ${v})`);
    for (const p of ps) {
      if (decoy !== null && near(p, decoy) && !near(p, v)) f.push(`${name}: the breakout cell reads the Trending value ${p.raw}`);
      else if (near(p, v * 100) && !near(p, v)) f.push(`${name}: the breakout cell prints ${p.raw}, 100x the served ${v}`);
      else if (!near(p, v)) f.push(`${name}: the breakout cell prints ${p.raw}, not the served ${v}`);
    }
    const pm = row.places_moved;
    if (typeof pm === 'number') {
      const ok = pm === 0 ? /\bunchanged\b|\bno change\b|\b0 places?\b|\bdid not move\b/i.test(cell) : new RegExp(`(^|[^0-9.])${Math.abs(pm)}\\s+places?\\b`, 'i').test(cell);
      if (!ok) f.push(`${name}: the breakout cell does not print places moved (${pm}): "${cell.slice(0, 80)}"`);
    }
  } else {
    const words = reasonWords(bp && bp.absent_reason);
    if (/#\d|%/.test(cell)) f.push(`${name}: the truly-absent breakout cell prints a number: "${cell.slice(0, 80)}"`);
    const missing = words.filter((w) => !cell.toLowerCase().includes(w));
    if (!words.length) f.push(`${name}: the fixture carries no absent_reason`);
    else if (missing.length) f.push(`${name}: the truly-absent breakout cell misses the served reason's words ${missing.join(', ')}: "${cell.slice(0, 90)}"`);
  }
  const asOf = (bp && bp.as_of_date) || (row && row.as_of_date);
  const readings = `${cell} ${foot}`;
  if (!asOf) f.push(`${name}: the fixture carries no as_of_date`);
  else {
    if (!dayWords(asOf).test(readings)) f.push(`${name}: the readings do not show the served day ${asOf} in words: "${readings.slice(0, 110)}"`);
    const wrong = longDays(readings).filter((d) => d !== asOf);
    if (wrong.length) f.push(`${name}: the readings show a day the payload did not serve (${wrong.join(', ')})`);
  }
  const all = textOf(root);
  if (/\btoday\b/i.test(all)) f.push(`${name}: the header says "today"`);
  const hit = /not served|unsupported|\bABSENT\b|\bREFUSED\b/.exec(all);
  if (hit) f.push(`${name}: absence word "${hit[0]}" in the header text`);
  return f;
}

// ---- stubs + fixtures -----------------------------------------------------------------------------------------------------
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);
L.stubSource('@tanstack/react-query', { __esModule: true,
  useQuery: () => ({ isLoading: false, isError: false, error: null, data: undefined, refetch: () => {} }),
  useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }) });
let setupError = null;
try {
  L.stubSource('src/ui/components/Controls.tsx', L.source('src/ui/components/Controls.tsx'));
  const realPanel = L.source('src/ui/components/panels/Panel.tsx').Panel;
  const stubCache = {};
  const panels = new Proxy({}, { get(_t, k) {
    if (k === '__esModule') return true;
    if (k === 'Panel') return realPanel;
    if (typeof k !== 'string') return undefined;
    if (!stubCache[k]) { const C = (p) => h('div', { 'data-stub': k }, (p || {}).children); C.displayName = k; stubCache[k] = C; }
    return stubCache[k];
  } });
  for (const k of ['src/ui/components/panels/index.ts', 'src/ui/components/panels']) L.stubSource(k, panels);
  L.stubSource('src/ui/components/graphic/GraphicCard.tsx', L.source('src/ui/components/graphic/GraphicCard.tsx'));
  L.stubSource('src/components/DataTooltip.tsx', L.source('src/components/DataTooltip.tsx'));
  const TL = (p) => h('div', { 'data-check-stub': 'TimelinePanel', 'data-security-key': (p || {}).securityKey || '' });
  L.stubSource(SA + 'components/TimelinePanel.tsx', { __esModule: true, TimelinePanel: TL });
  const realBrief = L.source(SA + 'components/HeaderBrief.tsx');
  const HB = (p) => h('div', { 'data-check-stub': 'HeaderBrief' }, (p || {}).postureLine);
  L.stubSource(SA + 'components/HeaderBrief.tsx', Object.assign({}, realBrief, { HeaderBrief: HB }));
} catch (e) { setupError = 'STUB SETUP: ' + String(e.message).split('\n')[0]; }

const KEYS = ['BA_US_Equity', 'VLO_US_Equity', '6501_JP_Equity'];
const OV = {};
for (const k of KEYS) OV[k] = readFix(`round15/fixtures/r15c.overlay.${k}.json`);
OV.BA_US_Equity = Object.assign({}, OV.BA_US_Equity, { display_name: 'The Boeing Company', display_name_source: 'crosswalk' });
const THESIS = {
  BA_US_Equity: readFix('round14/fixtures/thesisBundle.BA_US_Equity.json'),
  VLO_US_Equity: readFix('round14/fixtures/thesisBundle.VLO_US_Equity.json'),
  '6501_JP_Equity': readFix('round15/fixtures/r15c.thesisBundle.6501_JP_Equity.live.json'),
};
const CHATTER = { as_of: '2026-09-30', source: 'harvest gold chatter_daily', months: ['2026-09', '2026-10'], partial_months: ['2026-10'],
  rows: [{ security_key: 'BA_US_Equity', display_name: 'The Boeing Co', by_month: { '2026-09': { collected: 7 }, '2026-10': { collected: 20 } } },
    { security_key: 'VLO_US_Equity', display_name: 'Valero Energy Corp', by_month: { '2026-10': { collected: 3 } } }] };
L.hookState.impl = { useThesisBundle: (k) => THESIS[k], useCollectedChatter: () => CHATTER, usePeerSet: () => undefined, useManagement: () => undefined };

const safe = (fn) => { try { return fn(); } catch (e) { return `<p data-render-failed="1">RENDER FAILED ${String(e.message).split('\n')[0].replace(/</g, '&lt;')}</p>`; } };
const header = (props) => safe(() => { const m = L.source(SA + 'components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, Object.assign({ onBack: () => {}, onRefresh: () => {} }, props)); });
const failed = (html) => /data-render-failed/.test(html);

// ---- arm 1 -----------------------------------------------------------------------------------------------------------------
const arms = [];
{
  const f = [];
  const tally = [];
  if (setupError) f.push(setupError);
  const states = [['loaded', { bundle: OV.BA_US_Equity }], ['loading', { isLoading: true }], ['error', { loadError: 'read failed' }], ['no data', { bundle: undefined }]];
  for (const [name, props] of states) {
    const html = header(props);
    if (failed(html)) { f.push(`${name}: ${parse(html).children.map(textOf).join(' ').slice(0, 100)}`); continue; }
    const c = lightCensus(html);
    tally.push(`${name} ${c.bands}/${c.lightOnDark}/${c.lightInk}/${c.primaryOnDark}`);
    if (c.bands || c.lightOnDark || c.lightInk || c.primaryOnDark) f.push(`${name}: bands ${c.bands}, lightOnDark ${c.lightOnDark}, lightInk ${c.lightInk}, primaryOnDark ${c.primaryOnDark} (${c.first.join('; ')})`);
    if (name === 'loaded') {
      const els = elements(parse(html));
      const card = els.find((n) => has(n, 'data-identity-card'));
      if (!card) f.push('loaded: no [data-identity-card]');
      else { const g = [card, ...ancestors(card)].map(ownGround).find(Boolean); if (g !== 'light') f.push(`loaded: the identity card sits on ${g || 'the bare canvas'}, not a white panel`); }
      if (!els.some((n) => n.attrs['data-header-action'] === 'refresh' || n.attrs['data-primary-action'] === 'refresh')) f.push('loaded: no Refresh control ([data-header-action="refresh"])');
    }
  }
  arms.push(['LIGHT FACE: no band, no white on dark, no white ink on white, no primary on dark, in all four states (FWD-12, SAUX-02, SAUX-05)', f.length === 0,
    (f.length === 0 ? 'bands/lightOnDark/lightInk/primaryOnDark ' + tally.join(', ') + '; identity card on white; Refresh renders' : `${f.length} fault(s): ${f.slice(0, 4).join(' | ')}`)]);
}

// ---- arm 2 -----------------------------------------------------------------------------------------------------------------
{
  let f = [];
  const html = header({ bundle: OV.BA_US_Equity });
  let idLine = '';
  try { idLine = textOf(parse(L.render(L.source(SA + 'components/IdentityLine.tsx').IdentityLine, { identity: OV.BA_US_Equity.identity }))); } catch (e) { f.push('IdentityLine RENDER: ' + String(e.message).split('\n')[0]); }
  if (failed(html)) f.push(textOf(parse(html)).slice(0, 120));
  else f = f.concat(restFaults(html, idLine));
  arms.push(['AT REST, IN ORDER: identity < key figures < recent news < timeline; posture, dossier and readings behind the details control; no repeat (SAUX-15, FWD-12)', f.length === 0,
    f.length === 0 ? 'order holds, 0 stacked lines, posture x1 behind details, "identity as of" <= 1' : `${f.length} fault(s): ${f.map((x) => x.slice(0, 110)).join(' | ')}`]);
}

// ---- arm 3 (CONTROL) -------------------------------------------------------------------------------------------------------
{
  const f = [];
  for (const k of KEYS) {
    const html = header({ bundle: OV[k] });
    if (failed(html)) { f.push(`${k}: ${textOf(parse(html)).slice(0, 100)}`); continue; }
    f.push(...breakoutFaults(k.replace(/_Equity$/, ''), html, OV[k]));
  }
  arms.push(['CONTROL FWD-24: the Breakout (price) cell reads the breakout row with places moved and the served day; 6501 says its served reason', f.length === 0,
    f.length === 0 ? 'BA #4 +6.65% up 3, VLO #9 +2.31% down 4, served day September 30th, 2026; 6501 absent reason in words; 0 "today", 0 absence words' : `${f.length} fault(s): ${f.slice(0, 4).join(' | ')}`]);
}

// ---- arm 4 (PLANTED) -------------------------------------------------------------------------------------------------------
{
  const f = [];
  const caught = [];
  const lightBad = (c) => c.bands + c.lightOnDark + c.lightInk + c.primaryOnDark > 0;
  const BAND = '<div class="w-full dark-band bg-[hsl(var(--bg-band))]">';
  const goodLight = '<div class="w-full border border-[hsl(var(--hairline))] bg-[hsl(var(--bg-surface))]"><div data-identity-card="" class="border border-black bg-white"><div data-stub="GraphicPanel"><span class="text-white">BA US</span></div><div class="text-black">Industrials</div></div><button data-header-action="refresh" class="border bg-[hsl(var(--bg-surface))] text-[hsl(var(--foreground))]">Refresh</button></div>';
  if (lightBad(lightCensus(goodLight))) f.push('a correct light face is rejected');
  const LM = [
    ['a white card on a band', BAND + '<div class="bg-white">BA US</div></div>', 'lightOnDark'],
    ['a primary on a band', BAND + '<button class="bg-[hsl(var(--semantic-action-primary))] text-white">Refresh</button></div>', 'primaryOnDark'],
    ['white ink on white', '<div class="bg-white"><div class="text-[hsl(var(--palette-white))]">The Boeing Company</div></div>', 'lightInk'],
    ['a band header', BAND + '<span>BA US</span></div>', 'bands'],
  ];
  for (const [n, html, k] of LM) { if (lightCensus(html)[k] > 0) caught.push(n); else f.push(`"${n}" not caught as ${k}`); }
  const DET = '<details><summary>Details</summary><p data-header-posture="SERVED">Posture: HOLD</p><div data-header-reading="chatter"><div>Chatter</div><div>Collected this month: 20</div></div><div><div>Breakout (price)</div><div>#4 | +6.65%, up 3 places</div></div><div data-axis-footnote="">Readings of September 30th, 2026.</div></details>';
  const ID = '<div data-identity-card=""><span>BA US</span><div>Industrials -- US</div></div>';
  const KF = '<div data-key-figures=""><div>Price USD 196.80</div></div>';
  const NEWS = '<div data-check-stub="HeaderBrief"></div>';
  const TLM = '<div data-check-stub="TimelinePanel"></div>';
  const goodRest = `<div>${ID}${KF}${NEWS}${TLM}${DET}</div>`;
  const gr = restFaults(goodRest, '');
  if (gr.length) f.push(`a correct at-rest face is rejected: ${gr[0]}`);
  const RM = [
    ['a posture line at rest', `<div>${ID}${KF}<div data-check-stub="HeaderBrief"><p data-header-posture="SERVED">Posture: HOLD</p></div>${TLM}${DET.replace('<p data-header-posture="SERVED">Posture: HOLD</p>', '')}</div>`, /AT REST: the posture line/],
    ['the timeline above the news', `<div>${ID}${KF}${TLM}${NEWS}${DET}</div>`, /ORDER: recent news renders above timeline|ORDER: timeline/],
    ['an open details', `<div>${ID}${KF}${NEWS}${TLM}${DET.replace('<details>', '<details open="">')}</div>`, /AT REST/],
    ['a stray line at rest', `<div>${ID}${KF}<p>No fund of record: the research team has no dossier for this name.</p>${NEWS}${TLM}${DET}</div>`, /STACKED/],
    ['"identity as of" twice', `<div>${ID.replace('Industrials -- US', 'identity as of September 29th, 2026')}${KF}${NEWS}${TLM}${DET}</div>`, /REPEAT/, 'identity as of September 29th, 2026'],
  ];
  for (const [n, html, want, idl] of RM) { const r = restFaults(html, idl || ''); if (r.some((x) => want.test(x))) caught.push(n); else f.push(`"${n}" not rejected (${r[0] || 'no fault'})`); }
  const BA = OV.BA_US_Equity;
  const synth = (cell) => `<div><div><div>Breakout (price)</div><div>${cell}</div></div><div data-axis-footnote="">Readings of September 30th, 2026.</div></div>`;
  const gb = breakoutFaults('synthetic', synth('#4 | +6.65%, up 3 places'), BA);
  if (gb.length) f.push(`a correct breakout cell is rejected: ${gb[0]}`);
  for (const [n, cell, want] of [['breakout x100', '#4 | +665.03%, up 3 places', /100x/], ['places moved dropped', '#4 | +6.65%', /places moved/]]) {
    const r = breakoutFaults('planted', synth(cell), BA);
    if (r.some((x) => want.test(x))) caught.push(n); else f.push(`"${n}" not rejected (${r[0] || 'no fault'})`);
  }
  arms.push(['PLANTED: white-on-band, primary-on-band, white-on-white, a band, posture at rest, timeline above news, open details, a stray line, a repeat, x100 and dropped places are rejected; correct faces pass', f.length === 0,
    f.length === 0 ? `${caught.length} of 11 plants rejected; 3 correct synthetic faces accepted` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE HEADER IS ONE LIGHT FACE, AT REST IN THE BOOK ORDER: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
