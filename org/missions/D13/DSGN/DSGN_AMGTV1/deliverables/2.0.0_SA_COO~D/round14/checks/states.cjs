/**
 * states.cjs -- DSGN_AMGTV1 round 14, AV-k-2: ERROR SAYS WHAT FAILED, NO-PERMISSION NAMES THIS PAGE (round-13 analysis rulings 2
 * and 3; FWD-19, FWD-11; analysis section 4 row 2).
 *
 * Usage (repo root): node <this file>
 * Ruling 2: "ERROR states what failed and what to do, in navy text (C12.3). The response body never reaches the face; it rides a
 * `data-*` attribute for the instrument." Ruling 3: "NO-PERMISSION on this page names this page's object and who grants it (C12.4)
 * ... The shared component takes a page-specific sentence, with a capitalised second sentence. The shared default is untouched."
 * Today (DEV 118cd005) every Security Analysis ERROR prints `Cause: API request failed: 503 ... - {"error":...}` on the face, and the
 * only NO-PERMISSION render is the shared default "... this firm's advisor book. your firm administrator can grant it."
 *
 * The page's NO-PERMISSION contract read here: `portal/src/pages/SecurityAnalysis/components/ResearchNoPermission.tsx` exports
 * `ResearchNoPermission` (frame props only), rendering the shared `PanelNoPermission` with this page's sentences. It has no live
 * route (PanelStates.tsx docstring, row DSGN_REBRND-W3-S1); the render instrument's `--states-sweep` captures it standalone.
 *
 * Every render uses the REAL `src/ui/components/states/PanelStates.tsx` (not _load's stub), injected where the page imports
 * `@/ui/components/states`; the page's hooks return a forced 503 whose body is a JSON object.
 * Arms:
 *   1  ERROR on the face: on 7 surfaces (lead list, identity header, Thesis, Exec, Peers, Model, Posture) each forced to its read
 *      failure, an error panel renders; its visible text has 0 `{`, `}`, `"`; the body's words never reach any visible text; the
 *      body rides whole in some data-* attribute (Model prints no cause, so it is exempt from that limb only); the panel says what
 *      failed and what to do. NEGATIVE: the shared PanelError given the same body as its `cause` (its default placement) is caught.
 *   2  NO-PERMISSION names this page: `ResearchNoPermission` renders a no-permission panel whose text names this security's
 *      research, not "advisor book", has >= 2 sentences each starting with a capital, and one says who can grant it. NEGATIVE: the
 *      shared default render ("advisor book", lower-case second sentence) fails the same predicate.
 *   3  the shared defaults are byte-equal to DEV 118cd005: PanelNoPermission with the render instrument's props
 *      (portal/scripts/ui-contract-check.mjs) and PanelError with a cause and no option (Valuation.tsx's shape). NEGATIVE: a
 *      one-letter change to the no-permission props is detected. A CONTROL: it passes at the base by construction.
 * Prints one line per arm and "ERROR SAYS WHAT FAILED, NO-PERMISSION NAMES THIS PAGE: <k> of 3 arms"; exit 0 only at 3 of 3.
 * No network, no AWS, writes no file.
 */
const L = require('./_load.cjs');
const React = L.React;

const SA = 'src/pages/SecurityAnalysis/';
const BODY = '{"error":"forced failure","detail":"upstream unavailable"}';
const MSG = 'API request failed: 503 Service Unavailable - ' + BODY;
const ERR = Object.assign(new Error(MSG), { status: 503 });
const unesc = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const safe = (f) => { try { return f(); } catch (e) { return `<p data-render-failed="1">RENDER FAILED ${String(e.message).split('\n')[0].replace(/</g, '&lt;')}</p>`; } };

// ---- the REAL states module, where the page imports it ---------------------------------------------------------------------
const STATES = L.source('src/ui/components/states/PanelStates.tsx');
const CAUSE = L.source('src/ui/components/states/cause.ts');
L.stubSource('src/ui/components/states/index.ts', { __esModule: true, ...STATES, innermostCause: CAUSE.innermostCause });
// every page hook reads the forced failure
const failed = () => ({ data: undefined, isLoading: false, isError: true, error: ERR, refetch: () => {}, mutate: () => {}, isPending: false });
L.stubSource(SA + 'hooks/useLeadPanelApi.ts', new Proxy({}, { get(_t, k) { if (k === '__esModule') return true; if (typeof k !== 'string') return undefined; return failed; } }));
L.stubSource('@tanstack/react-query', {
  __esModule: true,
  useQuery: () => failed(),
  useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }),
});
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);

