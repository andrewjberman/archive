<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-34.bd49f-dim-convert-memory-3008-and-one-invoke</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~NFRA2</issued_to>
    <date>2026-10-20</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
    <round>38</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round30.md</decomp_doc> (workstream OUTCOME, round 30, amendment 12): part 2 of the CTO's three-part fix for the 49F dim converter
<owned_cells>CT-ck-1</owned_cells>
</decomp_ref>

  <preflight>
comp-schedule: RUN -- the scheduler `opal-assets-bd49f-dim-convert-daily` (ENABLED, `cron(5 7 * * ? *)`, read live by the issuer 2026-10-20 ~18:4xZ, target input null so the handler default date is yesterday UTC) is READ and not changed. The next scheduled fire is 07:05Z on the next UTC day. The act below is a configuration change plus ONE invoke with an EMPTY event, which is exactly the scheduler's shape (no `date` override), so it creates no state the schedule cannot reach.
comp-iam: DECLARED-NOT-APPLICABLE no IAM or policy change. The seat's existing CloudOps role does `lambda:UpdateFunctionConfiguration` through `safe-apply` (Terraform) and `lambda:InvokeFunction`; the seat reads its own grant first and stops if either is refused.
comp-adversary: RUN -- a plan that carries more than the one change (the opal-assets root holds many resources and old plan files: the plan must show exactly ONE in-place change, else STOP); a memory change that also redeploys code (the live `CodeSha256` is read before and after and must be equal); an invoke that times out at the 900 s function limit (read the REPORT line: Duration and Max Memory Used; a timeout is reported, not retried blind); an invoke that overruns the CLI read timeout (use `--cli-read-timeout 960`); an invoke that writes a partition and is mistaken for success (read S3, not the return code); an invoke that touches an existing partition (the before/after listing of every older `date=` prefix, ETags equal); a second invoke (not allowed without the issuer's word); cost (3008 MB for the run time of one daily run, cents).
risk: WORLD -- a live Lambda configuration change by Terraform and one real run that writes new date partitions under `s3://opal-data-assets/blackdiamond/49f/silver/` and `.../meta/`; the run is the producer's own scheduled rule, not an override. COO half of the blast radius (the CTO's half is the record cited below): this one function's configuration only; the next run writes NEW `date=` partitions and touches no existing partition (the fold writes today's partition and reads the prior); rollback of the configuration is `memory_size = 1024` through the same `safe-apply`; the partitions the run writes stay until Andrew confirms any delete.
lane: the seat is `0.7.0_AE_CloudOps~NFRA2`, a SECOND lane for the NFRA macro on the laptop, seated by the issuer on the CTO's word "seat your own applier" (msg 109983) because the macro lane `~NFRA1` is BLOCKED on the Alongside box (its own summary, read 18:2xZ). NEVER-2 ledger opened first.
  </preflight>

  <precondition>
    The CTO's record: `org/tier1_exec/1.0.0_SA_CTO/deliverables/DIAG_BD49F_DIM_CONVERT_OOM_XREF_STALE_20261020.md` @e99ca8caa4 (read it whole: sections Measured, The fix, ROOT CAUSE). Live state read by the issuer at the cut: Lambda `opal-assets-bd49f-dim-convert` `MemorySize 1024`, `Timeout 900`, `CodeSha256 Iosob5LmSTxT+Z5PdEViWyVTNNO/U6ZB0ENgut2uuks=`, `LastModified 2026-07-17T16:27:58Z`; newest xref partition `s3://opal-data-assets/blackdiamond/49f/silver/dim_account_xref/date=2026-09-28/`.
  </precondition>

  <objective>
    Make the live Lambda `opal-assets-bd49f-dim-convert` run at 3008 MB, then invoke it ONCE with the scheduler's event, so the converter lands a new `date=` partition for the xref and the dims, restoring the cadence that has failed on out-of-memory every trading day since 2026-09-29. Memory is headroom only; the cause (a false SCD2 change on every account) is fixed by cell `CT-cl-1` and its apply leg, and a later cell compacts the history.
    The partition the invoke writes is named by the invoke's own return `{"date": "<D>", "rc": 0}`; with the default event D is yesterday UTC (2026-10-19 if you act before 00:00Z). The CTO's phrase "today's date" means the run the scheduler would have made; do NOT pass a `date` override.
  </objective>

  <context>
    Terraform: `infra/aws/terraform/opal-assets/bd49f_convert.tf:113` reads `memory_size = 1024` inside `module "bd49f_convert"`; the change is that one number, 3008. The function map `infra/aws/lambda/ci/function-map/opal-assets-bd49f-dim-convert.json` records `"memory_size": 1024` for the same function: change that one value to 3008 in the same commit so the two records agree (leave every other field, `artifact_sha256` and `last_deployed_*` included, as they are; no code is deployed by this order). Apply with `safe-apply` in the root `infra/aws/terraform/opal-assets` (CLAUDE.md: never a bare `terraform apply`); load `/cloud-ops` first. The infra graph: run `comp-aws`/`comp-iam gaps` as `/cloud-ops` directs before the edit; the graph is for reading, verify your own change against live AWS.
    The handler (`lambda_function.py`) reads `event["date"]` or defaults to yesterday UTC, runs `conv.main()` with `--date <D> --upload`, and raises on a nonzero rc. The converter refuses loud, and writes nothing, if the bronze `pull_complete` sidecar is absent, unreadable, for the wrong day, or has no rows; that refusal is a correct result to REPORT, not a defect to work around.
  </context>

  <steps>
    0. NEVER-2: open the ledger entry FIRST, `org/critical_paths/change_management/<UTC>_bd49f-dim-convert-memory-3008_deploy_completion.md` plus the `org/critical_paths/.open_deploys/<slug>.json` sentinel (via `deploy_ledger.py open`), naming the ONE consumer (the Lambda) and the invoke as part of the act; commit it OPEN, then act.
    1. Read live, record in the entry (BEFORE): `aws lambda get-function-configuration --function-name opal-assets-bd49f-dim-convert --region us-east-1` (MemorySize, Timeout, CodeSha256, LastModified); `aws s3api list-objects-v2` listings with ETags of `s3://opal-data-assets/blackdiamond/49f/silver/dim_account_xref/` and `.../silver/dim_advisor_fee_role/` (the converter's `DIM_TABLE`) and `.../meta/` to a scratch file, with the count of objects printed beside each (the denominator).
    2. Edit exactly `bd49f_convert.tf:113` (1024 to 3008) and the one `memory_size` value in the function map. `git diff` must show two changed lines. Commit both with `.tools/safe-commit.sh --author "0.7.0_AE_CloudOps~NFRA2 <0.7.0_AE_CloudOps~NFRA2@opal.agent>" -F <msgfile> -- <the two paths>`; the message file is written by a non-shell writer.
    3. `safe-apply` in `infra/aws/terraform/opal-assets`: read the PLAN first. It must show exactly ONE resource changed, in place, `memory_size 1024 -> 3008` on `module.bd49f_convert.aws_lambda_function.this`, and no other change. Any other change: STOP and report (do not apply). Then apply.
    3a. AMENDMENT 1 (issuer 2.0.0_SA_COO~C, 2026-10-20 ~19:0xZ, answering the seat's STOP, msg 109984): the plan read 2 add + 2 change because the root also carries another project's unapplied change (71495f3448e, NFRA_SCHWABBF TO-BF-i2: two `aws_iam_role_policy` adds and the `aws_s3_bucket_notification.monolith_bronze` rewrite). That change is NOT this order's and is NOT applied by it. RULING: apply ONLY `-target=module.bd49f_convert.aws_lambda_function.this` through `safe-apply` (if `safe-apply` refuses a `-target`, STOP and report; do not run bare `terraform apply`). The targeted plan must show exactly ONE change, in place, `memory_size 1024 -> 3008` on that resource, and nothing else; any other line in the targeted plan: STOP. Before the apply, print the untargeted plan's four resource addresses beside the targeted plan's one, and after the apply re-run the untargeted plan to show the SCHWABBF resources are still pending exactly as before (2 add + 1 change left, the memory change gone). Blast radius is unchanged from the preflight (this one function's configuration; rollback `memory_size = 1024`, also by `-target`). Record the `-target` use in the ledger entry.
    4. AFTER the apply: read the configuration again. MemorySize must read 3008, Timeout 900, and `CodeSha256` must EQUAL the BEFORE value (a memory change does not touch the code).
    5. THE ONE INVOKE: `aws lambda invoke --function-name opal-assets-bd49f-dim-convert --payload '{}' --cli-binary-format raw-in-base64-out --cli-read-timeout 960 --log-type Tail <outfile>` once, region us-east-1. Record the return (`StatusCode`, `FunctionError` if any, the payload) and, from the log group `/aws/lambda/opal-assets-bd49f-dim-convert` for this invoke's request id, the REPORT line (Duration, Max Memory Used) and the converter's lines `dim rows total ... | xref rows ...`. If the invoke fails, read the log and report it; do NOT invoke a second time without the issuer's word.
    6. READ S3: list the same three prefixes again. The new `date=<D>/` partition must be present under the xref and the dim and a result under meta; every object listed in step 1 must be present with the SAME ETag (no existing partition touched). Print both denominators.
    7. Close the ledger entry with the proof; write a report in the seat's `deliverables/`; flip this order.
  </steps>

  <stops>
    STOP and report (do not improvise) if: the plan shows any change beyond the one in-place `memory_size`; the BEFORE configuration is not 1024/900 with the recorded `CodeSha256`; the AFTER `CodeSha256` differs; the apply or the invoke is refused by IAM; the invoke returns a FunctionError or the REPORT line shows Max Memory Used at 3008 or a timeout (report the log: that means the memory is not enough and the issuer and the CTO decide the next step); an existing object's ETag differs after the run. ROLLBACK the configuration (`memory_size = 1024` through `safe-apply`) only if the CTO or the issuer says so; a partition the run wrote is NOT deleted by you.
  </stops>

  <proof_of_spec>
    <criterion id="CTck1-AC1" cell_refs="CT-ck-1"><invocation>aws lambda get-function-configuration --function-name opal-assets-bd49f-dim-convert --region us-east-1 --query '{m:MemorySize,t:Timeout,s:CodeSha256}'</invocation><expect>m 3008, t 900, s equal to the value read before the apply (Iosob5LmSTxT+Z5PdEViWyVTNNO/U6ZB0ENgut2uuks=)</expect></criterion>
    <criterion id="CTck1-AC2" cell_refs="CT-ck-1"><invocation>the one aws lambda invoke of step 5 with its REPORT line from the log group (request id stated)</invocation><expect>StatusCode 200, no FunctionError, payload rc 0 with the date stated, and Max Memory Used below 3008 MB</expect></criterion>
    <criterion id="CTck1-AC3" cell_refs="CT-ck-1"><invocation>aws s3api list-objects-v2 of s3://opal-data-assets/blackdiamond/49f/silver/dim_account_xref/ before and after (counts printed)</invocation><expect>a date= partition newer than 2026-09-28 present and every pre-existing object present with an equal ETag</expect></criterion>
  </proof_of_spec>

  <expected_criteria>CTck1-AC1,CTck1-AC2,CTck1-AC3</expected_criteria>
</task_order>
