/**
 * headerchrome.cjs -- DSGN_AMGTV1 round 16: THE HEADER CHROME MEETS C1 AND C3 (issuer 2.0.0_SA_COO~D).
 *
 * Usage (repo root): cd "$(git rev-parse --show-toplevel)" && node <this file>
 * `portal/` under the working directory is the checkout under test. Optional: --base-dist <dir> (default
 * C:/tmp/dsgn-r15-dist/final, the vite build of portal DEV f4adf790) and --base-render <dir> (default
 * C:/tmp/dsgn-r15-close-render, the round-15 close render of that build by the same instrument, --states-sweep).
 *
 * THE DEFECT (round-15 close render of f4adf790): the selected-name header cards (HeaderCards.tsx) and the Lead Panel
 * header (LeadPanel.tsx) went through the shared card face (GraphicCard.tsx); since then every state reads `sizes` FAIL
 * (PanelEyebrow's 10px eyebrows; DESIGN.md C1 floor 11px) and `lowContrastChars` FAIL (the lilac eyebrow ink graded on
 * the card's white root, because the navy GraphicPanel paints only a background-image); and the four header cards
 * render content-wide (a <button> inside its grid cell does not stretch), uneven, with "MARKET FEATURES" wrapping under
 * its icon.
 *
 * Arms:
 *   1  THE CHECKOUT: vite-build portal/ into os.tmpdir(); run the checkout's own render instrument
 *      (scripts/ui-contract-check.mjs --dist <build> --out <dir> --states-sweep); grades.json must read `sizes` PASS and
 *      `lowContrastChars` PASS in each of the six states (list thesis exec peers model posture; a NOT_EXERCISED or a
 *      missing state is not a PASS). AND the LAYOUT clause, measured in the rendered page (playwright-core + Edge, the
 *      build served from disk through the checkout's scripts/ui-dist.mjs, the API answered from the instrument's own
 *      fixtures, no network beyond the routed localhost origin) on /security-analysis/BA_US_Equity at widths 1440 (the
 *      instrument's) and 1024: exactly 4 `[data-header-card]` elements; their widths equal within 2px; each card fills
 *      its grid cell (card width >= cell width - 2px); in each card the eyebrow (the panel's text element) and the icon
 *      (the panel's svg) have DISJOINT bounding boxes, and the eyebrow is not clipped (scrollWidth <= clientWidth,
 *      scrollHeight <= clientHeight, and its text box lies inside the navy panel's box).
 *   2  NEGATIVE AT BASE: the same predicates on the base build FAIL, each one separately -- sizes (some state), contrast
 *      (some state), equal widths, eyebrow/icon disjoint -- read from the base render's grades.json (equivalent: same
 *      instrument bytes, same build, --states-sweep) and the layout probe run fresh on the base build.
 *   3  CONTROL: /philosophy's card row stays byte-identical -- round15/checks/cardface.cjs run on the checkout reads
 *      "3 of 3 arms" (its arm 1 is the byte-identity of the PhilosophyPillars row through GraphicCard).
 * Writes only under os.tmpdir() (the build, the render). No AWS.
 * Wall time measured on site Z (2026-10-01): base checkout f4adf790 574 s (2 of 3: arm 1 FAILS; arms 2 and 3 are about
 * the base and the control and pass there by design); green C:/tmp/dsgn-r16-green-e (portal ea7b0a9b) 589 s (3 of 3).
 * The build is ~18 s; the instrument run is ~9 of those minutes.
 * Prints one line per arm and "THE HEADER CHROME MEETS C1 AND C3: <k> of 3 arms"; exit 0 only at 3 of 3.
 *
 * Internal: `--probe-only <dist>` prints the layout probe's JSON for one build and exits.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync, execFileSync } = require('child_process');
const { pathToFileURL } = require('url');
const { createRequire } = require('module');

const ROOT = process.cwd();
const PORTAL = path.join(ROOT, 'portal');
const args = process.argv.slice(2);
const opt = (name, dflt) => (args.includes(name) ? args[args.indexOf(name) + 1] : dflt);
const BASE_DIST = opt('--base-dist', 'C:/tmp/dsgn-r15-dist/final');
const BASE_RENDER = opt('--base-render', 'C:/tmp/dsgn-r15-close-render');
const STATES = ['list', 'thesis', 'exec', 'peers', 'model', 'posture'];
const ROUTE = '/security-analysis/BA_US_Equity';
const WIDTHS = [1440, 1024];
const CARDFACE = path.join(__dirname, '..', '..', 'round15', 'checks', 'cardface.cjs');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'; // the instrument's own browser

if (!fs.existsSync(path.join(PORTAL, 'package.json'))) {
  console.log('CHECK ERROR: no portal/package.json under ' + ROOT + ' -- run from the repository root');
  process.exit(3);
}

// ------------------------------------------------------------------ the grades clause -------------------------------------
/** sizes + lowContrastChars per state from a grades.json; ok only when all six states read PASS on both. */
function gradesClause(dir) {
  const f = path.join(dir, 'grades.json');
  if (!fs.existsSync(f)) return { ok: false, sizesFail: null, contrastFail: null, detail: `no grades.json in ${dir}` };
  const g = JSON.parse(fs.readFileSync(f, 'utf8'));
  const parts = [];
  let sizesFail = 0, contrastFail = 0, missing = 0;
  for (const s of STATES) {
    const st = (g.states || {})[s];
    if (!st) { missing += 1; parts.push(`${s} absent`); continue; }
    const sz = st.sizes || {}, lc = st.lowContrastChars || {};
    if (sz.grade !== 'PASS') sizesFail += 1;
    if (lc.grade !== 'PASS') contrastFail += 1;
    const small = sz.value && sz.value.smallest !== undefined ? sz.value.smallest : JSON.stringify(sz.value);
    parts.push(`${s} sizes ${sz.grade || '?'}(smallest ${small}) lowContrast ${lc.grade || '?'}(${JSON.stringify(lc.value)})`);
  }
  return { ok: missing === 0 && sizesFail === 0 && contrastFail === 0, sizesFail, contrastFail, missing, detail: parts.join('; ') };
}

