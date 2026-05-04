<task_order>
  <metadata>
    <id>MDLP_RVVALT.003</id>
    <project>MDLP_RVVALT</project>
    <title>yang-model-portfolio-benchmarks Lambda — emit model_portfolio_timeseries.json</title>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>pending</status>
    <priority>P2 — gates TO-4 (DE wire-up); GATED by TO-1 (RFR spec) — pre-engagement OK</priority>
    <estimated_effort>1.0d (Lambda extension + LAMBDA_DEPLOYMENT_PROTOCOL ship + tag)</estimated_effort>
  </metadata>

  <context>
    PRD: `docs/architecture/MDLP_RVVALT.md` (CTO commit `7e520d4bf`). PRD §2 Backend block.

    Extend `yang-model-portfolio-benchmarks` Lambda to emit a daily time-series JSON: `json/benchmarks/model_portfolio_timeseries.json`. Each row: `{date, model_code, model_return, benchmark_return, rfr_10y}`. Source: data.pkl `return_daily` (already loaded by Lambda) + 10Y Treasury yield extraction per TO-1 spec.

    Daily time-series only — frontend computes rolling Sharpe + drawdown so window-aperture sub-toggles are pure-frontend (PRD §2 + §3). Same Lambda invocation, additional output — no new Lambda, no IAM change (existing `s3:PutObject` on `opal-data-portal-v2/json/benchmarks/*` covers).
  </context>

  <objective>
    Lambda emits new artifact `s3://opal-data-portal-v2/json/benchmarks/model_portfolio_timeseries.json` on next invocation. Schema matches DE TO-2 types `ModelTimeseriesResponse` + `ModelTimeseriesPoint`. Deployed via standard LAMBDA_DEPLOYMENT_PROTOCOL (terraform plan/apply + tag bump + lambda-source-map.json update). Verify ETag + payload schema post-deploy.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>Lambda extension</title>
      <detail>
        Edit `infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py`:
        - Add 10Y Treasury yield extraction from data.pkl `return_daily` per TO-1 spec (`docs/architecture/MDLP_RVVALT_RFR_SPEC.md` — read after TO-1 RAVC4)
        - Build daily time-series rows: `{date, model_code, model_return, benchmark_return, rfr_10y}` for inception → latest, all 5 models
        - Emit `OUTPUT_KEY_TIMESERIES = 'json/benchmarks/model_portfolio_timeseries.json'`
        - Existing `model_portfolio_benchmarks.json` output untouched (PRD §8: no backwards-incompatible API change)
      </detail>
    </ac>
    <ac id="2">
      <title>Schema match with DE TO-2 types</title>
      <detail>
        Output JSON shape matches `ModelTimeseriesResponse` / `ModelTimeseriesPoint` types DE 0.4.0 authored in TO-2 portal-proxy.ts. If you ship before DE TO-2 lands, MCP DE for type sync; otherwise diff against their committed types.

        Per PRD §6 cross-domain: if TO-1 RFR spec deviates from PRD assumed unit, MCP DE before regenerating types.
      </detail>
    </ac>
    <ac id="3">
      <title>Source map update</title>
      <detail>
        Update `infra/aws/lambda/ci/lambda-source-map.json` for the Lambda — confirm new output is captured for CI drift detection (CLAUDE.md Critical Deployment Rule 4).
      </detail>
    </ac>
    <ac id="4">
      <title>Memory + timeout assessment</title>
      <detail>
        Per PRD §7.2 risk: data.pkl is large (~16+ MB); existing Lambda already loads it. Measure pre-vs-post Lambda duration on a test invocation. If >10s degradation, bump memory in terraform; document. If clean, no Terraform changes needed.
      </detail>
    </ac>
    <ac id="5">
      <title>Terraform deploy + tag</title>
      <detail>
        Per LAMBDA_DEPLOYMENT_PROTOCOL.md:
        - Build + upload zip to S3 via build-and-upload.sh
        - terraform plan → 0 drift outside Lambda diff
        - terraform apply → 0-diff on subsequent plan
        - Annotated git tag `yang-vX.Y.Z` (run `git tag -l "yang-v*" | sort -V | tail -5` first per pipeline-tag-versioning rule; current latest in MEMORY.md is `yang-v2.3.6` but verify)
        - `git push --follow-tags`
        - record-terraform-deploy.sh updates CHANGELOG.json
      </detail>
    </ac>
    <ac id="6">
      <title>Post-deploy verification</title>
      <detail>
        - Invoke Lambda once (manual `aws lambda invoke` or wait for next scheduled fire)
        - `aws s3 ls s3://opal-data-portal-v2/json/benchmarks/model_portfolio_timeseries.json` returns object with mtime > deploy time
        - Capture ETag in session log
        - `aws s3 cp ... -` and `jq '.[] | length, [.[] | .model_code] | unique'` to spot-check schema (date present, 5 model codes, rfr_10y populated)
        - Lambda CloudWatch log shows successful emit (PRD AC7)
      </detail>
    </ac>
    <ac id="7">
      <title>Session log + RAVC4</title>
      <detail>
        Session log under `org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-05-04/` (or whenever ship lands). Compiler Tools section. RAVC4 to me + DE 0.4.0 with: Lambda commit hash + tag + 0-diff plan + S3 ETag + payload schema sample.
      </detail>
    </ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before_edit">
      <step>
        <run>comp-iam service yang-model-portfolio-benchmarks</run>
        <expect>Lambda role + existing s3:PutObject on `opal-data-portal-v2/json/benchmarks/*` covers new artifact (PRD §5 — no IAM change needed)</expect>
        <if_mismatch>If new prefix or new permission needed, flag to COO before terraform changes</if_mismatch>
      </step>
      <step>
        <run>cat infra/aws/lambda/ci/lambda-source-map.json | jq '.["yang-model-portfolio-benchmarks"]'</run>
        <expect>Existing source map entry exists; locate for update</expect>
        <if_mismatch>Add/correct entry per CLAUDE.md Rule 4</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before_commit">
      <step>
        <run>terraform -chdir=infra/aws/terraform/yang-pipeline plan</run>
        <expect>Single Lambda code-update diff (S3 zip ETag); no other drift</expect>
        <if_mismatch>Investigate drift before applying</if_mismatch>
      </step>
      <step>
        <run>git tag -l "yang-v*" | sort -V | tail -5</run>
        <expect>Verify latest yang tag before tagging next patch (per pipeline-tag-versioning memory rule)</expect>
        <if_mismatch>Pick correct next-patch increment</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after_commit">
      <step>
        <run>terraform -chdir=infra/aws/terraform/yang-pipeline plan</run>
        <expect>0-diff (No changes)</expect>
        <if_mismatch>Investigate apply failure</if_mismatch>
      </step>
      <step>
        <run>comp-iam gaps</run>
        <expect>No new permission gaps for yang-model-portfolio-benchmarks</expect>
        <if_mismatch>Fix iam.tf if needed</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <resource>
      <path>portal/src/api/portal-proxy.ts (DE TO-2 owns types)</path>
      <owners>0.4.0_DE_ClientPlatform (TO-2 author); 0.5.0_AE_OpalETL (this TO matches JSON schema)</owners>
      <coordination>Per PRD §6: if TO-1 RFR spec deviates from PRD assumed unit, MCP DE before regenerating types. If your output schema diverges from DE's authored types, MCP DE for sync before ship.</coordination>
    </resource>
    <resource>
      <path>s3://opal-data-portal-v2/json/benchmarks/</path>
      <owners>0.5.0_AE_OpalETL (yang-pipeline write); existing artifact `model_portfolio_benchmarks.json` co-resides</owners>
      <coordination>No conflict — new sibling key. Existing artifact untouched.</coordination>
    </resource>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Reasoning: Lambda extension emits new artifact alongside existing; no historical data semantic change; downstream FE wires up in TO-4 against fresh emit; no replay needed.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    <item>Lambda commit + lambda-source-map.json update + Terraform deploy</item>
    <item>Annotated git tag `yang-vX.Y.Z` (run pipeline-tag-versioning check before)</item>
    <item>git push --follow-tags + record-terraform-deploy.sh CHANGELOG.json update</item>
    <item>S3 ETag of new artifact + payload schema sample</item>
    <item>Session log with Compiler Tools section + Lambda duration measurement (PRD §7.2)</item>
    <item>RAVC4 MCP to COO + DE 0.4.0</item>
  </deliverables>
</task_order>
