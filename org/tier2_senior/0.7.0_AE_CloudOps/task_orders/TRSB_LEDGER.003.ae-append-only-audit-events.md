<task_order>
  <metadata>
    <id>TRSB_LEDGER.003</id>
    <slug>ae-append-only-audit-events</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO~B decomposition of TRSB_LEDGER PRD v0.1). Phase 2 -- independent of Phase 1; sequenced after TO-2 on the AE 0.7.0 serial backend lane (shared file workflow_handler.py).</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- Pillar B. Closes holes B1 (no event log) and B3 (failure path silently erases the attempt -- "most serious hole" per PRD); snapshots actor authority (B7).</priority>
    <sla>2d wall.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.B B1/B3/B7; section 3.2 (append-only embedded audit_events); section 3.3 (per-stage record-completeness contract); section 6 TO-3; section 7 Q3 RESOLVED (embedded list, not a separate table).</prd>
    <ruling>CTO~B 2026-05-18: Q3 = embedded `audit_events` list on the submission item for v0.1. Atomicity with the status update is the deciding factor -- a separate table introduces a dual-write inconsistency window on the exact records that must have none. A separate `trade-audit-events` table is the documented scale-up path, NOT v1.</ruling>
  </references>

  <objective>
    Add an append-only `audit_events` list to every trade submission item so the trade carries an immutable, ordered record of every workflow action -- including failed execution attempts. This closes B1 (state is a destructive overwrite with no event log) and B3 (the execution failure path reverts the row and silently erases who tried, when, and why).
  </objective>

  <context>
    Today `update_submission` issues a DynamoDB `SET` on the live item -- no history, no record of prior values, no record of who acted beyond the single current `*_email` fields (B1). Worse (B3): on any exception during execute, `handle_execute` reverts `status->APPROVED`, `executed_at->None`, `executor_email->None`, `executor_name->None` -- a failed attempt leaves zero trace in DynamoDB, surviving only in retention-bounded CloudWatch logs.

    Target (§3.2): every submission item carries an append-only `audit_events` list. Each event is immutable, appended (never rewritten) via a DynamoDB `list_append` update expression:

      {
        "event": "SUBMITTED | APPROVED | REJECTED | EXECUTED | EXECUTION_FAILED",
        "actor_email": "<verified actor>",
        "actor_name": "<from trade-users record>",
        "actor_groups": ["approvers","executors"],   // snapshot at action time (B7)
        "timestamp": "<ISO-8601 UTC>",
        "outcome": "SUCCESS | FAILURE",
        "detail": "<rejection reason | failure error | brokerage | null>"
      }

    Embedded (not a separate table) per Q3: the append is atomic with the status update -- no dual-write window -- and is automatically captured by the S3 JSON snapshot (TO-4) and the parquet export. N is small (<= ~6 events/trade).

    Failure path (fixes B3): a failed execution appends an `EXECUTION_FAILED` event BEFORE any status revert. The status may still revert to `APPROVED` to permit retry, but the attempt -- actor, time, error -- is now durably recorded. Executor fields are no longer silently nulled into oblivion; the audit_events list is the durable trace.

    actor_groups snapshot (B7): each event records the `groups` the actor held AT action time -- so a later change to the executors list cannot rewrite history of what authority the actor had.

    Files: trade-submission-handler/src/submission_handler.py (the SUBMITTED event at row creation) and trade-workflow-handler/src/workflow_handler.py (APPROVED / REJECTED / EXECUTED / EXECUTION_FAILED).
  </context>

  <scope>
    <step>Phase 1 -- `submission_handler.py`: at row creation, initialize `audit_events` with the `SUBMITTED` event (actor = initiator, actor_groups snapshot, outcome SUCCESS).</step>
    <step>Phase 2 -- `workflow_handler.py`: `handle_approve` appends `APPROVED`; `handle_reject` appends `REJECTED` (detail = rejection reason); `handle_execute` appends `EXECUTED` on success. Every append uses a `list_append` update expression so it is atomic with the status update -- never a read-modify-write of the whole list.</step>
    <step>Phase 2 -- `handle_execute` failure path (B3 fix): on any exception in the execute block, append an `EXECUTION_FAILED` event (outcome FAILURE, detail = the error) BEFORE the status revert. The revert to `APPROVED` may stay (to permit retry) -- but the executor fields being nulled is no longer the only trace; the EXECUTION_FAILED audit event is the durable record.</step>
    <step>Phase 2 -- Each event snapshots `actor_groups` -- the `groups` list the actor held at action time, read from their trade-users row (B7).</step>
    <step>Phase 3 -- Deploy both Lambdas via terraform apply (CLAUDE.md Rules 1-6). Empirical end-to-end run.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: dynamodb.tf trade_submissions item schema + submission_handler.py update_submission + workflow_handler.py handle_execute revert block (~lines 347-353)</run>
        <expect>The item is schemaless beyond keys -- `audit_events` is a new top-level list attribute, no Terraform schema change. The revert block is confirmed at the cited lines. comp-* tools are N/A (uninstrumented, PRD §5).</expect>
        <if_mismatch>If the revert block is not where PRD §2.B B3 cites, locate it before writing -- the EXECUTION_FAILED append must land before whatever the actual revert is.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Empirical: run a trade through submit -> approve -> execute (success), and a separate trade through submit -> approve -> forced-failure execute</run>
        <expect>The success trade's `audit_events` holds the ordered set [SUBMITTED, APPROVED, EXECUTED] with actor_groups snapshots. The failed trade's `audit_events` holds [SUBMITTED, APPROVED, EXECUTION_FAILED] with EXECUTION_FAILED carrying outcome FAILURE + the error in detail -- even though the row status reverted to APPROVED.</expect>
        <if_mismatch>If EXECUTION_FAILED is absent on the forced-failure run, B3 is not fixed -- do not mark complete. The append must precede the revert.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>New code path -- `audit_events` is populated on future submit/approve/reject/execute invocations only. Historical rows predate the list and get no synthetic events here (a single synthetic `MIGRATED` event for historical rows is PRD R1's concern, folded into TO-5's backfill scope, not this TO). No silver/bronze script. No reprocessing of existing data by this TO.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py
    also_in_to: TRSB_LEDGER.001, .002, .004, .005 (workflow_handler.py); TRSB_LEDGER.009 stretch (submission_handler.py)
    last_write_owner: single agent -- 0.7.0_AE_CloudOps owns the AE backend serial lane. Execute after TO-2, before TO-4. One commit scope per TO.
    required_action: TO-3 follows TO-2 in-lane; no other agent edits workflow_handler.py or submission_handler.py during this wave.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Every trade submission item carries an `audit_events` list; the `SUBMITTED` event is written at row creation by submission_handler.py.</ac>
    <ac id="AC2">handle_approve / handle_reject / handle_execute each append their event (APPROVED / REJECTED / EXECUTED) via a `list_append` update expression, atomic with the status update.</ac>
    <ac id="AC3">The execute failure path appends an `EXECUTION_FAILED` event (outcome FAILURE, detail = error) BEFORE any status revert -- empirically verified by a forced-failure run that shows EXECUTION_FAILED in audit_events despite the row reverting to APPROVED.</ac>
    <ac id="AC4">Each event carries `event`, `actor_email`, `actor_name`, `actor_groups` (snapshot at action time), `timestamp` (ISO-8601 UTC), `outcome`, `detail` per the §3.2 schema.</ac>
    <ac id="AC5">Empirical end-to-end: a success trade shows [SUBMITTED, APPROVED, EXECUTED]; a forced-failure trade shows [SUBMITTED, APPROVED, EXECUTION_FAILED]. Both Lambdas deployed via terraform apply (0-diff plan); pipeline tag applied.</ac>
    <ac id="AC6">No emoji. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py</file>
    <file action="modify">infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py</file>
    <file action="reference">infra/aws/terraform/trade-pipeline/dynamodb.tf</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">workflow_handler.py + submission_handler.py append-only audit_events, deployed via terraform apply (0-diff plan), pipeline tag applied.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not use a read-modify-write of the whole audit_events list -- use a `list_append` update expression so the append is atomic with the status update (no lost-update window).</rule>
    <rule>Do not let the execute failure path revert the row before the EXECUTION_FAILED event is appended -- the append-before-revert order is the entire point of the B3 fix.</rule>
    <rule>Do not introduce a separate audit table -- Q3 ruling is embedded for v1.</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1).</rule>
  </do_not>
</task_order>
