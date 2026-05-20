<task_order>
  <metadata>
    <id>SSCN_DIVDEF.008-RD</id>
    <slug>presets-dropdown-implementation</slug>
    <issued_by>0.3.0_DE_TradingOperations</issued_by>
    <issued_to>0.3.4_RD_SecurityScanner</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <parent_to>org/tier2_senior/0.3.0_DE_TradingOperations/task_orders/SSCN_DIVDEF.008.de-rd-presets-dropdown.md</parent_to>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct "focus SSCN today" 2026-05-20. GO is live (COO batch GO -> DE -> you). Begin immediately.</priority>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md -- PRD v0.5 (commit adbc3c34e) §A/§B/§C/§6.8. Read it.</prd>
    <parent>The parent TO (SSCN_DIVDEF.008.de-rd-presets-dropdown.md) is the authority. This RD TO is DE's implementation decomposition of it. Where they differ, the parent governs -- flag any conflict to DE.</parent>
    <baseline>Implement on top of the post-SSCN_DIVDEF.007 portal DEV state (commit a844f0dd). ScannerHeaderPanel.tsx is byte-identical to pre-5/18 904caed5; the DIVZ-on-load seeding is the hardcoded initializeDefaultsWithWeights call. This TO refactors that seeding into a PRESETS-registry model + adds the Presets dropdown.</baseline>
  </references>

  <context>
    Today "DIVZ on load" is hardcoded seeding (initializeDefaultsWithWeights) -- invisible to the user, not switchable. PRD v0.5 makes the default an explicit, user-switchable "Presets:" dropdown. A preset = a named {universe, factor selection, weights} bundle. This is the ONE authorized layout addition under SSCN_DIVDEF -- the v0.4 "pre-5/18 layout frozen" rule otherwise stands in full. Do NOT reopen anything SSCN_DIVDEF.007 reverted (the ranking-method radiogroup and 4-group rollup strip stay reverted).
  </context>

  <scope>
    Four files, all inside portal/src/pages/SecurityScanner/ (your page directory). Implement exactly as specified.

    === FILE 1: constants.ts ===
    ADD (do NOT modify DEFAULT_PRESET -- its 13 codes/weights/group stay byte-identical):

      export interface Preset {
        id: string
        label: string
        universe: UniverseId
        entries: readonly PresetEntry[]
      }

      export const PRESETS: readonly Preset[] = [
        {
          id: 'divz',
          label: 'DIVZ -- Dividend',
          universe: 'r1000',
          entries: DEFAULT_PRESET,
        },
      ] as const

      export const DEFAULT_PRESET_ID = 'divz'

    `DEFAULT_PRESET` stays exported as-is (PRESETS.divz.entries references it). NO content change.

    === FILE 2: hooks/useScannerState.ts ===
    a. ADD action `applyPreset(presetId: string, allFactors: FactorDefinition[])`:
       - Look up the preset in PRESETS by id; if not found, return (no-op).
       - Build a code->FactorDefinition map from allFactors.
       - Resolve preset.entries -> picks: FactorDefinition[] (skip codes not in allFactors) + a
         weights record keyed by code.
       - Atomically set: universe = preset.universe, selectedFactors = picks, weights = the record.
    b. ADD a DERIVED `activePresetId: string | null` exposed value (useMemo):
       - Returns the id of the preset whose {universe, factor-code SET, per-code weights} EXACTLY
         matches the current live state; returns `null` when nothing matches (the Custom state).
       - Match logic: preset.universe === selectedUniverseId AND the set of preset entry codes
         equals the set of selectedFactors codes AND every entry weight === weights[code].
       - This is a pure derive -- no extra state, no mutator changes. A manual edit naturally
         stops matching -> activePresetId becomes null -> the dropdown shows Custom.
    c. REMOVE `initializeDefaultsWithWeights` (type member + function + return entry) -- applyPreset
       supersedes it and SecurityScanner.tsx no longer calls it. KEEP everything else
       (setUniverse/addFactor/removeFactor/setWeight/setEqualWeight/clearSelection, the r1000
       default, buildEqualWeights).
    d. Add `applyPreset` and `activePresetId` to the `ScannerStateActions` interface + the return object.

    === FILE 3: components/ScannerHeaderPanel.tsx ===
    Add ONE new control -- a labeled "Presets:" <select> -- inside the existing `actions` <div>
    (the flex row with the universe <select> + Equal Weight + Clear), placed FIRST (left of the
    universe select).
    - New props on ScannerHeaderPanelProps: `activePresetId: string | null` and
      `onPresetChange: (id: string) => void`.
    - Import PRESETS from '../constants'.
    - Markup (match the universe <select> styling exactly -- same className):
        <div className="flex items-center gap-1.5">
          <span className="text-sm text-white/50 font-medium">Presets:</span>
          <select
            value={activePresetId ?? 'custom'}
            onChange={e => onPresetChange(e.target.value)}
            className=  (same className string as the universe select)
          >
            {activePresetId === null && (
              <option value="custom" disabled className="bg-[hsl(var(--bg-header))] text-white">Custom</option>
            )}
            {PRESETS.map(p => (
              <option key={p.id} value={p.id} className="bg-[hsl(var(--bg-header))] text-white">{p.label}</option>
            ))}
          </select>
        </div>
    - The "Custom" option renders only when activePresetId is null (diverged) and is `disabled` so
      it cannot be actively selected -- it is a display-only state. Selecting a real preset fires
      onPresetChange.
    - DO NOT touch anything else in this file. No other control, no layout restructure.

    === FILE 4: SecurityScanner.tsx ===
    a. Seeding useEffect: replace the DEFAULT_PRESET loop + `initializeDefaultsWithWeights(picks, weights)`
       call with a single `scannerState.applyPreset(DEFAULT_PRESET_ID, factorData.factors)` call.
       Keep the `defaultsSeeded` ref guard + the `if (!factorData) return` guard.
    b. Change the import: `import { DEFAULT_PRESET } from './constants'` -> `import { DEFAULT_PRESET_ID } from './constants'`.
       (FactorDefinition import may become unused once the manual pick loop is gone -- remove it from
       the type import if so; tsc/lint will tell you.)
    c. Pass two new props to <ScannerHeaderPanel>:
         activePresetId={scannerState.activePresetId}
         onPresetChange={(id) => scannerState.applyPreset(id, factorData?.factors ?? [])}
    d. COPY FIX (folded in per the parent TO): fix the stale "6 universes" copy left by the .005
       6->5 universe migration. TWO occurrences, both -> "5 universes":
         - line ~6 JSDoc comment: "across 6 universes." -> "across 5 universes."
         - line ~74 `description=` prop: "Multi-factor screening across 6 universes ..." ->
           "Multi-factor screening across 5 universes with weighted composite ranking."
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Fresh page load (no prior user state): DIVZ preset applied -- universe r1000, 13 DIVZ factors at PRD §3.1 weights -- and the Presets dropdown shows "DIVZ -- Dividend" selected.</ac>
    <ac id="AC2">Selecting DIVZ from the dropdown after manual edits fully re-applies its universe + factor set + weights atomically.</ac>
    <ac id="AC3">A manual edit (universe, factor set, or any weight) away from the active preset flips the dropdown to the "Custom" state -- the UI never labels an edited config as a named preset.</ac>
    <ac id="AC4">No layout change vs the post-.007 baseline other than the single new "Presets:" dropdown.</ac>
    <ac id="AC5">`/frontend-dev` smoke green (DE runs it).</ac>
    <ac id="AC6">`bun run typecheck` clean and `bun run lint` clean -- run BOTH before handing back to DE; paste the transcript in your session log.</ac>
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT change the DIVZ factor codes, weights, or group metadata in DEFAULT_PRESET. The PRESETS registry REFERENCES it unchanged.</rule>
    <rule>Do NOT reopen any element SSCN_DIVDEF.007 reverted -- no ranking-method radiogroup, no 4-group rollup strip. ScannerHeaderPanel stays byte-identical to 904caed5 EXCEPT for the one new Presets select + its two new props.</rule>
    <rule>Do NOT add a second new control, panel, tab, or layout restructure. Exactly ONE new control.</rule>
    <rule>Do NOT commit or push. Hand the implementation back to DE 0.3.0 (MCP when done) -- DE runs the 3-phase compiler mandate, reviews vs all 6 ACs, commits, and owns the RAVC2. You MAY commit your own page per RD role abilities if DE asks; default is DE commits this one (constants.ts/useScannerState.ts touch shared hook/constants files DE is reviewing).</rule>
    <rule>No emojis in code or the session log (CLAUDE.md ASCII-only).</rule>
  </do_not>

  <deliverables>
    - The 4-file implementation on the portal working tree (DEV branch, uncommitted -- DE commits after review).
    - `bun run typecheck` + `bun run lint` both exit 0; transcript in your session log.
    - A session log under org/tier3_junior/0.3.4_RD_SecurityScanner/logs/2026-05-20/.
    - MCP 0.3.0_DE_TradingOperations when the implementation is ready for DE review + compiler mandate + commit.
  </deliverables>

  <handback>
    When done: MCP 0.3.0_DE_TradingOperations with "SSCN_DIVDEF.008 RD implementation ready" + the list of files changed + your typecheck/lint result. DE reviews, runs comp-cache + comp-transform schema-check + /frontend-dev smoke, commits, and RAVC2s to COO. Do NOT flip this TO to complete yourself -- DE closes the loop.
  </handback>
</task_order>
