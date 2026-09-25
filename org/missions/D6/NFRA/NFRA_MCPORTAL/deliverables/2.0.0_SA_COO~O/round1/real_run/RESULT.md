# NFRA_MCPORTAL round 1 -- the one real run at close

**Run by:** `2.0.0_SA_COO~O`, 2026-09-25 ~03:55Z.

**What was run:**
- mcportal `r1-drain` @920efd1: MP-w-1 + MP-t-5 + the issuer's router hookup.
- `bun run dev --port 5174 --strictPort --host 127.0.0.1` from a linked mcportal worktree.
- Opened in headless Edge through the portal's own playwright-core, at viewport 1440x900.

**Why 127.0.0.1:** `[::1]:5174` was already held by another session's portal dev server (pid 39284, started 08:58
local). That server was not touched.

**What is NOT in this run:**
- No gateway sits behind the dev server. MP-t-1 and MP-t-4 are merged but not deployed.
- MP-t-3 and MP-t-6 are superseded (CTO ruling R-1), so the admin API is not reachable from this page. This run
  covers the LOCAL cells' pages only. It is not a served outcome.

## Looked at

| Page | URL | HTTP | What it shows |
| --- | --- | --- | --- |
| Home | `/` | 200 | Sidebar with Andrew's eight entries in order; "Home -- The platform-ops summary lands here in a later cell." (`home.png`) |
| MCP Server | `/mcp-server` | 200 | "MCP Server -- Entitlements": Tenant ID and Object ID fields, a Look up button, "Pick a tenant and object id above to see their data grant."; the MCP Server entry is highlighted (`mcp-server.png`) |
| Recent Changes | `/mcp-server/recent-changes` | 200 | "Recent Changes": "Could not load recent changes: Unexpected token '<', "<!doctype "... is not valid JSON"; the MCP Server entry is highlighted (`recent-changes.png`) |

## Read

- **Routing:** the hookup routes both views inside the MCP Server entry. The sidebar keeps its eight entries (row
  W1-S2's placement).
- **Recent Changes with no API behind it:** the page shows a raw parse error, not a plain reason.
  - Cause: with no admin API, vite's SPA fallback answers `/api/admin/changes` with `index.html` and status 200 (log:
    `[response] 200 http://127.0.0.1:5174/api/admin/changes`). The client parses that HTML as JSON.
  - Enrichment for the round-2 analysis: the typed client should refuse a non-JSON response by content type and show
    a plain, quotable reason.
  - It is not a round-1 defect against any criterion: MP-t-5's AC1 and AC2 test the client with a mocked fetch.
- **Entitlements:** the page makes no request until Look up is pressed. The API-backed arm of both pages is round 2's,
  behind the staged-build cell and the re-cut MP-t-3 and MP-t-6.
