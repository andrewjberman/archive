<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFINGE.003</id>
    <project>ADVI_INFINGE</project>
    <title>POSITIONS_DAILY migration to Lambda-native bronze pull (Phase 1b TO-3; reuses TO-2 layer + module template)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- Flipped staged→pending 2026-05-05T~21:25Z post TO-2 RAVC5 close. COMPLETE: commits f7b70f844 (inf-api-positions Lambda) + 6eaea1600 (IAM rate_limiter key fix — positions_mv not positions) + b81294f8b (terraform-deploy inf-pipeline-v1.7.20); TO-3 RAVC5 confirmed per AE 0.6.1 sprint closeout (broker: TO-5a RAVC3 sent means TO-1/2/3 all closed). -->
    <priority>high</priority>
    <estimated_effort>~30-60min AE post TO-2 ship; pure clone+prefix substitute (no Phase 0; layer already published)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFINGE.md v0.2 (commit 050bd3695); §6 Phase 1b TO-3</ref>
    <ref type="template_reference">TO-2 (ADVI_INFINGE.002) — Phase 0 layer + Phase 1 Lambda module pattern. TO-3 reuses verbatim with prefix substitution `reps` → `positions`. NO Phase 0 (layer already published by TO-2).</ref>
    <ref type="phase_0_evidence">AE 0.6.1 Phase 0 RAVC3 — POSITIONS Lambda-fits: YES (~60s wall, &lt;256MB memory, ~50-100 API calls). Lambda config 3072MB/900s sufficient (per TO-1 empirical).</ref>
  </references>

  <context>
    POSITIONS pull script (`pull_inflection_positions_daily.py`) is mid-scope Phase 1b migration. ~50-100 API calls; ~60s wall; <256MB memory. Lambda-fits.

    Bronze output paths:
    - `bronze/orion-api-v2/{date}/positions_daily.json`

    Silver convert outputs:
    - `silver/api_dims/positions_daily/{date}/data.parquet`

    **Critical:** POSITIONS reads fresh `household_rep_mapping.json` from REPS (TO-2) for advisor attribution. EventBridge cron `cron(50 12 * * ? *)` = 12:50 UTC, fires 5min after TO-1 ASSETS_V2 (12:45 UTC) and 20min after TO-2 REPS (12:30 UTC).

    Naming per CTO ratify 20260505T~19:55Z:
    - Lambda function: `inf-api-positions`
    - EventBridge rule: `inf-api-positions-rule`
    - IAM execution role: `inf-api-positions-role`
  </context>

  <phase id="1" when="before writing — gates on TO-2 ship">
    <step>
      <run>Verify TO-2 (ADVI_INFINGE.002) ship complete: `aws lambda list-functions | grep inf-api-reps` MATCH; `pandas-pyarrow-requests-layer:1` published + ARN available.</run>
      <expect>TO-2 Lambda live; layer ARN published; module template stable</expect>
      <if_mismatch>Wait — do not begin TO-3 until TO-2 RAVC5 close.</if_mismatch>
    </step>
    <step>
      <run>git tag -l "inf-pipeline-v*" | sort -V | tail -5</run>
      <expect>Latest tag includes TO-2 ship; pick next semver patch</expect>
      <if_mismatch>Per CLAUDE.md tag versioning rule</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implementation — clone TO-2 module + prefix substitute">
    <step>
      <run>Clone `infra/aws/lambda/inf-pipeline/inf-api-reps/` → `infra/aws/lambda/inf-pipeline/inf-api-positions/`. Edit lambda_function.py to invoke pull_inflection_positions_daily.py + convert_orion_api_to_silver.py (--dim positions_daily). Reference `pandas-pyarrow-requests-layer:1` (no ad-hoc vendoring).</run>
      <expect>Lambda handler invokes POSITIONS pull + silver convert; sys.path co-location; LOCAL_PULLS_DIR /tmp/pulls patch; JWT fail-fast; NO lambda:InvokeFunction. Zip ~50-100KB.</expect>
      <if_mismatch>Pattern divergence: surface to me + CTO before terraform apply.</if_mismatch>
    </step>
    <step>
      <run>Clone `infra/aws/terraform/inf-pipeline/inf-api-reps.tf` → `infra/aws/terraform/inf-pipeline/inf-api-positions.tf`. Substitute prefix; IAM scope (bronze/orion-api-v2/* + silver/api_dims/positions_daily/* PutObject + secretsmanager + s3:GetObject JWT); EventBridge cron `cron(50 12 * * ? *)` (12:50 UTC).</run>
      <expect>9 resources to add; 0 destroys; clean plan</expect>
      <if_mismatch>If TO-2 module pattern needs deviation: surface before terraform apply.</if_mismatch>
    </step>
    <step>
      <run>Update lambda-source-map.json with inf-api-positions entry</run>
      <expect>New entry; CI drift detection picks it up</expect>
      <if_mismatch>Per CLAUDE.md rule 4</if_mismatch>
    </step>
    <step>
      <run>SILVER_BUILDERS extension on inf-silver-chain — add `positions_daily` if absent (verify; likely present per orchestrator path-1)</run>
      <expect>If already present: no edit. If absent: append with crossref `# AC6: ADVI_INFINGE.003 TO-3 — positions_daily silver-chain extension`</expect>
      <if_mismatch>Per TO-2 Phase 2 step 4</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="before terraform apply">
    <step>
      <run>terraform plan + comp-iam gaps + .tools/safe-commit.sh</run>
      <expect>Per TO-2 Phase 3 pattern; clean plan + 0 IAM gaps + safe-commit PASS</expect>
      <if_mismatch>Per TO-2 Phase 3 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="terraform apply + tag">
    <step>
      <run>terraform apply + 0-diff verify + tag bump + Lambda invoke empirical test (manual fire OR wait for natural cron at 12:50 UTC tomorrow)</run>
      <expect>Per TO-2 Phase 4 pattern; bronze/orion-api-v2/{date}/positions_daily.json + silver/api_dims/positions_daily/{date}/data.parquet written</expect>
      <if_mismatch>Per TO-2 Phase 4 if_mismatch</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on TO-2 ship.** Phase 1 Step 1 verifies layer ARN + REPS Lambda live. Don't author TO-3 module before TO-2 RAVC5; pattern instability would force rework.</coord>
    <coord>**Cron stagger ordering:** REPS @ 12:30 → ASSETS_V2 @ 12:45 → POSITIONS @ 12:50 → PERFORMANCE @ 12:55 → TXN @ 13:00 (TO-5 conditional). POSITIONS reads fresh hh_rep_mapping from REPS.</coord>
    <coord>**TO-4 reuses same template.** Once TO-3 ships, TO-4 (PERFORMANCE) ships in same hour with prefix substitution.</coord>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_required>
      <reason>TO-3 migrates POSITIONS pull from inf-bronze-runner orchestrator to Lambda-native daily cron. Going-forward: D+1 fresh ingestion at 12:50 UTC daily.</reason>
      <s3_prefix_globs>
        <glob>s3://opal-data-inf/bronze/orion-api-v2/{date}/positions_daily.json (D+1 onwards)</glob>
        <glob>s3://opal-data-inf/silver/api_dims/positions_daily/{date}/data.parquet (D+1 onwards)</glob>
      </s3_prefix_globs>
      <verification>aws s3 ls each prefix at D+1; LastModified > tag-bump timestamp</verification>
      <downstream_consumer_freshness_gate>Gold INF_C_* + INF_D_* read fresh positions_daily at gold-runner natural cron.</downstream_consumer_freshness_gate>
    </reprocess_required>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">Per TO-2 Phase 1 mandate; substitute `inf-api-positions` for `inf-api-reps`</phase>
    <phase id="2" when="before commit">Per TO-2 Phase 2 mandate</phase>
    <phase id="3" when="after deploy">Per TO-2 Phase 3 mandate; 24h empirical at 12:50 UTC tomorrow</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Fresh `bronze/orion-api-v2/{D+1}/positions_daily.json` + `silver/api_dims/positions_daily/{D+1}/data.parquet` by 12:55 UTC daily.</criterion>
    <criterion id="AC2">CW Metric `Opal/InflectionIngestion/PositionsPulled` increments daily.</criterion>
    <criterion id="AC3">CW Alarm fires on 2 consecutive failures.</criterion>
    <criterion id="AC4">comp-iam gaps clean post terraform apply.</criterion>
    <criterion id="AC5">Tag bumped + pushed.</criterion>
    <criterion id="AC6">RAVC5 close package: commit hash + apply 0-diff + tag bump + Lambda invoke empirical evidence + comp-iam gaps clean.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>2026-05-05T~21:25Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. TO-2 SHIPPED 2026-05-05 inf-pipeline-v1.7.19 + shared-infra-v1.9.0 (layer:1 ARN confirmed; StatusCode=200; 4 S3 artifacts; comp-iam gaps clean). Pure clone+prefix substitute from inf-api-reps template. Reference `pandas-pyarrow-requests-layer:1`. EventBridge cron 12:50 UTC. Sprint target ~30-60min. RAVC5 expectation: Lambda live + StatusCode=200 + bronze/orion-api-v2/{date}/positions_daily.json + silver/api_dims/positions_daily/{date}/data.parquet + comp-iam gaps clean + tag bump (next semver patch from inf-pipeline-v1.7.19). TO-4 (PERFORMANCE) flips pending on TO-3 RAVC5.</message>
  </go_signal>
</task_order>
