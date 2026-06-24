<to_id>DATA_PLATFORM.D3</to_id>
<project>DATA_PLATFORM</project>
<title>D3 Orion + Eclipse architecture spec -- full REST surface + join model + valuation-lag audit</title>
<assigned_to>0.4.0_DS_ClientPlatform (DS-lead; AE-consult for auth/infra)</assigned_to>
<consult>0.7.0_AE_CloudOps (auth/infra)</consult>
<verify>3.0.0_SA_CVO (reconcile-verify spec vs live inf/Orion pipeline)</verify>
<issued_by>2.0.0_SA_COO (DATA_PLATFORM Phase-1 decomposition; Andrew-direct via CTO 2026-06-23; PRD S6/S11; LD-0209)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>active</status>
<!-- SPEC/AUDIT (Phase-1), NOT a build. GO'd 2026-06-24 (Andrew start-now); CTO scope-confirmed. -->

<objective>
Produce the Orion + Eclipse architecture spec -- the full REST surfaces + the join model + the valuation-lag, so we know what Orion/Eclipse aggregate + the genuinely-hard trade/rebalance surface. SPEC-OF-RECORD: PRD S6 row D3.
</objective>

<the_work>
The FULL Orion REST surface (Portfolio / Trading / Reporting / Envision) + the Eclipse surface (models / portfolios / rebalance) + the join model across them + the valuation-lag (the ~3.4% characterized) -- field-level. Seeds: data/inf/manual_api/README.md + the feasibility briefs.
NOTE (PRD insight #2): the Eclipse-class trade/rebalance layer is the genuinely-hard new surface (reporting is displaceable; active portfolio management is not trivially self-built) -- characterize it so the D5 self-build-vs-partner decision (with D4) is informed.
SCOPE-REFINE (DS orientation 06-24, COO-confirmed): D3 spans THREE distinct surfaces (not just the README's one): (1) Orion Envision/ExcelReports saved-query path (data/inf/manual_api/README.md); (2) Orion Portfolio per-day Assets SNAPSHOT path (INF_B_00.canonical_holdings, PRD S3.3 -- the cleanest snapshot pass-through); (3) Eclipse (www.orioneclipse.com, SEPARATE JWT/ID-space: models/portfolios/rebalance, seed data/inf/scripts/bronze/pull_eclipse_portfolios.py). Deeper seeds: docs/architecture/ADVI_ORIAPI.md (45KB, HAR Appendix A) + go_nogo.md + PATH_DISCOVERY.md. Spec must span all three + the join model + the ~3.4% Orion-vs-Eclipse valuation-lag.
</the_work>

<acceptance_criteria>
1. Complete Orion+Eclipse arch-spec: the full REST surfaces (Portfolio/Trading/Reporting/Envision + Eclipse models/portfolios/rebalance), field-level.
2. The join model across Orion+Eclipse documented.
3. The valuation-lag characterized (the ~3.4%: cause + grain + materiality).
4. CVO reconcile-verifies the spec vs the live inf/Orion pipeline.
5. SPEC only -- no build. RAVC2 COO + CTO.
</acceptance_criteria>
