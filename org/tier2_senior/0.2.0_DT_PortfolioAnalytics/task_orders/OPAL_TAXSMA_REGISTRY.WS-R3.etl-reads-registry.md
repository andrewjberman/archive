<task_order>
<to_id>OPAL_TAXSMA_REGISTRY.WS-R3</to_id>
<title>ETL-READS-REGISTRY — replace the WS-1 producer discover_accounts() stub with a registry read (active entries); WS-5 schedule pulls all enrolled daily</title>
<issued_by>1.0.0_SA_CTO</issued_by>
<issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
<date>2026-07-17</date>
<status>pending</status>
<priority>P2 (Andrew-direct via CTO). Small — the producer is DT's (live @opal-assets-v0.27.0). Depends on WS-R1 (the registry exists) + the WS-1 role gaining GetObject on the roster key.</priority>

<authority>
Andrew-direct 2026-07-17 (DT brief @e43e9d0de -> CTO PRD). PRD §3, §5 WS-R3. Fixes the WS-1 defect: discover_accounts() is a stub; the first pull ran hardcoded Chiles.</authority>

<gate>
The producer reads the ACTIVE registry entries only (status=active) each run. D5 coherence: the ad-hoc /tax-newacc run + the daily ETL use the SAME producer + SAME pull_date bronze partitioning -> distinct snapshots, no silent overwrite (WS-1's BD-revision contract holds). NO alert leg (alert-suspension).
</gate>

<scope>
Replace discover_accounts() with a read of s3://opal-data-assets/blackdiamond/49f/_ops/taxsma_roster.json (active entries -> the account set to pull). The WS-5 schedule then pulls performance/costBasis/allocation per enrolled account daily. The WS-1 producer role needs s3:GetObject on the roster key (a 1-line additive grant to the EXISTING opal-assets-bd49f-reporting-pull-role, scoped to the roster key only) — route that grant through the AE apply + CTO note (it is additive + single-key; not a new role). Keep the pull otherwise unchanged (raw bronze 17a, metadata stamped).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before deploy">
    <step>
      <run>Confirm the producer role's GetObject on the roster key (additive) is applied + Rule-22a live-simulated (one --resource-arns on the roster key = allowed; a non-roster _ops key = implicitDeny)</run>
      <expect>Roster read allowed, no widening. comp-iam is necessary-not-sufficient — the live simulate is the truth.</expect>
      <if_mismatch>STOP. The producer can't read the registry -> the ETL can't discover accounts.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>Invoke the producer against a 2-account registry; aws s3 ls the bronze prefix — both accounts' raw JSON present, pull_date-partitioned</run>
      <expect>All ACTIVE registry accounts pulled; raw bronze 17a; no overwrite of a prior pull_date.</expect>
      <if_mismatch>STOP. Fix before signaling WS-2/WS-5.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Depends on WS-R1 (registry substrate). The 1-key additive producer-role grant -> AE applies, CTO notes (additive, single-key, not a WS-R5-class net-new). Feeds WS-5 (schedule) + the WS-2->WS-3 silver/gold chain (all enrolled accounts now flow).
</cross_domain_coordination>

<acceptance_criteria>
1. Producer reads the ACTIVE registry entries (no hardcoded roster remains).
2. Producer role's roster-key GetObject applied + Rule-22a live-verified (allowed on roster key, never-widen negative).
3. Exercised: a multi-account registry -> all active accounts pulled, raw bronze 17a, pull_date-partitioned (D5 no-overwrite).
4. Session log reproduces each mandate run + observed vs expect.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/OPAL_TAXSMA_REGISTRY_PRD.md (§3, §4 D5, §5 WS-R3)</ref>
</references>
</task_order>
