<task_order>
  <metadata>
    <id>SSCN_DIVDEF.008</id>
    <slug>de-rd-presets-dropdown</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <implementation_lane>0.3.4_RD</implementation_lane>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>SSCN_DIVDEF.007 (DE layout revert) RAVC2 COMPLETE. .007 and this TO both edit ScannerHeaderPanel.tsx + constants.ts -- they run SEQUENTIAL, not parallel, to avoid a working-tree collision. COO flips status to pending + fires GO MCP the moment .007 RAVCs clean. Do NOT start before .007 closes -- this TO refactors the DIVZ-on-load seeding code that .007 keeps.</dispatch_unblock_condition>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct "focus SSCN today" 2026-05-20 (post-v0.4 directive). Delivers the default preset as an explicit, user-switchable dropdown. ~45-60min combined DE+RD wall.</priority>
    <sla>~45-60min wall once GO lands. SEQUENTIAL after .007 (gated).</sla>
    <deadline>None -- ship at DE/RD pace once GO lands; bundles with .007 into the TO-4/.006 PROD push.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md -- PRD v0.5 (commit adbc3c34e, 1.0.0_SA_CTO, 2026-05-20). This TO is the literal decomposition of PRD §6.8 "TO-6". Read the full v0.5 Amendment block: §A (Preset data shape), §B (UI + behavior), §C (sequencing against .007), §6.8 (the spec).</prd>
    <directive>Andrew-direct 2026-05-20 (post-v0.4): the default preset is delivered through an explicit "Presets:" dropdown. A preset = a named bundle of {universe, factor selection, weights}. DIVZ is applied on page load. The dropdown lets a user load a different preset config in one action. This is the ONE authorized layout addition -- categorically distinct from the 3 unauthorized additions .007 reverts.</directive>
    <relationship_to_007>SSCN_DIVDEF.007 reverts 3 UNAUTHORIZED additions and produces a clean pre-5/18 baseline + retained DIVZ-on-load seeding. This TO (.008) adds 1 AUTHORIZED control (the Presets dropdown) and refactors the seeding .007 keeps into a PRESETS-registry model. .007 is NOT amended by this TO; it completes as-authored first.</relationship_to_007>
    <implementation_model>0.3.0_DE_TradingOperations is the PM/owner of this TO; 0.3.4_RD builds the front-end implementation under DE coordination (Andrew brought 0.3.4_RD online for this). DE owns the RAVC2 back to COO; DE coordinates the RD work, reviews it, and runs the compiler mandate.</implementation_model>
  </references>

  <context>
    Today "DIVZ on load" is hardcoded seeding magic (`initializeDefaultsWithWeights`) -- invisible to the user and not reversible by them. PRD v0.5 makes the default explicit, switchable, and extensible via a Presets dropdown: a preset is a named {universe, factor selection, weights} bundle; future presets drop into a registry with zero new UI.

    A preset data shape (PRD §A):
    ```
    interface Preset {
      id: string                        // stable key, e.g. 'divz'
      label: string                     // dropdown display, e.g. 'DIVZ -- Dividend'
      universe: UniverseId              // applied when the preset is chosen
      entries: readonly PresetEntry[]   // factor codes + weights (+ group metadata)
    }
    export const PRESETS: readonly Preset[]   // registry -- DIVZ is the only entry at v0.5
    export const DEFAULT_PRESET_ID = 'divz'   // applied on page load
    ```
    `DEFAULT_PRESET` (the 13 DIVZ entries retained by .007) becomes `PRESETS`'s `divz.entries` -- a REFACTOR, not a content change: codes, weights, and `group` metadata unchanged.

    This is the only authorized layout addition. v0.4's "pre-5/18 layout frozen" rule otherwise stands in full -- the Presets dropdown does NOT reopen any element .007 reverted (ranking-method radiogroup + rollup strip stay reverted).
  </context>

  <scope>
    <step>Phase 1 (before write) -- gate verify + baseline. Confirm SSCN_DIVDEF.007 has RAVC2-closed (COO fires this TO's GO only after that, but DE re-confirms the .007 commit is on portal DEV before editing -- the seeding code this TO refactors must be in its post-.007 state). Run the Phase 1 compiler baseline (see &lt;compiler_tools_mandate&gt;).</step>
    <step>Phase 2 (implement) -- DE coordinates 0.3.4_RD on the edits per PRD §6.8:
      - `constants.ts` -- add the `Preset` interface, the `PRESETS` registry (DIVZ entry: id:'divz', label:'DIVZ -- Dividend', universe:'r1000', entries: the 13 DIVZ codes/weights retained by .007), and `DEFAULT_PRESET_ID = 'divz'`. `DEFAULT_PRESET` becomes `PRESETS`'s divz entries (or is re-exported from it) -- NO content change to codes/weights/group.
      - `hooks/useScannerState.ts` -- add `activePresetId` state + an `applyPreset(id)` action that sets universe + factors + weights atomically; derive a `Custom` state when the live selection diverges from the active preset.
      - `components/ScannerHeaderPanel.tsx` -- add the labeled `Presets:` `<select>` adjacent to the universe dropdown, matching its styling; wire it to `applyPreset`. ONE new control -- no panel, tab, or layout restructure.
      - `SecurityScanner.tsx` -- the on-load seeding `useEffect` applies `DEFAULT_PRESET_ID` via `applyPreset` (replaces the direct `initializeDefaultsWithWeights` call .007 keeps).
    </step>
    <step>Phase 3 (verify + commit) -- run the Phase 2 + Phase 3 compiler mandate. DE reviews the RD implementation against all 6 ACs. Commit via `.tools/safe-commit.sh --author "0.3.0_DE_TradingOperations &lt;0.3.0_DE_TradingOperations@opal.agent&gt;"` (or the RD serial if RD commits its own page per role abilities -- DE's call; the RAVC2 is DE's regardless). Portal DEV push is a DT lane action -- CC DT 0.3.0 if a push is needed.</step>
    <step>Phase 4 (RAVC2) -- to 2.0.0_SA_COO + CC 1.0.0_SA_CTO with: AC1-AC6 evidence (fresh-load DIVZ-applied observation; re-select re-apply; manual-edit -> Custom label; /frontend-dev visual diff vs post-.007 baseline; smoke; tsc+lint); commit SHA(s); the compiler mandate transcript. DS-mode: TO status -> complete on RAVC2 send.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">On a fresh page load (no prior user state), the DIVZ preset is applied -- universe = r1000, the 13 DIVZ factors seeded at the PRD §3.1 weights -- and the `Presets:` dropdown shows `DIVZ` selected. Observed in DEV.</ac>
    <ac id="AC2">Selecting `DIVZ` from the dropdown after manual edits fully re-applies its universe + factor set + weights (atomic apply). Observed.</ac>
    <ac id="AC3">A manual edit to the universe, the factor set, or any weight -- away from the active preset -- flips the dropdown label to a non-preset `Custom` state, so the UI never misrepresents an edited config as a named preset.</ac>
    <ac id="AC4">No layout change vs the post-.007 baseline other than the single new `Presets:` dropdown. `/frontend-dev` visual diff of ScannerHeaderPanel shows only the one added control.</ac>
    <ac id="AC5">`/frontend-dev` smoke green.</ac>
    <ac id="AC6">`bun run typecheck` (tsc) clean and `bun run lint` clean. Transcript captured.</ac>
  </acceptance_criteria>

  <andrew_overridable_notes>
    Two CTO-default UX behaviors are baked into this TO; both are conventional preset-dropdown behavior and the TO is NOT gated on Andrew confirming them -- ship the defaults unless Andrew has already said otherwise:
    (a) Preset change applies immediately, with NO confirm dialog (presets are cheap to re-pick). Andrew may override to add a confirm step.
    (b) A manual edit flips the dropdown to a `Custom` label (AC3). Andrew may override the label text or the flip behavior.
  </andrew_overridable_notes>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check ScannerHeaderPanel</run>
        <expect>Baseline rendered-field set captured on the post-.007 ScannerHeaderPanel. Record any MISSING / NOTE / UNUSED -- pre-add reference for the Phase 3 re-run.</expect>
        <if_mismatch>If MISSING fields exist pre-add, note them as pre-existing so the Phase 3 comparison is not polluted; not a blocker for starting.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-cache collisions</run>
        <expect>No new React Query key collision. `applyPreset` sets the universe, which drives `useScannerApi` -- confirm the preset-driven universe change does not introduce a key collision or a same-key/different-response-type hazard for scanner data keys.</expect>
        <if_mismatch>If a collision surfaces for any scanner key, RAVC2 BLOCKED to COO -- investigate before commit; cache corruption is not shippable.</if_mismatch>
      </step>
      <step>
        <run>bun run typecheck</run>
        <expect>tsc exits clean (0 errors). The new Preset interface + PRESETS registry + activePresetId state must type-check end to end.</expect>
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
        <run>comp-transform schema-check ScannerHeaderPanel</run>
        <expect>No MISSING fields post-add (the new Presets dropdown's rendered fields all have types). Compared against the Phase 1 baseline, the rendered-field set gains the preset-select fields and no MISSING.</expect>
        <if_mismatch>A MISSING field = runtime undefined. Fix before RAVC2.</if_mismatch>
      </step>
      <step>
        <run>/frontend-dev smoke + visual diff vs post-.007 ScannerHeaderPanel baseline</run>
        <expect>Smoke green; the ONLY visual delta vs the post-.007 baseline is the single new `Presets:` dropdown (AC4).</expect>
        <if_mismatch>Any layout delta beyond the one dropdown = scope creep; reconcile against the post-.007 baseline before RAVC2.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    `constants.ts` and `ScannerHeaderPanel.tsx` are SHARED with SSCN_DIVDEF.007 (DE layout revert). The GATE on .007 RAVC2 close IS the coordination mechanism -- the two TOs run SEQUENTIAL, not parallel, so there is no working-tree collision. This TO refactors the DIVZ-on-load seeding code that .007 keeps; it cannot start until .007 has produced its clean post-revert baseline. No overlap with SSCN_DIVDEF.003 (DS, closed) or .002/.004/.005. COO enforces the sequence by holding this TO staged/dispatch_held until .007 RAVCs.
  </cross_domain_coordination>

  <deliverables>
    - Presets dropdown implementation on portal DEV: Preset interface + PRESETS registry + DEFAULT_PRESET_ID in constants.ts; activePresetId state + applyPreset() in useScannerState.ts; the `Presets:` &lt;select&gt; in ScannerHeaderPanel.tsx; on-load applyPreset in SecurityScanner.tsx.
    - Session log under `org/tier2_senior/0.3.0_DE_TradingOperations/logs/YYYY-MM-DD/` (DE; reference the RD implementation work) with: AC1-AC6 evidence; /frontend-dev smoke + visual-diff artifact paths; commit SHA(s); Compiler Tools section reproducing each &lt;run&gt; + observed result + pass/fail vs &lt;expect&gt;.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO on close; TO status -> complete on RAVC2 send.
  </deliverables>

  <do_not>
    <rule>Do NOT start before SSCN_DIVDEF.007 RAVC2 closes. The two TOs share constants.ts + ScannerHeaderPanel.tsx and MUST be sequential. COO gates the GO.</rule>
    <rule>Do NOT change the DIVZ factor codes, weights, or `group` metadata. Moving DEFAULT_PRESET into the PRESETS registry is a REFACTOR -- the divz preset's content is byte-equivalent to what .007 retains.</rule>
    <rule>Do NOT reopen any element SSCN_DIVDEF.007 reverted. The ranking-method radiogroup and the 4-group rollup strip stay reverted -- v0.4's "pre-5/18 layout frozen" rule stands; the Presets dropdown is the ONLY authorized addition.</rule>
    <rule>Do NOT add a second new control, panel, tab, or layout restructure. Exactly ONE new control -- the `Presets:` &lt;select&gt; adjacent to the universe dropdown.</rule>
    <rule>Do NOT push portal DEV -> PROD. The PROD push is the TO-4/.006 DT lane, bundling .007 + .008, gated on .003 close + Andrew DEV smoke. This TO lands on DEV only.</rule>
    <rule>No emojis in code, commit messages, or the session log (CLAUDE.md ASCII-only rule).</rule>
  </do_not>
</task_order>
