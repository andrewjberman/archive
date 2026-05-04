<task_order>
  <metadata>
    <id>MDLP_RVVALT.004</id>
    <project>MDLP_RVVALT</project>
    <title>DE wire-up — swap stub fixture for live endpoint + AC5/6/7/9 final verification</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>pending</status>
    <priority>P2 — final wire-up; gates on AE TO-3 RAVC4 (live endpoint shipped)</priority>
    <estimated_effort>0.5d (swap fetcher source + AC verification + PROD push)</estimated_effort>
  </metadata>

  <context>
    PRD: `docs/architecture/MDLP_RVVALT.md` (CTO commit `7e520d4bf`). Final wire-up step.

    TO-2 shipped the toggle + line-chart components driven by stub fixture (`portal/src/components/__fixtures__/modelTimeseriesFixture.ts`). TO-3 ships the live Lambda emit at `s3://opal-data-portal-v2/json/benchmarks/model_portfolio_timeseries.json`.

    This TO swaps the stub for the live endpoint via `getModelTimeseries()` fetcher, runs the live AC5 Sharpe spot-check (against real RFR data, not synthetic), and verifies AC6/AC7/AC9. Then PROD push.
  </context>

  <objective>
    Wire `getModelTimeseries()` fetcher to live `/api/general/benchmarks/model_portfolio_timeseries.json` endpoint. Run final AC matrix against live data. PROD push portal.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>Stub-to-live swap</title>
      <detail>
        Update `getModelTimeseries()` in `portal/src/api/portal-proxy.ts` from stub fixture import to live HTTP fetch on `/api/general/benchmarks/model_portfolio_timeseries.json` (existing `general/` route already covered by CF + auth — PRD §2 + §5 confirmed). Cache key remains `['model-portfolio-timeseries']`. Stub fixture file may stay as test-only artifact or be removed (DE call).
      </detail>
    </ac>
    <ac id="2">
      <title>Sharpe spot-check on live data (PRD AC5)</title>
      <detail>
        Pick a known model + window + as-of date from the live Lambda output. Manually compute Sharpe per PRD §3 formula using live RFR (not synthetic). Verify chart Y at that date matches manual calculation within ±0.01. Document in session log.

        If the live RFR has coverage gap (PRD §7.1 risk surfaced by AE TO-1), spot-check at an in-coverage date; document the SI Drawdown fallback behavior in session log.
      </detail>
    </ac>
    <ac id="3">
      <title>Endpoint payload + ETag verification (PRD AC6 + AC7)</title>
      <detail>
        - `curl https://portal.opalinvest.com/api/general/benchmarks/model_portfolio_timeseries.json` returns payload
        - `jq '. | length, [.[] | .model_code] | unique, [.[] | .date] | min'` validates: row count > 0, 5 distinct model_codes, earliest date matches inception OR documented RFR-coverage start
        - rfr_10y populated in all rows
        - CloudWatch log + S3 ETag confirmed via AE 0.5 RAVC4 from TO-3 (cite in session log)
      </detail>
    </ac>
    <ac id="4">
      <title>View toggle + URL persistence (PRD AC9)</title>
      <detail>
        View toggle (Scatter / Rolling Sharpe / Max Drawdown) persists across in-page interactions; refresh resets to "Scatter" default (no over-engineering URL-sync unless trivial). Manual click test + screenshot.
      </detail>
    </ac>
    <ac id="5">
      <title>Scatter regression re-verification (PRD AC8)</title>
      <detail>
        Re-run `comp-transform schema-check ReturnVolatilityScatter` post-wire-up; no NEW WARNs vs TO-2 baseline. `/frontend-dev` against unchanged Scatter view confirms byte-equivalence.
      </detail>
    </ac>
    <ac id="6">
      <title>PROD push</title>
      <detail>
        Standard portal DEV→PROD workflow. DT 0.4 push if needed (per Abilities table — DT pushes portal submodule). Confirm PROD CloudFront serves new endpoint + new chart components.
      </detail>
    </ac>
    <ac id="7">
      <title>Project closure trigger</title>
      <detail>
        Once AC1-6 PASS + PROD live, MCP me with: portal commit hash + CLOUD parent + PROD push commit + `/frontend-dev` PROD screenshot + AC matrix.

        I 3-step atomic close MDLP_RVVALT (JSON status complete + REGISTRY Active→Completed + PRD `Status:` line).
      </detail>
    </ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before_edit">
      <step>
        <run>comp-blast getModelTimeseries</run>
        <expect>Confirm function-level blast radius hasn't grown since TO-2 (PRD §6 TO-4 mandate)</expect>
        <if_mismatch>If new downstream nodes appeared, surface to COO</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before_commit">
      <step>
        <run>cd portal &amp;&amp; bun run typecheck</run>
        <expect>Exit 0</expect>
        <if_mismatch>Fix typecheck</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after_commit">
      <step>
        <run>curl -s https://portal.opalinvest.com/api/general/benchmarks/model_portfolio_timeseries.json | jq '. | length'</run>
        <expect>Non-zero row count returned from PROD endpoint</expect>
        <if_mismatch>Investigate CF/auth/Lambda chain</if_mismatch>
      </step>
      <step>
        <run>/frontend-dev</run>
        <expect>Closed-loop run on PROD against Model Portfolios; AC1-6 visual gates PASS with live data</expect>
        <if_mismatch>Per /frontend-dev convention</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Reasoning: portal-only wire-up; AE TO-3 already shipped the data; no replay needed.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    <item>Portal commit (DE 0.4.0 author) — fetcher swap + PROD push</item>
    <item>CLOUD parent commit + portal PROD push commit</item>
    <item>Sharpe spot-check log on live data (in session log)</item>
    <item>`/frontend-dev` PROD screenshots</item>
    <item>RAVC4 MCP to COO triggering MDLP_RVVALT 3-step atomic close</item>
  </deliverables>
</task_order>
