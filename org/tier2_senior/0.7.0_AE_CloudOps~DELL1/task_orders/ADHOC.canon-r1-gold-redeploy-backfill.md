# pipeline-override: MDPF_CANON round 1 (decomposition v1, cells CN-a-2 and CN-a-3, drained @c45bce257c and @55c3cc4642); the round-1 issuance @155ac2ce67 is closed to new order files (ONE ISSUER PER ROUND), so the gold Lambda's redeploy and the round's two on-demand invocations ride one CloudOps ADHOC order, on the MDPF_HEALGAP R2-1 precedent.
<task_order id="ADHOC.canon-r1-gold-redeploy-backfill">
<to_id>ADHOC.canon-r1-gold-redeploy-backfill</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P1 -- AFTER ADHOC.canon-r1-gold-writer-iam is CLOSED (the roles must exist before the code that assumes them)</priority>

<title>MDPF_CANON CN-a-2/CN-a-3: redeploy mdpf-gold-lambda at 55c3cc4642, one qa_local read (zero writes), then the on-demand run_class=backfill</title>

<context>
- **What ships.** `mdpf-gold-lambda` runs `ff1a8867a6` (MDPF_STRATID's deploy, LastModified 2026-10-09T18:00:35Z; `2.0.0_SA_COO~S1`,
  msg 3040). `ff1a8867a6` is an ancestor of box/dell1 `55c3cc4642`. In that range the packaged files that change are:
  - MDPF_CANON's `mdpf_gold_parquet.py` (new), `mdpf_gold_backfill.py` (new), `mdpf_gold_consolidator.py` and `build_package.py`;
  - LGIC's `lib/opal_naming.py`, `infra/logic/registry/scopes.json` and `name_rulings.json`.
- **The naming builders do not move.** The issuer compared `address()`/`lookup()` at both pins over 28 vectors (TAXSMA's
  gold/state keys, the new gold keys, `lookup()` per scope): 0 differ and 0 refusals at either pin.
- **MDPF_STRATID's ask:** its files ship byte-equal to `ff1a8867a6`. Its acceptance read is the 2026-10-10 13:30Z
  `mdpf-scheduled-floor` fire.
- **Not served output.** The new writes are gold parquet at `address()` (the firm buckets via the gold-writer roles, the composite in
  `opal-data-mdpf`). No served key moves and no never-widen pair is owed. The legacy JSON emits are unchanged.
- **The order of acts:** (1) redeploy; (2) one `qa_local` invocation (CTO ruling 015625Z: zero S3 writes) as the daily path's read;
  (3) one `run_class=backfill` invocation, the deliberate act that writes the dated history. The next scheduled floor
  (2026-10-10 13:30Z) is the confirmation for the daily path, never the proof.
</context>

<scope>
1. **Do not start until `ADHOC.canon-r1-gold-writer-iam` is CLOSED.** Edit no source file, with ONE exception (AMENDMENT 1, issuer ruling on msg 3111): set the one literal `MDPF_GOLD_COMMIT` at `infra/aws/terraform/mdpf-pipeline/gold-lambda.tf:293` to `55c3cc4642...` (the full 40-character hash of the build pin), committed via safe-commit AFTER the build and BEFORE the apply. The stamp names the pin the package was built from (the file's own instruction), never the commit that carries it. The build stays `--pin 55c3cc4642`. The live stamp `e20899bce7` is already stale against the live code `ff1a8867a6`, and this redeploy makes it true.
2. Open a deploy ledger.
3. Build the package from the pinned commit: `python infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py --pin 55c3cc4642`.
4. Deploy by the function's own Terraform path, never `update-function-code`:
   - upload the zip to its code key with its content-sha256 metadata, as the last deploy did;
   - run a targeted plan/apply on `aws_lambda_function.mdpf_gold` in `infra/aws/terraform/mdpf-pipeline`: 0 to add, 1 to change, 0 to destroy.
   - The change is the code version plus the env gaining `GOLD_WRITER_ROLE_ARN_49FINANCIAL`, `_INFLECTION` and `_COTTONWOOD` (and the
     `MDPF_GOLD_COMMIT` stamp).
5. Invoke once with `{"qa_local": true}` and record the response. It writes nothing.
6. Invoke once with `{"run_class": "backfill"}` and record the response (`planned`, `tally`) and its log's `BACKFILL ...` lines.
7. Read the written partitions back (criteria). Close the ledger.
8. Report to `2.0.0_SA_COO~D1` with each criterion's output, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
</scope>

<paths>
infra/aws/terraform/mdpf-pipeline/gold-lambda.tf
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4,C5,C6,C7</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>the build at --pin 55c3cc4642: its BUILD_MANIFEST.json, and sha256 of dim_mdpf_aum_metrics.py and mdpf_category_registry.py in the zip against `git show ff1a8867a6:data/mdpf/scripts/gold/<file>`</invocation>
  <expect>the manifest lists mdpf_gold_parquet.py and mdpf_gold_backfill.py; both MDPF_STRATID files are byte-equal to ff1a8867a6</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the targeted plan on aws_lambda_function.mdpf_gold, then .tools/aws lambda get-function-configuration --function-name mdpf-gold-lambda</invocation>
  <expect>plan 0/1/0; live CodeSha256 equals the build's; Environment carries the three GOLD_WRITER_ROLE_ARN_* (each the arn of its mdpf-*-gold-writer-role) and MDPF_GOLD_COMMIT naming 55c3cc4642</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>.tools/aws lambda invoke --function-name mdpf-gold-lambda --payload '{"qa_local": true}' (cli-binary-format raw-in-base64-out)</invocation>
  <expect>a response with status and a4_objects_built; no error naming mdpf_gold_parquet; and NO new object under any mdpf/*/gold/ prefix of the four artifacts (zero writes)</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>.tools/aws lambda invoke --function-name mdpf-gold-lambda --payload '{"run_class": "backfill"}'</invocation>
  <expect>status "backfill", planned > 0, tally with written > 0, conflict 0, error 0; the log shows one "BACKFILL {scope}/{artifact}: n of m source dates (k already present)" line per series</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>.tools/aws s3api list-objects-v2 --bucket opal-data-49financial --prefix mdpf/49financial/gold/aum_metrics/ (count printed), and the same prefix count of opal-data-assets portal/gold/mdpf/49financial/aum-metrics/</invocation>
  <expect>one date=YYYY-MM-DD/data.parquet per legacy dated object (the counts match, denominators printed)</expect>
</criterion>
<criterion id="C6" judgment="false">
  <invocation>.tools/aws s3api list-objects-v2 --bucket opal-data-mdpf --prefix mdpf/global/gold/ --max-items 1000 (count printed per artifact)</invocation>
  <expect>the composite's partitions for the artifacts its legacy tree holds, each a date=YYYY-MM-DD/data.parquet</expect>
</criterion>
<criterion id="C7" judgment="false">
  <invocation>python .tools/deploy_ledger.py check</invocation>
  <expect>this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
