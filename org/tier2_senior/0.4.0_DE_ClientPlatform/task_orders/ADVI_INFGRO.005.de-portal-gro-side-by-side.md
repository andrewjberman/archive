<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFGRO.005</id>
    <project>ADVI_INFGRO</project>
    <title>Portal GRO decomposition — AdvisorsTab + InflectionInsightsPanel side-by-side display</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>cancelled</status>
    <cancelled_date>2026-05-23</cancelled_date>
    <cancelled_reason>Andrew-directed surgical rollback 2026-05-23. TO architecturally misaligned: targeted shared AdvisorsTab.tsx but Inflection's user-visible UX is Distribution + Books only (AdvisorsTab is a 49F-only surface in the live nav). DE 0.4 ship `abe33b0c` (Return per-advisor column gated on advisor_return_pct_twr !== undefined — only Inflection emits, so dead code on both surfaces: 49F hides via gate, Inflection doesn't navigate to AdvisorsTab) reverted by CTO `5cee8276` on portal DEV. ADVI_INFGRO project closed. Data layer (.001-.009) retained — leaderboard.json continues to emit the per-advisor fields for any future re-target on an Inflection-appropriate surface.</cancelled_reason>
    <dispatch_held>false</dispatch_held>
    <dispatch_note>Receiver routing TBD — COO bench-state check 2026-05-12 morning. DS~A + DS~C killed or STANDDOWN 2026-05-11 ~22:31Z. Do NOT pick up this TO until COO issues GO.</dispatch_note>
    <priority>P1</priority>
    <estimated_effort>4-6 hours</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRO_PRD.md §3.3 + §4.6 + §6.TO-INFGRO.005</ref>
    <ref type="components">portal/src/pages/AdvisorIntelligence/_shared/tabs/AdvisorsTab.tsx</ref>
    <ref type="components">portal/src/pages/AdvisorIntelligence/_shared/types.ts (PlatinumLeaderboardResponse)</ref>
    <ref type="data_source">getFirmLeaderboard() → platinum/firm/leaderboard.json (extended by TO-INFGRO.004)</ref>
    <ref type="schema_check_result">comp-transform schema-check AdvisorsTab: 5 type fields / 1 rendered / UNUSED: available_windows + windows</ref>
    <ref type="gates">TO-INFGRO.004 COMPLETE — DS~A MCP-signals leaderboard.json with per-advisor GRO fields.</ref>
  </references>

  <context>
    The Inflection partner portal's AdvisorsTab currently shows advisor-level AUA and NNA.
    After the INFGRO data pipeline ships (TOs 001-004), leaderboard.json will include three
    new first-class fields per advisor: advisor_return_pct_twr, advisor_nna_$, advisor_epsilon_$.

    The portal goal: surface these three fields as a side-by-side column layout with:
      - Three hero cards at the top: AUA delta / Return (TWR%) / NNA (no toggle between them)
      - Per-advisor columns in the table: AUA / Return / NNA / epsilon (side-by-side, not stacked)
      - Epsilon data quality indicator in the column header (small icon + tooltip exposing
        the epsilon value and its GREEN/YELLOW classification for the selected advisor)
      - Cut-chip window labels STAY from ADVI_INFTGT TO-3 (already shipped)
      - NO toggle between GRO mode and other modes — render all three always

    Schema check found 2 UNUSED type fields: `available_windows` and `windows`. These may
    be the existing type placeholders for window data. Check if they need to be extended
    or if the new GRO fields need new type fields added.

    Design ref: PRD §3.3 has the full layout spec. The key principle is "three first-class
    fields" — not a toggle, not a collapsible section.
  </context>

  <scope>
    <step>
      Run comp-transform schema-check AdvisorsTab --feature gro_decomposition.
      Run comp-transform ternary-audit AdvisorsTab.
      Note all MISSING, UNUSED, WARN outputs. Check if PlatinumLeaderboardResponse type
      needs new fields for advisor_return_pct_twr, advisor_nna_$, advisor_epsilon_$.
    </step>
    <step>
      Read the actual leaderboard.json schema from platinum/firm/leaderboard.json
      (after TO-004 ships — wait for DS~A MCP signal). Identify the exact new field names
      so TypeScript types can be extended correctly.
    </step>
    <step>
      Extend PlatinumLeaderboardResponse (or per-advisor type) in types.ts with the new fields:
        - advisor_return_pct_twr: number (AUA-weighted TWR%)
        - advisor_nna_dollar: number (or use $ equivalent field name from JSON)
        - advisor_epsilon_dollar: number
        - advisor_epsilon_data_quality: "GREEN" | "YELLOW" | "MISSING_PERF"
      Use exact field names from the live leaderboard.json.
    </step>
    <step>
      Implement per PRD §3.3 + §4.6:
        a. Three hero cards at top of AdvisorsTab: AUA Growth / Return (TWR%) / NNA
           Each card shows firm-level value for selected window.
        b. Per-advisor table columns (side-by-side): AUA delta / Return % / NNA $ / epsilon $
        c. Epsilon quality indicator: column header icon (info circle) + tooltip:
           "epsilon: $X [GREEN/YELLOW] — accounting residual not attributable to NNA or Return"
           Color-coded: green dot = GREEN, yellow dot = YELLOW, grey = MISSING_PERF.
        d. Preserve all existing columns and cut-chip labels unchanged.
    </step>
    <step>
      Run visual test via /frontend-dev after dev server start (bun run dev --port 5175).
      Verify golden path: log in as Andrew → select Inflection partner → AdvisorsTab renders
      three columns + three hero cards + epsilon indicator visible.
      Verify no regressions in other portal pages.
    </step>
    <step>
      Run comp-routes trace getFirmLeaderboard post-change.
      Run comp-cache collisions.
      Resolve any cache key collisions before commit.
    </step>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      - comp-transform schema-check AdvisorsTab --feature gro_decomposition
      - comp-transform ternary-audit AdvisorsTab
      - comp-routes trace getFirmLeaderboard
      - comp-cache collisions
    </phase>
    <phase name="before_commit">
      - TypeScript type check: bun run typecheck or equivalent
      - comp-transform schema-check AdvisorsTab (confirm no new MISSING after type extension)
    </phase>
    <phase name="after_commit">
      - /frontend-dev visual test — screenshot golden path
      - comp-routes trace getFirmLeaderboard (confirm path unchanged)
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Upstream: DS~A TO-INFGRO.004 must complete first (leaderboard.json extended with GRO fields).
    Wait for DS~A MCP signal before starting. Confirm exact field names from live leaderboard.json
    before extending TypeScript types — do NOT guess names from PRD; use actual JSON.

    This TO is portal-only. No shared S3 artifacts with other active TOs.
    TO-INFGRO.006 (MAX window re-enable) depends on this TO completing first.
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">Three hero cards render at top of AdvisorsTab: AUA Growth / Return (TWR%) / NNA.
      Values match leaderboard.json firm-level fields.</criterion>
    <criterion id="AC2">Per-advisor columns render side-by-side: AUA / Return / NNA / epsilon.
      No toggle required to see all three.</criterion>
    <criterion id="AC3">Epsilon quality indicator visible in column header with tooltip showing
      epsilon value + GREEN/YELLOW/MISSING_PERF classification.</criterion>
    <criterion id="AC4">All pre-existing AdvisorsTab columns and cut-chip labels unchanged
      (visual regression check via /frontend-dev).</criterion>
    <criterion id="AC5">TypeScript type check PASS — no new MISSING fields in schema-check output.</criterion>
    <criterion id="AC6">comp-cache collisions: no new same-key / different-type collisions.</criterion>
    <criterion id="AC7">Visual test: screenshot of Inflection AdvisorsTab with GRO columns visible
      attached to session log.</criterion>
  </acceptance_criteria>

  <session_log_requirement>
    Session log in org/tier2_senior/0.4.0_DE_ClientPlatform/logs/{date}/
    Include Compiler Tools section + /frontend-dev screenshot reference.
    MCP DS~A (TO-INFGRO.006 coordinator) when portal changes committed.
  </session_log_requirement>
</task_order>
