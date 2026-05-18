<task_order>
  <metadata>
    <id>TRSB_LEDGER.005</id>
    <slug>ae-by-approver-gsi-repoint</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO~B decomposition of TRSB_LEDGER PRD v0.1). Phase 2 -- sequenced LAST among the workflow_handler.py TOs on the AE 0.7.0 serial backend lane (after TO-4). COO~B lane note: PRD §6 named AE 0.5.0 for TO-5 as "Terraform, no Lambda-source overlap" -- that is incorrect; TO-5 edits workflow_handler.py AND dashboard_api.py AND dynamodb.tf, so it belongs on the AE 0.7.0 serial lane. Reassigned from AE 0.5.0. Flagged to CTO~B.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- Pillar B. Closes hole B5 (rejected trades fall out of the by-approver GSI -- the approver's own decision history is incomplete by construction). HIGHEST-CARE item in the PRD (R3 -- GSI key-schema change).</priority>
    <sla>2-3d wall -- the GSI cutover has mandatory wait-for-ACTIVE steps.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.B B5; section 6 TO-5; section 8 R1 (backfill) + R3 (GSI key-schema change is the highest-care item -- the TO must specify the cutover mechanics).</prd>
  </references>

  <objective>
    Make rejected trades retrievable in an approver's decision history. Today the `by-approver` GSI is `hash=approver_email, range=approved_at`; `handle_reject` writes `approver_email` but not `approved_at`, so a rejected trade is never indexed into the GSI -- `dashboard_api.get_by_approver` silently omits every trade an approver rejected. The fix: a `decided_at` attribute written on BOTH approve and reject, and the GSI repointed to range on `decided_at`. Executed via a planned create-new -> backfill -> cutover -> drop-old GSI sequence (no in-place key-schema change is possible in DynamoDB).
  </objective>

  <context>
    DynamoDB indexes an item into a GSI only when the item carries BOTH key attributes. The `by-approver` GSI ranges on `approved_at`; rejected trades have `approver_email` but `rejected_at` (not `approved_at`) -> absent from the GSI (B5).

    DynamoDB does NOT permit modifying a GSI's key schema in place. The repoint is a create-new / drop-old sequence, and only ONE GSI create-or-delete is allowed per `UpdateTable` operation -- so the create and the drop are SEPARATE terraform applies.

    This TO touches three files: `workflow_handler.py` (write `decided_at` on approve + reject), `dashboard_api.py` (`get_by_approver` repointed to the new GSI), and `dynamodb.tf` (GSI definitions). Plus a one-time backfill of `decided_at` onto existing decided rows.

    Backfill (R1): existing approved/rejected rows predate `decided_at` -- without a backfill the new GSI stays incomplete for historical rows. The same one-time historical-row sweep also writes the synthetic `MIGRATED` audit_event onto pre-TO-3 rows that have no `audit_events` list (PRD R1 -- audit_events cannot be reconstructed for past trades; a single synthetic MIGRATED event documents the gap rather than silently skipping it).
  </context>

  <scope>
    <step>Phase 1 -- Direct read dynamodb.tf (the `by-approver` GSI def ~lines 105-110) + dashboard_api.get_by_approver + workflow_handler handle_approve/handle_reject. Confirm the GSI name + key schema and the get_by_approver query.</step>
    <step>Phase 2 step 1 -- Handler change: `handle_approve` and `handle_reject` both write a `decided_at` attribute (the decision timestamp -- equal to `approved_at` on approve, `rejected_at` on reject). `approved_at` / `rejected_at` remain as-is for backward compatibility. Deploy this via terraform apply FIRST so all new decisions carry `decided_at` before the new GSI is created.</step>
    <step>Phase 2 step 2 -- Backfill: a one-time governed script (committed, run from the local repo per CLAUDE.md Rule 12 -- S3-staged if run on EC2) scans `trade_submissions`; for every row with a decision, writes `decided_at` if absent (= existing `approved_at` or `rejected_at`); and for any row lacking an `audit_events` list, appends a single synthetic `MIGRATED` event documenting that pre-TO-3 history is unreconstructable. Idempotent -- safe to re-run.</step>
    <step>Phase 2 step 3 -- Create the new GSI: add `by-approver-decided` (hash=`approver_email`, range=`decided_at`) to dynamodb.tf. terraform apply. Wait for the new GSI to reach ACTIVE (`aws dynamodb describe-table` -- IndexStatus ACTIVE; DynamoDB auto-backfills the index from rows that now carry both key attributes).</step>
    <step>Phase 2 step 4 -- Cutover: repoint `dashboard_api.get_by_approver` to query `by-approver-decided`. Deploy via terraform apply. Verify the approver decision-history view now returns rejected trades.</step>
    <step>Phase 2 step 5 -- Drop the old GSI: remove `by-approver` from dynamodb.tf. terraform apply (separate from the create -- one GSI op per UpdateTable). Verify only `by-approver-decided` remains.</step>
    <step>Phase 3 -- Confirm end state: a query of the new GSI for an approver with a known rejected trade returns that trade.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: infra/aws/terraform/trade-pipeline/dynamodb.tf (by-approver GSI, ~lines 105-110) + dashboard_api.py get_by_approver</run>
        <expect>The `by-approver` GSI is hash=approver_email range=approved_at; get_by_approver queries it. comp-* tools N/A (uninstrumented, PRD §5).</expect>
        <if_mismatch>If the GSI name or key schema differs from PRD §2.B B5, use the actual dynamodb.tf as source of truth and adjust the cutover steps accordingly.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/terraform.exe plan (for the create-GSI apply; then again for the drop-GSI apply)</run>
        <expect>The create-apply plan shows ONLY the addition of `by-approver-decided`. The drop-apply plan shows ONLY the removal of `by-approver`. Neither plan touches the table's base key schema, billing mode, or unrelated attributes.</expect>
        <if_mismatch>If a plan shows more than the single intended GSI change, STOP -- do not apply. A GSI op that also rewrites the table is a data-loss risk. Re-isolate the change.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>aws dynamodb query --index-name by-approver-decided for an approver_email with a known rejected trade</run>
        <expect>The rejected trade appears in the result -- it was absent from the old `by-approver` GSI (B5). The approver's decision history is now complete.</expect>
        <if_mismatch>If the rejected trade is still absent, the backfill did not write decided_at on that row, or the cutover did not land -- do not mark complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>
      A one-time backfill of existing `trade_submissions` rows is MANDATORY -- the new GSI is incomplete for historical rows without it.
      - Affected data: every existing row in `opal-trade-submissions` with a decision (`approved_at` or `rejected_at` set).
      - Backfill writes: `decided_at` (if absent); a synthetic `MIGRATED` audit_event (if the row has no `audit_events` list).
      - The backfill script is committed to the repo and run as a governed one-time op (idempotent). It is NOT a silver/bronze script -- no S3 prefix re-ingestion -- but the `<data_reprocess_scope>` discipline applies: the backfill is explicit, scoped to decided rows, and verified.
      - Verification: post-backfill, `aws dynamodb scan` count of rows with `decided_at` equals the count of rows with a decision; spot-check that a known historical rejected trade now carries `decided_at`.
      - Sequencing: the backfill runs AFTER the handler change is deployed (so new rows already carry decided_at) and BEFORE the new GSI is created (so the GSI auto-backfill picks up the historical rows).
    </reprocess_required>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py; infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py; infra/aws/terraform/trade-pipeline/dynamodb.tf
    also_in_to: TRSB_LEDGER.001-.004 (workflow_handler.py); TRSB_LEDGER.008 (dashboard_api.py); TRSB_LEDGER.006 (dynamodb.tf -- PITR/deletion-protection)
    last_write_owner: 0.7.0_AE_CloudOps owns workflow_handler.py + dashboard_api.py (serial lane). TRSB_LEDGER.006 (AE 0.5.0) also edits dynamodb.tf -- COORDINATE: TO-5 and TO-6 both touch dynamodb.tf. They edit DIFFERENT stanzas (TO-5 = GSI definitions; TO-6 = point_in_time_recovery + deletion_protection_enabled table attributes) but the SAME file. Whoever applies second must pull latest and confirm their terraform plan shows only their own change.
    required_action: AE 0.7.0 (TO-5) and AE 0.5.0 (TO-6) MCP each other before either commits dynamodb.tf. Recommended: TO-6 (small, fast, table-attribute-only) lands first; TO-5 then rebases its GSI stanza changes on top. Each agent's terraform plan must isolate to its own change (Phase-2 gate above).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">`handle_approve` and `handle_reject` both write a `decided_at` attribute; `approved_at` / `rejected_at` are retained unchanged.</ac>
    <ac id="AC2">The one-time backfill has run: every existing decided row carries `decided_at`; rows lacking `audit_events` carry a single synthetic `MIGRATED` event. The backfill script is committed and idempotent. Post-backfill row-count verification is in the session log.</ac>
    <ac id="AC3">A new GSI `by-approver-decided` (hash=approver_email, range=decided_at) exists and is ACTIVE; the old `by-approver` GSI is dropped. The create and the drop were separate terraform applies, each with a plan isolated to the single GSI change.</ac>
    <ac id="AC4">`dashboard_api.get_by_approver` queries the new GSI. An approver decision-history query returns trades the approver REJECTED -- empirically verified against a known rejected trade.</ac>
    <ac id="AC5">All deploys via terraform apply with 0-diff-after plans; pipeline git tag applied. dynamodb.tf changes coordinated with TO-6 per cross_domain_coordination.</ac>
    <ac id="AC6">No emoji. Session log with the Compiler Tools section + the full GSI cutover step log. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py</file>
    <file action="modify">infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py</file>
    <file action="modify">infra/aws/terraform/trade-pipeline/dynamodb.tf</file>
    <file action="create">a committed one-time decided_at + MIGRATED-event backfill script</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">workflow_handler.py decided_at write + dashboard_api.py GSI cutover + dynamodb.tf GSI repoint + backfill script, deployed across the planned create/cutover/drop sequence, pipeline tags applied.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section and the ordered GSI-cutover step log (handler deploy -> backfill -> create GSI -> wait ACTIVE -> cutover reads -> drop old GSI). RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not attempt an in-place GSI key-schema change -- DynamoDB does not permit it. The create-new / drop-old sequence is mandatory.</rule>
    <rule>Do not create and drop a GSI in the same terraform apply -- DynamoDB allows one GSI op per UpdateTable. Separate applies.</rule>
    <rule>Do not create the new GSI before the handler writes decided_at and the backfill has run -- the GSI would index incomplete data.</rule>
    <rule>Do not cut `get_by_approver` over to the new GSI before it reaches IndexStatus ACTIVE.</rule>
    <rule>Do not commit dynamodb.tf without confirming with AE 0.5.0 (TO-6) -- both TOs touch that file.</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1). Do not inline the backfill in an SSM command (Rule 12).</rule>
  </do_not>
</task_order>
