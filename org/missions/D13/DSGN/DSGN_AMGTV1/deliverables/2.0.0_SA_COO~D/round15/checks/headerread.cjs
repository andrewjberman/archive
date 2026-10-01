/**
 * headerread.cjs -- DSGN_AMGTV1 round 15, AV-n-5: THE HEADER READS ITS NUMBERS (PRD FWD-24; shared CONTRACT sections 2-4;
 * batched repair row DSGN_AMGTV1-Z-S9).
 *
 * Usage (repo root): node <this file>
 *   (internal: `--arm1-json` runs arm 1 only and prints one ARM1JSON line; arm 2 spawns it on the base sources)
 * FWD-24: on 3 names the selected-name header shows the chatter and price readings of the latest served trading day the
 * payload carries (the page constructs no date; it renders the served `as_of_date`); the cell labelled "Breakout (price)" reads
 * the BREAKOUT row (never Trending's); every unit prints as served (breakout `*_pct` is already percent, never x100);
 * "places moved" prints wherever served; 0 "not served" / "unsupported" / "ABSENT" / "REFUSED" in visible text for a
 * field the payload carries, beside a positive control (a reading the payload truly lacks renders its designed empty
 * sentence with the served absent_reason in words). Z-S9: an interface code of shape /\b[A-Z]{1,2}-\d+\b/ ("M-1") never
 * reaches visible text; the served reason stays whole in a data- attribute.
 * Fixtures (round15/fixtures, r15c.*; see each file's _capture_note): r15c.overlay.{BA_US,VLO_US,6501_JP}_Equity.json =
 * the round-14 SERVED /overlay captures with axis_reads/chatter/price replaced by issuer-set readings in the CONTRACT
 * shape (axis-read `as_of_date` 2026-09-30 = T-1 of 2026-10-01, axis-read `absent_reason`, row `places_moved`, breakout row
 * `pct_jump_pct` in percent, trending row `return_30d_pct`); distinct Trending vs Breakout values by construction.
 * r15c.thesisBundle.6501_JP_Equity.live.json = the SERVED /thesis capture whose management reason is "no M-1 management
 * object has landed for this name" (unchanged). BA and VLO /thesis: round14/fixtures thesisBundle.*.json (header dossier line).
 * The cell under test is the label's PARENT element ("Trending (chatter)", "Breakout (price)"); the readings' date is read
 * from those two cells plus [data-axis-footnote].
 * Arms:
 *   1  BA, VLO, 6501 headers on the r15c overlays: (a) the served as_of in words ("September 30th, 2026") in the readings and
 *      every long date there is the served day; 0 "today" in the header's visible text; (b) Breakout (price) prints the
 *      breakout row's rank and pct_jump_pct, every percent in it equals the served value at its printed precision, none equals
 *      Trending's return or 100x the served value; Trending (chatter) prints its served rank and score; (c) places moved
 *      prints on every served reading; (d) 0 "not served"/"unsupported"/ABSENT/REFUSED in header visible text; (e) POSITIVE
 *      CONTROL: VLO's chatter reading and 6501's breakout reading are truly absent (row null, absent_reason served) and
 *      render an empty sentence carrying the served reason's words, no number; (f) 6501's Exec (ExecManagementTab on
 *      r15c.thesisBundle.6501_JP_Equity.live.json): 0 /\b[A-Z]{1,2}-\d+\b/ in visible text, the served reason whole in a
 *      data- attribute, "management" and "landed" still read
 *   2  NEGATIVE AT BASE: arm 1 re-run in a child process with every portal/src file that differs from b336b141 replaced by its
 *      b336b141 bytes (`git -C portal show b336b141:<path>` into os.tmpdir(), loaded through _load.cjs CHECK_SRC_OVERRIDE)
 *      FAILS, naming at least the Breakout (price) mislabel and the M-1 code
 *   3  PLANTED: (a) a synthetic correct readings face passes the arm-1 predicate (it CAN pass); its mutants -- breakout x100,
 *      the date replaced by today's, Trending's value under the breakout label, "today's" wording -- are each rejected;
 *      (b) mutant fixtures rendered by the page under test (breakout pct_jump_pct x100; as_of replaced by today's date) are
 *      rejected when graded against the served fixture; (c) the M-1 sentence planted into 6501's Exec face is rejected
 * Prints one line per arm and "THE HEADER READS ITS NUMBERS: <k> of 3 arms"; exit 0 only at 3 of 3.
 * Static renders only; no network, no AWS; writes only under os.tmpdir() (arm 2's base sources).
 * Measured wall time: ~2-4 s (the base child render included).
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const L = require('./_load.cjs');

const T0 = Date.now();
const BASE = 'b336b141';
const SA = 'src/pages/SecurityAnalysis/';
const KEYS = ['BA_US_Equity', 'VLO_US_Equity', '6501_JP_Equity'];
const J6501 = '6501_JP_Equity';
const CHATTER = 'Trending (chatter)';
const BREAKOUT = 'Breakout (price)';
const CODE = /\b[A-Z]{1,2}-\d+\b/;
const CENSUS = /not served|unsupported|\bABSENT\b|\bREFUSED\b/;
const CENSUS_CI = /not served|unsupported/i;
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const LONG_DATE = new RegExp(`\\b(${MONTHS.join('|')}) (\\d{1,2})(?:st|nd|rd|th)?,? (\\d{4})\\b`, 'g');
const clone = (x) => JSON.parse(JSON.stringify(x));
const unwrap = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const unesc = (s) => String(s).replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const text = (html) => unesc(L.textOf(html || ''));

// ---- stubs + fixtures --------------------------------------------------------------------------------------------------------
const api = { __esModule: true, apiRequest: () => Promise.resolve(undefined) };
L.stubSource('src/api/api-client.ts', api);
L.stubSource('src/api/api-client', api);
L.stubSource('@tanstack/react-query', {
  __esModule: true,
  useQuery: () => ({ isLoading: false, isError: false, error: null, data: undefined, refetch: () => {} }),
  useQueryClient: () => ({ invalidateQueries: () => {}, getQueryData: () => undefined }),
});
const overlays = {};
for (const k of KEYS) overlays[k] = unwrap(L.fixture(`r15c.overlay.${k}.json`));
const bundles = {
  BA_US_Equity: unwrap(L.fixture('thesisBundle.BA_US_Equity.json')),
  VLO_US_Equity: unwrap(L.fixture('thesisBundle.VLO_US_Equity.json')),
  [J6501]: unwrap(L.fixture(`r15c.thesisBundle.${J6501}.live.json`)),
};
L.hookState.impl = { useThesisBundle: (k) => bundles[k], usePeerSet: () => undefined, useManagement: (k) => (bundles[k] || {}).management };

const safe = (f) => { try { return f(); } catch (e) { return `<p data-render-failed="1">RENDER FAILED ${String(e.message).split('\n')[0].replace(/</g, '&lt;')}</p>`; } };
const headerOf = (ov) => safe(() => { const m = L.source(SA + 'components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: ov, onBack: () => {}, onRefresh: () => {} }); });
const execOf = (key) => safe(() => L.render(L.source(SA + 'tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: key }));

// ---- element helpers ---------------------------------------------------------------------------------------------------------
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
/** Inner HTML of the element whose opening tag starts at `open`. */
function innerAt(html, open) {
  const tag = /^<([a-zA-Z0-9]+)/.exec(html.slice(open))[1];
  const start = html.indexOf('>', open) + 1;
  let depth = 1;
  const re = new RegExp('<(/?)' + tag + '\\b[^>]*?(/?)>', 'g');
  re.lastIndex = start;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[2] === '/') continue;
    depth += m[1] === '/' ? -1 : 1;
    if (depth === 0) return html.slice(start, m.index);
  }
  return html.slice(start);
}
/** The visible text of the PARENT of the element whose own text is `label`, the label removed; null when not rendered. */
function cellText(html, label) {
  const at = html.indexOf('>' + label + '<');
  if (at < 0) return null;
  const labelOpen = html.lastIndexOf('<', at);
  const stack = [];
  const re = /<(\/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(\/?)>/g;
  let m;
  while ((m = re.exec(html)) !== null && m.index < labelOpen) {
    const tag = m[2].toLowerCase();
    if (m[3] === '/' || VOID.has(tag)) continue;
    if (m[1] === '/') { const i = stack.map((s) => s.tag).lastIndexOf(tag); if (i >= 0) stack.length = i; } else stack.push({ tag, start: m.index });
  }
  if (!stack.length) return null;
  return text(innerAt(html, stack[stack.length - 1].start)).replace(label, '').trim();
}
function footnoteText(html) {
  const at = html.indexOf('data-axis-footnote="');
  return at < 0 ? '' : text(innerAt(html, html.lastIndexOf('<', at)));
}
const longDays = (s) => { const out = []; let m; LONG_DATE.lastIndex = 0; while ((m = LONG_DATE.exec(s)) !== null) out.push(`${m[3]}-${String(MONTHS.indexOf(m[1]) + 1).padStart(2, '0')}-${m[2].padStart(2, '0')}`); return out; };
const dayWords = (iso) => { const [y, mo, d] = iso.split('-').map(Number); return new RegExp(`\\b${MONTHS[mo - 1]} ${d}(?:st|nd|rd|th)?,? ${y}\\b`); };
const percents = (s) => { const out = []; const re = /([-+]?\d+(?:\.(\d+))?)\s*%/g; let m; while ((m = re.exec(s)) !== null) out.push({ v: Number(m[1]), tol: 0.5 * Math.pow(10, -((m[2] || '').length)) + 1e-9, raw: m[0] }); return out; };
const near = (p, v) => Math.abs(Math.abs(p.v) - Math.abs(v)) <= p.tol && (p.v === 0 || v === 0 || Math.sign(p.v) === Math.sign(v) || !/[-+]/.test(p.raw));
const STOP = new Set(['this', 'that', 'with', 'from', 'have', 'there', 'their', 'which', 'were', 'been', 'into', 'than', 'then', 'each', 'among']);
const reasonWords = (r) => Array.from(new Set(String(r || '').toLowerCase().split(/[^a-z]+/).filter((w) => w.length >= 4 && !STOP.has(w))));
const axisRead = (ov, mv, sb) => (ov.axis_reads || []).find((e) => e.movement === mv && e.subject === sb);

/** Arm 1's header predicate: faults of one rendered header against the SERVED overlay `ov`. */
function gradeHeader(name, html, ov) {
  const f = [];
  if (!html || /data-render-failed/.test(html)) return [`${name}: header not rendered (${text(html).slice(0, 90)})`];
  const tc = axisRead(ov, 'TRENDING', 'CHATTER');
  const tp = axisRead(ov, 'TRENDING', 'PRICE');
  const bp = axisRead(ov, 'BREAKOUT', 'PRICE');
  const asOf = (bp && bp.as_of_date) || (tc && tc.as_of_date);
  const all = text(html);
  const cells = [[CHATTER, tc, 'chatter'], [BREAKOUT, bp, 'breakout']];
  const seen = {};
  for (const [label, read, kind] of cells) {
    const t = cellText(html, label);
    seen[label] = t;
    if (t === null) { f.push(`${name}: no cell labelled "${label}"`); continue; }
    const row = read && read.row;
    if (row) {
      if (!t.includes(`#${row.rank}`)) f.push(`${name}: "${label}" does not print the served rank #${row.rank}: "${t.slice(0, 80)}"`);
      if (kind === 'chatter' && !new RegExp(`\\b${Number(row.score).toFixed(0)}\\b`).test(t)) f.push(`${name}: "${label}" does not print the served score ${row.score}: "${t.slice(0, 80)}"`);
      if (kind === 'breakout') {
        const v = row.pct_jump_pct;
        const ps = percents(t);
        const decoy = tp && tp.row ? (tp.row.return_30d_pct ?? tp.row.score) : null;
        if (!ps.length) f.push(`${name}: "${label}" prints no percent (served pct_jump_pct ${v}): "${t.slice(0, 80)}"`);
        for (const p of ps) {
          if (decoy !== null && near(p, decoy) && !near(p, v)) f.push(`${name}: "${label}" reads the Trending value ${p.raw} (Trending return ${decoy}; breakout row pct_jump_pct ${v})`);
          else if (near(p, v * 100) && !near(p, v)) f.push(`${name}: "${label}" prints ${p.raw}, 100x the served pct_jump_pct ${v}`);
          else if (!near(p, v)) f.push(`${name}: "${label}" prints ${p.raw}, not the served pct_jump_pct ${v}`);
        }
      }
      const pm = row.places_moved;
      if (typeof pm === 'number') {
        const ok = pm === 0 ? /\bunchanged\b|\bno change\b|\b0 places?\b|\bdid not move\b/i.test(t) : new RegExp(`(^|[^0-9.])${Math.abs(pm)}\\s+places?\\b`, 'i').test(t);
        if (!ok) f.push(`${name}: "${label}" does not print the served places moved (${pm}): "${t.slice(0, 80)}"`);
      }
    } else {
      // POSITIVE CONTROL: the payload truly lacks this reading -- the designed empty sentence with the served reason in words.
      const words = reasonWords(read && read.absent_reason);
      if (!t) f.push(`${name}: "${label}" (truly absent) renders no empty sentence`);
      else {
        if (/#\d|%/.test(t)) f.push(`${name}: "${label}" (truly absent) prints a number: "${t.slice(0, 80)}"`);
        const missing = words.filter((w) => !t.toLowerCase().includes(w));
        if (!words.length) f.push(`${name}: "${label}" (truly absent) carries no served absent_reason in the fixture`);
        else if (missing.length) f.push(`${name}: "${label}" (truly absent) misses the served reason's words ${missing.join(', ')}: "${t.slice(0, 90)}"`);
      }
    }
  }
  const readings = [seen[CHATTER] || '', seen[BREAKOUT] || '', footnoteText(html)].join(' ');
  if (!asOf) f.push(`${name}: the fixture carries no as_of`);
  else {
    if (!dayWords(asOf).test(readings)) f.push(`${name}: the readings do not show the served day ${asOf} in words: "${readings.slice(0, 120)}"`);
    const wrong = longDays(readings).filter((d) => d !== asOf);
    if (wrong.length) f.push(`${name}: the readings show a day the payload did not serve (${wrong.join(', ')}; served ${asOf})`);
  }
  if (/\btoday\b/i.test(all)) f.push(`${name}: the header says "today": "${(/[^.;:]{0,40}\btoday\b[^.;:]{0,40}/i.exec(all) || [''])[0].trim()}"`);
  const hit = CENSUS.exec(all) || CENSUS_CI.exec(all);
  if (hit) f.push(`${name}: absence word "${hit[0]}" in visible text: "${all.slice(Math.max(0, hit.index - 50), hit.index + 40)}"`);
  return f;
}

/** Arm 1's Exec predicate (Z-S9). */
function gradeExec(html, reason) {
  const f = [];
  if (!html || /data-render-failed/.test(html)) return ['6501 Exec: not rendered'];
  const vis = text(html);
  const code = CODE.exec(vis);
  if (code) f.push(`6501 Exec: interface code "${code[0]}" in visible text: "${vis.slice(Math.max(0, code.index - 60), code.index + 50)}"`);
  const attrs = [];
  const re = /\sdata-[a-z0-9-]+="([^"]*)"/g;
  let m;
  while ((m = re.exec(html)) !== null) attrs.push(unesc(m[1]));
  if (!attrs.includes(reason)) f.push(`6501 Exec: the served reason "${reason}" is not whole in any data- attribute`);
  const at = html.indexOf('data-exec-status="');
  const face = at < 0 ? '' : text(innerAt(html, html.lastIndexOf('<', at)));
  for (const w of ['management', 'landed']) if (!face.toLowerCase().includes(w)) f.push(`6501 Exec: the empty state lost the served word "${w}": "${face.slice(0, 100)}"`);
  return f;
}

