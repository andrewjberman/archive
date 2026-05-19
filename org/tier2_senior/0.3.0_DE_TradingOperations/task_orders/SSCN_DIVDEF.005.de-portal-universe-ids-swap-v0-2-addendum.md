<task_order>
  <metadata>
    <id>SSCN_DIVDEF.005</id>
    <slug>de-portal-universe-ids-swap-v0-2-addendum</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.3.0_DE_TradingOperations</issued_to>
    <date>2026-05-19</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct PRD v0.2 ratification 2026-05-19; addendum on top of `45ea7210` (TO-1 ship). FE-only; parallel-OK with TO-AE-1 (Lambda UNIVERSE_MAP swap); ~30min DE wall.</priority>
    <sla>~30min DE wall. PARALLEL-OK with SSCN_DIVDEF.004 (AE 0.5.0 Lambda redeploy). PROD push gates per TO-4 framework.</sla>
    <deadline>None hard -- ship at DE pace; recommend land in same calendar window as TO-AE-1 so PROD push (TO-4) can fire when TO-3 closes + Andrew DEV smoke approves.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md PRD v0.2 §6.5 (1.0.0_SA_CTO~B, commit c34f16d13 2026-05-19) -- verbatim DE addendum scope + 8 ACs.</prd>
    <prior_de_commit>`45ea7210` portal DEV (DE 0.3.0; TO-1 ship 2026-05-19) -- DIVZ preset + ranking-method UI + 4-group strip + step=0.1 weight input. Universe-set-independent per DE 0.3.0 re-verification 2026-05-19 PM. PRESERVED VERBATIM; this TO is additive only.</prior_de_commit>
    <data_contract>docs/architecture/SSCN_DATA_CONTRACT.md §6.v0.2 (c34f16d13) -- canonical 5-universe set definitions.</data_contract>
    <design_contract>docs/architecture/SSCN_DESIGN_CONTRACT.md §6 (c34f16d13) -- Country-column conditional amended (all 5 new universes US-only); US_ONLY_UNIVERSES Set form retained for forward-compat per CTO~B recommendation + DE 0.3.0 lean.</design_contract>
    <coo_section_7_lock>Q7 LOCKED descriptive tokens `rmidcap/sp400/msciusa` (matches existing sp500/r1000 precedent; URL UX favors descriptive). COO~B + DE 0.3.0 converged 2026-05-19 PM; ratified by CTO~B in PRD v0.2 §7 Q7.</coo_section_7_lock>
    <de_scope_additions_2026_05_19>DE 0.3.0 surfaced `types.ts:27` UniverseId union as explicit edit (type-driven via UNIVERSE_IDS keyof but explicit edit is the convention; added to scope) + smoke-constitution choice = extend existing `sscn_divdef_001_smoke.json` with AC10 dropdown assertion (NOT a sibling smoke file) per COO~B + DE convergence.</de_scope_additions_2026_05_19>
  </references>

  <context>
    The DE TO-1 commit `45ea7210` shipped DIVZ default state + ranking-method UI + 4-group rollup strip + step=0.1 weight input + DEFAULT_CATEGORIES removal. All universe-set-independent (preset references factor codes only; `selectedUniverseId: UniverseId = 'r1000'` default carries forward to v0.2 because r1000 survives migration).

    This TO swaps the universe-set at three FE surfaces (`security-scanner.ts` UNIVERSE_IDS + `types.ts` UniverseId union + `constants.ts` US_ONLY_UNIVERSES). All US-equity, all 5 of the new tokens map to source columns the Lambda v1.1.0 (TO-AE-1) will read. Country column hides everywhere (all 5 US-only).

    Smoke constitution: extend the existing `sscn_divdef_001_smoke.json` with AC10 dropdown assertions (per DE + COO~B convergence; same DIVZ-feature lineage as TO-1, no need for a sibling smoke file).

    PROD push gating: TO-1b commits to portal/DEV; PROD push is deferred to optional TO-4 which gates on TO-1 (45ea7210) + TO-1b + TO-3 close + Andrew DEV smoke. Between TO-1b ship and TO-2 close, portal/DEV will offer the 3 new dropdown universes (rmidcap/sp400/msciusa) but their `latest/{token}/` paths won't exist until DT re-fires the Lambda. Expect 404s on those 3 paths during the window if you test the new dropdown options pre-Step-C; that's acceptable for DEV. PROD continues to serve uniform `asOf=2026-02-26` (Step A rollback state) through the entire sequence; only TO-4 ships the v1.1.0 + new dropdown + fresh data ALL ALIGNED to PROD.
  </context>

  <scope>
    <step>Phase 1 (before edit) -- compiler baseline:
      - `comp-routes trace getUniverseScanner` -- confirms `/api/general/security_scanner/latest/universes/{param}/scanner_data.json` path stable; the `{param}` is whatever portal sends (your UNIVERSE_IDS values).
      - `comp-cache collisions | grep -i scanner` -- expect clean (rankingMethod from TO-1 was already added; this TO doesn't add new cache keys).
    </step>
    <step>Phase 2 (edit) -- the 3 FE-surface changes per PRD v0.2 §6.5 + DE convergence:
      (a) `portal/src/api/endpoints/security-scanner.ts:28-35` -- swap UNIVERSE_IDS:
        ```
        sp500   -> { sourceColumn: 'wt_ivv',  label: 'S&P 500' }
        r1000   -> { sourceColumn: 'wt_iwb',  label: 'Russell 1000' }
        rmidcap -> { sourceColumn: 'wt_iwr',  label: 'Russell Midcap' }
        sp400   -> { sourceColumn: 'wt_ijh',  label: 'S&P MidCap 400' }
        msciusa -> { sourceColumn: 'wt_csus', label: 'MSCI USA Index' }
        ```
        DROP entries: r1000v, acwx, eafe, eafev (no source column in DIVZ feed).
      (b) `portal/src/pages/SecurityScanner/types.ts:27` UniverseId union -- drop `'r1000v' | 'acwx' | 'eafe' | 'eafev'`; add `'rmidcap' | 'sp400' | 'msciusa'`. Result: `'sp500' | 'r1000' | 'rmidcap' | 'sp400' | 'msciusa'`. (Type-driven from UNIVERSE_IDS keyof works but explicit edit per existing convention.)
      (c) `portal/src/pages/SecurityScanner/constants.ts:11-15` US_ONLY_UNIVERSES -- keep Set form per DE lean (forward-compat for any future ex-US universe); update entries to the new 5 tokens. Document keep-Set decision in commit message + session log per CTO~B §6.5 AC2 framework.
      (d) Bun: `bun run typecheck` clean; `bun run lint` clean; (if applicable) `bun run build`.
    </step>
    <step>Phase 3 (smoke constitution) -- extend `portal/.frontend-dev/testing/sscn_divdef_001_smoke.json` (existing TO-1 constitution; NOT a sibling file) with AC10 dropdown assertions:
      - dropdown.options.length === 5
      - dropdown.options.map(o => o.value) deep-equals `['sp500', 'r1000', 'rmidcap', 'sp400', 'msciusa']` (order: TO-1b implementation; lock the order in the assertion exactly)
      - dropdown.options.map(o => o.label).includes('Russell 1000') AND .includes('Russell Midcap') AND .includes('S&P MidCap 400') AND .includes('MSCI USA Index')
      - dropdown.options DOES NOT include 'r1000v' or 'acwx' or 'eafe' or 'eafev' (negative assertion)
      - Default-selected: Russell 1000 (preserved from TO-1 via `selectedUniverseId: UniverseId = 'r1000'`)
    </step>
    <step>Phase 4 (before commit) -- re-run Phase 1 compiler tools + `bun run typecheck` + `bun run lint` exit 0.</step>
    <step>Phase 5 (commit) -- `.tools/safe-commit.sh --author "0.3.0_DE_TradingOperations <0.3.0_DE_TradingOperations@opal.agent>" -m "..." -- <exact 4 paths>` per ADHC_OWNPTH.007 (4 paths: security-scanner.ts + types.ts + constants.ts + sscn_divdef_001_smoke.json). DE has no push to portal/PROD per role abilities; commit lands on portal/DEV. Push to portal/DEV done by DT/AE per existing portal-submodule push convention (TO-1 also followed this).</step>
    <step>Phase 6 (smoke + RAVC2) -- `/frontend-dev` Playwright smoke against the extended constitution: verifies AC1-AC8. Note: AC4 (each universe loads data) may show 404 on the 3 new universes (rmidcap/sp400/msciusa) if TO-AE-1 + TO-2 haven't shipped yet -- that's acceptable for the DEV smoke; documented in the commit + session log; the FULL data-load AC clears post-TO-2 re-fire. RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B with: commit SHA + Playwright screenshot + extended-smoke-constitution diff + AC1-AC8 confirmations (with AC4 caveat per the sequencing). DE-mode: TO status -> complete on receipt.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">`portal/src/api/endpoints/security-scanner.ts` UNIVERSE_IDS has EXACTLY 5 entries with the (token, sourceColumn, label) values from PRD v0.2 §3.5 (sp500/wt_ivv, r1000/wt_iwb, rmidcap/wt_iwr, sp400/wt_ijh, msciusa/wt_csus). git diff captured.</ac>
    <ac id="AC2">`portal/src/pages/SecurityScanner/constants.ts` US_ONLY_UNIVERSES contains all 5 new tokens (Set form retained per DE lean + CTO §6.5 AC2 framework). Decision documented in commit message + session log.</ac>
    <ac id="AC3">`portal/src/pages/SecurityScanner/types.ts:27` UniverseId union = `'sp500' | 'r1000' | 'rmidcap' | 'sp400' | 'msciusa'` (5 entries; legacy 4 dropped). git diff captured.</ac>
    <ac id="AC4">First-load page state in DEV → Universe dropdown shows the 5 new options in the v0.2 §3.5 order; Russell 1000 is preselected (preset default, inherited from `45ea7210` via TO-1). Country column hidden across all 5 universes (US-only). Switching to each of the 5 universes attempts to load data; the 3 new universes may show 404 if TO-AE-1+TO-2 haven't shipped yet (acceptable DEV state; full data-load test post-Step-C is TO-3 + TO-4 smoke).</ac>
    <ac id="AC5">Country column hidden across all 5 universes (US-only verification per PRD v0.2 §6.5 AC5 + SSCN_DESIGN_CONTRACT §6).</ac>
    <ac id="AC6">`comp-transform schema-check SecurityScanner` exits PASS (0 MISSING; 0 unexpected UNUSED).</ac>
    <ac id="AC7">`bun run typecheck` exit 0; `bun run lint` exit 0.</ac>
    <ac id="AC8">`/frontend-dev` Playwright smoke against `sscn_divdef_001_smoke.json` (extended with AC10 dropdown assertions per Phase 3) exits PASS modulo AC4 caveat above. Screenshot + result.json captured.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      `comp-routes trace getUniverseScanner` -- confirm `/api/general/security_scanner/latest/universes/{param}/scanner_data.json` route stable.
      `comp-cache collisions | grep -i scanner` -- expect clean.
    </before_write>
    <before_commit>
      Re-run Phase 1 tools (route trace + cache collisions) -- expect identical state.
      `bun run typecheck` exit 0; `bun run lint` exit 0.
    </before_commit>
    <after_commit>
      `comp-transform fields SecurityScanner` -- all rendered fields have a TypeScript type (no silent undefineds).
      `/frontend-dev` Playwright smoke per AC8.
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    None. PARALLEL-OK with SSCN_DIVDEF.004 (AE 0.5.0 Lambda redeploy) -- FE change is data-shape-independent. The 3 new dropdown universes (rmidcap/sp400/msciusa) may 404 on data load until DT 0.3.0 closes revised TO-2 (which writes `latest/{rmidcap,sp400,msciusa}/`); that's the AC4 caveat. PROD push is gated on TO-1 + TO-1b + TO-3 close + Andrew DEV smoke per TO-4 framework -- the multi-stage transient state (DEV-only) is structurally OK.
  </cross_domain_coordination>

  <deliverables>
    - `security-scanner.ts` UNIVERSE_IDS swap (5 entries).
    - `types.ts` UniverseId union swap.
    - `constants.ts` US_ONLY_UNIVERSES update (Set form retained, 5 new tokens).
    - `sscn_divdef_001_smoke.json` extended with AC10 dropdown assertions.
    - `bun run typecheck` clean transcript.
    - Playwright `/frontend-dev` smoke screenshot + result.json.
    - Session log under `org/tier2_senior/0.3.0_DE_TradingOperations/logs/YYYY-MM-DD/` with: 3-surface git diffs, AC1-AC8 evidence, AC4 caveat documentation (404 acceptable until TO-2 close), Compiler Tools section, US_ONLY_UNIVERSES Set-retention rationale.
    - RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B on close.
  </deliverables>

  <do_not>
    <rule>Do NOT touch the `45ea7210` TO-1 commit content (DIVZ preset + ranking-method UI + 4-group strip + step=0.1) -- it's universe-set-independent and stays verbatim. This TO is purely additive.</rule>
    <rule>Do NOT push to portal/PROD -- DE role has no push permission per Abilities by Role. TO-4 PROD push (DT 0.3.0 lane) gates on TO-1 + TO-1b + TO-3 close + Andrew DEV smoke.</rule>
    <rule>Do NOT delete `latest/universes/{r1000v,acwx,eafe,eafev}/` from S3 -- PRD v0.2 §3.5 preserves them as forensic / DO-NOT-DELETE. (DT does NOT touch them either per the revised TO-2.)</rule>
    <rule>Do NOT change React Query keys for `getUniverseScanner` / `getSecurityScannerFactors` -- the cache key structure is universe-token-keyed; swapping the tokens doesn't introduce collisions but introducing a NEW key shape would (do not do this).</rule>
    <rule>Do NOT change the DIVZ preset (the 13 factor codes + weights + 4-group structure) -- preset is universe-set-stable and survives the migration unchanged.</rule>
    <rule>Do NOT change route segments in `portal/src/routes/` -- the `/security-scanner?u=<token>` query-param routing absorbs the token swap automatically (the new descriptive tokens slot in cleanly).</rule>
    <rule>No emojis in code, comments, or session logs (CLAUDE.md ASCII-only rule).</rule>
  </do_not>
</task_order>
