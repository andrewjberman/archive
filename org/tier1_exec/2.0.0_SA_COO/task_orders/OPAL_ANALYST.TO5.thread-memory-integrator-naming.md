# OPAL_ANALYST.TO5 — Thread-memory integrator naming

<task_order>
<id>OPAL_ANALYST.TO5</id>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued_to>2.0.0_SA_COO~Z</issued_to>
<date>2026-08-10</date>
<status>pending</status>
<priority>P2</priority>

<references>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §4.5, §6 TO-5 (v1.0 @d179643ca)</ref>
</references>

<scope>
0.0.3_BG's prompt.md/README says "integrators sweep [threads/ + logs/] into git if wanted" but
names nobody — an unnamed integrator is a sweep that never happens. Decision (per PRD rec, COO
assignment authority): **0.0.0_AB_MSTR~Z is the named integrator** — they already integrate
SITEZ→CLOUD at :55 and hold the box. Execution: (1) message MSTR~Z requesting acceptance of the
role; (2) on acceptance, MSTR~Z lands the one-line naming edit in the 0.0.3_BG agent-home
integrator line during their integration window (their file domain — COO does not edit it).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before send">
    <step>
      <run>Grep the agent home for the integrator line (README.md/prompt.md) to cite exactly</run>
      <expect>The "integrators sweep them" line located with file:line for the request message.</expect>
      <if_mismatch>Re-read PRD §4.5; if the line moved, cite its current home.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination><none/> — one message + one line in a file owned by the accepting seat.</cross_domain_coordination>

<acceptance_criteria>
1. MSTR~Z acceptance on record (broker reply).
2. Naming edit landed by MSTR~Z; 08-07 session thread/log records present in git after the next
   integration window.
</acceptance_criteria>
</task_order>
