# ADVI_NNAFEE.001 — DE: Wire Advisor Fee Efficiency Endpoint + Types

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-nnafee-001-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-06</date>
    <status>staged</status>
    <project_code>ADVI_NNAFEE</project_code>
    <priority>high</priority>
    <phase>1</phase>
  </metadata>

  <objective>
    Wire the `advisor_fee_efficiency.json` gold artifact into the portal's API
    layer and define TypeScript interfaces for the data contract.
  </objective>

  <context>
    Gold script 08c (`data/black_diamond/scripts/gold/08c_build_advisor_fee_efficiency.py`)
    already produces `gold/artifacts/advisor_fee_efficiency.json` on S3. The portal
    has no endpoint or types for it yet.

    The JSON is served via CloudFront at:
    `/api/scoped/advisor-intelligence/artifacts/advisor_fee_efficiency.json`

    No new Lambda or CloudFront behavior is needed -- the existing wildcard behavior
    for `/api/scoped/advisor-intelligence/*` already covers `artifacts/*`.
  </context>

  <scope>
    ## 1. TypeScript Interfaces

    Add to `portal/src/pages/AdvisorIntelligence/types.ts`:

    ```typescript
    // --- Advisor Fee Efficiency (08c) ---

    export interface FeeEfficiencyRegression {
      slope: number | null
      intercept: number | null
      r_squared: number | null
      n_advisors: number
    }

    export interface FeeEfficiencyAdvisor {
      advisor: string
      roles: string[]
      account_count: number
      managed_aua: number
      implied_revenue_ytd: number
      implied_revenue_trailing_12m: number
      nna_ytd: number
      nna_trailing_12m: number
      growth_ytd: number
      book_growth_rate: number
      efficiency_ratio: number
      fee_yield_bps: number
      regression_residual: number
    }

    export interface FeeEfficiencyResponse {
      as_of_date: string
      regression: FeeEfficiencyRegression
      advisors: FeeEfficiencyAdvisor[]
    }
    ```

    ## 2. API Endpoint Function

    Add to `portal/src/api/endpoints/advisor-intelligence.ts`:

    ```typescript
    export async function getAdvisorFeeEfficiency(
      firmOverride?: string
    ): Promise<FeeEfficiencyResponse> {
      const base = '/api/scoped/advisor-intelligence/artifacts/advisor_fee_efficiency.json'
      return await apiRequest<FeeEfficiencyResponse>(
        firmOverride ? `${base}?firm=${firmOverride}` : base
      )
    }
    ```

    ## 3. Query Hook (if using React Query)

    Add a query hook following the existing pattern in the codebase (check how
    `getArchitectLeaderboard` is consumed). If hooks exist, add one for fee efficiency.

    ## 4. Type Check

    Run `bunx tsc -b` and fix any errors.
  </scope>

  <deliverables>
    <deliverable id="types">TypeScript interfaces in types.ts matching the JSON contract</deliverable>
    <deliverable id="endpoint">API function in advisor-intelligence.ts</deliverable>
    <deliverable id="hook">Query hook if pattern exists in codebase</deliverable>
    <deliverable id="tsc">Clean `bunx tsc -b`</deliverable>
  </deliverables>

  <additional_scope>
    ## 5. Fee Summary Types for L2/L3

    Also add types for the fee_summary block that DS 0.4.0 is adding to
    book.json (L2) and client_detail.json (L3):

    ```typescript
    export interface FeeRoleBreakdown {
      role: string
      aua: number
      fee_bps: number
      pct_of_book: number
    }

    export interface FeeAccountBreakdown {
      account_id: string
      fee_bps: number
      aua: number
    }

    export interface FeeSummaryByRole {
      weighted_avg_fee_bps: number
      annual_implied_revenue: number
      by_role: FeeRoleBreakdown[]
    }

    export interface FeeSummaryByAccount {
      weighted_avg_fee_bps: number
      annual_implied_revenue: number
      by_account: FeeAccountBreakdown[]
    }
    ```

    Add `fee_summary: FeeSummaryByRole | null` to AdvisorBookResponse.
    Add `fee_summary: FeeSummaryByAccount | null` to BooksClientDetailResponse.
    These types are consumed by RD's FeeRoleBreakdownPanel (L2) and FeeSummaryPanel (L3).
  </additional_scope>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_NNAFEE-000" status="complete">DS must add fee_summary to book.json and client_detail.json first</dependency>
  </dependencies>
</task_order>
