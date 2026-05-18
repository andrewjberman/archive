<task_order>
  <metadata>
    <id>TRSB_LEDGER.004</id>
    <slug>ae-compliance-json-snapshot-status-model</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO~B decomposition of TRSB_LEDGER PRD v0.1). Phase 2 -- Andrew Q2 RESOLVED (retire COMPLETE), so this TO is dispatched WHOLE -- no 4a/4b split needed. Sequenced after TO-3 on the AE 0.7.0 serial backend lane.</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- Pillar B. Closes hole B4 (compliance JSON snapshot never written) and B2 (EXECUTED status never durably rests).</priority>
    <sla>1-2d wall.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md (v0.1) -- section 2.B B2/B4; section 3.5 (EXECUTED is the durable resting state); section 6 TO-4; section 7 Q2 RESOLVED.</prd>
    <ruling>Andrew 2026-05-18: Q2 = RETIRE `COMPLETE`. EXECUTED is the durable terminal state. The back-office handoff IS the last step -- there is no separate manual "confirmed settled" close. Remove the `COMPLETE` enum value (backend) and the orphaned `completeSubmission` FE function (the FE removal is TRSB_LEDGER.008b's scope, not this TO).</ruling>
  </references>

  <objective>
    Make `handle_execute` write the immutable compliance JSON snapshot of the trade-as-executed (fixes B4 -- `json_s3_key` is always null today), and make `EXECUTED` the durable resting state by stopping the same-invocation auto-advance to `COMPLETE` (fixes B2). Retire `COMPLETE` from the backend status model per Andrew's Q2 ruling.
  </objective>

  <context>
    B4: `json_s3_key` exists in the DynamoDB schema, the `TradeSubmission` TS type, and the parquet export schema -- but the only code that writes it is `excel_generator.lambda_handler`, which `handle_execute` does NOT call (it calls `generate_vident_excel` directly, ~line 283). Result: `json_s3_key` is always null; the immutable raw-JSON archive of the trade-as-executed is never created. The sole S3 artifact of an executed trade is the `.xlsx`.

    B2: `handle_execute` flips the row to `EXECUTED` (~line 267) then, in the SAME invocation, flips it to `COMPLETE` (~line 303). A table query never observes an `EXECUTED` row; `executed_at` and `completed_at` are milliseconds apart. The status enum advertises a resting state that does not exist.

    Target (§3.5, Q2): after a successful back-office handoff (Excel generated, S3-archived, email sent, JSON snapshot written), the trade RESTS at `EXECUTED`. `EXECUTED` is the terminal success state for the three-stage model Andrew described. `COMPLETE` is retired from the backend status enum/constants. The orphaned `completeSubmission` FE function + FE `COMPLETE` references are removed by TRSB_LEDGER.008b (portal lane) -- this TO is backend-only.

    The JSON snapshot must include the full row INCLUDING `audit_events` (TO-3 ships before this TO, so audit_events exists on the row by the time TO-4 runs).

    File: trade-workflow-handler/src/workflow_handler.py. S3 target: opal-data-trade-submissions (s3:PutObject already granted -- iam.tf ~line 70).
  </context>

  <scope>
    <step>Phase 1 -- Confirm `s3:PutObject` on `opal-data-trade-submissions` is already granted in iam.tf (~line 70 -- PRD §2.C says yes). No IAM change expected.</step>
    <step>Phase 2 -- In `handle_execute`, after the back-office handoff succeeds (Excel generated + S3-archived + email sent), write the immutable compliance snapshot: serialize the full submission row -- including `audit_events` -- to `submission.json` and PutObject it to opal-data-trade-submissions under a stable key. Set `json_s3_key` on the row to that key (fixes B4).</step>
    <step>Phase 2 -- Remove the same-invocation flip to `COMPLETE` (the ~line 303 advance). After a successful execute the row rests at `EXECUTED` (fixes B2). `executed_at` is set; there is no `completed_at` auto-write.</step>
    <step>Phase 2 -- Retire `COMPLETE` from the backend status enum / constants / any backend status-validation list. Backend code no longer produces or expects `COMPLETE`. (FE `completeSubmission` removal is TO-8b.)</step>
    <step>Phase 3 -- Deploy via terraform apply (CLAUDE.md Rules 1-6). Empirical execute run.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: infra/aws/terraform/trade-pipeline/iam.tf -- s3:PutObject grant on opal-data-trade-submissions</run>
        <expect>s3:PutObject on opal-data-trade-submissions already granted (PRD §2.C, iam.tf ~line 70). comp-iam N/A (uninstrumented, PRD §5). No IAM change.</expect>
        <if_mismatch>If the PutObject grant is absent or scoped to a different bucket/prefix, STOP and flag COO~B -- an iam.tf change escalates the TO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Direct read: confirm iam.tf unchanged; grep the backend for remaining `COMPLETE` references</run>
        <expect>Zero IAM delta. No backend code path still writes or asserts `COMPLETE` (FE references are out of scope -- TO-8b).</expect>
        <if_mismatch>If a backend path still references COMPLETE, retire it before commit -- a half-retired enum is a latent bug.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Empirical: execute a trade end-to-end on the deployed Lambda; then query the row and list S3</run>
        <expect>`json_s3_key` is non-null and the object exists in opal-data-trade-submissions; the JSON contains the full row including `audit_events`. The row status RESTS at `EXECUTED` (not COMPLETE); `completed_at` is not set.</expect>
        <if_mismatch>If json_s3_key is null or the status advanced past EXECUTED, the fix is incomplete -- do not mark complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Logic change to handle_execute -- affects only future executions. Historical `EXECUTED`/`COMPLETE` rows are left as-is: they are semantically valid at their prior version, and retiring the enum value does not require rewriting closed trades. No silver/bronze script. The dashboard/portal must tolerate legacy `COMPLETE` rows on read -- noted to TO-8b.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py
    also_in_to: TRSB_LEDGER.001, .002, .003, .005
    last_write_owner: single agent -- 0.7.0_AE_CloudOps owns the AE backend serial lane. Execute after TO-3, before TO-5. One commit scope per TO.
    note: `COMPLETE` retirement spans backend (this TO) + FE (`completeSubmission` removal, TRSB_LEDGER.008b). The two must agree -- TO-8b references this TO's Q2 resolution. Legacy `COMPLETE` rows remain in the table; TO-8b's FE must render them without error.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">`handle_execute` writes an immutable `submission.json` (the full row including `audit_events`) to opal-data-trade-submissions and sets `json_s3_key` non-null on the row.</ac>
    <ac id="AC2">The same-invocation auto-advance to `COMPLETE` is removed; after a successful execute the row rests at `EXECUTED`. `executed_at` is set; `completed_at` is not auto-written.</ac>
    <ac id="AC3">`COMPLETE` is retired from the backend status enum / constants / validation lists -- no backend path produces or asserts it.</ac>
    <ac id="AC4">Empirical execute run: `json_s3_key` non-null, the S3 object exists and contains audit_events, and the row status is `EXECUTED`. Deployed via terraform apply (0-diff plan); pipeline tag applied.</ac>
    <ac id="AC5">No emoji. Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py</file>
    <file action="reference">infra/aws/terraform/trade-pipeline/iam.tf</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">workflow_handler.py compliance JSON snapshot + EXECUTED-rests + COMPLETE retirement, deployed via terraform apply (0-diff plan), pipeline tag applied.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not write the JSON snapshot before the back-office handoff succeeds -- the snapshot is the trade-as-executed; it must reflect the completed handoff.</rule>
    <rule>Do not retire `COMPLETE` from FE code -- that is TO-8b's scope. This TO is backend-only.</rule>
    <rule>Do not rewrite or migrate historical `COMPLETE` rows -- they stay; the FE tolerates them on read.</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1).</rule>
  </do_not>
</task_order>
