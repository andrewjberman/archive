<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-017-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>4</wave>
    <phase>P5</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~C" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Write the CI gold/ path ban script that prevents ADVI portal code from referencing
    gold/ paths. This is the structural enforcement that makes platinum migration
    irreversible after P3 validation.
  </objective>

  <context>
    PRD: docs/architecture/ADVI_49PUSH_P5_PRD.md (section: Deliverable 2 CI Gold Path Ban)

    The PRD has a reference implementation. Adapt it to work in this repo.
    Only ADVI code is checked -- other pages still use gold/ via other pipelines.
  </context>

  <requirements>
    <requirement id="1">
      Location: scripts/ci/check-no-gold-paths.sh
    </requirement>

    <requirement id="2">
      Check these locations for gold/ references:
      - portal/src/pages/AdvisorIntelligence/ (all .ts/.tsx files)
      - portal/src/api/endpoints/advisor-intelligence.ts
      - infra/aws/lambda-edge/shared-advisor-router/index.mjs (ADVI routes only)
      - infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py (ADVI routes only)
    </requirement>

    <requirement id="3">
      Allow escape hatch: lines containing "// LEGACY:" or "# LEGACY:" are excluded.
      This lets us document historical paths without triggering the check.
    </requirement>

    <requirement id="4">
      For opal-partners-data, only flag ADVI-related gold/ references. Non-ADVI routes
      may legitimately read gold/. Use WARNING not ERROR for this file.
    </requirement>

    <requirement id="5">
      Exit 0 = clean, exit 1 = gold/ references found.
      Print file:line for each violation.
      Script must work in Git Bash on Windows.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>scripts/ci/check-no-gold-paths.sh -- CI enforcement script</deliverable>
    <deliverable>Message to COO confirming script passes on current codebase state</deliverable>
  </deliverables>
</task_order>
