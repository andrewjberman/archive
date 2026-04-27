# Task Order: ADVI_INFLV2.003 — DS~A: GRO Market-Growth Challenge (Txn-Only)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-003</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>MEDIUM — ship if feasible; explicit DEFER acceptable if documented</priority>
  </metadata>

  <objective>
    Andrew direction: "Difficult but not impossible to do GRO for market growth …
    only transactions, no joins for realized/unrealized … i would task DS~A with
    figuring out how."

    GRO growth decomposition in timeseries_overview.json has a `market` component.
    For BD/49F, market growth = period_end_aua - period_start_aua - nna (residual).
    For Inflection (txn-only, no Schwab custodian price feeds), this residual may
    conflate market growth with pricing noise or missing data.

    DS~A: assess whether the residual approach produces a meaningful `market` signal
    for Inflection, or whether the estimate is too noisy to be useful.
    Ship if signal-to-noise ratio is acceptable. DEFER with explicit obstacle if not.
  </objective>

  <scope>
    <task id="1" label="Evaluate residual approach on post-INFGRD.003 data">
      Compute: market_estimate = period_end_aua - period_start_aua - nna
      for each period in timeseries_overview.json post-INFGRD.003 chain.

      Assess:
        - Are the values plausible given Inflection's $200M book and known market conditions?
        - Is the series monotone / volatile / noisy? Does it correlate with expected
          broad market movements (Q1'24 rally, etc.)?
        - Is NNA measured accurately enough for the residual to be meaningful?

      Output: a short analytical note (inline in RAVC or in docs/briefs/) documenting
      the assessment.
    </task>

    <task id="2" label="Ship or DEFER">
      If signal is acceptable:
        - Confirm D_04 already emits market = residual (per 7ecc140a fix)
        - Validate the values pass comp-validate checks
        - No additional code change needed — SHIP (RAVC signals COMPLETE)

      If signal is too noisy:
        - Document: the specific obstacle (e.g., "NNA undercount makes residual negative
          in 3 of 5 periods; unreliable as market signal")
        - Set market = null or 0 with a comment in D_04 explaining the DEFER
        - RAVC signals DEFER with documented reason

      Either outcome is acceptable. Do not ship noise as signal.
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      RAVC sent to 2.0.0_SA_COO with one of:
        SHIP — GRO market residual is plausible; D_04 already emits it; comp-validate passes
        DEFER — [specific reason] — market field set to null/0 with comment in D_04
    </criterion>
    <criterion id="2">
      If SHIP: timeseries_overview.json growth_decomposition.{period}.market is non-null
      and non-zero for at least 3 of the 5 most recent periods.
    </criterion>
    <criterion id="3">
      If DEFER: D_04 comment block documents the obstacle explicitly so a future
      DS can pick it up when better data is available.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gate: INFLV2.002 complete (NMEC/NMNC/NNA confirmed — NNA accuracy
    is a prerequisite for the residual to be meaningful).</constraint>
    <constraint>Do not ship a value that is analytically misleading. DEFER is better
    than wrong signal.</constraint>
    <constraint>No emojis in code.</constraint>
    <constraint>from __future__ import annotations first import if D_04 is modified.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_INFLV2.002"
                status="open"
                note="NNA accuracy confirmed before GRO residual is meaningful."/>
  </dependencies>

  <deliverables>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO: SHIP or DEFER with documented reason.</deliverable>
    <deliverable type="commit">D_04 DEFER comment if deferring (small change). No commit needed if SHIP.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §3 (Andrew direction on GRO)</ref>
    <ref type="script">data/orion/scripts/gold/D_04.client_portal_summary.py (_build_growth_periods)</ref>
    <ref type="prior">7ecc140a — _build_growth_periods already computes residual market; assess quality</ref>
  </references>
</task_order>
```
