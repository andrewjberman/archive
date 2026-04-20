<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-15-advi-rollup-fe01</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Shipped portal DEV 7b56698 2026-04-15. RECENT_YEARS_TO_SHOW=7. frontend-dev cost_basis_panel.json PASS (Books -> Travis Penfield L2 drill, no console errors, '& Earlier' + '>= N yrs' badge verified). Optional secondary not shipped. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W3</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 3 item #11)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-15_post_presentation_master_summary.md (§11)</ref>
    <ref type="commit">ae7b377 — CostBasisByYear collapse pre-2020 into '2020 & Earlier' (baseline)</ref>
  </references>

  <objective>
    Forward-compat FE polish. Commit `ae7b377` hardcoded a 2020 year-threshold in
    `CostBasisPanel` / `CostBasisByYear` bucket logic. Hardcode silently stales on Jan 1 2027.

    Parameterize:
      - `RECENT_YEARS_TO_SHOW = N` (module constant; recommend N = 7 so current is 2026-04-15, threshold floor = 2020)
      - Derive bucket label: `"{currentYear - N} & Earlier"`
      - Derive badge text: `"≥ {currentYear - (currentYear - N)} yrs · Long"` = `"≥ N yrs · Long"`

    Secondary (optional, only if DE agrees): Short/Long badge on `currentYear` and `currentYear - 1`
    rows overstates short-term classification (those are mixed-term). DS already emits
    `short_term_gain` / `long_term_gain` as separate scalars — the badge could be dropped on recent
    years. If you ship this secondary change, note in commit.

    10-minute edit. Math remains correct — commit `ae7b377` was verified on Travis book
    (totals reconcile to `capital_gains_ttm = $60,311,016.46` to the penny).
  </objective>

  <wire_contract>
    No type change. No DS dependency. Self-contained FE refactor.
  </wire_contract>

  <acceptance_criteria>
    1. `RECENT_YEARS_TO_SHOW` module constant added; default value chosen and documented.
    2. Bucket label + badge derive from `currentYear - RECENT_YEARS_TO_SHOW`, not hardcoded 2020.
    3. Travis book `capital_gains_ttm` total still reconciles to $60,311,016.46 post-change (regression).
    4. Optional secondary (Short/Long badge drop on recent years) — if shipped, DE notes decision in commit.
    5. `comp-transform schema-check CostBasisPanel` clean (no new MISSING, no new UNUSED).
    6. `/frontend-dev` Skill invoked with `cost_basis_panel` constitution (author new if absent). PASS required.
    7. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    8. MCP COMPLETE to COO with commit hash + `/frontend-dev` PASS + regression screenshot.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check CostBasisPanel</run>
        <expect>Currently clean (no MISSING, no UNUSED). Parameterization change touches constants + label format, not type shape — schema-check stays clean post-edit.</expect>
        <if_mismatch>If MISSING exists pre-edit, surface to COO — out of scope for this TO.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>bunx tsc -b</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check CostBasisPanel</run>
        <expect>Still clean post-edit.</expect>
        <if_mismatch>Debug before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>/frontend-dev Skill with cost_basis_panel constitution</run>
        <expect>PASS — label text now reflects `{currentYear - N} & Earlier` (currently "2019 & Earlier" if N=7); badge reads "≥ 7 yrs · Long"; Travis capital_gains_ttm regression passes to $60,311,016.46.</expect>
        <if_mismatch>Iterate per Skill ACTIONABLE_FIXES protocol up to 5 rounds.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None.
  </dependencies>

  <next>
    On commit + `/frontend-dev` PASS: DT batches into next portal push. Signal COO.
  </next>
</task_order>
