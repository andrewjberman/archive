/**
 * nolabel.cjs -- DSGN_AMGTV1 round 16, cell 5: NO INTERNAL NAME, THE NAME HEADER IN THE CARD FAMILY (round-15 analysis
 * ruling 5; PRD FWD-23; f-3 PARTIAL) (issuer 2.0.0_SA_COO~D).
 *
 * Usage (repo root): cd "$(git rev-parse --show-toplevel)" && node <this file>
 * `portal/` under the working directory is the checkout under test; the base is portal commit f4adf790 (DEV), read with
 * `git -C portal show f4adf790:<path>` into os.tmpdir().
 *
 * THE CONTRACT THE WORKER BUILDS TO (exact):
 *   - "Lead Panel" (any case, any spacing or hyphen) appears in NO visible text of the four DSGN tabs (ThesisTab, PeersTab,
 *     PostureTab, ExecManagementTab) or of the selected-name header (SecurityOverlay.tsx's IdentityHeader). Each tab with no
 *     security selected still renders ONE empty sentence (its PanelEmpty message) in a person's wording: at least 4 words;
 *     the word "name"; one of the verbs pick / choose / select / open / click / tap; the base sentence's words after "to"
 *     kept in order (e.g. "open its Thesis."); and no internal name (lead panel, security overlay, identity header,
 *     discovery band, security mode, a camelCase or PascalCase identifier, or any _load.cjs RAW_CLASSES hit).
 *   - IdentityHeader's IDENTITY BLOCK (the element holding the name, `identity.display_ticker`) renders through the shared
 *     card face: the GraphicCard export of portal/src/ui/components/graphic/GraphicCard.tsx (the module the Lead Panel
 *     header and the four header cards use). Measured by round15/checks/cardface.cjs's PROBE (the loader wraps every
 *     GraphicCard render in <div data-probe-graphic-card="<n>">), never by an attribute the worker writes: the deepest
 *     element outside every `data-header-card` card whose visible words contain the name has a probe ancestor whose subtree
 *     carries the face marker (the style attribute the checkout's own GraphicPanel renders) and holds NO `data-header-card`
 *     card (the identity block is its own card, not a wrap of the header cards); that probe's visible words contain the
 *     name and the served sector and country words (header_figures GICS_SECTOR_NAME and CNTRY_OF_DOMICILE).
 *   - ISSUER ADDITION (row AMGT_RESAPP-Z-W200-S1): BA's Thesis pillars sentence ([data-dossier-pillars], ThesisTab on
 *     round14 thesisBundle.BA_US_Equity.json, served thesis_pillars_absent.reason "no class A report for this security")
 *     carries the served words "class A report" and NOT the page's "research pack", and the served reason stays whole in a
 *     data- attribute of that element. NOTE: round14 reasonwords.cjs (no "class A" token in visible text) and round15
 *     packwords.cjs (a pack-absent Thesis reason must SAY "no research pack") grade the opposite on this one sentence.
 *   - Comments, __harness__ and __rendercheck__ files are not faces. ModelTab.tsx (AMGT_CORPUS's through the freeze, CTO
 *     msg 27547) is NOT graded: its empty-state line is PRINTED for the issuer to route to its writer.
 *
 * Loader: round15/checks/cardface.cjs's makeLoader (the installed typescript + react-dom/server render the REAL sources of
 * src/pages/**, src/lib/**, src/ui/components/graphic/**; every other src/ module and package is a stub that prints its
 * text props -- a PanelEmpty's `message` -- as visible text). Hooks: useThesisBundle returns round14
 * thesisBundle.BA_US_Equity.json for BA (the header's dossier line), undefined otherwise.
 * Inputs: <cwd>/portal (checkout); portal commit f4adf790 (base); round15/fixtures/r15c.overlay.BA_US_Equity.json (BA's
 * served overlay; fixture lookup round16, then round15, then round14).
 * Arms:
 *   1  THE CHECKOUT: each of the four DSGN tabs with securityKey null renders its empty sentence in a person's wording with
 *      0 "Lead Panel" in its visible text; IdentityHeader on BA's served overlay renders its identity block through
 *      GraphicCard with the name and sector words kept, and 0 "Lead Panel" in its visible text
 *   2  NEGATIVE AT BASE: the arm-1 predicate on the f4adf790 sources FAILS on all five faces, each named (the four tabs on
 *      "Lead Panel"; the identity block not through the card face)
 *   3  PLANTED: (a) the checkout ThesisTab with its empty sentence replaced by one naming the LEAD PANEL is rejected; a
 *      synthetic sentence carrying a PascalCase component name is rejected; a synthetic person's sentence passes;
 *      (b) the checkout IdentityHeader with a GraphicCard module mutant (the navy GraphicPanel replaced by a plain div) is
 *      rejected; a synthetic identity block inside a header card's probe, one outside every probe, and one carrying
 *      "Lead Panel" are each rejected; a synthetic identity block through the face passes
 * Also printed, NOT graded: ModelTab's empty-state line from the checkout (render + source line).
 * Writes only under os.tmpdir() (the base source copies). No network, no AWS.
 * Wall time measured on site Z (2026-10-01): base checkout f4adf790 2.9 s (2 of 3); green C:/tmp/dsgn-r16-green-h
 * (r16-green-h 06d0b70b) 3.6 s (3 of 3).
 * Prints one line per arm and "NO INTERNAL NAME, THE NAME HEADER IN THE CARD FAMILY: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const T0 = Date.now();
const CF = require('../../round15/checks/cardface.cjs');
const { RAW_CLASSES } = require('../../round15/checks/_load.cjs');
const { PORTAL, ROOT, PROBE, MODULE_REL, makeLoader, render, parse, attr, all, ancestors, words, faceMarker, hasMarker, probesOf, workingTree } = CF;

const BASE_REV = 'f4adf790';
const SA = 'src/pages/SecurityAnalysis/';
const OVERLAY_REL = SA + 'components/SecurityOverlay.tsx';
const TABS = [
  ['Thesis', SA + 'tabs/ThesisTab.tsx', 'ThesisTab'],
  ['Peers', SA + 'tabs/PeersTab.tsx', 'PeersTab'],
  ['Posture', SA + 'tabs/PostureTab.tsx', 'PostureTab'],
  ['Exec', SA + 'tabs/ExecManagementTab.tsx', 'ExecManagementTab'],
];
const MODEL = ['Model', SA + 'tabs/ModelTab.tsx', 'ModelTab'];
const LEAD = /lead[\s\u00a0-]*panel/i;
const INTERNAL = /lead[\s\u00a0-]*panel|security[\s-]*overlay|identity[\s-]*header|discovery[\s-]*band|security[\s-]*mode/i;
const IDENT = /\b[a-z]+[A-Z][A-Za-z0-9]*\b|\b[A-Z][a-z]+[A-Z][A-Za-z0-9]*\b/;
const VERB = /\b(pick|choose|select|open|click|tap)\b/i;
const SECTOR_MN = 'GICS_SECTOR_NAME';
const COUNTRY_MN = 'CNTRY_OF_DOMICILE';

if (!fs.existsSync(path.join(PORTAL, 'package.json'))) {
  console.log('CHECK ERROR: no portal/package.json under ' + ROOT + ' -- run from the repository root');
  process.exit(3);
}

// ------------------------------------------------------------------ fixtures + trees ---------------------------------------
const DELIV = path.join(ROOT, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D');
function fixture(name) {
  for (const r of ['round16', 'round15', 'round14']) {
    const f = path.join(DELIV, r, 'fixtures', name);
    if (fs.existsSync(f)) return JSON.parse(fs.readFileSync(f, 'utf8'));
  }
  throw new Error('no fixture ' + name + ' in round16/round15/round14');
}
const unwrap = (x) => (x && x.payload && (x._capture_note || x._capture) ? x.payload : x);
const BA = unwrap(fixture('r15c.overlay.BA_US_Equity.json'));
const BA_THESIS = unwrap(fixture('thesisBundle.BA_US_Equity.json'));
const HOOKS = { useThesisBundle: (k) => (k === 'BA_US_Equity' ? BA_THESIS : undefined), useManagement: () => undefined, usePeerSet: () => undefined };

const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'r16-nolabel-'));
function baseTree() {
  const list = new Set(
    execFileSync('git', ['-C', PORTAL, 'ls-tree', '-r', '--name-only', BASE_REV, '--', 'src'], { encoding: 'utf8', maxBuffer: 256 << 20 })
      .split('\n')
      .filter(Boolean)
  );
  const dir = path.join(TMP, 'base-' + BASE_REV);
  return {
    label: 'base',
    dir,
    read(rel) {
      if (!list.has(rel)) return null;
      const out = path.join(dir, rel);
      if (!fs.existsSync(out)) {
        const text = execFileSync('git', ['-C', PORTAL, 'show', `${BASE_REV}:${rel}`], { encoding: 'utf8', maxBuffer: 64 << 20 });
        fs.mkdirSync(path.dirname(out), { recursive: true });
        fs.writeFileSync(out, text);
      }
      return fs.readFileSync(out, 'utf8');
    },
  };
}
const BASE = baseTree();
const WORK = workingTree();
const tryOr = (fn) => { try { return { v: fn() }; } catch (e) { return { err: String(e && e.message).split('\n')[0] }; } };
const vis = (node) => words(node).join(' ');
const cut = (s, n) => (s.length > n ? s.slice(0, n) + '...' : s);

// ------------------------------------------------------------------ the tab predicate --------------------------------------
function tabHtml(tree, spec, overrides) {
  const ld = makeLoader(tree, { hooks: HOOKS, overrides: overrides || {} });
  const C = ld.load(spec[1])[spec[2]];
  if (typeof C !== 'function') throw new Error(`${spec[2]} is not exported by ${spec[1]}`);
  return render(C, { securityKey: null });
}
/** The empty sentence: the PanelEmpty stub's message (else the stub-printed message anywhere, else all visible text). */
function emptySentence(html) {
  const t = parse(html);
  const empty = all(t, (c) => attr(c, 'data-stub') === 'PanelEmpty')[0];
  const scope = empty || t;
  const msg = all(scope, (c) => attr(c, 'data-stub-text') === 'message')[0];
  return { sentence: vis(msg || scope).trim(), all: vis(t) };
}
const objectWords = (s) => { const i = s.search(/\bto\b/i); return i < 0 ? [] : s.slice(i + 2).trim().split(/\s+/).filter(Boolean); };
function isSubsequence(needle, hay) {
  let i = 0;
  for (const w of hay) if (i < needle.length && w === needle[i]) i += 1;
  return i === needle.length;
}
/** Faults of one tab face; `want` = the base sentence's words after "to". */
function gradeTab(name, html, want) {
  const f = [];
  const { sentence, all: allText } = emptySentence(html);
  const lead = LEAD.exec(allText);
  if (lead) f.push(`${name}: "${lead[0]}" in visible text: "${cut(allText, 110)}"`);
  if (!sentence) { f.push(`${name}: no empty sentence rendered`); return { f, sentence }; }
  const w = sentence.split(/\s+/);
  if (w.length < 4) f.push(`${name}: the empty sentence is ${w.length} words: "${sentence}"`);
  if (!/\bnames?\b/i.test(sentence)) f.push(`${name}: the empty sentence does not say "name": "${sentence}"`);
  if (!VERB.test(sentence)) f.push(`${name}: the empty sentence names no act (pick/choose/select/open/click/tap): "${sentence}"`);
  if (want && want.length && !isSubsequence(want, w)) f.push(`${name}: the base words "${want.join(' ')}" are not kept in order: "${sentence}"`);
  const internal = INTERNAL.exec(sentence) || IDENT.exec(sentence);
  if (internal) f.push(`${name}: internal name "${internal[0]}" in the empty sentence: "${sentence}"`);
  for (const [k, re] of Object.entries(RAW_CLASSES)) {
    const hits = sentence.match(new RegExp(re.source, re.flags)) || [];
    if (hits.length) f.push(`${name}: raw code (${k}) "${hits[0]}" in the empty sentence`);
  }
  return { f, sentence };
}

