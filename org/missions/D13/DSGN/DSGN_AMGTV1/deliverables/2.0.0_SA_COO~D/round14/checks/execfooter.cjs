/**
 * execfooter.cjs -- DSGN_AMGTV1 round 14, AV-k-4: EXEC READS ITS SERVED REASON, POSTURE'S FOOTER IS SETTLED
 * (round-13 analysis rulings 5 and 7; FWD-11, FWD-19; section 4 row 4).
 *
 * Usage (repo root): node <this file>
 * Ruling 5: Exec's empty-state sentence comes from the SERVED reason, never a static filer assumption ("the company's 10-K had
 * no officer section ..." was printed for every name; 6501 JP is a Japanese filer with no 10-K). Where no reason is served,
 * the fallback claims NO document type.
 * Ruling 7: Posture's settled footer never says "still loading"; at rest it states the comparable bundles' outcome (resolved /
 * not served / failed), and "loading" appears only while a first read is genuinely in flight.
 * Fixtures (round14/fixtures, SERVED): /thesis for 6501 JP (management ABSENT, reason served), INTU US (management ABSENT with a
 * served 10-K section 'Item 10 ...' and accession), BA US (posture SERVED, comparable DE_US_Equity, no DE capture). ISSUER
 * VARIANTS (labelled, in memory): the comparable's two reads as react-query states -- settled with nothing served, settled
 * failed, failed-and-retrying (isFetching with failureCount > 0: the close render's posture.png case), settled with a bundle
 * (WMB's served /thesis relabelled as DE's), and genuinely in flight (isFetching, failureCount 0, no data); a 6501 bundle
 * with no reason served.
 * The page's hooks module is replaced by a query-state stub (fixtures by key; the comparable key by the variant).
 * Arms:
 *   1  6501's Exec on its served bundle: its empty state carries the served reason's words (management, object, landed, name),
 *      and its visible text names no "10-K"; the CONTROL: INTU's Exec (a served 10-K section) still names "10-K" and carries
 *      its own served reason's words
 *   2  BA's Posture at rest, four settled comparable reads: the footer carries no "loading" (nor does any visible text of the
 *      tab), states the outcome in words ("comparable"), and its data-posture-comparable-read is resolved / not-served /
 *      failed as the read is
 *   3  NEGATIVES: (a) with the comparable read genuinely in flight the footer says "loading" (the check does not ban the
 *      word); (b) a 6501 bundle with NO reason served reads a fallback that claims no document type (10-K, 10-Q, 20-F,
 *      annual report); (c) the static 10-K sentence planted into 6501's rendered Exec face is caught by arm 1's predicate
 * Prints one line per arm and "EXEC READS ITS SERVED REASON, POSTURE'S FOOTER IS SETTLED: <k> of 3 arms"; exit 0 only at 3.
 * No network, no AWS, writes no file.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const text = (html) => unesc(L.textOf(html || ''));
const SA = 'src/pages/SecurityAnalysis/';
const K6501 = '6501_JP_Equity';
const KINTU = 'INTU_US_Equity';
const KBA = 'BA_US_Equity';
const DOC_TYPE = /10-K|10-Q|20-F|annual report/i;
const STATIC_10K = "No officer list is in this name's pack yet: the company's 10-K had no officer section this page could read, and no other source was used.";

// ---- the query-state hooks stub ---------------------------------------------------------------------------------------------
const bundles = Object.assign({}, S.bundles);
bundles[KBA] = S.unwrap(L.fixture(`thesisBundle.${KBA}.json`));
const COMP = (bundles[KBA].posture || {}).comparable || null;
const cmp = { thesis: null, peers: null }; // the comparable key's two query states (null = settled, nothing served)
const settled = (data) => ({ data, isLoading: false, isPending: false, isFetching: false, isError: false, isSuccess: true, error: null, failureCount: 0, status: 'success', refetch: () => {} });
function q(kind, key) {
  if (key && key === COMP && cmp[kind]) return Object.assign(settled(undefined), cmp[kind]);
  if (kind === 'thesis') return settled(key ? bundles[key] : undefined);
  if (kind === 'peers') return settled(undefined);
  return settled(key && bundles[key] ? bundles[key].management : undefined);
}
const hooks = new Proxy({}, {
  get(_t, k) {
    if (k === '__esModule') return true;
    if (k === 'useThesisBundle') return (key) => q('thesis', key);
    if (k === 'usePeerSet') return (key) => q('peers', key);
    if (k === 'useManagement') return (key) => q('management', key);
    if (typeof k !== 'string') return undefined;
    return () => settled(undefined);
  },
});
L.stubSource(SA + 'hooks/useLeadPanelApi.ts', hooks);

const safe = (f) => { try { return f(); } catch (e) { return `<p data-render-failed="1">RENDER FAILED ${String(e.message).split('\n')[0]}</p>`; } };
const execOf = (key) => safe(() => L.render(L.source(SA + 'tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: key }));
const postureOf = (key) => safe(() => L.render(L.source(SA + 'tabs/PostureTab.tsx').PostureTab, { securityKey: key }));
const failedRender = (html) => /data-render-failed/.test(html);

// The Exec empty state: the element carrying data-exec-status (not SERVED).
const emptyText = (html) => text(L.innerOf(html, 'data-exec-status') || '');
const STOP = new Set(['this', 'that', 'with', 'from', 'have', 'there', 'their', 'which', 'were', 'been', 'into', 'than', 'then', 'neither', 'each']);
const reasonWords = (reason) => Array.from(new Set(String(reason || '').toLowerCase().split(/[^a-z]+/).filter((w) => w.length >= 4 && !STOP.has(w))));
/** Arm 1's predicate: the Exec face carries the served reason's words and (unless allowed) no document type. */
function execVerdict(html, reason, allowDocType) {
  const fails = [];
  if (!html || failedRender(html)) return { fails: ['not rendered'], words: [] };
  const face = emptyText(html);
  if (!face) fails.push('no Exec empty state rendered');
  const words = reasonWords(reason);
  if (words.length === 0) fails.push('the served reason has no words');
  const missing = words.filter((w) => !face.toLowerCase().includes(w));
  if (missing.length) fails.push(`the served reason's words missing from the empty state: ${missing.join(', ')}`);
  if (!allowDocType && DOC_TYPE.test(text(html))) fails.push(`visible text names "${(DOC_TYPE.exec(text(html)) || [''])[0]}": "${((/[^.:]*(10-K|10-Q|20-F|annual report)[^.]*/i.exec(text(html))) || [''])[0].trim().slice(0, 110)}"`);
  return { fails, words };
}

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const m6501 = bundles[K6501].management;
const r6501 = m6501.reason || m6501.roster_reason;
const e6501 = execOf(K6501);
const v6501 = execVerdict(e6501, r6501, false);
for (const x of v6501.fails) f1.push(`6501: ${x}`);
const mINTU = bundles[KINTU].management;
const eINTU = execOf(KINTU);
const vINTU = execVerdict(eINTU, mINTU.reason || mINTU.roster_reason, true);
for (const x of vINTU.fails) f1.push(`INTU: ${x}`);
if (!/10-K/.test(text(eINTU))) f1.push("INTU (a served 10-K section) no longer names the 10-K (the control: the word was deleted everywhere)");
const a1 = f1.length === 0;
const a1d = a1
  ? `6501's empty state carries ${v6501.words.length} served-reason words (${v6501.words.join(', ')}), 0 "10-K"; INTU names the 10-K and carries ${vINTU.words.length} of its reason's words`
  : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const footerOf = (html) => {
  const at = html.indexOf('data-posture-cites-resolved="');
  if (at < 0) return null;
  const open = html.lastIndexOf('<', at);
  return { tag: html.slice(open, html.indexOf('>', at) + 1), text: text(L.innerOf(html, 'data-posture-cites-resolved') || '') };
};
const readAttr = (tag) => ((/data-posture-comparable-read="([^"]*)"/.exec(tag || '')) || [])[1] || null;
const wmb = clone(S.unwrap(L.fixture('thesisBundle.WMB_US_Equity.json')));
wmb.security_key = COMP;
const AT_REST = [
  ['not served', { thesis: {}, peers: {} }, 'not-served'],
  ['failed', { thesis: { isError: true, isSuccess: false, status: 'error', error: new Error('503'), failureCount: 3 }, peers: { isError: true, isSuccess: false, status: 'error', error: new Error('503'), failureCount: 3 } }, 'failed'],
  ['failed, retrying', { thesis: { isFetching: true, isPending: true, isSuccess: false, status: 'pending', failureCount: 1 }, peers: { isFetching: true, isPending: true, isSuccess: false, status: 'pending', failureCount: 1 } }, 'failed'],
  ['resolved', { thesis: { data: wmb }, peers: {} }, 'resolved'],
];
const f2 = [];
const seen2 = [];
if (!COMP) f2.push("BA's posture names no comparable in the fixture");
for (const [label, state, want] of AT_REST) {
  cmp.thesis = state.thesis; cmp.peers = state.peers;
  const html = postureOf(KBA);
  const ft = footerOf(html);
  if (failedRender(html) || !ft) { f2.push(`${label}: the footer was not rendered`); continue; }
  const got = readAttr(ft.tag);
  seen2.push(`${label}=${got}`);
  if (/loading/i.test(ft.text)) f2.push(`${label}: the settled footer reads "${ft.text.slice(-70)}"`);
  if (/loading/i.test(text(html))) f2.push(`${label}: the settled tab says "loading": "${((/[^.;]*loading[^.;]*/i.exec(text(html))) || [''])[0].trim().slice(0, 90)}"`);
  if (!/comparable/i.test(ft.text)) f2.push(`${label}: the footer states no comparable outcome: "${ft.text.slice(0, 110)}"`);
  if (got !== want) f2.push(`${label}: data-posture-comparable-read=${got}, want ${want}`);
}
cmp.thesis = null; cmp.peers = null;
const a2 = f2.length === 0;
const a2d = a2 ? `${AT_REST.length} settled comparable reads of ${COMP}: 0 "loading", each footer states its outcome (${seen2.join(', ')})` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
cmp.thesis = { isFetching: true, isPending: true, isSuccess: false, status: 'pending', failureCount: 0 };
cmp.peers = { isFetching: true, isPending: true, isSuccess: false, status: 'pending', failureCount: 0 };
const inflight = postureOf(KBA);
const fi = footerOf(inflight);
cmp.thesis = null; cmp.peers = null;
if (failedRender(inflight) || !fi) f3.push('in flight: the footer was not rendered');
else {
  if (!/loading/i.test(fi.text)) f3.push(`in flight: the footer does not say loading: "${fi.text.slice(-80)}"`);
  if (readAttr(fi.tag) !== 'loading') f3.push(`in flight: data-posture-comparable-read=${readAttr(fi.tag)}, want loading`);
}
const noReason = clone(bundles[K6501]);
noReason.management.reason = null; noReason.management.roster_reason = null;
const saved = bundles[K6501];
bundles[K6501] = noReason;
const eNo = execOf(K6501);
bundles[K6501] = saved;
if (failedRender(eNo) || !emptyText(eNo)) f3.push('no-reason 6501: no Exec empty state rendered');
else if (DOC_TYPE.test(text(eNo))) f3.push(`no-reason 6501: the fallback claims a document type: "${((/[^.:]*(10-K|10-Q|20-F|annual report)[^.]*/i.exec(text(eNo))) || [''])[0].trim().slice(0, 110)}"`);
const msgAt = e6501.indexOf('data-stub-text="message">');
let planted = null;
if (msgAt >= 0) {
  const s = msgAt + 'data-stub-text="message">'.length;
  planted = e6501.slice(0, s) + STATIC_10K.replace(/'/g, '&#x27;') + e6501.slice(e6501.indexOf('</span>', s));
}
if (!planted) f3.push('plant: no empty-state message element in 6501 Exec to plant into');
else if (execVerdict(planted, r6501, false).fails.length === 0) f3.push('plant: the static 10-K sentence planted into 6501 Exec was NOT caught');
const a3 = f3.length === 0;
const a3d = a3 ? 'in flight the footer says loading (read=loading); the no-reason fallback names no document type; the planted static 10-K sentence is caught' : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ["6501's Exec reads its served reason, no 10-K; INTU still names its 10-K", a1, a1d],
  ["BA's settled Posture footer states the comparable outcome, never loading", a2, a2d],
  ['negatives: in-flight loading allowed, no-reason fallback, planted 10-K caught', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`EXEC READS ITS SERVED REASON, POSTURE'S FOOTER IS SETTLED: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
