<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFINGE.002</id>
    <project>ADVI_INFINGE</project>
    <title>REPS migration to Lambda-native bronze pull (Phase 1b TO-2; reuses TO-1 module template)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- Flipped staged→pending 2026-05-05T~21:00Z post TO-1 RAVC5 close (AE 0.6.1 inf-pipeline-v1.7.18 LIVE; StatusCode=200 + S3 empirical confirmed). CTO ratified Phase 0 layer-publish framing. COMPLETE: commit 0dd4f6c07 (REPS Lambda + pandas-pyarrow-requests-layer); inf-pipeline-v1.7.19 LIVE per TO-3 staging note RAVC5 confirmed. -->
    <priority>high</priority>
    <estimated_effort>Phase 0 layer publish ~30min-1h + Phase 1 REPS Lambda ~30-60min; total ~1.5-2h sprint compressed</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFINGE.md v0.2 (commit 050bd3695); §6 Phase 1b TO-2 (line 243-249)</ref>
    <ref type="template_reference">TO-1 (ADVI_INFINGE.001) — Lambda module + Terraform pattern. TO-2 reuses verbatim with prefix substitution `assets-v2` → `reps`. Once TO-1 ships clean, TO-2 is mostly ~30 min of TF + Lambda authoring + per-prefix IAM scope.</ref>
    <ref type="phase_0_evidence">AE 0.6.1 Phase 0 RAVC3 — REPS Lambda-fits: YES (~30s wall, &lt;128MB memory, ~9 API calls). Smallest scope of Phase 1b family; ideal for template-validation second-shipper.</ref>
  </references>

  <context>
    REPS pull script (`pull_inflection_representatives.py`) is the smallest-scope Phase 1b migration. ~9 API calls (1 /Representatives + 7 /Clients?rep=N + 1 spare); ~30s wall; <128MB memory. Trivially Lambda-fits.

    Bronze output paths (per AE 0.6.1 RAVC3):
    - `bronze/orion-api-v2/{date}/representatives.json`
    - `bronze/orion-api-v2/{date}/household_rep_mapping.json`

    Silver convert outputs (paired in single Lambda execution):
    - `silver/api_dims/representatives/{date}/data.parquet`
    - `silver/api_dims/household_rep_mapping/{date}/data.parquet`

    **Critical:** REPS produces `household_rep_mapping.json` which is dependency input for downstream pulls (assets_v2, positions_daily, performance, transactions all use rep mapping for advisor attribution). EventBridge cron timing: REPS fires FIRST in the daily 12:00-13:00 UTC window so downstream Lambdas can read fresh hh_rep_mapping. Suggested: REPS @ 12:30 UTC; ASSETS_V2 @ 12:45 UTC (per TO-1 default); POSITIONS @ 12:50 UTC; PERFORMANCE @ 12:55 UTC.

    Naming per CTO ratify 20260505T~19:55Z:
    - Lambda function: `inf-api-reps`
    - EventBridge rule: `inf-api-reps-rule`
    - IAM execution role: `inf-api-reps-role`
  </context>

  <phase id="0" when="publish shared layer — pandas-pyarrow-requests-layer:1 — RATIFIED by CTO 2026-05-05T~20:55Z">
    <step>
      <run>Author `infra/aws/lambda/layers/pandas-pyarrow-requests-layer/requirements.txt` listing pandas + pyarrow + requests + urllib3 + certifi + charset_normalizer + idna at versions matching TO-1 vendor bundle.</run>
      <expect>requirements.txt mirrors TO-1's vendored set; pure-Python deps; layer build deterministic across TO-2..5.</expect>
      <if_mismatch>If versions diverge from TO-1 empirically validated set: pin to TO-1 versions; layer must be drop-in compatible with TO-1 Lambda config (3072MB/900s).</if_mismatch>
    </step>
    <step>
      <run>Build + upload layer zip to `opal-313476888478-lambda-layers/pandas-pyarrow-requests-layer.zip` per existing layer build pattern; publish via Terraform under shared-infra (`infra/aws/terraform/shared-infra/`).</run>
      <expect>Layer ARN published as `pandas-pyarrow-requests-layer:1`; shared-infra tag bumped (next semver patch from current shared-infra-v1.6.0).</expect>
      <if_mismatch>Per layer publishing protocol; shared-infra owns layer publish per memory.</if_mismatch>
    </step>
    <step>
      <run>Optional: refactor TO-1 (`inf-api-assets-v2`) to consume `pandas-pyarrow-requests-layer:1` and drop ad-hoc vendored requests. NOT REQUIRED for TO-2 ship — TO-1 stays as-is until follow-up cleanup TO. Document refactor candidate in commit message.</run>
      <expect>TO-1 refactor deferred; TO-2 onward consumes layer cleanly.</expect>
      <if_mismatch>If you elect to refactor TO-1 inline: ensure StatusCode=200 + S3 artifact byte-count match post-refactor; tag bump.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="before writing — TO-1 SHIPPED 2026-05-05 inf-pipeline-v1.7.18; verify">
    <step>
      <run>Verify TO-1 (ADVI_INFINGE.001) ship complete: `comp-pipescript deployed inf-api-assets-v2` MATCH; `aws lambda list-functions | grep inf-api-assets-v2`</run>
      <expect>TO-1 Lambda live; module template established; TO-2 reuses pattern</expect>
      <if_mismatch>Wait — do not begin TO-2 until TO-1 RAVC5 close. Template stability matters for fast TO-2 ship.</if_mismatch>
    </step>
    <step>
      <run>git tag -l "inf-pipeline-v*" | sort -V | tail -5</run>
      <expect>Latest tag includes TO-1 ship; pick next semver patch</expect>
      <if_mismatch>Per CLAUDE.md tag versioning rule</if_mismatch>
    </step>
    <step>
      <run>comp-iam service inf-api-reps + comp-pipescript io pull_inflection_representatives.py</run>
      <expect>Per TO-1 Phase 1 pattern; IAM scope = bronze/orion-api-v2/* PutObject + silver/api_dims/representatives/* + silver/api_dims/household_rep_mapping/* PutObject + secretsmanager + s3:GetObject on JWT path</expect>
      <if_mismatch>Cross-check vs PRD §6.2</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implementation — clone TO-1 module template + REPS-specific edits">
    <step>
      <run>Clone `infra/aws/lambda/inf-pipeline/inf-api-assets-v2/` → `infra/aws/lambda/inf-pipeline/inf-api-reps/`. Edit lambda_function.py to invoke pull_inflection_representatives.py + convert_orion_api_to_silver.py (--dim representatives + --dim household_rep_mapping). DROP ad-hoc requests vendoring — pull from `pandas-pyarrow-requests-layer:1` (Phase 0 published).</run>
      <expect>Lambda handler invokes REPS pull + 2 silver convert calls in sequence; Lambda packaging gotchas inherited from TO-1 (sys.path co-location for rate_limiter + jwt_freshness; LOCAL_PULLS_DIR /tmp/pulls patch); JWT read fail-fast pattern; NO lambda:InvokeFunction. Zip size should drop from TO-1's 936KB to ~50-100KB (pure handler code).</expect>
      <if_mismatch>Pattern divergence from TO-1: document in commit message; CTO consult if material. If layer-only deps insufficient: surface to me + CTO before vendoring.</if_mismatch>
    </step>
    <step>
      <run>Clone `infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf` → `infra/aws/terraform/inf-pipeline/inf-api-reps.tf`. Substitute prefix; update IAM scope (bronze/orion-api-v2/* + silver/api_dims/representatives/* + silver/api_dims/household_rep_mapping/* PutObject); set EventBridge cron `cron(30 12 * * ? *)` (12:30 UTC, 5min before TO-1 cron 12:45 UTC; provides fresh hh_rep_mapping for downstream).</run>
      <expect>9 resources to add; 0 destroys; clean plan</expect>
      <if_mismatch>If TO-1 module pattern needs deviation: surface to me before terraform apply.</if_mismatch>
    </step>
    <step>
      <run>Update lambda-source-map.json with inf-api-reps entry</run>
      <expect>New entry; CI drift detection picks it up</expect>
      <if_mismatch>Per CLAUDE.md rule 4</if_mismatch>
    </step>
    <step>
      <run>SILVER_BUILDERS extension on inf-silver-chain — add `representatives` + `household_rep_mapping` (already present per AE 0.7 preview; verify; if absent, append)</run>
      <expect>If already present (likely per orchestrator path-1 separate from REST-pull path-2): no edit needed; document.</expect>
      <if_mismatch>If absent: append with comment crossref `# AC6: ADVI_INFINGE.002 TO-2 — representatives + household_rep_mapping silver-chain extension`</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="before terraform apply">
    <step>
      <run>terraform plan + comp-iam gaps + .tools/safe-commit.sh</run>
      <expect>Per TO-1 Phase 3 pattern; clean plan + 0 IAM gaps + safe-commit PASS</expect>
      <if_mismatch>Per TO-1 Phase 3 if_mismatch</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="terraform apply + tag">
    <step>
      <run>terraform apply + 0-diff verify + tag bump + Lambda invoke empirical test (manual fire OR wait for natural cron at 12:30 UTC tomorrow)</run>
      <expect>Per TO-1 Phase 4 pattern; bronze/orion-api-v2/{date}/{representatives.json,household_rep_mapping.json} written + silver/api_dims/{representatives,household_rep_mapping}/{date}/data.parquet written</expect>
      <if_mismatch>Per TO-1 Phase 4 if_mismatch</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on TO-1 ship.** Phase 1 Step 1 verifies TO-1 module template established. Don't author TO-2 module before TO-1 RAVC5; pattern instability would force rework.</coord>
    <coord>**Cron stagger ordering:** REPS @ 12:30 UTC fires FIRST (downstream of Tier 1 12:13 UTC JWT refresh; produces hh_rep_mapping for downstream). ASSETS_V2 @ 12:45 UTC reads fresh hh_rep_mapping. POSITIONS @ 12:50, PERFORMANCE @ 12:55. TXN @ 13:00 (TO-5 conditional).</coord>
    <coord>**TO-3/TO-4 reuse same template.** Once TO-2 ships, TO-3 (POSITIONS) + TO-4 (PERFORMANCE) ship in same hour with prefix substitution.</coord>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_required>
      <reason>TO-2 migrates REPS pull from inf-bronze-runner orchestrator (current path-1) OR existing path-2 chain dispatch (if previously running via gold-runner SSM) to Lambda-native daily cron. Going-forward: D+1 fresh ingestion at 12:30 UTC daily. Historical hh_rep_mapping data continues to exist; ongoing daily ingestion handles it.</reason>
      <s3_prefix_globs>
        <glob>s3://opal-data-inf/bronze/orion-api-v2/{date}/representatives.json (D+1 onwards)</glob>
        <glob>s3://opal-data-inf/bronze/orion-api-v2/{date}/household_rep_mapping.json (D+1 onwards)</glob>
        <glob>s3://opal-data-inf/silver/api_dims/representatives/{date}/data.parquet (D+1 onwards)</glob>
        <glob>s3://opal-data-inf/silver/api_dims/household_rep_mapping/{date}/data.parquet (D+1 onwards)</glob>
      </s3_prefix_globs>
      <verification>aws s3 ls each prefix at D+1; LastModified > tag-bump timestamp</verification>
      <downstream_consumer_freshness_gate>ASSETS_V2 + POSITIONS + PERFORMANCE Lambdas read fresh hh_rep_mapping at 12:45/12:50/12:55 UTC (post REPS @ 12:30). Cron stagger ensures freshness ordering.</downstream_consumer_freshness_gate>
    </reprocess_required>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">Per TO-1 Phase 1 mandate; substitute `inf-api-reps` for `inf-api-assets-v2`</phase>
    <phase id="2" when="before commit">Per TO-1 Phase 2 mandate</phase>
    <phase id="3" when="after deploy">Per TO-1 Phase 3 mandate; 24h empirical at 12:30 UTC tomorrow</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Fresh `bronze/orion-api-v2/{D+1}/{representatives.json,household_rep_mapping.json}` + `silver/api_dims/representatives/{D+1}/data.parquet` + `silver/api_dims/household_rep_mapping/{D+1}/data.parquet` by 12:35 UTC daily.</criterion>
    <criterion id="AC2">CW Metric `Opal/InflectionIngestion/RepsPulled` increments daily.</criterion>
    <criterion id="AC3">CW Alarm fires on 2 consecutive failures.</criterion>
    <criterion id="AC4">comp-iam gaps clean post terraform apply.</criterion>
    <criterion id="AC5">Tag bumped + pushed.</criterion>
    <criterion id="AC6">RAVC5 close package: commit hash + apply 0-diff + tag bump + Lambda invoke empirical evidence + comp-iam gaps clean.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>2026-05-05T~21:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. TO-1 SHIPPED 2026-05-05 inf-pipeline-v1.7.18 (StatusCode=200 + bronze 943,982B + silver 928,737B empirical). Phase 0 layer-publish framing ratified by CTO 2026-05-05T~20:55Z (per AE 0.6.1 packaging note). Execute Phase 0 (publish `pandas-pyarrow-requests-layer:1` via shared-infra) then Phase 1 (REPS Lambda referencing the new layer). EventBridge cron 12:30 UTC for fresh hh_rep_mapping ahead of downstream TO-1 cron 12:45 UTC. RAVC5 expectation: layer ARN published + tag bump + REPS Lambda live + StatusCode=200 + bronze/orion-api-v2/{representatives.json, household_rep_mapping.json} + silver/api_dims/{representatives,household_rep_mapping}/data.parquet + comp-iam gaps clean. TO-3/TO-4/TO-5a inherit same layer; clean template post TO-2.</message>
  </go_signal>
</task_order>
