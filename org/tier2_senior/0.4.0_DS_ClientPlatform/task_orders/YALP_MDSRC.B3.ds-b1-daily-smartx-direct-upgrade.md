<task_order>
  <metadata>
    <id>YALP_MDSRC.B3</id>
    <slug>ds-b1-daily-smartx-direct-upgrade</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — unified COO+CTO ruling 2026-05-21 (B1 Path-A premise empirically superseded). B3 is the daily-SmartX-direct upgrade follow-on to B1. It begins once B1 ships v1 via B2 (the artifact B3 upgrades must exist deployed first); B3's endpoint-validation work (Phase 0) can start immediately in parallel — SmartX is NOT under the YCharts freeze. HARD SEQUENCE CONSTRAINT: B3 MUST land before the Q8-gated portal-wiring step (see scope) — that is the load-bearing condition that makes shipping Path-A v1 quality-equivalent to a full re-scope.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — the quality-completion of the B1 SmartX segment. B1 v1 ships as a correct labeled hybrid; B3 swaps the daily-estimation leg for the authoritative SmartX daily series so the portal surface is never wired to the interim estimate.</priority>
    <sla>~1-2 effort-days.</sla>
  </metadata>

  <references>
    <ruling>Unified COO+CTO ruling 2026-05-21 — B1 Option A-with-conditions. COO relay to 0.4.0_DS 20260521T182915Z; CTO converge 20260521T18xxZ. Formally revises session-29 Q8 (CTO folds into v0.4): end-state = SmartX daily-direct authoritative; model.pkl estimation leg retires for performance (model.pkl stays the proprietary design view per Q4).</ruling>
    <endpoint>GET /api/3.1/models/{modelId}/performance?grouping=daily|weekly|monthly — discovered by 0.2.0_DS's api/3.1 exhaustion sweep (S2, e2bd44014) and LIVE-VERIFIED by 0.4.0_DS for one modelId: 431-record daily series, FRESH to T-1, each record pnl{dollar,percent} + summary{beginningMarketValue, endingMarketValue, increaseByAmount, decreaseByAmount, isFullRange, transactions, fees}. pnl.percent = a per-day FLOW-ADJUSTED return (summary carries the cash flows + isFullRange clean-period flag). NOT closingEquity — already flow-adjusted.</endpoint>
    <b1>YALP_MDSRC.B1 (0.4.0_DS) — the SmartX REST model-portfolio performance pull, Path A as built: SmartX monthly+ authoritative / model.pkl + 1a-allocations for the daily-estimation leg. Correct labeled hybrid; ships v1 via B2.</b1>
  </references>

  <context>
    B1 Phase 0's central finding — and the session-29 Q8 Path-A ruling — rested on "SmartX model-performance is monthly-cadence; there is no daily model-return series; the daily portal surface cannot be SmartX-sourced." That premise is empirically false: /api/3.1/models/{id}/performance?grouping=daily returns a clean daily flow-adjusted model-return series. B1 v1 (Path A) is NOT a defect — it is a correct, explicitly-labeled hybrid — but its daily-estimation leg (model.pkl / 1a-allocations) is now an interim estimate where an authoritative source exists. B3 swaps it.
  </context>

  <scope>
    <in_scope>
      PHASE 0 — ENDPOINT GENERALIZATION VALIDATION (can start now; SmartX unfrozen):
      - 0.4.0_DS verified the endpoint for ONE modelId. Phase 0 confirms it GENERALIZES: pull /api/3.1/models/{modelId}/performance?grouping=daily for MULTIPLE models (a representative spread of the model universe).
      - Per model confirm: genuine daily resolution (inter-record spacing = trading days, NOT weekly-resampled-mislabeled — the A4/A5 sweep-artifact lesson), plausible history depth, plausible values, freshness to ~T-1, isFullRange semantics consistent.
      - If the endpoint does NOT generalize (some models empty / coarser / mislabeled) — STOP and RAVC1 COO with the per-model finding before the swap; the upgrade scope may need to be partial.

      PHASE 1 — THE SWAP:
      - Replace B1's daily-estimation leg (model.pkl / 1a-allocations for the daily periods + model_portfolio_timeseries.json) with /api/3.1/models/{id}/performance?grouping=daily as the authoritative daily model-return source.
      - The daily series becomes SmartX-direct; the hybrid estimation leg retires FOR PERFORMANCE. model.pkl stays the proprietary design view per Q4 — do not remove it, just stop sourcing performance from it.
      - Preserve B1's correctness properties: flow-adjusted returns, explicit labeling, the artifact contract downstream consumers expect.

      PHASE 2 — DELIVER:
      - The upgraded B1 pull + a brief documenting the swap, the Phase-0 generalization evidence, and the artifact-contract delta (if any) for downstream.
    </in_scope>
    <out_of_scope>
      - Re-deploying is the AE half (a B3-deploy follow-on, same B1/B2 split) — flag when B3 code is ready.
      - YCharts work — unrelated; YCharts stays frozen, SmartX does not.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>B3 modifies the B1 SmartX pull (infra/aws/lambda Lambda code / data/smartx pull) — not a gold/portal/route/IAM-schema change. Phase assertions are empirical self-checks; run ds-commit-gate before commit per CLAUDE.md Rule 14.</note>
    <phase id="0" when="after the multi-model endpoint pull">
      <step>
        <run>For each probed model: compute inter-record date spacing + record count + first/last dates on the grouping=daily series.</run>
        <expect>Spacing = trading-day cadence (not 7d); record count consistent with the date span; last record ~T-1; non-empty for every model in the representative spread.</expect>
        <if_mismatch>Weekly-spacing or empty series on any model = the endpoint does not generalize as assumed — STOP, RAVC1 COO before the Phase-1 swap.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh on the changed files (py_compile + ds-precommit-check + ruff py39).</run>
        <expect>All three exit 0.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - HARD SEQUENCE GATE (load-bearing): B3 MUST land before the Q8-gated portal-wiring step — the step that wires the B1 daily series to the portal/user surface. This guarantees users only ever see the authoritative SmartX-direct daily series, never B1 v1's interim estimate. COO + CTO track this sequence; if portal-wiring is scheduled to land first, flag COO immediately.
    - B1 v1 (Path A): its daily leg stays explicitly LABELED design/estimate until B3 lands and the swap is live.
    - The B3 deploy is an AE-half follow-on (same DS-author / AE-deploy split as B1/B2) — flag COO when B3 code is committed + verified so the deploy TO is authored.
    - SmartX is NOT under the YCharts execution freeze — B3's live endpoint work proceeds.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — Phase 0: /api/3.1/models/{id}/performance?grouping=daily validated across multiple models — genuine daily cadence, plausible depth/values, ~T-1 fresh; evidence committed in the brief. Any non-generalizing model explicitly flagged.
    - AC2 — Phase 1: B1's daily-estimation leg replaced by the SmartX-direct daily series; flow-adjustment + explicit labeling + the downstream artifact contract preserved.
    - AC3 — model.pkl retired for PERFORMANCE sourcing only; retained as the Q4 proprietary design view.
    - AC4 — ds-commit-gate clean; session log Compiler Tools section reproduces the Phase-0/Phase-2 checks.
    - AC5 — RAVC2 to COO + CC CTO; brief documents the swap + the Phase-0 generalization evidence + any artifact-contract delta. B3 code-ready triggers the AE deploy-half TO.
  </acceptance_criteria>
</task_order>
