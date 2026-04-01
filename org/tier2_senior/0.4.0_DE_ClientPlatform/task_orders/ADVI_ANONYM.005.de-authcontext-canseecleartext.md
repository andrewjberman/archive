<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-005-de-authcontext</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>pending</status>
    <priority>high</priority>
    <type>feature</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Add a `canSeeCleartext()` boolean helper to AuthContext. This is the single
    frontend gating function that RD components call to decide whether to show
    pseudonymization indicators. Small change, high leverage.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_PRD.md -- Phase 2: Frontend Graduated UI</ref>
    <ref type="file">portal/src/contexts/AuthContext.tsx</ref>
    <ref type="rd_to">ADVI_ANONYM.006.rd-pseudonymized-ui-indicators.md (depends on this helper)</ref>
  </references>

  <background>
    ADVI_ANONYM P1 deployed pseudonymization at the serving layer (Lambda). advisor/user
    tier now receives hashed client names from the API. Phase 2 adds frontend indicators
    so users know they are seeing pseudonymized data (not real names).

    The role matrix:
    - tier=internal, any role   -> canSeeCleartext() = true  (internal users see real data)
    - tier=advisor, role=admin  -> canSeeCleartext() = true  (advisor admins see real data)
    - tier=advisor, role=user   -> canSeeCleartext() = false (see hashed names + indicators)
    - any other combination     -> canSeeCleartext() = false (safe default)
  </background>

  <requirements>

    <requirement id="1">
      Read portal/src/contexts/AuthContext.tsx completely before editing.
      Understand the existing context shape -- specifically where `tier` and `role`
      are stored and how they are typed.
    </requirement>

    <requirement id="2">
      Add `canSeeCleartext()` as a method or derived boolean on the AuthContext value:

      ```typescript
      canSeeCleartext: () => boolean
      ```

      Implementation:
      ```typescript
      const canSeeCleartext = (): boolean => {
        if (tier === 'internal') return true;
        if (role === 'admin') return true;
        return false;
      };
      ```

      Where `tier` and `role` are the current user's values from context.
      Export the helper as part of the context value so RD components can call
      `const { canSeeCleartext } = useAuthContext()` (or equivalent hook).
    </requirement>

    <requirement id="3">
      Ensure the TypeScript interface / type for the AuthContext value includes
      `canSeeCleartext: () => boolean`. If there is a separate interface definition
      for the context shape, add it there.
    </requirement>

    <requirement id="4">
      Commit on DEV branch (portal submodule) with author attribution:
      ```
      git commit --author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>" \
          -m "feat(ADVI_ANONYM P2): add canSeeCleartext() helper to AuthContext"
      ```
      Do NOT merge to PROD. DT handles the DEV -> PROD merge after RD completes .006.
    </requirement>

    <requirement id="5">
      Write a brief session log:
      org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-04-01/advi_anonym_p2_authcontext.md
    </requirement>

    <requirement id="6">
      Message COO (2.0.0_SA_COO) when committed. Include the DEV commit hash.
      RD (.006) is waiting on this helper -- message promptly.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">canSeeCleartext() exported from AuthContext (usable via useAuthContext hook or equivalent).</criterion>
    <criterion id="2">Returns true for tier=internal (any role).</criterion>
    <criterion id="3">Returns true for role=admin (any tier).</criterion>
    <criterion id="4">Returns false for tier=advisor + role=user.</criterion>
    <criterion id="5">Returns false for any unknown tier/role (safe default).</criterion>
    <criterion id="6">TypeScript compiles clean (bunx tsc -b passes).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Change is additive only -- do not modify existing AuthContext behavior.</constraint>
    <constraint>Commit to portal DEV branch (submodule), not CLOUD parent repo.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="ADVI_ANONYM_P1_verification" status="complete">
      P1 fully deployed (partners-api-v1.11.0, auth-validator-edge v9). advisor/user
      receives hashed names from API as of 2026-04-01.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">AuthContext.tsx with canSeeCleartext() on portal DEV branch</deliverable>
    <deliverable type="message">COO notification with DEV commit hash</deliverable>
  </deliverables>
</task_order>
