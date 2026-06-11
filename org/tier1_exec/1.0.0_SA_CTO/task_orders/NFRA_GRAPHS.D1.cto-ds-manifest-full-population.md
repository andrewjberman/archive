<to_id>NFRA_GRAPHS.D1</to_id>
<project>NFRA_GRAPHS</project>
<title>D1 — graph-call-manifest.yaml FULL population (every graph use-case -> canonical call) = AC1 close-gate; ramp comp-manifest-check advisory->blocking behind coverage</title>
<assigned_to>1.0.0_SA_CTO + 0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decompose handoff 184809Z; Andrew-directed macro NFRA_GRAPHS PRD d9b6beac0)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>P1 -- scaffold v0.1 DONE (13 entries/11 canonical, org/modules/graph/graph-call-manifest.yaml). DS partly offline -> activates on respawn. AC1 (full coverage) = the binding completeness bar for NFRA_GRAPHS close.</status>

Populate graph-call-manifest.yaml to FULL coverage: every graph use-case (across the ~30 comp-* tools + repo-trace graph + live-AWS cloud graph + Kuzu query layer) -> its canonical call (query vs rebuild, layer, cost, freshness). CTO owns the manifest convention/schema; DS assists population + the ds-precommit coverage check. Incremental: ramp comp-manifest-check from advisory -> BLOCKING as coverage climbs (don't hard-gate before coverage is real). AC1 = full coverage = the close-gate. RAVC2 -> COO; CVO certifies AC1 coverage.
