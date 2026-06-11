<to_id>NFRA_GRAPHS.D3</to_id>
<project>NFRA_GRAPHS</project>
<title>D3 — comp-graph status + uniform --fresh/--force freshness contract across the graph tools</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decompose handoff 184809Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>COMPLETE 2026-06-11 ~2013Z (0bc6939cc, pushed; RAVC2-accepted by COO) — comp-graph status reports FRESH/STALE/MISSING/PRESENT + age + TTL across local trace caches (graph.json, baseline, per-firm platinum.*) + cloud artifacts (kuzu_db, stitch_graph); comp-graph clear <platinum|trace|all> verified; uniform --fresh/--force via graph_cache.add_freshness_args. ds-commit-gate clean.</status>

Add a `comp-graph status` view (which graphs exist / their freshness / last-derive) + a UNIFORM --fresh / --force freshness contract across the graph tools (consistent semantics: --fresh = re-derive if stale, --force = always re-derive). Makes freshness explicit + uniform per the manifest. RAVC2 -> COO+CTO. Pairs with D2.
