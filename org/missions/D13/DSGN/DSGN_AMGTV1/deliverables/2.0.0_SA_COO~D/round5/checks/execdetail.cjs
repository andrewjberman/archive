/**
 * execdetail.cjs -- DSGN_AMGTV1 round 5, AV-v-5: EXEC "READ DETAIL" WITHOUT THE MACHINE REASON (round-4 analysis s.4 item 5;
 * FWD-7, FWD-11).
 *
 * Usage (repo root): node <this file>
 * Renders the Exec Management tab (tabs/ExecManagementTab.tsx) on INTU (management ABSENT, roster UNRESOLVED-SOURCE; served
 * fixture) and on Valero (management SERVED, 5 officers). Visible text includes collapsed <details> content ("Read detail"
 * is a drawer a PM opens). The served machine reason is the fixture's own `management.roster_reason` / `reason` /
 * `absence_reason_evidence` string ("no declared shape read this section (4 usable line(s), 0 candidate(s)): ...").
 * Arms:
 *   1  INTU: the served machine reason appears NOWHERE in visible text (no substring of 24+ characters of it), and it still
 *      rides the markup on an attribute (the reason's text is found inside some attribute value)
 *   2  INTU: the drawer still says where it looked in words -- "Where we looked:" with the filing number as the round-4
 *      cell printed it ("0000896878-26-000037")
 *   3  Valero: the officer table is unchanged in count -- the 5 served officers' names all visible
 * Prints one line per arm and "EXEC DETAIL WITHOUT THE MACHINE REASON: <k> of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const bundles = {};
for (const k of ['INTU_US_Equity', 'VLO_US_Equity']) bundles[k] = L.fixture(`thesisBundle.${k}.json`);
L.hookState.impl = { useThesisBundle: (k) => bundles[k], useManagement: (k) => (bundles[k] || {}).management };
function render(key) {
  try {
    return L.render(L.source('src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx').ExecManagementTab, { securityKey: key });
  } catch (e) {
    console.log(`${key} render failed: ` + String(e.message).split('\n')[0]);
    return '';
  }
}
const intuHtml = render('INTU_US_Equity');
const vloHtml = render('VLO_US_Equity');
const intuText = L.textOf(intuHtml);
const m = bundles.INTU_US_Equity.management;
const reason = m.roster_reason || m.reason || m.absence_reason_evidence || '';
// a 24-character window of the machine reason, anywhere in visible text
const windows = [];
for (let i = 0; i + 24 <= reason.length; i += 8) windows.push(reason.slice(i, i + 24));
const leaks = windows.filter((w) => intuText.includes(w));
const attrs = [...intuHtml.matchAll(/\s[\w-]+="([^"]*)"/g)].map((x) => x[1].replace(/&#x27;/g, "'").replace(/&amp;/g, '&').replace(/&quot;/g, '"'));
const onAttr = reason.length > 0 && attrs.some((v) => v.includes(reason.slice(0, 40)));
const where = /Where we looked:/.test(intuText) && intuText.includes('0000896878-26-000037');
const officers = (bundles.VLO_US_Equity.management.officers || []).map((o) => o.name).filter(Boolean);
const vloText = L.textOf(vloHtml);
const shown = officers.filter((n) => vloText.includes(n));
const arms = [
  ['INTU: the machine reason is not visible, it rides an attribute', intuHtml.length > 0 && reason.length > 0 && leaks.length === 0 && onAttr,
    `visible 24-char windows of the reason ${leaks.length} of ${windows.length}${leaks.length ? ` ("${leaks[0]}")` : ''}; on an attribute ${onAttr}`],
  ['INTU: "Where we looked:" with the filing number', where, `Where we looked ${/Where we looked:/.test(intuText)}; filing 0000896878-26-000037 ${intuText.includes('0000896878-26-000037')}`],
  ['Valero: every served officer still shown', vloHtml.length > 0 && officers.length > 0 && shown.length === officers.length, `${shown.length} of ${officers.length} officer name(s) visible`],
];
let pass = 0;
for (const [name, ok, detail] of arms) {
  if (ok) pass += 1;
  console.log(`${ok ? 'ARM PASS' : 'ARM FAIL'} ${name} :: ${detail}`);
}
console.log(`EXEC DETAIL WITHOUT THE MACHINE REASON: ${pass} of ${arms.length} arms`);
process.exit(pass === arms.length ? 0 : 1);
