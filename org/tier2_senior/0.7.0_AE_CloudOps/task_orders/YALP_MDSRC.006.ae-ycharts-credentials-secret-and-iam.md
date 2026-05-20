<task_order>
  <metadata>
    <id>YALP_MDSRC.006</id>
    <slug>ae-ycharts-credentials-secret-and-iam</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <completed>2026-05-20 -- ycharts/credentials SM secret + ycharts-credentials-read IAM grant deployed inf-pipeline-v1.7.65 (commit 1f0c6b192; record-deploy c969c4113; 3-add/0-change/0-destroy; 0-diff verified). ARN arn:aws:secretsmanager:us-east-1:313476888478:secret:ycharts/credentials-2deEMz. GetSecretValue resource-scoped to IAM user Andrew_Berman (.007 runner). Value populated out-of-band (cookie-bundle format per Andrew; CTO/COO authorized in-band; never in git/TF-state/logs/MCP). comp-iam gaps 0 new gaps. Secret-ready signalled to DS 0.1.0; RAVC2 to COO + CC CTO.</completed>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO NOW — Andrew-direct via CTO, urgent (the YCharts seat is currently free; Alyssa signed out). This TO has NO gate — the secret RESOURCE + IAM can be created immediately. The credential VALUE is placed by Andrew out-of-band; this TO does not wait on it.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 urgent — time-boxed to the YCharts seat-free window. Enables the YALP_MDSRC.007 live-session capability test.</priority>
    <sla>~0.5-1h — one Secrets Manager secret resource + one IAM grant, Terraform-managed. Fast/light.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.2. This TO = a Phase-0 capability-test enabler (CTO dispatch ask 2026-05-20, Andrew-direct).</prd>
    <orion_precedent>Orion's `orion/credentials` Secrets Manager secret — the pattern this mirrors (credential secret consumed by an authenticated-pull runner).</orion_precedent>
    <pairs_with>YALP_MDSRC.007 (DS 0.1.0) — the live YCharts authenticated-session capability test that consumes this secret.</pairs_with>
  </references>

  <context>
    Andrew freed the YCharts seat (the single-concurrent-session constraint — WS-1 Finding F1 — is clear for a one-off live test) and wants a real authenticated-session test against YCharts now, while the seat is free. This TO stands up the credential-storage + IAM so YALP_MDSRC.007 (DS 0.1.0) can run that test. AE creates the secret RESOURCE and the IAM grant ONLY — Andrew populates the credential VALUE out-of-band via the AWS console so the credentials never transit chat / MCP / git / logs.

    SCOPE CAVEAT (carry into the session log): this enables a TECHNICAL validation of the scrape path. It does NOT make a shared-seat scrape the production answer — WS-4's single-concurrent-session finding stands; production still needs a dedicated automation seat or the official API (Q1). Do not let the secret's existence be read as a production-architecture commitment.
  </context>

  <scope>
    <in_scope>
      - Create an AWS Secrets Manager secret `ycharts/credentials` (mirror Orion's `orion/credentials` shape); the secret RESOURCE Terraform-managed. POPULATE it (CTO update 2026-05-20 + Andrew in-band authorization for this interim recon test) with a COOKIE BUNDLE — `{"cookies":"<full Cookie request-header>"}` — extracted from `C:\Users\AndrewBerman\Downloads\ycharts.com2.har` (the most recent authenticated ycharts.com entry; jq one-liner in the COO dispatch MCP). The cookie value goes from the HAR file straight into Secrets Manager — never echoed, never into git/tfstate/logs/MCP (use `put-secret-value` so the value stays out of tfstate).
      - Grant the YALP_MDSRC.007 test runner `secretsmanager:GetSecretValue` on exactly that secret ARN (least-privilege, resource-scoped — mirror the Orion credential-read grant). MCP-confirm with 0.1.0_DS_MarketIntelligence the exact runner principal (the IAM role/identity DS will run the .007 test under) before scoping the grant.
      - Report back to COO + CTO + Andrew: the exact secret name + ARN + region, so Andrew knows precisely where to paste the credential value.
    </in_scope>
    <out_of_scope>
      - Do NOT populate the credential value — Andrew places it out-of-band (console).
      - Do NOT build the production YCharts capture mechanism — that is the WS-4 design, a v0.3 implementation TO.
      - No portal/Lambda/chain change.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the change">
      <step>
        <run>comp-iam service &lt;the test-runner principal / lambda-or-role&gt;</run>
        <expect>The current IAM surface of the principal that will read the secret — confirm what it already has so the GetSecretValue add is scoped minimally and no existing grant is disturbed.</expect>
        <if_mismatch>If the runner principal is not a comp-graph node (likely, if it is an ad-hoc DS runner identity), fall back to a direct read of the role's policy + document it; verify the grant is resource-scoped to the `ycharts/credentials` ARN.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit / after iam change">
      <step>
        <run>comp-iam gaps</run>
        <expect>No NEW IAM gap introduced by the secret + GetSecretValue grant. (Pre-existing unrelated gaps — e.g. the known mdpf-daily-trigger-lambda-role finding — are not in scope.)</expect>
        <if_mismatch>If a new gap is flagged, resolve it in iam.tf before apply.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after apply">
      <step>
        <run>aws secretsmanager describe-secret --secret-id ycharts/credentials  +  0-diff terraform replan</run>
        <expect>Secret exists; replan shows "No changes". Report secret name + ARN + region.</expect>
        <if_mismatch>Non-0-diff replan -> investigate drift before declaring done.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    MCP-coordinate with 0.1.0_DS_MarketIntelligence (YALP_MDSRC.007 owner) on the exact test-runner IAM principal before scoping the GetSecretValue grant. No shared files. The credential value is Andrew's out-of-band action — coordinate the "where to paste" handoff via the report-back, not by handling the value.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Secrets Manager secret `ycharts/credentials` created (resource Terraform-managed) and POPULATED with the cookie-bundle JSON `{"cookies":"..."}` extracted from `ycharts.com2.har`. ycsessionid + csrftoken + aws-waf-token confirmed present in the string before save. Value placed via `put-secret-value` so it does not enter tfstate.</ac>
    <ac id="AC2">An IAM grant of `secretsmanager:GetSecretValue` to the confirmed YALP_MDSRC.007 test-runner principal, resource-scoped to exactly the `ycharts/credentials` ARN (least-privilege). comp-iam gaps shows 0 new gaps.</ac>
    <ac id="AC3">Deployed Terraform-only: plan -> apply -> 0-diff replan -> tag -> push --follow-tags -> record-terraform-deploy. Secret verified present via describe-secret.</ac>
    <ac id="AC4">Report to COO + CC CTO + Andrew with the exact secret name + ARN + region (the paste target for Andrew's out-of-band credential placement). Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - Secrets Manager `ycharts/credentials` secret resource + the resource-scoped GetSecretValue IAM grant, Terraform-managed + deployed.
    - The secret name + ARN + region reported to COO + CTO + Andrew.
    - Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Populate the secret VALUE via `put-secret-value` (not Terraform) so the cookie bundle never enters tfstate. The cookie value goes from the HAR file straight into Secrets Manager — never echoed to stdout, never into git, logs, or an MCP message.</rule>
    <rule>Do NOT grant broader than `secretsmanager:GetSecretValue` on the single `ycharts/credentials` ARN — least-privilege, resource-scoped.</rule>
    <rule>Terraform-only deploy (CLAUDE.md Rule 1). No console-created resources except Andrew's credential-value paste.</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
