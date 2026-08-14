# TO MDPF_TRGALN.TO-6 — Inflection surgical backfill of truth-table MISSING dates + re-publish

<task_order id="MDPF_TRGALN.TO-6" project="MDPF_TRGALN">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T05:1xZ (PRD v1.1 addendum @f50ee7223b)</issued>
<status>pending</status>
<priority>P0 — STAGED. GO comes ONLY from COO, citing (1) TO-5's per-date truth table delivered +
validated and (2) COO's routing check: if the truth table names a REGRESSION-AT-COMMIT/CUTOVER
requiring a CODE change to the builder, that code fix routes to DS per Rule 13 FIRST and this TO's
scope narrows to the run+republish mechanics. Completes TONIGHT per §8.2.</priority>

<dependencies>
  <dependency agent="TO-5 owner (per MSTR allocation)" task="MDPF_TRGALN.TO-5 atom_decomp truth-pass — per-date truth table (TRUE-ZERO | MISSING-AT-SURFACE-X | REGRESSION-INTRODUCED-AT-Y), mechanism of the 7 fully-empty dates named" status="pending"/>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_TRGALN TO-0..TO-3 applied + proofed (the §8.2 gate)" status="pending"/>
</dependencies>

<references>
  <ref type="prd">docs/architecture/MDPF_TRGALN_PRD.md v1.1 @f50ee7223b — §8.2 (this workstream), §8.3 (close bar), §7 (proof schema)</ref>
</references>

## SCOPE (PRD §8.2, verbatim discipline)

Surgical backfill of EXACTLY the dates the TO-5 truth table marks **MISSING** — NEVER a TRUE-ZERO
date (a TRUE-ZERO is correct history; "fixing" it fabricates data). Mechanics: re-emit the affected
dates through the CANONICAL builder (`dim_mdpf_aggregate_aua_timeseries.build_inflection_artifact`
+ carry-forward union logic — the existing production path, no new code path, no shadow builder),
then publisher re-publish.

⛔ **ROLL-FORWARD IS FALLBACK-ONLY AND REQUIRES ANDREW'S EXPLICIT WORD FIRST** (his stated
preference is surgical — PRD §8 verbatim). If surgical backfill cannot be provided for a date,
that date routes to COO → Andrew as a fork; do NOT roll forward on your own initiative.

Known context for the pass (test, don't assume): 2026-08-05 is also the platinum-cutover
carry-forward date. The 7 fully-empty dates: 2026-05-20, 05-29, 06-30, 07-10, 07-13, 07-14, 08-05.

## VALIDATION (PRD §8.2 verbatim)

Re-read of the served series: empty-date list == ∅ minus adjudicated TRUE-ZEROs; plus a
rendered-chart check (stacked bars display for the backfilled dates). No alarms/monitors built;
the reads are artifact reads.

<compiler_tools_mandate>
  <phase id="1" when="before any re-emit">
    <step><run>comp-pipescript io dim_mdpf_aggregate_aua_timeseries --pipeline mdpf + comp-blast on the builder fn</run>
    <expect>Column/consumer map current; blast radius carries no consumer that would double-ingest a re-emitted date.</expect>
    <if_mismatch>STOP; surface to COO.</if_mismatch></step>
  </phase>
  <phase id="3" when="after re-publish">
    <step><run>live read of served platinum/mdpf/inflection/aggregate-aua-timeseries.json + rendered-chart check</run>
    <expect>Every truth-table MISSING date now populated; TRUE-ZERO dates untouched; as_of unchanged by the backfill (backfill fills history, it does not advance the frontier).</expect>
    <if_mismatch>Surface to COO with the per-date delta; no roll-forward without Andrew's word.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<proof_of_spec>
Path: org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_TRGALN/proof_TO-6.json per PRD §7.
Claims = per-date backfill results (one claim per truth-table MISSING date: expected = populated
via canonical builder; desired = truth-table entry; applied = builder/publisher run evidence;
exercised = served re-read value). TRUE-ZERO dates listed as explicitly untouched.
</proof_of_spec>

<acceptance_criteria>
1. Every truth-table MISSING date populated in the served series; ZERO TRUE-ZERO dates modified.
2. Canonical builder + existing publisher only — no new paths, no shadow emitters, nothing standing.
3. Rendered-chart check performed and reported.
4. Any un-backfillable date routed to COO→Andrew as a fork; no roll-forward without his word.
5. No alarms/monitors/SNS/SES.
</acceptance_criteria>
</task_order>
