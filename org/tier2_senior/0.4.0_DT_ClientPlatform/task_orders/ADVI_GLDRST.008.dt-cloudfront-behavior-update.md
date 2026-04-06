<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-008-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_GLDRST</project_code>
    <revised_by>1.0.0_SA_CTO</revised_by>
    <revised_date>2026-03-26</revised_date>
    <revision_reason>CTO audit found task order missing shared-advisor-router Lambda@Edge code change (the core of this work), contradicted management model (said Terraform but distribution is console-managed), and lacked URL-to-key mapping.</revision_reason>
  </metadata>

  <objective>
    Update the shared-advisor-router Lambda@Edge function to rewrite
    portal URL paths to the new GLDRST S3 key layout. This is a code
    change to the origin-request Lambda@Edge, NOT a CloudFront behavior
    config change.

    After this, the portal reads from gold/artifacts/, gold/entities/,
    gold/timeseries/, and gold/dimensions/ — the new categorized layout.
    Old S3 keys can then be cleaned up (.010).
  </objective>

  <context>
    CURRENT STATE (shared-advisor-router v7):
    The router at infra/aws/lambda-edge/shared-advisor-router/index.mjs
    line 84 does a simple prefix swap:

      request.uri.replace("/api/scoped/advisor-intelligence/", "/gold/")

    This means:
      /api/scoped/advisor-intelligence/architect_leaderboard.json
        -> /gold/architect_leaderboard.json

    AFTER GLDRST:
    The flat /gold/ prefix no longer works because keys are now
    subcategorized. The router must map URL path suffixes to the
    correct S3 subcategory.

    DISTRIBUTION: EVTSA9VEHNZVH (d2n2nzpeqf34ge.cloudfront.net)
    MANAGEMENT: Console-managed, NOT Terraform. CloudFront behavior
    config is set via AWS console. Only cache policies are in Terraform
    (infra/aws/terraform/portal-auth/cloudfront.tf).

    PREREQUISITE: The blast radius assessment recommends importing
    CloudFront into Terraform before this TO. If time permits, do
    this first. If not, proceed with console updates and document
    every change for future Terraform import.

    LAMBDA@EDGE DEPLOY: Lambda@Edge functions must be published as
    numbered versions, then the CloudFront behavior association is
    updated to point to the new version ARN. This is a console
    operation (or Terraform if imported). Allow 5-15 minutes for
    CloudFront propagation after updating the behavior.
  </context>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda-edge/shared-advisor-router/index.mjs</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      UPDATE THE ROUTER REWRITE LOGIC (line 82-86 of index.mjs).

      Replace the simple prefix swap:
        request.uri = request.uri.replace("/api/scoped/advisor-intelligence/", "/gold/");

      With a categorized rewrite that maps URL suffixes to the correct
      S3 subcategory. The mapping:

      ARTIFACTS (flat JSON files written by publisher Lambdas or EC2 scripts):
        /api/scoped/.../architect_leaderboard.json    -> /gold/artifacts/architect_leaderboard.json
        /api/scoped/.../implementor_leaderboard.json  -> /gold/artifacts/implementor_leaderboard.json
        /api/scoped/.../timeseries_chart.json         -> /gold/artifacts/timeseries_chart.json
        /api/scoped/.../clients_tab.json              -> /gold/artifacts/clients_tab.json
        /api/scoped/.../advisor_rolling_flows.json    -> /gold/artifacts/advisor_rolling_flows.json
        /api/scoped/.../firm_mix_views.json           -> /gold/artifacts/firm_mix_views.json
        /api/scoped/.../summary/header_metrics.json   -> /gold/artifacts/summary/header_metrics.json
        /api/scoped/.../filters/dimensions.json       -> /gold/artifacts/filters/dimensions.json
        /api/scoped/.../snapshots/*.json              -> /gold/artifacts/snapshots/*.json
        /api/scoped/.../partner_analytics/*.json      -> /gold/artifacts/partner_analytics/*.json
        /api/scoped/.../clients/growth_timeseries.json      -> /gold/artifacts/clients/growth_timeseries.json
        /api/scoped/.../clients/tax_basis_breakdown.json    -> /gold/artifacts/clients/tax_basis_breakdown.json
        /api/scoped/.../clients/tax_deferred_candidates.json -> /gold/artifacts/clients/tax_deferred_candidates.json

      ENTITIES (per-advisor and per-client JSON bundles):
        /api/scoped/.../advisors/{id}/book.json          -> /gold/entities/advisors/{id}/book.json
        /api/scoped/.../advisors/{id}/timeseries.json    -> /gold/entities/advisors/{id}/timeseries.json
        /api/scoped/.../advisors/{id}/mix_timeseries.json -> /gold/entities/advisors/{id}/mix_timeseries.json
        /api/scoped/.../advisors/{id}/mix.json           -> /gold/entities/advisors/{id}/mix.json
        /api/scoped/.../advisors/{id}/composition.json   -> /gold/entities/advisors/{id}/composition.json
        /api/scoped/.../client_timeseries/{id}.json      -> /gold/entities/clients/{id}/timeseries.json

      VIEWS (pre-computed, already subcategorized — no change):
        /api/scoped/.../views/firm_composition.json      -> /gold/views/firm_composition.json

      TIMESERIES (already subcategorized — no change):
        /api/scoped/.../timeseries/nna_total.json        -> /gold/timeseries/nna_total.json
        /api/scoped/.../timeseries/nna_by_{dim}.json     -> /gold/timeseries/nna_by_{dim}.json

      IMPLEMENTATION APPROACH: Use pattern matching on the URI suffix.
      The cleanest implementation:

        const suffix = request.uri.replace("/api/scoped/advisor-intelligence/", "");

        if (suffix.startsWith("advisors/")) {
          request.uri = "/gold/entities/" + suffix;
        } else if (suffix.startsWith("client_timeseries/")) {
          // client_timeseries/{id}.json -> entities/clients/{id}/timeseries.json
          const id = suffix.replace("client_timeseries/", "").replace(".json", "");
          request.uri = "/gold/entities/clients/" + id + "/timeseries.json";
        } else if (suffix.startsWith("views/") || suffix.startsWith("timeseries/")) {
          request.uri = "/gold/" + suffix;  // already subcategorized
        } else {
          request.uri = "/gold/artifacts/" + suffix;  // everything else -> artifacts
        }

      This default-to-artifacts approach means any new flat JSON keys
      automatically land in artifacts without a code change. Only
      entities and the client_timeseries rename need explicit handling.
    </requirement>

    <requirement id="2">
      PUBLISH AND DEPLOY the updated Lambda@Edge function:
      1. Update index.mjs with the new rewrite logic
      2. Publish a new numbered version (v8)
      3. Update CloudFront behavior #4 (/api/scoped/advisor-intelligence/*.json)
         to associate with the new version ARN
      4. Wait 5-15 minutes for CloudFront propagation
      5. Verify end-to-end: portal loads all advisor-intelligence tabs
    </requirement>

    <requirement id="3">
      VERIFY all portal URL paths work after the router update.
      Test each URL pattern against a known firm bucket:

        /api/scoped/advisor-intelligence/architect_leaderboard.json
        /api/scoped/advisor-intelligence/summary/header_metrics.json
        /api/scoped/advisor-intelligence/advisors/{known_id}/book.json
        /api/scoped/advisor-intelligence/client_timeseries/{known_id}.json
        /api/scoped/advisor-intelligence/timeseries/nna_total.json
        /api/scoped/advisor-intelligence/views/firm_composition.json

      All must return HTTP 200 with valid JSON. Any 403/404 means
      the rewrite logic has a bug or the S3 key doesn't exist at
      the new path.
    </requirement>

    <requirement id="4">
      DOCUMENT every CloudFront console change for future Terraform
      import. Record: behavior number, path pattern, origin, associated
      Lambda@Edge function ARN + version, cache policy ID.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">shared-advisor-router v8 deployed and associated with behavior #4</criterion>
    <criterion id="2">All portal URL patterns return HTTP 200 with valid JSON from new S3 paths</criterion>
    <criterion id="3">Portal loads all 4 advisor-intelligence tabs without errors</criterion>
    <criterion id="4">CloudFront propagation complete (verify from multiple test URLs)</criterion>
    <criterion id="5">Console changes documented for Terraform import</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Requires .007 (Lambda dual-write to new paths) to be deployed and verified</constraint>
    <constraint>CloudFront distribution EVTSA9VEHNZVH is console-managed — all behavior changes are manual</constraint>
    <constraint>Lambda@Edge must be deployed in us-east-1 (CloudFront requirement)</constraint>
    <constraint>Allow 5-15 minutes for CloudFront propagation — do NOT declare failure before propagation completes</constraint>
    <constraint>Preserve ALL existing router behavior: OPTIONS handling (v6), Opal Capital staff routing (v7), dynamic firm bucket routing (v4)</constraint>
    <constraint>Do NOT modify any CloudFront behaviors other than #4 (scoped advisor-intelligence)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_GLDRST.007" status="pending">
      Lambda dual-write must be deployed and verified — old paths still need to work until router is updated
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">shared-advisor-router index.mjs v8 with categorized rewrite logic</deliverable>
    <deliverable type="deploy">Lambda@Edge version publish + CloudFront behavior association update</deliverable>
    <deliverable type="document">CloudFront console change log for Terraform import</deliverable>
  </deliverables>
  <tooling>
    <tool module="interpret.ast_extractor" when="before_coding">
      Parse shared-advisor-router index.mjs (Lambda@Edge). Extract the URL rewrite
      rules and path mappings. Document every route pattern before modification so
      the v7->v8 diff is auditable.
    </tool>

    <tool module="adapt.differential_regression" when="after_coding">
      Diff the router v8 against v7 baseline. Verify: every old route still resolves
      (through rewrite to new path), no route deleted without replacement, new
      categorized paths (gold/artifacts/, gold/entities/) are covered.
    </tool>
  </tooling>
</task_order>