// ------------------------------------------------------------------ the identity predicate ---------------------------------
function expectedIdentity(ov) {
  const fig = (m) => ((ov.header_figures || []).find((x) => x.mnemonic === m) || {}).value;
  const id = ov.identity || {};
  const name = id.identity_status === 'MEASURED' && id.display_ticker ? id.display_ticker : `UNRESOLVED: ${id.requested}`;
  return { name, sector: typeof fig(SECTOR_MN) === 'string' ? fig(SECTOR_MN) : null, country: typeof fig(COUNTRY_MN) === 'string' ? fig(COUNTRY_MN) : null };
}
function identityRender(tree, overrides) {
  const ld = makeLoader(tree, { probe: true, hooks: HOOKS, overrides: overrides || {} });
  const m = ld.load(OVERLAY_REL);
  const C = m.IdentityHeader || m.SecurityOverlay;
  if (typeof C !== 'function') throw new Error('SecurityOverlay.tsx exports no IdentityHeader');
  const html = render(C, { bundle: BA, onBack: () => {}, onRefresh: () => {} });
  return { html, marker: faceMarker(ld) };
}
const inHeaderCard = (n) => attr(n, 'data-header-card') !== null || ancestors(n).some((a) => attr(a, 'data-header-card') !== null);
/** Faults of one rendered header against the served overlay; `marker` = the checkout's GraphicPanel style. */
function gradeIdentity(name, html, marker, ov) {
  const f = [];
  const exp = expectedIdentity(ov);
  const t = parse(html);
  const allText = vis(t);
  const lead = LEAD.exec(allText);
  if (lead) f.push(`${name}: "${lead[0]}" in the header's visible text`);
  const holders = all(t, (c) => !inHeaderCard(c) && vis(c).includes(exp.name));
  const block = holders.filter((h) => !holders.some((o) => o !== h && ancestors(o).includes(h))).find(Boolean);
  if (!block) { f.push(`${name}: the name "${exp.name}" is not rendered outside the header cards`); return { f, detail: 'no identity block' }; }
  const probe = [block, ...ancestors(block)].find((a) => attr(a, PROBE) !== null) || null;
  if (!probe) { f.push(`${name}: the identity block <${block.tag}> holding "${exp.name}" is not through the card face (no GraphicCard render around it)`); return { f, detail: `block <${block.tag}>, no probe` }; }
  if (!hasMarker(probe, marker)) f.push(`${name}: the identity block's GraphicCard render carries no GraphicPanel face (not through the card face)`);
  if (all(probe, (c) => attr(c, 'data-header-card') !== null).length) f.push(`${name}: the identity block's GraphicCard wraps the header cards (it is not its own card)`);
  const pw = vis(probe);
  for (const [k, v] of [['name', exp.name], ['sector', exp.sector], ['country', exp.country]]) {
    if (v && !pw.includes(v)) f.push(`${name}: the identity card lost the ${k} words "${v}": "${cut(pw, 120)}"`);
  }
  return { f, detail: `identity card probe ${attr(probe, PROBE)} words "${cut(pw, 90)}"` };
}

