<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-13-reborn-w6-002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>pending</status>
    <!-- code landed portal DEV bf475f8 2026-04-13; 3-of-4 audit cells match, the 4th hits 365.55M vs TO's <=341M expectation — flagged for DS revalidation in the session log -->

    <project_code>ADVI_REBORN</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_LEADERBOARD_FEES_ROLES_FIX.md</ref>
    <ref type="project">org/projects/ADVI_REBORN.json</ref>
  </references>

  <dependencies>
    <dependency task="ADVI_REBORN.W6-001" status="pending"/>
  </dependencies>

  <objective>
    Wave 6-002 DE. Remove the `(data[feeView] ?? data)` silent fallback in AdvisorsTab leaderboard role math. Consume the per-role nested `fee_paying` and `no_fee` buckets shipped by W6-001. Fail closed when a required bucket is missing. Validate with Andrew's Travis Penfield four-cell audit matrix.
  </objective>

  <context>
    Bug: `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` computes:
    ```ts
    const bucket = feeView === 'all' ? data : (data[feeView] ?? data);
    ```
    When `data[feeView]` is missing (which was the case before W6-001 shipped), it silently falls back to the all-fee slice — the observed bug where Fees=Fee-Paying + Implementor-off returns the Fees=All-minus-Implementor value.

    After W6-001 ships, `platinum/firm/leaderboard.json` exposes `role_breakdown[role].fee_paying` and `.no_fee`. Frontend must:
    1. Sum only from `role_breakdown[role][feeView]` when `feeView !== 'all'`.
    2. Fail closed if a required nested bucket is absent (log + show error state; do NOT fall back silently).
    3. Mirror defensive behavior anywhere else this leaderboard role math is reused.

    Compiler pre-check (COO): `comp-blast AdvisorsTab.tsx` = 1 downstream (`getFirmLeaderboard`). Frontend-only scope.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code):
    - `comp-transform schema-check AdvisorsTab` — confirm type set.
    - Read DS-shipped `platinum/firm/leaderboard.json` sample (Travis Penfield or equivalent) to confirm nested bucket names + shape.

    Phase 2 (before committing):
    - Re-run `comp-transform schema-check AdvisorsTab` — no prop-shape regression.
    - Grep `?? data` across the file — confirm no silent fallback remains.
    - tsc + lint clean.

    Phase 3 (after committing):
    - Validate Andrew's four-cell audit matrix in the UI with Travis Penfield data:
      - Fees=All + all roles -> 427M
      - Fees=All + Implementor off -> 394M
      - Fees=Fee-Paying + all roles -> 341M
      - Fees=Fee-Paying + Implementor off -> <= 341M (the broken cell that must now be correct)
    - Run `/frontend-dev` closed-loop pass if the change lands in portal DEV during the same session.
    - Append compiler runs to `org/compiler-tools-log.md`.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</shared_resource>
    <shared_resource>platinum/firm/leaderboard.json</shared_resource>
    <also_in_to>ADVI_REBORN.W6-001 (DS — produces this artifact)</also_in_to>
    <last_write_owner>0.4.0_DE_ClientPlatform (this TO)</last_write_owner>
    <required_action>Wait for MCP signal from DS confirming W6-001 shipped + validated in S3 before starting. Pull latest DEV before writing to avoid conflict with HDRSPL.002/.003 (different surface but same pod).</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. The four-cell audit matrix (Travis Penfield) returns the expected values; the broken cell (Fees=Fee-Paying + Implementor off) returns <=341M, not 394M.
    2. For every `(feeView, selectedRoles)` combination, displayed AUA is the intersection of those filters.
    3. No code path silently falls back from `fee_paying` or `no_fee` to all-role totals (`?? data` removed).
    4. Missing nested bucket triggers an explicit error/log path, not a silent incorrect number.
    5. No TypeScript errors, no ESLint errors, no new console warnings.
    6. `/frontend-dev` visual-test pass recorded if change lands on DEV same session.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    - Do not modify D_04 or any gold script (W6-001 scope).
    - Do not hard-code against a specific role list; drive off the `role_breakdown` keys shipped in the artifact.
    - Update TypeScript types if the `PlatinumFirmLeaderboard` shape now carries nested `fee_paying` / `no_fee` — keep types aligned.
  </requirements>

  <deliverables>
    - Commit to portal DEV with `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`.
    - Session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-04-13/reborn_w6_002_advisors_tab_fee_fallback.md` with Compiler Tools section + four-cell audit result.
    - `org/compiler-tools-log.md` entries.
    - Flip `<status>` staged -> pending on DS ship signal, then -> complete after acceptance criteria 1-6.
  </deliverables>

  <do_not>
    - Do NOT ship before W6-001 artifact lands on S3 (the fix depends on new bucket presence).
    - Do NOT re-introduce `?? data` or any analogous silent fallback.
    - Do NOT modify other tabs' filter logic unless they share the same bucket-access pattern; flag them in the session log if found.
  </do_not>
</task_order>