// ------------------------------------------------------------------ the layout probe --------------------------------------
async function probe(dist) {
  const req = createRequire(path.join(PORTAL, 'package.json'));
  const { chromium } = req('playwright-core');
  const { serveFromDist } = await import(pathToFileURL(path.join(PORTAL, 'scripts', 'ui-dist.mjs')).href);
  const fixtures = JSON.parse(fs.readFileSync(path.join(PORTAL, 'src/pages/SecurityAnalysis/__harness__/tests/uiContractFixtures.json'), 'utf8'));
  const fkeys = Object.keys(fixtures).sort((a, b) => b.length - a.length);
  const ORIGIN = 'http://localhost:5175';
  const CORS = { 'Access-Control-Allow-Origin': ORIGIN, 'Access-Control-Allow-Credentials': 'true', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*', 'Content-Type': 'application/json' };
  const SESSION = { accessToken: 'ui-smoke-token', user: { email: 'dev@opalcapital.com', name: 'Dev User', role: 'admin', userType: 'Dev', firmId: 'opal-capital', firmRole: null, advisorId: null, advisorRole: null, mustChangePassword: false } };
  const browser = await chromium.launch(fs.existsSync(EDGE) ? { executablePath: EDGE, headless: true } : { headless: true });
  const out = {};
  try {
    for (const width of WIDTHS) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      await page.route('**/*', async (r) => {
        const rq = r.request();
        const url = rq.url();
        if (rq.method() === 'OPTIONS' && !url.startsWith(ORIGIN)) return r.fulfill({ status: 204, headers: CORS, body: '' });
        const fk = fkeys.find((k) => url.includes(k));
        if (fk) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(fixtures[fk]) });
        if (url.includes('/auth/refresh')) return r.fulfill({ status: 200, headers: CORS, body: JSON.stringify(SESSION) });
        if (await serveFromDist(r, dist, ORIGIN)) return undefined;
        return r.abort('blockedbyclient');
      });
      await page.goto(ORIGIN + ROUTE, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
      await page.waitForSelector('[data-header-card]', { timeout: 15000 }).catch(() => {});
      await page.waitForTimeout(1500);
      out[width] = await page.evaluate(() => {
        const box = (r) => ({ l: r.left, t: r.top, r: r.right, b: r.bottom, w: r.width, h: r.height });
        const cards = Array.from(document.querySelectorAll('[data-header-card]'));
        return {
          loc: location.pathname,
          cards: cards.map((card) => {
            let cell = card;
            while (cell.parentElement && getComputedStyle(cell.parentElement).display !== 'grid') cell = cell.parentElement;
            const panel = Array.from(card.querySelectorAll('*')).find((e) => /gradient/.test(getComputedStyle(e).backgroundImage)) || null;
            const eyebrow = panel ? Array.from(panel.children).find((e) => (e.innerText || '').trim().length > 0) || null : null;
            const icon = panel ? panel.querySelector('svg') : null;
            let text = null;
            if (eyebrow) { const rg = document.createRange(); rg.selectNodeContents(eyebrow); text = box(rg.getBoundingClientRect()); }
            return {
              key: card.getAttribute('data-header-card'),
              card: box(card.getBoundingClientRect()),
              cell: cell.parentElement ? box(cell.getBoundingClientRect()) : null,
              panel: panel ? box(panel.getBoundingClientRect()) : null,
              eyebrowText: eyebrow ? eyebrow.innerText.replace(/\s+/g, ' ').trim() : null,
              eyebrowSize: eyebrow ? getComputedStyle(eyebrow).fontSize : null,
              eyebrowScroll: eyebrow ? { sw: eyebrow.scrollWidth, cw: eyebrow.clientWidth, sh: eyebrow.scrollHeight, ch: eyebrow.clientHeight } : null,
              text,
              icon: icon ? box(icon.getBoundingClientRect()) : null,
            };
          }),
        };
      });
      await page.close();
    }
  } finally {
    await browser.close();
  }
  return out;
}