// ------------------------------------------------------------------ the pillars predicate (issuer addition, row W200-S1) ------
// ISSUER RULING (2.0.0_SA_COO~D, round-16 cut): the pillars clause is NOT graded. "research pack" is the designed worded form of
// the served "class A report" (CTO round-13 analysis ruling 1, k-1 MET at L9: no "class A" token on a face; round-15 packwords);
// since AV-f-5 the Exec sentence agrees with it, so the faces no longer contradict. Row AMGT_RESAPP-Z-W200-S1 is answered with
// this ruling, not a page change. Set PILLARS_GRADED=1 to grade it again.
const PILLARS_GRADED = process.env.PILLARS_GRADED === '1';
const PILLARS_REASON = ((BA_THESIS.dossier_fields || {}).thesis_pillars_absent || {}).reason || '';
const CLASS_A_REPORT = /\bclass[- ]A report\b/i;
const RESEARCH_PACK = /\bresearch[\s-]+pack\b/i;
function pillarsHtml(tree, overrides) {
  const ld = makeLoader(tree, { hooks: HOOKS, overrides: overrides || {} });
  return render(ld.load(TABS[0][1]).ThesisTab, { securityKey: 'BA_US_Equity' });
}
/** Faults of BA's Thesis pillars sentence ([data-dossier-pillars]) against its served reason. */
function gradePillars(name, html, reason) {
  const f = [];
  const el = all(parse(html), (c) => attr(c, 'data-dossier-pillars') !== null)[0];
  if (!el) return { f: [`${name}: no [data-dossier-pillars] sentence rendered`], line: '' };
  const line = vis(el).trim();
  if (!CLASS_A_REPORT.test(line)) f.push(`${name}: the pillars sentence does not carry the served words "class A report" (served "${reason}"): "${line}"`);
  const rp = RESEARCH_PACK.exec(line);
  if (rp) f.push(`${name}: the pillars sentence says "${rp[0]}" (page text; served "${reason}"): "${line}"`);
  const attrs = [];
  const re = /(?:^|\s)data-[a-z0-9-]+="([^"]*)"/g;
  let m;
  while ((m = re.exec(el.attrs)) !== null) attrs.push(m[1].replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&amp;/g, '&'));
  if (!attrs.includes(reason)) f.push(`${name}: the served reason "${reason}" is not whole in a data- attribute of the pillars element`);
  return { f, line };
}

