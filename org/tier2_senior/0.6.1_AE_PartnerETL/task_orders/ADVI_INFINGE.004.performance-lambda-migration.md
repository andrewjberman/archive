<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFINGE.004</id>
    <project>ADVI_INFINGE</project>
    <title>PERFORMANCE migration to Lambda-native bronze pull (Phase 1b TO-4; reuses TO-2 layer + module template)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>pending</status><!-- Flipped staged→pending 2026-05-05T~21:38Z post TO-3 RAVC5 close (inf-pipeline-v1.7.20 LIVE; positions_mv silver 24,205 rows confirmed; layer drop-in 31.5KB). Note: TO-3 surfaced dim-name convention positions_mv (per convert_orion_api_to_silver.py DIM_BUILDERS) + rate_limiter key suffix _positions_mv (not _positions). For TO-4 PERFORMANCE: verify dim-name in DIM_BUILDERS + rate_limiter key suffix matches actual runtime observation BEFORE TF apply. PRD v0.2 commit 050bd3695 §6.2 TO-4 spec. -->
    <priority>high</priority>
    <estimated_effort>~30-60min AE post TO-3 ship; pure clone+prefix substitute (no Phase 0; layer already published)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFINGE.md v0.2 (commit 050bd3695); §6 Phase 1b TO-4</ref>
    <ref type="template_reference">TO-2/TO-3 (ADVI_INFINGE.002/003) — Phase 0 layer + Phase 1 Lambda module pattern. TO-4 reuses verbatim with prefix substitution `positions` → `performance`.</ref>
    <ref type="phase_0_evidence">AE 0.6.1 Phase 0 RAVC3 — PERFORMANCE Lambda-fits: YES (~90s wall, &lt;256MB memory, ~30-50 API calls). Lambda config 3072MB/900s sufficient.</ref>
  </references>

  <context>
    PERFORMANCE pull script (`pull_inflection_performance.py`) is mid-scope Phase 1b migration. ~30-50 API calls; ~90s wall; <256MB memory. Lambda-fits.

    Bronze output paths:
    - `bronze/orion-api-v2/{date}/performance.json`

    Silver convert outputs:
    - `silver/api_dims/performance/{date}/data.parquet`

    **Critical:** PERFORMANCE reads fresh `household_rep_mapping.json` from REPS (TO-2) for advisor attribution. EventBridge cron `cron(55 12 * * ? *)` = 12:55 UTC, fires 5min after TO-3 POSITIONS (12:50 UTC).

    Naming per CTO ratify 20260505T~19:55Z:
    - Lambda function: `inf-api-performance`
    - EventBridge rule: `inf-api-performance-rule`
    - IAM execution role: `inf-api-performance-role`
  </context>

  <phase id="1" when="before writing — gates on TO-3 ship">
    <step>
      <run>Verify TO-3 (ADVI_INFINGE.003) ship complete: `aws lambda list-functions | grep inf-api-positions` MATCH; layer ARN already in use.</run>
      <expect>TO-3 Lambda live; module template stable</expect>
      <if_mismatch>Wait — do not begin TO-4 until TO-3 RAVC5 close.</if_mismatch>
    </step>
    <step>
      <run>git tag -l "inf-pipeline-v*" | sort -V | tail -5</run>
      <expect>Latest tag includes TO-3 ship; pick next semver patch</expect>
      <if_mismatch>Per CLAUDE.md tag versioning rule</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implementation — clone TO-3 module + prefix substitute">
    <step>
      <run>Clone `infra/aws/lambda/inf-pipeline/inf-api-positions/` → `infra/aws/lambda/inf-pipeline/inf-api-performance/`. Edit lambda_function.py to invoke pull_inflection_performance.py + convert_orion_api_to_silver.py (--dim performance). Reference `pandas-pyarrow-requests-layer:1`.</run>
      <expect>Lambda handler invokes PERFORMANCE pull + silver convert; sys.path co-location; LOCAL_PULLS_DIR /tmp/pulls patch; JWT fail-fast; NO lambda:InvokeFunction. Zip ~50-100KB.</expect>
      <if_mismatch>Pattern divergence: surface to me + CTO before terraform apply.</if_mismatch>
    </step>
    <step>
      <run>Clone `infra/aws/terraform/inf-pipeline/inf-api-positions.tf` → `infra/aws/terraform/inf-pipeline/inf-api-performance.tf`. Substitute prefix; IAM scope (bronze/orion-api-v2/* + silver/api_dims/performance/* PutObject + secretsmanager + s3:GetObject JWT); EventBridge cron `cron(55 12 * * ? *)` (12:55 UTC).</run>
      <expect>9 resources to add; 0 destroys; clean plan</expect>
      <if_mismatch>If TO-3 module pattern needs deviation: surface before terraform apply.</if_mismatch>
    </step>
    <step>
      <run>Update lambda-source-map.json with inf-api-performance entry</run>
      <expect>New entry; CI drift detection picks it up</expect>
      <if_mismatch>Per CLAUDE.md rule 4</if_mismatch>
    </step>
    <step>
      <run>SILVER_BUILDERS extension on inf-silver-chain — add `performance` if absent (verify; likely present per orchestrator path-1)</run>
      <expect>If already present: no edit. If absent: append with crossref `# AC6: ADVI_INFINGE.004 TO-4 — performance silver-chain extension`</expect>
      <if_mismatch>Per TO-3 Phase 2 step 4</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="before terraform apply">
    <step>
      <run>terraform plan + comp-iam gaps + .tools/safe-commit.sh</run>
      <expect>Per TO-3 Phase 3 pattern; clean plan + 0 IAM gaps + safe-commit PASS</expect>
      <if_mismatch>Per TO-3 Phase 3 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="terraform apply + tag">
    <step>
      <run>terraform apply + 0-diff verify + tag bump + Lambda invoke empirical test (manual fire OR wait for natural cron at 12:55 UTC tomorrow)</run>
      <expect>Per TO-3 Phase 4 pattern; bronze/orion-api-v2/{date}/performance.json + silver/api_dims/performance/{date}/data.parquet written</expect>
      <if_mismatch>Per TO-3 Phase 4 if_mismatch</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on TO-3 ship.** Phase 1 Step 1 verifies POSITIONS Lambda live. Don't author TO-4 module before TO-3 RAVC5; pattern instability would force rework.</coord>
    <coord>**Cron stagger ordering:** REPS @ 12:30 → ASSETS_V2 @ 12:45 → POSITIONS @ 12:50 → PERFORMANCE @ 12:55 → TXN @ 13:00 (TO-5 conditional). PERFORMANCE reads fresh hh_rep_mapping from REPS.</coord>
    <coord>**TO-4 ship completes Phase 1b non-conditional family.** TO-5a (TXN rate-empirical) follows; TO-5b (TXN migration) conditional on TO-5a results.</coord>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_required>
      <reason>TO-4 migrates PERFORMANCE pull from inf-bronze-runner orchestrator to Lambda-native daily cron. Going-forward: D+1 fresh ingestion at 12:55 UTC daily.</reason>
      <s3_prefix_globs>
        <glob>s3://opal-data-inf/bronze/orion-api-v2/{date}/performance.json (D+1 onwards)</glob>
        <glob>s3://opal-data-inf/silver/api_dims/performance/{date}/data.parquet (D+1 onwards)</glob>
      </s3_prefix_globs>
      <verification>aws s3 ls each prefix at D+1; LastModified > tag-bump timestamp</verification>
      <downstream_consumer_freshness_gate>Gold INF_C_* + INF_D_* read fresh performance at gold-runner natural cron.</downstream_consumer_freshness_gate>
    </reprocess_required>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">Per TO-3 Phase 1 mandate; substitute `inf-api-performance` for `inf-api-positions`</phase>
    <phase id="2" when="before commit">Per TO-3 Phase 2 mandate</phase>
    <phase id="3" when="after deploy">Per TO-3 Phase 3 mandate; 24h empirical at 12:55 UTC tomorrow</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Fresh `bronze/orion-api-v2/{D+1}/performance.json` + `silver/api_dims/performance/{D+1}/data.parquet` by 13:00 UTC daily.</criterion>
    <criterion id="AC2">CW Metric `Opal/InflectionIngestion/PerformancePulled` increments daily.</criterion>
    <criterion id="AC3">CW Alarm fires on 2 consecutive failures.</criterion>
    <criterion id="AC4">comp-iam gaps clean post terraform apply.</criterion>
    <criterion id="AC5">Tag bumped + pushed.</criterion>
    <criterion id="AC6">RAVC5 close package: commit hash + apply 0-diff + tag bump + Lambda invoke empirical evidence + comp-iam gaps clean.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>2026-05-05T~21:38Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. TO-3 SHIPPED inf-pipeline-v1.7.20 + commit 6eaea1600 (positions_mv 24,205 rows; rate_limiter key fixed). TO-4 pure clone+prefix substitute from inf-api-positions. Reference `pandas-pyarrow-requests-layer:1`. EventBridge cron 12:55 UTC. **Pre-flight check:** verify performance dim-name in `convert_orion_api_to_silver.py` DIM_BUILDERS (likely `performance`, but confirm — TO-3 surfaced positions_mv vs spec'd positions_daily) + rate_limiter key suffix matches runtime log observation BEFORE TF apply. Sprint target ~30-60min. RAVC5 expectation: Lambda live + StatusCode=200 + bronze/orion-api-v2/{date}/performance.json + silver/api_dims/{actual_dim_name}/{date}/data.parquet + comp-iam gaps clean + tag bump. TO-5a (TXN rate-empirical) flips pending on TO-4 RAVC5.</message>
  </go_signal>
</task_order>
