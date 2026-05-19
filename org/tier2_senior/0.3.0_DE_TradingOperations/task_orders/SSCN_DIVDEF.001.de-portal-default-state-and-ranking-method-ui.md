<task_order>
  <metadata>
    <id>SSCN_DIVDEF.001</id>
    <slug>de-portal-default-state-and-ranking-method-ui</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct directive 2026-05-19 to spin Pod 3 in parallel; PRD v0.1 shipped a5e1b7ef4 11:13Z; ~3h DE wall per CTO estimate (single page surface, fully self-contained per comp-blast SecurityScanner = 1942 nodes/2136 edges all internal to portal/src/pages/SecurityScanner).</priority>
    <sla>~3h DE wall. Independent of TO-2 (FE change works against any vintage of latest/). PARALLEL OK with TO-2 + TO-3.</sla>
    <deadline>None -- ship at DE 0.3.0 pace; Pod 3 ~0.5 effort-day if all 3 TOs run in parallel.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md (PRD v0.1, 1.0.0_SA_CTO~B, commit a5e1b7ef4 2026-05-19) -- canonical spec; section 3.1 has the exact 13-factor preset + weights; section 4.1 has the FE surface inventory.</prd>
    <prior_project>SSCN_PORTAL (2026-03-10 COMPLETE) shipped the page surface this TO evolves. SSCN_DATA_CONTRACT.md + SSCN_DESIGN_CONTRACT.md (2026-03-05) are the underlying contracts; this TO does NOT modify either contract -- it changes the default state seeded into the existing contracts.</prior_project>
    <coo_section_7_rulings>2.0.0_SA_COO~B accepts CTO recommendations on all six PRD section 7 questions verbatim 2026-05-19 -- documented in SSCN_DIVDEF.json phase narrative. Andrew may override any ruling by amending this TO; if no amendment lands before DE starts, CTO recommendations are authoritative. The two that materially shape DE work:
      Q1 (sector-neutral) -- v0.1 ships UI-only toggle, default = non-sector-neutral, sector-neutral option DISABLED with tooltip "Coming soon (v0.2)". Locks the user-facing label without coupling FE to a Lambda redeploy.
      Q2 (group rollup display) -- hybrid: ScannerHeaderPanel header strip shows 4-group summary (Andrew taxonomy: Dividend 40 / Momentum 30 / Value 15 / Quality 15) computed from preset entries; per-factor table still color-codes by registry category for cross-tool consistency with Factor Bank. The preset's `group` field is used ONLY by the summary strip.
      Q4 (weight input step) -- step=0.1 (permissive; isWeightValid total === 100 still enforces sum).
      Q6 (DEFAULT_CATEGORIES retention) -- if `grep -rn "DEFAULT_CATEGORIES" portal/src` shows only the seed-loop call site, remove it in this same commit. If external consumers exist, leave it.
    </coo_section_7_rulings>
    <compiler_baseline>CTO PRD section 5 already ran the authoritative compiler baseline: comp-blast SecurityScanner (1942 nodes / 2136 edges -- all internal to the page); comp-transform schema-check SecurityScanner PASS; comp-routes trace getUniverseScanner + getSecurityScannerFactors (no route change); comp-cache collisions clean; comp-iam service opal-security-scanner-processor (no Lambda IAM change). DE re-runs at Phase 1 to detect any cache-stale drift since 11:13Z.</compiler_baseline>
  </references>

  <context>
    The SecurityScanner page currently seeds defaults by picking the top-IC factor from each of ['value', 'growth', 'quality', 'momentum', 'size'] and equal-weighting them (SecurityScanner.tsx:50-63 + constants.ts:21 + useScannerState.ts:45). Universe defaults to 'sp500'. Weight input is integer-only (step=1) and rejects fractional weights. There is no UI control labeled "Ranking method" -- the Lambda computes universe-wide percentiles only (no sector-neutral variant).

    Andrew direct directive 2026-05-19: replace the generic seeding with an explicit DIVZ-style dividend-tilted 13-factor preset across Russell 1000 (universe r1000, sourceColumn wt_iwb), with the exact group structure Dividend 40 / Momentum 30 / Value 15 / Quality 15, and surface a ranking-method UI control (non-sector-neutral default; sector-neutral disabled "Coming soon" v0.1 per CTO Q1 ruling).

    This is FE-only. No Lambda code change. No Terraform change. No backend schema break. PRD section 4.2 is explicit: backend percentile computation unchanged in v0.1.
  </context>

  <scope>
    <step>Phase 1 (before edit) -- run compiler baseline + verify §7 Q6 ruling input:
      - `comp-transform schema-check SecurityScanner --feature divdef` (CTO PRD section 5 ran the baseline schema-check; the --feature flag escalates any divdef-named UNUSED fields to WARN. Expect: 0 feature-relevant WARN entries).
      - `comp-transform ternary-audit SecurityScanner` if any new union-type value (e.g., rankingMethod is a new TS union -- 'non-sector-neutral' | 'sector-neutral'; ternary-audit catches every cohort === / rankingMethod === routing missing the new branch).
      - `comp-cache collisions | grep -i scanner` (expect clean).
      - `grep -rn "DEFAULT_CATEGORIES" portal/src` -- if only call site is SecurityScanner.tsx seed loop, remove in this TO commit per Q6 ruling. If external consumers exist, leave the export in place and only stop consuming it from the seed loop.
    </step>
    <step>Phase 2 (edit) -- the five FE changes per PRD section 4.1:
      (a) `portal/src/pages/SecurityScanner/constants.ts` -- add new `DEFAULT_PRESET` constant as an array of `{ code, weight, group }` entries (13 entries) with the exact mapping in PRD section 3.1. Remove `DEFAULT_CATEGORIES` if grep showed it dead per Q6.
      (b) `portal/src/pages/SecurityScanner/hooks/useScannerState.ts` -- default `selectedUniverseId` from `'sp500'` → `'r1000'` (line 45); add `initializeDefaultsWithWeights(factors, weightsByCode)` alongside existing `initializeDefaults` (lines 94-99); extend `ScannerStateActions` interface with `rankingMethod: 'non-sector-neutral' | 'sector-neutral'` + `setRankingMethod(value): void` initialized to `'non-sector-neutral'`.
      (c) `portal/src/pages/SecurityScanner/SecurityScanner.tsx:50-63` -- replace top-IC-per-category seed loop with direct `picks = factorData.factors.filter(f => DEFAULT_PRESET.some(p => p.code === f.code))` lookup; pass weights via the new `initializeDefaultsWithWeights(picks, weights)` call. Plumb `rankingMethod` + `setRankingMethod` props to ScannerHeaderPanel.
      (d) `portal/src/pages/SecurityScanner/components/ScannerHeaderPanel.tsx` -- (1) Add Ranking Method segmented control (or dropdown) in header actions adjacent to universe selector: "Non-sector neutral" (default, enabled) | "Sector neutral" (disabled with tooltip "Coming soon (v0.2)" per Q1 ruling); (2) change weight input `step={1}` → `step={0.1}` per Q4 ruling; (3) Add 4-group rollup chip strip per Q2 hybrid -- render group weight totals (Dividend 40 / Momentum 30 / Value 15 / Quality 15) computed from `DEFAULT_PRESET` `.group` field; per-factor table colors STAY on registry `category` field for Factor Bank consistency.
      (e) Bun: `bun run typecheck` clean; `bun run lint` clean; (if applicable) `bun run build`.
    </step>
    <step>Phase 3 (before commit) -- re-run Phase 1 compiler tools; confirm no new MISSING/UNUSED + no new cache collisions; `bun run typecheck` clean; `bun run lint` clean.</step>
    <step>Phase 4 (commit + push) -- commit via `.tools/safe-commit.sh --author "0.3.0_DE_TradingOperations <0.3.0_DE_TradingOperations@opal.agent>" -m "..." -- <exact paths>` per ADHC_OWNPTH.007. DE cannot push to remote per role abilities (DT/AE gates); after commit lands locally, message DT 0.3.0 via MCP to handle PROD push when TO-3 closes (Andrew DEV smoke first per TO-4 optional).</step>
    <step>Phase 5 (visual smoke + RAVC2) -- `/frontend-dev` Playwright smoke: page loads on first mount with universe = "Russell 1000", 13 named factor chips in order Dividend → Momentum → Value → Quality, weights match section 3.1, sum = 100.0%; ranking method control visible with non-sector-neutral selected + sector-neutral disabled with "Coming soon" tooltip; weight input accepts 7.5; clearing all factors + reload restores the exact preset. Capture screenshot for the session log. RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B with: commit SHA + Playwright screenshot + AC1-AC8 confirmations + grep result on `DEFAULT_CATEGORIES` (kept vs removed). DE-mode: TO status -> complete on receipt.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">First-load page state in DEV: Universe dropdown reads "Russell 1000"; 13 named factor chips render in the order Dividend → Momentum → Value → Quality; weights match PRD section 3.1 exactly (dy_ntm=20, dps_gr_1yr=10, shldr_yield=10, eps_est_rev_45d=5, short_pct_chg_12m=5, days_to_cover=5, pcta52wl=5, ret_mom_252d=5, velocity_63d=5, ey_ntm=7.5, fcfy=7.5, accruals_bs=7.5, leverage=7.5); displayed sum = 100.0%. Playwright screenshot captured.</ac>
    <ac id="AC2">Ranking method control is visible with "Non-sector neutral" selected (default); "Sector neutral" option exists but is disabled with hover tooltip "Coming soon (v0.2)" (or equivalent v0.2 phrasing per Q1).</ac>
    <ac id="AC3">User edits a weight to `7.5` and the input accepts it (no integer rejection); sum recalculates to `100.0` with isWeightValid === true. Confirm `step={0.1}` is the attribute on the input element.</ac>
    <ac id="AC4">Clearing all factors + reseeding (reload / fresh mount) restores the exact section 3.1 preset (universe = r1000; 13 factors; weights match; group totals 40/30/15/15).</ac>
    <ac id="AC5">Universe selector still functions: switching to S&P 500 / ACWI ex-US / EAFE / EAFE Value / R1000 Value works; switching BACK to Russell 1000 does NOT re-trigger the preset reseed (preset is initial-mount only via `defaultsSeeded.current` ref, NOT "universe-default").</ac>
    <ac id="AC6">`comp-transform schema-check SecurityScanner --feature divdef` continues to exit PASS (0 MISSING; 0 divdef-named UNUSED; NOTE fields are expected aliases).</ac>
    <ac id="AC7">`bun run typecheck` exit 0; `bun run lint` exit 0; `bun run build` (if run) exit 0.</ac>
    <ac id="AC8">`/frontend-dev` Playwright smoke: page loads, no console errors, default Universe Scanner tab renders ranked rows. Screenshot captured. (Note: ranked rows depend on TO-2 data refresh fresh -- if TO-2 hasn't closed yet, AC8 may show stale 2026-03-06 vintage data; that's acceptable as long as the page renders with the new defaults applied to whatever vintage of `latest/` is live. The DATA-side smoke is TO-3.)</ac>
    <ac id="AC9">Group rollup chip strip in ScannerHeaderPanel shows the 4-group summary: Dividend 40 / Momentum 30 / Value 15 / Quality 15 (computed from DEFAULT_PRESET .group field; per Q2 hybrid). Per-factor chips in the table color-code by registry `category` (UNCHANGED -- preserves Factor Bank cross-consistency).</ac>
    <ac id="AC10">`DEFAULT_CATEGORIES` constant retention decision documented in session log: grep result on `portal/src` + decision (kept vs removed) + rationale.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      `comp-transform schema-check SecurityScanner --feature divdef` -- expect 0 feature-relevant WARN (any divdef-named UNUSED = routing ternary missing branch).
      `comp-transform ternary-audit SecurityScanner` -- expect 0 gaps on `rankingMethod ===` (new union type) -- if gaps, fix all before Phase 2.
      `comp-cache collisions | grep -i scanner` -- expect clean (no new React Query collisions).
      `grep -rn "DEFAULT_CATEGORIES" portal/src` -- input to Q6 ruling (remove if only seed-loop consumer).
    </before_write>
    <before_commit>
      Re-run all 3 Phase 1 compiler tools (schema-check, ternary-audit, cache collisions) -- expect identical or improved state (no regressions).
      `bun run typecheck` exit 0; `bun run lint` exit 0.
    </before_commit>
    <after_commit>
      `comp-transform fields SecurityScanner` -- all rendered fields have a TypeScript type (no silent undefineds).
      `/frontend-dev` Playwright smoke per AC8.
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    None. SecurityScanner page is fully self-contained per `comp-blast SecurityScanner` (1942 nodes/2136 edges all internal). No shared files with TO-2 (DT s3 cp) or TO-3 (DS R post-upload). TO-1 is FE-only; TO-2 is S3 ops; TO-3 is DS analysis -- three orthogonal lanes.
  </cross_domain_coordination>

  <deliverables>
    - constants.ts + useScannerState.ts + SecurityScanner.tsx + ScannerHeaderPanel.tsx edits per PRD section 4.1.
    - `bun run typecheck` clean transcript.
    - Playwright `/frontend-dev` smoke screenshot.
    - Session log under `org/tier2_senior/0.3.0_DE_TradingOperations/logs/YYYY-MM-DD/` with Compiler Tools section, AC1-AC10 evidence, Q6 grep + retention decision, group taxonomy summary.
    - RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B on close; SSCN_DIVDEF.json status -> ws=DE complete on receipt (COO~B updates JSON; DE just MCPs).
  </deliverables>

  <do_not>
    <rule>Do NOT modify the Lambda Python code (`infra/aws/lambda/opal_security_scanner_processor/`) -- backend percentile compute is unchanged in v0.1 (PRD section 4.2).</rule>
    <rule>Do NOT modify factor_metadata_registry.json -- the bundled registry already covers all 13 codes (PRD section 5 verified).</rule>
    <rule>Do NOT touch Factor Bank tab visual layout -- only ScannerHeaderPanel + state hook change.</rule>
    <rule>Do NOT modify `relationship` field assumptions in the FE -- the registry's relationship sign is authoritative (TO-3 will independently verify against FactSet semantics).</rule>
    <rule>Do NOT change React Query keys for `getUniverseScanner` / `getSecurityScannerFactors` -- `comp-cache collisions` clean today; do not introduce a collision via the new rankingMethod state.</rule>
    <rule>No emojis in code, comments, or session logs (CLAUDE.md ASCII-only rule).</rule>
    <rule>Do NOT push to PROD -- DE role has no push permission per Abilities by Role. Surface via MCP to DT 0.3.0 when TO-3 closes + Andrew DEV smoke approves (optional TO-4).</rule>
  </do_not>
</task_order>
