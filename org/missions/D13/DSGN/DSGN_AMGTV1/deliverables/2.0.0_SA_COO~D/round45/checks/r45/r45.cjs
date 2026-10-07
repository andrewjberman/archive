/**
 * r45.cjs -- DSGN_AMGTV1 round 45 issuer CHECK (2.0.0_SA_COO~D): THE TOP OF THE PAGE SAYS WHAT THE COMPANY IS AND WHAT IS SAID TODAY;
 * EACH INPUT SHOWS WHERE IT CAME FROM, WHEN IT LAST RAN AND WHETHER IT WORKED; THE RE-RUN BUTTON IS GONE.
 *
 * Usage (from the directory whose portal/ is the checkout under test):
 *   cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round45/checks/r45/r45.cjs"
 *
 * Why: AMGT_RESAPP ledger/ROUND_ANALYSIS.round75.md @326aea63b3 rulings 2-3 (the DSGN round 45 line), ROUND_ANALYSIS.round76.md
 * @c8bbeeac10 (az-2 deployed: /overlay serves `top_band` and `input_provenance` on 95 of 95) and its ADDENDUM 1 item 4 @a7b2c3e0ba
 * (the /refresh control is removed, PRD v0.41).
 * Fixtures: ../../fixtures/overlay.{BA,MSFT}_US_Equity.deployed-OVpDhfwD.json (read-only invokes of the deployed /overlay route).
 *   top_band: {description_line, description_reason, day, items[{title, url, publisher, published_utc, mentions}], items_reason,
 *              items_without_link, social}
 *   input_provenance: [{input, source, last_run ("20261006T132334Z" | "NEVER"), outcome ("landed" | "never read" | "failed"), reason}]
 * On the capture day 0 of 95 covered names served a news item (the scan at the cut), so the item arm PLANTS two items in the served
 * shape on BA's real block and says so. Every other arm reads the served bytes unchanged.
 *
 * The contract a cell builds to (from the task order):
 *   components/TopBand.tsx exports `TopBand: FC<{ band?: <top_band> | null }>`; root `data-top-band`; the description (or its served
 *     reason) in `data-top-band-description`; one `data-top-band-item` per served item, an `<a href>` opening a new tab when the item
 *     has a url; the served `items_reason` in `data-top-band-items-reason` when there are no items; the served `social` sentence in
 *     `data-top-band-social`.
 *   components/InputProvenance.tsx exports `InputProvenance: FC<{ entries?: <input_provenance> | null }>`; root
 *     `data-input-provenance`; one `data-provenance-row` per entry.
 *   SecurityAnalysis.tsx mounts both from the overlay, above the tabs.
 *
 * Arms (each prints its evidence; exit 0 only on all of them):
 *   1 THE TOP BAND SAYS WHAT THE COMPANY IS (BA, MSFT): the served description line is shown (BA); where none is served its plain
 *     reason is shown (MSFT); the social sentence is shown; with no items the served reason is shown and no item is drawn; no block
 *     renders nothing.
 *   2 THE DAY'S ITEMS CAN BE FOLLOWED (PLANTED items on BA's block): each item is drawn in served order with its title and
 *     publisher; an item with a url is a link to exactly that url that opens a new tab; an item with no url is drawn and is not a
 *     link; the items reason is not shown beside items.
 *   3 EACH INPUT SHOWS ITS SOURCE, ITS LAST RUN AND ITS RESULT (BA, MSFT): one row per served entry with its source in words; a
 *     last run reads as a date in words, never the raw stamp; a never-read input shows its served reason and never the raw token
 *     NEVER; the internal word "landed" is not on the page.
 *   4 MOUNTED ABOVE THE TABS; THE RE-RUN BUTTON IS GONE: SecurityAnalysis.tsx mounts <TopBand> and <InputProvenance> from the overlay
 *     before <TabNavigation>; no `useRequestRefresh` in the page or its hooks; no `onRefresh` / `refreshPending` in
 *     components/SecurityOverlay.tsx.
 *   5 PLANTED: the graders refuse a missing description, an item with no link, the raw stamp, the word "landed" and a leftover re-run
 *     hook, and accept the intended forms.
 */
const fs = require('fs');
const path = require('path');
const L = require(path.join(__dirname, '..', '..', '..', 'round15', 'checks', '_load.cjs'));

