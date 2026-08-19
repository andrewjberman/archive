# TO D3_MODELOVERLAY.TO-D3.2 — account_model_membership gold producer (LAPTOP-ONLY)

<task_order id="D3_MODELOVERLAY.TO-D3.2" project="D3_ACCOUNT_MODEL_OVERLAY">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:50Z</issued>
<dated>on TO-D3.1's spec + the D2 flip</dated>
<status>staged -- GATED ON TO-D3.1 + D2 flip landed</status>
<priority>P1-program</priority>
<authority>D3_ACCOUNT_MODEL_OVERLAY_PRD.md §4.2 + §6 item 2 at dispatch vintage @52a85baf08. Placement: LAPTOP-ONLY (safe-deploy DS lane + S3 code staging; Rule 13).</authority>
</task_order>

## Objective
New runner + a06 extension per the TO-D3.1 spec, producing the account_model_membership gold table.
The §6 existence check confirmed no such producer exists today — RE-RUN it as your Phase 1 rather
than inheriting the claim.

## Mandate
comp-pipescript io <script> --pipeline <tree> (the flag is REQUIRED; flagless is rc=2 refused),
comp-blast, comp-validate config. Rule 15: the file opens with from __future__ import annotations.
Rule 17: dedup/dtype belongs in silver — the judgment about membership is gold-tier and correctly
placed here. Rule 17b: gold is parquet.

## Acceptance criteria
- D3.2-1 TABLE LANDS WITH A DUAL-DENOMINATOR MANIFEST (both sides of the join counted).
- D3.2-2 COVERAGE >= THE SPEC FLOOR from TO-D3.1.
- D3.2-3 THE COVERAGE-BREACH FLAG NAMES ITS READER AND ITS MOMENT. CVO measured this exact row as
  one of four "honest record with no named reader" instances in this wave — a flag whose consumer is
  A CLASS rather than A READER. An acceptance of "the flag is written" is NOT the same as "the flag
  is read." So: name WHO reads it and AT WHICH ALREADY-EXECUTING MOMENT, and make the check recur at
  that moment. THIS IS A ROUTING/FLOW REQUIREMENT, NOT AUTHORIZATION TO BUILD AN ALERT, SNS TOPIC,
  OR MONITOR — the moratorium stands and the remedy here is canonical flow, not notification
  machinery.
- D3.2-4 DEPLOY VERIFIED ON THE STORED/SERVED ARTIFACT (Rule 22a APPLIED layer), never rc=0 and
  never a producer self-report.
- D3.2-5 proof instance VALID rc=0 positional: ids D3.2-1..D3.2-5. MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>D3.2-1,D3.2-2,D3.2-3,D3.2-4,D3.2-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D3_MODELOVERLAY.TO-D3.2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at table-landed. Distinguish real success from SILENT FALLBACK. Session log w/ Compiler Tools
section = deliverable.
