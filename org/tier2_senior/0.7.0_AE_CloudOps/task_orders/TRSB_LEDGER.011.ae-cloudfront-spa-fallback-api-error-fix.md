<task_order>
  <metadata>
    <id>TRSB_LEDGER.011</id>
    <slug>ae-cloudfront-spa-fallback-api-error-fix</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 -- P0-incident follow-on. Authored on the CTO~B mechanism ruling 2026-05-18. Dispatch immediately; AE 0.7.0 is free (TRSB backend lane complete).</dispatch_unblock_condition>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P1 -- UX-blocking. Surfaced by the 2026-05-18 P0 trade-approve incident: a correct API 403 was masked as HTML, crashing the portal's JSON.parse. Every API auth-denial portal-wide is currently unreadable to the user.</priority>
    <sla>Same-day. CloudFront apply + invalidation propagation ~15-40min.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md -- CTO~B adding a v0.3 note (doc-of-record) for this fix.</prd>
    <incident>2026-05-18 P0: Andrew's first live trade APPROVE failed with "Unexpected token '<', '<!doctype'... is not valid JSON". Root cause A (correct TO-1 group-auth 403) was working as designed; root cause B is this TO -- the CloudFront error-masking.</incident>
    <ruling>CTO~B 2026-05-18: remove the distribution-global custom_error_response; restore the SPA deep-link fallback via a CloudFront Function URI-rewrite on the DEFAULT (S3) behavior only. Explicitly DO NOT use the S3 website error-document (incompatible with OAC).</ruling>
  </references>

  <objective>
    Stop the portal CloudFront distribution from masking API error responses as HTML. Today distribution EVTSA9VEHNZVH carries a distribution-global `custom_error_response` mapping HTTP 403 and 404 to `200 /index.html` (a single-page-app deep-link fallback). Because `custom_error_response` is distribution-global it ALSO catches `/api/*` responses -- so a clean Lambda `403 {"message": ...}` is replaced by `200 <!doctype html>`, and the portal's `fetch().json()` crashes. Fix: remove the global `custom_error_response`; reimplement the SPA deep-link fallback so it applies to the S3 default behavior ONLY, leaving `/api/*` 4xx to pass through with their real status + JSON body.
  </objective>

  <context>
    Portal CloudFront distribution `EVTSA9VEHNZVH` (aliases opalinvest.dev / www.opalinvest.dev). `comp-routes behaviors` confirms: 23 cache behaviors; `custom_error_response`: `403 -> 200 /index.html` and `404 -> 200 /index.html`, both distribution-global. `comp-routes` itself flags this ("Lambda 403 auth-denials will be swallowed").

    Why the global rule exists: SPA deep-link support -- a user hitting `opalinvest.dev/advisor-intelligence/...` directly must get `index.html` (the S3 origin would 403/404 that key). The rule is correct for the S3 default behavior, wrong for the `/api/*` API-Gateway behaviors.

    CloudFront has NO per-cache-behavior error-response config -- `custom_error_response` cannot be scoped to exempt `/api/*`. So the fix is to drop it and move the SPA fallback into a mechanism that IS per-behavior: a CloudFront Function on the default behavior.

    MECHANISM (CTO~B ruling -- locked):
    - USE: a CloudFront Function (viewer-request) attached to the DEFAULT (S3) cache behavior ONLY. It rewrites the request URI to `/index.html` when the URI is a SPA deep-link (no file extension) so S3 returns index.html 200. Asset requests (`.js`/`.css`/`.png`/etc.) and all `/api/*` requests are NOT affected -- the function is not on the API behaviors, and even on the default behavior it leaves extensioned paths alone.
    - DO NOT USE: the S3 website error-document. That feature requires the S3 *website* endpoint, which is public and mutually exclusive with OAC. The portal origin is expected to be OAC-backed (private); a website endpoint would fail or force the bucket public.
  </context>

  <scope>
    <step>Phase 0 -- Confirm the mechanism preconditions: (a) the portal S3 origin on EVTSA9VEHNZVH IS OAC-backed (origin access control / private). If by some chance it is a public S3 website endpoint, STOP and flag COO~B -- the website error-document option re-opens. OAC is expected. (b) Confirm the `/api/*` ordered cache behaviors have HIGHER precedence than the default `/*` behavior, so API requests never resolve to the default behavior or its function.</step>
    <step>Phase 1 -- Author the CloudFront Function (viewer-request): if `request.uri` has no file extension (SPA deep-link), rewrite `request.uri` to `/index.html`; otherwise pass through unchanged. Keep it minimal and well-commented. No emoji.</step>
    <step>Phase 2 -- In the EVTSA9VEHNZVH Terraform: attach the CloudFront Function to the DEFAULT (S3) cache behavior's viewer-request ONLY. Remove the distribution-global `custom_error_response` block (both the 403 and 404 entries). Do NOT attach the function to any `/api/*` or other API behavior.</step>
    <step>Phase 3 -- terraform apply (CLAUDE.md Rules 1-6). After apply, issue a CloudFront invalidation (`/*`) -- the old `custom_error_response` may have edge-cached index.html-for-403 responses that must be purged.</step>
    <step>Phase 4 -- Regression smoke (portal-WIDE -- this changes deep-linking for every portal page, not just trade submission): (a) SPA deep-links still resolve -- load a deep sub-route directly (e.g. an /advisor-intelligence deep route) and confirm index.html renders; (b) a static asset still loads (extensioned path not rewritten); (c) an API 403 now returns real JSON -- repro the trade-approve 403 (a non-approver approve) and confirm the portal receives `{"message": "...not in the approvers group..."}` with HTTP 403, NOT index.html.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-routes behaviors</run>
        <expect>EVTSA9VEHNZVH: custom_error_response shows 403->200/index.html + 404->200/index.html (the defect). The /api/* behaviors are ordered ABOVE the default /* behavior. Confirms the precondition.</expect>
        <if_mismatch>If /api/* behaviors are NOT higher-precedence than /*, flag COO~B before proceeding -- the function placement assumption breaks.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/terraform.exe plan</run>
        <expect>The plan shows ONLY: the new aws_cloudfront_function resource, its association on the default behavior's viewer-request, and the removal of the custom_error_response block. No other behavior, origin, or distribution attribute touched.</expect>
        <if_mismatch>If the plan touches an API behavior, an origin, or anything else, STOP -- do not apply. Re-isolate.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-routes behaviors (re-run post-apply)</run>
        <expect>EVTSA9VEHNZVH no longer lists a custom_error_response (or lists none for 403). The default behavior carries the new viewer-request function; /api/* behaviors are unchanged.</expect>
        <if_mismatch>If custom_error_response is still present, the apply did not take -- recheck state.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>CloudFront-configuration change -- no data, no Lambda source, no S3 content, no DynamoDB. Post-apply CloudFront invalidation is required (edge cache), but that is cache purge, not data reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: the portal CloudFront distribution EVTSA9VEHNZVH (Terraform) -- the SHARED portal distribution.
    also_in_to: none active in TRSB_LEDGER -- but this is the portal-wide distribution that the BASE team (base CTO/COO + the ClientPlatform/portal pods) owns the bulk of portal work on.
    required_action: COO~B sends base CTO + base COO a courtesy heads-up that the shared portal distribution is getting a custom_error_response -> CloudFront-Function migration (a portal-wide deep-link mechanism change). This is not a permission ask -- it is the TRSB_LEDGER incident fix -- but the base team must not be surprised by a portal-wide CF change. AE 0.7.0: confirm the courtesy heads-up has gone out (COO~B owns sending it) before the apply, and call out the change in the session log.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0 confirmed: the portal S3 origin is OAC-backed; /api/* cache behaviors are higher-precedence than the default /* behavior. (If the origin is unexpectedly a public website endpoint, the TO was flagged to COO~B before proceeding.)</ac>
    <ac id="AC2">A CloudFront Function (viewer-request) is attached to the DEFAULT (S3) cache behavior ONLY -- it rewrites extensionless URIs to /index.html and passes extensioned + /api/* requests through untouched.</ac>
    <ac id="AC3">The distribution-global custom_error_response (403->/index.html and 404->/index.html) is REMOVED from EVTSA9VEHNZVH.</ac>
    <ac id="AC4">Deployed via terraform apply (plan isolated to the function + association + custom_error_response removal); a CloudFront invalidation was issued post-apply; pipeline git tag applied.</ac>
    <ac id="AC5">Regression smoke PASS: (a) a SPA deep-link sub-route loads index.html and renders; (b) a static asset loads; (c) an API 403 (repro: a non-approver trade approve) returns real JSON {"message": "...not in the approvers group..."} with HTTP 403 to the browser -- NOT index.html. The portal can now render a readable auth-denial message.</ac>
    <ac id="AC6">No emoji. Session log with the Compiler Tools section + the portal-wide-change call-out + confirmation the base-team courtesy heads-up went out. RAVC2 to 2.0.0_SA_COO~B, CC 1.0.0_SA_CTO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="create">a CloudFront Function source (viewer-request URI-rewrite) + its Terraform resource</file>
    <file action="modify">the EVTSA9VEHNZVH CloudFront distribution Terraform (remove custom_error_response; associate the function on the default behavior)</file>
  </scope_files>

  <deliverables>
    <deliverable type="commit">CloudFront Function + EVTSA9VEHNZVH Terraform change, deployed via terraform apply + post-apply invalidation, pipeline tag applied.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section + regression-smoke results. RAVC2 to 2.0.0_SA_COO~B, CC 1.0.0_SA_CTO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT use the S3 website error-document mechanism -- it is incompatible with an OAC-backed origin (CTO~B ruling). CloudFront Function URI-rewrite only.</rule>
    <rule>Do NOT attach the function to any /api/* or other API cache behavior -- default (S3) behavior only. API requests must pass through with their real status.</rule>
    <rule>Do NOT skip the post-apply CloudFront invalidation -- stale edge-cached index.html-for-403 responses would mask the fix.</rule>
    <rule>Do NOT begin the apply before the base-team courtesy heads-up has gone out (COO~B owns sending it).</rule>
    <rule>Do not deploy outside Terraform (CLAUDE.md Rule 1).</rule>
  </do_not>
</task_order>
