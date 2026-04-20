<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-15-advi-rollup-b9-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Shipped portal DEV a2d8f83 2026-04-15. types.ts FeeEfficiencyAdvisor.small_account_count required. FeeEfficiencyPanel column 'Small Accts (<$40k)' between NNA + Efficiency (account_count column doesn't exist on this table -- placed near other count metrics). frontend-dev fee_efficiency_panel.json PASS first iter. tsc + schema-check clean. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W3</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP_ADDENDUM_small_account_count.md</ref>
    <ref type="companion">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_ROLLUP.B9.ds-small-account-count-c08.md (DS side, ships first)</ref>
  </references>

  <objective>
    Paired FE for DS B9. Two edits, ~20 minutes total:

    1. **Type:** `portal/src/pages/AdvisorIntelligence/types.ts` (~line 1540) — add
       `small_account_count: number` to `FeeEfficiencyAdvisor` interface (required field, not optional).

    2. **Column:** `portal/src/pages/AdvisorIntelligence/tabs/FeeEfficiencyPanel.tsx` — add a new
       column immediately to the right of the existing `account_count` column.
       - Header label: `Small Accts (<$40k)`
       - Sortable, same pattern as other numeric columns
       - Tooltip: "Accounts under $40,000 AUA the advisor is attached to in any role."
       - No new filter, no new toggle, no role-scoping.

    Threshold literal in the label is acceptable (matches DS constant). If DS parameterizes later,
    label tracks via a shared helper.

    Ordering: DS ships first. This TO flips pending when the DEV artifact carries `small_account_count`.
  </objective>

  <wire_contract>
    TypeScript interface adds one required field:
    ```ts
    export interface FeeEfficiencyAdvisor {
      advisor: string
      roles: string[]
      account_count: number
      small_account_count: number  // NEW
      aua?: number
      ...
    }
    ```

    Column renders as `advisor.small_account_count` with `toLocaleString()`. Never null (DS guarantees
    default 0).
  </wire_contract>

  <acceptance_criteria>
    1. TypeScript compiles: `bunx tsc -b` exits 0.
    2. `comp-transform schema-check FeeEfficiencyPanel` clean (no MISSING, no new UNUSED).
    3. New column renders on AdvisorIntelligence Fee Efficiency table; header label `Small Accts (<$40k)`.
    4. Tooltip matches wire contract text.
    5. Sort ascending/descending works consistently with other numeric columns.
    6. `/frontend-dev` Skill invoked with `fee_efficiency_panel` constitution (author a new one under
       `portal/.frontend-dev/testing/` if absent, per schema in that folder's README). PASS required
       before flip to complete.
    7. Manual DEV spot-check: advisor known to have low-balance accounts (Travis Cobb) shows non-zero value.
    8. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    9. MCP COMPLETE to COO with portal DEV commit hash + `/frontend-dev` PASS confirmation.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check FeeEfficiencyPanel</run>
        <expect>All fields currently match; no MISSING. No new UNUSED. Addendum §Compiler Tools confirms this was clean at addendum time — adding `small_account_count` as required sibling of `account_count` will not introduce MISSING once DS artifact carries it.</expect>
        <if_mismatch>If pre-existing MISSING appears, surface to COO — not our scope to fix, may indicate upstream DS drift.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>bunx tsc -b</run>
        <expect>Exit 0. No new type errors introduced.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check FeeEfficiencyPanel</run>
        <expect>Clean after edit; `small_account_count` now in rendered set; no new MISSING.</expect>
        <if_mismatch>Debug type wiring; do not commit until clean.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>/frontend-dev Skill with fee_efficiency_panel constitution</run>
        <expect>PASS on all acceptance checks (column renders, tooltip visible, sort works, Travis row non-zero).</expect>
        <if_mismatch>Parse ACTIONABLE_FIXES from output, iterate Edit → re-test up to 5 times per Skill protocol, then escalate to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.B9.ds-small-account-count-c08" status="pending" description="artifact must carry `small_account_count` in DEV before FE merge"/>
  </dependencies>

  <next>
    On commit + `/frontend-dev` PASS: DT push to PROD in next batched bump. Signal COO.
  </next>
</task_order>
