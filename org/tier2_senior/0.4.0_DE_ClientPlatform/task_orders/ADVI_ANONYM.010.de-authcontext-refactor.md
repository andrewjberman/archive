<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-010-de-authcontext</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>staged</status>
    <!-- STAGED: activate after DS .007 commits. DE can work in parallel with DS but
         needs to know the final firmId/role model before finalizing. -->
    <priority>high</priority>
    <type>feature</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Update portal/src/contexts/AuthContext.tsx to remove tier=internal checks and
    align canSeeCleartext() with the new role-only PII gate. Four targeted edits.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_P3_PRD.md -- §1 Tier Refactor, §2 Role-Only PII Gate</ref>
    <ref type="file">portal/src/contexts/AuthContext.tsx</ref>
  </references>

  <pre_verified_facts>
    COO verified all line numbers before issuing this TO.

    AuthContext.tsx current state (confirmed by read):
    - Line 286: mock claims fallback `{ tier: 'internal', firmId: null, ... }`
    - Line 419: devBypass mock `{ tier: 'internal', ... }`
    - Line 441: devBypass user mock `tier: 'internal'`
    - Line 452-453: isInternal() -- `return state.claims?.tier === 'internal'`
    - Line 488: canAccessFirm() -- `if (state.claims.tier === 'internal') return true`
    - Line 498-499: canSeeCleartext() -- `if (state.claims?.tier === 'internal') return true`
                                          `if (state.user?.role === 'admin') return true`
  </pre_verified_facts>

  <requirements>

    <requirement id="1">
      Read portal/src/contexts/AuthContext.tsx completely before editing.
      Confirm line numbers match the pre-verified facts above (they may have shifted
      slightly since COO read the file).
    </requirement>

    <requirement id="2">
      isInternal() -- line ~453:
      Before: `return state.claims?.tier === 'internal'`
      After:  `return state.claims?.firmId === 'opal-capital'`
    </requirement>

    <requirement id="3">
      canAccessFirm() -- line ~488:
      Before: `if (state.claims.tier === 'internal') return true`
      After:  `if (state.claims.firmId === 'opal-capital') return true`
    </requirement>

    <requirement id="4">
      canSeeCleartext() -- lines ~498-499:
      Before:
        if (state.claims?.tier === 'internal') return true
        if (state.user?.role === 'admin') return true
        return false
      After:
        // role is the sole PII gate -- admin sees cleartext, user sees hashed
        return state.user?.role === 'admin'

      Remove the tier check entirely. One return statement.
    </requirement>

    <requirement id="5">
      Mock claims -- three locations (lines ~286, ~419, ~441):
      Change `tier: 'internal'` to `tier: 'advisor'` in all three.
      These are dev/fallback mock values; updating them prevents the dev bypass
      from granting cleartext to advisor/user mock accounts.
    </requirement>

    <requirement id="6">
      Verify TypeScript compiles: `bunx tsc -b` from portal/ directory.
      (`/c/Users/AndrewBerman/.bun/bin/bun x tsc -b` if bun not in PATH)

      Commit to portal DEV branch:
      ```
      git commit --author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>" \
          -m "feat(ADVI_ANONYM P3): AuthContext tier refactor -- isInternal=firmId, canSeeCleartext=role-only"
      ```
      Do NOT merge to PROD. DT handles portal deploy.

      Message COO with DEV commit hash when done.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">isInternal() returns true for firmId=opal-capital, false otherwise.</criterion>
    <criterion id="2">canAccessFirm() grants access to all firms when firmId=opal-capital.</criterion>
    <criterion id="3">canSeeCleartext() returns role === 'admin' only. No tier check.</criterion>
    <criterion id="4">All three mock claims use tier: 'advisor'.</criterion>
    <criterion id="5">bunx tsc -b passes.</criterion>
    <criterion id="6">Committed to portal DEV branch.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Additive changes only -- do not restructure AuthContext or change any logic beyond the four requirements above.</constraint>
    <constraint>Commit to portal DEV branch only. DT merges to PROD after Lambda deploy.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ANONYM.007" status="pending">
      DE can work in parallel. STAGED until DS commits .007 to confirm no surprises
      in the backend model that would affect the frontend logic.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">AuthContext.tsx updated on portal DEV branch</deliverable>
    <deliverable type="message">COO notification with DEV commit hash</deliverable>
  </deliverables>
</task_order>
