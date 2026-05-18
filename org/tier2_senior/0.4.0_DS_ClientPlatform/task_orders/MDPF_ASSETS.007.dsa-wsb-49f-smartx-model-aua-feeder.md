<task_order>
  <metadata>
    <id>MDPF_ASSETS.007</id>
    <slug>dsa-wsb-49f-smartx-model-aua-feeder</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-18</date>
    <status>in-progress</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-18 (COO) to DS~A -- MDPF Phase 2. WS-A contract is ratified; WS-B is authorable. NOTE: WS-B carries a genuine Phase-0 feasibility gate (per-account 49F model membership) -- it is dispatched GO because the Phase-0 assessment is real work that must happen regardless; if Phase 0 finds account-grain infeasible, DS~A STOPS and surfaces to COO before Phase 1.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF Phase 2. WS-B is Cohort 1a (49F model AUA) and the §4 residual's subtrahend -- WS-E (Cohort 1b) cannot compute non-model until WS-B's model_aua exists. WS-B is sequenced FIRST of the 49F pair.</priority>
    <sla>Phase 0: 1d. Phase 1-2: 2-3d if account-grain is feasible -- re-sized at the Phase-0 gate.</sla>
  </metadata>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md (RATIFIED) -- THE SPEC. WS-B emits two convergent artifacts: model_aua_positions (§3.1, account grain) + model_composition (§3.2, model x ticker grain), both firm_id=49financial. model_key per the §2 registry (data/mdpf/scripts/gold/mdpf_model_registry.json) -- WS-B CONFIRMS the provisional SmartX long-term-tier name alignment (contract §2 note + §9 ruling vii). model_value = account-decomposable value, NOT a cached headline (ruling ii). Feeder parquet lands in the non-portal opal-data-mdpf bucket (ruling vi) -- AE finalizes the bucket; coordinate.</contract>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.4) -- section 3.0 cohort taxonomy (49F = Cohort 1; 1a = model AUA, this TO), section 4 WS-B, section 6.1 (new SmartX-AUA work lands as MDPF TOs).</prd>
    <feeder_project>SXPL_RESTIN -- the SmartX REST integration. STATE (per SXPL_RESTIN.json): TO-1 (per-model availability matrix) COMPLETE -- docs/briefs/smartx-per-model-availability-matrix-20260515.md, 7 modelIds resolved, daily-snapshot model (no historical-holdings endpoint). TO-2 (the pull flow, AE 0.5.0) dispatched. TO-3+ (silver/gold modeling) NOT yet authored. Two open blockers: the data/smartx/ owned-paths lane registration (POD3 vs Pod-4 DS work -- routed to CTO) and a soak-safety hold (REST pull must write a shadow path, not the canonical EC2-exporter path).</feeder_project>
    <validation_ref>WS-A contract Appendix A -- the 49F 7-cohort reference set ($M, 2026-05-15): opal_ultra_short_term 52.70, opal_short_term 104.10, opal_intermediate 283.22, opal_long_term_conservative 686.74, opal_long_term_aggressive 208.90, opal_div_sma 19.51, opal_growth_sma 5.10 -- 7-cohort total model_aua(49financial) ~= $1,360.27M. WS-B's output must land near this.</validation_ref>
  </references>

  <context>
    WS-B feeds Cohort 1a -- 49 Financial's model AUA -- into the MDPF canonical schema. 49F's models run on the SmartX managed-account platform; the 7 Opal cohorts (5 core models + Dividend SMA + Opal Equity Growth SMA) are SmartX models.

    THE STRUCTURAL RISK (analyze at Phase 0). The WS-A contract's model_aua_positions artifact is ACCOUNT-grain -- one row per (firm_id, model_key, account_id, as_of_date) with per-account model_value. PRD named-gap-2 already flagged that 49F "model_aua is a SmartX scalar, not account-keyed to BD" -- i.e. the SmartX data seen so far is per-MODEL totals, not per-account. To emit account-grain WS-B needs per-account model membership: which 49F account is in which Opal model, with that account's market value. Black Diamond silver (silver/allocations, used by the .001 custody audit) has 49F account-grain market values but NO model tag; SmartX has the model assignment. Whether SmartX (REST or the existing exporter) exposes per-ACCOUNT model membership -- not just per-model totals -- is an OPEN question this TO must resolve before building.

    WS-B is sequenced before WS-E: WS-E's non_model_aua residual (Cohort 1b) is partner_custody_total - model_aua(49financial); the contract §7 model_aua_input check gates it. WS-B must ship model_aua(49financial) first.
  </context>

  <scope>
    <step>Phase 0 -- SmartX feeder data-path assessment. Resolve, before any build:
      (a) [DELEGATED -- do NOT redo] The core "does a 49F per-account model-membership mechanism exist" question is now a dedicated DS Base probe, MDPF_ASSETS.011 (Andrew-direct 2026-05-18). WS-B CONSUMES .011's verdict; it does not re-run the SmartX backend probe.
      (b) What does the SmartX feeder produce TODAY -- is SXPL_RESTIN.002's pull flow landing data, where, at what grain? Is the existing EC2 browser-exporter's output usable (it is the proven canonical 49F source, not being decommissioned)?
      (c) The data/smartx/ owned-paths lane blocker status (POD3-registered vs Pod-4 DS work) -- can WS-B commit data/smartx/ or data/mdpf/ code, and where does the SmartX-to-convergent-schema modeling script live?
      DECISION POINT: WS-B Phase 1 proceeds only on a YES verdict from MDPF_ASSETS.011 (account-to-model mechanism confirmed) -- .011's finding defines the data path WS-B builds on. If .011 returns NO, WS-B holds at Phase 0 and the account-grain contract question routes through COO+CTO -- not a silent model-grain downgrade. Record the (b)+(c) findings as a short brief.</step>
    <step>Phase 1 -- build the WS-B feeder (on the Phase-0-confirmed data path). A script that emits, for firm_id=49financial: (a) model_aua_positions -- one row per (model_key, account_id, as_of_date) with model_value (account-decomposable, contract §3.3 / ruling ii), custodian where known, source_pipeline=smartx; (b) model_composition -- one row per (model_key, as_of_date, ticker) with target_weight (decimal 0-1, sums to 1.0 per model), is_opal_etf flagged for DIVZ/IDVZ/PFDE/PFOE. model_key resolved through the §2 registry -- and CONFIRM + correct the provisional SmartX long-term-tier name alignment in mdpf_model_registry.json (contract §2 + ruling vii); a native model absent from the registry emits model_key=null + model_key_unmapped set (never silently dropped). Rule 15 (from __future__ import annotations) if a gold/silver/bronze script; ds-commit-gate exit 0.</step>
    <step>Phase 2 -- land + verify. Write the two artifacts to the opal-data-mdpf feeder prefix (coordinate the exact bucket with AE -- contract §8 / ruling vi). Verify model_aua(49financial) = Σ model_aua_positions.model_value lands near the Appendix-A reference (~$1,360.27M total; the 7 cohorts within a reasonable tolerance -- date offset expected). model_composition target_weights sum to 1.0 per model_key. Record the verified per-cohort numbers in the session log.</step>
  </scope>

  <gate_note>WS-B's model_aua(49financial) is WS-E's required input. On Phase-2 close, notify COO + the WS-E lane (DS~A) that model_aua(49financial) is live so WS-E's residual step can run.</gate_note>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io on any existing SmartX pipeline script WS-B will consume or extend; comp-iam service if WS-B adds a SmartX REST API call with new auth surface.</run>
        <expect>The SmartX data surface + any IAM gap before deploy. If WS-B only reads existing SmartX output, state N/A for IAM in one line.</expect>
        <if_mismatch>Resolve the IAM gap before deploy; reconcile the column surface.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast on the WS-B feeder function</run>
        <expect>Blast radius is the new opal-data-mdpf feeder artifacts only -- no overlap with the live SmartX EC2-exporter canonical path or the INF gold chain.</expect>
        <if_mismatch>If WS-B touches the canonical SmartX path, STOP -- the soak-safety hold (SXPL_RESTIN) forbids a dual-writer on the canonical path. Surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>WS-B is a NEW feeder writing NEW convergent artifacts to opal-data-mdpf; it modifies no existing pipeline producer and rewrites no existing artifact. The SmartX EC2 exporter's canonical output is untouched (soak-safety hold). No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    WS-B ↔ SXPL_RESTIN: WS-B is the 49F-model-AUA modeling that PRD §6.1 routes as an MDPF TO (not a new SXPL_RESTIN TO). It CONSUMES SXPL_RESTIN's pull output; coordinate with the SXPL_RESTIN lane (AE 0.5.0 owns the pull flow) on what the pull produces + where. The data/smartx/ owned-paths blocker is CTO-routed -- if it blocks a WS-B commit, surface to COO (do not force). The SmartX EC2 exporter is the proven canonical source and is NOT decommissioned -- WS-B must NOT write the canonical exporter path (soak-safety hold); it writes the opal-data-mdpf feeder prefix only. AE finalizes the opal-data-mdpf bucket at this TO -- coordinate.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase-0 brief: the 49F per-account model-membership feasibility verdict, the SmartX feeder-state assessment, the data-path + owned-paths decision. If account-grain is infeasible, the TO holds at Phase 0 with the question surfaced to COO+CTO -- that is a valid AC1 close, not a failure.</ac>
    <ac id="AC2">model_aua_positions ships for firm_id=49financial -- account-grain, model_key via the registry, account-decomposable model_value, conformant to contract §3.1.</ac>
    <ac id="AC3">model_composition ships for the 49F Opal models -- (model_key, as_of_date, ticker) grain, target_weight summing to 1.0 per model, is_opal_etf flagged. The provisional SmartX long-term-tier registry alignment is confirmed/corrected (ruling vii).</ac>
    <ac id="AC4">model_aua(49financial) verified near the Appendix-A reference (~$1,360.27M, 7 cohorts). Both artifacts land in the opal-data-mdpf feeder prefix. COO + WS-E lane notified that model_aua(49financial) is live.</ac>
    <ac id="AC5">No emoji; ds-commit-gate exit 0 on every .py edit; Rule 15 where applicable; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The Phase-0 feasibility brief (per-account model membership + feeder-state + data-path decision).
    - The WS-B feeder: model_aua_positions + model_composition for firm_id=49financial, in the convergent schema.
    - Session log with the Compiler Tools section + the verified per-cohort numbers. RAVC2 to COO.
  </deliverables>
</task_order>
