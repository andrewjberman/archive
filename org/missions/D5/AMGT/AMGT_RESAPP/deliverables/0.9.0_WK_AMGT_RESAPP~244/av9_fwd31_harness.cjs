/**
 * av9_fwd31_harness.cjs -- AMGT-av-9, FWD-31's BYTE ARM. A COPY of the loader in
 * portal/src/pages/SecurityAnalysis/__harness__/execText.harness.cjs (read only there), run from this folder.
 *
 * The ACTUAL ExecManagementTab, transpiled with the installed typescript and rendered by the ACTUAL
 * react-dom/server. The data is the LIVE /thesis answer the walker's probe saved (probe-body-N.json), NOT a
 * committed fixture: each name is rendered WITH its served `dossier_fields.management` and again with that key
 * REMOVED, then the roster rows (every <tr data-exec-officer=...>) and the whole remainder of the panel (the
 * passage slot cut out) are compared byte for byte. Writes fwd31_byte_arm.txt beside this file.
 *
 * usage: node av9_fwd31_harness.cjs <name>=<path to thesis body json> ...
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const crypto = require('crypto');
const { createRequire } = require('module');

const root = path.resolve(__dirname, '../../../../../../..');
const base = path.join(root, 'portal');
const req = createRequire(path.join(base, 'package.json'));
const ts = req('typescript');
const React = req('react');
const { renderToStaticMarkup } = req('react-dom/server');

const TAB = path.join(base, 'src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx');
const panelStub = ({ children }) => React.createElement('section', null, children);
const empty = ({ message, detail }) => React.createElement('div', { 'data-panel-state': 'empty' }, message, detail ?? null);
const loading = () => React.createElement('div', { 'data-panel-state': 'loading' });
const errorS = ({ message, hint }) => React.createElement('div', { 'data-panel-state': 'error' }, message, hint ?? null);
const cn = (...xs) => xs.filter(Boolean).join(' ');

function transpile(text) {
  return ts.transpileModule(text, { compilerOptions: { module: ts.ModuleKind.CommonJS, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022 } }).outputText;
}
function loadTab(text, filename, current) {
  const js = transpile(text);
  const mod = { exports: {} };
  function load(name) {
    if (name === '@/ui/components/panels') return { Panel: panelStub, PanelContent: panelStub, PanelHeader: panelStub };
    if (name === '../hooks/useLeadPanelApi') return { useThesisBundle: () => ({ data: current.value, isLoading: false, isError: false }) };
    if (name === '../components/IdentityLine') return { IdentityLine: () => null };
    if (name === '../components/CardFooter') return { CardFooter: () => null, footerFor: new Proxy({}, { get: () => () => ({ times: [], sources: [] }) }) };
    if (name === '../../../ui/components/states/index') return { PanelEmpty: empty, PanelLoading: loading, PanelError: errorS };
    if (name === '../../../ui/components/Controls') return { buttonClass: () => 'btn-secondary' };
    if (name === '@/lib/utils') return { cn };
    if (name === '../dateWords') return loadTab(fs.readFileSync(path.join(base, 'src/pages/SecurityAnalysis/dateWords.ts'), 'utf8'), 'dateWords.ts', current);
    if (name === '../reasonWords') return loadTab(fs.readFileSync(path.join(base, 'src/pages/SecurityAnalysis/reasonWords.ts'), 'utf8'), 'reasonWords.ts', current);
    if (name === '../../lib/dateUtils') return loadTab(fs.readFileSync(path.join(base, 'src/lib/dateUtils.ts'), 'utf8'), 'dateUtils.ts', current);
    if (name === '../types') return {};
    return req(name);
  }
  vm.runInThisContext('(function(require,module,exports){' + js + '\n})', { filename })(load, mod, mod.exports);
  return mod.exports;
}

const current = { value: null };
const { ExecManagementTab } = loadTab(fs.readFileSync(TAB, 'utf8'), TAB, current);
const render = (data, key) => { current.value = data; return renderToStaticMarkup(React.createElement(ExecManagementTab, { securityKey: key })); };
const sha = (s) => crypto.createHash('sha256').update(s, 'utf8').digest('hex').slice(0, 16);
const rowsOf = (html) => html.match(/<tr data-exec-officer=[\s\S]*?<\/tr>/g) || [];
// the passage slot: the ONE element carrying data-dossier-management (a <section> when served, a <p> when not)
const slotRe = /<(section|p) data-dossier-management=[\s\S]*?<\/\1>/;
const slotOf = (html) => { const m = html.match(slotRe); return m ? m[0] : null; };

const out = [];
const say = (s) => { out.push(s); console.log(s); };
let allOk = true;

for (const arg of process.argv.slice(2)) {
  const [name, file] = arg.split('=');
  const bytes = fs.readFileSync(file);
  const full = JSON.parse(bytes.toString('utf8'));
  const key = full.security_key;
  const served = full.dossier_fields && full.dossier_fields.management;
  const officers = (full.management && full.management.officers) || [];
  say(`NAME ${name} security_key=${key} source_body_sha256_16=${crypto.createHash('sha256').update(bytes).digest('hex').slice(0, 16)} served_officers=${officers.length} roster_source=${full.management && full.management.roster_source} dossier_management_status=${served && served.status}`);

  const withData = JSON.parse(bytes.toString('utf8'));
  const withoutData = JSON.parse(bytes.toString('utf8'));
  delete withoutData.dossier_fields.management; // the removal: the key is GONE, not nulled
  const htmlWith = render(withData, key);
  const htmlWithout = render(withoutData, key);

  // POSITIVE CONTROL (same render): the tab's own label and the panel marker are present
  const labelOk = htmlWith.includes('data-tab-panel="exec_management"') && htmlWith.includes('data-exec-status=');
  const slotWith = slotOf(htmlWith);
  const slotWithout = slotOf(htmlWithout);
  say(`  POSITIVE CONTROL: exec_management panel marker + data-exec-status present: ${labelOk}; slot WITH   = ${slotWith ? slotWith.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').slice(0, 160).trim() : 'NONE'} [${slotWith ? slotWith.match(/data-dossier-management="([^"]*)"/)[1] : '-'}]`);
  say(`  slot WITHOUT the key = ${slotWithout ? slotWithout.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').slice(0, 160).trim() : 'NONE'} [${slotWithout ? slotWithout.match(/data-dossier-management="([^"]*)"/)[1] : '-'}]`);
  const labelled = !!slotWith && slotWith.includes('The research team on management');
  const cited = !!slotWith && /Source: /.test(slotWith);
  say(`  passage arm (WITH): labelled-as-the-team's=${labelled} cited-to-report=${cited} slot-served=${slotWith ? /data-dossier-management="SERVED"/.test(slotWith) : false}`);

  // BESIDE, not in place of: the roster follows the slot in the same panel
  const iSlot = htmlWith.indexOf(slotWith || '\u0000');
  const iRoster = htmlWith.indexOf('<tr data-exec-officer=');
  say(`  beside-the-roster: passage slot offset ${iSlot}, first roster row offset ${iRoster}, roster rows rendered ${rowsOf(htmlWith).length}`);

  // THE BYTE COMPARE
  const rw = rowsOf(htmlWith);
  const ro = rowsOf(htmlWithout);
  let equalRows = 0;
  for (let i = 0; i < Math.max(rw.length, ro.length); i++) if (rw[i] !== undefined && rw[i] === ro[i]) equalRows++;
  const n = Math.max(rw.length, ro.length);
  const restWith = slotWith ? htmlWith.replace(slotWith, '') : htmlWith;
  const restWithout = slotWithout ? htmlWithout.replace(slotWithout, '') : htmlWithout;
  const restEqual = restWith === restWithout;
  say(`  roster rows: with=${rw.length} without=${ro.length}; sha256_16 of rows WITH=${sha(rw.join('\n'))} WITHOUT=${sha(ro.join('\n'))}`);
  say(`  rest of panel (slot cut out) byte-equal: ${restEqual} (len ${restWith.length} vs ${restWithout.length}; sha256_16 ${sha(restWith)} vs ${sha(restWithout)})`);
  const officersMatch = rw.length === officers.length;
  say(`  roster rows equal the served officer count: ${officersMatch} (${rw.length} of ${officers.length})`);

  // NEGATIVE CONTROL: one officer's name altered in the WITHOUT data must make the compare fail
  const mutated = JSON.parse(bytes.toString('utf8'));
  delete mutated.dossier_fields.management;
  if (mutated.management && mutated.management.officers && mutated.management.officers[0]) mutated.management.officers[0].name = mutated.management.officers[0].name + ' X';
  const rm = rowsOf(render(mutated, key));
  let eqMut = 0;
  for (let i = 0; i < Math.max(rw.length, rm.length); i++) if (rw[i] !== undefined && rw[i] === rm[i]) eqMut++;
  say(`  NEGATIVE CONTROL (officer 1 renamed in the WITHOUT copy): rows equal ${eqMut} of ${Math.max(rw.length, rm.length)} (must be below ${rw.length})`);
  const ok = n > 0 && equalRows === n && rw.length === ro.length && restEqual && eqMut < rw.length && labelOk;
  if (!ok) allOk = false;
  say(`ROSTER ROWS BYTE-EQUAL: ${equalRows} of ${n}   (${name}; ${ok ? 'whole-panel remainder equal and negative control discriminated' : 'CHECK FAILED'})`);
}
fs.writeFileSync(path.join(__dirname, 'fwd31_byte_arm.txt'), out.join('\n') + '\n', 'utf8');
process.exit(allOk ? 0 : 1);
