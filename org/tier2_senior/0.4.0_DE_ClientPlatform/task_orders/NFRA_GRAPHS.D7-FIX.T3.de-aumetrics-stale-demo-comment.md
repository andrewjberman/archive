<to_id>NFRA_GRAPHS.D7-FIX.T3</to_id>
<project>NFRA_GRAPHS</project>
<title>D7-FIX T3 — getAUMMetrics stale DEMO comment resolution (portal-proxy.ts:341-347)</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (D7 real_bug #3, 164849Z RAVC2)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete — 2026-06-12T~1800Z by 0.4.0_DE_ClientPlatform; commit 8b6a6466 (portal DEV)</status>
<priority>low — stale comment with unresolved TODO; decision needed before cleanup</priority>

<scope>
`portal-proxy.ts:341-347` has `// DEMO: Using public endpoint (no auth)` with a TODO to revert to `/api/private/portfolios/aum-metrics.json`. The `/api/general/` endpoint is NOW auth-gated (CF auth-validator-edge, behavior 16), so the comment is factually wrong.

Decision required: is the current `/api/general/` path intentional, or should it migrate to `/api/private/`? Either way, remove the stale DEMO comment and TODO. If migrating: confirm the `/api/private/` behavior exists and auth is equivalent.

Bundle with T1/T2 commit if convenient, or ride the next portal maintenance pass.

Acceptance: stale `// DEMO` comment removed or replaced with accurate current-state comment; no TODO left dangling.
</scope>
