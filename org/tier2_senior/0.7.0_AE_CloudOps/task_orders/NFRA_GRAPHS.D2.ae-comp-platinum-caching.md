<to_id>NFRA_GRAPHS.D2</to_id>
<project>NFRA_GRAPHS</project>
<title>D2 — comp-platinum caching: the rebuild-every-call outlier -> cached query-vs-rebuild per the manifest contract</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decompose handoff 184809Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>P1 -- parallel, no cross-dep. AE-lane partly offline -> activates on respawn. Per NFRA_GRAPHS.md D2.</status>

comp-platinum currently REBUILDS the graph every call (the outlier vs the cached query layer). Bring it under the query-vs-rebuild contract: add caching with a freshness/invalidation policy consistent with the manifest (query the cached graph by default; rebuild only on explicit --fresh/--force or staleness). RAVC2 -> COO+CTO. Pairs with D3 (uniform freshness contract).
