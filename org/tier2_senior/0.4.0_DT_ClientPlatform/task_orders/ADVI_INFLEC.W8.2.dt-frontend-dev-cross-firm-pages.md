<task_order>
  <metadata>
    <id>ADVI_INFLEC.W8.2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>staged</status>
    <acked>pending</acked>
    <project_code>ADVI_INFLEC</project_code>
    <priority>P1 — Andrew directive 2026-04-22; gated on W8.1 DEV merge</priority>
    <sla>~3h (3 pages × 2 JWTs + constitution authoring if missing)</sla>
    <decision_authority>Andrew directive 2026-04-22 (PRD §9 W8)</decision_authority>
    <dependency to="W8.1" status="pending">Gated on DE merging W8.1 to DEV. MCP signal from DE on merge flips this TO to `pending`.</dependency>
    <dependency to="W8.4" status="pending">Inflection JWT coverage requires at least one real-advisor row in `opal-partner-inflection` DDB (verified by W8.4). If W8.4 returns insufficient, 49F-only coverage proceeds and Inflection leg is deferred to post-W5.5 user provisioning.</dependency>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md §9 W8 (commit 7fae09b9)</ref>
    <ref type="constitution_dir">portal/.frontend-dev/testing/</ref>
  </references>

  <objective>
    Run `frontend-dev` constitution against each of `/cma`, `/positioning`, `/macro` under (a) a 49financial test JWT and (b) an Inflection test JWT. Three pages × two JWTs = six visual/behavior runs.

    Verify per-run:
    1. Page loads without JavaScript runtime error
    2. No firmId-aware data branch returns empty/undefined state
    3. No 401/403/404 from `/api/general/*` or `/v1/*` data fetches under partner-firm JWT
    4. No blank/placeholder panels that would appear to a logged-in partner user
  </objective>

  <scope>
    <files>
      <file action="modify_or_create">portal/.frontend-dev/testing/cma.md — constitution for /cma if absent; extend if present</file>
      <file action="modify_or_create">portal/.frontend-dev/testing/positioning.md — constitution for /positioning if absent; extend if present</file>
      <file action="modify_or_create">portal/.frontend-dev/testing/macro.md — constitution for /macro if absent; extend if present</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Each constitution includes a partner-firm JWT scenario matrix (49F + Inflection). If only 49F JWT available (Inflection W5.5 not yet landed), document Inflection leg as DEFERRED with explicit reason.</requirement>
    <requirement id="2">Use `/frontend-dev` closed-loop cycle per XXX.md Visual Testing section — Playwright + acceptance checks + ACTIONABLE_FIXES iteration up to 5 times until PASS.</requirement>
    <requirement id="3">Any FAIL that requires DE code changes (not test-config changes) — MCP DE 0.4.0 with ACTIONABLE_FIXES block. Do NOT edit portal/src/ files under this TO; escalate back to DE.</requirement>
    <requirement id="4">Commit with `--author="0.4.0_DT_ClientPlatform <0.4.0_DT_ClientPlatform@opal.agent>"` and `--only` on listed constitution files + session log.</requirement>
  </requirements>

  <compiler_tools_mandate>
    Phase 1 (before run): <run>comp-routes behaviors</run> — check for CustomErrorResponse rules that might intercept 403 and return HTML (caught Lambda auth incident). If rules exist, document them so any HTML-body 403 in runs is not misread as PASS.
    Phase 2 (post-PASS): <run>comp-cache collisions</run> — re-run to confirm no new React Query key collisions introduced by partner-firm traffic on these pages.
    Phase 3 (after commit): append compiler results to session log + `org/compiler-tools-log.md`.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <upstream to="W8.1">DE must have merged firmAccess.ts to DEV before this TO starts. Acceptance of 49F leg does not require W8.1 (49F already has access); Inflection leg requires W8.1 merge.</upstream>
    <upstream to="W8.4">DE must have verified opal-partner-inflection has a real-advisor row. If 0, Inflection leg deferred per requirement 1.</upstream>
    <parallel_to>W8.3 DT backend curl smoke runs in parallel; findings from W8.3 inform constitution failure hypothesis.</parallel_to>
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="1">All 3 constitutions have an explicit 49F JWT scenario with PASS or ACTIONABLE_FIXES → fixed → PASS.</ac>
    <ac id="2">All 3 constitutions have an Inflection JWT scenario with PASS, or documented DEFERRED with W5.5 dependency cited.</ac>
    <ac id="3">Zero 401/403/404 from `/api/general/*` or `/v1/*` under either JWT on any page.</ac>
    <ac id="4">Zero console errors or React render errors on any of the 6 runs.</ac>
    <ac id="5">Session log with Compiler Tools section; `org/compiler-tools-log.md` appended.</ac>
  </acceptance_criteria>

  <deliverables>
    <deliverable type="commit">portal/.frontend-dev/testing/{cma,positioning,macro}.md constitutions with partner-firm scenarios</deliverable>
    <deliverable type="test_output">Playwright screenshots + PASS/FAIL matrices for the 6 runs (saved to constitution output path per frontend-dev convention)</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.0_DT_ClientPlatform/logs/{date}/inflec_w8_2_frontend_dev.md`</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT modify portal/src/* files. Failures route to DE via MCP ACTIONABLE_FIXES.</rule>
    <rule>Do NOT ship without the Inflection leg unless W8.4 explicitly returns 0 real-advisor rows AND the deferral is documented.</rule>
    <rule>Do NOT treat a CloudFront-intercepted HTML 403 as PASS — `comp-routes behaviors` output defines what error-response HTML bodies to expect.</rule>
  </do_not>
</task_order>
