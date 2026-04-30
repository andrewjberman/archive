<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>AUTH_COTTON.TO4</id>
    <project>AUTH_COTTON</project>
    <title>Smoke test — Cottonwood user login + page allowlist + deny verification</title>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status><!-- Andrew did smoke test directly 2026-04-29 (established password + manually smoke-tested production). Stale flip by 1.0.0_SA_CTO 2026-04-30. Project AUTH_COTTON COMPLETE per REGISTRY. -->
    <priority>high</priority>
    <estimated_effort>30-60 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/AUTH_COTTON.md</ref>
    <ref type="prd_section">§6 TO-4</ref>
    <ref type="gates">AUTH_COTTON.TO1 + TO2 + TO3 all PROD-deployed</ref>
    <ref type="login_target">opal portal PROD (same URL as Andrew + 49F/Inflection users)</ref>
  </references>

  <context>
    Final gate for AUTH_COTTON. Verifies the full Cottonwood user experience:
    JWT issued correctly, allowlist enforced, deny-list redirects to /market.
    Only fires after TO-1 (table), TO-2 (firmAccess.ts on PROD), and TO-3 (DDB seed) complete.
    COO will relay explicit GO after TO-1 + TO-3 RACVs received.
  </context>

  <scope>
    Login as user@cottonwood.com with Andrew-supplied password against PROD portal.

    CHECK 1 — JWT claims:
    Open browser DevTools → Application → Cookies or Network → auth response.
    Decode JWT. Verify:
    - firmId = "cottonwood"
    - role = "user"
    - firmRole = "user"
    - No advisorRole claim (absence is correct)

    CHECK 2 — Default landing:
    After login, confirm redirect lands on /market (not /advisor-intelligence or any denied path).

    CHECK 3 — All 11 ALLOW paths render:
    Navigate to each path. Confirm page renders (no redirect, no 403, no blank):
    /market, /portfolios, /cma, /positioning, /attribution,
    /factor-tilts, /valuations, /correlations, /macro,
    /security-scanner, /trade-submission

    CHECK 4 — All 3 DENY paths redirect to /market:
    Navigate directly to each:
    /advisor-intelligence → should redirect to /market (or show deny — NOT render ADVI content)
    /portfolio-management → should redirect to /market
    /data-refresh → should redirect to /market

    CHECK 5 — NavBar:
    Confirm denied paths are either hidden from NavBar or, if visible, clicking redirects
    to /market without rendering the page. Document which pattern the current portal uses.
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="N/A — E2E test, no comp-* tools required">
      <step>
        <run>N/A — E2E test validates live behavior, not static analysis.</run>
        <expect>Absence acknowledged.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="N/A">
      <step>
        <run>N/A</run>
        <expect>N/A</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after smoke test">
      <step>
        <run>Use /frontend-dev if available, otherwise manual DevTools + screenshot capture</run>
        <expect>All 11 paths 200 + render. All 3 denied paths redirect to /market. JWT correct.</expect>
        <if_mismatch>Diagnose: check firmAccess.ts PROD deployment + DDB row presence.
        File follow-up TO if any path behaves unexpectedly.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      JWT decode shows firmId=cottonwood, role=user, firmRole=user, no advisorRole.
      Evidence: JWT payload (decoded) in session log.
    </criterion>
    <criterion id="2">
      Default landing after login = /market. Evidence: screenshot or log entry.
    </criterion>
    <criterion id="3">
      All 11 allowed paths render (HTTP 200 + page content visible). Evidence: log entry
      listing each path + outcome. Screenshot for at least 2 representative paths.
    </criterion>
    <criterion id="4">
      All 3 denied paths redirect to /market (no ADVI content, no 500, no blank).
      Evidence: log entry for each denied path + outcome. Screenshot for /advisor-intelligence.
    </criterion>
    <criterion id="5">
      NavBar behavior documented (hidden vs visible-but-redirect for denied items).
      No new behavior introduced vs 49F/Inflection NavBar pattern. Evidence: note in session log.
    </criterion>
    <criterion id="6">
      RAVC to 2.0.0_SA_COO and to 1.0.0_SA_CTO: all 5 checks passed, AUTH_COTTON LIVE.
      Include: login confirmation, path matrix (pass/fail for all 14 paths), JWT claims.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="AUTH_COTTON.TO1" status="REQUIRED">
      opal-partner-cottonwood table must be ACTIVE.
    </dependency>
    <dependency agent="0.4.0_DT_ClientPlatform" task="AUTH_COTTON.TO2" status="REQUIRED">
      firmAccess.ts with cottonwood entry must be on PROD portal.
    </dependency>
    <dependency agent="0.4.0_DT_ClientPlatform" task="AUTH_COTTON.TO3" status="REQUIRED">
      DDB rows (FIRM#META, USER#PROFILE, partner row) must be seeded.
    </dependency>
    COO will relay GO to DT after all three upstream RACVs confirmed.
  </dependencies>

  <cross_domain_coordination>
    <none/>
    Smoke test is read-only (login + navigation). No writes to any shared state.
  </cross_domain_coordination>

  <commit_identity>
    No git commit for smoke test. Session log only.
    DT session log: org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-04-29/auth_cotton_to4_smoke_test.md
    RAVC to 2.0.0_SA_COO + 1.0.0_SA_CTO on completion.
  </commit_identity>

  <notes>
    If /advisor-intelligence 500s instead of redirecting, file a follow-up TO before
    declaring AUTH_COTTON LIVE. A 500 on a denied path means the route guard is not
    firing correctly — must be fixed before Andrew can give Cottonwood user credentials.
    Trade Submission (Q4): if submit action fails backend authorization (trade-users missing),
    document in RAVC as known gap, not a blocking failure. Page-visibility is the v1 target.
  </notes>
</task_order>
