<task_order>
  <metadata>
    <id>SSCN_DIVDEF.010</id>
    <slug>de-rd-factor-bank-group-ordering</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <implementation_lane>0.3.4_RD</implementation_lane>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 -- decomposition of PRD v0.6 §6.9 TO-8. Gates met: PARALLEL with SSCN_DIVDEF.009 (categoryOrder.ts needs only the known 18-group master list, NOT .009's regenerated registry output). No upstream dependency.</dispatch_unblock_condition>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct "focus SSCN today" 2026-05-20 (v0.6 factor-grouping correction). ~30-45min combined DE+RD wall.</priority>
    <sla>~30-45min wall once GO lands. PARALLEL with .009.</sla>
    <deadline>None -- ship at DE/RD pace; gates the bundled TO-4/.006 PROD push.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md -- PRD v0.6 (commit 2e9fe7f3a, 1.0.0_SA_CTO, 2026-05-20). This TO is the literal decomposition of PRD v0.6 §6.9 "TO-8". Read the full v0.6 Amendment block: §A (the defect -- 176/282 factors mis-grouped), §B (correction of v0.4 §B -- the grouping IS defective), §C (the 3-surface fix), §D (scope decisions), §6.9 (TO-7/TO-8 spec).</prd>
    <directive>Andrew-direct 2026-05-20: the Security Scanner factor groups are wrong -- "Yield" and "Systematic" are not real factor groups. Andrew supplied the canonical master list (Signal Summary.xlsx) defining 18 groups. CTO empirically confirmed: the bundled registry uses a wrong collapsed 11-category taxonomy; 176 of 282 factors mis-grouped. This TO is the portal-side surface of the 3-surface fix (§C).</directive>
    <companion_to>SSCN_DIVDEF.009 (TO-7) regenerates factor_metadata_registry.json category field + redeploys the scanner Lambda so latest/factor_metadata.json emits the 18 correct groups. .009 and this TO run PARALLEL -- categoryOrder.ts needs only the known 18-group list (below), not .009's output. The two converge at the bundled .006 PROD push.</companion_to>
    <implementation_model>0.3.0_DE_TradingOperations is PM/owner; 0.3.4_RD builds the FE under DE coordination. DE authors the design spec, dispatches RD, reviews the implementation, runs the compiler mandate, owns the RAVC2.</implementation_model>
  </references>

  <context>
    The Factor Bank tab (`portal/src/pages/SecurityScanner/tabs/FactorBankTab.tsx`) displays each factor's group, ordered + colored via `utils/categoryOrder.ts`. Today `categoryOrder.ts` encodes the WRONG collapsed 11-category taxonomy (efficiency, growth, institutional, management, profitability, quality, sentiment, size, systematic, value, yield). PRD v0.6 corrects the taxonomy to the 18 canonical master groups. This TO updates the portal display layer to the 18-group taxonomy.

    The 18 canonical master groups (PRD v0.6 §A, from Signal Summary.xlsx sheet Python_SN_New):
    analyst, beta, crowding, efficiency, governance, growth, insider, liquidity, management, momentum, profitability, quality, short, size, solvency, technical, value, volatility.

    This is the portal DISPLAY surface. The DATA correction (registry `category` values + Lambda re-emit) is SSCN_DIVDEF.009's scope -- once .009 ships, `latest/factor_metadata.json` emits factors tagged with these 18 group values; this TO ensures the Factor Bank renders all 18 in a defined order + color rather than dropping unknown groups to the default gray.
  </context>

  <scope>
    <step>Phase 1 (before write) -- baseline. Run the Phase 1 compiler baseline (see &lt;compiler_tools_mandate&gt;). DE coordinates 0.3.4_RD; read PRD v0.6 §C item 3 + §6.9 TO-8.</step>
    <step>Phase 2 (implement) -- DE coordinates 0.3.4_RD on the edits per PRD §6.9 TO-8:
      - `utils/categoryOrder.ts` -- `CANONICAL_CATEGORY_ORDER`: replace the 11-category list with the 18 master groups. DE picks the canonical display order -- alphabetical is acceptable, or a thesis-grouped order (DE's call; document the choice in the commit message). `CATEGORY_COLORS` -- extend to 18 distinct, visually-separable entries (no two groups sharing a color; no group falling through to a default gray).
      - `tabs/FactorBankTab.tsx` -- relabel the "Category" column header to "Group". The category-filter dropdown auto-derives its options from the data (`allFactors.forEach(f => seen.add(f.category))`) -- NO change needed there; do not touch the filter logic.
    </step>
    <step>Phase 3 (verify + commit) -- run the Phase 2 + Phase 3 compiler mandate. DE reviews the RD implementation against all 3 ACs. Commit via `.tools/safe-commit.sh` (DE author, or RD serial if RD commits its own page -- DE's call; RAVC2 is DE's). Portal DEV push is a DT lane action -- CC DT 0.3.0 if a push is needed.</step>
    <step>Phase 4 (RAVC2) -- to 2.0.0_SA_COO + CC 1.0.0_SA_CTO with AC1-AC3 evidence + commit SHA(s) + compiler transcript. TO status -> complete on RAVC2 send.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">The Factor Bank tab renders all 18 master groups, each with a defined order position AND a distinct color. No group falls through to the default gray / unknown-group styling. Verified by loading the Factor Bank with data tagged across all 18 groups (or by inspecting that CANONICAL_CATEGORY_ORDER + CATEGORY_COLORS both enumerate exactly the 18 master groups).</ac>
    <ac id="AC2">No user-facing "Category" label remains on the Factor Bank tab -- the column header reads "Group". The filter-dropdown logic is unchanged (it auto-derives from data).</ac>
    <ac id="AC3">`/frontend-dev` smoke green; `bun run typecheck` (tsc) clean and `bun run lint` clean. Transcript captured.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check FactorBankTab</run>
        <expect>Baseline rendered-field set captured. Record any MISSING / NOTE / UNUSED -- pre-change reference for the Phase 3 re-run.</expect>
        <if_mismatch>If MISSING fields exist pre-change, note them as pre-existing so the Phase 3 comparison is not polluted; not a blocker for starting.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bun run typecheck</run>
        <expect>tsc exits clean (0 errors). The CANONICAL_CATEGORY_ORDER + CATEGORY_COLORS changes must type-check.</expect>
        <if_mismatch>Any TS error = fix before commit.</if_mismatch>
      </step>
      <step>
        <run>bun run lint</run>
        <expect>lint exits clean.</expect>
        <if_mismatch>Any lint error = fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-transform schema-check FactorBankTab</run>
        <expect>No MISSING fields post-change vs the Phase 1 baseline.</expect>
        <if_mismatch>A MISSING field = runtime undefined. Fix before RAVC2.</if_mismatch>
      </step>
      <step>
        <run>/frontend-dev smoke</run>
        <expect>Smoke green; Factor Bank tab renders the 18 groups ordered + colored, "Group" column header.</expect>
        <if_mismatch>Iterate until the 18-group render + relabel are clean.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    PARALLEL with SSCN_DIVDEF.009 (AE registry regen + Lambda redeploy). No shared files -- .009 touches infra/aws/lambda/opal_security_scanner_processor/** + the registry; this TO touches portal/src/pages/SecurityScanner/utils/categoryOrder.ts + tabs/FactorBankTab.tsx. Both reference the SAME 18-group master taxonomy (PRD v0.6 §A) -- categoryOrder.ts hardcodes the 18-group order/colors from the known master list, NOT from .009's regenerated registry, so there is no producer/consumer ordering dependency. Both gate the bundled TO-4/.006 PROD push. No overlap with the closed .001-.008 TOs.
  </cross_domain_coordination>

  <deliverables>
    - categoryOrder.ts (18-group CANONICAL_CATEGORY_ORDER + CATEGORY_COLORS) + FactorBankTab.tsx ("Group" relabel) on portal DEV.
    - Session log under org/tier2_senior/0.3.0_DE_TradingOperations/logs/YYYY-MM-DD/ with AC1-AC3 evidence + commit SHA(s) + Compiler Tools section reproducing each &lt;run&gt; + observed result vs &lt;expect&gt;.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO on close; TO status -> complete on RAVC2 send.
  </deliverables>

  <do_not>
    <rule>Do NOT change the internal field name `category` -- per PRD v0.6 §D the field stays `category` internally (rename = cross-cutting churn); only the user-facing column label changes to "Group" and the VALUES are corrected (the values come from .009's registry regen, not this TO).</rule>
    <rule>Do NOT touch the category-filter dropdown logic -- it auto-derives options from the data; it picks up the 18 groups for free once .009's data lands.</rule>
    <rule>Do NOT modify the DIVZ preset's `group` field (PresetEntry.group -- Dividend/Momentum/Value/Quality). Per PRD v0.6 §D the preset-thesis group is legitimately distinct from a factor's intrinsic master group and is UNTOUCHED.</rule>
    <rule>Do NOT push portal DEV -> PROD. The PROD push is the bundled TO-4/.006 DT lane, gated on .009 + .010 close + Andrew DEV smoke.</rule>
    <rule>No emojis in code, commit messages, or the session log (CLAUDE.md ASCII-only rule).</rule>
  </do_not>
</task_order>
