<task_order>
<to_id>ADHOC.comp-kuzu-fixes-k3-k4-k6-k7</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~B</issued_to>
<date>2026-08-04</date>
<status>staged</status>
<priority>P1 (ANDREW-DIRECT ~1900Z fan-out @fc42aacc5: parallel seats on the spine-tool items; graph infra = the 0.7.0 lane family)</priority>

<title>comp-kuzu fixes: K4 stitch adjudication-fix + K3 -full/-inc output contracts + K6 0-rows scope note + K7 edge-direction primer line</title>

<context>
Andrew ordered agents fanned out on the comp-kuzu dial items (CVO record @fc42aacc5; the dial
record CLOSED @395aaf053 is THE SPEC -- read its K-items before anything). CVO's dial records +
baselines are the declare-by-exercise source; CVO VERIFIES each item on landing (their standing
scope). comp-kuzu is the canonical auto-refreshing graph DB -- Rule 20 surface; regression care
is proportionate.
</context>

<scope>
Per the kuzu dial record's own item shapes (the record wins conflicts; surface, don't adjudicate):
K4 (stitch adjudication-fix), K3 (the -full/-inc output contracts declared), K6 (the 0-rows
scope note in output), K7 (the edge-direction primer line). NOTHING beyond the four items --
no re-dial, no engine work the record does not name. T2-class family questions stay PRD-gated.
Exercise-before-and-after per item (the dial's own method: every gate an exercise); CVO's
baselines are your pre-fix controls.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>read the comp-kuzu dial record in full + reproduce each K-item's finding (pre-fix control, verbatim captures)</run>
    <expect>4/4 reproduced or the delta from the record named to CVO before building.</expect>
    <if_mismatch>STOP on any item that no longer reproduces -- re-ground with CVO.</if_mismatch></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>per item: the fixed behavior exercised (the test that fails pre-fix, passes post-fix); comp-kuzu baseline queries byte-stable where the item does not intend change</run>
    <expect>Both directions captured per item; unintended-change surface = zero.</expect>
    <if_mismatch>STOP -- a kuzu output change beyond the item's intent is a Rule-20 surface change; surface to CTO.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>report per item to CVO (verify-on-landing) + me + CTO; commit-gate clean</run>
    <expect>CVO can verify without a follow-up ask.</expect>
    <if_mismatch>REWORK per CVO.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
comp-kuzu is estate-shared (Rule 20). ~A holds comp-blast (a) rework + the registration set --
your K3 contract declarations feed their registration work; cite your landing to ~A. No overlap
with the mdpf/CANRTE streams.
</cross_domain_coordination>

<acceptance_criteria>
1. 4/4 items: pre-fix control + post-fix exercise captured verbatim.
2. Baseline byte-stability shown outside each item's intended surface.
3. CVO verify-on-landing obtained per item.
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="authority">ANDREW-DIRECT ~1900Z fan-out (CVO record @fc42aacc5)</ref>
  <ref type="spec">comp-kuzu DIAL RECORD (@395aaf053 close) -- THE spec; CVO baselines = controls</ref>
</references>
<dependencies><none/></dependencies>
</task_order>
