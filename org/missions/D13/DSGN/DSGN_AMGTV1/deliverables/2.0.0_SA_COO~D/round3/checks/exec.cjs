/**
 * exec.cjs -- DSGN_AMGTV1 round 3: EXEC MANAGEMENT'S ABSENCE READS AS A SENTENCE SAYING WHERE THE LIST CAME FROM (FWD-7).
 *
 * Usage (repo root): node <this file>
 * Input: INTU's served /thesis bundle (management ABSENT, absent_because ZERO_OFFICERS), captured at the cut. Renders the
 * Exec Management tab (tabs/ExecManagementTab.tsx). The walk hit "Exec Management: ABSENT (ZERO_OFFICERS)." on the face.
 * Arms, all must hold:
 *   A  the tab's visible text carries none of: ZERO_OFFICERS, ROSTER_UNRESOLVED, roster_status, roster_reason, source_item,
 *      source_accession, "ABSENT (", crosswalk/v1 (collapsed <details> content excluded; attributes are free).
 *   B  the absence reads as a sentence that names the officers and where the list was looked for: the visible text of the
 *      element carrying data-exec-status="ABSENT" contains "officer" and one of "filing", "10-K", "research", "Bloomberg",
 *      "source".
 *   C  the served state is kept in attributes: data-exec-status="ABSENT" and data-exec-absent-because="ZERO_OFFICERS".
 * Prints "EXEC ABSENCE IN WORDS: k of 3 arms"; exit 0 only at 3 of 3.
 */
const L = require('./_load.cjs');
const intu = L.fixture('thesisBundle.INTU_US_Equity.json');
L.hookState.impl = { useThesisBundle: () => intu };
const { ExecManagementTab } = L.source('src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx');
const html = L.render(ExecManagementTab, { securityKey: 'INTU_US_Equity' });
const strip = (h) => h.replace(/<details(?![^>]*\sopen)[^>]*>[\s\S]*?<\/details>/g, '');
const text = L.textOf(strip(html));
const BAD = ['ZERO_OFFICERS', 'ROSTER_UNRESOLVED', 'roster_status', 'roster_reason', 'source_item', 'source_accession', 'ABSENT (', 'crosswalk/v1'];
const results = [];
{
  const hits = BAD.filter((b) => text.includes(b));
  results.push(['A no machine string on the face', text.length > 0 && hits.length === 0, `hits=[${hits.join(', ')}]`]);
}
{
  const inner = L.innerOf(strip(html), 'data-exec-status', 'ABSENT');
  const t = L.textOf(inner || '');
  const ok = /officer/i.test(t) && /(filing|10-K|research|Bloomberg|source)/i.test(t);
  results.push(['B a sentence naming the officers and where the list was looked for', ok, `text=${JSON.stringify(t.slice(0, 200))}`]);
}
{
  const ok = html.includes('data-exec-status="ABSENT"') && html.includes('data-exec-absent-because="ZERO_OFFICERS"');
  results.push(['C the served state kept in attributes', ok, `status_attr=${html.includes('data-exec-status="ABSENT"')} because_attr=${html.includes('data-exec-absent-because="ZERO_OFFICERS"')}`]);
}
let pass = 0;
for (const [n, ok, d] of results) {
  console.log(`ARM ${ok ? 'PASS' : 'FAIL'} ${n} :: ${d}`);
  if (ok) pass += 1;
}
console.log(`EXEC ABSENCE IN WORDS: ${pass} of 3 arms`);
process.exit(pass === 3 ? 0 : 1);
