/* AMGT_RESAPP round-93 PREP -- rr-1 (FWD-38's last gap): the peers table says WHY the dates differ, in reader words, on the page.
 *
 *   cd <the PORTAL worktree> && node ../org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round93_prep/checks/r93_caveat_rendered.cjs
 *
 * INSTRUMENT: the ACTUAL PeersTab.tsx of the working directory's portal (transpiled with its own TypeScript, rendered by react-dom/server; the
 * loader is peersPattern.harness.cjs's own, cut at its fixture marker), fed the LIVE served peers and header payloads of ASML, BA and ROG
 * (`../fixtures/peers_and_header_figures_ASML_BA_ROG_20261011.json`, captured from the deployed function 2026-10-11). No browser, no network.
 * The served `subject.cross_vintage_caveat` is an engineering sentence; the page prints ONE plain sentence built from the two served dates
 * (the subject's `market_cap_vintage` and the set's `universe_vintage`) and shown only when that caveat is served.
 *
 *   C1 each of the three pages carries exactly one element `data-peers-cross-vintage-caveat`, after the table, whose text names the subject's
 *      cap date and the peers' date (each as "as of <long date>") and says neither is restated.
 *   C2 control: the same pages with `subject.cross_vintage_caveat` removed carry no such element.
 *   C3 reader words: the element's text holds none of: vintage, scalars, model block, asOf, ACROSS, re-dated, mktVal.
 *   C4 control: the rest of the markup is the page's own: removing the element from the C1 markup leaves the C2 markup byte-equal.
 * Verdict: R93 CAVEAT RENDERED: YES|NO (exit 0|1). At the base (portal DEV c96efe17) C1, C3 and C4 FAIL (no element), C2 PASSes.
 */
const fs = require('node:fs');
const path = require('node:path');

const PORTAL = process.cwd().replace(/\\/g, '/');
const HARNESS = PORTAL + '/src/pages/SecurityAnalysis/__harness__/peersPattern.harness.cjs';
const FIXTURE = path.join(__dirname, '..', 'fixtures', 'peers_and_header_figures_ASML_BA_ROG_20261011.json');
if (!fs.existsSync(HARNESS)) {
  console.log('FAIL no peersPattern harness under the working directory: run this from the portal worktree root');
  process.exit(2);
}
let text = fs.readFileSync(HARNESS, 'utf8');
const marker = text.indexOf('// -- FIXTURE.');
if (marker < 0) throw new Error('fixture marker not found in the harness');
text = text.slice(0, marker)
  .replace("path.resolve(__dirname, '../../../..')", "'" + PORTAL + "'")
  .replace("PanelHeader: box,", "PanelHeader: box, PanelFooter: box,");
const tail = `
const pages = JSON.parse(fs.readFileSync(${JSON.stringify(FIXTURE)}, 'utf8'));
const FORBIDDEN = /vintage|scalars|model block|asof|across|re-dated|mktval/i;
const ELEMENT = /<[a-z]+[^>]*data-peers-cross-vintage-caveat[^>]*>([\\s\\S]*?)<\\/[a-z]+>/g;
const strip = (h) => h.replace(/<[^>]+>/g, ' ').replace(/\\s+/g, ' ').trim();
const render = (key, mutate) => {
  const doc = JSON.parse(JSON.stringify(pages[key]));
  if (mutate) mutate(doc);
  peer = doc.peers;
  hooks.useSecurityOverlay = () => ({ data: doc.overlay, isLoading: false });
  return renderToStaticMarkup(React.createElement(PeersTab, { securityKey: key }));
};
const results = [];
const say = (ok, label, detail) => { console.log((ok ? 'PASS ' : 'FAIL ') + label + (detail ? '  [' + detail + ']' : '')); results.push(ok); };
const DATE_RE = /as of ([A-Z][a-z]+ \\d{1,2}(?:st|nd|rd|th), \\d{4})/g;
let c1 = true, c2 = true, c3 = true, c4 = true;
const notes = [];
for (const key of Object.keys(pages)) {
  const withCaveat = render(key);
  const without = render(key, (d) => { delete d.peers.subject.cross_vintage_caveat; });
  const found = [...withCaveat.matchAll(ELEMENT)];
  const afterTable = found.length === 1 && withCaveat.indexOf('data-peers-cross-vintage-caveat') > withCaveat.indexOf('</table>');
  const sentence = found.length ? strip(found[0][1]) : '';
  const dates = [...sentence.matchAll(DATE_RE)].map((m) => m[1]);
  const ok1 = found.length === 1 && afterTable && dates.length >= 2 && new Set(dates).size >= 2 && /neither is restated/i.test(sentence);
  const ok2 = [...without.matchAll(ELEMENT)].length === 0;
  const ok3 = found.length === 1 && !FORBIDDEN.test(sentence);
  let ok4 = false;
  if (found.length === 1) {
    ok4 = withCaveat.replace(found[0][0], '') === without;
  }
  c1 = c1 && ok1; c2 = c2 && ok2; c3 = c3 && ok3; c4 = c4 && ok4;
  notes.push(key + ': elements ' + found.length + ', dates ' + JSON.stringify(dates) + ', sentence "' + sentence.slice(0, 200) + '"');
}
notes.forEach((n) => console.log('   ' + n));
say(c1, 'C1 one plain sentence after the table names both dates and says neither is restated (3 of 3 pages)');
say(c2, 'C2 control: without the served caveat the element is absent (3 of 3 pages)');
say(c3, 'C3 reader words: no engineering term in the sentence');
say(c4, 'C4 control: the rest of the page is byte-equal with and without the sentence');
console.log('   arms passed ' + results.filter(Boolean).length + ' of ' + results.length);
const verdict = results.every(Boolean);
console.log('R93 CAVEAT RENDERED: ' + (verdict ? 'YES' : 'NO'));
process.exit(verdict ? 0 : 1);
`;
const out = path.join(require('node:os').tmpdir(), 'r93_caveat_rendered_gen_' + process.pid + '.cjs');
fs.writeFileSync(out, text + tail);
process.on('exit', () => { try { fs.unlinkSync(out); } catch (e) { /* the temp file stays */ } });
require(out);