const FX = path.join(__dirname, '..', '..', 'fixtures');
const pay = (f) => JSON.parse(fs.readFileSync(path.join(FX, f), 'utf8')).payload;
const BA = pay('overlay.BA_US_Equity.deployed-OVpDhfwD.json');
const MSFT = pay('overlay.MSFT_US_Equity.deployed-OVpDhfwD.json');
const portal = path.join(process.cwd(), 'portal');
const OV = Object.fromEntries((process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]));
const src = (rel) => { const f = OV[rel] || path.join(portal, rel); return fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : ''; };
const decode = (s) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(html.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
const part = (html, attr) => { const m = new RegExp('<([a-z0-9]+)[^>]*' + attr + '[^>]*>([\\s\\S]*?)</\\1>').exec(html); return m ? text(m[2]) : null; };
const RAW_STAMP = /\b\d{8}T\d{6}Z\b/;
const MONTH = /(January|February|March|April|May|June|July|August|September|October|November|December)/;

const PLANTED_ITEMS = [
  { title: 'PLANTED Boeing wins a planted order', url: 'https://example.com/planted-a?x=1&y=2', publisher: 'Planted Wire', published_utc: '2026-10-06T14:05:00Z', mentions: 7 },
  { title: 'PLANTED second headline, no link', url: '', publisher: 'Planted Daily', published_utc: '2026-10-06T12:30:00Z', mentions: 3 },
];

function gradeBand(html, band) {
  const f = [];
  if (!/data-top-band[\s>=]/.test(html)) return ['no data-top-band root'];
  const desc = part(html, 'data-top-band-description');
  const want = norm(band.description_line || '') || norm(band.description_reason || '');
  if (desc === null) f.push('no data-top-band-description');
  else if (!want) f.push('fixture serves neither a description nor a reason');
  else if (!desc.includes(want.slice(0, 80))) f.push(band.description_line ? 'the served description line is not shown' : 'the served description reason is not shown');
  const social = part(html, 'data-top-band-social');
  if (social === null || !social.includes(norm(band.social))) f.push('the served social sentence is not shown');
  const items = band.items || [];
  const drawn = html.split(/(?=<[a-z0-9]+[^>]*data-top-band-item[\s>=])/).slice(1);
  if (drawn.length !== items.length) f.push(`${drawn.length} items drawn (${items.length} served)`);
  if (items.length === 0) {
    const why = part(html, 'data-top-band-items-reason');
    if (why === null || !why.includes(norm(band.items_reason).slice(0, 60))) f.push('no items and the served items reason is not shown');
  } else {
    if (/data-top-band-items-reason/.test(html)) f.push('the items reason is shown beside items');
    items.forEach((it, i) => {
      const el = drawn[i] || '';
      const open = /^<([a-z0-9]+)([^>]*)>/.exec(el) || [null, '', ''];
      const face = text(el);
      if (!face.includes(it.title)) f.push(`item ${i + 1}: title not shown in served order`);
      if (!face.includes(it.publisher)) f.push(`item ${i + 1}: publisher not shown`);
      const href = /href="([^"]*)"/.exec(open[2]);
      if (it.url) {
        if (open[1] !== 'a' || !href) f.push(`item ${i + 1}: has a url and is not a link`);
        else {
          if (decode(href[1]) !== it.url) f.push(`item ${i + 1}: link is not the served url`);
          if (!/target="_blank"/.test(open[2])) f.push(`item ${i + 1}: link does not open a new tab`);
          if (!/rel="[^"]*noopener/.test(open[2])) f.push(`item ${i + 1}: link has no rel noopener`);
        }
      } else if (open[1] === 'a' || href) f.push(`item ${i + 1}: no url served and it is a link`);
    });
  }
  return f;
}

function gradeProvenance(html, entries) {
  const f = [];
  if (!/data-input-provenance[\s>=]/.test(html)) return ['no data-input-provenance root'];
  const rows = html.split(/(?=<[a-z0-9]+[^>]*data-provenance-row[\s>=])/).slice(1);
  if (rows.length !== entries.length) f.push(`${rows.length} rows (${entries.length} served)`);
  const all = text(html);
  if (RAW_STAMP.test(all)) f.push('a raw stamp is on the page: ' + RAW_STAMP.exec(all)[0]);
  if (/\blanded\b/i.test(all)) f.push('the internal word "landed" is on the page');
  if (/\bNEVER\b/.test(all)) f.push('the raw token NEVER is on the page');
  entries.forEach((e, i) => {
    const t = text(rows[i] || '');
    if (!t.toLowerCase().includes(norm(e.source).toLowerCase())) f.push(`row ${i + 1}: source "${e.source}" not shown`);
    if (e.last_run === 'NEVER') {
      if (!t.toLowerCase().includes(norm(e.reason).toLowerCase().slice(0, 40))) f.push(`row ${i + 1}: never read and the served reason is not shown`);
    } else {
      const y = e.last_run.slice(0, 4);
      if (!(MONTH.test(t) && t.includes(y))) f.push(`row ${i + 1}: the last run is not a date in words`);
    }
  });
  return f;
}

