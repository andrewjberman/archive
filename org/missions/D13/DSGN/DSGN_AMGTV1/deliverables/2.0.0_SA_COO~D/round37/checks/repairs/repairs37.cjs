/**
 * repairs37.cjs -- DSGN_AMGTV1 round 37, the batched REPAIR CELL check (issuer 2.0.0_SA_COO~D): NO LABEL ACROSS A BUBBLE, NO
 * CROSS-CURRENCY AVERAGE, THE NO-CALL STATE IS DATED.
 *
 * Usage (from the directory whose portal/ is the checkout under test -- the repository root for a worker,
 *   `cd "$(git rev-parse --show-toplevel)" && node "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round37/checks/
 *   repairs/repairs37.cjs"`; C:/tmp/wk-dsgn-amgtv1-92 for the issuer). Fixtures resolve from this file's own location; the portal
 *   resolves from the cwd (cwd/portal).
 *   ISSUER GREEN ARM: CHECK_SRC_OVERRIDE (round15/checks/_load.cjs) is honoured for every render and every source read here; the
 *   render child (_render37.cjs beside this file) and the KEEP children inherit the same environment. A worker never sets it.
 * Fixtures: ../../fixtures/ (capture_r37.py, read-only lambda:Invoke of the deployed opal-amgt-scoped-api, GET routes only):
 *   chatter.{30,90,365}.json (/lead-panel/timeseries/collected/chatter), {peers,overlay,thesis}.{MSFT,AMD}_US_Equity.json.
 * Why (the CTO's round-37 enrichment list, ledger/CTO_COUNTERSIGN_COMPLETION_GRADES_ROUND36.md @9b2ed08fe2; rows in
 *   round36/COMPLETION_GRADES.round36.json):
 *   1 FWD-21 "365D edge labels inside the plot, with no collision": live at 365D (round35/walk/read-20261005T025451Z/
 *     fwd21-365D-face.png) "Kim..." (KMB_US_Equity) is drawn across a red bubble's outline and "Synopsys Inc" (SNPS_US_Equity)
 *     across a green bubble's outline. MEASURED HERE: the static render of this round's 365D capture reproduces both, and the
 *     bubble each one crosses is ITS OWN (KMB circle cx 754.97 r 8.3, label box x 748.0..787.6; SNPS circle cx 363.05 r 28.35,
 *     label box x 312.0..391.2). labels34.cjs read 0 collisions because it skips a label's own bubble entirely. The cause is
 *     ChatterBubbles.tsx's last-resort stage: "Only a slot no bubble touches, or one only this label's own bubble touches, is a
 *     candidate" -- a slot touching only the own bubble is admitted without asking whether the label sits wholly inside it.
 *   2 FWD-8 "no cross-currency average ever; a mixed group says it is mixed and prints no average": live on MSFT Peers the Price
 *     (last) column prints 2,365 / 230,500 / 172,100 / 1,495,000 unlabelled beside USD prices and the page-computed summary rows
 *     average them ("Average 158,633 (n=12)"). cscTable.ts buildCscTable computes every summary over every carried column with
 *     no currency test; PeersTab.tsx prints it.
 *   3 FWD-10 "the 'no call' state carries its as-of date": live on AMD and MSFT the no-call line ("No call on this name yet --
 *     no posture has been drafted for this name yet; the research team adds one") prints no date on any face.
 * SERVED FIELDS THE ARMS ARE GROUNDED ON (printed in the INFO lines at run time):
 *   arm 2 -- the /peers payload: members[].cap_currency (the currency of members[].market_cap_musd; "USD" on every member),
 *     subject.currency (the subject row's currency, "USD"), csc_columns.present[] {code, display_label, relation, transform}.
 *     NO served member carries a price currency: members[] has no `currency` / `price_currency` field, and the Price map entry
 *     states none (relation "the row's own last price scalar", units null). members[].country (United States / Taiwan / South
 *     Korea) is NOT a currency and is never read as one.
 *   arm 3 -- the /overlay and /thesis posture block {status "ABSENT", as_of absent, posture_read.as_of null,
 *     posture_read.read_completed true}; the /thesis bundle's generated_at (the moment the read that found no posture was made).
 * Definitions:
 *   COLLAGE GEOMETRY (arm 1): _collage37.cjs (labels34's model, copied, plus OWN OUTLINE). A label line box (0.6 x font-size per
 *     character, 1.2 x font-size tall, by text-anchor) COLLIDES when it meets another label's box, meets any bubble that is not
 *     its own (labels34's circle-vs-rect test, EPS 0.5), or STRADDLES its own bubble's outline (meets it and is not wholly inside
 *     it); a LEADER collides when it crosses a label other than its own; a box outside the viewBox is CLIPPED.
 *   COLUMN CURRENCY (arm 2), per present column, from served fields only: a column whose served map entry carries transform
 *     "reciprocal" is a RATIO (no currency). Every other column is MONEY; each member's currency for it is the served field for
 *     that figure -- Mkt Cap: members[].cap_currency; Price: members[].currency (the field name the served subject row carries);
 *     any money column: else the ISO code its served map entry states ("(USD mm)" / "USD millions"). The column is ONE currency
 *     when every member with a value has a served code and all are equal, MIXED when the served codes differ, UNSTATED when any
 *     member's code is not served. MIXED and UNSTATED are both "not one currency": no summary may be printed over them.
 *   SAYS MIXED (arm 2): a summary cell of the column, or any text on the tab that names the column's first word, reads
 *     /currencies differ|mixed currencies|currency ... not stated|.../ (MIXED_WORDS below).
 *   CELL NAMES ITS CURRENCY (arm 2): in a MIXED or UNSTATED money column, a member cell printing a figure carries the member's
 *     served code; where none is served, the cell or the column head says the currency is not stated (NOT_STATED below).
 *   THE NO-CALL DATE (arm 3): the served date of an absent posture is its own as_of, else posture_read.as_of, else the bundle's
 *     generated_at; the no-call element ([data-header-posture="ABSENT"], [data-posture-status="ABSENT"]) prints it through the
 *     page's own dateWords longDate (or longStamp), and prints no date (DATE_RE) when none is served.
 * Renders (the child _render37.cjs, one process per mode; the REAL page sources through round15/checks/_load.cjs):
 *   collage  round31 presets/_presets.cjs: the REAL LeadPanel + ChatterBubbles, presets 30/90/365 clicked, over chatter.*.json.
 *   peers    the REAL tabs/PeersTab.tsx over peers/overlay MSFT and AMD, plus PLANTED ONE CURRENCY (AMD, member currency USD) and
 *            PLANTED MIXED (MSFT, member currency USD/TWD/KRW by served country) -- labelled in _render37.cjs.
 *   posture  the header (SecurityOverlay.tsx IdentityHeader, its useThesisBundle answering /thesis), the Lead Panel's exported
 *            PostureHeaderLine (LeadPanel.tsx, rendered with {posture, subjectIdentity, readAt: <served generated_at>} -- the
 *            `readAt` prop is the interface this round pins, since no live page mounts that line), and tabs/PostureTab.tsx, for
 *            MSFT and AMD, plus PLANTED NO DATE and PLANTED OWN DATE per face.
 * Arms:
 *   1  NO LABEL ACROSS A BUBBLE (FWD-21): at 30, 90 and 365 days no label box meets another label box, a bubble not its own, or
 *      its own bubble's outline; no leader crosses a label not its own; every label box lies inside the viewBox; every window
 *      draws at least one label (else NOT_EXERCISED). Offenders print by window and label text.
 *   2  NO CROSS-CURRENCY AVERAGE (FWD-8): on MSFT and AMD as served and on PLANTED MIXED, every MIXED or UNSTATED money column
 *      prints no Average / Median / Min / Max value, says it is mixed, and each of its member cells names its currency (or says
 *      it is not stated); every ONE-currency column (USD Mkt Cap, EV) and every RATIO column still prints all four summaries;
 *      on PLANTED ONE CURRENCY the Price column is one currency and prints all four.
 *   3  THE NO-CALL STATE IS DATED (FWD-10): header, Lead Panel and Posture tab, MSFT and AMD as served: the no-call line still
 *      reads "No call on this name yet" and prints the served date in words; PLANTED OWN DATE prints the posture's own read date
 *      (September 30th, 2026); PLANTED NO DATE prints no date.
 *   4  KEEP: round36 repairs36.cjs; round35 changed35.cjs, cloud35.cjs, payload35.cjs; round34 labels34.cjs, repairs34.cjs,
 *      peername34.cjs; round29 timeline/chart.cjs exit 0 on the same tree.
 *   5  PLANTED: arm 1's grader flags a label over a foreign bubble, a label across its own outline, a label over a label, a leader
 *      through a foreign label and a clipped label, and accepts a clean layout (a label inside its own bubble, one beside it);
 *      arm 2's grader flags a mixed column printing an average, a mixed column that never says so, a bare figure in a mixed
 *      column, and a one-currency column that lost its summary, and accepts the good shape; arm 3's grader flags a no-call with
 *      no date while one is served and a dated no-call when none is, and accepts both good shapes.
 * Blind spots: the label box is the 0.6 em estimate (it over-measures Lato mixed case, round34 MEASURED), so a box straddle can be
 *   a near-miss on screen; a leader crossing a BUBBLE is printed (INFO) but not graded -- the list names labels only; the collage
 *   is this round's capture, not every day's data. Arm 2 grades the columns the tab shows; an UNSTATED column is "not one
 *   currency" because the served payload does not say otherwise -- the AMD Price summary goes too, until the producer serves a
 *   member price currency (PLANTED ONE CURRENCY proves the summaries come back the day it does). Arm 3 reads the header's date
 *   from the /thesis read (the /overlay serves no read time); longDate reads the UTC day of generated_at (03:45Z on Oct 5 is
 *   Oct 4 in ET) -- longStamp, which names the ET clock, is also accepted.
 * Prints INFO lines, one line per arm and "NO LABEL ACROSS A BUBBLE, NO CROSS-CURRENCY AVERAGE, THE NO-CALL STATE IS DATED: <k> of
 * 5 arms"; exit 0 only at 5 of 5. Static renders only; no network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const DROOT = path.join(__dirname, '..', '..', '..');
const PORTAL = path.join(process.cwd(), 'portal');
const SA = 'src/pages/SecurityAnalysis/';
const TITLE = 'NO LABEL ACROSS A BUBBLE, NO CROSS-CURRENCY AVERAGE, THE NO-CALL STATE IS DATED';
const C = require(path.join(__dirname, '_collage37.cjs'));
const norm = (s) => String(s === null || s === undefined ? '' : s).replace(/\s+/g, ' ').trim();

if (!fs.existsSync(path.join(PORTAL, 'package.json'))) {
  console.log('LOADER ERROR: no portal/package.json under ' + process.cwd() + ' -- run from the directory whose portal/ is under test');
  process.exit(3);
}

// ---- sources (override-aware) ----------------------------------------------------------------------------------------------
const OVERRIDES = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) {
  const i = pair.indexOf('=');
  OVERRIDES[pair.slice(0, i)] = pair.slice(i + 1);
}
function readSource(rel) {
  const f = OVERRIDES[rel] || path.join(PORTAL, rel);
  try { return fs.readFileSync(f, 'utf8'); } catch (e) { return null; }
}

function child(mode) {
  const r = spawnSync(process.execPath, [path.join(__dirname, '_render37.cjs'), mode], { cwd: process.cwd(), env: process.env, encoding: 'utf8', timeout: 600000, maxBuffer: 256 * 1024 * 1024 });
  const lines = String(r.stdout || '').split('\n').filter((x) => x.startsWith('{'));
  if (!lines.length) return { error: `the ${mode} render child printed no result (rc=${r.status}; ${norm(String(r.stderr || r.stdout || '')).slice(0, 160)})` };
  try { return JSON.parse(lines[lines.length - 1]); } catch (e) { return { error: `the ${mode} render child printed unreadable JSON` }; }
}

// ---- a small markup tree (react-dom/server output is well formed) -----------------------------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
function parse(html) {
  const root = { tag: '#root', attrs: {}, children: [], parent: null };
  let cur = root;
  const re = /<!--[\s\S]*?-->|<\/([a-zA-Z][\w:.-]*)\s*>|<([a-zA-Z][\w:.-]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>|([^<]+)/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[1]) { let n = cur; while (n && n.tag !== m[1].toLowerCase()) n = n.parent; if (n && n.parent) cur = n.parent; }
    else if (m[2]) {
      const attrs = {};
      const ar = /([^\s=>\/]+)(?:="([^"]*)")?/g;
      let a;
      while ((a = ar.exec(m[3] || '')) !== null) attrs[a[1]] = a[2] === undefined ? '' : decode(a[2]);
      const node = { tag: m[2].toLowerCase(), attrs, children: [], parent: cur };
      cur.children.push(node);
      if (!m[4] && !VOID.has(node.tag)) cur = node;
    } else if (m[5]) cur.children.push({ text: decode(m[5]), parent: cur });
  }
  return root;
}
function all(node, pred, out) {
  out = out || [];
  for (const c of node.children || []) if (c.tag) { if (pred(c)) out.push(c); all(c, pred, out); }
  return out;
}
const textOf = (node) => norm(node.text !== undefined ? node.text : (node.children || []).map(textOf).join(' '));
const ownText = (node) => norm((node.children || []).map((c) => (c.text !== undefined ? c.text : (['span', 'b', 'strong', 'em', 'i', 'a'].includes(c.tag) ? textOf(c) : ' '))).join(' '));

// ==== arm 1 grader ================================================================================================================
/** names: Map key -> served display name. Returns [{kind, text}] for one collage markup. */
function collageFaults(html, names) {
  const m = C.collageModel(html);
  return { model: m, faults: [...C.collisionFaults(m, names), ...C.clipFaults(m)] };
}

