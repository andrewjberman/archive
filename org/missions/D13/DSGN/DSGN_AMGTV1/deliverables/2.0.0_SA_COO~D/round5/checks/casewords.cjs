/**
 * casewords.cjs -- DSGN_AMGTV1 round 5, AV-v-7: FWD-30'S PARITY ADMITS THE EXPORT'S CASE LINE IN WORDS (AMGT_RESAPP round-48
 * ask item 2, msg 26588: "exportCompare.harness.cjs `artifactCases` stops requiring the raw formula in the export's case
 * line, so render_pack can print the words there").
 *
 * Usage (repo root): node <this file>
 * Runs the page's OWN parity harness (portal/src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs, `--rich`
 * mode) twice against the served AMD payload (round5/fixtures/thesisBundle.AMD_US_Equity.json as the fixture's `thesis`),
 * each time over a temporary export holding ONLY the three case lines the export prints for that payload
 * (render_pack `_model_case_line`: "<label or Name case>: SERVED -- <value, 2 dp> <CRNCY> (<formula>)" /
 * "<Name> case: ABSENT -- <served reason>"), built by this check from the payload itself:
 *   RAW    the case line with the served raw `formula` -- today's export
 *   WORDS  the same line with the served `formula_words` in the parenthesis -- the export once render_pack prints words
 * Only the harness's "CASES page=.. rich=.. same=.. missing=.. extra=.." line is read (the other sets are out of scope here:
 * the temporary export carries no figures). Temp files are written under the OS temp dir and removed.
 * Arms:
 *   1  RAW: CASES exact (missing=0 extra=0) -- the harness still reads today's export (a control that must stay green)
 *   2  WORDS: CASES exact -- the harness admits the words line
 * Prints one line per arm and "PARITY ADMITS THE WORDS CASE LINE: <k> of 2 arms"; exit 0 only at 2 of 2.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const root = process.cwd();
const FX = path.join(root, 'org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round5/fixtures/thesisBundle.AMD_US_Equity.json');
// ISSUER GREEN ARM ONLY: CASEWORDS_HARNESS=<absolute file> runs a scratch harness copy to prove the check CAN pass.
// A worker never sets it; the proof-of-spec invocation does not.
const HARNESS = process.env.CASEWORDS_HARNESS || path.join(root, 'portal/src/pages/SecurityAnalysis/__harness__/exportCompare.harness.cjs');
const thesis = JSON.parse(fs.readFileSync(FX, 'utf8'));
const crncy = ((thesis.header_figures || []).find((f) => f.mnemonic === 'CRNCY') || {}).value || null;
const cases = thesis.model_cases || {};

function lines(useWords) {
  const out = [];
  for (const name of ['Upside', 'Base', 'Downside']) {
    const c = cases[name.toLowerCase()] || {};
    const head = c.label ? c.label : `${name} case`;
    if (c.status === 'SERVED') {
      const cur = c.quote_currency && crncy && c.quote_currency !== crncy ? null : crncy;
      const value = typeof c.value === 'number' ? c.value.toFixed(2) : String(c.value);
      const f = useWords ? c.formula_words : c.formula;
      out.push(`${head}: SERVED -- ${value}${cur ? ` ${cur}` : ''}${f ? ` (${f})` : ''}`);
    } else {
      out.push(`${head}: ABSENT -- ${c.reason || `no ${name.toLowerCase()} case on the landed block`}`);
    }
  }
  return out;
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'casewords-'));
const fixturePath = path.join(tmp, 'served_fixture.AMD_US_Equity.json');
fs.writeFileSync(fixturePath, JSON.stringify({ security_key: 'AMD_US_Equity', thesis, overlay: null, peers: null, rankings_live: null }));
function run(label, useWords) {
  const rich = path.join(tmp, `${label}.rich.md`);
  fs.writeFileSync(rich, '# AMD US\n\n## Model\n\n' + lines(useWords).join('\n') + '\n');
  const r = spawnSync(process.execPath, [HARNESS, '--fixture', fixturePath, '--rich', rich], {
    cwd: path.join(root, 'portal'), encoding: 'utf8', timeout: 110000,
  });
  const out = (r.stdout || '') + (r.stderr || '');
  const m = /^CASES .*$/m.exec(out);
  const err = /(Cannot find module|^Error|TypeError|ReferenceError)[^\n]*/m.exec(out);
  return { line: m ? m[0] : `no CASES line (rc=${r.status}${err ? '; ' + err[0].slice(0, 120) : ''})`, exact: !!m && /missing=0 extra=0\s*$/.test(m[0]) && !/page=0 /.test(m[0]) };
}
let raw;
let words;
try {
  raw = run('raw', false);
  words = run('words', true);
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
const served = (cases.base || {}).formula_words;
const arms = [
  ['RAW export case lines: CASES exact (control)', raw.exact, raw.line],
  ['WORDS export case lines: CASES exact', !!served && words.exact, `${served ? '' : 'the payload carries no formula_words; '}${words.line}`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`PARITY ADMITS THE WORDS CASE LINE: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
