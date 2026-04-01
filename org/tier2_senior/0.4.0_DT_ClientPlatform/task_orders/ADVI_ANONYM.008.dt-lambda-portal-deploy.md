<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-008-dt-deploy</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>complete</status>
    <!-- Completed 2026-04-01. Track A: partners-api-v1.12.0 + portal-auth-v1.4.0 (commit 59b7eef2). Track B: portal-v2.1.22 (submodule 5038f0bd). DE 1390fa1 + DS schema doc + Andrew treemap fix included. All CI green. -->
    <!-- STAGED: activate after DS .007 commits for Lambda deploy.
                  Portal deploy activates after DE .010 commits. -->
    <priority>high</priority>
    <type>deploy</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Deploy three Lambda updates (opal-partners-data, portal-authorizer, auth-handler)
    after DS .007 commits, then deploy the portal frontend after DE .010 commits.
    Two sequential sub-tasks; Lambda deploy comes first.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_P3_PRD.md -- §Deployment Order</ref>
    <ref type="ds_to">ADVI_ANONYM.007.ds-tier-refactor-book-scoping.md</ref>
    <ref type="de_to">ADVI_ANONYM.010.de-authcontext-refactor.md</ref>
    <ref type="lambda_1">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/</ref>
    <ref type="lambda_2">infra/aws/users/lambda/portal-authorizer/</ref>
    <ref type="lambda_3">infra/aws/opalinvest_dev/lambda/auth-handler/</ref>
  </references>

  <requirements>

    <requirement id="A1">
      TRACK A -- LAMBDA DEPLOY (after DS .007 commit)
      PREREQUISITE: `git log --oneline --author="0.4.0_DS" -3` shows DS .007 commit.

      Check DS session log for any TypeScript concerns flagged on auth-handler.
      If DS flagged uncertainty on auth-handler TypeScript, verify those specific files
      before deploying -- DE may have needed to assist.
    </requirement>

    <requirement id="A2">
      TRACK A -- Deploy opal-partners-data Lambda (partners-api pipeline):
      ```bash
      export TMPDIR="C:/Windows/Temp"
      cd infra/aws/terraform/partners-api
      bash ../../../scripts/build-and-upload.sh opal-partners-data
      .tools/terraform plan   # verify pseudonymizer.py changes included
      .tools/terraform apply
      .tools/terraform plan   # MUST show No changes
      ```
      Tag: check current `git tag -l "partners-api-v*" | sort -V | tail -5`, increment patch.
      Push --follow-tags.
    </requirement>

    <requirement id="A3">
      TRACK A -- Deploy portal-authorizer Lambda:
      The authorizer now includes advisorId in context. Deploy via its pipeline.
      Check lambda-source-map.json for the correct pipeline name.
      Standard Terraform sequence: build-and-upload -> plan -> apply -> 0-diff -> tag.
    </requirement>

    <requirement id="A4">
      TRACK A -- Deploy auth-handler Lambda:
      auth-handler is TypeScript. Build process may differ from Python Lambdas.
      Check infra/aws/opalinvest_dev/lambda/auth-handler/ for build scripts (npm build,
      tsc compile, etc.). Use the established deploy mechanism for this Lambda.
      Standard Terraform sequence after build: plan -> apply -> 0-diff -> tag.
    </requirement>

    <requirement id="A5">
      TRACK A -- Verify Lambda deploys:
      - Test with internal JWT (opal-capital user): should see all firms, cleartext PII
        (because role=admin, not because tier=internal)
      - Test with opal-capital/user JWT: should see all firms, HASHED PII (new behavior)
      Note verification results in session log.
    </requirement>

    <requirement id="B1">
      TRACK B -- PORTAL DEPLOY (after DE .010 commit)
      PREREQUISITE: `git log --oneline` in portal/ on DEV shows DE .010 commit
      (`feat(ADVI_ANONYM P3): AuthContext tier refactor`).

      Standard portal deploy:
      1. cd portal && git checkout DEV && git pull origin DEV
      2. git checkout PROD && git pull origin PROD
      3. git merge DEV
      4. git push origin PROD
      5. ./scripts/deploy-manual.sh
      6. git checkout DEV
      7. Update parent submodule: cd .. && git add portal && git commit + push CLOUD
    </requirement>

    <requirement id="B2">
      TRACK B -- Verify portal deploy:
      - andrew@opalinvest.com login: isInternal() should return true (firmId=opal-capital)
      - user@opalinvest.com login (after AE creates the account): canSeeCleartext() false
      - No console errors on advisor-intelligence pages
    </requirement>

    <requirement id="C1">
      Write session log:
      org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-04-01/advi_anonym_p3_deploy.md

      Include: DS commit hash used, Terraform tags for each Lambda, portal version,
      verification results for Track A5 and B2.

      Message COO when BOTH tracks are complete with all tags and portal version.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">opal-partners-data, portal-authorizer, auth-handler all at 0-diff, tagged, pushed.</criterion>
    <criterion id="2">opal-capital/user JWT gets hashed PII (new behavior). opal-capital/admin gets cleartext.</criterion>
    <criterion id="3">Portal deployed. AuthContext isInternal() uses firmId. canSeeCleartext() uses role only.</criterion>
    <criterion id="4">Parent submodule pointer updated and pushed to CLOUD.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>TRACK A requires DS .007 commit. TRACK B requires DE .010 commit. Do not deploy without prerequisites.</constraint>
    <constraint>AE .009 DynamoDB migration (tier update + test accounts) is independent. Lambda deploy does not need to wait for it.</constraint>
    <constraint>auth-handler deploy process may differ from Python Lambdas -- read the existing build artifacts before assuming.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ANONYM.007" status="pending">
      Lambda deploy requires DS commit.
    </dependency>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_ANONYM.010" status="staged">
      Portal deploy requires DE portal DEV commit.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">3 Lambdas deployed at 0-diff with tags</deliverable>
    <deliverable type="deploy">Portal deployed (DEV->PROD merge + server)</deliverable>
    <deliverable type="message">COO completion message with all tags and portal version</deliverable>
  </deliverables>
</task_order>
