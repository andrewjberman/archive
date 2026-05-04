<task_order>
  <metadata>
    <id>MDLP_RVVALT.005</id>
    <project>MDLP_RVVALT</project>
    <title>Upside/Downside Capture rolling-view — fourth view in Return vs Volatility panel toggle</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>pending</status>
    <priority>P2 — parallel with TO-2/TO-4 wrap; frontend-only, no backend coord</priority>
    <estimated_effort>0.5d (component clone + ViewMode wiring + spot-check)</estimated_effort>
  </metadata>

  <context>
    Andrew → Yang → AE 0.5.0 → DE 0.4.0 relay, surfaced 2026-05-04 19:31Z. Full implementation spec
    in AE 0.5.0 MCP `20260504T193053Z` to DE 0.4.0 (subject "PLAN: Upside/Downside Capture rolling
    view — Benchmark tab"). Slots between Rolling Sharpe and Max Drawdown views.

    AE 0.5.0 confirmed NO BACKEND CHANGE NEEDED — `model_portfolio_timeseries.json` (yang-v2.4.0,
    S3 ETag `68277012ae6c4e45ec0492140a313d4d`) already carries per-day `model_return` and
    `benchmark_return` decimal fractions sufficient for sign-filtered compounding.

    This TO extends the existing 3-view toggle (Scatter / Rolling Sharpe / Max Drawdown) shipped
    via TO-2/TO-4 to a 4-view toggle. Pattern is identical clone-and-extend from RollingSharpeChart.
  </context>

  <objective>
    Ship a fourth view "Upside/Downside Capture" in ReturnVolatilityScatter.tsx panel toggle, slotted
    between 'sharpe' and 'drawdown' in ViewMode. Component: clone of RollingSharpeChart.tsx as
    RollingCaptureChart.tsx with two series (Up Capture green, Down Capture red), reference lines at
    0% and 100%, reusing existing `useQuery(['model-portfolio-timeseries'])` data fixture.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>ViewMode extension</title>
      <detail>
        `ReturnVolatilityScatter.tsx` ViewMode type extended to include `'capture'` between `'sharpe'`
        and `'drawdown'`. VIEW_LABELS adds `capture: 'Up/Down Capture'`. PANEL_CONFIG entry for
        'capture': title `'Upside/Downside Capture'`, helpText per AE 0.5 spec lines 39-40
        ("Percent of benchmark return the model captures on up vs down days. Above 100% upside
        plus below 100% downside indicates strong risk-adjusted performance."). Toggle order in
        header: Scatter / Rolling Sharpe / Up/Down Capture / Max Drawdown.
      </detail>
    </ac>
    <ac id="2">
      <title>RollingCaptureChart.tsx component (clone of RollingSharpeChart pattern)</title>
      <detail>
        New file `portal/src/components/RollingCaptureChart.tsx`. Same MODEL_CODES selector cards
        (UST/ST/INT/LTC/LTA), same INTERVALS array `[22, 65, 131, 261]` with labels {1M, 1Q, 6M, 1Y},
        same Bar/Line mode toggle (default Line + 1Y). Two series: `upCapture` (`#22c55e` green) and
        `downCapture` (`#ef4444` red). NO benchmark companion line (capture IS already vs benchmark).
        Y-axis label `'Capture (%)'`. Reference lines at 0 and 100. Domain auto, with optional clip
        to `[-50, 250]` if outliers appear. Tooltip shows `date + Up Capture % + Down Capture %`.
      </detail>
    </ac>
    <ac id="3">
      <title>Up/Down Capture math</title>
      <detail>
        For each rolling window ending at date D (window length = INTERVAL):
        - `up_subset` = window rows where `benchmark_return > 0`
        - `down_subset` = window rows where `benchmark_return &lt; 0`
        - `compound(rs)` = `rs.reduce((p, r) =&gt; p * (1 + r), 1) - 1` (already in RollingSharpeChart pattern)
        - `up_capture = compound(model_return on up-days) / compound(benchmark_return on up-days) * 100`
        - `down_capture = compound(model_return on down-days) / compound(benchmark_return on down-days) * 100`
        Edge cases per AE spec lines 25-27: empty subset → null; `|compound_bm| &lt; 1e-6` → null;
        days with `benchmark_return === 0` excluded from both subsets. Spot-check documented in
        session log: pick UST or LTC, 1Y window, known as-of date; manual subset compound vs chart Y.
      </detail>
    </ac>
    <ac id="4">
      <title>Data reuse — no new fetch</title>
      <detail>
        RollingCaptureChart consumes the existing `useQuery(['model-portfolio-timeseries'])` query
        result. NO new endpoint, NO Lambda change, NO terraform. Verified by `git grep` showing
        zero new query keys introduced. AE 0.5 confirmed sufficiency at relay time.
      </detail>
    </ac>
    <ac id="5">
      <title>Existing 3-view regression clean</title>
      <detail>
        Scatter / Rolling Sharpe / Max Drawdown views byte-equivalent to pre-TO-005 production.
        `/frontend-dev` Playwright screenshot diff CLEAN against pre-TO baseline for all 3 existing
        views. `comp-transform schema-check ReturnVolatilityScatter` no NEW WARNs vs baseline.
      </detail>
    </ac>
    <ac id="6">
      <title>Typecheck + build clean</title>
      <detail>
        `bun run typecheck` exit 0. `bun run build` exit 0. Frontend-dev local visual smoke
        (1366x912 Surface Laptop viewport): toggle through all 4 views, capture view renders both
        Up/Down series + reference lines + tooltip on hover.
      </detail>
    </ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      <tool>comp-transform schema-check ReturnVolatilityScatter</tool>
      <expect>Baseline WARN count captured for AC #5 regression compare</expect>
    </before_write>
    <before_commit>
      <tool>bun run typecheck</tool>
      <expect>Exit 0</expect>
    </before_commit>
    <before_commit>
      <tool>comp-transform fields RollingCaptureChart</tool>
      <expect>All rendered fields typed; no silent undefineds</expect>
    </before_commit>
    <after_commit>
      <tool>/frontend-dev</tool>
      <expect>4-view toggle Playwright pass; capture view shows Up green + Down red + 0/100 ref lines</expect>
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <coordination>
      Frontend-only TO. Touches `portal/src/components/RollingCaptureChart.tsx` (new) and
      `portal/src/pages/.../ReturnVolatilityScatter.tsx` (ViewMode + PANEL_CONFIG only — does NOT
      modify `RollingSharpeChart.tsx` or `MaxDrawdownChart.tsx`). No shared S3 / Lambda / IAM /
      data-contract surface with any other active TO. No coordination block needed.
    </coordination>
  </cross_domain_coordination>

  <dependencies>
    <dependency status="complete">MDLP_RVVALT.003 (AE Lambda emit `yang-v2.3.9` + `yang-v2.4.0` schema; per-model rfr + benchmark_return live)</dependency>
    <dependency status="complete">MDLP_RVVALT.002 (DE 3-view toggle + RollingSharpeChart + MaxDrawdownChart pattern shipped 2026-05-04 — pattern to clone)</dependency>
  </dependencies>

  <deliverables>
    - `portal/src/components/RollingCaptureChart.tsx` (new file)
    - `portal/src/pages/AdvisorIntelligence/.../ReturnVolatilityScatter.tsx` (ViewMode + VIEW_LABELS + PANEL_CONFIG diff only)
    - Session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-05-04/MDLP_RVVALT_005_capture_view.md` with Compiler Tools section + manual spot-check arithmetic
    - Portal commit on DEV; DT 0.4 ships PROD via standard portal-vX.Y.Z deploy pattern
  </deliverables>

  <issuance_provenance>
    Andrew authorized via Yang → AE 0.5.0 peer relay 2026-05-04 PM. AE 0.5.0 MCP `20260504T193053Z`
    to DE 0.4.0 carries the full implementation spec. DE 0.4.0 RAVC2-ACK'd to AE and held for COO
    formal TO dispatch (correct protocol — peer relays require exec authorization). COO confirms
    relay chain integrity by reading the AE→DE message in DE inbox archive; no inconsistency with
    AE 0.5.0 prior MDLP_RVVALT.001/.003/.004 deliverables.
  </issuance_provenance>

  <go_signal>
    GO authorized by 2.0.0_SA_COO 2026-05-04. Begin immediately. RAVC4 to COO on close with commit
    hash + frontend-dev screenshot evidence + manual spot-check arithmetic.
  </go_signal>
</task_order>
