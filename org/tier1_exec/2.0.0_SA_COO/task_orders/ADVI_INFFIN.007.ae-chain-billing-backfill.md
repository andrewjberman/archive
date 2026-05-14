<task_order>
  <metadata>
    <id>ADVI_INFFIN.007</id>
    <slug>ae-chain-billing-backfill</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-05-13</date>
    <status>complete</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>.003 DS~C INF emit batch RAVC2 PASS (signal that gold scripts ship + S3 SHA-MATCH on origin/CLOUD); contingent silver/billing/ backfill if .003 Phase 1 surfaced gap</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P0 — completes Phase 2 INFFIN by materializing DS~C's new fields in platinum; unblocks .006 RD Phase 2 wiring</priority>
    <sla>~60-90min wall post-unblock (chain mode=full ~80min wall observed today); contingent billing backfill adds ~30min if needed</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md (DE 0.4 INFFIN brief §Surface #6 backend gate + §Open Questions #3 silver/billing/ horizon)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct evening walkthrough 2026-05-13</ref>
    <ref type="cross_link">Gated on: .003 DS~C INF emit batch RAVC2 PASS. Sibling: .006 RD Phase 2 wiring (gated on THIS TO + .003)</ref>
    <ref type="adjacent_ship">Chain #27 mode=full SUCCESS today (19:53:06Z fire → 21:01:28Z exit, 8/8 sentinels PASS) — proven runbook for chain fire under current dispatch.sh. Bug 1 dispatch.sh ordering fix in AE 0.6.1 queue post-INFFIN.007 (Option C `|| exit 1`).</ref>
  </references>

  <context>
    Phase 2 chain-fire dispatch materializes DS~C's new gold emits (.003) in platinum so RD-C (.006) can wire FE consumers. Plus contingent silver/billing/ backfill if DS~C's .003 Phase 1 step 1 surfaced inf-billing-daily Lambda gap.

    **Primary task: chain fire post-DS~C ship.**
    - mode=full recommended (per AE's chain #27 routing pattern: full re-validates A+B+C+D stage when compounding fixes land across architectural layers — DS~C .003 is gold-tier add, so mode=full validates cross-stage)
    - Alternative: mode=gold-d if DS~C's .003 only touches D-stage scripts (e.g., INF_D_02 + INF_D_05*); mode=full is safer
    - Expected outcome: gold/dimensions/ + gold/canonical/ + gold/timeseries/ + platinum/advisors/{id}/book.json (and sibling) emit new fields per .003 spec

    **Contingent task: silver/billing/ backfill.**
    - DS~C .003 Phase 1 step 1 investigates silver/billing/ partition horizon
    - If gap surfaces (e.g., inf-billing-daily Lambda hasn't backfilled to QTD/YTD/Max horizon), AE 0.6.1 owns Lambda dispatch + backfill run
    - DS~C MCPs AE 0.6.1 with specific gap (date range + window requirement) via COO
    - AE 0.6.1 invokes inf-billing-daily Lambda with backfill payload OR runs ad-hoc backfill script per inf-pipeline runbook

    **Pre-chain verify:**
    - `comp-pipescript deployed INF_D_02` (and any other DS~C-touched scripts) — confirm MATCH on .003 commit
    - gold runner EC2 boot S3-sync includes fresh scripts per design

    **Sentinel scorecard target (post-chain):**
    - silver bronze-name canonical (regression check)
    - A-stage 861 accounts_dim + EXACT 4 advisor distribution (regression check)
    - B-stage canonical_holdings ~9,400 rows / $224M MV (regression check)
    - C-stage canonical_nna 2020→T-1 (regression check)
    - **D-stage NEW: per-account fee fields populated** (.003 Surface #6 verify)
    - **D-stage NEW: per-period fee-split parallel fields populated** (.003 Surface #8 verify)
    - **D-stage NEW: relationship_stacked_periods[]** (.003 Surface #2 verify)
    - **D-stage NEW: client_directory.json** at platinum/firm/ (.004 verify, if shipped by DS~A)
    - Lambda direct-invoke post-chain
    - Chain exit 0
  </context>

  <objective>
    Fire chain to materialize DS~C's new gold emits in platinum + contingent silver/billing/ backfill if needed:

    1. **Pre-fire verify:** confirm DS~C .003 ship + S3 SHA-MATCH on touched scripts; confirm .004 DS~A directory artifact ship if landed (additive)
    2. **Chain fire:** mode=full (default) OR mode=gold-d (if scope justifies) per AE call
    3. **Sentinel scorecard:** verify regression cleanliness on A+B+C stages + NEW field validation on D-stage (per-account fees + fee-paying split + stacked HH)
    4. **Contingent billing backfill:** if DS~C .003 surfaces silver/billing/ gap, fire inf-billing-daily Lambda backfill
    5. **Lambda direct-invoke post-chain** for inf-portal-advisor-publisher to confirm FE-consumed platinum artifacts fresh
    6. **MCP RAVC2 to COO** with full empirical scorecard + chain commit fingerprint + Lambda invoke evidence
  </objective>

  <scope>
    <action>Chain fire dispatch via inf-gold-trigger Lambda + sentinel verification + contingent billing backfill</action>
    <files>
      <file action="verify_only">comp-pipescript deployed INF_D_02 + any DS~C-touched scripts (S3 SHA-MATCH .003 commit)</file>
      <file action="invoke">aws lambda invoke inf-gold-trigger with payload `{"mode":"full","snapshot_date":"2026-05-13"}` (or chain mode per AE call)</file>
      <file action="conditional">If silver/billing/ gap: invoke inf-billing-daily Lambda with backfill payload OR run ad-hoc backfill script</file>
      <file action="verify">platinum/advisors/{id}/book.json + sibling — new fields per .003 spec</file>
      <file action="verify">platinum/firm/client_directory.json (if .004 shipped)</file>
      <file action="output">org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-{14|15}/ — chain RAVC2 session log</file>
    </files>
  </scope>

  <phase id="1" when="pre-unblock-verify">
    <run>Verify .003 DS~C ship signal received (RAVC2 PASS from COO)</run>
    <expect>.003 commit hash + scripts touched documented</expect>
    <if_mismatch>Do not start; surface to COO. dispatch_held=true.</if_mismatch>

    <run>comp-pipescript deployed on DS~C-touched scripts — confirm S3 SHA-MATCH on .003 commit</run>
    <expect>MATCH on all touched scripts</expect>
    <if_mismatch>Surface to DS~C for safe-deploy cycle re-run</if_mismatch>

    <run>If .003 Phase 1 step 1 flagged silver/billing/ gap: receive specific gap details from DS~C (date range + window requirement)</run>
    <expect>Gap details documented OR no gap surfaced</expect>
  </phase>

  <phase id="2" when="contingent-billing-backfill">
    <step>
      <description>IF silver/billing/ gap: invoke inf-billing-daily Lambda with backfill payload. Backfill horizon per DS~C requirement (likely 1Y/Max). Confirm partition write success.</description>
      <expect>Silver/billing/ partition horizon satisfies QTD/YTD/Max window requirements.</expect>
      <if_mismatch>If Lambda fails: investigate via CloudWatch; potentially run ad-hoc backfill script per inf-pipeline runbook. Surface to COO if blocked.</if_mismatch>
    </step>
    <step>
      <description>Post-backfill: empirical S3 inspect silver/billing/ partition coverage matches expected horizon.</description>
      <expect>Coverage verified.</expect>
    </step>
  </phase>

  <phase id="3" when="chain-fire">
    <step>
      <description>Pre-fire: verify INF_C_01.canonical_nna.py + INF_D_02.advisor_client_detail.py (and any DS~C-touched gold script) S3 mtime fresh post-.003 deploy.</description>
      <expect>S3 mtime current.</expect>
    </step>
    <step>
      <description>Fire chain via inf-gold-trigger Lambda. Mode=full (default; per AE chain #27 routing pattern when compounding fixes across stages).</description>
      <expect>Lambda returns 200; EC2 instance starts; chain runs ~60-90min wall.</expect>
    </step>
    <step>
      <description>Monitor chain progress via runner log. Watch for INF_C_01 (DS~D fix re-validate) + INF_D_02 + INF_D_05* + new sibling script (if .004 shipped DS~A INF_D_02b) emit success.</description>
      <expect>Chain exit 0; pipeline-complete.json sentinel written.</expect>
      <if_mismatch>If chain fails at any stage: capture stack trace; surface to COO + relevant DS lane (DS~C if .003 emit fails, DS~A if .004 emit fails). Forward-fix or rollback per failure class.</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="sentinel-scorecard">
    <step>
      <description>Regression-check A+B+C stages (carry forward from chain #27 scorecard):
- silver/transactions/ bronze-name canonical 1.27M+ rows
- silver/api_dims/accounts_v2/ ~861 rows
- gold/dimensions/accounts_dimension_latest 861 rows + α+β + EXACT 4 advisor distribution (Peter Lee + Patrick Scanlan + Joe Brandenburg + IWM)
- gold/canonical/holdings T-0 ~9,400 rows / $224M MV
- gold/canonical/canonical_nna T-1 emit (trans_type_desc NULL=0 + bucket-via-yaml-v3 classification)</description>
      <expect>All regression sentinels PASS.</expect>
    </step>
    <step>
      <description>NEW field verify (D-stage):
- platinum/advisors/{id}/book.json contains `clients[].accounts[].fee_*` fields populated for all 4 Inflection advisors
- Zero `null` fee fields across all advisors (null-elimination rule)
- Red-flag accounts (166, 477) carry `fee_structure_reason` sentinel
- platinum/advisors/{id}/book.json (or sibling) contains per-period fee-split parallel fields (aua_fee_paying/aua_no_fee + 6 more)
- platinum/advisors/{id}/timeseries.json (or wherever Lifetime Activity emit lives) contains split-bars data
- platinum/advisors/{id}/book.json (or sibling) contains `relationship_stacked_periods[]` block</description>
      <expect>All NEW field sentinels PASS.</expect>
    </step>
    <step>
      <description>If .004 DS~A shipped: platinum/firm/client_directory.json contains all Inflection HHs with advisor + display_name attribution.</description>
      <expect>Coverage spot-check passes.</expect>
    </step>
  </phase>

  <phase id="5" when="lambda-invoke-validation">
    <step>
      <description>Post-chain Lambda auto-fire (INFPUBLISHERDEDUP ObjectCreated trigger): verify inf-portal-advisor-publisher fires ~40s after chain. Confirms platinum artifacts pickled by FE-consumed Lambdas.</description>
      <expect>Auto-fire triggers; Lambda returns 200.</expect>
    </step>
    <step>
      <description>Direct-invoke verification: aws lambda invoke inf-portal-advisor-publisher with payload `{"advisor_id":"peter_lee"}` (smoke). Confirm 200 response + new fields propagated.</description>
      <expect>200 response; fields visible in Lambda output.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Chain fires with mode=full (or AE-justified gold-d) post .003 RAVC2.
    AC2: Chain exit code 0; pipeline-complete.json sentinel written.
    AC3: A+B+C stage regression sentinels PASS (carry forward from chain #27 8/8 scorecard).
    AC4: NEW D-stage fields verified (per-account fees + fee-paying split + relationship_stacked_periods); zero `null` fee fields; red-flag sentinels present.
    AC5: .004 DS~A directory artifact present at platinum/firm/client_directory.json if .004 shipped.
    AC6: Contingent silver/billing/ backfill: if gap surfaced, partition horizon satisfies QTD/YTD/Max requirements.
    AC7: Lambda auto-fire post-chain succeeds; direct-invoke smoke 200 response.
    AC8: Session log with full empirical scorecard + chain commit fingerprint + Lambda invoke evidence.
    AC9: MCP RAVC2 to COO with scorecard + signal to unblock .006 RD Phase 2.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-pipescript deployed verify on .003-touched scripts</phase_1>
    <phase_2>Chain fire + sentinel scorecard via comp-validate (if config exists for INFFIN scope; else manual S3 inspection)</phase_2>
    <phase_3>Lambda direct-invoke smoke validation</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES:
    - .003 DS~C INF emit batch RAVC2 PASS (signal that gold scripts ship + S3 SHA-MATCH on origin/CLOUD)
    - .003 Phase 1 step 1 silver/billing/ gap signal (yes/no) — informs whether contingent billing backfill fires

    DOWNSTREAM CONSUMER:
    - .006 RD Phase 2 wiring (dispatch_held=true) UNBLOCKS on this RAVC2 PASS

    PARALLEL ACTIVITY:
    - .005 DS~B 49F audit (informational only; not blocking chain fire)
    - .001/.002 RD lanes (already shipped Phase 1; ChartTooltip + advisor-selection wiring foundational for .006)

    NO PORTAL: AE-side chain dispatch only.

    BUG 1 dispatch.sh ordering fix (set -o pipefail per AE Option C lean): in AE 0.6.1's queue POST this TO. Not blocking INFFIN.007 since INF_S_00 silver-prep won't recur on chain #28+ (DWSPLT silver already canonical from chain #27).
  </cross_domain_coordination>

  <data_reprocess_scope>
    <chain_fire_required>
      Chain fire materializes DS~C's new gold emits in platinum. mode=full re-validates A+B+C stages + new D-stage fields.
    </chain_fire_required>
    <contingent_backfill>
      If silver/billing/ gap surfaced by DS~C, inf-billing-daily Lambda backfill required pre-chain-fire so silver layer has billing data when gold consumers read.
    </contingent_backfill>
  </data_reprocess_scope>

  <deliverables>
    1. Pre-chain verify (comp-pipescript deployed on .003-touched scripts)
    2. Contingent silver/billing/ backfill (if gap surfaced by .003)
    3. Chain fire via inf-gold-trigger Lambda
    4. Sentinel scorecard (A+B+C regression + NEW D-stage fields)
    5. Lambda auto-fire + direct-invoke verification
    6. Session log at org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-{14|15}/ with empirical evidence
    7. MCP RAVC2 to COO with scorecard + unblock signal for .006 RD Phase 2
  </deliverables>

  <ravc>
    AE 0.6.1 RAVC2 to COO post-AC1-9 PASS. COO unblocks .006 RD Phase 2 dispatch_held. Post-.006 ship + RAVC2 closes INFFIN v0.1 scope.
  </ravc>

  <notes>
    **Dispatch hold:** dispatch_held=true until .003 DS~C RAVC2 PASS. COO unblocks via MCP "INFFIN.007 dispatch unblocked; proceed chain fire."

    **Mode selection (chain #27 routing pattern carry-forward):** mode=full default per AE 0.6.1's chain #27 reasoning — "compounding fixes across architectural layers warrant mode=full for cross-stage validation." DS~C's .003 is gold-tier add affecting D-stage primarily; if you call mode=gold-d for speed, document the regression-validation tradeoff.

    **Billing backfill timing:** if silver/billing/ gap surfaces, run backfill BEFORE chain fire (silver must be ready when gold reads it). Sequence: DS~C .003 RAVC2 → billing gap signal → AE billing backfill (~30min) → AE chain fire (~80min).

    **Bug 1 dispatch.sh fix sequencing:** your queue has Bug 1 dispatch.sh Option C (`set -o pipefail` per chain #26/27 RAVC2). That fix is non-blocking for INFFIN.007 since INF_S_00 silver-prep reads DWSPLT-canonical silver on chain #28+. Pick up post-INFFIN.007 + .006 closeout.

    **Author identity:** `--author="0.6.1_AE_PartnerETL <0.6.1_AE_PartnerETL@opal.agent>"` per agent commit identity protocol.

    **Open question #3 silver/billing/ horizon:** depends on DS~C .003 Phase 1 step 1 empirical. If horizon is sufficient, no backfill needed. If gap, backfill horizon documented in your RAVC2.
  </notes>
</task_order>