const R6501 = bundles[J6501].management.reason || bundles[J6501].management.roster_reason;
function arm1() {
  const faults = [];
  for (const k of KEYS) faults.push(...gradeHeader(k.replace(/_Equity$/, ''), headerOf(overlays[k]), overlays[k]));
  faults.push(...gradeExec(execOf(J6501), R6501));
  return faults;
}

if (process.argv.includes('--arm1-json')) {
  console.log('ARM1JSON ' + JSON.stringify(arm1()));
  process.exit(0);
}

// ---- arm 1 -------------------------------------------------------------------------------------------------------------------
const f1 = arm1();
const a1 = f1.length === 0;
const a1d = a1
  ? '3 of 3 headers read September 30th, 2026 (0 "today"), Breakout (price) = the breakout row (BA 6.65%, VLO 2.31%), places moved on 5 of 5 served readings, 0 absence words; positive control: VLO chatter + 6501 breakout render their served absent_reason in words; 6501 Exec: 0 interface codes, served reason whole in data-'
  : `${f1.length} faults; first: ${f1[0]}${f1[1] ? ' | ' + f1[1] : ''}`;

// ---- arm 2: the same predicate on the b336b141 sources -----------------------------------------------------------------------
const f2 = [];
let a2d = '';
const git = (args) => spawnSync('git', ['-C', L.base, ...args], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
const diff = git(['diff', '--name-only', BASE, '--', 'src']);
if (diff.status !== 0) f2.push(`git diff against ${BASE} failed rc=${diff.status}: ${(diff.stderr || '').trim().slice(0, 120)}`);
const changed = diff.status === 0 ? diff.stdout.split('\n').map((s) => s.trim()).filter((s) => /\.(ts|tsx)$/.test(s)) : [];
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'headerread-base-'));
const pairs = [];
for (const rel of changed) {
  const shown = git(['show', `${BASE}:${rel}`]);
  if (shown.status !== 0) continue; // new since the base: the base sources never import it
  const out = path.join(tmp, rel.replace(/[\\/]/g, '__'));
  fs.writeFileSync(out, shown.stdout);
  pairs.push(`${rel}=${out}`);
}
let baseFaults = null;
if (!f2.length) {
  const env = Object.assign({}, process.env, { CHECK_SRC_OVERRIDE: pairs.join(';') });
  const child = spawnSync(process.execPath, [__filename, '--arm1-json'], { cwd: process.cwd(), env, encoding: 'utf8', timeout: 110000 });
  const line = ((child.stdout || '').split('\n').find((l) => l.startsWith('ARM1JSON ')) || '').slice(9);
  try { baseFaults = JSON.parse(line); } catch (e) { f2.push(`the base child printed no ARM1JSON line (rc=${child.status}): ${(child.stderr || '').trim().slice(0, 160)}`); }
}
try { fs.rmSync(tmp, { recursive: true, force: true }); } catch (e) { /* tmp only */ }
if (baseFaults) {
  const mislabel = baseFaults.filter((x) => x.includes(BREAKOUT) && /Trending value/.test(x));
  const m1 = baseFaults.filter((x) => /"M-1"/.test(x));
  if (baseFaults.length === 0) f2.push('arm 1 PASSES on the base sources (it cannot tell the base from a fix)');
  if (!mislabel.length) f2.push('the base faults do not name the Breakout (price) mislabel');
  if (!m1.length) f2.push('the base faults do not name the M-1 code');
  a2d = `base = the checkout with ${pairs.length} file(s) restored to ${BASE}; arm 1 at base: ${baseFaults.length} faults -- ${mislabel.length} Breakout mislabel (${(mislabel[0] || 'none').slice(0, 110)}), ${m1.length} M-1 code, ${baseFaults.filter((x) => /"today"/.test(x)).length} "today", ${baseFaults.filter((x) => /places moved/.test(x)).length} places moved, ${baseFaults.filter((x) => /in words|show a day/.test(x)).length} date`;
}
const a2 = f2.length === 0;
if (!a2) a2d = `${f2.length} failing; first: ${f2[0]}${a2d ? ' || ' + a2d : ''}`;

