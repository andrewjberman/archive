<to_id>NFRA_GRAPHS.D8-FP</to_id>
<project>NFRA_GRAPHS</project>
<title>D8 surface-scan baseline domain-match — resolve the 06-17 SEV1/SEV2 critical-surface false-positives (AWS-only derive diffed vs portal-inclusive baseline)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (CTO D8 adjudication 141614Z; base-AE diagnosis 140936Z; single-router dispatch)</issued_by>
<issued_date>2026-06-17</issued_date>
<status>complete</status>
<!-- COMPLETE 2026-06-17 (RAVC2-ACCEPTED COO 182914Z; CTO close-review). All 4 ACs met: AC1 FP-confirmed (baseline-provenance mismatch), AC2 Option-A AWS-backend-membership re-impl DEPLOYED (fdc1ddf31 + baseline re-signed d8fp-aws-backend-membership-v1), AC3 de-noise-WITHOUT-blinding ALL PASS (firm-sep + co-tenant control + 2 category rows), AC4 served-healthy. Deploy ledger d8fp-surface-scan-membership CLOSED (ee0b1d6bf), --red clean. Stale-pending flip per /to-check 2026-06-17. RESIDUAL (non-gating): 06-18 02:00Z nightly live-scan verify (base-AE morning check, event-driven). -->
<priority>HIGH — CTO-prioritized AHEAD of base-AE's lower items (COSTAWS). A false SEV1/SEV2 on the must-always-be-right critical-surfaces SNS = cried-wolf erosion. NOT a fire (failure mode is noise, not blindness; base-AE landed interim KNOWN-FP ledger 79d999355 = the 02:00Z FP is contained -> proceed deliberately). base-AE diagnosed it + owns the D8 alarm infra + is idle-pending-TO-3.</priority>

<scope_ruling>
SCOPE GREW + RULED OPTION A (CTO 143843Z; AC1 already satisfied — FP definitive per 142338Z). base-AE code-grounded that the originally-framed "AWS-scoped re-sign" would BLIND the scan (every AWS derive node has file_path="full-derive"; the finding loop fires only on portal-source-path matches -> after an AWS-scoped re-sign NO removed AWS node could ever fire = fails AC3 de-noise-without-blinding). The scan's matching mechanism is structurally incompatible with the AWS-only derive.

