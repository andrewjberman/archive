/**
 * _render36.cjs -- the render child of repairs36.cjs, DSGN_AMGTV1 round 36 (issuer 2.0.0_SA_COO~D). NOT a check: it grades
 * nothing and prints ONE JSON line on stdout. repairs36.cjs spawns it once per mode, because the three renders install different
 * stubs of the same packages (@tanstack/react-query, React.useState) and must not share one process.
 *
 * Usage (cwd = the directory whose portal/ is the checkout under test): node _render36.cjs list|tip|changed
 *   list     round31/checks/presets/_presets.cjs: the REAL LeadPanel with the REAL ChatterBubbles and PriceBars (round29
 *            leadprice/_render.cjs stubs: real Panel/PanelContent/GraphicCard, Segmented recorder, useAuth firm), each window
 *            preset (30/90/365 days) selected through the control's own onChange, on Subject CHATTER and PRICE, over
 *            round31/fixtures/windows.{chatter,price}.{30,90,365}.json. Also returns every portal source file the loader READ
 *            (fs.readFileSync is observed; an override file is mapped back to its portal-relative path).
 *   tip      round29/checks/timeline/_tl.cjs: the REAL TimelinePanel; the recorded Tooltip's `content` element is cloned with
 *            {active, payload: [{payload: <the day's served series entry>}]} and rendered, as round29 timeline/chart.cjs does.
 *            The day read is answered by _tl's query stub: a day absent from the day map is PENDING (isLoading true).
 *   changed  round15/checks/_load.cjs: the REAL tabs/ModelTab.tsx with useThesisBundle / useModelVersions / useModelCompare
 *            answering round35/fixtures/{thesis,versions,compare}.BA_US_Equity.json (round35 changed35.cjs's render path).
 * Honours the loader's CHECK_SRC_OVERRIDE. No network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');

const DROOT = path.join(__dirname, '..', '..', '..');
const R35FX = path.join(DROOT, 'round35', 'fixtures');
const PORTAL = path.join(process.cwd(), 'portal');
const pay = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const readFx = (p) => pay(JSON.parse(fs.readFileSync(p, 'utf8')));
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
const out = (o) => process.stdout.write(JSON.stringify(o) + '\n');

// ---- the source-read log (list mode reports which portal files the render loaded) ------------------------------------------
const OV = {};
for (const pair of (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean)) {
  const i = pair.indexOf('=');
  OV[path.resolve(pair.slice(i + 1)).toLowerCase()] = pair.slice(0, i);
}
const READS = new Set();
const origRead = fs.readFileSync;
fs.readFileSync = function observedRead(p, ...rest) {
  try {
    if (typeof p === 'string') {
      const abs = path.resolve(p);
      const ov = OV[abs.toLowerCase()];
      if (ov) READS.add(ov);
      else {
        const rel = path.relative(PORTAL, abs);
        if (rel && !rel.startsWith('..') && !path.isAbsolute(rel)) {
          const r = rel.split(path.sep).join('/');
          if (r.startsWith('src/')) READS.add(r);
        }
      }
    }
  } catch (e) { /* the log never blocks a read */ }
  return origRead.call(this, p, ...rest);
};

const mode = process.argv[2];

