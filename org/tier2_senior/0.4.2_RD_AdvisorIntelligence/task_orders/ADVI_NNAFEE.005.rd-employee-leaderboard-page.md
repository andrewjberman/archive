# ADVI_NNAFEE.005 — RD: Add Role Checkboxes to Leaderboard

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-nnafee-005-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-06</date>
    <status>complete</status>
    <!-- Completed 2026-04-07. Portal DEV commit 4b93007. Data source swapped, role_breakdown filtering active. -->
    <project_code>ADVI_NNAFEE</project_code>
    <priority>high</priority>
    <phase>2</phase>
  </metadata>

  <objective>
    Add role filter checkboxes to the existing Leaderboard panel in AdvisorsTab
    and swap the data source from `architect_leaderboard.json` to
    `employee_leaderboard.json`. The existing leaderboard design (Top 3 Highlights,
    NNA/AUA/Growth metric views, cards, search) stays as-is. The only UI addition
    is checkboxes in the controls area next to the AUA/NNA/GRO toggle.
  </objective>

  <context>
    Existing leaderboard: `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx`
    Uses `getArchitectLeaderboard()` -> `LeaderboardResponse`.

    The existing design is fine. The change is:
    1. Swap data source to `getEmployeeLeaderboard()` -> `EmployeeLeaderboardResponse`
    2. Add role checkboxes (Architect, Implementor, Consultant, Local Ops, Addtl Advisor)
    3. When checkboxes are active, derive displayed metrics from `role_breakdown`
       instead of using the top-level values

    New data: `EmployeeLeaderboardResponse` (.004 DE) has the same window structure
    but each entry includes `role_breakdown` with per-role metrics.
    ~155 entries, ~50KB. All computation client-side.
  </context>

  <scope>
    ## What Changes

    ### 1. Add Role Checkboxes

    Place in the Leaderboard panel controls, next to the existing AUA/NNA/GRO
    metric toggle. Multi-select checkboxes:

    - [x] Architect  (default checked)
    - [x] Implementor  (default checked)
    - [ ] Consultant
    - [ ] Local Ops
    - [ ] Addtl Advisor

    ### 2. Metric Filtering Logic

    When any role checkbox is toggled, recompute displayed values for each entry
    by summing only the checked roles from `entry.role_breakdown`:

    ```typescript
    function getDisplayMetrics(entry: EmployeeLeaderboardEntry, checkedRoles: Set<string>) {
      let aua = 0, nna = 0, revenue = 0, accounts = 0, clients = 0, newClients = 0;
      for (const [role, data] of Object.entries(entry.role_breakdown)) {
        if (checkedRoles.has(role)) {
          aua += data.managed_aua;
          nna += data.nna;
          revenue += data.implied_revenue;
          accounts += data.account_count;
          clients += data.client_count;
          newClients += data.new_clients;
        }
      }
      return { aua, nna, revenue, accounts, clients, newClients };
    }
    ```

    When ALL roles are checked (or no filtering is active), use the top-level
    entry values directly (they are the pre-computed all-roles totals).

    Visibility: hide a person only if they hold NONE of the checked roles.
    Ranking: recompute rank order from filtered metrics on every checkbox change.

    ### 3. Swap Data Source

    In AdvisorsTab.tsx:
    - `getArchitectLeaderboard()` -> `getEmployeeLeaderboard()`
    - `LeaderboardResponse` -> `EmployeeLeaderboardResponse`
    - `LeaderboardEntry` -> `EmployeeLeaderboardEntry`
    - The entry field names may differ slightly (check the new types from .004 DE)

    Keep Rolling Flows (Panel 1) and Top 3 Highlights unchanged -- they continue
    working with the same entry shape (name, total_aua, nna, aua_growth_pct, new_clients).

    ### 4. Edge Cases

    | Case | Behavior |
    |------|----------|
    | All checkboxes checked | Use top-level entry values (no filtering overhead) |
    | Person has only unchecked roles | Hide from view |
    | All checkboxes unchecked | Show "Select at least one role" empty state |

    ## What Does NOT Change

    - Top 3 Highlights cards
    - NNA cards view, AUA bar chart view, Growth bar chart view
    - LeaderboardRow / LeaderboardPinnedRow card design
    - Period/window toggle behavior
    - Search functionality
    - FIRM_ACCOUNT_NAME / PINNED_BOTTOM_NAMES handling
  </scope>

  <deliverables>
    <deliverable id="checkboxes">Role filter checkboxes in Leaderboard panel controls</deliverable>
    <deliverable id="filtering">Metric recomputation from role_breakdown on checkbox change</deliverable>
    <deliverable id="datasource">Data source swapped to employee_leaderboard.json</deliverable>
    <deliverable id="tsc">Clean `bunx tsc -b`</deliverable>
  </deliverables>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_NNAFEE.004" status="staged"/>
  </dependencies>
</task_order>
