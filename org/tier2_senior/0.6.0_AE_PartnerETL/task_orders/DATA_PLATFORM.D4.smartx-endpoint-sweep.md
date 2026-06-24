<to_id>DATA_PLATFORM.D4</to_id>
<project>DATA_PLATFORM</project>
<title>D4 SmartX endpoint + structure sweep -- full surface map + partnership-slot/build-vs-buy boundary</title>
<assigned_to>0.6.0_AE_PartnerETL (AE-lead; DS-consult)</assigned_to>
<!-- RE-ASSIGNED 0.7.0->0.6.0 2026-06-24 (COO offloaded D1/D4 to the 2nd AE lane). -->

<consult>0.4.0_DS_ClientPlatform</consult>
<verify>3.0.0_SA_CVO (reconcile-verify spec vs the HAR / live SmartX)</verify>
<issued_by>2.0.0_SA_COO (DATA_PLATFORM Phase-1 decomposition; Andrew-direct via CTO 2026-06-23; PRD S6/S11; LD-0209)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete</status>
<!-- SPEC-COMPLETE 2026-06-24: docs/briefs/DATA_PLATFORM_D4_SMARTX_ENDPOINT_SWEEP.md v0.2 (6d7d30ba0). AC1 (completeness-rigor-upgrade: spec-hunt no-spec + fresh 06-24 exhaustion sweep + per-surface basis taxonomy), AC2 (build-vs-buy/leverage boundary), AC3 CVO PASS, AC4 spec-not-build. CTO-ACCEPTED + canonicalizing. COO validated+closed. DEEP downstream: DC-LEV capability-leverage-map on the DC0/DC3 crawl. -->

<!-- SPEC/AUDIT (Phase-1), NOT a build. SmartX partnership-terms run PARALLEL (no gate, Andrew-confirmed). -->

<objective>
Produce the full SmartX endpoint + structure sweep -- map the entire SmartX surface + the partnership-slot map, so the build-vs-buy boundary (self-build the Eclipse-class trade/rebalance layer vs SmartX-partner) is explicit. SPEC-OF-RECORD: PRD S6 row D4.
</objective>

<the_work>
The full SmartX surface: identity / core-3.1 / performance / legacy-3.0 / GraphQL -- enterprises-aggregation, holdings, performance-SoR, model-management; field/endpoint-level; the partnership-slot map. Seed: smartx-rest-integration-design-20260515.md (the HAR of 243 entries).
SCOPE the build-vs-buy boundary explicitly (PRD insight #2/#6): reporting is displaceable; the active portfolio-management / rebalance layer is the genuinely-hard new surface -- where does self-build end + SmartX-partner begin? (Partnering deepens a vendor dependency we'd be reducing vis-a-vis BD/Orion -- name the tradeoff.)
</the_work>

<acceptance_criteria>
1. Complete SmartX endpoint+structure sweep: all surfaces (identity/core-3.1/performance/legacy-3.0/GraphQL), field/endpoint-level.
2. The partnership-slot map + the build-vs-buy boundary scoped (self-build-vs-partner, with the dependency tradeoff).
3. CVO reconcile-verifies the spec vs the HAR / live SmartX.
4. SPEC only -- no build. RAVC2 COO + CTO.
</acceptance_criteria>
