/**
 * feedrest.cjs -- DSGN_AMGTV1 round 31, AV-zi-2 (issuer 2.0.0_SA_COO~D): ONE NEWS ITEM AT REST, THE REST ONE PRESS AWAY.
 *
 * Usage (worktree root): node <this file>        (portal/ under the cwd is the checkout under test)
 * Why: SAUX-15 (FWD-12/27 first viewport): at 1440x900 the first tab panel must start inside 900 px. The round-30 close walk measured
 *   the active tab's underline at y=917 (first panel ~943): RESAPP an-7 now serves BA 69 feed items, so HeaderBrief draws 2 open items
 *   + "Expand (67 more)". One open item at rest recovers ~49 px (ROUND30_CLOSE.md section 3; CTO msg 28869 accepted it for round 31).
 *   The pixel grade is the issuer's close walk; this check grades the structure that buys the pixels.
 * Inputs: round30/fixtures/repairs/overlay.BA_US_Equity.urlnull.PLANTED.json (the served overlay shape; its feed items are the
 *   template), widened here to 69 and to 1 item; round14/fixtures/overlay.BA_US_Equity.json (SERVED, 1 item).
 * Arms:
 *   1  AT REST: with 69 and with 5 served items, exactly ONE [data-feed-item] sits outside a closed <details>; every other item sits
 *      inside one closed Expand <details> whose summary names the remaining count in words ("68 more").
 *   2  ONE ITEM: with 1 served item, that item is open and no Expand is drawn.
 *   3  KEEP (a control; passes at base by design): round29 timeline/dayopen.cjs and round30 repairs/served.cjs still exit 0 on the
 *      same checkout (they read HeaderBrief).
 *   4  PLANTED: the at-rest predicate rejects 2 open, 0 open, and an item outside both the open slot and the Expand; it accepts the
 *      good shape.
 * Prints one line per arm and "ONE NEWS ITEM AT REST, THE REST ONE PRESS AWAY: <k> of 4 arms"; exit 0 only at 4 of 4.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const SA = 'src/pages/SecurityAnalysis/';
const DROOT = path.join(__dirname, '..', '..', '..');
const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
const readJson = (p) => JSON.parse(fs.readFileSync(path.join(DROOT, p), 'utf8'));
const pay = (x) => (x && x.payload ? x.payload : x);
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
const clone = (x) => JSON.parse(JSON.stringify(x));

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const decode = (s) => String(s).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
function parse(html) {
  const root = { tag: '#root', attrs: {}, children: [], parent: null };
  let cur = root;
  const re = /<!--[\s\S]*?-->|<\/([a-zA-Z][\w:-]*)\s*>|<([a-zA-Z][\w:-]*)((?:\s+[^\s=>\/]+(?:="[^"]*")?)*)\s*(\/?)>|([^<]+)/g;
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
function all(node, pred, out = []) { for (const c of node.children || []) if (c.tag) { if (pred(c)) out.push(c); all(c, pred, out); } return out; }
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
const text = (n) => (n.text !== undefined ? n.text : (n.children || []).map(text).join(' '));
const closedDetailsAncestor = (n) => { for (let p = n.parent; p; p = p.parent) if (p.tag === 'details' && p.attrs.open === undefined) return p; return null; };

/** At rest: exactly ONE item outside a closed <details>; the rest inside ONE closed details whose summary names "<n> more". */
function atRestFaults(tree, served) {
  const f = [];
  const rows = all(tree, (n) => n.attrs['data-feed-item'] !== undefined);
  if (rows.length !== served) f.push(`${rows.length} [data-feed-item] rows for ${served} served`);
  const open = rows.filter((r) => !closedDetailsAncestor(r));
  const folded = rows.filter((r) => closedDetailsAncestor(r));
  if (open.length !== Math.min(1, served)) f.push(`${open.length} item(s) open at rest (want ${Math.min(1, served)})`);
  const holders = new Set(folded.map((r) => closedDetailsAncestor(r)));
  if (served > 1) {
    if (holders.size !== 1) f.push(`${holders.size} closed details hold the folded items (want 1)`);
    const h = [...holders][0];
    if (h) {
      const sum = all(h, (n) => n.tag === 'summary')[0];
      const want = served - 1;
      if (!sum || !new RegExp(`\\b${want}\\b[^0-9]*more`, 'i').test(norm(text(sum)))) f.push(`the Expand summary does not name "${want} more" ("${sum ? norm(text(sum)).slice(0, 40) : 'none'}")`);
    }
  } else if (holders.size) f.push(`an Expand is drawn for ${served} item`);
  return f;
}

