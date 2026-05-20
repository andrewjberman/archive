<task_order>
  <metadata>
    <id>SSCN_DIVDEF.007</id>
    <slug>de-portal-layout-revert-v0-4</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>0.3.0_DE_TradingOperations registers live (Andrew spinning up Pod 3 DE 2026-05-20). COO fires the GO MCP + flips status to pending on DE registration. TO body is complete and gates are met NOW -- the only hold is DE being offline at authoring time. No upstream dependency.</dispatch_unblock_condition>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct "focus SSCN today" 2026-05-20. Corrects a layout-scope violation on DEV before the TO-4/.006 PROD push. ~30-45min DE wall.</priority>
    <sla>~30-45min DE wall once GO lands. PARALLEL OK with .002/.003/.004/.005.</sla>
    <deadline>None -- ship at DE pace once GO lands; gates the TO-4/.006 PROD push.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md -- PRD v0.4 (commit d9b664e63, 1.0.0_SA_CTO, 2026-05-20). This TO is the literal decomposition of PRD §6.7 "TO-5". Read §A (TO-1 over-scope audit), §B (systematic/yield finding -- not a parse defect), §C (section dispositions), and §6.7 (the surgical-revert spec) before starting.</prd>
    <directive>Andrew-direct 2026-05-20 via 1.0.0_SA_CTO: Yang's clarification -- the Security Scanner keeps ALL pre-5/18 factors, functionality, AND layout. ONLY two changes are permitted: (1) updated data/indices, (2) the new default preset/weighting on load. TO-1 (commit 45ea7210, DEV) over-scoped by adding new UI controls + a functionality change. This TO surgically reverts the over-scope.</directive>
    <baseline_commit>904caed5 -- the pre-45ea7210 state of ScannerHeaderPanel.tsx. This is the byte-identical target for AC1.</baseline_commit>
    <in_scope_commits_to_preserve>45ea7210 carries the IN-SCOPE DIVZ DEFAULT_PRESET seeding (KEEP). b302f5cf (.005 universe migration, KEEP) layered on top. Neither may be reverted -- see &lt;do_not&gt;.</in_scope_commits_to_preserve>
  </references>

  <context>
    TO-1 (SSCN_DIVDEF.001, commit 45ea7210, on portal DEV only -- nothing in PROD) shipped one in-scope change bundled with three out-of-scope additions. Per PRD §A:

    IN SCOPE (keep): the DIVZ default preset on load -- DEFAULT_PRESET + initializeDefaultsWithWeights seeding + default universe sp500 -> r1000. This is the permitted "new default schema on load."

    OUT OF SCOPE (revert -- did not exist pre-5/18):
    - B. Ranking-method radiogroup ("Non-sector neutral / Sector neutral [disabled]") in ScannerHeaderPanel -- new control.
    - C. 4-group rollup chip strip ("Preset groups: Dividend 40% / Momentum 30% / ...") in ScannerHeaderPanel -- new UI element. (This strip, placed above factor rows still tagged by their 11-value FactSet registry category, is what made "systematic"/"yield" look like a parse bug -- per §B it is NOT a defect; reverting the strip removes the visual contradiction.)
    - D. Weight input step={1} -> step={0.1} -- functionality change to an existing control.

    This TO surgically restores the pre-5/18 layout while preserving the in-scope preset seeding and the .005 universe migration. The revert lands on DEV before the TO-4/.006 PROD push, so there is zero user-facing impact.
  </context>

  <scope>
    <step>Phase 1 (before write) -- baseline. Run the compiler baseline (see &lt;compiler_tools_mandate&gt; Phase 1). Capture `git show 904caed5:src/pages/SecurityScanner/components/ScannerHeaderPanel.tsx` as the byte-identical target. MCP DS 0.3.0 to coordinate the shared SSCN_GROUP_TAXONOMY.md edit window (DS owns §5+§8, you touch §3.5 only) -- see &lt;cross_domain_coordination&gt;.</step>
    <step>Phase 2 (edit) -- surgical revert. MUST be hand-surgical, NOT `git revert 45ea7210` (a blanket revert nukes the in-scope DEFAULT_PRESET seeding AND the b302f5cf universe migration). Specific edits per PRD §6.7:
      - `components/ScannerHeaderPanel.tsx` -- hand-restore to its pre-45ea7210 state (commit 904caed5): remove the ranking-method radiogroup, remove the 4-group rollup chip strip, restore weight input step={1}, remove the `rankingMethod` / `onRankingMethodChange` props, the `PRESET_GROUP_COLOR` / `PRESET_GROUP_TOTALS` constants, and the `RankingMethod` / `DEFAULT_PRESET` / `PRESET_GROUP_ORDER` imports TO-1 added. End state = byte-identical to 904caed5.
      - `hooks/useScannerState.ts` -- remove the `RankingMethod` type, `rankingMethod` state, and `setRankingMethod` setter. KEEP `initializeDefaultsWithWeights` (in-scope seeding).
      - `SecurityScanner.tsx` -- remove the `rankingMethod` / `onRankingMethodChange` prop wiring. KEEP the `DEFAULT_PRESET` seeding `useEffect`.
      - `constants.ts` -- KEEP `DEFAULT_PRESET`, `PresetEntry`, `PresetGroup`, `PRESET_GROUP_ORDER`, `US_ONLY_UNIVERSES`, and the universe entries. `PRESET_GROUP_ORDER` may become unimported once the strip is gone -- keep the export as documented forward-compat metadata (PRD §C "PresetEntry.group RETAINED"); an unused-export lint nit is your call and does not affect layout.
      - `docs/architecture/security-scanner-source/SSCN_GROUP_TAXONOMY.md` §3.5 -- patch in place to: "the group taxonomy is preset metadata; no UI strip renders it post-v0.4." Coordinate the commit window with DS 0.3.0 first.
    </step>
    <step>Phase 3 (verify + commit) -- run Phase 2 + Phase 3 compiler mandate. Commit via `.tools/safe-commit.sh --author "0.3.0_DE_TradingOperations &lt;0.3.0_DE_TradingOperations@opal.agent&gt;"`. Push to portal DEV is a DT lane action per role abilities -- if a push is needed, CC DT 0.3.0; the commit itself is yours.</step>
    <step>Phase 4 (RAVC2) -- to 2.0.0_SA_COO + CC 1.0.0_SA_CTO with: the AC1 `git diff 904caed5 HEAD` empty-output transcript; AC2 over-revert-guard evidence (DEFAULT_PRESET 13 entries + 5-universe set intact); AC3 fresh-load seeding observation; AC4 no-new-controls confirmation; AC5 /frontend-dev smoke + visual-diff result; AC6 tsc + lint clean; commit SHA(s); the §3.5 patch + DS coordination confirmation. DS-mode: TO status -> complete on RAVC2 send.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">`ScannerHeaderPanel.tsx` is byte-identical to commit 904caed5: `git diff 904caed5 HEAD -- src/pages/SecurityScanner/components/ScannerHeaderPanel.tsx` returns EMPTY output. Transcript captured in the session log.</ac>
    <ac id="AC2">Over-revert guard (paired with AC1): `constants.ts` `DEFAULT_PRESET` has 13 entries with weights summing to 100.0, AND the 5-universe set is intact (`US_ONLY_UNIVERSES` + the `UniverseId` union = sp500 / r1000 / rmidcap / sp400 / msciusa). Confirms the surgical revert did NOT over-revert into the in-scope preset/universe work.</ac>
    <ac id="AC3">On a fresh page load (no prior user state), the scanner seeds the 13 DIVZ factors at the PRD §3.1 weights and defaults the universe to r1000. Observed in DEV.</ac>
    <ac id="AC4">No ranking-method control and no "Preset groups" rollup strip render anywhere on the Security Scanner page; weight input is step={1} (unless Andrew has elected the override -- see &lt;andrew_overridable_note&gt;).</ac>
    <ac id="AC5">`/frontend-dev` smoke green; visual diff of `ScannerHeaderPanel` against a pre-5/18 screenshot shows ZERO layout delta -- only the seeded factor list / weights differ (the permitted default-state change). Visual-diff artifact path in the session log.</ac>
    <ac id="AC6">`bun run typecheck` (tsc) clean and `bun run lint` clean. Transcript captured.</ac>
  </acceptance_criteria>

  <andrew_overridable_note>
    Weight input step: this TO defaults to reverting step={0.1} -> step={1} ("functionality frozen" per Yang's directive). Andrew may elect to retain step={0.1} -- the DIVZ preset uses 0.5/7.5-granular weights so a finer spinner step is defensible (step only governs the spinner-arrow increment; the seeded 7.5 displays and persists correctly regardless). If Andrew elects to retain 0.1, that single line reverts back without re-opening this TO. The TO is NOT gated on his answer -- ship the default (step={1}) unless Andrew has already said otherwise.
  </andrew_overridable_note>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check ScannerHeaderPanel</run>
        <expect>Baseline rendered-field set captured. Record any MISSING / NOTE / UNUSED in the session log -- this is the pre-revert reference for the Phase 3 re-run.</expect>
        <if_mismatch>If MISSING fields already exist pre-revert, note them as pre-existing so the Phase 3 comparison is not polluted; not a blocker for starting.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-cache collisions</run>
        <expect>No new React Query key collision for scanner keys. This TO REMOVES state (RankingMethod) and adds none, so a collision is not expected -- the run confirms it.</expect>
        <if_mismatch>If a collision surfaces for any scanner key, RAVC2 BLOCKED to COO -- investigate before commit; do not ship a cache-corruption risk.</if_mismatch>
      </step>
      <step>
        <run>bun run typecheck</run>
        <expect>tsc exits clean (0 errors). Removing the RankingMethod type/state/setter + prop wiring must not leave a dangling reference.</expect>
        <if_mismatch>TS2304 / dangling-reference = revert incomplete. Fix every reference site before commit.</if_mismatch>
      </step>
      <step>
        <run>bun run lint</run>
        <expect>lint exits clean. An unused-export nit on PRESET_GROUP_ORDER is acceptable (kept as documented metadata) -- document the decision in the commit message if lint flags it.</expect>
        <if_mismatch>Any other lint error = fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-transform schema-check ScannerHeaderPanel</run>
        <expect>No MISSING fields post-revert (no field rendered without a type). Compare against the Phase 1 baseline -- the rendered-field set should shrink (controls removed), never gain a MISSING.</expect>
        <if_mismatch>A MISSING field = runtime undefined. Fix before RAVC2.</if_mismatch>
      </step>
      <step>
        <run>/frontend-dev smoke + visual diff vs pre-5/18 ScannerHeaderPanel screenshot</run>
        <expect>Smoke green; ZERO layout delta on ScannerHeaderPanel (only seeded factors/weights differ).</expect>
        <if_mismatch>Any layout delta = revert incomplete; iterate against the 904caed5 byte-identical target until AC1 + AC5 both pass.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    `docs/architecture/security-scanner-source/SSCN_GROUP_TAXONOMY.md` is SHARED with SSCN_DIVDEF.003 (DS 0.3.0 authoring that doc concurrently under the .003 GO). Ownership split: DS 0.3.0 owns §5 + §8 (empirical evidence + the v0.3 adjudication disposition); DE 0.3.0 (this TO) patches §3.5 ONLY (the stale group-weights-strip description). DE MUST MCP DS 0.3.0 to coordinate the commit window BEFORE committing the §3.5 patch so the two edits do not collide on the same file. If DS has the file checked out / uncommitted, sequence behind their RAVC2 COMPLETE commit. No other cross-domain resource -- this TO otherwise touches only portal/src/pages/SecurityScanner/** which no other active TO writes.
  </cross_domain_coordination>

  <deliverables>
    - Surgical layout-revert commit(s) on portal DEV: ScannerHeaderPanel.tsx restored byte-identical to 904caed5; useScannerState.ts + SecurityScanner.tsx RankingMethod removal; DEFAULT_PRESET + universe migration preserved.
    - SSCN_GROUP_TAXONOMY.md §3.5 patch (coordinated with DS 0.3.0).
    - Session log under `org/tier2_senior/0.3.0_DE_TradingOperations/logs/YYYY-MM-DD/` with: AC1 git-diff empty transcript; AC2 over-revert-guard evidence; AC3 fresh-load observation; AC4 no-new-controls confirmation; AC5 /frontend-dev smoke + visual-diff artifact path; AC6 tsc+lint transcript; Compiler Tools section reproducing each &lt;run&gt; + observed result + pass/fail vs &lt;expect&gt;.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO on close; TO status -> complete on RAVC2 send.
  </deliverables>

  <do_not>
    <rule>Do NOT `git revert 45ea7210`. The revert MUST be hand-surgical. 45ea7210 bundles the in-scope DEFAULT_PRESET seeding with the out-of-scope B/C/D elements; b302f5cf layered the .005 universe migration on top. A blanket revert destroys the preset AND the universe migration -- both in-scope, both must survive.</rule>
    <rule>Do NOT remove or alter DEFAULT_PRESET, PresetEntry, PresetGroup, the universe entries, US_ONLY_UNIVERSES, or the UniverseId union. PRESET_GROUP_ORDER is KEPT as forward-compat metadata even though its only renderer (the rollup strip) is being removed -- per PRD §C explicit decision.</rule>
    <rule>Do NOT push portal DEV -> PROD. PROD push is the TO-4/.006 DT lane, gated on this TO + .003 close + Andrew DEV smoke. This TO lands on DEV only.</rule>
    <rule>Do NOT touch SSCN_GROUP_TAXONOMY.md §5 or §8 -- those are DS 0.3.0's under .003. Patch §3.5 only, and coordinate the commit window with DS first.</rule>
    <rule>Do NOT modify FactorBankTab.tsx, utils/categoryOrder.ts, or factor_metadata_registry.json. The "systematic"/"yield" registry-category display is correct pre-5/18 behavior (PRD §B) -- it stays exactly as-is.</rule>
    <rule>No emojis in code, commit messages, the doc patch, or the session log (CLAUDE.md ASCII-only rule).</rule>
  </do_not>
</task_order>
