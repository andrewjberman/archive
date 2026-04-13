<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-13-othded-001</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>complete</status>
    <!-- code landed on portal DEV 801349d 2026-04-13; AC #6 (/frontend-dev visual pass) outstanding pending submodule bump -->
    <!-- Flipped by 1.0.0_SA_CTO 2026-04-13: shipped to PROD via 4575a1c. -->

    <project_code>ADVI_OTHDED</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/DISTRIBUTION_TAB_OTHER_DEDUPE.md</ref>
    <ref type="project">org/projects/ADVI_OTHDED.json</ref>
  </references>

  <objective>
    Eliminate the dual-"Other" legend rendering in the Distribution tab Segment Analytics panel (Snapshot-GEO-AUA) by extending `enforceTop9Other` in `DistributionTab.tsx` to recognize D_01's pre-rolled `other_{state}` key as an existing-Other sentinel. Frontend-only surgical fix. Also verify and cover the ADV cohort path if D_01 emits analogous `other_{architect}` rollups.
  </objective>

  <context>
    D_01.partner_analytics._build_cities pre-rolls each state's city tail into a single synthetic entry keyed `other_{state}` (label "Other {state} Cities"). Texas example at 2026-04-13: 10 cities shipped, #10 is `other_tx` ($416M / 1,795 acct).

    `DistributionTab.tsx enforceTop9Other` (line ~189) only treats `s.key.toLowerCase() === 'other'` as an Other sentinel. `other_tx` therefore bypasses the sentinel check, enters the Top-9 sort as a regular city (landing at #1 by AUA), and then the genuine tail (e.g. `college_station_tx`) gets merged into a *second* frontend-synthesized "Other". Two "Other" slices in the legend, Top-9 + Other rule broken.

    CTO's compiler evidence (re-verified by COO at TO time):
    - `comp-blast DistributionTab.tsx`: 6 downstream nodes, endpoints `getPlatinumCumulativeChart`, `getPlatinumAdvisorNnaClients`, `getTimeseriesOverview`, all through `opal-partners-data`. Frontend-only fix does NOT cross any Lambda or gold-script boundary.
    - `comp-transform schema-check DistributionTab`: all rendered fields match response types; segments path comes from `getTimeseriesOverview` -> `partner_analytics_monthly.json`. 12/17 unused cumulative-chart fields noted but irrelevant to this fix.
    - Raw S3 inspect confirmed 10-city Texas payload with literal `other_tx` 10th element.

    Fix pattern (PRD-approved):
    ```ts
    const isOther = s.key.toLowerCase() === 'other'
      || /^other_[a-z0-9_]+$/.test(s.key.toLowerCase());
    ```
    Applied at the `enforceTop9Other` sentinel check AND at `FOLD_INTO_OTHER_KEYS` lookup if that pattern also needs to match. Normalize the synthetic key to `Other` / label `Other` on match so downstream merge collapses to a single final row.

    Rationale for frontend-only (vs deleting D_01 pre-rollup): D_01 tail rollup serves other consumers; `.029` already designates the frontend as the authoritative Top-9 enforcer. Fix at the enforcement chokepoint.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code):
    - `comp-transform schema-check DistributionTab` — confirm rendered field set is unchanged by the fix.
    - Inspect D_01 output for Texas + 2 other high-city states (e.g. Florida, California) in `s3://opal-data-bd/platinum/firm/partner_analytics_monthly.json` to confirm the `other_{state}` pattern is consistent.
    - Spot-check D_01 ADV cohort client output for analogous `other_{architect}` entries.

    Phase 2 (before committing):
    - `comp-blast DistributionTab.tsx` — confirm no new downstream impact.
    - tsc + eslint clean on portal.

    Phase 3 (after committing):
    - `/frontend-dev` visual-test pass against the Distribution tab. Drill TX, FL, CA with >=10 cities — verify exactly 10 legend entries with single final "Other" per acceptance criteria 1-5.
    - Log every compiler run to `org/compiler-tools-log.md`.

    Results (pass/fail + output summary) must appear in session log Compiler Tools section. TO is NOT accepted complete without this.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <!-- Isolated to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx. No gold script, no Lambda, no CloudFront behavior. No active ADVI TO touches this file (PROFIL closed). -->
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Snapshot-GEO-AUA > drill TX: city list has exactly 10 entries, final entry keyed `Other` with combined AUA = sum(D_01 `other_tx` + any frontend tail beyond top-9). No duplicate-label "Other" rows.
    2. Snapshot-GEO-AUA > drill any other state with >=10 cities: same guarantee.
    3. Snapshot-ADV-AUA > drill architect with >=10 clients: if D_01 emits `other_{architect}` rollup, same guarantee; if not, no change required on ADV path (document DE verification in session log).
    4. Any state with <=9 distinct cities shows at most 1 "Other" entry (either D_01-emitted or frontend-generated, not both).
    5. City percentages in the legend sum to 100% of the displayed state AUA.
    6. `/frontend-dev` visual-test pass recorded (screenshots + WCAG check).
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
    </files>
  </scope>

  <requirements>
    - Fix must be contained to `DistributionTab.tsx`. Do not modify D_01, types.ts, or any Lambda.
    - Preserve current behavior for legitimate non-Other keys.
    - If the `other_{slug}` entry carries a custom label (e.g. "Other TX Cities"), normalize the display label to `Other` so a single row renders.
    - Confirm the fix works for BOTH existing-Other-only (state with <=9 cities after D_01 rollup) and tail-overflow (state where frontend still needs to merge additional entries into Other).
  </requirements>

  <deliverables>
    - Commit to portal DEV with `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`.
    - Session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-04-13/othded_001_distribution_tab_other_dedupe.md` with Compiler Tools section.
    - Append one line per compiler run to `org/compiler-tools-log.md`.
    - Flip `<status>staged</status>` -> `pending` on GO, then -> `complete` after acceptance criteria validated.
  </deliverables>

  <do_not>
    - Do NOT modify D_01.partner_analytics.py or any gold script.
    - Do NOT widen the sentinel regex beyond `^other_[a-z0-9_]+$` (avoid collateral matches).
    - Do NOT treat this as backend-surface work. Frontend-only.
  </do_not>
</task_order>
