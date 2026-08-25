<to_id>DATA_PLATFORM.DC1</to_id>
<project>DATA_PLATFORM</project>
<title>Phase-1-DEEP DC1 -- Orion (inf) comprehensive post-auth crawl + endpoint characterization (vendor-1, via the DC0 harness)</title>
<assigned_to>0.7.0_AE_CloudOps (lead -- runs the DC0 harness) + 0.5.0_AE_OpalETL (co -- the Orion-config it's building)</assigned_to>
<consult>0.4.0_DS_ClientPlatform (Orion data-domain / characterization -> feeds DC-REV)</consult>
<verify>3.0.0_SA_CVO (catalog basis-taxonomy + ROE-compliance + isolation-held-during-crawl)</verify>
<arch_gate>1.0.0_SA_CTO -- the DC0.4 LIVE-crawl gate (verifies the BUILT isolation works + ROE-compliance) BEFORE any live crawl</arch_gate>
<issued_by>2.0.0_SA_COO (CTO DC1-3-unblocked 150331Z; Phase-1-DEEP decomposition; Andrew-ratified Recon ROE)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project DATA_PLATFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<!-- GATED on (a) DC0 integration-ready (0.5.0's co-build landing) + (b) the DC0.4 live-crawl arch-gate. Authored now for coverage (CTO unblocked-to-author per the DC0 design arch-GO). Orion = the vendor-1 crawl-target (SmartX = vendor-2 / DC3, post-Orion; BD/cot = REST -> the D2-census, NOT a crawl-target). -->
<!-- RE-SLOT 2026-07-02 (COO, per CTO heads-up 164658Z, Andrew-direct 0.7.0-base->YCharts pivot): SEQUENCED BEHIND the 0.7.0_AE-base YCharts-skill refinement (Andrew-direct priority). Owner UNCHANGED (0.7.0 base lead + 0.5.0 co); base resumes this AFTER ycharts lands. Not 0.7.0~A (it must stay responsive for the bd(a) box-rollout GO during the ETLFIX P0). Recon = not-hot-path (ETLFIX P0 does not depend on it -> no orphan by deferral). CONTINGENCY: if a downstream DATA_PLATFORM need surfaces before ycharts completes, re-route to a live cloud-ops hand at that point. -->
<roe>MANDATORY: complies with docs/architecture/DATA_PLATFORM_RECON_ROE.md (Option-A passive capture + Option-B own-account, within the 4 constraints; careful/stealthy; forbidden-tier HARD-EXCLUDED; CTO rejects-forbidden at the DC0.4 gate).</roe>

<objective>
Comprehensive enumeration + characterization of Orion's (inf) endpoint surface via the DC0 harness post-auth crawl (Orion = vendor-1) -- the FULL surface beyond the 9 used production dimensions, feeding DC-REV (the Orion reverse-ETL -- bounded/INFERRED since no Fidelity-direct feed).
</objective>

<the_work>
Run the DC0 harness against the inf-exporter/Orion authenticated session (offline dry-run first, then DC0.4-gated live): walk every screen/route -> capture every XHR + the enriched-capture (source-maps[high-value] + bundle/header fingerprint) -> bronze->silver->gold catalog -> characterize (call-pattern + what-it-serves + the basis-taxonomy a/b/c). Surface the observed-but-unused frontier (the D3 §14: DataSources/SignalR/Authorization/Reports/Categories). CAREFUL/STEALTHY: hard-isolated from the live-serving pull, human-paced, NEVER burn the serving session (the DC0 isolation core enforces this non-bypassably).
</the_work>

<acceptance_criteria>
1. Comprehensive Orion catalog: full surface + per-endpoint characterization + the observed-but-unused frontier, basis-taxonomy-tagged (a provable / b best-effort / c used-only).
2. Isolation HELD throughout (zero live-serving disruption -- CVO verifies the serving-abort/fail-safe held).
3. ROE-compliant (CVO verifies; CTO rejected-forbidden at the DC0.4 gate).
4. Feeds DC-REV (the Orion reverse-ETL) + the partner-scoring. RAVC2 COO + CTO.
</acceptance_criteria>