CTO RULED OPTION A (rejected Option B retire-the-layer = loses out-of-band AWS-drift coverage commit-time can't give): RE-IMPLEMENT the in-derive scan to attribute removed/changed AWS nodes to surfaces by BACKEND-CHAIN MEMBERSHIP (per-surface AWS-backend subgraph carve by ARN/node_id) + re-sign the baseline AS that carved subgraph. This implements the yaml scheduled_scan's actual spec ("diff current SUBGRAPH vs signed baseline") and PRESERVES runtime out-of-band AWS-drift detection on the must-always-be-right surfaces. So this is a CODE change (scan matching: file_path -> AWS-backend membership) + per-surface carve + re-sign + AC3 egress-test — bigger than a data re-sign; scope/effort accordingly. base-AE carves from the 06-17 derive (no ad-hoc run). COO coverage-stake input concurred (Option B's commit-time-only loses runtime/infra-removal detection).
</scope_ruling>

<references>
  <ref type="adjudication">CTO 141614Z — high-confidence FP (baseline-scope mismatch), design ruling = domain-match the scan baseline; NOT declared definitive until AC1 provenance confirmed.</ref>
  <ref type="diagnosis">base-AE 140936Z — 06-17 02:00Z derive's in-run SURFACE_SCAN published SEV1+SEV2 ("model_portfolios","advisor_intelligence") on baseline_nodes=2139 -> current_nodes=1239; every REMOVED node is a portal-AST node (component:portal/src/pages/ModelPortfolios.tsx, endpoint:formatAUM) an AWS-only derive never emits; SURFACE_SCAN_STALENESS_SKIP prev_marker_ts=None (unreadable/first-run baseline).</ref>
  <ref type="infra">derive_runner post-kuzu_nessie_load surface-scan step + opal-critical-surface-alerts SNS topic (D8-AE Part B, globgrph-v0.1.13); comp-surface-check; org/modules/graph/critical-surfaces.yaml; critical-paths ledger org/critical_paths/.</ref>
</references>

<scope>
The in-derive SURFACE_SCAN diffs the current AWS-only derive against a baseline that includes portal-AST nodes (2139), so every portal node reads as REMOVED -> systematic false SEV1/SEV2 on model_portfolios + advisor_intelligence. CTO design ruling: the scan must diff DOMAIN-MATCHED (AWS-only current <-> AWS-only baseline). Diffing an AWS-only derive against a portal-inclusive baseline IS the defect.

DO: (1) confirm the 2139 baseline provenance FIRST (gating); (2) domain-match the in-derive surface-scan baseline to the derive's scope; (3) de-noise without blinding (the alarm must still fire on a TRUE removal); (4) independently confirm the two flagged surfaces are actually healthy on served state.

DO NOT: widen/weaken the critical-surface alarm coverage; touch the merged-AWS+portal-canonical-graph question (CTO folds that into NFRA_GRAPHS separately — this TO is the immediate domain-match fix only). Read-only until AC1 confirms FP.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change (AC1 gating)">
    <step>
      <run>comp-kuzu "MATCH (n) RETURN labels(n), count(*)" on the current canonical graph + inspect the 2139-node baseline source/provenance (where the baseline was captured from)</run>
      <expect>Current canonical = AWS-infra-only (node types S3/IAM/Lambda/EC2/...; 0 portal-AST nodes). The 2139 baseline contains portal-AST nodes (component:/endpoint:) -> it was built from a MERGED/stitched graph, not the AWS-only derive -> FP CONFIRMED.</expect>
      <if_mismatch>If the 2139 baseline was SUPPOSED to be AWS-only (i.e. a genuine ~900-node AWS-resource drop), this INVERTS to a REAL SEV1 — STOP, do NOT rescope/de-noise, escalate to CTO + COO immediately. (CTO AC1: dismissing a real SEV1 is the worse failure than the FP.)</if_mismatch>
    </step>
    <step>
      <run>comp-surface-check (current behavior) + locate the in-derive surface-scan baseline-capture + diff code in derive_runner</run>
      <expect>comp-surface-check itself is CLEAN (0 critical-surface touches — CTO confirmed); the SEV1/SEV2 came from the in-derive scan's baseline mismatch, not comp-surface-check. Identify exactly where the baseline scope diverges from the derive scope.</expect>
      <if_mismatch>If comp-surface-check is ALSO firing, the defect is broader than the in-derive scan — surface to COO/CTO before changing the in-derive scan alone.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before deploy">
    <step>
      <run>comp-iam gaps (if any iam.tf touched) + Terraform plan for any derive_runner/SNS change</run>
      <expect>No new IAM gap; Terraform-only change; 0-diff after apply. (Likely a code-side baseline-scoping fix, minimal/no infra change.)</expect>
      <if_mismatch>Resolve before apply (Terraform-only per Rules 1-6).</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>Re-run / dry-run the in-derive surface-scan on the AWS-only derive + a SYNTHETIC true-removal test</run>
      <expect>0 false SEV1/SEV2 on the AWS-only derive (portal nodes no longer read as REMOVED) AND a synthetic true AWS-resource removal STILL fires the SNS alarm (egress-verified — the alarm is de-noised, NOT blinded). Real critical surfaces still COVERED.</expect>
      <if_mismatch>If the synthetic true-removal does NOT fire, the fix blinded the alarm — STOP, revert, the de-noise over-reached. If false SEV1/SEV2 persist, the baseline domain-match is incomplete.</if_mismatch>
    </step>
    <step>
      <run>Independently confirm model_portfolios + advisor_intelligence are healthy on SERVED state (the FP did not mask a real issue)</run>
      <expect>Both surfaces serving correctly (served-artifact present/fresh, page renders) — the FP was scope-noise, not a real degradation hidden by the alarm.</expect>
      <if_mismatch>If either surface is actually degraded on served state, the "FP" masked a real issue — escalate to CTO/COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- INTERIM (binding NOW, until this TO lands): the 06-17 02:00Z SEV1/SEV2 on model_portfolios + advisor_intelligence is treated KNOWN-FP — nobody reacts to it as a real MP/ADVI removal. base-AE notes this in the critical-paths ledger so the next reader doesn't re-trip on it.
- This is the in-derive surface-scan (derive_runner post-kuzu_nessie_load step), NOT comp-surface-check (CLEAN). Scope to the in-derive scan's baseline.
- The bigger "should the canonical graph be merged AWS+portal" question is CTO's NFRA_GRAPHS fold — OUT of scope here; do not build toward merged-graph, just domain-match.
- Sequencing: this rides AHEAD of COSTAWS; if the GCONTR TO-3 contract-row load GO fires mid-flight, that load is the higher-priority interrupt (it's the live GCONTR chain) — RAVC2 this TO's increment, pivot to the load, resume.
</cross_domain_coordination>

<acceptance_criteria>
- AC1 (FIRST, GATING): 2139 baseline provenance confirmed — merged/stitched (-> FP confirmed, proceed) vs supposed-AWS-only (-> REAL drop, INVERT to SEV1, escalate, do NOT rescope). Evidence: the baseline source + node-type census.
- AC2 (RULED OPTION A — see scope_ruling): re-implement the in-derive scan matching from file_path-match to AWS-BACKEND-CHAIN MEMBERSHIP (per-surface AWS-backend subgraph carve by ARN/node_id) + re-sign the baseline AS that carved per-surface subgraph (implements the yaml scheduled_scan "diff current SUBGRAPH vs signed baseline" spec). A plain AWS-scoped re-sign is REJECTED (blinds the scan — fails AC3).
- AC3: re-run/dry-run -> 0 false SEV1/SEV2 on the AWS-only derive AND a synthetic true-removal STILL fires the SNS alarm (egress-verified — de-noised, not blinded).
- AC4: model_portfolios + advisor_intelligence independently confirmed healthy on SERVED state.
- Deployed via Terraform (0-diff); comp-iam gaps clean if iam.tf changed.
- Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail vs <expect>. RAVC2 to COO (CC CTO — D8/NFRA_GRAPHS owner).
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Surface-scan baseline-scoping logic + alarm-diff only; reads the derive graph each run. No pipeline/data re-emit. The fix changes which baseline the scan diffs against, not any served data.</no_reprocess_needed></data_reprocess_scope>
