<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-18-mvp318-002-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-18</date>
    <status>complete</status><!-- WS6 subsumed by GLDPRE.006 portal merge (portal-v2.1.16, 2026-03-23). All workstreams delivered. -->
    <!-- WS1-A: DONE. Root cause: BD country='United States' not 'USA' in script 07. geo_us empty -> 0 categories. DS fix: fec1f7e4. AE rebuilt geo parquet: b2119882. -->
    <!-- WS1-deploy: DONE. bd-portal-publisher deployed at fec1f7e4 (bd-v2.19.1). Lambda re-invoked, geo verified: TX=$900,754,857, 9 states. -->
    <!-- WS2+WS3b: DONE. bd-portal-advisor-publisher at a3903a03+14b3be3d (D4+WS3a+open_lots). bd-v2.19.0. -->
    <!-- WS3d: DONE. opal-partners-data at 6234d50c (WS3c handlers). partners-api-v1.4.0. -->
    <!-- API-GW: DONE (out-of-scope fix). 4 missing routes added to bd-pipeline TF: firm/composition, firm/mix-views, advisor/timeseries, advisor/mix-timeseries. bd-v2.19.2. -->
    <!-- WS6: BLOCKED. Gate: AE gold run complete + DS commits script 10. COO must confirm before merge. -->
    <project_code>ADVI_MVP318</project_code>
  </metadata>

  <objective>
    Execute four sequential tracks for ADVI_MVP318:
    (A) Run the WS1 diagnostic immediately to determine if bd-portal-publisher needs a fix deploy.
    (B) After DS commits D4+WS3a, deploy bd-portal-advisor-publisher (WS2+WS3b batched).
    (C) After DS commits WS3c, deploy opal-partners-data (WS3d).
    (D) After all portal DEV gates clear, perform the final DEV->PROD portal merge (WS6).
    DT is the deployment executor; do not begin deploys until DS confirms each commit gate.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_MVP318_PRD.md (WS1-A diagnostic, WS2, WS3b, WS3d, WS6).
    Deployment reference: docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md.
    Current bd pipeline tag: bd-v2.18.4. Check actual latest with:
      git tag -l "bd-v*" | sort -V | tail -5
    Current partners-api tag: partners-api-v1.0.0. Target for WS3d: partners-api-v1.4.0.
    Lambda source map: infra/aws/lambda/ci/lambda-source-map.json (must be updated for each deploy).
  </context>

  <scope>
    <files>
      <file action="run">.tmp_segment_analytics_diag.py (WS1-A diagnostic, read-only)</file>
      <file action="deploy">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py (WS2+WS3b)</file>
      <file action="deploy">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py (WS1, conditional)</file>
      <file action="deploy">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py (WS3d)</file>
      <file action="update">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS1-A" priority="immediate">
      Run the segment analytics diagnostic now — no DS gate required:
        python .tmp_segment_analytics_diag.py
      This script reads nna_aua_by_geography.parquet from S3 and prints whether the
      Snapshot value vs Continuous rightmost value gap is data-side or frontend-side.

      Interpret result:
      - S3 values match (gap &lt; $1K): Root Cause B (frontend windowing only). No data fix.
        Report to COO: skip WS1 deploy; RD will add "AUA as of [date]" subtitle (conditional).
      - S3 values differ: Root Cause A or C. DS fix applies; deploy bd-portal-publisher.

      Record the diagnostic output in your session log.
    </requirement>

    <requirement id="2" workstream="WS1-B-deploy" condition="Root Cause A or C only">
      If the diagnostic shows a data-side gap:
      1. Confirm DS committed the bd-portal-publisher fix to CLOUD (check git log).
      2. Build and upload bd-portal-publisher artifact:
           ./infra/aws/lambda/ci/build-and-upload.sh bd-pipeline bd-portal-publisher
      3. Update infra/aws/lambda/ci/lambda-source-map.json entry for bd-portal-publisher.
      4. Commit source map update:
           git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
             -m "deploy(bd-pipeline): bd-portal-publisher WS1 fix (ADVI_MVP318)"
      5. terraform plan + apply (bd-pipeline). Verify 0-diff plan on second apply.
      6. Check if this deploy can be batched with WS2 (same bd-pipeline) — prefer one terraform apply.
         If DS has also committed D4+WS3a by now, batch both into a single apply and single tag.
    </requirement>

    <requirement id="3" workstream="WS2+WS3b">
      GATE: DS must confirm commit of bd-portal-advisor-publisher (D4+WS3a) before proceeding.

      After gate clears:
      1. Build and upload artifact:
           ./infra/aws/lambda/ci/build-and-upload.sh bd-pipeline bd-portal-advisor-publisher
      2. Update infra/aws/lambda/ci/lambda-source-map.json entry for bd-portal-advisor-publisher.
      3. Commit source map update under DT author attribution.
      4. terraform plan (bd-pipeline). Verify expected changes (advisor-publisher function code hash).
      5. terraform apply. Verify 0-diff on second plan.
      6. If WS1 deploy is also needed (Root Cause A/C), batch both publishers into one apply.
      7. Tag: run `git tag -l "bd-v*" | sort -V | tail -5` FIRST to find actual latest.
         Recommended: bd-v2.19.0 (minor bump — new gold artifacts + architect override behavior).
         DT decides patch vs minor based on actual scope. Tag and push:
           git tag -a bd-v2.19.0 -m "ADVI_MVP318: architect override + advisor timeseries Lambda (WS2+WS3b)"
           git push --follow-tags
      8. Report deploy complete to COO. This is the gate for AE's gold layer run.
    </requirement>

    <requirement id="4" workstream="WS3d">
      GATE: DS must confirm commit of opal-partners-data WS3c handlers before proceeding.
      This deploy is on a separate Terraform pipeline (partners-api) — can run in parallel with WS2+WS3b
      once DS commits both.

      After gate clears:
      1. Build and upload:
           ./infra/aws/lambda/ci/build-and-upload.sh partners-api opal-partners-data
      2. Update lambda-source-map.json entry for opal-partners-data.
      3. Commit source map update under DT author attribution.
      4. terraform plan (partners-api module). Verify expected diff.
      5. terraform apply. Verify 0-diff on second plan.
      6. Tag: partners-api-v1.4.0 (check git tag -l "partners-api-v*" | sort -V | tail -5 first)
           git tag -a partners-api-v1.4.0 -m "ADVI_MVP318: advisor timeseries + mix-timeseries routes (WS3d)"
           git push --follow-tags
      7. Update deployment_map.xml.
      8. Report deploy complete to COO — this is the gate for DE's WS3e and RD's WS3f/L2 work.
    </requirement>

    <requirement id="5" workstream="WS6">
      GATE: All portal DEV gate conditions from PRD WS6 must be cleared:
      - WS1-C (conditional): RD "AUA as of [date]" label committed to DEV (if Root Cause B)
      - WS4: RD ConsolidatedOverviewPanel all levels (N1, L2, L3) committed to DEV
      - WS5: DE/RD periodToChartWindow + ChartWindowOption update committed to DEV
      Do not merge until COO confirms all gates cleared.

      After all gates cleared:
      1. Push portal DEV to remote:
           cd portal && git push origin DEV
      2. Verify DEV is at the correct commit (all WS commits present).
      3. Merge DEV to PROD:
           cd portal
           git checkout PROD
           git pull origin PROD
           git merge DEV
           git push origin PROD
           ./scripts/deploy-manual.sh
           git checkout DEV
      4. Update parent repo submodule pointer:
           cd ..
           git add portal
           git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
             -m "chore: update portal submodule (ADVI_MVP318 final merge)"
           git push origin CLOUD
      5. Report WS6 complete to COO.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1" status="DONE">WS1-A diagnostic run and result recorded; Root Cause reported to COO. Root Cause A: BD country encoding mismatch. Geo timeseries had 0 categories. TX=$900,754,857 verified post-fix.</criterion>
    <criterion id="2" status="DONE">bd-portal-advisor-publisher deployed at D4+WS3a+open_lots (a3903a03+14b3be3d). Tagged bd-v2.19.0.</criterion>
    <criterion id="3" status="DONE">bd-portal-publisher deployed. bd-v2.19.0 (MVPLVL.006 leaderboard). bd-v2.19.1 (WS1 geo fix fec1f7e4). Root Cause A/C confirmed.</criterion>
    <criterion id="4" status="DONE">opal-partners-data deployed at WS3c (6234d50c). Tagged partners-api-v1.4.0.</criterion>
    <criterion id="5" status="DONE">0-diff second plan confirmed: bd-v2.19.0, bd-v2.19.1, bd-v2.19.2, partners-api-v1.4.0.</criterion>
    <criterion id="6" status="BLOCKED">Portal DEV->PROD merge. Gate: AE gold run + DS script 10. Portal DEV is clean at 62143e7 (WS4 ConsolidatedOverviewPanel committed). WS5 cleared (933dfa3). Awaiting COO gate confirmation.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT run WS6 portal merge until COO explicitly confirms all gate conditions cleared</constraint>
    <constraint>Do NOT deploy bd-portal-advisor-publisher before DS commits D4+WS3a together in one commit</constraint>
    <constraint>Do NOT deploy bd-portal-publisher if Root Cause B — no data fix needed in that case</constraint>
    <constraint>Always check actual git tags before tagging — never assume next version number</constraint>
    <constraint>Terraform binary is at .tools/terraform.exe; export MSYS_NO_PATHCONV=1 for AWS ARN paths</constraint>
    <constraint>No emojis in any commit messages or shell commands (CLAUDE.md rule 13)</constraint>
    <constraint>lambda-source-map.json must be updated for every Lambda deploy</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVP318.001 req 3" status="done">
      DS committed D4+WS3a at a3903a03. Gate cleared. Deployed in bd-v2.19.0.
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVP318.001 req 4" status="done">
      DS committed WS3c handlers at 6234d50c. Gate cleared. Deployed in partners-api-v1.4.0.
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVP318.001 req 1" status="done">
      DS committed WS1 fix at fec1f7e4. Gate cleared. Deployed in bd-v2.19.1.
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_MVP318 gold run" status="pending">
      AE full gold run — gate for WS6 portal merge.
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVP318 script 10" status="pending">
      DS commits script 10 to CLOUD — gate for WS6 portal merge.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="report">WS1-A diagnostic result (root cause identified)</deliverable>
    <deliverable type="deploy">bd-portal-advisor-publisher deployed and tagged</deliverable>
    <deliverable type="deploy">opal-partners-data deployed and tagged partners-api-v1.4.0</deliverable>
    <deliverable type="deploy">Portal DEV->PROD merge complete; submodule pointer updated</deliverable>
  </deliverables>
</task_order>
