<task_order>
  <metadata>
    <id>TRSB_LEDGER.001</id>
    <slug>ae-group-auth-enforcement</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO~B decomposition of TRSB_LEDGER PRD v0.1). Phase 1 -- no hard dependency on TO-0; sequenced after TO-0 on the AE 0.7.0 serial backend lane (shared file workflow_handler.py).</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- Pillar A. Closes hole A1 (no role/group authorization on approve/reject/execute).</priority>
    <sla>1-2d wall.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.A A1/A2 (no authorization gate; two unenforced authority concepts); section 3.1 (groups is the single source of truth); section 6 TO-1; section 7 Q1 RESOLVED (role demoted, not removed).</prd>
    <ruling>CTO~B 2026-05-18: Q1 = (a) demote `role` to a display + dev-segregation-bypass attribute. Do NOT remove it -- removal is a migration with zero functional benefit. `groups` is canonical for authorization.</ruling>
  </references>

  <objective>
    Add server-side group-membership authorization to `trade-workflow-handler` so the set of users who can execute a trade is exactly the `executors` group, and approve/reject is exactly the `approvers` group -- enforced, not advisory. This closes hole A1: today every handler carries the explicit comment "No role restriction - any whitelisted user can [approve/reject/execute]."
  </objective>

  <context>
    `workflow_handler.py`: `handle_approve` (~line 168), `handle_reject` (~line 216), `handle_execute` (~line 261) currently enforce only segregation-of-duties (initiator != approver != executor, `lambda_handler` ~lines 118-138). There is no group/role gate. A `trade-users` row carries both a single-string `role` and a multi-valued `groups` list; today neither gates the action -- `groups` only drives the notification email.

    Target (§3.1): authorization is group-membership-based. `approvers` group -> may approve and reject. `executors` group -> may execute. A user may hold both. A user in neither cannot perform that action -> 403. `dev` retains the segregation-of-duties bypass for testing but does NOT bypass group membership -- a dev must still be in the relevant group to act (no silent superuser on workflow actions). The single-string `role` field is demoted to a display / segregation-bypass attribute (Q1 ruling) -- it is NOT removed.

    File: infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py. Deployed via Terraform per CLAUDE.md Rule 1 (lambdas.tf in infra/aws/terraform/trade-pipeline/).
  </context>

  <scope>
    <step>Phase 1 -- In `handle_approve` and `handle_reject`: immediately after the segregation-of-duties check, add an explicit check that the acting user's `trade-users` row carries `approvers` in its `groups` list. In `handle_execute`: same, requiring `executors`. On failure: return 403 with a specific message naming the missing group (e.g. "User {email} is not in the executors group and cannot execute trades").</step>
    <step>Phase 1 -- `dev` handling: `dev` keeps the segregation-of-duties bypass (may act on own-initiated trades for testing) but is still subject to the group check -- a `dev` not in `executors` still cannot execute. No silent superuser.</step>
    <step>Phase 1 -- Canonicalize on `groups`: the new checks read `groups`, not `role`. Leave the `role` field in place and untouched (Q1 -- demoted, not removed); it may still be read for display / the dev-segregation bypass.</step>
    <step>Phase 2 -- Unit coverage: a non-executor is denied execute (403); an executor who is not the approver is allowed to execute; an approver not in `executors` is denied execute; a user in neither group is denied both. Remove the stale "No role restriction" comments.</step>
    <step>Phase 3 -- Deploy via terraform apply per CLAUDE.md Rules 1-6 (commit -> source map -> plan -> apply -> 0-diff -> tag). Smoke the deployed Lambda.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: infra/aws/terraform/trade-pipeline/iam.tf (trade-submission-lambda-role)</run>
        <expect>No new IAM needed -- the role already grants dynamodb:GetItem/Query on trade-users (PRD §2.C, iam.tf ~lines 47-78). comp-iam does not model trade-* Lambdas (PRD §5); direct iam.tf read is the sanctioned substitute. Confirm: no IAM delta.</expect>
        <if_mismatch>If the group check requires a DynamoDB action not already granted, STOP and flag to COO~B before writing -- an iam.tf change escalates the TO scope.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Direct read: confirm iam.tf unchanged by this TO</run>
        <expect>Zero IAM delta -- TO-1 is pure handler logic on already-granted permissions.</expect>
        <if_mismatch>If iam.tf changed, run comp-iam gaps is N/A (uninstrumented) -- instead document the new grant + rationale in the session log and flag COO~B.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Deployed-Lambda smoke: invoke handle_execute as a user NOT in the executors group against an APPROVED trade</run>
        <expect>403 with the specific "not in the executors group" message. The trade status does NOT advance.</expect>
        <if_mismatch>If a non-executor can still execute, the gate is not wired -- do not mark complete; re-trace the check placement (must be after segregation, before the state change).</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Logic change to a Lambda handler -- affects only future approve/reject/execute invocations. No silver/bronze script, no historical data write, no S3 prefix. Existing trade rows are semantically correct at their prior version; no consumer reads the changed code path for already-decided trades.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py
    also_in_to: TRSB_LEDGER.002, .003, .004, .005 (all edit workflow_handler.py)
    last_write_owner: single agent -- 0.7.0_AE_CloudOps owns the entire AE backend serial lane (TO-0,1,2,3,4,5,8). These TOs are NOT parallelized across agents precisely because they share this file (CTO~B 2026-05-18: splitting would be false parallelism + merge contention).
    required_action: Execute TO-1 -> TO-2 -> TO-3 -> TO-4 -> TO-5 in order, one commit scope per TO. Pull latest before each. No other agent edits workflow_handler.py during this wave.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">`handle_approve` and `handle_reject` reject (403, specific message) any actor whose trade-users `groups` list lacks `approvers`; `handle_execute` rejects any actor lacking `executors`.</ac>
    <ac id="AC2">Segregation-of-duties (initiator != approver != executor) is still enforced -- unchanged. `dev` keeps the segregation bypass but is still subject to the group check.</ac>
    <ac id="AC3">The checks read `groups`; the `role` field is left in place and untouched (Q1 -- demoted, not removed). The stale "No role restriction" comments are removed.</ac>
    <ac id="AC4">Unit tests cover: non-executor denied execute; executor-not-approver allowed execute; user-in-neither-group denied both. Tests pass.</ac>
    <ac id="AC5">Deployed-Lambda smoke: a non-executor execute attempt returns 403 and does not advance the trade. Deployed via terraform apply with a 0-diff plan; pipeline git tag applied.</ac>
    <ac id="AC6">No emoji in code, logs, or print statements. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py</file>
    <file action="reference">infra/aws/terraform/trade-pipeline/iam.tf</file>
    <file action="reference">infra/aws/terraform/trade-pipeline/lambdas.tf</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">workflow_handler.py group-authorization enforcement, deployed via terraform apply (0-diff plan), pipeline tag applied.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not remove or migrate the `role` field -- Q1 ruling is demote-not-remove. Removing it is out of scope.</rule>
    <rule>Do not deploy via `aws lambda update-function-code` or the console -- Terraform only (CLAUDE.md Rule 1).</rule>
    <rule>Do not give `dev` a group-membership bypass -- `dev` bypasses segregation only, never group membership.</rule>
  </do_not>
</task_order>
