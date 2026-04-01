<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-010-de-authcontext</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-01</date>
    <status>pending</status>
    <!-- Updated 2026-04-01: scope expanded to full tier removal (not just internal rename). Andrew confirmed tier column not needed. DT .011 also removed regionId/officeId from JWT. -->
    <priority>high</priority>
    <type>feature</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Remove `tier` entirely from the portal AuthContext. `tier` is deprecated across
    the full stack -- `role` (admin/user) + `firmId` is the complete access model.
    This is a full tier removal, not just an 'internal' rename.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_P3_PRD.md -- §1 Tier Refactor, §2 Role-Only PII Gate</ref>
    <ref type="file_1">portal/src/contexts/AuthContext.context.ts -- Claims interface</ref>
    <ref type="file_2">portal/src/contexts/AuthContext.tsx -- provider, helpers, mock claims</ref>
  </references>

  <pre_verified_facts>
    COO verified state of both files before updating this TO (2026-04-01 session 9).

    AuthContext.context.ts (Claims interface):
    - Line 29: `tier: 'internal' | 'advisor' | 'client'` -- REMOVE tier field entirely
    - Lines 31-32: `regionId`/`officeId` -- also removed from JWT by DT .011; remove from Claims
    - Line 23-24: tier docstring references -- remove

    AuthContext.tsx current state:
    - Line 52-53: `regionId`/`officeId` in parseClaims interim type -- remove
    - Lines 73,75-76: parseClaims reads tier/regionId/officeId from userData -- remove
    - Line 286: mock claims `{ tier: 'internal', firmId: null, regionId: null, officeId: null, ... }`
    - Line 419: devClaims `{ tier: 'internal', firmId: null, regionId: null, officeId: null, ... }`
    - Line 441: user mock `tier: 'internal'`
    - Line 453: isInternal() `return state.claims?.tier === 'internal'`
    - Line 488: canAccessFirm() `if (state.claims.tier === 'internal') return true`
    - Line 498-499: canSeeCleartext() tier check + role check

    DT .011 already removed regionId/officeId from JWT (ec9ff6e2). Claims can drop them.
    DT .011 kept tier in JWT as vestigial -- but Andrew has confirmed tier should be
    removed entirely. Backend tier removal is a follow-on DT task (.012 or addendum to .011).
    DE removes tier from the portal side now; DT removes it from JWT/auth-handler separately.
  </pre_verified_facts>

  <requirements>

    <requirement id="1">
      Read BOTH files completely before editing:
      - portal/src/contexts/AuthContext.context.ts
      - portal/src/contexts/AuthContext.tsx
    </requirement>

    <requirement id="2">
      AuthContext.context.ts -- Claims interface: REMOVE tier, regionId, officeId entirely.

      Before:
      ```typescript
      export interface Claims {
        tier: 'internal' | 'advisor' | 'client'
        firmId: string | null
        regionId: string | null
        officeId: string | null
        userType: 'Dev' | null
      }
      ```
      After:
      ```typescript
      export interface Claims {
        firmId: string | null
        userType: 'Dev' | null
      }
      ```
      Also remove the tier/regionId/officeId docstring lines above the interface.
    </requirement>

    <requirement id="3">
      AuthContext.tsx -- parseClaims function:
      Remove tier, regionId, officeId from the mapping. These are no longer in JWT
      and not in the Claims interface. Also remove them from any intermediate type
      used within parseClaims.
    </requirement>

    <requirement id="4">
      AuthContext.tsx -- Mock claims (3 locations):
      Remove tier, regionId, officeId from all mock claims objects:
      - Line ~286: `{ tier: 'internal', firmId: null, regionId: null, officeId: null, userType: null }`
        → `{ firmId: null, userType: null }`
      - Line ~419: same shape → `{ firmId: null, userType: 'Dev' }`
      - Line ~441: object with tier field → remove tier
    </requirement>

    <requirement id="5">
      AuthContext.tsx -- isInternal():
      Before: `return state.claims?.tier === 'internal'`
      After:  `return state.claims?.firmId === 'opal-capital'`
    </requirement>

    <requirement id="6">
      AuthContext.tsx -- canAccessFirm():
      Before: `if (state.claims.tier === 'internal') return true`
      After:  `if (state.claims?.firmId === 'opal-capital') return true`
    </requirement>

    <requirement id="7">
      AuthContext.tsx -- canSeeCleartext():
      Before:
        if (state.claims?.tier === 'internal') return true
        if (state.user?.role === 'admin') return true
        return false
      After:
        return state.user?.role === 'admin'

      Role is the sole PII gate. No tier reference.
    </requirement>

    <requirement id="8">
      Search for any other tier, regionId, officeId references in BOTH files.
      Remove or replace all of them. Do not leave stale references.
    </requirement>

    <requirement id="9">
      Verify TypeScript compiles: `bunx tsc -b` from portal/ directory.
      Fix any type errors from the Claims interface change (e.g., code that was
      reading claims.tier or claims.regionId will now have TS errors -- fix those).

      Commit to portal DEV branch:
      ```
      git commit --author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>" \
          -m "feat(ADVI_ANONYM P3): remove tier/regionId/officeId from AuthContext -- role+firmId model"
      ```
      Do NOT merge to PROD. DT handles portal deploy.
      Message COO with DEV commit hash when done.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">Claims interface has NO tier, regionId, or officeId fields.</criterion>
    <criterion id="2">parseClaims does not read tier, regionId, or officeId from userData.</criterion>
    <criterion id="3">All mock claims objects contain only firmId and userType.</criterion>
    <criterion id="4">isInternal() uses firmId === 'opal-capital'.</criterion>
    <criterion id="5">canAccessFirm() uses firmId === 'opal-capital'.</criterion>
    <criterion id="6">canSeeCleartext() returns role === 'admin'. No tier reference anywhere in file.</criterion>
    <criterion id="7">bunx tsc -b passes with zero errors.</criterion>
    <criterion id="8">Committed to portal DEV branch.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Remove tier from the PORTAL side only. DT will remove tier from JWT/auth-handler backend in a separate follow-on task. Do not touch auth-handler or portal-authorizer.</constraint>
    <constraint>Commit to portal DEV branch only. DT merges to PROD after this commit.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ANONYM.007" status="complete">
      DS P3 commit a067e0fb confirmed. Backend model: firmId=opal-capital for internal,
      role is PII gate, tier=advisor for all. Portal-side cleanup can proceed.
    </dependency>
    <dependency agent="0.4.0_DT_ClientPlatform" task="ADVI_ANONYM.011" status="complete">
      DT removed regionId/officeId/allowedPages/allowedTabs from JWT (ec9ff6e2).
      Claims interface can now drop these fields without breakage.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">AuthContext.tsx updated on portal DEV branch</deliverable>
    <deliverable type="message">COO notification with DEV commit hash</deliverable>
  </deliverables>
</task_order>