/** Grade one probe result: { ok, widthsEqual, fill, disjoint, unclipped, detail }. */
function layoutClause(p) {
  const fails = [];
  const notes = [];
  let widthsEqual = true, fill = true, disjoint = true, unclipped = true, four = true;
  for (const width of WIDTHS) {
    const m = p[width];
    if (!m) { fails.push(`${width}: no measurement`); four = false; continue; }
    const cs = m.cards;
    if (cs.length !== 4) { fails.push(`${width}: ${cs.length} [data-header-card] (want 4; at ${m.loc})`); four = false; }
    if (!cs.length) continue;
    const ws = cs.map((c) => c.card.w);
    const spread = Math.max(...ws) - Math.min(...ws);
    if (spread > 2) { widthsEqual = false; fails.push(`${width}: card widths ${ws.map((w) => Math.round(w)).join('/')} (spread ${Math.round(spread)}px > 2)`); }
    for (const c of cs) {
      if (!c.cell || c.card.w < c.cell.w - 2) { fill = false; fails.push(`${width} ${c.key}: card ${Math.round(c.card.w)}px in a ${c.cell ? Math.round(c.cell.w) : '?'}px cell (does not fill)`); }
      if (!c.text || !c.icon || !c.panel) { disjoint = false; unclipped = false; fails.push(`${width} ${c.key}: eyebrow/icon/panel not found`); continue; }
      const a = c.text, b = c.icon;
      const inter = Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t));
      if (inter > 0) { disjoint = false; fails.push(`${width} ${c.key}: eyebrow "${c.eyebrowText}" box overlaps the icon by ${Math.round(inter)}px2`); }
      const s = c.eyebrowScroll;
      const inside = a.l >= c.panel.l - 0.5 && a.r <= c.panel.r + 0.5 && a.t >= c.panel.t - 0.5 && a.b <= c.panel.b + 0.5;
      if (s.sw > s.cw || s.sh > s.ch || !inside) { unclipped = false; fails.push(`${width} ${c.key}: eyebrow clipped (scroll ${s.sw}x${s.sh} vs client ${s.cw}x${s.ch}; text box ${inside ? 'inside' : 'OUTSIDE'} the panel)`); }
    }
    notes.push(`${width}: widths ${ws.map((w) => Math.round(w)).join('/')}, eyebrows ${cs.map((c) => c.eyebrowSize).join('/')}`);
  }
  const ok = fails.length === 0;
  return { ok, four, widthsEqual, fill, disjoint, unclipped, detail: ok ? notes.join('; ') : `${fails.length} failing; first: ${fails[0]} || ${notes.join('; ')}` };
}