// ------------------------------------------------------------------ arm 1 + arm 2 --------------------------------------------
function gradeTree(tree, wants) {
  const faults = [];
  const lines = [];
  const pr = PILLARS_GRADED ? tryOr(() => pillarsHtml(tree)) : { v: null, err: null, skip: true };
  if (pr.skip) { /* issuer ruling: the pillars clause is not graded (see header) */ }
  else if (pr.err) faults.push(`Pillars: BA Thesis render threw: ${pr.err}`);
  else {
    const g = gradePillars('Pillars', pr.v, PILLARS_REASON);
    faults.push(...g.f);
    lines.push(`Pillars (BA) "${g.line}"`);
  }
  for (const spec of TABS) {
    const r = tryOr(() => tabHtml(tree, spec));
    if (r.err) { faults.push(`${spec[0]}: render threw: ${r.err}`); continue; }
    const g = gradeTab(spec[0], r.v, wants[spec[0]]);
    faults.push(...g.f);
    lines.push(`${spec[0]} "${g.sentence}"`);
  }
  const ir = tryOr(() => identityRender(tree));
  if (ir.err) faults.push(`Identity: render threw: ${ir.err}`);
  else {
    const g = gradeIdentity('Identity', ir.v.html, ir.v.marker, BA);
    faults.push(...g.f);
    lines.push(`Identity: ${g.detail}`);
  }
  return { faults, lines };
}
const wants = {};
const baseSentences = {};
for (const spec of TABS) {
  const r = tryOr(() => emptySentence(tabHtml(BASE, spec)).sentence);
  baseSentences[spec[0]] = r.v || '';
  wants[spec[0]] = objectWords(r.v || '');
}
const G1 = gradeTree(WORK, wants);
const a1 = G1.faults.length === 0;
const a1d = a1 ? G1.lines.join('; ') : `${G1.faults.length} faults; first: ${G1.faults[0]}${G1.faults[1] ? ' | ' + G1.faults[1] : ''}${G1.faults[2] ? ' | ' + G1.faults[2] : ''}`;

