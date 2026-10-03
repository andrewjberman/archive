/**
 * peersmenu.cjs -- DSGN_AMGTV1 round 29, AV-zg-6 TABS + ACCOUNT MENU (issuer 2.0.0_SA_COO~D): PEERS MONEY READS ONE WAY WITH ITS
 * DATE, AND THE ACCOUNT MENU LETS GO.
 *
 * Usage (from the directory whose portal/ is the checkout under test, e.g. C:/tmp/wk-dsgn-amgtv1-70):
 *   node <this file>
 * Grades PRD v0.10 FWD-27 (DSGN_AMGTV1_PRD.md ~387-402): "one money format"; "every figure with its as-of date"; "no two
 * figures for one thing disagree without a label naming each measure and window"; "Escape closes the account menu".
 * Register rows (docs/briefs/amgt-security-analysis-ui-findings-20261002.json) and decomposition v29 issuer ruling (a):
 *   SAUX-33  "Every money figure on the page uses one format." Ruling (a): `<served currency code> <figure>` (e.g. "USD 196.80"),
 *            never a `$` sign. In the Peers table a figure carries the served code in ITS OWN CELL ("USD 196.80") or in ITS
 *            COLUMN HEAD ("Mkt Cap (USD mm)"); a figure with neither has no currency on the face.
 *   SAUX-34  "Each market-cap figure prints its as-of date beside it" -- the Peers subject market cap (159,623 in USD mm,
 *            served at subject.market_cap_vintage 2026-09-19T07:53:20Z) against the header's USD 156B.
 *   SAUX-35  "Escape closes the account menu, and with the menu open a click on a tab still switches the tab."
 * Inputs: round14/fixtures/peers.BA_US_Equity.json (the served /peers payload, captured 20260930T130033Z) and
 *   round15/fixtures/r15c.overlay.BA_US_Equity.json (the served overlay: header_figures PX_LAST / CURR_ENTP_VAL in USD).
 * Served currency per cell: subject Price -> overlay PX_LAST.currency; subject EV -> overlay CURR_ENTP_VAL.currency; subject Mkt
 *   Cap -> peers.subject.cap_currency (else .currency); member Mkt Cap -> member.cap_currency. A member's price and EV carry
 *   no served currency field and are not graded for a code (only for `$`).
 * THE MENU IS GRADED ON THE SOURCE (a static render cannot press Escape or hit-test a click). The account menu is the JSX
 *   subtree of portal/src/App.tsx that holds the text "Log Out". ESCAPE passes when that subtree sits inside a Headless UI
 *   Menu / MenuItems / Popover / PopoverPanel (closes on Escape natively), or when a key handler wired by addEventListener
 *   ('keydown'|'keyup') or onKeyDown/onKeyUp compares the key to 'Escape' and calls the setter of the menu's own open state with
 *   false. TAB CLICK passes when, while the menu is open, nothing in that subtree covers the page (no element whose className
 *   carries inset-0, top-0+right-0+bottom-0+left-0, or h-screen+w-screen, or whose style sets inset 0, unless it also
 *   carries pointer-events-none), and no Headless UI MenuItems is modal (Headless UI 2.2.9 MenuItems defaults modal=true,
 *   which makes the rest of the page inert) and no Dialog holds it. LEFT TO A LIVE CHECK: that the keypress really reaches
 *   the handler with focus anywhere on the page, and that a real click on a Security Analysis tab switches the tab with the
 *   menu open.
 * Arms:
 *   1  MONEY (SAUX-33): no `$` on the Peers face; every subject money cell and every member market-cap cell shows its served
 *      currency code in the cell or the column head.
 *   2  CAP AS-OF (SAUX-34): inside the subject row's Mkt Cap cell, an element carrying data-peers-cap-as-of="<served subject
 *      cap vintage, verbatim>" prints that date in words (month name, day, year, the ET calendar day).
 *   3  MENU (SAUX-35): App.tsx's account menu closes on Escape and lays no page-covering layer while open.
 *   4  PLANTED: each of the three predicates rejects known-bad inputs and accepts known-good ones.
 * Prints one line per arm and "PEERS MONEY READS ONE WAY WITH ITS DATE, AND THE ACCOUNT MENU LETS GO: <k> of 4 arms"; exit 0
 * only at 4 of 4. No network, no AWS, writes no file.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const D = path.join(__dirname, '..', '..', '..');
const L = require(path.join(D, 'round15', 'checks', '_load.cjs'));
const ts = require('module').createRequire(path.join(L.base, 'package.json'))('typescript');
const load = (p) => { const d = JSON.parse(fs.readFileSync(p, 'utf8')); return d && d.payload ? d.payload : d; };
const PEERS = load(path.join(D, 'round14', 'fixtures', 'peers.BA_US_Equity.json'));
const OVERLAY = load(path.join(D, 'round15', 'fixtures', 'r15c.overlay.BA_US_Equity.json'));
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const MONEY_CODES = ['price', 'mkt_val_sec', 'ev'];

/** Honours the loader's ISSUER GREEN ARM override (CHECK_SRC_OVERRIDE) so a scratch reference proves an arm CAN pass. */
function srcFile(rel) {
  const over = (process.env.CHECK_SRC_OVERRIDE || '').split(';').filter(Boolean).map((p) => [p.slice(0, p.indexOf('=')), p.slice(p.indexOf('=') + 1)]);
  const hit = over.find(([k]) => k === rel);
  return hit ? hit[1] : path.join(L.base, rel);
}