// ==== arm 2 grader ================================================================================================================
const MIXED_WORDS = /currenc(?:y|ies)\b[^.;]{0,80}\b(?:differ|different|mixed|not (?:stated|served|the same|all the same|one))|\b(?:mixed|different|differing|several|more than one)\s+currenc/i;
const NOT_STATED = /currenc(?:y|ies)\b[^.;]{0,40}\bnot (?:stated|served)|\bnot (?:stated|served)\b[^.;]{0,40}currenc/i;
const MEMBER_FIELD = { price: 'price', mkt_val_sec: 'market_cap_musd', ev: 'ev', ey: 'ey' };
const DIGIT = /\d/;
const pathGet = (o, p) => p.split('.').reduce((v, k) => (v && typeof v === 'object' ? v[k] : undefined), o);
/** The served currency status of one present column: {kind: RATIO|ONE|MIXED|UNSTATED, codes: [per member], members: [index]}. */
function columnCurrency(peers, code) {
  const entry = ((peers.csc_columns && peers.csc_columns.present) || []).find((e) => e.code === code);
  if (!entry) return null;
  if (entry.transform === 'reciprocal') return { kind: 'RATIO', codes: [], members: [] };
  const sm = /\b([A-Z]{3})\s*(?:mm|millions?)\b/.exec(`${entry.display_label || ''} ${entry.relation || ''}`);
  const mapCode = sm ? sm[1] : null;
  const codes = [];
  const members = [];
  (peers.members || []).forEach((m, i) => {
    const field = MEMBER_FIELD[code] || null;
    if (field && !Number.isFinite(pathGet(m, field))) return;
    const own = code === 'mkt_val_sec' ? m.cap_currency : code === 'price' ? m.currency : null;
    codes.push(typeof own === 'string' && own.trim() ? own.trim() : mapCode);
    members.push(i);
  });
  const set = [...new Set(codes)];
  const kind = codes.some((c) => !c) ? 'UNSTATED' : set.length > 1 ? 'MIXED' : 'ONE';
  return { kind, codes, members };
}
/** The tab's table as {heads: [{code, text, node}], members: [[cellText]], summary: {label: [cellText]}, texts: [ownText]}. */
function readTable(html) {
  const tree = parse(html);
  const table = all(tree, (n) => n.tag === 'table' && n.attrs['data-csc-table'] !== undefined)[0];
  if (!table) return null;
  const ths = all(table, (n) => n.tag === 'th');
  const heads = ths.map((n) => ({ code: n.attrs['data-csc-column-code'] || null, text: textOf(n) })).slice(2);
  const cells = (tr) => all(tr, (n) => n.tag === 'td' && n.parent === tr).map(textOf).slice(2);
  const members = all(table, (n) => n.tag === 'tr' && n.attrs['data-csc-row'] === 'member').map(cells);
  const summary = {};
  for (const tr of all(table, (n) => n.tag === 'tr' && n.attrs['data-csc-summary'] !== undefined)) summary[tr.attrs['data-csc-summary']] = cells(tr);
  const texts = all(tree, (n) => ['p', 'span', 'li', 'div', 'td', 'th', 'caption', 'summary'].includes(n.tag)).map(ownText).filter(Boolean);
  return { heads, members, summary, texts };
}
const SUMS = ['Average', 'Median', 'Min', 'Max'];
/** Arm 2 faults for one rendered case: c = {name, html, peers, stop}. Also returns the per-column reading. */
function peersFaults(c) {
  if (c.stop) return { faults: [`${c.name}: ${c.stop}`], read: [] };
  const t = readTable(c.html || '');
  if (!t) return { faults: [`${c.name}: no [data-csc-table] rendered`], read: [] };
  const f = [];
  const read = [];
  t.heads.forEach((h, k) => {
    if (!h.code) return;
    const cur = columnCurrency(c.peers, h.code);
    if (!cur) return;
    const sumCells = SUMS.map((s) => (t.summary[s] || [])[k] || '');
    const printed = SUMS.filter((s, j) => DIGIT.test(sumCells[j]));
    const head = h.text;
    if (cur.kind === 'RATIO' || cur.kind === 'ONE') {
      const hasValues = cur.kind === 'RATIO' ? t.members.some((r) => DIGIT.test(r[k] || '')) : cur.members.length > 0;
      const missing = SUMS.filter((s) => !printed.includes(s));
      if (hasValues && missing.length) f.push(`${c.name}: the ${cur.kind === 'ONE' ? `one-currency (${cur.codes[0]})` : 'ratio'} column "${head}" lost its ${missing.join('/')} (cells: ${sumCells.map((x) => `"${x}"`).join(' ')})`);
      read.push(`${head} ${cur.kind === 'ONE' ? cur.codes[0] : 'ratio'} ${printed.length}/4`);
      return;
    }
    const detail = cur.kind === 'MIXED' ? `served member currencies ${[...new Set(cur.codes)].sort().join('/')}` : `${cur.codes.filter((x) => !x).length} of ${cur.codes.length} members serve no currency for it`;
    for (const s of printed) f.push(`${c.name}: "${head}" is not one currency (${detail}) and still prints ${s} "${sumCells[SUMS.indexOf(s)]}"`);
    const word = (head.split(/[\s(]/)[0] || head).toLowerCase();
    const says = sumCells.some((x) => MIXED_WORDS.test(x)) || t.texts.some((x) => MIXED_WORDS.test(x) && x.toLowerCase().includes(word));
    if (!says) f.push(`${c.name}: "${head}" is not one currency (${detail}) and the tab says nowhere that its currencies differ or are not stated`);
    const bare = [];
    cur.members.forEach((mi, j) => {
      const cell = (t.members[mi] || [])[k] || '';
      if (!DIGIT.test(cell)) return;
      const code = cur.codes[j];
      if (code ? !new RegExp(`\\b${code}\\b`).test(cell) : !(NOT_STATED.test(cell) || NOT_STATED.test(head))) bare.push(`"${cell}"${code ? ` (served ${code})` : ' (no served currency)'}`);
    });
    if (bare.length) f.push(`${c.name}: "${head}" is not one currency and ${bare.length} member cell(s) do not name their currency: ${bare.slice(0, 4).join(', ')}${bare.length > 4 ? ', ...' : ''}`);
    read.push(`${head} ${cur.kind} ${printed.length}/4`);
  });
  return { faults: f, read };
}

// ==== arm 3 grader ================================================================================================================
const DATE_RE = /\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b|\b\d{4}-\d{2}-\d{2}\b/;
/** c = {name, kind, want, wantWords, wantStamp, line, stop}. */
function postureFaults(c) {
  if (c.stop) return [`${c.name}: ${c.stop}`];
  const f = [];
  const line = norm(c.line);
  if (!/No call on this name yet/.test(line)) f.push(`${c.name}: the no-call line lost "No call on this name yet" ("${line.slice(0, 80)}")`);
  if (c.want) {
    if (!(c.wantWords && line.includes(c.wantWords)) && !(c.wantStamp && line.includes(c.wantStamp))) f.push(`${c.name}: "${line.slice(0, 110)}" prints no date; the served ${c.want} reads "${c.wantWords}"`);
  } else {
    const m = DATE_RE.exec(line);
    if (m) f.push(`${c.name}: prints the date "${m[0]}" though the payload serves none`);
  }
  return f;
}

function keepsPassing(rels) {
  const faults = [];
  for (const rel of rels) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), env: process.env, encoding: 'utf8', timeout: 1800000, maxBuffer: 64 * 1024 * 1024 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) faults.push(`KEEP: ${rel} rc=${r.status} ("${last.slice(0, 100)}")`);
  }
  return faults;
}

