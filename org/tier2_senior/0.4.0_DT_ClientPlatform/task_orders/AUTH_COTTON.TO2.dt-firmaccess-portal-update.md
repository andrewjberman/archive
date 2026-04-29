<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>AUTH_COTTON.TO2</id>
    <project>AUTH_COTTON</project>
    <title>Portal firmAccess.ts — add Cottonwood allowlist + push to PROD</title>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>pending</status>
    <priority>high</priority>
    <estimated_effort>1-2h</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/AUTH_COTTON.md</ref>
    <ref type="prd_section">§4.5 + §6 TO-2</ref>
    <ref type="target_file">portal/src/lib/firmAccess.ts</ref>
    <ref type="verify_file">portal/src/App.tsx (route declarations — verify path strings)</ref>
    <ref type="q1_assumption">Email domain = cottonwood.com (PRD default; trivial to amend if Andrew corrects)</ref>
    <ref type="q5_assumption">Display name = Cottonwood (PRD default; for FIRM_EMAIL_DOMAINS key only — name field is in TO-3)</ref>
  </references>

  <context>
    firmAccess.ts is the single-file canonical allowlist governing which routes each
    partner firm can access. Current state has only '49financial' and 'inflection'.
    Cottonwood gets 11 ALLOW / 3 DENY (no /advisor-intelligence, /portfolio-management,
    /data-refresh per Andrew spec).

    The /market path MUST be in the set (it is the FIRM_DEFAULT_LANDING for all firms).
    All 11 path strings must exactly match &lt;Route path="..."&gt; declarations in App.tsx.

    Parallelizable with TO-1 (Terraform). No dependency on TO-1 for the portal source
    edit itself. Visual smoke (acceptance criterion 3) benefits from having TO-3 live,
    but bun typecheck passes without it.

    PRD §2.3 verified all 11 paths exist in App.tsx. This TO includes a re-verification.
  </context>

  <scope>
    EDIT portal/src/lib/firmAccess.ts:

    In FIRM_ALLOWED_PATHS, add after 'inflection' entry:
    ```ts
    'cottonwood': new Set([
      '/market',
      '/portfolios',
      '/cma',
      '/positioning',
      '/attribution',
      '/factor-tilts',
      '/valuations',
      '/correlations',
      '/macro',
      '/security-scanner',
      '/trade-submission',
    ]),
    ```

    In FIRM_EMAIL_DOMAINS, add after 'inflection' entry:
    ```ts
    'cottonwood': 'cottonwood.com',
    ```

    IMPORTANT: No other changes. Do not touch 49financial or inflection entries.
    Do not add cottonwood to FIRM_BUCKET_MAP in lambda-edge files — cottonwood
    is intentionally absent from that map (structural deny for ADVI routes per PRD §2.5).

    After edit:
    1. bun run typecheck (must PASS — exit 0)
    2. git commit to portal submodule (DEV branch)
    3. Fast-forward portal PROD from DEV
    4. Push portal pointer bump in workspace repo
    5. Tag portal-v{N+1} per portal tag sequence
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Read portal/src/App.tsx — scan Route declarations for all 11 paths</run>
        <expect>Exact path strings present:
        /market, /portfolios, /cma, /positioning, /attribution, /factor-tilts,
        /valuations, /correlations, /macro, /security-scanner, /trade-submission
        All 11 must appear verbatim. Case-sensitive check.</expect>
        <if_mismatch>STOP. If any path differs (e.g. /factor_tilts vs /factor-tilts),
        use the App.tsx exact string — do NOT use the PRD string. Surface discrepancy
        in session log.</if_mismatch>
      </step>
      <step>
        <run>Read portal/src/lib/firmAccess.ts (current state)</run>
        <expect>FIRM_ALLOWED_PATHS has '49financial' and 'inflection' entries only.
        FIRM_EMAIL_DOMAINS has '49financial' and 'inflection' entries only.
        No cottonwood entry present yet.</expect>
        <if_mismatch>If cottonwood already present (from a prior partial attempt),
        verify the existing entry matches the spec exactly. Report to COO before proceeding.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before portal commit">
      <step>
        <run>/c/Users/AndrewBerman/.bun/bin/bun run typecheck (in portal/ directory)</run>
        <expect>Exit 0. No TypeScript errors. firmAccess.ts type changes are additive
        (new Record entries) — should typecheck cleanly.</expect>
        <if_mismatch>STOP. Fix TypeScript errors before committing. Do not push
        a typecheck-failing portal build.</if_mismatch>
      </step>
      <step>
        <run>git diff portal/src/lib/firmAccess.ts</run>
        <expect>Diff shows exactly 2 additions: cottonwood Set (11 paths) and
        'cottonwood': 'cottonwood.com' domain entry. No deletions. No other files changed
        in portal/src/.</expect>
        <if_mismatch>STOP. Extra changes swept in — clean the index before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after portal push to PROD">
      <step>
        <run>Visual check: bun run dev -- login as internal user, navigate to /market;
        inspect firmAccess.ts in source to confirm cottonwood entry present.</run>
        <expect>Portal builds and runs without errors. cottonwood entry visible in source.</expect>
        <if_mismatch>Check bun build errors; ensure portal submodule PROD pointer updated.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      git diff portal/src/lib/firmAccess.ts shows exactly 2 insertions (the 11-path Set
      and the domain entry). No other portal source changed.
      Evidence: diff in session log.
    </criterion>
    <criterion id="2">
      bun run typecheck PASS (exit 0). Evidence: command output in session log.
    </criterion>
    <criterion id="3">
      portal-v{X.Y.Z+1} tag pushed to portal submodule origin.
      Evidence: git tag output in session log.
    </criterion>
    <criterion id="4">
      Workspace portal pointer bump committed and pushed to CLOUD.
      Evidence: commit hash in session log.
    </criterion>
    <criterion id="5">
      RAVC to 2.0.0_SA_COO with: portal commit hash, typecheck output, tag name.
      Include explicit note that portal is PROD-ready for Cottonwood route guard.
    </criterion>
    <criterion id="6">
      Session log includes Compiler Tools section reproducing all phase mandates
      with observed output and explicit pass/fail vs expect.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="AUTH_COTTON.TO1" status="parallelizable">
      Portal source edit requires no Terraform prerequisite. Run in parallel with TO-1.
      Visual smoke test (AC phase 3) benefits from TO-3 live user, but typecheck
      and portal push do not gate on TO-3.
    </dependency>
  </dependencies>

  <cross_domain_coordination>
    <none/>
    firmAccess.ts last touched in ADVI_INFLEC W1.4 (2026-04-21, complete). No active
    project touches this file concurrently.
  </cross_domain_coordination>

  <commit_identity>
    Portal submodule commit (DEV branch):
      git commit --author "0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
        -m "feat(AUTH_COTTON.TO2): add Cottonwood to firmAccess.ts allowlist (11 paths)"

    Workspace pointer bump:
    .tools/safe-commit.sh --author "0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
      -m "feat(AUTH_COTTON.TO2): bump portal pointer — Cottonwood allowlist" \
      -- portal
  </commit_identity>

  <notes>
    Bun path: /c/Users/AndrewBerman/.bun/bin/bun
    Portal lives at portal/ — must be on DEV branch for portal commits.
    After DEV commit: git checkout PROD in portal/ and git merge DEV --ff-only.
    Then workspace pointer bump commit.
    Do NOT add cottonwood to lambda-edge FIRM_BUCKET_MAP — intentional omission per PRD §2.5.
    cottonwood.com domain assumption from PRD Q1 default; Andrew may correct.
  </notes>
</task_order>
