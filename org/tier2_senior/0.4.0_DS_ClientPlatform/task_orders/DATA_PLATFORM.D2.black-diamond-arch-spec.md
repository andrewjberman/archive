<to_id>DATA_PLATFORM.D2</to_id>
<project>DATA_PLATFORM</project>
<title>D2 Black Diamond architecture spec -- DataMining template/level/fact model + lots-methodology audit</title>
<assigned_to>0.4.0_DS_ClientPlatform (DS-lead; AE-consult for auth/infra)</assigned_to>
<consult>0.7.0_AE_CloudOps (auth/session/IP-binding/infra)</consult>
<verify>3.0.0_SA_CVO (reconcile-verify spec vs live BD / cot pipeline)</verify>
<issued_by>2.0.0_SA_COO (DATA_PLATFORM Phase-1 decomposition; Andrew-direct via CTO 2026-06-23; PRD S6/S11; LD-0209)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>pending</status>
<!-- SPEC/AUDIT (Phase-1), NOT a build. -->

<objective>
Produce the Black Diamond architecture spec -- how BD aggregates + surfaces custodian data (the model we'd have to replicate/replace to own the aggregation layer). SPEC-OF-RECORD: PRD S6 row D2.
</objective>

<the_work>
The BD DataMining template/level/fact model; the FULL template catalog + every dimension/measure BD exposes; the auth/session/IP-binding model; the lots FIFO-vs-snapshot methodology (the cost-basis/lot-accounting approach). Seeds: cot_bronze_ingest.py + the templates + COTETL_METHODOLOGY_THESIS.md.
</the_work>

<acceptance_criteria>
1. Complete BD arch-spec: the DataMining template/level/fact model + the full template catalog (every dimension/measure).
2. The auth/session/IP-binding model documented.
3. The lots FIFO-vs-snapshot methodology characterized (how BD does cost-basis/lot-accounting).
4. CVO reconcile-verifies the spec vs the live BD / cot pipeline.
5. SPEC only -- no build. RAVC2 COO + CTO.
</acceptance_criteria>
