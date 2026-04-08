# ADVI_REBORN.W2-003 — DE: Add windowed types to FeeEfficiencyResponse

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w2-003-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-07</date>
    <status>staged</status>
    <project_code>ADVI_REBORN</project_code>
    <priority>high</priority>
    <phase>WS2</phase>
  </metadata>

  <objective>
    Update FeeEfficiencyResponse type to support windowed data (QTD/YTD/1Y/3Y/Max).
    Each window has its own regression and advisors array.
  </objective>

  <scope>
    Update types.ts:

    ```typescript
    export interface FeeEfficiencyWindowData {
      regression: FeeEfficiencyRegression
      advisors: FeeEfficiencyAdvisor[]
    }

    export type FeeEfficiencyWindow = 'qtd' | 'ytd' | 'trailing_1y' | 'trailing_3y' | 'max'

    // Update FeeEfficiencyResponse:
    export interface FeeEfficiencyResponse {
      as_of_date: string
      // Backward compat (mirrors trailing_1y window)
      regression: FeeEfficiencyRegression
      advisors: FeeEfficiencyAdvisor[]
      // New: windowed data
      windows?: Record<FeeEfficiencyWindow, FeeEfficiencyWindowData>
    }
    ```

    The `windows` field is optional so existing code using top-level regression/advisors doesn't break. RD will migrate to windows when available.

    Run bunx tsc -b, fix errors.
  </scope>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_REBORN.W2-002" status="complete">DS must produce the windowed JSON first</dependency>
  </dependencies>

  <commit_pattern>feat(types): add windowed FeeEfficiencyResponse for interval-aware scatter</commit_pattern>
</task_order>
