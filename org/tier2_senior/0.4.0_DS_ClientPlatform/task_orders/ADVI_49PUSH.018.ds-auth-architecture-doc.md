<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-018-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-08</date>
    <status>complete -- 0.4.0_DS_ClientPlatform~C, commit 928c4565. Doc at docs/architecture/ADVI_49PUSH_AUTH_ARCHITECTURE.md</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>4</wave>
    <phase>P5</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~B" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Write the permanent auth architecture document for Advisor Intelligence post-platinum.
    This replaces any stale auth docs from ANONYM and serves as the definitive reference
    for how auth works on every ADVI path.
  </objective>

  <context>
    PRD: docs/architecture/ADVI_49PUSH_P5_PRD.md (section: Deliverable 1 Auth Architecture Document)

    The PRD specifies exact contents: architecture diagram, RBAC tier table, pseudonymization
    rules, book scoping rules, token lifecycle, and platinum path -> auth layer mapping.

    Source material:
    - docs/architecture/ADVI_ANONYM_PRD.md (original auth design)
    - docs/architecture/ADVI_ANONYM_P3_PRD.md (P3 additions)
    - infra/aws/lambda-edge/auth-validator-edge/index.mjs (edge auth)
    - infra/aws/lambda-edge/shared-advisor-router/index.mjs (routing, just updated by .011)
    - infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py (Lambda auth)
    - portal/src/contexts/AuthContext.tsx (frontend auth)
    - portal/src/hooks/useAuth.ts (canSeeCleartext hook)
  </context>

  <compiler_tools_mandate>
    1. comp-routes auth-map
       -- complete auth layer mapping for all paths

    2. comp-routes behaviors
       -- all CloudFront behaviors

    3. comp-trace auth-validator-edge --direction both
    4. comp-trace opal-portal-authorizer --direction both
    5. comp-trace opal-partners-data --direction both
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      Location: docs/architecture/ADVI_49PUSH_AUTH_ARCHITECTURE.md
    </requirement>

    <requirement id="2">
      Contents (per P5 PRD):
      1. Architecture diagram (text-based) showing browser -> CloudFront -> edge auth ->
         S3-direct vs API GW -> authorizer -> Lambda flow
      2. RBAC tier table (4 tiers: internal admin, internal user, 49F admin, 49F advisor)
      3. Pseudonymization rules (what's hashed, what's not, HMAC key source, hash format)
      4. Book scoping rules (which routes enforce, which are direct S3)
      5. Token lifecycle (login flow, refresh, expiry, AuthContext behavior)
      6. Platinum path -> auth layer mapping table (every platinum file, which auth layers apply)
    </requirement>

    <requirement id="3">
      Read the ACTUAL code for auth-validator-edge, opal-portal-authorizer, and
      opal-partners-data to verify the auth flow. Do NOT copy from the ANONYM PRD
      without verifying -- ANONYM may not be perfectly executed.
    </requirement>

    <requirement id="4">
      The path -> auth layer mapping table must cover ALL platinum paths from .011:
      | Path | Edge Auth | API GW Auth | Lambda Scoping | Book Scoped | Pseudonymized |
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>docs/architecture/ADVI_49PUSH_AUTH_ARCHITECTURE.md</deliverable>
    <deliverable>Message to COO confirming doc complete with any auth gaps discovered</deliverable>
  </deliverables>
</task_order>