if (mode === 'list') {
  const renders = [];
  let error = null;
  try {
    const P = require(path.join(DROOT, 'round31', 'checks', 'presets', '_presets.cjs'));
    for (const subject of ['CHATTER', 'PRICE']) {
      for (const days of [30, 90, 365]) {
        let html = null;
        let stop = null;
        try {
          const r = P.renderAt(subject, days);
          if (r.at) html = r.at.html;
          else stop = r.stop;
        } catch (e) { stop = 'RENDER FAILED: ' + first(e); }
        renders.push({ name: `${subject} ${days}D`, subject, days, html, stop });
      }
    }
  } catch (e) { error = 'LOAD FAILED: ' + first(e); }
  out({ mode, error, renders, reads: [...READS].sort() });
} else if (mode === 'tip') {
  const cases = [];
  let error = null;
  try {
    const T = require(path.join(DROOT, 'round29', 'checks', 'timeline', '_tl.cjs'));
    const R35 = readFx(path.join(R35FX, 'timeline.BA_US_Equity.json'));
    const R14 = T.FX.rangeBA;
    const D0908 = T.FX.dayBA0908;
    // PLANTED (labelled): the day route's answer for 2026-09-28, strongest first, its first headline unlike any event's.
    const PLANTED_0928 = {
      security_key: R35.security_key, date: '2026-09-28', data_status: 'DENIED', publishers_covered: 0, publishers_covered_codes: [],
      articles: [
        { article_key: 'planted:r36-1', headline: 'PLANTED r36: the strongest headline the day route serves for 2026-09-28', publisher: 'bbg', signal_tier: 'A', mention_count: 12, mention_in_title: true, mention_in_lead: true, published_utc: '2026-09-28T13:00:00+00:00', published_precision: 'instant' },
        { article_key: 'planted:r36-2', headline: 'PLANTED r36: a weaker headline of the same day', publisher: 'sa', signal_tier: 'C', mention_count: 2, mention_in_title: false, mention_in_lead: true, published_utc: '2026-09-28T15:00:00+00:00', published_precision: 'instant' },
      ],
    };
    const SPEC = [
      ['BA 2026-09-28 (round 35 served range), day read PENDING', R35, {}, '2026-09-28', null],
      ['BA 2026-09-29 (round 35 served range), day read PENDING', R35, {}, '2026-09-29', null],
      ['BA 2026-09-08 (round 14 served range), day read PENDING', R14, {}, '2026-09-08', null],
      ['BA 2026-09-08 (round 14 served range), SERVED day read answered', R14, { '2026-09-08': D0908 }, '2026-09-08', D0908],
      ['BA 2026-09-28 (round 35 served range), PLANTED day read answered', R35, { '2026-09-28': PLANTED_0928 }, '2026-09-28', PLANTED_0928],
    ];
    for (const [name, range, days, date, body] of SPEC) {
      const entry = (range.series || []).find((e) => e.date === date);
      const covering = (range.events || []).filter((ev) => ev.first_day <= date && date <= ev.last_day && ev.lead_headline).map((ev) => ev.lead_headline);
      const rec = { name, date, pending: body === null, covering, want: body ? body.articles[0].headline : null, articles: entry ? entry.articles_total : null, html: null, rows: null, stop: null };
      try {
        const s = T.renderPanel(range, days);
        const tip = s.rc.find((c) => c.name === 'Tooltip');
        const c = tip && tip.props.content;
        if (!entry) rec.stop = `the served series carries no ${date}`;
        else if (!c) rec.stop = 'the Tooltip has no content';
        else {
          const tp = { active: true, label: date, coordinate: { x: 0, y: 0 }, payload: [{ payload: entry, value: entry.articles_total, dataKey: 'articles_total', name: 'articles_total' }] };
          const el = T.React.isValidElement(c) ? T.React.cloneElement(c, tp) : typeof c === 'function' ? T.h(c, tp) : null;
          const r = T.renderState(() => el, {});
          rec.html = r.html;
          if (/^RENDER FAILED/.test(r.html)) rec.stop = r.html.slice(0, 160);
          else {
            const tt = T.byAttr(r.tree, 'data-shared-tooltip')[0];
            rec.rows = tt ? T.byAttr(tt, 'data-tt-row').map((x) => {
              const label = x.attrs['data-tt-label'] || '';
              const v = T.visible(x);
              return { label, value: v.startsWith(label) ? v.slice(label.length).replace(/^\s*:\s*/, '') : v };
            }) : null;
          }
        }
      } catch (e) { rec.stop = 'RENDER FAILED: ' + first(e); }
      cases.push(rec);
    }
  } catch (e) { error = 'LOAD FAILED: ' + first(e); }
  out({ mode, error, cases });
} else if (mode === 'changed') {
  let error = null;
  const rows = [];
  const missing = [];
  let served = 0;
  try {
    const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
    const KEY = 'BA_US_Equity';
    const COMPARE = readFx(path.join(R35FX, `compare.${KEY}.json`));
    const THESIS = readFx(path.join(R35FX, `thesis.${KEY}.json`));
    const VERSIONS = readFx(path.join(R35FX, `versions.${KEY}.json`));
    const CHANGED = (COMPARE.compared && COMPARE.compared.changed) || [];
    served = CHANGED.length;
    const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
    L.hookState.data = undefined;
    L.hookState.impl = { useThesisBundle: () => THESIS, useModelVersions: () => VERSIONS, useModelCompare: () => COMPARE, useInputLedger: () => undefined };
    const MT = L.source('src/pages/SecurityAnalysis/tabs/ModelTab.tsx');
    const html = L.render(MT.ModelTab, { securityKey: KEY });
    const inner = L.innerOf(html, 'data-what-changed');
    if (inner === null) throw new Error('no [data-what-changed] panel in the rendered Model tab');
    for (const c of CHANGED) {
      const r = L.innerOf(inner, 'data-what-changed-row', esc(c.figure));
      if (r === null) { missing.push(c.figure); continue; }
      const cell = (k) => { const x = L.innerOf(r, 'data-what-changed-cell', k); return x === null ? null : L.textOf(x); };
      rows.push({ figure: c.figure, mnemonic: c.mnemonic, fiscal_year: c.fiscal_year, from: c.from, to: c.to, before: cell('before'), after: cell('after'), chg: cell('change'), pct: cell('pct') });
    }
  } catch (e) { error = 'RENDER FAILED: ' + first(e); }
  out({ mode, error, served, rows, missing });
} else {
  out({ mode, error: 'unknown mode (list | tip | changed)' });
  process.exitCode = 2;
}