// ---- arm 3: planted controls -------------------------------------------------------------------------------------------------
const f3 = [];
const BA = overlays.BA_US_Equity;
const baBp = axisRead(BA, 'BREAKOUT', 'PRICE').row;
const baTp = axisRead(BA, 'TRENDING', 'PRICE').row;
const baTc = axisRead(BA, 'TRENDING', 'CHATTER').row;
const now = new Date();
const TODAY = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
const todayWords = `${MONTHS[now.getMonth()]} ${now.getDate()}th, ${now.getFullYear()}`;
const fmt = (v) => `${v >= 0 ? '+' : ''}${Number(v).toFixed(2)}%`;
const synth = (o) => {
  const s = Object.assign({ chatter: `#${baTc.rank} | ${baTc.score}/100, up ${baTc.places_moved} places`, breakout: `#${baBp.rank} | ${fmt(baBp.pct_jump_pct)}, up ${baBp.places_moved} places`, foot: 'Readings of September 30th, 2026.' }, o);
  return `<div data-synthetic="1"><div class="grid"><div><div>${CHATTER}</div><div>${s.chatter}</div></div><div><div>${BREAKOUT}</div><div>${s.breakout}</div></div></div><div data-axis-footnote="">${s.foot}</div></div>`;
};
const good = gradeHeader('synthetic', synth({}), BA);
if (good.length) f3.push(`the synthetic correct face is rejected (the check cannot pass): ${good[0]}`);
const PLANTS = [
  ['breakout x100', { breakout: `#${baBp.rank} | ${fmt(baBp.pct_jump_pct * 100)}, up ${baBp.places_moved} places` }, /100x/],
  ["today's date", { foot: `Readings of ${todayWords}.` }, /did not serve|in words/],
  ["Trending's value under the breakout label", { breakout: `#${baTp.rank} | ${fmt(baTp.return_30d_pct)}, down 1 place` }, /Trending value/],
  ['"today\'s" wording', { foot: "On today's rankings: September 30th, 2026." }, /"today"/],
  ['places moved dropped', { breakout: `#${baBp.rank} | ${fmt(baBp.pct_jump_pct)}` }, /places moved/],
];
const caught = [];
for (const [label, o, want] of PLANTS) {
  const r = gradeHeader('planted', synth(o), BA);
  if (!r.some((x) => want.test(x))) f3.push(`planted ${label} was NOT rejected for its reason (${r[0] || 'no fault'})`);
  else caught.push(label);
}
const mx = clone(BA);
axisRead(mx, 'BREAKOUT', 'PRICE').row.pct_jump_pct = baBp.pct_jump_pct * 100;
const rx = gradeHeader('BA', headerOf(mx), BA);
if (!rx.some((x) => x.includes(BREAKOUT))) f3.push('the x100 mutant fixture rendered by the page was NOT rejected on the breakout cell');
const md = clone(BA);
for (const e of md.axis_reads) { e.as_of_date = TODAY; if (e.row) { e.row.as_of_date = TODAY; e.row.axis_date = String(e.row.axis_date).replace(/\d{4}-\d{2}-\d{2}/, TODAY); } }
for (const k of ['chatter', 'price']) if (md[k]) { md[k].as_of_date = TODAY; md[k].axis_date = String(md[k].axis_date).replace(/\d{4}-\d{2}-\d{2}/, TODAY); }
const rd = gradeHeader('BA', headerOf(md), BA);
if (TODAY !== '2026-09-30' && !rd.some((x) => /in words|did not serve|"today"/.test(x))) f3.push(`the as_of=${TODAY} mutant fixture rendered by the page was NOT rejected on the date`);
const e6501 = execOf(J6501);
const msgAt = e6501.indexOf('data-stub-text="message">');
let plantedExec = null;
if (msgAt >= 0) {
  const s = msgAt + 'data-stub-text="message">'.length;
  plantedExec = e6501.slice(0, s) + "No officer list is in this name&#x27;s pack yet: no M-1 management object has landed for this name, and no other source was used." + e6501.slice(e6501.indexOf('</span>', s));
}
if (!plantedExec) f3.push('plant: no Exec empty-state message element to plant into');
else if (!gradeExec(plantedExec, R6501).some((x) => /"M-1"/.test(x))) f3.push('the planted M-1 sentence in 6501 Exec was NOT rejected');
const a3 = f3.length === 0;
const a3d = a3
  ? `the synthetic correct face passes; ${caught.length} of ${PLANTS.length} planted faces rejected (${caught.join(', ')}); mutant fixtures (pct_jump_pct x100, as_of=${TODAY}) rendered by the page rejected (${rx.length} / ${rd.length} faults); planted M-1 Exec sentence rejected`
  : `${f3.length} failing; first: ${f3[0]}${f3[1] ? ' | ' + f3[1] : ''}`;

const arms = [
  ['3 headers read the served day, the breakout row, units as served and places moved; 6501 Exec shows no interface code', a1, a1d],
  [`NEGATIVE: arm 1 fails on the ${BASE} sources, naming the Breakout mislabel and M-1`, a2, a2d],
  ['PLANTED: x100, today\'s date, Trending under Breakout and the M-1 sentence are rejected; a correct face passes', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
console.log(`(wall ${((Date.now() - T0) / 1000).toFixed(1)} s)`);
console.log(`THE HEADER READS ITS NUMBERS: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
