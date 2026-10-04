/**
 * leadface.cjs -- DSGN_AMGTV1 round 29, AV-zg-3 LEAD PANEL + PRICE (issuer 2.0.0_SA_COO~D): THE LEAD PANEL IS ONE LIGHT CARD AND
 * SPEAKS READER WORDS.
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-70): node <this file>
 * Grades: PRD v0.10 FWD-12 v0.9, the Lead Panel half (DONE WHEN: "lightOnDark == 0 (no white panel, strip or card inside a dark
 *   container); the Lead Panel and the identity header are white hairline panels with navy ink, the /philosophy GraphicCard face").
 *   SAUX-01 (observed: "a dark container that holds a white control strip"; acceptance, CTO pick LIGHT: "white panels with navy ink").
 *   SAUX-30, the page subtitle only (observed: "Universe discovery, ranked server-side, above a per-name ..."; acceptance: replaced
 *   by reader words). SAUX-36 (observed: Details prints "generation 20261002T111010Z-a89fcf3c5f42 | state COMPLETE | 94 row(s)
 *   committed | coverage vintage bloomberg-dapi-boxside"; acceptance: "states the price list's date and source in words, with no
 *   generation id or system state token").
 * THE CONTRACT (the worker face quotes it):
 *   - LIGHT CARD: the REAL LeadPanel (components/LeadPanel.tsx, export LeadPanel) renders, on Price and on Chatter, a ROOT element
 *     with a white fill (`bg-white` or `bg-[hsl(var(--bg-surface))]`) and a `border` (e.g. Panel variant="nested", or the GraphicCard
 *     root); NO band anywhere in it: no `dark-band` class and no band background (`--bg-band`, `--bg-header`, `--bg-medium`,
 *     `--bg-card`, `--semantic-background-contentPanel`, `#0A1733`) -- so no Panel variant chart/mixed, PanelHeader, PanelFooter,
 *     SmartPanelFooter, DarkCard, NestedCard or SectionCard inside it. Light ink (`text-white*`, `text-[hsl(var(--palette-white))]`,
 *     `text-[hsl(var(--palette-mediumGray))]`, `text-[#E8ECF5]`, `text-[#A8B0C0]`, `text-<colour>-50..300`, `bg-white/N`, any
 *     `hover:`/`focus:`/`placeholder:` form of these) appears ONLY inside the GraphicCard's navy GraphicPanel, and no white fill sits
 *     inside that navy panel. The Chatter face mounts ChatterBubbles and hands it NO onMonthChange (ISSUER AMENDMENT 1, round 31:
 *     PRD FWD-26 replaces the month cursor with the 30D / 90D / 365D presets; round31/checks/presets/presets.cjs grades them).
 *   - READER WORDS: the page header's description (SecurityAnalysis.tsx, PageHeaderCleanBadge `description`) is at least three words
 *     and carries none of: "universe", "discovery", "server-side", "per-name", a " / " list, a code-shaped token. The Price face keeps
 *     ONE element carrying data-source-caption="detail" (the Details disclosure); its visible text and titles carry no generation id
 *     (`\d{8}T\d{6}Z-<hex>`, the served generation_id, a 12+ hex run), no system token ("state <CODE>", COMPLETE, SERVED, SHORT_READ,
 *     OVER_READ, NOT_SERVABLE, POINTER_UNREAD, ABSENT, EMPTY, UPPER_SNAKE, "row(s)", "vintage", "generation", "pointer",
 *     "bloomberg-dapi", "boxside", "blp_client", "127.0.0.1"), and on a served list it names the list's as_of_date in words and the
 *     source as "Bloomberg". data-* attributes may keep the machine values (data-generation-id stays).
 * Inputs: round29/fixtures/leadprice/rankings.trending.price.live.json (the served route, 94 rows, generation
 *   20261002T111010Z-a89fcf3c5f42, as_of_date 2026-10-01); a planted copy with ranking_status SHORT_READ; round16/fixtures/
 *   r16g.collected.chatter.json until round 31; since AMENDMENT 1 the Chatter face reads round31/fixtures/windows.chatter.30.json
 *   (the served 30-day window).
 * Render: ./_render.cjs (round15/_load.cjs over the real sources, with the REAL Panel / PanelContent / band-valued panel primitives
 *   and the REAL GraphicCard, so a band renders its own class). SecurityAnalysis is rendered with its tabs, LeadPanel, IdentityHeader,
 *   PrintExportAction, PageThemeProvider and useTabNavigation stubbed, and PageHeaderCleanBadge stubbed to print its `description`.
 * Arms:
 *   1  LIGHT CARD: Price and Chatter faces each have a white bordered root, 0 band tokens, 0 light-ink tokens outside the navy
 *      GraphicPanel, 0 white fills inside it; the Chatter face mounts ChatterBubbles with no month cursor (AMENDMENT 1).
 *   2  READER WORDS: the page description is reader words; the Price face's Details disclosure states the date and source in words
 *      with no generation id or system token, on the served payload and on a planted SHORT_READ payload.
 *   3  PLANTED: the predicates accept a reference light card, a reader subtitle and a reader Details line, and reject the base shape
 *      (band root holding a white strip), a white panel with band ink, a white strip inside the navy panel, a band footer inside a
 *      white panel, the base subtitle, the base Details line and a Details line carrying "state COMPLETE".
 * Blind spots: class tokens are read, not computed colours (an inline style colour or a new light token is not seen); the navy
 *   GraphicPanel's own fill is not measured; layout, spacing and the card's look are the person's PNG read.
 * Prints one line per arm and "THE LEAD PANEL IS ONE LIGHT CARD AND SPEAKS READER WORDS: <k> of 3 arms"; exit 0 only at 3 of 3.
 * Writes no file. No network, no AWS.
 */
