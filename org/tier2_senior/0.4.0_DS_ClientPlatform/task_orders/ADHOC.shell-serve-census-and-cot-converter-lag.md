<task_order>
<to_id>ADHOC.shell-serve-census-and-cot-converter-lag</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-03</date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ADHOC" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: pending</status>
<!-- Leg 1 DELIVERED @a6d1dc1797, routed CTO cc COO 233544Z/233549Z (4 serve days x 12
     artifacts within surviving evidence; pre-07-19 UNKNOWN). Leg 2 resolved NO-DEFECT
     (diagnosis corrected on instrument evidence, no fix deployed); closes on tonight's
     scheduled snapshot-frontier advance to 08-03 -- read, never hand-run (NEVER#4). -->
<priority>P1 (CTO ruling 232535Z items b-ii + c: the shell half of the Andrew disclosure package -- bounded, mechanical, no judgement calls; + the converter lag at the same seat because same channel, same evidence base. Sequencing within your seat yours.)</priority>

<title>Shell-serve census (bounded, serve-window) + cottonwood silver-converter lag diagnosis-to-fix -- one seat, one evidence base</title>

<context>
LEG 1 -- THE SHELL CENSUS (completes the Andrew package's shell half; CTO scope verbatim):
"enumerate silver allocation partitions, mark the near-empty ones, and determine which were
LATEST-SNAPSHOT at a serve moment -- that last condition is the whole question, since a shell
only harms if a consumer selected it. Finite, mechanical, no judgement calls." Bounds: the
standing serve-window rule (2024-11+; coverage matters, pre-floor archaeology does not).
"Anything not answerable from surviving partitions is recorded UNKNOWN with its reason, never
estimated." Your outcome-B evidence (the 07-09 cash_coverage documented instance + the measured
near-empty partials) seeds it; the deliverable is the complete day-list: which serve moments
consumed a shell/partial, per artifact.

LEG 2 -- THE CONVERTER LAG (CTO item c, DS lane per Rule 13): your own diagnosis stands (bronze
current through 08-03-labeled; silver fact tables stop 07-31; the converter's event/sweep leg
for the cottonwood xlsx families is where the evidence points). Diagnosis-to-FIX: source-confirm
the mechanism (file:line @ commit), fix it, scheduled-run evidence closes it (a hand-run
converts nothing per NEVER#4a -- QA only). Same channel + same partition evidence as Leg 1,
which is why both legs live at your seat.
</context>

<scope>
1. Leg 1: partition census per the CTO scope -- denominator printed (partitions enumerated per
   table, method stated); near-empty/shell marked with sizes; the LATEST-SNAPSHOT-at-serve-moment
   determination per artifact; output = the day-list + UNKNOWNs-with-reasons. Report feeds CTO's
   Andrew package DIRECTLY -- route to CTO cc COO the moment it lands.
2. Leg 2: converter mechanism cite -> fix per Rule 13 (commit-gate, safe-deploy, MATCH) ->
   next scheduled cycle advances the cottonwood silver frontier (the acceptance evidence).
3. NO alarms/monitors. Leg 1 is read-only; Leg 2 is the one mutation and it is the fix itself.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="Leg 1 census">
    <step>
      <run>silver-partition enumeration (s3 ls + sizes, method stated) + the gold latest-snapshot selection logic at pinned commits (A_00:13,:327 / A_01:29 seeds)</run>
      <expect>Denominator printed; every near-empty partition dated + sized; selection logic cited per consumer.</expect>
      <if_mismatch>A consumer whose selection logic cannot be source-confirmed makes its days UNKNOWN-with-reason, never inferred.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="Leg 2 diagnose + fix">
    <step>
      <run>converter event/sweep trace at source; fix; commit-gate + safe-deploy + MATCH</run>
      <expect>Mechanism file:line @ commit; fix one logical change; deployed MATCH.</expect>
      <if_mismatch>STOP on any second mechanism found -- route before widening.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after">
    <step>
      <run>Leg 1 report -> CTO cc COO (the Andrew package input); Leg 2 closes on the next scheduled cycle's frontier advance</run>
      <expect>Day-list complete-within-available-data; frontier advances without hand-runs.</expect>
      <if_mismatch>A Leg-2 close on a hand-run is REWORK (NEVER#4).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Leg 1's day-list is the last input to CTO's Andrew package (the double-count half is already
complete-within-available-data per 0.2.0's 42-partition census -- cite, do not redo). Leg 2
changes silver-tier production: cot firm-separation binds; the LAG=1 fix you already deployed
is upstream of the same converter -- note the interaction in the fix commit if any.
</cross_domain_coordination>

<acceptance_criteria>
1. Leg 1: denominator + day-list + per-artifact serve-moment determination + UNKNOWNs with
   reasons; complete-within-available-data stated; routed to CTO cc COO.
2. Leg 2: mechanism cited; fix deployed MATCH; next scheduled cycle advances the frontier
   (no hand-runs in evidence).
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="ruling">CTO 20260803T232535Z items (b-ii) + (c)</ref>
  <ref type="evidence">Your outcome-B report 232021Z + @bf4c0aabbe (the LAG fix + measured partials)</ref>
  <ref type="bounds">MEMORY standing: validation scopes to the serve window (2024-11+)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