const G2 = gradeTree(BASE, wants);
const f2 = [];
const failing = ['Thesis', 'Peers', 'Posture', 'Exec', 'Identity', ...(PILLARS_GRADED ? ['Pillars'] : [])].map((face) => [face, G2.faults.filter((x) => x.startsWith(face + ':'))]);
for (const [face, fx] of failing) if (!fx.length) f2.push(`${face} passes at the base (the predicate cannot tell the base from a fix)`);
const tabsLead = failing.slice(0, 4).filter(([, fx]) => fx.some((x) => /lead/i.test(x) && /visible text/.test(x))).length;
const idNotCard = (failing[4][1] || []).some((x) => /not through the card face/.test(x));
if (tabsLead !== 4) f2.push(`only ${tabsLead} of 4 base tabs fail on "Lead Panel"`);
if (!idNotCard) f2.push('the base identity block does not fail on the card face');
if (PILLARS_GRADED && !(failing[5][1] || []).some((x) => /research pack/.test(x))) f2.push('the base pillars sentence does not fail on "research pack"');
const a2 = f2.length === 0;
const a2names = failing.map(([face, fx]) => `${face} ${fx.length ? 'FAIL (' + cut(fx[0].replace(/^[A-Za-z]+: /, ''), 70) + ')' : 'pass'}`).join('; ');
const a2d = a2 ? `base ${BASE_REV}: ${G2.faults.length} faults over 6 of 6 faces -- ${a2names}` : `${f2.length} failing; first: ${f2[0]} || ${a2names}`;