const R = require('./_render.cjs');

const T0 = Date.now();
const L = R.L;
const ce = R.origCreateElement;
const LIVE = R.loadFixture('live');
// ISSUER AMENDMENT 1 (round 31, FWD-26): the Chatter face reads the served 30-day window, not the round-16 monthly payload.
const CHAT = (() => { const d = JSON.parse(require('fs').readFileSync(require('path').join(__dirname, '..', '..', '..', 'round31', 'fixtures', 'windows.chatter.30.json'), 'utf8')); return d.payload; })();
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

const unesc = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const textOf = (html) => unesc(String(html).replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();
const CODE = /\b[a-z]+_[a-z0-9_]+\b|_Equity\b|\.json\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;

/** [start, end) of every element whose opening tag matches `attrRe`, depth-matched on its own tag name. */
function rangesOf(html, attrRe) {
  const out = [];
  const re = /<([a-zA-Z0-9]+)\b[^>]*>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (!attrRe.test(m[0]) || m[0].endsWith('/>')) continue;
    const tag = m[1];
    let depth = 1;
    const r2 = new RegExp(`<(/?)${tag}\\b[^>]*?(/?)>`, 'g');
    r2.lastIndex = m.index + m[0].length;
    let n;
    let end = html.length;
    while ((n = r2.exec(html)) !== null) {
      if (n[2] === '/') continue;
      depth += n[1] === '/' ? -1 : 1;
      if (depth === 0) { end = n.index; break; }
    }
    out.push([m.index, end]);
  }
  return out;
}

