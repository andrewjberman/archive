<task_order>
  <metadata>
    <id>TRSB_TFIMPT.W1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-21</date>
    <status>complete</status>
    <closeout date="2026-04-21" commits="d1e27dfb, 62847274" tag="trade-pipeline-v1.3.0" mcp_complete="20260421T131104Z">
      47 min from GO (12:24:22Z) to COMPLETE (13:11:04Z). All 10 AC PASS. Phase 1 probe surfaced dormancy finding (trade-submission-handler 0 invocations/30d; no shadow-grant) — material for W2/W3 downstream, captured in TO addenda commits 57fb148a + b918fc4d + af0bb7e7 + 6dd9b0c3. AC#8 smoke substituted per COO GO 2026-04-21T13:02Z: IAM simulate-principal-policy on 5 CRUD actions — all allowed on opal-trade-submissions, old ARN implicitDeny (confirms old ARN was dead code). Pre/post DDB count 9=9=9 (metadata-only import). Two commits (feature + bookkeeping) due to CHANGELOG.json SHA self-reference. RAVC4-closed by COO.
    </closeout>
    <project_code>TRSB_TFIMPT</project_code>
    <priority>P1 (financial-txn DDB integrity; ~2-4h quick-win; clean wave)</priority>
    <sla>4h from GO</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/TRSB_TFIMPT.md (sections 1.G1, 3.Wave 1, 6.TO-1, 7, 9, 10)</ref>
    <ref type="source_brief">docs/analysis/2026-04-15_cloud_inventory_audit.md L129 (high — financial txns), L251 P1 recommendation</ref>
    <ref type="precedent_pattern">CDRS_TFIMPT.006 (opal-users-v2 DDB import, first-try 0-diff 2026-04-15 — closeout notes at that file L115-121 on SSE defaults, GSI recon-drives-implementation, composite-key spot-check)</ref>
    <ref type="precedent_pattern">AUTH_TFIMPT.002 (DynamoDB + SES + Secrets import 2026-04-06)</ref>
    <ref type="project_json">org/projects/TRSB_TFIMPT.json</ref>
    <ref type="target_files">infra/aws/terraform/trade-pipeline/{dynamodb,iam}.tf</ref>
  </references>

  <objective>
    Close G1: import the console-only `opal-trade-submissions` DynamoDB table into the trade-pipeline Terraform state, fix the wrong IAM ARN at `iam.tf:57`, and remove the stale "table does not exist in AWS" comment at `dynamodb.tf:4`. Single wave, single commit, single tag bump to `trade-pipeline-v1.3.0`.

    The table stores financial transaction records and is the highest-priority gap in the 2026-04-15 cloud inventory audit. `iam.tf:57` currently grants access to `trade-submissions` (non-existent resource) while the real table `opal-trade-submissions` is accessed via runtime hardcode in the Lambda code. Either (a) the Lambdas are silently receiving AccessDenied (unlikely — trade flow works) or (b) the IAM role has a broader grant elsewhere that shadows this specific ARN. Phase 1 probe resolves the hypothesis before the ARN change ships.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/terraform/trade-pipeline/dynamodb.tf (add `aws_dynamodb_table.trade_submissions` resource block matching live schema; remove stale comment at L4)</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/iam.tf (L57: replace `trade-submissions` ARN with `opal-trade-submissions` + `/index/*` wildcard for GSI access)</file>
      <file action="modify">infra/aws/terraform/trade-pipeline/CHANGELOG.json (per record-terraform-deploy.sh)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="ddb-import">
      1. `aws dynamodb describe-table --table-name opal-trade-submissions > /tmp/trade-submissions-live.json` — capture full schema (KeySchema, AttributeDefinitions, GSIs, TTL, PITR, StreamSpecification, SSE, Tags).
      2. Author `aws_dynamodb_table.trade_submissions` in `trade-pipeline/dynamodb.tf` matching live byte-for-byte. Follow CDRS_TFIMPT.006 precedent on SSE (AWS-managed KMS = no explicit `server_side_encryption{}` block needed) + GSI recon-drives-implementation (discover actual GSI count, don't assume).
      3. `terraform import aws_dynamodb_table.trade_submissions opal-trade-submissions` into trade-pipeline state (`opal-313476888478-terraform-state/trade-pipeline/tfstate`).
      4. Remove stale comment `# The trade-submissions table referenced in IAM policy does NOT exist in AWS` at `dynamodb.tf:4` (or equivalent wording).
      5. `terraform plan` → 0-diff. Fix any drift by editing TF to match live, NEVER by mutating live.
      6. `terraform apply` (no-op).
    </deliverable>
    <deliverable id="iam-arn-fix">
      1. Phase 1 probe: `aws iam get-role-policy --role-name trade-submission-lambda-role --policy-name <inline>` (or attached policies via `aws iam list-attached-role-policies`) — capture the full grant surface to understand why trade flow isn't broken today.
      2. Edit `iam.tf:57` — replace `arn:aws:dynamodb:us-east-1:313476888478:table/trade-submissions` (or wildcard equivalent) with `arn:aws:dynamodb:us-east-1:313476888478:table/opal-trade-submissions` + second line `arn:aws:dynamodb:us-east-1:313476888478:table/opal-trade-submissions/index/*` for GSI access.
      3. `terraform plan` → expect exactly 2 diffs: dynamodb.tf import (no change) + iam.tf policy statement replacement (change in place).
      4. `terraform apply`.
      5. Post-apply verify: `aws iam get-role-policy --role-name trade-submission-lambda-role` shows the new ARN pair.
      6. End-to-end smoke: Lambda can still read/write the table (live trade submission UI test). Risk envelope: if Lambdas were relying on a broader shadow-grant, tightening might break things — probe FIRST (Phase 1), change SECOND.
    </deliverable>
    <deliverable id="tag-and-push">
      1. Pre-tag: `git tag -l "trade-pipeline-v*" | sort -V | tail -5` — confirm next version is `v1.3.0` (current tip `trade-pipeline-v1.2.0`).
      2. `git commit --only --author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>" -m "infra(trade-pipeline): W1 DDB import + IAM ARN fix (TRSB_TFIMPT.W1)"` with explicit paths.
      3. `git tag -a trade-pipeline-v1.3.0 -m "..."` + `git push origin CLOUD --follow-tags`.
      4. Update `pipeline_inventory.xml` (if AE maintains one in deliverables) — +1 DDB row.
      5. Update `docs/analysis/2026-04-15_cloud_inventory_audit.md` (if COO-tracked): close G1 row, decrement P1 gap count.
    </deliverable>
  </deliverables>

  <wire_contract>
    Zero runtime behavior delta expected.
    - DDB import is metadata-only (no data mutation).
    - IAM ARN fix: current `trade-submissions` ARN refers to a non-existent table, so the policy statement is effectively dead. Replacing with `opal-trade-submissions` aligns the policy with live usage. Lambdas are already writing/reading successfully (trade flow works), so either a shadow-grant in another policy handles the real access, or IAM's "deny unless explicit" semantics mean the policy statement has been silently unused. Either way, explicit ARN is the correct state; Phase 1 probe confirms which scenario.
    - Stale comment removal is doc-only.
  </wire_contract>

  <acceptance_criteria>
    1. `aws_dynamodb_table.trade_submissions` resource in `trade-pipeline/tfstate`; resource ID = `opal-trade-submissions`.
    2. `terraform plan` 0-diff in trade-pipeline post-apply.
    3. All live attributes preserved: KeySchema, any/all GSIs, TTL enabled state, PITR state, stream spec, SSE config (check whether AWS-managed default applies — follow CDRS_TFIMPT.006 pattern).
    4. `iam.tf:57` references `opal-trade-submissions` + `/index/*` wildcard. Old `trade-submissions` ARN gone from the repo (`grep -r "trade-submissions[^-]" infra/aws/terraform/trade-pipeline/` returns zero non-`opal-trade-submissions` matches).
    5. Stale comment at `dynamodb.tf:4` removed.
    6. `git tag -l "trade-pipeline-v*"` includes `trade-pipeline-v1.3.0`; tag pushed to origin.
    7. `aws dynamodb scan --table-name opal-trade-submissions --select COUNT` returns a non-zero integer pre- and post-apply (count unchanged). Document baseline count in session log.
    8. End-to-end smoke test: submit one test trade through the UI (if §8 Q4 fixture is available) OR synthetic `aws lambda invoke` with a test payload (if Q4 is not yet resolved at W1 execution time). Write to DDB + CloudWatch log capture. Document in session log.
    9. Session log at `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-04-21/trsb_tfimpt_w1_ddb_import_and_iam_arn_fix.md` reproducing every `<run>` + observed-result + pass/fail vs `<expect>` (Rule 7 locked 2026-04-15).
    10. MCP COMPLETE to COO with commit hash + tag + probe evidence (pre/post ARN policy) + smoke-test evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws dynamodb describe-table --table-name opal-trade-submissions</run>
        <expect>Full table description returned — captures KeySchema + all GSIs + TTL + PITR + StreamSpec + SSE + Tags for byte-exact TF authoring. Record count via `--select COUNT` in a separate call (baseline for pre/post parity check).</expect>
        <if_mismatch>STOP. If ResourceNotFoundException, the table was deleted between PRD authoring and execution — surface to COO + CTO immediately.</if_mismatch>
      </step>
      <step>
        <run>terraform state list | grep -i trade_submissions</run>
        <expect>Zero matches (table is un-managed in trade-pipeline state). If `aws_dynamodb_table.trade_submissions` already exists, TO is moot — close with a note.</expect>
        <if_mismatch>If state reference found, another wave of work snuck the resource in — audit commits via `git log --all --oneline -- infra/aws/terraform/trade-pipeline/dynamodb.tf` before proceeding.</if_mismatch>
      </step>
      <step>
        <run>aws iam get-role-policy --role-name trade-submission-lambda-role --policy-name &lt;inline&gt; (enumerate via `aws iam list-role-policies` + `list-attached-role-policies`)</run>
        <expect>Full grant surface captured. Identify why trade flow works today despite `iam.tf:57` pointing at non-existent `trade-submissions` — probable answer: a broader shadow-grant (`dynamodb:*` or wildcard table ARN) exists on an attached policy, masking the specific broken statement.</expect>
        <if_mismatch>If only the broken ARN is present and no shadow-grant exists, the Lambdas SHOULD be getting AccessDenied — something else is load-bearing and must be understood before the ARN change ships. STOP and surface to COO.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service trade-submission-handler</run>
        <expect>"No service matching 'trade-submission-handler'" — baseline W2-gap signal. W1 does NOT fix this; W2 reclaims Lambda code which lets comp-iam index the function.</expect>
        <if_mismatch>If a real result returns, W2 may have shipped out-of-band — audit order-of-operations with COO.</if_mismatch>
      </step>
      <step>
        <run>grep -rn "trade-submissions\b" infra/aws/terraform/trade-pipeline/</run>
        <expect>Matches limited to `iam.tf:57` (the wrong ARN) + `dynamodb.tf:4` (stale comment). Any other hit must be understood before edit.</expect>
        <if_mismatch>If additional references found, document each and reconcile before committing.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>terraform plan</run>
        <expect>Exactly 1 import (aws_dynamodb_table.trade_submissions = 0-diff after-import match) + 1 in-place IAM policy statement change (ARN swap). NO other diffs.</expect>
        <if_mismatch>If additional diffs appear (e.g. drift on other resources from external edits), STOP. Reconcile via `terraform state show` + audit before any apply.</if_mismatch>
      </step>
      <step>
        <run>aws dynamodb scan --table-name opal-trade-submissions --select COUNT</run>
        <expect>Count matches Phase 1 baseline (DynamoDB import is metadata-only; data must not change).</expect>
        <if_mismatch>STOP — data touched during import. Investigate before any tag.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>terraform plan</run>
        <expect>0-diff post-apply.</expect>
        <if_mismatch>Post-apply drift = incomplete import. Capture delta, surface to COO; do NOT tag or mark complete.</if_mismatch>
      </step>
      <step>
        <run>aws iam get-role-policy --role-name trade-submission-lambda-role --policy-name &lt;inline&gt;</run>
        <expect>Policy document shows `arn:aws:dynamodb:us-east-1:313476888478:table/opal-trade-submissions` (+ `/index/*`). Old `trade-submissions` ARN gone.</expect>
        <if_mismatch>Apply didn't land the IAM change. Re-plan/re-apply; if still missing, halt and surface.</if_mismatch>
      </step>
      <step>
        <run>End-to-end smoke — single test trade submission via UI (if §8 Q4 fixture exists) OR `aws lambda invoke --function-name trade-submission-handler --payload &lt;synthetic&gt;` + `aws dynamodb scan --table-name opal-trade-submissions --limit 1 --select COUNT` before/after</run>
        <expect>Trade write succeeds; DDB row count increments by 1 (or expected N depending on fixture). CloudWatch trace shows authorizer + handler + DDB write + SES-email call chain.</expect>
        <if_mismatch>If AccessDenied surfaces post-apply, the IAM ARN change removed a grant the Lambda needed. Revert via `terraform apply` with the prior ARN; surface to COO + CTO.</if_mismatch>
      </step>
      <step>
        <run>comp-blast lambda:trade-submission-handler</run>
        <expect>Still empty (blast-graph gap persists — W2+W3 fix this downstream-visibility). Non-blocking for W1.</expect>
        <if_mismatch>If a result appears, W2 may have shipped concurrently — reconcile.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>Tag series: `trade-pipeline-v1.3.0`. Current tip is `trade-pipeline-v1.2.0` (2026-04-15 `6c98242f` recon CF). Run `git tag -l "trade-pipeline-v*" | sort -V | tail -5` before tagging to confirm no patch slipped in.</item>
    <item>No shared-infra touch. Stays in trade-pipeline tfstate per PRD §4 scope-negatives.</item>
    <item>No AE 0.6 conflict. AE 0.6 is executing HLOT2 + BFIX1/2 qa-runner cycle against `bd-gold-qa-runner` (c6a.8xlarge) on the BD pipeline. TRSB_TFIMPT.W1 touches trade-pipeline only — different pipeline, different state file, different AWS resources. Polite sequencing means don't fire `terraform apply` simultaneously with an AE 0.6 SSM if both lock the same state (they don't; different state keys).</item>
    <item>No portal/DT 0.4 touch. W3 will MCP-coordinate with DT 0.4 for CloudFront behavior adds; W1 doesn't touch CF.</item>
  </cross_domain_coordination>

  <dependencies>
    <dependency>None. This is the clean quick-win wave per PRD §3. W2 and W3 do NOT gate on W1, but conventional strict ordering per PRD §3 means ship W1 first.</dependency>
  </dependencies>

  <next>On commit + tag: MCP COMPLETE to COO with commit hash + tag + Phase 1 probe evidence (pre-change IAM grant surface) + Phase 3 smoke-test evidence + pre/post DDB count. COO flips TO status → complete, flags W2 unblocked (pending Andrew §8 Q2+Q4 answers).</next>
</task_order>