// ------------------------------------------------------------------ arm 3: planted -------------------------------------------
const f3 = [];
const n3 = [];
// (a) the checkout ThesisTab with its empty sentence replaced by one naming the LEAD PANEL
const thesis = TABS[0];
const workSentence = tryOr(() => emptySentence(tabHtml(WORK, thesis)).sentence);
const thesisSrc = WORK.read(thesis[1]);
const plantSentence = `Pick a name in the LEAD PANEL to ${(wants.Thesis || ['open', 'its', 'Thesis.']).join(' ')}`;
if (workSentence.err || !thesisSrc) f3.push(`(a) no checkout Thesis empty sentence to mutate (${workSentence.err || 'no source'})`);
else {
  const lit = workSentence.v;
  let mutantHtml = null;
  let how = '';
  if (lit && thesisSrc.includes(lit)) {
    const r = tryOr(() => tabHtml(WORK, thesis, { [thesis[1]]: thesisSrc.split(lit).join(plantSentence) }));
    if (r.err) f3.push(`(a) the source mutant threw: ${r.err}`);
    else { mutantHtml = r.v; how = 'source mutant'; }
  } else {
    const r = tryOr(() => tabHtml(WORK, thesis));
    if (!r.err) { mutantHtml = r.v.replace('data-stub-text="message">', 'data-stub-text="message">' + plantSentence + ' '); how = 'markup plant (sentence not a source literal)'; }
  }
  if (mutantHtml !== null) {
    const g = gradeTab('Thesis', mutantHtml, wants.Thesis);
    if (!g.f.some((x) => /lead/i.test(x))) f3.push(`(a) the LEAD PANEL mutant was NOT rejected (${g.f[0] || 'no fault'})`);
    else n3.push(`(a) ${how} "${plantSentence}" rejected`);
  }
}
const synth = (s) => `<div data-stub="Panel"><div data-stub="PanelEmpty"><span data-stub-text="message">${s}</span></div></div>`;
const want = wants.Thesis.length ? wants.Thesis : ['open', 'its', 'Thesis.'];
const pascal = gradeTab('Thesis', synth(`Pick a name in the PriceBars to ${want.join(' ')}`), want);
if (!pascal.f.some((x) => /internal name/.test(x))) f3.push(`(a) a PascalCase component name was NOT rejected (${pascal.f[0] || 'no fault'})`);
else n3.push('(a) "PriceBars" sentence rejected');
const good = gradeTab('Thesis', synth(`Pick a name above to ${want.join(' ')}`), want);
if (good.f.length) f3.push(`(a) a synthetic person's sentence is rejected (the tab predicate cannot pass): ${good.f[0]}`);
else n3.push(`(a) "Pick a name above to ${want.join(' ')}" passes`);