// ---------------- light-card predicates ----------------
const WHITE_FILL = /^(bg-white|bg-\[hsl\(var\(--bg-surface\)\)\]|bg-\[#(?:fff|ffffff)\])$/i;
const BAND_TOKEN = /^(dark-band|bg-\[hsl\(var\(--(?:bg-band|bg-header|bg-medium|bg-card|semantic-background-contentPanel)\)\)\]|bg-\[#0A1733\])$/i;
const LIGHT_INK = /^(text-white(\/\d+)?|text-\[hsl\(var\(--palette-(?:white|mediumGray)\)\)\]|text-\[#(?:E8ECF5|A8B0C0|fff|ffffff)\]|text-[a-z]+-(?:50|100|200|300)(\/\d+)?|bg-white\/\d+)$/i;
const bare = (tok) => tok.replace(/^(?:[a-z-]+:)+/, '');

function lightFaults(html) {
  const f = [];
  const tags = [...html.matchAll(/<([a-zA-Z0-9]+)\b[^>]*>/g)].filter((m) => !m[0].startsWith('</'));
  const navy = rangesOf(html, /data-stub="GraphicPanel"/);
  const inNavy = (i) => navy.some(([a, b]) => i > a && i < b);
  const classes = (m) => { const c = /\sclass="([^"]*)"/.exec(m[0]); return c ? unesc(c[1]).split(/\s+/).filter(Boolean) : []; };
  if (!tags.length) return ['RENDER: empty markup'];
  const root = classes(tags[0]);
  if (!root.some((t) => WHITE_FILL.test(t)) || !root.includes('border')) {
    f.push(`SURFACE: the root element is not a white bordered panel (class "${root.join(' ').slice(0, 120)}")`);
  }
  let band = 0; let ink = 0; let lod = 0;
  const bandSeen = []; const inkSeen = []; const lodSeen = [];
  for (const m of tags) {
    const toks = classes(m).map(bare);
    if (/\sclass="[^"]*\bdark-band\b/.test(m[0]) || toks.some((t) => BAND_TOKEN.test(t))) {
      band += 1; if (bandSeen.length < 2) bandSeen.push(toks.filter((t) => BAND_TOKEN.test(t)).join(' '));
    }
    if (inNavy(m.index)) {
      if (toks.some((t) => WHITE_FILL.test(t))) { lod += 1; if (lodSeen.length < 2) lodSeen.push(toks.filter((t) => WHITE_FILL.test(t)).join(' ')); }
    } else {
      const hits = classes(m).filter((t) => LIGHT_INK.test(bare(t)));
      if (hits.length) { ink += 1; if (inkSeen.length < 2) inkSeen.push(hits.join(' ')); }
    }
  }
  if (band) f.push(`BAND: ${band} element(s) carry a band class (${bandSeen.join(' ; ')})`);
  if (ink) f.push(`INK: ${ink} element(s) outside the navy panel carry light ink (${inkSeen.join(' ; ')})`);
  if (lod) f.push(`LIGHT-ON-DARK: ${lod} white fill(s) inside the navy panel (${lodSeen.join(' ; ')})`);
  return f;
}

// ---------------- reader-word predicates ----------------
const SUBTITLE_SYSTEM = /\buniverse\b|\bdiscovery\b|server[- ]?side|\bper[- ]name\b/i;
function subtitleFaults(text) {
  const f = [];
  if (text === null) return ['SUBTITLE: the page header carries no description'];
  if (text.split(/\s+/).filter((w) => /[A-Za-z]/.test(w)).length < 3) f.push(`SUBTITLE: fewer than three words ("${text}")`);
  const m = SUBTITLE_SYSTEM.exec(text);
  if (m) f.push(`SUBTITLE: system wording "${m[0]}"`);
  if (/\S\s\/\s\S/.test(text)) f.push('SUBTITLE: a " / " list');
  const c = CODE.exec(text);
  if (c) f.push(`SUBTITLE: code-shaped token "${c[0]}"`);
  return f;
}
function dateSrc(iso) {
  const [y, mo, d] = iso.split('-').map(Number);
  const M = MONTHS[mo - 1];
  const S = M.slice(0, 3);
  return `(?:(?:${M}|${S}\\.?)\\s+${d}(?:st|nd|rd|th)?,?\\s+${y}|${d}(?:st|nd|rd|th)?\\s+(?:${M}|${S}\\.?),?\\s+${y})`;
}
const MACHINE_CI = /row\(s\)|\bvintage\b|\bgeneration\b|\bpointer\b|bloomberg-dapi|boxside|blp_client|127\.0\.0\.1/i;
const MACHINE_CS = /\bstate\s+[A-Z_]{3,}\b|\b(?:COMPLETE|SERVED|SHORT_READ|OVER_READ|NOT_SERVABLE|POINTER_UNREAD|ABSENT|EMPTY)\b|\b[A-Z][A-Z0-9]*_[A-Z0-9_]+\b/;
function detailWordFaults(text, payload, served) {
  const f = [];
  const id = /\b\d{8}T\d{6}Z-[0-9a-f]{6,}\b/i.exec(text) || (payload.generation_id && text.includes(payload.generation_id) ? [payload.generation_id] : null) || /\b[0-9a-f]{12,}\b/i.exec(text);
  if (id) f.push(`ID: generation id "${id[0]}"`);
  const a = MACHINE_CI.exec(text) || MACHINE_CS.exec(text);
  if (a) f.push(`TOKEN: system token "${a[0]}"`);
  if (served) {
    if (!new RegExp(dateSrc(payload.as_of_date), 'i').test(text)) f.push(`DATE: ${payload.as_of_date} is not named in words`);
    if (!/\bBloomberg\b/.test(text)) f.push('SOURCE: the source is not named ("Bloomberg")');
  }
  return f;
}
function detailFaults(html, payload, served) {
  const r = rangesOf(html, /data-source-caption="detail"/);
  if (r.length !== 1) return [`DETAIL: ${r.length} element(s) carry data-source-caption="detail", want 1`];
  const open = html.lastIndexOf('<', r[0][0] + 1);
  const inner = html.slice(html.indexOf('>', open) + 1, r[0][1]);
  const head = html.slice(open, html.indexOf('>', open) + 1);
  const titles = [...(head + inner).matchAll(/\stitle="([^"]*)"/g)].map((m) => unesc(m[1]));
  return detailWordFaults([textOf(inner), ...titles].join(' | '), payload, served);
}

// ---------------- the page header render (SecurityAnalysis.tsx) ----------------
function pageDescription() {
  const stub = (name) => () => ce('div', { 'data-stub': name });
  R.both('src/components/PageHeaderVariants', {
    PageHeaderCleanBadge: (p) => ce('header', { 'data-page-header': '' }, ce('h1', null, p.title),
      p.description !== undefined && p.description !== null && p.description !== false ? ce('p', { 'data-page-description': '' }, p.description) : null),
  });
  R.both('src/contexts/PageThemeContext', { PageThemeProvider: (p) => ce(R.React.Fragment, null, p.children), usePageTheme: () => ({}) });
  R.both('src/hooks/useTabNavigation', { useTabNavigation: () => ({ activeTab: 'thesis', handleTabChange: () => {}, tabContentRef: null }) });
  R.both(R.SA + 'components/LeadPanel', { LeadPanel: stub('LeadPanel') });
  R.both(R.SA + 'components/SecurityOverlay', { IdentityHeader: stub('IdentityHeader') });
  R.both(R.SA + 'components/PrintExportAction', { PrintExportAction: stub('PrintExportAction') });
  for (const t of ['ThesisTab', 'ExecManagementTab', 'PeersTab', 'ModelTab', 'PostureTab']) R.both(R.SA + 'tabs/' + t, { [t]: stub(t) });
  const { SecurityAnalysis } = L.source(R.SA + 'SecurityAnalysis.tsx');
  const html = R.renderState(() => L.render(SecurityAnalysis, {})).html;
  const m = /<p data-page-description="">([\s\S]*?)<\/p><\/header>/.exec(html) || /<p data-page-description="">([\s\S]*?)<\/p>/.exec(html);
  return m ? textOf(m[1]) : null;
}

const arms = [];
// ---------------- arm 1: one light card ----------------
{
  const f = [];
  const tally = [];
  try {
    const price = R.renderState(() => R.renderLead('PRICE', LIVE, undefined)).html;
    const fp = lightFaults(price);
    f.push(...fp.map((x) => `price: ${x}`));
    tally.push(`price ${fp.length} fault(s)`);
    R.bubbleSeen.month = null; R.bubbleSeen.onMonthChange = null;
    const chat = R.renderState(() => R.renderLead('CHATTER', LIVE, CHAT)).html;
    const fc = lightFaults(chat);
    f.push(...fc.map((x) => `chatter: ${x}`));
    if (!/data-stub="ChatterBubbles"/.test(chat)) f.push('chatter: CURSOR: ChatterBubbles is not mounted');
    else if (R.bubbleSeen.onMonthChange === 'function') f.push('chatter: CURSOR: ChatterBubbles still gets an onMonthChange function (FWD-26 retires the month cursor)');
    tally.push(`chatter ${fc.length} fault(s), month cursor ${R.bubbleSeen.onMonthChange === 'function' ? 'STILL HANDED' : 'retired'}`);
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['LIGHT CARD: a white bordered root, 0 band classes, 0 light ink outside the navy GraphicPanel, 0 white fills inside it; no month cursor (FWD-26)',
    f.length === 0, f.length === 0 ? tally.join('; ') : f.slice(0, 5).join(' | ')]);
}
// ---------------- arm 2: reader words ----------------
{
  const f = [];
  let desc = null;
  try {
    desc = pageDescription();
    f.push(...subtitleFaults(desc));
  } catch (e) { f.push('SUBTITLE: RENDER: ' + String(e.message).split('\n')[0]); }
  const shortRead = JSON.parse(JSON.stringify(LIVE));
  shortRead.ranking_status = 'SHORT_READ';
  shortRead.ranking_reason = 'the pointer names 94 rows and 90 were read';
  for (const [label, p, served] of [['served', LIVE, true], ['planted SHORT_READ', shortRead, false]]) {
    try {
      const html = R.renderState(() => R.renderLead('PRICE', p, undefined)).html;
      f.push(...detailFaults(html, p, served).map((x) => `details (${label}): ${x}`));
    } catch (e) { f.push(`details (${label}): RENDER: ${String(e.message).split('\n')[0]}`); }
  }
  arms.push(['READER WORDS: the page description is reader words; the Details disclosure states the date and source with no generation id or system token',
    f.length === 0, f.length === 0 ? `description "${desc}"; details 2 of 2 payloads clean` : f.slice(0, 5).join(' | ')]);
}
// ---------------- arm 3: planted controls ----------------
{
  const f = [];
  const caught = [];
  const GOOD = '<div class="w-full rounded-[4px] border border-[hsl(var(--hairline))] bg-[hsl(var(--bg-surface))]"><div class="group flex flex-col overflow-hidden rounded-[4px] border border-black bg-white"><div data-stub="GraphicPanel"><h2 class="text-xl text-white">What is moving</h2></div><div class="flex gap-2"><div role="group" aria-label="Subject"><button>Price</button></div></div></div><ol><li data-price-bar="AMD_US_Equity" class="text-[hsl(var(--palette-navy))]">Advanced Micro Devices Inc</li></ol></div>';
  const g = lightFaults(GOOD);
  if (g.length) f.push(`the reference light card fails: ${g[0]}`);
  const LMUT = [
    ['base shape', GOOD.replace('border border-[hsl(var(--hairline))] bg-[hsl(var(--bg-surface))]', 'dark-band border border-[hsl(var(--bg-band))] bg-[hsl(var(--bg-band))]'), 'BAND'],
    ['band ink on white', GOOD.replace('text-[hsl(var(--palette-navy))]', 'text-[hsl(var(--palette-white))]'), 'INK'],
    ['white strip in the navy panel', GOOD.replace('<h2 class="text-xl text-white">', '<div class="bg-white px-2">strip</div><h2 class="text-xl text-white">'), 'LIGHT-ON-DARK'],
    ['band footer in a white panel', GOOD.replace('</ol></div>', '</ol><div class="px-4 bg-[hsl(var(--bg-header))]"><span class="text-white/50">Source</span></div></div>'), 'BAND'],
  ];
  for (const [n, html, cls] of LMUT) {
    const fx = lightFaults(html);
    if (fx.some((x) => x.startsWith(cls + ':'))) caught.push(`${n}->${cls}`); else f.push(`mutant "${n}" not rejected as ${cls} (${fx[0] || 'no fault'})`);
  }
  const BASE_SUB = 'Universe discovery, ranked server-side, above a per-name Thesis / Exec Management / Peers / Model / Posture.';
  const GOOD_SUB = 'What is moving in price and in the news, and the research behind each name we cover.';
  if (subtitleFaults(GOOD_SUB).length) f.push(`the reader subtitle fails: ${subtitleFaults(GOOD_SUB)[0]}`);
  if (subtitleFaults(BASE_SUB).length) caught.push('base subtitle->SUBTITLE'); else f.push('the base subtitle is accepted');
  const BASE_DET = 'Details generation 20261002T111010Z-a89fcf3c5f42 | state COMPLETE | 94 row(s) committed | coverage vintage bloomberg-dapi-boxside-pull:2026-10-02T11:10Z';
  const GOOD_DET = 'Details Prices from Bloomberg, as of October 1st, 2026; 94 names ranked by their change in price.';
  const dg = detailWordFaults(GOOD_DET, LIVE, true);
  if (dg.length) f.push(`the reader Details line fails: ${dg[0]}`);
  const db = detailWordFaults(BASE_DET, LIVE, true);
  if (db.some((x) => x.startsWith('ID:')) && db.some((x) => x.startsWith('TOKEN:'))) caught.push('base details->ID+TOKEN'); else f.push(`the base Details line is not rejected on ID and TOKEN (${db.join(' | ')})`);
  if (detailWordFaults(GOOD_DET + ' (state COMPLETE)', LIVE, true).some((x) => x.startsWith('TOKEN:'))) caught.push('state COMPLETE->TOKEN'); else f.push('"state COMPLETE" is accepted');
  arms.push(['PLANTED: a reference light card, reader subtitle and reader Details pass; the base shape, band ink, a strip in the navy panel, a band footer, the base subtitle and Details, and "state COMPLETE" are rejected',
    f.length === 0, f.length === 0 ? `3 references 0 faults; ${caught.length} of 7 mutants rejected (${caught.join(', ')})` : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`WALL: ${((Date.now() - T0) / 1000).toFixed(1)}s`);
console.log(`THE LEAD PANEL IS ONE LIGHT CARD AND SPEAKS READER WORDS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
