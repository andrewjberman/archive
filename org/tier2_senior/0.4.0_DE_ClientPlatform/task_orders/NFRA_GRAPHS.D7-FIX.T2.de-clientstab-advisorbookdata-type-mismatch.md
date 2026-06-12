<to_id>NFRA_GRAPHS.D7-FIX.T2</to_id>
<project>NFRA_GRAPHS</project>
<title>D7-FIX T2 — ClientsTab advisorBookData state var type mismatch (AdvisorBookResponse → PlatinumAdvisorSummary)</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (D7 real_bug #2, 164849Z RAVC2)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>active</status>
<priority>medium — type mismatch in ClientsTab state var; ADVI_PROFAU.004 partial fix left downstream state untyped</priority>

<scope>
ClientsTab state var `advisorBookData` is typed as `AdvisorBookResponse` but `getPlatinumAdvisorSummary()` returns `PlatinumAdvisorSummary`. ADVI_PROFAU.004 updated the function signature but not the downstream state typing.

Fix: update the `useState` / `useEffect` in ClientsTab to use `PlatinumAdvisorSummary` (or the correctly typed adapter result, consistent with T1's backfill).

Bundle with T1 if in the same edit session (they share the same type file + ClientsTab).

Acceptance: `comp-transform schema-check ClientsTab` shows no ADAPTER type mismatch; TypeScript compile clean.
</scope>
