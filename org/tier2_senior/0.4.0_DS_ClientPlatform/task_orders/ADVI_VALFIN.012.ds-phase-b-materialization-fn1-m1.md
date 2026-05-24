<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-05-23-valfin-012-phase-b-materialization</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-23</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_VALFIN</project_code>
    <priority>P2 -- VALFIN-001 Phase B materialization per Andrew sovereign ruling (LD-0025); Path B = fee-STATUS bools. Sequencing-gated on LD-0018 F1 fix (.010); not blocking active critical path but downstream-of-F1.</priority>
    <sla>~2-4h wall (M-1 probe + FN-1 doc deliverables; no DE-lane portal swap in this TO scope).</sla>
    <!-- GO ON AUTHOR by 2.0.0_SA_COO base 2026-05-23T21:45Z UTC. Andrew sovereign
         ruling per LD-0025: Path B (fee-STATUS bools) ratified via CVO CORROBORATE
         backstop (verdict file: cvo_loop_1801Z_LD0024_path_b_verdict.md). LD-0024
         (MSTR mechanical fee-rate-values pick) SUPERSEDED.

         MSTR-side framework miss banked: M-1 META yellow-flag was meant as
         additive consideration not counter; LD-0025 corrects + folds M-1 probe
         into materialization design as pre-check rather than gate. -->
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_PRODUCT_VALIDATION.md (v0.1)</prd>
    <ld_charter>org/tier0/ledger/LD-0025.md (Andrew sovereign correction; supersedes LD-0024)</ld_charter>
    <cvo_corroborate_verdict>org/tier1_exec/3.0.0_SA_CVO/logs/2026-05-23/cvo_loop_1801Z_LD0024_path_b_verdict.md (commit 4a929b29c)</cvo_corroborate_verdict>
    <upstream_dependency>ADVI_VALFIN.010 (INF_C_09 placeholder-zero filter fix; F1 sequencing gate)</upstream_dependency>
    <sibling_doc>ADVI_VALFIN.011 (INF_C_09 PHASE-2-STAGED doc; will be updated by this TO to reference Phase B/C consumer rather than purely Phase-2-staged)</sibling_doc>
    <field_rename_sibling>ADVI_VALFIN.008 Phase B portal type rename (capital_gains_ttm -> unrealized_gain_change_ttm); banked pending DE pod-4 re-spawn LD-0014; SEPARATE from this TO's scope</field_rename_sibling>
  </references>

  <objective>
    Materialize VALFIN-001 Phase B per Andrew sovereign ruling (Path B = fee-STATUS bools consumption). Two thrusts: (M-1 PRE-CHECK) empirically confirm that the Phase B portal type swap actually consumes fee-status bools (vs fee-independent); (FN-1 DELIVERABLES) document the cascade implications + display-contract + audit population-shift + update .011's INF_C_09 docstring reference. NO DE-lane portal type swap in this TO -- that stays banked under .008 Phase B pending DE pod-4 re-spawn.
  </objective>

  <context>
    LD-0025 (Andrew sovereign correction landed via CVO CORROBORATE backstop) ratified Path B (fee-STATUS bools) for VALFIN-001 Phase B. LD-0024 (MSTR mechanical fee-rate-values pick) superseded.

    CVO's verdict carries TWO bundled enhancements that materialize here:

    FN-1 (Forward-Looking Notes, verbatim from CVO verdict):
      "When LD-0024 materializes... materialization TO should explicitly include:
       - F1 sequencing gate (CVO will signal on re-probe)
       - display-contract for hold-backward imputation (69% state-change population means silent display would mislead)
       - audit-table population-shift documentation
       - INF_C_09 docstring update from F2 (c) materialization TO already in COO lane (should now reference Phase B/C consumer, no longer purely Phase-2-staged)"

    M-1 (META yellow-flag, demoted from gate to pre-check):
      "Phase B/C may be empirically fee-independent; charter empirical-consumption-probe before materialization?"

    Andrew's correction: M-1 was meant as additive consideration, not counter to CVO CORROBORATE. So M-1 folds into materialization as a PRE-CHECK -- DS Base empirically confirms Phase B consumes fee-status bools at pickup time; if probe reveals fee-independent, surface back to MSTR for Path C swap.
  </context>

  <scope>
    <in_scope>
      PHASE A -- M-1 EMPIRICAL PRE-CHECK (BEFORE any other deliverable):

        Confirm Phase B portal type swap empirically consumes fee-status bools (vs fee-independent). Mechanism:

        1. Identify which portal consumer files reference the Phase B target type (look at portal/src/pages/AdvisorIntelligence/_shared/ types.ts + downstream components per VALFIN.001 Phase-3 brief 5365d96f2).
        2. Grep for any consumption of `is_fee_earning`, `fee_status`, or related boolean flags downstream of the renamed types.
        3. Two outcomes:
           - CONFIRMED fee-status bool consumption -> PROCEED to Phase B FN-1 deliverables.
           - EMPIRICALLY fee-independent (no fee-status bool consumption found) -> SURFACE BACK to COO + MSTR via RAVC2 with the grep evidence; Path C swap candidate; HALT materialization until MSTR re-rules.

      PHASE B -- FN-1 DELIVERABLES (conditional on PHASE A confirming Path B):

        DELIVERABLE A -- F1 sequencing gate documentation.
          Document that VALFIN.010 F1 fix MUST be RAVC2-accepted (CVO re-probe of fee_status_audit.parquet shows 0% wrong first_known_fee_status_date) BEFORE any Phase B consumer activates. Capture in the materialization brief as the upstream gate.

        DELIVERABLE B -- Display-contract for hold-backward imputation.
          69% of accounts have state-change population per CVO audit-table empirical shape. Silent display of imputed-vs-actual fee-status would mislead users. Document the display contract: when a consumer renders fee-status, it MUST distinguish actual-observation vs hold-backward-imputed (e.g. tooltip, footnote, separate visual treatment, or explicit data-quality field). Concrete options listed; final visual treatment is RD/DE call when DE re-spawns.

        DELIVERABLE C -- Audit-table population-shift documentation.
          The audit table's population shifts: pre-LD-0018-F1-fix = 61% wrong placeholder dates; post-fix = 0%. Downstream consumers reading historical snapshots need awareness of this shift. Document as a note in the materialization brief + a docstring reference in INF_C_09.

        DELIVERABLE D -- INF_C_09 docstring update (modifies .011's output).
          .011's PHASE-2-STAGED block currently says "Phase-2-staged pending Andrew product-strategy call on consumer wiring." Update that block to reference: "Phase B materialization (Path B = fee-STATUS bools) materializing via ADVI_VALFIN.012; no longer purely Phase-2-staged. Consumer = portal AdvisorBookView + ClientsTab fee-status display. F1 sequencing gate per VALFIN.010 fix."

        DELIVERABLE E -- Materialization brief (~50-100 lines).
          Doc-of-record at docs/briefs/advi-valfin-012-phase-b-materialization-20260523.md capturing: Andrew ruling LD-0025 + Path B + FN-1 enhancements + M-1 pre-check outcome + display-contract options + audit population-shift impact + cross-refs to .010/.011/CVO verdict.

      PHASE C (post-materialization): RAVC2 to COO + CC CVO + reference LD-0025 charter.
    </in_scope>
    <out_of_scope>
      - The .008 Phase B portal type rename (capital_gains_ttm -> unrealized_gain_change_ttm in DE-lane TypeScript files) -- BANKED pending DE pod-4 re-spawn (LD-0014). This TO is the DS-side materialization documentation; the DE-side portal type swap is a future TO when DE returns.
      - Wiring a new consumer (Lambda billing aggregator or FE historical reporting) -- that's the LD-0018 F2 (a) product question Andrew has separately surfaced; not in this TO.
      - INF_C_09 logic changes (filter is .010 F1 scope; this is doc-only).
      - .010 / .011 sibling TOs unchanged in scope.
      - Display visual-treatment final-pick -- that's RD/DE judgment when they re-spawn; this TO documents the OPTIONS, not the final pick.
    </out_of_scope>
  </scope>

  <cross_domain_coordination>
    Lead: 0.4.0_DS_ClientPlatform (DS pod-4 base; if your queue is on the .010/.011 absorbed bundle via DS~C, DS Base picks this up separately; the M-1 pre-check + FN-1 deliverables are doc-focused not infra-touching).
    Coord with CVO: CVO will re-probe fee_status_audit.parquet post-.010 RAVC2-accept; their signal IS the F1 sequencing gate (DELIVERABLE A trigger). CVO already has the probe pattern from LD-0018 verify-channel.
    Coord with .011 author (also DS): the docstring update in DELIVERABLE D modifies .011's output; coordinate so both land cleanly.
    DE pod-4 NOT IN scope (killed per LD-0014).
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before write (M-1 probe)">
      <step>
        <run>(M-1 PRE-CHECK) grep -rE "is_fee_earning|fee_status|fee_data_available" portal/src/pages/AdvisorIntelligence/_shared/</run>
        <expect>Either: matches in types.ts + downstream consumers (CONFIRMS Path B fee-status bool consumption) OR no matches (EMPIRICALLY fee-independent).</expect>
        <if_mismatch>HALT this TO. Surface back via RAVC2 with grep evidence for MSTR Path C re-rule.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse fee_status_audit (audit-table consumers from gold-script side)</run>
        <expect>Per CVO verdict: ZERO downstream consumers in current state. If new consumers appear, fold into materialization brief.</expect>
        <if_mismatch>STOP. New consumer = scope-change; surface to COO before continuing.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before write (FN-1 deliverables, conditional on PHASE A pass)">
      <step>
        <run>cat .010 + .011 TO files for cross-reference consistency</run>
        <expect>.010 F1 fix scope unchanged; .011 PHASE-2-STAGED block reads as expected (will be updated by DELIVERABLE D of this TO).</expect>
        <if_mismatch>STOP. If .010/.011 contents have shifted since this TO authored, surface to COO for re-scope.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>aws s3 ls s3://opal-data-inf/gold/views/fee_status_audit.parquet --LastModified post-F1-fix-ratify</run>
        <expect>Audit table reflects .010 F1 fix landed; CVO has signaled re-probe clean.</expect>
        <if_mismatch>HALT. F1 sequencing gate not met; do not declare materialization complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <ac id="AC1">PHASE A M-1 pre-check executed; outcome (Path B confirmed OR fee-independent surface) documented with grep evidence.</ac>
    <ac id="AC2">DELIVERABLE A: F1 sequencing gate documented (VALFIN.010 RAVC2-accept gating Phase B consumer activation).</ac>
    <ac id="AC3">DELIVERABLE B: display-contract for hold-backward imputation documented; concrete options enumerated; final visual-treatment pick deferred to RD/DE.</ac>
    <ac id="AC4">DELIVERABLE C: audit-table population-shift (61% -> 0%) documented with downstream-consumer awareness note.</ac>
    <ac id="AC5">DELIVERABLE D: INF_C_09 docstring updated to reference Phase B Path B consumer + VALFIN.012 + F1 sequencing gate (modifies .011's previously-Phase-2-staged framing).</ac>
    <ac id="AC6">DELIVERABLE E: materialization brief at docs/briefs/advi-valfin-012-phase-b-materialization-20260523.md captures all of the above + cross-refs.</ac>
    <ac id="AC7">Session log + Compiler Tools section reproducing each &lt;run&gt; with observed output + pass/fail.</ac>
    <ac id="AC8">RAVC2 to COO + CC CVO + cite LD-0025 charter; if M-1 surfaces fee-independent, that's the RAVC2 substance instead.</ac>
  </acceptance_criteria>

  <not_authorized>
    - DE-lane portal type swap (.008 Phase B) -- banked pending DE re-spawn.
    - Wiring new consumers (LD-0018 F2 (a) Andrew product question).
    - INF_C_09 logic changes (this is doc-only).
    - Acceptance flex on AC1 (M-1 pre-check empirical) -- the pre-check IS the bundle gate.
    - Acceptance flex on AC2 (F1 sequencing gate) -- VALFIN.010 must RAVC2-accept first or downstream materialization is premature.
  </not_authorized>
</task_order>
