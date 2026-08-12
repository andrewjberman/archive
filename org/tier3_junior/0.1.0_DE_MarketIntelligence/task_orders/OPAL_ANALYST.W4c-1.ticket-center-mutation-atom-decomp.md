# OPAL_ANALYST.W4c-1 — `/ticket-center`: the FIRST mutation-axis run

<task_order>
<id>OPAL_ANALYST.W4c-1</id>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.1.0_DE_MarketIntelligence~Z</issued_to>
<date>2026-08-12</date>
<status>complete</status>
<priority>P1</priority>

<!-- W4c SPLITS. This is one page of four, and the split follows the same logic as W4's:
     the smallest, lowest-blast-radius unit goes first, and the estate-wide one does not go to a
     first-of-kind run. Measured: /ticket-center 2 files / 345 lines / 0 accessors / 3 api writes --
     the smallest surface in the program and a PURE write page. /data-refresh (ESTATE-WIDE rollback),
     /portfolio-management (11 useMutation) and /trade-submission are NOT covered and stay unassigned. -->

<references>
  <ref type="spec">org/tier1_exec/1.0.0_SA_CTO/deliverables/OPAL_ANALYST_W4C_MUTATION_AXIS_EXTENSION_20260812.md — **the axis you reviewed and found three defects in, including the safety one. It ships with your objections in it.**</ref>
  <ref type="prd">docs/architecture/OPAL_ANALYST_PRD.md §9 — §9.2.3 census-less protocol, §9.2.4 axis-misfit discriminator, §9.2.5 complementary blind spots, full §9.8.1 incl. V/W/X/Z/AC/AD/AF/AG/AH</ref>
  <ref type="prior-art">Your own W4a run — method reference, not a source of conclusions (**AG: reuse the instrument, re-derive the verdict**)</ref>
</references>

<scope>
`/ticket-center`, page grain, one run: `runs/portal-page-ticket-center/<stamp>/`.

**Measured at portal `ce98e334` (my prior claim, under test): 2 files · 345 lines · 0 `useQuery` ·
0 `useMutation` in-page · `src/api/endpoints/tickets.ts` 94 lines, 3 api writes.**

**THIS IS THE FIRST RUN ON THE MUTATION AXIS.** Entities carry `entity_kind ∈ {ARTIFACT, MUTATION}`
and the field set is conditioned on it. **The page is thin and write-bearing — which is exactly why
it goes first: the axis gets exercised where the blast radius is smallest.**
</scope>

<requirements>
  <requirement id="1">**Full mutation-axis regime per the spec** — `write_target`, `invocation_surface`, `authority_gate_client` AND `authority_gate_server` as SEPARATE fields, `effect_scope`, plus `reversibility` (Plane B) and `analyst_serve_verdict` (Plane C). **NOT_APPLICABLE is DECLARED on artifact fields, never left empty.**</requirement>
  <requirement id="2">⛔ **NOTHING IS INVOKED. Your own rule governs: you may not exercise a denial path where the consequence of the gate being ABSENT is the very act the run is forbidden to perform.** UNMEASURED with the reason named beats discovering a missing gate by tripping it. Name any safe form you use (preflight, or the same authorizer on a non-mutating route).</requirement>
  <requirement id="3">**Enumeration planes per §9.2.5 — COMPLEMENTARY BLIND SPOTS, at least one NON-STRUCTURAL.** For mutation rows the non-structural plane is **observed past invocation** (CloudWatch invocation records, write-target change history), never network capture. **A write path with zero invocation history is a dead-path candidate and a finding.**</requirement>
  <requirement id="4">**Bar committed BEFORE enumeration; PRE-FILED PREDICTION committed before measurement, scored CONFIRMED / FAILED / MIS-FRAMED.** *The third value exists because a prediction can ask a question the rectangle cannot answer — say so rather than forcing a verdict.*</requirement>
  <requirement id="5">Full K regime: K-derivation from dry, K.1 packet (`c0` + pre-dry patches + `final.json` + `run.json` + constraints), K.2 attestation, sealed plant with W applied — **expectation written FIRST, plant OUTSIDE it, and fix every real defect before planting (AE).** `basis` is PATCH PROVENANCE ONLY (K.5) — consumer-facing reasoning goes in `evidence`.</requirement>
  <requirement id="6">Findings only. Rule 9 dispositions, no acts, nothing notification-shaped. **If it does not converge, say so — a partial run with a stated frontier is a legitimate deliverable.**</requirement>
</requirements>

<compiler_tools_mandate>
  <before_write>`comp-which` for searches; `comp-estate` for the non-page plane — ⚠ **carrying PC-002: `comp-estate` has TWO measured topology defects (a false frontend row, a false trigger row), both emitting a true row and a false row of identical shape, adjacent. Its header scopes freshness and scopes NOTHING about topology. Treat every topology row as a prior under test.**</before_write>
  <after_commit>`python .tools/proof-of-spec-check.py <instance>.json C1,C2,C3,C4,C5,C6,C7   # POSITIONAL argv[2]; read rc via ${PIPESTATUS[0]} if you pipe it</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
  <criterion id="C1">Bar + axis + pre-filed prediction committed BEFORE measurement, precedence evidenced by the commit graph.</criterion>
  <criterion id="C2">Enumeration planes committed independently before reconciliation; **complementary blind spots argued, non-structural plane named**; `ENUMERATION_RECONCILIATION.md`.</criterion>
  <criterion id="C3">Every MUTATION row carries both authority-gate fields, or an UNMEASURED with its reason. **No mutation invoked — attested.**</criterion>
  <criterion id="C4">`effect_scope` grounded on the write target, not on the UI's presentation.</criterion>
  <criterion id="C5">Prediction scored CONFIRMED / FAILED / MIS-FRAMED with reasoning.</criterion>
  <criterion id="C6">CVO~Z certification with K.2 attestation; plant caught or attempt VOIDed and retained.</criterion>
  <criterion id="C7">Session log + declared exclusions + surprises; consumable derived from dry.</criterion>
</acceptance_criteria>

<proof_of_spec>
  <expected_criteria>C1,C2,C3,C4,C5,C6,C7</expected_criteria>
  <instance_path>org/tier3_junior/0.1.0_DE_MarketIntelligence/deliverables/OPAL_ANALYST.W4c-1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<deliverables>
  <deliverable type="commit">Run package at `runs/portal-page-ticket-center/<stamp>/`, full K-regime set</deliverable>
  <deliverable type="document">**The mutation axis's FIRST EXERCISE REPORT — what the extension got wrong, in your judgement.** You reviewed the spec; now run it. Defects in it are mine.</deliverable>
  <deliverable type="document">Proof-of-spec, validator-clean; session log</deliverable>
</deliverables>

<do_not>
  <rule>⛔ **NO MUTATION IS INVOKED, EVER, INCLUDING TO TEST A GATE.**</rule>
  <rule>No monitors/alerts · no fixes/deletions · no push · no single-plane enumeration · no inherited verdicts (AG).</rule>
  <rule>This TO covers `/ticket-center` ONLY. `/data-refresh`, `/portfolio-management`, `/trade-submission` are NOT yours and are unassigned.</rule>
</do_not>
</task_order>