function gradeMount(page, hooks, overlay) {
  const f = [];
  const tabs = page.indexOf('<TabNavigation');
  const band = /<TopBand\b[^>]*band=\{[^}]*\btop_band\b[^}]*\}/.exec(page);
  const prov = /<InputProvenance\b[^>]*entries=\{[^}]*\binput_provenance\b[^}]*\}/.exec(page);
  if (!band) f.push('SecurityAnalysis.tsx does not mount <TopBand band={...top_band}>');
  else if (tabs < 0 || band.index > tabs) f.push('<TopBand> is not above the tabs');
  if (!prov) f.push('SecurityAnalysis.tsx does not mount <InputProvenance entries={...input_provenance}>');
  else if (tabs < 0 || prov.index > tabs) f.push('<InputProvenance> is not above the tabs');
  if (/useRequestRefresh/.test(page)) f.push('SecurityAnalysis.tsx still uses useRequestRefresh');
  if (/useRequestRefresh/.test(hooks)) f.push('hooks/useLeadPanelApi.ts still exports useRequestRefresh');
  if (/\bonRefresh\b|\brefreshPending\b/.test(page)) f.push('SecurityAnalysis.tsx still passes onRefresh / refreshPending');
  if (/\bonRefresh\b|\brefreshPending\b/.test(overlay)) f.push('components/SecurityOverlay.tsx still carries onRefresh / refreshPending');
  return f;
}

const arms = [];
let TB = null; let IP = null;
try { TB = L.source('src/pages/SecurityAnalysis/components/TopBand.tsx'); } catch (e) { TB = null; }
try { IP = L.source('src/pages/SecurityAnalysis/components/InputProvenance.tsx'); } catch (e) { IP = null; }
const safe = (fn) => { try { return fn(); } catch (e) { return ['threw: ' + String(e.message).split('\n')[0]]; } };