// ---- the Peers table, read off its existing hooks: data-csc-table, th[data-csc-column-code], tr[data-csc-row] ----
function cells(rowHtml, tag) {
  const out = [];
  const re = new RegExp('<' + tag + '(\\s[^>]*)?>([\\s\\S]*?)</' + tag + '>', 'g');
  let m;
  while ((m = re.exec(rowHtml)) !== null) out.push({ attrs: m[1] || '', html: m[2], text: L.textOf(m[2]) });
  return out;
}
function readTable(html) {
  const at = html.indexOf('data-csc-table');
  if (at < 0) return null;
  const start = html.lastIndexOf('<table', at);
  const end = html.indexOf('</table>', at);
  const t = html.slice(start, end);
  const heads = cells(t, 'th').map((c) => ({ text: c.text, code: (/data-csc-column-code="([^"]*)"/.exec(c.attrs) || [])[1] || null }));
  const rows = [];
  const re = /<tr(\s[^>]*)?>([\s\S]*?)<\/tr>/g;
  let m;
  while ((m = re.exec(t)) !== null) {
    const kind = (/data-csc-row="([^"]*)"/.exec(m[1] || '') || [])[1];
    if (kind) rows.push({ kind, cells: cells(m[2], 'td') });
  }
  return { heads, rows };
}
function headerCurrency(mnemonic) {
  const f = (OVERLAY.header_figures || []).find((x) => x && x.mnemonic === mnemonic);
  return f && f.currency ? f.currency : null;
}
/** MONEY predicate: a figure shows its served code in its own cell ("USD 196.80") or its column head; `$` never. */
function moneyFault(cellText, headText, code) {
  const t = String(cellText).trim();
  if (/\$/.test(t) || /\$/.test(headText)) return 'a $ sign';
  if (t === '' || /^-+$/.test(t)) return null; // no figure in the cell
  if (!code) return null;
  if (new RegExp('^' + code + '\\s*[-+]?[\\d.,]+').test(t)) return null;
  if (new RegExp('\\b' + code + '\\b').test(headText)) return null;
  return 'no ' + code + ' on "' + t + '" (head "' + headText + '")';
}
function moneyFaults(html) {
  const f = [];
  const face = L.textOf(html);
  if (/\$/.test(face)) f.push('a $ sign on the Peers face');
  const tb = readTable(html);
  if (!tb) return f.concat(['NO TABLE: no data-csc-table']);
  const idx = {};
  tb.heads.forEach((h, i) => { if (h.code) idx[h.code] = i; });
  for (const code of MONEY_CODES) if (idx[code] === undefined) f.push('NO COLUMN: no th[data-csc-column-code="' + code + '"]');
  const subj = tb.rows.find((r) => r.kind === 'subject');
  if (!subj) f.push('NO SUBJECT ROW: no tr[data-csc-row="subject"]');
  else {
    const want = { price: headerCurrency('PX_LAST'), ev: headerCurrency('CURR_ENTP_VAL'), mkt_val_sec: (PEERS.subject && (PEERS.subject.cap_currency || PEERS.subject.currency)) || null };
    for (const code of MONEY_CODES) {
      if (idx[code] === undefined || !subj.cells[idx[code]]) continue;
      const x = moneyFault(subj.cells[idx[code]].text, tb.heads[idx[code]].text, want[code]);
      if (x) f.push('subject ' + code + ': ' + x);
    }
  }
  const members = tb.rows.filter((r) => r.kind === 'member');
  let graded = 0;
  for (const r of members) {
    const ticker = r.cells[1] ? r.cells[1].text : '';
    const m = (PEERS.members || []).find((x) => x.ticker === ticker);
    if (!m || idx.mkt_val_sec === undefined || !r.cells[idx.mkt_val_sec]) continue;
    graded += 1;
    const x = moneyFault(r.cells[idx.mkt_val_sec].text, tb.heads[idx.mkt_val_sec].text, m.cap_currency || null);
    if (x) f.push(ticker + ' mkt cap: ' + x);
    for (const code of ['price', 'ev']) {
      if (idx[code] !== undefined && r.cells[idx[code]] && /\$/.test(r.cells[idx[code]].text)) f.push(ticker + ' ' + code + ': a $ sign');
    }
  }
  if (graded !== (PEERS.members || []).length) f.push('MEMBERS: ' + graded + ' of ' + (PEERS.members || []).length + ' member rows matched by ticker');
  return f;
}

// ---- SAUX-34: the subject cap's as-of, in words, beside it ----
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
function etDay(iso) {
  const parts = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', year: 'numeric', month: 'numeric', day: 'numeric' }).formatToParts(new Date(iso));
  const get = (t) => Number(parts.find((p) => p.type === t).value);
  return { y: get('year'), m: get('month'), d: get('day') };
}
function dateWordsFault(text, iso) {
  const { y, m, d } = etDay(iso);
  const name = MONTHS[m - 1];
  const t = String(text);
  if (!new RegExp('\\b(' + name + '|' + name.slice(0, 3) + ')\\b\\.?\\s+' + d + '(st|nd|rd|th)?\\b').test(t)) return 'no "' + name + ' ' + d + '" in "' + t + '"';
  if (!new RegExp('\\b' + y + '\\b').test(t)) return 'no year ' + y + ' in "' + t + '"';
  return null;
}
function capAsOfFaults(html) {
  const f = [];
  const vintages = [PEERS.subject && PEERS.subject.market_cap_vintage, PEERS.subject && PEERS.subject.cap_vintage].filter(Boolean);
  if (!vintages.length) return ['INPUT: the subject serves no cap vintage'];
  const tb = readTable(html);
  if (!tb) return ['NO TABLE: no data-csc-table'];
  const i = tb.heads.findIndex((h) => h.code === 'mkt_val_sec');
  const subj = tb.rows.find((r) => r.kind === 'subject');
  if (i < 0 || !subj || !subj.cells[i]) return ['NO CELL: no subject Mkt Cap cell'];
  const cell = subj.cells[i];
  let value = (/data-peers-cap-as-of="([^"]*)"/.exec(cell.attrs) || [])[1];
  let text = cell.text;
  if (value === undefined) {
    value = (/data-peers-cap-as-of="([^"]*)"/.exec(cell.html) || [])[1];
    if (value !== undefined) text = L.textOf(L.innerOf(cell.html, 'data-peers-cap-as-of', value) || '');
  }
  if (value === undefined) return ['NO HOOK: no data-peers-cap-as-of in the subject Mkt Cap cell ("' + cell.text + '")'];
  value = decode(value);
  if (!vintages.includes(value)) f.push('HOOK VALUE "' + value + '" is not the served cap vintage (' + vintages.join(' / ') + ')');
  const x = dateWordsFault(text, value);
  if (x) f.push('DATE WORDS: ' + x);
  return f;
}

