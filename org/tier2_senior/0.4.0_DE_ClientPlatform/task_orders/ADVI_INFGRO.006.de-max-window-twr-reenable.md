<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFGRO.006</id>
    <project>ADVI_INFGRO</project>
    <title>Re-enable MAX window in TWR mode (CVO-gated on coverage + summaries coverage proof)</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_note>Receiver routing TBD — COO bench-state check 2026-05-12 morning. DS~A + DS~C killed or STANDDOWN 2026-05-11 ~22:31Z. Do NOT pick up this TO until COO issues GO.</dispatch_note>
    <priority>P1</priority>
    <estimated_effort>2-3 hours</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRO_PRD.md §6.TO-INFGRO.006 + §7 Q5</ref>
    <ref type="gates">TO-INFGRO.005 COMPLETE (portal side-by-side rendering live). Plus: empirical coverage proof that all 4 advisors have inception-to-date TWR data AND summaries block populated cleanly at MAX horizon.</ref>
    <ref type="cvo_ruling">Q5: "MAX window in TWR mode requires inception-to-date coverage clean for all 4 advisors + vendor summaries behave cleanly at MAX horizon." Coverage verification is DS~A responsibility; DE implements the conditional re-enable.</ref>
  </references>

  <context>
    The MAX window in AdvisorsTab is currently disabled (all modes). ADVI_INFTGT TO-4
    reverted auto-select of Washington on MAX. Per PRD §6, MAX-TWR is safe to re-enable
    under specific conditions: (1) all 4 Inflection advisors have inception-to-date TWR
    factor data (no gaps at MAX horizon), AND (2) vendor summaries block is populated
    cleanly at MAX horizon for all 4 advisors' clients.

    This is a conditional re-enable: MAX window is available ONLY when GRO mode = TWR.
    AUA-delta MAX stays DISABLED (fundamental denominator issue — no inception-to-date
    AUA start available reliably).

    DS~A is the coverage verifier (check silver/performance_dim/ coverage at MAX horizon
    for all 4 advisors' client sets). DE implements the conditional MAX enable in the portal
    once DS~A confirms coverage clean.

    Wait for DS~A coverage signal before implementing. Do not enable MAX speculatively.
  </context>

  <scope>
    <step>
      Wait for DS~A coverage verification signal (MCP or inline RAVC). DS~A should:
        - Query silver/performance_dim/ for the earliest available date per client
        - Confirm all 4 advisors' clients have full inception-to-date coverage (no gaps at MAX)
        - Confirm summaries_gain_dollar non-null at earliest-date partition
      If DS~A coverage is clean → proceed. If any gap → surface to CTO before implementing.
    </step>
    <step>
      In AdvisorsTab.tsx, implement conditional MAX enable:
        - When GRO display mode = TWR: include MAX in available_windows
        - When GRO display mode = AUA-delta: keep MAX disabled (existing behavior)
      The PRD mandates no toggle — if we're showing TWR columns (which we always are after
      TO-005), MAX is available. If there are per-advisor coverage gaps, the epsilon quality
      indicator ("MISSING_PERF") will surface the gap for specific advisors even when MAX
      is available at the window level.
    </step>
    <step>
      Run visual test at MAX window:
        - inception-to-date return_pct_twr renders for all 4 advisors
        - No "MISSING_PERF" on any advisor at MAX horizon (per DS~A coverage proof)
        - epsilon indicator shows GREEN or YELLOW (not MISSING_PERF) for all 4 advisors
    </step>
    <step>
      Manual spot-check: Peter Lee MAX return_pct_twr matches Orion UI inception-to-date
      performance for Peter's book. Document spot-check values in session log.
    </step>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      - comp-transform schema-check AdvisorsTab (confirm available_windows type is already extended)
      - Confirm DS~A coverage signal received (MCP or RAVC) — do NOT start without it
    </phase>
    <phase name="before_commit">
      - TypeScript type check
      - comp-transform schema-check AdvisorsTab (no new MISSING)
    </phase>
    <phase name="after_commit">
      - /frontend-dev visual test at MAX window — screenshot
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    DS~A must confirm coverage before DE starts implementation. This is a cross-lane gate:
    DE cannot complete TO-006 without DS~A's empirical coverage proof.
    DS~A: after completing TO-004, sample silver/performance_dim/ at earliest available dates
    for all 4 advisors' client IDs. Report: "MAX coverage CLEAN — all 4 advisors / inception-to-date
    TWR factors present / summaries_gain non-null" or enumerate gaps.
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">MAX window available in AdvisorsTab when TWR columns are displayed.</criterion>
    <criterion id="AC2">AUA-delta MAX remains disabled (existing behavior preserved).</criterion>
    <criterion id="AC3">All 4 advisors render non-MISSING_PERF epsilon at MAX horizon.</criterion>
    <criterion id="AC4">Peter Lee MAX return_pct_twr spot-checked vs Orion UI (within 0.1%).</criterion>
    <criterion id="AC5">DS~A coverage proof documented in session log (MCP signal text quoted).</criterion>
    <criterion id="AC6">Visual test screenshot at MAX horizon showing all 4 advisors.</criterion>
  </acceptance_criteria>

  <session_log_requirement>
    Session log in org/tier2_senior/0.4.0_DE_ClientPlatform/logs/{date}/
    Include Compiler Tools section + DS~A coverage signal quote + MAX horizon screenshot.
  </session_log_requirement>
</task_order>
