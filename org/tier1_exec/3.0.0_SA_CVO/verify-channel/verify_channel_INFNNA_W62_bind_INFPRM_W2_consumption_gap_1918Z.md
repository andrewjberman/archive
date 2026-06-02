# verify-channel — W6.2 checker W4-binding (CONFIRM) + ADVI_INFPRM.W2 FE-consumption gap (CONDITIONAL)

**archetype:** VALIDATE | **Reviewer:** 3.0.0_SA_CVO | triggered by AE RAVC2-CC (878fd6c8b + c080a8da2; partners-api-v1.16.2)

## (1) W6.2 inf-nna-partition-checker binds my W4 RIGID bar: CONFIRM
Read the checker (infra/aws/lambda/inf-pipeline/inf-nna-partition-checker/lambda_function.py). It binds the DATA-side W4 invariants as a STANDING DAILY re-assertion on the served artifact:
- reconciliation.all_pass + max_abs_delta + series_tie_max_abs_delta <= tolerance_usd (my W6 binding)
- per_window {geo_states_delta, advisors_delta, max_city_vs_state_delta, max_client_vs_advisor_delta} each <= tol = "sum(leaves)==parent" (my I1/I2/I3 partition invariants)
- granularity_coverage floors (n_advisors/n_states_real/n_cities/n_client_leaves) — catches a state/coverage collapse (17->8)
- breach->CW->ops SNS; treat_missing_data=breaching (dead-checker caught); READ_FAILURE_BREACH. AE evidence: real-artifact breach=0, 3 synthetic faults breach=1, AC8 PASS.
SCOPE: this is the DATA-artifact daily re-assertion (partition + W6 + coverage). It does NOT cover I4 cross-view (continuous==snapshot) or AC4 (FE fallback-removal) — those are FE-ship-time properties, correctly out of a daily-artifact checker's scope. Binding MATCHES my W4 data-side bar. The W4 gate is now a standing daily guard — excellent durability add.

## (2) ADVI_INFPRM.W2 FE-consumption gap: CONDITIONAL (config-OK != delivering) — closure-blocker
AE flagged + I independently CONFIRM: the W2 backend (getClientsTab firmId-fallback, my SECURITY PASS) is sound but NOT consumed by the FE for the Clients tab / Firm Overview:
- FE reads clients_tab from the STATIC dashboard.json: ClientsTab.tsx:307 `const ct = dashboardQuery.data?.clients_tab`. NOT getClientsTab.
- Served dashboard.json (s3://opal-data-inf/platinum/firm/dashboard.json): 308 bytes, top keys=[firm_id,firm_name,generated_at,data_as_of,split,headline,ytd]; **clients_tab ABSENT (null)** — emptied by the v10 carve-out.
=> INFPRM Symptom-2 (Firm Overview absent for Peter) is NOT resolved end-to-end by W2 alone — the FE consumes an EMPTY static source, not the W2-fixed Lambda. Textbook ship-attestation-vs-deploy-attestation / config-OK-!=-delivering.

CLOSURE STANCE: INFPRM W1 (regression PASS) + W2 (security PASS) verify the COMPONENTS are correct, but INFPRM is NOT closeable until an RD~C FE rewire makes the Clients tab read the W2-fixed source (getClientsTab) AND it delivers non-empty firm-scoped data — then I re-verify Symptom-2 end-to-end. CONDITIONAL. AE routed detail to COO; RD~C owns the FE rewire.

— 3.0.0_SA_CVO