// ---- SAUX-35: the account menu, on the source ----
const HEADLESS_ESC = new Set(['Menu', 'MenuItems', 'Popover', 'PopoverPanel']);
function menuFaults(srcText) {
  const sf = ts.createSourceFile('App.tsx', srcText, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const imported = {};
  for (const st of sf.statements) {
    if (ts.isImportDeclaration(st) && st.moduleSpecifier.text === '@headlessui/react' && st.importClause && st.importClause.namedBindings && ts.isNamedImports(st.importClause.namedBindings)) {
      for (const el of st.importClause.namedBindings.elements) imported[el.name.text] = (el.propertyName || el.name).text;
    }
  }
  const all = [];
  (function walk(n) { all.push(n); ts.forEachChild(n, walk); })(sf);
  const logout = all.find((n) => (ts.isJsxText(n) && /Log Out/.test(n.text)) || (ts.isStringLiteral(n) && n.text === 'Log Out'));
  if (!logout) return ['NO MENU: no "Log Out" item in App.tsx'];
  const anc = [];
  for (let p = logout.parent; p; p = p.parent) anc.push(p);
  const tagOf = (n) => (ts.isJsxElement(n) ? n.openingElement.tagName.getText(sf) : ts.isJsxSelfClosingElement(n) ? n.tagName.getText(sf) : null);
  const headlessAnc = anc.filter((a) => tagOf(a) && imported[tagOf(a)]);
  let openName = null;
  let subtree = null;
  for (const a of anc) {
    if (ts.isBinaryExpression(a) && a.operatorToken.kind === ts.SyntaxKind.AmpersandAmpersandToken) { openName = a.left.getText(sf).trim(); subtree = a.right; break; }
    if (ts.isConditionalExpression(a)) { openName = a.condition.getText(sf).trim(); subtree = a; break; }
  }
  if (headlessAnc.length) subtree = headlessAnc[headlessAnc.length - 1];
  const f = [];
  // ESCAPE
  const escNative = headlessAnc.some((a) => HEADLESS_ESC.has(imported[tagOf(a)]));
  if (!escNative) {
    let setter = null;
    for (const n of all) {
      if (ts.isVariableDeclaration(n) && ts.isArrayBindingPattern(n.name) && n.name.elements.length >= 2) {
        const [a, b] = n.name.elements;
        if (ts.isBindingElement(a) && ts.isBindingElement(b) && a.name.getText(sf) === openName) setter = b.name.getText(sf);
      }
    }
    if (!setter) f.push('ESCAPE: the menu is not a Headless UI Menu/Popover and its open condition "' + openName + '" is not a useState value');
    else {
      const isFn = (n) => ts.isArrowFunction(n) || ts.isFunctionExpression(n) || ts.isFunctionDeclaration(n);
      const resolveFn = (expr) => {
        if (!expr) return null;
        if (isFn(expr)) return expr;
        if (ts.isIdentifier(expr)) {
          const name = expr.text;
          for (const n of all) {
            if (ts.isVariableDeclaration(n) && n.name.getText(sf) === name && n.initializer) {
              if (isFn(n.initializer)) return n.initializer;
              // useCallback(fn, deps) / useMemo-wrapped handlers
              if (ts.isCallExpression(n.initializer) && n.initializer.arguments.length && isFn(n.initializer.arguments[0])) return n.initializer.arguments[0];
            }
            if (ts.isFunctionDeclaration(n) && n.name && n.name.text === name) return n;
          }
        }
        return null;
      };
      const scan = (fn) => {
        const r = { esc: false, close: false, called: [] };
        (function walk(n) {
          if (ts.isStringLiteral(n) && (n.text === 'Escape' || n.text === 'Esc')) r.esc = true;
          if (ts.isCallExpression(n) && n.expression.getText(sf) === setter && n.arguments.length === 1) {
            const a = n.arguments[0];
            if (a.kind === ts.SyntaxKind.FalseKeyword || (ts.isArrowFunction(a) && a.body.kind === ts.SyntaxKind.FalseKeyword)) r.close = true;
          }
          if (ts.isCallExpression(n) && ts.isIdentifier(n.expression)) { const g = resolveFn(n.expression); if (g && g !== fn) r.called.push(g); }
          ts.forEachChild(n, walk);
        })(fn);
        return r;
      };
      // A function closes on Escape when it compares the key to 'Escape' and calls setter(false) itself or through one
      // named function it calls.
      const closesOnEscape = (fn) => {
        const r = scan(fn);
        return r.esc && (r.close || r.called.some((g) => scan(g).close));
      };
      const wired = [];
      for (const n of all) {
        if (ts.isCallExpression(n) && /\.addEventListener$/.test(n.expression.getText(sf)) && n.arguments.length >= 2 &&
            ts.isStringLiteral(n.arguments[0]) && /^key(down|up)$/.test(n.arguments[0].text)) wired.push(n.arguments[1]);
        if (ts.isJsxAttribute(n) && /^onKey(Down|Up)(Capture)?$/.test(n.name.getText(sf)) && n.initializer && ts.isJsxExpression(n.initializer)) wired.push(n.initializer.expression);
      }
      const ok = wired.some((w) => {
        const fn = resolveFn(w);
        if (!fn) return false;
        // the wired function itself, or one named function it calls (onKeyDown={(e) => handleKey(e)})
        return closesOnEscape(fn) || scan(fn).called.some((g) => closesOnEscape(g));
      });
      if (!ok) f.push('ESCAPE: no key handler wired by addEventListener(keydown|keyup) or onKeyDown/onKeyUp compares the key to "Escape" and calls ' + setter + '(false)');
    }
  }
  // TAB CLICK
  if (!subtree) f.push('TAB CLICK: the menu is not conditionally rendered and not a Headless UI component -- its open layer cannot be located');
  else {
    (function walk(n) {
      const tag = tagOf(n);
      if (tag) {
        const attrs = ts.isJsxElement(n) ? n.openingElement.attributes.properties : n.attributes.properties;
        const attr = (name) => attrs.find((p) => ts.isJsxAttribute(p) && p.name.getText(sf) === name);
        const cls = attr('className') ? attr('className').getText(sf) : '';
        const style = attr('style') ? attr('style').getText(sf) : '';
        const has = (t) => new RegExp('(^|[\\s"\'`{])' + t.replace(/[-]/g, '\\-') + '($|[\\s"\'`}])').test(cls);
        const covers = has('inset-0') || (has('top-0') && has('bottom-0') && has('left-0') && has('right-0')) || (has('h-screen') && has('w-screen')) ||
          /inset\s*:\s*['"]?0\b/.test(style);
        if (covers && !has('pointer-events-none')) f.push('TAB CLICK: <' + tag + '> covers the page while the menu is open (' + cls.replace(/\s+/g, ' ').slice(0, 60) + ')');
        const real = imported[tag];
        if (real === 'MenuItems') {
          const modal = attr('modal');
          const off = modal && modal.initializer && ts.isJsxExpression(modal.initializer) && modal.initializer.expression && modal.initializer.expression.kind === ts.SyntaxKind.FalseKeyword;
          if (!off) f.push('TAB CLICK: <' + tag + '> is modal (Headless UI MenuItems defaults modal=true; the page goes inert) -- set modal={false}');
        }
        if (real === 'Dialog' || real === 'DialogPanel') f.push('TAB CLICK: the menu sits in a Headless UI Dialog, which is modal');
      }
      ts.forEachChild(n, walk);
    })(subtree);
  }
  return f;
}

function renderPeers() {
  L.hookState.impl = { usePeerSet: () => PEERS, useSecurityOverlay: () => OVERLAY };
  const m = L.source(SA + 'tabs/PeersTab.tsx');
  return L.render(m.PeersTab, { securityKey: 'BA_US_Equity' });
}

const arms = [];
let peersHtml = null;
try { peersHtml = renderPeers(); } catch (e) { peersHtml = null; arms.push(['MONEY', false, 'RENDER: ' + String(e.message).split('\n')[0]]); }
if (peersHtml !== null) {
  const f = moneyFaults(peersHtml);
  arms.push(['MONEY: no $ on Peers; every subject money cell and member market cap shows its served currency code', f.length === 0,
    f.length === 0 ? 'subject 3 of 3 + member caps 12 of 12' : f.slice(0, 5).join(' | ')]);
  const g = capAsOfFaults(peersHtml);
  arms.push(['CAP AS-OF: the subject market cap prints its served as-of date in words beside it', g.length === 0,
    g.length === 0 ? 'data-peers-cap-as-of matches the served vintage; date in words' : g.join(' | ')]);
} else arms.push(['CAP AS-OF', false, 'RENDER failed']);
{
  let f;
  try { f = menuFaults(fs.readFileSync(srcFile('src/App.tsx'), 'utf8')); } catch (e) { f = ['READ: ' + String(e.message).split('\n')[0]]; }
  arms.push(['MENU: the account menu closes on Escape and lays no page-covering layer while open (source-graded)', f.length === 0,
    f.length === 0 ? 'Escape wired to the menu state; no covering layer' : f.join(' | ')]);
}

// Arm 4 -- PLANTED.
{
  const f = [];
  // money
  if (moneyFault('USD 196.80', 'Price (last)', 'USD') || moneyFault('196.80', 'Price (last, USD)', 'USD') || moneyFault('--', 'Price (last)', 'USD')) f.push('money: a good cell is rejected');
  for (const [n, c, h] of [['dollar sign', '$196.80', 'Price (last)'], ['bare figure', '196.80', 'Price (last)'], ['wrong code', 'EUR 196.80', 'Price (last)']]) {
    if (!moneyFault(c, h, 'USD')) f.push('money mutant "' + n + '" accepted');
  }
  // as-of words
  const v = '2026-09-19T07:53:20Z';
  if (dateWordsFault('USD 160B as of September 19th, 2026', v) || dateWordsFault('159,623 (Sep 19, 2026)', v)) f.push('date: a good date is rejected');
  for (const [n, t] of [['the set as-of', 'as of September 24th, 2026'], ['no date', '159,623'], ['numeric only', '2026-09-19']]) {
    if (!dateWordsFault(t, v)) f.push('date mutant "' + n + '" accepted');
  }
  // menu
  const head = "import { useState, useEffect } from 'react'\n";
  const menuOpen = (inner) => "      {showUserMenu && (\n        <>\n" + inner + "        </>\n      )}\n";
  const backdrop = "          <div className={`fixed inset-0 ${Z}`} onClick={() => setShowUserMenu(false)} />\n";
  const popup = "          <div className=\"fixed bottom-2\"><button onClick={handleLogout}>Log Out</button></div>\n";
  const layout = (effect, body) => head + 'function DashboardLayout() {\n  const [showUserMenu, setShowUserMenu] = useState(false)\n  const [showSettingsModal, setShowSettingsModal] = useState(false)\n' +
    effect + '  return (\n    <div>\n      <button onClick={() => setShowUserMenu(!showUserMenu)}>A</button>\n' + body + '    </div>\n  )\n}\n';
  const escEffect = (setter) => "  useEffect(() => {\n    if (!showUserMenu) return\n    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') " + setter + "(false) }\n" +
    "    document.addEventListener('keydown', onKey)\n    return () => document.removeEventListener('keydown', onKey)\n  }, [showUserMenu])\n";
  const hl = (modal) => "import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/react'\nfunction DashboardLayout() {\n  return (\n    <Menu>\n      <MenuButton>A</MenuButton>\n" +
    '      <MenuItems anchor="top start"' + modal + '>\n        <MenuItem><button>Log Out</button></MenuItem>\n      </MenuItems>\n    </Menu>\n  )\n}\n';
  const cbEffect = "  const closeMenu = () => setShowUserMenu(false)\n  const onKey = useCallback((e: KeyboardEvent) => { if (e.key === 'Escape') closeMenu() }, [])\n" +
    "  useEffect(() => { window.addEventListener('keydown', onKey); return () => window.removeEventListener('keydown', onKey) }, [onKey])\n";
  const GOOD = [['hand-rolled', layout(escEffect('setShowUserMenu'), menuOpen(popup))], ['useCallback + helper', layout(cbEffect, menuOpen(popup))],
    ['headless non-modal', hl(' modal={false}')]];
  const BAD = [['base shape', layout('', menuOpen(backdrop + popup))], ['Escape kept the backdrop', layout(escEffect('setShowUserMenu'), menuOpen(backdrop + popup))],
    ['Escape closes the wrong state', layout(escEffect('setShowSettingsModal'), menuOpen(popup))], ['headless modal', hl('')]];
  for (const [n, s] of GOOD) { const x = menuFaults(s); if (x.length) f.push('menu: good "' + n + '" rejected: ' + x[0]); }
  for (const [n, s] of BAD) { if (!menuFaults(s).length) f.push('menu mutant "' + n + '" accepted'); }
  arms.push(['PLANTED: 3 money, 3 date and 4 menu mutants are rejected; the good inputs pass', f.length === 0,
    f.length === 0 ? '10 of 10 mutants rejected, 8 good inputs accepted' : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log((ok ? 'ARM PASS' : 'ARM FAIL') + ' ' + n + ' :: ' + d); }
console.log('PEERS MONEY READS ONE WAY WITH ITS DATE, AND THE ACCOUNT MENU LETS GO: ' + pass + ' of ' + arms.length + ' arms');
process.exit(pass === arms.length ? 0 : 1);
