<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-04-15-cdrs-tfimpt-006-users-v2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <project_code>CDRS_TFIMPT</project_code>
    <priority>P1 (Phase 2 sprint; lightest of two identity-table TOs)</priority>
  </metadata>

  <references>
    <ref type="scope_brief">docs/architecture/CDRS_TFIMPT_PHASE2_HANDOFF.md (DT 0.4 memo, 2026-04-15)</ref>
    <ref type="source_design">0.7.0_AE_CloudOps → 0.4.0_DT MCP 2026-04-15T16:20Z (4-step shared partner-firm infra plan)</ref>
    <ref type="precedent">CDRS_TFIMPT.001-.005 (2-hour sprint close, 5/5 imports, first-try 0-diff on .005)</ref>
    <ref type="phase_0_context">org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-04-15/identity_permissions_overhaul.md (firmRole framework)</ref>
  </references>

  <objective>
    Import hand-created DynamoDB table `opal-users-v2` into Terraform. Table created via `aws` CLI for
    speed during DT's firmRole framework rollout; now needs TF management per DT RULES.md R10.

    Per DT memo point 3: fold `opal-users-v2` into `infra/aws/terraform/shared-infra/` (do NOT create
    a new top-level module for it — it's firm-agnostic, shared-infra is the right home). Separate from
    the `opal-partner-{firmId}` partner-table work which goes into `.007` as a new module.

    Scope narrow: schema + keys + GSI + TTL + PITR + stream-spec (if any) captured from live table,
    written into `shared-infra/users-v2.tf` (or folded into existing `shared-infra/dynamodb.tf` if
    that's the established pattern), imported, 0-diff verified. Same tag-bump pattern as `.001-.005`.
  </objective>

  <scope>
    <files>
      <file action="create-or-modify">infra/aws/terraform/shared-infra/users-v2.tf (or fold into existing shared-infra/dynamodb.tf — AE picks the cleaner placement)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="dynamo-import">
      1. `aws dynamodb describe-table --table-name opal-users-v2` — capture full schema including KeySchema, AttributeDefinitions, GlobalSecondaryIndexes, TimeToLiveSpecification, PointInTimeRecoverySpecification, StreamSpecification.
      2. Write `aws_dynamodb_table.users_v2` resource matching every field exactly.
      3. Handle TTL + PITR via separate resource types if needed (`aws_dynamodb_table_item_ttl` is not a real resource — TTL is inline on the table; PITR via `point_in_time_recovery` block).
      4. Import: `terraform import aws_dynamodb_table.users_v2 opal-users-v2` into shared-infra state.
      5. `terraform plan` → 0-diff. Fix any drift by editing TF to match live, NOT by mutating live.
      6. `terraform apply` (no-op).
      7. Tag `shared-infra-v{next}` per `git tag -l "shared-infra-v*" | sort -V | tail -3` next-version rule.
    </deliverable>
  </deliverables>

  <wire_contract>
    Zero runtime behavior change. Table keeps all 10 admin+user records intact. DT's auth-handler
    reads `GetItem` on `opal-users-v2` exactly as before. No IAM grant changes needed (auth-handler
    already has policy via existing shared-infra IAM).
  </wire_contract>

  <acceptance_criteria>
    1. `aws_dynamodb_table.users_v2` in shared-infra state; resource ID = `opal-users-v2`.
    2. `terraform plan` 0-diff post-apply in shared-infra.
    3. All attributes preserved: KeySchema (USER#email PK), any GSIs, TTL enabled state, PITR state, stream spec.
    4. Tag `shared-infra-v{next}` exists and pushed.
    5. pipeline_inventory.xml updated (+1 dynamodb row tracked).
    6. Audit doc `docs/analysis/2026-04-15_cloud_inventory_audit.md` section 3 (DynamoDB) updated: 1 less gap, 18/30 → 19/30 coverage.
    7. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7 locked 2026-04-15).
    8. MCP COMPLETE to COO with commit hash + tag + regression evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws dynamodb describe-table --table-name opal-users-v2 > /tmp/users-v2-live.json</run>
        <expect>Full table description captured to disk for behavior-by-behavior TF authoring.</expect>
        <if_mismatch>STOP. If ResourceNotFoundException, the table was deleted — surface to COO + DT before proceeding.</if_mismatch>
      </step>
      <step>
        <run>grep -rn "opal-users-v2\|users_v2" infra/aws/terraform/</run>
        <expect>Zero matches (table is un-managed) OR pre-existing references in IAM/Lambda env vars only (which is fine, just non-blocking).</expect>
        <if_mismatch>If aws_dynamodb_table references found, TO is moot — table is already managed; close with a note.</if_mismatch>
      </step>
      <step>
        <run>grep -rn "dynamodb" infra/aws/terraform/shared-infra/</run>
        <expect>Identify whether `shared-infra/dynamodb.tf` (or similar) exists as the folding point, OR if a new users-v2.tf file is the cleaner placement.</expect>
        <if_mismatch>Reconcile with shared-infra layout conventions before authoring.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>terraform plan</run>
        <expect>0-diff in shared-infra state after `aws_dynamodb_table.users_v2` import.</expect>
        <if_mismatch>Edit TF field-by-field to match live; re-plan. Do NOT apply a plan that mutates live.</if_mismatch>
      </step>
      <step>
        <run>aws dynamodb scan --table-name opal-users-v2 --select COUNT</run>
        <expect>Record count unchanged pre/post import (≥10 rows per DT session log evidence).</expect>
        <if_mismatch>STOP — import touched data (shouldn't; DynamoDB imports are metadata-only). Investigate before any tag.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>terraform plan</run>
        <expect>Still 0-diff post-apply.</expect>
        <if_mismatch>Post-apply drift = incomplete import. STOP, capture delta, surface to COO; do NOT tag or mark complete.</if_mismatch>
      </step>
      <step>
        <run>aws dynamodb get-item --table-name opal-users-v2 --key '{"PK":{"S":"USER#andrew@opalinvest.com"}}'</run>
        <expect>Andrew's user record returns (spot-check reader access preserved).</expect>
        <if_mismatch>Surface to COO + DT — auth-handler may be broken.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>None for .006. .007 follows (requires AE 4-Q resolution in DT memo — delivered 18:56Z).</dependencies>

  <closeout date="2026-04-15" commit="pending-on-commit">
    (a) **First-try 0-diff (same as .005 sprint close).** No `terraform apply` needed -- table was already tagged with shared-infra provider defaults + the System="PortalAuth" resource-level override I matched to live. Plan returned `No changes` immediately after import.
    (b) **Phase 1 delta from TO:** TO assumed single GSI (firmId-index per DT memo). Live has TWO: firmId-index + email-index (KEYS_ONLY). Added both — no Rule 7 flex event because TO `<compiler_tools_mandate>` step 1 was "capture schema from live" not "limit to one GSI". Normal recon-drives-implementation flow.
    (c) **SSE:** live uses AWS-managed KMS key (aws/dynamodb). Provider default behavior without an explicit `server_side_encryption{}` block matches; no config needed.
    (d) Spot-check substituted: TO's GetItem `PK=USER#andrew@opalinvest.com` returned ValidationException (composite key requires PK+SK for GetItem, and actual PK format is `USER#usr_<id>`, not `USER#<email>`). Substituted with `scan --select COUNT` = 39 (preserved) + query-by-PK format probe. Same evidence shape; noted for future TO authoring.
    (e) System=PortalAuth tag preserved on resource; shared-infra default_tags would set it to SharedInfra but explicit resource tag overrides. Avoids a tag-mutation apply on a table that was pre-tagged by the hand-create flow.
  </closeout>

  <next>On commit + tag + push: MCP COMPLETE to COO. Pivot to .007 (pending flip unlocks once COO processes 4-Q resolution).</next>

  <next>On commit: MCP to COO + AE pivots to .007 (opal-partner-{firmId} TF module + shared-lib + auth-handler generalization, paired AE+DT commit).</next>
</task_order>
