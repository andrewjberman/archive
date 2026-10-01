/**
 * bubbles.cjs -- DSGN_AMGTV1 round 15, AV-n-2: CHATTER IS BUBBLES BY MONTH (FWD-21; CONTRACT s.1; rulings: chatter has
 * ONLY bubbles, the List view / line chart / List-Chart toggle removed, Trending only through the demo).
 *
 * ISSUER AMENDMENT (round 15, CONTRACT amendment 2 @5ca1a00f56): arm 1 also requires the denominator line
 *   "<k> of <n> covered names" (k = rows with a count in the month, n = all served rows); the fixture drops zero publishers
 *   and carries 10 covered names with an empty by_month; arm 3 adds the mutant 'nodenom'.
 * Usage (repo root): node <this file>          (portal/ under the cwd is the checkout under test)
 *        node <this file> --grade-only     (internal: prints "GRADE-JSON {...}" for arm 1's predicates and exits; arm 2
 *                                           runs it with the cwd at the extracted base tree)
 *
 * THE CONTRACT the worker builds to (quote it in the task order):
 *   - components/ChatterBubbles.tsx exports `ChatterBubbles`, a pure component (no hook, no fetch) taking
 *     `{ data, month }`: `data` is the CONTRACT s.1 payload exactly ({ as_of, source, months, partial_months, rows:
 *     [{ security_key, display_name, by_month: { 'YYYY-MM': { collected, by_publisher } } }] }), `month` one of data.months.
 *   - The same file exports the month cursor `stepMonth(months, month, step)` (step -1 or +1): it returns the neighbouring
 *     SERVED month in `months`, clamped at both ends (never constructs a date).
 *   - ONE bubble per row whose by_month carries `month`; a row without that month gets NO bubble (never a zero bubble).
 *     A bubble is an SVG <circle> carrying data-bubble="<security_key>", data-collected="<served collected>", and r = the
 *     drawn radius, with AREA proportional to `collected` (r = k * sqrt(collected), one k per render; no minimum-radius
 *     clamp; r printed unrounded or to >= 2 decimals; tolerance 2% on area).
 *   - Every bubbled row's display_name is in the chart's text (an SVG <text> label or a <title>).
 *   - The caption contains "articles collected"; no visible text contains "market chatter".
 *   - When `month` is in partial_months the visible text says "partial" in words; for a complete month it does not.
 *   - LeadPanel on subject CHATTER renders the bubbles for the LATEST served month (data.months' last) and NO list, table,
 *     line chart or view toggle: no recharts LineChart/Line, no data-rank-legend / data-series-ticker, no aria-label
 *     "List view" / "Chart view" / "View", no aria-label "Movement", no data-list-columns / data-row-lead /
 *     data-list-unserved-columns. The monthly read is a hook under pages/SecurityAnalysis/hooks/ (name it
 *     `useCollectedChatter`; this check feeds the fixture to that name and to any hook it does not know).
 *
 * Inputs: round15/fixtures/r15a.collected.chatter.json (CONTRACT s.1 shape: as_of 2026-10-01, months 2026-05..2026-10,
 * partial_months ["2026-10"], 12 rows; 2026-10 bubbles 9 rows, 2026-09 bubbles 11; months absent where nothing was
 * collected); round14/fixtures/rankings.TRENDING_CHATTER.json (the served chatter ranking, fed to the rankings hook so a
 * page that still lists it is caught). Render method: round15/checks/_load.cjs plus the stubs pricebars.cjs sets (lucide
 * icons with aria-label, Segmented with aria-label, panels rendering their actions slot, useAuth).
 * Arms:
 *   1  ChatterBubbles rendered for the latest month (2026-10, partial) and M-1 (2026-09) meets every bubble clause; at least
 *      one bubble's radius differs between the two; stepMonth walks latest -> M-1 -> M-2 and back and clamps at both ends;
 *      LeadPanel (movement TRENDING, subject CHATTER) renders the latest month's bubbles and nothing of the one-form census.
 *   2  NEGATIVE: arm 1's predicates on the BASE page source (portal b336b141, extracted to os.tmpdir() as pricebars.cjs
 *      does) FAIL, with "no ChatterBubbles" and "no bubbles in LeadPanel" among the reasons.
 *   3  PLANTED controls: a reference bubble markup built here passes; mutants are each rejected for their class -- radius
 *      linear in the count (AREA), a zero bubble drawn for a row absent that month (ABSENT), a caption reading "market
 *      chatter" (CAPTION), the partial month unlabelled (PARTIAL).
 * Blind spots: the hook is stubbed, so the route wiring and the one-call-for-every-month read are not graded; the cursor's
 * CONTROLS in LeadPanel are not clicked (only stepMonth is); a static render does not lay out, so overlap/packing and colour
 * are unseen; area proportionality is graded within one month's render, not across months.
 * Writes only under os.tmpdir(). No network, no AWS.
 * Wall time measured on site Z (2026-10-01): base run 1.2 s (base extract cached; a cold extract adds ~2.3 s), green
 * run 0.9 s.
 * Prints one line per arm and "CHATTER IS BUBBLES BY MONTH: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const T0 = Date.now();
const ROOT = process.cwd();
const PIN = 'b336b141';
const LP_PATH = 'src/pages/SecurityAnalysis/components/LeadPanel.tsx';
const CB_PATH = 'src/pages/SecurityAnalysis/components/ChatterBubbles.tsx';
const FIXTURE = 'r15a.collected.chatter.json';

function readFixture(name) {
  const own = path.join(__dirname, '..', 'fixtures', name);
  const r14 = path.join(__dirname, '..', '..', 'round14', 'fixtures', name);
  const x = JSON.parse(fs.readFileSync(fs.existsSync(own) ? own : r14, 'utf8'));
  return x && x.payload && x._capture_note ? x.payload : x;
}
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const unesc = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const count = (html, re) => (html.match(re) || []).length;
const textOf = (html) =>
  html.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/\s+/g, ' ').trim();

const DATA = readFixture(FIXTURE);
const CHATTER_RANKING = readFixture('rankings.TRENDING_CHATTER.json');
const MONTHS = DATA.months;
const LATEST = MONTHS[MONTHS.length - 1];
const M1 = MONTHS[MONTHS.length - 2];
const M2 = MONTHS[MONTHS.length - 3];

// ---------------- the predicates (pure over html) ----------------
function oneFormFaults(html) {
  const f = [];
  const lines = count(html, /data-stub="(?:LineChart|Line)"/g) + count(html, /data-(?:rank-legend|series-ticker)\b/g);
  if (lines) f.push(`LINE: ${lines} line-chart element(s) (recharts LineChart/Line or a RankedChart marker)`);
  const toggles = count(html, /aria-label="(?:List view|Chart view|View)"/g);
  if (toggles) f.push(`TOGGLE: ${toggles} List/Chart view toggle element(s)`);
  const movement = count(html, /aria-label="Movement"/g);
  if (movement) f.push(`MOVEMENT: ${movement} Movement control(s)`);
  const list = count(html, /data-(?:list-columns|row-lead|list-unserved-columns)\b/g);
  if (list) f.push(`LIST: ${list} RankedList table marker(s)`);
  return f;
}

function bubblesIn(html) {
  const out = [];
  const re = /<([a-zA-Z0-9]+)\b([^>]*\sdata-bubble="[^"]*"[^>]*)>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    const attrs = {};
    const ar = /([a-zA-Z_:][-a-zA-Z0-9_:.]*)="([^"]*)"/g;
    let a;
    while ((a = ar.exec(m[2])) !== null) attrs[a[1]] = unesc(a[2]);
    out.push({ tag: m[1], key: attrs['data-bubble'], collected: attrs['data-collected'], r: Number(attrs.r) });
  }
  return out;
}

function bubbleFaults(html, data, month) {
  const f = [];
  const byKey = new Map(data.rows.map((r) => [r.security_key, r]));
  const want = data.rows.filter((r) => r.by_month && r.by_month[month]);
  const bs = bubblesIn(html);
  const keys = bs.map((b) => b.key);
  if (bs.length !== want.length) f.push(`COUNT: ${bs.length} bubbles for ${want.length} rows with ${month}`);
  const dup = keys.filter((k, i) => keys.indexOf(k) !== i);
  if (dup.length) f.push(`COUNT: duplicate bubbles ${dup.slice(0, 3).join(', ')}`);
  const missing = want.map((r) => r.security_key).filter((k) => !keys.includes(k));
  if (missing.length) f.push(`COUNT: no bubble for ${missing.length} row(s) with ${month}, first ${missing.slice(0, 3).join(', ')}`);
  const absent = bs.filter((b) => !(byKey.get(b.key) && byKey.get(b.key).by_month[month]));
  if (absent.length) f.push(`ABSENT: ${absent.length} bubble(s) drawn for a row with nothing collected in ${month}: ${absent.slice(0, 3).map((b) => b.key).join(', ')}`);
  const ks = [];
  for (const b of bs) {
    const row = byKey.get(b.key);
    const served = row && row.by_month[month] ? row.by_month[month].collected : null;
    if (b.tag !== 'circle') f.push(`SHAPE: bubble ${b.key} is a <${b.tag}>, not an SVG <circle>`);
    if (!(Number(b.collected) > 0)) f.push(`ZERO: bubble ${b.key} carries data-collected="${b.collected}"`);
    else if (served !== null && Number(b.collected) !== served) f.push(`VALUE: bubble ${b.key} carries data-collected="${b.collected}" for served ${served}`);
    if (!(b.r > 0)) f.push(`RADIUS: bubble ${b.key} has r="${b.r}"`);
    else if (served) ks.push({ key: b.key, k: (b.r * b.r) / served });
  }
  if (ks.length >= 2) {
    const sortedK = ks.map((x) => x.k).sort((a, b) => a - b);
    const med = sortedK[Math.floor(sortedK.length / 2)];
    const off = ks.filter((x) => Math.abs(x.k / med - 1) > 0.02);
    if (off.length) f.push(`AREA: ${off.length} of ${ks.length} bubbles' area (r^2/collected) off the render's constant by > 2%, first ${off[0].key} at ${((off[0].k / med - 1) * 100).toFixed(1)}%`);
  }
  const text = textOf(html);
  if (!/articles collected/i.test(text)) f.push('CAPTION: no "articles collected" in visible text');
  if (/market chatter/i.test(text)) f.push('CAPTION: visible text reads "market chatter"');
  const partial = (data.partial_months || []).includes(month);
  if (partial && !/\bpartial\b/i.test(text)) f.push(`PARTIAL: ${month} is a partial month and the text does not say so`);
  if (!partial && /\bpartial\b/i.test(text)) f.push(`PARTIAL: ${month} is complete and the text calls it partial`);
  const unnamed = want.filter((r) => !text.includes(r.display_name)).map((r) => r.security_key);
  if (unnamed.length) f.push(`NAME: ${unnamed.length} bubbled row(s) without their display name in the chart text, first ${unnamed[0]}`);
  // Issuer amendment (CONTRACT amendment 2 @5ca1a00f56, CTO msg 27571): the denominator beside the chart.
  const denom = `${want.length} of ${data.rows.length} covered names`;
  if (!text.includes(denom)) f.push(`DENOMINATOR: the text does not print "${denom}" (names with a count in ${month} of all served names)`);
  return f;
}

// ---------------- the renders (arm 1, and arm 2's child) ----------------
let L = null;
function loader() {
  if (L) return L;
  L = require('./_load.cjs');
  const React = L.React;
  const icons = {};
  L.stubSource('lucide-react', new Proxy({}, {
    get(_t, key) {
      if (key === '__esModule') return true;
      if (typeof key !== 'string') return undefined;
      if (!icons[key]) { icons[key] = (p) => React.createElement('svg', { 'data-icon': key, 'aria-label': (p || {})['aria-label'] }); icons[key].displayName = key; }
      return icons[key];
    },
  }));
  const ctl = {};
  const Segmented = (p) => React.createElement('div', { role: 'group', 'data-segmented': '', 'aria-label': p.ariaLabel },
    ...(p.options || []).map((o, i) => React.createElement('button', { key: i, type: 'button', 'data-segment-value': String(o.value) }, o.label)));
  const controls = new Proxy({}, {
    get(_t, key) {
      if (key === '__esModule') return true;
      if (typeof key !== 'string') return undefined;
      if (key === 'Segmented') return Segmented;
      if (!ctl[key]) ctl[key] = (p) => React.createElement('div', { 'data-stub': key, 'aria-label': (p || {}).ariaLabel }, (p || {}).children);
      return ctl[key];
    },
  });
  for (const k of ['src/ui/components/Controls', 'src/ui/components/Controls.tsx', 'src/ui/components/Controls.ts']) L.stubSource(k, controls);
  const pan = {};
  const panels = new Proxy({}, {
    get(_t, key) {
      if (key === '__esModule') return true;
      if (typeof key !== 'string') return undefined;
      if (!pan[key]) {
        pan[key] = (p) => {
          const q = p || {};
          const kids = [];
          for (const s of ['title', 'subtitle', 'eyebrow']) if (typeof q[s] === 'string' && q[s]) kids.push(React.createElement('span', { key: s, 'data-stub-text': s }, q[s]));
          for (const s of ['actions', 'leftContent', 'children', 'footer']) if (q[s] !== undefined && q[s] !== null) kids.push(React.createElement(React.Fragment, { key: s }, q[s]));
          return React.createElement('div', { 'data-stub': key }, ...kids);
        };
      }
      return pan[key];
    },
  });
  for (const k of ['src/ui/components/panels', 'src/ui/components/panels/index.ts', 'src/ui/components/panels/index.tsx']) L.stubSource(k, panels);
  for (const k of ['src/hooks/useAuth', 'src/hooks/useAuth.ts', 'src/hooks/useAuth.tsx']) L.stubSource(k, { useAuth: () => ({ claims: { firmId: 'opal' } }) });
  L.hookState.impl = {
    useLeadPanelRankings: (_movement, subject) => (String(subject).toUpperCase() === 'CHATTER' ? CHATTER_RANKING : undefined),
    useRankTimeSeries: () => undefined,
    useStarredList: () => [],
    useSetStarred: () => undefined,
    useCollectedChatter: () => DATA,
  };
  L.hookState.data = DATA; // any monthly hook under another name reads the same fixture
  return L;
}

function gradeCheckout() {
  const faults = [];
  const info = {};
  let mod = null;
  try {
    mod = loader().source(CB_PATH);
  } catch (e) {
    faults.push(`MISSING: ${CB_PATH} did not load: ${String(e.message).split('\n')[0].slice(0, 120)}`);
  }
  if (mod) {
    const renders = {};
    if (typeof mod.ChatterBubbles !== 'function') faults.push('MISSING: no exported ChatterBubbles component');
    else {
      for (const m of [LATEST, M1]) {
        try {
          renders[m] = loader().render(mod.ChatterBubbles, { data: DATA, month: m });
          for (const x of bubbleFaults(renders[m], DATA, m)) faults.push(`${x.split(':')[0]}: [${m}]${x.slice(x.indexOf(':') + 1)}`);
          info[m] = bubblesIn(renders[m]).length;
        } catch (e) {
          faults.push(`RENDER: ChatterBubbles for ${m} threw: ${String(e.message).split('\n')[0]}`);
        }
      }
      if (renders[LATEST] && renders[M1]) {
        const a = new Map(bubblesIn(renders[LATEST]).map((b) => [b.key, b.r]));
        const changed = bubblesIn(renders[M1]).filter((b) => a.has(b.key) && Math.abs(a.get(b.key) - b.r) > 1e-6 * Math.max(b.r, 1));
        info.changed = changed.length;
        if (!changed.length) faults.push(`STEP: no bubble's size differs between ${LATEST} and ${M1}`);
      }
    }
    if (typeof mod.stepMonth !== 'function') faults.push('CURSOR: no exported stepMonth helper');
    else {
      const cases = [
        [[MONTHS, LATEST, -1], M1], [[MONTHS, M1, -1], M2], [[MONTHS, M2, 1], M1], [[MONTHS, M1, 1], LATEST],
        [[MONTHS, LATEST, 1], LATEST], [[MONTHS, MONTHS[0], -1], MONTHS[0]],
      ];
      for (const [args, want] of cases) {
        let got;
        try { got = mod.stepMonth(...args); } catch (e) { got = 'threw ' + e.message; }
        if (got !== want) faults.push(`CURSOR: stepMonth(months, ${args[1]}, ${args[2]}) = ${got}, want ${want}`);
      }
    }
  }
  try {
    const noop = () => {};
    const { LeadPanel } = loader().source(LP_PATH);
    const html = loader().render(LeadPanel, {
      movement: 'TRENDING', setMovement: noop, subject: 'CHATTER', setSubject: noop, starredOnly: false, setStarredOnly: noop,
      view: 'list', setView: noop, selectedSecurityKey: null, onSelectSecurity: noop, onClearSecuritySelection: noop,
      searchInput: '', setSearchInput: noop,
    });
    info.lead = bubblesIn(html).length;
    for (const x of [...bubbleFaults(html, DATA, LATEST), ...oneFormFaults(html)]) faults.push(`${x.split(':')[0]}: [LeadPanel]${x.slice(x.indexOf(':') + 1)}`);
  } catch (e) {
    faults.push(`RENDER: LeadPanel on CHATTER threw: ${String(e.message).split('\n')[0]}`);
  }
  return { faults, info };
}

if (process.argv.includes('--grade-only')) {
  const g = gradeCheckout();
  console.log('GRADE-JSON ' + JSON.stringify(g));
  process.exit(0);
}

// ---------------- arm 1 ----------------
const g1 = gradeCheckout();
const a1 = g1.faults.length === 0;
const a1d = a1
  ? `${LATEST} (partial): ${g1.info[LATEST]} bubbles, ${M1}: ${g1.info[M1]} bubbles, area ~ collected within 2%, absent months undrawn, captioned "articles collected"; ${g1.info.changed} bubble(s) change size ${LATEST} -> ${M1}; stepMonth 6 of 6; LeadPanel on CHATTER ${g1.info.lead} bubbles, 0 list, 0 line chart, 0 view toggle, 0 Movement control`
  : `${g1.faults.length} faults; ${g1.faults.slice(0, 3).join(' | ')}`;

// ---------------- arm 2: the base tree, graded by this file's child ----------------
function prepareBase() {
  const dir = path.join(os.tmpdir(), `dsgn-r15-base-${PIN}`);
  if (fs.existsSync(path.join(dir, '.complete'))) return { dir, fresh: false };
  const portalGit = path.join(ROOT, 'portal');
  const ls = spawnSync('git', ['-C', portalGit, 'ls-tree', '-r', '-z', PIN, '--', 'src', 'package.json'], { encoding: 'utf8', maxBuffer: 64 << 20 });
  if (ls.status !== 0) throw new Error(`git ls-tree ${PIN} rc=${ls.status}: ${String(ls.stderr).trim()}`);
  const entries = ls.stdout.split('\0').filter(Boolean).map((line) => {
    const tab = line.indexOf('\t');
    const [mode, type, sha] = line.slice(0, tab).split(' ');
    return { mode, type, sha, p: line.slice(tab + 1) };
  }).filter((e) => e.type === 'blob' && e.mode !== '120000');
  if (!entries.some((e) => e.p === LP_PATH)) throw new Error(`${LP_PATH} is not in ${PIN}`);
  const cat = spawnSync('git', ['-C', portalGit, 'cat-file', '--batch'], { input: entries.map((e) => e.sha).join('\n') + '\n', maxBuffer: 512 << 20 });
  if (cat.status !== 0) throw new Error(`git cat-file rc=${cat.status}`);
  const stage = fs.mkdtempSync(path.join(os.tmpdir(), `dsgn-r15-base-${PIN}-stage-`));
  const buf = cat.stdout;
  let off = 0;
  for (const e of entries) {
    const nl = buf.indexOf(10, off);
    const header = buf.slice(off, nl).toString();
    if (/ missing$/.test(header)) throw new Error('object missing: ' + header);
    const size = Number(header.split(' ')[2]);
    const out = path.join(stage, 'portal', e.p);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, buf.slice(nl + 1, nl + 1 + size));
    off = nl + 1 + size + 1;
  }
  fs.symlinkSync(fs.realpathSync(path.join(portalGit, 'node_modules')), path.join(stage, 'portal', 'node_modules'), 'junction');
  fs.writeFileSync(path.join(stage, '.complete'), `portal ${PIN}: ${entries.length} files (src + package.json)\n`);
  try {
    fs.renameSync(stage, dir);
  } catch (e) {
    if (!fs.existsSync(path.join(dir, '.complete'))) throw e; // another check built it first: use theirs
  }
  return { dir, fresh: true };
}
const f2 = [];
let a2d = '';
try {
  const t = Date.now();
  const { dir, fresh } = prepareBase();
  const env = { ...process.env };
  delete env.CHECK_SRC_OVERRIDE;
  const r = spawnSync(process.execPath, [__filename, '--grade-only'], { cwd: dir, encoding: 'utf8', env, timeout: 120000 });
  const line = (r.stdout || '').split(/\r?\n/).find((x) => x.startsWith('GRADE-JSON '));
  if (!line) f2.push(`the base child printed no grade (rc=${r.status}): ${String(r.stderr || r.stdout).trim().split('\n').slice(-1)[0]}`);
  else {
    const g = JSON.parse(line.slice('GRADE-JSON '.length));
    const classes = {};
    for (const x of g.faults) { const c = x.split(':')[0]; classes[c] = (classes[c] || 0) + 1; }
    if (g.faults.length === 0) f2.push('the base page source PASSES arm 1 -- the predicates do not see the defect');
    else {
      if (!g.faults.some((x) => /^MISSING:/.test(x))) f2.push('the base fails, but not on "no ChatterBubbles"');
      if (!g.faults.some((x) => /^COUNT: \[LeadPanel\] 0 bubbles/.test(x) || /^RENDER: LeadPanel/.test(x))) f2.push('the base fails, but not on "no bubbles in LeadPanel"');
    }
    a2d = `base portal ${PIN} (${fresh ? 'extracted' : 'cached'} at ${dir}, ${((Date.now() - t) / 1000).toFixed(1)}s): ${g.faults.length} faults by class ${JSON.stringify(classes)}; first: ${g.faults.slice(0, 4).join(' | ')}`;
  }
} catch (e) {
  f2.push('base extract/grade failed: ' + String(e.message).split('\n')[0]);
}
const a2 = f2.length === 0;
if (!a2) a2d = `${f2[0]}${a2d ? ' || ' + a2d : ''}`;

// ---------------- arm 3: planted controls ----------------
function synth(month, mut) {
  const rows = DATA.rows.filter((r) => r.by_month[month]);
  const max = Math.max(...rows.map((r) => r.by_month[month].collected));
  const partial = DATA.partial_months.includes(month) && mut !== 'unlabelled';
  const caption = mut === 'chatter' ? 'Bubble area = market chatter' : 'Bubble area = articles collected';
  const circles = rows.map((r, i) => {
    const c = r.by_month[month].collected;
    const rad = mut === 'linear' ? (40 * c) / max : 40 * Math.sqrt(c / max);
    return `<circle cx="${50 + i * 90}" cy="60" r="${rad}" data-bubble="${esc(r.security_key)}" data-collected="${c}"><title>${esc(r.display_name)}</title></circle>`;
  });
  if (mut === 'zero') {
    const gone = DATA.rows.find((r) => !r.by_month[month]);
    circles.push(`<circle cx="0" cy="0" r="0" data-bubble="${esc(gone.security_key)}" data-collected="0"><title>${esc(gone.display_name)}</title></circle>`);
  }
  const denom = mut === 'nodenom' ? '' : `<p>${rows.length} of ${DATA.rows.length} covered names have collected articles this period</p>`;
  return `<figure><figcaption>${month}${partial ? ' (partial month)' : ''} -- ${caption}</figcaption><svg>${circles.join('')}</svg>${denom}</figure>`;
}
const f3 = [];
const ctl3 = [...bubbleFaults(synth(LATEST), DATA, LATEST), ...bubbleFaults(synth(M1), DATA, M1)];
if (ctl3.length) f3.push(`the reference markup fails: ${ctl3[0]}`);
const MUTANTS = [['linear', 'AREA', M1], ['zero', 'ABSENT', LATEST], ['chatter', 'CAPTION', M1], ['unlabelled', 'PARTIAL', LATEST], ['nodenom', 'DENOMINATOR', LATEST]];
const caught = [];
for (const [mut, cls, month] of MUTANTS) {
  const fx = bubbleFaults(synth(month, mut), DATA, month);
  if (fx.some((x) => x.startsWith(cls + ':'))) caught.push(`${mut}->${cls}`);
  else f3.push(`mutant ${mut} not rejected as ${cls} (faults: ${fx.slice(0, 2).join(' | ') || 'none'})`);
}
const a3 = f3.length === 0;
const a3d = a3
  ? `reference markup 0 faults on ${LATEST} and ${M1}; ${caught.length} of ${MUTANTS.length} mutants rejected (${caught.join(', ')})`
  : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['ChatterBubbles by month: one bubble per collected row, area ~ count, cursor steps, LeadPanel chatter is bubbles only', a1, a1d],
  [`NEGATIVE: the base page source (portal ${PIN}) fails arm 1 on "no ChatterBubbles" and "no bubbles in LeadPanel"`, a2, a2d],
  ['PLANTED controls: the reference passes; linear radius, zero bubble, "market chatter" and an unlabelled partial month are rejected', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`WALL: ${((Date.now() - T0) / 1000).toFixed(1)}s`);
console.log(`CHATTER IS BUBBLES BY MONTH: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
