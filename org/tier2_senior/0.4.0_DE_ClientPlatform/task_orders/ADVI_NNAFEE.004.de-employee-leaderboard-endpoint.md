# ADVI_NNAFEE.004 — DE: Rewire Leaderboard Endpoint to Employee Leaderboard

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-nnafee-004-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-06</date>
    <status>staged</status>
    <project_code>ADVI_NNAFEE</project_code>
    <priority>high</priority>
    <phase>2</phase>
  </metadata>

  <objective>
    Replace the existing `getArchitectLeaderboard()` endpoint with a new
    `getEmployeeLeaderboard()` that reads `employee_leaderboard.json`.
    Define new TypeScript interfaces that include `role_breakdown` per entry
    and the per-window `regression` and `summary` objects.
  </objective>

  <context>
    Gold script 11a (`data/black_diamond/scripts/gold/11a_publish_portal_aggregates.py`)
    already builds `gold/artifacts/employee_leaderboard.json` from 08c detail data.
    The existing portal reads `architect_leaderboard.json` via `getArchitectLeaderboard()`
    in `advisor-intelligence.ts`.

    The employee leaderboard has a different JSON structure:
    - `windows.{window}.entries[]` includes `role_breakdown` per person
    - Each entry has per-role metrics (account_count, client_count, managed_aua, nna,
      implied_revenue, aua_growth_pct, new_clients, avg_split_pct)
    - Windows include `regression` (slope, intercept, r_squared, n_entries) and
      `summary` (total_nna, total_aua, etc.)
    - Available roles: architect, implementor, consultant, local_ops, additional_advisor

    Endpoint path:
    `/api/scoped/advisor-intelligence/artifacts/employee_leaderboard.json`

    Keep `getArchitectLeaderboard()` temporarily for backwards compatibility (dual-write
    from 11a), but the Advisors tab should switch to the new endpoint.
  </context>

  <scope>
    ## 1. New TypeScript Interfaces

    Add to `portal/src/pages/AdvisorIntelligence/types.ts`:

    ```typescript
    // --- Employee Leaderboard (11a, from 08c detail) ---

    export interface EmployeeRoleBreakdown {
      account_count: number
      client_count: number
      managed_aua: number
      nna: number
      implied_revenue: number
      aua_growth_pct: number
      new_clients: number
      avg_split_pct: number
    }

    export interface EmployeeLeaderboardEntry {
      name: string
      roles: string[]
      total_aua: number
      nna: number
      implied_revenue: number
      aua_growth_pct: number
      new_clients: number
      client_count: number
      account_count: number
      fee_yield_bps: number
      efficiency_ratio: number
      regression_residual: number
      role_breakdown: Record<string, EmployeeRoleBreakdown>
    }

    export interface EmployeeLeaderboardRegression {
      slope: number | null
      intercept: number | null
      r_squared: number | null
      n_entries: number
    }

    export interface EmployeeLeaderboardSummary {
      total_entries: number
      total_nna: number
      total_aua: number
      positive_nna_count: number
      negative_nna_count: number
      total_implied_revenue: number
      avg_efficiency_ratio: number
    }

    export interface EmployeeLeaderboardWindow {
      entries: EmployeeLeaderboardEntry[]
      summary: EmployeeLeaderboardSummary
      regression: EmployeeLeaderboardRegression
    }

    export interface EmployeeLeaderboardResponse {
      generated_at: string
      data_as_of: string
      firm_id: string
      leaderboard_type: 'employee'
      available_roles: string[]
      available_windows: string[]
      windows: Record<string, EmployeeLeaderboardWindow>
    }
    ```

    ## 2. New API Endpoint Function

    Add to `portal/src/api/endpoints/advisor-intelligence.ts`:

    ```typescript
    export async function getEmployeeLeaderboard(
      firmOverride?: string
    ): Promise<EmployeeLeaderboardResponse> {
      const base = '/api/scoped/advisor-intelligence/artifacts/employee_leaderboard.json'
      return await apiRequest<EmployeeLeaderboardResponse>(
        firmOverride ? `${base}?firm=${firmOverride}` : base
      )
    }
    ```

    ## 3. Type Check

    Run `bunx tsc -b` and fix any errors. Do NOT remove the old
    `LeaderboardResponse` type or `getArchitectLeaderboard()` yet -- RD will
    migrate the Advisors tab to the new types in .005.
  </scope>

  <deliverables>
    <deliverable id="types">EmployeeLeaderboard* interfaces in types.ts</deliverable>
    <deliverable id="endpoint">getEmployeeLeaderboard() in advisor-intelligence.ts</deliverable>
    <deliverable id="tsc">Clean `bunx tsc -b`</deliverable>
  </deliverables>

  <dependencies>
    None -- gold script already produces the data.
  </dependencies>
</task_order>