// ================================================================== the check =============================================
async function main() {
  if (args.includes('--probe-only')) {
    console.log(JSON.stringify(await probe(path.resolve(opt('--probe-only')))));
    return 0;
  }
  const T0 = Date.now();
  const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'r16-headerchrome-'));
  const head = (() => { try { return execFileSync('git', ['-C', PORTAL, 'rev-parse', '--short', 'HEAD'], { encoding: 'utf8' }).trim(); } catch (e) { return '?'; } })();
  const dirty = (() => { try { return execFileSync('git', ['-C', PORTAL, 'status', '--porcelain', '--', 'src'], { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length; } catch (e) { return '?'; } })();

  // ---------------- arm 1: the checkout ----------------
  const f1 = [];
  let a1d = '';
  const dist = path.join(TMP, 'dist');
  const render = path.join(TMP, 'render');
  const vite = path.join(PORTAL, 'node_modules', 'vite', 'bin', 'vite.js');
  const b = spawnSync(process.execPath, [vite, 'build', '--configLoader', 'runner', '--outDir', dist, '--emptyOutDir'], { cwd: PORTAL, encoding: 'utf8', timeout: 15 * 60 * 1000, maxBuffer: 256 << 20 });
  const tBuild = Math.round((Date.now() - T0) / 1000);
  let G1 = null, L1 = null;
  if (b.status !== 0 || !fs.existsSync(path.join(dist, 'index.html'))) {
    f1.push(`vite build rc=${b.status}: ${String(b.stderr || b.stdout || '').trim().split('\n').slice(-2).join(' ')}`);
  } else {
    const r = spawnSync(process.execPath, ['scripts/ui-contract-check.mjs', '--dist', dist, '--out', render, '--states-sweep'], { cwd: PORTAL, encoding: 'utf8', timeout: 40 * 60 * 1000, maxBuffer: 256 << 20 });
    G1 = gradesClause(render);
    if (!G1.ok) f1.push(`grades (instrument rc=${r.status}): ${G1.sizesFail} state(s) sizes not PASS, ${G1.contrastFail} lowContrastChars not PASS${G1.missing ? `, ${G1.missing} absent` : ''}`);
    try { L1 = layoutClause(await probe(dist)); } catch (e) { L1 = { ok: false, detail: 'probe threw: ' + String(e.message).split('\n')[0] }; }
    if (!L1.ok) f1.push(`layout: ${L1.detail}`);
  }
  const tArm1 = Math.round((Date.now() - T0) / 1000);
  const a1 = f1.length === 0;
  a1d = `${a1 ? '' : `${f1.length} failing; first: ${f1[0]} || `}${G1 ? G1.detail : ''}${L1 && L1.ok ? ' || layout ' + L1.detail : ''}`;

  // ---------------- arm 2: negative at base ----------------
  const f2 = [];
  const n2 = [];
  const G2 = gradesClause(BASE_RENDER);
  if (G2.sizesFail === null) f2.push(`base grades unreadable: ${G2.detail}`);
  else {
    if (G2.sizesFail === 0) f2.push('at base no state reads sizes FAIL -- the sizes clause cannot say no');
    else n2.push(`sizes not PASS in ${G2.sizesFail} of 6`);
    if (G2.contrastFail === 0) f2.push('at base no state reads lowContrastChars FAIL -- the contrast clause cannot say no');
    else n2.push(`lowContrast not PASS in ${G2.contrastFail} of 6`);
  }
  let L2 = null;
  if (!fs.existsSync(path.join(BASE_DIST, 'index.html'))) f2.push(`no base build at ${BASE_DIST}`);
  else {
    try { L2 = layoutClause(await probe(path.resolve(BASE_DIST))); } catch (e) { f2.push('base probe threw: ' + String(e.message).split('\n')[0]); }
    if (L2) {
      if (!L2.four) f2.push('the base page did not show 4 header cards -- the layout clause was not exercised');
      if (L2.widthsEqual) f2.push('at base the card widths read equal -- the width clause cannot say no');
      else n2.push('widths unequal');
      if (L2.disjoint) f2.push('at base every eyebrow reads disjoint from its icon -- the overlap clause cannot say no');
      else n2.push('an eyebrow overlaps its icon');
      n2.push(`fill ${L2.fill ? 'held' : 'failed'}, clip ${L2.unclipped ? 'held' : 'failed'}`);
    }
  }
  const a2 = f2.length === 0;
  const a2d = `${a2 ? '' : `${f2.length} failing; first: ${f2[0]} || `}base ${BASE_RENDER} + ${BASE_DIST}: ${n2.join(', ')}${L2 ? ' || base layout: ' + L2.detail : ''}`;

  // ---------------- arm 3: /philosophy control ----------------
  const f3 = [];
  let a3d = '';
  if (!fs.existsSync(CARDFACE)) f3.push(`no ${CARDFACE}`);
  else {
    const c = spawnSync(process.execPath, [CARDFACE], { cwd: ROOT, encoding: 'utf8', timeout: 5 * 60 * 1000, maxBuffer: 64 << 20 });
    const lines = String(c.stdout || '').trim().split('\n');
    const title = lines.find((l) => /^THE HEADER CARDS ARE THE PHILOSOPHY CARD FACE:/.test(l)) || '(no title line)';
    const arm1 = lines.find((l) => /^ARM (PASS|FAIL) the \/philosophy card row/.test(l)) || '';
    if (c.status !== 0 || !/: 3 of 3 arms$/.test(title)) f3.push(`cardface.cjs rc=${c.status}: ${title}`);
    a3d = `cardface.cjs: ${title}; its arm 1 ${arm1.slice(0, 220)}`;
  }
  const a3 = f3.length === 0;
  const a3dd = a3 ? a3d : `${f3.length} failing; first: ${f3[0]} || ${a3d}`;

  console.log(`RUNS: checkout portal@${head} (${dirty} dirty src paths) built in ${tBuild}s, arm 1 done at ${tArm1}s, under ${TMP}; wall ${Math.round((Date.now() - T0) / 1000)}s`);
  const arms = [
    ['the checkout: sizes and lowContrastChars PASS in all six states; four equal header cards that fill their cells, eyebrows clear of icons and unclipped', a1, a1d],
    ['negative at base: sizes, contrast, equal widths and eyebrow/icon clearance each FAIL', a2, a2d],
    ['control: /philosophy card row byte-identical (cardface.cjs 3 of 3)', a3, a3dd],
  ];
  let pass = 0;
  for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
  console.log(`THE HEADER CHROME MEETS C1 AND C3: ${pass} of ${arms.length} arms`);
  return pass === arms.length ? 0 : 1;
}

main().then((rc) => process.exit(rc), (e) => { console.log('CHECK ERROR: ' + (e && e.stack ? e.stack : e)); process.exit(3); });