/** Every error panel's inner HTML (all of them, in order). */
function errorPanels(html) {
  const out = [];
  let rest = html;
  for (;;) {
    const at = rest.indexOf('data-panel-state="error"');
    if (at < 0) break;
    const inner = L.innerOf(rest.slice(rest.lastIndexOf('<', at)), 'data-panel-state', 'error');
    out.push(inner || '');
    rest = rest.slice(at + 10);
  }
  return out;
}
function dataAttrs(html) {
  const out = [];
  const re = /\sdata-[\w-]+="([^"]*)"/g;
  let m;
  while ((m = re.exec(html)) !== null) out.push(unesc(m[1]));
  return out;
}
const WHAT_FAILED = /could not|did not|failed|failure|not be (read|loaded)/i;
const WHAT_TO_DO = /try again|reload|retry|if it keeps failing|contact|administrator/i;
/** One surface's failing limbs ([] = clean). */
function gradeError(surface, html, { causeExempt } = {}) {
  const f = [];
  if (/data-render-failed/.test(html)) return [`${surface}: render failed -- ${L.textOf(html).slice(0, 120)}`];
  const panels = errorPanels(html);
  if (panels.length === 0) return [`${surface}: no error panel rendered (subject not rendered)`];
  const text = panels.map((p) => L.textOf(p)).join(' | ');
  const bad = (text.match(/[{}"]/g) || []).length;
  if (bad) f.push(`${surface}: ${bad} brace/quote char(s) on the error face: "${text.slice(0, 160)}"`);
  if (/forced failure|upstream unavailable|Service Unavailable/i.test(L.textOf(html))) f.push(`${surface}: the response body's words reach the visible face`);
  if (!causeExempt && !dataAttrs(html).some((v) => v.includes(BODY))) f.push(`${surface}: the body does not ride whole in any data-* attribute`);
  const retry = /data-state-retry/.test(panels.join(''));
  if (!WHAT_FAILED.test(text)) f.push(`${surface}: no what-failed sentence ("${text.slice(0, 100)}")`);
  if (!WHAT_TO_DO.test(text) && !retry) f.push(`${surface}: no what-to-do sentence and no retry ("${text.slice(0, 100)}")`);
  return f;
}

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const K = 'BA_US_Equity';
const surfaces = [
  ['lead list', () => L.render(L.source(SA + 'components/RankedList.tsx').RankedList, {
    rows: [], starredTickers: new Set(), resolution: null, onToggleStar: () => {}, onSelectSecurity: () => {},
    isLoading: false, readError: ERR, rankingStatus: null, rankingReason: null, emptyReason: null,
  })],
  ['identity header', () => { const m = L.source(SA + 'components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: undefined, isLoading: false, loadError: MSG, onBack: () => {}, onRefresh: () => {} }); }],
  ['thesis', () => L.render(L.source(SA + 'tabs/ThesisTab.tsx').ThesisTab, { securityKey: K })],
  ['exec', () => L.render(L.source(SA + 'tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: K })],
  ['peers', () => L.render(L.source(SA + 'tabs/PeersTab.tsx').PeersTab, { securityKey: K })],
  ['model', () => L.render(L.source(SA + 'tabs/ModelTab.tsx').ModelTab, { securityKey: K }), { causeExempt: true }],
  ['posture', () => L.render(L.source(SA + 'tabs/PostureTab.tsx').PostureTab, { securityKey: K })],
];
const f1 = [];
let seen = 0;
for (const [name, fn, opts] of surfaces) {
  const html = safe(fn);
  const g = gradeError(name, html, opts);
  if (errorPanels(html).length) seen += 1;
  f1.push(...g);
}
// NEGATIVE: the shared default placement, given the same body, must be caught.
const planted = safe(() => L.render(STATES.PanelError, { message: 'Thesis could not be loaded.', hint: 'Try again.', cause: MSG }));
const plantedCaught = gradeError('planted', planted).some((x) => /brace\/quote/.test(x));
if (!plantedCaught) f1.push('NEGATIVE NOT CAUGHT: the shared PanelError with the body as its cause reads clean');
const a1 = f1.length === 0;
const a1d = a1
  ? `${seen} of ${surfaces.length} surfaces render an error panel; 0 brace/quote chars on any error face; body whole in a data-* attribute on ${surfaces.length - 1} of ${surfaces.length - 1} cause-bearing surfaces; what-failed + what-to-do on all; planted default-placement caught`
  : `${f1.length} failing (${seen} of ${surfaces.length} surfaces rendered an error panel); first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
function gradeNoPermission(label, html) {
  const f = [];
  if (/data-render-failed/.test(html)) return [`${label}: render failed -- ${L.textOf(html).slice(0, 140)}`];
  const inner = L.innerOf(html, 'data-panel-state', 'no-permission');
  if (inner === null) return [`${label}: no no-permission panel rendered (subject not rendered)`];
  const text = L.textOf(inner);
  if (/advisor book/i.test(text)) f.push(`${label}: names "advisor book"`);
  if (!/\b(security|name)\b[^.]*\bresearch\b/i.test(text)) f.push(`${label}: does not name this security's research ("${text}")`);
  const sentences = text.split(/(?<=[.!?])\s+/).filter(Boolean);
  if (sentences.length < 2) f.push(`${label}: ${sentences.length} sentence(s), want >= 2 ("${text}")`);
  const lower = sentences.filter((s) => !/^[A-Z]/.test(s));
  if (lower.length) f.push(`${label}: ${lower.length} sentence(s) not starting with a capital: "${lower[0]}"`);
  if (!sentences.some((s) => /\bcan grant\b|\bgrants?\b/i.test(s))) f.push(`${label}: no sentence says who grants access`);
  return f;
}
const fs = require('fs');
const path = require('path');
const NP_FILE = SA + 'components/ResearchNoPermission.tsx';
let npHtml;
if (!fs.existsSync(path.join(L.base, NP_FILE))) npHtml = `<p data-render-failed="1">RENDER FAILED ${NP_FILE} does not exist</p>`;
else npHtml = safe(() => L.render(L.source(NP_FILE).ResearchNoPermission, { surface: 'panel' }));
const f2 = gradeNoPermission('ResearchNoPermission', npHtml);
const SCRIPT_PROPS = { subject: "this firm's advisor book", grantedBy: 'your firm administrator', surface: 'panel', className: 'w-[480px]' };
const defaultNp = safe(() => L.render(STATES.PanelNoPermission, SCRIPT_PROPS));
const negCaught = gradeNoPermission('default', defaultNp).length >= 2;
if (!negCaught) f2.push('NEGATIVE NOT CAUGHT: the shared default (advisor book, lower-case second sentence) passes the predicate');
const a2 = f2.length === 0;
const npText = L.innerOf(npHtml, 'data-panel-state', 'no-permission');
const a2d = a2
  ? `reads "${L.textOf(npText)}"; planted shared default fails the same predicate`
  : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
// Base bytes: DEV 118cd005 PanelStates.tsx rendered by this loader (lucide icons are _load's stubs on both sides).
const BASE_NP = '<div data-panel-state="no-permission" role="status" class="flex flex-col rounded-[4px] bg-[hsl(var(--bg-surface))] text-[hsl(var(--palette-navy))] border border-[hsl(var(--hairline))] items-center justify-center text-center gap-3 px-6 py-10 w-[480px]"><div data-stub="Lock"></div><p class="max-w-[56ch] text-sm"><span class="font-bold">You do not have access to this firm&#x27;s advisor book.</span> your firm administrator can grant it.</p></div>';
const BASE_ER = '<div data-panel-state="error" role="alert" class="flex w-full flex-col rounded-[4px] bg-[hsl(var(--bg-surface))] text-[hsl(var(--palette-navy))] items-center justify-center text-center gap-3 px-6 py-10"><div class="flex max-w-[60ch] items-start gap-2 text-left"><div data-stub="AlertCircle"></div><div class="flex flex-col gap-1"><p class="font-bold text-sm">Valuation metrics could not be loaded.</p><p class="text-xs">Reload the page to try again.</p><p data-state-ink="secondary" class="text-[hsl(var(--palette-darkGray))] text-xs">Cause: upstream timeout</p></div></div></div>';
const erNow = safe(() => L.render(STATES.PanelError, { message: 'Valuation metrics could not be loaded.', hint: 'Reload the page to try again.', cause: 'upstream timeout' }));
const f3 = [];
if (defaultNp !== BASE_NP) f3.push(`PanelNoPermission default differs from the base (${defaultNp.length} vs ${BASE_NP.length} bytes): ${defaultNp.slice(0, 200)}`);
if (erNow !== BASE_ER) f3.push(`PanelError default (cause, no option) differs from the base (${erNow.length} vs ${BASE_ER.length} bytes): ${erNow.slice(0, 200)}`);
const mutant = safe(() => L.render(STATES.PanelNoPermission, { ...SCRIPT_PROPS, grantedBy: 'Your firm administrator' }));
if (mutant === BASE_NP) f3.push('NEGATIVE NOT CAUGHT: a one-letter change to the props renders byte-equal');
const a3 = f3.length === 0;
const a3d = a3
  ? `PanelNoPermission default ${defaultNp.length} bytes == base; PanelError default ${erNow.length} bytes == base; one-letter mutant differs`
  : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['ERROR says what failed and what to do; the body rides a data attribute', a1, a1d],
  ["NO-PERMISSION names this page's object and who grants it, capitalised", a2, a2d],
  ['the shared defaults stay byte-equal to the base', a3, a3d],
];
if (process.env.STATES_VERBOSE) for (const x of [...f1, ...f2, ...f3]) console.log('  - ' + x.slice(0, 220));
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`ERROR SAYS WHAT FAILED, NO-PERMISSION NAMES THIS PAGE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
