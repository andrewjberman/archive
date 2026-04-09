<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-015-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~C</issued_to>
    <date>2026-04-08</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>4</wave>
    <phase>P4</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform~C" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Write test_platinum_auth.py -- an automated auth smoke test that hits every platinum
    path via CloudFront with 4 test account tiers and verifies correct response codes,
    firm scoping, pseudonymization, and book scoping.
  </objective>

  <context>
    PRD: docs/architecture/ADVI_49PUSH_P4_PRD.md (sections: Test Plan, Test Matrix T1-T6)

    The P4 PRD defines 4 test accounts and a full test matrix (T1-T6). This script
    automates those tests so they can run instantly after deploy.

    DT route mapping (.011): all platinum URLs use the pattern
    /api/scoped/advisor-intelligence/platinum/{path}

    Auth layers (from ANONYM):
    - Layer 1: auth-validator-edge (Lambda@Edge) -- validates JWT, injects X-User-* headers
    - Layer 2: opal-portal-authorizer (API GW) -- validates JWT, returns allowedFirmIds
    - Layer 3: opal-partners-data (Lambda) -- firmId scoping, book scoping, pseudonymization

    Reference: docs/architecture/ADVI_ANONYM_PRD.md, docs/architecture/ADVI_ANONYM_P3_PRD.md
  </context>

  <compiler_tools_mandate>
    1. comp-routes auth-map
       -- which platinum paths have edge-only vs double auth

    2. comp-routes trace getEmployeeLeaderboard
       -- example auth chain to understand layer structure

    3. comp-trace auth-validator-edge --direction both
    4. comp-trace opal-portal-authorizer --direction both
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      Location: scripts/test_platinum_auth.py
    </requirement>

    <requirement id="2">
      Test accounts (from P4 PRD):
      - Internal admin (andrew@opalinvest.com): full access, cleartext, all firms
      - Internal user (user@opalinvest.com): full access, cleartext, all firms
      - 49F admin: 49F only, cleartext, all 49F books
      - 49F advisor: 49F only, pseudonymized (except own book), own book only
    </requirement>

    <requirement id="3">
      Test matrix (from P4 PRD T1-T6):

      T1: Page load -- hit firm-level platinum files, verify 200 + correct scoping
      T2: Advisors tab -- leaderboard access, verify pseudonymization for 49F advisor
      T3: Books drill -- own vs other advisor's book, verify 403 or filtered for 49F advisor
      T4: ClientDetail -- mix_timeseries + concentration access scoping
      T5: Cross-firm isolation -- 49F requesting other firm = 403
      T6: Pseudonymization integrity -- verify HMAC format (64-char hex) for name fields
    </requirement>

    <requirement id="4">
      Script takes JWT token and expected tier/role as CLI arguments:
        python test_platinum_auth.py --token <JWT> --tier internal --role admin
        python test_platinum_auth.py --token <JWT> --tier partner --role advisor --advisor-id <id>
    </requirement>

    <requirement id="5">
      For each test case: hit the platinum URL via CloudFront (not direct S3),
      assert response code, check response body for scoping/pseudonymization.
      For pseudonymization: check that name fields are 64-char hex (HMAC format) vs cleartext.
    </requirement>

    <requirement id="6">
      Output: PASS/FAIL per test case (ASCII prefixes, no emojis).
      Summary: X/Y passed. Exit 0 = all pass, exit 1 = failures.
      --json flag for machine-readable output.
    </requirement>

    <requirement id="7">
      Standalone script. Uses requests library for HTTP calls.
      Must work from local machine (not EC2). Hits CloudFront URL directly.
      py_compile clean, all ASCII.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>scripts/test_platinum_auth.py -- complete auth smoke test</deliverable>
    <deliverable>Message to COO with test case inventory</deliverable>
  </deliverables>
</task_order>
