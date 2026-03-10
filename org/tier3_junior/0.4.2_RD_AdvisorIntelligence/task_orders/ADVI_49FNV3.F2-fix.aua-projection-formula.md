<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-09-F2-fix</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-09</date>
    <status>complete</status>
  </metadata>

  <objective>
    The AUA projection in F2 (ghost bars) uses the wrong formula. AUA is a stock value
    (point-in-time portfolio worth), not a flow. The current code at
    PartnerAnalytics.tsx line 462 does `projected = actual * ratio` where ratio is
    totalDays / elapsedDays. This multiplies the entire portfolio value by a time
    ratio, producing absurd results.

    Example: Q4 2025 ended at $1.37B. Q1 2026 actual on March 2 is $1.55B. With
    ~60 elapsed / ~90 total days, the code computes $1.55B * 1.5 = $2.325B (capped
    to ~$2.05B). The real projection should extrapolate the CHANGE ($180M in 60 days
    -> ~$270M in 90 days) giving $1.37B + $270M = $1.64B.

    The NNA and GRO projections are correct as-is because those are flow metrics
    that accumulate over time. Only the AUA projection needs to change.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
    </files>
  </scope>

  <context>
    The bug is in the augmentedAuaData useMemo (line 443-471). The current logic:

    ```
    const actual = Number(entry[cat]) || 0
    const projected = actual * ratio          // WRONG for stock metrics
    const priorValue = prior ? ... : actual
    const cap = priorValue * 1.5
    const capped = Math.min(projected, Math.max(actual, cap))
    aug[`${cat}_ghost`] = Math.max(0, capped - actual)
    ```

    The NNA projection (line 473-501) and GRO projection (line 503+) are correct
    and must NOT be changed. They are flow metrics where `actual * ratio` is valid.
  </context>

  <requirements>
    <requirement id="1">Replace the AUA projection formula with delta-based
      extrapolation:
      ```
      priorEnd = prior ? Number(prior[cat]) || 0 : actual
      delta = actual - priorEnd
      projectedDelta = delta * ratio
      projectedValue = priorEnd + projectedDelta
      ```
      The ghost extension is `projectedValue - actual`.</requirement>
    <requirement id="2">Cap: the projected value should not exceed
      `priorEnd + abs(priorPeriodChange) * 1.5` where priorPeriodChange is the
      change during the prior completed period. If there is no prior-prior period
      to compute this, fall back to `abs(delta) * 1.5` as the cap on the
      projected delta.</requirement>
    <requirement id="3">Ghost must be non-negative (ghost bar extends upward from
      actual, never downward). If projectedValue < actual, ghost = 0.</requirement>
    <requirement id="4">Do NOT change the NNA or GRO projection logic. Those are
      flow metrics and the current formula is correct for them.</requirement>
    <requirement id="5">Verify with the numbers Andrew cited: Q4 2025 = $1.37B,
      Q1 2026 actual = $1.55B at ~60/90 days elapsed. The projection should land
      near $1.64B, not $2B+.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">AUA ghost bars show reasonable projections that extrapolate
      the period-over-period change, not the absolute level.</criterion>
    <criterion id="2">NNA and GRO ghost projections unchanged.</criterion>
    <criterion id="3">TypeScript clean (bunx tsc -b).</criterion>
    <criterion id="4">Portal DEV commit with --author flag.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This is a formula fix only. Do not change the rendering, opacity,
      stacking, or visual behavior of ghost bars.</constraint>
    <constraint>Do not touch augmentedNnaData or augmentedGroData.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Portal DEV commit fixing AUA projection formula.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md (F2 section, corrected 2026-03-09)</ref>
    <ref type="source">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx (lines 443-471)</ref>
  </references>
</task_order>
