/**
 * unavailable.cjs -- DSGN_AMGTV1 round 16, cell g-4: THE CHATTER FACE IS DESIGNED WHEN UNSERVED (CTO round-15 analysis
 * ruling 3; CONTRACT section 4: a designed state, never a raw failure) (issuer 2.0.0_SA_COO~D).
 *
 * THE CONTRACT the worker builds to (quote it in the task order):
 *   LeadPanel on subject CHATTER, when the monthly collected-articles read (`useCollectedChatter`) is NOT SERVED -- the read
 *   FAILED (an HTTP 404 or 500 from apiRequest: `API request failed: 404 Not Found - ...`), or it answered with a payload
 *   that is not the CONTRACT s.1 shape -- shows the estate's designed empty state (`PanelEmpty` from
 *   `@/ui/components/states`) carrying ONE plain-words sentence saying the monthly counts are not available yet (the
 *   sentence names "month" -- monthly / per month -- and says "not available yet" or "not yet available"; it is the
 *   state's only sentence: no detail, no hint, no cause). The face shows NO "Read failure", NO "UNKNOWN", no PanelError, no
 *   status token (ERROR, FAILED, READ_FAILED, ABSENT, HTTP), no HTTP code (404, 500, 503), no text of the read's error, no
 *   raw code (round16/checks/_load.cjs RAW_CLASSES), and NO ranking SourceCaption under it (no data-source-caption, no
 *   data-resolution, no "Source:"). Served (the s.1 shape), the face is the bubbles as round 15 built them.
 *
 * Usage (repo root): node <this file>          (portal/ under the cwd is the checkout under test)
 *        node <this file> --grade-only     (internal: prints "GRADE-JSON {...}" for arm 1's predicates and exits; arm 2 runs
 *                                           it with the cwd at the extracted base tree)
 * Inputs: round15/fixtures/r15a.collected.chatter.json (the served s.1 shape, 22 rows, latest month 2026-10 with 9 names
 * collected); round14/fixtures/rankings.TRENDING_CHATTER.json (the served chatter ranking: fed to the ranking hook, so a
 * face that still prints its SourceCaption is caught, and used as one non-s.1 answer). Render method: round16/checks/
 * _load.cjs (round 15's loader, fixtures round16 -> round15 -> round14) with the stubs round15/checks/bubbles.cjs sets
 * (lucide icons with aria-label, Segmented with aria-label, panels rendering their actions slot, useAuth), and the page's
 * hooks module replaced so each read returns a react-query-shaped result {data, isLoading, isError, error}.
 * Arms:
 *   1  On the checkout, LeadPanel (movement TRENDING, subject CHATTER, not starred) rendered five ways: (a) the read FAILED
 *      404, (a) FAILED 500, (b) answered the ranking payload, (b) answered {}, (b) answered {"message":"Not Found"} -- each
 *      shows the designed unavailable state and nothing of the failure and no SourceCaption; (c) SERVED r15a -- 9 bubbles,
 *      "9 of 22 covered names", the chatter footer, no PanelEmpty, no PanelError.
 *   2  NEGATIVE: arm 1's predicates on the BASE page source (portal f4adf790, extracted to os.tmpdir()) FAIL, with
 *      "Read failure" (READFAIL) and the SourceCaption (CAPTION) among the reasons.
 *   3  PLANTED controls: a reference markup built here passes; each mutant is rejected for its class -- the read failure
 *      words (READFAIL), "UNKNOWN" (UNKNOWN), an HTTP code (CODE), a SourceCaption under the state (CAPTION), a second
 *      sentence (ONE), no sentence (DESIGNED), a PanelError in place of PanelEmpty (STATE); and on the served face, a
 *      bubble short (SERVED).
 * Blind spots: the hooks are stubbed, so the route wiring (the read after RESAPP round 57 deploys the route) is not graded;
 * a static render does not lay out or colour, so the sentence's contrast and placement are unseen; the starred filter on
 * an unserved face is not rendered; "plain words" is graded by token classes, not by a reader.
 * Writes only under os.tmpdir() (the base extract). No network, no AWS.
 * Wall time measured on site Z (2026-10-01): see the WALL line (base extract cached after its first run).
 * Prints one line per arm and "THE CHATTER FACE IS DESIGNED WHEN UNSERVED: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const T0 = Date.now();
const ROOT = process.cwd();
const PIN = 'f4adf790';
const LP_PATH = 'src/pages/SecurityAnalysis/components/LeadPanel.tsx';
const HOOKS = 'src/pages/SecurityAnalysis/hooks/useLeadPanelApi';

function readFixture(name) {
  for (const r of ['round16', 'round15', 'round14']) {
    const f = path.join(__dirname, '..', '..', r, 'fixtures', name);
    if (fs.existsSync(f)) {
      const x = JSON.parse(fs.readFileSync(f, 'utf8'));
      return x && x.payload && x._capture_note ? x.payload : x;
    }
  }
  throw new Error('fixture ' + name + ' not found under round16/15/14 fixtures');
}
const textOf = (html) =>
  html.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/\s+/g, ' ').trim();
const count = (html, re) => (html.match(re) || []).length;
const sentencesOf = (text) => text.split(/(?<=[.!?])\s+/).map((s) => s.trim()).filter((s) => /[a-z]{3}/i.test(s));

const SERVED = readFixture('r15a.collected.chatter.json');
const RANKING = readFixture('rankings.TRENDING_CHATTER.json');
const LATEST = SERVED.months[SERVED.months.length - 1];
const SERVED_K = SERVED.rows.filter((r) => r.by_month[LATEST]).length;

const UNSERVED = [
  { id: 'failed-404', kind: 'FAILED', error: 'API request failed: 404 Not Found - {"message":"Not Found"}' },
  { id: 'failed-500', kind: 'FAILED', error: 'API request failed: 500 Internal Server Error - {"error":"Internal Server Error"}' },
  { id: 'shape-ranking', kind: 'SHAPE', data: RANKING },
  { id: 'shape-empty-object', kind: 'SHAPE', data: {} },
  { id: 'shape-message', kind: 'SHAPE', data: { message: 'Not Found' } },
];

// ---------------- the predicates (pure over html) ----------------
const UNAVAILABLE_RE = /(?=.*\bmonth)(?=.*\b(?:not available yet|not yet available)\b)/i;
const STATUS_RE = /\b(?:ERROR|FAILED|FAILURE|READ_FAILED|ABSENT|NOT_SERVED|UNSERVED|HTTP|NULL|UNDEFINED)\b/;
const CODE_RE = /\b(?:404|500|503)\b|API request failed|Not Found|Internal Server Error/i;

function unservedFaults(html, rawCensus) {
  const f = [];
  const text = textOf(html);
  if (/read failure/i.test(text)) f.push('READFAIL: the face reads "Read failure"');
  if (/\bUNKNOWN\b/.test(text)) f.push('UNKNOWN: the face reads "UNKNOWN"');
  const st = STATUS_RE.exec(text);
  if (st) f.push(`STATUS: a status token "${st[0]}" in the visible text`);
  const code = CODE_RE.exec(text);
  if (code) f.push(`CODE: "${code[0]}" in the visible text`);
  const raw = rawCensus(html);
  if (raw.total) f.push(`RAW: ${raw.total} raw code(s) in the visible text, first ${JSON.stringify([...raw.mnemonic_first, ...raw.machine_word_first, ...raw.storage_path_first, ...raw.long_digits_first].slice(0, 2))}`);
  if (/data-stub="PanelError"/.test(html) || /data-panel-state="error"/.test(html)) f.push('STATE: a PanelError (the error state) on the face');
  const empties = count(html, /data-stub="PanelEmpty"/g);
  const inner = empties ? innerOfStub(html, 'PanelEmpty') : null;
  if (empties !== 1) f.push(`STATE: ${empties} PanelEmpty designed state(s) on the face, want 1`);
  const all = sentencesOf(text).filter((s) => UNAVAILABLE_RE.test(s));
  if (all.length === 0) f.push('DESIGNED: no sentence saying the monthly counts are not available yet');
  else if (all.length > 1) f.push(`ONE: ${all.length} sentences say the counts are not available yet, want one`);
  if (inner !== null) {
    const own = sentencesOf(textOf(inner));
    if (own.length !== 1) f.push(`ONE: the designed state carries ${own.length} sentence(s), want exactly one (${own.slice(0, 3).map((s) => JSON.stringify(s.slice(0, 50))).join(' | ')})`);
    else if (!UNAVAILABLE_RE.test(own[0])) f.push(`DESIGNED: the designed state's sentence ${JSON.stringify(own[0].slice(0, 80))} does not say the monthly counts are not available yet`);
  }
  const cap = count(html, /data-source-caption=/g) + count(html, /data-resolution=/g);
  if (cap) f.push(`CAPTION: ${cap} ranking SourceCaption / resolution element(s) under the state`);
  if (/\bSource:/.test(text)) f.push('CAPTION: "Source:" in the visible text');
  if (count(html, /data-bubble=/g)) f.push('SERVED: bubbles drawn for an unserved read');
  return f;
}

function servedFaults(html, data) {
  const f = [];
  const text = textOf(html);
  const latest = data.months[data.months.length - 1];
  const k = data.rows.filter((r) => r.by_month[latest]).length;
  const n = count(html, /<circle\b[^>]*\bdata-bubble="/g);
  if (n !== k) f.push(`SERVED: ${n} bubble(s) for ${k} names collected in ${latest}`);
  if (!text.includes(`${k} of ${data.rows.length} covered names`)) f.push(`SERVED: no "${k} of ${data.rows.length} covered names" denominator`);
  if (!/data-chatter-footer=/.test(html)) f.push('SERVED: no chatter footer (data-chatter-footer)');
  if (/data-stub="PanelEmpty"|data-stub="PanelError"/.test(html)) f.push('SERVED: a PanelEmpty/PanelError on the served face');
  if (/read failure/i.test(text) || UNAVAILABLE_RE.test(text)) f.push('SERVED: the served face says unavailable or read failure');
  return f;
}

function innerOfStub(html, name) {
  const needle = `data-stub="${name}"`;
  const at = html.indexOf(needle);
  if (at < 0) return null;
  const start = html.indexOf('>', at) + 1;
  const re = /<(\/?)div\b[^>]*?(\/?)>/g;
  re.lastIndex = start;
  let depth = 1;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[2] === '/') continue;
    depth += m[1] === '/' ? -1 : 1;
    if (depth === 0) return html.slice(start, m.index);
  }
  return html.slice(start);
}

// ---------------- the renders (arm 1, and arm 2's child) ----------------
let L = null;
const current = { chatter: null };
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
  // The page's hooks module: each read is a react-query-shaped result. The collected-chatter read is the variant under
  // test; the ranking read answers the served chatter ranking (so a SourceCaption has something to print); the rest idle.
  const q = (data) => ({ data, isLoading: false, isError: false, error: null, refetch: () => {} });
  const hooks = new Proxy({}, {
    get(_t, key) {
      if (key === '__esModule') return true;
      if (typeof key !== 'string') return undefined;
      if (key === 'useCollectedChatter') return () => current.chatter;
      if (key === 'useLeadPanelRankings') return (_m, subject) => q(String(subject).toUpperCase() === 'CHATTER' ? RANKING : undefined);
      if (key === 'useStarredList') return () => q([]);
      return () => q(undefined);
    },
  });
  for (const k of [HOOKS, HOOKS + '.ts', HOOKS + '.tsx']) L.stubSource(k, hooks);
  return L;
}

function renderLead(chatterResult) {
  const noop = () => {};
  current.chatter = chatterResult;
  const { LeadPanel } = loader().source(LP_PATH);
  return loader().render(LeadPanel, {
    movement: 'TRENDING', setMovement: noop, subject: 'CHATTER', setSubject: noop, starredOnly: false, setStarredOnly: noop,
    view: 'list', setView: noop, selectedSecurityKey: null, onSelectSecurity: noop, onClearSecuritySelection: noop,
    searchInput: '', setSearchInput: noop,
  });
}

function gradeCheckout() {
  const faults = [];
  const info = { sentences: {} };
  for (const v of UNSERVED) {
    const result = v.kind === 'FAILED'
      ? { data: undefined, isLoading: false, isError: true, error: new Error(v.error), refetch: () => {} }
      : { data: v.data, isLoading: false, isError: false, error: null, refetch: () => {} };
    try {
      const html = renderLead(result);
      for (const x of unservedFaults(html, loader().rawCensus)) faults.push(`${x.split(':')[0]}: [${v.id}]${x.slice(x.indexOf(':') + 1)}`);
      const inner = innerOfStub(html, 'PanelEmpty');
      info.sentences[v.id] = inner === null ? null : sentencesOf(textOf(inner)).join(' / ');
    } catch (e) {
      faults.push(`RENDER: [${v.id}] LeadPanel on CHATTER threw: ${String(e.message).split('\n')[0]}`);
    }
  }
  try {
    const html = renderLead({ data: SERVED, isLoading: false, isError: false, error: null, refetch: () => {} });
    info.served = count(html, /<circle\b[^>]*\bdata-bubble="/g);
    for (const x of servedFaults(html, SERVED)) faults.push(`${x.split(':')[0]}: [served]${x.slice(x.indexOf(':') + 1)}`);
  } catch (e) {
    faults.push(`RENDER: [served] LeadPanel on CHATTER threw: ${String(e.message).split('\n')[0]}`);
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
const uniq = [...new Set(Object.values(g1.info.sentences))];
const a1d = a1
  ? `${UNSERVED.length} unserved reads (2 FAILED 404/500, 3 non-s.1 shapes) each show one PanelEmpty sentence ${JSON.stringify(uniq.length === 1 ? uniq[0] : uniq)}, 0 failure words, 0 status/code tokens, 0 raw codes, 0 SourceCaption; served: ${g1.info.served} bubbles, "${SERVED_K} of ${SERVED.rows.length} covered names"`
  : `${g1.faults.length} faults; ${g1.faults.slice(0, 4).join(' | ')}`;

// ---------------- arm 2: the base tree, graded by this file's child ----------------
function prepareBase() {
  const dir = path.join(os.tmpdir(), `dsgn-r16g-base-${PIN}`);
  if (fs.existsSync(path.join(dir, '.complete'))) return { dir, fresh: false };
  const portalGit = path.join(ROOT, 'portal');
  const ls = spawnSync('git', ['-C', portalGit, 'ls-tree', '-r', '-z', PIN, '--', 'src', 'scripts', 'package.json'], { encoding: 'utf8', maxBuffer: 64 << 20 });
  if (ls.status !== 0) throw new Error(`git ls-tree ${PIN} rc=${ls.status}: ${String(ls.stderr).trim()}`);
  const entries = ls.stdout.split('\0').filter(Boolean).map((line) => {
    const tab = line.indexOf('\t');
    const [mode, type, sha] = line.slice(0, tab).split(' ');
    return { mode, type, sha, p: line.slice(tab + 1) };
  }).filter((e) => e.type === 'blob' && e.mode !== '120000');
  if (!entries.some((e) => e.p === LP_PATH)) throw new Error(`${LP_PATH} is not in ${PIN}`);
  const cat = spawnSync('git', ['-C', portalGit, 'cat-file', '--batch'], { input: entries.map((e) => e.sha).join('\n') + '\n', maxBuffer: 512 << 20 });
  if (cat.status !== 0) throw new Error(`git cat-file rc=${cat.status}`);
  const stage = fs.mkdtempSync(path.join(os.tmpdir(), `dsgn-r16g-base-${PIN}-stage-`));
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
  fs.writeFileSync(path.join(stage, '.complete'), `portal ${PIN}: ${entries.length} files (src + scripts + package.json)\n`);
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
  // The child reads its fixtures beside this file (readFixture uses __dirname), so the base tree needs only portal/.
  const r = spawnSync(process.execPath, [__filename, '--grade-only'], { cwd: dir, encoding: 'utf8', env, timeout: 120000 });
  const line = (r.stdout || '').split(/\r?\n/).find((x) => x.startsWith('GRADE-JSON '));
  if (!line) f2.push(`the base child printed no grade (rc=${r.status}): ${String(r.stderr || r.stdout).trim().split('\n').slice(-1)[0]}`);
  else {
    const g = JSON.parse(line.slice('GRADE-JSON '.length));
    const classes = {};
    for (const x of g.faults) { const c = x.split(':')[0]; classes[c] = (classes[c] || 0) + 1; }
    if (g.faults.length === 0) f2.push('the base page source PASSES arm 1 -- the predicates do not see the defect');
    else {
      if (!classes.READFAIL) f2.push('the base fails, but not on "Read failure" (READFAIL)');
      if (!classes.CAPTION) f2.push('the base fails, but not on the SourceCaption under the state (CAPTION)');
    }
    a2d = `base portal ${PIN} (${fresh ? 'extracted' : 'cached'} at ${dir}, ${((Date.now() - t) / 1000).toFixed(1)}s): ${g.faults.length} faults by class ${JSON.stringify(classes)}; first: ${g.faults.slice(0, 3).join(' | ')}`;
  }
} catch (e) {
  f2.push('base extract/grade failed: ' + String(e.message).split('\n')[0]);
}
const a2 = f2.length === 0;
if (!a2) a2d = `${f2[0]}${a2d ? ' || ' + a2d : ''}`;

// ---------------- arm 3: planted controls ----------------
const RAW_ZERO = () => ({ total: 0, mnemonic_first: [], machine_word_first: [], storage_path_first: [], long_digits_first: [] });
const census = (html) => (L ? L.rawCensus(html) : RAW_ZERO());
const SENTENCE = 'The monthly counts of articles collected are not available yet.';
function synthUnserved(mut) {
  const state = mut === 'errorstate' ? 'PanelError' : 'PanelEmpty';
  let body = `<span data-stub-text="message">${SENTENCE}</span>`;
  if (mut === 'readfail') body = '<span data-stub-text="message">Read failure -- the monthly counts are not available yet.</span>';
  if (mut === 'unknown') body = `<span data-stub-text="message">${SENTENCE}</span><span data-stub-text="detail">Whether any were collected is UNKNOWN</span>`;
  if (mut === 'code') body = `<span data-stub-text="message">${SENTENCE}</span><span data-stub-text="cause">API request failed: 404 Not Found</span>`;
  if (mut === 'two') body = `<span data-stub-text="message">${SENTENCE}</span><span data-stub-text="detail">Check back after the next harvest.</span>`;
  if (mut === 'none') body = '<span data-stub-text="message">Nothing to draw here.</span>';
  const caption = mut === 'caption' ? '<div data-source-caption="generation">Source: ranked chatter</div>' : '';
  return `<div data-stub="Panel"><div data-panel-header=""><div role="group" aria-label="Subject"><button>Chatter</button><button>Price</button></div></div><div data-stub="PanelContent"><div data-stub="${state}">${body}</div><div class="flex">${caption}</div></div></div>`;
}
function synthServed(mut) {
  const rows = SERVED.rows.filter((r) => r.by_month[LATEST]);
  const shown = mut === 'short' ? rows.slice(1) : rows;
  const circles = shown.map((r, i) => `<circle cx="${i * 40}" cy="40" r="10" data-bubble="${r.security_key}" data-collected="${r.by_month[LATEST].collected}"></circle>`).join('');
  return `<div data-chatter-bubbles=""><svg>${circles}</svg><p data-chatter-denominator="">${rows.length} of ${SERVED.rows.length} covered names have collected articles this period</p></div><p data-chatter-footer="">Articles collected per month, from the harvest.</p>`;
}
const f3 = [];
const ref = [...unservedFaults(synthUnserved(), census), ...servedFaults(synthServed(), SERVED)];
if (ref.length) f3.push(`the reference markup fails: ${ref[0]}`);
const MUTANTS = [
  ['readfail', 'READFAIL'], ['unknown', 'UNKNOWN'], ['code', 'CODE'], ['caption', 'CAPTION'], ['two', 'ONE'], ['none', 'DESIGNED'], ['errorstate', 'STATE'],
];
const caught = [];
for (const [mut, cls] of MUTANTS) {
  const fx = unservedFaults(synthUnserved(mut), census);
  if (fx.some((x) => x.startsWith(cls + ':'))) caught.push(`${mut}->${cls}`);
  else f3.push(`mutant ${mut} not rejected as ${cls} (faults: ${fx.slice(0, 2).join(' | ') || 'none'})`);
}
{
  const fx = servedFaults(synthServed('short'), SERVED);
  if (fx.some((x) => x.startsWith('SERVED:'))) caught.push('short->SERVED');
  else f3.push('mutant short (a bubble missing) not rejected as SERVED');
}
const a3 = f3.length === 0;
const a3d = a3
  ? `reference markup 0 faults (unserved and served); ${caught.length} of ${MUTANTS.length + 1} mutants rejected (${caught.join(', ')})`
  : `${f3.length} failing; first: ${f3[0]}`;

const arms = [
  ['the chatter face, read FAILED (404, 500) or answered a non-s.1 shape, is ONE designed sentence with no failure words and no SourceCaption; served, it is the bubbles', a1, a1d],
  [`NEGATIVE: the base page source (portal ${PIN}) fails arm 1 on "Read failure" and the SourceCaption`, a2, a2d],
  ['PLANTED controls: the reference passes; failure words, UNKNOWN, an HTTP code, a SourceCaption, two sentences, none, a PanelError and a missing bubble are rejected', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`WALL: ${((Date.now() - T0) / 1000).toFixed(1)}s`);
console.log(`THE CHATTER FACE IS DESIGNED WHEN UNSERVED: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
