<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-23-mvplvl-009-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>ADVI_MVPLVL</project_code>
    <thread_serial>ADVI_MVPLVL-006</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-006-mix-and-composition-e2e-trace----broken/</thread_ref>
  </metadata>

  <objective>
    REVISED 2026-03-23 (COO, revision 2): DS verification revealed 3 data-layer
    issues beyond what the thread diagnosed. DS has already fixed one (06b advisor
    ID normalization, committed f6a4b5b8). The remaining issues require AE to
    redeploy scripts to EC2 and run a full gold rebuild.

    Original scope was verification-only. DS exceeded scope productively by
    identifying and fixing the 06b advisor ID mismatch. This revision acknowledges
    that work and closes the DS task order after confirming the handoff to AE.

    Phase 1 findings summary:
    1. (HIGH) Script 12 on EC2 is pre-ETFClassifier version (uploaded 2026-03-19,
       before commit 5c6fd9d0). Produces structured_notes instead of alternatives.
       Repo version is correct. Needs EC2 redeploy. -> AE owns.
    2. (HIGH, FIXED) 06b advisor ID format mismatch: raw display names vs snake_case.
       DS added _advisor_id() normalization matching script 12. Committed f6a4b5b8.
    3. (MEDIUM) Only 1 period per granularity in firm_mix_views.json. Needs full
       rebuild (not incremental). -> AE owns (part of gold rebuild).
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="verify">data/black_diamond/scripts/gold/12_build_composition_artifacts.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      COMPLETE: Verified S3 artifacts exist. firm_mix_views.json, firm_composition.json,
      and advisor-level files all present with valid JSON. Gold rerun 2026-03-20 confirmed.
    </requirement>

    <requirement id="2">
      COMPLETE: Identified taxonomy mismatch in script 12 on EC2 (structured_notes
      instead of alternatives). Repo version uses ETFClassifier correctly (commit
      5c6fd9d0). The deployed EC2 copy is stale.
    </requirement>

    <requirement id="3">
      COMPLETE: Fixed 06b advisor ID normalization. Added _advisor_id() function
      matching script 12's snake_case sanitization. Committed f6a4b5b8.
    </requirement>

    <requirement id="4">
      Confirm handoff to AE: the following items are AE-owned and require EC2
      deployment + full gold rebuild:
      - Deploy repo versions of 06b (f6a4b5b8) + 12 (5c6fd9d0) to EC2 gold runner
      - Run full gold rebuild (not incremental) to regenerate all artifacts with:
        (a) correct 4-class taxonomy from ETFClassifier (no structured_notes)
        (b) consistent snake_case advisor IDs across both scripts
        (c) full date range for firm_mix_views.json (not just 1 period)
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">S3 verification report delivered (DONE)</criterion>
    <criterion id="2">06b advisor ID fix committed to CLOUD (DONE: f6a4b5b8)</criterion>
    <criterion id="3">Taxonomy mismatch escalated to AE for EC2 redeploy (DONE)</criterion>
    <criterion id="4">After AE gold rebuild: re-verify firm_mix_views.json has full date range, firm_composition.json uses alternatives (not structured_notes), advisor paths use snake_case consistently</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>DS does NOT deploy to EC2. AE owns EC2 gold runner deployment.</constraint>
    <constraint>The ONLY classifier is the DynamoDB-backed ETFClassifier (bd-securities table). If any artifact contains structured_notes, it was produced by the old pre-ETFClassifier script and must be regenerated.</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_MVPLVL.009-ae.verify-lambda-routes" status="pending">
      AE must deploy updated scripts to EC2 and run full gold rebuild.
      DS re-verifies artifacts after rebuild completes.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="document">S3 verification report with 3 findings (DELIVERED)</deliverable>
    <deliverable type="commit">06b advisor ID normalization fix (DELIVERED: f6a4b5b8)</deliverable>
    <deliverable type="document">Post-rebuild re-verification (PENDING: after AE gold rebuild)</deliverable>
  </deliverables>
</task_order>
