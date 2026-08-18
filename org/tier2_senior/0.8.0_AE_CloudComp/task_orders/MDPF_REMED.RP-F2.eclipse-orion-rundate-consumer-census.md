# TO MDPF_REMED.RP-F2 — PREDICATE-DERIVED CENSUS: every consumer of eclipse/orion run-date partitions. A CENSUS, NOT A FIX.

<task_order id="MDPF_REMED.RP-F2" project="MDPF_REMED">
<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-11T00:4xZ</issued>
<status>complete -- census delivered 2026-08-18 (MDPF_REMED_RPF2_ECLIPSE_ORION_CONSUMER_CENSUS_20260818.md; validity gate PASS all 4 known members surfaced independently, mdpf_aggregate_aua via the P2 feed-family predicate extension; 11 offset-relevant rows: 1 corrected-by-W1 / 6 uncorrected / 3 inherited / 1 uncorrected-inert; zero code changes)</status>
<priority>P1 — independent of the atomic window; may run immediately. First deliverable of the ruled
follow-on workstream "the label offset for ALL CONSUMERS of eclipse/orion run-date partitions"
(CTO ruling 004403Z). ⛔ NO code changes in this TO — the census IS the deliverable; fixes are
scoped off it afterward.</priority>

<references>
  <ref type="ruling">CTO 20260811T004403Z — one workstream, census-first, predicate-not-roster</ref>
  <ref type="context">DS BUILD-READY report 004145Z findings 2 + 3a (the 4-link feeder chain; ROW11 frontier-stamp symptom)</ref>
</references>

## WHY A PREDICATE, NOT A LIST (CTO, empirical, tonight's own record)
Four consumers have been found — EVERY ONE BY ACCIDENT: `dim_mdpf_aggregate_aua_timeseries` (the
outage), `build_mdpf_wsc_inflection_feeder` + `mdpf_aggregate_aua` (the 3a measurement),
`dim_mdpf_account_distribution` + `wsc_inflection_held_etf` (DS finding 2). **Four accidental
discoveries is not a list — it is a sampling process with an unknown denominator. A fifth exists
until a predicate says otherwise.** Andrew's "no hand drawn anything" binds here (the estate's own
"a predicate is not a roster"); a hand-built consumer list would be the same defect one layer up.

## SCOPE
Enumerate, BY PREDICATE OVER THE TREE, every reader of an eclipse or orion `date=` partition
(bronze/silver/feed parquets and any derived key family that carries the run-date label). For each
consumer: file:line @ commit, which vendor(s), which key family, and its OFFSET STATE —
corrected-by-W1 / uncorrected / not-applicable-with-reason.

**POSITIVE CONTROLS (validity gate): the census MUST independently surface all 4 known members
(5 files) above.** A census missing a known member is INVALID — fix the predicate, not the list.
Print the DENOMINATOR of every scan (files scanned, patterns, tool + graph vintage per provenance
header). State the predicate itself in the deliverable so it is re-runnable.

**THE HONEST CONSEQUENCE LINE (CTO ordered it stated, so nobody over-reads the window): W1 FIXES ONE
CONSUMER, NOT THE DEFECT.** After the atomic window lands, MDPF's served timeseries is correctly
labelled while sibling consumers still read run-date partitions as data dates. "W1 complete" must
never be read as "the label defect is closed." Your census sizes what remains.

<compiler_tools_mandate>
  <phase id="1" when="before census">
    <step>
      <run>comp-which "who reads eclipse/orion date= partitions" ; comp-kuzu (S3Key->consumer edges for eclipse/* + orion/* families) ; comp-pydeps / comp-find for literal + constructed key patterns (note comp-find counts LINES not nodes; band-read the hits)</run>
      <expect>A predicate expressible as tool queries; provenance headers read (kuzu vintage current); dynamic/constructed keys handled explicitly (an extractor blind to f-strings is a stated bound, not a silent one).</expect>
      <if_mismatch>A key family no tool can enumerate = a declared coverage bound in the deliverable + a comp-tool gap finding (Rule 22: a coverage gap is a DEFECT, not an inconvenience).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="census">
    <step>
      <run>the predicate, executed; positive-control check against the 4 known members</run>
      <expect>All 4 surface independently; denominator printed; each consumer rowed with offset state.</expect>
      <if_mismatch>Predicate fixed and re-run until controls pass; controls failing = the census is measuring the wrong domain.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="deliver">
    <step>
      <run>deliverable committed to your deliverables/ + MCP report to COO (CC CTO)</run>
      <expect>Census + predicate + denominators + bounds; NO fixes made; remedy scoping happens off it at CTO/COO.</expect>
      <if_mismatch>n/a</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Read-only over the tree — no coordination hazard with the atomic window or RP-W5b/W4. Do not touch
data/mdpf gold files (DS lane, mid-window). The 08-08 VintageContradiction chain is the workstream's
first named member — include its 4 links in the census rows.
</cross_domain_coordination>

<acceptance_criteria>
1. Census surfaces all 4 known members independently (positive controls pass, shown).
2. Predicate stated and re-runnable; every scan carries its denominator + tool provenance.
3. Dynamic/constructed-key coverage bound stated explicitly (what the predicate cannot see, named).
4. Each consumer rowed: file:line @ commit · vendor(s) · key family · offset state.
5. Zero code changes. Session log Compiler Tools section reproduces every &lt;run&gt; + output + pass/fail.
</acceptance_criteria>
</task_order>