// ==== renders =====================================================================================================================
const COL = child('collage');
const PEERS = child('peers');
const POST = child('posture');

// ---- INFO: the served fields and the source lines at fault ----
{
  const fx = (f) => { try { const d = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'fixtures', f), 'utf8')); return d.payload; } catch (e) { return null; } };
  const parts = [];
  for (const key of ['MSFT_US_Equity', 'AMD_US_Equity']) {
    const p = fx(`peers.${key}.json`);
    const th = fx(`thesis.${key}.json`);
    const ov = fx(`overlay.${key}.json`);
    if (p) {
      const ms = p.members || [];
      const cnt = (k) => ms.filter((m) => m[k] !== undefined && m[k] !== null).length;
      const price = ((p.csc_columns && p.csc_columns.present) || []).find((e) => e.code === 'price') || {};
      parts.push(`${key.split('_')[0]} /peers: members[].cap_currency on ${cnt('cap_currency')} of ${ms.length} (${[...new Set(ms.map((m) => m.cap_currency))].join('/')}), members[].currency on ${cnt('currency')}, members[].price_currency on ${cnt('price_currency')}, subject.currency ${p.subject && p.subject.currency}, Price map {relation "${price.relation}", units ${price.units}}, member countries ${[...new Set(ms.map((m) => m.country))].join('/')}`);
    }
    if (th && ov) parts.push(`${key.split('_')[0]} posture: /overlay status ${ov.posture && ov.posture.status} as_of ${ov.posture && ov.posture.as_of} posture_read.as_of ${ov.posture && ov.posture.posture_read && ov.posture.posture_read.as_of}; /thesis status ${th.posture && th.posture.status} posture_read.as_of ${th.posture && th.posture.posture_read && th.posture.posture_read.as_of}, generated_at ${th.generated_at}; /overlay generated_at ${ov.generated_at}`);
  }
  console.log(`INFO served fields: ${parts.join(' | ')}`);
  const SITES = [
    [SA + 'components/ChatterBubbles.tsx', /Only a slot no bubble touches, or one only this label's own bubble touches, is a candidate/],
    [SA + 'cscTable.ts', /values\.push\(numbers\.length === 0 \? null : statistic/],
    [SA + 'components/LeadPanel.tsx', /\$\{NO_CALL_WORDS\} -- \$\{NO_CALL_REASON_WORDS\['not-drafted'\]\}`\}/],
    [SA + 'components/SecurityOverlay.tsx', /\$\{NO_CALL_WORDS\} -- \$\{NO_CALL_REASON_WORDS\['not-drafted'\]\}`\}/],
    [SA + 'tabs/PostureTab.tsx', /<PanelEmpty message=\{NO_CALL_WORDS\} detail=\{NO_CALL_REASON_WORDS\['not-drafted'\]\} \/>/],
  ];
  const hits = [];
  for (const [rel, re] of SITES) String(readSource(rel) || '').split(/\r?\n/).forEach((l, i) => { if (re.test(l)) hits.push(`${rel.replace(SA, '')}:${i + 1} ${norm(l).slice(0, 90)}`); });
  console.log(`INFO base fault-site census (not graded): ${hits.length} line(s)${hits.length ? ': ' + hits.join(' | ') : ''}`);
}

