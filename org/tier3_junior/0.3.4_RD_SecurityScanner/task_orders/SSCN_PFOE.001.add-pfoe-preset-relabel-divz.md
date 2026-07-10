<task_order>
  <metadata>
    <id>SSCN_PFOE.001-RD</id>
    <slug>add-pfoe-preset-and-relabel-divz</slug>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.3.4_RD_SecurityScanner</issued_to>
    <date>2026-07-10</date>
    <status>complete</status>
    <!-- COMPLETE 2026-07-10: committed portal DEV 7db8f6b5 (constants.ts; DE review WAIVED by Andrew,
         RD self-commit per COO~C GO 211717Z); DT DEV->PROD promote LIVE on portal-v2.1.134; COO~C
         RAVC-ACCEPTED + served-verified 214639Z (CI SUCCESS, tag peels to PROD head, deploy ledger
         CLOSED 4 legs, live www.opalinvest.dev bundle carries PFOE codes + DIVZ relabel, weights 16/16
         vs Yang). Flipped on the RAVC owner's explicit acceptance (not a premature self-close).
         Only remaining item is Andrew's visual final smoke (his gate; does not need RD). -->
    <completed>2026-07-10</completed>
    <ship_evidence>portal DEV 7db8f6b5 -> PROD portal-v2.1.134; COO~C RAVC-ACCEPTED 214639Z (served-verified)</ship_evidence>
    <project_code>SSCN_PFOE</project_code>
    <priority>P1 -- Andrew-direct 2026-07-10 ("SSCN_PFOE and POSN_CUSTOM are priorities now, go and proceed them" / "the easiest one to enact immediately"). GO is LIVE. Begin immediately on spawn.</priority>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_PFOE.md -- PRD v0.1 (1.0.0_SA_CTO~C, @ e010d37b3). READ IT -- esp. Appendix A (the 16-factor spec, reproduced below), sec.4 (component specs + the two real hazards), sec.6 (this TO's authority). All sec.7 OQs are RESOLVED; no spec gate remains.</prd>
    <arch_gate>1.0.0_SA_CTO~C arch-gates your build diff. RAVC back to CTO~C (via COO~C). Do NOT self-close.</arch_gate>
    <baseline>Extends SSCN_DIVDEF (COMPLETE 2026-05-20, portal-v2.1.95) -- the PRESETS registry model in portal/src/pages/SecurityScanner/constants.ts. DIVZ is the lone existing preset. This TO adds a 2nd (PFOE) + relabels DIVZ. See SSCN_DIVDEF.008 in this same folder for the registry pattern you are extending.</baseline>
  </references>

  <context>
    Yang asked (Andrew<->Yang call 2026-07-10) for a second built-in Security Scanner preset "PFOE" -- a 16-factor growth/quality/sentiment/valuation/momentum screen -- plus a cleanup of the DIVZ dropdown label ("take out the dividend and the double dash"). Empirically GROUNDED FE-ONLY: presets live in constants.ts, scoring is 100% client-side (compositeScore = Sum(pctls[code]*weight)/100), and ALL 16 PFOE codes are present in the served factor_metadata.json (289 factors, asOf 20260521) -- so there is NO backend / Lambda / S3 / DS work. This is a single-file config extension (+ a type-union widening).
  </context>

  <scope>
    Primary file: portal/src/pages/SecurityScanner/constants.ts (only). Possibly types.ts IF PresetGroup is re-exported there (Phase-1 grep confirms).

    === 1. Extend the PresetGroup union + PRESET_GROUP_ORDER ===
    PresetGroup (constants.ts:27) is currently 'Dividend' | 'Momentum' | 'Value' | 'Quality'.
    ADD 'Growth' | 'Sentiment' | 'Valuation' to BOTH the union AND PRESET_GROUP_ORDER (constants.ts:30).
    (tsc fails if any PFOE entry's group is not in the union -- do this in the same edit.)

    === 2. Add PFOE_PRESET (16 entries) + the PRESETS registry entry ===
    Declare a readonly PresetEntry[] named PFOE_PRESET with these 16 {code, weight, group} entries
    (Appendix A of the PRD, verbatim -- codes chosen by served coverage per Andrew-direct; Sum = 100):

      Growth      sales_fwd_gr_1yr    7
      Growth      sales_gr_3yr        7
      Growth      sales_fwd_gr_3yr    7
      Growth      eps_fwd_gr_1yr      7
      Growth      eps_gr_3yr          7
      Growth      eps_fwd_gr_3yr      7
      Quality     gross_mgn           6
      Quality     oper_mgn            6
      Quality     fcf_mgn             6
      Quality     roe                 6
      Quality     int_cov             6
      Sentiment   eps_stability       5     (higher-coverage 96.7% pick per Andrew rule; see Yang-flag below)
      Sentiment   eps_est_rev_45d     5
      Valuation   peg_ntm             8
      Momentum    ret_mom_252d        5
      Momentum    short_pct_chg_12m   5
                                    ----
                                     100    (Growth 42 / Quality 30 / Sentiment 10 / Valuation 8 / Momentum 10)

    Then append to PRESETS: { id:'pfoe', label:'PFOE', universe:'r1000', entries: PFOE_PRESET }.

    === 3. Relabel DIVZ ===
    PRESETS['divz'].label: 'DIVZ -- Dividend' -> 'DIVZ'.  id / entries / universe UNTOUCHED
    (so activePresetId matching + the DIVZ default-on-load seed are unaffected).

    HAZARDS (PRD sec.4.1 -- do NOT skip):
    - applyPreset silently drops any code absent from the page's loaded allFactors -> applied weights
      sum <100 and mis-rank. Phase-1 re-verify all 16 codes against the allFactors the page actually
      loads (Factor Bank / factor_metadata fetch), not only the S3 file. Phase-3 assert applied
      totalWeight === 100 after selecting PFOE.
    - Any PFOE group not in the widened PresetGroup union fails tsc.

    DO NOT change DIVZ's factor codes/weights/groups. DO NOT change the default-on-load preset (stays DIVZ).
    DO NOT add any second control / panel / layout change -- adding a registry entry auto-adds the
    dropdown option; no edit to ScannerHeaderPanel.tsx / useScannerState.ts / SecurityScanner.tsx is needed.
  </scope>

  <compiler_tools_mandate>
    <phase_1_before_write>grep -rn "PRESET_GROUP_ORDER\|PresetGroup" portal/src to confirm no render consumer breaks on the union extension; re-verify the 16 codes against the allFactors the page loads (Factor Bank / factor_metadata fetch), not just the S3 file.</phase_1_before_write>
    <phase_2_before_commit>comp-cache collisions (must stay 0 mismatch, no new scanner key); comp-transform schema-check SecurityScanner (must stay clean); bun run typecheck (union coverage) + bun run lint -- both exit 0, paste transcript in session log.</phase_2_before_commit>
    <phase_3_after_commit>DEV smoke -- select PFOE: assert 16 factors applied, totalWeight === 100 (green badge), grid re-ranks; select DIVZ: label reads "DIVZ", 13 factors, totalWeight === 100; default-on-load still DIVZ.</phase_3_after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>  <!-- PRD Appendix D: comp-cache collisions clean for all scanner keys; PFOE reuses DIVZ's r1000 universe/endpoint (no new query key); only file touched is SecurityScanner/constants.ts, owned by SSCN_PFOE. No shared files or S3 keys with any other active project. -->
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">PRESETS has exactly 2 entries, ids ['divz','pfoe']; divz.label === 'DIVZ'; pfoe.label === 'PFOE'.</ac>
    <ac id="AC2">PFOE_PRESET has 16 entries; Sum weight === 100; every code is present in the served factor_metadata.json.</ac>
    <ac id="AC3">Each PFOE entry group is in the extended PresetGroup union; bun run typecheck passes.</ac>
    <ac id="AC4">DEV: selecting PFOE yields a 16-factor screen with the totalWeight badge = 100 (green) and a non-empty ranked grid; selecting DIVZ yields 13 factors, badge 100; default-on-load still DIVZ.</ac>
    <ac id="AC5">bun run typecheck + bun run lint both exit 0 (transcript in session log). /frontend-dev smoke green (DE runs it).</ac>
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT change DIVZ's factor codes/weights/group metadata, nor the default-on-load preset (stays DIVZ). Only DIVZ's label string changes.</rule>
    <rule>Do NOT add a second new control / panel / tab / layout restructure. The registry entry auto-adds the dropdown option -- no other file edit is required.</rule>
    <rule>Do NOT commit or push to PROD. Build on portal DEV working tree; hand to 0.3.0_DE_TradingOperations for the compiler mandate + review + commit; 0.3.0_DT owns the DEV->PROD promote.</rule>
    <rule>No emojis / non-ASCII in code or the session log (CLAUDE.md ASCII-only).</rule>
  </do_not>

  <deliverables>
    - constants.ts implementation on the portal DEV working tree (PFOE preset + union extension + DIVZ relabel).
    - bun run typecheck + bun run lint both exit 0; transcript in your session log.
    - Session log under org/tier3_junior/0.3.4_RD_SecurityScanner/logs/2026-07-10/ (Compiler Tools section mandatory).
    - MCP 0.3.0_DE_TradingOperations when ready for DE review + compiler mandate + commit.
  </deliverables>

  <yang_flag_nonblocking>
    eps_stability (Quality "EPS Stability", the higher-coverage 96.7% pick per Andrew's coverage rule) differs from the exact-name analyst factor eps_stable_est (81.2%, Yang's Sentiment sleeve). Built per Andrew's coverage rule; a one-line code swap if Yang wants the analyst-estimate factor. COO~C routes this to Yang -- does NOT block the build.
  </yang_flag_nonblocking>

  <handback>
    When done: MCP 0.3.0_DE_TradingOperations "SSCN_PFOE.001 RD implementation ready" + files changed + typecheck/lint result. DE runs the 3-phase compiler mandate, reviews vs all 5 ACs, commits, and the build diff routes to 1.0.0_SA_CTO~C for arch-gate; RAVC to COO~C. Do NOT flip this TO to complete yourself.
  </handback>
</task_order>
