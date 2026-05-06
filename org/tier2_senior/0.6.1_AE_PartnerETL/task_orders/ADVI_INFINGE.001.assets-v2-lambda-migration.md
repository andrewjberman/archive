<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFINGE.001</id>
    <project>ADVI_INFINGE</project>
    <title>assets_v2 migration to Lambda-native bronze pull (absorbs AUDIT-008.PERM; establishes Phase 1b template)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- Authored 2026-05-05 sprint mode per Andrew override "aint no tomorrow my friend, we're doing this all right now"; PRD v0.2 commit 050bd3695 §6 TO-1 spec; TO-1 ASSETS_V2 establishes Phase 1b template that TO-2/3/4/5 reuse. COMPLETE: commits 9e37d0b1c (vendor requests fix) + b81294f8b (terraform-deploy inf-pipeline-v1.7.20); inf-pipeline-v1.7.18 shipped; RAVC5 close confirmed per TO-2 staging note. -->
    <priority>high</priority>
    <estimated_effort>~0.5d AE per CTO PRD v0.2 §6.1; sprint compressed ~3-4h tonight target</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFINGE.md v0.2 (commit 050bd3695); §6 Phase 1b TO-1 (line 230-241); §3 Tier 2 path-2 architectural shape; §5.2 Compiler Evidence (AE 0.6.1 RAVC3 5-section deliverable)</ref>
    <ref type="phase_0_evidence">AE 0.6.1 Phase 0 RAVC3 (20260505T194541Z): Lambda-fits table (ASSETS_V2 = YES, ~150s wall, 300-500MB); JWT lifecycle map (SM primary + S3 fallback; Lambda IAM = secretsmanager:GetSecretValue + s3:GetObject; NO lambda:InvokeFunction for inf-jwt-trigger); Lambda packaging gotchas (sys.path co-location + LOCAL_PULLS_DIR patch)</ref>
    <ref type="salvage_reference">AE 0.6.1 C-gold authoring `04448b49c` — sentinel pattern + IAM enumeration + EventBridge structure preserved for TO-1 reference; Lambda body shifts from gold-runner SSM trigger → direct invocation of pull + convert</ref>
    <ref type="iam_pre_apply">AE 0.6.1 targeted IAM apply 2026-05-05T~19:40Z — `aws_iam_role_policy.inf_gold_qa_runner_s3` 0-diff covering silver/assets_v2/* + silver/api_dims/assets/* PutObject; closes AUDIT-003 + AUDIT-008 IAM gaps; **TO-1 IAM diff is now ZERO for QA-runner side**</ref>
    <ref type="absorbs">ADVI_INFLEC.AUDIT-008 — AUDIT-008.PERM standalone CANCELLED 2026-05-05T~18:13Z; closes when this TO ships; matrix flips RED-(c) → GREEN at AC5</ref>
  </references>

  <context>
    Phase 1b TO-1 establishes the Lambda-native pattern for REST-pull migration. AUDIT-008 root cause was `assets_v2` excluded from inf-silver-chain Lambda's SILVER_BUILDERS list (Phase C trigger never implemented). C-gold path was authored (04448b49c) but superseded by Andrew's Lambda-native architectural directive. TO-1 ships per-script Lambda that EXECUTES `pull_inflection_assets_v2.py` + `convert_assets_v2_to_silver.py` directly (NOT SSM trigger to gold-runner).

    Empirical Lambda fitness validated per AE 0.6.1 Phase 0 RAVC3: ~150s wall on 313 households / 24,205 rows / 944KB. Within 900s Lambda cap with ~75% margin.

    Lambda packaging strategy: zip co-location for `rate_limiter.py` + `jwt_freshness.py` (per AE 0.6.1 RAVC3 simpler than Layer for Phase 1); `LOCAL_PULLS_DIR` patch from `/var/task` to `/tmp/pulls`. JWT read pattern uses `assert_fresh_or_exit()` fail-fast; cron stagger handles staleness (Tier 1 JWT refresh at 12:00 UTC; this Lambda runs in 12:00-13:00 UTC window).

    SILVER_BUILDERS extension on `inf-silver-chain` Lambda — adds `assets_v2` to the silver-conversion list. This Lambda's bronze write (bronze/assets/{date}.parquet) triggers existing `_BRONZE_COMPLETE.json` sentinel on its OWN downstream silver chain via direct convert-call, NOT via inf-silver-chain (since this Lambda does both pull AND convert in single execution per Lambda-native pattern).

    **Naming convention locked per CTO ratify 20260505T~19:55Z (supersedes PRD v0.2 §6.1 draft language):**
    - Lambda function: `inf-api-assets-v2`
    - EventBridge rule: `inf-api-assets-v2-rule`
    - IAM execution role: `inf-api-assets-v2-role`

    Phase 1b family convention: `inf-api-{prefix}` for REST-pull execution Lambdas (assets-v2 / reps / positions / performance / transactions). Distinguishes from `inf-{role}-trigger` (trigger Lambdas like `inf-jwt-trigger`, `inf-bronze-trigger`) and `inf-{role}-chain` (chain orchestrators like `inf-silver-chain`).

    Tag bump discovery mandate: `git tag -l "inf-pipeline-v*" | sort -V | tail -5` BEFORE bump per CLAUDE.md MEMORY.md "Pipeline Tag Versioning — Critical Rule".
  </context>

  <phase id="1" when="before writing Lambda code or Terraform">
    <step>
      <run>git tag -l "inf-pipeline-v*" | sort -V | tail -5</run>
      <expect>Latest tag enumerated; pick next semver patch (likely inf-pipeline-v1.7.18 or v1.7.19 per current state)</expect>
      <if_mismatch>If tag list shows non-monotonic versions: investigate before bumping; do NOT skip versions arbitrarily per MEMORY.md guidance.</if_mismatch>
    </step>
    <step>
      <run>comp-iam service inf-api-assets-v2 (per CLAUDE.md auto-rule 3 — Lambda touches new boto3 calls)</run>
      <expect>NOT_INDEXED expected (Lambda doesn't exist yet pre-deploy); empirical IAM scope derived from PRD §6.1 spec: bronze/assets/* PutObject + silver/assets_v2/* PutObject + silver/api_dims/assets/* PutObject (note: last two ALREADY in QA-runner role; Lambda role inherits its own IAM block) + secretsmanager:GetSecretValue on orion/jwt/current* + s3:GetObject on opal-data-inf/orion/jwt/current.json + CW Logs + AWSLambdaBasicExecutionRole</expect>
      <if_mismatch>If `comp-iam service` returns indexed (Lambda was authored prior): cross-check existing IAM scope against PRD §6.1; reconcile.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io pull_inflection_assets_v2.py</run>
      <expect>Script enumerates as Phase 1 known-quantity per AE 0.6.1 RAVC3; bronze/assets/{date}.parquet write path confirmed</expect>
      <if_mismatch>If script not indexed: cross-check against AE 0.6.1 RAVC3 empirical wall-time + memory data; rely on RAVC3 if comp-pipescript silent.</if_mismatch>
    </step>
    <step>
      <run>comp-blast inf-silver-chain</run>
      <expect>Surface inf-silver-chain Lambda's SILVER_BUILDERS list current state; confirm assets_v2 NOT yet present (will be added in Phase 2 of this TO)</expect>
      <if_mismatch>If assets_v2 is already in SILVER_BUILDERS: skip Phase 2 step on inf-silver-chain edit; document.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implementation — Lambda code + Terraform module">
    <step>
      <run>Author Lambda function code at `infra/aws/lambda/inf-pipeline/inf-api-assets-v2/lambda_function.py`</run>
      <expect>Lambda handler invokes `pull_inflection_assets_v2.py` then `convert_assets_v2_to_silver.py` in sequence within single execution. Bundles `rate_limiter.py` + `jwt_freshness.py` from `data/orion/scripts/bronze/`. Patches `LOCAL_PULLS_DIR = Path("/tmp/pulls")`. JWT read via `assert_fresh_or_exit()` fail-fast (NO `recover_or_exit()` invocation; NO lambda:InvokeFunction for inf-jwt-trigger).</expect>
      <if_mismatch>If pull/convert script signatures don't match Lambda handler invocation pattern: refactor scripts to expose `def main(date: str)` entry point; document rationale in commit message.</if_mismatch>
    </step>
    <step>
      <run>Author Terraform module at `infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf` (or analogous shared lambdas.tf entry per existing pattern)</run>
      <expect>aws_lambda_function + aws_cloudwatch_event_rule (cron `0 12 * * ? *` placeholder; per-prefix offset within 12:00-13:00 UTC window; refine per OQ3 default in PRD §7) + aws_cloudwatch_event_target + aws_lambda_permission + aws_iam_role + aws_iam_role_policy (per Phase 1 Step 2 IAM enumeration) + aws_cloudwatch_log_group + aws_cloudwatch_metric_alarm (CW Alarm on 2 consecutive failures)</expect>
      <if_mismatch>If existing `inf-assets-trigger.tf` from C-gold authoring (`04448b49c`) conflicts: delete obsolete C-gold resources (Lambda + EventBridge + IAM role from that commit) in same Terraform plan; or re-target via `terraform state rm` if applied (NOT applied per HALT directive).</if_mismatch>
    </step>
    <step>
      <run>Edit `infra/aws/lambda/inf-pipeline/inf-silver-chain/lambda_function.py` to add `assets_v2` to SILVER_BUILDERS list (with comment crossref `# AC6: ADVI_INFINGE.001 TO-1 — assets_v2 silver-chain extension`)</run>
      <expect>SILVER_BUILDERS = [..., 'household_rep_mapping', 'positions_mv', 'assets_v2'] (or similar; preserve existing order, append). Phase 1 Step 4 comp-blast surface confirms safety.</expect>
      <if_mismatch>If silver-chain Lambda timeout headroom &lt;50% post-extension (per PRD §7 OQ4 trigger): consult CTO before proceeding; revisit dedicated S3 ObjectCreated trigger pattern instead of SILVER_BUILDERS extension.</if_mismatch>
    </step>
    <step>
      <run>Update `infra/aws/lambda/ci/lambda-source-map.json` with inf-api-assets-v2 entry</run>
      <expect>New entry per existing pattern (function_name + source_dir + handler + runtime); CI drift detection picks it up</expect>
      <if_mismatch>Per CLAUDE.md rule 4: every Lambda must have entry; if entry missing post-deploy, CI drift will catch.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="before terraform apply">
    <step>
      <run>.tools/terraform.exe -chdir=infra/aws/terraform/inf-pipeline plan -out=tfplan</run>
      <expect>Plan shows: ~9-10 resources to add (Lambda + EventBridge rule + target + permission + IAM role + 2-3 IAM policies + CW Log Group + CW Metric Alarm + lambda-source-map entry); 0 destroys; 1 change (potentially inf-silver-chain Lambda code if SILVER_BUILDERS extension via Lambda layer; if direct code edit, that's separate commit not Terraform-resourced)</expect>
      <if_mismatch>Unexpected destroys: investigate before apply. If destroying C-gold-authored resources from `04448b49c` (which were never applied per HALT): plan should NOT show destroys since those resources were never `terraform apply`-ed; OR if applied unnoticed: cross-check + reconcile.</if_mismatch>
    </step>
    <step>
      <run>comp-iam gaps</run>
      <expect>0 new permission gaps post-plan (since silver/assets_v2/* + silver/api_dims/assets/* PutObject already structurally applied via bonus IAM apply 2026-05-05T~19:40Z; new Lambda role IAM is net-new but scoped per Phase 1 Step 2 enumeration)</expect>
      <if_mismatch>Any gap surfaced: amend iam.tf before apply; do NOT proceed with gap.</if_mismatch>
    </step>
    <step>
      <run>.tools/safe-commit.sh --author "0.6.1_AE_PartnerETL &lt;0.6.1_AE_PartnerETL@opal.agent&gt;" -m "feat(ADVI_INFINGE.001): inf-api-assets-v2 Lambda-native bronze pull migration (Phase 1b TO-1; absorbs AUDIT-008.PERM)" -- infra/aws/lambda/inf-pipeline/inf-api-assets-v2/ infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf infra/aws/terraform/inf-pipeline/lambdas.tf infra/aws/lambda/ci/lambda-source-map.json infra/aws/lambda/inf-pipeline/inf-silver-chain/lambda_function.py</run>
      <expect>safe-commit.sh PASS — pathspec scoped + index clean. Owned-paths hook PASS — AE has authority on infra/aws/* + lambdas.tf.</expect>
      <if_mismatch>safe-commit abort: clean staged extras with `git reset HEAD -- &lt;path&gt;`; re-run.</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="terraform apply + tag">
    <step>
      <run>.tools/terraform.exe -chdir=infra/aws/terraform/inf-pipeline apply tfplan</run>
      <expect>Apply complete; resources counted match Phase 3 Step 1 plan; no errors</expect>
      <if_mismatch>Apply failure: read state; potentially split apply by resource group (Lambda first; EventBridge second). DO NOT force-recreate without consultation.</if_mismatch>
    </step>
    <step>
      <run>.tools/terraform.exe -chdir=infra/aws/terraform/inf-pipeline plan</run>
      <expect>0-diff plan post-apply; canonical state.</expect>
      <if_mismatch>Diff after apply = drift; investigate before tag bump.</if_mismatch>
    </step>
    <step>
      <run>git tag -a inf-pipeline-v{X.Y.Z} -m "ADVI_INFINGE.001 TO-1 — assets_v2 Lambda-native migration; absorbs AUDIT-008.PERM" &amp;&amp; git push origin --follow-tags</run>
      <expect>Tag {X.Y.Z} per Phase 1 Step 1 discovery + push successful</expect>
      <if_mismatch>If tag conflict: pick next non-conflicting patch.</if_mismatch>
    </step>
    <step>
      <run>aws cloudwatch describe-alarms --alarm-names {inf-pull-assets-v2-failure-alarm} (or analogous)</run>
      <expect>Alarm STATE_VALUE=OK or INSUFFICIENT_DATA initially; ACTIONS_ENABLED=true</expect>
      <if_mismatch>Alarm not present or misconfigured: re-author Terraform; re-apply.</if_mismatch>
    </step>
  </phase>

  <phase id="5" when="empirical functional test (24h smoke)">
    <step>
      <run>Empirical Lambda invocation: `aws lambda invoke --function-name inf-api-assets-v2 --payload '{"date": "2026-05-06"}' /tmp/lambda-test-output.json` (or wait for natural cron fire at next 12:00-13:00 UTC window)</run>
      <expect>Lambda invocation returns Statuscode 200; /tmp/lambda-test-output.json shows successful pull + convert; bronze/assets/2026-05-06.parquet + silver/assets_v2/2026-05-06.parquet written within ~150s wall</expect>
      <if_mismatch>Lambda timeout: increase timeout to 900s; if still fails, investigate per-prefix script-level wall time. Lambda OOM: increase memory beyond 512MB; cap at 10GB.</if_mismatch>
    </step>
    <step>
      <run>aws s3 ls s3://opal-data-inf/silver/assets_v2/ | tail -5 (24h post-deploy)</run>
      <expect>Fresh partition for D+1 date present without manual SSM dispatch (matches AC1)</expect>
      <if_mismatch>Missing partition 24h post-deploy: investigate Lambda execution log + EventBridge rule fire history; debug.</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**TO 1a-1 (lib drift CI check) preferably ships first** but NOT strict prerequisite. If CI ships post-TO-1, the structural detection catches future drift; doesn't block this TO.</coord>
    <coord>**Phase 1b TO-2/3/4/5 reuse this TO's Lambda module template.** Establish clean module pattern; subsequent TOs inherit.</coord>
    <coord>**SILVER_BUILDERS extension on inf-silver-chain (Phase 2 Step 3)** is the ONLY edit to existing Lambda. Avoid touching other dim builders. If timeout headroom &lt;50% post-extension, consult CTO before alternative trigger pattern.</coord>
    <coord>**Bonus IAM apply 2026-05-05T~19:40Z (`aws_iam_role_policy.inf_gold_qa_runner_s3`)** covered silver/assets_v2/* + silver/api_dims/assets/* PutObject for QA-runner role. NEW Lambda IAM role is independent — Phase 1 Step 2 enumeration.</coord>
    <coord>**Salvage reference `04448b49c`** AE 0.6.1 C-gold authoring is preserved on CLOUD as authoring reference. If TF resources from that commit show in `terraform plan`: they were never `terraform apply`-ed (per HALT 2026-05-05T~19:01Z). Plan should NOT show destroys for unapplied resources; cross-check.</coord>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_required>
      <reason>This TO migrates the assets_v2 ingestion path from gold-runner SSM (manual or pinch-hit) to Lambda-native daily cron. Going-forward: D+1 fresh ingestion. Historical data already in S3 from prior backfill (silver/assets_v2/2026-05-01..05 partitions present per AE 0.7 D2b). No backfill needed via this TO; ongoing daily ingestion handles it.</reason>
      <s3_prefix_globs>
        <glob>s3://opal-data-inf/bronze/assets/{date}.parquet (D+1 onwards)</glob>
        <glob>s3://opal-data-inf/silver/assets_v2/{date}.parquet (D+1 onwards)</glob>
      </s3_prefix_globs>
      <verification>aws s3 ls each prefix at D+1; LastModified > tag-bump timestamp; CW Metric increment</verification>
      <downstream_consumer_freshness_gate>Gold-tier scripts (INF_B_00 etc) read silver paths daily; cron stagger ensures gold scripts read fresh silver. No manual freshness coordination needed.</downstream_consumer_freshness_gate>
    </reprocess_required>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">
      <step>
        <run>git tag -l "inf-pipeline-v*" | sort -V | tail -5</run>
        <expect>Latest tag enumerated</expect>
        <if_mismatch>Investigate non-monotonic versions</if_mismatch>
      </step>
      <step>
        <run>comp-iam service inf-api-assets-v2</run>
        <expect>NOT_INDEXED pre-deploy; PRD §6.1 IAM enumeration applies</expect>
        <if_mismatch>Cross-check vs PRD</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io pull_inflection_assets_v2.py</run>
        <expect>Script enumerated; bronze write path confirmed</expect>
        <if_mismatch>Rely on AE 0.6.1 RAVC3 empirical</if_mismatch>
      </step>
      <step>
        <run>comp-blast inf-silver-chain</run>
        <expect>SILVER_BUILDERS surface; safety check for extension</expect>
        <if_mismatch>Document; revisit extension strategy</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>terraform plan + comp-iam gaps + safe-commit.sh</run>
        <expect>0 gaps; clean plan; safe-commit PASS</expect>
        <if_mismatch>Amend per surfaced issue</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after deploy">
      <step>
        <run>comp-iam service inf-api-assets-v2 + comp-pipescript deployed inf-api-assets-v2</run>
        <expect>Lambda indexed post-deploy; MATCH</expect>
        <if_mismatch>Investigate</if_mismatch>
      </step>
      <step>
        <run>24h empirical functional test (Lambda invoke + S3 verify)</run>
        <expect>Fresh silver/assets_v2/{D+1}/.parquet without manual SSM</expect>
        <if_mismatch>Per Phase 5 if_mismatch</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Fresh `silver/assets_v2/{D+1}.parquet` by 16:00 UTC without manual SSM dispatch (24h smoke post-deploy).</criterion>
    <criterion id="AC2">CW Metric `Opal/InflectionIngestion/AssetsV2Pulled` increments daily.</criterion>
    <criterion id="AC3">CW Alarm fires on 2 consecutive failures (test via 24h smoke; intentional Lambda fault if needed).</criterion>
    <criterion id="AC4">`comp-iam gaps` clean post terraform apply (expected ZERO new diff).</criterion>
    <criterion id="AC5">Matrix v10 row "Inflection AUA strip" flips RED-(c) → GREEN (matrix update routed via DS~A v10 patch process; lane-enforced via CTO commit).</criterion>
    <criterion id="AC6">SILVER_BUILDERS extension on inf-silver-chain Lambda (assets_v2 added with comment crossref to TO-1).</criterion>
    <criterion id="AC7">Tag bumped `inf-pipeline-v{next}` + pushed.</criterion>
    <criterion id="AC8">RAVC5 close package: commit hash + apply 0-diff verify + tag bump + Lambda invoke empirical evidence + comp-iam gaps clean output.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>2026-05-05T20:00:00Z (sprint dispatch per Andrew override)</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Sprint mode authoring + impl tonight. PRD v0.2 §6.1 is canonical spec; this TO transcribes + adds explicit phase mandate structure. Tag bump version-discovery mandate stands. Begin Phase 1 immediately. Standing by for RAVC3 (terraform plan clean + comp-iam gaps clean) before apply.</message>
  </go_signal>
</task_order>
