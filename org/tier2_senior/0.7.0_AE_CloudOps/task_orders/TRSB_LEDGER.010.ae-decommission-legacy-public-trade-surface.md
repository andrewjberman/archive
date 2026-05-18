<task_order>
  <metadata>
    <id>TRSB_LEDGER.010</id>
    <slug>ae-decommission-legacy-public-trade-surface</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-18. Tier 1 of the CTO~B legacy-surface decommission ruling. Dispatch is GATED on an Andrew supersession confirm -- that nobody still uses the legacy standalone trade form (trades.opalcapital.com / opal-trade-form-ui). CTO~B is requesting that confirm from Andrew. COO~B flips to pending + fires GO once Andrew confirms supersession. EXPEDITED same-day once unblocked -- the public GET routes leak all trade data unauthenticated (P1 data exposure).</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- same-day once unblocked. The /api/public/trades/* GET routes leak ALL trade submissions (parties, securities, comments, users) with no authentication.</priority>
    <sla>Same-day from GO.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md -- §9 "Legacy unauthenticated trade surface" (CTO~B amending to v0.2).</prd>
    <finding>TO-0 probe brief docs/briefs/trsb-ledger-to0-identity-seeding-probe-20260518.md §3.</finding>
    <ruling>CTO~B 2026-05-18: there is NO legitimate unauthenticated trade surface. The authenticated portal (/api/general/trades/* + portal/src/pages/TradeSubmission) is the complete current product. The /api/public/trades/* family AND the legacy opal-trade-form-ui standalone form (CloudFront distribution E2RNVVND8GSGG3, LIVE) are superseded scaffolding + a live exposure -- decommission both. TIER 0 (the workflow route) is TRSB_LEDGER.010a, already dispatched. This TO is Tier 1 -- the rest.</ruling>
  </references>

  <objective>
    Decommission the legacy unauthenticated trade surface: remove the remaining `/api/public/trades/*` routes (`submit`, all `submissions*` GET variants, `identifiers/search` + `identifiers/batch`, `users`) and retire the legacy `opal-trade-form-ui` CloudFront distribution + its S3 origin bucket. The authenticated portal is the complete product; this surface is superseded scaffolding and a live data-exposure.
  </objective>

  <context>
    `infra/aws/terraform/shared-infra/apigateway-portal/routes.tf` defines a `/api/public/trades/*` family with `authorization_type = NONE` on the same Lambda integrations as the authenticated `/api/general/` twins. The `workflow` route is removed by TRSB_LEDGER.010a (Tier 0, expedited). This TO removes the rest:
    - `POST /api/public/trades/submit`
    - all `GET /api/public/trades/submissions*` variants (by-* / {id} / excel)
    - `GET /api/public/trades/identifiers/search`, `POST /api/public/trades/identifiers/batch`
    - `GET /api/public/trades/users`

    The GET routes leak every trade submission -- parties, securities, comments, the user list -- with no auth. That is a P1 data exposure, not a cosmetic cleanup.

    The consumer of this surface is the legacy `opal-trade-form-ui` CloudFront distribution (`E2RNVVND8GSGG3`, currently LIVE + enabled) -- a pre-portal standalone unauthenticated trade form. CTO~B's ruling: it is superseded by the authenticated portal TradeSubmission page and is retired together with the routes.

    DESTRUCTIVE-OP NOTE: retiring a CloudFront distribution + deleting an S3 bucket are destructive, non-trivially-reversible operations (CLAUDE.md Agent Autonomy -- "Deleting S3 objects", distribution teardown). The Andrew supersession confirm (the dispatch gate) IS the human authorization for the teardown. Even so, the S3 bucket teardown step must be performed deliberately -- see Phase 3.
  </context>

  <scope>
    <step>Phase 1 -- SUPERSESSION CONFIRM (gate). Do NOT proceed until COO~B relays Andrew's confirmation that the legacy standalone trade form (trades.opalcapital.com / opal-trade-form-ui) is genuinely superseded and unused. CTO~B is requesting this confirm from Andrew. If Andrew says any partner/ops user still uses the legacy form, STOP -- this TO re-scopes (the form would need migration onto the authenticated portal first).</step>
    <step>Phase 2 -- Routes: remove the remaining `/api/public/trades/*` route resources from routes.tf (submit, submissions* variants, identifiers/search, identifiers/batch, users). Leave all shared integrations and ALL `/api/general/trades/*` authenticated routes intact. terraform plan must show only public-route destructions.</step>
    <step>Phase 3 -- Legacy form teardown: disable the `opal-trade-form-ui` CloudFront distribution (E2RNVVND8GSGG3), wait for the disable to propagate, then delete the distribution; then empty + delete its S3 origin bucket. If these resources are Terraform-managed, do the teardown via Terraform (`terraform destroy` scoped to those resources, or remove the stanzas + apply); if not, document the manual teardown step-by-step in the session log. Confirm no other distribution or bucket is affected.</step>
    <step>Phase 4 -- terraform apply; commit per CLAUDE.md Rules 1-6 + tag. Smoke: a `/api/public/trades/*` route returns 404; the legacy form URL no longer serves; the authenticated portal TradeSubmission page is unaffected.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct read: infra/aws/terraform/shared-infra/apigateway-portal/routes.tf + the opal-trade-form-ui CloudFront/S3 Terraform stanzas (cloudfront-trade-form-ui.tf or equivalent under infra/aws/terraform/trade-pipeline/ or shared-infra/)</run>
        <expect>Every remaining /api/public/trades/* route is enumerated; the opal-trade-form-ui distribution + its origin bucket are located and their Terraform-managed-vs-manual status is known. comp-routes N/A (uninstrumented, PRD §5).</expect>
        <if_mismatch>If the distribution/bucket is not Terraform-managed, document the manual teardown path; do not guess at resource ids -- confirm E2RNVVND8GSGG3 via `aws cloudfront get-distribution`.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/terraform.exe plan</run>
        <expect>Only the remaining /api/public/trades/* routes (and the opal-trade-form-ui distribution + bucket, if Terraform-managed) are destroyed. No shared integration destroyed; no /api/general/ route touched; no unrelated resource.</expect>
        <if_mismatch>If the plan destroys a shared integration or any /api/general/ route or any non-trade-form distribution, STOP -- do not apply. Re-isolate.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>Smoke: curl a /api/public/trades/* route; load the legacy form URL; load the authenticated portal TradeSubmission page</run>
        <expect>Public routes return 404; the legacy form URL no longer serves; the authenticated portal page is unaffected and still reaches /api/general/trades/*.</expect>
        <if_mismatch>If the authenticated portal broke, a shared integration or general route was disturbed -- roll back and re-isolate.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Decommission only -- removes routes + a distribution + an origin bucket. No trade data in DynamoDB is touched; no Lambda source; no reprocessing. (The S3 bucket emptied/deleted is the legacy FORM UI's static-asset origin -- it holds the legacy web form's HTML/JS, NOT trade records. Confirm this in Phase 1 before the teardown.)</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/terraform/shared-infra/apigateway-portal/routes.tf
    also_in_to: TRSB_LEDGER.010a (removes the POST /api/public/trades/workflow route from the same file -- lands FIRST)
    last_write_owner: 0.7.0_AE_CloudOps owns both. 010a lands first (P0); this TO pulls latest routes.tf and removes the remainder.
    required_action: Begin only after 010a has landed and Andrew's supersession confirm is relayed by COO~B.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 1 gate honored -- work began only after COO~B relayed Andrew's supersession confirm. (If Andrew did not confirm, the TO is re-scoped, not completed.)</ac>
    <ac id="AC2">All remaining `/api/public/trades/*` routes are removed from routes.tf. Every shared integration and every `/api/general/trades/*` authenticated route is intact.</ac>
    <ac id="AC3">The `opal-trade-form-ui` CloudFront distribution (E2RNVVND8GSGG3) is disabled + deleted, and its S3 origin bucket is emptied + deleted. No other distribution or bucket affected.</ac>
    <ac id="AC4">terraform plan isolated to the intended destructions; terraform apply succeeds with a 0-diff-after plan; pipeline git tag applied.</ac>
    <ac id="AC5">Smoke: public routes 404; legacy form URL dead; authenticated portal TradeSubmission unaffected.</ac>
    <ac id="AC6">No emoji. Session log with the Compiler Tools section + the destructive-teardown step log. RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="modify">infra/aws/terraform/shared-infra/apigateway-portal/routes.tf</file>
    <file action="modify">the opal-trade-form-ui CloudFront + S3 Terraform stanzas (cloudfront-trade-form-ui.tf or equivalent -- locate in Phase 1)</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">routes.tf + opal-trade-form-ui teardown, deployed via terraform apply, tag applied.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section + destructive-teardown step log. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not begin before Andrew's supersession confirm is relayed -- the legacy form teardown is destructive and irreversible without that confirm.</rule>
    <rule>Do not delete any shared integration or any /api/general/trades/* route -- the authenticated portal depends on them.</rule>
    <rule>Do not delete any S3 bucket other than the opal-trade-form-ui static-asset origin -- confirm the bucket's contents are legacy form UI assets, not trade records, before emptying it.</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1) unless the distribution/bucket is confirmed non-Terraform-managed -- then document every manual step.</rule>
  </do_not>
</task_order>
