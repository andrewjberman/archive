<task_order>
  <metadata>
    <id>TRSB_LEDGER.010</id>
    <slug>ae-decommission-legacy-public-trade-surface</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO FIRED 2026-05-18 -- Andrew authorized FULL DECOMMISSION (relayed via CTO~B): both gates cleared -- (1) legacy-form supersession CONFIRMED, (2) destructive-op authorization GRANTED for the CloudFront + S3 teardown (Andrew's explicit "authorize full decommission" IS the human authorization per CLAUDE.md autonomy rule). Tier 1 of the CTO~B legacy-surface decommission ruling. REASSIGNED 2026-05-18 from 0.7.0_AE_CloudOps to 0.6.1_AE_PartnerETL (COO~B lane call): TO-10 edits routes.tf + the opal-trade-form-ui CloudFront/S3 stanzas -- a file set disjoint from 0.7.0's handler serial lane (workflow_handler.py / dashboard_api.py / dynamodb.tf), so it parallelizes cleanly. Routing it to the idle-clear 0.6.1 lets it hit its same-day SLA the moment it unblocks instead of queuing behind TO-5 (R3, multi-day) + TO-8 on 0.7.0. Dispatch is GATED on an Andrew supersession confirm -- that nobody still uses the legacy standalone trade form (trades.opalcapital.com / opal-trade-form-ui). CTO~B is requesting that confirm from Andrew. COO~B flips to pending + fires GO to 0.6.1 once Andrew confirms supersession. EXPEDITED same-day once unblocked -- the public GET routes leak all trade data unauthenticated (P1 data exposure).</dispatch_unblock_condition>
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
    <step>Phase 3 -- Legacy form teardown. CONFIRMED by the Phase-1 recon (2026-05-18): the resources ARE Terraform-managed -- cloudfront-trade-form-ui.tf carries 3 resources (aws_cloudfront_origin_access_control.trade_form_ui, aws_cloudfront_distribution.trade_form_ui = E2RNVVND8GSGG3, aws_s3_bucket_policy.trade_form_ui) and s3.tf carries the trade_form_ui bucket block (opal-trade-form-ui). RECON GOTCHA -- `aws_s3_bucket.trade_form_ui` has NO `force_destroy` arg (defaults false) and versioning is ENABLED, so a Terraform destroy of the non-empty versioned bucket will FAIL. Required sequence: (a) add `force_destroy = true` to `aws_s3_bucket.trade_form_ui`, apply that one-line change first; (b) remove the cloudfront-trade-form-ui.tf resources + the trade_form_ui block in s3.tf, then apply -- Terraform disables the distribution, waits for CloudFront edge propagation, deletes it (~15-40min, fits the same-day SLA but plan for it), and force-purges all object versions + delete-markers from the bucket. Confirm NO other distribution or bucket is affected -- the other 5 trade-pipeline buckets (recon-ui, 3 recon-data, opal-data-trade-submissions) stay untouched. Recon also confirmed: the distribution has NO custom-domain alias (no Route53 cleanup in scope) and the bucket holds 7 legacy web-form static assets (HTML/JS/CSS/logo), NOT trade records -- do_not rule 3 satisfied.</step>
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
        <expect>Public routes return 401 OR 404 -- a removed route falls through to the authorizer-protected $default route, so 401 (active auth-reject) is the expected end state and is equivalent to 404 for the security objective (handler not reached). The legacy form URL no longer serves; the authenticated portal page is unaffected and still reaches /api/general/trades/*. (Precedent: TRSB_LEDGER.010a -- the removed workflow route returned 401 via $default; confirmed correct by CTO~B 2026-05-18.)</expect>
        <if_mismatch>If the authenticated portal broke, a shared integration or general route was disturbed -- roll back and re-isolate.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Decommission only -- removes routes + a distribution + an origin bucket. No trade data in DynamoDB is touched; no Lambda source; no reprocessing. (The S3 bucket emptied/deleted is the legacy FORM UI's static-asset origin -- it holds the legacy web form's HTML/JS, NOT trade records. Confirm this in Phase 1 before the teardown.)</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: infra/aws/terraform/shared-infra/apigateway-portal/routes.tf
    also_in_to: TRSB_LEDGER.010a (removed the POST /api/public/trades/workflow route from the same file -- ALREADY LANDED, shared-infra-v1.12.0).
    last_write_owner: 010a is complete (0.7.0_AE_CloudOps). This TO (0.6.1_AE_PartnerETL) pulls latest routes.tf and removes the remainder. 0.7.0's concurrent TRSB handler lane (TO-5/TO-8) edits a disjoint file set (workflow_handler.py / dashboard_api.py / dynamodb.tf) -- no contention; this TO parallelizes cleanly.
    required_action: Begin only after Andrew's supersession confirm is relayed by COO~B. (010a has already landed -- that prerequisite is satisfied.)
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 1 gate honored -- work began only after COO~B relayed Andrew's supersession confirm. (If Andrew did not confirm, the TO is re-scoped, not completed.)</ac>
    <ac id="AC2">All remaining `/api/public/trades/*` routes are removed from routes.tf. Every shared integration and every `/api/general/trades/*` authenticated route is intact.</ac>
    <ac id="AC3">The `opal-trade-form-ui` CloudFront distribution (E2RNVVND8GSGG3) is disabled + deleted, and its S3 origin bucket is emptied + deleted. No other distribution or bucket affected.</ac>
    <ac id="AC4">terraform plan isolated to the intended destructions; terraform apply succeeds with a 0-diff-after plan; pipeline git tag applied.</ac>
    <ac id="AC5">Smoke: each removed public route returns 401 or 404 (401 via the authorizer-protected $default fall-through is the expected/accepted end state); legacy form URL dead; authenticated portal TradeSubmission unaffected.</ac>
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
