<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-16-005-dt-artifact-rebuild</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-16</date>
    <status>pending</status>
    <thread_serial>ADVI_MVPLVL-005</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-005-addendum-a-mix-timeseries-alignment/</thread_ref>
    <revision>REVISED 2026-03-16 — partners-api-v1.0.0 (ddce9fef) and v1.0.1 hotfix
    (da5c527f) already deployed. This revision covers the artifact rebuild with DS 005
    Addendum A code, end-to-end verification, and portal DEV->PROD merge.</revision>
  </metadata>

  <objective>
    Rebuild the opal-partners-data Lambda artifact from current source (includes DS 005
    Addendum A endpoints: handle_mix_timeseries, handle_concentration_timeseries), deploy
    via Terraform, verify all Books Tab endpoints end-to-end, then merge portal DEV->PROD
    and deploy.
  </objective>

  <context>
    Current state (partners-api-v1.0.1):
    - Lambda Terraform module: infra/aws/terraform/partners-api/ (1024MB, 120s)
    - API Gateway: 6 /api/scoped/partners/books/* routes live with JWT authorizer
    - awswrangler 3.x compat fixes applied (post-read filtering, dtype_backend='numpy', NA safety)
    - Gold artifacts exist on S3: client_mix_timeseries.parquet, client_concentration_timeseries.parquet (AE Gate 2 passed)

    What's missing: the deployed artifact was built from code BEFORE DS 005 commit (6cae4815).
    handle_mix_timeseries and handle_concentration_timeseries do not exist in the deployed Lambda.
    The 2 mix/concentration API Gateway routes return 500 (unhandled path).
  </context>

  <scope>
    <files>
      <file action="none">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py (source — already committed, do not modify)</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify">infra/aws/terraform/partners-api/ (terraform apply)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Rebuild artifact zip from current source at
      infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/.
      Upload to s3://opal-313476888478-lambda-artifacts/partners-api/opal-partners-data.zip.
      Use build-and-upload.sh or the PowerShell workaround (see MEMORY.md re: bun/MSYS2 path issue).
    </requirement>

    <requirement id="2">
      terraform plan on partners-api module. Expected change: source_code_hash update only.
      terraform apply. Verify 0-diff plan after apply.
    </requirement>

    <requirement id="3">
      Update lambda-source-map.json with new deployed commit hash and SHA256.
    </requirement>

    <requirement id="4">
      End-to-end verification — test ALL 8 Books Tab endpoint patterns via Lambda test invoke
      or curl. Use relationship z08327149 (confirmed working in v1.0.1 hotfix):

      | Endpoint | Expected |
      |---|---|
      | /books/relationship/{id}/timeseries?firmId=49financial | 200 + records (424 confirmed in v1.0.1) |
      | /books/relationship/{id}/composition?firmId=49financial | 200 + asset classes + top-10 |
      | /books/account/{id}/timeseries?firmId=49financial | 200 + records |
      | /books/account/{id}/composition?firmId=49financial | 200 + asset classes |
      | /books/relationship/{id}/mix-timeseries?firmId=49financial | 200 + daily mix pct data |
      | /books/relationship/{id}/concentration-timeseries?firmId=49financial | 200 + top-N holdings over time |

      The last 2 are the NEW Addendum A endpoints. If they return 500 or empty, the artifact
      rebuild did not pick up the DS 005 code — stop and investigate.
    </requirement>

    <requirement id="5">
      Tag: `partners-api-v1.1.0` (check `git tag -l "partners-api-v*" | sort -V | tail -5` first).
      Push with --follow-tags.
    </requirement>

    <requirement id="6">
      After DE firmId fix lands on portal DEV and endpoint verification passes:
      Portal DEV -> PROD merge and deploy.

      ```bash
      cd portal
      git checkout PROD
      git pull origin PROD
      git merge DEV
      git push origin PROD
      ./scripts/deploy-manual.sh
      git checkout DEV
      cd ..
      git add portal
      git commit --author="0.4.0_DT_ClientPlatform <0.4.0_DT_ClientPlatform@opal.agent>" -m "chore: update portal submodule (ADVI_MVPLVL Books Tab + Addendum A)"
      ```
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">0-diff Terraform plan after apply</criterion>
    <criterion id="2">All 6 original endpoints return valid JSON (timeseries, composition per relationship + account)</criterion>
    <criterion id="3">Both Addendum A endpoints return valid JSON (mix-timeseries, concentration-timeseries)</criterion>
    <criterion id="4">lambda-source-map.json updated with deployed commit + SHA256</criterion>
    <criterion id="5">Portal PROD reflects all ADVI_MVPLVL portal work (Books Tab + Addendum A panels)</criterion>
    <criterion id="6">Tag partners-api-v1.1.0 pushed</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify lambda_function.py — DS code is committed and correct. Only rebuild the artifact.</constraint>
    <constraint>Terraform is the only Lambda deployment mechanism (CLAUDE.md rule 1)</constraint>
    <constraint>Commit before apply (CLAUDE.md rule 2)</constraint>
    <constraint>Do NOT merge portal DEV->PROD until DE firmId fix is committed on DEV and all endpoints verified</constraint>
    <constraint>partners-api module is at infra/aws/terraform/partners-api/ — do NOT put it in bd-pipeline</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.005.gold-script-and-endpoints" status="complete">
      Lambda endpoint code committed (6cae4815)
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_MVPLVL.005.ec2-gold-deploy" status="complete">
      Gold artifacts exist on S3 and Gate 2 passed (9ee5a752, d1bd3a18)
    </dependency>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_MVPLVL.004.p4-books-proxy-wiring" status="complete">
      DE firmId fix committed on portal DEV (db52d31). DEV->PROD merge gate cleared.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">Lambda artifact rebuilt and deployed via Terraform</deliverable>
    <deliverable type="tag">partners-api-v1.1.0</deliverable>
    <deliverable type="deploy">Portal PROD updated with all ADVI_MVPLVL work</deliverable>
  </deliverables>
</task_order>
