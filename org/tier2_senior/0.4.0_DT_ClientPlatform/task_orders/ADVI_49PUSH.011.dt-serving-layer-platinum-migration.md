<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-011-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>3</wave>
    <phase>P1+P3</phase>
  </metadata>

  <objective>
    Migrate the serving layer to route ALL Advisor Intelligence paths to platinum/ instead
    of gold/. Two components: shared-advisor-router (Lambda@Edge, S3 direct paths) and
    opal-partners-data (Lambda, API Gateway paths). After this change, every ADVI fetch
    that hits CloudFront resolves to a platinum/ S3 key.
  </objective>

  <context>
    D_04 produces pre-sliced JSON files under the platinum/ prefix in opal-data-bd. The
    serving layer currently rewrites ADVI URLs to gold/ S3 keys. This TO changes those
    rewrites to point at platinum/.

    PRD: docs/architecture/ADVI_49PUSH_P1_PRD.md (section: Serving Layer Changes)
    PRD: docs/architecture/ADVI_49PUSH_P3_PRD.md (section: Step 4 Update Serving Layer)

    The P1 PRD recommends Option A: add NEW /platinum/ path prefix routes. Old gold/ routes
    remain for any non-ADVI consumers. After all tabs migrate (P3), old gold/ rewrites for
    ADVI paths can be removed.

    Platinum file structure (canonical):
    platinum/firm/dashboard.json
    platinum/firm/mix_summary.json
    platinum/firm/partner_analytics_{quarterly|monthly|annual}.json
    platinum/firm/cumulative_chart.json
    platinum/firm/leaderboard.json
    platinum/firm/timeseries_overview.json
    platinum/advisors/{id}/summary.json
    platinum/clients/{rel_id}/summary.json
    platinum/clients/{rel_id}/mix_timeseries.json
    platinum/clients/{rel_id}/concentration.json
    platinum/accounts/{acct_id}/summary.json

    Audit briefs with full fetch-to-path mappings:
    - docs/briefs/ADVI_49PUSH_P2_2.1_partner_analytics.md
    - docs/briefs/ADVI_49PUSH_P2_2.2_distribution.md
    - docs/briefs/ADVI_49PUSH_P2_2.3_advisors_tab.md
    - docs/briefs/ADVI_49PUSH_P2_2.4_books_remaining.md
    - docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md (master catalog)
  </context>

  <compiler_tools_mandate>
    1. comp-routes behaviors
       -- list all 23 CloudFront behaviors to understand current routing

    2. comp-routes auth-map
       -- which ADVI paths use edge-only vs double auth (affects migration strategy)

    3. comp-routes trace getEmployeeLeaderboard
       -- example full chain: URL -> CF -> auth -> router -> S3 key

    4. comp-routes trace getPartnerAnalytics
       -- another chain to understand the rewrite pattern

    5. comp-trace shared-advisor-router --direction both
       -- what the router connects to

    6. comp-trace opal-partners-data --direction both
       -- what the Lambda connects to
  </compiler_tools_mandate>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda-edge/shared-advisor-router/index.mjs</file>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="reference">docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      shared-advisor-router (index.mjs):

      Add rewrite rules for platinum/ paths. For every ADVI URL pattern that currently
      rewrites to a gold/ S3 key, add a corresponding platinum/ rewrite.

      Current pattern (example):
        /api/scoped/advisor-intelligence/artifacts/employee_leaderboard.json
        -> rewrites to S3 key: gold/artifacts/employee_leaderboard.json

      New pattern:
        /api/scoped/advisor-intelligence/platinum/firm/dashboard.json
        -> rewrites to S3 key: platinum/firm/dashboard.json

      OR (if the router can swap in-place):
        Keep the same URL patterns but change the S3 key target from gold/ to platinum/
        for ALL ADVI artifact paths.

      Read the router code to determine which approach works. The goal: frontend calls
      the same or similar URLs, S3 reads come from platinum/ not gold/.
    </requirement>

    <requirement id="2">
      opal-partners-data (lambda_function.py):

      For routes that serve ADVI data through the Lambda (not direct S3):
      - Mix timeseries routes: change from reading gold/entities/clients/{id}.json to
        reading platinum/clients/{id}/mix_timeseries.json
      - Concentration routes: change from reading gold/entities/clients/{id}.json to
        reading platinum/clients/{id}/concentration.json
      - Any other ADVI routes that read gold/ should switch to platinum/

      Non-ADVI routes (model portfolios, market overview, etc.) MUST NOT be changed.
      They still read from gold/ via their own pipelines.
    </requirement>

    <requirement id="3">
      For routes that currently do Lambda-side transformation (filtering, pseudonymization):
      - Verify the platinum JSON structure matches what the Lambda expects
      - If field names changed between gold and platinum schemas, update the Lambda's
        field access accordingly
      - Pseudonymization must still work on platinum field names (check the HMAC function
        targets the right fields)
    </requirement>

    <requirement id="4">
      Do NOT remove old gold/ rewrite rules yet. Keep them for:
      - Non-ADVI consumers (if any)
      - Rollback safety
      Mark them with // LEGACY: ADVI_49PUSH -- remove after P3 validation
    </requirement>

    <requirement id="5">
      Do NOT deploy via Terraform. Write the code changes only. AE will deploy
      everything together (gold runner + Lambda + Lambda@Edge) in a coordinated deploy.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>shared-advisor-router/index.mjs updated with platinum/ rewrites</deliverable>
    <deliverable>opal-partners-data/lambda_function.py updated with platinum/ reads for ADVI routes</deliverable>
    <deliverable>Message to COO (2.0.0_SA_COO): route mapping table (old gold/ path -> new platinum/ path for each ADVI route)</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT modify non-ADVI routes -- only ADVI paths change</rule>
    <rule>Do NOT remove old gold/ rewrite rules -- mark as LEGACY</rule>
    <rule>Do NOT deploy via Terraform -- code changes only</rule>
    <rule>Do NOT break pseudonymization or book scoping (auth layer must still work)</rule>
  </do_not>
</task_order>
