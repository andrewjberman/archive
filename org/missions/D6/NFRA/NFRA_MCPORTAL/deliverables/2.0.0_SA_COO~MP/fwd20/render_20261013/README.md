# Issuer's rendered run -- mcportal 0e02a1f (MP-z-2 + AMENDMENT 1), 2026-10-13 ~17:4xZ

Dev build on localhost:5174 from the mcportal worktree at `0e02a1f`. The `/api/admin/*` responses are LIVE data captured at
~17:35Z by running the gateway's own compute functions (`admin_fabric._compute(6)`, `admin_fabric_overlap._compute(6)`,
`admin_fabric_gitstate._compute()`, `admin_fabric_calls._compute('open')`, `admin_gateway_breakdown._compute()`) from
trunk under the issuer's read-only AWS credentials, then served to the page through Playwright routes.

- `mp_cp_after.png`: Control Plane boxes table. Every identifier stays whole; seats are a count; one line per project.
- `mp_cp_full.png`: the full Control Plane, with the Overlap and Git state panels.
- `mp_oc_after.png`: Open Calls. Box, Project, Asked by and Age stay whole; Subject wraps at spaces.
- `mp_gw.png`: Gateway (FWD-20). Only the m365 channel shows locally, because no integration is enabled in the issuer's
  environment; the served host enables its integrations.

This is the artifact on which `3.0.0_SA_CVO~Z` grades MP-z-2 AC3 (judgment), against Andrew's screenshots of the old
bundle (recorded in ANDREW_DIRECT_20261013_162xZ_CONTROL_PLANE_OPEN_CALLS_READABILITY.md).
