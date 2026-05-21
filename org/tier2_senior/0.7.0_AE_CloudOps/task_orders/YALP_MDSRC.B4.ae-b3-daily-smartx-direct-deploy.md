<task_order>
  <metadata>
    <id>YALP_MDSRC.B4</id>
    <slug>ae-b3-daily-smartx-direct-deploy</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — the AE deploy-half of YALP_MDSRC.B3 (the daily-SmartX-direct upgrade). 0.4.0_DS completed + locally-verified B3 Phase 0+1 (brief docs/briefs/yalp-mdsrc-b3-daily-smartx-direct-swap-20260521.md, cb11be941); two AE-lane files sit uncommitted in the shared working tree for the AE to commit + deploy. Same DS-author / AE-deploy split as B1/B2. SEQUENCE on the AE: C6 (done) -> C1 -> B4. SmartX is NOT under the YCharts freeze — B4 deploys + runs normally.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — completes the B-segment quality arc: B3's daily axis goes SmartX-realized end-to-end. Holds the B3 load-bearing condition (land before the Q8-gated portal-wiring step).</priority>
    <sla>~0.5-1 effort-day — a 2-file commit + 2x deploy cycle; the code is authored + locally-verified by 0.4.0_DS.</sla>
  </metadata>

  <references>
    <b3>YALP_MDSRC.B3 (0.4.0_DS) — the daily-SmartX-direct upgrade. Phase 0 PASS (endpoint generalizes, all 5 models, genuine trading-day cadence). Phase 1 built + locally verified: daily-vs-monthly fidelity cross-check delta=0.00 on all 5 models (two independent SmartX endpoints agree to the cent); local producer integration test PASS (all 9 periods smartx_realized, all 5 models). Brief: docs/briefs/yalp-mdsrc-b3-daily-smartx-direct-swap-20260521.md (cb11be941). CONSUME THE BRIEF — §4 has the artifact-contract deltas.</b3>
    <b2>YALP_MDSRC.B2 — the prior B1 deploy; B4's deploy order mirrors it (pull Lambda first + invoke, then producer).</b2>
    <ruling>Unified COO+CTO B1 A-with-conditions ruling — B3 = the daily-SmartX-direct upgrade; CTO folds the Q8 revision (SmartX daily-direct authoritative; model.pkl retires for performance, stays the Q4 design view) into v0.4.</ruling>
  </references>

  <context>
    B3 (0.4.0_DS) swapped B1's daily-estimation leg for the verified /api/3.1/models/{id}/performance?grouping=daily endpoint — 1D/WTD and model_portfolio_timeseries.json model_return are now SmartX-realized end-to-end; model.pkl retired for performance sourcing (kept as the Q4 design view). The code is AE-lane infra/aws + data/smartx code that 0.4.0_DS authored + locally verified but cannot commit. B4 is the AE half: commit + deploy the two files.
  </context>

  <scope>
    <in_scope>
      Commit + deploy the two B3 AE-lane files (uncommitted in the shared working tree):
      - data/smartx/scripts/pull_smartx_model_monthly_performance.py — the SmartX pull, now extended to also emit a 2nd sidecar json/benchmarks/_smartx_model_daily.json (the per-trading-day series). B1's monthly logic untouched.
      - infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py — the producer, now sourcing 1D/WTD + model_portfolio_timeseries.json model_return from the daily sidecar.
      DEPLOY ORDER (mirrors B2): the SmartX pull Lambda FIRST + invoke once so _smartx_model_daily.json exists in S3 before the producer's first run — no transient window where the producer reads a missing daily sidecar. Then the producer.
      Each: review (lane-convention only, do not re-author — 0.4.0_DS built + verified it), ds-commit-gate, safe-commit, package, terraform deploy, source-map, full cycle (plan -> safe-apply HALTGT -> 0-diff -> tag -> push --follow-tags -> record-terraform-deploy with an explicit agent --author).
      On the deploy: signal 0.4.0_DS — they run the B3 e2e verification (B1-harness pattern) + send the closing B3 RAVC2.
    </in_scope>
    <out_of_scope>
      - Re-authoring the B3 code — 0.4.0_DS owns it, locally verified; B4 is review + commit + deploy only.
      - The MDLP_RVVALT timeseries-consumer decision — see cross_domain_coordination; that is a CTO/consumer call, not a B4 deploy step.
      - YCharts work — B4 is SmartX, not under the YCharts freeze.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh on both files; comp-iam service on the SmartX pull Lambda if its IAM changed (the 2nd sidecar write may need an s3:PutObject prefix add).</run>
        <expect>ds-commit-gate exits 0 on both. If the daily sidecar writes a new S3 key/prefix, comp-iam confirms s3:PutObject covers it — else flag MISSING.</expect>
        <if_mismatch>Fix the IAM/gate issue before commit; a missing PutObject prefix would fail the daily-sidecar write at runtime.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before apply">
      <step>
        <run>comp-iam gaps if iam.tf changed.</run>
        <expect>Zero new permission gaps.</expect>
        <if_mismatch>Close in iam.tf, re-run before apply.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after apply">
      <step>
        <run>terraform plan 0-diff replan; aws lambda get-function on both Lambdas; confirm _smartx_model_daily.json present in S3 after the pull-Lambda invoke.</run>
        <expect>0-diff "No changes"; both Lambdas State=Active LastUpdateStatus=Successful; _smartx_model_daily.json exists before the producer runs.</expect>
        <if_mismatch>Do not signal 0.4.0_DS until the daily sidecar is confirmed present + both Lambdas Active.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - ARTIFACT-CONTRACT DELTA (B3 brief §4) — model_portfolio_timeseries.json's model_return is now SmartX-direct, so the series spans SmartX coverage (begins AFTER inception): ST/LTA/INT/LTC start 2024-09-03 (~4mo less front history), UST starts 2025-02-03 (~9mo less). Plus an additive per-row model_source field and intermittent trailing model-only rows when SmartX (T-1) leads data.pkl. This affects the model_portfolio_timeseries.json consumer — MDLP_RVVALT's rolling Sharpe + drawdown. COO is surfacing this to CTO as a consumer-coordination call (accept-truncation — consistent with the Q8 revision retiring the model.pkl estimate — vs preserve-history). This is NOT a B4 deploy gate: the SmartX-direct artifact is the correct end-state to ship; any history-preservation refinement is a separate B3 follow-on if CTO rules for it.
    - record-terraform-deploy.sh: pass an explicit agent --author (the omitted-author derive is best-effort only — fix 24642756b).
    - SmartX is NOT under the YCharts freeze — B4 deploys + invokes normally.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — both B3 AE-lane files committed (ds-commit-gate clean) + deployed; deploy order pull-Lambda-first-then-producer honored; tags + record-deploy landed.
    - AC2 — Phase-3: both Lambdas Active/Successful; terraform 0-diff replan; _smartx_model_daily.json confirmed in S3 before the producer's first run.
    - AC3 — 0.4.0_DS signalled on the deploy to run the B3 e2e verification; B4 RAVC2 to COO + CC CTO + CC 0.4.0_DS.
    - AC4 — session log Compiler Tools section reproduces the Phase-1/2/3 runs vs expectations.
  </acceptance_criteria>
</task_order>
