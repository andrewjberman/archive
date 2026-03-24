<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-23-mvplvl-009-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>ADVI_MVPLVL</project_code>
    <thread_serial>ADVI_MVPLVL-006</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-006-mix-and-composition-e2e-trace----broken/</thread_ref>
  </metadata>

  <objective>
    QA gate + deploy for ADVI_MVPLVL .009 fixes. After DE and RD commit their
    portal fixes to DEV, DT reviews, pushes DEV, and triggers the CI pipeline
    (DEV->PROD merge -> push PROD -> auto-deploy). If AE commits a Lambda fix
    (advisor mix-timeseries S3 key), DT also deploys that via Terraform.
  </objective>

  <scope>
    <files>
      <file action="verify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
      <file action="verify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
      <file action="verify">portal/src/api/endpoints/advisor-intelligence.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      QA gate: verify DE + RD commits pass TypeScript build (bunx tsc -b) and
      ESLint (0 errors). Check that no "Cash" label appears in the codebase
      where "Other" is required.
    </requirement>

    <requirement id="2">
      Push portal DEV branch to remote. Merge DEV->PROD (fast-forward). Push PROD
      to trigger CI auto-deploy pipeline (validate -> build -> S3 -> CF -> tag).
      Verify pipeline completes green.
    </requirement>

    <requirement id="3">
      If AE commits advisor mix-timeseries S3 key fix to CLOUD:
      - Run build-and-upload.sh for opal-partners-data
      - Commit source map update
      - terraform plan -> terraform apply -> verify 0-diff
      - record-terraform-deploy.sh -> tag -> push --follow-tags
    </requirement>

    <requirement id="4">
      Visual verification: after deploy, confirm in browser:
      - Assets Overview Mix toggle shows stacked bar (not error/loading state)
      - Books tab Overview shows Asset Mix radial + Top Holdings at firm level
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">TypeScript build passes (0 errors)</criterion>
    <criterion id="2">ESLint passes (0 errors)</criterion>
    <criterion id="3">Portal CI pipeline green (auto-tagged portal-v{X.Y.Z})</criterion>
    <criterion id="4">Mix toggle and Books overview visually render in browser</criterion>
    <criterion id="5">If Lambda deployed: 0-diff plan, tag pushed, CHANGELOG.json updated</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Wait for DE + RD commits before pushing. Do not push partial work.</constraint>
    <constraint>Portal CI pipeline is already configured (deploy.yml). Use it -- do not deploy manually unless pipeline fails.</constraint>
    <constraint>Commit with --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13).</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_MVPLVL.009-de.api-wiring-normalization" status="pending">
      DE must commit API wiring + normalization before DT pushes.
    </dependency>
    <dependency agent="0.4.2_RD_AdvisorIntelligence" task="ADVI_MVPLVL.009-rd.mix-rendering-normalization" status="pending">
      RD must commit PartnerAnalytics Mix normalization before DT pushes.
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_MVPLVL.009-ae.verify-lambda-routes" status="pending">
      Optional: if AE commits Lambda fix, DT deploys it. If no Lambda fix needed, skip Terraform.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Portal DEV push + PROD merge + CI deploy</deliverable>
    <deliverable type="commit">Optional: Lambda deploy (partners-api-v1.9.0) if S3 key fix committed</deliverable>
    <deliverable type="verify">Browser visual confirmation of both views rendering</deliverable>
  </deliverables>
</task_order>
