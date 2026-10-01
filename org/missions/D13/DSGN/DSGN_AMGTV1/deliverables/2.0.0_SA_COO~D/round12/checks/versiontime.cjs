/**
 * versiontime.cjs -- DSGN_AMGTV1 round 12, AV-m-2: EVERY LANDED VERSION IS LABELLED WITH ITS DATE AND ITS TIME, SO TWO VERSIONS OF
 * ONE DAY CAN BE TOLD APART (round-11 analysis ruling 2; AMGT_RESAPP FWD-6 page half).
 *
 * Usage (repo root): node <this file>
 * The ruling: "each version is labelled with its date AND time (UTC) from the served stamp. Where two stamps share a minute, the
 * seconds are added. No new route; the stamp is already served (C-PRESENTATION-ONLY)." Round 11's walk K read BA's picker
 * offering four identical "September 10th, 2026" entries over four served stamps.
 * Fixtures (round12/fixtures, SERVED, captured at the cut): BA US /thesis, /versions (15 stamps: four on 20260910, two each on
 * 20260919, 20260924, 20260925, 20260930; no two in one minute) and /compare oldest -> newest. ISSUER VARIANT (labelled, in
 * memory): the served versions with 20260910T224459Z added, sharing a minute with 20260910T224432Z.
 * The label form checked: the page's long date ("September 10th, 2026") followed by the stamp's clock in 24-hour UTC --
 * "22:44 UTC", or "22:44:32 UTC" where two served stamps share that minute.
 * Arms:
 *   1  the list: each of the 15 `[data-model-version]` items shows its stamp's long date AND its "HH:MM UTC"; the 15 labels are
 *      pairwise distinct (the four 20260910 labels included); no raw stamp in visible text
 *   2  the pickers and the sentence: each compare picker offers 15 pairwise-distinct options carrying the same labels; the What-
 *      moved sentence names the earlier and the later version with their times
 *   3  a shared minute adds the seconds: in the planted variant the two stamps of 22:44 read "22:44:32 UTC" and "22:44:59 UTC";
 *      the other 20260910 stamps keep "HH:MM UTC" with no seconds (the control)
 * Prints one line per arm and "VERSIONS CARRY THEIR TIME: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const S = require('./surfaces.cjs');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unesc = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'");
const DU = (() => { try { return L.source('src/lib/dateUtils.ts'); } catch (e) { return {}; } })();
const longDate = (d) => String(DU.formatPanelTimestamp(null, d) || '').replace(/,\s*\d{1,2}:\d{2}[ap]\s*ET$/i, '');
const stampDay = (s) => `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`;
const hhmm = (s) => `${s.slice(9, 11)}:${s.slice(11, 13)}`;
const hhmmss = (s) => `${hhmm(s)}:${s.slice(13, 15)}`;

const thesis = S.unwrap(L.fixture('thesisBundle.BA_US_Equity.json'));
const versions = S.unwrap(L.fixture('versions.BA_US_Equity.json'));
const compare = S.unwrap(L.fixture('compare.BA_US_Equity.oldest-latest.json'));
let V = versions;
L.hookState.impl = Object.assign({}, L.hookState.impl, {
  useThesisBundle: (k) => (k === 'BA_US_Equity' ? thesis : (S.bundles[k] || undefined)),
  useModelVersions: () => V,
  useModelCompare: () => compare,
  useInputLedger: () => undefined,
});
const MT = (() => { try { return L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx'); } catch (e) { return null; } })();
const render = () => { try { return MT ? L.render(MT.ModelTab, { securityKey: 'BA_US_Equity' }) : ''; } catch (e) { return 'RENDER FAILED ' + e.message; } };
const items = (html) => [...html.matchAll(/<li[^>]*data-model-version="([^"]+)"[^>]*>([\s\S]*?)<\/li>/g)].map((m) => ({ stamp: m[1], text: unesc(L.textOf(m[2])).trim() }));
const selects = (html) => [...html.matchAll(/<select[\s\S]*?<\/select>/g)].map((m) => [...m[0].matchAll(/<option[^>]*>([\s\S]*?)<\/option>/g)].map((o) => unesc(L.textOf(o[1])).trim()));
const distinct = (a) => new Set(a).size === a.length;

const stamps = versions.versions.map((v) => v.stamp);
const html = render();

// ---- arm 1 ------------------------------------------------------------------------------------------------------------------
const f1 = [];
const li = items(L.innerOf(html, 'data-model-versions') || '');
if (li.length !== stamps.length) f1.push(`${li.length} version items, want ${stamps.length}`);
for (const { stamp, text } of li) {
  if (!text.includes(longDate(stampDay(stamp)))) { f1.push(`${stamp}: its long date is not in "${text}"`); break; }
  if (!new RegExp(`\\b${hhmm(stamp)}(:\\d{2})?\\s*UTC\\b`).test(text)) { f1.push(`${stamp}: "${hhmm(stamp)} UTC" is not in "${text}"`); break; }
}
if (!distinct(li.map((x) => x.text))) f1.push(`the labels are not pairwise distinct: ${JSON.stringify(li.map((x) => x.text).slice(0, 5))}`);
const sept10 = li.filter((x) => x.stamp.startsWith('20260910')).map((x) => x.text);
if (sept10.length !== 4 || !distinct(sept10)) f1.push(`the 20260910 labels ${JSON.stringify(sept10)} are not 4 distinct`);
if (/\b\d{8}T\d{6}Z\b/.test(unesc(L.textOf(html)))) f1.push('a raw stamp in visible text');
const a1 = f1.length === 0;
const a1d = a1 ? `${li.length} versions, each with its long date and "HH:MM UTC"; all distinct (4 distinct on September 10th); no raw stamp` : `${f1.length} failing; first: ${f1[0]}`;

// ---- arm 2 ------------------------------------------------------------------------------------------------------------------
const f2 = [];
const sel = selects(L.innerOf(html, 'data-model-compare') || '');
if (sel.length < 2) f2.push(`${sel.length} pickers in the compare, want 2`);
for (const [i, opts] of sel.entries()) {
  if (opts.length !== stamps.length) f2.push(`picker ${i + 1}: ${opts.length} options, want ${stamps.length}`);
  else if (!distinct(opts)) f2.push(`picker ${i + 1}: repeated options ${JSON.stringify(opts.filter((o, j) => opts.indexOf(o) !== j))}`);
  else if (!opts.every((o) => /\b\d{2}:\d{2}(:\d{2})?\s*UTC\b/.test(o))) f2.push(`picker ${i + 1}: an option without its UTC time`);
}
const csec = unesc(L.textOf(L.innerOf(html, 'data-model-compare') || ''));
const cf = compare.compared.from_stamp;
const ct = compare.compared.to_stamp;
if (!new RegExp(`earlier version of ${longDate(stampDay(cf)).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')},?\\s*${hhmm(cf)}(:\\d{2})?\\s*UTC`, 'i').test(csec)) f2.push(`the sentence does not name the earlier version with its time (${longDate(stampDay(cf))}, ${hhmm(cf)} UTC)`);
if (!new RegExp(`${hhmm(ct)}(:\\d{2})?\\s*UTC`).test(csec)) f2.push(`the sentence does not name the later version's time ${hhmm(ct)} UTC`);
const a2 = f2.length === 0;
const a2d = a2 ? `both pickers offer ${stamps.length} distinct labelled options; the sentence names both versions with their UTC times` : `${f2.length} failing; first: ${f2[0]}`;

// ---- arm 3 ------------------------------------------------------------------------------------------------------------------
const f3 = [];
V = clone(versions);
const planted = '20260910T224459Z';
V.versions.splice(1, 0, { stamp: planted, object_key: `derived/model_block/BA_US_Equity/${planted}/model_block.json` });
const li3 = items(L.innerOf(render(), 'data-model-versions') || '');
const byStamp = Object.fromEntries(li3.map((x) => [x.stamp, x.text]));
for (const s of ['20260910T224432Z', planted]) {
  if (!byStamp[s]) f3.push(`${s} is not listed`);
  else if (!new RegExp(`\\b${hhmmss(s)}\\s*UTC\\b`).test(byStamp[s])) f3.push(`${s} shares a minute but reads "${byStamp[s]}" (want ${hhmmss(s)} UTC)`);
}
for (const s of ['20260910T225428Z', '20260910T231417Z', '20260910T232018Z']) {
  if (!byStamp[s]) f3.push(`${s} is not listed`);
  else if (!new RegExp(`\\b${hhmm(s)}\\s*UTC\\b`).test(byStamp[s])) f3.push(`${s} (no shared minute) reads "${byStamp[s]}" (want ${hhmm(s)} UTC, no seconds)`);
}
V = versions;
const a3 = f3.length === 0;
const a3d = a3 ? 'the two 22:44 stamps read 22:44:32 UTC and 22:44:59 UTC; the other September 10th stamps keep HH:MM UTC' : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['each version shows its date and its time, all distinct', a1, a1d],
  ['the pickers and the what-moved sentence carry the time', a2, a2d],
  ['a shared minute adds the seconds (and only then)', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`VERSIONS CARRY THEIR TIME: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
