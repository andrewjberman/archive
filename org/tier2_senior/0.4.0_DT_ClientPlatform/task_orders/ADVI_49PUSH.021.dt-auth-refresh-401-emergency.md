<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-09-49push-021-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>HOTFIX</wave>
    <phase>P4</phase>
  </metadata>

  <objective>
    EMERGENCY: Auth refresh endpoint returning 401 on opalinvest.dev after .019 Lambda deploy.
    Andrew is logged in as Opal admin, getting repeated 401s on POST /auth/refresh.
    API Gateway: 7k3ed8px20.execute-api.us-east-1.amazonaws.com
    Error source: AuthContext.tsx:93

    Diagnose and fix immediately. This likely broke during the portal-auth Terraform apply
    (.019) which touched shared-advisor-router (Lambda@Edge) and the CloudFront distribution.
  </objective>

  <context>
    .019 deployed two things:
    1. shared-advisor-router Lambda@Edge (platinum routes + PII block)
    2. opal-partners-data Lambda (platinum handlers)

    The portal-auth Terraform apply showed "2 changed (Lambda@Edge + CF distribution version)"
    with a note about persistent CF origin ordering drift. The auth/refresh endpoint goes
    through API Gateway (7k3ed8px20), NOT through CloudFront/shared-advisor-router. But the
    CF distribution change may have affected origin routing.

    The auth/refresh flow:
    - Browser POST to API GW /auth/refresh with refresh token cookie
    - API GW -> portal-auth Lambda (opal-portal-authorizer or opal-auth-handler)
    - Returns new JWT

    This is NOT an ADVI platinum path -- it's the core auth flow. If it's broken, NO user
    can authenticate.
  </context>

  <compiler_tools_mandate>
    1. comp-routes auth-map
       -- see which auth layers apply to /auth/refresh

    2. comp-routes trace auth/refresh
       -- full serving chain for the refresh endpoint

    3. comp-trace opal-portal-authorizer --direction both
       -- what the authorizer connects to

    4. comp-trace auth-validator-edge --direction both
       -- did the edge Lambda change break something?

    Check the Terraform state diff from .019 -- what EXACTLY changed in the CF distribution.
    Check if the API Gateway authorizer was affected by the portal-auth apply.
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      FIRST: Check if the 401 is a Terraform regression from .019.
      - Compare the CF distribution config before and after .019 apply
      - Check if API GW authorizer config was touched
      - Check if the auth-validator-edge Lambda@Edge viewer-request function was affected
      - The /auth/refresh path should NOT go through shared-advisor-router at all
    </requirement>

    <requirement id="2">
      Check CloudFront behaviors for /auth/* paths:
      - Which behavior catches /auth/refresh?
      - Does it route to API Gateway origin (7k3ed8px20)?
      - Was the origin config changed in .019?
    </requirement>

    <requirement id="3">
      Check the auth-validator-edge Lambda@Edge function:
      - Does it intercept /auth/refresh?
      - If so, does it try to validate a JWT on a refresh request (which has no JWT -- only a refresh cookie)?
      - This would cause 401 if the edge function validates JWT on ALL requests including /auth/refresh
    </requirement>

    <requirement id="4">
      If the issue is in .019 changes: FIX IT and re-deploy immediately.
      If the issue is pre-existing or unrelated: document and report.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>Root cause identified</deliverable>
    <deliverable>Fix deployed if .019 caused it</deliverable>
    <deliverable>Message to COO with root cause + fix status</deliverable>
  </deliverables>
</task_order>
