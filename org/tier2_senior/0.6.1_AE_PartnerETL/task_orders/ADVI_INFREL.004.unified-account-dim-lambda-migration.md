<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.004</id>
    <project>ADVI_INFREL</project>
    <title>unified_account_dim Lambda migration (Phase 2 foundational; ship first)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>staged</status><!-- Authored sprint mode 2026-05-05T~21:15Z. Gates on TO-1 silver-chain fix (per dim Lambda bronze writes still need silver-chain to convert) AND INFINGE TO-2 layer publish (pandas-pyarrow-requests-layer:1). Phase 2 ship-first per PRD §6 (most foundational; many downstream readers). -->
    <priority>high</priority>
    <estimated_effort>~0.5d AE; pure clone+prefix substitute from INFINGE Phase 1b template</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1; §4.4 + §6 TO-4</ref>
    <ref type="template_reference">INFINGE TO-1 (assets-v2 Lambda LIVE 270d37c98) + INFINGE TO-2 (REPS Lambda + Phase 0 layer publish, in flight) — Phase 1b Lambda module template</ref>
    <ref type="layer_dep">pandas-pyarrow-requests-layer:1 (published under INFINGE TO-2 Phase 0)</ref>
    <ref type="silver_dep">TO-1 silver-chain RCA + fix (gates Phase 2 silver propagation)</ref>
  </references>

  <context>
    `unified_account_dim` is a path-1 orchestrator-bound dim (currently runs on inf-bronze-runner orchestrator.py). Migration to per-script Lambda matches INFINGE Phase 1b template.

    Output paths:
    - Bronze: `bronze/orion-api-v2/{date}/unified_account_dim.json` (Lambda writes)
    - Silver: `silver/api_dims/unified_account_dim/{date}/data.parquet` (silver-chain Lambda converts post TO-1 fix)

    EventBridge cron: 13:05 UTC (5min after INFINGE TO-4 PERFORMANCE 12:55 UTC; staggered to avoid burst).

    Naming:
    - Lambda function: `inf-api-unified-account-dim`
    - EventBridge rule: `inf-api-unified-account-dim-rule`
    - IAM execution role: `inf-api-unified-account-dim-role`

    **Foundational** — many downstream gold-tier scripts read unified_account_dim. Migration must be silver-chain-functional before bronze writes are useful.
  </context>

  <phase id="1" when="before writing — gates on TO-1 + INFINGE TO-2">
    <step>
      <run>Verify TO-1 (silver-chain RCA + fix) RAVC5 close + 24h empirical: silver propagation working. Verify INFINGE TO-2 RAVC5 close: pandas-pyarrow-requests-layer:1 ARN published.</run>
      <expect>Both gates green; silver propagation reliable; layer ARN available.</expect>
      <if_mismatch>Wait. Do not author TO-4 module before both gates green; bronze writes would orphan without silver propagation.</if_mismatch>
    </step>
    <step>
      <run>git tag -l "inf-pipeline-v*" | sort -V | tail -5</run>
      <expect>Latest tag includes INFINGE Phase 1b ship; pick next semver patch</expect>
      <if_mismatch>Per CLAUDE.md tag versioning rule</if_mismatch>
    </step>
    <step>
      <run>comp-iam service inf-api-unified-account-dim + comp-pipescript io <unified_account_dim pull script>. Identify pull script in data/orion/scripts/ OR equivalent path.</run>
      <expect>Per INFINGE TO-1 Phase 1 pattern; IAM scope = bronze/orion-api-v2/* PutObject + silver/api_dims/unified_account_dim/* PutObject + secretsmanager + s3:GetObject JWT</expect>
      <if_mismatch>If pull script doesn't exist as standalone (currently embedded in orchestrator.py): factor out to standalone script as part of Phase 2.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implementation — clone INFINGE Phase 1b module + prefix substitute">
    <step>
      <run>Clone `infra/aws/lambda/inf-pipeline/inf-api-reps/` (post INFINGE TO-2 ship) → `infra/aws/lambda/inf-pipeline/inf-api-unified-account-dim/`. Edit lambda_function.py to invoke unified_account_dim pull + convert_orion_api_to_silver.py (--dim unified_account_dim). Reference `pandas-pyarrow-requests-layer:1`.</run>
      <expect>Lambda handler invokes unified_account_dim pull + silver convert; sys.path co-location; LOCAL_PULLS_DIR /tmp/pulls patch; JWT fail-fast; NO lambda:InvokeFunction. Zip ~50-100KB.</expect>
      <if_mismatch>Pattern divergence from INFINGE Phase 1b: surface to me + CTO before terraform apply</if_mismatch>
    </step>
    <step>
      <run>Clone `infra/aws/terraform/inf-pipeline/inf-api-reps.tf` → `infra/aws/terraform/inf-pipeline/inf-api-unified-account-dim.tf`. Substitute prefix; IAM scope; EventBridge cron `cron(5 13 * * ? *)` (13:05 UTC).</run>
      <expect>9 resources to add; 0 destroys; clean plan</expect>
      <if_mismatch>Per INFINGE Phase 1b pattern</if_mismatch>
    </step>
    <step>
      <run>Update lambda-source-map.json with inf-api-unified-account-dim entry per CLAUDE.md rule 4</run>
      <expect>New entry; CI drift detection picks it up</expect>
      <if_mismatch>Per CLAUDE.md rule 4</if_mismatch>
    </step>
    <step>
      <run>Remove unified_account_dim from inf-bronze-runner orchestrator.py chain config — destructive operation. PRE-CONFIRM via MCP citing PRD §3 MODIFIED clause + this TO before edit (per memory `feedback_destructive_op_pre_confirm.md`).</run>
      <expect>Pre-confirm sent; orchestrator.py edit removes only unified_account_dim line; no other dim affected.</expect>
      <if_mismatch>Pre-confirm denied or unclear: surface to me before edit. If concurrent agent has orchestrator.py open: serialize.</if_mismatch>
    </step>
    <step>
      <run>SILVER_BUILDERS extension on inf-silver-chain — add `unified_account_dim` if absent (verify; per TO-1 fix, may auto-include)</run>
      <expect>If already present (post TO-1 fix): no edit. If absent: append with crossref.</expect>
      <if_mismatch>Per TO-1 fix scope</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="before terraform apply">
    <step>
      <run>terraform plan + comp-iam gaps + safe-commit.sh</run>
      <expect>Clean plan + 0 IAM gaps + safe-commit PASS</expect>
      <if_mismatch>Per LAMBDA_DEPLOYMENT_PROTOCOL.md</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="terraform apply + tag + empirical">
    <step>
      <run>terraform apply + 0-diff verify + tag bump + Lambda invoke empirical (manual fire OR wait for natural cron 13:05 UTC tomorrow)</run>
      <expect>Bronze + silver paths populated; comp-iam gaps clean</expect>
      <if_mismatch>Per LAMBDA_DEPLOYMENT_PROTOCOL.md</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on TO-1 + INFINGE TO-2.** Both must close clean before TO-4 author/deploy.</coord>
    <coord>**Cron stagger:** REPS@12:30 → ASSETS_V2@12:45 → POSITIONS@12:50 → PERFORMANCE@12:55 → unified_account_dim@13:05 → transactions_v2@13:10 → billing@13:15 → tax@13:20 → TXN@13:00 (TO-5a conditional)</coord>
    <coord>**Foundational — TO-5..7 inherit pattern.** Once TO-4 ships clean, TO-5/6/7 are pure clone+prefix substitute.</coord>
    <coord>**Hardcoded mapping audit** — per PRD Risk Register, search the unified_account_dim pull script for ADVISOR_KEY_TO_REP_ID-style hardcoded dicts; route to canonical source if found (defense against AUDIT-003 sibling cascade pattern).</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">Per INFINGE Phase 1b mandate; substitute `inf-api-unified-account-dim` for `inf-api-reps`</phase>
    <phase id="2" when="before commit">Per INFINGE Phase 1b mandate</phase>
    <phase id="3" when="after deploy">Per INFINGE Phase 1b mandate; 24h empirical at 13:05 UTC tomorrow</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Fresh `bronze/orion-api-v2/{D+1}/unified_account_dim.json` + `silver/api_dims/unified_account_dim/{D+1}/data.parquet` by 13:10 UTC daily.</criterion>
    <criterion id="AC2">CW Metric `Opal/InflectionIngestion/UnifiedAccountDimPulled` increments daily.</criterion>
    <criterion id="AC3">CW Alarm fires on 2 consecutive failures.</criterion>
    <criterion id="AC4">orchestrator.py removed unified_account_dim entry; no downstream gold-tier breakage.</criterion>
    <criterion id="AC5">Silver propagates daily (gates on TO-1 fix).</criterion>
    <criterion id="AC6">comp-iam gaps clean post terraform apply.</criterion>
    <criterion id="AC7">Tag bumped + pushed.</criterion>
    <criterion id="AC8">RAVC5 close: commit hash + apply 0-diff + tag bump + Lambda invoke empirical + comp-iam gaps clean.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — gates on TO-1 + INFINGE TO-2 RAVC5</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged` until both gates green. Foundational; TO-5..7 inherit pattern.</message>
  </go_signal>
</task_order>