const arms = [];
// ---- arm 1 ----
{
  const f = [];
  const tally = [];
  const names = new Map(Object.entries(COL.names || {}));
  if (COL.error) f.push(COL.error);
  const renders = COL.renders || [];
  if (!COL.error && renders.length !== 3) f.push(`${renders.length} of 3 collage renders`);
  let info = [];
  for (const r of renders) {
    if (!r.html) { f.push(`${r.name}: no render (${r.stop})`); continue; }
    const { model, faults } = collageFaults(r.html, names);
    if (!model.labels.length) f.push(`${r.name}: NOT_EXERCISED (no label drawn)`);
    const k = (re) => faults.filter((x) => re.test(x.kind)).length;
    tally.push(`${r.name} ${model.marks.length} bubbles, ${model.labels.length} labels, ${model.leaders.length} leaders: ${k(/OVER LABEL/)} label/label, ${k(/OVER BUBBLE/)} label/bubble, ${k(/OWN OUTLINE/)} own-outline, ${k(/LINE THROUGH/)} line/label, ${k(/CLIPPED/)} clipped`);
    f.push(...faults.map((x) => `${r.name} ${x.kind}: ${x.text}`));
    if (r.days === 365) {
      const live = ['Kim...', 'Synopsys Inc'].map((t) => `"${t}" ${faults.some((x) => x.text.startsWith(`"${t}"`)) ? 'REPRODUCED' : 'not reproduced'}`);
      info.push(`365D walk read-20261005T025451Z offenders: ${live.join(', ')}`);
    }
    info.push(`${r.name} leaders through a bubble not their own: ${C.leaderBubbleCrossings(model, names).length}`);
  }
  console.log(`INFO collage (not graded): ${info.join('; ')}`);
  arms.push(['NO LABEL ACROSS A BUBBLE: at 30/90/365 no label meets another label, a bubble not its own or its own bubble\'s outline, no leader crosses a foreign label, every label inside the viewBox', f.length === 0,
    (f.length ? `${f.length} fault(s): ${f.join(' | ')}` : '0 collisions') + ` [${tally.join('; ')}]`]);
}
// ---- arm 2 ----
{
  const f = [];
  const reads = [];
  if (PEERS.error) f.push(PEERS.error);
  const cases = PEERS.cases || [];
  if (!PEERS.error && cases.length !== 4) f.push(`${cases.length} of 4 peers cases rendered`);
  let sawNotOne = false;
  let sawOnePrice = false;
  for (const c of cases) {
    const r = peersFaults(c);
    f.push(...r.faults);
    reads.push(`${c.name.replace(/ \(.*\)$/, '')}: ${r.read.join(', ')}`);
    if (!c.planted && r.read.some((x) => /^Price.* (MIXED|UNSTATED) /.test(x))) sawNotOne = true;
    if (/ONE CURRENCY/.test(c.name) && r.read.some((x) => /^Price.* USD /.test(x))) sawOnePrice = true;
  }
  if (!PEERS.error && !sawNotOne) f.push('NOT_EXERCISED: no served case has a Price column that is not one currency');
  if (!PEERS.error && !sawOnePrice) f.push('NOT_EXERCISED: PLANTED ONE CURRENCY did not read its Price column as one currency (USD)');
  arms.push(['NO CROSS-CURRENCY AVERAGE: a money column that is not one served currency prints no Average/Median/Min/Max, says so, and names each cell\'s currency; one-currency and ratio columns keep all four', f.length === 0,
    (f.length ? `${f.length} fault(s): ${f.join(' | ')}` : `${cases.length} of ${cases.length} cases clean`) + ` [${reads.join('; ')}]`]);
}
// ---- arm 3 ----
{
  const f = [];
  if (POST.error) f.push(POST.error);
  const cases = POST.cases || [];
  if (!POST.error && cases.length !== 12) f.push(`${cases.length} of 12 no-call cases rendered`);
  for (const c of cases) f.push(...postureFaults(c));
  const shown = cases.filter((c) => c.kind === 'served' && c.key === 'MSFT_US_Equity').map((c) => `${c.face}: "${norm(c.line).slice(0, 120)}"`);
  arms.push(['THE NO-CALL STATE IS DATED: header, Lead Panel and Posture tab print the served date of an absent posture in words, its own read date first, and no date when none is served', f.length === 0,
    (f.length ? `${f.length} fault(s): ${f.join(' | ')}` : `${cases.length} of ${cases.length} cases`) + ` [served MSFT: ${shown.join('; ')}]`]);
}
// ---- arm 4: KEEP ----
{
  const KEEP = ['round36/checks/repairs/repairs36.cjs', 'round35/checks/changed/changed35.cjs', 'round35/checks/cloud/cloud35.cjs',
    'round35/checks/words/payload35.cjs', 'round34/checks/collage/labels34.cjs', 'round34/checks/repairs/repairs34.cjs',
    'round34/checks/names/peername34.cjs', 'round29/checks/timeline/chart.cjs'];
  const f = keepsPassing(KEEP);
  arms.push(['KEEP: round36 repairs36, round35 changed35/cloud35/payload35, round34 labels34/repairs34/peername34 and round29 timeline/chart.cjs exit 0 on the same tree', f.length === 0,
    f.length ? f.join(' | ') : `${KEEP.length} of ${KEEP.length} exit 0`]);
}
// ---- arm 5: PLANTED ----
{
  const f = [];
  let bad = 0; let rej = 0; let good = 0; let acc = 0;
  const R = (label, faults, why) => { bad += 1; if (faults.some((x) => why.test(x))) rej += 1; else f.push(`"${label}" not flagged for its reason (${faults.length ? faults[0] : 'accepted'})`); };
  const A = (label, faults) => { good += 1; if (!faults.length) acc += 1; else f.push(`"${label}" rejected: ${faults[0]}`); };
  // arm 1's grader
  const names = new Map([['A', 'Alpha'], ['B', 'Beta Holdings'], ['C', 'Gamma'], ['D', 'Delta Co']]);
  const g = (k, c, l, extra) => `<g><circle data-bubble="${k}" cx="${c[0]}" cy="${c[1]}" r="${c[2]}"></circle>${extra || ''}<g data-bubble-label-group="${k}"><title>${names.get(k)}</title>` +
    `<text data-bubble-label="${k}" x="${l[0]}" y="${l[1]}" font-size="11" text-anchor="middle" dominant-baseline="central">${l[2]}</text></g></g>`;
  const CLEAN = { A: [[100, 100, 40], [100, 100, 'Alpha']], B: [[220, 100, 20], [220, 140, 'Beta Holdings'], '<line x1="220" y1="120" x2="220" y2="133"></line>'], C: [[330, 100, 10], [330, 125, 'Gamma']], D: [[330, 220, 10], [330, 245, 'Delta Co']] };
  const build = (over) => { const s = JSON.parse(JSON.stringify(CLEAN)); (over || (() => {}))(s); return `<div><svg viewBox="0 0 400 300">${Object.keys(s).map((k) => g(k, s[k][0], s[k][1], s[k][2])).join('')}</svg></div>`; };
  const cj = (html) => collageFaults(html, names).faults.map((x) => `${x.kind}: ${x.text}`);
  A('a clean collage (a label inside its own bubble, three beside theirs)', cj(build()));
  R('a label over a foreign bubble', cj(build((s) => { s.C[1] = [100, 135, 'Gamma']; })), /^LABEL OVER BUBBLE: "Gamma" over the bubble of "Alpha"/);
  R('a label across its own outline', cj(build((s) => { s.C[1] = [340, 100, 'Gamma']; })), /^LABEL ACROSS ITS OWN OUTLINE: "Gamma"/);
  R('a label over a label', cj(build((s) => { s.C[1] = [330, 243, 'Gamma']; })), /^LABEL OVER LABEL/);
  R('a leader through a foreign label', cj(build((s) => { s.B[2] = '<line x1="220" y1="120" x2="335" y2="250"></line>'; })), /^LINE THROUGH LABEL: the leader line of "Beta Holdings" runs through "Delta Co"/);
  R('a clipped label', cj(build((s) => { s.D[1] = [395, 245, 'Delta Co']; })), /^CLIPPED: "Delta Co"/);
  // arm 2's grader
  const PEER = {
    csc_columns: { present: [
      { code: 'price', display_label: 'Price (last)', relation: "the row's own last price scalar", transform: null },
      { code: 'mkt_val_sec', display_label: 'Mkt Cap (USD mm)', relation: 'direct (USD millions)', transform: null },
      { code: 'ey', display_label: 'P/E (trailing)', relation: 'RECIPROCAL', transform: 'reciprocal' },
    ] },
    members: [
      { name: 'One', price: 100, market_cap_musd: 10, cap_currency: 'USD', ey: 5, currency: 'USD' },
      { name: 'Two', price: 2365, market_cap_musd: 20, cap_currency: 'USD', ey: 4, currency: 'TWD' },
      { name: 'Three', price: 230500, market_cap_musd: 30, cap_currency: 'USD', ey: 2, currency: 'KRW' },
    ],
  };
  const tbl = (cells, sums, head, note) => `<div><table data-csc-table=""><thead><tr><th>Name</th><th>Ticker</th><th data-csc-column-code="price">${head || 'Price (last)'}</th><th data-csc-column-code="mkt_val_sec">Mkt Cap (USD mm)</th><th data-csc-column-code="ey">P/E (trailing)</th></tr></thead><tbody>` +
    PEER.members.map((m, i) => `<tr data-csc-row="member"><td>${m.name}</td><td>T${i}</td><td>${cells[i]}</td><td>USD ${m.market_cap_musd}</td><td>${(100 / m.ey).toFixed(2)}</td></tr>`).join('') +
    SUMS.map((s) => `<tr data-csc-summary="${s}"><td>${s}</td><td></td><td>${sums}</td><td>20.00 (n=3)</td><td>30.00 (n=3)</td></tr>`).join('') + `</tbody></table>${note || ''}</div>`;
  const GOODC = ['USD 100.00', 'TWD 2,365', 'KRW 230,500'];
  const pj = (html) => peersFaults({ name: 'planted', html, peers: PEER, stop: null }).faults;
  A('a mixed Price column: no summary, "not averaged: currencies differ", every cell coded', pj(tbl(GOODC, 'not averaged: currencies differ')));
  R('a mixed column printing an average', pj(tbl(GOODC, '77,655 (n=3)', null, '<p>Price (last): currencies differ.</p>')), /still prints Average "77,655 \(n=3\)"/);
  R('a mixed column that never says so', pj(tbl(GOODC, '--')), /says nowhere that its currencies differ/);
  R('a bare figure in a mixed column', pj(tbl(['USD 100.00', '2,365', 'KRW 230,500'], 'not averaged: currencies differ')), /do not name their currency: "2,365" \(served TWD\)/);
  R('a one-currency column that lost its summary', pj(tbl(GOODC, 'not averaged: currencies differ').replace(/<td>20\.00 \(n=3\)<\/td>/g, '<td>--</td>')), /one-currency \(USD\) column "Mkt Cap \(USD mm\)" lost its Average/);
  // arm 3's grader
  const pc = (want, line) => postureFaults({ name: 'planted', kind: want ? 'served' : 'nodate', want, wantWords: want ? 'October 5th, 2026' : null, wantStamp: null, line, stop: null });
  R('a no-call with no date while one is served', pc('2026-10-05T03:45Z', 'No call on this name yet -- no posture has been drafted for this name yet'), /prints no date; the served 2026-10-05T03:45Z reads "October 5th, 2026"/);
  A('a no-call carrying the served date', pc('2026-10-05T03:45Z', 'No call on this name yet as of October 5th, 2026 -- no posture has been drafted'));
  R('a dated no-call when none is served', pc(null, 'No call on this name yet as of October 5th, 2026'), /prints the date "October 5th, 2026" though the payload serves none/);
  A('an undated no-call when none is served', pc(null, 'No call on this name yet -- no posture has been drafted for this name yet'));
  arms.push(['PLANTED: the three graders flag their planted faults (foreign bubble, own outline, label/label, leader/label, clipped; a mixed average, an unsaid mix, a bare mixed cell, a lost one-currency summary; an undated served no-call, a dated unserved one) and accept the good shapes', f.length === 0,
    f.length ? f.join(' | ') : `${rej} of ${bad} planted faults flagged for their reason; ${acc} of ${good} good shapes accepted`]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`${TITLE}: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
