<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-35.bd49f-dim-convert-fixed-code-deploy</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~NFRA2</issued_to>
    <date>2026-10-20</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
    <round>40</round>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round30.md</decomp_doc> (workstream OUTCOME, round 30, amendment 13): the apply leg of cell `CT-cl-1` (the built cell is `CT-cl-1`, merged @82484219d4b)
<owned_cells>CT-cm-1</owned_cells>
</decomp_ref>

  <preflight>
comp-schedule: RUN -- the scheduler `opal-assets-bd49f-dim-convert-daily` (ENABLED, `cron(5 7 * * ? *)`) is READ and not changed. The next fire is 07:05Z on the next UTC day; the deploy below must be finished and read back before 06:30Z so that fire runs the fixed code. NO invoke is made by this order (see the context: an invoke for yesterday UTC would overwrite the partition `TO-APPLY-34` wrote).
comp-iam: DECLARED-NOT-APPLICABLE no IAM or policy change; the seat's existing CloudOps role uploads to the artifact bucket and applies through `safe-apply`, as in `TO-APPLY-34`. The seat reads its own grant first and stops if refused.
comp-adversary: RUN -- the wrong bytes zipped (the deployed file inside the zip is hashed against the repo file at the pin, with a one-byte negative control); a plan that carries more than the code swap (the SCHWABBF change `71495f3448e` is still pending in this root: use `-target`, as in `TO-APPLY-34` step 3a); a deploy that also changes memory or timeout (read before and after); an unreadable import closure (the build script's own gates; `stream_parquet.py` stays in the zip); a stale rollback (the prior artifact `VersionId` and `CodeSha256` recorded BEFORE the upload); a deploy landing inside the 07:05Z window; cost (none).
risk: WORLD -- a live Lambda code swap by Terraform. COO half of the blast radius: this one function's code; behaviour changes only in `scd2_fold`'s comparison (identical rows now read unchanged; a real change still closes), it writes only NEW `date=` partitions on its next scheduled run and rewrites nothing that exists; rollback is re-pointing to the prior S3 object version recorded before the upload, through the same `safe-apply -target`.
lane: the seat is `0.7.0_AE_CloudOps~NFRA2` (the second NFRA lane seated for `TO-APPLY-34`); NEVER-2 ledger opened first.
  </preflight>

  <precondition>
    The build cell `CT-cl-1` is merged on `box/laptop` @82484219d4b (close commit cfbcc72a667). The pin file: `data/assets/scripts/silver/bd49f_dim_conversion.py` AND the vendored copy `infra/aws/lambda/opal-assets/opal-assets-bd49f-dim-convert/bd49f_dim_conversion.py` have sha256 `bc3019570d49ac1ee10d7cd7668dfdc23a09e938d14dece7abd7c662cf00d503` (the issuer read both at the merge; `BUILD_MANIFEST.json` `vendor_sha256` carries the same value). Its tests: `29 passed` (base 26). The issuer's read-only seam probe on the real stored dim at `date=2026-09-28`: the unfixed file closes 5338 of 5338 open accounts, the fixed file 0, a one-real-change control 1. Live state after `TO-APPLY-34`: `MemorySize 3008`, `Timeout 900`, `CodeSha256 Iosob5LmSTxT+Z5PdEViWyVTNNO/U6ZB0ENgut2uuks=`; newest partitions `date=2026-10-19` (xref and dim, 288,194 dim rows).
  </precondition>

  <objective>
    Make the live Lambda `opal-assets-bd49f-dim-convert` run the fixed converter, so the next scheduled fire (07:05Z, as-of date yesterday UTC) folds with the schema-typed comparison and does not reopen every account again. Memory stays 3008 (the history already written stays 288k rows until the compaction cell).
  </objective>

  <context>
    The module `yang-lambda` reads the artifact `s3://opal-313476888478-lambda-artifacts/opal-assets/opal-assets-bd49f-dim-convert.zip` by its S3 object version and its `content-sha256` metadata; the Terraform update runs when a new version is uploaded. Method: the ledger `org/critical_paths/change_management/20260717T1615Z_opal-assets-bd49f-dim-convert-vendor-fix_deploy_completion.md` (legs 2-6) and `infra/aws/lambda/ci/build-and-upload.sh` (read its header: `bash infra/aws/lambda/ci/build-and-upload.sh opal-assets opal-assets-bd49f-dim-convert`; `BUILD_ONLY=1` builds and prints the zip path and sha256 without uploading). The source must be committed (it is, @82484219d4b). The script updates the function's own file under `infra/aws/lambda/ci/function-map/` (`artifact_sha256`, and the deploy fields): commit that change with the ledger.
    Do NOT invoke the Lambda. The converter's rule for an event `{"date": D}` is a same-key overwrite of the partitions for D; an invoke with the default event today would be yesterday UTC = 2026-10-19 and would OVERWRITE the partition `TO-APPLY-34` wrote, which is a served-history rewrite that needs a never-widen pair. The behaviour proof is the deployed-bytes diff plus the issuer's seam probe run on the deployed bytes (criteria below); the next scheduled fire is the standing proof, read by the issuer after 07:15Z.
    The box CLI is v1: do not pass `--cli-binary-format` to any aws call.
  </context>

  <steps>
    0. NEVER-2: open the ledger entry FIRST, `org/critical_paths/change_management/<UTC>_bd49f-dim-convert-fixed-code_deploy_completion.md` plus the `org/critical_paths/.open_deploys/<slug>.json` sentinel (via `deploy_ledger.py open`), naming the ONE consumer (the Lambda); commit it OPEN, then act.
    1. BEFORE, recorded in the entry: `aws lambda get-function-configuration` (MemorySize, Timeout, CodeSha256, LastModified); `aws s3api head-object` and `list-object-versions` for the artifact key (the CURRENT `VersionId`, `LastModified`, `content-sha256` metadata): this is the rollback. Read the file sha256 at the pin: `git show 82484219d4b:data/assets/scripts/silver/bd49f_dim_conversion.py | sha256sum` must read the value in the precondition (STOP if not).
    2. Window: it is before 06:30Z of the next UTC day. Say the time.
    3. Build and upload: `bash infra/aws/lambda/ci/build-and-upload.sh opal-assets opal-assets-bd49f-dim-convert`. It must report the closure gate clean. Record the printed zip sha256.
    4. `safe-apply` with `-target=module.bd49f_convert.aws_lambda_function.this` in `infra/aws/terraform/opal-assets`: read the PLAN first. It must show exactly ONE change, in place, on that resource (`source_code_hash` and `s3_object_version`), and no `memory_size` or `timeout` change. Any other line: STOP. Print the untargeted plan's resource list beside the targeted one (the SCHWABBF resources stay pending for their owner and are not applied here). Then apply.
    5. AFTER: `aws lambda get-function-configuration`: MemorySize 3008, Timeout 900, `CodeSha256` DIFFERENT from the BEFORE value and equal to the zip's base64 sha256 from step 3. A targeted re-plan reads `No changes`.
    6. DEPLOYED BYTES: `aws lambda get-function --function-name opal-assets-bd49f-dim-convert --query Code.Location`, download that package to a scratch folder of its own (never run anything from inside it), extract `bd49f_dim_conversion.py` and `stream_parquet.py`, and hash them. The first must equal the pin sha256; run the one-byte-changed negative control and show it reads UNEQUAL.
    7. SEAM PROBE ON THE DEPLOYED BYTES: `python -I org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/seam_probe_bd49f_scd2.py <the extracted bd49f_dim_conversion.py>` (read-only: it reads the stored dim at `date=2026-09-28` and writes nothing). Report its last three lines. It must read `newly_closed=0 of 5338` and the control `newly_closed=1`. Run the same script on the BEFORE zip's file as the negative control if the seat can fetch it (the prior object version); it reads `newly_closed=5338`.
    8. Close the ledger entry (record-terraform-deploy and the tag as the 2026-07-17 ledger did; LOCAL, push is the integrator's), commit the function-map change with it, write a report in `deliverables/`, flip this order.
  </steps>

  <stops>
    STOP and report (do not improvise) if: the pin sha256 differs; the targeted plan shows any change beyond the code swap; the AFTER `CodeSha256` equals the BEFORE value or `MemorySize` is not 3008; the deployed file's sha256 differs from the pin; the seam probe on the deployed bytes does not read `newly_closed=0`; the time passes 06:30Z before the apply (do not apply inside the 07:05Z fire; report). ROLLBACK to the recorded prior object version only if the deployed bytes or the probe fail; do not delete any partition, and do not invoke.
  </stops>

  <proof_of_spec>
    <criterion id="CTcm1-AC1" cell_refs="CT-cm-1"><invocation>aws lambda get-function Code.Location download, sha256 of bd49f_dim_conversion.py extracted from the deployed package against `git show 82484219d4b:data/assets/scripts/silver/bd49f_dim_conversion.py`</invocation><expect>equal to bc3019570d49ac1ee10d7cd7668dfdc23a09e938d14dece7abd7c662cf00d503, with a one-byte-changed negative control reading unequal</expect></criterion>
    <criterion id="CTcm1-AC2" cell_refs="CT-cm-1"><invocation>aws lambda get-function-configuration --function-name opal-assets-bd49f-dim-convert --region us-east-1 --query '{m:MemorySize,t:Timeout,s:CodeSha256}'</invocation><expect>m 3008, t 900, s different from Iosob5LmSTxT+Z5PdEViWyVTNNO/U6ZB0ENgut2uuks= and equal to the built zip's sha256</expect></criterion>
    <criterion id="CTcm1-AC3" cell_refs="CT-cm-1"><invocation>python -I org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/seam_probe_bd49f_scd2.py on the bd49f_dim_conversion.py extracted from the deployed package</invocation><expect>FOLD same-rows: newly_closed=0 of 5338 open and CONTROL one real flat_fee change: newly_closed=1</expect></criterion>
  </proof_of_spec>

  <expected_criteria>CTcm1-AC1,CTcm1-AC2,CTcm1-AC3</expected_criteria>
</task_order>
