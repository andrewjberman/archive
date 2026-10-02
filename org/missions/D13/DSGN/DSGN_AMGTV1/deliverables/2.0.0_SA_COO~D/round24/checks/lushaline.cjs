/**
 * lushaline.cjs -- DSGN_AMGTV1 round 24, AV-zc-1 (issuer 2.0.0_SA_COO~D): THE EXEC CONTACT-ENRICHMENT LINE SAYS IT ONCE.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO ruling msg 28350 on row DSGN_AMGTV1-Z-S14: "when the served Lusha reason is code-free, print it alone, as one sentence."
 * Today the line prints the page's lead-in "Contact enrichment was skipped for this company" and then " -- <served reason>", and
 * RESAPP B2's plain served reason begins "Contact enrichment was skipped: ...", so the phrase repeats.
 * THE CONTRACT for a SKIPPED enrichment (`management.lusha_enrichment.status === 'SKIPPED'`), on the `data-lusha-enrichment` line:
 *   - a CODE-FREE served reason prints ALONE: the line's visible text is the served reason (trimmed), and "Contact enrichment was
 *     skipped" appears at most once on the Exec face;
 *   - a served reason carrying a code-shaped token (AV-z-1's guard) prints the page's plain sentence instead, with no token;
 *   - the served reason rides `data-lusha-reason` in both cases.
 * Inputs: portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.BA_US_Equity.json (thesis), lusha_enrichment planted.
 * Render: round15/checks/_load.cjs (the real ExecManagementTab).
 * Arms:
 *   1  THE CHECKOUT, code-free: served "Contact enrichment was skipped: no company web domain is on record for this name, and a
 *      guessed domain would enrich the wrong company" -> the line reads exactly that (a trailing period allowed), the phrase once.
 *   2  THE GUARD HOLDS, coded: served "no declared domain for VLO_US_Equity in domains.json" -> the line carries no `_Equity` and
 *      no `.json`, is non-empty, and `data-lusha-reason` carries the served string.
 *   3  PLANTED: the comparator rejects a repeated line and a line with the lead-in prepended; it accepts the reason alone.
 * Prints one line per arm and "THE CONTACT-ENRICHMENT LINE SAYS IT ONCE: <k> of 3 arms"; exit 0 only at 3 of 3. Seconds.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const L = require(path.join(__dirname, '..', '..', 'round15', 'checks', '_load.cjs'));
const FIX = JSON.parse(fs.readFileSync(path.join(L.base, SA + '__harness__/tabsFixture.BA_US_Equity.json'), 'utf8'));
const PLAIN = 'Contact enrichment was skipped: no company web domain is on record for this name, and a guessed domain would enrich the wrong company';
const CODED = 'no declared domain for VLO_US_Equity in domains.json';
const PHRASE = /Contact enrichment was skipped/g;
const decode = (s) => String(s).replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');

function render(reason) {
  const t = JSON.parse(JSON.stringify(FIX.thesis));
  t.management.lusha_enrichment = { status: 'SKIPPED', reason };
  L.hookState.impl = { useThesisBundle: () => t, usePeerSet: () => FIX.peers, useSecurityOverlay: () => FIX.overlay, useCollectedChatter: () => undefined };
  return L.render(L.source(SA + 'tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: FIX.security_key });
}
function line(html) {
  const m = /<p\b([^>]*\bdata-lusha-enrichment="SKIPPED"[^>]*)>([\s\S]*?)<\/p>/.exec(html);
  if (!m) return null;
  const r = /data-lusha-reason="([^"]*)"/.exec(m[1]);
  return { text: L.textOf(m[2]), reasonAttr: r ? decode(r[1]) : null };
}
const norm = (s) => s.trim().replace(/\.$/, '');
function aloneFaults(text, faceText, served) {
  const f = [];
  if (norm(text) !== norm(served)) f.push(`LINE: reads "${text.slice(0, 120)}" (want the served reason alone)`);
  const n = (faceText.match(PHRASE) || []).length;
  if (n > 1) f.push(`REPEAT: "Contact enrichment was skipped" x${n} on the face`);
  return f;
}

const arms = [];
{
  const f = [];
  try {
    const h = render(PLAIN);
    const l = line(h);
    if (!l) f.push('no data-lusha-enrichment="SKIPPED" line');
    else {
      f.push(...aloneFaults(l.text, L.textOf(h), PLAIN));
      if (l.reasonAttr !== PLAIN) f.push('ATTR: data-lusha-reason does not carry the served reason');
    }
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['the checkout: a code-free served reason prints alone, the phrase once', f.length === 0, f.length === 0 ? 'one sentence' : f.join(' | ')]);
}
{
  const f = [];
  try {
    const l = line(render(CODED));
    if (!l) f.push('no data-lusha-enrichment="SKIPPED" line');
    else {
      if (/_Equity\b|\.json\b/.test(l.text)) f.push(`TOKEN on the face: "${l.text}"`);
      if (l.text.replace(/[\s.]/g, '').length < 10) f.push(`EMPTY: "${l.text}"`);
      if (l.reasonAttr !== CODED) f.push('ATTR: data-lusha-reason does not carry the served reason');
    }
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['THE GUARD HOLDS: a coded served reason prints the plain sentence, the reason in the attribute', f.length === 0, f.length === 0 ? 'guarded' : f.join(' | ')]);
}
{
  const f = [];
  const repeated = `Contact enrichment was skipped for this company -- ${PLAIN}`;
  if (aloneFaults(PLAIN + '.', PLAIN + '.', PLAIN).length) f.push('the reason alone is rejected');
  if (!aloneFaults(repeated, repeated, PLAIN).length) f.push('a repeated line is accepted');
  if (!aloneFaults(`Lusha enrichment: SKIPPED -- ${PLAIN}`, PLAIN, PLAIN).length) f.push('a prepended lead-in is accepted');
  arms.push(['PLANTED: a repeated line and a prepended lead-in are rejected; the reason alone passes', f.length === 0, f.length === 0 ? '2 of 2 rejected' : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE CONTACT-ENRICHMENT LINE SAYS IT ONCE: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