// (b) identity: a GraphicCard module mutant without the navy face, and synthetic blocks
const modText = WORK.read(MODULE_REL);
const realMarker = tryOr(() => identityRender(WORK).marker);
if (!modText) f3.push(`(b) no ${MODULE_REL} in the checkout to mutate`);
else if (!/<GraphicPanel\b/.test(modText)) f3.push(`(b) ${MODULE_REL} renders no <GraphicPanel> to replace`);
else {
  const mutant = modText.replace(/<GraphicPanel\b/g, '<div data-r16h-mutant=""').replace(/<\/GraphicPanel>/g, '</div>');
  const r = tryOr(() => identityRender(WORK, { [MODULE_REL]: mutant }));
  if (r.err) f3.push(`(b) the face mutant threw: ${r.err}`);
  else {
    const g = gradeIdentity('Identity', r.v.html, realMarker.v, BA);
    if (!g.f.some((x) => /not through the card face/.test(x))) f3.push(`(b) the GraphicCard face mutant was NOT rejected (${g.f[0] || 'no fault'})`);
    else n3.push('(b) face mutant (GraphicPanel -> div) rejected');
  }
}
const exp = expectedIdentity(BA);
const mk = realMarker.v || 'background-image:url(x)';
const idBody = `<span>${exp.name}</span><div>${[exp.sector, exp.country].filter(Boolean).join(' -- ')}</div>`;
const face = (inner) => `<div ${PROBE}="1"><div><div style="${mk.replace(/"/g, '&quot;')}"></div><div>${inner}</div></div></div>`;
const cards = `<div data-header-card="price"><div ${PROBE}="9"><div><div style="${mk.replace(/"/g, '&quot;')}"></div><div>Price</div></div></div></div>`;
const SYN = [
  ['inside a header card', `<div>${cards.replace('<div>Price</div>', '<div>' + idBody + '</div>')}</div>`, /not rendered outside|not through|wraps/],
  ['outside every probe', `<div><div>${idBody}</div>${cards}</div>`, /not through the card face/],
  ['carrying "Lead Panel"', `<div>${face(idBody + '<p>From the Lead Panel</p>')}${cards}</div>`, /Lead Panel/],
  ['wrapping the header cards', `<div>${face(idBody + cards)}</div>`, /wraps the header cards/],
];
for (const [label, html, re] of SYN) {
  const g = gradeIdentity('Identity', html, mk, BA);
  if (!g.f.some((x) => re.test(x))) f3.push(`(b) a synthetic identity block ${label} was NOT rejected (${g.f[0] || 'no fault'})`);
  else n3.push(`(b) synthetic ${label} rejected`);
}
const goodId = gradeIdentity('Identity', `<div>${face(idBody)}${cards}</div>`, mk, BA);
if (goodId.f.length) f3.push(`(b) a synthetic identity block through the face is rejected (the predicate cannot pass): ${goodId.f[0]}`);
else n3.push('(b) synthetic block through the face passes');
// (c) pillars: the base wording, a dropped attribute and a correct sentence, each spliced into a synthetic element
const pel = (txt, attrv) => `<div><p data-dossier-pillars="ABSENT"${attrv === null ? '' : ` data-dossier-reason="${attrv}"`}>${txt}</p></div>`;
const PS = [
  ['the base "research pack" wording', pel("The research team's thesis pillars: no research pack for this security.", PILLARS_REASON), /class A report|research pack/],
  ['"class A report" beside "research pack"', pel("The research team's thesis pillars: no class A report (research pack) for this security.", PILLARS_REASON), /research pack/],
  ['the served reason dropped from the attribute', pel("The research team's thesis pillars: no class A report for this security.", null), /not whole/],
];
for (const [label, html, re] of (PILLARS_GRADED ? PS : [])) {
  const g = gradePillars('Pillars', html, PILLARS_REASON);
  if (!g.f.some((x) => re.test(x))) f3.push(`(c) pillars ${label} was NOT rejected (${g.f[0] || 'no fault'})`);
  else n3.push(`(c) pillars ${label} rejected`);
}
const goodP = PILLARS_GRADED ? gradePillars('Pillars', pel("The research team's thesis pillars: no class A report for this security.", PILLARS_REASON), PILLARS_REASON) : { f: [] };
if (!PILLARS_GRADED) n3.push('(c) pillars not graded (issuer ruling)');
else if (goodP.f.length) f3.push(`(c) a correct pillars sentence is rejected: ${goodP.f[0]}`);
else n3.push('(c) "no class A report for this security" passes');
const a3 = f3.length === 0;
const a3d = a3 ? n3.join('; '): `${f3.length} failing; first: ${f3[0]}${f3[1] ? ' | ' + f3[1] : ''}`;

// ------------------------------------------------------------------ ModelTab (not graded) -------------------------------------
const mr = tryOr(() => emptySentence(tabHtml(WORK, MODEL)));
const modelSrc = WORK.read(MODEL[1]) || '';
const srcLines = modelSrc.split('\n').map((l, i) => [i + 1, l]).filter(([, l]) => /lead[\s-]+panel/i.test(l) && !/^\s*(\*|\/\/|\/\*)/.test(l));
console.log(`NOT GRADED (ModelTab, AMGT_CORPUS's file): render ${mr.err ? 'threw: ' + mr.err : `"${cut(mr.v.all, 160)}"`}; source ${srcLines.length ? srcLines.map(([n, l]) => `ModelTab.tsx:${n}: ${l.trim()}`).join(' | ') : '0 non-comment "Lead Panel" lines'}`);

console.log(`RUNS: base ${BASE_REV} sources in ${BASE.dir}; base empty sentences: ${TABS.map((s) => `${s[0]} "${baseSentences[s[0]]}"`).join('; ')}`);
const arms = [
  ['the four DSGN tabs say a person\'s empty sentence with 0 "Lead Panel"; the identity block is through GraphicCard, name and sector kept', a1, a1d],
  [`NEGATIVE: the predicate fails on the ${BASE_REV} sources, every face named`, a2, a2d],
  ['PLANTED: a LEAD PANEL mutant, a component name and an identity block off the card face are rejected; correct faces pass', a3, a3d],
];
let pass = 0;
for (const [name, ok, detail] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`); }
try { fs.rmSync(TMP, { recursive: true, force: true }); } catch (e) { /* tmp only */ }
console.log(`(wall ${((Date.now() - T0) / 1000).toFixed(1)} s)`);
console.log(`NO INTERNAL NAME, THE NAME HEADER IN THE CARD FAMILY: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
