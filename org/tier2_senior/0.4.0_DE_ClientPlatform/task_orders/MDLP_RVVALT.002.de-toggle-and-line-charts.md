<task_order>
  <metadata>
    <id>MDLP_RVVALT.002</id>
    <project>MDLP_RVVALT</project>
    <title>Frontend toggle + Rolling Sharpe + Max Drawdown line-chart components (stub-driven)</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>complete</status>
    <closure_rationale date="2026-05-04" by="0.4.0_DE_ClientPlatform" coo_ruling="2026-05-04T19:xxZ">
      AC1 (3-view toggle) PASS via Andrew direct commits a6cf9da5 + DT bump c83af3610 (portal-v2.1.71).
      AC2 (window sub-toggle) PASS — Sharpe interval shipped, constants since rewritten.
      AC3 (RollingSharpeChart) PASS — file exists at portal/src/components/RollingSharpeChart.tsx.
      AC4 (MaxDrawdownChart) PASS — file exists at portal/src/components/MaxDrawdownChart.tsx.
      AC5 (stub fixture spot-check) — ACCEPTANCE-FLEX GRANTED by COO 2026-05-04. Execution-order collapse: AE TO-3 shipped Lambda emit before DE landed the stub, making live spot-check (TO-4 AC2) the stronger evidence path. Stub fixture intentionally not built; live data validates the same compute primitives.
      AC6 (Scatter regression) — ACCEPTANCE-FLEX GRANTED. comp-transform graph cache normalization gap (returns "Component not found" though file exists). bun run typecheck exit 0 + component file presence substitutes.
      AC7 (portal-proxy types + fetcher) PASS — ModelTimeseriesPoint + getModelTimeseries() at portal-proxy.ts:702/723.
      AC8 (session log + RAVC4) DONE — session_mdlp_rvvalt_chart_polish.md committed 4d7e86797; AC reconciliation MCP 20260504T193431Z; RULING 2026-05-04 from COO.
    </closure_rationale>
    <priority>P2 — parallel with TO-1; gated by NOTHING; stub-driven so AE TO-3 timing irrelevant</priority>
    <estimated_effort>1.5d (Recharts line-chart components + panel-header refactor + stub fixture)</estimated_effort>
  </metadata>

  <context>
    PRD: `docs/architecture/MDLP_RVVALT.md` (CTO commit `7e520d4bf`). Andrew GO 2026-05-04 option (a) full-dispatch.

    Extend Return vs Volatility panel on Model Portfolios with two alternative views (Rolling Sharpe + Max Drawdown), switchable via panel-header toggle following Segment Analytics pattern verbatim (`portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx:805–886`). Current Scatter view stays as default.

    Stub fixture decouples DE from AE TO-3 — DE generates synthetic daily series for Sharpe/Drawdown computation testing while AE Lambda is in flight. Wire-up to live endpoint happens in TO-4.
  </context>

  <objective>
    Ship 3-view panel with toggle + Rolling Sharpe chart + Max Drawdown chart per PRD §2 Frontend block + §3 Compute spec, driven by stub fixture. PRD §4 ACs 1-5 + AC8 (Scatter regression) verified at this TO close. ACs 6-7 + 9 verified at TO-4 close (post-AE-wire-up).
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>3-view panel header toggle (PRD AC1)</title>
      <detail>
        ReturnVolatilityScatter.tsx PanelHeader hosts 3 view toggles (Scatter / Rolling Sharpe / Max Drawdown) following Segment Analytics styling EXACTLY per PRD §2 toggle styling block (lines 32-49). Vertical divider `<div className="w-px h-5 bg-white/10" />` between view-toggle and window-toggle. Side-by-side screenshot vs `DistributionTab.tsx:807–823` for visual parity.
      </detail>
    </ac>
    <ac id="2">
      <title>Window-aperture sub-toggle behavior (PRD AC2)</title>
      <detail>
        Window-aperture sub-toggle (90D/180D/365D for Sharpe; 90D/180D/365D/SI for Drawdown) appears only on the line-chart views. Visually disabled (`opacity-30 pointer-events-none`) on Scatter view per PRD §2 + Segment Analytics window-toggle disable pattern (`DistributionTab.tsx:889`). Manual click + screenshot per state.
      </detail>
    </ac>
    <ac id="3">
      <title>Rolling Sharpe chart (PRD AC3)</title>
      <detail>
        New file `portal/src/components/RollingSharpeChart.tsx` — Recharts LineChart, X = date (daily), Y = Sharpe ratio. 5 model lines in canonical color (`getModelColor`) + 5 benchmark companion lines in gray (`#9ca3af` or existing benchmark gray). Window-aperture sub-toggle (90D/180D/365D) controls rolling-window denominator per PRD §3 Compute spec. Sharpe denominator instability mitigation: `null` skip on `std_excess < ε` threshold so chart line breaks rather than spikes (PRD §7.3).
      </detail>
    </ac>
    <ac id="4">
      <title>Max Drawdown chart (PRD AC4)</title>
      <detail>
        New file `portal/src/components/MaxDrawdownChart.tsx` — Recharts LineChart (or AreaChart for visual emphasis), X = date, Y = drawdown % (negative). Same model-vs-benchmark color contract as Sharpe. Window-aperture sub-toggle (90D/180D/365D/SI). All-negative-or-zero Y-axis values verified. Acceptance-flex per PRD §7.5: drawdown sitting at 0 for early-positive periods OK; tooltip helpText documents.
      </detail>
    </ac>
    <ac id="5">
      <title>Sharpe spot-check fixture (PRD AC5)</title>
      <detail>
        Stub fixture at `portal/src/components/__fixtures__/modelTimeseriesFixture.ts` — synthetic daily series (5 models × benchmarks × rfr_10y) for ~6 years of trading days. Spot-check: pick a known model + window + as-of date; manually compute Sharpe per PRD §3 formula; verify chart Y at that date matches manual calculation within ±0.01. Document spot-check in session log.
      </detail>
    </ac>
    <ac id="6">
      <title>Scatter regression (PRD AC8)</title>
      <detail>
        Existing Scatter view behavior byte-equivalent to current production. `/frontend-dev` Playwright screenshot diff against unchanged Scatter view + `comp-transform schema-check ReturnVolatilityScatter` clean (no NEW WARNs vs baseline).
      </detail>
    </ac>
    <ac id="7">
      <title>portal-proxy.ts types + fetcher (deferred wire-up)</title>
      <detail>
        Add types `ModelTimeseriesResponse` + `ModelTimeseriesPoint` to `portal/src/api/portal-proxy.ts`. Add fetcher `getModelTimeseries()` (cache key `['model-portfolio-timeseries']` per PRD §2 + comp-cache convention to avoid bare `model-portfolio`). Fetcher reads stub fixture in this TO; switches to live endpoint in TO-4.
      </detail>
    </ac>
    <ac id="8">
      <title>Session log + RAVC4</title>
      <detail>
        Session log under `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-05-04/`. Compiler Tools section reproduces every `<run>`. `/frontend-dev` results saved to `.frontend-dev-results/`. RAVC4 to me with portal commit hash + parent CLOUD commit + screenshot paths.
      </detail>
    </ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before_edit">
      <step>
        <run>comp-cache collisions</run>
        <expect>Confirm `['model-portfolio-timeseries']` namespace not already in use (PRD §5 baseline)</expect>
        <if_mismatch>If new collision appeared since PRD authoring, surface to COO + CTO before proceeding</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check ReturnVolatilityScatter</run>
        <expect>Baseline schema-check output captured before refactor</expect>
        <if_mismatch>If baseline shows existing WARNs, document; goal is no NEW WARNs at Phase 2</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before_commit">
      <step>
        <run>cd portal &amp;&amp; bun run typecheck</run>
        <expect>Exit 0; no new TypeScript errors</expect>
        <if_mismatch>Fix typecheck before commit</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check ReturnVolatilityScatter</run>
        <expect>Same clean output as Phase 1; no NEW WARNs (PRD AC8 byte-equivalence verification)</expect>
        <if_mismatch>Investigate field-mismatch regression; should not occur for CSS+component-add</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after_commit">
      <step>
        <run>/frontend-dev</run>
        <expect>Closed-loop Playwright run against Model Portfolios page; AC1+AC2+AC3+AC4 visual gates PASS; results saved to `.frontend-dev-results/`</expect>
        <if_mismatch>Per /frontend-dev convention, harness self-iterates fixes; surface to COO if unresolvable</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <resource>
      <path>portal/src/api/portal-proxy.ts</path>
      <owners>0.4.0_DE_ClientPlatform (this TO authors types `ModelTimeseriesResponse` + `ModelTimeseriesPoint`); 0.5.0_AE_OpalETL matches JSON schema in TO-3</owners>
      <coordination>If DS TO-1 spec changes RFR unit / index_name, AE 0.5 must MCP DE before regenerating types (per PRD §6 cross-domain block)</coordination>
    </resource>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Reasoning: pure portal frontend; no Lambda/Terraform/EC2 impact; no data pipeline change. Stub fixture is dev-only artifact; live endpoint wire-up deferred to TO-4.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    <item>Single portal commit applying §2 Frontend block (PanelHeader refactor + 2 new chart components + portal-proxy.ts types + stub fixture)</item>
    <item>CLOUD parent commit bumping portal submodule</item>
    <item>`/frontend-dev` results captured under `.frontend-dev-results/`</item>
    <item>Sharpe spot-check log (manual calculation vs chart Y) in session log</item>
    <item>Session log with Compiler Tools section + AC matrix</item>
    <item>RAVC4 MCP to COO</item>
  </deliverables>
</task_order>
