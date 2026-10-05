/**
 * _render37.cjs -- the render child of repairs37.cjs, DSGN_AMGTV1 round 37 (issuer 2.0.0_SA_COO~D). NOT a check: it grades
 * nothing and prints ONE JSON line on stdout. repairs37.cjs spawns it once per mode, because the collage render installs
 * process-wide stubs (@tanstack/react-query, React.useState numbering) the tab renders must not share.
 *
 * Usage (cwd = the directory whose portal/ is the checkout under test): node _render37.cjs collage|peers|posture
 *   collage  round31/checks/presets/_presets.cjs: the REAL LeadPanel with the REAL ChatterBubbles in window mode, each preset
 *            (30/90/365 days) selected through the control's own onChange, Subject CHATTER -- with _presets' served windows
 *            REPLACED by this round's captures ../../fixtures/chatter.{30,90,365}.json (the collected-chatter route, captured
 *            read-only on the deployed opal-amgt-scoped-api, the same data the 02:54Z walk read drew).
 *   peers    round15/checks/_load.cjs: the REAL tabs/PeersTab.tsx (and cscTable.ts) with usePeerSet / useSecurityOverlay answering
 *            ../../fixtures/{peers,overlay}.<key>.json, for MSFT and AMD as served, plus two LABELLED PLANTS (below).
 *   posture  round15/checks/_load.cjs: every no-call face -- the header (SecurityOverlay.tsx IdentityHeader over the served
 *            /overlay, its useThesisBundle answering the served /thesis; TimelinePanel and HeaderBrief stubbed as round35
 *            payload35.cjs does), the Lead Panel's exported PostureHeaderLine (LeadPanel.tsx; no live page mounts it, so it is
 *            rendered with {posture: <served /thesis posture>, subjectIdentity: <served identity>, readAt: <served /thesis
 *            generated_at>} -- `readAt` is the interface this round pins), and tabs/PostureTab.tsx over the served /thesis and
 *            /peers -- for MSFT and AMD, plus two LABELLED PLANTS per face (below). Returns, per case, the served date it wants
 *            and that date through the page's own dateWords longDate / longStamp.
 * PLANTS (labelled, in this file only; nothing here edits a fixture):
 *   peers  PLANTED ONE CURRENCY: the AMD capture with every member given `currency: "USD"` (the field name the served SUBJECT row
 *          carries; no served member carries it) -- the Price column is then one currency and its summaries must survive.
 *          PLANTED MIXED: the MSFT capture with each member given `currency` by its served `country` (United States USD, Taiwan
 *          TWD, any other KRW) -- the Price column then mixes three stated currencies.
 *   posture NO DATE: the MSFT /thesis with `generated_at` removed and the posture's `as_of` / `posture_read.as_of` null -- the
 *          no-call face must print no date. OWN DATE: the MSFT posture with `posture_read.as_of` "2026-09-30" -- the posture's
 *          own read date is served, so the face must print it (it outranks the bundle's generated_at).
 * Honours the loader's CHECK_SRC_OVERRIDE. No network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');

const DROOT = path.join(__dirname, '..', '..', '..');
const FIX = path.join(__dirname, '..', '..', 'fixtures');
const SA = 'src/pages/SecurityAnalysis/';
const pay = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const readFx = (f) => pay(JSON.parse(fs.readFileSync(path.join(FIX, f), 'utf8')));
const first = (e) => String(e && e.message ? e.message : e).split('\n')[0];
const out = (o) => process.stdout.write(JSON.stringify(o) + '\n');
const clone = (o) => JSON.parse(JSON.stringify(o));
const KEYS = ['MSFT_US_Equity', 'AMD_US_Equity'];

const mode = process.argv[2];

if (mode === 'collage') {
  const renders = [];
  const names = {};
  let error = null;
  try {
    const P = require(path.join(DROOT, 'round31', 'checks', 'presets', '_presets.cjs'));
    for (const d of P.WINDOWS) {
      P.CHATTER[d] = readFx(`chatter.${d}.json`);
      for (const r of P.CHATTER[d].rows) names[r.security_key] = r.display_name;
    }
    for (const days of P.WINDOWS) {
      let html = null;
      let stop = null;
      try {
        const r = P.renderAt('CHATTER', days);
        if (r.at) html = r.at.html;
        else stop = r.stop;
      } catch (e) { stop = 'RENDER FAILED: ' + first(e); }
      renders.push({ name: `${days}D`, days, html, stop, served_rows: P.CHATTER[days].rows.length, window_end: P.CHATTER[days].window_end });
    }
  } catch (e) { error = 'LOAD FAILED: ' + first(e); }
  out({ mode, error, renders, names });
} else if (mode === 'peers') {
  const cases = [];
  let error = null;
  try {
    const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
    const render = (peers, overlay, key) => {
      L.hookState.data = undefined;
      L.hookState.impl = { usePeerSet: () => peers, useSecurityOverlay: () => overlay };
      return L.render(L.source(SA + 'tabs/PeersTab.tsx').PeersTab, { securityKey: key });
    };
    const SPEC = [];
    for (const key of KEYS) SPEC.push([`${key.split('_')[0]} served`, key, readFx(`peers.${key}.json`), readFx(`overlay.${key}.json`), false]);
    {
      const p = clone(readFx('peers.AMD_US_Equity.json'));
      for (const m of p.members || []) m.currency = 'USD';
      SPEC.push(['AMD PLANTED ONE CURRENCY (every member currency "USD")', 'AMD_US_Equity', p, readFx('overlay.AMD_US_Equity.json'), true]);
    }
    {
      const p = clone(readFx('peers.MSFT_US_Equity.json'));
      for (const m of p.members || []) m.currency = m.country === 'United States' ? 'USD' : m.country === 'Taiwan' ? 'TWD' : 'KRW';
      SPEC.push(['MSFT PLANTED MIXED (member currency USD / TWD / KRW by served country)', 'MSFT_US_Equity', p, readFx('overlay.MSFT_US_Equity.json'), true]);
    }
    for (const [name, key, peers, overlay, planted] of SPEC) {
      const rec = { name, key, planted, peers, html: null, stop: null };
      try { rec.html = render(peers, overlay, key); } catch (e) { rec.stop = 'RENDER FAILED: ' + first(e); }
      cases.push(rec);
    }
  } catch (e) { error = 'LOAD FAILED: ' + first(e); }
  out({ mode, error, cases });
} else if (mode === 'posture') {
  const cases = [];
  let error = null;
  try {
    const L = require(path.join(DROOT, 'round15', 'checks', '_load.cjs'));
    const h = L.React.createElement;
    L.stubSource(SA + 'components/TimelinePanel.tsx', { __esModule: true, TimelinePanel: () => h('div', { 'data-check-stub': 'TimelinePanel' }) });
    const realBrief = L.source(SA + 'components/HeaderBrief.tsx');
    L.stubSource(SA + 'components/HeaderBrief.tsx', Object.assign({}, realBrief, { HeaderBrief: () => h('div', { 'data-check-stub': 'HeaderBrief' }) }));
    const D = L.source(SA + 'dateWords.ts');
    const hooks = (thesis, peers) => {
      L.hookState.data = undefined;
      L.hookState.impl = { useThesisBundle: () => thesis, usePeerSet: () => peers, useCollectedChatter: () => undefined, useManagement: () => undefined };
    };
    /** The served date an absent posture carries: its own as_of, else its read's as_of, else the bundle's generated_at. */
    const servedDate = (posture, thesis) => (posture && (posture.as_of || (posture.posture_read && posture.posture_read.as_of))) || (thesis && thesis.generated_at) || null;
    const FACES = {
      header: (ov, th, pe, key) => { hooks(th, pe); const m = L.source(SA + 'components/SecurityOverlay.tsx'); return L.render(m.IdentityHeader || m.SecurityOverlay, { bundle: ov, onBack: () => {}, onRefresh: () => {} }); },
      lead: (ov, th) => { hooks(th, undefined); return L.render(L.source(SA + 'components/LeadPanel.tsx').PostureHeaderLine, { posture: th.posture, subjectIdentity: th.identity, readAt: th.generated_at }); },
      tab: (ov, th, pe, key) => { hooks(th, pe); return L.render(L.source(SA + 'tabs/PostureTab.tsx').PostureTab, { securityKey: key }); },
    };
    const ATTR = { header: ['data-header-posture', 'ABSENT'], lead: ['data-header-posture', 'ABSENT'], tab: ['data-posture-status', 'ABSENT'] };
    const SPEC = [];
    for (const key of KEYS) SPEC.push(['served', key, readFx(`overlay.${key}.json`), readFx(`thesis.${key}.json`), readFx(`peers.${key}.json`)]);
    {
      const ov = clone(readFx('overlay.MSFT_US_Equity.json'));
      const th = clone(readFx('thesis.MSFT_US_Equity.json'));
      delete th.generated_at;
      for (const p of [ov.posture, th.posture]) { p.as_of = null; if (p.posture_read) p.posture_read.as_of = null; }
      SPEC.push(['PLANTED NO DATE', 'MSFT_US_Equity', ov, th, readFx('peers.MSFT_US_Equity.json')]);
    }
    {
      const ov = clone(readFx('overlay.MSFT_US_Equity.json'));
      const th = clone(readFx('thesis.MSFT_US_Equity.json'));
      for (const p of [ov.posture, th.posture]) { if (p.posture_read) p.posture_read.as_of = '2026-09-30'; }
      SPEC.push(['PLANTED OWN DATE', 'MSFT_US_Equity', ov, th, readFx('peers.MSFT_US_Equity.json')]);
    }
    for (const [kind, key, ov, th, pe] of SPEC) {
      for (const face of Object.keys(FACES)) {
        const posture = face === 'header' ? ov.posture : th.posture;
        const want = servedDate(posture, th);
        const rec = { name: `${face} ${key.split('_')[0]} ${kind}`, face, key, kind, status: posture && posture.status, want,
          wantWords: want ? D.longDate(want) : null, wantStamp: want ? D.longStamp(want) : null, line: null, stop: null };
        try {
          const html = FACES[face](ov, th, pe, key);
          const inner = L.innerOf(html, ATTR[face][0], ATTR[face][1]);
          if (inner === null) rec.stop = `no [${ATTR[face][0]}="${ATTR[face][1]}"] element rendered`;
          else rec.line = L.textOf(inner);
        } catch (e) { rec.stop = 'RENDER FAILED: ' + first(e); }
        cases.push(rec);
      }
    }
  } catch (e) { error = 'LOAD FAILED: ' + first(e); }
  out({ mode, error, cases });
} else {
  out({ mode, error: 'unknown mode (collage | peers | posture)' });
  process.exitCode = 2;
}
