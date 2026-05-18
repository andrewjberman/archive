<task_order>
  <metadata>
    <id>MDPF_ASSETS.010</id>
    <slug>dsa-wse-49f-non-model-aua-residual</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO) to DS~A. WS-B (MDPF_ASSETS.007) Phase 0+1+2 is complete -- model_aua(49financial) = $1,360,250,355 is computed + verified. WS-E builds now: the gold script (Schwab crosswalk + the residual) can be built + verified LOCALLY immediately, exactly as WS-B was. The S3-landing step + the contract §7 model_aua_input cross-check (which reads model_aua_positions from S3) gate on the opal-data-mdpf bucket -- MDPF_ASSETS.012 (AE 0.5.0); WS-E's S3 upload + final verification land concurrent with WS-B's --upload when the bucket exists.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF Phase 2. WS-E produces Cohort 1b (49F non-model AUA) -- the live-residual replacement for today's frozen ~$271M plug.</priority>
    <sla>1.5-2d wall -- the Schwab-custody crosswalk is already built (the .001 audit); WS-E builds it into the gold layer + computes the residual.</sla>
  </metadata>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md (RATIFIED) -- §4 IS THE SPEC. WS-E emits the non_model_aua artifact, one row per (firm_id, as_of_date): non_model_aua = partner_custody_total − model_aua_input. For 49F: partner_custody_total = certified_aua restricted to Schwab-custodied accounts; model_aua_input = model_aua(49financial) from WS-B; custody_scope = schwab_only; method e.g. 49f_schwab_custody_minus_smartx_model. The 15-account / $7.3M unmatched-custodian bucket stays EXCLUDED from partner_custody_total (not-confirmed-Schwab) until the crosswalk resolves it. §7: the aggregation script asserts non_model_aua.model_aua_input == Σ model_aua_positions.model_value for the same (firm_id, as_of_date) -- a mismatch is a stale/cross-date residual = ERROR.</contract>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.4) -- section 3.0 (49F = Cohort 1; 1b = non-model AUA, this TO), section 3.4, section 4 WS-E.</prd>
    <custody_ruling>Andrew direct 2026-05-18: Opal advised AUA = SCHWAB-CUSTODIED ONLY. 49F's custody book splits cleanly two ways -- model + non-model -- with NO excluded category. All Schwab-custodied 49F assets not in an Opal model are Cohort 1b. The ~$283M on the SmartX platform in non-Opal models IS Cohort 1b, counted in full.</custody_ruling>
    <built_basis>docs/briefs/mdpf-49f-nonmodel-custody-cutout-audit-20260518.md (MDPF_ASSETS.001, DS~A) -- the audit. certified_aua = Σ silver/allocations.account_market_value minus 3 liability types (E_19), reproduced to the cent ($1,812,432,585.32 for 2026-05-14). The account_id→billing_account_custodian crosswalk was built off all 1,855 silver/fees partitions (3.3M rows, 0 conflicts, custodian stable per account). Schwab-custodied certified_aua = $1,655.4M. DS~A's implementation note: the crosswalk must be rebuilt from full silver/fees history each gold run (custodian is stable + cheap); the 15-acct/$7.3M unmatched bucket stays excluded until a fee event classifies each.</built_basis>
    <validation_ref>WS-A contract Appendix A: 49F Schwab custody ~$1,682.52M (2026-05-15) − 49F model AUA ~$1,360.27M ≈ non_model_aua(49financial) ~$322M. WS-E's residual must land near this.</validation_ref>
  </references>

  <context>
    WS-E produces Cohort 1b -- 49 Financial's non-model AUA -- replacing today's frozen ~$271M plug with a live daily residual. Per Andrew's Schwab-only ruling and the ratified contract §4, non_model_aua(49financial) is NOT independently sourced: it is the residual

      non_model_aua(49financial) = partner_custody_total(49financial) − model_aua(49financial)

    where partner_custody_total = certified_aua restricted to Schwab-custodied accounts, and model_aua(49financial) comes from WS-B. The .001 audit already built and validated the account→custodian crosswalk; WS-E's job is to build that crosswalk into the gold layer, compute partner_custody_total (Schwab-include filter), and emit the non_model_aua residual artifact.

    HARD DEPENDENCY: WS-E's residual requires model_aua(49financial) from WS-B (.007) for the SAME (firm_id, as_of_date). The contract §7 model_aua_input consistency check gates it -- non_model_aua.model_aua_input MUST equal Σ model_aua_positions.model_value for that partner/date. WS-E does not run its residual step until WS-B's model_aua is live. (Both TOs are DS~A's lane -- WS-B first, then WS-E -- so the sequencing is within one lane.)
  </context>

  <scope>
    <step>Phase 1 -- the Schwab-custody crosswalk in the gold layer. Build the account_id→billing_account_custodian crosswalk (the .001 method: scan full silver/fees history; custodian is stable per account, 0 conflicts) into the WS-E gold script -- rebuilt each run per DS~A's .001 implementation note. Compute partner_custody_total(49financial) = certified_aua (Σ silver/allocations.account_market_value minus the 3 E_19 liability types) restricted to Schwab-custodied accounts via the crosswalk. The 15-account / $7.3M unmatched-custodian bucket is EXCLUDED (not-confirmed-Schwab) -- carry it as a named, surfaced exclusion, not a silent drop.</step>
    <step>Phase 2 -- the non_model_aua residual artifact. Emit the contract §4 non_model_aua artifact for firm_id=49financial: non_model_aua = partner_custody_total − model_aua_input, with partner_custody_total + model_aua_input + method + custody_scope=schwab_only + source_pipeline carried for audit reproducibility. model_aua_input = model_aua(49financial) read from WS-B's model_aua_positions for the matching as_of_date. Land in the opal-data-mdpf feeder prefix (coordinate the bucket with AE -- ruling vi).</step>
    <step>Phase 3 -- verify. non_model_aua(49financial) must land near the Appendix-A reference (~$322M = ~$1,682.52M Schwab − ~$1,360.27M model; date offset expected). Confirm the §7 model_aua_input check passes -- non_model_aua.model_aua_input == Σ model_aua_positions.model_value(49financial) for the same date. Confirm the 15-acct/$7.3M bucket is excluded and surfaced. Record the verified residual + its two inputs.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io on the WS-E gold script (the silver/allocations + silver/fees reads) -- COLUMN GAPS check.</run>
        <expect>account_market_value, the E_19 liability fields, and billing_account_custodian are all loaded -- no column accessed-but-not-loaded.</expect>
        <if_mismatch>Reconcile the load set against the .001 audit's field inventory before building.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-validate on the WS-E gold script against the emitted non_model_aua artifact (if a gold_validate_config entry applies); comp-blast on the WS-E function.</run>
        <expect>The residual artifact is well-formed; blast radius is the opal-data-mdpf feeder only.</expect>
        <if_mismatch>Debug before close.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>WS-E is a NEW gold script emitting a NEW convergent artifact (non_model_aua) to opal-data-mdpf. It READS silver/allocations + silver/fees (existing); it modifies no producer and rewrites no existing artifact. No reprocessing. (Note: WS-E replaces the FROZEN non_model_assets.json plug as the aggregate's non-model source -- but that swap is a WS-F/portal wiring concern, not a WS-E reprocess.)</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    WS-E ↔ WS-B: HARD dependency -- WS-E's residual requires WS-B's model_aua(49financial). Both are DS~A's lane; WS-B (.007) closes first. The §7 model_aua_input check enforces same-date consistency. WS-E ↔ the 49F silver tier: WS-E READS silver/allocations + silver/fees -- it does not modify them (Rule 17: no silver-side field slimming; WS-E reads, the crosswalk + filter are gold-tier business logic, correctly placed). AE finalizes the opal-data-mdpf bucket -- coordinate. WS-E does NOT touch the legacy non_model_assets.json plug -- superseding it is a Phase-3 WS-F wiring decision.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The account_id→custodian crosswalk is built into the WS-E gold script (rebuilt from full silver/fees history each run); partner_custody_total(49financial) = certified_aua restricted to Schwab-custodied accounts is computed.</ac>
    <ac id="AC2">The non_model_aua artifact ships for firm_id=49financial per contract §4 -- the residual with partner_custody_total + model_aua_input + method + custody_scope=schwab_only carried for audit. The 15-acct/$7.3M unmatched bucket is excluded and surfaced as a named exclusion.</ac>
    <ac id="AC3">Verified: non_model_aua(49financial) lands near ~$322M (Appendix-A reference); the §7 model_aua_input check passes (model_aua_input == Σ model_aua_positions.model_value for the same firm/date).</ac>
    <ac id="AC4">No emoji; ds-commit-gate exit 0; Rule 15 (from __future__ import annotations first); Rule 17 (no silver-side modification -- WS-E reads silver, business logic is gold-tier); session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The WS-E gold script: the Schwab-custody crosswalk + partner_custody_total + the non_model_aua residual artifact for firm_id=49financial.
    - Session log with the Compiler Tools section + the verified residual and its two inputs. RAVC2 to COO.
  </deliverables>
</task_order>
