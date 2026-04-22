<task_order>
  <metadata>
    <id>ADVI_INFLEC.W8.3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>pending</status>
    <acked>pending</acked>
    <project_code>ADVI_INFLEC</project_code>
    <priority>P1 — Andrew directive 2026-04-22; pre-flight gate for W8.1 PROD</priority>
    <sla>~2h (curl enumeration + matrix + escalation if any failure)</sla>
    <decision_authority>Andrew directive 2026-04-22 (PRD §9 W8)</decision_authority>
    <dependency to="none">Independent. Runs first as backend verification; result gates W8.1 PROD promotion.</dependency>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md §9 W8 (commit 7fae09b9)</ref>
    <ref type="architectural_claim">`/api/general/*` + `/v1/*` = universal-auth (auth-validator-edge v7+ accepts any valid JWT). Partner-firm JWTs should pass. W8.3 verifies this claim empirically.</ref>
    <ref type="related_endpoints">portal-proxy getters: getCMAAssumptions, getOpalViews, getPositioningData, getHoldingsAttribution, getMacroData, getVolatilityData, getMacroTimeSeries, getYieldCurveData</ref>
  </references>

  <objective>
    Backend network-level verification that the three pages' data-fetch endpoints return 200 OK under a partner-firm bearer token (both 49F and Inflection). Enumerate endpoints, curl each, matrix the result. Any 403/404 = escalate to CTO BEFORE W8.1 merges to PROD (indicates hidden firm-scoped gate contradicting `/api/general/*` = any-auth claim).
  </objective>

  <scope>
    <files>
      <file action="read-only">portal/src/pages/CapitalMarketAssumptions/</file>
      <file action="read-only">portal/src/pages/Positioning/</file>
      <file action="read-only">portal/src/pages/Macroeconomics/</file>
      <file action="read-only">portal/src/api/portal-proxy.ts (for endpoint URL resolution)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Enumerate every data endpoint per page:
      <run>grep -rn "publicApiRequest\|apiRequest\|/v1/\|/api/" portal/src/pages/CapitalMarketAssumptions portal/src/pages/Positioning portal/src/pages/Macroeconomics</run>
      Resolve portal-proxy getter names to actual HTTP URLs via `portal/src/api/portal-proxy.ts` + `portal/src/api/endpoints/`.
    </requirement>
    <requirement id="2">Obtain valid bearer tokens:
      (a) 49financial test user token (ask DE / use existing test bearer per portal-auth runbook)
      (b) Inflection test user token (if W5.5 has provisioned a test user; if 0 users, document and skip Inflection leg)
    </requirement>
    <requirement id="3">For each endpoint × each JWT:
      <run>curl -s -o /tmp/resp.json -w "%{http_code}\n" -H "Authorization: Bearer $TOKEN" "$ENDPOINT"</run>
      Record: HTTP status, content-type, response size, first 500 chars of body (to catch CloudFront-intercepted HTML 403s).
    </requirement>
    <requirement id="4">Produce a matrix: rows=endpoint, cols=JWT, cells=status+content-type. Commit matrix as part of session log.</requirement>
    <requirement id="5">ANY 403 or 404 under a partner-firm JWT on `/api/general/*` or `/v1/*` → immediately MCP 1.0.0_SA_CTO with the failing endpoint + response headers + response body first 500 chars. Do NOT merge W8.1 to PROD until CTO resolves.</requirement>
    <requirement id="6">Commit with `--author="0.4.0_DT_ClientPlatform <0.4.0_DT_ClientPlatform@opal.agent>"` and `--only` on session log only (no portal/src changes under this TO).</requirement>
  </requirements>

  <compiler_tools_mandate>
    Phase 1 (before curl): <run>comp-routes behaviors</run> — list CloudFront CustomErrorResponse rules. Some CF configs rewrite 403 → index.html with 200 status. If any such rule exists for the paths in question, document it so "200 with HTML body" is treated as a FAILURE, not a PASS.
    Phase 2 (before curl): <run>comp-routes auth-map</run> — confirm which edge functions gate each path.
    Phase 3 (after matrix): <run>comp-routes trace {endpoint}</run> for any endpoint that failed — full CF→auth→origin trace for the CTO escalation packet.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <downstream to="W8.1">W8.3 FAIL = W8.1 PROD merge halted. W8.3 PASS = W8.1 cleared for PROD.</downstream>
    <parallel_to>W8.2 frontend-dev runs independently; W8.3 data-layer findings can explain W8.2 page-level failures.</parallel_to>
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="1">Endpoint enumeration matrix committed — every data URL the three pages fetch, resolved to its full CF origin path.</ac>
    <ac id="2">Matrix rows covered under 49F JWT — 200 status, JSON content-type, no HTML body.</ac>
    <ac id="3">Matrix rows covered under Inflection JWT (if test user provisioned) — same bar. If no Inflection test user, documented DEFER with W5.5 dependency.</ac>
    <ac id="4">Any failure produces a CTO escalation packet (endpoint + full request/response + `comp-routes trace` output + hypothesis).</ac>
    <ac id="5">Session log with Compiler Tools section; `org/compiler-tools-log.md` appended.</ac>
  </acceptance_criteria>

  <deliverables>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/{date}/inflec_w8_3_backend_curl_smoke.md` with endpoint matrix + compiler tools section</deliverable>
    <deliverable type="mcp" optional="true">If any failure: MCP to 1.0.0_SA_CTO with escalation packet</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT modify any portal/src file or any IAM/CF/Lambda resource under this TO. Verification only.</rule>
    <rule>Do NOT treat a 200-status HTML-body response as PASS. Inspect content-type AND body prefix.</rule>
    <rule>Do NOT let W8.1 merge to PROD while this TO has an unresolved failure.</rule>
  </do_not>
</task_order>
