<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-09-49push-022-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>HOTFIX</wave>
    <phase>P4</phase>
  </metadata>

  <objective>
    EMERGENCY: Auth refresh returning 401. Trace the frontend side in parallel with DT's
    backend investigation (.021).

    Error: AuthContext.tsx:93 POST /auth/refresh -> 401
    Andrew is logged in as Opal admin on opalinvest.dev.
  </objective>

  <context>
    Portal was just deployed to DEV with platinum wiring changes (.012/.013/.014).
    Auth refresh is core infrastructure -- it should not have been affected by ADVI
    platinum changes. But the deploy included 5 TS build fixes (committed d8b6c3b)
    which may have touched shared code.
  </context>

  <compiler_tools_mandate>
    1. comp-transform trace AuthContext
       -- trace the auth refresh data flow in the frontend

    2. comp-routes trace auth/refresh
       -- full serving chain

    3. comp-cache map
       -- check if any React Query cache key collision affects auth
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      Read AuthContext.tsx line 93 and the surrounding refresh logic.
      - What URL is it POSTing to?
      - What headers/cookies does it send?
      - Did any of the .012/.013/.014 changes or the TS build fixes touch AuthContext?
    </requirement>

    <requirement id="2">
      Check git diff on AuthContext.tsx and any auth-related files:
      git diff HEAD~6 -- portal/src/contexts/AuthContext.tsx
      git diff HEAD~6 -- portal/src/hooks/useAuth.ts
      If these files are unchanged, the issue is backend (DT's .021).
    </requirement>

    <requirement id="3">
      Check if the portal build removed or changed any auth-related code:
      - Was @/api/endpoints/auth.ts modified?
      - Were any imports changed that affect the auth flow?
    </requirement>

    <requirement id="4">
      Report findings to COO immediately. If frontend is clean, this is a backend issue
      and DT (.021) owns the fix.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>Frontend auth trace: changed or unchanged</deliverable>
    <deliverable>Message to COO with finding</deliverable>
  </deliverables>
</task_order>