{
  let f;
  if (!TB || !TB.TopBand) f = ['no components/TopBand.tsx exporting TopBand'];
  else {
    f = safe(() => {
      const a = gradeBand(L.render(TB.TopBand, { band: BA.top_band }), BA.top_band).map((x) => 'BA: ' + x);
      const b = gradeBand(L.render(TB.TopBand, { band: MSFT.top_band }), MSFT.top_band).map((x) => 'MSFT: ' + x);
      const none = L.render(TB.TopBand, { band: undefined }) !== '' ? ['renders something with no block'] : [];
      return a.concat(b, none);
    });
  }
  arms.push(['THE TOP BAND SAYS WHAT THE COMPANY IS', f.length === 0, f.length ? f.join(' | ') : 'BA: the served line; MSFT: the served reason; social sentence; no items reads as its reason; no block: empty']);
}
{
  let f;
  if (!TB || !TB.TopBand) f = ['no TopBand'];
  else {
    const band = Object.assign({}, BA.top_band, { items: PLANTED_ITEMS, items_reason: null });
    f = safe(() => gradeBand(L.render(TB.TopBand, { band }), band));
  }
  arms.push(["THE DAY'S ITEMS CAN BE FOLLOWED (PLANTED items; 0 of 95 names served one on the capture day)", f.length === 0, f.length ? f.join(' | ') : '2 planted items in served order; the one with a url is a new-tab link to it; the one without is not a link']);
}
{
  let f;
  if (!IP || !IP.InputProvenance) f = ['no components/InputProvenance.tsx exporting InputProvenance'];
  else {
    f = safe(() => {
      const a = gradeProvenance(L.render(IP.InputProvenance, { entries: BA.input_provenance }), BA.input_provenance).map((x) => 'BA: ' + x);
      const b = gradeProvenance(L.render(IP.InputProvenance, { entries: MSFT.input_provenance }), MSFT.input_provenance).map((x) => 'MSFT: ' + x);
      const none = L.render(IP.InputProvenance, { entries: undefined }) !== '' ? ['renders something with no entries'] : [];
      return a.concat(b, none);
    });
  }
  arms.push(['EACH INPUT SHOWS ITS SOURCE, ITS LAST RUN AND ITS RESULT', f.length === 0, f.length ? f.join(' | ') : `BA ${BA.input_provenance.length} rows, MSFT ${MSFT.input_provenance.length} rows: source in words, dates in words, never-read reasons, no raw stamp`]);
}
{
  const f = gradeMount(src('src/pages/SecurityAnalysis/SecurityAnalysis.tsx'), src('src/pages/SecurityAnalysis/hooks/useLeadPanelApi.ts'), src('src/pages/SecurityAnalysis/components/SecurityOverlay.tsx'));
  arms.push(['MOUNTED ABOVE THE TABS; THE RE-RUN BUTTON IS GONE', f.length === 0, f.length ? f.join(' | ') : 'both mounted from the overlay before the tabs; no re-run hook, prop or button']);
}
{
  const f = [];
  const b = Object.assign({}, BA.top_band, { items: PLANTED_ITEMS, items_reason: null });
  const good = `<section data-top-band><p data-top-band-description>${b.description_line}</p><ul>`
    + `<a data-top-band-item href="https://example.com/planted-a?x=1&amp;y=2" target="_blank" rel="noopener noreferrer">${PLANTED_ITEMS[0].title} ${PLANTED_ITEMS[0].publisher}</a>`
    + `<span data-top-band-item>${PLANTED_ITEMS[1].title} ${PLANTED_ITEMS[1].publisher}</span></ul><p data-top-band-social>${b.social}</p></section>`;
  if (gradeBand(good, b).length) f.push('a good band refused: ' + gradeBand(good, b).join(';'));
  if (!gradeBand(good.replace(/<p data-top-band-description>[\s\S]*?<\/p>/, ''), b).length) f.push('a missing description accepted');
  if (!gradeBand(good.replace(/<a data-top-band-item[^>]*>/, '<span data-top-band-item>').replace('</a>', '</span>'), b).length) f.push('an item with a url and no link accepted');
  if (!gradeBand(good.replace(' target="_blank"', ''), b).length) f.push('a same-tab link accepted');
  const e = BA.input_provenance;
  const row = (x, when, extra) => `<li data-provenance-row>${x.source} ${when} ${extra}</li>`;
  const goodP = `<section data-input-provenance>${e.map((x) => row(x, x.last_run === 'NEVER' ? x.reason : 'October 6th, 2026', x.last_run === 'NEVER' ? '' : 'Worked')).join('')}</section>`;
  if (gradeProvenance(goodP, e).length) f.push('a good provenance refused: ' + gradeProvenance(goodP, e).join(';'));
  if (!gradeProvenance(goodP.replace('October 6th, 2026', e[0].last_run), e).length) f.push('the raw stamp accepted');
  if (!gradeProvenance(goodP.replace('Worked', 'landed'), e).length) f.push('the word "landed" accepted');
  const page = '<TopBand band={overlayQuery.data?.top_band} />\n<InputProvenance entries={overlayQuery.data?.input_provenance} />\n<TabNavigation';
  if (gradeMount(page, '', '').length) f.push('a good mount refused: ' + gradeMount(page, '', '').join(';'));
  if (!gradeMount(page, 'export function useRequestRefresh() {', '').length) f.push('a leftover re-run hook accepted');
  if (!gradeMount('<TabNavigation\n' + page.replace('<TabNavigation', ''), '', '').length) f.push('a mount below the tabs accepted');
  arms.push(['PLANTED: the graders refuse a missing description, an unlinked item, the raw stamp, "landed" and a leftover re-run hook', f.length === 0, f.length ? f.join(' | ') : '6 of 6 faults refused; 3 of 3 good forms accepted']);
}

let ok = 0;
for (const [name, pass, ev] of arms) { console.log(`ARM ${pass ? 'PASS' : 'FAIL'} ${name} :: ${ev}`); if (pass) ok += 1; }
console.log(`THE TOP OF THE PAGE AND THE INPUT PROVENANCE ARE DRAWN; THE RE-RUN BUTTON IS GONE: ${ok} of ${arms.length} arms`);
process.exit(ok === arms.length ? 0 : 1);