function widen(bundle, n) {
  const b = clone(bundle);
  const tpl = b.feed.items;
  const items = [];
  for (let i = 0; i < n; i++) {
    const t = clone(tpl[i % tpl.length]);
    const d = new Date(Date.UTC(2026, 9, 2) - i * 86400000).toISOString().slice(0, 10);
    t.article_key = `harvest:BA:${d}:r31-${i}`;
    t.title = `Planted headline ${i + 1} for the at-rest count`;
    t.published_date = d;
    t.published_at = `${d}T12:00:00Z`;
    items.push(t);
  }
  b.feed.items = items;
  return b;
}

const arms = [];
let HB = null;
let loadErr = null;
try { HB = L.source(SA + 'components/HeaderBrief.tsx').HeaderBrief; if (typeof HB !== 'function') throw new Error('no HeaderBrief export'); } catch (e) { loadErr = 'LOAD: ' + first(e); }
const PLANTED = pay(readJson('round30/fixtures/repairs/overlay.BA_US_Equity.urlnull.PLANTED.json'));
const SERVED1 = pay(readJson('round14/fixtures/overlay.BA_US_Equity.json'));

// Arm 1 -- at rest with many items.
{
  const f = [];
  if (!HB) f.push(loadErr);
  else for (const n of [69, 5]) {
    try { f.push(...atRestFaults(parse(L.render(HB, { bundle: widen(PLANTED, n) })), n).map((x) => `${n} items: ${x}`)); } catch (e) { f.push(`${n} items: RENDER ${first(e)}`); }
  }
  arms.push(['AT REST: with 69 and 5 served items, exactly one item is open and the rest sit in one closed Expand naming the count', f.length === 0, f.length ? f.join(' | ') : '69 -> 1 open + "68 more"; 5 -> 1 open + "4 more"']);
}
// Arm 2 -- one item.
{
  const f = [];
  if (!HB) f.push(loadErr);
  else {
    const n = (SERVED1.feed && SERVED1.feed.items || []).length;
    try { f.push(...atRestFaults(parse(L.render(HB, { bundle: SERVED1 })), n).map((x) => `served (${n}): ${x}`)); } catch (e) { f.push('RENDER ' + first(e)); }
  }
  arms.push(['ONE ITEM: the served BA feed (1 item) draws that item open and no Expand', f.length === 0, f.length ? f.join(' | ') : '1 open, no Expand']);
}
// Arm 3 -- the checks over the same file keep passing.
{
  const f = [];
  for (const rel of ['round29/checks/timeline/dayopen.cjs', 'round30/checks/repairs/served.cjs']) {
    const r = spawnSync(process.execPath, [path.join(DROOT, rel)], { cwd: process.cwd(), encoding: 'utf8', timeout: 600000 });
    const last = ((r.stdout || '') + (r.stderr || '')).trim().split('\n').pop() || '';
    if (r.status !== 0) f.push(`${rel} rc=${r.status} ("${last.slice(0, 80)}")`);
  }
  arms.push(['KEEP: round29 dayopen.cjs and round30 served.cjs still exit 0', f.length === 0, f.length ? f.join(' | ') : 'both exit 0']);
}
// Arm 4 -- planted.
{
  const f = [];
  const item = (k) => `<li data-feed-item="${k}"><span>Headline ${k}</span></li>`;
  const good = `<div data-header-feed="SERVED"><ul>${item('a')}</ul><details data-feed-expand=""><summary>Expand (2 more)</summary><ul>${item('b')}${item('c')}</ul></details></div>`;
  const twoOpen = `<div data-header-feed="SERVED"><ul>${item('a')}${item('b')}</ul><details><summary>Expand (1 more)</summary><ul>${item('c')}</ul></details></div>`;
  const noneOpen = `<div data-header-feed="SERVED"><details><summary>Expand (3 more)</summary><ul>${item('a')}${item('b')}${item('c')}</ul></details></div>`;
  const stray = `<div data-header-feed="SERVED"><ul>${item('a')}</ul><details><summary>Expand (1 more)</summary><ul>${item('b')}</ul></details><ul>${item('c')}</ul></div>`;
  if (atRestFaults(parse(good), 3).length) f.push(`the good shape is rejected: ${atRestFaults(parse(good), 3)[0]}`);
  for (const [n, h] of [['two open', twoOpen], ['none open', noneOpen], ['a stray open item', stray]]) if (!atRestFaults(parse(h), 3).length) f.push(`"${n}" accepted`);
  arms.push(['PLANTED: the at-rest predicate rejects 2 open, 0 open and a stray item; accepts the good shape', f.length === 0, f.length ? f.join(' | ') : '3 of 3 rejected, good accepted']);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`ONE NEWS ITEM AT REST, THE REST ONE PRESS AWAY: ${pass} of 4 arms`);
process.exit(pass === 4 ? 0 : 1);
