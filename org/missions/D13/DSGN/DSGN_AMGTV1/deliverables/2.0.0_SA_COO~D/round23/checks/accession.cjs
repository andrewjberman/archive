/**
 * accession.cjs -- DSGN_AMGTV1 round 23, AV-zb-2 (issuer 2.0.0_SA_COO~D): THE EXEC FACE NAMES THE FILING, NEVER ITS ACCESSION NUMBER.
 *
 * Usage (repo root): node <this file>        (portal/ under the cwd is the checkout under test)
 * CTO round-22 analysis @eee9380be7 ruling 2 / section 3 row 2 (FWD-11): the SEC accession is an id and comes off the face. The face
 * names the filing in words -- its form and filing date -- and the accession rides a data- attribute (or a link target).
 * The served form and date: the thesis bundle's `drafting_provenance` ({accession, form, filing_date}) when its accession equals
 * `management.source_accession`. When they differ the page names no form or date it was not served for that filing.
 * Inputs: portal/src/pages/SecurityAnalysis/__harness__/tabsFixture.BA_US_Equity.json (thesis: management.source_accession
 * 000162828026004357; drafting_provenance {accession 000162828026004357, form 10-K, filing_date 2026-01-30}).
 * Render: round15/checks/_load.cjs (the real ExecManagementTab; useThesisBundle returns the fixture's thesis).
 * Census (visible text only): ACCESSION /\d{10}-\d{2}-\d{6}/ and /\b\d{18}\b/.
 * Arms:
 *   1  THE CHECKOUT (served match): 0 ACCESSION on the Exec face; the face carries "10-K" and "January 30th, 2026"; some element
 *      carries the accession 000162828026004357 in a data- attribute.
 *   2  NO MATCH: drafting_provenance.accession set to another filing -> still 0 ACCESSION, no "January 30th, 2026" (no date
 *      invented for a filing it was not served for), the accession still in a data- attribute.
 *   3  PLANTED: the census reads >= 1 on "filing 0001628280-26-004357" and on a bare 18-digit run, and 0 on "10-K, filed January
 *      30th, 2026".
 * Prints one line per arm and "THE EXEC FACE NAMES THE FILING, NOT ITS ACCESSION: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const fs = require('fs');
const path = require('path');

const SA = 'src/pages/SecurityAnalysis/';
const L = require(path.join(__dirname, '..', '..', 'round15', 'checks', '_load.cjs'));
const FIX = JSON.parse(fs.readFileSync(path.join(L.base, SA + '__harness__/tabsFixture.BA_US_Equity.json'), 'utf8'));
const ACC = '000162828026004357';
const DATE_WORDS = 'January 30th, 2026';
const RE = [/\d{10}-\d{2}-\d{6}/g, /\b\d{18}\b/g];
const census = (text) => RE.reduce((n, re) => n + (text.match(re) || []).length, 0);
const clone = (x) => JSON.parse(JSON.stringify(x));

function render(thesis) {
  L.hookState.impl = { useThesisBundle: () => thesis, usePeerSet: () => FIX.peers, useSecurityOverlay: () => FIX.overlay, useCollectedChatter: () => undefined };
  return L.render(L.source(SA + 'tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: FIX.security_key });
}
const inAttr = (html) => new RegExp(`data-[a-z0-9-]+="${ACC}"`).test(html);

const arms = [];
{
  const f = [];
  const t = clone(FIX.thesis);
  if (!t.management || t.management.source_accession !== ACC || !t.drafting_provenance || t.drafting_provenance.accession !== ACC) f.push('INPUT: the fixture no longer pairs the accession');
  else {
    try {
      const h = render(t);
      const text = L.textOf(h);
      const n = census(text);
      if (n) f.push(`ACCESSION on the face x${n}`);
      if (!text.includes('10-K')) f.push('FORM: "10-K" is not on the face');
      if (!text.includes(DATE_WORDS)) f.push(`DATE: "${DATE_WORDS}" is not on the face`);
      if (!inAttr(h)) f.push('ATTR: no data- attribute carries the accession');
    } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  }
  arms.push(['the checkout: the filing is named by form and date, the accession only in a data- attribute', f.length === 0,
    f.length === 0 ? '0 accession on the face; 10-K + date shown; attribute present' : f.join(' | ')]);
}
{
  const f = [];
  const t = clone(FIX.thesis);
  t.drafting_provenance = { ...t.drafting_provenance, accession: '000000000026000001' };
  try {
    const h = render(t);
    const text = L.textOf(h);
    const n = census(text);
    if (n) f.push(`ACCESSION on the face x${n}`);
    if (text.includes(DATE_WORDS)) f.push(`INVENTED: "${DATE_WORDS}" shown for a filing it was not served for`);
    if (!inAttr(h)) f.push('ATTR: no data- attribute carries the accession');
  } catch (e) { f.push('RENDER: ' + String(e.message).split('\n')[0]); }
  arms.push(['NO MATCH: another filing\'s provenance -> no accession, no borrowed date, the accession still in an attribute', f.length === 0,
    f.length === 0 ? 'held' : f.join(' | ')]);
}
{
  const f = [];
  if (census('5 officer(s), filing 0001628280-26-004357') < 1) f.push('the dashed accession is not caught');
  if (census(`accession ${ACC}`) < 1) f.push('the 18-digit run is not caught');
  if (census('the company\'s 10-K, filed January 30th, 2026') !== 0) f.push('a form-and-date line is flagged');
  arms.push(['PLANTED: a dashed accession and an 18-digit run are caught; a form-and-date line is not', f.length === 0,
    f.length === 0 ? '2 of 2 caught; clean 0' : f.join(' | ')]);
}

let pass = 0;
for (const [n, ok, d] of arms) { if (ok) pass += 1; console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${n} :: ${d}`); }
console.log(`THE EXEC FACE NAMES THE FILING, NOT ITS ACCESSION: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
